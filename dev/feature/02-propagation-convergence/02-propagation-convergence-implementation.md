# Implementation Record: Propagation Convergence

## Summary

Added a bounded, verified repository propagation API and centralized mutation classification without changing the one-pass `propagate_once` contract. Added a convergence-gated deployment boundary with full-set destination preflight, active-home containment, structured per-harness outcomes, and isolated failure behavior. The CLI and watcher now use bounded convergence, and the watcher states the restart requirement for migration and release verification.

## Sibling Features

- Depends on `01-interceptor-retirement` and uses its final propagation counters, including explicit retirement-removal counters.
- Exposes `HarnessDestination`, `preflight_destinations`, and `deploy_after_convergence` for `03-cross-platform-destinations` and `04-managed-copy-reconciliation` to supply policy and mutation operations without duplicating convergence.
- Supplies the watcher restart wording consumed by `05-deployment-guidance`.
- Leaves the consolidated cross-feature runtime scenarios to `06-runtime-verification` because `tests/test_phase04_runtime_deployment.py` does not yet exist.

## AC Coverage Matrix

| AC | Criterion ID | Planned Test ID | Planned Test Pattern | Status | Implementing Files | Evidence Paths | Implement Commit SHA | Review Commit SHA |
|----|--------------|-----------------|----------------------|--------|--------------------|----------------|----------------------|-------------------|
| AC1 | AC1 | `test_convergence_requires_an_immediate_zero_change_pass`; `test_convergence_exhaustion_includes_pass_count`; fixed-point regressions | Multi-pass convergence, immediate zero verification, bounded exhaustion | Complete | `scripts/propagate_master_assets.py` | `tests/test_propagate_master_assets.py`; `tests/test_retirement_reconciliation.py` | PENDING | PENDING |
| AC2 | AC2 | `test_convergence_requires_an_immediate_zero_change_pass` | Reusable public convergence API | Complete | `scripts/propagate_master_assets.py` | `scripts/propagate_master_assets.py` (`propagate_until_converged`) | PENDING | PENDING |
| AC3 | AC3 | `test_convergence_fails_closed_for_exception_and_malformed_result`; `test_convergence_exhaustion_includes_pass_count`; `test_preflight_rejects_unsafe_destinations_before_any_copy`; `test_global_cli_converges_before_mutating_user_output` | Failure and malformed-result gates block preflight/mutation | Complete | `scripts/propagate_master_assets.py` | `tests/test_propagate_master_assets.py` | PENDING | PENDING |
| AC4 | AC4 | Existing direct `propagate_once` suite; fixed-point regressions | One-pass compatibility plus bounded CLI path | Complete | `scripts/propagate_master_assets.py` | `tests/test_propagate_master_assets.py`; `tests/test_retirement_reconciliation.py` | PENDING | PENDING |
| AC5 | AC5 | `test_preflight_rejects_unsafe_destinations_before_any_copy`; `test_preflight_reports_missing_parent_evidence_and_collision` | Scratch-home containment, symlink escape, parent, ownership, collision checks | Complete | `scripts/propagate_master_assets.py` | `tests/test_propagate_master_assets.py` | PENDING | PENDING |
| AC6 | AC6 | `test_failed_harness_skips_only_its_reconciliation` | Successful harness retained; failed harness skips reconciliation | Complete | `scripts/propagate_master_assets.py` | `tests/test_propagate_master_assets.py` | PENDING | PENDING |
| AC7 | AC7 | `test_watcher_announces_restart_requirement` | Watcher startup requires restart after propagator changes | Complete | `scripts/propagate_master_assets.py` | `tests/test_propagate_master_assets.py`; watcher startup output | PENDING | PENDING |
| AC8 | AC8 | Convergence, preflight, partial-failure, and CLI tests above | Structured pass/change/failure/copy/reconciliation evidence with redacted failures | Complete | `scripts/propagate_master_assets.py` | `tests/test_propagate_master_assets.py` | PENDING | PENDING |

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | Repeat propagation within a bound through an immediate zero-change verification pass. | Complete | `scripts/propagate_master_assets.py` | Default bound is 5 total passes; validated maximum is 25. |
| AC2 | Provide one reusable public convergence API. | Complete | `scripts/propagate_master_assets.py` | Public API selected as `propagate_until_converged`. |
| AC3 | Block preflight and mutation on failed or incomplete convergence. | Complete | `scripts/propagate_master_assets.py` | Deployment returns a structured propagation failure; CLI exits before global generation. |
| AC4 | Preserve `propagate_once` while deployment-capable CLI paths converge. | Complete | `scripts/propagate_master_assets.py` | Direct callers retain one-pass behavior. |
| AC5 | Validate active home, parents, ownership evidence, and collision readiness. | Complete | `scripts/propagate_master_assets.py` | All intended destinations are checked before the first callback. |
| AC6 | Isolate deployment results by harness. | Complete | `scripts/propagate_master_assets.py` | Copy failure skips only that harness's reconciliation and does not roll back prior success. |
| AC7 | Require stale watcher restart before migration/release verification. | Complete | `scripts/propagate_master_assets.py` | Exact requirement is printed when the watcher starts. |
| AC8 | Return structured, redacted propagation and harness outcomes. | Complete | `scripts/propagate_master_assets.py` | Failure categories omit exception text, paths, and content. |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `scripts/propagate_master_assets.py` | Modified | Added centralized counter classification, bounded convergence, destination preflight, deployment result models, CLI convergence gating, and watcher restart guidance. | Implements AC1–AC8 while preserving the one-pass primitive and sibling-feature boundaries. |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| `tests/test_propagate_master_assets.py` | Modified | Added nine convergence, preflight, harness-isolation, CLI-gate, redaction, and watcher tests. | AC1–AC8 |
| `tests/test_retirement_reconciliation.py` | Modified | Reused the production `propagation_changes` classifier in existing fixed-point regressions. | AC1, AC4, AC8 |

## Test Results
- **Baseline**: 66 passed, 45 subtests passed (before implementation)
- **Final**: 75 passed, 49 subtests passed
- **New tests added**: 9 test methods (including 4 invalid-bound subtests)
- **Regressions**: None
- **Additional verification**: Real `.venv/bin/python scripts/propagate_master_assets.py --once` completed with convergence JSON and zero verification changes; `py_compile` and `git diff --check` passed.

## Deviations from Plan

- Did not create `tests/test_phase04_runtime_deployment.py`; the plan explicitly made this conditional, and the shared file does not exist yet. Cross-feature scenarios remain handed off to Feature 6.
- Did not modify `.vscode/tasks.json`; the existing watch task invokes the updated watcher, and the restart requirement is emitted directly at watcher startup.
- The CLI's `--global-output` is a repository-derived staging-output generator used by the existing setup script, not the destination-record contract. It is convergence-gated, while active-home destination preflight remains on `deploy_after_convergence` for Features 3–4 to invoke with real destination records.

## Gaps

None within this feature's scope. Platform destination selection and concrete managed-copy/reconciliation mutations remain intentionally owned by Features 3 and 4.

## Reviewer Focus Areas

- `scripts/propagate_master_assets.py` — confirm unknown integer counters fail closed as mutation counters and malformed/non-integer counters block convergence.
- `scripts/propagate_master_assets.py` — verify resolved containment plus lexical symlink-parent checks cover scratch-home escape cases without exposing destination paths.
- `scripts/propagate_master_assets.py` — confirm a failed copy skips reconciliation only for that harness and preserves earlier verified outcomes.
- `scripts/propagate_master_assets.py` — confirm the default five-pass total bound is sufficient for the documented three-pass identifier reclassification while still requiring a final verification pass.
