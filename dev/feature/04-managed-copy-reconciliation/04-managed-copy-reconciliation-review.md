# Review Record: Managed-Copy Reconciliation

## Summary

Reviewed implementation commit `847835d` against AC1–AC10, with focused
attention to ownership proof, non-following link removal, staged replacement,
collision preservation, Windows sharing failures, harness-scoped pruning, and
idempotency. Five safety defects were found and fixed. The most serious allowed
a preserved user replacement to be written back into ownership metadata and
overwritten on a later run.

## Verdict

Approved

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1 | Verified | `scripts/runtime_deployment.py:692`; `scripts/runtime_deployment.py:711`; `tests/test_phase04_runtime_deployment.py:342` | Every record is copied to a sibling stage and manifest-verified before any record in that harness mutates. |
| AC2 | Verified after fixes | `scripts/runtime_deployment.py:430`; `scripts/runtime_deployment.py:475`; `scripts/runtime_deployment.py:547` | Ownership now requires an exact positional generated marker, a current fingerprint in valid metadata, or a repository-output link target; identical content alone is not adopted. |
| AC3 | Verified | `scripts/runtime_deployment.py:396`; `scripts/runtime_deployment.py:425`; `scripts/runtime_deployment.py:572` | Live links and junctions are classified with `lstat`/recorded targets and moved as entries; deletion never walks the target. |
| AC4 | Verified after fix | `scripts/runtime_deployment.py:662`; `scripts/runtime_deployment.py:739`; `tests/test_phase04_runtime_deployment.py:424` | Owned dangling links are handled by recorded targets, and an empty generated roster now still runs owned-only stale reconciliation. |
| AC5 | Verified | `scripts/runtime_deployment.py:596`; `tests/test_phase04_runtime_deployment.py:356`; `tests/test_phase04_runtime_deployment.py:584` | Owned root and child links are replaced by verified regular files/directories from generated sources. |
| AC6 | Verified after fixes | `scripts/runtime_deployment.py:495`; `scripts/runtime_deployment.py:627`; `scripts/runtime_deployment.py:653` | Foreign content, links, metadata entries, and quoted markers fail closed as collisions and are excluded from refreshed ownership metadata. |
| AC7 | Verified after fixes | `scripts/runtime_deployment.py:547`; `scripts/runtime_deployment.py:662`; `tests/test_phase04_runtime_deployment.py:408` | Overwrite and prune share the same positive ownership predicate; pruning rechecks entry identity immediately before removal. |
| AC8 | Verified | `scripts/runtime_deployment.py:711`; `scripts/runtime_deployment.py:742`; `tests/test_phase04_runtime_deployment.py:488` | Harness-wide staging precedes mutation; staging or install failure marks the harness failed and prevents its prune phase. |
| AC9 | Verified; native evidence pending | `scripts/runtime_deployment.py:572`; `tests/test_phase04_runtime_deployment.py:602` | Simulated locked-file replacement restores the backup, reports failure, and skips pruning without elevation. Native Windows sharing/junction evidence remains assigned to Feature 6. |
| AC10 | Verified after fixes | `scripts/runtime_deployment.py:508`; `tests/test_phase04_runtime_deployment.py:514`; `tests/test_phase04_runtime_deployment.py:526` | Current fingerprints produce unchanged outcomes, foreign collisions remain foreign across later runs, and managed root links become regular directories. |

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | Collision handling retained the collided name in the ownership set. Metadata then fingerprinted the user replacement, authorizing a later run to overwrite it. Identical unmarked files were also adopted solely by content equality. | Critical | `scripts/runtime_deployment.py:632` | AC2, AC6, AC7, AC10 | Fixed |
| 2 | Marker ownership searched the entire file for a generic substring. A hand-maintained file quoting a generated marker could therefore be pruned as repository-owned. | High | `scripts/runtime_deployment.py:430` | AC2, AC6, AC7 | Fixed |
| 3 | Metadata used a fixed temporary path and unconditionally replaced an invalid or foreign metadata entry, allowing user content at either control path to be overwritten. | High | `scripts/runtime_deployment.py:495` | AC6, AC8, AC9 | Fixed |
| 4 | An empty expected source roster was treated like a record collision, so positively owned obsolete entries were never reconciled. | Medium | `scripts/runtime_deployment.py:739` | AC4, AC7, AC10 | Fixed |
| 5 | Pruning checked ownership and then removed the path without rechecking entry identity, allowing a user replacement introduced during the race window to be deleted. | High | `scripts/runtime_deployment.py:662` | AC6, AC7 | Fixed |

## Fixes Applied

| File | What Changed | Issue # |
|------|--------------|---------|
| `scripts/runtime_deployment.py` | Centralized positive ownership; removed collided names from metadata; requires ownership even for byte-identical entries. | 1 |
| `scripts/runtime_deployment.py` | Replaced generic marker search with exact type-specific markers at the established emitter position. | 2 |
| `scripts/runtime_deployment.py` | Preserves foreign metadata, uses exclusive temporary metadata files, rechecks metadata identity, cleans temporary files, and writes metadata into whole-root stages before replacement. | 3 |
| `scripts/runtime_deployment.py` | Distinguishes successful empty installs from skipped collision records so empty rosters still prune proven-owned stale entries. | 4 |
| `scripts/runtime_deployment.py` | Captures and rechecks stale-entry identity immediately before removal. | 5 |
| `tests/test_phase04_runtime_deployment.py` | Added regressions for third-run ownership ratcheting, identical unmarked files, foreign metadata, quoted markers, empty rosters, and prune races. | 1–5 |

## Remaining Concerns

Native Windows junction/reparse-point behavior and live sharing violations were
not executable on this macOS runner. The platform adapter and recovery paths are
covered deterministically, and Feature 6 owns native runtime evidence. No
unresolved feature-scope code finding remains.

## Test Coverage Assessment

- Full post-fix result: 105 passed, 0 failed via `python3 -m unittest discover -s tests`.
- `python3 -m py_compile scripts/runtime_deployment.py tests/test_phase04_runtime_deployment.py`: passed.
- `git diff --check`: passed.
- Graph analysis rated the original implementation medium risk with a high
  two-hop blast radius: 328 nodes and 25 additional files. Direct scratch-home
  scenarios cover all ACs and each corrected ownership or collision branch.

## Risk Summary

- Ownership fails closed for edited metadata-owned entries, unmarked equal
  content, foreign links, foreign metadata, and marker quotations.
- Link replacement uses recorded repository-output targets for authorization,
  stages verified replacements beside destinations, and removes only link
  entries rather than their targets.
- Fixed-point gating remains the only public propagation handoff.
- Staging and replacement failures are isolated per harness; successful
  harnesses remain committed while failed harnesses skip reconciliation.
- Live native Windows evidence remains a release-verification concern rather
  than an unresolved implementation defect.
