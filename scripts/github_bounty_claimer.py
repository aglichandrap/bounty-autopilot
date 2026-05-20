from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.parse import quote
from urllib.request import Request, urlopen


API = "https://api.github.com"
CANDIDATES_PATH = Path("bounty_candidates.json")
STATE_PATH = Path("github_bounty_claim_state.json")
REPORT_PATH = Path("github_bounty_claim_report.md")
MAX_CLAIMS = int(os.environ.get("GITHUB_BOUNTY_MAX_CLAIMS", "3"))
MAX_COMMENTS = int(os.environ.get("GITHUB_BOUNTY_CLAIM_MAX_COMMENTS", "80"))
MAX_COMPETING_PRS = int(os.environ.get("GITHUB_BOUNTY_MAX_COMPETING_PRS", "4"))
MIN_CLAIM_AMOUNT = float(os.environ.get("GITHUB_BOUNTY_MIN_CLAIM_AMOUNT", "10"))
PAID_LABEL_WORDS = ("bounty", "reward", "microgrant")
REAL_BOUNTY_PATTERN = re.compile(
    r"\b(bounty|reward|microgrant|opire|algora|lightning bounties)\b"
    r"|\b(will pay|payable upon|payment details|payout|prize)\b",
    re.IGNORECASE,
)

CLAIM_COMMENT = (
    "I can take this if it is still available. I will first reproduce the issue, "
    "keep the PR focused, and include a regression test or clear verification notes before asking for review."
)

ASSIGNMENT_COMMENT = (
    "I can work on this if it is still available. Please assign it to me if assignment is required before opening a PR."
)

WITHDRAW_COMMENT = (
    "Withdrawing this. After reviewing the issue more carefully, I noticed the apparent dollar amount "
    "was from a log/code block rather than a bounty signal. Sorry for the noise."
)


@dataclass
class ClaimResult:
    title: str
    issue_url: str
    status: str
    comment_url: str = ""
    message: str = ""


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def request_json(path: str, token: str | None = None, method: str = "GET", payload: dict[str, Any] | None = None) -> Any:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
        "User-Agent": "bounty-autopilot-claimer",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(f"{API}{path}", data=data, headers=headers, method=method)
    with urlopen(request, timeout=60) as response:
        text = response.read().decode("utf-8", errors="replace")
    return json.loads(text) if text else {}


def http_error_message(exc: HTTPError) -> str:
    try:
        body = exc.read().decode("utf-8", errors="replace")
    except Exception:
        body = ""
    return f"HTTP {exc.code}: {body or exc.reason}"


def load_candidates() -> list[dict[str, Any]]:
    if not CANDIDATES_PATH.exists():
        return []
    try:
        data = json.loads(CANDIDATES_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def load_state() -> dict[str, Any]:
    if not STATE_PATH.exists():
        return {"claims": {}}
    try:
        state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"claims": {}}
    if not isinstance(state, dict):
        return {"claims": {}}
    state.setdefault("claims", {})
    return state


def parse_issue(url: str) -> tuple[str, int] | None:
    match = re.search(r"github\.com/([^/]+/[^/]+)/issues/(\d+)", url or "")
    if not match:
        return None
    return match.group(1), int(match.group(2))


def strip_code_blocks(value: str) -> str:
    text = re.sub(r"```.*?```", " ", value or "", flags=re.S)
    text = re.sub(r"~~~.*?~~~", " ", text, flags=re.S)
    return text


def amount_value(text: str) -> float:
    prose = strip_code_blocks(text)
    best = 0.0
    for match in re.finditer(r"\$\s*([0-9][0-9,]*(?:\.[0-9]+)?)(\s*k)?", prose, flags=re.I):
        value = float(match.group(1).replace(",", ""))
        if match.group(2):
            value *= 1000
        best = max(best, value)
    for match in re.finditer(r"\b([0-9][0-9,]*(?:\.[0-9]+)?)\s*(usd|usdc)\b", prose, flags=re.I):
        best = max(best, float(match.group(1).replace(",", "")))
    return best


def issue_labels(issue: dict[str, Any]) -> set[str]:
    return {
        str(label.get("name") or "").lower()
        for label in issue.get("labels", [])
        if isinstance(label, dict)
    }


def amount_blob(candidate: dict[str, Any], issue: dict[str, Any]) -> str:
    return " ".join(
        str(value or "")
        for value in (
            candidate.get("title"),
            candidate.get("amount_hint"),
            issue.get("title"),
            strip_code_blocks(str(issue.get("body") or "")),
            " ".join(issue_labels(issue)),
        )
    ).lower()


def bounty_blob(candidate: dict[str, Any], issue: dict[str, Any]) -> str:
    return " ".join(
        str(value or "")
        for value in (
            candidate.get("title"),
            issue.get("title"),
            strip_code_blocks(str(issue.get("body") or "")),
            " ".join(issue_labels(issue)),
        )
    ).lower()


def text_blob(candidate: dict[str, Any], issue: dict[str, Any]) -> str:
    return f"{amount_blob(candidate, issue)} {bounty_blob(candidate, issue)}"


def has_paid_signal(candidate: dict[str, Any], issue: dict[str, Any]) -> bool:
    amount_text = amount_blob(candidate, issue)
    bounty_text = bounty_blob(candidate, issue)
    labels = issue_labels(issue)
    bounty_label = any(any(word in label for word in PAID_LABEL_WORDS) for label in labels)
    explicit_bounty = REAL_BOUNTY_PATTERN.search(bounty_text) is not None
    return (bounty_label or explicit_bounty) and amount_value(amount_text) >= MIN_CLAIM_AMOUNT


def forbidden(blob: str) -> str:
    patterns = {
        "security-sensitive": r"\b(security|vulnerability|credential|private key|api key|secret)\b",
        "private-access-needed": r"\b(stripe live|vercel|production access|admin access|customer account|private repo)\b",
        "manual-verification-only": r"\b(smoke test|end-to-end smoke|manual verification|verify .* live-mode)\b",
        "spam/deception": r"\b(spam|fake account|referral|airdrop|casino|gambling|trading bot)\b",
        "prompt/context": r"\b(prompt|context|pre_task_context|runtime_instructions)\b",
        "content-only": r"\b(article|blog post|tutorial|content proposal)\b",
    }
    for reason, pattern in patterns.items():
        if re.search(pattern, blob):
            return reason
    return ""


def claim_comment_by_us(comments: list[dict[str, Any]], login: str) -> dict[str, Any] | None:
    for comment in comments:
        if not isinstance(comment, dict):
            continue
        user = comment.get("user") if isinstance(comment.get("user"), dict) else {}
        if str(user.get("login") or "").lower() == login.lower():
            return comment
    return None


def blocking_competition_in_comments(comments: list[dict[str, Any]], login: str) -> str:
    pattern = re.compile(
        r"\b(opened|submitted|raised)\s+(?:a\s+)?(?:focused\s+)?(?:fix\s+)?(?:pr|pull request)\b"
        r"|/claim\b|/attempt\b|pull/\d+|\bassigned to me\b|\bassigned this to\b",
        re.I,
    )
    for comment in comments:
        if not isinstance(comment, dict):
            continue
        user = comment.get("user") if isinstance(comment.get("user"), dict) else {}
        author = str(user.get("login") or "")
        if author.lower() == login.lower():
            continue
        if pattern.search(str(comment.get("body") or "")):
            return f"strong active attempt/comment by {author or 'another user'}"
    return ""


def open_competing_prs(repo: str, issue_number: int, login: str, token: str) -> int:
    query = quote(f"repo:{repo} is:pr is:open {issue_number}")
    payload = request_json(f"/search/issues?q={query}&per_page=10", token)
    count = 0
    for item in payload.get("items", []):
        user = item.get("user") if isinstance(item, dict) and isinstance(item.get("user"), dict) else {}
        if str(user.get("login") or "").lower() != login.lower():
            count += 1
    return count


def select_comment(blob: str) -> str:
    if re.search(r"\bassign(ed|ment)?\b|\bplease assign\b", blob):
        return ASSIGNMENT_COMMENT
    return CLAIM_COMMENT


def retract_comment(repo: str, comment: dict[str, Any], token: str) -> str:
    comment_id = comment.get("id")
    if not comment_id:
        return "existing comment had no id"
    try:
        request_json(f"/repos/{repo}/issues/comments/{comment_id}", token, method="PATCH", payload={"body": WITHDRAW_COMMENT})
    except HTTPError as exc:
        return f"withdraw failed: {http_error_message(exc)}"
    return "withdrawn false-positive claim comment"


def claim_candidate(candidate: dict[str, Any], token: str, login: str, state: dict[str, Any]) -> ClaimResult:
    title = str(candidate.get("title") or "Untitled")
    issue_url = str(candidate.get("url") or "")
    parsed = parse_issue(issue_url)
    if not parsed:
        return ClaimResult(title, issue_url, "skipped", message="Not a parseable GitHub issue URL.")
    repo, issue_number = parsed

    issue = request_json(f"/repos/{repo}/issues/{issue_number}", token)
    if issue.get("state") != "open":
        return ClaimResult(title, issue_url, "skipped", message="Issue is not open.")
    if issue.get("pull_request"):
        return ClaimResult(title, issue_url, "skipped", message="This is a pull request, not an issue.")
    assignees = issue.get("assignees") or []
    if assignees:
        return ClaimResult(title, issue_url, "skipped", message="Issue is already assigned.")
    comments_count = int(issue.get("comments") or 0)
    if comments_count > MAX_COMMENTS:
        return ClaimResult(title, issue_url, "skipped", message=f"Issue has too many comments ({comments_count}).")

    comments = request_json(f"/repos/{repo}/issues/{issue_number}/comments?per_page=50", token)
    comments = comments if isinstance(comments, list) else []
    existing = claim_comment_by_us(comments, login)
    paid = has_paid_signal(candidate, issue)
    comment_url = str(existing.get("html_url") or "") if existing else ""
    if not paid:
        if existing:
            message = retract_comment(repo, existing, token)
            state["claims"][issue_url] = {"comment_url": comment_url, "updated_at": now_utc(), "status": "withdrawn_false_positive"}
            return ClaimResult(title, issue_url, "withdrawn_false_positive", comment_url, message)
        return ClaimResult(title, issue_url, "skipped", message=f"No claimable paid signal >= ${MIN_CLAIM_AMOUNT:.0f}.")

    if issue_url in state["claims"] and not existing:
        return ClaimResult(title, issue_url, "already_recorded", state["claims"][issue_url].get("comment_url", ""), "Already recorded in claim state.")

    blob = text_blob(candidate, issue)
    reason = forbidden(blob)
    if reason:
        return ClaimResult(title, issue_url, "skipped", message=f"Forbidden/risky category: {reason}.")

    if existing:
        state["claims"][issue_url] = {"comment_url": comment_url, "updated_at": now_utc(), "status": "already_claimed"}
        return ClaimResult(title, issue_url, "already_claimed", comment_url, "Existing comment by account found.")
    competition = blocking_competition_in_comments(comments, login)
    if competition:
        return ClaimResult(title, issue_url, "skipped", message=competition)
    competing_prs = open_competing_prs(repo, issue_number, login, token)
    if competing_prs > MAX_COMPETING_PRS:
        return ClaimResult(title, issue_url, "skipped", message=f"Too many open competing PRs found: {competing_prs}.")

    try:
        comment = request_json(
            f"/repos/{repo}/issues/{issue_number}/comments",
            token,
            method="POST",
            payload={"body": select_comment(blob)},
        )
    except HTTPError as exc:
        return ClaimResult(title, issue_url, "claim_failed", message=http_error_message(exc))
    new_comment_url = str(comment.get("html_url") or "")
    state["claims"][issue_url] = {"comment_url": new_comment_url, "updated_at": now_utc(), "status": "claimed"}
    return ClaimResult(title, issue_url, "claimed", new_comment_url, "Posted cautious availability comment.")


def claim_sort_key(item: dict[str, Any]) -> tuple[float, int]:
    return amount_value(str(item.get("amount_hint") or "")), int(item.get("score") or 0)


def write_report(results: list[ClaimResult], state: dict[str, Any]) -> None:
    state["updated_at"] = now_utc()
    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = ["# GitHub Bounty Claim Report", "", f"Last run: {now_utc()}", ""]
    if not results:
        lines.extend(["No safe claim target was processed.", ""])
    for result in results:
        lines.extend([
            f"## {result.title}", "",
            f"- Issue: {result.issue_url or 'not available'}",
            f"- Status: {result.status}",
            f"- Comment: {result.comment_url or 'not posted'}",
            f"- Message: {result.message or 'ok'}", "",
        ])
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    token = os.environ.get("BOUNTY_GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or ""
    token = token.strip()
    state = load_state()
    if not token:
        write_report([ClaimResult("Configuration missing", "", "blocked", message="BOUNTY_GITHUB_TOKEN/GH_TOKEN is required to comment on GitHub issues.")], state)
        return 0
    try:
        viewer = request_json("/user", token)
    except HTTPError as exc:
        write_report([ClaimResult("GitHub auth failed", "", "blocked", message=http_error_message(exc))], state)
        return 0
    login = str(viewer.get("login") or "")
    candidates = [item for item in load_candidates() if str(item.get("triage_decision") or "keep").lower() == "keep"]
    candidates.sort(key=claim_sort_key, reverse=True)
    results: list[ClaimResult] = []
    claimed = 0
    for candidate in candidates:
        if claimed >= MAX_CLAIMS:
            break
        result = claim_candidate(candidate, token, login, state)
        results.append(result)
        if result.status == "claimed":
            claimed += 1
    write_report(results, state)
    print(f"Processed {len(results)} claim candidates; claimed {claimed}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
