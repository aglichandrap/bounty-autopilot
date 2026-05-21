# TaskBounty Worker

Last run: 2026-05-21 04:56 UTC

This worker is the execution layer after scouting: it uses the TaskBounty agent API, requests repo access, prepares a workspace profile, and submits a patch when a matching `taskbounty_patches/<task_id>.patch` file exists.

## 1. Fix: Security Roadmap: Protecting API Keys from Agent Access

- Amount: $10
- Task: https://www.task-bounty.com/task/fix-security-roadmap-protecting-api-keys-from-agen-uej5sq
- Task ID: 623bb359-6405-4142-a1c5-f06ce4b9779c
- Status: public_workspace_prepared
- Repo: https://github.com/openclaw/openclaw
- Message: TaskBounty access endpoint had no GitHub installation, but the public upstream repo was cloned and profiled. A patch can still be submitted through /submissions/patch.
- Detected stack markers: package.json
- Detected languages: js, ts

### Sample Files

- `.gitattributes`
- `pnpm-workspace.yaml`
- `tsconfig.core.json`
- `.semgrepignore`
- `vitest.config.ts`
- `Dockerfile`
- `tsdown.config.ts`
- `docker-compose.yml`
- `appcast.xml`
- `AGENTS.md`
- `tsconfig.plugin-sdk.dts.json`
- `openclaw.mjs`
- `.npmrc`
- `render.yaml`
- `LICENSE`
- `VISION.md`
- `CHANGELOG.md`
- `.oxfmtrc.jsonc`
- `SECURITY.md`
- `.gitignore`
- `.oxlintrc.json`
- `.crabbox.yaml`
- `tsconfig.extensions.json`
- `package.json`
- `pnpm-lock.yaml`
- `CONTRIBUTING.md`
- `tsconfig.projects.json`
- `.dockerignore`
- `.pre-commit-config.yaml`
- `fly.toml`
