# Feature Context: Runtime Verification

## Feature Boundary

This is the Phase 04 integration/bootstrap feature. It composes the upstream convergence, destination-resolution, managed-copy reconciliation, and guidance contracts into one runnable path through the existing propagation CLI, then records scratch-home, live-runtime, and repository fixed-point evidence. It does not reimplement any upstream policy and does not infer unavailable platform results.

The automated boundary ends at temporary repositories and temporary active homes. Mutation of the author's live runtime directories requires a fresh inventory, explicit human review, and a second inventory immediately before execution. Native Windows and WSL are separate environments and require separate runs.

## Key Files and Modules

| Path | Status | Relevance |
|---|---|---|
| `scripts/propagate_master_assets.py` | Existing, verified | Current CLI and integration entry point. Verified public functions include `propagate_once`, `watch_loop`, `generate_global_hooks`, and `main`. The current parser exposes only `--once`, `--watch`, and `--global-output`; the Phase 04 end-to-end option remains `[PROPOSED - name TBD]`. |
| `scripts/runtime_deployment.py` | `[PROPOSED - name TBD]`; missing at discovery | Planned shared module from upstream Features 2–4. Feature 6 must import and compose its settled public APIs rather than duplicate convergence, destination, ownership, copy, or reconciliation logic. |
| `tests/test_phase04_runtime_deployment.py` | `[PROPOSED - name TBD]`; missing at discovery | Proposed consolidated Phase 04 scratch-home integration coverage. Match the repository's standard-library `unittest` style unless upstream implementation establishes a different local convention. |
| `tests/test_propagate_master_assets.py` | Existing, verified | Contains 42 `unittest` tests and current CLI/propagation, containment, regular-file hook-copy, idempotency, and orphan-pruning coverage. Add only integration-boundary regressions that belong with the CLI rather than the consolidated workflow file. |
| `tests/hooks/test_hook_distribution_integration.py` | Existing, verified; update only if still required after Feature 1 | Pytest-based mixed hook suite. Several verified tests are guard-specific and are expected to be removed or rewritten by Feature 1. Feature 6 should verify surviving scanner/framework behavior without restoring retired guard or latency assertions. |
| `.github/learnings/cross-phase-decisions.md` | Existing, verified | Authoritative cross-phase decision record. Final claims must identify the revision and distinguish implemented behavior from fresh verification. Do not reinterpret older uses of “Phase 04” without accounting for the documented renumbering history. |
| `.github/learnings/project-learnings.md` | Existing, verified | Project-level operational lessons and measured final behavior. Add only durable findings supported by final evidence. |
| `claude/learnings/cross-phase-decisions.md` | Existing generated copy | Must be regenerated through `propagate_learnings_once` after its `.github` source changes; do not hand-author divergent content. |
| `claude/learnings/project-learnings.md` | Existing generated copy | Must be regenerated through `propagate_learnings_once` after its `.github` source changes; do not hand-author divergent content. |
| `docs/phases/PHASE_04/PHASE_04_DISCOVERY_CONTEXT.md` | Existing, verified | Holds the 2026-07-16 research and 113-link author-machine baseline. Preserve the baseline as historical evidence and append or clearly distinguish fresh inventory results rather than replacing it with an assumed constant. |
| `docs/phases/PHASE_04/PHASE_04_SUMMARY.md` | Existing, verified | Authoritative phase scope and acceptance boundaries. Record final evidence without moving Phase 01, Phase 02, or Phase 07 status lines. |

## Discovery Delta

| Finding | Impact | Action |
|---|---|---|
| `scripts/runtime_deployment.py` does not exist in the pre-implementation tree. | The plan correctly labels it proposed, but Feature 6 cannot select API names in advance. | At implementation start, inventory the actual public APIs delivered by Features 2–4 and update imports/tests to those settled names. Do not create a second integration module merely to preserve the placeholder. |
| `tests/test_phase04_runtime_deployment.py` does not exist. | The consolidated suite is a new verification asset, not an existing test contract. | Create it only once, use scenario descriptions rather than presuming test method names, and keep all home paths temporary. |
| The existing `main` parser has only `--once`, `--watch`, and `--global-output`. | The exact end-to-end CLI flag is not codebase-verified. | Select the narrowest parser extension consistent with upstream Features 2–4; record the final name in implementation notes and preserve existing default-one-pass behavior unless an upstream acceptance criterion intentionally changes it. |
| `tests/test_propagate_master_assets.py` has a runnable 42-test `unittest` baseline, but the hook integration suite requires pytest and pytest is absent from the active interpreter. | Evidence has two runner classes; a pytest failure cannot be claimed from this environment because collection cannot start. | Keep new core integration coverage runnable under `unittest` where practical. Record pytest checks as runner-constrained until dependencies are installed, and never report them as passed based on code review. |
| `tests/hooks/test_hook_distribution_integration.py` currently contains verified guard-specific smoke and latency tests alongside independent scanner/framework tests. | Blindly retaining the file's current assertions would contradict Feature 1 retirement; blindly deleting the file would weaken independent Phase 02 protection. | Re-read the post-Feature-1 version. Retain or add only surviving shared-framework and prompt-injection evidence; treat whether this file needs a Feature 6 edit as a verified-at-execution decision. |
| `propagate_learnings_once` copies every `.github/learnings/*.md` file into `claude/learnings/`. | Directly editing both copies risks divergence and can defeat the final fixed-point claim. | Edit `.github/learnings/` sources, regenerate the Claude copies through propagation, then require an immediate zero-change verification pass. |
| The discovery document's 113 runtime links are explicitly a historical baseline. | Hard-coding 113 would make migration verification stale and machine-specific. | Generate and review a fresh classified inventory; preserve both the old baseline and new timestamped/revision-scoped evidence. |
| The graph does not currently link `scripts/propagate_master_assets.py` to tests through `tests_for`, despite the verified 42-test module. | Graph absence is a coverage-index limitation, not proof of missing tests. | Use the verified test module and direct baseline as the implementation evidence source. Accepted risk: graph test-edge coverage may remain incomplete. |

## Verified Existing Contracts

- `propagate_once` is the one-pass repository-generation primitive and returns structured inventory, change, and removal counters.
- `watch_loop` calls `propagate_once` at startup and after changes, so a watcher started before Phase 04 code lands must be restarted before migration or release verification.
- `main` defaults to one repository propagation pass when no current option is supplied.
- Generated repository roots are `claude/`, `codex/`, and `opencode/`; user-global deployment must consume these completed outputs rather than transform `.github` sources independently.
- Existing propagation safety checks reject escaping or symlink-diverted generated-output paths, and existing tests cover leaf and intermediate symlink cases.
- `propagate_learnings_once` makes `.github/learnings/` authoritative over `claude/learnings/`.
- The Phase document requires one current-environment run only. macOS, Linux, native Windows, and WSL results are separate evidence rows; unavailable platforms are `NOT RUN`.

## Architectural Decisions

1. **Keep the CLI integration thin.** Feature 6 calls the settled upstream public APIs in phase order: repository convergence, destination preflight, managed-copy deployment, owned stale reconciliation, and verification. It does not reproduce their internals.
2. **Use one structured end-to-end result.** Preserve per-stage and per-harness status, inventory counts, failure categories, and overall readiness in data. Human-readable output may summarize these fields but is not the verification contract.
3. **Separate scratch, live, and platform evidence.** Automated scratch-home success cannot stand in for live-home migration or fresh-session discovery. Each evidence class records its own environment, revision, command, result, and limitations.
4. **Make GO fail closed.** Any failed required check, partial harness result, unreviewed inventory, non-idempotent second run, unavailable platform, or `NOT RUN` required platform prevents a full cross-platform GO verdict.
5. **Verify freshness by content and roster evidence.** File type, source/version marker or content identity, expected roster membership, and runtime discovery establish freshness. Modification time alone is insufficient.
6. **Preserve historical ownership.** Phase 04 may correct its discovery, friction, deployment, composition, and security-posture records. Phase 01, Phase 02, and Phase 07 status lines remain owned by project-level reconciliation.
7. **Avoid new noisy logging.** One structured phase result and actionable failure diagnostics are sufficient. Do not add per-file normal-path logs or expose sensitive home paths/content.

## Contracts and Evidence Boundaries

- **Feature 2 input:** the settled bounded convergence/orchestration API and authoritative mutation classification.
- **Feature 3 input:** normalized current-environment destination records, including active-home and harness boundaries.
- **Feature 4 input:** ownership classification, staged replacement, managed-copy verification, per-harness failure isolation, and safe reconciliation APIs.
- **Feature 5 input:** supported setup guidance and generated Evangelize outputs that invoke or verify this same entry point.
- **Feature 6 output:** one executable phase path plus evidence showing scratch-home behavior, reviewed live inventory, available-platform runtime discovery, hook/RTK survival and retirement, repository fixed point, deployment idempotency, and explicit limitations.
- If an upstream API name or result shape differs from its proposed planning name, use the implemented upstream contract and record the naming delta. Duplication is not an acceptable compatibility strategy.

## Constraints and Failure Handling

- Never point automated tests at `Path.home()` or mutate the author's live Claude, Codex, OpenCode, or shared skill roots.
- Require a reviewable preflight inventory before live mutation, then inventory again immediately before execution and stop if classifications drift materially.
- Preserve the old usable destination when replacement fails; do not prune that harness after a copy or verification failure.
- Do not follow a symlink or junction during classification or deletion. Validate the containing root before enumeration.
- A successful harness remains successful if another harness fails, but the phase verdict is partial/non-GO.
- Restart long-running propagation watchers before trusting final propagation or deployment evidence.
- Run runtime-discovery checks in fresh processes/sessions so cached agents, watchers, or loaded configuration cannot create false passes.
- Treat explicit RTK usability as a manual/runtime check independent of automatic rewriting. Do not use the retired hook as the verification mechanism.
- Do not infer native Windows or WSL behavior from POSIX path-policy simulations.
- Record the exact revision under test; stale evidence does not verify current code.

## Scope Boundaries

- Do not uninstall or modify the RTK executable.
- Do not restore the retired file-access guard, Bash analyzer, or automatic RTK rewrite hook.
- Do not remove or weaken the shared hook framework or prompt-injection scanner.
- Do not deploy across native Windows/WSL boundaries, across WSL distributions, or into another user's home.
- Do not deploy project-local assets, packages, plugins, user-global hooks, unrelated application-managed links, package-manager links, plugin-cache links, debug pointers, or Git hook links.
- Do not hand-edit generated learning copies independently of their `.github/learnings/` sources.
- Do not move Phase 01, Phase 02, or Phase 07 status lines.

## Relationships to Sibling Plans

| Feature | Relationship |
|---|---|
| `01-interceptor-retirement` | Supplies the retired hook roster and surviving scanner/framework state. Final verification must prove behavior, not only file absence. |
| `02-propagation-convergence` | Supplies the fixed-point gate, preflight ordering, structured result, and per-harness failure semantics consumed by the end-to-end path. |
| `03-cross-platform-destinations` | Supplies normalized current-environment destination records and the platform/override policy exercised by scratch and live evidence. |
| `04-managed-copy-reconciliation` | Supplies ownership proof, safe replacement, collision preservation, stale reconciliation, and idempotency behavior. |
| `05-deployment-guidance` | Documents and regenerates the supported workflow. Feature 6 verifies the documented command against the actual integration entry point. |

Execution is sequential after all five siblings because Feature 6 consumes their runtime contracts and shares the propagation CLI, deployment support module, tests, generated learnings, and phase records.

## Environment State

| Property | Value |
|---|---|
| Tech Stack | Python 3.12.6; standard-library propagation CLI; `unittest` and pytest test modules; Markdown/TOML generated assets |
| Host Captured | macOS Darwin arm64 on 2026-07-16 |
| Focused Test Runner | `python3 -m unittest tests.test_propagate_master_assets -q` |
| Focused Test Baseline | 42 passed, 0 failed in 1.939s — captured 2026-07-16 |
| Planned Consolidated Runner | `python3 -m unittest tests.test_phase04_runtime_deployment -v` `[PROPOSED - name TBD]` |
| Pytest Runner | `python3 -m pytest tests/hooks/test_hook_distribution_integration.py -q` |
| Pytest Baseline | Runner constrained on 2026-07-16: active `python3` reports `No module named pytest`; no pass/fail claim available |
| Test Dependencies | `requirements-dev.txt` declares `pytest>=9.0,<10` and `pytest-cov>=7.0,<8` |
| Lint | Not configured in `pyproject.toml` |
| Format | Not configured in `pyproject.toml` |

## Relevant Learnings

- **Fresh evidence must name its revision.** `.github/learnings/cross-phase-decisions.md` states that implemented remediation is not verification and that a stale finding is not a current finding. Final platform and record claims must identify the code revision they cover.
- **Generated roots and ownership markers are type-specific.** The same learning file defines `claude/`, `codex/`, and `opencode/` as generated roots and records distinct markers for generated Markdown, skill Markdown, and Codex TOML. Runtime freshness and ownership checks must use the applicable contract rather than one universal marker assumption.
- **Restart stale watchers and prove convergence.** The propagation contracts record that a watcher retains old code and that reclassification can require multiple runs. Final evidence must restart watchers and require an immediate zero-change verification pass.
- **Validate roots before enumeration.** `.github/learnings/debugging-learnings.md` records that leaf checks do not make deletion safe when an enumeration root or parent escapes. Live inventory and reconciliation checks must validate roots before walking them.
- **Validate both source and destination containment.** `.github/learnings/review-learnings.md` requires resolved source assets and resolved destination directories to remain inside their declared roots; leaf-only link handling is insufficient.
- **`NOT RUN` caps readiness.** `.github/learnings/review-learnings.md` records that failed delegated evidence needs a concrete `NOT RUN` reason and an explicit below-GO ceiling. Apply the same honest classification to unavailable platform verification.
- **Use the resolved interpreter for subprocesses.** `.github/learnings/project-learnings.md` records pyenv/asdf shim distortion. Fresh-process CLI tests should invoke `sys.executable`, not a bare `python3`, when spawning from Python.

## Implementation Handoff Checklist

- Re-read upstream implementation records and replace all proposed names with settled APIs before coding the integration.
- Preserve existing CLI behavior and add only the narrow Phase 04 orchestration surface.
- Keep automated fixtures in temporary repository and home roots.
- Capture a fresh, reviewed live inventory; never reuse 113 as an expected count.
- Record each platform independently and cap the verdict when required evidence is failed or `NOT RUN`.
- Verify regular-copy type, freshness, roster coverage, runtime discovery, fixed point, and second-run idempotency.
- Verify surviving scanner/framework behavior, absence of retired interception, and explicit RTK usability without conflating them.
- Update authoritative learning sources, regenerate copies, and finish with an immediate zero-change repository propagation pass.
- Keep evidence categories explicit: automated pass/fail, runner-constrained, code review, manual QA, failure, and `NOT RUN`.

## Unverified Assumptions

- The exact public API and result names produced by Features 2–4 are not known until those sequential features are implemented.
- The final supported CLI flag is not known; the existing parser provides no deployment option yet.
- Live Linux, native Windows, and WSL environments may be unavailable during implementation. Their absence must remain `NOT RUN` and block a full cross-platform GO verdict.
- Runtime-specific commands for proving fresh-session discovery must be confirmed against the installed harness versions and Feature 5 guidance before execution.
