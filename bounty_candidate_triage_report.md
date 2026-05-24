# GitHub Bounty Candidate Triage

Last run: 2026-05-24 17:47 UTC

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

## 4. MVP-7 blocker: require real-run RunPod safety gate before further live automation

- Decision: drop
- Score: 110 -> 40
- Issue: https://github.com/uda-lab/yomotsusaka/issues/127
- Reason: no clear open paid bounty signal >= $10 found

## 5. 🎯 Bounty Alert: 14 New Opportunityies found

- Decision: keep
- Score: 104 -> 69
- Issue: https://github.com/dev-kp-eloper/BountyScout/issues/9
- Reason: competition already visible in comments; still allowed in aggressive mode

## 6. Postmortem: 3 orphan RunPod Pods + cost overrun (delete-after-use policy code-side hole since MVP-4 #76)

- Decision: drop
- Score: 96 -> 26
- Issue: https://github.com/uda-lab/yomotsusaka/issues/124
- Reason: no clear open paid bounty signal >= $10 found

## 7. [Bug] release workflow — dev/main squash divergence compounds; needs main→dev sync after each release

- Decision: drop
- Score: 85 -> 15
- Issue: https://github.com/me2resh/apexyard/issues/403
- Reason: no clear open paid bounty signal >= $10 found

## 8. Critical: audit all tx.execute(SELECT *) callsites in commandBus.ts — snake_case reads silently return undefined

- Decision: drop
- Score: 85 -> 15
- Issue: https://github.com/EvanTenenbaum/terp-operator/issues/267
- Reason: no clear open paid bounty signal >= $10 found

## 9. Mapper sub-agent runs out of turns when the verifier rejects the first attempt (maxTurns: 4 too tight)

- Decision: drop
- Score: 85 -> 15
- Issue: https://github.com/Pleusch/SharpMind/issues/205
- Reason: no clear open paid bounty signal >= $10 found

## 10. Test runs leak orphan processes (Puppeteer chromium + testhost + Mangarr.Console) — needs unified pre-flight + validation harness

- Decision: drop
- Score: 85 -> 15
- Issue: https://github.com/devbrian/Mangarr/issues/252
- Reason: no clear open paid bounty signal >= $10 found

## 11. test(d8): remaining failure modes F1-F10 (post-D7 sign-off)

- Decision: drop
- Score: 85 -> 15
- Issue: https://github.com/dreamlx/lh-enterprise/issues/345
- Reason: no clear open paid bounty signal >= $10 found

## 12. Stale comments in DefaultConfig claim a finite retry default, contradicting the actual unbounded behavior

- Decision: drop
- Score: 85 -> 15
- Issue: https://github.com/xrf9268-hue/aiops-platform/issues/367
- Reason: no clear open paid bounty signal >= $10 found

## 13. Ollama model swaps in mixed ingests pay full reload cost on every switch

- Decision: drop
- Score: 85 -> 15
- Issue: https://github.com/jswest/bartleby/issues/11
- Reason: no clear open paid bounty signal >= $10 found

## 14. Roadmap: turn GradSharp from CV builder into application-pack engine

- Decision: drop
- Score: 85 -> 15
- Issue: https://github.com/vanadiuminternational/HireReady/issues/57
- Reason: no clear open paid bounty signal >= $10 found

## 15. [WIKI-DOCS] SPLITROOT polish — UMG HUD (rung-2 final gate; health/ammo/respawn/squad/body-picker widgets)

- Decision: drop
- Score: 79 -> -56
- Issue: https://github.com/Jonnyton/Workflow/issues/1060
- Reason: issue explicitly indicates no paid bounty or free-only payment status
- Reason: competition already visible in comments; still allowed in aggressive mode

## 16. Backend/AI: Prevent Groq API Abuse by Disallowing Empty Interview Completions

- Decision: drop
- Score: 79 -> -21
- Issue: https://github.com/anurag3407/career-pilot/issues/1693
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty

## 17. Consistently getting errors with using ollama cloud w/o agent

- Decision: drop
- Score: 79 -> 9
- Issue: https://github.com/dyad-sh/dyad/issues/3498
- Reason: no clear open paid bounty signal >= $10 found

## 18. Critical data loss: startup GC silently deletes all session transcripts

- Decision: drop
- Score: 79 -> 9
- Issue: https://github.com/anthropics/claude-code/issues/62041
- Reason: no clear open paid bounty signal >= $10 found

## 19. [WIKI-DOCS] SPLITROOT polish — representative audio direction (rung-2 gate; four-layer cue discipline + faction palettes)

- Decision: drop
- Score: 79 -> -56
- Issue: https://github.com/Jonnyton/Workflow/issues/1059
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty
- Reason: competition already visible in comments; still allowed in aggressive mode

## 20. Explorer page: Miner data stuck at 'Loading miners...' indefinitely (frontend rendering bug)

- Decision: drop
- Score: 79 -> 9
- Issue: https://github.com/Scottcjn/Rustchain/issues/6211
- Reason: no clear open paid bounty signal >= $10 found

## 21. [WIKI-DOCS] SPLITROOT hero plan — Briar Saint + Master Artificer (the two starting heroes; horizontal-only paid discipline locked)

- Decision: drop
- Score: 79 -> -56
- Issue: https://github.com/Jonnyton/Workflow/issues/1054
- Reason: issue explicitly indicates no paid bounty or free-only payment status
- Reason: competition already visible in comments; still allowed in aggressive mode

## 22. [WIKI-DESIGN] Factory branch substrate improvement — JSONify faction registry (eliminate the biggest remix-friction point)

- Decision: drop
- Score: 79 -> -56
- Issue: https://github.com/Jonnyton/Workflow/issues/1050
- Reason: issue explicitly indicates no paid bounty or free-only payment status
- Reason: competition already visible in comments; still allowed in aggressive mode

## 23. Slice 16 — PaymentExecution (bank transfer) + QR + screenshot + DB constraints

- Decision: drop
- Score: 79 -> 9
- Issue: https://github.com/yutobeo2024/KT/issues/18
- Reason: no clear open paid bounty signal >= $10 found

## 24. [WIKI-DOCS] SPLITROOT "Second 60 Seconds" combat slice — death/respawn loop, faction weapons, command-while-you-wait (rung-2 anchor)

- Decision: drop
- Score: 79 -> -56
- Issue: https://github.com/Jonnyton/Workflow/issues/1042
- Reason: issue explicitly indicates no paid bounty or free-only payment status
- Reason: competition already visible in comments; still allowed in aggressive mode

## 25. Keep the map tile cache in sync with feature writes (write-reactive invalidation)

- Decision: drop
- Score: 79 -> -21
- Issue: https://github.com/un-fao/GeoID/issues/1292
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty

## 26. README whitepaper PDF link times out via raw.githubusercontent.com

- Decision: drop
- Score: 79 -> -26
- Issue: https://github.com/Scottcjn/Rustchain/issues/6202
- Reason: no clear open paid bounty signal >= $10 found
- Reason: competition already visible in comments; still allowed in aggressive mode

## 27. [WIKI-DESIGN] Factory branch remix proof — "STELLAR FRONT" sci-fi canary scoped against SPLITROOT substrate (the factory's product validation)

- Decision: drop
- Score: 79 -> -21
- Issue: https://github.com/Jonnyton/Workflow/issues/1049
- Reason: issue explicitly indicates no paid bounty or free-only payment status

## 28. [WIKI-DESIGN] Factory branch games/ directory substrate contract — multi-canary physical layout + second-canary spawn workflow

- Decision: drop
- Score: 79 -> -21
- Issue: https://github.com/Jonnyton/Workflow/issues/1048
- Reason: issue explicitly indicates no paid bounty or free-only payment status

## 29. How Strong Backlinks Continue Supporting Long Term SEO Results

- Decision: drop
- Score: 79 -> 9
- Issue: https://github.com/vefoGix00/VefoGix-/issues/372
- Reason: no clear open paid bounty signal >= $10 found

## 30. Why Strong SEO Link Building Still Matters For Online Growth

- Decision: drop
- Score: 79 -> 9
- Issue: https://github.com/vefoGix00/VefoGix-/issues/371
- Reason: no clear open paid bounty signal >= $10 found

## 31. [WIKI-DOCS] SPLITROOT C6 contract — second-60-seconds integration smoke (Proof/second-60-seconds-smoke.ps1)

- Decision: drop
- Score: 73 -> -77
- Issue: https://github.com/Jonnyton/Workflow/issues/1040
- Reason: issue explicitly indicates no paid bounty or free-only payment status
- Reason: light competition allowed: 1 open competing PR(s)
- Reason: competition already visible in comments; still allowed in aggressive mode
- Competing PR: https://github.com/Jonnyton/Workflow/pull/1064

## 32. GoldBean API (goldbean-api.xyz) — 120 endpoints fail batchTest after successful discovery

- Decision: drop
- Score: 73 -> 3
- Issue: https://github.com/Merit-Systems/x402scan/issues/923
- Reason: no clear open paid bounty signal >= $10 found

## 33. Scope team fee checkout loading state to the selected fee

- Decision: drop
- Score: 73 -> -77
- Issue: https://github.com/pauljsnider/allplays/issues/1286
- Reason: issue explicitly indicates no paid bounty or free-only payment status
- Reason: light competition allowed: 1 open competing PR(s)
- Reason: competition already visible in comments; still allowed in aggressive mode
- Competing PR: https://github.com/pauljsnider/allplays/pull/1287

## 34. [WIKI-DOCS] SPLITROOT C5 contract — command-while-you-wait (the Archon heartbeat; remove the dead-state gate on map table)

- Decision: drop
- Score: 73 -> -77
- Issue: https://github.com/Jonnyton/Workflow/issues/1039
- Reason: issue explicitly indicates no paid bounty or free-only payment status
- Reason: light competition allowed: 1 open competing PR(s)
- Reason: competition already visible in comments; still allowed in aggressive mode
- Competing PR: https://github.com/Jonnyton/Workflow/pull/1063

## 35. [WIKI-DOCS] SPLITROOT C4 contract — death + respawn loop (observer pawn, body picker, 5s timer)

- Decision: drop
- Score: 73 -> -27
- Issue: https://github.com/Jonnyton/Workflow/issues/1038
- Reason: issue explicitly indicates no paid bounty or free-only payment status

## 36. [repo-health] Medium: logout-button silently ignores signOut errors — user appears logged out locally but session remains on server

- Decision: drop
- Score: 73 -> 3
- Issue: https://github.com/Liohtml/ausschreibungen-app/issues/38
- Reason: no clear open paid bounty signal >= $10 found

## 37. [RFC]: Harden wallet_screening data pipeline, parsing, coverage, and report schema v2

- Decision: drop
- Score: 73 -> -27
- Issue: https://github.com/ARPAHLS/skillware/issues/115
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty

## 38. MRWK bounty: public docs and contributor onboarding improvements

- Decision: drop
- Score: 71 -> -49
- Issue: https://github.com/ramimbo/mergework/issues/114
- Reason: no clear open paid bounty signal >= $10 found
- Reason: light competition allowed: 1 open competing PR(s)
- Reason: competition already visible in comments; still allowed in aggressive mode
- Competing PR: https://github.com/ramimbo/mergework/pull/125

## 39. implement Algora task rules for comment and implementation

- Decision: drop
- Score: 61 -> -9
- Issue: https://github.com/xFengleN/MiniBountyFactory_LangGraph/issues/24
- Reason: no clear open paid bounty signal >= $10 found

## 40. [Bug] Badge create returns 200 when username is missing

- Decision: drop
- Score: 49 -> -21
- Issue: https://github.com/Scottcjn/Rustchain/issues/6198
- Reason: no clear open paid bounty signal >= $10 found

## 41. Pressure setting dissapered

- Decision: drop
- Score: 49 -> -21
- Issue: https://github.com/ankohanse/hass-dab-pumps/issues/99
- Reason: no clear open paid bounty signal >= $10 found

## 42. AI Builders Digest — 2026-05-24

- Decision: drop
- Score: 43 -> -27
- Issue: https://github.com/zarazhangrui/follow-builders/issues/45
- Reason: no clear open paid bounty signal >= $10 found

## 43. P1: Re-verify Tencent SSH known_hosts self-healing recurrence

- Decision: drop
- Score: 41 -> -64
- Issue: https://github.com/lanyusea/screeps/issues/1394
- Reason: no clear open paid bounty signal >= $10 found
- Reason: competition already visible in comments; still allowed in aggressive mode

## 44. Dev Tooling: Support for deployment factories

- Decision: drop
- Score: 39 -> -31
- Issue: https://github.com/ethereum-optimism/Retro-Funding/issues/12
- Reason: no clear open paid bounty signal >= $10 found

## 45. Sats to Local Currency | Mexico

- Decision: drop
- Score: 39 -> -66
- Issue: https://github.com/sutt/docs/issues/5
- Reason: no clear open paid bounty signal >= $10 found
- Reason: competition already visible in comments; still allowed in aggressive mode

## 46. Epic: Controlled Modular Rebuild — Simple Coach Default + Core Loop Modularization

- Decision: drop
- Score: 35 -> -70
- Issue: https://github.com/silentsn3akeR/Obscura_V2_MVP/issues/148
- Reason: no clear open paid bounty signal >= $10 found
- Reason: competition already visible in comments; still allowed in aggressive mode

## 47. [App] BountyPay

- Decision: drop
- Score: 35 -> -65
- Issue: https://github.com/gitcoinco/gitcoin_co_30/issues/391
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty

## 48. [App] uBounty

- Decision: drop
- Score: 35 -> -65
- Issue: https://github.com/gitcoinco/gitcoin_co_30/issues/390
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty

## 49. Fixing the bounty award system

- Decision: drop
- Score: 35 -> -35
- Issue: https://github.com/ResearchHub/issues/issues/531
- Reason: no clear open paid bounty signal >= $10 found

## 50. Create a Bounty Amount Box Issue

- Decision: drop
- Score: 35 -> -65
- Issue: https://github.com/ResearchHub/issues/issues/540
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty

## 51. Sync Issue-Assigned property from GH to LB

- Decision: drop
- Score: 35 -> -35
- Issue: https://github.com/Lightning-Bounties/progress-tracker/issues/53
- Reason: no clear open paid bounty signal >= $10 found

## 52. [post] Cash is what I used to buy my mum’s funeral flowers when her card...

- Decision: drop
- Score: 33 -> -37
- Issue: https://github.com/proxima424/westworld/issues/2199
- Reason: no clear open paid bounty signal >= $10 found
