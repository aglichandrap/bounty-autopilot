# Bounty Autopilot

Autonomous scout and worker queue for paid coding bounties.

## Active lanes

- GitHub bounty scout: scans public GitHub issues every 2 hours.
- TaskBounty scout: scans TaskBounty every 2 hours and works better after `TASKBOUNTY_API_KEY` and `TASKBOUNTY_AGENT_ID` are added as repository secrets.
- Codex automations: active for scout and solver follow-up.

## Current financial state

No income has been received yet. A bounty counts as income only after a PR or patch is accepted and paid.

## One-time setup still needed

1. Create/register a TaskBounty agent: https://www.task-bounty.com/for-agents
2. Add GitHub repository secrets:
   - `TASKBOUNTY_API_KEY`
   - `TASKBOUNTY_AGENT_ID`
3. Configure payout method on TaskBounty.
