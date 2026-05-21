from __future__ import annotations

import json
import os
import re
import subprocess
import tempfile
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


TASKS_PATH = Path("taskbounty_tasks.json")
PATCH_DIR = Path("taskbounty_patches")
REPORT_PATH = Path("openai_patch_solver_report.md")
OPENAI_API_URL = "https://api.openai.com/v1/responses"
GITHUB_API = "https://api.github.com"
MAX_CONTEXT_BYTES = int(os.environ.get("SOLVER_MAX_CONTEXT_BYTES", "70000"))
MAX_FILE_BYTES = int(os.environ.get("SOLVER_MAX_FILE_BYTES", "12000"))
MAX_TASKS = int(os.environ.get("SOLVER_MAX_TASKS", "1"))


@dataclass
class SolverResult:
    task_id: str
    title: str
    status: str
    repo_url: str = ""
    issue_url: str = ""
    patch_file: str = ""
    message: str = ""
    test_output: str = ""


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def redact(value: str) -> str:
    value = re.sub(r"tb_live_[A-Za-z0-9]+", "[REDACTED]", value)
    value = re.sub(r"sk-[A-Za-z0-9_-]+", "[REDACTED]", value)
    value = re.sub(r"x-access-token:[^@\s]+@", "x-access-token:[REDACTED]@", value)
    return value


def run(args: list[str], cwd: Path | None = None, timeout: int = 180) -> tuple[int, str]:
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


def load_tasks() -> list[dict[str, Any]]:
    if not TASKS_PATH.exists():
        return []
    try:
        data = json.loads(TASKS_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def github_get(path_or_url: str, token: str | None = None) -> Any:
    url = path_or_url if path_or_url.startswith("https://") else f"{GITHUB_API}{path_or_url}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "bounty-autopilot-openai-patch-solver",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(url, headers=headers)
    with urlopen(request, timeout=30) as response:
        raw = response.read().decode("utf-8", errors="replace")
    return json.loads(raw) if raw else {}


def parse_issue(issue_url: str) -> tuple[str, int] | None:
    match = re.search(r"github\.com/([^/]+/[^/]+)/issues/(\d+)", issue_url)
    if not match:
        return None
    return match.group(1), int(match.group(2))


def is_candidate(task: dict[str, Any]) -> bool:
    if not task.get("task_id") or not task.get("github_repo_url") or not task.get("github_issue_url"):
        return False
    if str(task.get("status") or "").upper() not in {"", "OPEN"}:
        return False
    if str(task.get("triage_decision") or "candidate").lower() in {"blocked"}:
        return False
    try:
        score = int(task.get("score") or 0)
    except (TypeError, ValueError):
        score = 0
    return score >= int(os.environ.get("TASKBOUNTY_SOLVER_MIN_SCORE", "5"))


def keyword_tokens(text: str) -> list[str]:
    blocked = {
        "fix",
        "bug",
        "issue",
        "open",
        "task",
        "with",
        "when",
        "using",
        "from",
        "admin",
        "submission",
    }
    tokens = []
    for token in re.findall(r"[A-Za-z0-9_]{4,}", text.lower()):
        if token not in blocked and token not in tokens:
            tokens.append(token)
    return tokens[:12]


def candidate_files(repo_dir: Path, keywords: list[str]) -> list[Path]:
    allowed = {".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java", ".rb", ".json", ".toml", ".yaml", ".yml"}
    ignored = {".git", "node_modules", ".next", "dist", "build", ".venv", "__pycache__", ".pytest_cache"}
    files: list[Path] = []
    for path in repo_dir.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in allowed:
            continue
        parts = set(path.relative_to(repo_dir).parts)
        if parts & ignored:
            continue
        rel = path.relative_to(repo_dir).as_posix().lower()
        if keywords and not any(token in rel for token in keywords):
            continue
        files.append(path)
        if len(files) >= 20:
            break
    if files:
        return files
    for path in repo_dir.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in allowed:
            continue
        parts = set(path.relative_to(repo_dir).parts)
        if parts & ignored:
            continue
        files.append(path)
        if len(files) >= 25:
            break
    return files


def build_context(repo_dir: Path, issue: dict[str, Any], task: dict[str, Any]) -> str:
    title = str(task.get("title") or issue.get("title") or "")
    body = str(issue.get("body") or task.get("summary") or "")
    keywords = keyword_tokens(f"{title} {body}")
    files = candidate_files(repo_dir, keywords)
    chunks = [
        f"Task title: {title}",
        f"Task summary: {task.get('summary') or ''}",
        f"Issue title: {issue.get('title') or ''}",
        f"Issue body:\n{body[:12000]}",
        "",
        "Repository files:",
    ]
    total = sum(len(chunk.encode("utf-8")) for chunk in chunks)
    for path in files:
        rel = path.relative_to(repo_dir).as_posix()
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        text = text[:MAX_FILE_BYTES]
        block = f"\n--- FILE: {rel} ---\n{text}\n"
        size = len(block.encode("utf-8"))
        if total + size > MAX_CONTEXT_BYTES:
            break
        chunks.append(block)
        total += size
    return "\n".join(chunks)


def extract_output_text(payload: dict[str, Any]) -> str:
    if isinstance(payload.get("output_text"), str):
        return payload["output_text"]
    texts: list[str] = []
    for item in payload.get("output", []):
        if not isinstance(item, dict):
            continue
        for content in item.get("content", []):
            if isinstance(content, dict) and isinstance(content.get("text"), str):
                texts.append(content["text"])
    return "\n".join(texts)


def call_openai(context: str, api_key: str) -> dict[str, Any]:
    model = os.environ.get("OPENAI_SOLVER_MODEL") or "gpt-4.1"
    instructions = (
        "You are a senior software engineer producing safe, minimal patches for open-source bounty tasks. "
        "Return only JSON. If the task cannot be solved confidently from the provided context, return "
        '{"status":"blocked","message":"reason","patch":"","test_commands":[]}. '
        "If solvable, return a unified git diff patch in the patch field. Do not include secrets, tokens, "
        "private data, spam, or unrelated refactors."
    )
    body = {
        "model": model,
        "instructions": instructions,
        "input": (
            "Create the smallest correct patch for this task. Include regression tests when feasible. "
            "Return JSON with keys: status, message, patch, test_commands. test_commands must be a list of command arrays.\n\n"
            f"{context}"
        ),
    }
    request = Request(
        OPENAI_API_URL,
        data=json.dumps(body).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    with urlopen(request, timeout=240) as response:
        payload = json.loads(response.read().decode("utf-8", errors="replace"))
    text = extract_output_text(payload).strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.S)
    return json.loads(text)


def choose_test_command(repo_dir: Path, proposed: Any) -> list[list[str]]:
    commands: list[list[str]] = []
    if isinstance(proposed, list):
        for command in proposed:
            if isinstance(command, list) and command and all(isinstance(part, str) for part in command):
                commands.append(command)
    if commands:
        return commands[:3]
    if (repo_dir / "pyproject.toml").exists() or (repo_dir / "pytest.ini").exists():
        return [["python", "-m", "pytest", "-q"]]
    if (repo_dir / "package.json").exists():
        return [["npm", "test", "--", "--runInBand"]]
    return []


def solve_task(task: dict[str, Any], api_key: str) -> SolverResult:
    task_id = str(task.get("task_id") or "")
    title = str(task.get("title") or "")
    repo_url = str(task.get("github_repo_url") or "")
    issue_url = str(task.get("github_issue_url") or "")
    parsed = parse_issue(issue_url)
    if not parsed:
        return SolverResult(task_id, title, "blocked", repo_url, issue_url, message="No parseable GitHub issue URL.")

    repo, issue_number = parsed
    token = os.environ.get("GITHUB_TOKEN")
    issue = github_get(f"/repos/{repo}/issues/{issue_number}", token=token)
    if issue.get("state") != "open":
        return SolverResult(task_id, title, "blocked", repo_url, issue_url, message="GitHub issue is not open.")

    with tempfile.TemporaryDirectory(prefix="openai-patch-solver-") as tmp:
        repo_dir = Path(tmp) / "repo"
        code, output = run(["git", "clone", "--depth", "1", f"{repo_url}.git", str(repo_dir)], timeout=240)
        if code != 0:
            return SolverResult(task_id, title, "clone_failed", repo_url, issue_url, message=output[-2000:])

        context = build_context(repo_dir, issue, task)
        try:
            answer = call_openai(context, api_key)
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
            return SolverResult(task_id, title, "solver_failed", repo_url, issue_url, message=redact(str(exc)))

        if str(answer.get("status") or "").lower() != "solved":
            return SolverResult(
                task_id,
                title,
                "blocked",
                repo_url,
                issue_url,
                message=str(answer.get("message") or "Model did not return a solved patch."),
            )

        patch = str(answer.get("patch") or "").strip()
        if "diff --git " not in patch:
            return SolverResult(task_id, title, "blocked", repo_url, issue_url, message="Model returned no git diff patch.")

        patch_path = Path(tmp) / "candidate.patch"
        patch_path.write_text(patch + "\n", encoding="utf-8")
        code, output = run(["git", "apply", "--check", str(patch_path)], cwd=repo_dir)
        if code != 0:
            return SolverResult(task_id, title, "patch_rejected", repo_url, issue_url, message=output[-2000:])
        code, output = run(["git", "apply", str(patch_path)], cwd=repo_dir)
        if code != 0:
            return SolverResult(task_id, title, "patch_apply_failed", repo_url, issue_url, message=output[-2000:])

        test_output = ""
        for command in choose_test_command(repo_dir, answer.get("test_commands")):
            code, output = run(command, cwd=repo_dir, timeout=300)
            test_output += f"$ {' '.join(command)}\n{output[-3000:]}\n"
            if code != 0:
                return SolverResult(task_id, title, "tests_failed", repo_url, issue_url, message="Patch applied but tests failed.", test_output=test_output)

        code, diff = run(["git", "diff", "--binary"], cwd=repo_dir)
        if code != 0 or not diff.strip():
            return SolverResult(task_id, title, "blocked", repo_url, issue_url, message="No diff remained after applying patch.")

        PATCH_DIR.mkdir(exist_ok=True)
        final_patch = PATCH_DIR / f"{task_id}.patch"
        final_patch.write_text(diff, encoding="utf-8")
        return SolverResult(
            task_id,
            title,
            "patch_ready",
            repo_url,
            issue_url,
            patch_file=final_patch.as_posix(),
            message=str(answer.get("message") or "Patch generated and validated."),
            test_output=test_output.strip(),
        )


def write_report(results: list[SolverResult]) -> None:
    lines = [
        "# OpenAI Patch Solver",
        "",
        f"Last run: {now_utc()}",
        "",
        "This solver tries to turn a clear public TaskBounty GitHub issue into a ready patch file for the TaskBounty worker.",
        "",
    ]
    if not results:
        lines.extend(["No solver candidates were processed.", ""])
    for index, result in enumerate(results, start=1):
        lines.extend(
            [
                f"## {index}. {result.title or result.task_id}",
                "",
                f"- Status: {result.status}",
                f"- Task ID: {result.task_id or 'not available'}",
                f"- Repo: {result.repo_url or 'not available'}",
                f"- Issue: {result.issue_url or 'not available'}",
                f"- Patch: {result.patch_file or 'not ready'}",
                f"- Message: {result.message or 'ok'}",
                "",
            ]
        )
        if result.test_output:
            lines.extend(["### Test Output", "", "```text", result.test_output[-4000:], "```", ""])
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        write_report(
            [
                SolverResult(
                    "",
                    "Configuration missing",
                    "not_configured",
                    message="OPENAI_API_KEY is required for online autonomous patch generation.",
                )
            ]
        )
        return 0

    candidates = [task for task in load_tasks() if is_candidate(task)]
    results = [solve_task(task, api_key) for task in candidates[:MAX_TASKS]]
    write_report(results)
    print(f"Wrote {len(results)} OpenAI patch solver results.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
