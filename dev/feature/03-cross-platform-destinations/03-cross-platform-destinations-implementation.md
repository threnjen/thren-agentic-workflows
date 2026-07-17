# Implementation Record: Cross-Platform Destinations

## Summary

Implemented a read-only, injectable runtime destination resolver for the supported Claude, Codex, and OpenCode generated asset classes. The resolver classifies macOS, Linux, native Windows, and WSL as mutually exclusive current environments; honors only the three documented relocation variables; rejects unsafe or ambiguous destinations with content-safe categories; preserves destination leaf links for downstream ownership classification; and exposes a home-relativized preflight inventory. `scripts/propagate_master_assets.py` now provides a narrow handoff that accepts destinations only after a successful `PropagationConvergenceResult` from `propagate_until_converged()`.

## Sibling Features

- `02-propagation-convergence`: supplies the settled `propagate_until_converged()` and `PropagationConvergenceResult` gate consumed by this feature.
- `04-managed-copy-reconciliation`: consumes immutable `DestinationRecord` values and their `active_home` boundary; it should not recompute destination policy.
- Shared modules: `scripts/propagate_master_assets.py`, `scripts/runtime_deployment.py`, and `tests/test_phase04_runtime_deployment.py`.

## AC Coverage Matrix

| AC | Criterion ID | Planned Test ID | Planned Test Pattern | Status | Implementing Files | Evidence Paths | Implement Commit SHA | Review Commit SHA |
|----|--------------|-----------------|----------------------|--------|--------------------|----------------|----------------------|-------------------|
| AC1 | AC1 | RD-01 | Complete asset roster and stable record fields after convergence | Complete | `scripts/runtime_deployment.py`; `scripts/propagate_master_assets.py` | `tests/test_phase04_runtime_deployment.py::RuntimeDestinationTests::test_complete_roster_uses_only_documented_generated_sources`; `test_unconverged_handoff_is_rejected_before_resolution` | PENDING | PENDING |
| AC2 | AC2 | RD-02 | Claude default and `CLAUDE_CONFIG_DIR` matrix | Complete | `scripts/runtime_deployment.py` | `tests/test_phase04_runtime_deployment.py::RuntimeDestinationTests::test_default_destinations_stay_in_active_posix_home`; `test_overrides_relocate_only_documented_owner_classes` | PENDING | PENDING |
| AC3 | AC3 | RD-03 | Codex default, `CODEX_HOME`, existing-directory rule, and shared skill root | Complete | `scripts/runtime_deployment.py` | `tests/test_phase04_runtime_deployment.py::RuntimeDestinationTests::test_overrides_relocate_only_documented_owner_classes`; `test_custom_codex_home_must_already_be_a_directory` | PENDING | PENDING |
| AC4 | AC4 | RD-04 | OpenCode config override with fixed documented skill root and ignored XDG value | Complete | `scripts/runtime_deployment.py` | `tests/test_phase04_runtime_deployment.py::RuntimeDestinationTests::test_overrides_relocate_only_documented_owner_classes` | PENDING | PENDING |
| AC5 | AC5 | RD-05 | POSIX defaults and simulated native Windows profile containment | Complete | `scripts/runtime_deployment.py` | `tests/test_phase04_runtime_deployment.py::RuntimeDestinationTests::test_default_destinations_stay_in_active_posix_home`; `test_simulated_native_windows_stays_in_active_profile` | PENDING | PENDING |
| AC6 | AC6 | RD-06 | WSL classification and absence of Windows-profile/mount destinations | Complete | `scripts/runtime_deployment.py` | `tests/test_phase04_runtime_deployment.py::RuntimeDestinationTests::test_windows_and_wsl_classification_are_mutually_exclusive`; `test_wsl_never_targets_a_windows_profile_or_mount` | PENDING | PENDING |
| AC7 | AC7 | RD-07 | Unsupported platform and unsafe override rejection with safe diagnostics | Complete | `scripts/runtime_deployment.py`; `scripts/propagate_master_assets.py` | `tests/test_phase04_runtime_deployment.py::RuntimeDestinationTests::test_invalid_overrides_fail_with_content_safe_categories`; `test_windows_and_wsl_classification_are_mutually_exclusive`; `test_unconverged_handoff_is_rejected_before_resolution` | PENDING | PENDING |
| AC8 | AC8 | RD-08 | Preserve destination leaf while rejecting a symlinked escaping parent | Complete | `scripts/runtime_deployment.py` | `tests/test_phase04_runtime_deployment.py::RuntimeDestinationTests::test_leaf_link_is_preserved_but_escaping_parent_is_rejected` | PENDING | PENDING |

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | Return explicit source and active-user destination records for supported assets. | Complete | `scripts/runtime_deployment.py`; `scripts/propagate_master_assets.py` | Eight documented, currently generated asset classes are returned after the convergence handoff. |
| AC2 | Resolve Claude assets under the default or configured Claude root. | Complete | `scripts/runtime_deployment.py` | Includes agents, commands, skills, and learnings; hooks remain excluded. |
| AC3 | Apply `CODEX_HOME` only to Codex-owned assets and keep skills shared. | Complete | `scripts/runtime_deployment.py` | Custom Codex home must be an existing directory. |
| AC4 | Apply `OPENCODE_CONFIG_DIR` only to documented config-owned generated assets. | Complete | `scripts/runtime_deployment.py` | Skills remain at `~/.config/opencode/skills`; XDG is not inferred; absent commands are not invented. |
| AC5 | Keep defaults inside the active POSIX home or Windows profile. | Complete | `scripts/runtime_deployment.py` | Windows policy is simulated on this macOS runner. |
| AC6 | Treat WSL as an independent Linux environment. | Complete | `scripts/runtime_deployment.py` | WSL and Windows classifications are mutually exclusive and cross-environment forms are rejected. |
| AC7 | Fail before mutation for unsafe, ambiguous, or unsupported inputs. | Complete | `scripts/runtime_deployment.py`; `scripts/propagate_master_assets.py` | Errors expose category names only, not submitted path content. Empty variables are invalid. |
| AC8 | Preserve the leaf for classification and validate its parents. | Complete | `scripts/runtime_deployment.py` | Parent entries are checked without resolving the destination leaf. |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `scripts/runtime_deployment.py` | Added | Added platform facts, destination records, documented roster policy, normalization/validation, parent checks, and redacted inventory. | Centralizes user-runtime destination policy in one read-only API. |
| `scripts/propagate_master_assets.py` | Modified | Added `resolve_destinations_after_convergence()` using the settled fixed-point result. | Prevents destination resolution from bypassing repository convergence. |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| `tests/test_phase04_runtime_deployment.py` | Added | Added 11 scenario-driven resolver, platform, override, safety, convergence, link, and inventory tests. | AC1–AC8 |

## Test Results
- **Baseline**: 55 passed, 0 failed (`python3 -m unittest tests.test_propagate_master_assets` before implementation)
- **Final**: 87 passed, 0 failed (`python3 -m unittest discover -s tests -v`); 66 passed, 0 failed in the two focused modules
- **New tests added**: 11
- **Regressions**: None

## Deviations from Plan

- Settled the proposed support module name as `scripts/runtime_deployment.py` and the public APIs as `resolve_runtime_destinations()`, `DestinationRecord`, `destination_inventory()`, and `resolve_destinations_after_convergence()`.
- The deployable roster intentionally excludes generated `instructions/` trees and `codex/profiles/`: Phase 04 research documents no compatible user-runtime destination for them. OpenCode commands are documented but absent as a generated source, so no command record is invented.
- Destination resolution is integrated as an explicit post-convergence handoff rather than changing existing `--once`, `--watch`, or `--global-output` CLI behavior before Feature 4 supplies mutation semantics.

## Gaps

- Native Windows and WSL policy tests are simulated on macOS. Live Windows path/junction and live WSL evidence is runner-constrained and remains `NOT RUN` for Feature 6.
- Restarting and observing a real long-running watcher is manual runtime evidence; the existing watcher restart regression and all automated propagation tests pass.

## Reviewer Focus Areas

- `scripts/runtime_deployment.py` path-flavor normalization and containment behavior, especially native Windows drive/case semantics.
- `scripts/runtime_deployment.py::_check_existing_parents` preserves the destination leaf while rejecting symlinked ancestors.
- The intentionally narrow asset roster excludes unsupported generated trees and must remain aligned with Phase 04 primary-documentation research.
- `scripts/propagate_master_assets.py::resolve_destinations_after_convergence` must remain the only propagation-to-resolution handoff used by Feature 4.
