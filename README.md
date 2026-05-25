# Bounty Autopilot (aglichandrap)

Autonomous scout and worker queue for paid coding bounties.

## Active lanes

- **GitHub bounty scout**: scans public GitHub issues every 15 minutes
- **Algora bounty scout**: scans Algora.io for high-value bounties
- **TaskBounty scout**: scans TaskBounty every 15 minutes
- **Codex automations**: active for scout and solver follow-up
- **Telegram notifications**: sends messages when reports change

## Current financial state

Income tracking will be updated as bounties are claimed and paid.

## Setup

### GitHub Secrets Required

Add these secrets in Settings → Secrets and variables → Actions:

1. `BOUNTY_GITHUB_TOKEN` — GitHub PAT with `repo` scope
2. `TELEGRAM_BOT_TOKEN` — Telegram bot token from @BotFather
3. `TELEGRAM_CHAT_ID` — Your Telegram chat ID
4. `OPENAI_API_KEY` — (Optional) For AI-powered patch generation
5. `SOLVER_API_KEY` — (Optional) Custom solver API key
6. `SOLVER_BASE_URL` — (Optional) Custom solver endpoint
7. `SOLVER_MODEL` — (Optional) Custom solver model

### Telegram Setup

1. In Telegram, message `@BotFather` and create a bot with `/newbot`
2. Copy the bot token into GitHub secret `TELEGRAM_BOT_TOKEN`
3. Send any message to your bot from your Telegram account
4. Open `https://api.telegram.org/botYOUR_TOKEN/getUpdates` in the browser
5. Copy your numeric `chat.id` and add as GitHub secret `TELEGRAM_CHAT_ID`

### Enable Workflows

1. Go to Actions tab in the repository
2. Enable all workflows
3. The bounty scout will run every 15 minutes automatically

## Bounty Strategy

- **First mover**: Target issues with 0-2 comments
- **Volume play**: Even small bounties ($10-$50) are worth it at scale
- **Quality**: Always read CONTRIBUTING.md before submitting PRs
- **Token rewards**: Accept token/gas rewards (not just USD)

## Target Repos

- FreeCAD Documentation (€€€ bounties)
- HELPDESK.AI (GSSoC bounties)
- Cognitive-OS ($3k research bounties)
- projectdiscovery/nuclei ($100 Algora bounties)
- calcom/cal.com ($50-$200 Algora bounties)

## Author

GitHub: [@aglichandrap](https://github.com/aglichandrap)
