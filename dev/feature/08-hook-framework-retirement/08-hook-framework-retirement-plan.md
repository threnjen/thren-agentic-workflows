# Feature Plan: 08-hook-framework-retirement

## Execution Metadata

- **Wave:** 2
- **Parallel safe:** yes
- **Depends on:** 07-propagator-hook-pipeline-removal
- **Key files modified:** `.github/hooks/lib/framework.py` (delete), `.github/hooks/scripts/audit-log.py` (delete), `.github/hooks/scripts/audit-log.sh` (delete), `.github/hooks/audit-log.json` (delete), `.github/hooks/lib/__pycache__/` + `.github/hooks/scripts/__pycache__/` (delete), `tests/hooks/` (delete entire directory), `tests/test_phase04_runtime_deployment.py`, `.github/hooks/DEFUNCT.md` [PROPOSED - name TBD] (new)
- **Sequential reason:** n/a (no shared files with 07; runtime dependency only — 07 must unwire the harness configs before the scripts they reference are deleted)

Phase document: `docs/phases/PHASE_05/PHASE_05_SUMMARY.md` (Deliverable 2). Discovery
context: `docs/phases/PHASE_05/PHASE_05_DISCOVERY_CONTEXT.md`.

## A. Requirements & Traceability

Acceptance criteria:

- **AC1**: Deleted: `.github/hooks/lib/framework.py`,
  `.github/hooks/scripts/audit-log.py`, `.github/hooks/scripts/audit-log.sh`,
  `.github/hooks/audit-log.json`, and all `__pycache__` directories under
  `.github/hooks/`. (`done-notify.json` was already deleted by feature 07.)
- **AC2**: Retained on disk, unwired: `.github/hooks/lib/injection_scanner.py`,
  `.github/hooks/lib/__init__.py`, `.github/hooks/scripts/injection-scanner.py`,
  `.github/hooks/injection-scanner.json`, `.github/hooks/config/`
  (`injection-patterns.json`, `injection-allowlist.json`).
- **AC3**: A DEFUNCT marker exists — `.github/hooks/DEFUNCT.md` [PROPOSED - name TBD]
  (or replace the deleted-by-this-feature content of any existing README) — stating:
  the scanner is intentionally inert and wired nowhere; `framework.py` was deleted, so
  while `lib/injection_scanner.py` itself does not import it, the package
  (`lib/__init__.py`) and the CLI script do — the scanner is **unrunnable by design**;
  it is not part of the product and must
  not be counted in asset inventories; git history is the archival record
  (cancellation decision 2026-07-17).
- **AC4**: `tests/hooks/` is deleted in full (framework tests, injection
  corpus/benchmark, distribution integration tests, fixtures, conftest, README).
- **AC5**: Hook assertions are stripped from `tests/test_phase04_runtime_deployment.py`
  (~12 references); its deployment assertions survive. This explicitly includes
  removing `test_explicit_rtk_guidance_remains_available` (~line 1003), which reads
  `docs/hooks/*.md` from disk and would otherwise break when feature 09 deletes
  `docs/hooks/` (feature 09's purge commit must stay docs-only). Full suite
  `.venv/bin/python -m pytest tests/` passes.

Decision recorded (per phase Notes): **`framework.py` is deleted**, accepting an
unimportable dead scanner module. The phase document's In Scope section lists the
deletion as primary; retention was only a fallback shape. The DEFUNCT marker carries
this forward (AC3).

Non-goals: propagator or harness-config changes (feature 07, already landed); docs
and record purge (feature 09); `eval/hooks/`; `docs/inspiration/`; deleting any
scanner file listed in AC2.

| Acceptance Criteria | Code Areas/Modules | Test / Evidence Category |
|---------------------|-------------------|--------------------------|
| AC1, AC2 | `.github/hooks/` tree | Code-review evidence (exact post-state file listing) |
| AC3 | `.github/hooks/DEFUNCT.md` [PROPOSED - name TBD] | Code-review evidence |
| AC4 | `tests/hooks/` | Code-review evidence (directory absent) |
| AC5 | `tests/test_phase04_runtime_deployment.py`, full suite | Existing tests to update; full-suite run is the gate |

## B. Correctness & Edge Cases

- **Pytest collection**: deleting `tests/hooks/conftest.py` must not break collection
  of the remaining `tests/` modules — verify no surviving test imports fixtures or
  helpers from `tests/hooks/` (grep before deleting).
- **Mixed test file**: `tests/test_phase04_runtime_deployment.py` mixes hook and
  deployment assertions; strip only hook assertions/parametrizations, keep deployment
  coverage intact. If a test function covers both, split it rather than deleting it.
- **Propagator source scan**: after feature 07, nothing scans `.github/hooks/` — the
  leftover dead files must not re-enter any inventory. Evidence: run `--once` after
  deletion, zero diff.

## C. Consistency & Architecture Fit

- The DEFUNCT marker mirrors the roadmap's "Defunct scanner" architecture note
  (`docs/phases/PROJECT_ROADMAP.md` § Architecture Notes) — keep the two consistent;
  feature 09 verifies.
- `.github/hooks/lib/__init__.py` is retained so the surviving tree stays a coherent
  (if unimportable-in-practice) snapshot; do not add any compatibility shims.

## D. Clean Design & Maintainability

Pure deletion plus one small marker file. Keep-it-clean: no orphaned fixtures, no
skipped/xfailed hook tests left behind, no empty directories except those holding
retained files.

## E. Observability, Security, Operability

- **Observability**: none — no code paths change.
- **Security**: the DEFUNCT marker must not claim any protection; it states inertness.
- **Runbook**: `.venv/bin/python -m pytest tests/` green; `--once` zero-diff; revert
  is a single `git revert`.

## F. Test Plan

- Must-have automated: none new beyond keeping the suite green — this feature is
  deletion; the full-suite run is the evidence.
- Existing tests to update: `tests/test_phase04_runtime_deployment.py` (strip ~12
  hook references).
- Existing tests to delete: `tests/hooks/` wholesale.
- Code-review evidence: post-state listing of `.github/hooks/` matches AC2 + marker
  exactly.
- Manual QA: none specific (covered by phase-level smoke in the manifest).
- Top evidence checks: (1) Given the full suite, When run post-deletion, Then 0
  failures/errors and no collection errors; (2) Given `.github/hooks/`, When listed,
  Then only scanner files, configs, `__init__.py`, and the marker remain; (3) Given
  `--once`, When run, Then zero diff.

## Stage 1: Framework and test deletion
**Goal**: AC1, AC4, AC5
**Success Criteria**: files gone; full suite green
**Status**: Not Started

## Stage 2: DEFUNCT marking and post-state verification
**Goal**: AC2, AC3
**Success Criteria**: marker in place; `.github/hooks/` listing matches spec; `--once` zero-diff
**Status**: Not Started

## Relationship Notes

Runs after 07 (harness configs must be unwired before the scripts they referenced are
deleted). Feature 09 deletes the docs that describe the framework this feature
removes, and verifies the roadmap's defunct-scanner note against the AC3 marker.
