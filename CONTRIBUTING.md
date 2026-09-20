# Contributing & Maintaining

This document is for people **editing the agents**, not deploying them. If you just want
to use the agents in your own harness, see [README.md](README.md) and
[INSTALLATION.md](INSTALLATION.md).

## The Authoring Model

Everything is authored **once** under `source_of_truth/`, transformed into per-harness
variants under `ports/`, and then deployed into the real config directories each harness
reads.

`source_of_truth/` is the only authoring surface. Everything under `ports/` and the real
`.github/` mirror are generated outputs — never hand-edit them. Neither is tracked.

The repository has two jobs. `deploy_agents.py` runs both, in order, on every run:

1. **Transform** — the propagator in `scripts/propagate_master_assets.py` reads
   `source_of_truth/` and regenerates platform-specific variants under
   `ports/{claude,codex,opencode,cursor}`. It also emits GitHub-native copies to
   `ports/github` and to a real `.github/` directory at the repository root (so GitHub
   Copilot reads the same source).
2. **Deploy** — `deploy_agents.py` copies the generated `ports/` outputs out to the real
   user-level config directories each harness reads (`~/.claude`, `~/.codex`,
   `~/.config/opencode`, `~/.cursor`), mirrors the `github` port into this repo's
   `.github/`, and then deletes `ports/`.

`ports/` exists only between those two steps. Run the propagator on its own when you want
to read the generated output, and give it `--target DIR` so the output lands somewhere a
deploy will not delete.

Both steps are safe by construction: a destination file is only ever overwritten or
pruned when it positively carries a generated marker (or lives inside a generated skill
directory). Hand-maintained files are never touched.

## What's in the Repo

- **59 agent definitions** in `source_of_truth/agents/` (all `*.agent.md`), of
  which **16 are user-invocable** and **50 are hidden subagents** (`user-invocable: false`)
  that orchestrators spawn automatically.
- **51 skills** — directory-based capabilities agents load on demand, each rooted at
  `SKILL.md`.
- **24 instruction files** — cross-cutting guidance applied by `applyTo` file-glob
  matching.

Only the destinations differ per harness; the agents behave the same everywhere.

## Repository Structure

```text
.
├── AGENTS.md                       # Repo-specific code-review-graph MCP guidance
├── INSTALLATION.md                 # How to deploy the agents into your harness
├── README.md                       # User-facing overview
├── CONTRIBUTING.md                 # This file
├── source_of_truth/                # THE authoring surface — edit here
│   ├── agents/                     # 59 agent definitions (catalog lives in USAGE.md)
│   ├── skills/                     # 51 skill directories, each rooted at SKILL.md
│   ├── instructions/               # 24 instruction files matched by applyTo globs
│   └── baseline/                   # baseline-instructions.md, rendered at deploy time
├── ports/                          # Generated landing zone — untracked, deleted after deploy
│   ├── claude/                     # agents, commands, skills
│   ├── codex/                      # agents, skills (TOML agents; profiles/ is a cleanup root)
│   ├── opencode/                   # agents, skills
│   ├── cursor/                     # agents, commands, rules (.mdc), skills
│   └── github/                     # GitHub-native mirror of the source subdirs
├── .github/                        # Real mirror of ports/github (for Copilot)
├── scripts/
│   ├── propagate_master_assets.py  # Transform: source_of_truth/ -> ports/ + .github/
│   ├── asset_paths.py              # Shared markers + poll-watch primitives (watch: propagator only)
│   └── extract_pdfs.py             # Utility
├── deploy_agents.py                # Propagate, deploy to harness config dirs, delete ports/
├── docs/                           # ARCHITECTURE, CODEBASE_CONTEXT, LOCAL_DEVELOPMENT,
│                                   # TROUBLESHOOTING, COPILOT_SETUP, porting/
├── eval/                           # Past benchmark run artifacts + deprecated/ (archived grader)
├── benchmarks/                     # Model cost/performance benchmark data
├── packages/                       # Distributable UPM package (com.threnjen.visual-verification)
├── dev/                            # gitignored local scratch; nothing tracked
└── tests/                          # Python regression tests for both scripts
```

## The Maintenance Loop

There is no application to build or serve. The loop is: edit `source_of_truth/`,
review the source diff, deploy.

### Deploy

```bash
python3 deploy_agents.py
```

Propagates, deploys, and deletes `ports/`. This is the only command most changes need.

### Read the generated output without deploying

```bash
python3 scripts/propagate_master_assets.py --target /tmp/inspect-ports
```

Runs one propagation pass to a fixed point against `/tmp/inspect-ports`, leaving this
repository untouched. Use this to check what a source edit produces. Omit `--target` to
propagate in place, and `--watch` to re-propagate on every save under `source_of_truth/`.

`.vscode/` is gitignored, so a fresh clone ships no editor tasks — the commands above are
the canonical interface. Wire up your own tasks if you want them on folder open.

The test suite propagates into a throwaway tree of its own, so it neither needs nor reads
a `ports/` directory in this repository.

## Key Contents

### Agent system

`source_of_truth/agents/` follows an orchestrator + subagent pattern: the project
planning pipeline (planner, refiner, decomposer, phase executor), the feature
implementation pipeline (plan expander, implementer, reviewer, QA writer, QA runner), Local Final Checks
orchestration and evaluators, the audit orchestrator and its auditors
(code, infra, refactor, security, delta, remediation research, remediation
reconciler), the Client Deliverable
engagement fleet, QA bootstrapping, test operations, and standalone utility agents
(docs writer, debugger, single-feature agent, unity reviewer, web
researcher). See
[USAGE.md](USAGE.md) for the full catalog
and pipeline flow.

### Shared skills and instructions

`source_of_truth/skills/` holds directory-based skills (each rooted at `SKILL.md`) that
agents load on demand. `source_of_truth/instructions/` holds instruction files matched by
`applyTo` globs — consumed directly by Copilot and transformed into inline guidance or
Cursor rules for other harnesses.

There is no learnings asset here. Durable, repo-agnostic rules are skills. A working
repository's own findings live in its `docs/learnings/`, written by the agents working
there and never seeded from this repository.

An instruction's `applyTo` globs are matched with `fnmatch` against each agent's
repo-relative path, so `**/name.agent.md` only matches when a `/` immediately precedes
`name`. A numbered agent must be named in full (`**/03b-feature-implementer.agent.md`); a
pattern that matches nothing fails silently.

### Distributable package

`packages/com.threnjen.visual-verification/` is a Unity UPM package for deterministic
screenshot capture. No pipeline stage invokes it.

## Related Documentation

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — components and the transform/deploy flow
- [docs/CODEBASE_CONTEXT.md](docs/CODEBASE_CONTEXT.md) — AI-oriented quick orientation
- [docs/LOCAL_DEVELOPMENT.md](docs/LOCAL_DEVELOPMENT.md) — setup, commands, testing
- [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) — non-obvious failures and fixes
- [docs/porting/README.md](docs/porting/README.md) — per-harness porting references
- [eval/deprecated/README.md](eval/deprecated/README.md) — the archived eval-grader system,
  why it was retired, and what reactivating it would require
