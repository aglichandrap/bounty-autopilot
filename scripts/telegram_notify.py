#!/usr/bin/env python3
"""Send concise Arabic bounty-autopilot status updates to Telegram."""

from __future__ import annotations

import os
import pathlib
import re
import sys
import urllib.parse
import urllib.request

MAX_MESSAGE_CHARS = 3900
MAX_SUMMARY_LINES = 14

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


def _read_file(path: str) -> str:
    file_path = pathlib.Path(path.strip())
    if not file_path.exists() or not file_path.is_file():
        return ""
    return file_path.read_text(encoding="utf-8", errors="replace").strip()


def _first_match(pattern: str, text: str, default: str = "غير معروف") -> str:
    match = re.search(pattern, text, flags=re.I | re.M)
    return match.group(1).strip() if match else default


def _count(pattern: str, text: str) -> int:
    return len(re.findall(pattern, text, flags=re.I | re.M))


def _clean_title(title: str) -> str:
    return re.sub(r"^#+\s*", "", title).strip()


def _extract_queue_items(text: str) -> list[tuple[str, str, str]]:
    items: list[tuple[str, str, str]] = []
    sections = re.split(r"\n## Queue Item \d+: ", text)
    for section in sections[1:]:
        title = _clean_title(section.splitlines()[0])
        issue = _first_match(r"^- Issue:\s*(.+)$", section, "")
        amount = _first_match(r"^- Amount hint:\s*(.+)$", section, "غير واضح")
        items.append((title, amount, issue))
    return items


def _summarize_bounty_queue(text: str) -> list[str]:
    last = _first_match(r"^Last built:\s*(.+)$", text)
    items = _extract_queue_items(text)
    if not items:
        return [f"طابور GitHub: لا يوجد فرصة قابلة للشغل حاليا. آخر فحص: {last}"]
    lines = [f"طابور GitHub: {len(items)} فرصة. آخر فحص: {last}"]
    for title, amount, issue in items[:3]:
        lines.append(f"- {title} | {amount} | {issue}")
    if len(items) > 3:
        lines.append(f"- وفيه {len(items) - 3} فرص إضافية بالطابور.")
    return lines


def _summarize_taskbounty_report(text: str) -> list[str]:
    last = _first_match(r"^Last run:\s*(.+)$", text)
    sections = re.split(r"\n## \d+\. ", text)
    tasks = []
    for section in sections[1:]:
        title = _clean_title(section.splitlines()[0])
        amount = _first_match(r"^- Amount hint:\s*(.+)$", section, "غير واضح")
        status = _first_match(r"^- Status:\s*(.+)$", section, "غير معروف")
        task_url = _first_match(r"^- Task:\s*(https?://\S+)", section, "")
        tasks.append((title, amount, status, task_url))
    if not tasks:
        return [f"بحث TaskBounty: لا توجد مهام مناسبة حاليا. آخر فحص: {last}"]
    lines = [f"بحث TaskBounty: {len(tasks)} مهمة. آخر فحص: {last}"]
    for title, amount, status, task_url in tasks[:3]:
        lines.append(f"- {title} | {amount} | {status} | {task_url}")
    return lines


def _summarize_claim_report(text: str) -> list[str]:
    last = _first_match(r"^Last run:\s*(.+)$", text)
    claimed = _count(r"^- Status:\s*claimed\b", text)
    skipped = _count(r"^- Status:\s*skipped\b", text)
    lines = [f"تعليقات GitHub: {claimed} تعليق جديد، {skipped} تخطي. آخر تشغيل: {last}"]
    comments = re.findall(r"^- Comment:\s*(https?://\S+)", text, flags=re.M)
    if comments:
        lines.append(f"- رابط التعليق: {comments[0]}")
    messages = re.findall(r"^- Message:\s*(.+)$", text, flags=re.M)
    for message in messages[:2]:
        if "strong active" in message.lower():
            lines.append("- تم تخطي فرصة لأن فيها محاولة قوية قبلنا.")
        elif "posted" in message.lower():
            lines.append("- تم نشر تعليق حذر على فرصة مفتوحة.")
    return lines


def _summarize_patch_solver(text: str) -> list[str]:
    last = _first_match(r"^Last run:\s*(.+)$", text)
    queued = _count(r"^- Status:\s*local_fallback_queued\b", text)
    ready = _count(r"^- Patch:\s*(?!not ready).+", text)
    lines = [f"حل الكود: {queued} مهمة بانتظار Codex المحلي، patches جاهزة: {ready}. آخر تشغيل: {last}"]
    if "No online model key is configured" in text:
        lines.append("- GitHub Actions لا يولد كود أونلاين بدون model key؛ الاعتماد الحالي على Codex المحلي عند الحاجة.")
    first_issue = _first_match(r"^- Issue:\s*(https?://\S+)", text, "")
    if first_issue:
        lines.append(f"- أول مهمة تنتظر فحص كود: {first_issue}")
    return lines


def _summarize_taskbounty_worker(text: str) -> list[str]:
    last = _first_match(r"^Last run:\s*(.+)$", text)
    failed_409 = _count(r"submit_failed_409", text)
    submitted = _count(r"^- Status:\s*(submitted|accepted|success)\b", text)
    lines = [f"TaskBounty: submitted/accepted={submitted}، أخطاء 409={failed_409}. آخر تشغيل: {last}"]
    if failed_409:
        lines.append("- خطأ 409 من منصة TaskBounty نفسها، التقرير يقول إنهم يعيدونها تلقائيا.")
    task = _first_match(r"^- Task:\s*(https?://\S+)", text, "")
    if task:
        lines.append(f"- المهمة: {task}")
    return lines


def _summarize_taskbounty_triage(text: str) -> list[str]:
    decision = _first_match(r"^- Decision:\s*(.+)$", text, "غير معروف")
    reasons = re.findall(r"^- Reason:\s*(.+)$", text, flags=re.M)
    lines = [f"فرز TaskBounty: القرار {decision}."]
    if reasons:
        lines.append("- السبب: " + "؛ ".join(reasons[:3]))
    return lines


def _summarize_health(text: str) -> list[str]:
    last = _first_match(r"^Last run:\s*(.+)$", text)
    overall = _first_match(r"^Overall:\s*`?([^`\n]+)`?", text)
    degraded = re.findall(r"^- `degraded`\s*([^:]+):\s*(.+)$", text, flags=re.M)
    lines = [f"صحة النظام: {overall}. آخر فحص: {last}"]
    for name, message in degraded[:2]:
        lines.append(f"- تنبيه: {name.strip()} - {message.strip()}")
    return lines


def _summarize_pr_followup(text: str) -> list[str]:
    last = _first_match(r"^Last run:\s*(.+)$", text)
    announced = _count(r"^## already_announced", text)
    skipped = _count(r"^## skipped", text)
    posted = _count(r"^- Comment:\s*https?://", text)
    return [f"متابعة PR/Issue: معلن سابقا={announced}، تخطي={skipped}، تعليقات جديدة={posted}. آخر تشغيل: {last}"]


def _summarize_submission_report(text: str) -> list[str]:
    last = _first_match(r"^Last run:\s*(.+)$", text)
    submitted = _count(r"^- Status:\s*(submitted|opened|created|ready)\b", text)
    skipped = _count(r"^- Status:\s*skipped\b", text)
    failed = _count(r"^- Status:\s*(failed|error)\b", text)
    prs = re.findall(r"^- PR:\s*(https?://\S+)", text, flags=re.M)
    lines = [f"إرسال PRs: جديد={submitted}، تخطي={skipped}، فشل={failed}. آخر تشغيل: {last}"]
    if prs:
        lines.append(f"- آخر PR: {prs[0]}")
    elif submitted == 0 and failed == 0:
        lines.append("- لا يوجد PR جديد في هذه الجولة.")
    return lines


def _summarize_generic(path: str, text: str) -> list[str]:
    if path.endswith("taskbounty_report.md"):
        return _summarize_taskbounty_report(text)
    if path.endswith("bounty_worker_queue.md"):
        return _summarize_bounty_queue(text)
    if path.endswith("github_bounty_claim_report.md"):
        return _summarize_claim_report(text)
    if path.endswith("github_openai_patch_solver_report.md") or path.endswith("openai_patch_solver_report.md"):
        return _summarize_patch_solver(text)
    if path.endswith("taskbounty_worker_report.md"):
        return _summarize_taskbounty_worker(text)
    if path.endswith("taskbounty_triage_report.md"):
        return _summarize_taskbounty_triage(text)
    if path.endswith("AUTOPILOT_HEALTH.md"):
        return _summarize_health(text)
    if path.endswith("github_pr_issue_announcement_report.md"):
        return _summarize_pr_followup(text)
    if path.endswith("github_bounty_submission_report.md"):
        return _summarize_submission_report(text)
    heading = _first_match(r"^#\s*(.+)$", text, pathlib.Path(path).name)
    last = _first_match(r"^Last (?:run|built):\s*(.+)$", text, "")
    suffix = f" آخر تحديث: {last}" if last else ""
    return [f"{heading}.{suffix}"]


def _arabic_title(title: str) -> str:
    lowered = title.lower()
    for key, value in TITLE_AR.items():
        if lowered.startswith(key.lower()):
            return value
    for key, value in sorted(TITLE_AR.items(), key=lambda item: len(item[0]), reverse=True):
        if key.lower() in lowered:
            return value
    return title


def _build_message() -> str:
    raw_title = os.getenv("TELEGRAM_TITLE", "Bounty autopilot update").strip()
    title = _arabic_title(raw_title)
    status = STATUS_AR.get(os.getenv("TELEGRAM_STATUS", "updated").strip().lower(), os.getenv("TELEGRAM_STATUS", "updated").strip())
    run_url = os.getenv("GITHUB_RUN_URL") or (
        f"https://github.com/{os.getenv('GITHUB_REPOSITORY', '')}/actions/runs/{os.getenv('GITHUB_RUN_ID', '')}"
        if os.getenv("GITHUB_REPOSITORY") and os.getenv("GITHUB_RUN_ID")
        else ""
    )
    custom_message = os.getenv("TELEGRAM_MESSAGE", "").strip()
    report_files = [p.strip() for p in os.getenv("TELEGRAM_REPORT_FILES", "").split(",") if p.strip()]

    lines = [f"تحديث الباونتي: {title}", f"الحالة: {status}"]
    if custom_message:
        lines.append(f"الخلاصة: {custom_message}")

    summary_lines: list[str] = []
    for report_file in report_files:
        text = _read_file(report_file)
        if text:
            summary_lines.extend(_summarize_generic(report_file, text))

    if summary_lines:
        lines.append("الخلاصة:")
        lines.extend(summary_lines[:MAX_SUMMARY_LINES])
    else:
        lines.append("الخلاصة: لا يوجد تقرير قابل للقراءة في هذه الجولة.")

    if run_url:
        lines.append(f"الرن: {run_url}")

    if os.getenv("TELEGRAM_INCLUDE_RAW_REPORTS", "0") == "1":
        for report_file in report_files:
            text = _read_file(report_file)
            if text:
                lines.append(f"\n--- {report_file} ---\n{text[:900].rstrip()}" + ("\n..." if len(text) > 900 else ""))

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

    message = _build_message()
    data = urllib.parse.urlencode(
        {
            "chat_id": chat_id,
            "text": message,
            "disable_web_page_preview": "true",
        }
    ).encode("utf-8")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    request = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            print(response.read().decode("utf-8", errors="replace"))
    except Exception as exc:  # noqa: BLE001 - notifications must not block bounty work.
        print(f"Telegram notification failed: {exc}", file=sys.stderr)
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
