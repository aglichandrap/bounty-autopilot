#!/usr/bin/env python3
"""Send concise bounty-autopilot status updates to Telegram.

The script is intentionally dependency-free so GitHub Actions can run it from any
workflow without installing packages.
"""

from __future__ import annotations

import os
import pathlib
import sys
import urllib.parse
import urllib.request

MAX_MESSAGE_CHARS = 3900
MAX_FILE_CHARS = 900


def _read_file(path: str) -> str:
    file_path = pathlib.Path(path.strip())
    if not file_path.exists() or not file_path.is_file():
        return ""
    text = file_path.read_text(encoding="utf-8", errors="replace").strip()
    if len(text) <= MAX_FILE_CHARS:
        return text
    return text[:MAX_FILE_CHARS].rstrip() + "\n..."


def _build_message() -> str:
    title = os.getenv("TELEGRAM_TITLE", "Bounty autopilot update").strip()
    run_url = os.getenv("GITHUB_RUN_URL") or (
        f"https://github.com/{os.getenv('GITHUB_REPOSITORY', '')}/actions/runs/{os.getenv('GITHUB_RUN_ID', '')}"
        if os.getenv("GITHUB_REPOSITORY") and os.getenv("GITHUB_RUN_ID")
        else ""
    )
    status = os.getenv("TELEGRAM_STATUS", "updated").strip()
    custom_message = os.getenv("TELEGRAM_MESSAGE", "").strip()
    report_files = [p.strip() for p in os.getenv("TELEGRAM_REPORT_FILES", "").split(",") if p.strip()]

    parts = [f"{title}", f"Status: {status}"]
    if run_url:
        parts.append(f"Run: {run_url}")
    if custom_message:
        parts.append(custom_message)

    for report_file in report_files:
        snippet = _read_file(report_file)
        if snippet:
            parts.append(f"\n--- {report_file} ---\n{snippet}")

    message = "\n".join(parts).strip()
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
