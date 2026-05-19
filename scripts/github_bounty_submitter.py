from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.request import Request, urlopen


API = "https://api.github.com"
PATCH_DIR = Path("github_bounty_patches")
STATE_PATH = Path("github_bounty_submission_state.json")
REPORT_PATH = Path("github_bounty_submission_report.md")


@dataclass
class SubmissionResult:
    target: str
    issue_url: str
    status: str
    pr_url: str | None = None
    message: str = ""


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


def http_error_message(exc: HTTPError) -> str:
    try:
        body = exc.read().decode("utf-8", errors="replace")
    except Exception:
        body = ""
    return f"HTTP {exc.code}: {body or exc.reason}"


def request_json(path: str, token: str | None = None, method: str = "GET", payload: dict[str, Any] | None = None) -> Any:
    data = None
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "bounty-autopilot-submitter",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = Request(f"{API}{path}", data=data, headers=headers, method=method)
    with urlopen(request, timeout=60) as response:
        text = response.read().decode("utf-8", errors="replace")
        return json.loads(text) if text else {}


def read_public_json(path: str, token: str | None) -> Any:
    try:
        return request_json(path, token)
    except HTTPError as exc:
        if exc.code not in {403, 404}:
            raise
        return request_json(path, None)


def request_empty(path: str, token: str, method: str = "PUT") -> None:
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "Content-Length": "0",
        "User-Agent": "bounty-autopilot-submitter",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    request = Request(f"{API}{path}", data=b"", headers=headers, method=method)
    with urlopen(request, timeout=60) as response:
        response.read()


def run(command: list[str], cwd: Path, token: str | None = None) -> str:
    if token and command and command[0] == "git" and command[1] in {"clone", "push", "fetch"}:
        command = ["git", "-c", f"http.extraHeader=Authorization: Bearer {token}"] + command[1:]
    completed = subprocess.run(
        command,
        cwd=str(cwd),
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return completed.stdout


def load_state() -> dict[str, Any]:
    if not STATE_PATH.exists():
        return {"submissions": {}}
    try:
        state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"submissions": {}}
    if not isinstance(state, dict):
        return {"submissions": {}}
    state.setdefault("submissions", {})
    return state


def metadata_files() -> list[Path]:
    if not PATCH_DIR.exists():
        return []
    return sorted(PATCH_DIR.glob("*.json"))


def validate_metadata(meta: dict[str, Any]) -> tuple[str, int, Path]:
    repo = str(meta.get("repo") or "")
    issue_number = int(meta.get("issue_number") or 0)
    patch_path = Path(str(meta.get("patch") or ""))
    if not repo or "/" not in repo:
        raise ValueError("metadata repo must be owner/name")
    if issue_number <= 0:
        raise ValueError("metadata issue_number must be positive")
    if not patch_path.exists():
        raise ValueError(f"patch file is missing: {patch_path}")
    return repo, issue_number, patch_path


def apply_and_submit(meta_path: Path, token: str, actor_login: str, state: dict[str, Any]) -> SubmissionResult:
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    repo, issue_number, patch_path = validate_metadata(meta)
    issue_url = f"https://github.com/{repo}/issues/{issue_number}"
    key = f"{repo}#{issue_number}:{patch_path}"
    existing = state["submissions"].get(key)
    if existing and existing.get("pr_url"):
        return SubmissionResult(repo, issue_url, "already_submitted", existing.get("pr_url"))

    issue = read_public_json(f"/repos/{repo}/issues/{issue_number}", token)
    issue_url = issue.get("html_url", issue_url)
    if issue.get("state") != "open":
        return SubmissionResult(repo, issue_url, "skipped", message="issue is not open")

    repo_info = read_public_json(f"/repos/{repo}", token)
    default_branch = str(repo_info.get("default_branch") or "main")
    _, name = repo.split("/", 1)
    branch = str(meta.get("branch") or f"bounty-{issue_number}-{int(time.time())}")

    body_text = str(issue.get("body") or "").lower()
    if meta.get("star_required") or "must star" in body_text:
        try:
            request_empty(f"/user/starred/{repo}", token, method="PUT")
        except HTTPError as exc:
            return SubmissionResult(repo, issue_url, "blocked", message=f"token cannot star required repo: {http_error_message(exc)}")

    try:
        request_json(f"/repos/{repo}/forks", token, method="POST", payload={})
    except HTTPError as exc:
        if exc.code not in {202, 422}:
            return SubmissionResult(repo, issue_url, "blocked", message=f"token cannot fork repo: {http_error_message(exc)}")

    fork = None
    for _ in range(24):
        try:
            fork = request_json(f"/repos/{actor_login}/{name}", token)
            break
        except HTTPError as exc:
            if exc.code != 404:
                return SubmissionResult(repo, issue_url, "blocked", message=f"cannot read fork: {http_error_message(exc)}")
            time.sleep(5)
    if not fork:
        return SubmissionResult(repo, issue_url, "blocked", message="fork was not available after waiting")

    open_prs = read_public_json(f"/repos/{repo}/pulls?state=all&head={actor_login}:{branch}", token)
    if isinstance(open_prs, list) and open_prs:
        pr_url = open_prs[0].get("html_url")
        state["submissions"][key] = {"pr_url": pr_url, "updated_at": now_utc()}
        return SubmissionResult(repo, issue_url, "already_submitted", pr_url)

    work_root = Path(tempfile.mkdtemp(prefix="github-bounty-submit-"))
    try:
        clone_dir = work_root / name
        run(["git", "clone", "--depth", "1", "--branch", default_branch, f"https://github.com/{actor_login}/{name}.git", str(clone_dir)], work_root, token=token)
        run(["git", "checkout", "-b", branch], clone_dir)
        run(["git", "apply", "--check", str((Path.cwd() / patch_path).resolve())], clone_dir)
        run(["git", "apply", str((Path.cwd() / patch_path).resolve())], clone_dir)

        for command in meta.get("test_commands", []):
            if not isinstance(command, list) or not command:
                continue
            run([str(part) for part in command], clone_dir)

        run(["git", "config", "user.name", "asaadnashed"], clone_dir)
        run(["git", "config", "user.email", "asaadnashed@users.noreply.github.com"], clone_dir)
        run(["git", "add", "."], clone_dir)
        run(["git", "commit", "-m", str(meta.get("commit_message") or f"Fix issue #{issue_number}")], clone_dir)
        run(["git", "push", "origin", branch], clone_dir, token=token)

        pr_body = str(meta.get("pr_body") or "")
        if not pr_body:
            pr_body = f"Fixes #{issue_number}.\n\nVerification: see commit notes and automated checks."
        pr = request_json(
            f"/repos/{repo}/pulls",
            token,
            method="POST",
            payload={
                "title": str(meta.get("pr_title") or f"Fix issue #{issue_number}"),
                "head": f"{actor_login}:{branch}",
                "base": default_branch,
                "body": pr_body,
                "maintainer_can_modify": True,
            },
        )
        pr_url = pr.get("html_url")
        state["submissions"][key] = {"pr_url": pr_url, "updated_at": now_utc()}
        return SubmissionResult(repo, issue_url, "submitted", pr_url)
    finally:
        shutil.rmtree(work_root, ignore_errors=True)


def write_report(results: list[SubmissionResult], state: dict[str, Any]) -> None:
    state["updated_at"] = now_utc()
    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = ["# GitHub Bounty Submission Report", "", f"Last run: {now_utc()}", ""]
    if not results:
        lines.extend(["No patch metadata files were ready for submission.", ""])
    for result in results:
        lines.extend(
            [
                f"## {result.target}",
                "",
                f"- Issue: {result.issue_url}",
                f"- Status: {result.status}",
                f"- PR: {result.pr_url or 'not created'}",
                f"- Message: {result.message or 'ok'}",
                "",
            ]
        )
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    token = os.environ.get("BOUNTY_GITHUB_TOKEN")
    if not token:
        write_report([SubmissionResult("github", "", "blocked", message="BOUNTY_GITHUB_TOKEN is not configured")], load_state())
        return 0

    actor = request_json("/user", token)
    actor_login = str(actor.get("login") or "")
    if not actor_login:
        raise RuntimeError("Could not resolve GitHub actor login from token")

    state = load_state()
    results: list[SubmissionResult] = []
    for meta_path in metadata_files():
        try:
            results.append(apply_and_submit(meta_path, token, actor_login, state))
        except Exception as exc:
            results.append(SubmissionResult(str(meta_path), "", "error", message=str(exc)))
    write_report(results, state)
    for result in results:
        print(asdict(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
