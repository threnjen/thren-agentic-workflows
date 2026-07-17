# Phase 5: Hook Removal

**Status**: Planned
**Depends on**: None (removal work; Phases 01–04 are historical inputs, not prerequisites)
**Estimated complexity**: Medium
**Cross-references**: None

## What's New

This repository stops being a hook project. Every live hook — wiring, framework,
scripts, tests, the propagator's entire hook-emission pipeline, and the documentation
record around them — is removed. What remains afterward is the PR Review agent family,
the agent/skill/instruction propagation and managed-copy deployment machinery, and two
deliberately kept artifacts: the prompt-injection scanner **on disk but dead** (retained
code, wired nowhere, explicitly marked defunct) and the `done-notify` desktop
notification, which survives as **static, hand-committed harness config** — no longer a
propagated asset. `docs/inspiration/` (the survey of other projects' hook patterns) is
kept as research history.

The practical effect for the user: no hook fires anywhere, in any harness, in this repo
or any deployed home — except the Stop-event desktop notification, which keeps working
as plain checked-in config. The bypass-permissions security claim is dropped from the
project entirely.

## Objective

Remove all hook functionality — including the propagator's hook-emission machinery —
and its documentation record from the repository, so the project's surface is exactly
what it actually ships: the PR Review agent family and the propagation/deployment
machinery, with no dead security claims attached.

## Scope

### In Scope

- **Propagator pipeline deletion**: remove all hook emission/translation code from
  `scripts/propagate_master_assets.py` — the event map (`HOOK_EVENT_MAP`), hook command
  resolution/anchoring (`_resolve_hook_events`, `_resolve_hook_command`,
  `_project_root_hook_command`, `HOOK_PROJECT_ROOT_TOKENS`), settings/plugin hook
  writers (`_strip_propagated_hooks`, OpenCode plugin generation for hooks),
  `HOOK_SOURCE_KEY` handling, hook source discovery of `.github/hooks/`, and the
  `hooks_source` inventory counter. Retired-hook-asset pruning entries
  (`RETIRED_HOOK_ASSETS` / hashes) are extended or simplified as needed so `--once`
  converges with the generated roots clean of hook outputs.
  > Suggested implementation shape, to be verified by Feature Decomposer against
  > current code and tests.
- **`done-notify` converted to static config**: delete `.github/hooks/done-notify.json`
  as a propagated source; commit its wiring directly as static, unmanaged config in
  `.claude/settings.json`, `.codex/hooks.json`, and `.opencode/plugins/done-notify.js`,
  with any `$source` generation tags removed so nothing ever treats it as a generated
  orphan. The propagator must neither emit nor prune it.
- **Unwiring**: remove all other hook wiring from the generated harness configs
  (`.claude/settings.json` hook entries, `.codex/hooks.json`, `.codex/config.toml`
  hook entries if any, `.opencode/plugins/audit-log.js` and
  `.opencode/plugins/injection-scanner.js`).
- **Framework deletion**: delete `.github/hooks/lib/framework.py`,
  `.github/hooks/scripts/audit-log.py` / `audit-log.sh`, `audit-log.json`, `__pycache__`
  directories, and any hook config not required by the retained-dead scanner.
- **Test deletion**: delete `tests/hooks/` in full (framework tests, injection
  corpus/benchmark, distribution integration tests, fixtures). In
  `tests/test_propagate_master_assets.py` (~148 hook references — hook emission is the
  backbone of that suite) hook-emission tests are **deleted, not retargeted**; add
  small new assertions that the propagator ignores and never prunes the static
  done-notify wiring. Strip hook assertions from
  `tests/test_phase04_runtime_deployment.py` (~12 references) so the remaining suites
  pass.
- **Scanner retained dead**: keep `.github/hooks/lib/injection_scanner.py`,
  `.github/hooks/scripts/injection-scanner.py`, `injection-scanner.json`, and
  `.github/hooks/config/` on disk, unwired everywhere, with a short DEFUNCT marker
  (file header or adjacent README) stating it is intentionally inert. After this phase,
  `.github/hooks/` contains only the dead scanner files, their configs, and the marker.
- **Record purge**: delete `docs/phases/PHASE_01/`, `docs/phases/PHASE_02/`,
  `docs/phases/PHASE_04/`, and `docs/hooks/`. In
  `.github/learnings/cross-phase-decisions.md`: delete pure-hook sections wholesale
  (Hook Composition; Guard Friction and Command Prompting; File-Access Guard
  Retirement; hook-only entries within Deferred Pipeline Work); in mixed sections
  (Deferred Pipeline Work, Propagation Contracts, Phase 04 Runtime Deployment
  Contract) remove only hook lines, preserving everything the propagation/deployment
  machinery and Phase 07 still rely on.
- **Docs scrub**: scrub hook content from `README.md`, `docs/ARCHITECTURE.md`,
  `docs/CODEBASE_CONTEXT.md`, `docs/TROUBLESHOOTING.md`, `HARNESS_SETUP.md`, and
  `docs/LOCAL_DEVELOPMENT.md`. The README Acknowledgments section is **rewritten to
  past tense**, keeping attribution to the surveyed repos (per the `docs/inspiration/`
  retention decision) while removing any claim of a live hook system.
- **Roadmap verification**: `docs/phases/PROJECT_ROADMAP.md` was rewritten at planning
  time; Phase 05 verifies the final state matches post-removal reality.

### Out of Scope

- Deleting `docs/inspiration/` — kept as research history.
- Deleting the injection scanner's code — it stays on disk, dead.
- Rewriting git history — everything removed remains recoverable via git.
- **`eval/hooks/post-commit.sh` and the eval commit-hook machinery** — this is the
  planning pipeline's own git hook, not a harness hook. Untouchable by this phase.
- Any change to the PR Review agent family (Phase 03 assets) beyond removing hook
  references in shared docs.
- Agent packaging/distribution — that is Phase 07 (Package Agents for General Use).
- Removing hook registrations in user-global config outside this repo (none are
  installed; the retired `rtk-rewrite` global entry was already removed).

## Key Deliverables

| # | Deliverable | Description | Likely Features |
|---|-------------|-------------|-----------------|
| 1 | Propagator pipeline deletion + static done-notify + unwiring | All hook emission code removed from the propagator; done-notify committed as static unmanaged config in all three harnesses; all other generated hook wiring removed; `--once` converges clean | Propagator surgery, static config commit, prune/convergence verification |
| 2 | Framework/test deletion + dead-scanner marking | Hook framework, audit-log, and `tests/hooks/` deleted; propagation/deployment test suites purged of hook-emission tests with new done-notify non-interference assertions; scanner files retained with DEFUNCT marker; suite green | File deletion, test surgery, defunct marker |
| 3 | Documentation and record purge | Phase docs 01/02/04, `docs/hooks/`, decision-log hook sections deleted (line-level scrub in mixed sections); standard docs scrubbed; README Acknowledgments rewritten historical; roadmap verified consistent | Docs sweep, decision-log edit, final consistency check |

## Technical Context

- **Wiring today**: `scripts/propagate_master_assets.py` generates hook wiring from
  `.github/hooks/*.json` into `.claude/settings.json`
  (`$CLAUDE_PROJECT_DIR`-anchored commands), `.codex/hooks.json`, and
  `.opencode/plugins/`. Its orphan-pruning removes generated outputs whose source is
  gone. Hook emission is interleaved with agent/skill/command/learning propagation,
  which must survive intact.
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
- **Tests**: `tests/hooks/` is wholly hook-scoped.
  `tests/test_propagate_master_assets.py` (~148 hook references) and
  `tests/test_phase04_runtime_deployment.py` (~12) mix hook assertions with
  propagation/deployment assertions that must survive. Test entry point:
  `.venv/bin/python -m pytest tests/` (system python3 lacks pytest).
- **`--runtime-deploy`** (`scripts/runtime_deployment.py`, `_ASSET_POLICIES`) never
  shipped hooks — no deployed-home cleanup is needed beyond regenerated repo outputs.

## Dependencies & Risks

- **Risk — over-deletion breaking propagation**: hook emission is interleaved with the
  agent/skill/command/learning logic the propagator must keep. Mitigation: the
  surviving pytest suites must pass after every feature, and `--once` must converge
  with a clean diff.
- **Risk — done-notify silently pruned or clobbered**: the static wiring lives in
  files the propagator still writes (`.claude/settings.json`, `.opencode/plugins/`).
  Mitigation: `$source` tags removed from the static entries, explicit
  non-interference test assertions, and a manual smoke check.
- **Risk — decision-log over-scrub**: mixed sections contain propagation/deployment
  contracts Phase 07 depends on. Mitigation: line-level scrub rule (only hook lines
  removed from mixed sections) and review of the record-purge commit in isolation.
- **Risk — lost rationale**: deleting phase docs and decision-log hook sections removes
  the written record of why a dead scanner sits in the tree. Accepted deliberately by
  the user (2026-07-17); git history is the only remaining trail, and the DEFUNCT
  marker carries the one-line explanation forward.
- **Dependency**: none upstream. Downstream, Phase 07 (agent packaging) assumes the
  propagator/deployment machinery still works exactly as before minus hooks.

## Success Criteria

- [ ] The propagator contains no hook emission, translation, or source-discovery code;
      `scripts/propagate_master_assets.py --once` converges with no hook outputs
      emitted and no stranded hook artifacts in any generated root.
- [ ] No hook wiring exists in `.claude/settings.json`, `.codex/hooks.json`,
      `.codex/config.toml`, or `.opencode/plugins/` except the static done-notify
      entries, which carry no `$source` tag and still fire at Stop.
- [ ] Running `--once` twice in a row leaves the static done-notify wiring
      byte-identical (the propagator neither prunes nor rewrites it).
- [ ] `.github/hooks/` contains only the dead scanner files, their configs, and a
      DEFUNCT marker; `done-notify.json` and `audit-log.json` are gone.
- [ ] `tests/hooks/` is gone and `.venv/bin/python -m pytest tests/` passes.
- [ ] `docs/phases/PHASE_01/`, `PHASE_02/`, `PHASE_04/`, and `docs/hooks/` are deleted;
      `cross-phase-decisions.md` contains no hook content, and its surviving
      propagation/deployment contract sections are intact.
- [ ] `README.md`, `docs/ARCHITECTURE.md`, `docs/CODEBASE_CONTEXT.md`,
      `docs/TROUBLESHOOTING.md`, `HARNESS_SETUP.md`, and `docs/LOCAL_DEVELOPMENT.md`
      contain no live-hook claims; the README Acknowledgments section is past-tense
      with attribution preserved; inventory counts in the three standard docs agree.
- [ ] `eval/hooks/post-commit.sh` and `docs/inspiration/` are unchanged.
- [ ] `PROJECT_ROADMAP.md` reflects the post-removal reality (verified, not rewritten,
      by this phase).

## QA Considerations

- No UI. QA is: full pytest run, a double `--once` propagation convergence run, and one
  manual smoke — start a fresh harness session in this repo and confirm no hook fires
  and the done-notify notification still appears at Stop.
- Doc-count reconciliation across README / ARCHITECTURE / CODEBASE_CONTEXT (the three
  must agree, per `docs/TROUBLESHOOTING.md` § Documentation Drift).

## Notes for Feature - Decomposer

- Three features, in order: (1) propagator pipeline deletion + static done-notify
  conversion + regeneration/prune verification; (2) framework/test deletion + DEFUNCT
  marking, keeping the suite green; (3) docs/record purge + final consistency check.
  Order matters: convert done-notify to static config and delete the emission pipeline
  in the same feature so no intermediate state has wiring pointing at deleted scripts
  or a source file with no emitter.
- Feature 1 must decide how the propagator's writers avoid disturbing the static
  done-notify entries (e.g., it only ever managed `$source`-tagged entries; once those
  are gone it should leave foreign entries alone) — verify against current merge logic.
- Feature 2 must decide the scanner-retention shape (delete `framework.py` and accept
  an unimportable dead module, or retain it) and record the choice in the DEFUNCT
  marker.
- The record purge (feature 3) is destructive to planning docs — it should be a single
  reviewed commit, separate from code deletion commits, so it is trivially revertable.
  Apply the mixed-section rule: whole-section deletion only for pure-hook sections;
  line-level scrub elsewhere.
- Do not touch `eval/hooks/`, `docs/inspiration/`, Phase 03 / PR Review assets, or
  `docs/phases/PHASE_03/` and `PHASE_07/` (Phase 07's doc is rewritten by
  project-planner separately, not by this phase).
