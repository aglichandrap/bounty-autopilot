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
MAX_QUERIES_PER_RUN = int(os.environ.get("BOUNTY_SCOUT_MAX_QUERIES", "6"))
QUERY_DELAY_SECONDS = float(os.environ.get("BOUNTY_QUERY_DELAY_SECONDS", "3"))
QUERY_OFFSET = int(os.environ.get("BOUNTY_SCOUT_QUERY_OFFSET", os.environ.get("GITHUB_RUN_NUMBER", "0")) or "0")

BLOCKLIST_PATTERNS = [
    r"\u6bcf\u65e5\u4fe1\u606f\u6d41",
    r"\bdaily\s+(info|information)\s+flow\b",
    r"\bnews\s+feed\b",
    r"\bmarket\s+cap\b",
    r"\bprice\s+(?:is|feed|update)\b",
    r"\btoken\s+pool\b",
    r"\breward\s+pool\b",
    r"\brtc\s+pool\b",
    r"\bpr\s+review\s+bounty\b",
    r"\breview\s+prs?\b",
    r"\bbounty\s+claim\b",
    r"\bbug\s+fix\s+claim\b",
    r"^\s*\[claim\]",
    r"^\s*\[bounty claim\]",
    r"\bsecurity remediation\b",
    r"\biam\s+key\b",
    r"\bs3\s+bucket\b",
    r"\bcivil\s+id\b",
    r"\bcredential(s)?\b",
    r"\bprivate\s+key\b",
    r"\bpre_task_context\b",
    r"\bgeneration_context\b",
    r"\bruntime_instructions\b",
    r"paste.*entire.*session",
    r"paste.*everything.*platform",
    r"entire block of text.*start",
    r"\bai only allowed\b",
    r"\bcontest\b",
    r"\bhackathon\b",
    r"\bsecurity report\b",
    r"\bsecurity\b",
    r"\bresponsible disclosure\b",
    r"\breferral\b",
    r"\bairdrop\b",
    r"\bcasino\b",
    r"\bgambling\b",
    r"\btrading bot\b",
]

CLAIMED_PATTERNS = [
    r"\balready assigned\b",
    r"\bassigning this to you\b",
    r"\bi am working on it\b",
    r"\braised pr\b",
    r"\bopened a pr\b",
    r"\bopen(ed)? new prs?\b",
    r"\bplease go ahead and raise a pr\b",
    r"\bdo not open new prs?\b",
    r"\bunder active review\b",
    r"\bwill not be reviewed\b",
    r"\bnot assigned to you\b",
    r"\bclaim\b",
]

REPO_BLOCKLIST = {
    "UnsafeLabs/Bounty-Hunters",
}

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


def strip_code_blocks(value: str) -> str:
    text = re.sub(r"```.*?```", " ", value or "", flags=re.S)
    text = re.sub(r"~~~.*?~~~", " ", text, flags=re.S)
    return text


def amount_hint(text: str) -> str:
    prose = strip_code_blocks(text)
    if re.search(r"\u6bcf\u65e5\u4fe1\u606f\u6d41|\bmarket\s+cap\b|\bprice\s+(?:is|feed|update)\b", prose, flags=re.I):
        return "amount not obvious"
    patterns = [
        r"\$\s?\d[\d,]*(?:\.\d+)?",
        r"\d[\d,]*\s?(?:sats|sat|usd|usdc|eur|gbp)",
        r"(?:reward|bounty)\s?(?:of|:)?\s?\$?\s?\d[\d,]*",
    ]
    matches: list[str] = []
    for pattern in patterns:
        matches.extend(re.findall(pattern, prose, flags=re.I))
    return ", ".join(dict.fromkeys(m.strip() for m in matches[:4])) or "amount not obvious"


def score_issue(item: dict) -> tuple[int, str]:
    title = clean_text(item.get("title", ""))
    body = item.get("body", "") or ""
    body_clean = clean_text(body)
    labels = " ".join(label.get("name", "") for label in item.get("labels", []))
    full_text = f"{title} {body_clean} {labels}".lower()
    prose_text = f"{title} {clean_text(strip_code_blocks(body))} {labels}".lower()

    score = 0
    reasons: list[str] = []

    if re.search(r"^\s*\[(?:claim|bounty claim)\]", title, flags=re.I):
        return -100, "skip: this is a claim, not an open bounty"

    if "pull_request" in item:
        return -100, "skip: this is already a pull request"

    repo_full_name = item.get("repository_url", "").split("/repos/")[-1]
    if repo_full_name in REPO_BLOCKLIST:
        return -100, f"skip: repo blocked ({repo_full_name})"

    assignees = item.get("assignees") or []
    if assignees:
        names = ", ".join(user.get("login", "unknown") for user in assignees[:3])
        return -80, f"skip: already assigned to {names}"

    comments = int(item.get("comments", 0))
    if comments > 80:
        return -80, "skip: overcrowded bounty thread"

    if "bounty" in prose_text or "reward" in prose_text or "opire" in prose_text or "lightning bounties" in prose_text:
        score += 30
        reasons.append("mentions bounty/reward")

    if re.search(r"\$\s?\d|\d+\s?(sats|sat|usd|usdc)", prose_text, flags=re.I):
        score += 25
        reasons.append("has visible amount")

    for pattern in POSITIVE_PATTERNS:
        if re.search(pattern, prose_text, flags=re.I):
            score += 4

    if len(body_clean) < 80:
        score -= 15
        reasons.append("thin description")

    if len(body_clean) > 5000:
        score -= 8
        reasons.append("large issue body")

    for pattern in BLOCKLIST_PATTERNS:
        if re.search(pattern, full_text, flags=re.I):
            return -100, f"skip: blocked pattern: {pattern}"

    for pattern in CLAIMED_PATTERNS:
        if re.search(pattern, full_text, flags=re.I):
            score -= 50
            reasons.append(f"likely claimed: {pattern}")

    if comments > 20:
        score -= 25
        reasons.append("busy thread")
    elif comments <= 5:
        score += 5
        reasons.append("low discussion volume")

    return score, ", ".join(reasons[:5]) or "general bounty candidate"


def comments_url_from_issue(item: dict) -> str | None:
    comments_url = item.get("comments_url")
    if isinstance(comments_url, str) and comments_url:
        return comments_url
    return None


def recent_comments_text(item: dict, token: str | None = None) -> str:
    comments_url = comments_url_from_issue(item)
    if not comments_url or int(item.get("comments", 0)) <= 0:
        return ""
    try:
        comments = github_get(f"{comments_url}?per_page=30", token=token)
    except Exception as exc:
        print(f"Could not inspect comments for {item.get('html_url', '')}: {exc}", file=sys.stderr)
        return ""
    return " ".join(clean_text(comment.get("body", "")) for comment in comments if isinstance(comment, dict))


def load_queries() -> list[str]:
    queries = list(SEARCH_QUERIES)
    if os.path.exists(EXTRA_QUERY_FILE):
        with open(EXTRA_QUERY_FILE, "r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if line and not line.startswith("#"):
                    queries.append(line)
    unique_queries = list(dict.fromkeys(queries))
    if not unique_queries:
        return []
    limit = max(1, min(MAX_QUERIES_PER_RUN, len(unique_queries)))
    offset = (QUERY_OFFSET * limit) % len(unique_queries)
    selected = [unique_queries[(offset + index) % len(unique_queries)] for index in range(limit)]
    print(
        f"Bounty scout using {len(selected)}/{len(unique_queries)} queries "
        f"from offset {offset} with {QUERY_DELAY_SECONDS:g}s delay."
    )
    return selected


def iter_candidates(token: str | None = None) -> Iterable[Candidate]:
    seen: set[str] = set()

    for query in load_queries():
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
            if score >= 25 and int(item.get("comments", 0)) > 0:
                comment_text = recent_comments_text(item, token=token).lower()
                for pattern in BLOCKLIST_PATTERNS:
                    if re.search(pattern, comment_text, flags=re.I):
                        score, reason = -100, f"skip: blocked comment pattern: {pattern}"
                        break
                if score >= 25:
                    for pattern in CLAIMED_PATTERNS:
                        if re.search(pattern, comment_text, flags=re.I):
                            score -= 50
                            reason = f"{reason}, likely claimed in comments: {pattern}"
                            break
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
        time.sleep(QUERY_DELAY_SECONDS)


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
