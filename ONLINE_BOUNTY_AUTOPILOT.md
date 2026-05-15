# Online Bounty Autopilot

This repo contains a free GitHub Actions runner that searches for public paid coding opportunities every 6 hours.

## What It Does

- Searches public GitHub issues for bounty/reward signals.
- Filters out obvious spam, contests, security-report bait, referral schemes, gambling, and vague issues.
- Scores issues that look like small coding tasks.
- Writes:
  - `bounty_report.md`
  - `bounty_candidates.json`
- Opens or updates a GitHub issue named `Bounty scout candidates`.

## Why This Is The Chosen Path

This is not passive income in the fake internet-marketing sense. It is the closest controllable path with no daily posting, no audience, no inventory, no ads, and no trading.

The income path is:

1. Scout finds a legitimate paid issue.
2. Agent inspects the repository.
3. Agent submits a real focused PR.
4. Maintainer accepts/merges it.
5. Bounty platform pays through the connected payout account.

## One-Time Setup

1. Create a new GitHub repository.
2. Upload these files:
   - `.github/workflows/bounty-scout.yml`
   - `scripts/bounty_scout.py`
   - `scripts/bounty_worker_queue.py`
   - `bounty_extra_queries.txt`
   - `ONLINE_BOUNTY_AUTOPILOT.md`
3. Open the repository's Actions tab.
4. Enable workflows if GitHub asks.
5. Run `Bounty Scout` manually once.

After that, GitHub runs it every 6 hours online.

## Payout Reality

GitHub Actions can scout opportunities online for free. It cannot receive money by itself.

When a bounty is worth pursuing, a payout account or wallet will be needed once for that bounty platform. Do not connect payout accounts to suspicious platforms.

## Operating Rule

Only submit PRs that genuinely fix the issue. Do not submit noisy AI-generated changes, mass PRs, or fake reports. Reputation is the asset that makes small bounties compound.
