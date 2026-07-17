# Tasks: 07-propagator-hook-pipeline-removal

## Stage 1: Propagator surgery + static done-notify conversion (AC1–AC3)

- [x] Delete all hook-pipeline symbols from `scripts/propagate_master_assets.py`: `HOOK_EVENT_MAP`, `HOOK_SOURCE_KEY`, `RETIRED_HOOK_ASSETS`, `RETIRED_HOOK_ASSET_HASHES`, `_resolve_hook_events`, `_resolve_hook_command`, `_project_root_hook_command`, `HOOK_PROJECT_ROOT_TOKENS`, `_strip_propagated_hooks`, `GENERATED_OPENCODE_PLUGIN_HEADER`, the settings hook writer, the OpenCode plugin hook writer, and the `.github/hooks/` source discovery (AC1)
- [x] Decide whether retired-hook-asset pruning completes cleanly or is removed with the pipeline; record the choice in implementation notes (AC1, must keep AC4 satisfiable)
- [x] Remove the `hooks_source` inventory counter everywhere (including its `INVENTORY_COUNTERS` entry, reducing it to `{"source_agents"}`) and the `hooks_source` summary line (AC1)
- [x] Prune now-unused imports; verify no commented-out hook code and no surviving `hook` identifiers except incidental words in unrelated strings (AC1)
- [x] Delete `.github/hooks/done-notify.json` (AC2)
- [x] Convert `.claude/settings.json` done-notify Stop and Notification entries to static config: remove `$source` keys, preserve command content byte-for-byte (AC2)
- [x] Convert `.codex/hooks.json` done-notify Stop entry to static config: remove `$source` key, preserve command content (AC2)
- [x] Remove the generated-file header comment (first line) from `.opencode/plugins/done-notify.js`, keeping the rest as-is (AC2)
- [x] Remove audit-log and injection-scanner entries from `.claude/settings.json` and `.codex/hooks.json` (AC3)
- [x] Delete `.opencode/plugins/audit-log.js` and `.opencode/plugins/injection-scanner.js` (AC3)
- [x] Verify untagged code-review-graph PostToolUse/SessionStart entries in both settings files are byte-identical to before (AC3)
- [x] Grep-verify: no `$source`, `audit-log`, or `injection-scanner` strings remain in `.claude/settings.json` or `.codex/hooks.json`; AC1 symbol-list grep over the propagator returns nothing (code-review evidence)

## Stage 2: Test surgery and convergence verification (AC4–AC5)

- [x] Delete hook-emission/translation/pruning tests from `tests/test_propagate_master_assets.py`, auditing each test individually — includes `test_hook_propagation_*`, `test_generated_hook_commands_resolve_from_a_subdirectory`, `test_generate_global_hooks_uses_absolute_source_commands`, `test_hook_regeneration_*`, `test_hook_asset_copy_*`, and hook-exercising tests without `hook` in the name (`test_phase02_generated_wiring_is_complete_and_idempotent`, `test_phase02_opencode_adapter_*`, `test_propagated_scanner_runs_from_detached_consumer_without_dependencies`) (AC5)
- [x] Audit partially hook-coupled tests (`test_global_setup_backs_up_user_files_and_installs_regular_outputs`, `test_global_cli_converges_before_mutating_user_output`, retired-asset ownership tests) and delete or trim per the Stage 1 pruning decision (AC5)
- [x] Add non-interference assertion [PROPOSED - name TBD]: given a settings file with the untagged done-notify Stop entry, run propagation, assert the entry is byte-identical (AC5)
- [x] Add non-interference assertion [PROPOSED - name TBD]: given `.opencode/plugins/done-notify.js` without the generated header, run propagation/pruning, assert the file survives (AC5)
- [x] Reuse existing tmp-root propagation fixtures for the new assertions; do not build a large retirement suite (AC5)
- [x] Run `.venv/bin/python -m pytest tests/test_propagate_master_assets.py` — must pass (AC5)
- [x] Manual QA: run `scripts/propagate_master_assets.py --once` twice; second run produces zero `git diff`; no hook outputs emitted, no stranded hook artifacts, static done-notify wiring byte-identical (AC4)
- [x] Manual QA: fresh Claude session — no hook fires; Stop notification appears (AC2 evidence)
- [x] Note in implementation record: restart any long-running `--watch` propagator after merge
