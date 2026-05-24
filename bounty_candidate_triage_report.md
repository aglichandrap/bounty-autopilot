# GitHub Bounty Candidate Triage

Last run: 2026-05-24 16:45 UTC

Kept candidates: 2

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

## 7. Critical: audit all tx.execute(SELECT *) callsites in commandBus.ts — snake_case reads silently return undefined

- Decision: drop
- Score: 85 -> 15
- Issue: https://github.com/EvanTenenbaum/terp-operator/issues/267
- Reason: no clear open paid bounty signal >= $10 found

## 8. Mapper sub-agent runs out of turns when the verifier rejects the first attempt (maxTurns: 4 too tight)

- Decision: drop
- Score: 85 -> 15
- Issue: https://github.com/Pleusch/SharpMind/issues/205
- Reason: no clear open paid bounty signal >= $10 found

## 9. Test runs leak orphan processes (Puppeteer chromium + testhost + Mangarr.Console) — needs unified pre-flight + validation harness

- Decision: drop
- Score: 85 -> 15
- Issue: https://github.com/devbrian/Mangarr/issues/252
- Reason: no clear open paid bounty signal >= $10 found

## 10. test(d8): remaining failure modes F1-F10 (post-D7 sign-off)

- Decision: drop
- Score: 85 -> 15
- Issue: https://github.com/dreamlx/lh-enterprise/issues/345
- Reason: no clear open paid bounty signal >= $10 found

## 11. Stale comments in DefaultConfig claim a finite retry default, contradicting the actual unbounded behavior

- Decision: drop
- Score: 85 -> 15
- Issue: https://github.com/xrf9268-hue/aiops-platform/issues/367
- Reason: no clear open paid bounty signal >= $10 found

## 12. Ollama model swaps in mixed ingests pay full reload cost on every switch

- Decision: drop
- Score: 85 -> 15
- Issue: https://github.com/jswest/bartleby/issues/11
- Reason: no clear open paid bounty signal >= $10 found

## 13. Roadmap: turn GradSharp from CV builder into application-pack engine

- Decision: drop
- Score: 85 -> 15
- Issue: https://github.com/vanadiuminternational/HireReady/issues/57
- Reason: no clear open paid bounty signal >= $10 found

## 14. [WIKI-DOCS] SPLITROOT polish — representative audio direction (rung-2 gate; four-layer cue discipline + faction palettes)

- Decision: drop
- Score: 79 -> -56
- Issue: https://github.com/Jonnyton/Workflow/issues/1059
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty
- Reason: competition already visible in comments; still allowed in aggressive mode

## 15. Critical data loss: startup GC silently deletes all session transcripts

- Decision: drop
- Score: 79 -> 9
- Issue: https://github.com/anthropics/claude-code/issues/62041
- Reason: no clear open paid bounty signal >= $10 found

## 16. Explorer page: Miner data stuck at 'Loading miners...' indefinitely (frontend rendering bug)

- Decision: drop
- Score: 79 -> 9
- Issue: https://github.com/Scottcjn/Rustchain/issues/6211
- Reason: no clear open paid bounty signal >= $10 found

## 17. [WIKI-DOCS] SPLITROOT hero plan — Briar Saint + Master Artificer (the two starting heroes; horizontal-only paid discipline locked)

- Decision: drop
- Score: 79 -> -56
- Issue: https://github.com/Jonnyton/Workflow/issues/1054
- Reason: issue explicitly indicates no paid bounty or free-only payment status
- Reason: competition already visible in comments; still allowed in aggressive mode

## 18. [WIKI-DESIGN] Factory branch substrate improvement — JSONify faction registry (eliminate the biggest remix-friction point)

- Decision: drop
- Score: 79 -> -56
- Issue: https://github.com/Jonnyton/Workflow/issues/1050
- Reason: issue explicitly indicates no paid bounty or free-only payment status
- Reason: competition already visible in comments; still allowed in aggressive mode

## 19. Slice 16 — PaymentExecution (bank transfer) + QR + screenshot + DB constraints

- Decision: drop
- Score: 79 -> 9
- Issue: https://github.com/yutobeo2024/KT/issues/18
- Reason: no clear open paid bounty signal >= $10 found

## 20. [WIKI-DOCS] SPLITROOT "Second 60 Seconds" combat slice — death/respawn loop, faction weapons, command-while-you-wait (rung-2 anchor)

- Decision: drop
- Score: 79 -> -56
- Issue: https://github.com/Jonnyton/Workflow/issues/1042
- Reason: issue explicitly indicates no paid bounty or free-only payment status
- Reason: competition already visible in comments; still allowed in aggressive mode

## 21. Keep the map tile cache in sync with feature writes (write-reactive invalidation)

- Decision: drop
- Score: 79 -> -21
- Issue: https://github.com/un-fao/GeoID/issues/1292
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty

## 22. README whitepaper PDF link times out via raw.githubusercontent.com

- Decision: drop
- Score: 79 -> -26
- Issue: https://github.com/Scottcjn/Rustchain/issues/6202
- Reason: no clear open paid bounty signal >= $10 found
- Reason: competition already visible in comments; still allowed in aggressive mode

## 23. [WIKI-DOCS] SPLITROOT C6 contract — second-60-seconds integration smoke (Proof/second-60-seconds-smoke.ps1)

- Decision: drop
- Score: 79 -> -56
- Issue: https://github.com/Jonnyton/Workflow/issues/1040
- Reason: issue explicitly indicates no paid bounty or free-only payment status
- Reason: competition already visible in comments; still allowed in aggressive mode

## 24. GoldBean API (goldbean-api.xyz) — 120 endpoints fail batchTest after successful discovery

- Decision: drop
- Score: 79 -> 9
- Issue: https://github.com/Merit-Systems/x402scan/issues/923
- Reason: no clear open paid bounty signal >= $10 found

## 25. Scope team fee checkout loading state to the selected fee

- Decision: drop
- Score: 79 -> -56
- Issue: https://github.com/pauljsnider/allplays/issues/1286
- Reason: issue explicitly indicates no paid bounty or free-only payment status
- Reason: competition already visible in comments; still allowed in aggressive mode

## 26. [WIKI-DESIGN] Factory branch remix proof — "STELLAR FRONT" sci-fi canary scoped against SPLITROOT substrate (the factory's product validation)

- Decision: drop
- Score: 79 -> -21
- Issue: https://github.com/Jonnyton/Workflow/issues/1049
- Reason: issue explicitly indicates no paid bounty or free-only payment status

## 27. [WIKI-DESIGN] Factory branch games/ directory substrate contract — multi-canary physical layout + second-canary spawn workflow

- Decision: drop
- Score: 79 -> -21
- Issue: https://github.com/Jonnyton/Workflow/issues/1048
- Reason: issue explicitly indicates no paid bounty or free-only payment status

## 28. How Strong Backlinks Continue Supporting Long Term SEO Results

- Decision: drop
- Score: 79 -> 9
- Issue: https://github.com/vefoGix00/VefoGix-/issues/372
- Reason: no clear open paid bounty signal >= $10 found

## 29. Why Strong SEO Link Building Still Matters For Online Growth

- Decision: drop
- Score: 79 -> 9
- Issue: https://github.com/vefoGix00/VefoGix-/issues/371
- Reason: no clear open paid bounty signal >= $10 found

## 30. [WIKI-PATCH] Add concurrent-session discipline to chatbot-builder-behaviors: in-flight markers + required sha256 on patches when concurrency is possible

- Decision: drop
- Score: 79 -> -21
- Issue: https://github.com/Jonnyton/Workflow/issues/1029
- Reason: issue explicitly indicates no paid bounty or free-only payment status

## 31. [WIKI-DOCS] SPLITROOT two-session coordination — Opus 4.7 + GPT-5.5 Codex as passion-project siblings, model-grounded routing

- Decision: drop
- Score: 73 -> -62
- Issue: https://github.com/Jonnyton/Workflow/issues/1034
- Reason: issue explicitly indicates no paid bounty or free-only payment status
- Reason: competition already visible in comments; still allowed in aggressive mode

## 32. [WIKI-DOCS] SPLITROOT C5 contract — command-while-you-wait (the Archon heartbeat; remove the dead-state gate on map table)

- Decision: drop
- Score: 73 -> -62
- Issue: https://github.com/Jonnyton/Workflow/issues/1039
- Reason: issue explicitly indicates no paid bounty or free-only payment status
- Reason: competition already visible in comments; still allowed in aggressive mode

## 33. [WIKI-DOCS] SPLITROOT C4 contract — death + respawn loop (observer pawn, body picker, 5s timer)

- Decision: drop
- Score: 73 -> -27
- Issue: https://github.com/Jonnyton/Workflow/issues/1038
- Reason: issue explicitly indicates no paid bounty or free-only payment status

## 34. [repo-health] Medium: logout-button silently ignores signOut errors — user appears logged out locally but session remains on server

- Decision: drop
- Score: 73 -> 3
- Issue: https://github.com/Liohtml/ausschreibungen-app/issues/38
- Reason: no clear open paid bounty signal >= $10 found

## 35. [RFC]: Harden wallet_screening data pipeline, parsing, coverage, and report schema v2

- Decision: drop
- Score: 73 -> -27
- Issue: https://github.com/ARPAHLS/skillware/issues/115
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty

## 36. [WIKI-DOCS] SPLITROOT S6 contract — first-60-seconds integration smoke (Proof/first-60-seconds-smoke.ps1)

- Decision: drop
- Score: 73 -> -62
- Issue: https://github.com/Jonnyton/Workflow/issues/1033
- Reason: issue explicitly indicates no paid bounty or free-only payment status
- Reason: competition already visible in comments; still allowed in aggressive mode

## 37. implement Algora task rules for comment and implementation

- Decision: drop
- Score: 61 -> -9
- Issue: https://github.com/xFengleN/MiniBountyFactory_LangGraph/issues/24
- Reason: no clear open paid bounty signal >= $10 found

## 38. Opire

- Decision: keep
- Score: 55 -> 20
- Issue: https://github.com/ubiquity/business-development/issues/89
- Reason: competition already visible in comments; still allowed in aggressive mode

## 39. CookieRift

- Decision: drop
- Score: 51 -> -19
- Issue: https://github.com/davidrencse/damocles/issues/17
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

## 44. Sats to Local Currency | Mexico

- Decision: drop
- Score: 39 -> -66
- Issue: https://github.com/sutt/docs/issues/5
- Reason: no clear open paid bounty signal >= $10 found
- Reason: competition already visible in comments; still allowed in aggressive mode

## 45. BIM Workbench: Adding Missing Information

- Decision: drop
- Score: 35 -> -35
- Issue: https://github.com/Reqrefusion/FreeCAD-Documentation-Project/issues/26
- Reason: no clear open paid bounty signal >= $10 found

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

## 49. [post] Cash is what I used to buy my mum’s funeral flowers when her card...

- Decision: drop
- Score: 33 -> -37
- Issue: https://github.com/proxima424/westworld/issues/2199
- Reason: no clear open paid bounty signal >= $10 found

## 50. [refactor-design] cluster-087-mcp-connector-registry-disposal(iter87)

- Decision: drop
- Score: 31 -> -39
- Issue: https://github.com/aevatarAI/aevatar/issues/988
- Reason: no clear open paid bounty signal >= $10 found
