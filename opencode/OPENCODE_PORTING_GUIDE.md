# OpenCode Porting Guide

This document describes how to port agent definitions from the GitHub master source into OpenCode-specific agent files.

## Scope

- Source: `.github/agents/*.agent.md` and `.github/agents/*.md` agent definitions
- Destination: `opencode/agents/*.md`
- This guide is OpenCode-only by design.

For Claude, see `claude/CLAUDE_PORTING_GUIDE.md`.
For Codex, see `codex/CODEX_PORTING_GUIDE.md`.
For cross-platform tool names, see `docs/porting/TOOL_MAPPING.md`.

## OpenCode Model

OpenCode agent files use frontmatter with:

- `description: "..."`
- `model: ...` (for example: `model: deepseek/deepseek-v4-pro`)
- optional `mode: subagent` and `hidden: true`
- optional `permission:` object (omit if no permissions are derived)

## Tool Mapping (GitHub to OpenCode)

- `read` -> `permission.read: allow`
- `search` -> `permission.grep: allow`, `permission.glob: allow`
- `edit` -> `permission.edit: allow`
- `fetch` -> `permission.webfetch: allow`
- `execute` -> `permission.bash: allow`
- `agent` -> `permission.task: allow`
- `todo` -> `permission.todowrite: allow`

## Instruction Handling

OpenCode does not use GitHub `applyTo` resolution natively.
Agent output should include the required instruction intent in agent content so behavior remains aligned with source constraints. Append inlined instruction content under a `## Auto-Loaded Instructions` section header at the end of the agent body.

## Conversion Checklist

1. Start from `.github/agents/*` source.
2. Resolve applicable `.github/instructions/*.instructions.md` entries by `applyTo`.
3. Convert GitHub tools to OpenCode permission keys.
4. Apply established filename aliases. The canonical alias list is:
   - `documentation-architect` → `docs-writer`
   - `web-research-specialist` → `web-researcher`
   - `audit-code-or-infra` → `audit-code-infra-refactor`
5. Rewrite source agent references in body text to OpenCode destination identifiers. Use destination filename stems, preserving established aliases such as `@web-researcher` and `docs-writer`.
6. Ensure behavioral equivalence with source intent.

## Validation Checklist

- Frontmatter parses correctly.
- Permission keys are valid OpenCode keys.
- Required permissions are present and minimal.
- Agent references in workflow text point at OpenCode destination identifiers, not GitHub display names.
- Agent behavior remains aligned with source intent.
- Agent appears in OpenCode discovery.

## Maintenance Note

Treat `.github/` as source of truth. Do not directly hand-edit generated agent behavior in `opencode/agents` unless you are intentionally creating an OpenCode-only override with documented rationale.
