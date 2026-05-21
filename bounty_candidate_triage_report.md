# GitHub Bounty Candidate Triage

Last run: 2026-05-21 16:05 UTC

Kept candidates: 17

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

## 4. [CAL-3105] BigBlueButton Integration

- Decision: keep
- Score: 145 -> 110
- Issue: https://github.com/calcom/cal.com/issues/1985
- Reason: competition already visible in comments; still allowed in aggressive mode

## 5. [BUG][低] KANG_F11 活动 Download 没反应

- Decision: keep
- Score: 104 -> 69
- Issue: https://github.com/LeoVeeNetVip/team-docs/issues/125
- Reason: competition already visible in comments; still allowed in aggressive mode

## 6. [BUG][中] JIAN_15 注册后无邮件 + 后台无记录

- Decision: keep
- Score: 104 -> 69
- Issue: https://github.com/LeoVeeNetVip/team-docs/issues/105
- Reason: competition already visible in comments; still allowed in aggressive mode

## 7. [BUG][高] L_13 VIP 规则奖励应为「锁」vip-rule reward ·

- Decision: drop
- Score: 104 -> -1
- Issue: https://github.com/LeoVeeNetVip/team-docs/issues/75
- Reason: no clear open paid bounty signal >= $10 found
- Reason: competition already visible in comments; still allowed in aggressive mode

## 8. Address Kafka 4.3.0 moving non-public classes to an internal subpackage

- Decision: drop
- Score: 104 -> -1
- Issue: https://github.com/kroxylicious/kroxylicious/issues/3996
- Reason: no clear open paid bounty signal >= $10 found
- Reason: competition already visible in comments; still allowed in aggressive mode

## 9. [BUG][高] L_2 新用户没收到欢迎邮件

- Decision: keep
- Score: 104 -> 69
- Issue: https://github.com/LeoVeeNetVip/team-docs/issues/64
- Reason: competition already visible in comments; still allowed in aggressive mode

## 10. 探索bug

- Decision: drop
- Score: 96 -> 26
- Issue: https://github.com/AzurTian/OnmyojiAutoScript/issues/105
- Reason: no clear open paid bounty signal >= $10 found

## 11. [Experiment] P1.3 Formal baseline training and evaluation

- Decision: drop
- Score: 85 -> 15
- Issue: https://github.com/w2030298-art/HybridArena/issues/8
- Reason: no clear open paid bounty signal >= $10 found

## 12. [Blocker] ISSUE-F13 objective shaping does not produce hard wins

- Decision: drop
- Score: 85 -> 15
- Issue: https://github.com/w2030298-art/HybridArena/issues/4
- Reason: no clear open paid bounty signal >= $10 found

## 13. adversarial-review: add scope discipline to prevent finding-count inflation

- Decision: drop
- Score: 85 -> 15
- Issue: https://github.com/oalders/kitchen-sink/issues/11
- Reason: no clear open paid bounty signal >= $10 found

## 14. gemma4 grpo异常loss spike

- Decision: drop
- Score: 85 -> 15
- Issue: https://github.com/modelscope/ms-swift/issues/9400
- Reason: no clear open paid bounty signal >= $10 found

## 15. launch-selected-element: include the page URL (and ideally route + query) for context

- Decision: drop
- Score: 85 -> 15
- Issue: https://github.com/anthropics/claude-code/issues/61161
- Reason: no clear open paid bounty signal >= $10 found

## 16. [ FastAPI ] Add request ID middleware for log correlation

- Decision: drop
- Score: 81 -> -54
- Issue: https://github.com/UnsafeLabs/Bounty-Hunters/issues/797
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty
- Reason: competition already visible in comments; still allowed in aggressive mode

## 17. [ FastAPI ] Fix jsonable_encoder TypeError on bytes and memoryview objects

- Decision: drop
- Score: 81 -> -54
- Issue: https://github.com/UnsafeLabs/Bounty-Hunters/issues/759
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty
- Reason: competition already visible in comments; still allowed in aggressive mode

## 18. [ Laravel ] Add rate limiting middleware to web routes and fix session driver fallback

- Decision: keep
- Score: 81 -> 46
- Issue: https://github.com/UnsafeLabs/Bounty-Hunters/issues/749
- Reason: competition already visible in comments; still allowed in aggressive mode

## 19. [ Laravel ] Fix logging config to separate error logs and add JSON structured logging

- Decision: drop
- Score: 81 -> -54
- Issue: https://github.com/UnsafeLabs/Bounty-Hunters/issues/787
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty
- Reason: competition already visible in comments; still allowed in aggressive mode

## 20. [ CONTEXT RIFT ] Fix typos in knowledge-base/context.json

- Decision: drop
- Score: 81 -> -54
- Issue: https://github.com/UnsafeLabs/Bounty-Hunters/issues/611
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty
- Reason: competition already visible in comments; still allowed in aggressive mode

## 21. [ T3 Code ] Add round-trip schema validation tests for all contract types

- Decision: keep
- Score: 81 -> 46
- Issue: https://github.com/UnsafeLabs/Bounty-Hunters/issues/827
- Reason: competition already visible in comments; still allowed in aggressive mode

## 22. [ T3 Code ] Fix turbo.json missing dependency graph for incremental builds

- Decision: keep
- Score: 81 -> 46
- Issue: https://github.com/UnsafeLabs/Bounty-Hunters/issues/828
- Reason: competition already visible in comments; still allowed in aggressive mode

## 23. [ T3 Code ] Fix ProviderModelPicker not persisting selection across reloads

- Decision: keep
- Score: 81 -> 46
- Issue: https://github.com/UnsafeLabs/Bounty-Hunters/issues/834
- Reason: competition already visible in comments; still allowed in aggressive mode

## 24. [ T3 Code ] Add Tailscale peer diagnostics with latency graph

- Decision: keep
- Score: 81 -> 46
- Issue: https://github.com/UnsafeLabs/Bounty-Hunters/issues/844
- Reason: competition already visible in comments; still allowed in aggressive mode

## 25. [ FastAPI ] Fix OpenAPI schema missing server, contact, and license information

- Decision: keep
- Score: 81 -> 46
- Issue: https://github.com/UnsafeLabs/Bounty-Hunters/issues/801
- Reason: competition already visible in comments; still allowed in aggressive mode

## 26. [ Laravel ] Fix phpunit.xml coverage config and add route and model test suites

- Decision: keep
- Score: 81 -> 46
- Issue: https://github.com/UnsafeLabs/Bounty-Hunters/issues/794
- Reason: competition already visible in comments; still allowed in aggressive mode

## 27. [ FastAPI ] Fix generate_unique_id producing duplicate operation IDs across routers

- Decision: keep
- Score: 81 -> 46
- Issue: https://github.com/UnsafeLabs/Bounty-Hunters/issues/764
- Reason: competition already visible in comments; still allowed in aggressive mode

## 28. [ FastAPI ] Fix hardcoded CDN URLs in Swagger UI and ReDoc HTML generation

- Decision: keep
- Score: 81 -> 46
- Issue: https://github.com/UnsafeLabs/Bounty-Hunters/issues/762
- Reason: competition already visible in comments; still allowed in aggressive mode

## 29. P1: Restore true policy-gradient update step after fixed-vector recurrence

- Decision: drop
- Score: 79 -> 9
- Issue: https://github.com/lanyusea/screeps/issues/1299
- Reason: no clear open paid bounty signal >= $10 found

## 30. [ T3 Code ] Add Prometheus metrics endpoint with Effect.Metric integration

- Decision: keep
- Score: 71 -> 36
- Issue: https://github.com/UnsafeLabs/Bounty-Hunters/issues/833
- Reason: competition already visible in comments; still allowed in aggressive mode

## 31. [ Javascript ] Missing supported_versions Extension in ClientHello

- Decision: drop
- Score: 71 -> -34
- Issue: https://github.com/UnsafeLabs/Bounty-Hunters/issues/389
- Reason: no clear open paid bounty signal >= $10 found
- Reason: competition already visible in comments; still allowed in aggressive mode

## 32. Example task for Base market-data agents: Bazaar Signal Agent

- Decision: keep
- Score: 71 -> 36
- Issue: https://github.com/coinbase/agentic-wallet-skills/issues/37
- Reason: competition already visible in comments; still allowed in aggressive mode

## 33. [Tutorial] Testing Compact Contracts: Unit Tests, Assertions, and Local Simulation

- Decision: drop
- Score: 71 -> -64
- Issue: https://github.com/midnightntwrk/contributor-hub/issues/312
- Reason: content bounty has AI-content disqualification risk for autonomous work
- Reason: competition already visible in comments; still allowed in aggressive mode

## 34. [ FastAPI ] Add concurrent task runner with semaphore limiting and timeout

- Decision: keep
- Score: 71 -> 36
- Issue: https://github.com/UnsafeLabs/Bounty-Hunters/issues/803
- Reason: competition already visible in comments; still allowed in aggressive mode

## 35. [Bug - Gameplay/Logic]: Winning the curtain game causes stray sprites to appear

- Decision: drop
- Score: 64 -> -6
- Issue: https://github.com/pidgezero-one/smrpg_web_randomizer/issues/108
- Reason: no clear open paid bounty signal >= $10 found

## 36. Fix the schematic view by also optionally accepting kicad_sym and converting into a schPortArrangement and pinLabels

- Decision: keep
- Score: 63 -> 28
- Issue: https://github.com/tscircuit/kicad-component-converter/issues/114
- Reason: competition already visible in comments; still allowed in aggressive mode

## 37. [ English ] Complete missing lines in limericks.md — finish three limericks

- Decision: drop
- Score: 61 -> -74
- Issue: https://github.com/UnsafeLabs/Bounty-Hunters/issues/577
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty
- Reason: competition already visible in comments; still allowed in aggressive mode

## 38. [ English ] Complete Sonnet I — The Weight of Stars in sonnets.md

- Decision: drop
- Score: 61 -> -44
- Issue: https://github.com/UnsafeLabs/Bounty-Hunters/issues/579
- Reason: no clear open paid bounty signal >= $10 found
- Reason: competition already visible in comments; still allowed in aggressive mode

## 39. [ English ] Complete missing closing lines in haikus.md

- Decision: drop
- Score: 61 -> -74
- Issue: https://github.com/UnsafeLabs/Bounty-Hunters/issues/576
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty
- Reason: competition already visible in comments; still allowed in aggressive mode

## 40. [ English ] Complete missing lines in acrostics.md — finish UNSAFE acrostic and write BOUNTY acrostic

- Decision: drop
- Score: 61 -> -44
- Issue: https://github.com/UnsafeLabs/Bounty-Hunters/issues/575
- Reason: no clear open paid bounty signal >= $10 found
- Reason: competition already visible in comments; still allowed in aggressive mode

## 41. [AUTORESEARCH][ONLINE] RAxer bug fix sweep — 40+ fixes need aggregate offline evaluation before merge

- Decision: drop
- Score: 56 -> -14
- Issue: https://github.com/SolbiatiAlessandro/cogames/issues/77
- Reason: no clear open paid bounty signal >= $10 found

## 42. Random TODOs

- Decision: drop
- Score: 54 -> -16
- Issue: https://github.com/yihui/yihui.org/issues/20
- Reason: no clear open paid bounty signal >= $10 found

## 43. [Bug - cosmetic]: Various player character sprite issues (Bowser and others) [v9]

- Decision: drop
- Score: 54 -> -16
- Issue: https://github.com/pidgezero-one/smrpg_web_randomizer/issues/99
- Reason: no clear open paid bounty signal >= $10 found

## 44. [Bug]: Various issues with Belome Temple fortunes

- Decision: drop
- Score: 54 -> -16
- Issue: https://github.com/pidgezero-one/smrpg_web_randomizer/issues/96
- Reason: no clear open paid bounty signal >= $10 found

## 45. [Bug]: Prizes can be assigned to the wrong locations, and will infinitely replenish [v9]

- Decision: drop
- Score: 54 -> -16
- Issue: https://github.com/pidgezero-one/smrpg_web_randomizer/issues/102
- Reason: no clear open paid bounty signal >= $10 found

## 46. research: run issue-749 BC warm-start PPO experiment

- Decision: drop
- Score: 46 -> -59
- Issue: https://github.com/ll7/robot_sf_ll7/issues/1108
- Reason: no clear open paid bounty signal >= $10 found
- Reason: competition already visible in comments; still allowed in aggressive mode

## 47. Sketcher Workbench: Adding Missing Information

- Decision: drop
- Score: 46 -> -59
- Issue: https://github.com/Reqrefusion/FreeCAD-Documentation-Project/issues/94
- Reason: no clear open paid bounty signal >= $10 found
- Reason: competition already visible in comments; still allowed in aggressive mode

## 48. Wayland version does not support external keyboard/mouse

- Decision: drop
- Score: 46 -> -59
- Issue: https://github.com/autokey/autokey/issues/1003
- Reason: no clear open paid bounty signal >= $10 found
- Reason: competition already visible in comments; still allowed in aggressive mode

## 49. [FEATURE] Add Empty States and Skeleton Loaders for Better UX

- Decision: drop
- Score: 43 -> -57
- Issue: https://github.com/RatLoopz/sahidawa-india/issues/381
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty

## 50. 'get' command returns the same wallpaper for different screens with different wallpapers.

- Decision: drop
- Score: 41 -> -29
- Issue: https://github.com/sindresorhus/macos-wallpaper/issues/25
- Reason: no clear open paid bounty signal >= $10 found

## 51. Add FAQ page and link it in footer

- Decision: drop
- Score: 39 -> -111
- Issue: https://github.com/RatLoopz/sahidawa-india/issues/408
- Reason: no clear open paid bounty signal >= $10 found
- Reason: already assigned to ANISHA-RAWAT

## 52. Add About Us page and link it in footer

- Decision: drop
- Score: 39 -> -111
- Issue: https://github.com/RatLoopz/sahidawa-india/issues/407
- Reason: no clear open paid bounty signal >= $10 found
- Reason: already assigned to ANISHA-RAWAT

## 53. Footer missing on inner/subpages

- Decision: drop
- Score: 39 -> -111
- Issue: https://github.com/RatLoopz/sahidawa-india/issues/406
- Reason: no clear open paid bounty signal >= $10 found
- Reason: already assigned to ANISHA-RAWAT

## 54. Sats to Local Currency | Mexico

- Decision: drop
- Score: 39 -> -66
- Issue: https://github.com/sutt/docs/issues/5
- Reason: no clear open paid bounty signal >= $10 found
- Reason: competition already visible in comments; still allowed in aggressive mode

## 55. Developer feedback: three friction points when integrating v4 for the first time

- Decision: drop
- Score: 39 -> -31
- Issue: https://github.com/hashgraph/hedera-agent-kit-js/issues/836
- Reason: no clear open paid bounty signal >= $10 found

## 56. feat: handle offline validators on the consumer chain side and punish them on provider

- Decision: drop
- Score: 36 -> -34
- Issue: https://github.com/allinbits/vaas/issues/38
- Reason: no clear open paid bounty signal >= $10 found

## 57. [BOUNTY] Write a Blog Post About Proof-of-Antiquity — 15 RTC

- Decision: drop
- Score: 36 -> -34
- Issue: https://github.com/Scottcjn/rustchain-bounties/issues/282
- Reason: no clear open paid bounty signal >= $10 found

## 58. [Minter] Add solo staking

- Decision: drop
- Score: 36 -> -114
- Issue: https://github.com/SharedStake/Contracts/issues/12
- Reason: no clear open paid bounty signal >= $10 found
- Reason: light competition allowed: 3 open competing PR(s)
- Reason: competition already visible in comments; still allowed in aggressive mode
- Competing PR: https://github.com/SharedStake/Contracts/pull/31
- Competing PR: https://github.com/SharedStake/Contracts/pull/26
- Competing PR: https://github.com/SharedStake/Contracts/pull/16
