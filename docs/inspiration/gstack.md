# gstack — "Garry's Stack" (Garry Tan)

**Local path:** `/Users/jennywadkins/github_repos/claude_skills/gstack`

## Overview

MIT-licensed, v1.60.1.0, mature and very actively developed (912KB CHANGELOG, 279-entry test suite, CI). Turns Claude Code into a "virtual engineering team" — CEO, eng manager, designer, reviewer, QA lead, security officer, release engineer — invoked as slash commands. **Skill-centric architecture** (~59 SKILL.md files) in TypeScript/Bun, bundling real tooling: a fast headless Chromium browser, a Chrome MV3 extension, PDF generator, diagram renderer, and a Supabase/PGLite-backed memory system ("gbrain"). Multi-host adapters for Claude, Codex, Cursor, Kiro, OpenCode, and more.

## Agents

No standalone agent files — the "23 specialists" are implemented **as skills** embodying roles (CEO → `/plan-ceo-review`, Reviewer → `/review`, CSO → `/cso`, Release Engineer → `/ship`, etc.).

## Skills (59, by category)

- **Plan-mode review (9):** office-hours, plan-ceo-review, plan-eng-review, plan-design-review, plan-devex-review, plan-tune, **autoplan** (runs CEO→design→eng→DX sequentially), design-consultation, spec (vague intent → executable spec, files a GitHub issue).
- **Implementation/review (8):** **review** (pre-landing PR review for prod bugs that pass CI), codex (OpenAI Codex second opinion), investigate (root-cause debugging), design-review/design-shotgun/design-html, devex-review, health (code-quality dashboard).
- **QA/browser (7+):** qa (real-browser test+fix), qa-only, browse, open-gstack-browser, scrape, skillify (codify a scrape into a permanent skill), benchmark/benchmark-models, pair-agent.
- **Release/deploy (5):** ship (test→review→bump→PR), land-and-deploy, canary (post-deploy monitoring), landing-report, document-release.
- **Security/safety (4):** **cso** (OWASP Top 10 + STRIDE audit), **careful** (destructive-command guardrails), **guard** (careful + directory-scoped edits), **freeze/unfreeze** (restrict edit boundary to a dir). Note: safety is skill-delivered, not hook-delivered.
- **iOS suite (5):** ios-qa, ios-fix, ios-clean, ios-design-review, ios-sync.
- **Docs/knowledge/memory (8):** document-generate, diagram, make-pdf, learn, retro, context-save/context-restore, setup-gbrain, sync-gbrain.
- Setup/maintenance skills + 4 OpenClaw-ported variants.

## Hooks (3, Bun/TypeScript)

All exist to make the `plan-tune` AskUserQuestion preference system deterministic — **not** security hooks:

- **question-preference-hook** (PreToolUse on AskUserQuestion) — enforces never-ask/always-ask preferences; denies two-way questions with an auto-decided recommendation; one-way doors always defer to the user.
- **question-log-hook** (PostToolUse) — logs every question + user choice, deduped.
- **auq-error-fallback-hook** (PostToolUse) — injects a fallback reminder when the question tool errors.

Registered into `~/.claude/settings.json` by the setup script (no committed settings.json).

## Other assets

~76 helper binaries (`browse` CLI, gbrain memory suite, analytics/security dashboards, JSONL decision/learnings logs, a **redaction engine** that blocks AWS keys/tokens/PEM/JWT before memory sync, background job runner, team mode); Chrome extension; per-model prompt overlays; Supabase backend; LLM-eval harnesses.

## Character

**General-purpose, opinionated, end-to-end engineering workflow** spanning ideation → planning → build → review → QA → security → ship → monitor → retro, plus its own browser and memory infrastructure. Audience: founders/technical CEOs, tech leads wanting rigorous review+release automation.

## Install verdict

**Install as-is if you want the full opinionated workflow; otherwise cherry-pick skills.** Official install clones into `~/.claude/skills/gstack` and runs `./setup` (self-contained namespace — low-risk to back out; team mode available). Requirements are non-trivial: Bun 1.0+, Chromium for browser tools. High-value standalone cherry-picks (largely portable markdown): **review, cso, qa, investigate, retro, careful/guard/freeze**. Skip the 3 hooks unless you adopt the plan-tune preference system.
