# github-agents-source-of-truth

Source-of-truth templates, agent definitions, and porting references for a multi-harness AI development workflow.

This repository has three main jobs:

1. Provide copyable `AGENTS.md` and `docs/STYLE_GUIDE.md` templates for Node.js and Python projects.
2. Maintain the master `.github/` agent system used by GitHub Copilot.
3. Regenerate derived agent outputs for Claude, OpenCode, and Codex from that master source.

## Overview

The repository is documentation-heavy, but it is not purely static. Most files are Markdown, and one maintenance script, `scripts/propagate_master_assets.py`, keeps the generated platform variants aligned with the `.github/` source-of-truth.

Current inventory:

- 43 source agent definitions under `.github/agents/`
- 16 shared skills under `.github/skills/`
- 15 shared instruction files under `.github/instructions/`
- 2 copyable language template sets under `nodejs/` and `python/`

## Repository Structure

```text
.
├── AGENTS.md                         # Repo-specific graph/MCP guidance for contributors
├── README.md
├── HARNESS_SETUP.md                  # Harness-specific setup and linking instructions
├── .github/
│   ├── agents/                       # Master Copilot agent definitions and agent README
│   ├── instructions/                 # Shared instruction files matched by applyTo globs
│   └── skills/                       # Shared skill directories with SKILL.md entrypoints
├── claude/
│   ├── agents/                       # Generated Claude-formatted agent copies
│   ├── skills/                       # Symlinked to .github/skills/
│   └── README.md
├── opencode/
│   ├── agents/                       # Generated OpenCode-formatted agent copies
│   └── OPENCODE_PORTING_GUIDE.md
├── codex/
│   ├── agents/                       # Generated Codex TOML agents
│   ├── instructions/                 # Repo-owned Codex source material
│   └── *.md                          # Codex platform reference and porting docs
├── .codex/
│   ├── config.toml                   # Repo-scoped Codex runtime config
│   └── hooks.json
├── docs/
│   ├── ARCHITECTURE.md
│   ├── CODEBASE_CONTEXT.md
│   ├── LOCAL_DEVELOPMENT.md
│   ├── TROUBLESHOOTING.md
│   └── porting/                      # Cross-platform mapping/index docs
├── eval/
│   ├── EVAL_SYSTEM_USAGE.md
│   ├── EVAL_GRADER_SCORE_HISTORY.md
│   ├── rubrics/
│   └── runs/
├── nodejs/                           # Copyable Node.js/TypeScript template set
│   ├── AGENTS.md
│   └── docs/STYLE_GUIDE.md
├── python/                           # Copyable Python template set
│   ├── AGENTS.md
│   └── docs/STYLE_GUIDE.md
├── packages/                         # Distributable packages consumed by other repos
│   └── com.threnjen.visual-verification/  # Unity UPM package: deterministic screenshot capture (paired with the Visual Verifier agent)
├── scripts/
│   └── propagate_master_assets.py    # Regenerates claude/, opencode/, and codex/agents/
└── .vscode/tasks.json                # One-shot and watch tasks for propagation
```

## Platform Model

`.github/` is the master authoring surface. The other platform directories are downstream outputs or platform-specific reference areas.

| Surface | Role | Notes |
|---|---|---|
| `.github/` | Source of truth | Copilot agents, skills, and instructions are authored here first. |
| `claude/` | Generated output | Agent content is rewritten into Claude format, with applicable instructions inlined. |
| `opencode/` | Generated output | Agent content is rewritten into OpenCode frontmatter and permission blocks. |
| `codex/` | Repo-owned Codex surface | Holds Codex docs and generated TOML agents; distinct from runtime `.codex/`. |
| `.codex/` | Runtime config surface | Repo-scoped Codex runtime configuration, not authoring source. |

## Prerequisites

- `python3` available in your shell for the propagation script
- VS Code if you want the built-in watch task and Copilot agent picker workflow
- Optional harness tooling depending on what you are validating: GitHub Copilot, Claude Code, OpenCode, or Codex

There is no `package.json`, `pyproject.toml`, or project test suite at the repo root. The normal maintenance loop is editing Markdown and agent manifests, then rerunning propagation.

## Common Workflows

### Update source-of-truth agents and regenerate derived outputs

```bash
python3 scripts/propagate_master_assets.py --once
```

In VS Code, the equivalent task is `propagate: master assets (once)`. A background task, `watch: propagate master assets`, is configured to start on folder open and keep generated outputs current while you edit `.github/agents/`, `.github/skills/`, or `.github/instructions/`.

### Copy a language template into another repository

```bash
# Node.js / TypeScript
cp nodejs/AGENTS.md /path/to/project/AGENTS.md
cp nodejs/docs/STYLE_GUIDE.md /path/to/project/docs/STYLE_GUIDE.md

# Python
cp python/AGENTS.md /path/to/project/AGENTS.md
cp python/docs/STYLE_GUIDE.md /path/to/project/docs/STYLE_GUIDE.md
```

After copying, customize the files for the destination codebase rather than treating them as locked templates.

### Work with the full GitHub Copilot agent system

Use the `.github/agents/`, `.github/skills/`, and `.github/instructions/` directories together. For multi-root VS Code setup and non-Copilot harness linking, see [HARNESS_SETUP.md](HARNESS_SETUP.md).

## Key Contents

### Language templates

The `nodejs/` and `python/` folders each contain:

- `AGENTS.md` for workflow and coding-behavior guidance
- `docs/STYLE_GUIDE.md` for the detailed language conventions that the template points to

### Agent system

`.github/agents/` contains 43 source agent definitions following an orchestrator plus subagent pattern. These include the project planning pipeline (planner, refiner, decomposer, phase executor), the feature implementation pipeline (plan expander, implementer, reviewer, QA writer), Phase Final Review orchestration and evaluators, evaluation agents (eval grader, eval decomposition reporter, eval metric grader, eval score recorder), audit orchestrators (code, infra, refactor), test operations (test orchestrator, analyst, writer, fixer), and standalone utility agents (documentation architect, debugger, evangelize, single-feature agent, prod code review, unity reviewer, web researcher). Most source agent files use the `.agent.md` suffix; `prod-code-review.md` is an intentional exception and is still treated as an agent definition by the propagation script.

See [.github/agents/README.md](.github/agents/README.md) for agent-by-agent descriptions and pipeline flow.

### Shared skills and instructions

`.github/skills/` contains reusable skill directories that agents load on demand.

`.github/instructions/` contains shared instruction files matched by `applyTo` globs. These are consumed directly by Copilot and transformed into inline guidance for generated Claude and Codex outputs.

### Propagation tooling

`scripts/propagate_master_assets.py` reads the `.github/` master content, applies platform-specific filename aliases and tool mapping rules, and updates:

- `claude/agents/`
- `opencode/agents/`
- `codex/agents/`

For agent, instruction, and skill changes in this repository, `.github/` is the only authoring surface. The downstream `claude/`, `opencode/`, and `codex/` directories are synchronized from there and should not be edited manually except during intentional porting work.

## Related Documentation

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for component relationships and propagation flow
- [docs/CODEBASE_CONTEXT.md](docs/CODEBASE_CONTEXT.md) for AI-oriented quick orientation
- [docs/LOCAL_DEVELOPMENT.md](docs/LOCAL_DEVELOPMENT.md) for setup and maintenance commands
- [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for non-obvious setup and propagation failures
- [docs/porting/README.md](docs/porting/README.md) for the porting docs index
- [eval/EVAL_SYSTEM_USAGE.md](eval/EVAL_SYSTEM_USAGE.md) for grader workflows and run artifacts
