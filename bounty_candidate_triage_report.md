# GitHub Bounty Candidate Triage

Last run: 2026-05-24 17:41 UTC

Kept candidates: 3

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

## 7. Paid Max plan usage limits interrupt real work mid-task; need predictable quota or graceful continuation

- Decision: drop
- Score: 90 -> -45
- Issue: https://github.com/anthropics/claude-code/issues/61906
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty
- Reason: competition already visible in comments; still allowed in aggressive mode

## 8. [Bug] release workflow — dev/main squash divergence compounds; needs main→dev sync after each release

- Decision: drop
- Score: 85 -> 15
- Issue: https://github.com/me2resh/apexyard/issues/403
- Reason: no clear open paid bounty signal >= $10 found

## 9. Critical: audit all tx.execute(SELECT *) callsites in commandBus.ts — snake_case reads silently return undefined

- Decision: drop
- Score: 85 -> 15
- Issue: https://github.com/EvanTenenbaum/terp-operator/issues/267
- Reason: no clear open paid bounty signal >= $10 found

## 10. Mapper sub-agent runs out of turns when the verifier rejects the first attempt (maxTurns: 4 too tight)

- Decision: drop
- Score: 85 -> 15
- Issue: https://github.com/Pleusch/SharpMind/issues/205
- Reason: no clear open paid bounty signal >= $10 found

## 11. 改进 X/Twitter 适配器：去噪、Thread 过滤、文件名优化

- Decision: drop
- Score: 85 -> 15
- Issue: https://github.com/yuevthins/markdownload-zh/issues/22
- Reason: no clear open paid bounty signal >= $10 found

## 12. Known issue: processor fee tracking is a complete stub — no processor_fees rows are ever created

- Decision: drop
- Score: 85 -> -15
- Issue: https://github.com/EvanTenenbaum/terp-operator/issues/261
- Reason: issue explicitly indicates no paid bounty or free-only payment status

## 13. Known issue: postSalesOrder reversal has 3 silent data gaps — consignment bills, line status, reservedQty

- Decision: drop
- Score: 85 -> 15
- Issue: https://github.com/EvanTenenbaum/terp-operator/issues/257
- Reason: no clear open paid bounty signal >= $10 found

## 14. Stale comments in DefaultConfig claim a finite retry default, contradicting the actual unbounded behavior

- Decision: drop
- Score: 85 -> 15
- Issue: https://github.com/xrf9268-hue/aiops-platform/issues/367
- Reason: no clear open paid bounty signal >= $10 found

## 15. Medium: Backfill test coverage for new Stripe and Xero code paths

- Decision: drop
- Score: 85 -> 15
- Issue: https://github.com/thatskiff33/AlpineClubBookingsNZ/issues/503
- Reason: no clear open paid bounty signal >= $10 found

## 16. chore(catalogue): round 4 — weird worlds (low priority, ideas bucket)

- Decision: drop
- Score: 85 -> 15
- Issue: https://github.com/teseor/teseor/issues/722
- Reason: no clear open paid bounty signal >= $10 found

## 17. [ Bounty $3k ] [ Research ] Collect and compare AI-generated AGI architecture proposals

- Decision: keep
- Score: 81 -> 46
- Issue: https://github.com/aLexzzz430/Cognitive-OS/issues/5
- Reason: competition already visible in comments; still allowed in aggressive mode

## 18. Misleading "Usage limit reached" error when selecting Sonnet — actually a 1M context tier gate

- Decision: drop
- Score: 79 -> 9
- Issue: https://github.com/anthropics/claude-code/issues/62052
- Reason: no clear open paid bounty signal >= $10 found

## 19. Consistently getting errors with using ollama cloud w/o agent

- Decision: drop
- Score: 79 -> 9
- Issue: https://github.com/dyad-sh/dyad/issues/3498
- Reason: no clear open paid bounty signal >= $10 found

## 20. Bounties dashboard shows closed $5 issues as open

- Decision: drop
- Score: 79 -> 9
- Issue: https://github.com/OWASP-BLT/BLT/issues/6437
- Reason: no clear open paid bounty signal >= $10 found

## 21. External uptime monitor + status.ligate.io migration

- Decision: drop
- Score: 79 -> -56
- Issue: https://github.com/ligate-io/ligate-chain/issues/319
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty
- Reason: competition already visible in comments; still allowed in aggressive mode

## 22. Explorer page: Miner data stuck at 'Loading miners...' indefinitely (frontend rendering bug)

- Decision: drop
- Score: 79 -> 9
- Issue: https://github.com/Scottcjn/Rustchain/issues/6211
- Reason: no clear open paid bounty signal >= $10 found

## 23. claude issue

- Decision: drop
- Score: 79 -> 9
- Issue: https://github.com/kirodotdev/Kiro/issues/8836
- Reason: no clear open paid bounty signal >= $10 found

## 24. [WIKI-DOCS] SPLITROOT hero plan — Briar Saint + Master Artificer (the two starting heroes; horizontal-only paid discipline locked)

- Decision: drop
- Score: 79 -> -56
- Issue: https://github.com/Jonnyton/Workflow/issues/1054
- Reason: issue explicitly indicates no paid bounty or free-only payment status
- Reason: competition already visible in comments; still allowed in aggressive mode

## 25. AU Rubber: productise into tiered ZAR SaaS — pricing, packaging & feature-gated RBAC licensing

- Decision: drop
- Score: 79 -> -21
- Issue: https://github.com/AnnixInvestments/annix/issues/306
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty

## 26. research: TanStack ecosystem — patterns to steal + adapter strategy

- Decision: drop
- Score: 79 -> -21
- Issue: https://github.com/teseor/teseor/issues/725
- Reason: issue explicitly indicates no paid bounty or free-only payment status

## 27. Roadmap: polished VB-Audio MCP for Matrix, workflows, and future Voicemeeter support

- Decision: drop
- Score: 79 -> 9
- Issue: https://github.com/BASIC-BIT/vbmatrix-mcp/issues/2
- Reason: no clear open paid bounty signal >= $10 found

## 28. chore(atdd): Surface Smoke Acceptance Rule In Planner Flow

- Decision: drop
- Score: 79 -> 9
- Issue: https://github.com/afokapu/atdd/issues/849
- Reason: no clear open paid bounty signal >= $10 found

## 29. F3. Migrasi ke Integer-Cents untuk Monetary Values

- Decision: drop
- Score: 75 -> 5
- Issue: https://github.com/Robbybaehaqi1122/MondokQu/issues/34
- Reason: no clear open paid bounty signal >= $10 found

## 30. Desktop app (Code): ~30s delay before any response on every prompt — including first message of a fresh chat. CLI on same machine is ~5s.

- Decision: drop
- Score: 73 -> 3
- Issue: https://github.com/anthropics/claude-code/issues/61898
- Reason: no clear open paid bounty signal >= $10 found

## 31. [BUG] Sonnet 4.6 blocked by forced 1M context mode requiring additional credits on Pro plan

- Decision: drop
- Score: 73 -> 3
- Issue: https://github.com/anthropics/claude-code/issues/61921
- Reason: no clear open paid bounty signal >= $10 found

## 32. MRWK bounty: live public smoke checks and useful reports, round 2

- Decision: drop
- Score: 71 -> 1
- Issue: https://github.com/ramimbo/mergework/issues/109
- Reason: no clear open paid bounty signal >= $10 found

## 33. Roadmap: public launch distribution checklist

- Decision: drop
- Score: 69 -> -31
- Issue: https://github.com/zr9959/ai-saas-guard/issues/55
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty

## 34. Feature candidate_H: directory-only manifest signal for D.4-shape multi-route services — 1 voice

- Decision: drop
- Score: 64 -> -6
- Issue: https://github.com/fardinvahdat/x402trace/issues/85
- Reason: no clear open paid bounty signal >= $10 found

## 35. [MMIR-D126][P0][agent-ready] Publish ChatGPT/Open WebUI parity matrix for product gaps

- Decision: drop
- Score: 64 -> -6
- Issue: https://github.com/inkognitroz/inkognitroz.github.io/issues/108
- Reason: no clear open paid bounty signal >= $10 found

## 36. [Bug]: ollama-cloud provider does not inject SOUL.md into outgoing request (loader fires correctly; content drops downstream)

- Decision: drop
- Score: 64 -> -6
- Issue: https://github.com/NousResearch/hermes-agent/issues/29871
- Reason: no clear open paid bounty signal >= $10 found

## 37. Generate public MCP capability documentation from the tool catalog

- Decision: drop
- Score: 64 -> -6
- Issue: https://github.com/alexhowgego/glovelly/issues/147
- Reason: no clear open paid bounty signal >= $10 found

## 38. [DATA] Open-source intraday acquisition path for replay/training coverage

- Decision: drop
- Score: 60 -> -40
- Issue: https://github.com/seanyofthedead/Ross-trading/issues/78
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty

## 39. Bug: Async workflow time-slice scheduler for sandbox tier is incomplete (risk of stuck RUNNING state)

- Decision: drop
- Score: 54 -> -16
- Issue: https://github.com/langgenius/dify/issues/35499
- Reason: no clear open paid bounty signal >= $10 found

## 40. P1: Restore local RL experiment-card fallback after NO_EXPERIMENT_CARD recurrence

- Decision: drop
- Score: 50 -> -55
- Issue: https://github.com/lanyusea/screeps/issues/1291
- Reason: no clear open paid bounty signal >= $10 found
- Reason: competition already visible in comments; still allowed in aggressive mode

## 41. [Bug] Badge create returns 200 when username is missing

- Decision: drop
- Score: 49 -> -21
- Issue: https://github.com/Scottcjn/Rustchain/issues/6198
- Reason: no clear open paid bounty signal >= $10 found

## 42. Pressure setting dissapered

- Decision: drop
- Score: 49 -> -21
- Issue: https://github.com/ankohanse/hass-dab-pumps/issues/99
- Reason: no clear open paid bounty signal >= $10 found

## 43. ROADMAP: doc PR cascade pattern — CLAUDE.md cross-ref line invalidates parallel doc PRs

- Decision: drop
- Score: 48 -> -57
- Issue: https://github.com/EffortlessMetrics/perl-lsp/issues/7126
- Reason: no clear open paid bounty signal >= $10 found
- Reason: competition already visible in comments; still allowed in aggressive mode

## 44. Validate and structure SRD spells for combat automation

- Decision: drop
- Score: 48 -> -52
- Issue: https://github.com/BlueLinks/bluDM/issues/43
- Reason: issue explicitly indicates no paid bounty or free-only payment status

## 45. MCP tool schema with $defs/$ref is exposed incorrectly to the model

- Decision: drop
- Score: 46 -> -24
- Issue: https://github.com/openai/codex/issues/13746
- Reason: no clear open paid bounty signal >= $10 found

## 46. PEP 541 Request: Lost Access to PyPi Account hosting my project

- Decision: drop
- Score: 43 -> -27
- Issue: https://github.com/pypi/support/issues/10757
- Reason: no clear open paid bounty signal >= $10 found

## 47. File Limit Request: LiteLLM - 25,000 MB

- Decision: drop
- Score: 43 -> -27
- Issue: https://github.com/pypi/support/issues/10756
- Reason: no clear open paid bounty signal >= $10 found

## 48. CLAUDE AI subscription not recognized

- Decision: drop
- Score: 43 -> -27
- Issue: https://github.com/anthropics/claude-code/issues/61920
- Reason: no clear open paid bounty signal >= $10 found

## 49. P0: Run validation-scale policy-gradient samples for trusted updates

- Decision: drop
- Score: 40 -> -30
- Issue: https://github.com/lanyusea/screeps/issues/1337
- Reason: no clear open paid bounty signal >= $10 found

## 50. PEP 541 Request: sisou2

- Decision: drop
- Score: 39 -> -31
- Issue: https://github.com/pypi/support/issues/10761
- Reason: no clear open paid bounty signal >= $10 found

## 51. [Bug]: xAI OAuth (xai-oauth) returns HTTP 403 for standard SuperGrok subscribers — backend enforcing Heavy-only despite docs claiming all tiers

- Decision: drop
- Score: 36 -> -99
- Issue: https://github.com/NousResearch/hermes-agent/issues/26847
- Reason: false positive claim/cost/market/manual-access issue, not an open coding bounty
- Reason: competition already visible in comments; still allowed in aggressive mode

## 52. Opire

- Decision: keep
- Score: 36 -> 1
- Issue: https://github.com/ubiquity/business-development/issues/89
- Reason: competition already visible in comments; still allowed in aggressive mode

## 53. Account recovery request

- Decision: drop
- Score: 33 -> -37
- Issue: https://github.com/pypi/support/issues/10760
- Reason: no clear open paid bounty signal >= $10 found

## 54. File Limit Request: pykep - 250 MiB

- Decision: drop
- Score: 33 -> -37
- Issue: https://github.com/pypi/support/issues/10759
- Reason: no clear open paid bounty signal >= $10 found

## 55. Corrupted PDF

- Decision: drop
- Score: 30 -> -40
- Issue: https://github.com/Hopding/pdf-lib/issues/951
- Reason: no clear open paid bounty signal >= $10 found

## 56. OpenClaw/Hermes Agent Integration & Configuration

- Decision: drop
- Score: 28 -> -42
- Issue: https://github.com/AKALANI-AI/akalani-paa/issues/40
- Reason: no clear open paid bounty signal >= $10 found
