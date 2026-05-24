# GitHub Bounty Candidate Triage

Last run: 2026-05-24 15:35 UTC

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
- Score: 150 -> 15
- Issue: https://github.com/projectdiscovery/nuclei/issues/6674
- Reason: issue is not open
- Reason: competition already visible in comments; still allowed in aggressive mode

## 3. Integrate typos tool into CI

- Decision: drop
- Score: 150 -> 15
- Issue: https://github.com/projectdiscovery/nuclei/issues/6532
- Reason: issue is not open
- Reason: competition already visible in comments; still allowed in aggressive mode

## 4. MRWK bounty: live public smoke checks and useful reports, round 2

- Decision: drop
- Score: 51 -> -19
- Issue: https://github.com/ramimbo/mergework/issues/109
- Reason: no clear open paid bounty signal >= $10 found

## 5. Feedback from building Kalipso (Week 1 bounty): v4 SDK transition friction, mirror-node tx-id gap, transitive vulnerabilities

- Decision: drop
- Score: 47 -> -53
- Issue: https://github.com/hashgraph/hedera-agent-kit-js/issues/857
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty

## 6. Feature Request: Copy rule(s) to Private Workspace

- Decision: keep
- Score: 30 -> -5
- Issue: https://github.com/requestly/requestly/issues/3825
- Reason: competition already visible in comments; still allowed in aggressive mode

## 7. Support / add `proxy-server` input mode to fuzz / run checks on live traffic

- Decision: drop
- Score: 8 -> -62
- Issue: https://github.com/projectdiscovery/nuclei/issues/4953
- Reason: no clear open paid bounty signal >= $10 found

## 8. bug: Rule shows “1 applied filter” even when no filter is applied

- Decision: keep
- Score: 5 -> -30
- Issue: https://github.com/requestly/requestly/issues/3826
- Reason: competition already visible in comments; still allowed in aggressive mode
