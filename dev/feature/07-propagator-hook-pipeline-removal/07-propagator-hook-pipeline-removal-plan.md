# Feature Plan: 07-propagator-hook-pipeline-removal

## Execution Metadata

- **Wave:** 1
- **Parallel safe:** yes
- **Depends on:** none
- **Key files modified:** `scripts/propagate_master_assets.py`, `tests/test_propagate_master_assets.py`, `.github/hooks/done-notify.json` (delete), `.github/hooks/.distribution-version` (delete), `.claude/settings.json`, `.codex/hooks.json`, `.opencode/plugins/done-notify.js`, `.opencode/plugins/audit-log.js` (delete), `.opencode/plugins/injection-scanner.js` (delete)
- **Sequential reason:** n/a

Phase document: `docs/phases/PHASE_05/PHASE_05_SUMMARY.md` (Deliverable 1). Discovery
context: `docs/phases/PHASE_05/PHASE_05_DISCOVERY_CONTEXT.md`.

## A. Requirements & Traceability

Acceptance criteria:

- **AC1**: `scripts/propagate_master_assets.py` contains no hook emission, translation,
  or source-discovery code. All of the following symbols are deleted: `HOOK_EVENT_MAP`,
  `HOOK_SOURCE_KEY`, `RETIRED_HOOK_ASSETS`, `RETIRED_HOOK_ASSET_HASHES`,
  `_resolve_hook_events`, `_resolve_hook_command`, `_project_root_hook_command`,
  `HOOK_PROJECT_ROOT_TOKENS`, `_strip_propagated_hooks`,
  `GENERATED_OPENCODE_PLUGIN_HEADER`, the `.github/hooks/` source discovery, and the
  `hooks_source` inventory counter (including its entry in `INVENTORY_COUNTERS`).
  Retired-asset pruning of former hook outputs either completes cleanly or is removed
  along with the pipeline — implementer's call, provided AC4 holds.
  `.github/hooks/.distribution-version` (referenced by the propagator at ~lines
  1226/1411) is deleted along with the code that reads it — it is hook-distribution
  state, not scanner code.
  Note: hook-emission test surgery extends beyond name-matched tests — phase02 /
  global-setup / scanner distribution tests exercise emission without "hook" in their
  names; sweep by behavior, not by name.
- **AC2**: `.github/hooks/done-notify.json` is deleted. The done-notify wiring is
  committed as static config with **no `$source` key**: the Stop/Notification entries
  in `.claude/settings.json`, the Stop entry in `.codex/hooks.json`, and
  `.opencode/plugins/done-notify.js` (with the generated-file header comment removed).
  The notification command content is preserved as-is from the current generated
  output.
- **AC3**: All other hook wiring is removed: the audit-log and injection-scanner
  entries in `.claude/settings.json` and `.codex/hooks.json`, and the files
  `.opencode/plugins/audit-log.js` and `.opencode/plugins/injection-scanner.js`.
  Untagged non-hook-project entries (code-review-graph PostToolUse/SessionStart
  entries) are preserved byte-identical.
- **AC4**: `scripts/propagate_master_assets.py --once` converges: it emits no hook
  outputs, strands no hook artifacts in any generated root, and a second `--once` run
  produces zero diff — in particular the static done-notify wiring is byte-identical
  after both runs.
- **AC5**: Hook-emission tests in `tests/test_propagate_master_assets.py` are deleted
  (not retargeted). New assertions are added that the propagator leaves the static
  done-notify entries untouched and never prunes them (scenario: run propagation over
  a settings file containing the untagged done-notify entry; assert the entry survives
  unchanged). `.venv/bin/python -m pytest tests/test_propagate_master_assets.py`
  passes. (`tests/test_phase04_runtime_deployment.py` and `tests/hooks/` are feature
  08's scope; the full-suite green gate lands there.)

Non-goals: deleting `.github/hooks/` scanner/audit-log files or `tests/hooks/`
(feature 08); any docs changes (feature 09); `eval/hooks/`; `scripts/runtime_deployment.py`
(never shipped hooks); `.codex/config.toml` (verified to contain no hook entries).

| Acceptance Criteria | Code Areas/Modules | Test / Evidence Category |
|---------------------|-------------------|--------------------------|
| AC1 | `scripts/propagate_master_assets.py` | Code-review evidence (symbol absence grep) + surviving suite passes |
| AC2 | `.github/hooks/done-notify.json`, `.claude/settings.json`, `.codex/hooks.json`, `.opencode/plugins/done-notify.js` | Code-review evidence + manual QA (Stop notification fires) |
| AC3 | `.claude/settings.json`, `.codex/hooks.json`, `.opencode/plugins/audit-log.js`, `.opencode/plugins/injection-scanner.js` | Code-review evidence (grep for `$source`, `audit-log`, `injection-scanner` in configs) |
| AC4 | propagator `--once` runs | Manual QA: double `--once`, `git diff` empty second run |
| AC5 | `tests/test_propagate_master_assets.py` | Existing tests to delete + must-have new automated non-interference tests [PROPOSED - names TBD] |

## B. Correctness & Edge Cases

- **Interleaving risk**: hook emission is interleaved with agent/skill/command/learning
  propagation (settings writer at ~line 1196, opencode writer at ~1446, inventory at
  ~1393/1767). Delete surgically; every non-hook propagation path must survive. The
  surviving test suite is the guard.
- **Foreign-entry preservation**: current `_strip_propagated_hooks` removes only
  `$source`-tagged entries — once the static done-notify entries lose their `$source`
  tag, the historical merge logic would have left them alone. After this feature the
  propagator must not touch the `hooks` key of `.claude/settings.json` at all (verify:
  if the settings writer rewrites the whole file for agent/skill reasons, it must
  round-trip the `hooks` block unchanged).
- **Orphan pruning edge**: with `.github/hooks/` no longer a discovered source, ensure
  the pruning pass does not classify the static done-notify plugin
  `.opencode/plugins/done-notify.js` as an orphan. The generated-file header is
  removed from it precisely so header-based ownership checks skip it — verify the
  ownership check is header-based before relying on this.
- **Ordering within the feature**: delete emission + convert to static in one change
  so no intermediate state has wiring pointing at deleted scripts.

## C. Consistency & Architecture Fit

- Follow the existing retirement pattern from Phase 04 (see
  `tests/test_retired_evaluator_removal.py` for the shape of absence-assertions), but
  note the phase directive: hook-emission tests are deleted, not converted into a
  large retirement suite — only the small done-notify non-interference assertions are
  added.
- Static config contract (consumed by features 08/09 and by the manifest's QA):
  done-notify entries carry no `$source` key and no generated header; they are
  hand-owned. This is the cross-feature contract — feature 09's docs describe it.
- No new config keys, no new APIs. All named symbols above verified in codebase
  (`scripts/propagate_master_assets.py` lines 61–143, 1058–1214, 1273–1302,
  1393–1481, 1767).

## D. Clean Design & Maintainability

Simplest design: pure deletion plus one static-config commit. Keep-it-clean checklist:
no commented-out hook code left behind; no `hook` identifiers surviving in the
propagator except incidental words in unrelated strings; `INVENTORY_COUNTERS` reduced
to `{"source_agents"}`; imports pruned.

## E. Observability, Security, Operability

- **Observability**: no new logs. The propagator's existing summary output simply
  loses its `hooks_source` line.
- **Security**: this removes the (dead) security-hook claim surface; nothing new.
- **Runbook**: run `--once` twice, `git diff` must be empty on the second; restart any
  long-running `--watch` process after merging (watchers execute the code they started
  with).

## F. Test Plan

- Must-have automated: new done-notify non-interference assertions in
  `tests/test_propagate_master_assets.py` [PROPOSED - names TBD] — (1) Given a
  settings file with the untagged done-notify Stop entry, When propagation runs, Then
  the entry is byte-identical; (2) Given `.opencode/plugins/done-notify.js` without
  the generated header, When pruning runs, Then the file survives.
- Existing tests to delete: all hook-emission/translation/pruning tests in
  `tests/test_propagate_master_assets.py` (~148 hook references).
- Code-review evidence: grep for the AC1 symbol list returns nothing.
- Manual QA: double `--once` convergence; fresh Claude session — no hook fires,
  Stop notification appears.
- Fixtures: existing tmp-root propagation fixtures in the suite are reused for the
  new assertions.

## Stage 1: Propagator surgery + static done-notify conversion
**Goal**: AC1–AC3 in a single coherent change
**Success Criteria**: symbol list absent; static config in place; other wiring gone
**Status**: Not Started

## Stage 2: Test surgery and convergence verification
**Goal**: AC4–AC5
**Success Criteria**: propagation suite green; double `--once` zero-diff
**Status**: Not Started

## Relationship Notes

Feature 08 depends on this feature at runtime: it deletes the audit-log/scanner
scripts that the harness configs reference until this feature unwires them. Feature 09
documents the end state this feature creates.
