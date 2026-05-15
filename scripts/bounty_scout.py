from __future__ import annotations

import json
import re
import sys
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import os
from typing import Iterable
from urllib.parse import urlencode
from urllib.request import Request, urlopen


GITHUB_SEARCH_URL = "https://api.github.com/search/issues"

SEARCH_QUERIES = [
    'is:issue is:open bounty in:title,body sort:updated-desc',
    'is:issue is:open "good first issue" bounty sort:updated-desc',
    'is:issue is:open reward bounty sort:updated-desc',
    'is:issue is:open "paid" "PR" "bounty" sort:updated-desc',
    'is:issue is:open "Lightning Bounties" sort:updated-desc',
    'is:issue is:open "Opire" bounty sort:updated-desc',
]

EXTRA_QUERY_FILE = "bounty_extra_queries.txt"

BLOCKLIST_PATTERNS = [
    r"\bcontest\b",
    r"\bhackathon\b",
    r"\bsecurity report\b",
    r"\bresponsible disclosure\b",
    r"\breferral\b",
    r"\bairdrop\b",
    r"\bcasino\b",
    r"\bgambling\b",
    r"\btrading bot\b",
]

POSITIVE_PATTERNS = [
    r"\bbug\b",
    r"\bfix\b",
    r"\btest\b",
    r"\bdocs?\b",
    r"\btypescript\b",
    r"\bpython\b",
    r"\bfrontend\b",
    r"\bbackend\b",
    r"\bapi\b",
    r"\bcli\b",
]


@dataclass
class Candidate:
    title: str
    url: str
    repository_url: str
    updated_at: str
    score: int
    amount_hint: str
    reason: str


def github_get(url: str, token: str | None = None) -> dict:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "bounty-scout-autopilot",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(url, headers=headers)
    with urlopen(request, timeout=25) as response:
        return json.loads(response.read().decode("utf-8"))


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def amount_hint(text: str) -> str:
    patterns = [
        r"\$\s?\d[\d,]*(?:\.\d+)?",
        r"\d[\d,]*\s?(?:sats|sat|usd|usdc|eur|gbp)",
        r"(?:reward|bounty)\s?(?:of|:)?\s?\$?\s?\d[\d,]*",
    ]
    matches: list[str] = []
    for pattern in patterns:
        matches.extend(re.findall(pattern, text, flags=re.I))
    return ", ".join(dict.fromkeys(m.strip() for m in matches[:4])) or "amount not obvious"


def score_issue(item: dict) -> tuple[int, str]:
    title = clean_text(item.get("title", ""))
    body = clean_text(item.get("body", ""))
    labels = " ".join(label.get("name", "") for label in item.get("labels", []))
    text = f"{title} {body} {labels}".lower()

    score = 0
    reasons: list[str] = []

    if "pull_request" in item:
        return -100, "skip: this is already a pull request"

    if "bounty" in text or "reward" in text or "opire" in text or "lightning bounties" in text:
        score += 30
        reasons.append("mentions bounty/reward")

    if re.search(r"\$\s?\d|\d+\s?(sats|sat|usd|usdc)", text, flags=re.I):
        score += 25
        reasons.append("has visible amount")

    for pattern in POSITIVE_PATTERNS:
        if re.search(pattern, text, flags=re.I):
            score += 4

    if len(body) < 80:
        score -= 15
        reasons.append("thin description")

    if len(body) > 5000:
        score -= 8
        reasons.append("large issue body")

    for pattern in BLOCKLIST_PATTERNS:
        if re.search(pattern, text, flags=re.I):
            score -= 60
            reasons.append(f"blocked pattern: {pattern}")

    comments = int(item.get("comments", 0))
    if comments > 20:
        score -= 10
        reasons.append("busy thread")
    elif comments <= 5:
        score += 5
        reasons.append("low discussion volume")

    return score, ", ".join(reasons[:5]) or "general bounty candidate"


def iter_candidates(token: str | None = None) -> Iterable[Candidate]:
    seen: set[str] = set()
    queries = list(SEARCH_QUERIES)
    if os.path.exists(EXTRA_QUERY_FILE):
        with open(EXTRA_QUERY_FILE, "r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if line and not line.startswith("#"):
                    queries.append(line)

    for query in queries:
        params = urlencode({"q": query, "per_page": 20})
        try:
            data = github_get(f"{GITHUB_SEARCH_URL}?{params}", token=token)
        except Exception as exc:
            print(f"Search failed for {query!r}: {exc}", file=sys.stderr)
            continue

        for item in data.get("items", []):
            url = item.get("html_url", "")
            if not url or url in seen:
                continue
            seen.add(url)
            score, reason = score_issue(item)
            if score < 25:
                continue
            repo_url = item.get("repository_url", "").replace("api.github.com/repos", "github.com")
            text = f"{item.get('title', '')}\n{item.get('body', '')}"
            yield Candidate(
                title=clean_text(item.get("title", "")),
                url=url,
                repository_url=repo_url,
                updated_at=item.get("updated_at", ""),
                score=score,
                amount_hint=amount_hint(text),
                reason=reason,
            )
        time.sleep(2)


def write_outputs(candidates: list[Candidate]) -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    candidates = sorted(candidates, key=lambda item: item.score, reverse=True)[:12]

    with open("bounty_candidates.json", "w", encoding="utf-8") as handle:
        json.dump([asdict(candidate) for candidate in candidates], handle, indent=2, ensure_ascii=False)
        handle.write("\n")

    lines = [
        "# Bounty Scout Candidates",
        "",
        f"Last run: {now}",
        "",
        "This report filters public GitHub issues for small paid coding opportunities. It is a scout, not a payout guarantee.",
        "",
    ]
    if not candidates:
        lines.extend(["No strong candidates found in this run.", ""])
    for index, candidate in enumerate(candidates, start=1):
        lines.extend(
            [
                f"## {index}. {candidate.title}",
                "",
                f"- Score: {candidate.score}",
                f"- Amount hint: {candidate.amount_hint}",
                f"- Issue: {candidate.url}",
                f"- Repository: {candidate.repository_url}",
                f"- Updated: {candidate.updated_at}",
                f"- Why it matched: {candidate.reason}",
                "- Next action: inspect repo, confirm bounty rules, reproduce issue, submit a focused PR only if the fix is real.",
                "",
            ]
        )
    with open("bounty_report.md", "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))


def main() -> int:
    token = os.environ.get("GITHUB_TOKEN")
    candidates = list(iter_candidates(token=token))
    write_outputs(candidates)
    print(f"Wrote {len(candidates)} candidates.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
