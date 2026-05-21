from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPORT_PATH = Path("AUTOPILOT_HEALTH.md")
STATUS_PATH = Path("autopilot_health.json")
GITHUB_API = "https://api.github.com"
REPOSITORY = os.environ.get("GITHUB_REPOSITORY", "asaadnashed/bounty-autopilot")
STALE_MINUTES = int(os.environ.get("AUTOPILOT_STALE_MINUTES", "45"))


@dataclass
class Check:
    name: str
    status: str
    detail: str


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def read_text(path: str) -> str:
    p = Path(path)
    if not p.exists():
        return ""
    return p.read_text(encoding="utf-8", errors="replace")


def load_json(path: str) -> Any:
    p = Path(path)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def has_secret(name: str) -> bool:
    return bool(os.environ.get(name, "").strip())


def github_token() -> str:
    return (
        os.environ.get("BOUNTY_GITHUB_TOKEN")
        or os.environ.get("GH_TOKEN")
        or os.environ.get("GITHUB_TOKEN")
        or ""
    ).strip()


def report_timestamp(text: str) -> datetime | None:
    match = re.search(r"Last (?:built|run):\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}) UTC", text or "")
    if not match:
        return None
    try:
        return datetime.strptime(match.group(1), "%Y-%m-%d %H:%M").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def report_age_minutes(path: str) -> int | None:
    timestamp = report_timestamp(read_text(path))
    if not timestamp:
        return None
    return int((utc_now() - timestamp).total_seconds() // 60)


def dispatch_workflow(workflow_file: str) -> str:
    token = github_token()
    if not token:
        return "dispatch skipped: missing GitHub token"
    url = f"{GITHUB_API}/repos/{REPOSITORY}/actions/workflows/{workflow_file}/dispatches"
    body = json.dumps({"ref": "main"}).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "bounty-autopilot-health-dispatcher",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=45):
            return "dispatch sent"
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        return f"dispatch failed: HTTP {exc.code}: {detail[:300]}"
    except urllib.error.URLError as exc:
        return f"dispatch failed: {exc.reason}"


def dispatch_if_stale(name: str, report_path: str, workflow_file: str, checks: list[Check]) -> None:
    age = report_age_minutes(report_path)
    if age is None:
        status = "missing"
        detail = f"{report_path} has no parseable timestamp; {dispatch_workflow(workflow_file)}."
    elif age > STALE_MINUTES:
        status = "degraded"
        detail = f"{report_path} is stale ({age} minutes old); {dispatch_workflow(workflow_file)}."
    else:
        status = "ok"
        detail = f"{report_path} is fresh ({age} minutes old)."
    checks.append(Check(name, status, detail))


def status_from_report(text: str, *, local_solver_fallback: bool = False) -> str:
    if not text:
        return "missing"
    lowered = text.lower()
    missing_model = (
        "openai_api_key is required" in lowered
        or "no model key configured" in lowered
        or "configuration missing" in lowered
        or "not_configured" in lowered
    )
    if missing_model:
        return "degraded" if local_solver_fallback else "blocked"
    if "patch_ready" in lowered or "submitted" in lowered or "pr_opened" in lowered or "claimed" in lowered:
        return "active"
    if "access_failed" in lowered or "blocked" in lowered or "no solver candidates" in lowered or "claim_failed" in lowered:
        return "degraded"
    return "ok"


def count_files(pattern: str) -> int:
    return len(list(Path(".").glob(pattern)))


def extract_prs(text: str) -> list[str]:
    return sorted(set(re.findall(r"https://github\.com/[^\s)]+/pull/\d+", text)))


def extract_comments(text: str) -> list[str]:
    return sorted(set(re.findall(r"https://github\.com/[^\s)]+/issues/\d+#issuecomment-\d+", text)))


def main() -> int:
    checks: list[Check] = []

    bounty_token = has_secret("BOUNTY_GITHUB_TOKEN") or has_secret("GH_TOKEN") or has_secret("GITHUB_TOKEN")
    checks.append(
        Check(
            "GitHub interaction token",
            "ok" if bounty_token else "blocked",
            "Token available for comments, fork, push, and PR submission."
            if bounty_token
            else "Missing token for GitHub comments, fork, push, and PR submission.",
        )
    )

    dispatch_if_stale("Bounty scout scheduler", "bounty_worker_queue.md", "bounty-scout.yml", checks)
    dispatch_if_stale("GitHub claimer scheduler", "github_bounty_claim_report.md", "github-bounty-claim.yml", checks)
    dispatch_if_stale("GitHub submitter scheduler", "github_bounty_submission_report.md", "github-bounty-submit.yml", checks)
    dispatch_if_stale("TaskBounty scout scheduler", "taskbounty_scout_report.md", "taskbounty-scout.yml", checks)
    dispatch_if_stale("TaskBounty worker scheduler", "taskbounty_worker_report.md", "taskbounty-worker.yml", checks)

    model_ready = has_secret("OPENAI_API_KEY") or has_secret("OPENROUTER_API_KEY") or (has_secret("SOLVER_API_KEY") and has_secret("SOLVER_BASE_URL"))
    checks.append(
        Check(
            "Online model solver key",
            "ok" if model_ready else "degraded",
            "Online patch solver can call a model."
            if model_ready
            else "GitHub Actions cannot generate new code patches without a model key. Local Codex automation is configured as the solving fallback.",
        )
    )

    taskbounty_ready = has_secret("TASKBOUNTY_API_KEY") and has_secret("TASKBOUNTY_AGENT_ID")
    checks.append(
        Check(
            "TaskBounty credentials",
            "ok" if taskbounty_ready else "degraded",
            "TaskBounty API and agent id are available."
            if taskbounty_ready
            else "TaskBounty scanning/submission may be limited without API key and agent id.",
        )
    )

    claim_report = read_text("github_bounty_claim_report.md")
    claim_status = status_from_report(claim_report)
    comments = extract_comments(claim_report)
    checks.append(Check("GitHub bounty claimer", claim_status, f"Comments tracked: {len(comments)}" if comments else "No claim comments tracked yet."))

    github_solver_report = read_text("github_openai_patch_solver_report.md")
    checks.append(
        Check(
            "GitHub patch solver report",
            status_from_report(github_solver_report, local_solver_fallback=True),
            "Latest report parsed; local Codex is fallback if online model key is missing."
            if github_solver_report
            else "No GitHub patch solver report yet.",
        )
    )

    task_solver_report = read_text("openai_patch_solver_report.md")
    checks.append(
        Check(
            "TaskBounty patch solver report",
            status_from_report(task_solver_report, local_solver_fallback=True),
            "Latest report parsed; local Codex is fallback if online model key is missing."
            if task_solver_report
            else "No TaskBounty patch solver report yet.",
        )
    )

    submitter_report = read_text("github_bounty_submission_report.md")
    submitter_status = status_from_report(submitter_report)
    prs = extract_prs(submitter_report)
    checks.append(Check("GitHub bounty submitter", submitter_status, f"PRs tracked: {len(prs)}" if prs else "No PRs tracked in submitter report."))

    worker_report = read_text("taskbounty_worker_report.md")
    checks.append(Check("TaskBounty worker", status_from_report(worker_report), "Worker report exists." if worker_report else "No worker report yet."))

    github_patch_count = count_files("github_bounty_patches/*.patch")
    task_patch_count = count_files("taskbounty_patches/*.patch")
    checks.append(Check("Ready patch files", "ok" if github_patch_count or task_patch_count else "watching", f"GitHub patches: {github_patch_count}; TaskBounty patches: {task_patch_count}."))

    candidates = load_json("bounty_candidates.json") or []
    task_candidates = load_json("taskbounty_tasks.json") or []
    checks.append(Check("Candidate feeds", "ok" if candidates or task_candidates else "watching", f"GitHub candidates: {len(candidates) if isinstance(candidates, list) else 0}; TaskBounty candidates: {len(task_candidates) if isinstance(task_candidates, list) else 0}."))

    severities = {"blocked": 4, "degraded": 3, "watching": 2, "missing": 2, "ok": 1, "active": 1}
    worst = max(checks, key=lambda item: severities.get(item.status, 0)).status if checks else "unknown"
    if any(check.status == "active" for check in checks) and worst not in {"blocked"}:
        overall = "active"
    elif worst == "blocked":
        overall = "blocked"
    elif worst in {"degraded", "missing"}:
        overall = "degraded"
    else:
        overall = "watching"

    data = {
        "updated_at": now_utc(),
        "overall": overall,
        "checks": [check.__dict__ for check in checks],
        "tracked_prs": prs,
        "tracked_comments": comments,
    }
    STATUS_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = ["# Autopilot Health", "", f"Last run: {data['updated_at']}", "", f"Overall: `{overall}`", ""]
    if overall == "blocked":
        lines.extend(["The automation has a blocker that prevents unattended execution.", ""])
    elif overall == "active":
        lines.extend(["The automation has active work in flight, claim comments, or ready submission paths.", ""])
    elif overall == "degraded":
        lines.extend(["The automation can still scout, solve locally through Codex, submit ready patches, and follow up; at least one online capability is degraded.", ""])
    else:
        lines.extend(["The automation is watching for the next suitable opportunity.", ""])

    lines.extend(["## Checks", ""])
    for check in checks:
        lines.append(f"- `{check.status}` {check.name}: {check.detail}")
    if comments:
        lines.extend(["", "## Tracked Comments", ""])
        for comment in comments:
            lines.append(f"- {comment}")
    if prs:
        lines.extend(["", "## Tracked PRs", ""])
        for pr in prs:
            lines.append(f"- {pr}")
    lines.append("")
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Autopilot health: {overall}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
