# Feature Plan: Managed-Copy Reconciliation

## Execution Metadata

- **Wave:** 4
- **Parallel safe:** no
- **Depends on:** `03-cross-platform-destinations`
- **Key files modified:** `scripts/propagate_master_assets.py`, `scripts/runtime_deployment.py` `[PROPOSED - name TBD]`, `tests/test_propagate_master_assets.py`, `tests/test_phase04_runtime_deployment.py` `[PROPOSED - name TBD]`
- **Sequential reason:** shares `scripts/propagate_master_assets.py`, the proposed deployment support module, and the proposed phase integration test with upstream `03-cross-platform-destinations`

## A. Requirements & Traceability

### Acceptance Criteria

1. **AC1:** A reusable managed-copy API `[PROPOSED - name TBD]` consumes Feature 3 destination records and stages complete replacements beside each destination before replacement.
2. **AC2:** Repository ownership is represented through generated markers or equivalent deployment metadata independently of whether the destination currently exists.
3. **AC3:** A live symlink, directory link, or Windows junction is replaceable only when its recorded or resolved target belongs to this repository's generated outputs; deletion never traverses the link.
4. **AC4:** A dangling link whose recorded target belongs to this repository is replaced by a managed copy when an output exists, or removed when the managed output is obsolete.
5. **AC5:** Whole-directory repository links become real directories populated from the matching generated root; per-file and per-skill links become regular managed files or directories.
6. **AC6:** Foreign regular files, foreign directories, foreign links, package-manager links, plugin-cache links, debug pointers, and Git hook links are preserved and reported as collisions.
7. **AC7:** Stale regular copies are pruned only when ownership is proven; unmarked or ambiguous content survives and is reported.
8. **AC8:** A failed copy or verification for one harness leaves its prior usable destination intact and suppresses destructive reconciliation for that harness.
9. **AC9:** Windows sharing violations or locked-file failures leave the existing destination intact, report the failure, and skip pruning for that destination without requiring elevation.
10. **AC10:** Repeated deployment against unchanged generated outputs and runtime destinations is idempotent, and no managed destination remains a symlink or junction into the repository.

### Non-Goals

- Following or copying content from arbitrary existing destination links.
- Overwriting foreign or unmarked content to force roster completeness.
- Cross-user or cross-environment cleanup.
- Global transaction rollback across harnesses.
- Plugin packaging or project-local runtime installation.

### Traceability Matrix

| Acceptance Criteria | Code Areas/Modules | Planned Tests |
|---|---|---|
| AC1–AC2 | `[PROPOSED - name TBD]` deployment support module; structured ownership metadata | Staging-completeness and destination-absence ownership scenarios |
| AC3–AC5 | Link/junction classifier and replacement operations | Live link, dangling link, directory link, per-file, per-skill, and obsolete-output scratch-home cases |
| AC6–AC7 | Collision classifier and stale-copy reconciliation | Foreign/unmarked/package/plugin/Git-link preservation and owned stale-copy pruning cases |
| AC8–AC9 | Per-harness transaction boundary and replacement error handling | Copy failure, verification failure, locked file, and sharing-violation simulations |
| AC10 | End-to-end managed-copy verification | Second-run idempotency and no-repository-link inventory assertions |

## B. Correctness & Edge Cases

- Classify the destination itself with non-following filesystem operations before reading any target.
- Preserve the original destination until the staged replacement is complete and verified.
- Reject a symlinked or junction-based parent that escapes the active-home boundary.
- Compare repository ownership against canonical generated roots while retaining the recorded target needed for dangling-link classification.
- Treat permission errors, sharing violations, and races between preflight and replacement as failures that preserve the old entry.
- Do not prune a harness after any copy or verification failure in that harness.
- Refresh the live inventory at execution time; do not assume the discovery count of 113 links.

## C. Consistency & Architecture Fit

- Reuse the existing generated markers and path-boundary validation patterns in `scripts/propagate_master_assets.py` where their contracts match user-global deployment.
- Do not reuse repository orphan-pruning functions blindly: runtime ownership and collision semantics are stricter and require an explicit public API.
- Upstream API: consume destination records from `03-cross-platform-destinations`; do not duplicate environment or platform resolution.
- Downstream API: `05-deployment-guidance` and `06-runtime-verification` call the reusable managed-copy operation through Feature 2 orchestration.
- Relationship: this is the highest-risk feature and requires focused security review before live-home use.

## D. Clean Design & Maintainability

- Separate inventory/classification, staging, replacement, verification, and pruning into reviewable operations.
- Use one ownership predicate across overwrite and prune decisions.
- Keep platform-specific junction handling behind the narrowest adapter.
- Keep it clean checklist: never follow deletion links, never overwrite unknown content, stage first, verify before prune, preserve on failure, idempotent second run.

## E. Completeness: Observability, Security, Operability

- Observability: structured inventory categories include replace, remove, copy, unchanged, collision, failed, and skipped-prune; avoid new per-file normal-path logs unless explicitly requested by verbose mode.
- Security: defend against hostile links, symlinked parents, path races, ownership spoofing, and destination escape.
- Operability: require scratch-home QA and a reviewed live inventory before author-home migration.
- Rollback: retain the prior destination until replacement succeeds; record enough ownership/version metadata to restore or redeploy the previous managed copy where available.

## F. Test Plan

- Add scratch-home cases to `tests/test_phase04_runtime_deployment.py` `[PROPOSED - name TBD]`.
- Update propagation tests for shared path safety, generated marker behavior, and CLI result integration.
- Use Windows-specific tests or runner-constrained evidence for junctions and sharing violations.
- Never point automated tests at the author's actual home.

### Top 5 High-Value Test Cases

1. **Given** live and dangling links into generated roots, **when** deployment runs, **then** they become regular managed copies without traversing the old targets.
2. **Given** foreign files, directories, and links alongside managed entries, **when** reconciliation runs, **then** foreign content survives and collisions are reported.
3. **Given** an owned stale copy and an unmarked stale-looking copy, **when** pruning runs, **then** only the owned copy is removed.
4. **Given** a locked Windows destination or injected replacement failure, **when** deployment runs, **then** the old destination remains and pruning is skipped.
5. **Given** a completed deployment, **when** the inventory and a second run execute, **then** every managed path is regular, fresh, and unchanged.

## Stage 1: Ownership and Inventory
**Goal**: Classify runtime destinations without following hostile or stale links.
**Success Criteria**: AC2–AC4 and AC6 pass scratch-home classification tests.
**Status**: Not Started

## Stage 2: Staged Managed Copies
**Goal**: Replace repository-owned links and owned copies safely.
**Success Criteria**: AC1, AC5, AC8, and AC9 pass failure-preservation tests.
**Status**: Not Started

## Stage 3: Safe Reconciliation
**Goal**: Prune only proven-owned stale assets and verify idempotent regular-copy state.
**Success Criteria**: AC7 and AC10 pass end-to-end inventory and second-run tests.
**Status**: Not Started

## Unverified Assumptions

- Python's platform APIs may not distinguish every Windows junction case consistently across supported versions; the implementation must verify behavior on native Windows and isolate any platform-specific classifier.

