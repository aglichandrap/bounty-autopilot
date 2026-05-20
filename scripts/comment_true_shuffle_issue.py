#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

TOKEN = os.environ.get("BOUNTY_GITHUB_TOKEN") or os.environ.get("GITHUB_TOKEN")
if not TOKEN:
    raise SystemExit("BOUNTY_GITHUB_TOKEN is required")

REPO = "Meeep1/EeveeSpotifyRevivedPublic"
ISSUE = 11
PR_URL = "https://github.com/Meeep1/EeveeSpotifyRevivedPublic/pull/91"
BODY = f"""Submitted a focused implementation in PR #91: {PR_URL}

It keeps the original TrueShuffle behavior by disabling the weighted recommendation shuffle path, but avoids a hard startup hook on `SPTFreeTierPlaylistTrackShuffler`. The installer checks for the known class, scans compatible loaded shuffle classes, and retries briefly for lazily-loaded Spotify classes so a missing or renamed class should not crash startup.

I also added a Settings > Patching toggle and included verification notes in the PR."""

API = "https://api.github.com"
HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "bounty-autopilot-issue-commenter",
}


def request(method: str, endpoint: str, data: dict | None = None):
    body = None if data is None else json.dumps(data).encode("utf-8")
    req = urllib.request.Request(API + endpoint, data=body, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else None
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"GitHub API {method} {endpoint} failed: {exc.code} {raw}") from exc


def main() -> int:
    comments = request("GET", f"/repos/{REPO}/issues/{ISSUE}/comments?per_page=100")
    for comment in comments:
        if PR_URL in comment.get("body", ""):
            print("PR comment already exists")
            return 0

    created = request("POST", f"/repos/{REPO}/issues/{ISSUE}/comments", {"body": BODY})
    print(f"Created comment: {created['html_url']}")
    with open("true_shuffle_issue_comment_report.md", "w", encoding="utf-8") as fh:
        fh.write("# True Shuffle issue comment report\n\n")
        fh.write(f"- Status: commented\n- Comment: {created['html_url']}\n- PR: {PR_URL}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
