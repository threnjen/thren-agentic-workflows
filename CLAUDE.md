# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

A library of AI development agents (planning, implementation, review, testing, auditing, docs) deployed across five harnesses: Claude Code, Codex, OpenCode, Cursor, and GitHub Copilot. There is no application to build or serve — the workflow is: edit source, propagate, review the diff, deploy.

## The One Rule That Matters

**`source_of_truth/` is the only authoring surface.** Everything under `ports/` and the real `.github/` directory is generated output — never hand-edit them. If generated output looks wrong, fix the source and re-propagate. A sync-test failure means "rerun propagation," not "edit the output."

## Commands

```bash
# Transform: regenerate ports/ and .github/ from source_of_truth/
python3 scripts/propagate_master_assets.py --once

# Watch mode: re-propagate on every save under source_of_truth/
python3 scripts/propagate_master_assets.py --watch

# Deploy generated ports/ to real harness config dirs (~/.claude, ~/.codex, etc.)
python3 deploy_agents.py                     # uses saved selection in .deploy-config.json
python3 deploy_agents.py --harness claude,cursor
python3 deploy_agents.py --list              # show harnesses and resolved destinations
python3 deploy_agents.py --skip-tools        # skip companion-tool bootstrap

# Tests (pytest is a dev dep, not in the base interpreter)
uv run pytest tests/
uv run pytest tests/test_propagate_master_assets.py            # one file
uv run pytest tests/test_deploy_assets.py -k <test_name>       # one test
```

No third-party runtime dependencies — both scripts are stdlib-only Python.

## Architecture

Two-stage pipeline, two scripts:

1. **Transform** — `scripts/propagate_master_assets.py` reads `source_of_truth/{agents,skills,instructions,learnings}` and regenerates per-harness variants under `ports/{claude,codex,opencode,cursor}` (Claude/OpenCode markdown agents, Codex TOML agents + profiles, Cursor `.mdc` rules/commands). It also mirrors the source verbatim to `ports/github` and the real `.github/` (read by Copilot). Runs to a fixed point; prints a JSON convergence summary — a second run reporting zero changes confirms convergence. `scripts/asset_paths.py` holds shared markers and watch primitives.

2. **Deploy** — `deploy_agents.py` (repo root, not `scripts/`) copies `ports/` outputs into the real harness config dirs (`~/.claude`, `~/.codex` + `~/.agents/skills`, `~/.config/opencode`, `~/.cursor`; env overrides `CLAUDE_CONFIG_DIR`, `CODEX_HOME`, `OPENCODE_CONFIG_DIR`). It also splices a baseline instructions file per harness (rendered from `source_of_truth/baseline/baseline-instructions.md`), replacing only three sentinel-delimited sections (`<!-- context7 -->`, `<!-- code-review-graph -->`, `<!-- agent-discovery -->`) and leaving user content outside sentinels untouched.

Both stages are safe by construction: a destination file is only overwritten or pruned when it carries a generated marker (or lives inside a generated skill directory). Hand-placed files are skipped and reported under `skipped_paths`.

### Content model

- **Agents** (`source_of_truth/agents/`) — 52 definitions (14 user-invocable, 38 hidden) following an orchestrator + subagent pattern: user-invocable primary agents (planner → refiner → decomposer → phase-execute pipeline, PR review, audits, test orchestrator, standalone specialists) plus hidden `user-invocable: false` subagents (deployed with a `z-` prefix) that orchestrators spawn. Full catalog: `source_of_truth/agents/README.md`.
- **Skills** (`source_of_truth/skills/`) — directory-based capabilities, each rooted at `SKILL.md`, loaded on demand by agents.
- **Instructions** (`source_of_truth/instructions/`) — cross-cutting guidance matched by `applyTo` file globs; consumed directly by Copilot, transformed for other harnesses.
- **Learnings** (`source_of_truth/learnings/`) — shared cross-phase knowledge propagated to every harness.

**Brevity constraint on authored agent and skill definitions**: the agent and skill files written to `source_of_truth/` are loaded into model context at runtime — every unnecessary word is wasted context. Definitions must be terse: state the behavior, the constraints, and the output contract once each, and stop. No restating context the agent already has, no motivational preamble, no repeating a rule in different words, no exhaustive examples where one suffices. Carry this into every feature's AC: a definition that says the same thing twice fails review.

### Tests

`tests/` are regression tests over both scripts — they verify source↔generated sync, deploy safety (marker respect), naming conventions (aliases, `z-` prefixes), and per-harness invocation contracts. After editing `source_of_truth/`, propagate before running tests or sync tests will fail.

### Other areas

- `eval/` — past benchmark run artifacts; `eval/deprecated/` holds the archived eval-grader system (see `eval/deprecated/README.md`)
- `packages/com.threnjen.visual-verification/` — Unity UPM package paired with the Visual Verifier agent
- `docs/` — ARCHITECTURE, CODEBASE_CONTEXT, LOCAL_DEVELOPMENT, TROUBLESHOOTING, porting references; keep counts/paths in these aligned with README and CONTRIBUTING when editing docs
