# Implementation Record: 08-hook-framework-retirement

## Summary

Retired the hook framework by pure deletion plus one marker file. Deleted the framework
core (`lib/framework.py`), the audit-log hook (script, shell wrapper, manifest), and all
`__pycache__` under `.github/hooks/` (AC1). Retained the injection scanner tree on disk,
unwired (AC2). Added `.github/hooks/DEFUNCT.md` declaring the scanner intentionally
inert and unrunnable by design (AC3). Deleted `tests/hooks/` in full (AC4). Stripped all
hook assertions from `tests/test_phase04_runtime_deployment.py` while preserving every
deployment assertion (AC5). Full suite is green; `--once` re-inventories no hook
artifacts (zero diff); post-state listing matches AC2 + marker exactly.

## Sibling Features

- **07-propagator-hook-pipeline-removal** (wave 1, dependency): unwired harness configs
  and removed `done-notify.json` before this feature deleted the scripts they
  referenced. Confirmed landed: `done-notify.json` absent; no propagator reference to
  `.distribution-version` (which does not exist on disk — no disposition needed).
- **09-hook-record-purge** (wave 3, consumer): deletes `docs/hooks/` and phase docs, and
  verifies the roadmap "Defunct scanner" note against this feature's AC3 marker. My AC5
  removal of `test_explicit_rtk_guidance_remains_available` (which read `docs/hooks/*.md`)
  clears 09's path to a docs-only deletion. Marker wording mirrors
  `docs/phases/PROJECT_ROADMAP.md` § Architecture Notes.
- No files modified for a sibling's sole benefit.

## AC Coverage Matrix

| AC | Criterion ID | Planned Test ID | Planned Test Pattern | Status | Implementing Files | Evidence Paths | Implement Commit SHA | Review Commit SHA |
|----|--------------|-----------------|----------------------|--------|--------------------|----------------|----------------------|-------------------|
| AC1 | AC1 | n/a (deletion; code-review evidence) | Post-state file listing | Done | `.github/hooks/lib/framework.py`, `.github/hooks/scripts/audit-log.py`, `.github/hooks/scripts/audit-log.sh`, `.github/hooks/audit-log.json`, `__pycache__/` | `git status --short .github/hooks/` shows the four deletions; no `__pycache__` under `.github/hooks/` | PENDING | PENDING |
| AC2 | AC2 | n/a (code-review evidence) | Retained-file listing byte-identical | Done | `.github/hooks/lib/injection_scanner.py`, `lib/__init__.py`, `scripts/injection-scanner.py`, `injection-scanner.json`, `config/*.json` | `find .github/hooks -type f` listing; `git status --short` shows AC2 files unmodified | PENDING | PENDING |
| AC3 | AC3 | n/a (code-review evidence) | Marker content present | Done | `.github/hooks/DEFUNCT.md` | `.github/hooks/DEFUNCT.md` | PENDING | PENDING |
| AC4 | AC4 | n/a (code-review evidence) | Directory absent | Done | `tests/hooks/` (deleted) | `find tests/hooks` returns nothing; `git status` shows 11 file deletions | PENDING | PENDING |
| AC5 | AC5 | Full suite `.venv/bin/python -m pytest tests/` | Suite green, no collection errors | Done | `tests/test_phase04_runtime_deployment.py` | pytest output 237 passed; no `hook`/`docs/hooks` matches remain in the file | PENDING | PENDING |

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | Delete framework.py, audit-log script/shell/manifest, all `__pycache__` under `.github/hooks/` | Done | (deleted files listed above) | `done-notify.json` already removed by feature 07 |
| AC2 | Retain injection scanner tree unwired | Done | scanner files, `__init__.py`, `injection-scanner.json`, `config/` | Byte-identical; no shims added |
| AC3 | DEFUNCT marker declaring scanner inert/unrunnable | Done | `.github/hooks/DEFUNCT.md` | Mirrors roadmap note; no protection claim; git history is archival record |
| AC4 | Delete `tests/hooks/` in full | Done | `tests/hooks/` | Confirmed only `test_phase04_runtime_deployment.py` referenced it (benchmark subprocess); collection-safe |
| AC5 | Strip ~12 hook assertions from `test_phase04_runtime_deployment.py`; deployment coverage intact | Done | `tests/test_phase04_runtime_deployment.py` | Removed 2 hook-scoped tests + unused `runpy` import |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `.github/hooks/lib/framework.py` | Delete | Hook framework core removed | AC1 — framework retirement |
| `.github/hooks/scripts/audit-log.py` | Delete | Audit-log hook script removed | AC1 |
| `.github/hooks/scripts/audit-log.sh` | Delete | Audit-log shell wrapper removed | AC1 |
| `.github/hooks/audit-log.json` | Delete | Audit-log hook manifest removed | AC1 |
| `.github/hooks/lib/__pycache__/`, `.github/hooks/scripts/__pycache__/` | Delete | Stale bytecode caches removed | AC1 |
| `.github/hooks/DEFUNCT.md` | Create | Marker declaring scanner intentionally inert, unrunnable by design, not counted in inventories, git history is archival record | AC3 |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| `tests/hooks/` (11 files + `__pycache__`) | Delete | Entire hook-scoped test suite removed | AC4 |
| `tests/test_phase04_runtime_deployment.py` | Modify | Removed `test_retired_interceptors_are_absent_while_scanner_framework_remains` (asserted deleted `framework.py` exists and ran the deleted `tests/hooks/injection_benchmark.py`) and `test_explicit_rtk_guidance_remains_available` (read `docs/hooks/*.md`); removed now-unused `runpy` import | AC5 |

## Test Results
- **Baseline** (feature-level, pre-pass): non-hook suite 239 passed, 141 subtests (the 4 errors + 1 failure in `tests/hooks/` were pre-existing from feature 07 unwiring configs, and that directory is deleted by AC4)
- **Final**: 237 passed, 134 subtests passed, 0 failed, 0 collection errors
- **New tests added**: 0 (pure deletion; full-suite run is the evidence)
- **Regressions**: None (delta = 2 removed hook tests + 7 removed hook subtests)

## Deviations from Plan
- `.github/hooks/.distribution-version` does not exist on disk and has no propagator
  reference (grep of `scripts/propagate_master_assets.py` returns nothing), so the
  Discovery Delta "delete vs retain" decision is moot — no action needed. Post-state
  listing matches AC2 + marker with nothing extra.
- The two AC5 tests were removed rather than split: both are entirely hook-scoped (hook
  file-existence asserts, the deleted benchmark subprocess, and `docs/hooks/*.md` reads).
  Neither contained a deployment assertion to preserve, so a split would leave an empty
  body. Every genuine deployment test in the file is untouched.

## Gaps
None.

## Reviewer Focus Areas
- `.github/hooks/` post-state (`find .github/hooks -type f`) must contain exactly the six
  AC2 files plus `DEFUNCT.md` — confirm nothing stray remains.
- `tests/test_phase04_runtime_deployment.py` — confirm only hook assertions were removed
  and all deployment/reconciliation/guidance tests still run (237 passed).
- `.github/hooks/DEFUNCT.md` wording vs `docs/phases/PROJECT_ROADMAP.md` § Architecture
  Notes "Defunct scanner" — must stay consistent (feature 09 verifies) and claim no
  protection.
- `--once` zero-diff: confirm no hook artifact re-enters any inventory.
