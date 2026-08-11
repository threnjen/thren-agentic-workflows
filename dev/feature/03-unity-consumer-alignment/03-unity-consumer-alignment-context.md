# Feature Context: Unity Consumer Alignment

## Key Files

### Files to Change

| File / Module | Role | Change Type |
|---------------|------|-------------|
| `source_of_truth/agents/04-phase-execute.agent.md` | Owns Step 2.5, the wave-level evidence gate, retry behavior, `not-executed` handling, and direct-supervisor attestation. | Modify |
| `source_of_truth/agents/04g-unity-visual-verification.agent.md` | Owns Unity editor discovery, saved machine-local editor-path handling, the PlayMode capture invocation, and rendered-evidence verification. | Modify |
| `source_of_truth/agents/04h-unity-reviewer.agent.md` | Owns the Unity review compile/test gate and conditional serialized-asset import validation. | Modify |
| `tests/[PROPOSED - name TBD: Unity consumer contract guards]` | New focused structural guard module for the three consumer contracts, including non-vacuity and mutation/negation proof. No corresponding file or test class exists yet. | Create |

### Read-Only References

| File / Module | Role | Change Type |
|---------------|------|-------------|
| `source_of_truth/skills/unity-development/SKILL.md` | Canonical Test Execution and Serialized Assets contracts produced by Features 01 and 02; consumers reference these rules rather than copying them. | Read-only reference |
| `docs/AUTHORING.md` | Repository-specific agent-authoring rules: preserve harness-neutral display names, source-only authoring, executable branches, and terse definitions. | Read-only reference |
| `docs/phases/PHASE_01/PHASE_01_SUMMARY.md` | Phase requirements, risk register, integration points, and success criteria for consumer alignment. | Read-only reference |
| `docs/phases/PHASE_01/PHASE_01_DISCOVERY_CONTEXT.md` | Verified reference-project facts, worktree decisions, Unity version, and maintainer decisions. | Read-only reference |
| `dev/feature/01-unity-test-execution-contract/01-unity-test-execution-contract-plan.md` | Upstream public Test Execution contract and its guard ownership. | Read-only reference |
| `dev/feature/02-headless-asset-import/02-headless-asset-import-plan.md` | Upstream Serialized Assets/import contract and shared guard ownership. | Read-only reference |
| `dev/feature/04-unity-test-reference-assets/04-unity-test-reference-assets-plan.md` | Parallel-safe sibling consuming the same finalized skill contracts through disjoint files. | Read-only reference |
| `tests/test_agent_corpus_invariants.py` | Existing structural frontmatter, roster, `applyTo`, and duplicate-block invariants; intentionally does not pin agent prose. | Read-only reference |
| `tests/test_propagate_master_assets.py` | Existing propagation, alias, consumer-path, and generated-sync coverage; source-only edits can leave sync checks red until maintainer propagation. | Read-only reference |
| `tests/test_pr_review_orchestrator.py` | Source of one unrelated current baseline failure; must remain distinguishable from feature regressions. | Read-only reference |

## Discovery Delta

| Finding | Impact | Action |
|---------|--------|--------|
| All three referenced consumer files and the exact plan sections exist: Phase Execute `### Step 2.5: Wave Test Gate`, Visual Verifier Steps 1–2, and Unity Reviewer `### Phase 2: Compilation Check`. | The plan targets valid source files and existing headings; no symbol-name correction is needed. | Use these headings as structural test boundaries. |
| The proposed focused consumer guard file does not exist, and no existing test class represents this contract. Existing propagation tests mention the consumer paths only for generation/alias behavior. | AC6 requires new focused coverage; generic corpus tests cannot prove role-specific Unity command semantics. | Create `tests/[PROPOSED - name TBD: Unity consumer contract guards]`; keep the final filename and any class name proposed until the implementer chooses and records idiomatic names. |
| The checked-in `unity-development` skill still contains the pre-phase rules: `-batchmode` is described as optional and an Editor lock asks the user to run the suite. | This feature cannot align consumers against the current skill text without encoding a stale contract. This validates, and makes operationally important, the declared dependency on Features 01 and 02. | Do not begin consumer edits until both upstream features have finalized the Test Execution and Serialized Assets sections. Warn the Decomposer if scheduling does not enforce that dependency. |
| The full test baseline on 2026-08-10 is 141 passed and 2 failed. Failures are `tests/test_pr_review_orchestrator.py::test_agent_name_does_not_collide_with_prose_in_any_source_asset` and `tests/test_propagate_master_assets.py::InstructionApplyToTests::test_every_enumerated_applyto_target_exists`. | A later run must not attribute either existing failure to this feature. | Resolved: the plan now records both failures. Treat them as pre-existing unless their signatures change and report focused-test results separately. |
| No phase-scoped test directory or consolidated current-phase test module exists under `tests/`; the only phase-named hit is stale bytecode for a removed test module. | There is no omitted phase consolidation target to update. | Keep consumer coverage in the proposed focused module and run the named repository regression suites. |
| Phase Execute currently asks the user to run the suite on `not-executed`; Visual Verifier currently targets `-projectPath .`; Unity Reviewer points at the old Editor-lock rule. | These are the concrete stale behaviors AC1–AC4 are intended to replace. | Add red-first guards for each behavior before editing the agent definitions. |
| The consumer files use exact command tokens and status vocabulary whose relationships matter more than surrounding prose (`-batchmode`, `-runTests`, `-testPlatform PlayMode`, `-nographics`, `-quit`, `executed-green`, `executed-failing`, `not-executed`). | Broad substring checks could pass against unrelated sections or comments. | Scope parsing to the named consumer sections, assert non-vacuity, and test token combinations and branch relationships rather than arbitrary wording. |

## Architectural Decisions

- Keep the full worktree ladder, editor resolution, result-path rules, and import mechanics canonical in `unity-development`; consumer agents contain only role-specific decisions and explicit references to the canonical sections.
- Phase Execute owns orchestration semantics: absolute main-checkout result consumption, retry behavior, evidence statuses, the decline/unattended fallback, and the direct-supervisor-attestation exception.
- Visual Verifier remains the single verified editor-discovery procedure. Its saved executable path is independent of the `-projectPath` execution target.
- Visual capture always runs PlayMode with `-batchmode`, graphics enabled, and no `-quit` paired with `-runTests`; EditMode's `-nographics` rule must not leak into this consumer.
- Unity Reviewer distinguishes two permitted batch operations: tests follow Test Execution and exclude `-quit` with `-runTests`; serialized-asset import follows Serialized Assets and may use `-quit`.
- Use a dedicated focused guard module because `tests/test_agent_corpus_invariants.py` is deliberately structural and should not become coupled to rewordable agent prose.
- Derive the three consumer paths in the guard rather than maintaining an unrelated duplicate roster, then prove each consumer-specific mechanism can make the guard fail.

## Constraints

- Author only in `source_of_truth/`; never edit `ports/` or the real `.github/` mirror.
- Never run `scripts/propagate_master_assets.py`. Source/port sync failures after implementation mean maintainer propagation is pending.
- Preserve all three agents' frontmatter, tool grants, rosters, display names, numbering, and personality-canary content.
- Use harness-neutral display names when an agent references a sibling; do not introduce source slugs as invocation names.
- Keep runtime-loaded agent definitions terse. Do not repeat the full ladder or editor-discovery procedure in consumers.
- Preserve Phase Execute's wave retry budget, evidence status vocabulary, `all-approved: no` behavior, and direct-supervisor-attestation escape hatch.
- Preserve the existing affected-suite `-testFilter` semantics from the canonical Test Execution contract.
- Do not store machine-local editor paths, Unity license data, or reference-project-specific absolute editor paths in source definitions.
- Structural guards must be non-vacuous and must be demonstrated red through targeted deletion or negation before restoration.
- No Unity runtime execution is required for this feature; empirical Unity invocation verification belongs to Features 01 and 02.

## Scope Boundaries

- Do not modify `source_of_truth/skills/unity-development/SKILL.md`; Features 01 and 02 own it.
- Do not modify the GameCI template or local Unity runbook owned by `04-unity-test-reference-assets`.
- Do not redesign visual capture configuration, editor-path persistence, screenshot assessment, or the capture package contract.
- Do not remove supervisor attestation, alter the wave retry count, or weaken non-green handling.
- Do not broaden batchmode to unrelated Unity operations.
- Do not change generated ports, deploy assets, or run propagation.
- Do not fold consumer-specific prose assertions into the generic corpus-invariant suite unless reusing a genuinely structural helper without prose coupling.
- Preserve non-Unity uses of Phase Execute's generic `not-executed` branch.

## Relationships to Sibling Plans

- `01-unity-test-execution-contract` is a hard prerequisite. It defines mandatory headless execution, per-platform graphics rules, absolute result paths, worktree lifecycle, editor discovery reuse, and the three-rung fallback.
- `02-headless-asset-import` is a hard prerequisite after Feature 01. It finalizes the permitted serialized-asset import command and corrects Unity test-path guidance in the same skill.
- `03-unity-consumer-alignment` consumes those finalized public contracts and must not restate or fork them.
- `04-unity-test-reference-assets` also consumes Features 01 and 02 but changes disjoint files, so it may execute in parallel with this feature once both prerequisites finish.
- The focused consumer guard module is separate from the shared Unity skill guard module owned sequentially by Features 01 and 02.

## Suggested Implementation Order

1. Complete `01-unity-test-execution-contract`.
2. Complete `02-headless-asset-import` against the finalized skill.
3. In Wave 3, execute this feature in parallel with `04-unity-test-reference-assets` because their write scopes are disjoint.
4. Within this feature, add and prove the focused guards red, align Phase Execute, align the two Unity specialists, then run focused and repository regression checks.

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Python 3.12.6 structural test suite over Markdown agent/skill assets; pytest 9.1.1. This repository is not a Unity project, but the feature governs external Unity 6000.3.13f1 consumers. |
| Test Runner | `uv run pytest tests/` |
| Test Baseline | 141 passed, 2 failed — captured 2026-08-10. Existing failures: `test_agent_name_does_not_collide_with_prose_in_any_source_asset` and `InstructionApplyToTests::test_every_enumerated_applyto_target_exists`. |
| Lint | Not configured |
| Format | Not configured |

## Relevant Learnings

None applicable. No `docs/learnings/*.md` files exist in this repository.
