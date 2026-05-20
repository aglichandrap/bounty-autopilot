from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CANDIDATES_PATH = Path("bounty_candidates.json")
REPORT_PATH = Path("bounty_repo_filter_report.md")

DEFAULT_BLOCKED_REPOS = {
    # Synthetic/fake bounty feed that repeatedly advertises large dollar amounts
    # but resolves to no-paid/free-only issues after triage.
    "orchestration-agent/AgentOrchestration",
    # The autopilot's own tracking issue can match bounty searches; never work it.
    "asaadnashed/bounty-autopilot",
}


def blocked_repos() -> set[str]:
    repos = set(DEFAULT_BLOCKED_REPOS)
    extra = os.environ.get("BOUNTY_BLOCKED_REPOS", "")
    for item in re.split(r"[,\n]", extra):
        item = item.strip()
        if item:
            repos.add(item)
    return repos


def repo_from_candidate(candidate: dict[str, Any]) -> str:
    for key in ("repository_full_name", "repo", "repository"):
        value = str(candidate.get(key) or "").strip()
        if re.match(r"^[^/]+/[^/]+$", value):
            return value
    for key in ("repository_url", "url", "issue"):
        value = str(candidate.get(key) or "")
        match = re.search(r"github\.com/([^/]+/[^/]+)", value)
        if match:
            return match.group(1)
    return ""


def load_candidates() -> list[dict[str, Any]]:
    if not CANDIDATES_PATH.exists():
        return []
    try:
        data = json.loads(CANDIDATES_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def main() -> int:
    candidates = load_candidates()
    blocked = blocked_repos()
    kept: list[dict[str, Any]] = []
    dropped: list[tuple[dict[str, Any], str]] = []

    for candidate in candidates:
        repo = repo_from_candidate(candidate)
        if repo in blocked:
            dropped.append((candidate, repo))
        else:
            kept.append(candidate)

    CANDIDATES_PATH.write_text(json.dumps(kept, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Bounty Repository Filter",
        "",
        f"Last run: {now}",
        "",
        f"Input candidates: {len(candidates)}",
        f"Kept candidates: {len(kept)}",
        f"Dropped candidates: {len(dropped)}",
        "",
        "This filter removes known false-positive or self-tracking repositories before expensive triage/solver work runs.",
        "",
    ]
    if dropped:
        lines.append("## Dropped")
        lines.append("")
        for index, (candidate, repo) in enumerate(dropped[:50], start=1):
            title = candidate.get("title") or "Untitled"
            url = candidate.get("url") or ""
            lines.extend([
                f"### {index}. {title}",
                "",
                f"- Repository: {repo}",
                f"- Issue: {url}",
                "- Reason: known false-positive bounty source",
                "",
            ])
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Repo filter kept {len(kept)} candidates and dropped {len(dropped)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
