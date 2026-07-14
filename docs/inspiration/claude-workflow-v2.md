# claude-workflow-v2 / project-starter (CloudAI-X)

**Local path:** `/Users/jennywadkins/github_repos/claude_skills/claude-workflow-v2`

## Overview

A **universal Claude Code workflow plugin** (MIT, v2.0.6): agents, skills, hooks, 26 slash commands, and templates for "any software project." Notably mature: full plugin manifest, npm installer, skills.sh compatibility (claims 35+ AI tools incl. Cursor/Codex/Windsurf), 20KB README, CHANGELOG/SECURITY/PRIVACY/PERMISSIONS docs, GitHub workflows. Ships Codex-flavored variants too.

## Agents (7)

- **code-reviewer** — Post-edit/pre-commit review: quality, security, performance, maintainability.
- **debugger** — Root-cause analysis for errors, crashes, memory leaks, race conditions, failing tests.
- **docs-writer** — READMEs, API docs, architecture docs, changelogs, migration notes.
- **orchestrator** — Master coordinator for multi-step tasks; delegates to specialists; GitHub PR workflows (largest, 12KB).
- **refactorer** — Tech debt, code smells, DRY/SOLID, design patterns.
- **security-auditor** — OWASP Top 10, auth/secrets/JWT/CORS review and hardening.
- **test-architect** — Test strategy, coverage, mocking, flaky/integration/E2E handling.

## Skills (14)

analyzing-projects, convex-backend, database-design, designing-apis, designing-architecture, designing-tests, devops-infrastructure, error-handling, managing-git, optimizing-performance, **parallel-execution** (parallel subagent patterns), security-patterns, vercel-react-best-practices, web-design-guidelines.

## Hooks (15 scripts, wired via `hooks/hooks.json`)

Mix of Python 3 (stdlib-only) and bash (notifiers want `jq`). **Three can block; the rest are informational.**

| Hook | Event | What it does |
|---|---|---|
| protect-files.py | PreToolUse (Edit\|Write) | **Blocks** edits to production configs, lock files, sensitive dirs |
| security-check.py | PreToolUse (Edit\|Write) | **Blocks** writes containing secrets/security issues |
| pre-commit-check.py | PreToolUse (Edit\|Write) | Flags debug statements, temp markers, oversized content |
| log-commands.sh | PreToolUse (Bash) | Audit-logs every bash command to `.claude/command-history.log` |
| branch-protection.sh | PreToolUse (Bash) | Warns on git ops targeting protected branches (non-blocking) |
| format-on-edit.py | PostToolUse | Auto-runs the right formatter by file type |
| typescript-check.py | PostToolUse | `tsc --noEmit` after .ts/.tsx edits (informational) |
| notify-input.sh | Notification | Desktop alert when Claude needs input |
| verify-on-complete.py | Stop | Quick validation checks on completion |
| suggest-doc-updates.py | Stop | Suggests CLAUDE.md/AGENTS.md updates after big changes |
| notify-complete.sh | Stop | Desktop alert on completion |
| track-metrics.py | Stop | Session telemetry → `.claude/agent-metrics.jsonl` |
| validate-environment.py | SessionStart | Checks required tools/config at startup |
| validate-prompt.py | UserPromptSubmit | Validates prompts, may inject warnings/context |

## Other assets

- **26 commands** (plan, review, commit-push-pr, security-scan, parallel-analyze, parallel-review, save-session-learnings, validate-build, …).
- Templates (CLAUDE.md, settings.json, mcp.json), plugin marketplace manifests, npm installer (`npx install-claude-workflow-v2`), `.codex/` port, orchestration examples. No bundled MCP servers.

## Character

**Broad, general-purpose toolset** covering the full SDLC — planning, architecture, review, testing, security, docs, git, DevOps. Emphasis on orchestration and parallel multi-agent workflows. Only mildly niche: Convex + Vercel/React skills.

## Install verdict

**Safe to install as-is, or cherry-pick — a genuine distributable plugin.** Multiple first-class install paths (skills.sh, npm installer, plugin marketplace, `--plugin-dir`). Agents and skills are cleanly modular for cherry-picking. **Review hooks before enabling:** protect-files/security-check/pre-commit-check gate edits, log-commands writes a full audit log. Dependencies are light (stdlib Python, bash + jq).
