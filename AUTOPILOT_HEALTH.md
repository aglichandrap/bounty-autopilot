# Autopilot Health

Last run: 2026-05-20 06:46 UTC

Overall: `active`

The automation has active work in flight, claim comments, or ready submission paths.

## Checks

- `ok` GitHub interaction token: Token available for comments, fork, push, and PR submission.
- `degraded` Online model solver key: GitHub Actions cannot generate new code patches without a model key. Local Codex automation is configured as the solving fallback.
- `ok` TaskBounty credentials: TaskBounty API and agent id are available.
- `ok` GitHub bounty claimer: No claim comments tracked yet.
- `degraded` GitHub patch solver report: Latest report parsed; local Codex is fallback if online model key is missing.
- `degraded` TaskBounty patch solver report: Latest report parsed; local Codex is fallback if online model key is missing.
- `active` GitHub bounty submitter: PRs tracked: 3
- `degraded` TaskBounty worker: Worker report exists.
- `ok` Ready patch files: GitHub patches: 3; TaskBounty patches: 0.
- `ok` Candidate feeds: GitHub candidates: 2; TaskBounty candidates: 4.

## Tracked PRs

- https://github.com/orchestration-agent/AgentOrchestration/pull/20
- https://github.com/orchestration-agent/AgentOrchestration/pull/98
- https://github.com/orchestration-agent/AgentOrchestration/pull/99
