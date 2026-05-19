# TaskBounty Worker

Last run: 2026-05-19 17:10 UTC

This worker is the execution layer after scouting: it uses the TaskBounty agent API, requests repo access, prepares a workspace profile, and submits a patch when a matching `taskbounty_patches/<task_id>.patch` file exists.

## 1. Fix: Flows not working when using celery rabitmq and redis

- Amount: $10
- Task: https://www.task-bounty.com/task/fix-flows-not-working-when-using-celery-rabitmq-an-9rt47y
- Task ID: 1a7cb78f-67a3-4d95-a37b-404d773d9099
- Status: public_workspace_prepared
- Repo: https://github.com/langflow-ai/langflow
- Message: TaskBounty access endpoint had no GitHub installation, but the public upstream repo was cloned and profiled. A patch can still be submitted through /submissions/patch.
- Detected stack markers: package.json, pyproject.toml
- Detected languages: js, py, ts

### Sample Files

- `.gitattributes`
- `codecov.yml`
- `.coderabbit.yaml`
- `.secrets.baseline`
- `.composio.lock`
- `DESIGN.md`
- `uv.lock`
- `RELEASE.md`
- `ci-skip-analysis.md`
- `Makefile`
- `AGENTS.md`
- `render.yaml`
- `LICENSE`
- `DEVELOPMENT.md`
- `SECURITY.md`
- `package-lock.json`
- `.gitignore`
- `.eslintrc.json`
- `package.json`
- `CONTRIBUTING.md`
- `pyproject.toml`
- `.dockerignore`
- `CODE_OF_CONDUCT.md`
- `.pre-commit-config.yaml`
- `Makefile.frontend`
- `.whitesource`
- `AGENTS-example.md`
- `CLAUDE.md`
- `README.md`
- `.env.example`

## 2. Fix: Editor: scroll jumps randomly (related to Chrome, Electron, xinput)

- Amount: $10
- Task: https://www.task-bounty.com/task/fix-editor-scroll-jumps-randomly-related-to-chrome-97d1ll
- Task ID: 5e9ad131-6f9b-45b7-929e-30f5421b7f8b
- Status: public_workspace_prepared
- Repo: https://github.com/microsoft/vscode
- Message: TaskBounty access endpoint had no GitHub installation, but the public upstream repo was cloned and profiled. A patch can still be submitted through /submissions/patch.
- Detected stack markers: package.json
- Detected languages: js, rs, ts

### Sample Files

- `.gitattributes`
- `CodeQL.yml`
- `.nvmrc`
- `.mention-bot`
- `gulpfile.mjs`
- `.vscode-test.js`
- `AGENTS.md`
- `cglicenses.json`
- `.npmrc`
- `cgmanifest.json`
- `SECURITY.md`
- `package-lock.json`
- `.gitignore`
- `product.json`
- `.lsifrc.json`
- `ThirdPartyNotices.txt`
- `.eslint-ignore`
- `tsfmt.json`
- `.editorconfig`
- `package.json`
- `.mailmap`
- `CONTRIBUTING.md`
- `eslint.config.js`
- `.git-blame-ignore-revs`
- `README.md`
- `LICENSE.txt`
- `extensions/esbuild-common.mts`
- `extensions/esbuild-webview-common.mts`
- `extensions/.npmrc`
- `extensions/cgmanifest.json`

## 3. Fix: Security Roadmap: Protecting API Keys from Agent Access

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
