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
- `tools: Skill, Read, Grep, Glob, Edit, Write, WebFetch, Bash, Agent` (`Skill` is always included; other tools are included as applicable)
- `user-invocable: false` (required in this repository so Claude-derived agents stay hidden in the GitHub Copilot agent picker)

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
4. Resolve the final Claude destination identifier from the generated filename stem, including any aliasing or `z-` prefixing for hidden subagents.
5. Rewrite source agent references in the body to Claude handles. User-facing agents should be referenced by Claude filename handle such as `@project-planner`; hidden subagents should use their `@z-...` handle such as `@z-feature-plan-expander`.
6. Set frontmatter `name:` to that same final destination identifier rather than to the raw source slug.
7. Add `user-invocable: false` to every Claude agent frontmatter/header block without exception.
8. Append inlined instruction content under a `## Auto-Loaded Instructions` section header at the end of the agent body.
9. Ensure instruction intent is present in the final agent body.
10. Keep behavior equivalent to source, excluding unsupported tool semantics.

## Validation Checklist

- Frontmatter parses correctly.
- Frontmatter `name:` matches the generated Claude filename stem, including alias and `z-` prefix cases.
- `user-invocable: false` is present in every Claude agent frontmatter/header block.
- Tool names are valid Claude names.
- Agent references in workflow text point at Claude handles, not GitHub display names.
- Unsupported GitHub-only tools are dropped.
- Agent behavior remains aligned with source intent.
- Agent appears in Claude agent discovery.

## Claude Code Behavioral Notes

These are Claude Code-specific behaviors that must be enforced in every ported agent. The source `.github/` agents do not need them because GitHub Copilot's tool model does not exhibit these failure modes.

### File Operations: Never Fall Back to Bash

In Claude Code, when `Edit` or `Write` tool calls fail (e.g., wrong path, missing parent directory, permissions), Claude may incorrectly conclude those tools are "not available" and fall back to writing files via `Bash` using `cat`, `echo`, or heredoc syntax. This produces unreadable diffs, bypasses linting, and breaks project conventions.

**Rule:** Any ported agent that has both `Bash` AND `Edit`/`Write` in its tools list and is responsible for creating or modifying files **must** include the following constraint in its `## Constraints` section:

```
- NEVER write or overwrite files using Bash (`cat`, `echo`, heredoc, etc.) — always use the `Write` tool to create new files and `Edit` to modify existing ones. If these tools return an error, stop and report the failure; do not fall back to shell commands.
```

This applies to: `z-feature-implementer`, `z-feature-reviewer`, `z-test-writer`, `z-test-fixer`, `debugger`, `single-feature-agent`, and any other agent that produces source code or test files.

## Maintenance Note

Treat `.github/` as source of truth. Do not directly hand-edit generated agent behavior in `claude/agents` unless you are intentionally creating a Claude-only override with documented rationale.
