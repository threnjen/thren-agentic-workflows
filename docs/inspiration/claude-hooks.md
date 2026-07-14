# claude-hooks (Lasso Security)

**Local path:** `/Users/jennywadkins/github_repos/claude_skills/claude-hooks`

## Overview

A small, focused, single-purpose security repo: a **Prompt Injection Defender** protecting Claude Code from *indirect* prompt injection (malicious instructions hidden in files, web pages, or command outputs Claude reads). Early but polished — 2 commits, MIT-licensed, dual-language implementation, tied to Lasso Security's published research ("The Hidden Backdoor in Claude Coding Assistant"). Despite the plural name, it contains exactly **one** hook.

## Agents

None.

## Skills

- **prompt-injection-defender** (`.claude/skills/prompt-injection-defender/SKILL.md`) — Installs/configures the PostToolUse defense hooks; ships patterns, dual Python/TS implementations, workflow cookbook, and test fixtures.

## Hooks

One logical hook, two interchangeable implementations. Entirely security-oriented.

- **prompt-injection-defender** (PostToolUse; matchers: `Read`, `WebFetch`, `Bash`, `Grep`, `Task`, documented `mcp__*`) — Regex-scans tool outputs against `patterns.yaml` (~96 patterns across Instruction Override, Role-Playing/DAN, Encoding/Obfuscation, Context Manipulation, Instruction Smuggling; severity high/med/low). On match, emits `{"decision":"block","reason":…}` injecting a "PROMPT INJECTION WARNING" into context. **Warn-and-continue design — alerts Claude rather than hard-blocking.**
  - Python impl: run via `uv`, PEP-723 inline metadata, only dep `pyyaml`, Python ≥3.8; includes settings template + tests.
  - TypeScript impl: run via Bun; includes settings template + tests.

## Other assets

- Commands: `/install` (interactive guided installer), `/prime` (teaches the agent to react correctly to injection warnings).
- `install.sh` install script; ready-to-copy settings templates; cookbook workflows; test files/prompts for the four injection categories.

## Character

**Highly specialized — single domain** (indirect prompt-injection defense). For security-conscious users who read untrusted content (web, third-party repos, MCP outputs) and want a fast, deterministic, no-API-cost, auditable regex guardrail.

## Install verdict

**Install-as-is is reasonable** (install script + interactive command + manual docs). Low-risk: read-only scanning, warn-only, one tiny dependency.

- **Install as-is** for turnkey injection defense if the warn-only model and a `uv`/`bun` runtime are acceptable.
- **Cherry-pick** if you already run a hooks setup: the real value is `patterns.yaml` (96 curated regexes) + the single hook script — drop into your own `.github/hooks/scripts/` without the skill/commands scaffolding.
- **Caveats:** very new (2 commits, single vendor); warns rather than blocks; regex detection is bypassable and false-positive-prone. Good defense-in-depth, not a security boundary.
