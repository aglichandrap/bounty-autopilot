from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


TASKBOUNTY_PATH = Path("taskbounty_tasks.json")
GITHUB_PATH = Path("bounty_candidates.json")
QUEUE_PATH = Path("claim_queue.md")


CLAIM_TEMPLATE = (
    "I can take this if it is still available. I will first reproduce the issue, "
    "keep the PR focused, and include a regression test or clear verification notes before asking for review."
)

ASSIGNMENT_TEMPLATE = (
    "I can work on this. Please assign it to me if it is still available; "
    "I will wait for assignment before opening a PR."
)


def load_json(path: Path) -> list[dict]:
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def is_actionable(item: dict) -> bool:
    text = " ".join(str(item.get(key, "")) for key in ("title", "reason", "amount_hint", "source")).lower()
    if any(word in text for word in ("closed", "claim", "security", "credential", "prompt", "context")):
        return False
    return bool(item.get("url")) and "amount not obvious" not in text


def main() -> int:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    taskbounty = [item for item in load_json(TASKBOUNTY_PATH) if is_actionable(item)]
    github = [item for item in load_json(GITHUB_PATH) if is_actionable(item)]

    lines = [
        "# Claim Queue",
        "",
        f"Last built: {now}",
        "",
        "Identity: use the owner account `asaadnashed`; do not impersonate another human or use fake accounts.",
        "",
    ]

    if not taskbounty and not github:
        lines.extend(
            [
                "No safe claim target is ready right now.",
                "",
                "Next action: keep scouting. Do not comment just to look active.",
                "",
            ]
        )

    if taskbounty:
        lines.extend(["## TaskBounty", ""])
        for item in taskbounty[:3]:
            lines.extend(
                [
                    f"### {item.get('title', 'Untitled')}",
                    "",
                    f"- URL: {item.get('url')}",
                    f"- Amount: {item.get('amount_hint')}",
                    "- Status: needs TaskBounty agent API access before attempting/submitting.",
                    "",
                ]
            )

    if github:
        lines.extend(["## GitHub", ""])
        for item in github[:3]:
            lines.extend(
                [
                    f"### {item.get('title', 'Untitled')}",
                    "",
                    f"- URL: {item.get('url')}",
                    f"- Amount: {item.get('amount_hint')}",
                    "- Claim comment if rules allow:",
                    "",
                    "```text",
                    CLAIM_TEMPLATE,
                    "```",
                    "",
                    "- Assignment-first comment if the project requires assignment:",
                    "",
                    "```text",
                    ASSIGNMENT_TEMPLATE,
                    "```",
                    "",
                ]
            )

    QUEUE_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {QUEUE_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
