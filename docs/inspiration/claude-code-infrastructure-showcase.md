# claude-code-infrastructure-showcase

**Local path:** `/Users/jennywadkins/github_repos/claude_skills/claude-code-infrastructure-showcase`

## Overview

A **reference library** (explicitly "NOT a working application") of production-tested Claude Code infrastructure from 6 months of real use on a TypeScript microservices project. Its centerpiece: a **hook-driven skill auto-activation system** solving "skills don't activate automatically," plus modular skills, agents, and a dev-docs system that survives context resets. High maturity: v2.0.0 hooks package, self-verifying setup wizard (`setup.ts`), 24KB README + 29KB integration guide, multi-platform mirrors (`.claude`, `.codex`, `.agents`), health checks. Stack focus: Node/Express/TS + React/MUI/TanStack, Prisma, Sentry.

## Agents (8)

- **auto-error-resolver** — Auto-fixes TypeScript compile errors from error caches left by the tsc hook.
- **code-architecture-reviewer** — Reviews recent code for best practices and architectural consistency.
- **code-refactor-master** — Comprehensive refactoring: file reorganization, splitting components, dependency-aware import updates (opus).
- **documentation-architect** — Dev docs, READMEs, API docs, data-flow diagrams.
- **frontend-error-fixer** — Frontend build-time and browser-console error diagnosis/fixes.
- **plan-reviewer** — Reviews development plans pre-implementation for flaws and alternatives (opus).
- **refactor-planner** — Produces step-by-step refactoring plans with risk assessment.
- **web-research-specialist** — Researches problems across GitHub issues, SO, Reddit, forums.

## Skills (5)

- **backend-dev-guidelines** — Node/Express/TS layered architecture, Prisma, Zod, Sentry, DI (11 resource files, progressive disclosure).
- **frontend-dev-guidelines** — React/TS: Suspense, useSuspenseQuery, MUI v7, TanStack Router, performance (11 resource files).
- **error-tracking** — Sentry v8 error tracking and performance monitoring.
- **skill-developer** — Meta-skill for creating skills and editing `skill-rules.json` triggers/enforcement (6 supporting docs).
- **source-command-verify-setup** — Runs the infra health check and fixes failures.

## Hooks (the core asset)

Pattern: thin bash wrappers shelling into **TypeScript** implementations via `tsx`. Deps: `better-sqlite3`, `minimatch`, `tsx`, `typescript`; optional AI SDKs (Anthropic/OpenAI/Gemini/Ollama behind a pluggable provider factory). Config via `.env`; "Classic" regex-only or "AI-Enhanced" modes.

Wired in settings.json:
- **skill-activation-prompt** (UserPromptSubmit) — Injects skill suggestions + session intelligence into each prompt; the auto-activation engine (~36KB TS, driven by `skill-rules.json`, optional AI classification).
- **skill-verification-guard** (PreToolUse: Edit|MultiEdit|Write) — **Can block edits** when required skills weren't activated; enforcement + guardrails (~20KB TS). Safety-oriented.
- **post-tool-use-tracker** (PostToolUse) — Tracks edited files/repos (bash, needs `jq`).
- **skill-activation-tracker** (PostToolUse: Skill) — Clears activated skills from pending-enforcement lists.
- **session-doc-updater** (Stop) — Indexes session docs, prunes stale state/caches older than 7 days.

Present but not wired (optional): **tsc-check**, **stop-build-check-enhanced**, **trigger-build-resolver**, **error-handling-reminder**.

Support libs: SQLite-backed semantic session index (`vector-store.ts`, `embeddings.ts`), session parser/state, metrics. `.codex/hooks.json` mirrors the same events via an adapter.

## Other assets

- Commands: `/dev-docs`, `/dev-docs-update`, `/route-research-for-testing`, `/verify-setup`.
- Scripts: `verify-setup.sh` health check, `skill-stats.sh`, `sync-agent-skills.sh`, `index-sessions.ts`.
- `skill-rules.json` — central trigger config: keywords, enforcement levels (block/suggest/warn), priority, guardrails per skill.
- NeoVim editor config. No MCP servers, no plugin marketplace.

## Character

**General-purpose infrastructure, stack-opinionated content.** The framework (skill auto-activation, enforcement guard, session intelligence) is broadly reusable; the bundled skills assume TS full-stack. For intermediate-to-advanced users wanting enterprise-grade automation/guardrails.

## Install verdict

**Cherry-pick / adapt — the repo itself says "copy what you need."** Real install mechanisms exist (setup wizard `npx tsx setup.ts`, 8 self-verifying health checks; manual copy; "let Claude do it").

- **Wholesale** only if you run the matching TS/React/Express/Prisma/Sentry stack.
- **Cherry-pick the hook framework** (skill-activation-prompt + skill-verification-guard + provider abstraction + skill-rules.json) and the `skill-developer` meta-skill — this is the highest-value piece for other setups; swap the stack skills for your own.
- Caveats: bash-based (macOS/Linux/WSL2 only), needs Node 18+ and `npm install` in `.claude/hooks`, some hooks need `jq`; review the verification guard's enforcement config before enabling since it can block edits.
