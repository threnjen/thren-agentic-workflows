# Phase 04 QA Coverage Map

## Verification Asset Coverage

| Required asset | Phase coverage | Release use |
|---|---|---|
| `tests/test_phase04_runtime_deployment.py` | Destination policy, managed copies, reviewed inventory, runtime orchestration, documentation, interceptor/RTK checks | Mandatory focused suite and primary cross-feature scratch-home evidence |
| `tests/test_propagate_master_assets.py` | Retired-asset ownership, generated roster, convergence, preflight, harness isolation, watcher restart, renderer parity | Mandatory shared regression suite |
| `tests/hooks/test_hook_distribution_integration.py` | Behavioral absence of interception, surviving scanner/framework, generated wiring, reduced posture | Mandatory when pytest is available; otherwise `NOT RUN` plus standalone behavioral evidence |
| `tests/test_retirement_reconciliation.py` | Committed-tree propagation fixed point and retirement regressions | Mandatory shared fixed-point suite |

## Feature-to-Evidence Traceability

| Feature | Acceptance coverage | Automated evidence | Manual/runtime evidence | Gate |
|---|---|---|---|---|
| 01 Interceptor retirement | Remove guard and automatic RTK rewrite; preserve scanner/framework, explicit RTK, ownership-safe cleanup, reduced-posture docs | Hook distribution tests; retired-asset tests in propagation suite; `test_retired_interceptors_are_absent_while_scanner_framework_remains`; `test_explicit_rtk_prefixed_command_remains_usable` | Inspect final hook rosters and user-global registrations without secret reads; execute explicit RTK | Any active retired interceptor, scanner/framework regression, or RTK removal is NO-GO |
| 02 Propagation convergence | Bounded fixed point, no-write failure gate, full-set preflight, per-harness isolation, watcher restart, safe structured results | Convergence, invalid-bound, failure, preflight, harness-isolation, CLI-gate, and watcher tests in `test_propagate_master_assets.py`; end-to-end nonconvergence test | Restart watcher; capture zero-change verification pass | Any runtime write before convergence/preflight is NO-GO |
| 03 Cross-platform destinations | Eight-class roster, documented overrides, home containment, native Windows/WSL separation, parent-link rejection | `RuntimeDestinationTests` in consolidated suite | Validate defaults/overrides on each live platform | Simulation alone cannot produce full GO |
| 04 Managed-copy reconciliation | Verified staging, positive ownership, non-following link migration, collision preservation, owned pruning, restoration, idempotency | Managed-copy scratch tests in consolidated suite | Reviewed live inventory; verify regular fresh copies, foreign preservation, two-run fixed point | Foreign loss, stale/link output, or unauthorized pruning is NO-GO |
| 05 Deployment guidance | Evangelize and setup surfaces use managed copies, generated parity, no operational link recipes, honest platform evidence | Guidance classifier and renderer parity tests | Operator follows documented sequence without ad hoc links | Supported link-creation/repair path is NO-GO |
| 06 Runtime verification | One ordered CLI path, digest/home binding, drift gate, scratch harness integration, evidence classes, live platform ceiling | Runtime orchestration tests and full discovery | Authorized migration and separate fresh sessions on four environments | Any unavailable platform prevents full GO; failed platform is NO-GO |

## Critical Requirement Matrix

| Requirement | Automated proof | Manual proof | Expected result |
|---|---|---|---|
| Scratch homes precede live mutation | All mutation scenarios use temporary homes | QA record shows scratch run completed first | Pass |
| Reviewed preflight inventory | Review-required, wrong-digest, cross-home replay, and drift tests | Inventory rows and digest reviewed for exact active home | Pass before mutation |
| No live-home mutation without authorization | Zero-write assertions on unreviewed/wrong/drift states | Explicit authorization artifact | Pass; violation is NO-GO |
| Watcher restart | `test_watcher_announces_restart_requirement` | Restart timestamp/process evidence | Pass before migration |
| Separate macOS/Linux/Windows/WSL evidence | Platform-separation assertions | Four independent fresh-session records | All Pass for full GO |
| Unavailable platform caps verdict | `test_native_windows_and_wsl_are_separate_evidence`; runtime result reduction | `NOT RUN` reason per unavailable row | Partial, never full GO |
| Fresh roster, not historical 113 | Inventory/roster classification tests | Compare current inventory with current generated roster | Exact current roster; 113 informational only |
| Foreign content preservation | Collision, foreign-link, foreign-metadata, quoted-marker, identical-unowned tests | Before/after hashes or identities for foreign entries | Unchanged |
| Regular fresh managed copies; no repo links | Scratch success and verification reducer tests | Type/content/link inspection after migration | All expected entries regular and fresh |
| Retired interceptors absent; scanner/framework and RTK survive | Consolidated AC7 checks plus hook integration suite | Final hook roster and explicit RTK command | Pass |
| Two-run fixed point | `test_second_run_is_idempotent`; reviewed scratch deployment idempotency; committed-tree fixed-point tests | Second authorized run result | Zero copy/replace/remove mutations |

## Detailed Automated Scenario Map

| Concern | Representative tests |
|---|---|
| Destination roster and platform policy | `test_complete_roster_uses_only_documented_generated_sources`, `test_default_destinations_stay_in_active_posix_home`, `test_overrides_relocate_only_documented_owner_classes`, `test_windows_and_wsl_classification_are_mutually_exclusive`, `test_wsl_never_targets_a_windows_profile_or_mount` |
| Destination safety | `test_invalid_overrides_fail_with_content_safe_categories`, `test_leaf_link_is_preserved_but_escaping_parent_is_rejected`, `test_junction_parent_is_rejected_before_mutation`, `test_unconverged_handoff_is_rejected_before_resolution` |
| Ownership and collision safety | `test_foreign_content_and_foreign_links_are_preserved_as_collisions`, `test_foreign_metadata_entry_blocks_record_without_mutation`, `test_identical_unmarked_file_is_not_adopted_as_managed`, `test_quoted_generated_marker_does_not_prove_ownership`, `test_stale_metadata_does_not_authorize_overwriting_user_replacement` |
| Link migration and pruning | `test_repository_link_is_unlinked_without_traversing_target`, `test_dangling_repository_link_is_replaced_but_foreign_one_survives`, `test_owned_stale_copy_is_pruned_but_unmarked_copy_survives`, `test_empty_generated_root_prunes_only_owned_stale_entries`, `test_prune_rechecks_identity_before_removing_owned_stale_copy` |
| Failure isolation and recovery | `test_stage_failure_preserves_old_destination_and_skips_harness_pruning`, `test_replacement_failure_restores_prior_managed_file`, `test_mixed_harness_failure_does_not_roll_back_success`, `test_partial_harness_failure_is_non_go_and_preserves_success` |
| Review and mutation gates | `test_runtime_cli_reports_review_required_without_deploying`, `test_unreviewed_or_wrong_inventory_digest_never_mutates`, `test_review_digest_is_bound_to_the_active_home`, `test_material_inventory_drift_aborts_before_deploy`, `test_nonconverged_repository_causes_zero_runtime_writes` |
| Idempotency and verification | `test_reviewed_scratch_home_path_deploys_all_harnesses_and_is_idempotent`, `test_second_run_is_idempotent`, `test_propagation_is_idempotent`, `test_committed_tree_is_at_a_propagation_fixed_point` |
| Retirement and surviving behavior | `test_interceptors_are_retired_while_independent_hooks_survive`, `test_direct_operations_are_not_intercepted_by_surviving_hooks`, `test_surviving_scanner_blocks_and_redacts_injected_output`, `test_retired_interceptors_are_absent_while_scanner_framework_remains`, `test_explicit_rtk_prefixed_command_remains_usable` |
| Guidance and generated parity | `test_supported_guidance_has_no_runtime_link_creation_recipe`, `test_runtime_link_guard_rejects_negative_fixture`, `test_security_and_retirement_discussion_remains_allowed`, `test_evangelize_requires_managed_copy_readiness_contract`, `test_evangelize_matches_every_generated_harness_variant` |

## Evidence Classification

| Class | Current phase record | Release treatment |
|---|---|---|
| Automated focused/full unittest | Passing implementation/review evidence; rerun on final revision | Required |
| Pytest hook integration | Runner availability has varied; must be rerun or recorded `NOT RUN` | Condition if unavailable; never infer pass |
| Simulated native Windows/WSL policy | Passing deterministic tests | Supports code confidence only, not live readiness |
| Live macOS | `NOT RUN` because active-home migration was not authorized | Blocks full GO |
| Live Linux | `NOT RUN` because runner unavailable | Blocks full GO |
| Live native Windows | `NOT RUN` because runner unavailable | Blocks full GO |
| Live WSL | `NOT RUN` because runner unavailable | Blocks full GO |

## Final Sign-Off Checklist

- [ ] Final revision and clean/dirty state recorded.
- [ ] Mandatory focused and full automated suites pass.
- [ ] Pytest evidence is either passing or explicitly `NOT RUN` with reason.
- [ ] Watcher restarted before runtime verification.
- [ ] Scratch-home flow passes before any live-home action.
- [ ] Fresh inventory reviewed and authorized for the exact active home.
- [ ] Current generated roster used; historical 113 count not used as expectation.
- [ ] First deployment preserves foreign content and reports every collision/failure.
- [ ] Expected destinations are regular, fresh, and do not link into the repository.
- [ ] Second deployment is a zero-mutation fixed point.
- [ ] Retired interceptors are absent; scanner/framework and explicit RTK pass.
- [ ] Supported guidance contains no runtime-link creation, repair, or validation path.
- [ ] macOS fresh-session evidence passes.
- [ ] Linux fresh-session evidence passes.
- [ ] Native Windows fresh-session evidence passes.
- [ ] WSL fresh-session evidence passes.
- [ ] Final verdict respects the evidence ceiling.
