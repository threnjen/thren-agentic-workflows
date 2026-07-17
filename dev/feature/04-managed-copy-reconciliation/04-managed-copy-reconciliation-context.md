# Feature Context: Managed-Copy Reconciliation

## Feature Boundary

This feature owns the mutation layer that converts repository-owned runtime links, junctions, and managed copies into safe regular user-global copies. It consumes the normalized destination records produced by `03-cross-platform-destinations` and runs only through the convergence and per-harness orchestration boundary established by `02-propagation-convergence`.

This feature does not resolve platform destinations, invent generated asset rosters, change source propagation, rewrite setup guidance, or perform live author-home migration. It supplies the reusable inventory, staging, replacement, ownership, collision, verification, and pruning behavior that later guidance and integration features invoke.

## Key Files and Modules

| Path | Status | Relevance |
|---|---|---|
| `scripts/propagate_master_assets.py` | Existing, verified | Current propagation entry point, generated markers, path-containment helpers, structured result counters, and orchestration integration surface. |
| `scripts/runtime_deployment.py` | `[PROPOSED - name TBD]` | Proposed shared module from Features 2 and 3. The managed-copy API, ownership model, inventory classifier, staging/replacement operations, and harness result data may live here if that remains the settled upstream structure. |
| `tests/test_propagate_master_assets.py` | Existing, verified | Existing propagation, marker, path-containment, symlink-replacement, and orphan-pruning regression coverage. Update only shared contracts and CLI/result integration; preserve repository-generation behavior. |
| `tests/test_phase04_runtime_deployment.py` | `[PROPOSED - name TBD]` | Proposed consolidated Phase 04 scratch-home coverage for managed copies, live and dangling repository links, foreign collisions, failure preservation, pruning, and idempotency. |
| `docs/phases/PHASE_04/PHASE_04_SUMMARY.md` | Existing, verified; read-only input | Authoritative ownership, collision, migration, failure-isolation, and cross-platform requirements. |
| `docs/phases/PHASE_04/PHASE_04_DISCOVERY_CONTEXT.md` | Existing, verified; read-only input | Records the 2026-07-16 author-machine link baseline, documented runtime destinations, and platform constraints. |
| `claude/`, `codex/`, `opencode/` | Existing, verified; read-only deployment sources | Generated platform roots are the only source of deployed content. Never copy from existing runtime links or hand-maintained source roots. |

## Discovery Delta

| Finding | Impact | Action |
|---|---|---|
| `scripts/runtime_deployment.py` and `tests/test_phase04_runtime_deployment.py` do not yet exist. | The plan correctly labels both paths `[PROPOSED - name TBD]`; implementation must consume the exact file/API settled by upstream Features 2 and 3 rather than assuming these names. | Verify upstream implementation before editing; update imports, tests, and implementation notes together if names differ. |
| Existing `_prune_orphaned_outputs` and `_prune_orphaned_skill_dirs` intentionally skip symlinks and operate only inside repository generated roots. | They are useful safety references but cannot satisfy runtime migration, which must replace or remove proven repository-owned links and preserve all foreign links. | Implement a separate runtime ownership and reconciliation contract; do not broaden the repository pruners blindly. |
| Existing `_write_if_changed` unlinks or removes the destination before its final write and suppresses several removal errors. | Reusing it for user-global deployment would violate AC8 and AC9 because a failed final write can destroy the prior usable destination. | Add an explicit task for stage-and-verify-before-replacement with failure-preserving cleanup. |
| Existing `_generated_marker_line_index`, `_is_generated_output`, `GENERATED_AGENT_MARKDOWN_HEADER`, `GENERATED_AGENT_HEADER`, and `GENERATED_SKILL_HEADER` provide verified marker semantics. | Runtime ownership can reuse marker recognition where valid, but skills contain a marker in `SKILL.md` and non-hook assets do not have `$source` metadata. | Centralize one runtime ownership predicate that handles each generated asset type and does not require `$source` on agents or skills. |
| Existing containment helpers `_validate_output_directory` and `_validate_nested_output_directory` protect repository output roots; learning records require root validation before enumeration. | Runtime deployment needs the same fail-closed shape against the active-home boundary, including symlinked or junction-based parents. | Reuse the pattern where contracts match, but validate the user-global root before inventory or pruning and preserve the leaf for link classification. |
| Existing exact tests include `test_hook_asset_copy_replaces_symlink_without_writing_through_it`, `test_hook_asset_copy_rejects_symlinked_intermediate_directory`, `test_symlinked_orphan_is_not_unlinked`, and `test_prune_refuses_a_root_escaping_through_a_symlinked_parent`. | These are valuable regressions and design evidence, but they do not cover the new user-global transaction and ownership rules. | Preserve them and add distinct scratch-home scenarios rather than repurposing their names as new test claims. |
| The active Python 3.12.6 environment lacks `pytest`. | Automated execution is runner-constrained in this environment even though pytest is declared as a development dependency. | Write tests as required, run them when dependencies are available, and distinguish runner-constrained evidence from pass/fail evidence. |

## Verified Existing Contracts

- `propagate_once` returns structured integer counters and uses an injected `repo_root` for isolated tests.
- Generated asset ownership markers are type-specific: `GENERATED_AGENT_MARKDOWN_HEADER` for Claude/OpenCode Markdown, `GENERATED_AGENT_HEADER` for Codex TOML, and `GENERATED_SKILL_HEADER` in generated skill `SKILL.md` files.
- `$source` metadata applies to propagated hook JSON, not to generated agents, commands, profiles, or skills.
- Repository orphan pruning requires both absence from the expected roster and positive marker evidence; unreadable, unmarked, and symlink entries survive.
- Repository generation validates output roots before enumeration and rejects escaping or symlinked parent paths.
- No user-global managed-copy, Windows-junction, ownership-metadata, collision-inventory, or per-harness replacement API exists in the verified current code.
- The 113 repository-targeting links recorded in Phase discovery are a changing baseline, not a constant or expected assertion count.

## Architectural Decisions

### One Managed-Copy Contract

Expose one reusable managed-copy operation `[PROPOSED - name TBD]` that accepts Feature 3 destination records and the per-harness execution boundary from Feature 2. It returns structured outcomes for inventory, copied, replaced, removed, unchanged, collision, failed, and skipped-prune states. Feature 5 documents this operation, and Feature 6 invokes the same operation for integration evidence.

The operation must not independently resolve platform paths or regenerate source rosters. If the upstream record/API names differ from the proposals, adopt the settled upstream names and record the change in the implementation notes.

### Ownership Independent of Destination Existence

Represent ownership through verified generated markers or equivalent deployment metadata that is derived before mutation and remains meaningful when a destination is missing or dangling. A destination's name or mere presence in an expected roster is not ownership proof.

Use one ownership predicate for overwrite and prune authorization. The predicate must distinguish:

- generated regular files with a valid type-specific marker;
- generated skill directories whose owned marker is in `SKILL.md`;
- deployment metadata for copies whose content type cannot safely carry a marker;
- live or dangling links whose recorded target belongs to this repository's generated roots;
- foreign, unmarked, unreadable, or ambiguous content, which always fails closed.

### Non-Following Inventory

Classify the destination entry itself before reading content or resolving ownership. Link target resolution may be used only to prove that the recorded target lies inside a canonical generated root; deletion or replacement must unlink the directory entry and must never traverse the target. Validate the active-home enumeration root and every existing parent before walking descendants.

For dangling links, retain and normalize the recorded target even though normal existence checks fail. Windows reparse-point and junction handling stays behind the narrowest platform adapter and must not require elevation or Developer Mode.

### Stage, Verify, Then Replace

Build each complete replacement beside its final destination, verify the staged file or directory against the generated source roster, and only then perform the narrow replacement. Keep the old entry usable until the staged asset is complete. If replacement cannot be atomic for a platform or entry type, use the safest recoverable sequence and preserve or restore the prior entry on failure.

The existing `_write_if_changed` is not the runtime transaction primitive because it removes the destination before the final write and suppresses some errors. Runtime deployment must report permission failures, sharing violations, and race losses explicitly.

### Harness-Scoped Destructive Authorization

Copy and verification success authorizes pruning only for that same harness. Any failure during inventory validation, staging, replacement, or verification marks the harness failed and suppresses destructive reconciliation for it. A successful harness remains committed when another harness fails; there is no cross-harness rollback.

### Observability

Extend the structured result model from Features 2 and 3. Normal output should aggregate categories by harness and asset class; avoid noisy per-file success logs. Failure and collision records must be reviewable while home-relativizing or redacting sensitive absolute paths. A collision is an expected preserved state, not permission to overwrite.

## Correctness and Failure Constraints

- Refresh inventory immediately before mutation; never rely on the 2026-07-16 count of 113 links.
- Generated repository outputs are the only copy sources; never follow a runtime link and copy whatever it currently points to.
- A whole-directory repository link is unlinked as one entry and replaced with a real directory populated from the matching generated root.
- A per-file or per-skill repository link becomes a regular file or directory.
- A repository-owned dangling link is replaced when a generated source exists and removed only when the corresponding output is obsolete.
- Foreign files, directories, links, package-manager links, plugin-cache links, debug pointers, and Git hook links survive and appear as collisions or preserved exclusions.
- Stale regular files and directories are pruned only with positive ownership evidence; ambiguous and unreadable entries survive.
- A symlinked or junction-based parent that escapes the injected active home blocks that destination before enumeration or mutation.
- Recheck relevant entry facts immediately before replacement to reduce time-of-check/time-of-use races.
- Windows sharing violations, locked files, permission errors, and verification failures preserve the prior destination and skip pruning for the affected harness or destination as required by the settled Feature 2 status contract.
- Temporary staging artifacts must be cleaned only when cleanup cannot touch the prior destination or foreign content.
- A second run against unchanged generated outputs and runtime copies reports no mutations and leaves no managed symlink or junction into the repository.

## Scope Boundaries

- Do not modify destination resolution rules or environment-variable semantics established by `03-cross-platform-destinations`.
- Do not alter source propagation naming, marker placement, or fixed-point logic unless a verified shared contract requires a narrow integration change.
- Do not deploy hooks, plugin packages, project-local assets, another user's home, another WSL distribution, or the paired native Windows/WSL environment.
- Do not migrate the author's live home in automated tests or during this feature's implementation handoff.
- Do not delete or rewrite application-managed links, package-manager links, plugin-cache links, debug pointers, or Git hook links.
- Do not rewrite Evangelize, setup guides, or records; `05-deployment-guidance` owns those documents.
- Do not claim full cross-platform GO from simulated tests; `06-runtime-verification` owns live platform evidence.

## Relationships to Sibling Plans

| Feature | Relationship |
|---|---|
| `01-interceptor-retirement` | Earlier shared propagator change; do not restore retired hook behavior or use retired guard metadata as runtime ownership evidence. |
| `02-propagation-convergence` | Runtime and shared-file prerequisite. Reuse its convergence gate, per-harness transaction boundary, and structured outcome model; failed or non-converged propagation cannot reach this feature. |
| `03-cross-platform-destinations` | Direct API prerequisite. Consume its destination records and active-home boundaries without recomputing platform or environment policy. |
| `05-deployment-guidance` | Downstream documentation consumer. It must invoke or verify the settled managed-copy operation and describe collision/failure behavior accurately. |
| `06-runtime-verification` | Downstream integration consumer. It exercises scratch-home and live-platform deployment through this same API, verifies regular-copy freshness, and inventories remaining links. |

## Environment State

| Property | Value |
|---|---|
| Tech Stack | Python 3.12.6; standard-library `pathlib`, `shutil`, dataclasses, JSON, and filesystem operations; Markdown/TOML generated assets |
| Host Captured | macOS on 2026-07-16 |
| Test Runner | `python3 -m pytest tests/test_propagate_master_assets.py tests/test_phase04_runtime_deployment.py -q` |
| Test Baseline | Runner constrained on 2026-07-16: active `python3` reports `No module named pytest`; no pass/fail baseline captured for this feature |
| Test Dependencies | `requirements-dev.txt` declares `pytest>=9.0,<10` and `pytest-cov>=7.0,<8` |
| Lint | Not configured in `pyproject.toml` |
| Format | Not configured in `pyproject.toml` |

Runner constraints: native Windows junction classification, sharing violations, and WSL runtime behavior require their respective environments. Unit tests should inject platform adapters and error conditions, but unavailable live platforms must remain `NOT RUN` rather than inferred.

## Relevant Learnings

### Generated ownership and convergence

From `.github/learnings/cross-phase-decisions.md`:

- Generated roots are `claude/`, `opencode/`, and `codex/`; user-global `.claude` and `.codex` paths are destinations, not source roots.
- Marker placement is type-specific, and generated skills differ from their `.github/skills` sources by the generated marker line.
- `$source` is a hook JSON contract and must not be assumed on non-hook assets.
- Unmarked old orphans are deliberately unprunable; absence from the expected roster is not ownership proof.
- A stale long-running watcher can emit old behavior. Restart it before trusting deployment evidence.
- Repository propagation can require multiple passes after reclassification, so managed-copy deployment must remain behind the verified fixed-point gate.

### Root validation before destructive enumeration

From `.github/learnings/review-learnings.md` and `.github/learnings/debugging-learnings.md`:

- Validate resolved source assets and destination directories against declared roots before reading, writing, or walking them.
- Leaf-only checks do not protect against a symlinked parent; validate the enumeration root before globbing or recursive deletion.
- Deletion is less reversible than writing, so destructive sweeps must fail loudly and tests must prove both refusal of an escaping parent and continued operation for a legitimate root.
- Procedural collision handling must implement explicit create, reuse, recreate, and refusal branches; prose describing a policy does not make an unconditional copy or cleanup safe.

### No additional managed-copy rule

`.github/learnings/project-learnings.md` contains no additional managed-copy ownership or reconciliation contract applicable to this feature.

## Unverified Assumptions

- The exact public destination-record, per-harness result, and managed-copy API names and module placement remain unsettled until Features 2 and 3 are implemented.
- Python's platform APIs may not distinguish all supported Windows junction/reparse-point cases consistently. The implementation must verify native Windows behavior and isolate any platform-specific classifier.
- The repository's generated markers may be sufficient ownership evidence for most regular copies, but directory-level or non-marker asset classes may require separate deployment metadata. The exact metadata representation must be chosen conservatively and documented.
- Atomic replacement semantics differ by platform and file-versus-directory type. The implementation must verify the safest available operation and test recovery behavior rather than assuming POSIX rename semantics on Windows.

## Implementation Handoff Checklist

- Consume settled upstream APIs; do not duplicate convergence or destination resolution.
- Inventory without following destination links and validate roots before enumeration.
- Use one positive ownership predicate for overwrite and pruning.
- Stage and verify complete replacements before changing the prior destination.
- Preserve every foreign or ambiguous collision.
- Suppress destructive reconciliation after failure in the affected harness.
- Keep structured results reviewable and normal-path logging quiet.
- Distinguish simulated, runner-constrained, code-review, and live-platform evidence.

