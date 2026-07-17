# Tasks: 08-hook-framework-retirement

## Stage 1: Framework and test deletion (AC1, AC4, AC5)

- [ ] Confirm feature 07 has landed: harness configs unwired and `.github/hooks/done-notify.json` gone; abort and report if not
- [ ] Grep `tests/` (excluding `tests/hooks/`) for any import or path reference to `tests/hooks/` fixtures/helpers; confirm only `tests/test_phase04_runtime_deployment.py` references it
- [ ] Delete `.github/hooks/lib/framework.py`
- [ ] Delete `.github/hooks/scripts/audit-log.py` and `.github/hooks/scripts/audit-log.sh`
- [ ] Delete `.github/hooks/audit-log.json`
- [ ] Delete `.github/hooks/lib/__pycache__/` and `.github/hooks/scripts/__pycache__/`
- [ ] Resolve `.github/hooks/.distribution-version` disposition per Decomposer decision (Discovery Delta warning) and delete or retain accordingly
- [ ] Delete `tests/hooks/` in full (framework tests, injection corpus/benchmark, distribution integration tests, fixtures, conftest, README, `__pycache__`)
- [ ] Strip the 12 hook references from `tests/test_phase04_runtime_deployment.py` (framework/scanner existence asserts ~lines 882–900, `tests/hooks/injection_benchmark.py` subprocess run ~line 900, retired-asset path list entries), splitting any test that mixes hook and deployment assertions; keep all deployment coverage
- [ ] Confirm no skipped/xfailed hook tests or orphaned fixtures remain anywhere in `tests/`
- [ ] Run `.venv/bin/python -m pytest tests/` — 0 failures, 0 collection errors (baseline: 401 passed + 156 subtests)

## Stage 2: DEFUNCT marking and post-state verification (AC2, AC3)

- [ ] Create `.github/hooks/DEFUNCT.md` [PROPOSED - name TBD] stating: the scanner is intentionally inert and wired nowhere; `framework.py` was deleted so the package/CLI entry points (`lib/__init__.py`, `scripts/injection-scanner.py`) are unimportable by design; it is not part of the product and must not be counted in asset inventories; git history is the archival record (cancellation decision 2026-07-17); no claim of protection
- [ ] Keep marker wording consistent with `docs/phases/PROJECT_ROADMAP.md` § Architecture Notes "Defunct scanner"
- [ ] Verify `.github/hooks/` post-state listing contains exactly: `lib/injection_scanner.py`, `lib/__init__.py`, `scripts/injection-scanner.py`, `injection-scanner.json`, `config/injection-patterns.json`, `config/injection-allowlist.json`, the DEFUNCT marker, and the resolved `.distribution-version` outcome — nothing else
- [ ] Verify AC2 retained files are byte-identical (no shims or edits added)
- [ ] Run `scripts/propagate_master_assets.py --once` and confirm zero diff (no re-inventoried hook artifacts)
- [ ] Re-run `.venv/bin/python -m pytest tests/` — full suite green; record results and final marker filename in implementation notes
