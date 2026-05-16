from __future__ import annotations

import html
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


BASE_URL = os.environ.get("TASKBOUNTY_BASE_URL", "https://www.task-bounty.com").rstrip("/")
TASKS_API_URL = f"{BASE_URL}/api/v1/tasks"
BROWSE_URL = f"{BASE_URL}/browse"

TASKS_PATH = "taskbounty_tasks.json"
REPORT_PATH = "taskbounty_report.md"


@dataclass
class TaskBountyCandidate:
    title: str
    url: str
    task_id: str
    amount_hint: str
    score: int
    source: str
    reason: str


def http_get(url: str, token: str | None = None, accept: str = "application/json") -> str:
    headers = {
        "Accept": accept,
        "User-Agent": "bounty-autopilot-taskbounty-scout",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(url, headers=headers)
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="replace")


def clean_text(value: str) -> str:
    value = html.unescape(value or "")
    value = re.sub(r"<[^>]+>", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def amount_from_cents(value: Any) -> str:
    try:
        cents = int(value)
    except (TypeError, ValueError):
        return "amount not obvious"
    dollars = cents / 100
    if dollars.is_integer():
        return f"${int(dollars)}"
    return f"${dollars:.2f}"


def task_url(task: dict[str, Any]) -> str:
    for key in ("url", "task_url", "public_url"):
        value = task.get(key)
        if isinstance(value, str) and value:
            return value if value.startswith("http") else f"{BASE_URL}{value}"
    slug = task.get("slug")
    if isinstance(slug, str) and slug:
        return f"{BASE_URL}/task/{slug}"
    task_id = str(task.get("id") or task.get("task_id") or "")
    return f"{BASE_URL}/browse#{task_id}" if task_id else BROWSE_URL


def score_task(title: str, amount_hint: str, task: dict[str, Any] | None = None) -> tuple[int, str]:
    text = f"{title} {json.dumps(task or {}, ensure_ascii=False)}".lower()
    score = 40
    reasons = ["TaskBounty paid task"]

    if re.search(r"\bclosed\b|\bcompleted\b|\bpaid\b|\bexpired\b", text):
        return -100, "skip: task is not open"

    amount_match = re.search(r"\$(\d+(?:\.\d+)?)", amount_hint)
    if amount_match:
        amount = float(amount_match.group(1))
        if amount >= 25:
            score += 25
            reasons.append("visible funded amount")
        if amount > 150:
            score -= 15
            reasons.append("larger scope")

    for keyword in ("bug", "fix", "test", "regression", "typescript", "python"):
        if keyword in text:
            score += 5

    for keyword in ("security", "abuse", "spam", "casino", "trading", "prompt", "context"):
        if keyword in text:
            score -= 60
            reasons.append(f"blocked risk keyword: {keyword}")

    attempts = task.get("attempts") if task else None
    try:
        attempts_count = int(attempts)
    except (TypeError, ValueError):
        attempts_count = None
    if attempts_count == 0:
        score += 15
        reasons.append("no attempts shown")
    elif attempts_count and attempts_count > 1:
        score -= 20
        reasons.append("contested")

    return score, ", ".join(reasons[:5])


def candidates_from_api(token: str | None) -> list[TaskBountyCandidate]:
    try:
        payload = json.loads(http_get(TASKS_API_URL, token=token))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        print(f"TaskBounty API read failed: {exc}", file=sys.stderr)
        return []

    items = payload.get("data", payload) if isinstance(payload, dict) else payload
    if not isinstance(items, list):
        return []

    candidates: list[TaskBountyCandidate] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        title = clean_text(str(item.get("title") or item.get("name") or "Untitled TaskBounty task"))
        amount_hint = amount_from_cents(
            item.get("bounty_cents")
            or item.get("amount_cents")
            or item.get("reward_cents")
            or item.get("bounty")
        )
        score, reason = score_task(title, amount_hint, item)
        if score < 25:
            continue
        task_id = str(item.get("id") or item.get("task_id") or item.get("slug") or "")
        candidates.append(
            TaskBountyCandidate(
                title=title,
                url=task_url(item),
                task_id=task_id,
                amount_hint=amount_hint,
                score=score,
                source="api",
                reason=reason,
            )
        )
    return candidates


def candidates_from_browse_page() -> list[TaskBountyCandidate]:
    try:
        page = http_get(BROWSE_URL, accept="text/html")
    except (HTTPError, URLError, TimeoutError) as exc:
        print(f"TaskBounty browse read failed: {exc}", file=sys.stderr)
        return []

    candidates: list[TaskBountyCandidate] = []
    seen: set[str] = set()
    link_pattern = re.compile(r'href="(?P<href>/task/[^"]+)"[^>]*>(?P<body>.*?)</a>', re.I | re.S)
    for match in link_pattern.finditer(page):
        href = html.unescape(match.group("href"))
        if href in seen:
            continue
        seen.add(href)
        raw_body = match.group("body")
        body = clean_text(raw_body)
        if re.search(r"\bclosed\b|\bcompleted\b|\bpaid\b|\bexpired\b", body, flags=re.I):
            continue
        heading_match = re.search(r"<h3[^>]*>(?P<title>.*?)</h3>", raw_body, re.I | re.S)
        heading = clean_text(heading_match.group("title")) if heading_match else ""
        amount_match = re.search(r"\$\s?\d+(?:\.\d+)?", body)
        amount_hint = amount_match.group(0).replace(" ", "") if amount_match else "amount not obvious"
        title = heading or body
        if amount_match and not heading:
            title = clean_text(body[: amount_match.start()])
        score, reason = score_task(title, amount_hint)
        if score < 25:
            continue
        candidates.append(
            TaskBountyCandidate(
                title=title or "TaskBounty task",
                url=f"{BASE_URL}{href}",
                task_id=href.rsplit("/", 1)[-1],
                amount_hint=amount_hint,
                score=score,
                source="browse",
                reason=reason,
            )
        )

    if not candidates:
        text = clean_text(page)
        coarse = re.search(r"(Bug: .*?\$\s?\d+(?:\.\d+)?)", text)
        if coarse and not re.search(r"\bclosed\b|\bcompleted\b|\bpaid\b|\bexpired\b", coarse.group(1), flags=re.I):
            body = coarse.group(1)
            amount_match = re.search(r"\$\s?\d+(?:\.\d+)?", body)
            amount_hint = amount_match.group(0).replace(" ", "") if amount_match else "amount not obvious"
            title = clean_text(body[: amount_match.start()]) if amount_match else clean_text(body)
            score, reason = score_task(title, amount_hint)
            candidates.append(
                TaskBountyCandidate(
                    title=title,
                    url=BROWSE_URL,
                    task_id="browse-detected",
                    amount_hint=amount_hint,
                    score=score,
                    source="browse-text",
                    reason=reason,
                )
            )
    return candidates


def write_outputs(candidates: list[TaskBountyCandidate]) -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    candidates = sorted(candidates, key=lambda item: item.score, reverse=True)[:10]

    with open(TASKS_PATH, "w", encoding="utf-8") as handle:
        json.dump([asdict(candidate) for candidate in candidates], handle, indent=2, ensure_ascii=False)
        handle.write("\n")

    lines = [
        "# TaskBounty Scout",
        "",
        f"Last run: {now}",
        "",
        "This report tracks TaskBounty tasks because they are designed for AI coding agents and pay only after verified accepted work.",
        "",
        f"Mode: {'agent API enabled' if os.environ.get('TASKBOUNTY_API_KEY') else 'public browse fallback only'}",
        "",
    ]
    if not candidates:
        lines.extend(
            [
                "No actionable TaskBounty task was visible in this run.",
                "",
                "If API credentials are not configured, add `TASKBOUNTY_API_KEY` and `TASKBOUNTY_AGENT_ID` as repository secrets.",
                "",
            ]
        )
    for index, candidate in enumerate(candidates, start=1):
        lines.extend(
            [
                f"## {index}. {candidate.title}",
                "",
                f"- Amount hint: {candidate.amount_hint}",
                f"- Score: {candidate.score}",
                f"- Task: {candidate.url}",
                f"- Task ID: {candidate.task_id or 'not exposed'}",
                f"- Source: {candidate.source}",
                f"- Why it matched: {candidate.reason}",
                "- Next action: attempt only if access is available, the task is still open, and the fix can include a regression test.",
                "",
            ]
        )

    with open(REPORT_PATH, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))


def main() -> int:
    token = os.environ.get("TASKBOUNTY_API_KEY")
    candidates = candidates_from_api(token=token)
    if not candidates:
        candidates = candidates_from_browse_page()
    write_outputs(candidates)
    print(f"Wrote {len(candidates)} TaskBounty candidates.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
