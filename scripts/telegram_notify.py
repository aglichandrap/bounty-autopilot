#!/usr/bin/env python3
"""Send concise Arabic bounty-autopilot status updates to Telegram.

The workflows run often and most runs only refresh timestamps. This notifier is
intentionally quiet unless there is something actionable: a posted claim, a new
PR/submission, a maintainer/reviewer follow-up, a ready patch, a real failure, or
a health problem that needs the owner.
"""

from __future__ import annotations

import os
import pathlib
import re
import sys
import urllib.parse
import urllib.request

MAX_MESSAGE_CHARS = 3900

TITLE_AR = {
    "TaskBounty Worker": "عامل TaskBounty",
    "TaskBounty Scout": "بحث TaskBounty",
    "GitHub Bounty Submitter": "إرسال PRs",
    "GitHub Bounty Claimer": "تعليقات GitHub",
    "Bounty Scout": "بحث فرص GitHub",
    "PR/Issue Follow-up": "متابعة PR/Issue",
    "Autopilot Health": "صحة النظام",
}

STATUS_AR = {
    "updated": "تحديث جديد",
    "failure": "فشل ويحتاج انتباه",
    "success": "نجح",
}

QUIET_MESSAGES = (
    "no actionable bounty",
    "no safe claim target",
    "no eligible github bounty candidates",
    "no strong candidates",
    "forbidden/risky category: content-only",
    "strong active attempt/comment",
    "already_submitted",
    "triage_skipped_blocked",
    "no github issue url exposed",
)


def read_file(path: str) -> str:
    file_path = pathlib.Path(path.strip())
    if not file_path.exists() or not file_path.is_file():
        return ""
    return file_path.read_text(encoding="utf-8", errors="replace").strip()


def first(pattern: str, text: str, default: str = "غير معروف") -> str:
    match = re.search(pattern, text, flags=re.I | re.M)
    return match.group(1).strip() if match else default


def count(pattern: str, text: str) -> int:
    return len(re.findall(pattern, text, flags=re.I | re.M))


def arabic_title(title: str) -> str:
    lowered = title.lower()
    for key, value in TITLE_AR.items():
        if lowered.startswith(key.lower()) or key.lower() in lowered:
            return value
    return title


def report_files() -> list[str]:
    return [p.strip() for p in os.getenv("TELEGRAM_REPORT_FILES", "").split(",") if p.strip()]


def reports_text() -> str:
    return "\n\n".join(read_file(path) for path in report_files())


def patch_values(text: str) -> list[str]:
    values = re.findall(r"^- Patch:\s*(.+)$", text, flags=re.I | re.M)
    return [value.strip() for value in values if value.strip() and value.strip().lower() != "not ready"]


def has_real_health_problem(text: str) -> bool:
    if re.search(r"^Overall:\s*`?(blocked|failed|error)`,?", text, flags=re.I | re.M):
        return True
    degraded_lines = re.findall(r"^- `degraded`\s*([^:]+):\s*(.+)$", text, flags=re.I | re.M)
    for name, message in degraded_lines:
        combined = f"{name} {message}".lower()
        if "scheduler" in combined or "dispatch sent" in combined or "online model" in combined:
            continue
        return True
    return False


def is_actionable(title: str, status: str, text: str) -> bool:
    lowered = text.lower()
    if status == "failure" or "failed" in title.lower():
        return True
    if os.getenv("TELEGRAM_FORCE_SEND", "0") == "1":
        return True
    if os.getenv("TELEGRAM_MESSAGE", "").strip():
        return True

    if "github_bounty_claim_report.md" in ",".join(report_files()):
        return bool(re.search(r"^- Status:\s*(claimed|claim_failed|blocked)\b", text, flags=re.I | re.M))

    if "github_bounty_submission_report.md" in ",".join(report_files()):
        return bool(re.search(r"^- Status:\s*(submitted|opened|created|ready|failed|error)\b", text, flags=re.I | re.M))

    if "github_pr_issue_announcement_report.md" in ",".join(report_files()):
        return bool(re.search(r"^- Comment:\s*https?://", text, flags=re.I | re.M))

    if "taskbounty_worker_report.md" in ",".join(report_files()):
        if re.search(r"^- Status:\s*(submitted|accepted|success)\b", text, flags=re.I | re.M):
            return True
        return bool(re.search(r"submit_failed_(?!409)\d+", text, flags=re.I))

    if "github_openai_patch_solver_report.md" in ",".join(report_files()) or "openai_patch_solver_report.md" in ",".join(report_files()):
        return bool(patch_values(text))

    if "bounty_worker_queue.md" in ",".join(report_files()):
        # Scout output changes constantly. Keep Telegram quiet unless explicitly enabled.
        return os.getenv("TELEGRAM_NOTIFY_QUEUE", "0") == "1" and "## Queue Item" in text

    if "AUTOPILOT_HEALTH.md" in ",".join(report_files()):
        return has_real_health_problem(text)

    if all(message in lowered for message in ("no actionable", "no eligible")):
        return False
    if any(message in lowered for message in QUIET_MESSAGES):
        return False
    return False


def queue_summary(text: str) -> list[str]:
    last = first(r"^Last built:\s*(.+)$", text)
    items = re.findall(r"^## Queue Item \d+:\s*(.+)$", text, flags=re.M)
    if not items:
        return [f"طابور GitHub: لا توجد فرصة قابلة للشغل حاليا. آخر فحص: {last}"]
    lines = [f"طابور GitHub: {len(items)} فرصة قابلة للفحص. آخر فحص: {last}"]
    for title in items[:3]:
        lines.append(f"- {title.strip()}")
    return lines


def claim_summary(text: str) -> list[str]:
    last = first(r"^Last run:\s*(.+)$", text)
    claimed = count(r"^- Status:\s*claimed\b", text)
    failed = count(r"^- Status:\s*claim_failed\b", text)
    blocked = count(r"^- Status:\s*blocked\b", text)
    lines = [f"تعليقات GitHub: claimed={claimed}، failed={failed}، blocked={blocked}. آخر تشغيل: {last}"]
    comment = first(r"^- Comment:\s*(https?://\S+)", text, "")
    if comment:
        lines.append(f"- التعليق: {comment}")
    issue = first(r"^- Issue:\s*(https?://\S+)", text, "")
    if issue:
        lines.append(f"- الفرصة: {issue}")
    return lines


def submission_summary(text: str) -> list[str]:
    last = first(r"^Last run:\s*(.+)$", text)
    new_count = count(r"^- Status:\s*(submitted|opened|created|ready)\b", text)
    failed = count(r"^- Status:\s*(failed|error)\b", text)
    lines = [f"إرسال PRs: جديد={new_count}، فشل={failed}. آخر تشغيل: {last}"]
    prs = re.findall(r"^- PR:\s*(https?://\S+)", text, flags=re.M)
    if prs:
        lines.append(f"- PR: {prs[0]}")
    return lines


def patch_summary(text: str) -> list[str]:
    last = first(r"^Last run:\s*(.+)$", text)
    ready = patch_values(text)
    queued = count(r"^- Status:\s*local_fallback_queued\b", text)
    lines = [f"حل الكود: queued={queued}، patches جاهزة={len(ready)}. آخر تشغيل: {last}"]
    if ready:
        lines.append(f"- أول patch جاهز: {ready[0]}")
    return lines


def taskbounty_worker_summary(text: str) -> list[str]:
    last = first(r"^Last run:\s*(.+)$", text)
    accepted = count(r"^- Status:\s*(submitted|accepted|success)\b", text)
    failed_non_409 = count(r"submit_failed_(?!409)\d+", text)
    lines = [f"TaskBounty: submitted/accepted={accepted}، أخطاء مهمة={failed_non_409}. آخر تشغيل: {last}"]
    task = first(r"^- Task:\s*(https?://\S+)", text, "")
    if task:
        lines.append(f"- المهمة: {task}")
    return lines


def health_summary(text: str) -> list[str]:
    last = first(r"^Last run:\s*(.+)$", text)
    overall = first(r"^Overall:\s*`?([^`\n]+)`?", text)
    lines = [f"صحة النظام: {overall}. آخر فحص: {last}"]
    for name, message in re.findall(r"^- `degraded`\s*([^:]+):\s*(.+)$", text, flags=re.M)[:3]:
        combined = f"{name} {message}".lower()
        if "scheduler" in combined or "dispatch sent" in combined or "online model" in combined:
            continue
        lines.append(f"- تنبيه: {name.strip()} - {message.strip()}")
    return lines


def followup_summary(text: str) -> list[str]:
    last = first(r"^Last run:\s*(.+)$", text)
    posted = count(r"^- Comment:\s*https?://", text)
    return [f"متابعة PR/Issue: تعليقات جديدة={posted}. آخر تشغيل: {last}"]


def generic_summary(path: str, text: str) -> list[str]:
    if path.endswith("bounty_worker_queue.md"):
        return queue_summary(text)
    if path.endswith("github_bounty_claim_report.md"):
        return claim_summary(text)
    if path.endswith("github_bounty_submission_report.md"):
        return submission_summary(text)
    if path.endswith("github_openai_patch_solver_report.md") or path.endswith("openai_patch_solver_report.md"):
        return patch_summary(text)
    if path.endswith("taskbounty_worker_report.md"):
        return taskbounty_worker_summary(text)
    if path.endswith("AUTOPILOT_HEALTH.md"):
        return health_summary(text)
    if path.endswith("github_pr_issue_announcement_report.md"):
        return followup_summary(text)
    heading = first(r"^#\s*(.+)$", text, pathlib.Path(path).name)
    return [heading]


def build_message(title: str, status: str, text: str) -> str:
    lines = [f"تحديث الباونتي: {arabic_title(title)}", f"الحالة: {STATUS_AR.get(status, status)}"]
    custom = os.getenv("TELEGRAM_MESSAGE", "").strip()
    if custom:
        lines.append(f"الخلاصة: {custom}")
    summary: list[str] = []
    for path in report_files():
        report = read_file(path)
        if report:
            summary.extend(generic_summary(path, report))
    if summary:
        lines.append("الخلاصة:")
        lines.extend(summary[:10])
    run_url = os.getenv("GITHUB_RUN_URL", "").strip()
    if run_url:
        lines.append(f"الرن: {run_url}")
    message = "\n".join(lines).strip()
    if len(message) > MAX_MESSAGE_CHARS:
        message = message[:MAX_MESSAGE_CHARS].rstrip() + "\n..."
    return message


def main() -> int:
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "").strip()
    if not token or not chat_id:
        print("Telegram secrets are not configured; skipping notification.")
        return 0

    title = os.getenv("TELEGRAM_TITLE", "Bounty autopilot update").strip()
    status = os.getenv("TELEGRAM_STATUS", "updated").strip().lower()
    text = reports_text()
    if not is_actionable(title, status, text):
        print("Telegram update is not actionable; skipping notification.")
        return 0

    message = build_message(title, status, text)
    data = urllib.parse.urlencode(
        {
            "chat_id": chat_id,
            "text": message,
            "disable_web_page_preview": "true",
        }
    ).encode("utf-8")
    request = urllib.request.Request(f"https://api.telegram.org/bot{token}/sendMessage", data=data, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            print(response.read().decode("utf-8", errors="replace"))
    except Exception as exc:  # noqa: BLE001 - notifications must not block bounty work.
        print(f"Telegram notification failed: {exc}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
