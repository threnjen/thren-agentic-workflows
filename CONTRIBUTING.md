# Contributing & Maintaining

This document is for people **editing the agents**, not deploying them. If you just want
to use the agents in your own harness, see [README.md](README.md) and
[INSTALLATION.md](INSTALLATION.md).

## The Authoring Model

Everything is authored **once** under `source_of_truth/`, transformed into per-harness
variants under `ports/`, and then deployed into the real config directories each harness
reads.

`source_of_truth/` is the only authoring surface. Everything under `ports/` and the real
`.github/` mirror are generated outputs — never hand-edit them.

The repository has two jobs, handled by two scripts:

1. **Transform** — `scripts/propagate_master_assets.py` reads `source_of_truth/` and
   regenerates platform-specific variants under `ports/{claude,codex,opencode,cursor}`.
   It also mirrors the source verbatim to `ports/github` and to a real `.github/`
   directory at the repository root (so GitHub Copilot reads the same source). This step
   is for maintainers editing the agents; end users can skip it.
2. **Deploy** — `deploy_agents.py` copies the generated `ports/` outputs out to the real
   user-level config directories each harness reads (`~/.claude`, `~/.codex`,
   `~/.config/opencode`, `~/.cursor`), and mirrors the `github` port into this repo's
   `.github/`. This is the step end users run.

Both steps are safe by construction: a destination file is only ever overwritten or
pruned when it positively carries a generated marker (or lives inside a generated skill
directory). Hand-maintained files are never touched.

## What's in the Repo

- **54 agent definitions** in `source_of_truth/agents/` (50 `*.agent.md` plus the plain
  `auditor.md`, `delta-auditor.md`, `docs-writer.md`, and `04f-prod-code-review.md`), of
  which **15 are user-invocable** and **38 are hidden subagents** (`user-invocable: false`)
  that orchestrators spawn automatically.
- **34 skills** — directory-based capabilities agents load on demand, each rooted at
  `SKILL.md`.
- **16 instruction files** — cross-cutting guidance applied by `applyTo` file-glob
  matching.
- **4 learnings files** — seed rule sets that ship into a target repo and grow there as
  agents append what they learn.

Only the destinations differ per harness; the agents behave the same everywhere.

## Repository Structure

```text
.
├── AGENTS.md                       # Repo-specific code-review-graph MCP guidance
├── INSTALLATION.md                 # How to deploy the agents into your harness
├── README.md                       # User-facing overview
├── CONTRIBUTING.md                 # This file
├── source_of_truth/                # THE authoring surface — edit here
│   ├── agents/                     # 54 agent definitions (catalog lives in USAGE.md)
│   ├── skills/                     # 34 skill directories, each rooted at SKILL.md
│   ├── instructions/               # 16 instruction files matched by applyTo globs
│   └── learnings/                  # 4 seed learnings files
├── ports/                          # Generated outputs — do not edit by hand
│   ├── claude/                     # agents, commands, skills, learnings
│   ├── codex/                      # agents, profiles, skills, learnings (TOML agents)
│   ├── opencode/                   # agents, skills
│   ├── cursor/                     # commands, rules (.mdc)
│   └── github/                     # verbatim mirror of the source subdirs
├── .github/                        # Real mirror of ports/github (for Copilot)
├── scripts/
│   ├── propagate_master_assets.py  # Transform: source_of_truth/ -> ports/ + .github/
│   ├── asset_paths.py              # Shared markers + poll-watch primitives
│   └── extract_pdfs.py             # Utility
├── deploy_agents.py                # Deploy: ports/ -> real harness config dirs
├── docs/                           # ARCHITECTURE, CODEBASE_CONTEXT, LOCAL_DEVELOPMENT,
│                                   # TROUBLESHOOTING, COPILOT_SETUP, porting/
├── eval/                           # Past benchmark run artifacts + deprecated/ (archived grader)
├── benchmarks/                     # Model cost/performance benchmark data
├── packages/                       # Distributable UPM package (com.threnjen.visual-verification)
├── dev/                            # inspiration/ write-ups; pr-review/ fixtures
└── tests/                          # Python regression tests for both scripts
```

## The Maintenance Loop

There is no application to build or serve. The loop is: edit `source_of_truth/`,
propagate, review the diff, deploy.

### Regenerate ports/ and .github/ from source

```bash
python3 scripts/propagate_master_assets.py --once
```

Runs one propagation pass to a fixed point (converges, then exits). Run this only if you
have edited files under `source_of_truth/`. Use `--watch` instead to re-propagate on
every save under `source_of_truth/`.

`.vscode/` is gitignored, so a fresh clone ships no editor tasks — the two commands above
are the canonical interface. Wire up your own tasks if you want them on folder open.

The test suite (`tests/test_propagate_master_assets.py`) fails when source and generated
outputs drift; a sync failure means "rerun propagation," not "edit the output."

## Key Contents

### Agent system

`source_of_truth/agents/` follows an orchestrator + subagent pattern: the project
planning pipeline (planner, refiner, decomposer, phase executor), the feature
implementation pipeline (plan expander, implementer, reviewer, QA writer), PR Review
orchestration and evaluators, the audit orchestrator and its auditors
(code, infra, refactor, security, delta, remediation research, remediation
reconciler), the Client Deliverable
engagement fleet, QA bootstrapping, test operations, and standalone utility agents
(docs writer, debugger, single-feature agent, unity reviewer, visual verifier, web
researcher). See
[USAGE.md](USAGE.md) for the full catalog
and pipeline flow.

### Shared skills, instructions, and learnings

`source_of_truth/skills/` holds directory-based skills (each rooted at `SKILL.md`) that
agents load on demand. `source_of_truth/instructions/` holds instruction files matched by
`applyTo` globs — consumed directly by Copilot and transformed into inline guidance or
Cursor rules for other harnesses.

`source_of_truth/learnings/` holds four seed files of durable, repo-agnostic rules —
review patterns, cross-phase conventions, project traps, and debugging root causes. They
reach a working repository through its `.github/learnings/` directory (and as Cursor
agent-requested rules), where agents both read them and append newly learned rules. Keep
what is authored here general: anything specific to one repository belongs in that
repository's copy, not in the seed.

An instruction's `applyTo` globs are matched with `fnmatch` against each agent's
repo-relative path, so `**/name.agent.md` only matches when a `/` immediately precedes
`name`. A numbered agent must be named in full (`**/04b-feature-implementer.agent.md`); a
pattern that matches nothing fails silently.

### Distributable package

`packages/com.threnjen.visual-verification/` is a Unity UPM package for deterministic
screenshot capture, paired with the Visual Verifier agent.

## Related Documentation

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — components and the transform/deploy flow
- [docs/CODEBASE_CONTEXT.md](docs/CODEBASE_CONTEXT.md) — AI-oriented quick orientation
- [docs/LOCAL_DEVELOPMENT.md](docs/LOCAL_DEVELOPMENT.md) — setup, commands, testing
- [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) — non-obvious failures and fixes
- [docs/porting/README.md](docs/porting/README.md) — per-harness porting references
- [eval/deprecated/README.md](eval/deprecated/README.md) — the archived eval-grader system,
  why it was retired, and what reactivating it would require
