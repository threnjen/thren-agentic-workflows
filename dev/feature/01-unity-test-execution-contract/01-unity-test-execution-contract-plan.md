# Feature Plan: Unity Test Execution Contract

## Execution Metadata

- **Wave:** 1
- **Parallel safe:** yes
- **Depends on:** none
- **Key files modified:** `source_of_truth/skills/unity-development/SKILL.md`, `tests/[PROPOSED - name TBD: Unity skill contract guards]`
- **Sequential reason:** n/a

## A. Requirements & Traceability

### Acceptance Criteria

1. **AC1:** The `## Test Execution` section makes `-batchmode` mandatory for every agent-driven Unity test run and removes the current statement that it is optional everywhere under `source_of_truth/`.
2. **AC2:** The section contains a two-row platform table: EditMode uses `-batchmode -nographics`; PlayMode and visual-capture use `-batchmode` with graphics enabled and explicitly exclude `-nographics`.
3. **AC3:** The section preserves the rule that `-quit` must not be paired with `-runTests`, and preserves the existing affected-suite `-testFilter` semantics unchanged.
4. **AC4:** Test commands use the editor path resolved by the existing discovery procedure in `source_of_truth/agents/04g-unity-visual-verification.agent.md`; the skill does not introduce a second discovery implementation or assume bare `Unity` is on `PATH`.
5. **AC5:** `-testResults` always receives an absolute path under the main checkout's `dev/test-results/`; the shadow worktree remains execution-only and results are never read from its copy.
6. **AC6:** The skill states commit-before-test as a precondition for shadow-worktree execution and explains that the normal per-feature commit usually satisfies it.
7. **AC7:** The first ladder rung prunes stale registrations, creates or reuses one detached persistent sibling worktree at `<project-dir>-agent-tests/`, refreshes it to the committed SHA, retains its gitignored `Library/`, announces its path, approximate disk cost, and multi-minute first import, then runs headless there while the main Editor remains usable.
8. **AC8:** The procedure makes persistence indefinite, names per-run worktree creation as an anti-pattern, and supplies a manual teardown command without automating teardown.
9. **AC9:** The second ladder rung handles a licensing or lock failure by asking the user to close the Editor and then running headless in the main checkout; it never delegates the test run to the user.
10. **AC10:** The third ladder rung forbids a GUI and silent refusal. A decline reports `not-executed`; an unattended non-response is treated as a decline and reports exactly `not-executed: editor open, user unavailable`.
11. **AC11:** The documented worktree EditMode invocation is executed against `/Users/jennywadkins/github_repos/the-movies` with its main Editor open, and evidence records whether Unity Personal permits the concurrent process, whether any GUI appeared, whether the Editor remained usable, and the absolute results path.
12. **AC12:** Structural guards cover AC1–AC10, normalize irrelevant Markdown whitespace where needed, scope assertions to the `## Test Execution` section, include non-vacuity checks, and are proven red by deleting or negating each protected obligation before being restored green.

### Non-Goals

- Do not change Unity test assertions, Test Authenticity Rules, or `-testFilter` behavior.
- Do not change serialized-asset or EditMode-path guidance; `02-headless-asset-import` owns those sections.
- Do not edit consumer agent definitions; `03-unity-consumer-alignment` owns them.
- Do not create, remove, or alter any worktree in this repository during implementation; the reference-project worktree is a manual QA asset.
- Do not run propagation or edit `ports/` or `.github/`.

### Traceability

| Acceptance Criteria | Code Areas/Modules | Test / Evidence Category |
|---|---|---|
| AC1–AC5 | `source_of_truth/skills/unity-development/SKILL.md` — `## Test Execution` | Must-have automated test |
| AC6–AC10 | `source_of_truth/skills/unity-development/SKILL.md` — execution ladder and worktree procedure | Must-have automated test |
| AC11 | `/Users/jennywadkins/github_repos/the-movies` and main-checkout `dev/test-results/` | Manual QA check |
| AC12 | `tests/[PROPOSED - name TBD: Unity skill contract guards]` | Must-have automated test |

## B. Correctness & Edge Cases

- A dirty main checkout cannot be represented by a detached worktree checkout. Fail fast with the commit-before-test precondition.
- A fixed sibling path may exist but not be a registered worktree, or may point at the wrong project. Verify ownership before reuse; do not overwrite foreign content.
- Run `git worktree prune` before deciding whether the fixed path is reusable, but do not delete the persistent test worktree.
- A concurrent Unity Personal license failure is an expected ladder transition, not proof the test failed.
- Rung 2 must distinguish a user decline from silence. Silence in unattended execution terminates as the exact unavailable status instead of waiting indefinitely.
- Exit code zero is insufficient. The existing results-XML rule remains authoritative, and zero discovered tests remains `not-executed`.
- EditMode and PlayMode flags must remain distinct. A shared blanket `-nographics` rule would break rendering.
- Error handling is bounded and fail-fast: try rung 1 once, request rung 2 once, then report the correct `not-executed` state without opening a GUI.

## C. Consistency & Architecture Fit

- Follow the dense, terse machine-facing style already used in `unity-development/SKILL.md`.
- Reuse the verified editor-discovery procedure in `source_of_truth/agents/04g-unity-visual-verification.agent.md`; this feature adds a pointer, not a duplicate API.
- Preserve the verified results parser contract at the end of `## Test Execution`.
- Keep all commands expressed as procedures and placeholders copied from Phase 01. Do not introduce a helper script or new runtime dependency.
- Relationship: `02-headless-asset-import` depends on this feature because it edits the same skill file after this section is stable. `03-unity-consumer-alignment` and `04-unity-test-reference-assets` consume this feature's finalized execution contract.

### Unverified Assumptions

- Unity Personal on the maintainer's machine may reject a second concurrent process. AC11 determines whether rung 1 is the normal path or an attempted optimization that falls back to rung 2.
- The exact Unity editor executable must be resolved by the existing discovery procedure during manual QA; it is not assumed from `PATH`.

## D. Clean Design & Maintainability

- Keep the ladder in one section and in one order; do not scatter fallback behavior across unrelated headings.
- Keep the platform flags in the required two-row table so PlayMode graphics cannot be flattened into the EditMode command.
- Prefer one canonical worktree procedure over command variants.
- Avoid a helper script, new config format, or automatic teardown mechanism.
- Keep guards structural: section boundaries, table rows, command-token relationships, forbidden-state sweeps, and non-vacuity assertions.

### Keep It Clean Checklist

- [ ] No repeated explanation of why headless execution matters.
- [ ] No new editor-discovery algorithm.
- [ ] No bare `Unity` executable assumption.
- [ ] No GUI fallback.
- [ ] No generated-output edits.

## E. Completeness: Observability, Security, Operability

- **Observability decision:** Add no normal-path logs to the corpus. Require existing Unity log output plus the absolute results XML as evidence, and require the agent to announce first creation, path, disk cost, cold-start time, and ladder transition reason.
- **Security:** Quote resolved paths safely in documented commands. Never persist license material or machine-specific editor paths in tracked files.
- **Runbook:** Verify with the focused structural guard module, then perform AC11 manually. Roll back by reverting only the skill and its new guard module. Monitor results XML and Unity log output; an exit code alone is not evidence.
- **Baseline:** The full discovery run produced 141 passes and two unrelated existing failures: `tests/test_pr_review_orchestrator.py::test_agent_name_does_not_collide_with_prose_in_any_source_asset` and `tests/test_propagate_master_assets.py::InstructionApplyToTests::test_every_enumerated_applyto_target_exists`. Do not absorb either failure into this feature.

## F. Test Plan

| Acceptance Criteria | Evidence | Category |
|---|---|---|
| AC1–AC3 | Parse the Test Execution section and verify command/table relationships plus prohibited combinations without pinning arbitrary prose | Must-have automated test |
| AC4–AC5 | Verify the section points to the existing discovery source and constrains results to an absolute main-checkout path | Must-have automated test |
| AC6–AC10 | Verify all ladder states and worktree invariants occur in order and forbidden GUI/refusal states are absent | Must-have automated test |
| AC11 | Run the real reference-project scenario and record artifacts and license outcome | Manual QA check |
| AC12 | Perform deletion and negation mutations for every guard obligation | Must-have automated test |

### Top Five High-Value Checks

1. Given the Test Execution section, when its platform table is parsed, then EditMode contains `-batchmode` and `-nographics` while PlayMode/visual contains `-batchmode` and excludes `-nographics`.
2. Given the execution ladder, when its ordered rungs are inspected, then worktree execution precedes close-the-Editor fallback, and only decline or unattended silence reaches `not-executed`.
3. Given a mutation that changes mandatory `-batchmode` back to optional or permits a GUI, when the focused guard runs, then it fails with the violated obligation named.
4. Given the reference project with the main Editor open, when the detached persistent worktree run executes, then no GUI appears and the result records either executed evidence or the licensing transition to rung 2.
5. Given a zero-test or missing-results run, when evidence is evaluated, then it remains `not-executed` despite exit code zero.

### Fixtures and Test Impact

- Create `tests/[PROPOSED - name TBD: Unity skill contract guards]`; do not add prose assertions to `tests/test_agent_corpus_invariants.py`, whose contract explicitly excludes them.
- Use small parser fixtures derived from the live section boundaries. Add non-vacuity checks so missing headings or rows cannot yield a false pass.
- No existing Unity tests are modified; the external reference project is manual QA only.
- Run `uv run pytest tests/[PROPOSED - name TBD: Unity skill contract guards]` and the existing corpus/propagation suites. Propagation-backed sync checks may remain red until the maintainer propagates.

## Stage 1: Contract Guards
**Goal**: Add failing structural guards for the mandatory flags, ladder, result path, worktree lifecycle, and forbidden states.
**Success Criteria**: Each AC1–AC10 obligation has a scoped guard, and deletion/negation proves each guard turns red for the intended reason.
**Status**: Not Started

## Stage 2: Test Execution Rule Rewrite
**Goal**: Rewrite `## Test Execution` to satisfy the complete headless execution contract without duplicating editor discovery.
**Success Criteria**: AC1–AC10 guards pass; `-testFilter` and results-XML semantics remain unchanged.
**Status**: Not Started

## Stage 3: Reference-Project Verification
**Goal**: Exercise the shadow-worktree EditMode path against Unity 6000.3.13f1 and record the license/fallback outcome.
**Success Criteria**: AC11 evidence exists at the absolute main-checkout results path and records GUI, Editor usability, results, and licensing behavior honestly.
**Status**: Not Started

## Stage 4: Regression Verification
**Goal**: Run focused and repository regression checks without propagating generated outputs.
**Success Criteria**: New guards pass, unrelated baseline failures are distinguished, and any sync-only failure is reported as propagation pending.
**Status**: Not Started
