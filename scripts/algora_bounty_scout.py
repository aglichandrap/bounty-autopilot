from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from urllib.request import Request, urlopen


CANDIDATES_PATH = Path("bounty_candidates.json")
REPORT_PATH = Path("algora_bounty_report.md")

PAGES = [
    ("https://algora.io/projectdiscovery/bounties", {"nuclei": "projectdiscovery/nuclei"}),
    ("https://algora.io/cal/bounties", {"cal.com": "calcom/cal.com"}),
    ("https://algora.io/algora/bounties/community", {"tv": "algora-io/tv", "permit-cli": "algora-io/permit-cli"}),
]


@dataclass
class AlgoraCandidate:
    title: str
    url: str
    repository_url: str
    updated_at: str
    score: int
    amount_hint: str
    reason: str
    source: str = "algora"


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def fetch(url: str) -> str:
    request = Request(url, headers={"User-Agent": "bounty-autopilot-algora-scout"})
    with urlopen(request, timeout=40) as response:
        return response.read().decode("utf-8", errors="replace")


def strip_tags(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    value = unescape(value)
    return re.sub(r"\s+", " ", value).strip()


def load_existing() -> list[dict]:
    if not CANDIDATES_PATH.exists():
        return []
    try:
        data = json.loads(CANDIDATES_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def algora_score(amount: str) -> int:
    value = int(amount.replace(",", ""))
    # Algora pages are dedicated paid bounty feeds, so these should outrank noisy
    # generic GitHub search hits and always survive the merged candidate cap.
    return 140 + min(value // 10, 40)


def candidate_sort_key(item: dict) -> tuple[int, int]:
    source_boost = 1000 if str(item.get("source") or "").lower() == "algora" else 0
    return source_boost + int(item.get("score") or 0), int(bool(item.get("amount_hint")))


def parse_page(url: str, repo_map: dict[str, str]) -> list[AlgoraCandidate]:
    html = fetch(url)
    text = strip_tags(html)
    candidates: list[AlgoraCandidate] = []
    pattern = re.compile(
        r"\$(?P<amount>\d[\d,]*)\s+(?P<repo>[A-Za-z0-9_.-]+)#(?P<issue>\d+)\s+(?P<title>.*?)(?:\s+\d+\s+claims?|\s+\d+\s+claim|\s+\d+\s+(?:month|months|day|days|hour|hours) ago|\s+View Reward|\s+Completed|\s+Open|$)",
        re.I,
    )
    for match in pattern.finditer(text):
        short_repo = match.group("repo")
        full_repo = repo_map.get(short_repo)
        if not full_repo:
            continue
        amount = match.group("amount")
        issue_number = match.group("issue")
        title = re.sub(r"\s+", " ", match.group("title")).strip(" -")
        if not title:
            title = f"Algora bounty {short_repo}#{issue_number}"
        candidates.append(
            AlgoraCandidate(
                title=title[:180],
                url=f"https://github.com/{full_repo}/issues/{issue_number}",
                repository_url=f"https://github.com/{full_repo}",
                updated_at=datetime.now(timezone.utc).isoformat(),
                score=algora_score(amount),
                amount_hint=f"${amount}",
                reason=f"Algora open paid bounty from {url}",
            )
        )
    return candidates


def main() -> int:
    existing = load_existing()
    by_url = {str(item.get("url")): item for item in existing if isinstance(item, dict) and item.get("url")}
    found: list[AlgoraCandidate] = []
    errors: list[str] = []
    for page_url, repo_map in PAGES:
        try:
            found.extend(parse_page(page_url, repo_map))
        except Exception as exc:
            errors.append(f"{page_url}: {exc}")
    for candidate in found:
        by_url[candidate.url] = asdict(candidate)
    merged = sorted(by_url.values(), key=candidate_sort_key, reverse=True)[:60]
    CANDIDATES_PATH.write_text(json.dumps(merged, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = ["# Algora Bounty Scout", "", f"Last run: {now_utc()}", "", f"Found candidates: {len(found)}", ""]
    for candidate in found[:20]:
        lines.extend([
            f"## {candidate.title}", "",
            f"- Amount: {candidate.amount_hint}",
            f"- Issue: {candidate.url}",
            f"- Repository: {candidate.repository_url}",
            f"- Score: {candidate.score}",
            f"- Reason: {candidate.reason}", "",
        ])
    if errors:
        lines.extend(["## Errors", ""])
        for error in errors:
            lines.append(f"- {error}")
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Added {len(found)} Algora candidates; merged total {len(merged)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
