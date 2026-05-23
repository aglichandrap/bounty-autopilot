# Bounty Repository Filter

Last run: 2026-05-23 05:30 UTC

Input candidates: 60
Kept candidates: 18
Dropped candidates: 42

This filter removes known false-positive, unsafe, self-tracking, stale, or overcrowded bounty sources before expensive triage/solver work runs.

## Dropped

### 1. [CAL-3105] BigBlueButton Integration

- Repository: calcom/cal.com
- Issue: https://github.com/calcom/cal.com/issues/1985
- Reason: known stale/crowded bounty issue

### 2. [ Bounty $5k ] [ Data ] Apply retention policy to failed validation payloads — quarantine store

- Repository: orchestration-agent/AgentOrchestration
- Issue: https://github.com/orchestration-agent/AgentOrchestration/issues/2828
- Reason: known false-positive or unsafe bounty source

### 3. [ Bounty $7k ] [ Deploy ] Run migrations before application rollout — database release order

- Repository: orchestration-agent/AgentOrchestration
- Issue: https://github.com/orchestration-agent/AgentOrchestration/issues/2823
- Reason: known false-positive or unsafe bounty source

### 4. [ Bounty $3k ] [ Registry ] Prevent handler name path traversal — local plugin metadata

- Repository: orchestration-agent/AgentOrchestration
- Issue: https://github.com/orchestration-agent/AgentOrchestration/issues/2810
- Reason: known false-positive or unsafe bounty source

### 5. [ Bounty $10k ] [ Webhook ] Handle 410 Gone by disabling endpoint safely — webhook delivery

- Repository: orchestration-agent/AgentOrchestration
- Issue: https://github.com/orchestration-agent/AgentOrchestration/issues/2832
- Reason: known false-positive or unsafe bounty source

### 6. [ Bounty $4k ] [ Metrics ] Reject negative counter increments — counter integrity

- Repository: orchestration-agent/AgentOrchestration
- Issue: https://github.com/orchestration-agent/AgentOrchestration/issues/2417
- Reason: known false-positive or unsafe bounty source

### 7. [ Bounty $6k ] [ Webhook ] Avoid leaking internal run metadata in public events — payload shaping

- Repository: orchestration-agent/AgentOrchestration
- Issue: https://github.com/orchestration-agent/AgentOrchestration/issues/2821
- Reason: known false-positive or unsafe bounty source

### 8. [ Bounty $5k ] [ Sandbox ] Enforce disk_mb or remove the option — resource limits

- Repository: orchestration-agent/AgentOrchestration
- Issue: https://github.com/orchestration-agent/AgentOrchestration/issues/2799
- Reason: known false-positive or unsafe bounty source

### 9. [ Bounty $2k ] [ Data ] Document data lineage for transformed task records — analytics pipeline

- Repository: orchestration-agent/AgentOrchestration
- Issue: https://github.com/orchestration-agent/AgentOrchestration/issues/2815
- Reason: known false-positive or unsafe bounty source

### 10. [ Bounty $4k ] [ Storage ] Use atomic writes for JSONL event logs — concurrent appenders

- Repository: orchestration-agent/AgentOrchestration
- Issue: https://github.com/orchestration-agent/AgentOrchestration/issues/2801
- Reason: known false-positive or unsafe bounty source

### 11. [ Bounty $4k ] [ Scheduler ] Deduplicate cron ticks across replicas — leader election changes

- Repository: orchestration-agent/AgentOrchestration
- Issue: https://github.com/orchestration-agent/AgentOrchestration/issues/2664
- Reason: known false-positive or unsafe bounty source

### 12. [ Bounty $5k ] [ Sandbox ] Verify tracked paths before get_path returns — workspace access

- Repository: orchestration-agent/AgentOrchestration
- Issue: https://github.com/orchestration-agent/AgentOrchestration/issues/2685
- Reason: known false-positive or unsafe bounty source

### 13. [ Bounty $2k ] [ Webhook ] Validate subscription filters against allowed fields — filter API

- Repository: orchestration-agent/AgentOrchestration
- Issue: https://github.com/orchestration-agent/AgentOrchestration/issues/2676
- Reason: known false-positive or unsafe bounty source

### 14. [ Bounty $4k ] [ Runtime ] Handle timezone-aware schedules consistently — cron runtime

- Repository: orchestration-agent/AgentOrchestration
- Issue: https://github.com/orchestration-agent/AgentOrchestration/issues/2701
- Reason: known false-positive or unsafe bounty source

### 15. [ Bounty $3k ] [ Metrics ] Shorten snapshot lock hold time — threaded exporters

- Repository: orchestration-agent/AgentOrchestration
- Issue: https://github.com/orchestration-agent/AgentOrchestration/issues/2694
- Reason: known false-positive or unsafe bounty source

### 16. [ Bounty $5k ] [ Deploy ] De-duplicate scheduled jobs during rollout — cron workers

- Repository: orchestration-agent/AgentOrchestration
- Issue: https://github.com/orchestration-agent/AgentOrchestration/issues/2722
- Reason: known false-positive or unsafe bounty source

### 17. [ Bounty $5k ] [ Scheduler ] Avoid backlog burst after resume — paused tenant resumes

- Repository: orchestration-agent/AgentOrchestration
- Issue: https://github.com/orchestration-agent/AgentOrchestration/issues/2736
- Reason: known false-positive or unsafe bounty source

### 18. [ Bounty $5k ] [ Middleware ] Propagate cancellation to downstream agent calls — async middleware

- Repository: orchestration-agent/AgentOrchestration
- Issue: https://github.com/orchestration-agent/AgentOrchestration/issues/2714
- Reason: known false-positive or unsafe bounty source

### 19. [ Bounty $3k ] [ Runtime ] Prevent worker heartbeat from reviving completed runs — heartbeat monitor

- Repository: orchestration-agent/AgentOrchestration
- Issue: https://github.com/orchestration-agent/AgentOrchestration/issues/2748
- Reason: known false-positive or unsafe bounty source

### 20. [ Bounty $4k ] [ Metrics ] Handle exporter counter range limits — large counters

- Repository: orchestration-agent/AgentOrchestration
- Issue: https://github.com/orchestration-agent/AgentOrchestration/issues/2771
- Reason: known false-positive or unsafe bounty source

### 21. [ Bounty $3k ] [ Storage ] Add checksum validation to download cache — artifact consumers

- Repository: orchestration-agent/AgentOrchestration
- Issue: https://github.com/orchestration-agent/AgentOrchestration/issues/2791
- Reason: known false-positive or unsafe bounty source

### 22. [ Bounty $4k ] [ API ] Prevent partial batch update success masking failures — agent config API

- Repository: orchestration-agent/AgentOrchestration
- Issue: https://github.com/orchestration-agent/AgentOrchestration/issues/2807
- Reason: known false-positive or unsafe bounty source

### 23. [ Bounty $5k ] [ CLI ] Expand user paths for --config — config loading

- Repository: orchestration-agent/AgentOrchestration
- Issue: https://github.com/orchestration-agent/AgentOrchestration/issues/2750
- Reason: known false-positive or unsafe bounty source

### 24. [ Bounty $6k ] [ SDK ] Validate task decorator timeout values — decorator guardrails

- Repository: orchestration-agent/AgentOrchestration
- Issue: https://github.com/orchestration-agent/AgentOrchestration/issues/2623
- Reason: known false-positive or unsafe bounty source

### 25. [ Bounty $2k ] [ Queue ] Handle malformed job payloads safely — legacy queue records

- Repository: orchestration-agent/AgentOrchestration
- Issue: https://github.com/orchestration-agent/AgentOrchestration/issues/2594
- Reason: known false-positive or unsafe bounty source

### 26. [ Bounty $3k ] [ SDK ] Reject blank agent names before POST — registration validation

- Repository: orchestration-agent/AgentOrchestration
- Issue: https://github.com/orchestration-agent/AgentOrchestration/issues/2618
- Reason: known false-positive or unsafe bounty source

### 27. [ Bounty $5k ] [ CLI ] Validate logs tail is non-negative — logs arguments

- Repository: orchestration-agent/AgentOrchestration
- Issue: https://github.com/orchestration-agent/AgentOrchestration/issues/2580
- Reason: known false-positive or unsafe bounty source

### 28. [ Bounty $7k ] [ Webhook ] Handle DNS resolution failures without blocking workers — delivery runtime

- Repository: orchestration-agent/AgentOrchestration
- Issue: https://github.com/orchestration-agent/AgentOrchestration/issues/2645
- Reason: known false-positive or unsafe bounty source

### 29. [ Bounty $6k ] [ CLI ] Inject SDK clients into CLI handlers — test isolation

- Repository: orchestration-agent/AgentOrchestration
- Issue: https://github.com/orchestration-agent/AgentOrchestration/issues/2554
- Reason: known false-positive or unsafe bounty source

### 30. [ Bounty $5k ] [ Config ] Support literal underscores in override keys — env key mapping

- Repository: orchestration-agent/AgentOrchestration
- Issue: https://github.com/orchestration-agent/AgentOrchestration/issues/2588
- Reason: known false-positive or unsafe bounty source

### 31. [ Bounty $4k ] [ Metrics ] Include min and max in histograms — observability fidelity

- Repository: orchestration-agent/AgentOrchestration
- Issue: https://github.com/orchestration-agent/AgentOrchestration/issues/2559
- Reason: known false-positive or unsafe bounty source

### 32. [ Bounty $3k ] [ Metrics ] Reject non-numeric histogram observations — histogram integrity

- Repository: orchestration-agent/AgentOrchestration
- Issue: https://github.com/orchestration-agent/AgentOrchestration/issues/2564
- Reason: known false-positive or unsafe bounty source

### 33. [ Bounty $3k ] [ Queue ] Keep delayed jobs out of ready scans — priority queue polling

- Repository: orchestration-agent/AgentOrchestration
- Issue: https://github.com/orchestration-agent/AgentOrchestration/issues/2583
- Reason: known false-positive or unsafe bounty source

### 34. [ Bounty $4k ] [ Config ] Report JSON parse failures with path context — file loading

- Repository: orchestration-agent/AgentOrchestration
- Issue: https://github.com/orchestration-agent/AgentOrchestration/issues/2600
- Reason: known false-positive or unsafe bounty source

### 35. TaskBounty worker status

- Repository: asaadnashed/bounty-autopilot
- Issue: https://github.com/asaadnashed/bounty-autopilot/issues/5
- Reason: known false-positive or unsafe bounty source

### 36. TaskBounty candidates

- Repository: asaadnashed/bounty-autopilot
- Issue: https://github.com/asaadnashed/bounty-autopilot/issues/2
- Reason: known false-positive or unsafe bounty source

### 37. Bounty scout candidates

- Repository: asaadnashed/bounty-autopilot
- Issue: https://github.com/asaadnashed/bounty-autopilot/issues/1
- Reason: known false-positive or unsafe bounty source

### 38. [ FastAPI ] Fix OpenAPI schema missing server, contact, and license information

- Repository: UnsafeLabs/Bounty-Hunters
- Issue: https://github.com/UnsafeLabs/Bounty-Hunters/issues/801
- Reason: known false-positive or unsafe bounty source

### 39. [ FastAPI ] Add request ID middleware for log correlation

- Repository: UnsafeLabs/Bounty-Hunters
- Issue: https://github.com/UnsafeLabs/Bounty-Hunters/issues/797
- Reason: known false-positive or unsafe bounty source

### 40. [ Laravel ] Fix console.php missing scheduled task registration and add log cleanup command

- Repository: UnsafeLabs/Bounty-Hunters
- Issue: https://github.com/UnsafeLabs/Bounty-Hunters/issues/753
- Reason: known false-positive or unsafe bounty source

### 41. GitHub bounty claim status

- Repository: asaadnashed/bounty-autopilot
- Issue: https://github.com/asaadnashed/bounty-autopilot/issues/8
- Reason: known false-positive or unsafe bounty source

### 42. Implement Differential Reward Distribution for Reopened Issues

- Repository: devpool-directory/devpool-directory
- Issue: https://github.com/devpool-directory/devpool-directory/issues/5012
- Reason: known stale/crowded bounty issue
