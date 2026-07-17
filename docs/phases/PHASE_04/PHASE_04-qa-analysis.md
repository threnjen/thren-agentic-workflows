# QA Readiness Analysis: Phase 04 — Hook Retirement & Cross-Platform Deployment

**Date:** 2026-07-17  
**Analyst:** prod-code-review (automated)  
**Mode:** Fast-track (`All verdicts Approved: YES`)  
**Verdict:** **GO WITH CONDITIONS**  
**Phase baseline:** `fd0f1a0`  
**Reviewed revision:** `6adb1de` plus Phase 04 final-review pipeline artifacts  
**Visual verification:** Not applicable — not a Unity project

## Readiness Verdict

**GO WITH CONDITIONS.** The implementation is suitable to proceed to controlled release
QA and pull-request review, but it is not eligible for an unconditional cross-platform
production declaration or an unreviewed active-home deployment.

All six feature reviews are Approved or Approved with Reservations, and the one reserved
review (`06-runtime-verification`) accurately preserves the evidence ceiling rather than
claiming unavailable platform success. The diff-scoped security scan found no Critical or
High issue. The consolidated QA plan covers every verification asset named by the
execution manifest.

The conditions are substantive:

1. The pytest-based hook integration evidence is **NOT RUN**. No success is inferred from
   standalone scanner checks, unittest records, or earlier pytest claims.
2. Fresh-session macOS, Linux, native Windows, and WSL evidence is **NOT RUN** for all four
   environments. Simulation and scratch-home tests do not substitute for those runs.
3. The reviewed live inventory, watcher restart, authorized active-home deployment,
   foreign-content comparison, regular-copy/no-repository-link verification, and second-run
   fixed point remain manual release gates.
4. The security scan's Medium concurrent-filesystem race remains open. Deployment must be
   performed in a quiescent, reviewed home environment until containment and mutation are
   made atomic enough for an adversarial concurrent-writer claim.
5. Retirement of file/Bash access enforcement is intentional and must remain an explicit
   accepted defense-in-depth reduction. The surviving injection scanner must not be
   represented as replacement authorization.

These conditions cap the verdict at **GO WITH CONDITIONS**. A failure in any required
platform row, foreign-content loss, a repository link left in managed output, a stale or
linked managed copy, a convergence/inventory-gate bypass, or a failed second-run fixed point
changes the verdict to **NO-GO**.

## Executive Summary

Phase 04 removes two interceptors and adds a user-global deployment system with a large
filesystem blast radius. The phase diff contains 66 changed files, 4,733 insertions, and
6,542 deletions. Graph analysis classified the two-hop blast radius as high: 340 directly
changed nodes, 224 impacted nodes, and 21 additional affected files. No stored runtime flow
mapped to the new CLI path, so readiness depends primarily on direct scenario coverage and
manual runtime evidence rather than graph-derived flow proof.

The strongest implementation properties are the bounded repository fixed-point gate,
active-home-bound inventory approval, per-harness failure isolation, positive ownership
requirements, staged and verified replacement, collision preservation, non-following link
handling, and structured content-safe failures. Review found and fixed serious defects in
these areas, including cross-home digest replay, ownership ratcheting, foreign metadata
replacement, junction-parent traversal, preflight ordering, and prune identity races.

The remaining uncertainty is concentrated where the QA plan says it is: native filesystem
semantics, fresh harness discovery, and final-run evidence. All four supported environments
are still `NOT RUN`; the mandatory pytest hook integration is also `NOT RUN`. This analysis
does not convert recorded test claims, policy simulation, or behavior on another platform
into missing evidence.

## Feature Readiness

| Feature | Review verdict | Production-readiness assessment |
|---|---|---|
| `01-interceptor-retirement` | Approved | Retired registrations and implementation surfaces are removed; reduced security posture is documented. Final pytest hook integration remains NOT RUN. |
| `02-propagation-convergence` | Approved | Bounded fixed point, preflight-before-copy, and per-harness isolation are implemented. Watcher restart and live execution evidence remain manual gates. |
| `03-cross-platform-destinations` | Approved | Destination policy and platform separation are deterministically covered. Native Windows, WSL, macOS, and Linux live behavior remain NOT RUN. |
| `04-managed-copy-reconciliation` | Approved | Ownership, collision, staging, restoration, and pruning logic passed feature review. Native junction/sharing semantics and the Medium TOCTOU condition remain open. |
| `05-deployment-guidance` | Approved | Supported guidance uses managed copies and preserves explicit RTK use. Operator execution of the documented sequence remains unverified live. |
| `06-runtime-verification` | Approved with Reservations | Scratch evidence and result reduction are implemented; all four platform rows and pytest hook integration remain explicitly NOT RUN. |

No review has an unresolved Changes Requested verdict. Feature 06's reservations are
release conditions, not concealed feature completion claims.

## Verification Asset Assessment

| Manifest verification asset | Coverage in QA documents | Final-review treatment |
|---|---|---|
| `tests/test_phase04_runtime_deployment.py` | Destination policy, inventory binding, reconciliation, orchestration, guidance, retirement, and explicit RTK | Recorded unittest evidence exists; this analysis did not rerun it. |
| `tests/test_propagate_master_assets.py` | Convergence, preflight, failure isolation, watcher restart, roster, and renderer parity | Recorded unittest evidence exists; this analysis did not rerun it. |
| `tests/hooks/test_hook_distribution_integration.py` | Behavioral interceptor absence and surviving scanner/framework integration | **NOT RUN** under pytest; must not be inferred from standalone checks. |
| `tests/test_retirement_reconciliation.py` | Committed-tree fixed point and retired-asset regressions | Included in the mandatory final automated suite; final release record must identify the exact revision and result. |
| Scratch-home deployment | Full three-harness, collision, failure, and fixed-point checklist | Recorded implementation evidence exists; repeat on the release revision before live mutation. |
| Preflight and reviewed inventory | Digest/home binding and drift gate | Automated contract exists; live inventory review and authorization remain pending. |
| Watcher restart | Required by CLI/guidance | Manual evidence pending. |
| Platform/fresh-session matrix | Four independent rows | macOS, Linux, native Windows, and WSL are all **NOT RUN**. |
| Fixed point, foreign preservation, no repository link | Automated scratch coverage plus manual comparison | Manual active-home evidence pending. |

The QA coverage map preserves all manifest verification assets. No required asset was
dropped. Its release-decision rules correctly distinguish a conditional result from a full
GO and correctly make a failed platform row a NO-GO rather than a condition.

## Security Readiness

The diff-scoped security scan verdict is **Pass with Conditions** with totals of Critical
0, High 0, Medium 2, Low 0.

### Condition S1 — Concurrent filesystem mutation / TOCTOU

Containment, parent-link, ownership, backup-name, and prune identity checks occur before
later filesystem mutation. A process capable of concurrently changing the same home tree
may exchange a checked parent or destination during the remaining window. The current
implementation fails closed for stable-state collisions and narrows several windows, but it
does not provide an atomic adversarial-filesystem boundary.

**Release handling:** stop/restart relevant watchers as documented, close harness processes
that can mutate destinations, review the exact inventory, and run deployment in a quiescent
active home. Before claiming safety against a hostile concurrent writer, harden the mutation
path with platform-appropriate descriptor-relative/no-follow or equivalent atomic controls
and add race-focused tests.

### Condition S2 — Intentional defense-in-depth reduction

The file-access guard and Bash-mediated access controls are deliberately retired. Prompt
injection scanning remains useful but is not file/Bash authorization.

**Release handling:** retain the reduced-posture disclosure, rely on OS permissions,
harness-native controls, operator review, and secret-management hygiene, and do not describe
the scanner as restoring the retired boundary.

### Categories still requiring native evidence

- Windows reparse points, junctions, ACLs, sharing violations, and replacement semantics.
- WSL home separation and actual distribution-local runtime discovery.
- macOS/Linux active-home permissions and harness loading.
- Interaction with concurrently running harness or watcher processes.

## Required Conditions Before Unconditional GO

1. Record the exact release revision and clean/expected dirty state.
2. Run the mandatory automated suites on that revision, including the pytest hook
   integration; record pass/fail/skip counts. Any failure is NO-GO.
3. Restart the watcher before migration or release verification.
4. Run the complete deployment flow against scratch homes first and confirm the second run
   makes zero copy, replace, remove, or prune mutations.
5. Produce and review the current home-relative inventory and its digest for the exact
   authorized active home. Do not reuse the historical 113-link count as the expected
   roster.
6. Perform the authorized live migration and prove foreign files, directories, links, and
   metadata remain unchanged.
7. Prove every expected managed destination is regular and content-fresh, and no managed
   destination links or junctions into the repository.
8. Run a second authorized deployment and prove a zero-mutation fixed point.
9. Record separate fresh-session discovery results for macOS, Linux, native Windows, and
   WSL. `NOT RUN` keeps this conditional; any `FAIL` is NO-GO.
10. Keep the two Medium security conditions visible in release notes and operational
    guidance; do not overstate the remaining containment or authorization boundary.

## Final Decision

**GO WITH CONDITIONS.** The static implementation and review record are sufficient to move
forward with controlled QA and PR review. They are not sufficient for an unconditional
cross-platform release or unreviewed active-home mutation.

The path to full **GO** is evidence-driven rather than feature-driven: execute the missing
pytest and manual QA gates, obtain four independent live platform results, close or
explicitly accept the Medium filesystem-race condition for the intended threat model, and
retain the disclosed defense-in-depth reduction. Until then, the Phase 04 summary status
must not imply complete cross-platform production verification.
