# Feature Context: 08-hook-framework-retirement

Phase document: `docs/phases/PHASE_05/PHASE_05_SUMMARY.md` (Deliverable 2).
Discovery context: `docs/phases/PHASE_05/PHASE_05_DISCOVERY_CONTEXT.md`.

## Key Files

### Files changed (deleted or edited)

| File | Role | Change Type |
|------|------|-------------|
| `.github/hooks/lib/framework.py` | Hook framework core (payload parsing, decisions, guards) | Delete |
| `.github/hooks/scripts/audit-log.py` | Audit-log hook script | Delete |
| `.github/hooks/scripts/audit-log.sh` | Audit-log shell wrapper | Delete |
| `.github/hooks/audit-log.json` | Audit-log hook manifest | Delete |
| `.github/hooks/lib/__pycache__/`, `.github/hooks/scripts/__pycache__/` | Stale bytecode caches | Delete |
| `tests/hooks/` (entire directory: `conftest.py`, `fixtures/`, `injection_benchmark.py`, `README.md`, `test_hook_distribution_integration.py`, `test_hook_framework.py`, `test_injection_corpus.py`, `test_injection_scanner.py`) | Hook-scoped test suite | Delete |
| `tests/test_phase04_runtime_deployment.py` | Mixed hook/deployment assertions — strip hook assertions only (12 hook references, incl. a subprocess run of `tests/hooks/injection_benchmark.py` at line ~900 and framework/scanner file-existence asserts at lines ~882–900) | Modify |
| `.github/hooks/DEFUNCT.md` [PROPOSED - name TBD] | Marker declaring the scanner intentionally inert and unimportable by design | Create |

### Read-only reference files

| File | Role |
|------|------|
| `.github/hooks/lib/injection_scanner.py` | Retained dead scanner (self-contained, no framework import) |
| `.github/hooks/lib/__init__.py` | Retained; re-exports from `.framework`, becomes unimportable after deletion (by design) |
| `.github/hooks/scripts/injection-scanner.py` | Retained dead scanner CLI (imports `from lib` / `from lib.injection_scanner`) |
| `.github/hooks/injection-scanner.json` | Retained scanner manifest |
| `.github/hooks/config/injection-patterns.json`, `.github/hooks/config/injection-allowlist.json` | Retained scanner configs |
| `docs/phases/PROJECT_ROADMAP.md` § Architecture Notes ("Defunct scanner", line ~67) | Wording the DEFUNCT marker must stay consistent with |
| `scripts/propagate_master_assets.py` | Post-deletion `--once` zero-diff evidence (modified by feature 07, not by this feature) |

## Discovery Delta

| Finding | Impact | Action |
|---------|--------|--------|
| `.github/hooks/.distribution-version` exists but has no disposition in this plan's AC1 (delete) or AC2 (retain) lists, and feature 07's plan does not mention it either. It is referenced by `scripts/propagate_master_assets.py` (lines ~1226, ~1411). | Post-state listing per AC2 cannot "match spec exactly" while an unclassified file remains; risk of stranded artifact or accidental propagator breakage | **Warning to Decomposer** — decide delete vs retain; if feature 07's pipeline removal drops the propagator references, delete it here |
| Import-coupling refinement: `lib/injection_scanner.py` does **not** import `framework.py` (contrary to the phase doc's "Scanner coupling" note). The unimportability arises via `lib/__init__.py` (re-exports `.framework`) and `scripts/injection-scanner.py` (`from lib import ...`). `lib/injection_scanner.py` itself remains importable directly. | DEFUNCT marker wording should describe the actual coupling: the package/CLI entry points are unimportable; the scanner module is inert, not literally broken | Refine marker wording; no plan-structure change |
| `done-notify.json` still present on disk at expansion time — feature 07 (wave 1) has not landed yet | Expected; plan's parenthetical "already deleted by feature 07" is true only at execution time | None — dependency ordering already enforced by manifest |
| `tests/hooks/` cross-reference confirmed: only `tests/test_phase04_runtime_deployment.py` references `tests/hooks/` (the benchmark subprocess call). No surviving test imports fixtures/helpers from `tests/hooks/`; `tests/hooks/conftest.py` deletion is collection-safe | Validates plan's edge-case B1 | None |
| Hook reference count in `tests/test_phase04_runtime_deployment.py` verified: exactly 12 case-insensitive `hook` matches, matching the plan's "~12" | Validates AC5 scope | None |
| `tests/__pycache__/` and `tests/hooks/__pycache__/` exist; deleting `tests/hooks/` should include its `__pycache__` (covered by directory delete) | None beyond thoroughness | None |
| Roadmap defunct-scanner note verified at `docs/phases/PROJECT_ROADMAP.md` § Architecture Notes; AC3 marker language should mirror it ("not part of the product and must not be counted in asset inventories", 2026-07-17 cancellation decision) | Confirms AC3 source text | None |
| `.github/hooks/DEFUNCT.md` does not exist and the name is not in the phase doc (phase says "file header or adjacent README") — `[PROPOSED - name TBD]` marker correctly applied in the plan | Implementer picks final name and records it | None |

## Architectural Decisions

- **`framework.py` is deleted**, accepting an unimportable dead scanner package. The
  phase's In Scope section lists deletion as primary; retention was only a fallback
  shape. The DEFUNCT marker must record this ("unimportable by design").
- **`lib/__init__.py` is retained** so the surviving tree stays a coherent snapshot.
  Do not add compatibility shims, stubs, or edits to make it importable.
- **DEFUNCT marker is a single small file** (or replacement of deleted README
  content), mirroring `PROJECT_ROADMAP.md`'s "Defunct scanner" architecture note.
  Feature 09 verifies the two stay consistent.
- **No new tests** — this is pure deletion; the full-suite run and post-state file
  listing are the evidence.

## Constraints

- Test entry point is `.venv/bin/python -m pytest tests/` (system python3 lacks pytest).
- The DEFUNCT marker must not claim any protection; it states inertness only, and
  that git history is the archival record (cancellation decision 2026-07-17).
- If a test function in `tests/test_phase04_runtime_deployment.py` covers both hook
  and deployment behavior, split it rather than deleting it.
- No skipped/xfailed hook tests left behind; no orphaned fixtures; no empty
  directories except those holding retained files.
- Revert path must remain a single `git revert`.

## Scope Boundaries

- Do NOT delete any AC2 file: `injection_scanner.py`, `lib/__init__.py`,
  `scripts/injection-scanner.py`, `injection-scanner.json`, `.github/hooks/config/`.
- Do NOT touch `scripts/propagate_master_assets.py`, harness configs
  (`.claude/settings.json`, `.codex/hooks.json`, `.opencode/plugins/`), or
  `tests/test_propagate_master_assets.py` — feature 07's territory.
- Do NOT touch `eval/hooks/` (planning-pipeline git hook, not a harness hook),
  `docs/inspiration/`, `docs/hooks/`, phase docs, `README.md`, or
  `cross-phase-decisions.md` — docs/record purge is feature 09.
- Do NOT modify PR Review / Phase 03 assets.

## Relationships to Sibling Plans

- **Depends on 07-propagator-hook-pipeline-removal** (wave 1): harness configs must
  be unwired and `done-notify.json` deleted before this feature deletes the scripts
  they referenced. No shared files — runtime dependency only.
- **Feeds 09-hook-record-purge**: 09 deletes the docs describing the framework this
  feature removes and verifies the roadmap defunct-scanner note against the AC3 marker.

## Suggested Implementation Order

Wave 2, parallel-safe, after 07 lands. Within the feature: Stage 1 (deletions +
test surgery + green suite) then Stage 2 (DEFUNCT marker + post-state and `--once`
zero-diff verification).

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Python 3.12, stdlib-only scripts (no framework); pytest test suite |
| Test Runner | `.venv/bin/python -m pytest tests/` |
| Test Baseline | 401 passed, 156 subtests passed, 0 failed — captured 2026-07-17 |
| Lint | Not configured |
| Format | Not configured |

## Relevant Learnings

From `.github/learnings/project-learnings.md` (hook command paths): generated hook
wiring bricked sessions when scripts resolved relative to cwd — context for why the
harness unwiring (feature 07) must precede this deletion; nothing may still reference
`.github/hooks/scripts/` at delete time.

From `.github/learnings/cross-phase-decisions.md`: mixed propagation/deployment
contract sections must survive hook scrubbing — for this feature, the analog is
`tests/test_phase04_runtime_deployment.py`: strip only hook assertions, preserve
deployment coverage.

No other entries applicable.
