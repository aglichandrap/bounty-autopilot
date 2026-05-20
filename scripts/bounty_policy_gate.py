from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote
from urllib.request import Request, urlopen


CANDIDATES_PATH = Path("bounty_candidates.json")
REPORT_PATH = Path("bounty_policy_gate_report.md")
GITHUB_API = "https://api.github.com"

BLOCK_PATTERNS = [
    (re.compile(r"~~[^~]*(?:bounty|reward|paid)[^~]*~~", re.I), "paid bounty text is struck through"),
    (re.compile(r"\bbefore\s+llms?\b", re.I), "bounty terms changed because it predates LLMs"),
    (re.compile(r"\bllm\s+pr\b|\bllm-generated\b|\bai-generated\b", re.I), "LLM/AI contribution terms require human review before work"),
    (re.compile(r"\bhuman-to-human\b|\bhuman-to-claw\b|\bhuman relationship\b", re.I), "maintainer requires a human relationship before accepting work"),
    (re.compile(r"\bjoin\s+(?:our\s+)?slack\b|\blet us know\s+they'?re interested\b", re.I), "maintainer asks contributors to coordinate in Slack before working"),
    (re.compile(r"\bvolunteer\b.{0,80}\bjoin\b", re.I), "volunteer-only or coordination-first task"),
]


def github_get(path_or_url: str, token: str | None = None) -> Any:
    url = path_or_url if path_or_url.startswith("https://") else f"{GITHUB_API}{path_or_url}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "bounty-autopilot-policy-gate",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(url, headers=headers)
    with urlopen(request, timeout=30) as response:
        raw = response.read().decode("utf-8", errors="replace")
    return json.loads(raw) if raw else {}


def parse_issue_url(url: str) -> tuple[str, int] | None:
    match = re.search(r"https://github\.com/([^/]+/[^/]+)/issues/(\d+)", url or "")
    if not match:
        return None
    return match.group(1), int(match.group(2))


def load_candidates() -> list[dict[str, Any]]:
    if not CANDIDATES_PATH.exists():
        return []
    try:
        data = json.loads(CANDIDATES_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def policy_reasons(issue_text: str) -> list[str]:
    reasons: list[str] = []
    for pattern, reason in BLOCK_PATTERNS:
        if pattern.search(issue_text):
            reasons.append(reason)
    return reasons


def main() -> int:
    token = os.environ.get("GITHUB_TOKEN")
    kept: list[dict[str, Any]] = []
    dropped: list[tuple[dict[str, Any], list[str]]] = []
    errors: list[str] = []

    for candidate in load_candidates():
        parsed = parse_issue_url(str(candidate.get("url") or ""))
        if not parsed:
            kept.append(candidate)
            continue
        repo, issue_number = parsed
        try:
            issue = github_get(f"/repos/{repo}/issues/{issue_number}", token=token)
        except Exception as exc:
            errors.append(f"{candidate.get('url')}: {exc}")
            kept.append(candidate)
            continue
        labels = " ".join(str(label.get("name") or "") for label in issue.get("labels", []) if isinstance(label, dict))
        issue_text = "\n".join(
            str(value or "")
            for value in (
                candidate.get("title"),
                candidate.get("reason"),
                candidate.get("amount_hint"),
                labels,
                issue.get("title"),
                issue.get("body"),
            )
        )
        reasons = policy_reasons(issue_text)
        if reasons:
            candidate = dict(candidate)
            candidate["policy_gate_decision"] = "drop"
            candidate["policy_gate_reasons"] = reasons
            dropped.append((candidate, reasons))
        else:
            kept.append(candidate)

    CANDIDATES_PATH.write_text(json.dumps(kept, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Bounty Policy Gate",
        "",
        f"Last run: {now}",
        "",
        f"Kept candidates: {len(kept)}",
        f"Dropped candidates: {len(dropped)}",
        "",
        "This gate removes opportunities whose issue text says the bounty is withdrawn, LLM/AI-ineligible, or requires human coordination before autonomous work.",
        "",
    ]
    for index, (candidate, reasons) in enumerate(dropped, start=1):
        lines.extend([
            f"## {index}. {candidate.get('title') or 'Untitled'}",
            "",
            f"- Issue: {candidate.get('url')}",
        ])
        for reason in reasons:
            lines.append(f"- Reason: {reason}")
        lines.append("")
    if errors:
        lines.extend(["## Inspection Errors", ""])
        for error in errors:
            lines.append(f"- {error}")
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Policy gate kept {len(kept)} candidates and dropped {len(dropped)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
