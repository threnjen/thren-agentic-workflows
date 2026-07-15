# buildwithclaude (davepoon)

**Local path:** `/Users/jennywadkins/github_repos/claude_skills/buildwithclaude`

## Overview

A **plugin marketplace and discovery platform** for Claude Code (powers buildwithclaude.com) — a huge curated *aggregator*, not a cohesive toolset. `.claude-plugin/marketplace.json` registers **160 plugins**: ~226 unique agents, ~206 unique skills, ~360 commands, 28 unique hooks, plus a 100KB MCP-server index, Next.js web UI, and active PR-driven contributions. Install model: `/plugin marketplace add davepoon/buildwithclaude`, then install individual plugins (or `all-*` aggregates — don't).

## Agents (~226, by bundle)

Category bundles: ai-agents (mcp-expert, project-supervisor-orchestrator…), data-ai (ai-engineer, prompt-engineer, mlops-engineer…), development-architecture (backend-architect, graphql-architect, nextjs-app-router-developer…), language-specialists (12 language experts), quality-security (security-auditor, incident-responder, error-detective, test-automator, mcp-security-auditor…), infrastructure-operations (cloud-architect, terraform-specialist…), research (9 research orchestration agents), documentation, design, media/podcasting, crypto, sales/marketing, business/finance, meta-orchestration personas, uc-taskmanager (planner/specifier/builder/verifier/committer/scheduler spec pipeline).

Notable standalone plugins: **gsd** (33 agents — full research→plan→build→audit pipeline), **claude-ops** (15 — autonomous ops with exec personas), **meeting-bots** (25 — simulated review panels), **ralph-review-trio** (haiku/sonnet/opus tiered review), ag2-agent-builder, agent-triforce, startup-superpowers.

## Skills (~206)

Concentrated in standalone plugins: **gsd (83)**, **claude-ops (30)**, origin (11, provenance/attribution), venture-capital-intelligence (9), startup-superpowers (8), vulnetix (7, vulnerability management), frontend-design-pro (6), agent-triforce (6), plus dozens of single-skill plugins.

## Hooks (28 unique — the interesting part for this project)

**Safety/security (bash, mostly PreToolUse):**
- `file-protection` — block edits to critical/protected files.
- `conventional-commits` — validate & block non-conforming commit messages.
- `sql-bulk-delete-warn` — warn on destructive DELETE/UPDATE/TRUNCATE without safeguards.
- `notify-before-bash` — security notice before any Bash exec.
- `file-backup` — back up files before editing.
- `security-scanner` (PostToolUse) — scan for secrets/vulns after modification.
- `dependency-checker` (PostToolUse) — audit dependencies.
- `no-vibes` (Stop) — blocks "done/shipped" claims lacking same-turn verification evidence.
- `windows-python-stub-detector` (SessionStart) — warns about the Windows Store python3 stub.

**Git/format/dev (PostToolUse):** auto-git-add, git-add-changes, smart-commit, format-python-files (black), format-javascript-files (prettier), smart-formatting, lint-on-save, build-on-change, test-runner, run-tests-after-changes, change-tracker, performance-monitor, context-monitor.

**Notifications:** desktop, Discord/Slack/Telegram (simple/error/detailed variants) — need webhook/bot tokens.

Deps: `jq`/`curl`, black/prettier for formatters; no Node hooks. A `hook-validation-report.json` suggests automated hook validation.

## Other assets

~360 commands in category bundles (code-analysis-testing 19, project-task-management 17, git 12, security-audit, ci-deployment…); a 100KB `mcp-servers.json` ecosystem index; ~25 `msapps-*` MCP plugins (notion, wordpress, whatsapp, gcloud health checks…).

## Character

**Broad meta-catalog / app store** — spans engineering, DevOps, security, data/AI, crypto, media, marketing, bioinformatics. For users browsing for extensions and plugin authors, not an opinionated workflow.

## Install verdict

**Cherry-pick — never bulk-install.** Add the marketplace and install only specific plugins. Best reusable pieces: the **safety hooks** (`file-protection`, `sql-bulk-delete-warn`, `no-vibes`, `conventional-commits`, `security-scanner`), quality/security agent bundles, and any `msapps-*` MCP server you actually need. The big opinionated pipelines (gsd, claude-ops, meeting-bots) are better studied than adopted. **Vet each hook's script body before enabling** — they auto-run on tool events and some need secrets.
