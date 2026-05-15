# Bounty Worker Queue

Last manual build: 2026-05-16 Asia/Dubai

## Queue Item 1: Verify Opire featured $120 TypeScript bounty

- Source: https://opire.dev/
- Amount hint: $120
- Task hint: Migration generation drops and creates columns instead of altering, resulting in data loss.
- Worker action:
  1. Open Opire account/login.
  2. Find the featured bounty detail page.
  3. Confirm repository, issue URL, claim rules, and whether it is already claimed.
  4. If open, inspect repo and reproduce.

## Queue Item 2: AsyncAPI CLI request body validation bug

- Issue: https://github.com/asyncapi/cli/issues/1987
- Aggregate: https://github.com/asyncapi/cli/issues/2125
- Worker action:
  1. Confirm microgrant eligibility and claim rules.
  2. Clone `asyncapi/cli`.
  3. Reproduce skipped request body validation.
  4. Patch validator logic and add test.

## Queue Item 3: AsyncAPI website dashboard workflow bug

- Issue: https://github.com/asyncapi/website/issues/5333
- Worker action:
  1. Confirm if it is in a paid microgrant round.
  2. Inspect dashboard update workflow.
  3. Reproduce missing dashboard output.
  4. Patch workflow/API handling if scope is clear.
