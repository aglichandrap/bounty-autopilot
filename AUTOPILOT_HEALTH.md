# Autopilot Health

Last run: 2026-05-20 05:55 UTC

Overall: `blocked`

The automation has at least one blocker that prevents full unattended execution.

## Checks

- `ok` GitHub interaction token: Token available for comments, fork, push, and PR submission.
- `degraded` Online model solver key: GitHub Actions cannot generate new code patches without OPENAI_API_KEY, OPENROUTER_API_KEY, or SOLVER_API_KEY+SOLVER_BASE_URL. Local Codex automation is the fallback.
- `ok` TaskBounty credentials: TaskBounty API and agent id are available.
- `ok` GitHub bounty claimer: No claim comments tracked yet.
- `ok` GitHub patch solver report: Latest report parsed.
- `blocked` TaskBounty patch solver report: Latest report parsed.
- `active` GitHub bounty submitter: PRs tracked: 3
- `degraded` TaskBounty worker: Worker report exists.
- `ok` Ready patch files: GitHub patches: 3; TaskBounty patches: 0.
- `ok` Candidate feeds: GitHub candidates: 2; TaskBounty candidates: 4.

## Tracked PRs

- https://github.com/orchestration-agent/AgentOrchestration/pull/20
- https://github.com/orchestration-agent/AgentOrchestration/pull/98
- https://github.com/orchestration-agent/AgentOrchestration/pull/99
