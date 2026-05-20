# GitHub Bounty Candidate Triage

Last run: 2026-05-20 21:14 UTC

Kept candidates: 0

This pass removes unpaid, crowded, assigned, closed, already-attempted, market-alert, token-cost, HITL-blocked, or false-positive GitHub bounty issues before worker time is spent.

## 1. Proton Calendar Integration

- Decision: drop
- Score: 160 -> -30
- Issue: https://github.com/calcom/cal.com/issues/5756
- Reason: no clear open paid bounty signal >= $10 found
- Reason: busy issue thread (124 comments)
- Reason: issue comments indicate submitted/claimed PR or missing-source uncertainty

## 2. Replace panic with error handling in template loader when dialers are missing

- Decision: drop
- Score: 150 -> -55
- Issue: https://github.com/projectdiscovery/nuclei/issues/6674
- Reason: issue is not open
- Reason: light competition allowed: 3 open competing PR(s)
- Reason: issue comments indicate submitted/claimed PR or missing-source uncertainty
- Competing PR: https://github.com/projectdiscovery/nuclei/pull/6746
- Competing PR: https://github.com/projectdiscovery/nuclei/pull/7316
- Competing PR: https://github.com/projectdiscovery/nuclei/pull/7368

## 3. Integrate typos tool into CI

- Decision: drop
- Score: 150 -> -10
- Issue: https://github.com/projectdiscovery/nuclei/issues/6532
- Reason: issue is not open
- Reason: issue comments indicate submitted/claimed PR or missing-source uncertainty

## 4. [CAL-3105] BigBlueButton Integration

- Decision: drop
- Score: 145 -> 85
- Issue: https://github.com/calcom/cal.com/issues/1985
- Reason: issue comments indicate submitted/claimed PR or missing-source uncertainty

## 5. Multi-account configurations re-trigger OAuth browser tabs on every Claude Code session and sub-agent spawn

- Decision: drop
- Score: 42 -> -73
- Issue: https://github.com/superhuman/mcp-mail/issues/4
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty
- Reason: light competition allowed: 1 open competing PR(s)
- Competing PR: https://github.com/superhuman/mcp-mail/pull/2

## 6. ⚠️ Kiro rate limit reached: Request quota exceeded. Please wait a moment and try again.

- Decision: drop
- Score: 38 -> -32
- Issue: https://github.com/kirodotdev/Kiro/issues/8709
- Reason: no clear open paid bounty signal >= $10 found

## 7. [WIKI-DOCS] Archon fantasy RTS/FPS v0 map blockout

- Decision: drop
- Score: 35 -> -65
- Issue: https://github.com/Jonnyton/Workflow/issues/947
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty

## 8. [BUG] $480 paid across 3 Stripe invoices for Max 20x — Anthropic's own Stripe sent "payment unsuccessful" while charging card — no provisioning, ticket #98190248 unanswered 17 days

- Decision: drop
- Score: 34 -> -36
- Issue: https://github.com/anthropics/claude-code/issues/60923
- Reason: no clear open paid bounty signal >= $10 found
