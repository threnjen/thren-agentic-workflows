# Phase 05 Execution Manifest: Hook Removal

**Phase document**: `docs/phases/PHASE_05/PHASE_05_SUMMARY.md`
**Discovery context**: `docs/phases/PHASE_05/PHASE_05_DISCOVERY_CONTEXT.md`
**Test runner**: `.venv/bin/python -m pytest tests/` (baseline 2026-07-17: 401 passed, 156 subtests, 0 failed)

## Feature List (execution order)

1. `07-propagator-hook-pipeline-removal`
2. `08-hook-framework-retirement`
3. `09-hook-record-purge`

Ordering matches the Phase document's Key Deliverables sequence exactly.

## Feature Table

| Feature | Wave | Parallel Safe | Depends On | Key Files Modified | Sequential Reason |
|---|---|---|---|---|---|
| `07-propagator-hook-pipeline-removal` | 1 | yes | none | `scripts/propagate_master_assets.py`, `tests/test_propagate_master_assets.py`, `.github/hooks/done-notify.json` (delete), `.github/hooks/.distribution-version` (delete), `.claude/settings.json`, `.codex/hooks.json`, `.opencode/plugins/done-notify.js`, `.opencode/plugins/audit-log.js` (delete), `.opencode/plugins/injection-scanner.js` (delete) | n/a |
| `08-hook-framework-retirement` | 2 | yes | `07-propagator-hook-pipeline-removal` | `.github/hooks/lib/framework.py` (delete), `.github/hooks/scripts/audit-log.py` (delete), `.github/hooks/scripts/audit-log.sh` (delete), `.github/hooks/audit-log.json` (delete), `.github/hooks/**/__pycache__/` (delete), `tests/hooks/` (delete), `tests/test_phase04_runtime_deployment.py`, `.github/hooks/DEFUNCT.md` [PROPOSED - name TBD] (new) | n/a — no shared files with 07; runtime dependency only (07 must unwire harness configs before the referenced scripts are deleted) |
| `09-hook-record-purge` | 3 | yes | `07-propagator-hook-pipeline-removal`, `08-hook-framework-retirement` | `docs/phases/PHASE_01/` (delete), `docs/phases/PHASE_02/` (delete), `docs/phases/PHASE_04/` (delete), `docs/hooks/` (delete), `.github/learnings/cross-phase-decisions.md`, `claude/learnings/cross-phase-decisions.md` (regenerated via propagator), `README.md`, `docs/ARCHITECTURE.md`, `docs/CODEBASE_CONTEXT.md`, `docs/TROUBLESHOOTING.md`, `HARNESS_SETUP.md`, `docs/LOCAL_DEVELOPMENT.md`, `docs/phases/PROJECT_ROADMAP.md` (verify) | n/a — no shared files with 07/08; runtime dependency (docs must describe the final tree; count reconciliation needs the final inventory). Must land as a single dedicated commit. |

## Execution Schedule

- **Wave 1 (sequential — single feature)**: `07-propagator-hook-pipeline-removal`
- **Wave 2 (sequential — single feature)**: `08-hook-framework-retirement`
- **Wave 3 (sequential — single feature)**: `09-hook-record-purge`

Each wave contains one feature; no parallel execution occurs in this phase. The
dependency chain is strict: 07 → 08 → 09.

## Expected Bundle Files

- `dev/feature/07-propagator-hook-pipeline-removal/07-propagator-hook-pipeline-removal-{plan,context,tasks}.md`
- `dev/feature/08-hook-framework-retirement/08-hook-framework-retirement-{plan,context,tasks}.md`
- `dev/feature/09-hook-record-purge/09-hook-record-purge-{plan,context,tasks}.md`

## Decisions Made at Decomposition

- **`framework.py` deleted** (feature 08): the retained scanner is unrunnable by
  design; the DEFUNCT marker records this. Retention was the fallback shape and was
  not chosen.
- **`.codex/config.toml`**: verified to contain no hook entries — the phase's "if
  any" clause resolves to no work.
- **`.github/hooks/.distribution-version`**: deleted in feature 07 with the propagator
  code that reads it (hook-distribution state, not scanner code).
- **`test_explicit_rtk_guidance_remains_available`** (reads `docs/hooks/*.md`) is
  removed in feature 08 so feature 09's record-purge commit stays docs-only.
- Hook-emission tests are deleted, not retargeted (phase directive); only small
  done-notify non-interference assertions are added.

## Verification Assets

### New Test Files

| Path | Associated Feature(s) | Purpose |
|---|---|---|
| None identified — new assertions land inside the existing `tests/test_propagate_master_assets.py` | `07-propagator-hook-pipeline-removal` | Done-notify non-interference (propagator neither prunes nor rewrites the static entries) |

### Existing Test Files Updated By Multiple Features

| Path | Associated Feature(s) | Purpose |
|---|---|---|
| None — test-file scopes are disjoint by design (`test_propagate_master_assets.py` → 07 only; `tests/hooks/` + `test_phase04_runtime_deployment.py` → 08 only) | — | — |

### Manual QA Checklist

- [ ] Run `scripts/propagate_master_assets.py --once` twice after each feature; the second run must produce zero `git diff` (static done-notify wiring byte-identical).
- [ ] Fresh harness session in this repo: no hook fires; the done-notify desktop notification still appears at Stop.
- [ ] `.github/hooks/` post-08 listing contains only scanner files, configs, `lib/__init__.py`, and the DEFUNCT marker.
- [ ] Three-way doc-count reconciliation across README / ARCHITECTURE / CODEBASE_CONTEXT after feature 09.
- [ ] Surviving decision-log sections (Propagation Contracts, Phase 04 Runtime Deployment Contract, Deferred Pipeline Work remainder) read intact after the feature 09 scrub.
- [ ] `eval/hooks/post-commit.sh` and `docs/inspiration/` unchanged (`git status` clean for those paths).
