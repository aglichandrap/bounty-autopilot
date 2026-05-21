# Autopilot Health

Last run: 2026-05-21 16:32 UTC

Overall: `active`

The automation has active work in flight, claim comments, or ready submission paths.

## Checks

- `ok` GitHub interaction token: Token available for comments, fork, push, and PR submission.
- `ok` Bounty scout scheduler: bounty_worker_queue.md is fresh (9 minutes old).
- `degraded` GitHub claimer scheduler: github_bounty_claim_report.md is stale (123 minutes old); dispatch sent.
- `degraded` GitHub submitter scheduler: github_bounty_submission_report.md is stale (122 minutes old); dispatch sent.
- `degraded` TaskBounty scout scheduler: taskbounty_report.md is stale (124 minutes old); dispatch sent.
- `degraded` TaskBounty worker scheduler: taskbounty_worker_report.md is stale (125 minutes old); dispatch sent.
- `degraded` Online model solver key: GitHub Actions cannot generate new code patches without a model key. Local Codex automation is configured as the solving fallback.
- `ok` TaskBounty credentials: TaskBounty API and agent id are available.
- `active` GitHub bounty claimer: Comments tracked: 1
- `ok` GitHub patch solver report: Latest report parsed; local Codex is fallback if online model key is missing.
- `ok` TaskBounty patch solver report: Latest report parsed; local Codex is fallback if online model key is missing.
- `active` GitHub bounty submitter: PRs tracked: 3
- `ok` TaskBounty worker: Worker report exists.
- `ok` Ready patch files: GitHub patches: 3; TaskBounty patches: 1.
- `ok` Candidate feeds: GitHub candidates: 1; TaskBounty candidates: 1.

## Tracked Comments

- https://github.com/SingularityNet-Ambassador-Program/Treasury-Guild/issues/113#issuecomment-4509254558

## Tracked PRs

- https://github.com/orchestration-agent/AgentOrchestration/pull/20
- https://github.com/orchestration-agent/AgentOrchestration/pull/98
- https://github.com/orchestration-agent/AgentOrchestration/pull/99
