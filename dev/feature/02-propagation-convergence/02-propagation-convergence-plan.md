# Feature Plan: Propagation Convergence

## Execution Metadata

- **Wave:** 2
- **Parallel safe:** no
- **Depends on:** `01-interceptor-retirement`
- **Key files modified:** `scripts/propagate_master_assets.py`, `.vscode/tasks.json` `(verify)`, `tests/test_propagate_master_assets.py`, `tests/test_retirement_reconciliation.py`, `tests/test_phase04_runtime_deployment.py` `[PROPOSED - name TBD]`
- **Sequential reason:** shares `scripts/propagate_master_assets.py` and `tests/test_propagate_master_assets.py` with upstream `01-interceptor-retirement`

## A. Requirements & Traceability

### Acceptance Criteria

1. **AC1:** Repository propagation repeats within a documented bound until an immediate verification pass reports zero changes across Claude, Codex, and OpenCode outputs.
2. **AC2:** A new reusable public convergence API `[PROPOSED - name TBD]` is provided by the propagation layer so downstream deployment calls one verified implementation rather than duplicating fixed-point logic.
3. **AC3:** User-global preflight and mutation cannot begin when any repository propagation pass fails, the bound is exhausted, or the verification pass remains non-zero.
4. **AC4:** The current `propagate_once` contract remains usable for one repository pass, while the CLI path that performs deployment uses the bounded convergence API.
5. **AC5:** Destination preflight validates the active user's home boundary, required parent handling, ownership evidence availability, and collision readiness before any user-global write.
6. **AC6:** Deployment results are isolated per harness: one failed harness is reported as partial deployment, skips its destructive reconciliation, and does not roll back verified copies from another harness.
7. **AC7:** Watch-mode and operator guidance require restart of a stale watcher before migration or release verification after propagator changes.
8. **AC8:** Structured results distinguish propagation changes, convergence passes, preflight failures, per-harness copy outcomes, and reconciliation skips without emitting sensitive paths or content in normal logs.

### Non-Goals

- Choosing platform destination paths; `03-cross-platform-destinations` owns that policy.
- Copying or reconciling runtime assets; `04-managed-copy-reconciliation` owns mutations.
- Fixing agent identifier derivation beyond what is necessary to guarantee bounded convergence.
- Cross-user, cross-distribution, or native-Windows-to-WSL deployment.

### Traceability Matrix

| Acceptance Criteria | Code Areas/Modules | Planned Tests |
|---|---|---|
| AC1–AC4 | `scripts/propagate_master_assets.py`; verified `propagate_once` behavior | Multi-pass convergence, immediate verification, bounded exhaustion, and failure-before-deployment scenarios |
| AC5–AC6 | Propagation orchestration and `[PROPOSED - name TBD]` deployment result model | Scratch-home preflight and per-harness partial-failure scenarios |
| AC7 | Watch CLI path, `.vscode/tasks.json` `(verify)`, and operator guidance | Stale-watcher/restart regression assertion and manual runbook check |
| AC8 | Structured result payload returned by orchestration | Exact result-category assertions with redacted failure detail |

## B. Correctness & Edge Cases

- Count every change key that represents repository mutation; do not mistake a valid-looking pass for convergence.
- Reject negative, zero, or unreasonably large convergence bounds through the narrowest validated contract.
- Do not enter preflight after an exception or malformed propagation result.
- Preflight must complete for the intended harness set before the first user-global mutation.
- A failure after one harness succeeds must retain that verified state and suppress pruning only for the failed harness.
- Multiple invocations against a converged tree and unchanged runtime state must be idempotent.

## C. Consistency & Architecture Fit

- Extend the existing `propagate_once`/CLI architecture instead of creating an unrelated installer command.
- Reuse existing structured result counters and fail-closed path-validation conventions.
- Public downstream contract: `03-cross-platform-destinations` supplies destination records to the orchestration API; `04-managed-copy-reconciliation` supplies per-harness deployment operations; `05-deployment-guidance` and `06-runtime-verification` invoke the same orchestration entry point.
- The exact new API name is `[PROPOSED - name TBD]`; implementation must select a name consistent with neighboring `propagate_*` functions and update all plans' relationship notes if it changes.
- Relationship: depends on Feature 1 due to shared propagator retirement changes.

## D. Clean Design & Maintainability

- Separate one-pass propagation from bounded orchestration so existing focused tests remain small.
- Centralize the definition of “zero changes” rather than repeating key lists in callers.
- Represent per-harness status as data, not inferred from console text.
- Keep it clean checklist: one convergence loop, one bound, one preflight boundary, explicit harness status, no implicit live-home fallback.

## E. Completeness: Observability, Security, Operability

- Observability: structured counters and per-harness statuses are required; no new normal-path line-by-line log is justified.
- Security: preflight must reject destinations outside the active home and must not expose inventory contents in error strings.
- Operability: bounded failure reports the pass count and blocks user deployment; stale watchers are restarted before verification.
- Rollback: repository propagation remains reversible through version control; user-global rollback is deferred to managed-copy metadata in Feature 4.

## F. Test Plan

- Update `tests/test_propagate_master_assets.py` for bounded convergence and CLI orchestration.
- Preserve verified existing `test_real_repository_propagation_removes_nothing` and fixed-point coverage in `tests/test_retirement_reconciliation.py`.
- Add cross-feature scratch-home scenarios to `tests/test_phase04_runtime_deployment.py` `[PROPOSED - name TBD]`.
- No established new test method names are asserted; scenarios remain name-agnostic until implementation.

### Top 5 High-Value Test Cases

1. **Given** a reclassification requiring multiple passes, **when** bounded convergence runs, **then** it stops only after a zero-change verification pass.
2. **Given** propagation throws on an intermediate pass, **when** orchestration handles the failure, **then** no user-global preflight or mutation begins.
3. **Given** convergence never reaches zero within the bound, **when** the bound is exhausted, **then** deployment is blocked with a structured failure.
4. **Given** Claude succeeds and Codex fails during deployment, **when** results are finalized, **then** Claude remains verified and Codex pruning is skipped.
5. **Given** a converged repository and unchanged scratch home, **when** orchestration runs twice, **then** the second result reports no mutations.

## Stage 1: Bounded Repository Convergence
**Goal**: Produce one reusable fixed-point API over existing propagation passes.
**Success Criteria**: AC1–AC4 pass automated convergence and compatibility tests.
**Status**: Not Started

## Stage 2: Preflight and Harness Isolation
**Goal**: Establish the no-mutation boundary and partial-deployment result model.
**Success Criteria**: AC5, AC6, and AC8 pass scratch-home failure tests.
**Status**: Not Started

## Stage 3: Operational Integration
**Goal**: Integrate bounded convergence with CLI/watch behavior and restart guidance.
**Success Criteria**: AC7 passes automated or documented verification and the CLI cannot bypass convergence.
**Status**: Not Started

## Unverified Assumptions

- The current change-result dictionary contains every repository mutation counter needed to determine convergence; implementation must verify and centralize that set.
