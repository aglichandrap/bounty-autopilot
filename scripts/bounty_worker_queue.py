from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


CANDIDATES_PATH = Path("bounty_candidates.json")
QUEUE_PATH = Path("bounty_worker_queue.md")
MAX_QUEUE_ITEMS = 10


def main() -> int:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    if not CANDIDATES_PATH.exists():
        candidates = []
    else:
        candidates = json.loads(CANDIDATES_PATH.read_text(encoding="utf-8"))

    candidates = sorted(candidates, key=lambda item: item.get("score", 0), reverse=True)
    top = candidates[:MAX_QUEUE_ITEMS]

    lines = [
        "# Bounty Worker Queue",
        "",
        f"Last built: {now}",
        "",
        f"Purpose: turn scouting results into a concrete work queue for an agent. Up to {MAX_QUEUE_ITEMS} candidates are kept so one stale opportunity does not block the whole system. Do not submit a PR unless the bug is reproduced or the requested change is clearly verified.",
        "",
    ]

    if not top:
        lines.extend(
            [
                "No actionable bounty is queued right now.",
                "",
                "Next action: wait for the next scout run or broaden search queries.",
                "",
            ]
        )
    else:
        for index, item in enumerate(top, start=1):
            lines.extend(
                [
                    f"## Queue Item {index}: {item['title']}",
                    "",
                    f"- Issue: {item['url']}",
                    f"- Repository: {item['repository_url']}",
                    f"- Amount hint: {item['amount_hint']}",
                    f"- Score: {item['score']}",
                    f"- Match reason: {item['reason']}",
                    "",
                    "### Worker Instructions",
                    "",
                    "1. Open the issue and confirm the bounty is still active.",
                    "2. Read the repository contribution rules.",
                    "3. Clone or fork the repository only if the issue is still open and not already solved.",
                    "4. Reproduce the bug or identify the smallest requested change.",
                    "5. Add or update tests when practical.",
                    "6. Submit a focused PR with a short explanation and link it to the bounty issue.",
                    "7. Stop immediately if the issue is vague, already fixed, requires private credentials, or asks for spam/security-abuse behavior.",
                    "",
                ]
            )

    QUEUE_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {QUEUE_PATH} with {len(top)} queue items.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
