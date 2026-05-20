from __future__ import annotations

import json
import os
import re
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


CANDIDATES_PATH = Path("bounty_candidates.json")
EXTRA_QUERY_FILE = Path("bounty_extra_queries.txt")
GITHUB_SEARCH_URL = "https://api.github.com/search/issues"
MAX_CANDIDATES = int(os.environ.get("BOUNTY_VOLUME_MAX_CANDIDATES", "80"))
MIN_SCORE = int(os.environ.get("BOUNTY_VOLUME_MIN_SCORE", "20"))

VOLUME_QUERIES = [
    'is:issue is:open "bounty" "bug" no:assignee comments:<40 sort:updated-desc',
    'is:issue is:open "bounty" "fix" no:assignee comments:<40 sort:updated-desc',
    'is:issue is:open "bounty" "test" no:assignee comments:<40 sort:updated-desc',
    'is:issue is:open "bounty" "docs" no:assignee comments:<30 sort:updated-desc',
    'is:issue is:open "reward" "bug" no:assignee comments:<40 sort:updated-desc',
    'is:issue is:open "reward" "fix" no:assignee comments:<40 sort:updated-desc',
    'is:issue is:open "paid" "bug" no:assignee comments:<40 sort:updated-desc',
    'is:issue is:open "paid" "fix" no:assignee comments:<40 sort:updated-desc',
    'is:issue is:open "microgrant" no:assignee comments:<40 sort:updated-desc',
    'is:issue is:open "Algora" no:assignee comments:<40 sort:updated-desc',
    'is:issue is:open "Opire" no:assignee comments:<40 sort:updated-desc',
    'is:issue is:open "Lightning Bounties" no:assignee comments:<40 sort:updated-desc',
    'repo:requestly/requestly is:issue is:open label:bounty-$20 no:assignee comments:<40 sort:updated-desc',
]

BLOCK_PATTERNS = [
    r"\bsecurity\b",
    r"\bresponsible disclosure\b",
    r"\bcredential(s)?\b",
    r"\bprivate key\b",
    r"\breferral\b",
    r"\bairdrop\b",
    r"\bcasino\b",
    r"\bgambling\b",
    r"\btrading bot\b",
    r"\bcontest\b",
    r"\bhackathon\b",
    r"\bpr review bounty\b",
    r"\breview prs?\b",
    r"^\s*\[(?:claim|bounty claim)\]",
]

CLAIM_PATTERNS = [
    r"\balready assigned\b",
    r"\bi am working on it\b",
    r"\bopened a pr\b",
    r"\braised pr\b",
    r"\bunder active review\b",
    r"\bnot assigned to you\b",
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
    source: str = "volume-expander"


def _github_get_once(url: str, token: str | None = None) -> dict[str, Any]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "bounty-autopilot-volume-expander",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(url, headers=headers)
    try:
        with urlopen(request, timeout=30) as response:
            raw = response.read().decode("utf-8", errors="replace")
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {body[:500] or exc.reason}") from exc
    return json.loads(raw) if raw else {}


def github_get(url: str, token: str | None = None) -> dict[str, Any]:
    if not token:
        return _github_get_once(url)
    try:
        return _github_get_once(url, token=token)
    except RuntimeError as exc:
        # GitHub Actions installation tokens can be forbidden from cross-repo search.
        # Public unauthenticated search is often enough for scouting, so keep going.
        if "HTTP 403" not in str(exc):
            raise
        return _github_get_once(url)


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def load_existing() -> list[dict[str, Any]]:
    if not CANDIDATES_PATH.exists():
        return []
    try:
        data = json.loads(CANDIDATES_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def load_queries() -> list[str]:
    queries = list(VOLUME_QUERIES)
    if EXTRA_QUERY_FILE.exists():
        for line in EXTRA_QUERY_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and line not in queries:
                queries.append(line)
    return queries


def amount_hint(text: str) -> str:
    matches = re.findall(r"\$\s?\d[\d,]*(?:\.\d+)?|\b\d[\d,]*\s?(?:usd|usdc|sats?|eur|gbp)\b", text, flags=re.I)
    return ", ".join(dict.fromkeys(match.strip() for match in matches[:4])) or "amount not obvious"


def score_item(item: dict[str, Any]) -> tuple[int, str]:
    if "pull_request" in item:
        return -100, "skip: pull request"
    if item.get("assignees"):
        return -90, "skip: assigned"
    title = clean(str(item.get("title") or ""))
    body = clean(str(item.get("body") or ""))
    labels = " ".join(str(label.get("name") or "") for label in item.get("labels", []) if isinstance(label, dict))
    text = f"{title} {body} {labels}".lower()
    for pattern in BLOCK_PATTERNS:
        if re.search(pattern, text, flags=re.I):
            return -100, f"skip: blocked pattern {pattern}"
    score = 0
    reasons: list[str] = []
    if any(word in text for word in ("bounty", "reward", "paid", "microgrant", "opire", "algora", "lightning bounties")):
        score += 30
        reasons.append("paid/bounty wording")
    if re.search(r"\$\s?\d|\b\d+\s?(?:usd|usdc|sats?)\b", text, flags=re.I):
        score += 25
        reasons.append("visible amount")
    if re.search(r"\b(bug|fix|test|typescript|python|api|frontend|backend|cli|docs?)\b", text, flags=re.I):
        score += 10
        reasons.append("coding scope")
    comments = int(item.get("comments") or 0)
    if comments <= 5:
        score += 8
        reasons.append("low discussion")
    elif comments > 40:
        score -= 25
        reasons.append("busy discussion")
    for pattern in CLAIM_PATTERNS:
        if re.search(pattern, text, flags=re.I):
            score -= 50
            reasons.append("likely claimed")
            break
    if len(body) < 60:
        score -= 8
        reasons.append("thin description")
    return score, ", ".join(reasons[:5]) or "volume candidate"


def search(query: str, token: str | None) -> list[Candidate]:
    params = urlencode({"q": query, "per_page": 50})
    payload = github_get(f"{GITHUB_SEARCH_URL}?{params}", token=token)
    candidates: list[Candidate] = []
    for item in payload.get("items", []):
        if not isinstance(item, dict):
            continue
        score, reason = score_item(item)
        if score < MIN_SCORE:
            continue
        url = str(item.get("html_url") or "")
        repo_url = str(item.get("repository_url") or "").replace("api.github.com/repos", "github.com")
        text = f"{item.get('title') or ''}\n{item.get('body') or ''}"
        if not url or not repo_url:
            continue
        candidates.append(
            Candidate(
                title=clean(str(item.get("title") or "Untitled")),
                url=url,
                repository_url=repo_url,
                updated_at=str(item.get("updated_at") or ""),
                score=score,
                amount_hint=amount_hint(text),
                reason=reason,
            )
        )
    return candidates


def write_report(found: list[Candidate], errors: list[str]) -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = ["# Bounty Volume Expander", "", f"Last run: {now}", "", f"Fresh candidates found before triage: {len(found)}", ""]
    for candidate in found[:25]:
        lines.extend([
            f"## {candidate.title}",
            "",
            f"- Score: {candidate.score}",
            f"- Amount: {candidate.amount_hint}",
            f"- Issue: {candidate.url}",
            f"- Repository: {candidate.repository_url}",
            f"- Reason: {candidate.reason}",
            "",
        ])
    if errors:
        lines.extend(["## Search Errors", ""])
        for error in errors:
            lines.append(f"- {error}")
    Path("bounty_volume_report.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    token = os.environ.get("GITHUB_SEARCH_TOKEN") or os.environ.get("BOUNTY_GITHUB_TOKEN") or os.environ.get("GITHUB_TOKEN")
    by_url: dict[str, dict[str, Any]] = {str(item.get("url")): item for item in load_existing() if item.get("url")}
    found: list[Candidate] = []
    errors: list[str] = []
    for query in load_queries():
        try:
            hits = search(query, token=token)
            found.extend(hits)
            for candidate in hits:
                existing = by_url.get(candidate.url)
                data = asdict(candidate)
                if not existing or int(existing.get("score") or 0) < candidate.score:
                    by_url[candidate.url] = data
        except Exception as exc:
            errors.append(f"{query}: {exc}")
        time.sleep(1)
    merged = sorted(by_url.values(), key=lambda item: int(item.get("score") or 0), reverse=True)[:MAX_CANDIDATES]
    CANDIDATES_PATH.write_text(json.dumps(merged, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_report(found, errors)
    print(f"Volume expander added {len(found)} raw candidates; merged total {len(merged)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
