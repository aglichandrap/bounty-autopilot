# GitHub Bounty Candidate Triage

Last run: 2026-05-22 15:42 UTC

Kept candidates: 4

This pass removes unpaid, assigned, closed, market-alert, token-cost, HITL-blocked, or false-positive GitHub bounty issues before worker time is spent. Crowded but still-paid issues are allowed with a score penalty.

## 1. Proton Calendar Integration

- Decision: drop
- Score: 160 -> 55
- Issue: https://github.com/calcom/cal.com/issues/5756
- Reason: no clear open paid bounty signal >= $10 found
- Reason: competition already visible in comments; still allowed in aggressive mode

## 2. Replace panic with error handling in template loader when dialers are missing

- Decision: drop
- Score: 150 -> -30
- Issue: https://github.com/projectdiscovery/nuclei/issues/6674
- Reason: issue is not open
- Reason: light competition allowed: 3 open competing PR(s)
- Reason: competition already visible in comments; still allowed in aggressive mode
- Competing PR: https://github.com/projectdiscovery/nuclei/pull/6746
- Competing PR: https://github.com/projectdiscovery/nuclei/pull/7316
- Competing PR: https://github.com/projectdiscovery/nuclei/pull/7368

## 3. Integrate typos tool into CI

- Decision: drop
- Score: 150 -> 15
- Issue: https://github.com/projectdiscovery/nuclei/issues/6532
- Reason: issue is not open
- Reason: competition already visible in comments; still allowed in aggressive mode

## 4. Bug bounty Submission-Unaccounted ERC20 Transfers to Colony Contract Deflate Reward Snapshot and Distort Payouts

- Decision: drop
- Score: 85 -> -15
- Issue: https://github.com/JoinColony/colonyNetwork/issues/1345
- Reason: issue explicitly indicates no paid bounty or free-only payment status

## 5. Code Review Bounty Claim - RustChain PR #6110 setup_miner help

- Decision: drop
- Score: 85 -> -165
- Issue: https://github.com/Scottcjn/rustchain-bounties/issues/12018
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty
- Reason: light competition allowed: 10 open competing PR(s)
- Competing PR: https://github.com/Scottcjn/rustchain-bounties/pull/12023
- Competing PR: https://github.com/Scottcjn/rustchain-bounties/pull/11177
- Competing PR: https://github.com/Scottcjn/rustchain-bounties/pull/11878
- Competing PR: https://github.com/Scottcjn/rustchain-bounties/pull/11957
- Competing PR: https://github.com/Scottcjn/rustchain-bounties/pull/11534

## 6. Bounty claim: code review for RustChain PR #6104

- Decision: drop
- Score: 85 -> -165
- Issue: https://github.com/Scottcjn/rustchain-bounties/issues/12016
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty
- Reason: light competition allowed: 10 open competing PR(s)
- Competing PR: https://github.com/Scottcjn/rustchain-bounties/pull/12023
- Competing PR: https://github.com/Scottcjn/rustchain-bounties/pull/11177
- Competing PR: https://github.com/Scottcjn/rustchain-bounties/pull/11878
- Competing PR: https://github.com/Scottcjn/rustchain-bounties/pull/11957
- Competing PR: https://github.com/Scottcjn/rustchain-bounties/pull/11534

## 7. Hosted Marketplace docs omit the MEV Leaderboard demo

- Decision: drop
- Score: 85 -> 15
- Issue: https://github.com/eigenphi/MEVScan-marketplace/issues/6
- Reason: no clear open paid bounty signal >= $10 found

## 8. [App] OnlyDust

- Decision: drop
- Score: 85 -> 15
- Issue: https://github.com/gitcoinco/gitcoin_co_30/issues/396
- Reason: no clear open paid bounty signal >= $10 found

## 9. [App] Lightning Bounties

- Decision: drop
- Score: 85 -> -15
- Issue: https://github.com/gitcoinco/gitcoin_co_30/issues/389
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty

## 10. Bounce VERP Return-Path silently overridden by Sender header in 7.1+

- Decision: drop
- Score: 85 -> 0
- Issue: https://github.com/mautic/mautic/issues/16151
- Reason: no clear open paid bounty signal >= $10 found
- Reason: light competition allowed: 1 open competing PR(s)
- Competing PR: https://github.com/mautic/mautic/pull/16152

## 11. [App] BountyPay

- Decision: drop
- Score: 75 -> -25
- Issue: https://github.com/gitcoinco/gitcoin_co_30/issues/391
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty

## 12. [App] uBounty

- Decision: drop
- Score: 75 -> -25
- Issue: https://github.com/gitcoinco/gitcoin_co_30/issues/390
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty

## 13. [Tutorial] Testing Compact Contracts: Unit Tests, Assertions, and Local Simulation

- Decision: drop
- Score: 71 -> -109
- Issue: https://github.com/midnightntwrk/contributor-hub/issues/312
- Reason: content bounty has AI-content disqualification risk for autonomous work
- Reason: light competition allowed: 3 open competing PR(s)
- Reason: competition already visible in comments; still allowed in aggressive mode
- Competing PR: https://github.com/midnightntwrk/contributor-hub/pull/486
- Competing PR: https://github.com/midnightntwrk/contributor-hub/pull/519
- Competing PR: https://github.com/midnightntwrk/contributor-hub/pull/499

## 14. [Tutorial] Bringing External Data On-Chain: Oracle Patterns for Midnight

- Decision: drop
- Score: 71 -> -59
- Issue: https://github.com/midnightntwrk/contributor-hub/issues/304
- Reason: content bounty has AI-content disqualification risk for autonomous work
- Reason: light competition allowed: 2 open competing PR(s)
- Competing PR: https://github.com/midnightntwrk/contributor-hub/pull/489
- Competing PR: https://github.com/midnightntwrk/contributor-hub/pull/532

## 15. [Tutorial] Multi-Party Private State and Contracts Between Two+ Users

- Decision: drop
- Score: 71 -> -64
- Issue: https://github.com/midnightntwrk/contributor-hub/issues/303
- Reason: content bounty has AI-content disqualification risk for autonomous work
- Reason: competition already visible in comments; still allowed in aggressive mode

## 16. [Tutorial] Working with Maps and Merkle Trees in Compact

- Decision: drop
- Score: 71 -> -64
- Issue: https://github.com/midnightntwrk/contributor-hub/issues/289
- Reason: content bounty has AI-content disqualification risk for autonomous work
- Reason: competition already visible in comments; still allowed in aggressive mode

## 17. Element should ignore events it cannot process (IoT)

- Decision: keep
- Score: 71 -> 71
- Issue: https://github.com/element-hq/element-web/issues/22662

## 18. When a user returns `return { ... }` from a route instead of `return ctx.json({ ... })`, throw an error telling them to use `ctx.json`

- Decision: drop
- Score: 71 -> -34
- Issue: https://github.com/tscircuit/winterspec/issues/30
- Reason: no clear open paid bounty signal >= $10 found
- Reason: competition already visible in comments; still allowed in aggressive mode

## 19. Claim Bounty Payment - PR #5661 boot chime capture duration

- Decision: drop
- Score: 64 -> -71
- Issue: https://github.com/Scottcjn/Rustchain/issues/5761
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty
- Reason: competition already visible in comments; still allowed in aggressive mode

## 20. [WIKI-DOCS] Archon fantasy RTS/FPS v0 unit sheet

- Decision: drop
- Score: 64 -> -71
- Issue: https://github.com/Jonnyton/Workflow/issues/950
- Reason: issue explicitly indicates no paid bounty or free-only payment status
- Reason: competition already visible in comments; still allowed in aggressive mode

## 21. Create wallet benchmarks

- Decision: drop
- Score: 56 -> -49
- Issue: https://github.com/tari-project/wallet-benchmarks/issues/1
- Reason: no clear open paid bounty signal >= $10 found
- Reason: competition already visible in comments; still allowed in aggressive mode

## 22. Claim Reward - Troubleshooting and FAQ

- Decision: drop
- Score: 54 -> -16
- Issue: https://github.com/sutt/docs/issues/3
- Reason: no clear open paid bounty signal >= $10 found

## 23. Sats to Local Currency | Mexico

- Decision: drop
- Score: 48 -> -57
- Issue: https://github.com/sutt/docs/issues/5
- Reason: no clear open paid bounty signal >= $10 found
- Reason: competition already visible in comments; still allowed in aggressive mode

## 24. structural: Phase 06b — bootstrap RL training scaffold (TRL venv + episteme/rl module)

- Decision: drop
- Score: 47 -> -23
- Issue: https://github.com/forkwright/aletheia/issues/3979
- Reason: no clear open paid bounty signal >= $10 found

## 25. Upload Photo Button Opens Scanner Instead of File Gallery

- Decision: drop
- Score: 47 -> -53
- Issue: https://github.com/RatLoopz/sahidawa-india/issues/325
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty

## 26. Agent template catalog

- Decision: keep
- Score: 46 -> 11
- Issue: https://github.com/archestra-ai/archestra/issues/3858
- Reason: competition already visible in comments; still allowed in aggressive mode

## 27. Sync Issue-Assigned property from GH to LB

- Decision: drop
- Score: 44 -> -26
- Issue: https://github.com/Lightning-Bounties/progress-tracker/issues/53
- Reason: no clear open paid bounty signal >= $10 found

## 28. Add durable agent memory for user, team, and organization context across sessions

- Decision: keep
- Score: 40 -> 5
- Issue: https://github.com/archestra-ai/archestra/issues/3837
- Reason: competition already visible in comments; still allowed in aggressive mode

## 29. Chinese language documentation

- Decision: drop
- Score: 40 -> -95
- Issue: https://github.com/counterspec/isnad/issues/4
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty
- Reason: competition already visible in comments; still allowed in aggressive mode

## 30. json in mcp server args textarea

- Decision: keep
- Score: 40 -> 5
- Issue: https://github.com/archestra-ai/archestra/issues/3859
- Reason: competition already visible in comments; still allowed in aggressive mode

## 31. feat(aletheia): Q-learning router with prioritized experience replay for dispatch routing

- Decision: drop
- Score: 39 -> -31
- Issue: https://github.com/forkwright/aletheia/issues/3969
- Reason: no clear open paid bounty signal >= $10 found

## 32. BIMI VMC purchase + activate (deferred, paid)

- Decision: drop
- Score: 38 -> -67
- Issue: https://github.com/pinohu/lead-os/issues/71
- Reason: no clear open paid bounty signal >= $10 found
- Reason: competition already visible in comments; still allowed in aggressive mode
