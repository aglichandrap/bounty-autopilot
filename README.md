# Bounty Autopilot

Autonomous scout and worker queue for paid coding bounties.

## Active lanes

- GitHub bounty scout: scans public GitHub issues every 15 minutes.
- TaskBounty scout: scans TaskBounty every 15 minutes and works better after `TASKBOUNTY_API_KEY` and `TASKBOUNTY_AGENT_ID` are added as repository secrets.
- Codex automations: active for scout and solver follow-up.
- Telegram notifications: send messages when reports change, submissions/claims update, health changes, or workflows fail.

## Current financial state

No income has been received yet. A bounty counts as income only after a PR or patch is accepted and paid.

## One-time setup still needed

1. Create/register a TaskBounty agent: https://www.task-bounty.com/for-agents
2. Add GitHub repository secrets:
   - `TASKBOUNTY_API_KEY`
   - `TASKBOUNTY_AGENT_ID`
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
3. Configure payout method on TaskBounty.

## Telegram setup

1. In Telegram, message `@BotFather` and create a bot with `/newbot`.
2. Copy the bot token into GitHub secret `TELEGRAM_BOT_TOKEN`.
3. Send any message to your bot from your Telegram account.
4. Open `https://api.telegram.org/botYOUR_TOKEN/getUpdates` in the browser and copy your numeric `chat.id`.
5. Add that number as GitHub secret `TELEGRAM_CHAT_ID`.
