# GitHub Bounty Candidate Triage

Last run: 2026-05-21 16:42 UTC

Kept candidates: 1

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

## 4. [CAL-3105] BigBlueButton Integration

- Decision: keep
- Score: 145 -> 110
- Issue: https://github.com/calcom/cal.com/issues/1985
- Reason: competition already visible in comments; still allowed in aggressive mode

## 5. [BUG-087] run_branch fails immediately with AllProvidersExhaustedError instead of retry/backoff despite actionable retry message

- Decision: drop
- Score: 43 -> -107
- Issue: https://github.com/Jonnyton/Workflow/issues/917
- Reason: issue explicitly indicates no paid bounty or free-only payment status
- Reason: light competition allowed: 1 open competing PR(s)
- Reason: competition already visible in comments; still allowed in aggressive mode
- Competing PR: https://github.com/Jonnyton/Workflow/pull/1000

## 6. Sats to Local Currency | Mexico

- Decision: drop
- Score: 39 -> -81
- Issue: https://github.com/sutt/docs/issues/5
- Reason: no clear open paid bounty signal >= $10 found
- Reason: light competition allowed: 1 open competing PR(s)
- Reason: competition already visible in comments; still allowed in aggressive mode
- Competing PR: https://github.com/sutt/docs/pull/13

## 7. Endless scrolling in Excel on Terminal Server 2008 R2

- Decision: drop
- Score: 35 -> -35
- Issue: https://github.com/rdesktop/rdesktop/issues/77
- Reason: no clear open paid bounty signal >= $10 found

## 8. Fixing the bounty award system

- Decision: drop
- Score: 35 -> -35
- Issue: https://github.com/ResearchHub/issues/issues/531
- Reason: no clear open paid bounty signal >= $10 found

## 9. Create a Bounty Amount Box Issue

- Decision: drop
- Score: 35 -> -65
- Issue: https://github.com/ResearchHub/issues/issues/540
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty

## 10. Sync Issue-Assigned property from GH to LB

- Decision: drop
- Score: 35 -> -35
- Issue: https://github.com/Lightning-Bounties/progress-tracker/issues/53
- Reason: no clear open paid bounty signal >= $10 found

## 11. Support / add `proxy-server` input mode to fuzz / run checks on live traffic

- Decision: drop
- Score: 8 -> -62
- Issue: https://github.com/projectdiscovery/nuclei/issues/4953
- Reason: no clear open paid bounty signal >= $10 found
