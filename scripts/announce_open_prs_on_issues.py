#!/usr/bin/env python3
"""Post clear issue comments for submitted bounty PRs.

For every open PR authored by this account, parse `Fixes #123` style links from
the PR body. If the linked issue does not already contain this PR URL in a
comment by the account, post a concise implementation announcement.
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

API = "https://api.github.com"
REPORT_PATH = Path("github_pr_issue_announcement_report.md")
TOKEN = (os.environ.get("BOUNTY_GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or "").strip()
MAX_PRS = int(os.environ.get("PR_ANNOUNCER_MAX_PRS", "25"))


@dataclass
class Result:
    pr_url: str
    issue_url: str
    status: str
    comment_url: str = ""
    message: str = ""


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def headers() -> dict[str, str]:
    out = {
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
        "User-Agent": "bounty-autopilot-pr-announcer",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if TOKEN:
        out["Authorization"] = f"Bearer {TOKEN}"
    return out


def request_json(method: str, endpoint_or_url: str, payload: dict[str, Any] | None = None) -> Any:
    url = endpoint_or_url if endpoint_or_url.startswith("https://") else f"{API}{endpoint_or_url}"
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers(), method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {raw or exc.reason}") from exc


def parse_repo_from_api_url(url: str) -> str:
    match = re.search(r"/repos/([^/]+/[^/]+)$", url or "")
    return match.group(1) if match else ""


def parse_issue_refs(body: str, repo: str) -> list[tuple[str, int]]:
    refs: list[tuple[str, int]] = []
    patterns = [
        r"(?:fixes|closes|resolves)\s+#(\d+)",
        r"(?:fixes|closes|resolves)\s+https://github\.com/([^/]+/[^/]+)/issues/(\d+)",
    ]
    for match in re.finditer(patterns[0], body or "", flags=re.I):
        refs.append((repo, int(match.group(1))))
    for match in re.finditer(patterns[1], body or "", flags=re.I):
        refs.append((match.group(1), int(match.group(2))))
    deduped: list[tuple[str, int]] = []
    for ref in refs:
        if ref not in deduped:
            deduped.append(ref)
    return deduped


def compact_section(body: str, heading: str, fallback: str = "") -> list[str]:
    lines = body.splitlines()
    start = -1
    for index, line in enumerate(lines):
        normalized = line.strip().lower().strip(":")
        if normalized.startswith(heading.lower()):
            start = index + 1
            break
    if start == -1:
        return [fallback] if fallback else []
    bullets: list[str] = []
    for line in lines[start:]:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#") or stripped.lower().rstrip(":") in {"verification", "what changed", "summary", "testing"}:
            break
        stripped = re.sub(r"^[-*]\s*", "", stripped)
        if stripped:
            bullets.append(stripped)
        if len(bullets) >= 4:
            break
    return bullets


def build_comment(pr: dict[str, Any], issue_number: int) -> str:
    pr_url = str(pr.get("html_url") or "")
    pr_number = int(pr.get("number") or 0)
    body = str(pr.get("body") or "")
    title = str(pr.get("title") or f"PR #{pr_number}")
    changes = compact_section(body, "What changed", title)
    verification = compact_section(body, "Verification") or compact_section(body, "Testing")

    lines = [
        f"Submitted a focused implementation in PR #{pr_number}: {pr_url}",
        "",
        "What changed:",
    ]
    for item in changes[:4]:
        lines.append(f"- {item}")
    if verification:
        lines.extend(["", "Verification:"])
        for item in verification[:3]:
            lines.append(f"- {item}")
    lines.extend([
        "",
        "I will watch for review feedback and adjust the PR if the maintainer asks for changes.",
    ])
    return "\n".join(lines)


def already_announced(repo: str, issue_number: int, login: str, pr_url: str) -> bool:
    comments = request_json("GET", f"/repos/{repo}/issues/{issue_number}/comments?per_page=100")
    if not isinstance(comments, list):
        return False
    for comment in comments:
        user = comment.get("user") if isinstance(comment, dict) else {}
        author = str(user.get("login") or "") if isinstance(user, dict) else ""
        body = str(comment.get("body") or "") if isinstance(comment, dict) else ""
        if author.lower() == login.lower() and pr_url in body:
            return True
    return False


def open_prs(login: str) -> list[dict[str, Any]]:
    query = urllib.parse.quote(f"author:{login} is:pr is:open archived:false")
    data = request_json("GET", f"/search/issues?q={query}&sort=updated&order=desc&per_page={MAX_PRS}")
    items = data.get("items", []) if isinstance(data, dict) else []
    prs: list[dict[str, Any]] = []
    for item in items:
        if not isinstance(item, dict) or "pull_request" not in item:
            continue
        repo = parse_repo_from_api_url(str(item.get("repository_url") or ""))
        pr_number = int(item.get("number") or 0)
        if not repo or not pr_number:
            continue
        try:
            prs.append(request_json("GET", f"/repos/{repo}/pulls/{pr_number}"))
        except RuntimeError:
            continue
    return prs


def process() -> list[Result]:
    if not TOKEN:
        return [Result("", "", "blocked", message="BOUNTY_GITHUB_TOKEN/GH_TOKEN/GITHUB_TOKEN is required.")]
    viewer = request_json("GET", "/user")
    login = str(viewer.get("login") or "")
    results: list[Result] = []
    for pr in open_prs(login):
        repo = parse_repo_from_api_url(str(pr.get("base", {}).get("repo", {}).get("url", "")))
        if not repo:
            base_repo = pr.get("base", {}).get("repo", {}) if isinstance(pr.get("base"), dict) else {}
            repo = str(base_repo.get("full_name") or "") if isinstance(base_repo, dict) else ""
        pr_url = str(pr.get("html_url") or "")
        refs = parse_issue_refs(str(pr.get("body") or ""), repo)
        if not refs:
            results.append(Result(pr_url, "", "skipped", message="PR body has no Fixes/Closes/Resolves issue reference."))
            continue
        for issue_repo, issue_number in refs:
            issue_url = f"https://github.com/{issue_repo}/issues/{issue_number}"
            try:
                if already_announced(issue_repo, issue_number, login, pr_url):
                    results.append(Result(pr_url, issue_url, "already_announced", message="Matching issue comment already exists."))
                    continue
                comment = request_json(
                    "POST",
                    f"/repos/{issue_repo}/issues/{issue_number}/comments",
                    {"body": build_comment(pr, issue_number)},
                )
                results.append(Result(pr_url, issue_url, "commented", str(comment.get("html_url") or "")))
            except RuntimeError as exc:
                results.append(Result(pr_url, issue_url, "comment_failed", message=str(exc)))
    return results


def write_report(results: list[Result]) -> None:
    lines = ["# GitHub PR Issue Announcement Report", "", f"Last run: {now_utc()}", ""]
    if not results:
        lines.extend(["No open PR announcements were needed.", ""])
    for result in results:
        lines.extend([
            f"## {result.status}",
            "",
            f"- PR: {result.pr_url or 'not available'}",
            f"- Issue: {result.issue_url or 'not available'}",
            f"- Comment: {result.comment_url or 'not posted'}",
            f"- Message: {result.message or 'ok'}",
            "",
        ])
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    results = process()
    write_report(results)
    print(f"Processed {len(results)} PR announcement targets.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
