# Autopilot Hardening Report

Last updated: 2026-05-20

This file tracks the real failure points in the bounty-autopilot pipeline and the concrete mitigation added for each one.

## Current End-to-End Flow

1. `Bounty Scout` finds public GitHub paid-bounty candidates hourly.
2. `GitHub Bounty Candidate Triage` removes closed, crowded, unpaid, assigned, or already-attempted issues.
3. `GitHub OpenAI Patch Solver` attempts to generate and validate a focused patch for the best candidate.
4. Patch metadata is written under `github_bounty_patches/`.
5. `GitHub Bounty Submitter` runs hourly and turns ready patch metadata into a fork/branch/PR.
6. `Bounty Reply Monitor` follows reviewer/maintainer responses and pushes follow-up work when needed.
7. `TaskBounty Worker` refreshes TaskBounty candidates hourly, triages them, tries to generate a patch, and submits when a matching patch exists.

## Weak Points And Fixes

### 1. Scouting without patch generation

Previous risk: the system could find tasks but not solve them.

Mitigation added:

- Added `scripts/github_openai_patch_solver.py`.
- Wired it into `.github/workflows/bounty-scout.yml`.
- It creates `github_bounty_patches/<repo>-<issue>.patch` plus JSON metadata that the submitter already understands.

Remaining blocker:

- Online model credentials are still required for GitHub Actions to generate code patches by itself.

### 2. Patch generation tied to one provider

Previous risk: only one model key name/provider worked.

Mitigation added for GitHub bounty solver:

- Supports `OPENAI_API_KEY` via Responses API.
- Supports `OPENROUTER_API_KEY` via chat completions.
- Supports `SOLVER_API_KEY`/`AI_API_KEY`/`FREE_AI_API_KEY` when paired with `SOLVER_BASE_URL` or `OPENAI_BASE_URL`.

Remaining blocker:

- TaskBounty's older `openai_patch_solver.py` still uses OpenAI Responses API directly. Prefer setting `OPENAI_API_KEY` for TaskBounty until it is refactored to share the generic solver client.

### 3. Ready patches not automatically submitted

Previous risk: a patch could sit in the repo without becoming a PR.

Mitigation added:

- Added `.github/workflows/github-bounty-submit.yml`.
- It runs hourly and on changes under `github_bounty_patches/**`.
- It calls `scripts/github_bounty_submitter.py`, which forks, branches, commits, pushes, and opens a PR when token permissions allow it.

Required secret:

- `BOUNTY_GITHUB_TOKEN` with repo/fork/PR permissions.

### 4. TaskBounty hidden repo access

Known blocker:

- Some TaskBounty feed items do not expose a public GitHub repo before access is granted.
- If the platform returns `access_failed_409` and no public repo URL, no solver can safely create a real patch because there is no source code to inspect.

Mitigation already present:

- Worker records this explicitly instead of pretending work happened.
- Public GitHub tasks continue through the solver path.

### 5. Low-quality or spam risk

Previous risk: commenting or submitting weak speculative work can damage account trust.

Mitigation already present:

- Triage skips crowded/assigned/competing PR tasks.
- Submitter only acts on real patch metadata.
- Reply monitor is instructed to post only when there is a concrete maintainer/reviewer need.

## One-Time Setup Still Required

For full online autonomy, GitHub repository secrets should include:

- `BOUNTY_GITHUB_TOKEN`: GitHub token with fork, branch, push, pull request, issue comment, and star permissions if bounty rules require starring.
- `TASKBOUNTY_API_KEY`: TaskBounty API key.
- `TASKBOUNTY_AGENT_ID`: TaskBounty agent id.
- `OPENAI_API_KEY`: preferred model key for both GitHub and TaskBounty solvers.

Optional alternatives for GitHub bounty solver:

- `OPENROUTER_API_KEY`
- `SOLVER_API_KEY`
- `SOLVER_BASE_URL`
- `SOLVER_MODEL`

## Honest Status

The system is now connected from discovery to PR submission for public GitHub bounty patches, and from TaskBounty discovery to patch submission when a valid TaskBounty patch exists.

It still cannot guarantee income. Money only arrives after a maintainer or platform accepts/merges the work and payout rules are satisfied.
