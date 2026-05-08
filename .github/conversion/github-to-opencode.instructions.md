# GitHub to OpenCode Conversion Standard

Source of truth is `.github/agents/*.agent.md` (and `.github/agents/*.md` when frontmatter declares `name` and `description`). OpenCode output is written to `opencode/agents/*.md`.

## Trigger Policy

Any save under these master folders triggers a full OpenCode propagation run:

- `.github/agents/`
- `.github/skills/`
- `.github/instructions/`

This ensures OpenCode output tracks both direct agent edits and indirect behavior changes from instructions/skills.

## Frontmatter Mapping

Output frontmatter format:

- `description: "..."`
- `deepseek/deepseek-v4-pro`
- `mode: subagent` when source has `user-invocable: false`
- `hidden: true` when source has `user-invocable: false`
- `permission:` object generated from source `tools`

## Permission Mapping

- `read` -> `permission.read: allow`
- `search` -> `permission.grep: allow`, `permission.glob: allow`
- `edit` -> `permission.edit: allow`
- `fetch` -> `permission.web_fetch: allow`
- `execute` -> `permission.bash: allow`
- `agent` -> `permission.task: allow`
- `todo` -> `permission.todowrite: allow`

## Instruction Inlining Rule

OpenCode does not support GitHub `applyTo` frontmatter routing.

For each source agent:

1. Resolve matching `.github/instructions/*.instructions.md` by `applyTo` glob.
2. Append resolved instruction bodies under `## Auto-Loaded Instructions` in the generated output.

## Filename Mapping Rule

Keep established OpenCode aliases:

- `documentation-architect` -> `docs-writer.md`
- `web-research-specialist` -> `web-researcher.md`
- `audit-code-or-infra` -> `audit-code-infra-refactor.md`

All other files map from source slug to `<slug>.md`.

## Canonical Generation Contract

- Never manually edit generated OpenCode agents.
- Always edit master files in `.github/`.
- Regenerate via `python3 scripts/propagate_master_assets.py --once` or the background watch task.
