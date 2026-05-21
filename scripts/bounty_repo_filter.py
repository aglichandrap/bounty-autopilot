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
    # Repeatedly asks contributors to attach hidden session/pre-task context files.
    # Those requests are not safe to satisfy and crowd the worker queue.
    "UnsafeLabs/Bounty-Hunters",
    # Public repo only contains generated docs/screenshots, not the H5 app source
    # needed to fix the advertised bug bounties.
    "LeoVeeNetVip/team-docs",
    # High-value-looking Solidity bounties ask contributors to paste the full
    # platform-provided instructions/session-start text into source files.
    "ClankerNation/OpenAgents",
}

DEFAULT_BLOCKED_ISSUES = {
    # CAL-3105 is a real bounty, but the thread has many prior attempts and
    # active/open PRs for the same BigBlueButton integration. Keep Codex time
    # for less-crowded work instead of burning a full local implementation here.
    "https://github.com/calcom/cal.com/issues/1985",
    "https://github.com/calcom/cal.diy/issues/1985",
    # Algora #238 is a real paid UI bug, but the thread is already crowded and
    # has prior fixing PRs (#248 and #282). Avoid duplicate claim/solver work.
    "https://github.com/algora-io/algora/issues/238",
    # Liberdus #274 looks high-value, but already has an active /attempt before
    # our claim. Avoid spending local Codex on a likely duplicate UI PR.
    "https://github.com/Liberdus/lib-lp-staking-frontend/issues/274",
    # tscircuit #114 has many prior attempts, PRs, and rewarded claims; a new
    # local fallback patch would be duplicate work with poor odds.
    "https://github.com/tscircuit/kicad-component-converter/issues/114",
    # ZoneMinder #2138 is an old/stale Bountysource-era request with unclear
    # payout state and a fresh competing /attempt.
    "https://github.com/ZoneMinder/zoneminder/issues/2138",
    # devpool #5012 is a mirror/directory issue with many claim comments and
    # unclear implementation target; use the source issue only if it becomes clear.
    "https://github.com/devpool-directory/devpool-directory/issues/5012",
}


def blocked_repos() -> set[str]:
    repos = set(DEFAULT_BLOCKED_REPOS)
    extra = os.environ.get("BOUNTY_BLOCKED_REPOS", "")
    for item in re.split(r"[,\n]", extra):
        item = item.strip()
        if item:
            repos.add(item)
    return repos


def blocked_issues() -> set[str]:
    issues = set(DEFAULT_BLOCKED_ISSUES)
    extra = os.environ.get("BOUNTY_BLOCKED_ISSUES", "")
    for item in re.split(r"[,\n]", extra):
        item = item.strip()
        if item:
            issues.add(item.rstrip("/"))
    return issues


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


def issue_from_candidate(candidate: dict[str, Any]) -> str:
    for key in ("url", "issue", "html_url"):
        value = str(candidate.get(key) or "").strip().rstrip("/")
        if re.match(r"^https://github\.com/[^/]+/[^/]+/issues/\d+$", value):
            return value
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
    blocked_repo_set = blocked_repos()
    blocked_issue_set = blocked_issues()
    kept: list[dict[str, Any]] = []
    dropped: list[tuple[dict[str, Any], str, str]] = []

    for candidate in candidates:
        repo = repo_from_candidate(candidate)
        issue = issue_from_candidate(candidate)
        if issue in blocked_issue_set:
            dropped.append((candidate, repo, "known stale/crowded bounty issue"))
        elif repo in blocked_repo_set:
            dropped.append((candidate, repo, "known false-positive or unsafe bounty source"))
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
        "This filter removes known false-positive, unsafe, self-tracking, stale, or overcrowded bounty sources before expensive triage/solver work runs.",
        "",
    ]
    if dropped:
        lines.append("## Dropped")
        lines.append("")
        for index, (candidate, repo, reason) in enumerate(dropped[:50], start=1):
            title = candidate.get("title") or "Untitled"
            url = candidate.get("url") or ""
            lines.extend([
                f"### {index}. {title}",
                "",
                f"- Repository: {repo}",
                f"- Issue: {url}",
                f"- Reason: {reason}",
                "",
            ])
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Repo filter kept {len(kept)} candidates and dropped {len(dropped)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
