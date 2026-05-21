from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TASKS_PATH = Path("taskbounty_tasks.json")
REPORT_PATH = Path("openai_patch_solver_report.md")
MAX_TASKS = int(os.environ.get("TASKBOUNTY_SOLVER_MAX_TASKS", "3"))


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def has_online_model_key() -> bool:
    return bool(os.environ.get("OPENAI_API_KEY"))


def load_tasks() -> list[dict[str, Any]]:
    if not TASKS_PATH.exists():
        return []
    try:
        data = json.loads(TASKS_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def is_local_fallback_task(item: dict[str, Any]) -> bool:
    decision = str(item.get("triage_decision") or "").lower()
    if decision in {"blocked"}:
        return False
    status = str(item.get("status") or "").upper()
    return status in {"", "OPEN", "AVAILABLE"}


def write_local_fallback_report(tasks: list[dict[str, Any]]) -> None:
    lines = [
        "# OpenAI Patch Solver",
        "",
        f"Last run: {now_utc()}",
        "",
        "This solver tries to turn a clear public TaskBounty GitHub issue into a ready patch file for the TaskBounty worker.",
        "",
        "No online model key is configured, so GitHub Actions did not attempt code generation.",
        "Eligible tasks were queued for the local Codex solver instead of marking the run as failed.",
        "",
    ]
    if not tasks:
        lines.extend([
            "No eligible TaskBounty tasks were available for local fallback.",
            "",
        ])
    for index, item in enumerate(tasks[:MAX_TASKS], 1):
        title = str(item.get("title") or item.get("url") or "Untitled")
        lines.extend([
            f"## {index}. {title}",
            "",
            "- Status: local_fallback_queued",
            f"- Task ID: {item.get('task_id') or 'not available'}",
            f"- Repo: {item.get('github_repo_url') or 'not available'}",
            f"- Issue: {item.get('github_issue_url') or item.get('url') or 'not available'}",
            "- Patch: not ready",
            "- Message: Online model key missing; local Codex automation should request access if needed, inspect, patch, test, and prepare the submission.",
            "",
        ])
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    if has_online_model_key():
        completed = subprocess.run([sys.executable, "scripts/openai_patch_solver.py"], check=False)
        return completed.returncode
    tasks = [item for item in load_tasks() if is_local_fallback_task(item)]
    write_local_fallback_report(tasks)
    print(f"Queued {min(len(tasks), MAX_TASKS)} TaskBounty tasks for local Codex fallback.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
