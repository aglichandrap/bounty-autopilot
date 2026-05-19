from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote
from urllib.request import Request, urlopen


TASKS_PATH = Path("taskbounty_tasks.json")
REPORT_PATH = Path("taskbounty_triage_report.md")
GITHUB_API = "https://api.github.com"


@dataclass
class TriageResult:
    task_id: str
    title: str
    issue_url: str
    repository_url: str
    decision: str
    score_adjustment: int
    reasons: list[str]
    linked_prs: list[str]


def github_get(path_or_url: str, token: str | None = None) -> Any:
    url = path_or_url if path_or_url.startswith("https://") else f"{GITHUB_API}{path_or_url}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "bounty-autopilot-taskbounty-triage",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(url, headers=headers)
    with urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def parse_issue_url(url: str) -> tuple[str, int] | None:
    match = re.search(r"https://github\.com/([^/]+/[^/]+)/issues/(\d+)", url)
    if not match:
        return None
    return match.group(1), int(match.group(2))


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def search_linked_prs(repo: str, issue_number: int, title: str, token: str | None) -> list[str]:
    title_terms = " ".join(re.findall(r"[A-Za-z0-9_+-]{4,}", title)[:4])
    queries = [
        f"repo:{repo} is:pr {issue_number}",
        f"repo:{repo} is:pr {quote(title_terms)}" if title_terms else "",
    ]
    urls: list[str] = []
    seen: set[str] = set()
    for query in queries:
        if not query:
            continue
        try:
            payload = github_get(f"/search/issues?q={quote(query)}&per_page=5", token=token)
        except Exception as exc:
            print(f"PR search failed for {repo}#{issue_number}: {exc}", file=sys.stderr)
            continue
        for item in payload.get("items", []):
            url = item.get("html_url")
            if isinstance(url, str) and url not in seen:
                seen.add(url)
                urls.append(url)
    return urls


def triage_task(task: dict[str, Any], token: str | None) -> tuple[dict[str, Any], TriageResult]:
    title = clean(str(task.get("title") or "Untitled TaskBounty task"))
    issue_url = clean(str(task.get("github_issue_url") or ""))
    repo_url = clean(str(task.get("github_repo_url") or ""))
    reasons: list[str] = []
    linked_prs: list[str] = []
    decision = "candidate"
    score_adjustment = 0

    parsed = parse_issue_url(issue_url)
    if not parsed:
        decision = "blocked"
        score_adjustment -= 60
        reasons.append("no GitHub issue URL exposed")
    else:
        repo, issue_number = parsed
        try:
            issue = github_get(f"/repos/{repo}/issues/{issue_number}", token=token)
            labels = {label.get("name", "").lower() for label in issue.get("labels", []) if isinstance(label, dict)}
            comments_count = int(issue.get("comments") or 0)
            body = clean(str(issue.get("body") or ""))
            text = f"{title} {body} {' '.join(labels)}".lower()
            linked_prs = search_linked_prs(repo, issue_number, title, token=token)

            if issue.get("state") != "open":
                decision = "blocked"
                score_adjustment -= 100
                reasons.append("GitHub issue is not open")
            if comments_count > 100:
                score_adjustment -= 40
                reasons.append(f"very busy issue thread ({comments_count} comments)")
            elif comments_count > 20:
                score_adjustment -= 20
                reasons.append(f"busy issue thread ({comments_count} comments)")
            else:
                score_adjustment += 10
                reasons.append("low discussion volume")

            if {"upstream", "electron"} & labels:
                score_adjustment -= 50
                reasons.append("likely upstream platform issue")
            if "security" in labels or "security" in text:
                score_adjustment -= 20
                reasons.append("security-sensitive scope")

            if linked_prs:
                score_adjustment -= 70
                reasons.append(f"linked or competing PRs found ({len(linked_prs)})")

            try:
                comments = github_get(f"/repos/{repo}/issues/{issue_number}/comments?per_page=30", token=token)
            except Exception:
                comments = []
            comments_text = " ".join(clean(str(comment.get("body") or "")) for comment in comments if isinstance(comment, dict)).lower()
            if re.search(r"\bopened\s+(?:a\s+)?(?:focused\s+)?(?:fix\s+)?(?:pr|pull request)\b|#\d+\s+for\s+this\s+path|opened\s+#\d+", comments_text):
                score_adjustment -= 70
                reasons.append("comments indicate a competing PR already exists")

            if decision == "candidate" and score_adjustment <= -60:
                decision = "crowded"
            if decision == "candidate" and score_adjustment <= -40:
                decision = "hard"
            if decision == "candidate" and score_adjustment >= 0:
                reasons.append("still worth solver inspection")
        except Exception as exc:
            decision = "unknown"
            score_adjustment -= 10
            reasons.append(f"GitHub triage failed: {exc}")

    updated = dict(task)
    updated["triage_decision"] = decision
    updated["triage_score_adjustment"] = score_adjustment
    updated["triage_reasons"] = reasons
    updated["linked_prs"] = linked_prs
    updated["score"] = int(updated.get("score") or 0) + score_adjustment

    return updated, TriageResult(
        task_id=str(task.get("task_id") or ""),
        title=title,
        issue_url=issue_url,
        repository_url=repo_url,
        decision=decision,
        score_adjustment=score_adjustment,
        reasons=reasons,
        linked_prs=linked_prs,
    )


def load_tasks() -> list[dict[str, Any]]:
    if not TASKS_PATH.exists():
        return []
    try:
        data = json.loads(TASKS_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def write_report(results: list[TriageResult]) -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# TaskBounty Triage",
        "",
        f"Last run: {now}",
        "",
        "This report filters scouted TaskBounty tasks before solver time is spent.",
        "",
    ]
    if not results:
        lines.extend(["No TaskBounty tasks were available to triage.", ""])
    for index, result in enumerate(results, start=1):
        lines.extend(
            [
                f"## {index}. {result.title}",
                "",
                f"- Decision: {result.decision}",
                f"- Score adjustment: {result.score_adjustment}",
                f"- Issue: {result.issue_url or 'not available'}",
                f"- Repository: {result.repository_url or 'not available'}",
            ]
        )
        for reason in result.reasons:
            lines.append(f"- Reason: {reason}")
        for pr_url in result.linked_prs[:5]:
            lines.append(f"- Linked PR: {pr_url}")
        lines.append("")
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    token = os.environ.get("GITHUB_TOKEN")
    tasks = load_tasks()
    updated: list[dict[str, Any]] = []
    results: list[TriageResult] = []
    for task in tasks:
        triaged, result = triage_task(task, token=token)
        updated.append(triaged)
        results.append(result)
    updated = sorted(updated, key=lambda item: item.get("score", 0), reverse=True)
    TASKS_PATH.write_text(json.dumps(updated, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_report(results)
    print(f"Triaged {len(results)} TaskBounty tasks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
