# claudekit (carlrannaberg)

**Local path:** `/Users/jennywadkins/github_repos/claude_skills/claudekit`

## Overview

A mature, published npm package: "smart guardrails and workflow automation for Claude Code." Not a loose markdown collection — a full **TypeScript CLI application** (`bin/claudekit` + `bin/claudekit-hooks`) that installs and manages agents, commands, and executable hooks via `claudekit setup`. High maturity: npm v0.9.5+, OIDC trusted publishing, 89KB CHANGELOG, full unit/integration/e2e test suite, listed in Awesome Claude Code. Requires Node 20+ (docs say Claude Code Max plan). Core value: real-time error catching (typecheck/lint/test on edit), git checkpoints, file-access security guard, and ~35 expert subagents.

## Agents (~35 domain experts)

Highlights: **oracle** (deep reasoning advisor), **code-search**, **triage-expert**, **code-review-expert** (6-aspect review), **research-expert**, plus deep specialists: typescript-expert/-type-expert/-build-expert, react-expert/-performance-expert, framework-nextjs-expert, nodejs-expert, database-postgres/-mongodb/-expert, testing/jest/vitest/e2e-playwright experts, devops-expert, infrastructure-docker/-github-actions experts, build-tools-webpack/-vite experts, frontend-accessibility/-css experts, git-expert, refactoring-expert, code-quality-linting-expert, cli-expert, ai-sdk-expert, nestjs-expert, kafka-expert, loopback-expert, documentation-expert.

## Skills

None — capabilities are delivered as agents + commands + hooks.

## Hooks (20+, TypeScript, dispatched via the `claudekit-hooks` binary)

Mostly quality/safety-oriented, validation-only, non-destructive:

- **file-guard** (PreToolUse: Read|Edit|Write|Bash) — **SECURITY**: blocks AI access to sensitive files via ignore-file patterns; includes a bash-command parser + heuristics engine to block exfiltration. The standout safety hook.
- **typecheck-changed / lint-changed / test-changed** (PostToolUse) — tsc / Biome-ESLint / related tests on changed files.
- **check-any-changed** (PostToolUse) — blocks `any` types in changed TS.
- **check-comment-replacement** (PostToolUse) — detects real code replaced by comments (anti-laziness guard).
- **codebase-map-update** (PostToolUse) / **codebase-map** (UserPromptSubmit) — maintains and injects a codebase map.
- **create-checkpoint** (Stop) — git auto-checkpoint enabling `/checkpoint:restore`.
- **check-todos** (Stop) — validates todo completion before finishing.
- **typecheck-project / lint-project / test-project / self-review** (Stop + SubagentStop) — full-project validation and critical self-review.
- **thinking-level** (UserPromptSubmit) — injects thinking-level keywords.
- Unwired extra: check-unused-parameters. Infra: hook profiling, logging, session-utils, registry/runner auto-discovery, sensitive-patterns defaults.

## Other assets

- Namespaced commands: `git:*`, `checkpoint:*`, `spec:*` (create/decompose/execute/validate — spec-driven workflow), `hook:*` (enable/disable/status), `agents-md:*`, plus code-review, create-command, create-subagent, research, validate-and-fix.
- Ready-to-copy example settings per stack (typescript, python, javascript, ci-cd, minimal…).
- 30KB AGENTS.md symlinked to CLAUDE.md/GEMINI.md/.cursorrules/.windsurfrules — cross-tool rules. No MCP servers.

## Character

**General-purpose guardrail/productivity framework**, leaning heavily JS/TS ecosystem in its agent roster; hooks and workflow commands (checkpoints, file-guard, spec workflow) are language-agnostic.

## Install verdict

**Install as-is via its official CLI** (`npm i -g claudekit && claudekit setup`) — hooks are a compiled binary, so cherry-picking individual hooks by copy-paste is impractical. The agent/command *markdown* is portable if you only want prompt content. Standout adoption reasons: **file-guard** and **codebase-map**; also checkpoints + self-review. Low trust risk: validation-oriented, non-destructive, well-tested.
