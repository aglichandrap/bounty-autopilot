# GitHub Bounty Candidate Triage

Last run: 2026-05-22 17:29 UTC

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

## 4. "Send Invoice" failure shown as blocking native dialog instead of inline error

- Decision: drop
- Score: 85 -> 15
- Issue: https://github.com/tuttle-dev/tuttle/issues/264
- Reason: no clear open paid bounty signal >= $10 found

## 5. bug(create): mapEventToDb silently drops 12 event columns — paid/playlist/invite-style/series/geo data lost on create

- Decision: drop
- Score: 85 -> 15
- Issue: https://github.com/aliiishhh-nerd/tableaux/issues/60
- Reason: no clear open paid bounty signal >= $10 found

## 6. bug(transport): FileRegistry::write_atomic skips fsync — services.json can survive as a zero-padded ghost file after power-loss / hard-kill

- Decision: drop
- Score: 85 -> 15
- Issue: https://github.com/loonghao/dcc-mcp-core/issues/1104
- Reason: no clear open paid bounty signal >= $10 found

## 7. CRITICAL: "Generate Report" is a 100% hardcoded fake template (Proof attached)

- Decision: drop
- Score: 85 -> 15
- Issue: https://github.com/666ghj/MiroFish/issues/639
- Reason: no clear open paid bounty signal >= $10 found

## 8. [Bug]: xAI OAuth (xai-oauth) returns HTTP 403 for standard SuperGrok subscribers — backend enforcing Heavy-only despite docs claiming all tiers

- Decision: drop
- Score: 81 -> -54
- Issue: https://github.com/NousResearch/hermes-agent/issues/26847
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty
- Reason: competition already visible in comments; still allowed in aggressive mode

## 9. Spurious `PY02001` "Payment Gateway Error" in logs on successful Cash / Stripe Terminal checkouts

- Decision: drop
- Score: 79 -> 9
- Issue: https://github.com/wcpos/monorepo/issues/509
- Reason: no clear open paid bounty signal >= $10 found

## 10. bug: dolt-health zombie scan forks one ps per dolt PID — O(zombies) spawn storm under non-reaping PID 1

- Decision: drop
- Score: 79 -> -26
- Issue: https://github.com/gastownhall/gascity/issues/2482
- Reason: no clear open paid bounty signal >= $10 found
- Reason: competition already visible in comments; still allowed in aggressive mode

## 11. Project explorer doesn't show files of symlink VSCode does

- Decision: drop
- Score: 79 -> 9
- Issue: https://github.com/warpdotdev/warp/issues/11528
- Reason: no clear open paid bounty signal >= $10 found

## 12. Per-call-site LML timeouts: shorten /proxy/metadata/album to ~8s with existing search-URL fallback

- Decision: drop
- Score: 79 -> 9
- Issue: https://github.com/WXYC/Backend-Service/issues/990
- Reason: no clear open paid bounty signal >= $10 found

## 13. claude-companion injects full file contents instead of diffs — burns subscription token budget

- Decision: drop
- Score: 79 -> -21
- Issue: https://github.com/seungpyoson/codex-plugin-multi/issues/163
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty

## 14. Build Fizban's Wands — complete static e-commerce React site

- Decision: drop
- Score: 71 -> -64
- Issue: https://github.com/cindy-pi/ai-storefront-gpt/issues/3
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty
- Reason: competition already visible in comments; still allowed in aggressive mode

## 15. feat: mirror or selectively borrow ShotPattern app's aim-point UX (web + mobile)

- Decision: drop
- Score: 64 -> -6
- Issue: https://github.com/cner-smith/opengolfapp/issues/361
- Reason: no clear open paid bounty signal >= $10 found

## 16. P1: Restore local RL experiment-card fallback after NO_EXPERIMENT_CARD recurrence

- Decision: drop
- Score: 64 -> -6
- Issue: https://github.com/lanyusea/screeps/issues/1291
- Reason: no clear open paid bounty signal >= $10 found

## 17. [Bug] Course learning data endpoint is publicly accessible without authentication or enrollment check

- Decision: drop
- Score: 64 -> -6
- Issue: https://github.com/Mukesh-01-dev/Ai-Mentor/issues/320
- Reason: no clear open paid bounty signal >= $10 found

## 18. Microgrant Proposal: Field verified OpenStreetMap data

- Decision: drop
- Score: 63 -> -37
- Issue: https://github.com/osmfoundation/ewg_bidding/issues/24
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty

## 19. [FEATURE] Add stateful polling helper for pr-resolve-all settle window (replace time-based sleep)

- Decision: drop
- Score: 56 -> -49
- Issue: https://github.com/mikejmckinney/ai-repo-template/issues/326
- Reason: no clear open paid bounty signal >= $10 found
- Reason: competition already visible in comments; still allowed in aggressive mode

## 20. Codex Desktop visible chats fail to resume when saved provider id is no longer configured

- Decision: drop
- Score: 54 -> -16
- Issue: https://github.com/openai/codex/issues/22484
- Reason: no clear open paid bounty signal >= $10 found

## 21. WaterwayMap.org hosting costs

- Decision: drop
- Score: 54 -> -46
- Issue: https://github.com/osmfoundation/ewg_bidding/issues/45
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty

## 22. Microgrant Proposal: OSMAutoDrone

- Decision: drop
- Score: 54 -> -46
- Issue: https://github.com/osmfoundation/ewg_bidding/issues/39
- Reason: issue explicitly indicates no paid bounty or free-only payment status

## 23. MICROGRANT PROPOSAL:OSM-BASED DASHBOARD FOR CLIMATE CHANGE MONITORING IN AFRICA

- Decision: drop
- Score: 54 -> -16
- Issue: https://github.com/osmfoundation/ewg_bidding/issues/22
- Reason: no clear open paid bounty signal >= $10 found

## 24. Microgrant Proposal: Enhancing Drone Tasking Manager for Multi-Drone Support and Operational Refinements

- Decision: drop
- Score: 54 -> -46
- Issue: https://github.com/osmfoundation/ewg_bidding/issues/28
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty

## 25. MicroGrant Proposal : OSMSG

- Decision: drop
- Score: 54 -> -16
- Issue: https://github.com/osmfoundation/ewg_bidding/issues/30
- Reason: no clear open paid bounty signal >= $10 found

## 26. MIcrogrant Proposal: OSMLocalizer

- Decision: drop
- Score: 54 -> -46
- Issue: https://github.com/osmfoundation/ewg_bidding/issues/29
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty

## 27. Microgrant Proposal: OpenStreetMap Before-After Maps Generator

- Decision: drop
- Score: 54 -> -16
- Issue: https://github.com/osmfoundation/ewg_bidding/issues/27
- Reason: no clear open paid bounty signal >= $10 found

## 28. Runner task: create fresh tiny PR for Telegram approve pilot

- Decision: drop
- Score: 49 -> -21
- Issue: https://github.com/alanua/Skeleton/issues/187
- Reason: no clear open paid bounty signal >= $10 found

## 29. Claude Code suggests non-existent "fan out subagents" command

- Decision: drop
- Score: 49 -> -56
- Issue: https://github.com/anthropics/claude-code/issues/61491
- Reason: no clear open paid bounty signal >= $10 found
- Reason: competition already visible in comments; still allowed in aggressive mode

## 30. Microgrant Proposal: Map Review Team

- Decision: drop
- Score: 48 -> -22
- Issue: https://github.com/osmfoundation/ewg_bidding/issues/46
- Reason: no clear open paid bounty signal >= $10 found

## 31. Microgrant Proposal: GeoAI for Maternal Health Risk Mapping in Kenya

- Decision: drop
- Score: 48 -> -22
- Issue: https://github.com/osmfoundation/ewg_bidding/issues/43
- Reason: no clear open paid bounty signal >= $10 found

## 32. Microgrant Proposal: Campus Guide

- Decision: drop
- Score: 48 -> -22
- Issue: https://github.com/osmfoundation/ewg_bidding/issues/23
- Reason: no clear open paid bounty signal >= $10 found

## 33. Draft: MIcrogrant Proposal- OSMLocalizer

- Decision: drop
- Score: 48 -> -52
- Issue: https://github.com/osgeonepal/site/issues/74
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty

## 34. Record and release training video based on VIDEO_6_SCRIPT.md

- Decision: drop
- Score: 46 -> -24
- Issue: https://github.com/asyncapi/training/issues/65
- Reason: no clear open paid bounty signal >= $10 found

## 35. Multiline slash commands should not be evaluated as a comment

- Decision: drop
- Score: 45 -> -25
- Issue: https://github.com/devpool-directory/devpool-directory/issues/5873
- Reason: no clear open paid bounty signal >= $10 found

## 36. Insulation as Infrastructure: supporting “Dobra Maisternia” in frontline Kharkiv region

- Decision: drop
- Score: 44 -> -26
- Issue: https://github.com/maxzalevski/community_spaces/issues/7
- Reason: no clear open paid bounty signal >= $10 found

## 37. W3I Network Initiative in Action: Building a Sarafu-Based DAO for Regenerative Coordination in Ukraine

- Decision: drop
- Score: 44 -> -26
- Issue: https://github.com/maxzalevski/grants/issues/2
- Reason: no clear open paid bounty signal >= $10 found

## 38. Radaria three bunk beds in hostel

- Decision: drop
- Score: 44 -> -26
- Issue: https://github.com/maxzalevski/community_spaces/issues/6
- Reason: no clear open paid bounty signal >= $10 found

## 39. Add policies / visa letter page

- Decision: drop
- Score: 44 -> -26
- Issue: https://github.com/open-life-science/open-life-science.github.io/issues/1108
- Reason: no clear open paid bounty signal >= $10 found

## 40. Meeting [2025-06-06]

- Decision: drop
- Score: 44 -> -26
- Issue: https://github.com/osgeonepal/site/issues/73
- Reason: no clear open paid bounty signal >= $10 found

## 41. **Message from Whitehat**

- Decision: drop
- Score: 43 -> -27
- Issue: https://github.com/qubic/core/issues/892
- Reason: no clear open paid bounty signal >= $10 found

## 42. BYOK fails to start

- Decision: drop
- Score: 41 -> -29
- Issue: https://github.com/warpdotdev/warp/issues/11538
- Reason: no clear open paid bounty signal >= $10 found

## 43. [Bug] Subagent delegation lacks timeout, monitoring, and abort controls—caused 12+ hour session hang

- Decision: drop
- Score: 41 -> -64
- Issue: https://github.com/anthropics/claude-code/issues/61405
- Reason: no clear open paid bounty signal >= $10 found
- Reason: competition already visible in comments; still allowed in aggressive mode

## 44. [Bug] Can't run on MacOS - Damaged

- Decision: drop
- Score: 41 -> -29
- Issue: https://github.com/phodal/routa/issues/552
- Reason: no clear open paid bounty signal >= $10 found

## 45. Prior-turn agent commitments are silently dropped on operator task-shift unless explicitly re-anchored

- Decision: drop
- Score: 41 -> -64
- Issue: https://github.com/anthropics/claude-code/issues/61388
- Reason: no clear open paid bounty signal >= $10 found
- Reason: competition already visible in comments; still allowed in aggressive mode

## 46. Microgrant Proposal: Redesign of the OSM Apps Catalog to reach a wider audience

- Decision: drop
- Score: 40 -> -60
- Issue: https://github.com/osmfoundation/ewg_bidding/issues/31
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty

## 47. Set of issues for resolution under the MICROGRANT Program 2026-05

- Decision: drop
- Score: 40 -> -65
- Issue: https://github.com/asyncapi/cli/issues/2124
- Reason: no clear open paid bounty signal >= $10 found
- Reason: competition already visible in comments; still allowed in aggressive mode

## 48. PauseAI.se takes up first place in google

- Decision: drop
- Score: 40 -> -30
- Issue: https://github.com/PauseAI/pauseai-website/issues/385
- Reason: no clear open paid bounty signal >= $10 found

## 49. Microgrant Proposal: StreetComplete as an entry point to OpenStreetMap

- Decision: drop
- Score: 40 -> -65
- Issue: https://github.com/osmfoundation/ewg_bidding/issues/34
- Reason: no clear open paid bounty signal >= $10 found
- Reason: competition already visible in comments; still allowed in aggressive mode

## 50. Microgrant Proposal: Underpass stabilization, packaging and testing

- Decision: drop
- Score: 40 -> -30
- Issue: https://github.com/osmfoundation/ewg_bidding/issues/42
- Reason: no clear open paid bounty signal >= $10 found

## 51. Microgrant Proposal: Localized Open Geocoder Plugin for Ethiopia and Africa

- Decision: drop
- Score: 40 -> -30
- Issue: https://github.com/osmfoundation/ewg_bidding/issues/21
- Reason: no clear open paid bounty signal >= $10 found

## 52. Microgrant Proposal: AI-Based Feature Extraction from Satellite Imagery for OpenStreetMap (OSM) Enrichment

- Decision: drop
- Score: 40 -> -60
- Issue: https://github.com/osmfoundation/ewg_bidding/issues/38
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty

## 53. Microgrant proposal: Speedwalk

- Decision: drop
- Score: 40 -> -30
- Issue: https://github.com/osmfoundation/ewg_bidding/issues/25
- Reason: no clear open paid bounty signal >= $10 found

## 54. Microgrant Proposal: Data Rescue Pipeline - Preserving Deleted OpenStreetMap Features in OpenHistoricalMap

- Decision: drop
- Score: 40 -> -30
- Issue: https://github.com/osmfoundation/ewg_bidding/issues/41
- Reason: no clear open paid bounty signal >= $10 found

## 55. Microgrant Proposal: Atlas Design System & Modernization of OSM.org

- Decision: drop
- Score: 40 -> -60
- Issue: https://github.com/osmfoundation/ewg_bidding/issues/26
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty
