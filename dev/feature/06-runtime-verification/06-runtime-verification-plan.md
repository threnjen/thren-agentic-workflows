# Feature Plan: Runtime Verification

## Execution Metadata

- **Wave:** 6
- **Parallel safe:** no
- **Depends on:** `01-interceptor-retirement`, `02-propagation-convergence`, `03-cross-platform-destinations`, `04-managed-copy-reconciliation`, `05-deployment-guidance`
- **Key files modified:** `scripts/propagate_master_assets.py`, `scripts/runtime_deployment.py` `[PROPOSED - name TBD]`, `tests/test_phase04_runtime_deployment.py` `[PROPOSED - name TBD]`, `tests/test_propagate_master_assets.py`, `tests/test_retirement_reconciliation.py` `(verify)`, `tests/hooks/test_hook_distribution_integration.py` `(verify)`, `.github/learnings/cross-phase-decisions.md`, `.github/learnings/project-learnings.md`, `claude/learnings/cross-phase-decisions.md` `(generated)`, `claude/learnings/project-learnings.md` `(generated)`, `docs/phases/PHASE_04/PHASE_04_DISCOVERY_CONTEXT.md`, `docs/phases/PHASE_04/PHASE_04_SUMMARY.md`
- **Sequential reason:** runtime integration depends on every upstream feature and shares `scripts/propagate_master_assets.py`, the proposed deployment support module, and phase verification tests with them

## A. Requirements & Traceability

### Acceptance Criteria

1. **AC1:** The existing propagation CLI exposes one runnable end-to-end path that converges repository outputs, resolves current-environment destinations, preflights, deploys managed copies, reconciles owned stale assets, and verifies runtime state in that order.
2. **AC2:** Automated scratch-home integration coverage proves the complete Claude, Codex, and OpenCode path without reading or mutating the author's live runtime directories.
3. **AC3:** A fresh execution inventory replaces the discovery baseline of 113 links and classifies every planned replacement, removal, unchanged managed copy, collision, failure, and preserved foreign entry before live migration.
4. **AC4:** After migration, every expected managed runtime asset is a regular fresh file or directory and no managed user-global path points into the repository through a symlink or junction.
5. **AC5:** Fresh sessions discover expected Claude, Codex, and OpenCode assets from managed copies on macOS, Linux, native Windows, and WSL using separate evidence for each environment.
6. **AC6:** Unavailable platform evidence is recorded as `NOT RUN`; any `NOT RUN` or failed platform prevents a full cross-platform GO verdict.
7. **AC7:** Final verification proves the shared hook framework and injection scanner remain functional, the retired interceptors no longer act, and an explicitly RTK-prefixed command remains usable.
8. **AC8:** Friction, deployment, hook-composition, and security-posture records are corrected to describe measured final behavior without moving Phase 01, Phase 02, or Phase 07 status lines.
9. **AC9:** The committed generated roots are at a repository fixed point, the deployment second run is idempotent, and the final evidence distinguishes automated tests, runner-constrained checks, code-review evidence, manual QA, failures, and `NOT RUN` platforms.

### Non-Goals

- Inferring one platform's result from another platform.
- Running live migration without explicit preflight and reviewed inventory.
- Changing historical phase status ownership.
- Packaging or public distribution.
- Deploying across Windows/WSL boundaries in one run.

### Traceability Matrix

| Acceptance Criteria | Code Areas/Modules | Planned Tests |
|---|---|---|
| AC1–AC2 | Propagator CLI; `[PROPOSED - name TBD]` deployment support; consolidated Phase 04 test | Full scratch-home workflow and failure-boundary integration scenarios |
| AC3–AC4 | Inventory and managed-copy verification outputs | Fresh inventory reconciliation and no-link/fresh-content assertions |
| AC5–AC6 | Platform runtime QA records | Separate macOS, Linux, Windows, and WSL fresh-session evidence matrix |
| AC7 | Surviving hooks, retired hook absence, explicit RTK | Focused hook smoke checks and manual explicit-RTK verification |
| AC8 | Cross-phase/project learnings and Phase 04 records | Exact claim review without status-line mutation |
| AC9 | Repository and runtime second-pass results | Fixed-point test, deployment idempotency test, and evidence classification audit |

## B. Correctness & Edge Cases

- Stop before live mutation unless the inventory has been explicitly reviewed for the active home.
- Re-inventory immediately before migration to catch drift between preflight and execution.
- Verify freshness by content/version evidence, not modification time alone.
- Fresh-session checks must avoid inheriting stale long-running watcher or process state.
- A platform marked unavailable remains `NOT RUN`; do not translate it to pass based on unit tests.
- A partial harness deployment must produce a non-GO result while preserving verified harness evidence.
- Phase record edits must not silently broaden to roadmap or status-line reconciliation.

## C. Consistency & Architecture Fit

- The final entry point stays in `scripts/propagate_master_assets.py`; it composes the upstream public APIs instead of duplicating their internals.
- Runtime verification consumes the Feature 2 orchestration result, Feature 3 destination records, and Feature 4 ownership/copy results.
- Feature 5 guidance is verified against this same entry point.
- `.github/learnings/` remains the record source of truth; `claude/learnings/` changes only through propagation and fixed-point verification.
- The exact new CLI flag and helper API names are `[PROPOSED - name TBD]` until implementation verifies naming against the current argument parser.
- This is the required integration/bootstrap feature and is the phase tail.

## D. Clean Design & Maintainability

- Keep the end-to-end path as thin orchestration over tested feature APIs.
- Separate automated scratch evidence from live platform evidence in the final record.
- Avoid embedding author-machine counts or paths as expected constants.
- Keep it clean checklist: one entry point, current inventory, fresh sessions, explicit platform status, no live-home test fixture, no status-line drift.

## E. Completeness: Observability, Security, Operability

- Observability: emit one structured phase result with per-stage/per-harness status and inventory counts; verbose detail may enumerate reviewed paths, but normal output must not expose sensitive content.
- Security: live migration requires active-home validation, ownership proof, collision preservation, and human inventory review.
- Operability: document watcher restart, dry/scratch run, preflight, live run, fresh-session verification, partial failure, rerun, and rollback.
- Rollback: retain prior usable destinations on failed replacement and use managed ownership/version evidence for controlled redeployment.

## F. Test Plan

- Create `tests/test_phase04_runtime_deployment.py` `[PROPOSED - name TBD]` as consolidated cross-feature integration coverage because the repository has no prior phase-scoped test directory convention.
- Update shared propagation and hook-distribution tests where the final CLI and retired roster require it.
- Run focused and full suites when the test runner is available; otherwise classify evidence as runner-constrained and do not claim pass.
- Execute manual QA separately on macOS, Linux, native Windows, and WSL.

### Top 5 High-Value Test Cases

1. **Given** a scratch repository and scratch home containing owned links, dangling links, managed copies, and foreign collisions, **when** the end-to-end CLI runs, **then** only owned entries become fresh regular copies and the second run is unchanged.
2. **Given** repository propagation cannot converge, **when** the end-to-end path runs, **then** no scratch-home mutation occurs.
3. **Given** one harness replacement fails, **when** integration completes, **then** its previous state survives, pruning is skipped for it, and the overall verdict is partial/non-GO.
4. **Given** a fresh session on each available platform, **when** runtime discovery executes, **then** expected assets load from regular copies and evidence is recorded per platform.
5. **Given** final hook and RTK checks, **when** the retired and surviving behaviors are exercised, **then** guard/rewrite interception is absent, scanner/framework behavior survives, and explicit RTK works.

## Stage 1: End-to-End Bootstrap
**Goal**: Compose upstream APIs into one runnable deployment entry point.
**Success Criteria**: AC1 and AC2 pass scratch-home integration coverage.
**Status**: Not Started

## Stage 2: Inventory and Live Verification
**Goal**: Review a fresh inventory and verify managed runtime state in fresh sessions.
**Success Criteria**: AC3–AC7 have platform-specific evidence with no inferred passes.
**Status**: Not Started

## Stage 3: Evidence and Record Reconciliation
**Goal**: Consolidate fixed-point, idempotency, security-posture, and platform results.
**Success Criteria**: AC8 and AC9 pass record review and evidence-classification checks.
**Status**: Not Started

## Unverified Assumptions

- Live native Windows and WSL environments may be unavailable in this session; absence must remain `NOT RUN` and block a full GO verdict.
