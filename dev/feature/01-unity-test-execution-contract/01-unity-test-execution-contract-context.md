# Context: Unity Test Execution Contract

## Key Files

### Files Changed

| File / Module | Role | Change Type |
|---|---|---|
| `source_of_truth/skills/unity-development/SKILL.md` — `## Test Execution` | Canonical machine-facing Unity test invocation, evidence, editor-lock, and affected-suite contract | Modify |
| `tests/[PROPOSED - name TBD: Unity skill contract guards]` | Focused structural guards and mutation probes for AC1–AC10 and AC12; no file or test class with this name currently exists | Create |

### Read-Only References

| File / Module | Role | Change Type |
|---|---|---|
| `source_of_truth/agents/04g-unity-visual-verification.agent.md` — Step 1 | Existing editor-discovery procedure and verified PlayMode constraints: graphics on, no `-nographics`, and no `-quit` with `-runTests` | Read-only reference |
| `source_of_truth/instructions/test-execution-evidence.instructions.md` | Authoritative executed/not-executed evidence vocabulary referenced by the skill | Read-only reference |
| `source_of_truth/skills/guard-integrity/SKILL.md` | Mutation, negation, non-vacuity, derivation, and whitespace-normalization rules for content guards | Read-only reference |
| `tests/test_agent_corpus_invariants.py` | Existing generic structural corpus guards and normalization precedent; intentionally not extended with prose-contract assertions | Read-only reference |
| `docs/phases/PHASE_01/PHASE_01_SUMMARY.md` | Phase requirements, decisions, risks, manual QA conditions, and success criteria | Read-only reference |
| `docs/phases/PHASE_01/PHASE_01_DISCOVERY_CONTEXT.md` | Verified reference-project facts and maintainer decisions | Read-only reference |
| `dev/feature/02-headless-asset-import/02-headless-asset-import-plan.md` | Sequential downstream owner of other sections in the same skill and the shared proposed guard module | Read-only reference |
| `dev/feature/03-unity-consumer-alignment/03-unity-consumer-alignment-plan.md` | Downstream consumer of the finalized Test Execution contract | Read-only reference |
| `dev/feature/04-unity-test-reference-assets/04-unity-test-reference-assets-plan.md` | Downstream documentation/reference-asset consumer of the finalized contract | Read-only reference |
| `/Users/jennywadkins/github_repos/the-movies/ProjectSettings/ProjectVersion.txt` | External manual-QA reference confirming Unity `6000.3.13f1` | Read-only reference |
| `/Users/jennywadkins/github_repos/the-movies` | External Unity project used only for AC11 execution evidence and its persistent sibling worktree | Read-only reference |

## Discovery Delta

| Finding | Impact | Action |
|---|---|---|
| The initial plan baseline was stale. A live `uv run pytest tests/` on 2026-08-10 collected 143 tests: 141 passed and 2 failed. The failures are `tests/test_pr_review_orchestrator.py::test_agent_name_does_not_collide_with_prose_in_any_source_asset` and `tests/test_propagate_master_assets.py::InstructionApplyToTests::test_every_enumerated_applyto_target_exists`. | Regression comparison must distinguish two pre-existing failures. | Resolved: the plan now records this live baseline. Preserve it in implementation and verification records; do not absorb either failure into this feature. |
| The current `## Test Execution` section exists and contains the exact conflicting rule, “`-batchmode` is optional,” a bare `Unity` command, a relative `dev/test-results/` destination, and an Editor-lock handoff that asks the user to run the suite. | AC1, AC4, AC5, and AC7–AC10 address verified defects rather than hypothetical wording. | Replace only this section's execution contract while preserving its affected-suite and XML parsing semantics. |
| `source_of_truth/agents/04g-unity-visual-verification.agent.md` contains the editor-discovery order required by AC4: environment override, machine-local JSON override, then project version plus Unity Hub locations. It also already forbids `-nographics` and `-quit` for PlayMode capture. | The plan points to a real, suitable canonical discovery procedure. | Link to that procedure; do not copy it into the skill. |
| No existing test file or test class implements the proposed Unity skill contract guards. The plan correctly labels the module `[PROPOSED - name TBD]` and does not invent exact test method or class names. | The implementer must choose the final idiomatic module and scenario names. | Keep the proposal marker in planning tasks until implementation records the selected name. |
| The repository has no phase-scoped test directory or consolidated current-phase test module under `tests/`; tests are flat modules. | No omitted phase-consolidated test file needs to be added to this feature. | Create one focused flat test module, consistent with repository layout. |
| The plan includes explicit impact analysis: generic corpus prose assertions stay untouched, a new focused guard module is required, and the external Unity check remains manual QA. | No missing refactor/rewire test-maintenance analysis was found. | Follow the stated split between automated guards and AC11 manual evidence. |
| The external reference project exists, is currently clean, reports Unity `6000.3.13f1`, and its current registered worktree list contains only the main checkout. Earlier phase discovery observed four stale prunable worktrees. | AC11's target/version remain valid; the stale-worktree observation is historical rather than current state. | Still prune registrations on each use as the contract requires; do not claim stale entries exist during the implementation run unless re-observed. |
| No `docs/learnings/*.md` files exist in this repository. | There are no repository learnings to apply to this feature. | Use the phase discovery and loaded guard-integrity rules as the relevant guidance. |

## Architectural Decisions

- Make `source_of_truth/skills/unity-development/SKILL.md` the single canonical execution contract. Consumer alignment is downstream work, and editor discovery remains owned by the existing Visual Verifier procedure.
- Require `-batchmode` for every agent-driven test run, but preserve a two-row platform split: EditMode adds `-nographics`; PlayMode and visual capture keep graphics enabled and explicitly exclude `-nographics`.
- Keep `-quit` out of every `-runTests` invocation because it can terminate before tests execute and create false-green exit codes.
- Test only committed code in a detached persistent sibling worktree at `<project-dir>-agent-tests/`. Refresh the checkout to the committed SHA while retaining the gitignored `Library/` cache.
- Treat the shadow worktree as execution-only. Resolve `-testResults` to an absolute path under the main checkout's `dev/test-results/` and read evidence only there.
- Use a bounded three-rung ladder: persistent worktree once; on licensing/lock failure, request Editor closure and run headless in the main checkout once; on decline or unattended silence, report the specified `not-executed` status.
- Persist one worktree per project indefinitely. Prune stale registrations before reuse, announce first-use cost and delay, forbid per-run worktree creation, and provide manual rather than automatic teardown.
- Keep guards structural and scoped. Parse section boundaries and table/command relationships, normalize irrelevant Markdown whitespace, assert non-vacuity, and prove each obligation red through deletion or semantic negation before restoring green.
- Add no helper script, runtime dependency, config format, or normal-path corpus logging. The simplest design is a concise policy rewrite plus focused Python guards.

## Constraints

- Author only in `source_of_truth/`; never hand-edit `ports/` or `.github/`.
- Do not run `scripts/propagate_master_assets.py`. Generated sync failures remain pending maintainer propagation.
- Keep the skill dense and terse because it is loaded into agent context at runtime; do not restate the same rationale in multiple places.
- Preserve the existing `-testFilter` semantics exactly: affected suites use a semicolon-separated list of full names or a regex with negation support; wave/phase gates remain unfiltered.
- Preserve the results-XML evidence rule: exit code zero is insufficient, missing/zero-test results are `not-executed`, and failures are read from `<test-case result="Failed">`.
- Commit-before-test is mandatory because a detached worktree cannot represent uncommitted main-checkout changes.
- Before reusing the fixed sibling path, verify its ownership and registration; never overwrite foreign content.
- Attempt each runnable ladder tier once. Never open a GUI, silently refuse, delegate the test run to the user, or wait indefinitely for an unattended response.
- Safely quote resolved filesystem paths. Never track machine-specific editor paths, license material, or secrets.
- Do not create, remove, or alter a worktree in this repository. AC11's worktree belongs to the external reference project and is a manual QA asset.

## Scope Boundaries

- Change only the `## Test Execution` section of `source_of_truth/skills/unity-development/SKILL.md` and the new focused guard module.
- Do not change Unity test assertions, Test Authenticity Rules, or the meaning of `-testFilter`.
- Do not change serialized-asset generation, headless asset import, or EditMode test-path guidance; Feature 02 owns those sections.
- Do not edit Phase Execute, Visual Verifier, Unity Reviewer, or any other consumer agent; Feature 03 owns consumer alignment.
- Do not create the GameCI template or local Unity runbook; Feature 04 owns those reference assets.
- Do not modify the external reference project's source or tests. AC11 may create or reuse its execution-only sibling worktree and write evidence to the main checkout's gitignored `dev/test-results/`.
- Do not automate teardown of the persistent reference-project worktree.
- Do not add prose-contract assertions to `tests/test_agent_corpus_invariants.py`.

## Relationships to Sibling Plans

- `02-headless-asset-import` depends on this feature and must run after it because both modify `unity-development/SKILL.md` and the same proposed focused guard module. Feature 02 must preserve this feature's Test Execution ladder and flags.
- `03-unity-consumer-alignment` depends on Features 01 and 02. It updates Phase Execute, Visual Verifier, and Unity Reviewer to consume the finalized canonical contracts without duplicating them.
- `04-unity-test-reference-assets` depends on Features 01 and 02. Its GameCI template and human runbook must reflect this feature's platform flags, worktree lifecycle, result path, and fallback ladder.
- This feature establishes the upstream public documentation contract required by all three sibling plans; no new runtime API is introduced.

## Suggested Implementation Order

1. Execute this feature in Wave 1 and finalize its guards and Test Execution contract.
2. Execute `02-headless-asset-import` in Wave 2 because it shares the skill and focused guard module.
3. Execute `03-unity-consumer-alignment` and `04-unity-test-reference-assets` in Wave 3; their file scopes are disjoint and they can proceed in parallel after Features 01 and 02 are final.

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Markdown agent/skill corpus plus Python 3.12.6 standard-library tooling; target contract is Unity 6, with reference project Unity `6000.3.13f1` |
| Test Runner | `uv run pytest tests/` using pytest 9.1.1 |
| Test Baseline | 141 passed, 2 failed, 143 collected — captured 2026-08-10; both failures are unrelated and named in Discovery Delta |
| Lint | Not configured |
| Format | Not configured |

## Relevant Learnings

None applicable. No `docs/learnings/*.md` files exist. For this feature's content guards, apply the loaded `guard-integrity` rules: scope assertions to the owning section, normalize irrelevant whitespace, assert non-vacuity, derive enumerations where applicable, and prove semantic deletion/negation mutations fail for the intended reason.
