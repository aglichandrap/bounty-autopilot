# GitHub OpenAI Patch Solver

Last run: 2026-05-20 10:45 UTC

No online model key is configured, so GitHub Actions cannot generate new code patches by itself.

No eligible GitHub bounty candidates are queued for local Codex right now.

Recent cleanup:

- `matchmoments-admin/ask-arthur#321` was removed because it was superseded by a maintainer-built path and PR #339.
- `ResearchHub/issues#531` and `ResearchHub/issues#540` were removed because no clear paid bounty signal was confirmed.

The scout runs every 15 minutes and will queue a new `local_fallback_queued` item only when a paid, accessible, low-competition issue appears.
