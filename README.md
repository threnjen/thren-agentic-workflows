# github-agents-source-of-truth

A ready-to-use library of AI development agents, skills, and instructions that work
across Claude, Codex, OpenCode, Cursor, and GitHub Copilot. Everything is authored once
under `source_of_truth/`, transformed into per-harness variants under `ports/`, and
deployed into the real config directories each harness reads.

## Get Started

If you just want to use these agents in your own harness, install them with one command
from the repository root:

```bash
python3 deploy_agents.py
```

The first run asks which harnesses you use (Claude, Codex, OpenCode, Cursor, GitHub) and
remembers your choice. It only writes files this system generated — your hand-maintained
config is never touched.

**→ See [INSTALLATION.md](INSTALLATION.md) for full installation instructions, options,
and destinations.**

## What You Get

- **41 agents** — a full project workflow (planner, refiner, decomposer, phase executor),
  a feature implementation pipeline (implementer, reviewer, QA writer), PR review, audit
  orchestrators, test operations, and standalone helpers (docs writer, debugger, web
  researcher, and more).
- **24 skills** — directory-based capabilities agents load on demand.
- **15 instruction files** and **4 learnings files** — cross-cutting guidance applied by
  file-glob matching.

Only the destinations differ per harness; the agents behave the same everywhere.

## How It Works

The repository has two jobs, handled by two scripts:

1. **Transform** — `scripts/propagate_master_assets.py` reads `source_of_truth/`
   and regenerates platform-specific variants under `ports/{claude,codex,opencode,cursor}`.
   It also mirrors the source verbatim to `ports/github` and to a real `.github/`
   directory at the repository root (so GitHub Copilot reads the same source). This step
   is for maintainers editing the agents; end users can skip it.
2. **Deploy** — `deploy_agents.py` copies the generated `ports/` outputs out to the
   real user-level config directories each harness reads (`~/.claude`, `~/.codex`,
   `~/.config/opencode`, `~/.cursor`), and mirrors the `github` port into this
   repo's `.github/`. This is the step end users run.

Both steps are safe by construction: a destination file is only ever overwritten
or pruned when it positively carries a generated marker (or lives inside a
generated skill directory). Hand-maintained files are never touched.

## Current Inventory

- 41 source agent definitions under `source_of_truth/agents/` (39 `*.agent.md`
  plus `docs-writer.md` and `prod-code-review.md`, which are plain `.md` but still
  loaded as agents)
- 24 shared skills under `source_of_truth/skills/`
- 15 shared instruction files under `source_of_truth/instructions/`
- 4 learnings files under `source_of_truth/learnings/`
- A defunct prompt-injection scanner under `source_of_truth/hooks/` (retained,
  wired nowhere; see `source_of_truth/hooks/DEFUNCT.md`)

## Repository Structure

```text
.
├── AGENTS.md                       # Repo-specific code-review-graph MCP guidance
├── INSTALLATION.md                 # How to deploy the agents into your harness
├── README.md
├── source_of_truth/                # THE authoring surface — edit here
│   ├── agents/                     # 41 agent definitions + README (agent catalog)
│   ├── skills/                     # 24 skill directories, each rooted at SKILL.md
│   ├── instructions/               # 15 instruction files matched by applyTo globs
│   ├── learnings/                  # 4 shared learnings files
│   └── hooks/                      # Defunct prompt-injection scanner (inert)
├── ports/                          # Generated outputs — do not edit by hand
│   ├── claude/                     # agents, commands, skills, learnings
│   ├── codex/                      # agents, profiles, skills (TOML agents)
│   ├── opencode/                   # agents, skills
│   ├── cursor/                     # commands, rules (.mdc)
│   └── github/                     # verbatim mirror of the 5 source subdirs
├── .github/                        # Real mirror of ports/github (for Copilot)
├── scripts/
│   ├── propagate_master_assets.py  # Transform: source_of_truth/ -> ports/ + .github/
│   ├── asset_paths.py              # Shared markers + poll-watch primitives
│   ├── extract_pdfs.py             # Utility
│   └── setup-hook-symlinks.sh      # Utility
├── deploy_agents.py                # Deploy: ports/ -> real harness config dirs
├── docs/                           # ARCHITECTURE, CODEBASE_CONTEXT, LOCAL_DEVELOPMENT,
│                                   # TROUBLESHOOTING, porting/, inspiration/
├── eval/                           # Agent evaluation grader system and run artifacts
├── benchmarks/                     # Model cost/performance benchmark data
├── packages/                       # Distributable UPM package (visual-verification)
├── tests/                          # Python regression tests for both scripts
└── .vscode/tasks.json              # One-shot + watch tasks for propagate and deploy
```

## Platform Model

`source_of_truth/` is the only authoring surface. Everything under `ports/` and the
real `.github/` mirror are generated outputs.

| Surface | Role | Notes |
|---|---|---|
| `source_of_truth/` | Source of truth | Agents, skills, instructions, learnings, hooks authored here first. |
| `ports/claude/` | Generated output | Agents rewritten into Claude format with applicable instructions inlined; plus commands, skills, learnings. |
| `ports/codex/` | Generated output | TOML agents; skills. `profiles/` is generated but not deployed. |
| `ports/opencode/` | Generated output | Agents rewritten into OpenCode frontmatter/permission blocks; skills. |
| `ports/cursor/` | Generated output | User-invocable agents → `commands/*.md`; instructions/learnings → `rules/*.mdc`. |
| `ports/github/` | Generated mirror | Verbatim copy of the five source subdirs. |
| `.github/` | Deployed mirror | Real mirror of `ports/github` in this repo, for GitHub Copilot. |

## Prerequisites

- `python3` (standard library only — no third-party runtime dependencies)
- VS Code if you want the built-in watch tasks and Copilot agent picker
- Optional harness tooling depending on what you deploy to: Claude Code, Codex,
  OpenCode, Cursor, or GitHub Copilot

There is no application to build or serve. The maintenance loop is: edit
`source_of_truth/`, propagate, review the diff, deploy.

## Common Workflows

### Deploy the agents to your real harness directories (users)

```bash
python3 deploy_agents.py            # use saved selection, or prompt (tty) and save
python3 deploy_agents.py --harness claude,cursor
python3 deploy_agents.py --all
python3 deploy_agents.py --list     # show harnesses and resolved destinations
```

The first interactive run asks which harnesses you use and saves the choice to
`.deploy-config.json` (gitignored). Subsequent runs are just `python3 deploy_agents.py`.
Full details are in [INSTALLATION.md](INSTALLATION.md).

### Regenerate ports/ and .github/ from source (maintainers)

```bash
python3 scripts/propagate_master_assets.py --once
```

Runs one propagation pass to a fixed point (converges, then exits). Run this only if you
have edited files under `source_of_truth/`. In VS Code the equivalent task is
`propagate: master assets (once)`. The background task `watch: propagate master assets`
starts on folder open and re-propagates on every save under `source_of_truth/`.

See [docs/LOCAL_DEVELOPMENT.md](docs/LOCAL_DEVELOPMENT.md) for the full command
reference and [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for failure modes.

## Key Contents

### Agent system

`source_of_truth/agents/` contains 41 agent definitions following an orchestrator +
subagent pattern: the project planning pipeline (planner, refiner, decomposer, phase
executor), the feature implementation pipeline (plan expander, implementer, reviewer,
QA writer), PR Review orchestration and evaluators, evaluation agents, audit
orchestrators (code, infra, refactor), test operations, and standalone utility agents
(docs writer, debugger, evangelize, single-feature agent, prod code review, unity
reviewer, web researcher). See
[source_of_truth/agents/README.md](source_of_truth/agents/README.md) for the full
catalog and pipeline flow.

### Shared skills, instructions, and learnings

`source_of_truth/skills/` holds directory-based skills (each rooted at `SKILL.md`)
that agents load on demand. `source_of_truth/instructions/` holds instruction files
matched by `applyTo` globs — consumed directly by Copilot and transformed into inline
guidance or Cursor rules for other harnesses. `source_of_truth/learnings/` holds
cross-cutting learnings that propagate as learnings/rules.

### Distributable package

`packages/com.threnjen.visual-verification/` is a Unity UPM package for deterministic
screenshot capture, paired with the Visual Verifier agent.

## Related Documentation

- [INSTALLATION.md](INSTALLATION.md) — how to deploy the agents into your harness
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — components and the transform/deploy flow
- [docs/CODEBASE_CONTEXT.md](docs/CODEBASE_CONTEXT.md) — AI-oriented quick orientation
- [docs/LOCAL_DEVELOPMENT.md](docs/LOCAL_DEVELOPMENT.md) — setup, commands, testing
- [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) — non-obvious failures and fixes
- [docs/porting/README.md](docs/porting/README.md) — per-harness porting references
- [eval/EVAL_SYSTEM_USAGE.md](eval/EVAL_SYSTEM_USAGE.md) — grader workflows and run artifacts

## Acknowledgments

This repository once carried an original, clean-room hook system written from scratch
in stdlib Python. That system has been retired; git history is its archival record, and
a single prompt-injection scanner snapshot is retained under `source_of_truth/hooks/`
as an explicitly defunct, unrunnable artifact that is not part of the product and makes
no security claim. No code, pattern file, or prompt from any project below was ever
copied. They are credited because surveying them shaped that former design. Each survey
write-up lives in [docs/inspiration/](docs/inspiration/).

The now-retired hook work was informed by claudekit (carlrannaberg), claude-hooks
(Lasso Security), claude-code-hooks-mastery (IndyDevDan / disler), claude-workflow-v2 /
project-starter (CloudAI-X), buildwithclaude (davepoon),
claude-code-infrastructure-showcase, claude-code-hooks (shanraisshan), and ponytail
(Dietrich Gebert) — the last for multi-harness distribution from a single source of
truth: generated per-platform adapters, staleness-failing tests, and honest per-harness
support tiers.
