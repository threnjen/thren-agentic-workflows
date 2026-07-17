# Phase 05 Discovery Context

Context gathered during the 2026-07-17 refinement session. Load alongside
`PHASE_05_SUMMARY.md`.

## Verified repo facts (2026-07-17)

- `tests/test_propagate_master_assets.py` contains ~148 hook references;
  `tests/test_phase04_runtime_deployment.py` ~12. Hook emission is the backbone of the
  propagation suite — the surgery there is large.
- Propagator hook surfaces confirmed in `scripts/propagate_master_assets.py`:
  `HOOK_EVENT_MAP`, `HOOK_SOURCE_KEY` (`$source`), `RETIRED_HOOK_ASSETS` +
  `RETIRED_HOOK_ASSET_HASHES`, `_resolve_hook_events`, `_resolve_hook_command`,
  `_project_root_hook_command` / `HOOK_PROJECT_ROOT_TOKENS`, `_strip_propagated_hooks`,
  hook source discovery of `.github/hooks/`, `hooks_source` inventory counter, and
  OpenCode plugin generation (`GENERATED_OPENCODE_PLUGIN_HEADER`).
- Current generated hook wiring: `.claude/settings.json` (audit-log, injection-scanner,
  done-notify entries), `.codex/hooks.json`, `.opencode/plugins/{audit-log,
  injection-scanner, done-notify}.js`.
- `.github/learnings/cross-phase-decisions.md` section map: pure-hook sections are
  "Hook Composition", "Guard Friction and Command Prompting", "File-Access Guard
  Retirement"; mixed sections needing line-level scrub are "Deferred Pipeline Work",
  "Propagation Contracts", "Phase 04 Runtime Deployment Contract".
- `README.md` Acknowledgments (~lines 170–194) claims a live clean-room hook system
  and credits surveyed hook repos — rewrite to past tense, keep attribution.
- `eval/hooks/post-commit.sh` is the planning pipeline's own git hook — out of scope.

## Decisions made during refinement (user, 2026-07-17)

- **done-notify**: delete the propagator's entire hook-emission pipeline; hand-wire
  done-notify as static, unmanaged config in each harness (no `$source` tag, never
  emitted or pruned). Chosen over keeping the pipeline with one source, and over
  dropping the notification entirely.
- Hook-emission tests are deleted, not retargeted; new assertions cover only
  non-interference with the static done-notify wiring.
- Record-purge rules: whole-section deletion for pure-hook decision-log sections;
  line-level scrub in mixed sections; README attribution preserved historically.
