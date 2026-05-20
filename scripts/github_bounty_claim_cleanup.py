from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import github_bounty_claimer as claimer


def main() -> int:
    token = os.environ.get("BOUNTY_GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or ""
    token = token.strip()
    state = claimer.load_state()
    if not token or not state.get("claims"):
        return 0

    try:
        viewer = claimer.request_json("/user", token)
    except Exception as exc:
        print(f"Claim cleanup skipped: GitHub auth failed: {exc}")
        return 0
    login = str(viewer.get("login") or "")

    results: list[claimer.ClaimResult] = []
    for issue_url, record in list(state.get("claims", {}).items()):
        if not isinstance(record, dict):
            continue
        if str(record.get("status") or "").startswith("withdrawn"):
            continue
        candidate = {
            "title": str(record.get("title") or "Recorded claim cleanup"),
            "url": issue_url,
            "amount_hint": str(record.get("amount_hint") or ""),
            "triage_decision": "keep",
        }
        result = claimer.claim_candidate(candidate, token, login, state)
        if result.status == "withdrawn_false_positive":
            results.append(result)

    if results:
        claimer.write_report(results, state)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
