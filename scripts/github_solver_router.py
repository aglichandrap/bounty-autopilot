from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

import github_openai_patch_solver


REPORT_PATH = Path("github_openai_patch_solver_report.md")
CANDIDATES_PATH = Path("bounty_candidates.json")


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def online_model_ready() -> bool:
    return bool(
        os.environ.get("OPENAI_API_KEY")
        or os.environ.get("OPENROUTER_API_KEY")
        or (os.environ.get("SOLVER_API_KEY") and os.environ.get("SOLVER_BASE_URL"))
    )


def load_top_candidate() -> dict:
    if not CANDIDATES_PATH.exists():
        return {}
    try:
        data = json.loads(CANDIDATES_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    if not isinstance(data, list):
        return {}
    for item in data:
        if isinstance(item, dict) and str(item.get("triage_decision") or "keep").lower() == "keep":
            return item
    return {}


def write_local_fallback_report() -> None:
    item = load_top_candidate()
    title = str(item.get("title") or "No candidate ready")
    issue = str(item.get("url") or "not available")
    repo = str(item.get("repository_url") or "not available")
    lines = [
        "# GitHub OpenAI Patch Solver",
        "",
        f"Last run: {now_utc()}",
        "",
        f"## 1. {title}",
        "",
        "- Status: local_fallback_queued",
        f"- Repository: {repo}",
        f"- Issue: {issue}",
        "- Patch: not ready",
        "- Metadata: not ready",
        "- Message: No online model key is configured. This is not a hard failure: the opportunity is queued for the local Codex solver automation.",
        "",
    ]
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    if online_model_ready():
        return github_openai_patch_solver.main()
    write_local_fallback_report()
    print("No online model key; queued GitHub solver work for local Codex fallback.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
