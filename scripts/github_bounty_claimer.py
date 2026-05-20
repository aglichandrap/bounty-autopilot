from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen


API = "https://api.github.com"
CANDIDATES_PATH = Path("bounty_candidates.json")
STATE_PATH = Path("github_bounty_claim_state.json")
REPORT_PATH = Path("github_bounty_claim_report.md")
MAX_CLAIMS = int(os.environ.get("GITHUB_BOUNTY_MAX_CLAIMS", "1"))
MAX_COMMENTS = int(os.environ.get("GITHUB_BOUNTY_CLAIM_MAX_COMMENTS", "8"))
MIN_CLAIM_AMOUNT = float(os.environ.get("GITHUB_BOUNTY_MIN_CLAIM_AMOUNT", "20"))

CLAIM_COMMENT = (
    "I can take this if it is still available. I will first reproduce the issue, "
    "keep the PR focused, and include a regression test or clear verification notes before asking for review."
)

ASSIGNMENT_COMMENT = (
    "I can work on this if it is still available. Please assign it to me if assignment is required before opening a PR."
)


@dataclass
class ClaimResult:
    title: str
    issue_url: str
    status: str
    comment_url: str = ""
    message: str = ""


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def request_json(path: str, token: str | None = None, method: str = "GET", payload: dict[str, Any] | None = None) -> Any:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
        "User-Agent": "bounty-autopilot-claimer",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(f"{API}{path}", data=data, headers=headers, method=method)
    with urlopen(request, timeout=60) as response:
        text = response.read().decode("utf-8", errors="replace")
    return json.loads(text) if text else {}


def http_error_message(exc: HTTPError) -> str:
    try:
        body = exc.read().decode("utf-8", errors="replace")
    except Exception:
        body = ""
    return f"HTTP {exc.code}: {body or exc.reason}"


def load_candidates() -> list[dict[str, Any]]:
    if not CANDIDATES_PATH.exists():
        return []
    try:
        data = json.loads(CANDIDATES_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def load_state() -> dict[str, Any]:
    if not STATE_PATH.exists():
        return {"claims": {}}
    try:
        state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"claims": {}}
    if not isinstance(state, dict):
        return {"claims": {}}
    state.setdefault("claims", {})
    return state


def parse_issue(url: str) -> tuple[str, int] | None:
    match = re.search(r"github\.com/([^/]+/[^/]+)/issues/(\d+)", url or "")
    if not match:
        return None
    return match.group(1), int(match.group(2))


def amount_value(text: str) -> float:
    best = 0.0
    for match in re.finditer(r"\$\s*([0-9][0-9,]*(?:\.[0-9]+)?)(\s*k)?", text or "", flags=re.I):
        value = float(match.group(1).replace(",", ""))
        if match.group(2):
            value *= 1000
        best = max(best, value)
    for match in re.finditer(r"\b([0-9][0-9,]*(?:\.[0-9]+)?)\s*(usd|usdc)\b", text or "", flags=re.I):
        best = max(best, float(match.group(1).replace(",", "")))
    return best


def text_blob(candidate: dict[str, Any], issue: dict[str, Any]) -> str:
    return " ".join(
        str(value or "")
        for value in (
            candidate.get("title"),
            candidate.get("amount_hint"),
            candidate.get("reason"),
            issue.get("title"),
            issue.get("body"),
            " ".join(str(label.get("name") or "") for label in issue.get("labels", []) if isinstance(label, dict)),
        )
    ).lower()


def has_paid_signal(blob: str) -> bool:
    if "amount not obvious" in blob:
        return False
    return amount_value(blob) >= MIN_CLAIM_AMOUNT


def forbidden(blob: str) -> str:
    patterns = {
        "security-sensitive": r"\b(security|vulnerability|credential|private key|api key|secret)\b",
        "private-access-needed": r"\b(stripe live|vercel|production access|admin access|customer account|private repo)\b",
        "manual-verification-only": r"\b(smoke test|end-to-end smoke|manual verification|verify .* live-mode)\b",
        "spam/deception": r"\b(spam|fake account|referral|airdrop|casino|gambling|trading bot)\b",
        "prompt/context": r"\b(prompt|context|pre_task_context|runtime_instructions)\b",
        "content-only": r"\b(article|blog post|tutorial|content proposal)\b",
    }
    for reason, pattern in patterns.items():
        if re.search(pattern, blob):
            return reason
    return ""


def already_claimed_by_us(comments: list[dict[str, Any]], login: str) -> str:
    for comment in comments:
        if not isinstance(comment, dict):
            continue
        user = comment.get("user") if isinstance(comment.get("user"), dict) else {}
        if str(user.get("login") or "").lower() == login.lower():
            return str(comment.get("html_url") or "")
    return ""


def competition_in_comments(comments: list[dict[str, Any]], login: str) -> str:
    pattern = re.compile(
        r"\b(i can work|i'?m interested in taking|working on this|opened a pr|submitted|raised pr|/claim|/attempt|assign(ed)? me)\b",
        re.I,
    )
    for comment in comments:
        if not isinstance(comment, dict):
            continue
        user = comment.get("user") if isinstance(comment.get("user"), dict) else {}
        author = str(user.get("login") or "")
        if author.lower() == login.lower():
            continue
        if pattern.search(str(comment.get("body") or "")):
            return f"active attempt/comment by {author or 'another user'}"
    return ""


def open_competing_prs(repo: str, issue_number: int, login: str, token: str) -> int:
    query = quote(f"repo:{repo} is:pr is:open {issue_number}")
    payload = request_json(f"/search/issues?q={query}&per_page=10", token)
    count = 0
    for item in payload.get("items", []):
        user = item.get("user") if isinstance(item, dict) and isinstance(item.get("user"), dict) else {}
        if str(user.get("login") or "").lower() != login.lower():
            count += 1
    return count


def select_comment(blob: str) -> str:
    if re.search(r"\bassign(ed|ment)?\b|\bplease assign\b", blob):
        return ASSIGNMENT_COMMENT
    return CLAIM_COMMENT


def claim_candidate(candidate: dict[str, Any], token: str, login: str, state: dict[str, Any]) -> ClaimResult:
    title = str(candidate.get("title") or "Untitled")
    issue_url = str(candidate.get("url") or "")
    parsed = parse_issue(issue_url)
    if not parsed:
        return ClaimResult(title, issue_url, "skipped", message="Not a parseable GitHub issue URL.")
    repo, issue_number = parsed
    if issue_url in state["claims"]:
        return ClaimResult(title, issue_url, "already_recorded", state["claims"][issue_url].get("comment_url", ""), "Already recorded in claim state.")

    issue = request_json(f"/repos/{repo}/issues/{issue_number}", token)
    if issue.get("state") != "open":
        return ClaimResult(title, issue_url, "skipped", message="Issue is not open.")
    if issue.get("pull_request"):
        return ClaimResult(title, issue_url, "skipped", message="This is a pull request, not an issue.")
    assignees = issue.get("assignees") or []
    if assignees:
        return ClaimResult(title, issue_url, "skipped", message="Issue is already assigned.")
    comments_count = int(issue.get("comments") or 0)
    if comments_count > MAX_COMMENTS:
        return ClaimResult(title, issue_url, "skipped", message=f"Issue has too many comments ({comments_count}).")

    blob = text_blob(candidate, issue)
    if not has_paid_signal(blob):
        return ClaimResult(title, issue_url, "skipped", message=f"No claimable paid signal >= ${MIN_CLAIM_AMOUNT:.0f}.")
    reason = forbidden(blob)
    if reason:
        return ClaimResult(title, issue_url, "skipped", message=f"Forbidden/risky category: {reason}.")

    comments = request_json(f"/repos/{repo}/issues/{issue_number}/comments?per_page=50", token)
    comments = comments if isinstance(comments, list) else []
    existing = already_claimed_by_us(comments, login)
    if existing:
        state["claims"][issue_url] = {"comment_url": existing, "updated_at": now_utc(), "status": "already_claimed"}
        return ClaimResult(title, issue_url, "already_claimed", existing, "Existing comment by account found.")
    competition = competition_in_comments(comments, login)
    if competition:
        return ClaimResult(title, issue_url, "skipped", message=competition)
    competing_prs = open_competing_prs(repo, issue_number, login, token)
    if competing_prs > 0:
        return ClaimResult(title, issue_url, "skipped", message=f"Open competing PRs found: {competing_prs}.")

    try:
        comment = request_json(
            f"/repos/{repo}/issues/{issue_number}/comments",
            token,
            method="POST",
            payload={"body": select_comment(blob)},
        )
    except HTTPError as exc:
        return ClaimResult(title, issue_url, "claim_failed", message=http_error_message(exc))
    comment_url = str(comment.get("html_url") or "")
    state["claims"][issue_url] = {"comment_url": comment_url, "updated_at": now_utc(), "status": "claimed"}
    return ClaimResult(title, issue_url, "claimed", comment_url, "Posted cautious availability comment.")


def claim_sort_key(item: dict[str, Any]) -> tuple[float, int]:
    return amount_value(str(item.get("amount_hint") or "")), int(item.get("score") or 0)


def write_report(results: list[ClaimResult], state: dict[str, Any]) -> None:
    state["updated_at"] = now_utc()
    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = ["# GitHub Bounty Claim Report", "", f"Last run: {now_utc()}", ""]
    if not results:
        lines.extend(["No safe claim target was processed.", ""])
    for result in results:
        lines.extend([
            f"## {result.title}", "",
            f"- Issue: {result.issue_url or 'not available'}",
            f"- Status: {result.status}",
            f"- Comment: {result.comment_url or 'not posted'}",
            f"- Message: {result.message or 'ok'}", "",
        ])
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    token = os.environ.get("BOUNTY_GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or ""
    token = token.strip()
    state = load_state()
    if not token:
        write_report([ClaimResult("Configuration missing", "", "blocked", message="BOUNTY_GITHUB_TOKEN/GH_TOKEN is required to comment on GitHub issues.")], state)
        return 0
    try:
        viewer = request_json("/user", token)
    except HTTPError as exc:
        write_report([ClaimResult("GitHub auth failed", "", "blocked", message=http_error_message(exc))], state)
        return 0
    login = str(viewer.get("login") or "")
    candidates = [item for item in load_candidates() if str(item.get("triage_decision") or "keep").lower() == "keep"]
    candidates.sort(key=claim_sort_key, reverse=True)
    results: list[ClaimResult] = []
    claimed = 0
    for candidate in candidates:
        if claimed >= MAX_CLAIMS:
            break
        result = claim_candidate(candidate, token, login, state)
        results.append(result)
        if result.status == "claimed":
            claimed += 1
    write_report(results, state)
    print(f"Processed {len(results)} claim candidates; claimed {claimed}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
