from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


REPORT_PATH = Path("AUTOPILOT_HEALTH.md")
STATUS_PATH = Path("autopilot_health.json")


@dataclass
class Check:
    name: str
    status: str
    detail: str


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


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


def status_from_report(text: str) -> str:
    if not text:
        return "missing"
    lowered = text.lower()
    if "not_configured" in lowered or "configuration missing" in lowered:
        return "blocked"
    if "patch_ready" in lowered or "submitted" in lowered or "pr_opened" in lowered:
        return "active"
    if "access_failed" in lowered or "blocked" in lowered or "no solver candidates" in lowered:
        return "degraded"
    return "ok"


def count_files(pattern: str) -> int:
    return len(list(Path(".").glob(pattern)))


def extract_prs(text: str) -> list[str]:
    return sorted(set(re.findall(r"https://github\.com/[^\s)]+/pull/\d+", text)))


def main() -> int:
    checks: list[Check] = []

    bounty_token = has_secret("BOUNTY_GITHUB_TOKEN") or has_secret("GH_TOKEN") or has_secret("GITHUB_TOKEN")
    checks.append(Check("GitHub PR submit token", "ok" if bounty_token else "blocked", "BOUNTY_GITHUB_TOKEN/GH_TOKEN available" if bounty_token else "Missing token for fork, push, and PR submission."))

    model_ready = has_secret("OPENAI_API_KEY") or has_secret("OPENROUTER_API_KEY") or (has_secret("SOLVER_API_KEY") and has_secret("SOLVER_BASE_URL"))
    checks.append(Check("Online model solver key", "ok" if model_ready else "degraded", "Online patch solver can call a model." if model_ready else "GitHub Actions cannot generate new code patches without OPENAI_API_KEY, OPENROUTER_API_KEY, or SOLVER_API_KEY+SOLVER_BASE_URL. Local Codex automation is the fallback."))

    taskbounty_ready = has_secret("TASKBOUNTY_API_KEY") and has_secret("TASKBOUNTY_AGENT_ID")
    checks.append(Check("TaskBounty credentials", "ok" if taskbounty_ready else "degraded", "TaskBounty API and agent id are available." if taskbounty_ready else "TaskBounty scanning/submission may be limited without API key and agent id."))

    github_solver_report = read_text("github_openai_patch_solver_report.md")
    checks.append(Check("GitHub patch solver report", status_from_report(github_solver_report), "Latest report parsed." if github_solver_report else "No GitHub patch solver report yet."))

    task_solver_report = read_text("openai_patch_solver_report.md")
    checks.append(Check("TaskBounty patch solver report", status_from_report(task_solver_report), "Latest report parsed." if task_solver_report else "No TaskBounty patch solver report yet."))

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
    }
    STATUS_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = ["# Autopilot Health", "", f"Last run: {data['updated_at']}", "", f"Overall: `{overall}`", ""]
    if overall == "blocked":
        lines.extend(["The automation has at least one blocker that prevents full unattended execution.", ""])
    elif overall == "active":
        lines.extend(["The automation has active work in flight or ready submission paths.", ""])
    elif overall == "degraded":
        lines.extend(["The automation can still scout/follow up, but at least one capability is degraded.", ""])
    else:
        lines.extend(["The automation is watching for the next suitable opportunity.", ""])

    lines.extend(["## Checks", ""])
    for check in checks:
        lines.append(f"- `{check.status}` {check.name}: {check.detail}")
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
