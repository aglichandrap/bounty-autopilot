# GitHub Bounty Candidate Triage

Last run: 2026-05-21 09:46 UTC

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

## 4. [CAL-3105] BigBlueButton Integration

- Decision: keep
- Score: 145 -> 110
- Issue: https://github.com/calcom/cal.com/issues/1985
- Reason: competition already visible in comments; still allowed in aggressive mode

## 5. P0: Correct Loop A Tencent stuck-run age classifier

- Decision: drop
- Score: 110 -> 40
- Issue: https://github.com/lanyusea/screeps/issues/1297
- Reason: no clear open paid bounty signal >= $10 found

## 6. Bounty: USDC for first external agent x402 MCP call

- Decision: drop
- Score: 86 -> 16
- Issue: https://github.com/RileyCraig14/nexus-agent/issues/1
- Reason: no clear open paid bounty signal >= $10 found

## 7. quality: ?? "default" fallbacks mask backend failure on /customer/billing — anti-pattern: defensive fallbacks on data that should never be missing

- Decision: drop
- Score: 85 -> 15
- Issue: https://github.com/iogrid/iogrid/issues/417
- Reason: no clear open paid bounty signal >= $10 found

## 8. bug: affiliate click tracking failures break redirects

- Decision: drop
- Score: 85 -> -35
- Issue: https://github.com/profullstack/ugig.net/issues/210
- Reason: no clear open paid bounty signal >= $10 found
- Reason: light competition allowed: 1 open competing PR(s)
- Reason: competition already visible in comments; still allowed in aggressive mode
- Competing PR: https://github.com/profullstack/ugig.net/pull/211

## 9. bug: manual affiliate conversion notes can crash after insert

- Decision: drop
- Score: 85 -> -35
- Issue: https://github.com/profullstack/ugig.net/issues/208
- Reason: no clear open paid bounty signal >= $10 found
- Reason: light competition allowed: 1 open competing PR(s)
- Reason: competition already visible in comments; still allowed in aggressive mode
- Competing PR: https://github.com/profullstack/ugig.net/pull/209

## 10. bug: affiliate conversion edits can mark commissions paid without payout

- Decision: drop
- Score: 85 -> -35
- Issue: https://github.com/profullstack/ugig.net/issues/205
- Reason: no clear open paid bounty signal >= $10 found
- Reason: light competition allowed: 1 open competing PR(s)
- Reason: competition already visible in comments; still allowed in aggressive mode
- Competing PR: https://github.com/profullstack/ugig.net/pull/207

## 11. P0 #2 Live-Blocker — Provision-Auszahlungs-Tracking aus alt-CRM portieren

- Decision: drop
- Score: 85 -> 15
- Issue: https://github.com/ZAP-Wunschlachen/wunschlachen-crm/issues/37
- Reason: no clear open paid bounty signal >= $10 found

## 12. fix(payment): handleSuccess/handleFail 동시성 결함 — JPA L1 캐시 + 2-phase lock

- Decision: drop
- Score: 85 -> 15
- Issue: https://github.com/chunbae-tour/chunbae-tour/issues/114
- Reason: no clear open paid bounty signal >= $10 found

## 13. Self-hosted code review pipeline aborts: `400 invalid temperature: only 1 is allowed for this model`

- Decision: drop
- Score: 85 -> 15
- Issue: https://github.com/kodustech/kodus-ai/issues/1146
- Reason: no clear open paid bounty signal >= $10 found

## 14. [Bug] maintainer_cut carve-out paid to penalized miners despite zeroed scoring

- Decision: drop
- Score: 85 -> 0
- Issue: https://github.com/entrius/gittensor/issues/1328
- Reason: no clear open paid bounty signal >= $10 found
- Reason: light competition allowed: 1 open competing PR(s)
- Competing PR: https://github.com/entrius/gittensor/pull/1329

## 15. [Bug]: xAI OAuth (xai-oauth) returns HTTP 403 for standard SuperGrok subscribers — backend enforcing Heavy-only despite docs claiming all tiers

- Decision: drop
- Score: 81 -> -34
- Issue: https://github.com/NousResearch/hermes-agent/issues/26847
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty
- Reason: light competition allowed: 1 open competing PR(s)
- Competing PR: https://github.com/NousResearch/hermes-agent/pull/29348

## 16. bug: affiliate tracking link copy fails when Clipboard API is blocked

- Decision: drop
- Score: 79 -> -26
- Issue: https://github.com/profullstack/ugig.net/issues/155
- Reason: no clear open paid bounty signal >= $10 found
- Reason: competition already visible in comments; still allowed in aggressive mode

## 17. bug: manual affiliate payouts can bypass settlement delay

- Decision: drop
- Score: 79 -> -26
- Issue: https://github.com/profullstack/ugig.net/issues/212
- Reason: no clear open paid bounty signal >= $10 found
- Reason: competition already visible in comments; still allowed in aggressive mode

## 18. bug: reapplying affiliates lose their existing tracking link

- Decision: drop
- Score: 79 -> -26
- Issue: https://github.com/profullstack/ugig.net/issues/160
- Reason: no clear open paid bounty signal >= $10 found
- Reason: competition already visible in comments; still allowed in aggressive mode

## 19. P1: Restore true policy-update iterations after fixed-vector recurrence

- Decision: drop
- Score: 79 -> -26
- Issue: https://github.com/lanyusea/screeps/issues/1295
- Reason: no clear open paid bounty signal >= $10 found
- Reason: competition already visible in comments; still allowed in aggressive mode

## 20. [Bug] moonlight/Artemis shortcut card

- Decision: drop
- Score: 79 -> -21
- Issue: https://github.com/spocky/miproja1/issues/514
- Reason: issue explicitly indicates no paid bounty or free-only payment status

## 21. [WIKI-DESIGN] Goal selection logic should be user-buildable — bind a selector branch instead of baking formula into platform quality_leaderboard

- Decision: drop
- Score: 79 -> -56
- Issue: https://github.com/Jonnyton/Workflow/issues/995
- Reason: issue explicitly indicates no paid bounty or free-only payment status
- Reason: competition already visible in comments; still allowed in aggressive mode

## 22. PACT Protocol — Trustless Agent Commerce Infrastructure on FVM (Open Grant)

- Decision: keep
- Score: 63 -> 63
- Issue: https://github.com/filecoin-project/devgrants/issues/2081

## 23. Microgrant Proposal: Field verified OpenStreetMap data

- Decision: drop
- Score: 63 -> -37
- Issue: https://github.com/osmfoundation/ewg_bidding/issues/24
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty

## 24. 📡 P3 RADAR 🔴 [ZEC/USD/4H] ▼ BAJISTA (SHORT) · 04h BOG

- Decision: drop
- Score: 60 -> -40
- Issue: https://github.com/Metapro-art/zec-scanner/issues/159
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty

## 25. Gap-analysis: ItemsReadPolicy SSOT (axis 2 private indexer already shipped)

- Decision: drop
- Score: 56 -> -14
- Issue: https://github.com/un-fao/GeoID/issues/950
- Reason: no clear open paid bounty signal >= $10 found

## 26. [rocket-pool] DEFI@home

- Decision: keep
- Score: 55 -> 20
- Issue: https://github.com/guil-lambert/defipunkd/issues/227
- Reason: competition already visible in comments; still allowed in aggressive mode

## 27. [Audit] General sweep 2026-05-11

- Decision: drop
- Score: 54 -> -16
- Issue: https://github.com/RUNSTR-LLC/RUNSTR/issues/331
- Reason: no clear open paid bounty signal >= $10 found

## 28. Resistent Memory for instructions

- Decision: drop
- Score: 54 -> -46
- Issue: https://github.com/deepseek-ai/DeepSeek-V3/issues/1225
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty

## 29. WaterwayMap.org hosting costs

- Decision: drop
- Score: 54 -> -46
- Issue: https://github.com/osmfoundation/ewg_bidding/issues/45
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty

## 30. Microgrant Proposal: OSMAutoDrone

- Decision: drop
- Score: 54 -> -46
- Issue: https://github.com/osmfoundation/ewg_bidding/issues/39
- Reason: issue explicitly indicates no paid bounty or free-only payment status

## 31. MICROGRANT PROPOSAL:OSM-BASED DASHBOARD FOR CLIMATE CHANGE MONITORING IN AFRICA

- Decision: drop
- Score: 54 -> -16
- Issue: https://github.com/osmfoundation/ewg_bidding/issues/22
- Reason: no clear open paid bounty signal >= $10 found

## 32. Microgrant Proposal: Enhancing Drone Tasking Manager for Multi-Drone Support and Operational Refinements

- Decision: drop
- Score: 54 -> -46
- Issue: https://github.com/osmfoundation/ewg_bidding/issues/28
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty

## 33. MicroGrant Proposal : OSMSG

- Decision: drop
- Score: 54 -> -16
- Issue: https://github.com/osmfoundation/ewg_bidding/issues/30
- Reason: no clear open paid bounty signal >= $10 found

## 34. MIcrogrant Proposal: OSMLocalizer

- Decision: drop
- Score: 54 -> -46
- Issue: https://github.com/osmfoundation/ewg_bidding/issues/29
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty

## 35. Microgrant Proposal: OpenStreetMap Before-After Maps Generator

- Decision: drop
- Score: 54 -> -16
- Issue: https://github.com/osmfoundation/ewg_bidding/issues/27
- Reason: no clear open paid bounty signal >= $10 found

## 36. Bug: plugin skill discovery broken -- 0 skills loaded for mcp-server-dev AND sonatype-guide (ecosystem-wide pattern)

- Decision: drop
- Score: 49 -> -21
- Issue: https://github.com/anthropics/claude-plugins-official/issues/1954
- Reason: no clear open paid bounty signal >= $10 found

## 37. Circular import: blocks.registry ↔ ai.agent.* (10-module cross-layer SCC)

- Decision: drop
- Score: 49 -> -51
- Issue: https://github.com/zjzcpj/SciStudio/issues/1336
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty

## 38. Record and release training video based on VIDEO_6_SCRIPT.md

- Decision: drop
- Score: 48 -> -22
- Issue: https://github.com/asyncapi/training/issues/65
- Reason: no clear open paid bounty signal >= $10 found

## 39. Microgrant Proposal: Map Review Team

- Decision: drop
- Score: 48 -> -22
- Issue: https://github.com/osmfoundation/ewg_bidding/issues/46
- Reason: no clear open paid bounty signal >= $10 found

## 40. Microgrant Proposal: GeoAI for Maternal Health Risk Mapping in Kenya

- Decision: drop
- Score: 48 -> -22
- Issue: https://github.com/osmfoundation/ewg_bidding/issues/43
- Reason: no clear open paid bounty signal >= $10 found

## 41. Microgrant Proposal: Campus Guide

- Decision: drop
- Score: 48 -> -22
- Issue: https://github.com/osmfoundation/ewg_bidding/issues/23
- Reason: no clear open paid bounty signal >= $10 found

## 42. Draft: MIcrogrant Proposal- OSMLocalizer

- Decision: drop
- Score: 48 -> -52
- Issue: https://github.com/osgeonepal/site/issues/74
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty

## 43. [Ulduar] - Problems with Immortal Guardian.

- Decision: drop
- Score: 47 -> -23
- Issue: https://github.com/azerothcore/azerothcore-wotlk/issues/4989
- Reason: no clear open paid bounty signal >= $10 found

## 44. WhatsApp support for agents similar to MS Teams and Slack

- Decision: keep
- Score: 46 -> 11
- Issue: https://github.com/archestra-ai/archestra/issues/4145
- Reason: competition already visible in comments; still allowed in aggressive mode

## 45. 🚀 Avo 4 status and feedback

- Decision: drop
- Score: 46 -> -54
- Issue: https://github.com/avo-hq/avo/issues/4349
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty

## 46. Insulation as Infrastructure: supporting “Dobra Maisternia” in frontline Kharkiv region

- Decision: drop
- Score: 44 -> -26
- Issue: https://github.com/maxzalevski/community_spaces/issues/7
- Reason: no clear open paid bounty signal >= $10 found

## 47. W3I Network Initiative in Action: Building a Sarafu-Based DAO for Regenerative Coordination in Ukraine

- Decision: drop
- Score: 44 -> -26
- Issue: https://github.com/maxzalevski/grants/issues/2
- Reason: no clear open paid bounty signal >= $10 found

## 48. Radaria three bunk beds in hostel

- Decision: drop
- Score: 44 -> -26
- Issue: https://github.com/maxzalevski/community_spaces/issues/6
- Reason: no clear open paid bounty signal >= $10 found

## 49. Add policies / visa letter page

- Decision: drop
- Score: 44 -> -26
- Issue: https://github.com/open-life-science/open-life-science.github.io/issues/1108
- Reason: no clear open paid bounty signal >= $10 found

## 50. Meeting [2025-06-06]

- Decision: drop
- Score: 44 -> -26
- Issue: https://github.com/osgeonepal/site/issues/73
- Reason: no clear open paid bounty signal >= $10 found

## 51. [FEATURE] Add Empty States and Skeleton Loaders for Better UX

- Decision: drop
- Score: 43 -> -57
- Issue: https://github.com/RatLoopz/sahidawa-india/issues/381
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty

## 52. [ui] Phase 6.4 · Token-spend dashboard (per role / project / day)

- Decision: drop
- Score: 43 -> -27
- Issue: https://github.com/svv2014/loop-monitor/issues/137
- Reason: no clear open paid bounty signal >= $10 found

## 53. Bazaar discovery not indexing after successful CDP settlement on Base Mainnet

- Decision: drop
- Score: 41 -> -29
- Issue: https://github.com/x402-foundation/x402/issues/2156
- Reason: no clear open paid bounty signal >= $10 found

## 54. Microgrant Proposal: Redesign of the OSM Apps Catalog to reach a wider audience

- Decision: drop
- Score: 40 -> -60
- Issue: https://github.com/osmfoundation/ewg_bidding/issues/31
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty

## 55. Set of issues for resolution under the MICROGRANT Program 2026-05

- Decision: drop
- Score: 40 -> -65
- Issue: https://github.com/asyncapi/cli/issues/2124
- Reason: no clear open paid bounty signal >= $10 found
- Reason: competition already visible in comments; still allowed in aggressive mode

## 56. PauseAI.se takes up first place in google

- Decision: drop
- Score: 40 -> -30
- Issue: https://github.com/PauseAI/pauseai-website/issues/385
- Reason: no clear open paid bounty signal >= $10 found

## 57. Microgrant Proposal: StreetComplete as an entry point to OpenStreetMap

- Decision: drop
- Score: 40 -> -65
- Issue: https://github.com/osmfoundation/ewg_bidding/issues/34
- Reason: no clear open paid bounty signal >= $10 found
- Reason: competition already visible in comments; still allowed in aggressive mode

## 58. Microgrant Proposal: Underpass stabilization, packaging and testing

- Decision: drop
- Score: 40 -> -30
- Issue: https://github.com/osmfoundation/ewg_bidding/issues/42
- Reason: no clear open paid bounty signal >= $10 found

## 59. Microgrant Proposal: Localized Open Geocoder Plugin for Ethiopia and Africa

- Decision: drop
- Score: 40 -> -30
- Issue: https://github.com/osmfoundation/ewg_bidding/issues/21
- Reason: no clear open paid bounty signal >= $10 found
