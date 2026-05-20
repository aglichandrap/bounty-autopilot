from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CANDIDATES_PATH = Path("bounty_candidates.json")
REPORT_PATH = Path("github_openai_patch_solver_report.md")
MAX_TASKS = int(os.environ.get("GITHUB_SOLVER_MAX_TASKS", "3"))


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def has_online_model_key() -> bool:
    return bool(
        os.environ.get("OPENAI_API_KEY")
        or os.environ.get("OPENROUTER_API_KEY")
        or (os.environ.get("SOLVER_API_KEY") and os.environ.get("SOLVER_BASE_URL"))
    )


def parse_issue(url: str) -> tuple[str, int] | None:
    match = re.search(r"github\.com/([^/]+/[^/]+)/issues/(\d+)", url or "")
    if not match:
        return None
    return match.group(1), int(match.group(2))


def repo_from_url(url: str) -> str:
    match = re.search(r"github\.com/([^/]+/[^/#?]+)", url or "")
    return match.group(1) if match else ""


def load_candidates() -> list[dict[str, Any]]:
    if not CANDIDATES_PATH.exists():
        return []
    try:
        data = json.loads(CANDIDATES_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def is_local_fallback_candidate(item: dict[str, Any]) -> bool:
    decision = str(item.get("triage_decision") or "keep").lower()
    if decision in {"drop", "blocked", "crowded", "hard"}:
        return False
    issue_url = str(item.get("url") or "")
    return parse_issue(issue_url) is not None


def write_local_fallback_report(candidates: list[dict[str, Any]]) -> None:
    lines = [
        "# GitHub OpenAI Patch Solver",
        "",
        f"Last run: {now_utc()}",
        "",
        "No online model key is configured, so GitHub Actions did not attempt code generation.",
        "Eligible candidates were queued for the local Codex solver instead of marking the run as failed.",
        "",
    ]
    if not candidates:
        lines.extend([
            "No eligible GitHub bounty candidates were available for local fallback.",
            "",
        ])
    for index, item in enumerate(candidates[:MAX_TASKS], 1):
        issue_url = str(item.get("url") or "")
        parsed = parse_issue(issue_url)
        repo = repo_from_url(str(item.get("repository_url") or "")) or (parsed[0] if parsed else "")
        title = str(item.get("title") or issue_url or "Untitled")
        lines.extend([
            f"## {index}. {title}",
            "",
            "- Status: local_fallback_queued",
            f"- Repository: {repo or 'not available'}",
            f"- Issue: {issue_url or 'not available'}",
            "- Patch: not ready",
            "- Metadata: not ready",
            "- Message: Online model key missing; local Codex automation should inspect, patch, test, and prepare submission metadata.",
            "",
        ])
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    if has_online_model_key():
        completed = subprocess.run([sys.executable, "scripts/github_openai_patch_solver.py"], check=False)
        return completed.returncode
    candidates = [item for item in load_candidates() if is_local_fallback_candidate(item)]
    write_local_fallback_report(candidates)
    print(f"Queued {min(len(candidates), MAX_TASKS)} GitHub bounty candidates for local Codex fallback.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
