# GitHub to Codex Conversion Standard

Source of truth is `.github/agents/*.agent.md` (and `.github/agents/*.md` when frontmatter declares `name` and `description`). Codex output is written as TOML files to `codex/agents/*.toml`.

## Trigger Policy

Any save under these master folders triggers a full Codex propagation run:

- `.github/agents/`
- `.github/skills/`
- `.github/instructions/`

Codex generation reruns on all three because effective instructions can change when instructions/skills change.

## TOML Output Contract

Each generated Codex agent file must include:

- `name = "..."`
- `description = "..."`
- `developer_instructions = """..."""`

`name` should be a kebab-case slug based on source agent slug with leading phase prefixes removed where applicable (example: `01-project-planner` -> `project-planner`).

## Content Assembly Rule

`developer_instructions` is composed from:

1. Source GitHub agent body content.
2. Matching instruction docs resolved from `.github/instructions/*.instructions.md` using `applyTo` patterns.
3. A section header `## Auto-Loaded Instructions` followed by matched instruction bodies.

This keeps Codex behavior deterministic and self-contained.

## Tool Semantics Rule

Codex agent TOML generation does not directly copy GitHub `tools` arrays.

Tool behavior should be represented in natural-language `developer_instructions` and any future Codex-specific fields can be added in a later migration phase if needed.

## Canonical Generation Contract

- Never manually edit generated Codex TOML files.
- Always edit master files in `.github/`.
- Regenerate via `python3 scripts/propagate_master_assets.py --once` or the background watch task.
