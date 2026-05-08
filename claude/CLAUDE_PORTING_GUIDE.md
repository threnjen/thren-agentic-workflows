# Claude Porting Guide

This document describes how to port agent definitions from the GitHub master source into Claude-specific agent files.

## Scope

- Source: `.github/agents/*.agent.md` and `.github/agents/*.md` agent definitions
- Destination: `claude/agents/*.md`
- This guide is Claude-only by design.

For OpenCode, see `opencode/OPENCODE_PORTING_GUIDE.md`.
For Codex, see `codex/CODEX_PORTING_GUIDE.md`.
For cross-platform tool names, see `docs/porting/TOOL_MAPPING.md`.

## Golden Rule

Claude does not support `.github/instructions/*.instructions.md` `applyTo` loading.
Instruction content must be present in the generated agent body.

## Frontmatter Expectations

Claude agent files use Markdown frontmatter with:

- `name: <kebab-case>`
- `description: <text>`
- `tools: Skill, Read, Grep, Glob, Edit, Write, WebFetch, Bash, Agent` (as applicable)

## Tool Mapping (GitHub to Claude)

- `read` -> `Read`
- `search` -> `Grep`, `Glob`
- `edit` -> `Edit`, `Write`
- `fetch` -> `WebFetch`
- `execute` -> `Bash`
- `agent` -> `Agent`
- `todo` -> no Claude equivalent

## Conversion Checklist

1. Start from `.github/agents/*` source.
2. Resolve applicable `.github/instructions/*.instructions.md` entries by `applyTo`.
3. Convert tool names to Claude names.
4. Ensure instruction intent is present in the final agent body.
5. Keep behavior equivalent to source, excluding unsupported tool semantics.

## Validation Checklist

- Frontmatter parses correctly.
- Tool names are valid Claude names.
- Unsupported GitHub-only tools are dropped.
- Agent behavior remains aligned with source intent.
- Agent appears in Claude agent discovery.

## Maintenance Note

Treat `.github/` as source of truth. Do not directly hand-edit generated agent behavior in `claude/agents` unless you are intentionally creating a Claude-only override with documented rationale.
