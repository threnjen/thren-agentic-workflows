# Review Record: Runtime Verification

## Summary

Reviewed implementation commit `5089a6b` against AC1–AC9, including CLI
handshake and stage ordering, inventory classification and recheck safety,
scratch-home isolation, managed-copy freshness, failure reduction, exit codes,
interceptor retirement, surviving scanner/framework behavior, explicit RTK,
repository fixed point, and platform evidence classification. Two defects were
found and fixed. The most important allowed a digest reviewed for one active
home to authorize a different home when their relative inventories matched.

## Verdict

Approved with Reservations

## Traceability

| AC | Status | Evidence | Notes |
|----|--------|----------|-------|
| AC1 | Verified | `scripts/propagate_master_assets.py:1962`; `tests/test_phase04_runtime_deployment.py:686`; `tests/test_phase04_runtime_deployment.py:914` | `--runtime-deploy` preserves the existing default one-pass path and orders convergence, destination preflight, inventory, immediate recheck, deployment/reconciliation, and verification. Review-required exits 2; failed/partial exits 1; only GO exits 0. |
| AC2 | Verified | `tests/test_phase04_runtime_deployment.py:686`; `tests/test_phase04_runtime_deployment.py:774` | Claude, Codex, and OpenCode execute entirely beneath temporary repositories and homes. The review digest is now cryptographically bound to the selected active home, so scratch evidence cannot be replayed against another home. |
| AC3 | Verified for scratch evidence; live inventory NOT RUN | `scripts/runtime_deployment.py:327`; `tests/test_phase04_runtime_deployment.py:708` | Fresh inventory covers planned replacement, unchanged managed copy, collision, obsolete owned removal, and preserved foreign entries, with generated-source fingerprints. Deployment failures remain structured result evidence rather than being misreported as inventory classifications. |
| AC4 | Verified for scratch evidence; live migration NOT RUN | `scripts/propagate_master_assets.py:1919`; `tests/test_phase04_runtime_deployment.py:686` | Verification requires regular destination directories and content identity for every expected source entry; links/junctions and stale content fail verification. Foreign extras do not create false failures. |
| AC5 | NOT RUN | `docs/phases/PHASE_04/PHASE_04_SUMMARY.md:191` | macOS author-home migration, live Linux, native Windows, and WSL fresh-session discovery were unavailable. Scratch policy simulation is not promoted to live platform evidence. |
| AC6 | Verified | `scripts/propagate_master_assets.py:1989`; `tests/test_phase04_runtime_deployment.py:686` | All four platform rows remain explicit `NOT RUN` values and force `partial`, preventing a full cross-platform GO verdict. |
| AC7 | Verified after fix | `tests/test_phase04_runtime_deployment.py:880` | Retired interceptors are absent; scanner/framework integration loads; the deterministic scanner benchmark passes 19 positive and 7 negative fixtures; explicit `rtk git status --short` succeeds. |
| AC8 | Verified | `.github/learnings/cross-phase-decisions.md:368`; `.github/learnings/project-learnings.md:82`; `docs/phases/PHASE_04/PHASE_04_DISCOVERY_CONTEXT.md:140` | Records distinguish scratch automation from unavailable live evidence, preserve the 113-link baseline as historical, and do not move Phase 01, Phase 02, or Phase 07 status ownership. |
| AC9 | Verified | `tests/test_phase04_runtime_deployment.py:686`; propagation fixed-point output | Second reviewed scratch deployment makes zero copy/replace/remove mutations. A post-review propagation pass converged in one pass with zero propagation or verification changes. Automated, runner-constrained, manual/live, and `NOT RUN` evidence remain distinct. |

## Issues Found

| # | Severity | Issue | Status |
|---|----------|-------|--------|
| 1 | High | `_runtime_inventory_digest` hashed only home-relative inventory and generated-source fingerprints. A digest reviewed for an identical scratch home could therefore be replayed with a different `--active-home`, bypassing the requirement that review authorize the exact mutation root. | Fixed |
| 2 | Medium | The consolidated AC7 unittest asserted only scanner/config file presence while the behavioral hook suite was unavailable because pytest is not installed. The implementation record nevertheless described the scanner/framework as functional. | Fixed |

## Fixes Applied

| Files | Change |
|-------|--------|
| `scripts/propagate_master_assets.py` | Added the absolute active-home identity to the deterministic digest payload and uses the same binding for the immediate recheck. The path remains undisclosed; only its SHA-256 digest is emitted. |
| `tests/test_phase04_runtime_deployment.py` | Added cross-home digest replay coverage proving an inventory-drift result and zero writes. Expanded AC7 coverage to load the scanner/framework integration and execute the deterministic injection benchmark through `sys.executable`. |

## Test Coverage Assessment

- Focused runtime and propagation suites: 101 passed via
  `python3 -m unittest tests.test_phase04_runtime_deployment tests.test_propagate_master_assets -v`.
- Full unittest discovery: 122 passed via
  `python3 -m unittest discover -s tests -v`.
- Injection benchmark: passed 19 positive and 7 negative fixtures with zero
  misses and zero false positives.
- Explicit RTK check: passed.
- Python compilation: passed for the deployment CLI, runtime module, and
  consolidated phase test.
- Repository fixed point: one pass, zero propagation changes, zero verification
  changes.
- `git diff --check`: passed.
- Pytest hook integration: `NOT RUN` because the active interpreter reports
  `No module named pytest`; no pass claim is inferred.
- Graph review rated the implementation medium direct risk (0.55) and high
  two-hop blast radius (332 impacted nodes across 25 additional files). The
  graph did not infer test edges for the new functions, so direct focused and
  full-suite execution was used as the coverage authority.

## Remaining Concerns

- Live macOS author-home migration was not authorized. Live Linux, native
  Windows, and WSL runners were unavailable. All remain `NOT RUN`, so release
  readiness must stay below full cross-platform GO.
- The pytest-based hook integration suite remains runner-constrained. The
  standalone scanner benchmark and framework-loading check provide behavioral
  AC7 evidence in this runner but do not replace the full pytest suite.
- Inventory recheck closes review-time drift before mutation, but filesystem
  races after the recheck remain constrained by the managed-copy layer's
  identity rechecks and fail-closed replacement behavior.

## Risk Summary

- Reviewed inventory now authorizes one exact active home, generated source
  state, and classified destination state; missing, stale, or cross-home review
  fails before runtime mutation.
- Harness failures and collisions remain non-GO while successful harness
  evidence is preserved.
- Verification rejects linked or stale managed destinations without rejecting
  preserved foreign extras.
- Retired interceptors remain absent; no automatic RTK rewriting or file-access
  guard behavior was restored.
- Unavailable platform evidence is explicitly `NOT RUN` and cannot be inferred
  from scratch tests or platform-policy simulation.
