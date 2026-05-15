# Bounty Scout Candidates

Last manual scan: 2026-05-16 Asia/Dubai

Status: online automation is not deployed yet. This is a manual scan from Codex.

## 1. Opire featured bounties

- Source: https://opire.dev/
- Amounts visible on public page:
  - $390 - Add Wayland support - Python
  - $120 - Migration generation drops and creates columns instead of altering, resulting in data loss - TypeScript
  - $110 - Storybook controls type select problem - TypeScript
  - $70 - View test coverage in editor - Rust
  - $30 - QueryEngine deleteMany nested entity bug - TypeScript
- Status: promising, but needs Opire account/login to open details and claim rules.
- Next action: after Opire account setup, inspect the $120 TypeScript issue first because it is specific and bug-like.

## 2. AsyncAPI Microgrant 2026-05

- Source issue: https://github.com/asyncapi/cli/issues/2125
- Candidate linked issue: https://github.com/asyncapi/cli/issues/1987
- Summary: request body validation skipped for some paths or HTTP methods.
- Status: promising, but must confirm microgrant claim process and whether the issue is unclaimed.
- Next action: inspect AsyncAPI contribution and microgrant rules, then reproduce bug locally.

## 3. AsyncAPI website workflow issue

- Candidate: https://github.com/asyncapi/website/issues/5333
- Summary: dashboard update workflow not updating dashboard data due to likely API/rate-limit/workflow problem.
- Status: possible microgrant-related candidate from AsyncAPI discussion, but needs confirmation.
- Next action: inspect repo workflows and determine if issue is scoped to microgrant round.

## 4. ProjectDiscovery OSS bounty program

- Source: https://github.com/projectdiscovery/oss-bounty-program
- Status: valid bounty program exists, but no open `bounty` labeled issue found in the checked repositories during this scan.
- Next action: keep monitoring official ProjectDiscovery repos for `bounty` label.

## 5. PromptLayer slash encoding issue

- Prior candidate: https://github.com/MagnivOrg/prompt-layer-library/issues/254
- Status: no current actionable open candidate found in scan; main branch already appears to encode prompt names with `quote(prompt_name, safe='')`.
- Next action: do not spend time unless a fresh bounty/issue appears.

## Current recommendation

First target after accounts are ready: Opire featured bounties, then AsyncAPI Microgrant.

Reason: Opire shows explicit dollar amounts. AsyncAPI has structured microgrant issues but may require stricter claiming rules.
