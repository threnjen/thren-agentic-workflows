# Implementation Record: Managed-Copy Reconciliation

## Summary

Implemented a reusable `runtime_deployment.deploy_managed_copies` operation over the settled Feature 3 `DestinationRecord` API and exposed it through the Feature 2 convergence gate as `propagate_master_assets.deploy_managed_copies_after_convergence`. Each harness validates and stages every generated source before mutation, verifies staged content by SHA-256 manifest, replaces only positively owned entries, preserves foreign collisions, and prunes only after all installs for that harness succeed. Generated markers, repository-targeting link records, and hash-bound deployment metadata provide ownership evidence. Replacement uses a sibling backup and identity recheck, never follows a destination link for deletion, and restores the prior entry when installation fails.

## Sibling Features

- Consumes `02-propagation-convergence`'s `PropagationConvergenceResult` and fixed-point rejection contract.
- Consumes `03-cross-platform-destinations`'s `DestinationRecord`, including its source, destination, and active-home boundaries.
- Exposes the shared managed-copy operation and structured per-harness counters for `05-deployment-guidance` and `06-runtime-verification`; downstream features do not need to reimplement ownership or destination resolution.
- Preserves the interceptor retirement from Feature 1 and does not use retired guard metadata as ownership evidence.

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | Reusable API stages complete replacements before replacement | Implemented | `scripts/runtime_deployment.py`, `scripts/propagate_master_assets.py` | All records in a harness stage and verify before that harness mutates. |
| AC2 | Ownership exists independently of destination existence | Implemented | `scripts/runtime_deployment.py` | Generated markers and hash-bound `.github-agents-managed.json` metadata establish positive ownership. |
| AC3 | Replace only repository-owned links/junctions without traversing deletion | Implemented; native Windows verification pending | `scripts/runtime_deployment.py` | Uses `lstat`, recorded targets, `Path.is_junction`, and entry-only unlink/rename behavior. |
| AC4 | Handle owned dangling links for current and obsolete outputs | Implemented | `scripts/runtime_deployment.py` | Recorded relative/absolute targets are classified with `strict=False`; expected links are replaced and obsolete owned links are pruned. |
| AC5 | Whole roots and per-entry links become regular copies | Implemented | `scripts/runtime_deployment.py` | Verified staged trees replace owned root links; owned child links become regular files/directories. |
| AC6 | Preserve and report foreign content and links | Implemented | `scripts/runtime_deployment.py` | Unknown files, directories, links, unreadable entries, and stale metadata mismatches fail closed as collisions. |
| AC7 | Prune only proven-owned stale copies | Implemented | `scripts/runtime_deployment.py` | The overwrite and prune paths share marker, recorded-link, and hash-bound metadata evidence. |
| AC8 | Failed copy/verification preserves prior state and suppresses pruning | Implemented | `scripts/runtime_deployment.py` | Harness-wide staging precedes mutation; install failures restore backups and skip harness pruning. |
| AC9 | Locked/sharing failures preserve existing destination | Implemented; native Windows verification pending | `scripts/runtime_deployment.py` | Permission/replacement errors are categorized without sensitive exception text; simulated locked replacement passes. |
| AC10 | Repeated deployment is idempotent and leaves regular copies | Implemented | `scripts/runtime_deployment.py` | Content manifests produce unchanged outcomes; link conversion and second-run behavior are tested. |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `scripts/runtime_deployment.py` | Modified | Added managed-copy result models, non-following classification, marker/metadata ownership, verified staging, recoverable replacement, collision handling, harness-gated pruning, and idempotency checks. | Implements AC1-AC10 at the user-global mutation boundary. |
| `scripts/propagate_master_assets.py` | Modified | Added `deploy_managed_copies_after_convergence`. | Makes the settled operation callable only after verified repository convergence. |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| `tests/test_phase04_runtime_deployment.py` | Modified | Added 12 scratch-home tests for absent copies, live/dangling links, collisions, owned-only pruning, staged and replacement failures, stale metadata, mixed harnesses, convergence gating, active-home refusal, and idempotency. | AC1-AC10; Windows failure behavior is simulated, not live evidence. |

## Test Results
- **Baseline**: 67 passed, 0 failed via focused `unittest` modules before the feature tests; pytest unavailable in the active Python.
- **Final**: 79 passed, 0 failed in focused modules; 100 passed, 0 failed with `python3 -m unittest discover -s tests`.
- **New tests added**: 12
- **Regressions**: None
- **Pytest command**: `python3 -m pytest tests/test_phase04_runtime_deployment.py tests/test_propagate_master_assets.py -q` was `NOT RUN` because the active Python reports `No module named pytest`.

## Deviations from Plan

- Settled API names are `deploy_managed_copies`, `ManagedCopyResult`, and `HarnessManagedCopyResult`; no additional module was introduced because Feature 3 had already established `scripts/runtime_deployment.py` as the shared destination boundary.
- Deployment metadata is a hash-bound per-destination JSON file instead of name-only metadata, so a user replacement at a formerly managed path is preserved as a collision.
- Windows junction and sharing-violation coverage is limited to platform-adapter/error simulation on this macOS runner. Native evidence remains assigned to Feature 6.
- No author-home migration or watcher restart was performed. All mutation tests use temporary injected homes; watcher restart belongs to release/runtime evidence rather than unit implementation.

## Gaps

- Native Windows junction/reparse-point behavior, sharing violations, and WSL operation are `NOT RUN` on this macOS host and require Feature 6 runtime evidence.
- Pytest-specific execution and coverage reporting are `NOT RUN` because pytest is not installed in the active Python; the equivalent focused and full unittest suites pass.

## Reviewer Focus Areas

- `scripts/runtime_deployment.py` ownership decisions: confirm marker evidence and hash-bound metadata fail closed for edited or foreign content.
- `scripts/runtime_deployment.py` replacement path: confirm the identity recheck, sibling backup, restoration, and cleanup never traverse destination links.
- `scripts/runtime_deployment.py` harness transaction boundary: confirm every stage succeeds before mutation and pruning is skipped after any staging/install failure.
- Native Windows adapter behavior remains runner-constrained; confirm `Path.is_junction`, `os.readlink` fallback, and `os.replace` error handling are appropriately conservative.
