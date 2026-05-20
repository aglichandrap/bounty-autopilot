from __future__ import annotations

import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote
from urllib.request import Request, urlopen


CANDIDATES_PATH = Path("bounty_candidates.json")
REPORT_PATH = Path("bounty_candidate_triage_report.md")
GITHUB_API = "https://api.github.com"
OWNER_LOGIN = os.environ.get("BOUNTY_OWNER_LOGIN", "asaadnashed").lower()
MAX_COMMENTS_FOR_NEW_WORK = int(os.environ.get("BOUNTY_MAX_COMMENTS", "25"))
MAX_OPEN_COMPETING_PRS = int(os.environ.get("BOUNTY_MAX_COMPETING_PRS", "0"))
PAID_LABEL_WORDS = ("bounty", "reward", "microgrant")
NO_PAY_PATTERN = re.compile(
    r"\b(no paid bounty|no bounty|not paid|unpaid|free[- ]?ok|volunteer only|no compensation)\b"
)
MONEY_PATTERN = re.compile(r"(?:usd\s*)?\$\s*\d|(?:\b\d+\s*(?:usd|usdc)\b)", re.IGNORECASE)
REAL_BOUNTY_PATTERN = re.compile(
    r"\b(bounty|reward|microgrant|opire|algora|lightning bounties)\b"
    r"|\b(will pay|payable upon|payment details|payout|prize)\b",
    re.IGNORECASE,
)
FALSE_POSITIVE_PATTERN = re.compile(
    r"\b(bounty claim|claim:)\b|\b(completed|working submission)\b.*\b(sol(ana)? wallet|payment details)\b"
    r"|\b(cost floor|cost impact|monthly cost|per month|/month|/mo|paid once|paid api|budget tokens|cache info|prompt_cache_key|token consumption)\b"
    r"|\b(wast(e|ing)|unnecessary|expensive)\b.{0,40}\b(tokens?|edits?|calls?)\b"
    r"|\b(smoke test|stripe live|vercel|production access)\b"
    r"|\b(watch|short|long|bajista|alcista|bearish|bullish)\b.*\b([a-z]{2,6}/usd|usd/[a-z]{2,6}|scanner)\b"
    r"|\b(zec/usd|btc/usd|eth/usd|trading signal|market signal)\b",
    re.IGNORECASE,
)
COMMENT_BLOCK_PATTERN = re.compile(
    r"\b(submitted|opened|raised)\s+(?:a\s+)?(?:focused\s+)?(?:fix\s+)?(?:pr|pull request)\b"
    r"|/attempt\b|/claim\b|pull/\d+|#\d+\s+for\s+this"
    r"|\bi can take this\b|\bi'?m interested in taking\b|\binterested in taking a focused look\b"
    r"|\bi'll open a focused pr\b|\bi will open a focused pr\b"
    r"|\bsuperseded\b|\bshipped as pr\b|\bbuilt\b.*\bpr\s+#?\d+\b"
    r"|\bsource or patching workflow available\b|\bpublic branch only contains the readme\b"
    r"|\bexpected deliverable a binary patch\b|\bnot the source/build setup\b"
    r"|\bthis issue can be closed once\b|\bno code written yet\b.*\bthe handoff\b",
    re.IGNORECASE,
)


@dataclass
class TriageEntry:
    title: str
    url: str
    decision: str
    reasons: list[str]
    linked_prs: list[str]
    original_score: int
    final_score: int


def github_get(path_or_url: str, token: str | None = None) -> Any:
    url = path_or_url if path_or_url.startswith("https://") else f"{GITHUB_API}{path_or_url}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "bounty-autopilot-candidate-triage",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(url, headers=headers)
    with urlopen(request, timeout=30) as response:
        raw = response.read().decode("utf-8", errors="replace")
    return json.loads(raw) if raw else {}


def parse_issue_url(url: str) -> tuple[str, int] | None:
    match = re.search(r"https://github\.com/([^/]+/[^/]+)/issues/(\d+)", url or "")
    if not match:
        return None
    return match.group(1), int(match.group(2))


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def search_related_prs(repo: str, issue_number: int, title: str, token: str | None) -> list[dict[str, Any]]:
    title_terms = " ".join(re.findall(r"[A-Za-z0-9_+-]{4,}", title)[:5])
    queries = [
        f"repo:{repo} is:pr is:open {issue_number}",
        f"repo:{repo} is:pr is:open {title_terms}" if title_terms else "",
    ]
    seen: set[str] = set()
    prs: list[dict[str, Any]] = []
    for query in queries:
        if not query:
            continue
        try:
            payload = github_get(f"/search/issues?q={quote(query)}&per_page=10", token=token)
        except Exception as exc:
            print(f"PR search failed for {repo}#{issue_number}: {exc}", file=sys.stderr)
            continue
        for item in payload.get("items", []):
            url = item.get("html_url")
            if not isinstance(url, str) or url in seen:
                continue
            seen.add(url)
            prs.append(item)
    return prs


def comments_indicate_competition(repo: str, issue_number: int, token: str | None) -> bool:
    try:
        comments = github_get(f"/repos/{repo}/issues/{issue_number}/comments?per_page=50", token=token)
    except Exception as exc:
        print(f"Comment triage failed for {repo}#{issue_number}: {exc}", file=sys.stderr)
        return False
    if not isinstance(comments, list):
        return False
    text = " ".join(clean(str(comment.get("body") or "")) for comment in comments if isinstance(comment, dict)).lower()
    return COMMENT_BLOCK_PATTERN.search(text) is not None


def has_paid_signal(candidate: dict[str, Any], labels: set[str], issue_text: str) -> bool:
    candidate_text = " ".join(
        clean(str(candidate.get(key) or ""))
        for key in ("title", "amount_hint", "reason", "source")
    ).lower()
    combined = f"{candidate_text} {issue_text} {' '.join(labels)}"
    if FALSE_POSITIVE_PATTERN.search(combined):
        return False
    bounty_label = any(any(word in label for word in PAID_LABEL_WORDS) for label in labels)
    explicit_bounty = REAL_BOUNTY_PATTERN.search(combined) is not None
    has_money = MONEY_PATTERN.search(combined) is not None
    return bounty_label or (explicit_bounty and has_money)


def triage_candidate(candidate: dict[str, Any], token: str | None) -> tuple[dict[str, Any] | None, TriageEntry]:
    title = clean(str(candidate.get("title") or "Untitled"))
    url = clean(str(candidate.get("url") or ""))
    score = int(candidate.get("score") or 0)
    final_score = score
    reasons: list[str] = []
    linked_pr_urls: list[str] = []
    decision = "keep"

    parsed = parse_issue_url(url)
    if not parsed:
        decision = "drop"
        reasons.append("not a GitHub issue URL")
        final_score -= 100
    else:
        repo, issue_number = parsed
        try:
            issue = github_get(f"/repos/{repo}/issues/{issue_number}", token=token)
            comments_count = int(issue.get("comments") or 0)
            assignees = issue.get("assignees") or []
            state = issue.get("state")
            labels = {
                str(label.get("name") or "").lower()
                for label in issue.get("labels", [])
                if isinstance(label, dict)
            }
            issue_text = f"{title} {issue.get('body') or ''}".lower()

            if FALSE_POSITIVE_PATTERN.search(issue_text):
                decision = "drop"
                reasons.append("false positive claim/cost/market/manual-access issue, not an open coding bounty")
                final_score -= 100
            elif NO_PAY_PATTERN.search(issue_text) or any("free-ok" in label for label in labels):
                decision = "drop"
                reasons.append("issue explicitly indicates no paid bounty or free-only payment status")
                final_score -= 100
            elif not has_paid_signal(candidate, labels, issue_text):
                decision = "drop"
                reasons.append("no clear open paid bounty signal found")
                final_score -= 70

            if (
                "content-proposal" in labels
                or re.search(r"\b(tutorial|article|blog post|written tutorial|dev\.to|medium|hashnode)\b", issue_text)
            ) and re.search(r"\bai[- ]generated content\b|substantially ai-generated|ai content", issue_text):
                decision = "drop"
                reasons.append("content bounty has AI-content disqualification risk for autonomous work")
                final_score -= 100

            if state != "open":
                decision = "drop"
                reasons.append("issue is not open")
                final_score -= 100
            if assignees:
                decision = "drop"
                names = ", ".join(str(user.get("login") or "unknown") for user in assignees[:3] if isinstance(user, dict))
                reasons.append(f"already assigned to {names or 'someone'}")
                final_score -= 80
            if comments_count > MAX_COMMENTS_FOR_NEW_WORK:
                decision = "drop"
                reasons.append(f"busy issue thread ({comments_count} comments)")
                final_score -= 60

            related_prs = search_related_prs(repo, issue_number, title, token=token)
            competing_prs = []
            for pr in related_prs:
                user = pr.get("user") if isinstance(pr, dict) else None
                login = str(user.get("login") or "").lower() if isinstance(user, dict) else ""
                if login != OWNER_LOGIN:
                    competing_prs.append(pr)
            linked_pr_urls = [str(pr.get("html_url")) for pr in competing_prs if pr.get("html_url")]
            if len(competing_prs) > MAX_OPEN_COMPETING_PRS:
                decision = "drop"
                reasons.append(f"open competing PRs found ({len(competing_prs)})")
                final_score -= 90
            elif related_prs:
                reasons.append("own/related PR already exists; avoid duplicate work")
                final_score -= 20

            if comments_indicate_competition(repo, issue_number, token=token):
                decision = "drop"
                reasons.append("issue comments indicate active attempts, claims, missing-source uncertainty, or superseded/built work")
                final_score -= 60
        except Exception as exc:
            reasons.append(f"GitHub triage failed: {exc}")
            final_score -= 10

    updated = dict(candidate)
    updated["score"] = final_score
    updated["triage_decision"] = decision
    updated["triage_reasons"] = reasons
    updated["linked_prs"] = linked_pr_urls

    if decision == "drop" or final_score < 25:
        kept = None
    else:
        kept = updated
    return kept, TriageEntry(title, url, decision, reasons, linked_pr_urls, score, final_score)


def load_candidates() -> list[dict[str, Any]]:
    if not CANDIDATES_PATH.exists():
        return []
    try:
        data = json.loads(CANDIDATES_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def write_report(entries: list[TriageEntry], kept_count: int) -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# GitHub Bounty Candidate Triage",
        "",
        f"Last run: {now}",
        "",
        f"Kept candidates: {kept_count}",
        "",
        "This pass removes unpaid, crowded, assigned, closed, already-attempted, market-alert, token-cost, or false-positive GitHub bounty issues before worker time is spent.",
        "",
    ]
    if not entries:
        lines.extend(["No candidates were available to triage.", ""])
    for index, entry in enumerate(entries, start=1):
        lines.extend(
            [
                f"## {index}. {entry.title}",
                "",
                f"- Decision: {entry.decision}",
                f"- Score: {entry.original_score} -> {entry.final_score}",
                f"- Issue: {entry.url}",
            ]
        )
        for reason in entry.reasons:
            lines.append(f"- Reason: {reason}")
        for pr_url in entry.linked_prs[:5]:
            lines.append(f"- Competing PR: {pr_url}")
        lines.append("")
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    token = os.environ.get("GITHUB_TOKEN")
    kept: list[dict[str, Any]] = []
    entries: list[TriageEntry] = []
    for candidate in load_candidates():
        updated, entry = triage_candidate(candidate, token=token)
        entries.append(entry)
        if updated is not None:
            kept.append(updated)
    kept = sorted(kept, key=lambda item: item.get("score", 0), reverse=True)
    CANDIDATES_PATH.write_text(json.dumps(kept, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_report(entries, kept_count=len(kept))
    print(f"Triaged {len(entries)} GitHub bounty candidates; kept {len(kept)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
