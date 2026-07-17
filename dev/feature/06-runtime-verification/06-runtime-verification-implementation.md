# Implementation Record: Runtime Verification

## Summary

Added the Phase 04 `--runtime-deploy` integration path over the settled convergence,
destination, and managed-copy APIs. The path emits a content-bound, home-relative
inventory for review, requires its SHA-256 digest, re-inventories immediately before
mutation, deploys and reconciles by harness, and verifies expected managed assets as
fresh regular copies. Scratch-home integration covers Claude, Codex, and OpenCode,
idempotency, collisions, preserved foreign entries, failure boundaries, interceptor
retirement, surviving injection defenses, and explicit RTK. No author runtime home was
read or mutated. Live platform checks are recorded separately as `NOT RUN`, so the
cross-platform result remains partial rather than GO.

## Sibling Features

- `02-propagation-convergence`: consumed `propagate_until_converged` and
  `PropagationConvergenceResult` without duplicating fixed-point logic.
- `03-cross-platform-destinations`: consumed `resolve_destinations_after_convergence`,
  `DestinationRecord`, and the settled eight-class roster.
- `04-managed-copy-reconciliation`: consumed `deploy_managed_copies` and its per-harness
  ownership, collision, rollback, and reconciliation results.
- `05-deployment-guidance`: verified the documented convergence, inventory review,
  managed-copy, and fresh-session sequence against `--runtime-deploy`.

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | One ordered end-to-end propagation and runtime deployment path. | Complete | `scripts/propagate_master_assets.py` | `--runtime-deploy` orders convergence, preflight, inventory, recheck, deployment, reconciliation, and verification. |
| AC2 | Scratch-home Claude, Codex, and OpenCode integration. | Complete | `tests/test_phase04_runtime_deployment.py` | All mutation stays under temporary repositories and homes. |
| AC3 | Fresh classified execution inventory. | Complete for scratch evidence; live inventory NOT RUN | `scripts/runtime_deployment.py` | Classifies replacement, unchanged, collision, obsolete owned removal, and preserved foreign entries; 113 remains historical only. |
| AC4 | Managed assets are fresh regular copies with no repository links. | Complete for scratch evidence; live verification NOT RUN | `scripts/propagate_master_assets.py`; `tests/test_phase04_runtime_deployment.py` | Content identity and entry type are verified after deployment. |
| AC5 | Separate macOS, Linux, native Windows, and WSL fresh-session evidence. | NOT RUN | `scripts/propagate_master_assets.py` | Live home/runner evidence was unavailable and was not inferred from simulations. |
| AC6 | NOT RUN prevents full cross-platform GO. | Complete | `scripts/propagate_master_assets.py` | Every unavailable row includes a reason and the structured status is `partial`. |
| AC7 | Surviving scanner/framework, retired interceptors, explicit RTK. | Complete | `tests/test_phase04_runtime_deployment.py` | Retired entrypoints are absent; scanner integration remains; explicit `rtk git status --short` passed. |
| AC8 | Correct final friction, deployment, composition, and security records. | Complete | `.github/learnings/*.md`; Phase 04 documents | Generated Claude learning copies were propagated; Phase 01/02/07 ownership was not moved. |
| AC9 | Repository fixed point, deployment idempotency, explicit evidence classes. | Complete | runtime tests; learning and Phase 04 documents | Immediate propagation pass had zero changes; second scratch deployment had zero mutations; live platforms remain NOT RUN. |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `scripts/propagate_master_assets.py` | Modified | Added structured runtime orchestration, digest review gate, immediate drift check, verification reducer, CLI, and redacted JSON output. | AC1, AC4, AC6, AC9 |
| `scripts/runtime_deployment.py` | Modified | Added content-bound managed-copy inventory classification. | AC3, AC4 |
| `.github/learnings/cross-phase-decisions.md` | Modified | Recorded the verified Phase 04 runtime deployment and evidence contract. | AC8, AC9 |
| `.github/learnings/project-learnings.md` | Modified | Recorded the content-bound inventory review lesson. | AC8 |
| `claude/learnings/cross-phase-decisions.md` | Regenerated | Propagated the authoritative learning source. | AC8, AC9 |
| `claude/learnings/project-learnings.md` | Regenerated | Propagated the authoritative learning source. | AC8, AC9 |
| `docs/phases/PHASE_04/PHASE_04_DISCOVERY_CONTEXT.md` | Modified | Preserved 113 as history and recorded fresh scratch/live evidence boundaries. | AC3, AC5, AC8 |
| `docs/phases/PHASE_04/PHASE_04_SUMMARY.md` | Modified | Recorded the implemented entry point, automated evidence, and NOT RUN platforms. | AC5, AC6, AC8, AC9 |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| `tests/test_phase04_runtime_deployment.py` | Modified | Added nine orchestration, inventory, failure, idempotency, CLI, hook-retirement, and explicit-RTK tests. | AC1-AC7, AC9 |

## Test Results
- **Baseline**: 91 passed, 0 failed in the focused runtime/propagation modules
- **Final**: 100 passed, 0 failed focused; 121 passed, 0 failed full `unittest` discovery
- **New tests added**: 9
- **Regressions**: None
- **Repository fixed point**: `propagation_passes=1`, `changed_passes=0`, `propagation_changes={}`, `verification_changes={}`
- **Pytest**: NOT RUN — active Python reports `No module named pytest`
- **Live platforms**: macOS NOT RUN (author-home migration not authorized); Linux NOT RUN (runner unavailable); native Windows NOT RUN (runner unavailable); WSL NOT RUN (runner unavailable)

## Deviations from Plan

- Settled the CLI name as `--runtime-deploy`, with `--active-home`,
  `--reviewed-inventory`, and `--watcher-restarted`; no second integration module was created.
- Did not produce or execute an author-home migration inventory. The task explicitly
  limited this implementation to scratch homes, so all live evidence remains NOT RUN.
- Did not modify `tests/hooks/test_hook_distribution_integration.py`; its post-retirement
  suite already covers the surviving framework/scanner behavior. The consolidated
  unittest suite adds only final file-presence/absence and explicit RTK checks.

## Gaps

- Fresh live Claude, Codex, and OpenCode discovery on macOS, Linux, native Windows,
  and WSL remains NOT RUN and blocks a full cross-platform GO verdict.
- Native Windows junction/sharing behavior remains simulated rather than live evidence.
- Pytest-based hook integration is runner-constrained because pytest is unavailable.

## Reviewer Focus Areas

- `scripts/runtime_deployment.py::managed_copy_inventory` — confirm the deterministic
  digest covers generated-source changes and classifies links without following them.
- `scripts/propagate_master_assets.py::run_runtime_deployment` — confirm absent review,
  wrong review, convergence failure, and immediate inventory drift all stop before the
  first runtime write.
- `scripts/propagate_master_assets.py::_verify_runtime_records` — confirm expected managed
  entries must match while preserved foreign extras do not create false failures.
- CLI status reduction — review-required exits 2, partial/failure exits 1, and only a
  fully evidenced GO could exit 0.
