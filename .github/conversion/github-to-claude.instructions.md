# GitHub to Claude Conversion Standard

Source of truth is `.github/agents/*.agent.md` (and `.github/agents/*.md` when frontmatter declares `name` and `description`). Claude output is written to `claude/agents/*.md`.

## Trigger Policy

Any save under these master folders triggers a full Claude propagation run:

- `.github/agents/`
- `.github/skills/`
- `.github/instructions/`

Even when the edited file is not an agent, rerun propagation because instruction and skill changes alter effective agent behavior.

## Frontmatter Mapping

Input frontmatter (GitHub):

- `name`
- `description`
- `tools: [read, search, edit, fetch, execute, agent, todo]`
- optional: `agents`, `user-invocable`

Output frontmatter (Claude):

- `name: <kebab-case slug>`
- `description: <same description text>`
- `tools: Skill, Read, Grep, Glob, Edit, Write, WebFetch, Bash, Agent` (generated from source tools)

## Tool Mapping

- `read` -> `Read`
- `search` -> `Grep`, `Glob`
- `edit` -> `Edit`, `Write`
- `fetch` -> `WebFetch`
- `execute` -> `Bash`
- `agent` -> `Agent`
- `todo` -> dropped (no Claude equivalent)

`Skill` is always included so skill loading remains available.

## Instruction Inlining Rule

Claude does not support `applyTo`-based instruction loading from `.github/instructions/`.

For each source agent:

1. Evaluate every `.github/instructions/*.instructions.md` `applyTo` pattern against the source agent path.
2. Collect every matching instruction document body.
3. Append those bodies to the generated Claude agent under `## Auto-Loaded Instructions`.

This keeps Claude behavior aligned with GitHub behavior.

## Subagent Naming Rule

When source `user-invocable: false` and no existing Claude filename mapping exists, generate a `z-` prefixed Claude filename.

## Canonical Generation Contract

- Never manually edit generated Claude agents.
- Always edit master files in `.github/`.
- Regenerate via `python3 scripts/propagate_master_assets.py --once` or the background watch task.
