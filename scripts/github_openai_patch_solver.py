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


CANDIDATES_PATH = Path("bounty_candidates.json")
PATCH_DIR = Path("github_bounty_patches")
REPORT_PATH = Path("github_openai_patch_solver_report.md")
GITHUB_API = "https://api.github.com"
MAX_TASKS = int(os.environ.get("GITHUB_SOLVER_MAX_TASKS", "1"))
MAX_CONTEXT_BYTES = int(os.environ.get("SOLVER_MAX_CONTEXT_BYTES", "70000"))
MAX_FILE_BYTES = int(os.environ.get("SOLVER_MAX_FILE_BYTES", "12000"))


@dataclass
class SolverResult:
    title: str
    status: str
    issue_url: str = ""
    repository: str = ""
    patch_file: str = ""
    metadata_file: str = ""
    message: str = ""
    test_output: str = ""


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def redact(value: str) -> str:
    value = re.sub(r"sk-[A-Za-z0-9_-]+", "[REDACTED]", value)
    value = re.sub(r"gh[pousr]_[A-Za-z0-9_]+", "[REDACTED]", value)
    value = re.sub(r"x-access-token:[^@\s]+@", "x-access-token:[REDACTED]@", value)
    return value


def run(args: list[str], cwd: Path | None = None, timeout: int = 240) -> tuple[int, str]:
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


def github_get(path_or_url: str, token: str | None = None) -> Any:
    url = path_or_url if path_or_url.startswith("https://") else f"{GITHUB_API}{path_or_url}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "bounty-autopilot-github-patch-solver",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(url, headers=headers)
    with urlopen(request, timeout=40) as response:
        raw = response.read().decode("utf-8", errors="replace")
    return json.loads(raw) if raw else {}


def parse_issue(url: str) -> tuple[str, int] | None:
    match = re.search(r"github\.com/([^/]+/[^/]+)/issues/(\d+)", url or "")
    if not match:
        return None
    return match.group(1), int(match.group(2))


def repo_from_url(url: str) -> str:
    match = re.search(r"github\.com/([^/]+/[^/#?]+)", url or "")
    return match.group(1) if match else ""


def slug(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "-", value).strip("-")[:90] or "github-bounty"


def load_candidates() -> list[dict[str, Any]]:
    if not CANDIDATES_PATH.exists():
        return []
    try:
        data = json.loads(CANDIDATES_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def is_candidate(item: dict[str, Any]) -> bool:
    if str(item.get("triage_decision") or "keep").lower() in {"drop", "blocked"}:
        return False
    issue_url = str(item.get("url") or "")
    repo_url = str(item.get("repository_url") or "")
    if not parse_issue(issue_url) or not repo_from_url(repo_url):
        return False
    try:
        score = int(item.get("score") or 0)
    except (TypeError, ValueError):
        score = 0
    return score >= int(os.environ.get("GITHUB_SOLVER_MIN_SCORE", "35"))


def keyword_tokens(text: str) -> list[str]:
    blocked = {"fix", "bug", "issue", "bounty", "reward", "with", "when", "using", "from", "this", "that"}
    tokens: list[str] = []
    for token in re.findall(r"[A-Za-z0-9_]{4,}", text.lower()):
        if token not in blocked and token not in tokens:
            tokens.append(token)
    return tokens[:14]


def candidate_files(repo_dir: Path, keywords: list[str]) -> list[Path]:
    allowed = {".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java", ".rb", ".json", ".toml", ".yaml", ".yml", ".md"}
    ignored = {".git", "node_modules", ".next", "dist", "build", ".venv", "__pycache__", ".pytest_cache", "vendor"}
    scored: list[tuple[int, Path]] = []
    for path in repo_dir.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in allowed:
            continue
        parts = set(path.relative_to(repo_dir).parts)
        if parts & ignored:
            continue
        rel = path.relative_to(repo_dir).as_posix().lower()
        score = sum(3 for token in keywords if token in rel)
        if "test" in rel or "spec" in rel:
            score += 1
        if path.name.lower() in {"package.json", "pyproject.toml", "requirements.txt", "readme.md"}:
            score += 2
        scored.append((score, path))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [path for _, path in scored[:30]]


def build_context(repo_dir: Path, issue: dict[str, Any], item: dict[str, Any], comments: list[dict[str, Any]]) -> str:
    title = str(issue.get("title") or item.get("title") or "")
    body = str(issue.get("body") or "")
    comment_text = "\n\n".join(str(comment.get("body") or "")[:2500] for comment in comments[:8] if isinstance(comment, dict))
    keywords = keyword_tokens(f"{title} {body} {comment_text}")
    chunks = [
        f"Bounty title: {item.get('title') or title}",
        f"Amount hint: {item.get('amount_hint') or ''}",
        f"Issue title: {title}",
        f"Issue body:\n{body[:12000]}",
        f"Recent comments:\n{comment_text[:12000]}",
        "",
        "Repository context:",
    ]
    total = sum(len(chunk.encode("utf-8")) for chunk in chunks)
    for path in candidate_files(repo_dir, keywords):
        rel = path.relative_to(repo_dir).as_posix()
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        block = f"\n--- FILE: {rel} ---\n{text[:MAX_FILE_BYTES]}\n"
        size = len(block.encode("utf-8"))
        if total + size > MAX_CONTEXT_BYTES:
            break
        chunks.append(block)
        total += size
    return "\n".join(chunks)


def model_config() -> tuple[str, str, str]:
    if os.environ.get("OPENAI_API_KEY"):
        return "responses", "https://api.openai.com/v1/responses", os.environ["OPENAI_API_KEY"]
    if os.environ.get("OPENROUTER_API_KEY"):
        return "chat", "https://openrouter.ai/api/v1/chat/completions", os.environ["OPENROUTER_API_KEY"]
    key = os.environ.get("SOLVER_API_KEY") or os.environ.get("AI_API_KEY") or os.environ.get("FREE_AI_API_KEY")
    base = (os.environ.get("SOLVER_BASE_URL") or os.environ.get("OPENAI_BASE_URL") or "").rstrip("/")
    if key and base:
        return "chat", f"{base}/chat/completions", key
    return "", "", ""


def extract_output_text(payload: dict[str, Any]) -> str:
    if isinstance(payload.get("output_text"), str):
        return payload["output_text"]
    choices = payload.get("choices")
    if isinstance(choices, list) and choices:
        message = choices[0].get("message") if isinstance(choices[0], dict) else None
        if isinstance(message, dict) and isinstance(message.get("content"), str):
            return message["content"]
    texts: list[str] = []
    for item in payload.get("output", []):
        if isinstance(item, dict):
            for content in item.get("content", []):
                if isinstance(content, dict) and isinstance(content.get("text"), str):
                    texts.append(content["text"])
    return "\n".join(texts)


def call_solver(context: str) -> dict[str, Any]:
    kind, url, key = model_config()
    if not key:
        raise RuntimeError("No model key configured. Set OPENAI_API_KEY, OPENROUTER_API_KEY, or SOLVER_API_KEY with SOLVER_BASE_URL.")
    model = os.environ.get("GITHUB_SOLVER_MODEL") or os.environ.get("OPENAI_SOLVER_MODEL") or os.environ.get("SOLVER_MODEL") or "gpt-4.1"
    instructions = (
        "You are a senior engineer creating safe, minimal open-source bounty fixes. Return only JSON. "
        "If not confidently solvable, return {\"status\":\"blocked\",\"message\":\"reason\",\"patch\":\"\",\"test_commands\":[]}. "
        "If solvable, return status solved plus a unified git diff patch and test_commands as list of command arrays. "
        "Do not include unrelated refactors, secrets, spam, or misleading claims."
    )
    user_input = f"Create the smallest correct patch for this issue. Include tests when feasible.\n\n{context}"
    if kind == "responses":
        body = {"model": model, "instructions": instructions, "input": user_input}
    else:
        body = {"model": model, "messages": [{"role": "system", "content": instructions}, {"role": "user", "content": user_input}], "temperature": 0.2}
    request = Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        method="POST",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json", "Accept": "application/json"},
    )
    with urlopen(request, timeout=300) as response:
        payload = json.loads(response.read().decode("utf-8", errors="replace"))
    text = extract_output_text(payload).strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.S)
    return json.loads(text)


def test_commands(repo_dir: Path, proposed: Any) -> list[list[str]]:
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


def solve_item(item: dict[str, Any]) -> SolverResult:
    title = str(item.get("title") or "Untitled")
    issue_url = str(item.get("url") or "")
    repo = repo_from_url(str(item.get("repository_url") or ""))
    parsed = parse_issue(issue_url)
    if not parsed:
        return SolverResult(title, "blocked", issue_url, repo, message="No parseable GitHub issue URL.")
    repo = repo or parsed[0]
    issue_number = parsed[1]
    token = os.environ.get("GITHUB_TOKEN")
    issue = github_get(f"/repos/{repo}/issues/{issue_number}", token)
    if issue.get("state") != "open":
        return SolverResult(title, "blocked", issue_url, repo, message="Issue is not open.")
    comments = github_get(f"/repos/{repo}/issues/{issue_number}/comments?per_page=20", token)
    comments = comments if isinstance(comments, list) else []
    with tempfile.TemporaryDirectory(prefix="github-bounty-solver-") as tmp:
        repo_dir = Path(tmp) / "repo"
        code, output = run(["git", "clone", "--depth", "1", f"https://github.com/{repo}.git", str(repo_dir)], timeout=300)
        if code != 0:
            return SolverResult(title, "clone_failed", issue_url, repo, message=output[-2000:])
        context = build_context(repo_dir, issue, item, comments)
        try:
            answer = call_solver(context)
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, RuntimeError) as exc:
            return SolverResult(title, "solver_failed", issue_url, repo, message=redact(str(exc)))
        if str(answer.get("status") or "").lower() != "solved":
            return SolverResult(title, "blocked", issue_url, repo, message=str(answer.get("message") or "Model did not return a solved patch."))
        patch = str(answer.get("patch") or "").strip()
        if "diff --git " not in patch:
            return SolverResult(title, "blocked", issue_url, repo, message="Model returned no git diff patch.")
        candidate_patch = Path(tmp) / "candidate.patch"
        candidate_patch.write_text(patch + "\n", encoding="utf-8")
        code, output = run(["git", "apply", "--check", str(candidate_patch)], cwd=repo_dir)
        if code != 0:
            return SolverResult(title, "patch_rejected", issue_url, repo, message=output[-2000:])
        code, output = run(["git", "apply", str(candidate_patch)], cwd=repo_dir)
        if code != 0:
            return SolverResult(title, "patch_apply_failed", issue_url, repo, message=output[-2000:])
        output_all = ""
        for command in test_commands(repo_dir, answer.get("test_commands")):
            code, output = run(command, cwd=repo_dir, timeout=600)
            output_all += f"$ {' '.join(command)}\n{output[-3000:]}\n"
            if code != 0:
                return SolverResult(title, "tests_failed", issue_url, repo, message="Patch applied but tests failed.", test_output=output_all)
        code, diff = run(["git", "diff", "--binary"], cwd=repo_dir)
        if code != 0 or not diff.strip():
            return SolverResult(title, "blocked", issue_url, repo, message="No diff remained after patch application.")
        PATCH_DIR.mkdir(exist_ok=True)
        base = slug(f"{repo}-{issue_number}")
        patch_path = PATCH_DIR / f"{base}.patch"
        meta_path = PATCH_DIR / f"{base}.json"
        patch_path.write_text(diff, encoding="utf-8")
        meta = {
            "repo": repo,
            "issue_number": issue_number,
            "patch": patch_path.as_posix(),
            "pr_title": str(answer.get("pr_title") or f"Fix issue #{issue_number}"),
            "pr_body": str(answer.get("message") or f"Fixes #{issue_number}.\n\nVerification: see automated solver report."),
            "commit_message": str(answer.get("commit_message") or f"Fix issue #{issue_number}"),
            "test_commands": test_commands(repo_dir, answer.get("test_commands")),
        }
        meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return SolverResult(title, "patch_ready", issue_url, repo, patch_path.as_posix(), meta_path.as_posix(), str(answer.get("message") or "Patch generated."), output_all.strip())


def write_report(results: list[SolverResult]) -> None:
    lines = ["# GitHub OpenAI Patch Solver", "", f"Last run: {now_utc()}", ""]
    if not results:
        lines.extend(["No GitHub bounty candidates were processed.", ""])
    for index, result in enumerate(results, 1):
        lines.extend([
            f"## {index}. {result.title}", "",
            f"- Status: {result.status}",
            f"- Repository: {result.repository or 'not available'}",
            f"- Issue: {result.issue_url or 'not available'}",
            f"- Patch: {result.patch_file or 'not ready'}",
            f"- Metadata: {result.metadata_file or 'not ready'}",
            f"- Message: {result.message or 'ok'}", "",
        ])
        if result.test_output:
            lines.extend(["### Test Output", "", "```text", result.test_output[-4000:], "```", ""])
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    candidates = [item for item in load_candidates() if is_candidate(item)]
    results = [solve_item(item) for item in candidates[:MAX_TASKS]]
    if not candidates and not model_config()[2]:
        results = [SolverResult("Configuration missing", "not_configured", message="Set OPENAI_API_KEY, OPENROUTER_API_KEY, or SOLVER_API_KEY with SOLVER_BASE_URL for online patch generation.")]
    write_report(results)
    print(f"Processed {len(results)} GitHub bounty solver candidates.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
