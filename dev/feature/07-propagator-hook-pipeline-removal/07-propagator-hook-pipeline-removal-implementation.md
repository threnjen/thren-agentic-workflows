# Implementation Record: 07-propagator-hook-pipeline-removal

## Summary

Deleted the propagator's entire hook-emission pipeline from
`scripts/propagate_master_assets.py` (all AC1-named symbols, source discovery,
asset copy/pruning, settings/plugin writers, `hooks_source` inventory counter, and
the `--global-output` CLI path). Converted the done-notify wiring to hand-owned
static config in `.claude/settings.json`, `.codex/hooks.json`, and
`.opencode/plugins/done-notify.js` (no `$source` tag, no generated header). Removed
all audit-log and injection-scanner wiring and deleted their OpenCode plugins,
`.github/hooks/done-notify.json`, and `.github/hooks/.distribution-version`.
Untagged code-review-graph entries preserved byte-identical. Deleted all
hook-emission tests and added two done-notify non-interference tests. Double
`--once` produces zero diff.

## Sibling Features

Read the first lines of sibling plans in `dev/feature/`. This is Phase 05
Deliverable 1. Feature 08 (`08-hook-framework-retirement`) depends on this at
runtime — it deletes the audit-log/scanner scripts under `.github/hooks/` that
harness configs referenced until this feature unwired them, and it owns the
`tests/hooks/` deletion plus the full-suite green gate. Feature 09
(`09-hook-record-purge`) documents the static-config end state created here.
Shared module touched by siblings: `.github/hooks/` (08) and
`.github/learnings/cross-phase-decisions.md` (09) — neither touched here.

## AC Coverage Matrix

| AC | Criterion ID | Planned Test ID | Planned Test Pattern | Status | Implementing Files | Evidence Paths | Implement Commit SHA | Review Commit SHA |
|----|--------------|-----------------|----------------------|--------|--------------------|----------------|----------------------|-------------------|
| AC1 | AC1 | n/a (absence grep + surviving suite) | symbol-absence grep | Done | `scripts/propagate_master_assets.py` | `scripts/propagate_master_assets.py`; `tests/test_propagate_master_assets.py` | PENDING | PENDING |
| AC2 | AC2 | non-interference (new) | `test_propagation_leaves_untagged_done_notify_entry_untouched` | Done | `.claude/settings.json`, `.codex/hooks.json`, `.opencode/plugins/done-notify.js`, `.github/hooks/done-notify.json` (del) | `.claude/settings.json:49-60`; `.codex/hooks.json:49-60`; `.opencode/plugins/done-notify.js` | PENDING | PENDING |
| AC3 | AC3 | code-review grep | `$source`/`audit-log`/`injection-scanner` absence | Done | `.claude/settings.json`, `.codex/hooks.json`, `.opencode/plugins/audit-log.js` (del), `.opencode/plugins/injection-scanner.js` (del) | `.claude/settings.json`; `.codex/hooks.json` | PENDING | PENDING |
| AC4 | AC4 | manual QA double `--once` | zero-diff on second run | Done | `scripts/propagate_master_assets.py` | double `--once` diff-hash identical (see Test Results) | PENDING | PENDING |
| AC5 | AC5 | new non-interference tests | `StaticDoneNotifyNonInterferenceTests` | Done | `tests/test_propagate_master_assets.py` | `tests/test_propagate_master_assets.py` (StaticDoneNotifyNonInterferenceTests) | PENDING | PENDING |

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | No hook emission/translation/discovery code; all named symbols + `hooks_source` counter deleted; `.distribution-version` deleted | Done | `scripts/propagate_master_assets.py` | `grep -ni hook` returns nothing; all 14 named symbols absent; `INVENTORY_COUNTERS = frozenset({"source_agents"})`; `shlex` import pruned; also removed the hook-only `--global-output` CLI path and `_to_pascal_case`/`_absolute_hook_command`/`generate_global_hooks` |
| AC2 | done-notify committed as static config, no `$source`, header removed; command content preserved | Done | `.claude/settings.json`, `.codex/hooks.json`, `.opencode/plugins/done-notify.js`, `.github/hooks/done-notify.json` (deleted) | Stop+Notification (claude), Stop (codex); notification commands byte-preserved |
| AC3 | audit-log + injection-scanner wiring removed; plugins deleted; code-review-graph entries byte-identical | Done | `.claude/settings.json`, `.codex/hooks.json`, `.opencode/plugins/audit-log.js` (deleted), `.opencode/plugins/injection-scanner.js` (deleted) | no `$source`/`audit-log`/`injection-scanner` strings remain; CRG PostToolUse/SessionStart lines unchanged in git diff |
| AC4 | `--once` converges, emits no hook outputs, second run zero diff | Done | `scripts/propagate_master_assets.py` | diff-hash identical before/after a second `--once`; no hook artifacts regenerated/stranded |
| AC5 | Hook-emission tests deleted; done-notify non-interference tests added; suite passes | Done | `tests/test_propagate_master_assets.py` | 36 passed, 34 subtests passed |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `scripts/propagate_master_assets.py` | Modify | Deleted all hook constants (`HOOK_EVENT_MAP`, `HOOK_SOURCE_KEY`, `RETIRED_HOOK_ASSETS`, `RETIRED_HOOK_ASSET_HASHES`, `GENERATED_OPENCODE_PLUGIN_HEADER`, `HOOK_PROJECT_ROOT_TOKENS`), hook path constants, resolvers/`_strip_propagated_hooks`/`_render_opencode_plugin`/`_update_nested_settings_file`, asset copy/version/retired-pruning helpers, `_validate_hook_commands`, `propagate_hooks_once`, `_absolute_hook_command`, `generate_global_hooks`, `_to_pascal_case`; removed `hooks_source` from `INVENTORY_COUNTERS`, from `propagate_once` result dict and change tallies; removed `.github/hooks` from `WATCH_DIRS`, `--global-output` CLI arg + branch; pruned `shlex` import; updated watch banner | AC1 |
| `.claude/settings.json` | Modify | Removed audit-log + injection-scanner PostToolUse entries; stripped `$source` from done-notify Stop + Notification | AC2/AC3 |
| `.codex/hooks.json` | Modify | Removed audit-log + injection-scanner PostToolUse entries; stripped `$source` from done-notify Stop | AC2/AC3 |
| `.opencode/plugins/done-notify.js` | Modify | Removed generated-file header line; body preserved | AC2 |
| `.github/hooks/done-notify.json` | Delete | Propagated done-notify source removed | AC2 |
| `.github/hooks/.distribution-version` | Delete | Hook-distribution state removed with the pipeline | AC1 |
| `.opencode/plugins/audit-log.js` | Delete | Generated audit-log plugin removed | AC3 |
| `.opencode/plugins/injection-scanner.js` | Delete | Generated scanner plugin removed | AC3 |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| `tests/test_propagate_master_assets.py` | Modify | Deleted `_make_hook_source` helper and the entire hook-emission test block (`test_hook_propagation_*`, `test_generated_hook_commands_*`, `test_generate_global_hooks_*`, `test_hook_regeneration_*`, `test_hook_asset_copy_*`, `test_every_retired_regular_asset_*`, `test_propagated_scanner_runs_from_detached_consumer_*`, `test_global_setup_backs_up_user_files_*`, `test_phase02_generated_wiring_*`, `test_phase02_opencode_adapter_*`); deleted `test_global_cli_converges_before_mutating_user_output` (referenced deleted `--global-output`/`generate_global_hooks`); dropped `hooks_source` from convergence-counter fixture; added `StaticDoneNotifyNonInterferenceTests` with two assertions | AC5 |

## Test Results
- **Baseline**: 56 passed, 49 subtests passed (`tests/test_propagate_master_assets.py`, pre-pass)
- **Final**: 36 passed, 34 subtests passed (`tests/test_propagate_master_assets.py`)
- **New tests added**: 2 (`test_propagation_leaves_untagged_done_notify_entry_untouched`, `test_propagation_does_not_prune_static_done_notify_plugin`)
- **Regressions**: None within feature scope. Full-suite `tests/` shows 5 failures/errors, all in `tests/hooks/test_hook_distribution_integration.py`, which is feature 08's scope (full-suite green gate lands there per plan). AC4 zero-diff: `--once` diff-hash identical before/after a second run.

## Deviations from Plan
- Retired-hook-asset pruning (`RETIRED_HOOK_ASSETS`, `RETIRED_HOOK_ASSET_HASHES`, `_remove_retired_hook_assets`) was **removed with the pipeline** rather than kept — the plan (AC1) and context explicitly leave this to implementer's discretion provided AC4 holds. AC4 zero-diff confirmed, so the simpler pure-deletion path was taken. The dependent ownership tests were deleted alongside it.
- Also removed the hook-only `--global-output` CLI flag, its `generate_global_hooks`/`_absolute_hook_command` functions, and `_to_pascal_case` (only consumed by the deleted plugin renderer). These are part of the hook-emission pipeline and left no non-hook caller.

## Gaps
None within this feature's gate. Feature 08 owns the `tests/hooks/` failures and the full-suite green gate.

## Reviewer Focus Areas
- A stale long-running `--watch` propagator (PID 63253, old in-memory code) was regenerating the deleted hook wiring mid-implementation; it was stopped per the plan's runbook. **Anyone with a running `--watch` must restart it after this merge** or it will re-emit hooks from stale code.
- `scripts/propagate_master_assets.py` `propagate_once` result dict (`claude_changed`/`opencode_changed`/`codex_changed` no longer add hook contributions) — confirm no non-hook counter was dropped.
- `.claude/settings.json` / `.codex/hooks.json` — verify the untagged code-review-graph PostToolUse/SessionStart entries are byte-identical (git diff shows no change on those lines) and JSON remains valid.
- `StaticDoneNotifyNonInterferenceTests` in `tests/test_propagate_master_assets.py` — these pass because `propagate_once` no longer touches settings/plugin paths at all; confirm they would fail against the old hook-emitting propagator (they exercise the real done-notify wiring shape).
