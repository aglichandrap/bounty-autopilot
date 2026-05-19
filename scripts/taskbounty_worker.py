from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


BASE_URL = os.environ.get("TASKBOUNTY_BASE_URL", "https://www.task-bounty.com").rstrip("/")
API_BASE = f"{BASE_URL}/api/v1"
TASKS_PATH = Path("taskbounty_tasks.json")
REPORT_PATH = Path("taskbounty_worker_report.md")
STATE_PATH = Path("taskbounty_worker_state.json")
AGENT_STATE_PATH = Path("taskbounty_agent_state.json")
PATCH_DIR = Path(os.environ.get("TASKBOUNTY_PATCH_DIR", "taskbounty_patches"))


@dataclass
class WorkerResult:
    task_id: str
    title: str
    amount_hint: str
    task_url: str
    status: str
    repo_url: str | None = None
    repo_profile: dict[str, Any] | None = None
    submission_id: str | None = None
    message: str = ""


def redact(value: str) -> str:
    value = re.sub(r"tb_live_[A-Za-z0-9]+", "[REDACTED]", value)
    value = re.sub(r"x-access-token:[^@\\s]+@", "x-access-token:[REDACTED]@", value)
    return value


def is_uuid(value: str) -> bool:
    try:
        uuid.UUID(value)
    except (TypeError, ValueError):
        return False
    return True


def load_state_agent_id() -> str:
    if not AGENT_STATE_PATH.exists():
        return ""
    try:
        data = json.loads(AGENT_STATE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return ""
    agent_id = str(data.get("agent_id") or "").strip() if isinstance(data, dict) else ""
    return agent_id if is_uuid(agent_id) else ""


def save_state_agent_id(agent_id: str, source: str) -> None:
    AGENT_STATE_PATH.write_text(
        json.dumps(
            {
                "agent_id": agent_id,
                "source": source,
                "updated_at": datetime.now(timezone.utc).isoformat(),
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )


def api_request(path: str, token: str, method: str = "GET", body: dict[str, Any] | None = None) -> dict[str, Any]:
    data = None if body is None else json.dumps(body).encode("utf-8")
    request = Request(
        f"{API_BASE}{path}",
        data=data,
        method=method,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
            "User-Agent": "bounty-autopilot-taskbounty-worker",
        },
    )
    with urlopen(request, timeout=60) as response:
        raw = response.read().decode("utf-8", errors="replace")
    if not raw:
        return {}
    return json.loads(raw)


def register_agent(token: str) -> str:
    payload = api_request(
        "/agents",
        token=token,
        method="POST",
        body={
            "name": os.environ.get("TASKBOUNTY_AGENT_NAME", "AsaadCode"),
            "skills": ["Python", "JavaScript", "GitHub Actions", "Bug fixes", "APIs"],
        },
    )
    data = payload.get("data", payload)
    if not isinstance(data, dict):
        return ""
    agent_id = str(data.get("id") or data.get("agent_id") or data.get("agentId") or "").strip()
    return agent_id if is_uuid(agent_id) else ""


def resolve_agent_id(token: str) -> tuple[str, str]:
    secret_agent_id = os.environ.get("TASKBOUNTY_AGENT_ID", "").strip()
    if is_uuid(secret_agent_id):
        save_state_agent_id(secret_agent_id, "secret")
        return secret_agent_id, "secret"

    state_agent_id = load_state_agent_id()
    if state_agent_id:
        return state_agent_id, "state"

    agent_id = register_agent(token)
    if agent_id:
        save_state_agent_id(agent_id, "created")
        return agent_id, "created"
    return "", "missing"


def load_tasks() -> list[dict[str, Any]]:
    if not TASKS_PATH.exists():
        return []
    try:
        data = json.loads(TASKS_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def run_command(args: list[str], cwd: Path | None = None, timeout: int = 120) -> tuple[int, str]:
    completed = subprocess.run(
        args,
        cwd=str(cwd) if cwd else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )
    return completed.returncode, redact(completed.stdout)


def repo_profile(repo_dir: Path) -> dict[str, Any]:
    paths: list[str] = []
    for path in repo_dir.rglob("*"):
        if len(paths) >= 120:
            break
        if not path.is_file():
            continue
        rel = path.relative_to(repo_dir).as_posix()
        if rel.startswith(".git/") or "/.git/" in rel:
            continue
        if any(part in {".next", "node_modules", "dist", "build", ".venv", "__pycache__"} for part in rel.split("/")):
            continue
        paths.append(rel)

    markers = {
        "package.json": (repo_dir / "package.json").exists(),
        "pyproject.toml": (repo_dir / "pyproject.toml").exists(),
        "requirements.txt": (repo_dir / "requirements.txt").exists(),
        "Cargo.toml": (repo_dir / "Cargo.toml").exists(),
        "go.mod": (repo_dir / "go.mod").exists(),
    }
    languages = sorted(
        {
            Path(path).suffix.lower().lstrip(".")
            for path in paths
            if Path(path).suffix.lower() in {".py", ".js", ".ts", ".tsx", ".go", ".rs", ".java", ".rb"}
        }
    )
    return {"markers": markers, "languages": languages, "sample_files": paths[:80]}


def github_repo_from_task(task: dict[str, Any]) -> str:
    repo_url = str(task.get("github_repo_url") or "").strip()
    if repo_url.startswith("https://github.com/"):
        return repo_url.rstrip("/")

    text = " ".join(
        str(task.get(key) or "")
        for key in ("summary", "reason", "title", "url", "github_issue_url")
    )
    issue_url_match = re.search(r"https://github\.com/([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)/issues/\d+", text)
    if issue_url_match:
        return f"https://github.com/{issue_url_match.group(1)}"

    repo_match = re.search(r"issue\s+#\d+.*?\bin\s+([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)", text, flags=re.I)
    if repo_match:
        return f"https://github.com/{repo_match.group(1).rstrip('.')}"

    repo_match = re.search(r"\bin\s+([A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+).*?issue\s+#\d+", text, flags=re.I)
    if repo_match:
        return f"https://github.com/{repo_match.group(1).rstrip('.')}"
    return ""


def clone_profile_public_repo(task: dict[str, Any], result: WorkerResult) -> WorkerResult:
    repo_url = github_repo_from_task(task)
    if not repo_url:
        result.message = "Access failed and no public GitHub repo was exposed by the task."
        return result

    result.repo_url = repo_url
    clone_url = f"{repo_url}.git"
    with tempfile.TemporaryDirectory(prefix="taskbounty-public-") as tmp:
        repo_dir = Path(tmp) / "repo"
        code, output = run_command(["git", "clone", "--depth", "1", clone_url, str(repo_dir)], timeout=180)
        if code != 0:
            result.status = "public_clone_failed"
            result.message = output[-2000:]
            return result
        result.repo_profile = repo_profile(repo_dir)
        result.status = "public_workspace_prepared"
        result.message = "TaskBounty access endpoint had no GitHub installation, but the public upstream repo was cloned and profiled. A patch can still be submitted through /submissions/patch."
        return result


def request_access(task_id: str, agent_id: str, token: str) -> dict[str, Any]:
    payload = api_request(
        f"/tasks/{task_id}/access",
        token=token,
        method="POST",
        body={"agent_id": agent_id},
    )
    data = payload.get("data", payload)
    return data if isinstance(data, dict) else {}


def submit_patch(task: dict[str, Any], token: str, agent_id: str, patch_file: Path) -> dict[str, Any]:
    patch = patch_file.read_text(encoding="utf-8")
    body = {
        "task_id": task["task_id"],
        "agent_id": agent_id,
        "result_text": f"Automated patch submission for {task.get('title', 'TaskBounty task')}.",
        "patch": patch,
    }
    payload = api_request("/submissions/patch", token=token, method="POST", body=body)
    data = payload.get("data", payload)
    return data if isinstance(data, dict) else {}


def process_task(task: dict[str, Any], token: str, agent_id: str, clone_repos: bool) -> WorkerResult:
    result = WorkerResult(
        task_id=str(task.get("task_id") or ""),
        title=str(task.get("title") or "Untitled TaskBounty task"),
        amount_hint=str(task.get("amount_hint") or ""),
        task_url=str(task.get("url") or ""),
        status="pending",
    )
    if not result.task_id:
        result.status = "skipped"
        result.message = "Task has no task_id."
        return result

    triage_decision = str(task.get("triage_decision") or "").lower()
    if triage_decision in {"blocked", "crowded", "hard"}:
        result.status = f"triage_skipped_{triage_decision}"
        reasons = task.get("triage_reasons")
        if isinstance(reasons, list) and reasons:
            result.message = "; ".join(str(reason) for reason in reasons[:4])
        else:
            result.message = "Skipped by TaskBounty triage."
        return result

    patch_file = PATCH_DIR / f"{result.task_id}.patch"
    if patch_file.exists():
        try:
            submission = submit_patch(task, token, agent_id, patch_file)
            result.status = "submitted_patch"
            result.submission_id = str(submission.get("submission_id") or submission.get("id") or "")
            result.message = f"Submitted patch file {patch_file.as_posix()}."
            return result
        except HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            result.status = f"submit_failed_{exc.code}"
            result.message = redact(body or str(exc))
            return result

    try:
        access = request_access(result.task_id, agent_id, token)
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        result.status = f"access_failed_{exc.code}"
        result.message = redact(body or str(exc))
        if exc.code == 409 and "no GitHub installation" in body:
            return clone_profile_public_repo(task, result)
        return result
    except (URLError, TimeoutError, json.JSONDecodeError) as exc:
        result.status = "access_failed"
        result.message = redact(str(exc))
        return result

    result.repo_url = access.get("repoUrl")
    clone_url = access.get("cloneUrl")
    if not clone_url:
        result.status = "access_ready"
        result.message = "Access returned no cloneUrl; task may be public or not a code task."
        return result

    if not clone_repos:
        result.status = "access_ready"
        result.message = "Repo access is ready. No patch file exists yet."
        return result

    with tempfile.TemporaryDirectory(prefix="taskbounty-worker-") as tmp:
        repo_dir = Path(tmp) / "repo"
        code, output = run_command(["git", "clone", "--depth", "1", clone_url, str(repo_dir)], timeout=180)
        if code != 0:
            result.status = "clone_failed"
            result.message = output[-2000:]
            return result
        result.repo_profile = repo_profile(repo_dir)
        result.status = "workspace_prepared"
        result.message = "Repo access succeeded and workspace profile was generated. No patch file exists yet."
        return result


def write_outputs(results: list[WorkerResult]) -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    STATE_PATH.write_text(
        json.dumps([asdict(result) for result in results], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    lines = [
        "# TaskBounty Worker",
        "",
        f"Last run: {now}",
        "",
        "This worker is the execution layer after scouting: it uses the TaskBounty agent API, requests repo access, prepares a workspace profile, and submits a patch when a matching `taskbounty_patches/<task_id>.patch` file exists.",
        "",
    ]
    if not results:
        lines.extend(["No TaskBounty tasks were available to process.", ""])
    for index, result in enumerate(results, start=1):
        lines.extend(
            [
                f"## {index}. {result.title}",
                "",
                f"- Amount: {result.amount_hint}",
                f"- Task: {result.task_url}",
                f"- Task ID: {result.task_id}",
                f"- Status: {result.status}",
                f"- Repo: {result.repo_url or 'not available'}",
            ]
        )
        if result.submission_id:
            lines.append(f"- Submission ID: {result.submission_id}")
        if result.message:
            lines.append(f"- Message: {result.message}")
        if result.repo_profile:
            markers = ", ".join(name for name, exists in result.repo_profile.get("markers", {}).items() if exists)
            languages = ", ".join(result.repo_profile.get("languages", []))
            lines.extend(
                [
                    f"- Detected stack markers: {markers or 'none'}",
                    f"- Detected languages: {languages or 'unknown'}",
                    "",
                    "### Sample Files",
                    "",
                ]
            )
            for path in result.repo_profile.get("sample_files", [])[:30]:
                lines.append(f"- `{path}`")
        lines.append("")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    token = os.environ.get("TASKBOUNTY_API_KEY", "").strip()
    if not token:
        write_outputs(
            [
                WorkerResult(
                    task_id="",
                    title="Configuration missing",
                    amount_hint="",
                    task_url="",
                    status="not_configured",
                    message="TASKBOUNTY_API_KEY is required.",
                )
            ]
        )
        return 0

    try:
        agent_id, agent_source = resolve_agent_id(token)
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        write_outputs(
            [
                WorkerResult(
                    task_id="",
                    title="Agent setup failed",
                    amount_hint="",
                    task_url="",
                    status=f"agent_failed_{exc.code}",
                    message=redact(body or str(exc)),
                )
            ]
        )
        return 0
    except (URLError, TimeoutError, json.JSONDecodeError) as exc:
        write_outputs(
            [
                WorkerResult(
                    task_id="",
                    title="Agent setup failed",
                    amount_hint="",
                    task_url="",
                    status="agent_failed",
                    message=redact(str(exc)),
                )
            ]
        )
        return 0

    if not agent_id:
        write_outputs(
            [
                WorkerResult(
                    task_id="",
                    title="Agent configuration missing",
                    amount_hint="",
                    task_url="",
                    status="not_configured",
                    message="Could not resolve or create a valid TaskBounty agent id.",
                )
            ]
        )
        return 0

    tasks = load_tasks()
    max_tasks = int(os.environ.get("TASKBOUNTY_WORKER_MAX_TASKS", "2"))
    clone_repos = os.environ.get("TASKBOUNTY_CLONE_REPOS", "1") == "1"
    results = [process_task(task, token, agent_id, clone_repos) for task in tasks[:max_tasks]]
    write_outputs(results)
    print(f"Wrote {len(results)} TaskBounty worker results using agent source: {agent_source}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
