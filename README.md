# github-agents-source-of-truth

Source-of-truth templates, agent definitions, and porting references for a multi-harness AI development workflow.

This repository has three main jobs:

1. Provide copyable `AGENTS.md` and `docs/STYLE_GUIDE.md` templates for Node.js and Python projects.
2. Maintain the master `.github/` agent system used by GitHub Copilot.
3. Regenerate derived agent outputs for Claude, OpenCode, and Codex from that master source, then optionally deploy them as reviewed user-global managed copies.

## Overview

The repository is documentation-heavy, but it is not purely static. Most files are
Markdown; Python tooling under `scripts/` keeps generated platform variants aligned
with the `.github/` source of truth and performs reviewed managed-copy deployment.

Current inventory:

- 41 source agent definitions under `.github/agents/`
- 24 shared skills under `.github/skills/`
- 15 shared instruction files under `.github/instructions/`
- 2 copyable language template sets under `nodejs/` and `python/`

## Repository Structure

```text
.
├── AGENTS.md                         # Repo-specific graph/MCP guidance for contributors
├── README.md
├── HARNESS_SETUP.md                  # Cross-harness managed-copy deployment guidance
├── .github/
│   ├── agents/                       # Master Copilot agent definitions and agent README
│   ├── instructions/                 # Shared instruction files matched by applyTo globs
│   └── skills/                       # Shared skill directories with SKILL.md entrypoints
├── claude/
│   ├── agents/                       # Generated Claude-formatted agent copies
│   ├── skills/                       # Generated copies from .github/skills/
│   └── README.md
├── opencode/
│   └── agents/                       # Generated OpenCode-formatted agent copies
├── codex/
│   ├── agents/                       # Generated Codex TOML agents
│   ├── instructions/                 # Repo-owned Codex source material
│   └── *.md                          # Codex platform reference and pilot-slice history (porting guide lives in docs/porting/)
├── .codex/
│   ├── config.toml                   # Repo-scoped Codex runtime config
│   └── hooks.json                  # Static hand-owned Codex notify/graph hooks (not propagated)
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
│   ├── propagate_master_assets.py    # Regenerates platform outputs and orchestrates optional runtime deployment
│   └── runtime_deployment.py         # Destination, inventory, managed-copy, and reconciliation logic
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

Use the `.github/agents/`, `.github/skills/`, and `.github/instructions/` directories together. For multi-root VS Code setup and managed-copy deployment to non-Copilot harnesses, see [HARNESS_SETUP.md](HARNESS_SETUP.md).

## Key Contents

### Language templates

The `nodejs/` and `python/` folders each contain:

- `AGENTS.md` for workflow and coding-behavior guidance
- `docs/STYLE_GUIDE.md` for the detailed language conventions that the template points to

### Agent system

`.github/agents/` contains 41 source agent definitions following an orchestrator plus subagent pattern. These include the project planning pipeline (planner, refiner, decomposer, phase executor), the feature implementation pipeline (plan expander, implementer, reviewer, QA writer), PR Review orchestration and evaluators, evaluation agents (eval grader, eval decomposition reporter, eval metric grader, eval score recorder), audit orchestrators (code, infra, refactor), test operations (test orchestrator, analyst, writer, fixer), and standalone utility agents (documentation architect, debugger, evangelize, single-feature agent, prod code review, unity reviewer, web researcher). Most source agent files use the `.agent.md` suffix; `prod-code-review.md` and `docs-writer.md` are intentional exceptions and are still treated as agent definitions by the propagation script.

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

After repository outputs converge, `--runtime-deploy --active-home <path>` can produce
a content-bound deployment inventory for Claude, Codex, and OpenCode. Runtime mutation
requires the reviewed inventory digest and watcher-restart confirmation. The deployment
uses regular managed copies, preserves foreign collisions, and reconciles only harnesses
whose copy stage succeeds. See [HARNESS_SETUP.md](HARNESS_SETUP.md) for the canonical
reviewed workflow; do not substitute ad hoc links or copy commands.

## Related Documentation

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for component relationships and propagation flow
- [docs/CODEBASE_CONTEXT.md](docs/CODEBASE_CONTEXT.md) for AI-oriented quick orientation
- [docs/LOCAL_DEVELOPMENT.md](docs/LOCAL_DEVELOPMENT.md) for setup and maintenance commands
- [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for non-obvious setup and propagation failures
- [docs/porting/README.md](docs/porting/README.md) for the porting docs index
- [eval/EVAL_SYSTEM_USAGE.md](eval/EVAL_SYSTEM_USAGE.md) for grader workflows and run artifacts

## Acknowledgments

This repository once carried an original, clean-room hook system written from
scratch in stdlib Python. That hook system has since been retired; git history is
its archival record, and a single prompt-injection scanner snapshot is retained
under `.github/hooks/` as an explicitly defunct, unrunnable artifact that is not
part of the product and makes no security claim. No code, pattern file, or prompt
from any project below was ever copied. They are credited because surveying them
shaped that former design: which lifecycle events were worth hooking, which
failure modes mattered, and which enforcement tiers a guard needed to be useful
rather than merely noisy. Each survey write-up lives in
[docs/inspiration/](docs/inspiration/).

The now-retired hook work was informed by:

- **[claudekit](URL)** (carlrannaberg) — ignore-file-driven blocking of
  sensitive-file access, and the insight that a guard must parse bash commands to
  catch indirect reads rather than only inspecting file-tool arguments.
- **[claude-hooks](URL)** (Lasso Security) — prompt-injection defense belongs at
  PostToolUse, treating tool output as untrusted input before the model sees it.
- **[claude-code-hooks-mastery](URL)** (IndyDevDan / disler) — the baseline
  hazard set for a pre-tool guard: environment-file reads and destructive
  recursive deletes.
- **[claude-workflow-v2 / project-starter](URL)** (CloudAI-X) — blocking writes
  that carry secrets, as a write-side complement to read-side protection.
- **[buildwithclaude](URL)** (davepoon) — Stop-time gating of unverified
  completion claims, the idea that "done" is a claim a hook can hold to evidence.
- **[claude-code-infrastructure-showcase](URL)** — deterministic skill
  activation driven by a rules file, instead of relying on model judgment.
- **[claude-code-hooks](URL)** (shanraisshan) — the most complete catalog of
  hook events available, used to choose which events to attach to.
- **[ponytail](URL)** (Dietrich Gebert) — multi-harness distribution from a
  single source of truth: generated per-platform adapters, staleness-failing
  tests, and honest per-harness support tiers.
