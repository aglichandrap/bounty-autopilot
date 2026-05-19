# Bounty Autopilot Status

## Current State

- GitHub bounty scout workflow: deployed, scheduled every 2 hours.
- GitHub candidate triage: deployed. It now removes crowded, assigned, closed, or already-attempted GitHub bounty issues before worker time is spent.
- GitHub worker queue generator: deployed.
- GitHub bounty submitter workflow: deployed; it can submit ready patches through `BOUNTY_GITHUB_TOKEN` when the token has the required external-repo permissions.
- TaskBounty scout workflow: deployed, scheduled every 2 hours.
- TaskBounty worker workflow: deployed, scheduled every 2 hours, with triage before execution.
- Codex scout automation: active every 2 hours.
- Codex worker automation: active every 2 hours.
- TaskBounty solver loop: active every 2 hours.
- Duplicate broad TaskBounty solver automation: paused to avoid duplicate work.
- Bounty reply monitor: active every 1 hour.
- Online GitHub repo: deployed to `asaadnashed/bounty-autopilot`.
- TaskBounty credentials: configured as repository secrets.

## Active Work

- Live upstream PR: https://github.com/orchestration-agent/AgentOrchestration/pull/20
- PR state: open, mergeable, not draft.
- Additional branch-safety regression tests were added to the PR branch to improve competitiveness.

## Known Blockers

- Some external GitHub PR creation attempts are blocked by token permissions: `Resource not accessible by personal access token`.
- The first live bounty is competitive; several other contributors have opened PRs for the same issue.
- Payout is not earned until a bounty owner accepts or merges the work.

## Financial Status

No income yet. No bounty has been accepted or paid yet.
