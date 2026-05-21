# GitHub Bounty Candidate Triage

Last run: 2026-05-21 16:58 UTC

Kept candidates: 0

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

## 4. Bug: PR auto-detection matches wrong GHB bounty

- Decision: drop
- Score: 85 -> 15
- Issue: https://github.com/Ghbounty/GhBounty/issues/108
- Reason: no clear open paid bounty signal >= $10 found

## 5. Code Review Bounty #73 — BossChaos FINAL CLAIM (27 PRs, 33 findings)

- Decision: drop
- Score: 85 -> -15
- Issue: https://github.com/Scottcjn/rustchain-bounties/issues/11900
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty

## 6. [BOUNTY] Claim: <Mobile SERP Tracker - Working Submission ($50 Wave 2)>

- Decision: drop
- Score: 81 -> -69
- Issue: https://github.com/bolivian-peru/marketplace-service-template/issues/463
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty
- Reason: light competition allowed: 1 open competing PR(s)
- Reason: competition already visible in comments; still allowed in aggressive mode
- Competing PR: https://github.com/bolivian-peru/marketplace-service-template/pull/464

## 7. PR Review Claim - 9 PRs - 2026-05-21 16:37 UTC

- Decision: drop
- Score: 75 -> -10
- Issue: https://github.com/Scottcjn/rustchain-bounties/issues/11910
- Reason: no clear open paid bounty signal >= $10 found
- Reason: light competition allowed: 1 open competing PR(s)
- Competing PR: https://github.com/Scottcjn/rustchain-bounties/pull/11619

## 8. PR Review Claim - 3 PRs - 2026-05-21 13:21 UTC

- Decision: drop
- Score: 75 -> -10
- Issue: https://github.com/Scottcjn/rustchain-bounties/issues/11876
- Reason: no clear open paid bounty signal >= $10 found
- Reason: light competition allowed: 1 open competing PR(s)
- Competing PR: https://github.com/Scottcjn/rustchain-bounties/pull/11619

## 9. [Tutorial] Midnight Development on Windows via WSL2

- Decision: drop
- Score: 71 -> -59
- Issue: https://github.com/midnightntwrk/contributor-hub/issues/282
- Reason: content bounty has AI-content disqualification risk for autonomous work
- Reason: light competition allowed: 2 open competing PR(s)
- Competing PR: https://github.com/midnightntwrk/contributor-hub/pull/498
- Competing PR: https://github.com/midnightntwrk/contributor-hub/pull/497

## 10. [Tutorial] Designing Public vs. Private State: What Goes Where and Why

- Decision: drop
- Score: 71 -> -109
- Issue: https://github.com/midnightntwrk/contributor-hub/issues/292
- Reason: content bounty has AI-content disqualification risk for autonomous work
- Reason: light competition allowed: 3 open competing PR(s)
- Reason: competition already visible in comments; still allowed in aggressive mode
- Competing PR: https://github.com/midnightntwrk/contributor-hub/pull/510
- Competing PR: https://github.com/midnightntwrk/contributor-hub/pull/346
- Competing PR: https://github.com/midnightntwrk/contributor-hub/pull/425

## 11. More thorough benchmarks [$200]

- Decision: keep
- Score: 71 -> -69
- Issue: https://github.com/QuantumSavory/QuantumSavory.jl/issues/131
- Reason: light competition allowed: 7 open competing PR(s)
- Reason: competition already visible in comments; still allowed in aggressive mode
- Competing PR: https://github.com/QuantumSavory/QuantumSavory.jl/pull/430
- Competing PR: https://github.com/QuantumSavory/QuantumSavory.jl/pull/422
- Competing PR: https://github.com/QuantumSavory/QuantumSavory.jl/pull/353
- Competing PR: https://github.com/QuantumSavory/QuantumSavory.jl/pull/377
- Competing PR: https://github.com/QuantumSavory/QuantumSavory.jl/pull/375

## 12. [UI Bug] Unauthorized 'Edit' and 'Delete' buttons visible on /bounties page

- Decision: keep
- Score: 71 -> -129
- Issue: https://github.com/algora-io/algora/issues/238
- Reason: light competition allowed: 11 open competing PR(s)
- Reason: competition already visible in comments; still allowed in aggressive mode
- Competing PR: https://github.com/algora-io/algora/pull/257
- Competing PR: https://github.com/algora-io/algora/pull/271
- Competing PR: https://github.com/algora-io/algora/pull/267
- Competing PR: https://github.com/algora-io/algora/pull/266
- Competing PR: https://github.com/algora-io/algora/pull/282

## 13. [Tutorial] Bringing External Data On-Chain: Oracle Patterns for Midnight

- Decision: drop
- Score: 71 -> -44
- Issue: https://github.com/midnightntwrk/contributor-hub/issues/304
- Reason: content bounty has AI-content disqualification risk for autonomous work
- Reason: light competition allowed: 1 open competing PR(s)
- Competing PR: https://github.com/midnightntwrk/contributor-hub/pull/489

## 14. [Tutorial] Integrating Midnight Proofs into an Existing Backend (Node.js/REST)

- Decision: drop
- Score: 71 -> -94
- Issue: https://github.com/midnightntwrk/contributor-hub/issues/311
- Reason: content bounty has AI-content disqualification risk for autonomous work
- Reason: light competition allowed: 2 open competing PR(s)
- Reason: competition already visible in comments; still allowed in aggressive mode
- Competing PR: https://github.com/midnightntwrk/contributor-hub/pull/336
- Competing PR: https://github.com/midnightntwrk/contributor-hub/pull/459

## 15. HAK v4: Plugin registration order affects tool availability in HederaAgentAPI

- Decision: drop
- Score: 70 -> 0
- Issue: https://github.com/hashgraph/hedera-agent-kit-js/issues/834
- Reason: no clear open paid bounty signal >= $10 found

## 16. [BUG-087] run_branch fails immediately with AllProvidersExhaustedError instead of retry/backoff despite actionable retry message

- Decision: drop
- Score: 64 -> -71
- Issue: https://github.com/Jonnyton/Workflow/issues/917
- Reason: issue explicitly indicates no paid bounty or free-only payment status
- Reason: competition already visible in comments; still allowed in aggressive mode
