# Context: 07-propagator-hook-pipeline-removal

Plan: `dev/feature/07-propagator-hook-pipeline-removal/07-propagator-hook-pipeline-removal-plan.md`
Phase: `docs/phases/PHASE_05/PHASE_05_SUMMARY.md` (Deliverable 1)
Discovery: `docs/phases/PHASE_05/PHASE_05_DISCOVERY_CONTEXT.md`

## Key Files

### Files Being Changed

| File | Role | Change Type |
|------|------|-------------|
| `scripts/propagate_master_assets.py` | Propagator; hook pipeline lives at lines 61–143 (constants), 1058–1110 (resolvers/strip), 1112–1217 (settings writer + plugin header use), 1273–1302 (retired-asset pruning), 1380–1481 (hook propagation entry, opencode plugin writer, `hooks_source` counts), 1767/1806 (inventory) | Modify (delete hook pipeline) |
| `tests/test_propagate_master_assets.py` | Propagation suite; 141 `hook` occurrences; hook-emission tests include `test_hook_propagation_*`, `test_generated_hook_commands_resolve_from_a_subdirectory`, `test_generate_global_hooks_uses_absolute_source_commands`, `test_hook_regeneration_*`, `test_hook_asset_copy_*`, `test_phase02_generated_wiring_is_complete_and_idempotent`, `test_phase02_opencode_adapter_*`, `test_propagated_scanner_runs_from_detached_consumer_without_dependencies` | Modify (delete hook tests, add non-interference assertions) |
| `.github/hooks/done-notify.json` | Propagated done-notify source | Delete |
| `.claude/settings.json` | Has `$source`-tagged audit-log, injection-scanner, done-notify (Stop + Notification) entries plus untagged code-review-graph PostToolUse/SessionStart entries | Modify (remove audit-log/scanner entries; strip `$source` from done-notify; preserve code-review-graph entries byte-identical) |
| `.codex/hooks.json` | Same shape: tagged audit-log, injection-scanner, done-notify (Stop only) plus untagged code-review-graph entries | Modify (same treatment) |
| `.opencode/plugins/done-notify.js` | Generated plugin; first line is the generated header | Modify (remove header line only; keep content) |
| `.opencode/plugins/audit-log.js` | Generated audit-log plugin | Delete |
| `.opencode/plugins/injection-scanner.js` | Generated scanner plugin | Delete |

### Read-Only Reference Files

| File | Role |
|------|------|
| `tests/test_retired_evaluator_removal.py` | Shape reference for absence-assertions (do not copy into a large retirement suite — phase directive) |
| `.codex/config.toml` | Verified: contains no hook entries — do not touch |
| `scripts/runtime_deployment.py` | Never shipped hooks — do not touch |
| `tests/test_phase04_runtime_deployment.py`, `tests/hooks/` | Feature 08 scope — do not touch |

## Discovery Delta

| Finding | Impact | Action |
|---------|--------|--------|
| All AC1 symbols verified present at the plan's cited lines (`HOOK_EVENT_MAP` L128, `HOOK_SOURCE_KEY` L62, `RETIRED_HOOK_ASSETS` L63, `RETIRED_HOOK_ASSET_HASHES` L83, `_resolve_hook_events` L1058, `_resolve_hook_command` L1066, `HOOK_PROJECT_ROOT_TOKENS` L1074, `_project_root_hook_command` L1080, `_strip_propagated_hooks` L1100, `GENERATED_OPENCODE_PLUGIN_HEADER` L61, `INVENTORY_COUNTERS` L143) | Plan is accurate | None |
| The settings hook writer (the function around L1186–1217, using `CLAUDE_SETTINGS_FILE`/`claude_settings_file` at L48/1380/1433) is the **only** code path touching the `hooks` key of `.claude/settings.json` — deleting it means the propagator never touches that file at all, satisfying the plan's foreign-entry preservation requirement structurally | Confirms the plan's B-section verification question: yes, removal is sufficient | None |
| OpenCode plugin pruning ownership check confirmed header-based (`content.startswith(GENERATED_OPENCODE_PLUGIN_HEADER)` at L1465); removing the header from `done-notify.js` protects it from pruning — but the whole pruning path is deleted anyway | Confirms plan's orphan-pruning edge analysis | None |
| Hook-test surgery is larger than "grep for hook": `test_phase02_generated_wiring_is_complete_and_idempotent`, `test_phase02_opencode_adapter_replaces_blocked_output_and_appends_warning`, `test_phase02_opencode_adapter_revalidates_scanner_result`, `test_propagated_scanner_runs_from_detached_consumer_without_dependencies`, `test_global_setup_backs_up_user_files_and_installs_regular_outputs`, and `test_global_cli_converges_before_mutating_user_output` exercise or partially exercise hook emission without `hook` in every name | Implementer must audit each test individually, not just name-match | Add task |
| `test_every_retired_regular_asset_has_explicit_ownership_hashes`, `test_hook_regeneration_preserves_unowned_retired_name_collisions`, etc. depend on `RETIRED_HOOK_ASSETS`/hashes — if implementer keeps retired-asset pruning (AC1 allows either), these tests need corresponding treatment | Deletion choice cascades into test choice | Implementer decision, record in implementation notes |
| `.codex/hooks.json` has done-notify under **Stop only**; `.claude/settings.json` has it under **Stop and Notification** — plan AC2 matches reality exactly | Confirms plan | None |
| `.codex/hooks.json` itself is entirely generated hook wiring plus the untagged code-review-graph PostToolUse/SessionStart entries; after removal it becomes a static hand-owned file containing code-review-graph + done-notify entries | Clarifies AC2/AC3 end-state for that file | None |
| New non-interference test names remain `[PROPOSED - name TBD]` per the plan; scenario descriptions in the plan's Section F are the contract | None | Implementer chooses idiomatic names |
| No contradictions found | — | — |

## Architectural Decisions

- **Pure deletion + static commit**: the entire hook-emission pipeline is deleted rather than kept with one source; done-notify becomes hand-owned static config (user decision, 2026-07-17, see discovery context).
- **Static config contract** (consumed by features 08/09 and manifest QA): done-notify entries carry no `$source` key and no generated header; they are hand-owned. The propagator must never touch the `hooks` key of harness settings files.
- **Tests deleted, not retargeted**: hook-emission tests are removed wholesale; only small done-notify non-interference assertions are added. Do not build a large retirement suite.
- **Retired-asset pruning of former hook outputs**: implementer's call to complete cleanly or remove with the pipeline, provided AC4 (double `--once` zero-diff) holds.
- **Single coherent change** for AC1–AC3 so no intermediate state has wiring pointing at deleted scripts.
- `INVENTORY_COUNTERS` reduces to `{"source_agents"}`; propagator summary loses its `hooks_source` line; no new logs.

## Constraints

- Every non-hook propagation path (agents, skills, commands, learnings, pruning of agent/skill orphans) must survive intact — the surviving test suite is the guard.
- Untagged code-review-graph entries in `.claude/settings.json` and `.codex/hooks.json` preserved byte-identical.
- Notification command content preserved as-is from current generated output (`osascript -e display notification ...`).
- Gate for this feature: `.venv/bin/python -m pytest tests/test_propagate_master_assets.py` passes. The full-suite green gate belongs to feature 08.
- No commented-out hook code; no surviving `hook` identifiers in the propagator except incidental words in unrelated strings; prune unused imports.

## Scope Boundaries

- Do NOT touch: `.github/hooks/` scanner/audit-log/framework files, `tests/hooks/`, `tests/test_phase04_runtime_deployment.py` (feature 08); any docs (feature 09); `eval/hooks/`; `scripts/runtime_deployment.py`; `.codex/config.toml`; `docs/inspiration/`; PR Review agent assets.
- Do NOT modify the `-plan.md` file.
- Preserve all agent/skill/command/learning propagation and orphan-pruning behavior.

## Relationships to Sibling Plans

- **Feature 08** depends on this feature at runtime: it deletes the audit-log/scanner scripts that harness configs reference until this feature unwires them. It also owns `tests/hooks/` deletion, `test_phase04_runtime_deployment.py` surgery, DEFUNCT marker, and the full-suite green gate.
- **Feature 09** documents the static-config end state this feature creates.

## Suggested Implementation Order

Wave 1, no dependencies, parallel safe. Within the feature: Stage 1 (propagator surgery + static conversion as one change), then Stage 2 (test surgery + convergence verification). Feature 08 follows, then 09.

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Python 3.12.6 (stdlib scripts; no package config — no pyproject.toml/setup.cfg) |
| Test Runner | `.venv/bin/python -m pytest tests/` (feature gate: `.venv/bin/python -m pytest tests/test_propagate_master_assets.py`) |
| Test Baseline | 401 passed, 156 subtests passed — captured 2026-07-17 |
| Lint | Not configured |
| Format | Not configured |

## Relevant Learnings

- `.github/learnings/cross-phase-decisions.md` § "Propagation Contracts" (line ~293): contains propagation/deployment contracts that Phase 07 relies on — this feature must not violate them; feature 09 handles the line-level hook scrub of that file.
- Phase discovery context (2026-07-17 refinement decisions): done-notify goes static/unmanaged; hook tests deleted not retargeted; pure-hook decision-log sections deleted wholesale, mixed sections line-scrubbed (feature 09).
- Watchers execute the code they started with — restart any long-running `--watch` process after merging (runbook note from plan §E).
