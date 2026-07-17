# Phase 5: Hook Removal

**Status**: Planned
**Depends on**: None (removal work; Phases 01–04 are historical inputs, not prerequisites)
**Estimated complexity**: Medium
**Cross-references**: None

## What's New

This repository stops being a hook project. Every live hook — wiring, framework,
scripts, tests, and the documentation record around them — is removed. What remains
afterward is the PR Review agent family, the agent/skill/instruction propagation and
managed-copy deployment machinery, and two deliberately kept artifacts: the
prompt-injection scanner **on disk but dead** (retained code, wired nowhere, explicitly
marked defunct) and the `done-notify` desktop notification. `docs/inspiration/` (the
survey of other projects' hook patterns) is kept as research history.

The practical effect for the user: no hook fires anywhere, in any harness, in this repo
or any deployed home. The bypass-permissions security claim is dropped from the project
entirely.

## Objective

Remove all hook functionality and its documentation record from the repository so the
project's surface is exactly what it actually ships — the PR Review agent family and
the propagation/deployment machinery — with no dead security claims attached.

## Scope

### In Scope

- **Unwiring**: remove all hook wiring from the generated harness configs
  (`.claude/settings.json` hooks block, `.codex/hooks.json`, `.opencode/plugins/`
  hook plugins) and remove hook emission/propagation support from
  `scripts/propagate_master_assets.py`, letting its orphan-pruning clean the
  generated roots.
- **Framework deletion**: delete `.github/hooks/lib/framework.py`,
  `.github/hooks/scripts/audit-log.py` / `audit-log.sh`, `audit-log.json`, and any
  hook config not required by the retained-dead scanner.
- **Test deletion**: delete `tests/hooks/` in full (framework tests, injection
  corpus/benchmark, distribution integration tests, fixtures), and strip
  hook-related assertions from `tests/test_propagate_master_assets.py` and
  `tests/test_phase04_runtime_deployment.py` so the remaining suites pass.
- **Scanner retained dead**: keep `.github/hooks/lib/injection_scanner.py`,
  `.github/hooks/scripts/injection-scanner.py`, `injection-scanner.json`, and
  `.github/hooks/config/` on disk, unwired everywhere, with a short DEFUNCT marker
  (file header or adjacent README) stating it is intentionally inert.
- **`done-notify` retained**: `.github/hooks/done-notify.json` and its generated
  notification wiring keep working (it is the one wiring survivor).
- **Record purge**: delete `docs/phases/PHASE_01/`, `docs/phases/PHASE_02/`,
  `docs/phases/PHASE_04/`, and `docs/hooks/`; remove the hook sections from
  `.github/learnings/cross-phase-decisions.md`; scrub hook content from
  `README.md`, `docs/ARCHITECTURE.md`, `docs/CODEBASE_CONTEXT.md`,
  `docs/TROUBLESHOOTING.md`, `HARNESS_SETUP.md`, and `docs/LOCAL_DEVELOPMENT.md`.
- **Roadmap rewrite**: `docs/phases/PROJECT_ROADMAP.md` Vision and phase table
  rewritten around PR Review + agent deployment (performed by project-planner at
  planning time; Phase 05 verifies the final state matches reality after removal).

### Out of Scope

- Deleting `docs/inspiration/` — kept as research history.
- Deleting the injection scanner's code — it stays on disk, dead.
- Rewriting git history — everything removed remains recoverable via git.
- Any change to the PR Review agent family (Phase 03 assets) beyond removing hook
  references in shared docs.
- Agent packaging/distribution — that is Phase 07 (Package Agents for General Use).
- Removing hook registrations in user-global config outside this repo (none are
  installed; the retired `rtk-rewrite` global entry was already removed).

## Key Deliverables

| # | Deliverable | Description | Likely Features |
|---|-------------|-------------|-----------------|
| 1 | Unwiring + propagator cleanup | No hook wiring in any generated output except `done-notify`; propagator no longer knows how to emit hook assets; orphan-pruning removes stranded outputs | Propagator change, generated-config regeneration, prune verification |
| 2 | Framework/test deletion + dead-scanner marking | Hook framework, audit-log, and `tests/hooks/` deleted; scanner files retained with DEFUNCT marker; remaining test suites green | File deletion, test surgery, defunct marker |
| 3 | Documentation and record purge | Phase docs 01/02/04, `docs/hooks/`, decision-log hook sections deleted; standard docs scrubbed; roadmap verified consistent | Docs sweep, decision-log edit, final consistency check |

## Technical Context

- **Wiring sources**: `scripts/propagate_master_assets.py` generates hook wiring into
  `.claude/settings.json` (`$CLAUDE_PROJECT_DIR`-anchored commands),
  `.codex/hooks.json`, and `.opencode/plugins/`. It also has orphan-pruning that
  removes generated outputs whose source is gone — deleting sources plus removing the
  emission logic, then running `--once`, should converge the roots.
- **Hook sources**: `.github/hooks/` contains `lib/` (`framework.py`,
  `injection_scanner.py`), `scripts/` (`injection-scanner.py`, `audit-log.py`,
  `audit-log.sh`), `config/` (`injection-patterns.json`, `injection-allowlist.json`),
  and top-level `injection-scanner.json`, `audit-log.json`, `done-notify.json`.
- **Scanner coupling**: `injection_scanner.py` imports from `framework.py`. Retaining
  the scanner dead while deleting the framework leaves an unimportable module — that is
  acceptable for a defunct artifact, but the DEFUNCT marker must say so. Alternative
  shape (retain `framework.py` too) is a Feature-Decomposer call.
  > Suggested implementation shape, to be verified by Feature Decomposer against
  > current code and tests.
- **Tests**: `tests/hooks/` is wholly hook-scoped. `tests/test_propagate_master_assets.py`
  and `tests/test_phase04_runtime_deployment.py` contain hook-related assertions mixed
  with propagation/deployment assertions that must survive. Test entry point:
  `.venv/bin/python -m pytest tests/` (system python3 lacks pytest).
- **`--runtime-deploy`** (`scripts/runtime_deployment.py`, `_ASSET_POLICIES`) never
  shipped hooks — no deployed-home cleanup is needed beyond regenerated repo outputs.

## Dependencies & Risks

- **Risk — over-deletion breaking propagation**: the propagator serves agents, skills,
  commands, and learnings; hook emission is interleaved with that logic. Mitigation:
  the surviving pytest suites (propagation, runtime deployment, PR Review) must pass
  after every feature, and `--once` must converge with a clean diff.
- **Risk — `done-notify` regression**: the one wiring survivor uses the same emission
  path being removed. Mitigation: an explicit success criterion below.
- **Risk — lost rationale**: deleting phase docs and decision-log hook sections removes
  the written record of why a dead scanner sits in the tree. Accepted deliberately by
  the user (2026-07-17); git history is the only remaining trail, and the DEFUNCT
  marker carries the one-line explanation forward.
- **Dependency**: none upstream. Downstream, Phase 07 (agent packaging) assumes the
  propagator/deployment machinery still works exactly as before minus hooks.

## Success Criteria

- [ ] No hook wiring exists in `.claude/settings.json`, `.codex/hooks.json`, or
      `.opencode/plugins/` except the `done-notify` notification, which still fires.
- [ ] `scripts/propagate_master_assets.py --once` converges with no hook outputs
      emitted and no stranded hook artifacts in any generated root.
- [ ] `.github/hooks/` contains only the dead scanner files, their configs, a DEFUNCT
      marker, and `done-notify.json`.
- [ ] `tests/hooks/` is gone and `.venv/bin/python -m pytest tests/` passes.
- [ ] `docs/phases/PHASE_01/`, `PHASE_02/`, `PHASE_04/`, and `docs/hooks/` are deleted;
      `cross-phase-decisions.md` contains no hook sections.
- [ ] `README.md`, `docs/ARCHITECTURE.md`, `docs/CODEBASE_CONTEXT.md`,
      `docs/TROUBLESHOOTING.md`, `HARNESS_SETUP.md`, and `docs/LOCAL_DEVELOPMENT.md`
      contain no live-hook claims (historical mentions only where unavoidable);
      inventory counts in the three standard docs agree.
- [ ] `docs/inspiration/` is unchanged.
- [ ] `PROJECT_ROADMAP.md` reflects the post-removal reality (verified, not rewritten,
      by this phase).

## QA Considerations

- No UI. QA is: full pytest run, a propagation convergence run, and one manual smoke —
  start a fresh harness session in this repo and confirm no hook fires and the
  done-notify notification still appears at Stop.
- Doc-count reconciliation across README / ARCHITECTURE / CODEBASE_CONTEXT (the three
  must agree, per `docs/TROUBLESHOOTING.md` § Documentation Drift).

## Notes for Feature - Decomposer

- Three features, in order: (1) propagator unwiring + regeneration + prune
  verification; (2) framework/test deletion + DEFUNCT marking, keeping the suite
  green; (3) docs/record purge + final consistency check. Order matters: unwire before
  deleting sources so no intermediate state has wiring pointing at deleted scripts.
- Feature 2 must decide the scanner-retention shape (delete `framework.py` and accept
  an unimportable dead module, or retain it) and record the choice in the DEFUNCT
  marker.
- The record purge (feature 3) is destructive to planning docs — it should be a single
  reviewed commit, separate from code deletion commits, so it is trivially revertable.
- Do not touch `docs/inspiration/`, Phase 03 / PR Review assets, or
  `docs/phases/PHASE_03/` and `PHASE_07/` (Phase 07's doc is rewritten by
  project-planner separately, not by this phase).
