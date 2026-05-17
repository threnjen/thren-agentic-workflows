# Codebase Context

Quick-reference for AI agents working in this repository.

## What This Repo Is

- Source-of-truth repository for multi-harness agent assets.
- Primary authoring surface is `.github/`.
- Derived or related platform surfaces are `claude/`, `opencode/`, `codex/`, and `.codex/`.
- Includes copyable template packs for Node.js and Python projects.
- Mostly Markdown plus one maintenance script: `scripts/propagate_master_assets.py`.
- No root `package.json`, `pyproject.toml`, or automated test suite.

## Current Counts

- 25 source agent definitions in `.github/agents/`.
- 14 skills in `.github/skills/`.
- 15 instructions in `.github/instructions/`.
- 2 template packs: `nodejs/` and `python/`.

## Key Paths

```text
AGENTS.md                                  # Repo-specific graph/MCP workflow guidance
HARNESS_SETUP.md                           # How to expose repo assets to Copilot, Claude, and OpenCode
.mcp.json                                  # Registers code-review-graph MCP with uvx
.codex/config.toml                         # Repo-scoped Codex runtime MCP config
.github/
  agents/
    README.md                              # Full agent catalog and pipeline docs
    *.agent.md                             # Most source agents
    prod-code-review.md                    # Plain .md agent definition; still part of source set
  instructions/                            # 15 shared instruction files with applyTo globs
  skills/                                  # 14 shared skill directories with SKILL.md entrypoints
claude/agents/                             # Generated Claude copies
opencode/agents/                           # Generated OpenCode copies
codex/
  agents/                                  # Generated Codex TOML agents
  instructions/                            # Repo-owned Codex instruction source material
  *.md                                     # Codex platform and porting docs
docs/
  ARCHITECTURE.md
  CODEBASE_CONTEXT.md
  LOCAL_DEVELOPMENT.md
  TROUBLESHOOTING.md
  porting/README.md
eval/
  EVAL_SYSTEM_USAGE.md
  EVAL_GRADER_SCORE_HISTORY.md
nodejs/
  AGENTS.md
  docs/STYLE_GUIDE.md
python/
  AGENTS.md
  docs/STYLE_GUIDE.md
scripts/
  propagate_master_assets.py               # Master propagation entry point
.vscode/tasks.json                         # One-shot and watch propagation tasks
```

## Propagation Model

- Edit `.github/agents/`, `.github/skills/`, or `.github/instructions/` first.
- Regenerate downstream outputs with `python3 scripts/propagate_master_assets.py --once`.
- The VS Code task `watch: propagate master assets` runs `--watch` and is configured to start on folder open.
- Generated targets are:
  - `claude/agents/`
  - `opencode/agents/`
  - `codex/agents/`

## Important Script Facts

- `load_source_agents()` reads any `.github/agents/*.md` file with `name` and `description` frontmatter.
- Source agent detection is not limited to `.agent.md`; that is why `prod-code-review.md` still propagates.
- The script watches three directories: `.github/agents`, `.github/skills`, and `.github/instructions`.
- Claude and OpenCode outputs preserve existing filename aliases when present.
- Known aliases include:
  - `documentation-architect` -> `docs-writer`
  - `web-research-specialist` -> `web-researcher`
  - `audit-code-or-infra` -> `audit-code-infra-refactor`
- Hidden agents are renamed for some targets:
  - Claude uses `z-` filenames for non-user-invocable subagents.
  - Codex uses `z-` in both filename and TOML `name`.

## Agent Topology

- 3 orchestrators: `04 Phase - Execute`, `Audit - Code, Infra, Refactor`, `Test - Orchestrator`.
- 11 standalone user-facing agents: planner, refiner, decomposer, eval grader, documentation architect, debugger, evangelize, single-feature agent, prod code review, unity reviewer, web research specialist.
- 11 hidden subagents: plan expander, implementer, reviewer, QA writer, 3 auditors, eval metric grader, test analyst, test writer, test fixer.

## Template Pack Facts

- `nodejs/AGENTS.md` and `python/AGENTS.md` are meant to be copied into another repo's root as `AGENTS.md`.
- Each template expects a sibling `docs/STYLE_GUIDE.md` in the destination repository.
- The two template packs intentionally share structure but differ on ecosystem-specific tooling and style guidance.
- Do not introduce inheritance or a shared base file for the template packs.

## Platform Surface Rules

- `.github/` is the only shared source-of-truth for agents, skills, and instructions.
- `claude/` and `opencode/` are generated outputs, not normal authoring surfaces.
- `codex/` is a repository-owned Codex area; `.codex/` is runtime configuration.
- Do not treat `codex/` as if it were the live runtime install path.
- Code-review-graph MCP is configured in both `.mcp.json` and `.codex/config.toml` via `uvx code-review-graph serve`.

## Authoring Boundary

- When the task is about agent definitions, instruction files, skill content, or agent behavior in this repo, constrain discovery and edits to:
  - `.github/agents/`
  - `.github/instructions/`
  - `.github/skills/`
- Treat `claude/`, `opencode/`, and `codex/` as downstream or platform-specific outputs for those tasks.
- Ignore those downstream directories during normal discovery and editing unless the assigned role is `Evangelize` or the user explicitly asks for propagation debugging or output verification.
- Make the logical change in `.github/` first; do not mirror the same change manually into generated outputs.

## File Relationships

- `.github/agents/README.md` must stay in sync with the actual source agent set.
- `docs/ARCHITECTURE.md` and this file should be updated when counts, directories, or propagation rules change.
- `HARNESS_SETUP.md` is the canonical setup reference for multi-root VS Code and non-Copilot harness linking.
- `docs/porting/README.md` is the neutral index for porting docs.
- `codex/README.md` defines the separation between repository-owned Codex content and runtime `.codex/` content.

## Editing Guidance

- When changing shared agent behavior, edit `.github/` first and rerun propagation.
- When the task is about agent, instruction, or skill behavior, do not widen discovery into `claude/`, `opencode/`, or `codex/` unless the task is explicitly about porting or generated-output verification.
- When adding or removing an agent, update both `.github/agents/README.md` and the standard docs.
- When adding a skill or instruction, update the relevant counts and documentation references.
- When documenting commands, prefer the existing `python3 scripts/propagate_master_assets.py --once` and `--watch` entry points.

## Do Not

- Do not assume this repo is Markdown-only; the propagation script is part of the maintenance flow.
- Do not edit generated Claude, OpenCode, or Codex agents first unless you are intentionally repairing generation output.
- Do not search `claude/`, `opencode/`, or `codex/` to decide how source agent, instruction, or skill behavior should change; decide that from `.github/`.
- Do not assume filename parity across platforms; aliases and `z-` prefixes are intentional.
- Do not document a root `dev/` directory as if it exists in this repo.
- Do not treat `prod-code-review.md` as non-agent content just because it lacks the `.agent.md` suffix.
- Do not add deployment or CI/CD runbooks to the standard docs.
