# claude-code-hooks (shanraisshan)

**Local path:** `/Users/jennywadkins/github_repos/claude_skills/claude-code-hooks`

## Overview

A **novelty/educational sound-notification system** — plays a spoken/sound effect every time a Claude Code hook event fires. Its real reason for existence: it tracks and demonstrates **all 30 official Claude Code hook events**, kept meticulously in sync with upstream releases (badge synced to Claude Code v2.1.162, Jun 2026). Polished and marketing-forward but single-purpose: one ~480-line Python script does all the work, plus rich assets (36 sound folders, demo visualization, HTML presentation, per-OS install guides, a Codex-CLI port).

## Agents

- **claude-code-hook-agent** — Scripted workflow that triggers the 6 hooks that fire in agent sessions, playing agent-specific sounds.
- **claude-code-test-agent** — Configures all 30 hooks in frontmatter, logs each firing, reports which fire in agent contexts.
- **workflow-changelog-agent** — Read-only research agent that detects drift vs upstream Claude Code docs/changelog. ⚠️ Its prompt uses manipulative roleplay framing ("hospital system", "$200 tip") — don't copy that pattern.

## Skills

None.

## Hooks

**All 30 hook events** wired in `.claude/settings.json`, every one invoking a single Python 3 dispatcher (`hooks.py`, stdlib-only, `async: true`) that maps event → sound folder → platform audio player (`afplay`/`paplay`/PowerShell).

- **Not a safety system** — no hook blocks or validates anything; all exit 0. Minor defensive coding: directory-traversal guard on sound filenames, silent-fail, optional JSONL audit log (off by default).
- Events covered: PreToolUse (special-cases `git commit`), PermissionRequest, PostToolUse, PostToolUseFailure, PostToolBatch, UserPromptSubmit, UserPromptExpansion, Notification, MessageDisplay, Stop, SubagentStart, SubagentStop, PreCompact, PostCompact, SessionStart, SessionEnd, Setup, TeammateIdle, TaskCreated, TaskCompleted, ConfigChange, WorktreeCreate, WorktreeRemove, InstructionsLoaded, Elicitation, ElicitationResult, StopFailure, CwdChanged, FileChanged (matcher `.envrc|.env|.env.local`), PermissionDenied.
- Agent-frontmatter hooks: the 6 that fire in agent sessions, routed with `--agent=` for separate sounds.
- Per-hook enable/disable toggles in `.claude/hooks/config/hooks-config.json` (with `.local.json` override).

## Other assets

- Commands: `/commit`, `/workflows:workflow-add-hook`, `/workflows:workflow-changelog`.
- MCP: `elicit` server (demonstrates Elicitation hooks).
- `.codex/` port (hooks.json + config.toml for Codex CLI).
- Interactive real-time hook-lifecycle visualization demo (`demo/`, localhost:3456), HTML presentation, per-OS install guides.

## Character

**Highly specialized, single-domain** (audible hook notifications). Its real value is **reference**: arguably the most complete public catalog of every Claude Code hook event and when it fires, including which fire inside agent contexts.

## Install verdict

**Cherry-pick / use as reference — don't install wholesale.** Install is manual copy-paste (no installer/marketplace). All 30 hooks means a sound on nearly every action — overwhelming; most users would keep a few (SessionStart, Stop, Notification) via the config toggles. Strongest use: the authoritative example of hook wiring and an up-to-date hook-event catalog to mine for your own hook designs.
