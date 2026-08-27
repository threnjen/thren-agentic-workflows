# Claude Porting Guide

This document describes how to port agent definitions from the GitHub master source into Claude-specific agent files.

## Scope

- Source: `.github/agents/*.agent.md` and `.github/agents/*.md` agent definitions
- Destinations: `claude/agents/*.md` (subagents) and `claude/commands/*.md` (slash commands)
- This guide is Claude-only by design.

For OpenCode, see `OPENCODE_PORTING_GUIDE.md`.
For Codex, see `CODEX_PORTING_GUIDE.md`.
For cross-platform tool names, see `docs/porting/TOOL_MAPPING.md`.

## Emission Model (which file(s) each agent produces)

Claude cannot make its main loop *become* a subagent — a subagent is only ever
reached by spawning it into an isolated context. So a "primary" persona that
should be adopted inline must be ported as a **slash command**, not a subagent.
The source-of-truth flag `user-invocable:` (default `true`) drives the split:

| Source `user-invocable` | Referenced as a child agent? | Emits |
|---|---|---|
| `false` | (n/a) | **Subagent only** → `claude/agents/z-<id>.md` |
| `true` | no | **Slash command only** → `claude/commands/<id>.md` |
| `true` | yes (dual-use) | **Both** → `claude/commands/<id>.md` **and** `claude/agents/<id>.md` |

- "Referenced as a child agent" means the source `name:` appears in some other
  agent's `agents:` frontmatter list. This is derived from the source of truth —
  never hard-coded. Add a new reference and the agent automatically becomes
  dual-use on the next propagation.
- Dual-use exists so an orchestrator command can still `Task`-spawn the worker
  (e.g. `project-planner` spawns `web-researcher`) while the same role is also
  directly invocable as `/web-researcher`.
- When an agent is reclassified to command-only, delete any stale
  `claude/agents/<id>.md` it previously generated. Never delete hand-authored
  Claude-only agents (e.g. `single-feature.md`) or `README.md`.

## Golden Rule

Claude does not support `.github/instructions/*.instructions.md` `applyTo` loading.
Instruction content must be present in the generated agent body.

## Frontmatter Expectations

**Subagent files** (`claude/agents/*.md`) use Markdown frontmatter with:

- `name: <kebab-case>`
- `description: <text>`
- `tools: Skill, Read, Grep, Glob, Edit, Write, WebFetch, Bash, Agent` (`Skill` is always included; other tools are included as applicable)
- `user-invocable: false` (required in this repository so Claude-derived subagents stay hidden in the GitHub Copilot agent picker)

**Slash command files** (`claude/commands/*.md`) use minimal frontmatter:

- `description: <text>`
- No `tools:` line — a command runs in the main conversation and inherits the live session's tools (that is the whole point: the persona is adopted inline).
- No `name:` line — the command's invocation name is its filename stem (`/<id>`).

## Tool Mapping (GitHub to Claude)

- `read` -> `Read`
- `search` -> `Grep`, `Glob`
- `edit` -> `Edit`, `Write`
- `fetch` -> `WebFetch`
- `execute` -> `Bash`
- `agent` -> `Agent`
- `todo` -> no Claude equivalent

## Conversion Checklist

1. Start from `.github/agents/*` source. Read its `user-invocable:` flag (default `true`) and determine whether its `name:` is referenced in any other agent's `agents:` list. Use the [Emission Model](#emission-model-which-files-each-agent-produces) table to decide which file(s) to produce.
2. Resolve applicable `.github/instructions/*.instructions.md` entries by `applyTo`.
3. Convert tool names to Claude names (subagent files only — commands carry no `tools:` line).
4. Resolve the final Claude destination identifier from the generated filename stem, including any aliasing or `z-` prefixing for hidden subagents. The slash command uses the same stem (without any `z-` prefix, since only user-invocable agents become commands).
5. Rewrite source agent references in the body to Claude handles. Worker subagents use their `@z-...` handle such as `@z-feature-plan-expander`; dual-use agents use their bare handle such as `@web-researcher`. References always resolve to the **subagent** file so orchestrators can spawn them.
6. **Subagent file:** set frontmatter `name:` to the final destination identifier and add `user-invocable: false`. **Command file:** emit only `description:` frontmatter (no `name:`, no `tools:`, no `user-invocable:`).
7. Append inlined instruction content under a `## Auto-Loaded Instructions` section header at the end of the body (both file types).
8. Ensure instruction intent is present in the final body. Keep behavior equivalent to source, excluding unsupported tool semantics.
9. Insert the correct adoption paragraph after the opening identity statement (the first "You are..." block), before any workflow or constraint content:
   - **Slash command** (the inline persona): use the command adoption clause —
     ```
     You are now operating as **<name>** directly in this conversation. Adopt this role and carry out the work yourself in the current session — do not spawn `<id>` (or any copy of this role) as a subagent to do it. Delegate only to distinct child agents when this workflow explicitly calls for them.
     ```
     Replace `<name>` with the source `name:` value and `<id>` with the command stem.
   - **Dual-use subagent file** (`user-invocable: true` agent that is also spawned): keep the legacy subagent clause —
     ```
     When the user addresses you by name or role, begin work in this role immediately. Do not spend your first action invoking `<id>` as a subagent. Delegate only to distinct child agents when the workflow explicitly calls for them.
     ```
   - **Worker subagent** (`z-` prefixed, `user-invocable: false`): add **no** adoption paragraph.

## Validation Checklist

- Each source agent emitted the correct file(s) per the Emission Model table (subagent-only / command-only / both).
- Frontmatter parses correctly for both file types.
- Subagent files: `name:` matches the filename stem (including alias and `z-` cases) and `user-invocable: false` is present.
- Command files: only `description:` frontmatter; no `name:`, `tools:`, or `user-invocable:` lines.
- Tool names in subagent files are valid Claude names; commands carry no tools list.
- Agent references in workflow text point at Claude subagent handles, not GitHub display names.
- Unsupported GitHub-only tools are dropped.
- Behavior remains aligned with source intent.
- Command files include the command adoption clause; dual-use subagent files include the legacy subagent clause; `z-` workers include neither.
- No stale `claude/agents/*.md` remains for an agent reclassified to command-only; hand-authored agents and `README.md` are untouched.

## Claude Code Behavioral Notes

These are Claude Code-specific behaviors that must be enforced in every ported agent. The source `.github/` agents do not need them because GitHub Copilot's tool model does not exhibit these failure modes.

### User-Invocable Personas Are Slash Commands, Not Subagents

A Claude subagent can only be reached by spawning it into an isolated context —
the main loop cannot "become" it. Prompt text inside a subagent file telling it
to "begin work immediately, don't spawn yourself" cannot change that, because the
file is only loaded *by spawning*. This is why user-invocable personas are ported
as **slash commands** (`claude/commands/*.md`): a command body is injected into
the current conversation, so the main persona adopts the role inline.

**Rule:** Every `user-invocable: true` source agent emits a `claude/commands/<id>.md`
slash command whose body carries the command adoption clause (see Conversion
Checklist step 9). If that agent is also spawned as a child by an orchestrator
(dual-use), it *additionally* emits a `claude/agents/<id>.md` subagent file that
keeps the legacy subagent clause. `z-` workers (`user-invocable: false`) emit a
subagent file only and receive no adoption clause.

### File Operations: Never Fall Back to Bash

In Claude Code, when `Edit` or `Write` tool calls fail (e.g., wrong path, missing parent directory, permissions), Claude may incorrectly conclude those tools are "not available" and fall back to writing files via `Bash` using `cat`, `echo`, or heredoc syntax. This produces unreadable diffs, bypasses linting, and breaks project conventions.

**Rule:** Any ported agent that has both `Bash` AND `Edit`/`Write` in its tools list and is responsible for creating or modifying files **must** include the following constraint in its `## Constraints` section:

```
- NEVER write or overwrite files using Bash (`cat`, `echo`, heredoc, etc.) — always use the `Write` tool to create new files and `Edit` to modify existing ones. If these tools return an error, stop and report the failure; do not fall back to shell commands.
```

This applies to: `z-feature-implementer`, `z-reviewer-plan-conformance`, `z-test-writer`, `z-test-fixer`, `debugger`, `single-feature-agent`, and any other agent that produces source code or test files.

## Maintenance Note

Treat `.github/` as source of truth. Do not directly hand-edit generated agent behavior in `claude/agents` unless you are intentionally creating a Claude-only override with documented rationale.
