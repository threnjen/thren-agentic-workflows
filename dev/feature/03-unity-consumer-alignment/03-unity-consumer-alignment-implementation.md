# Implementation Record: Unity Consumer Alignment

## Summary

Aligned all three Unity consumers to the finalized canonical contracts without copying the worktree or editor-discovery algorithms. Phase Execute now owns Unity execution through the canonical ladder, commits visual-capture inputs at the feature checkpoint, and keeps missing evidence non-green. Visual Verifier preserves its machine-local editor discovery while resolving the Unity version from the selected root or nested execution project and running graphics-on PlayMode commands with absolute main-checkout evidence. Unity Reviewer separates canonical test execution from conditional serialized-asset import. Added 30 focused structural and semantic-mutation guards.

### Preflight

- Repository: Python 3.12 structural tests over Markdown agent definitions; this checkout is not itself a Unity project.
- Canonical prerequisites: Features 01 and 02 are present in `source_of_truth/skills/unity-development/SKILL.md`; Test Execution defines resolved editor discovery, root/nested execution paths, absolute XML/log artifacts, and the three-rung ladder. Serialized Assets defines conditional headless asset import.
- Owned consumers and headings verified: Phase Execute `### Step 2.5: Wave Test Gate`, Visual Verifier Steps 1–2, Unity Reviewer `### Phase 2: Compilation Check`.
- Frontmatter, tools, agent rosters, display names, and personality content were preserved.
- Unity runtime execution: not required by this feature. No Unity process or external project was used or mutated.
- Concurrent sibling: Feature 04 owns reference assets, its test module, and its feature folder. Those files were not edited here.

## Sibling Features

- `01-unity-test-execution-contract` supplies the finalized Test Execution contract consumed here.
- `02-headless-asset-import` supplies the finalized Serialized Assets contract consumed here.
- `04-unity-test-reference-assets` executed concurrently in disjoint files. Its assets and guards were not modified by Feature 03; its focused fixes are green in the final safe full run.

## AC Coverage Matrix

| AC | Criterion ID | Planned Test ID | Planned Test Pattern | Status | Implementing Files | Evidence Paths | Implement Commit SHA | Review Commit SHA |
|----|--------------|-----------------|----------------------|--------|--------------------|----------------|----------------------|-------------------|
| AC1 | Phase Execute canonical execution | `UCA-AC1` | Scoped Step 2.5 guard checks canonical ladder reference, execution project, absolute XML/logs, orchestrator-owned execution, retry, and attestation | Complete | `source_of_truth/agents/04-phase-execute.agent.md`, `tests/test_unity_consumer_contract.py` | `dev/test-results/03-unity-consumer-alignment-focused.xml` | PENDING | PENDING |
| AC2 | Non-green `not-executed` | `UCA-AC2` | Branch guard and semantic mutations preserve three statuses, decline/unattended reasons, and `all-approved: no` | Complete | Same | `dev/test-results/03-unity-consumer-alignment-focused.xml` | PENDING | PENDING |
| AC3 | Visual Verifier PlayMode execution | `UCA-AC3` | Scoped Step 1 guard checks discovery order, saved path, Unity-version path bound to the root/nested execution target, graphics-on flags, and absolute artifacts | Complete | `source_of_truth/agents/04g-unity-visual-verification.agent.md`, `tests/test_unity_consumer_contract.py` | `dev/test-results/03-unity-consumer-alignment-review-focused.xml` | PENDING | PENDING |
| AC4 | Reviewer test/import distinction | `UCA-AC4` | Scoped Phase 2 guard distinguishes no-quit tests from canonical import-only quit and preserves evidence limits | Complete | `source_of_truth/agents/04h-unity-reviewer.agent.md`, `tests/test_unity_consumer_contract.py` | `dev/test-results/03-unity-consumer-alignment-focused.xml` | PENDING | PENDING |
| AC5 | Canonical single-source mechanics | `UCA-AC5` | All-consumer sweep rejects copied worktree mechanics and duplicate editor discovery outside Visual Verifier | Complete | All three agents, focused guard | `dev/test-results/03-unity-consumer-alignment-focused.xml` | PENDING | PENDING |
| AC6 | Non-vacuous consumer guards | `UCA-AC6` | Derived three-path roster plus deletion/negation/injection mutations for each role-specific obligation and the post-wave commit lifecycle | Complete | `tests/test_unity_consumer_contract.py` | `dev/test-results/03-unity-consumer-alignment-review-focused.xml` | PENDING | PENDING |

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | Phase Execute consumes the canonical ladder and never hands Unity execution to the user | Complete | Phase Execute, focused guards | Absolute main-checkout XML/logs and `<execution-unity-project>` are explicit; direct-supervisor attestation and one retry remain. |
| AC2 | `not-executed` remains non-green and honestly bounded | Complete | Phase Execute, focused guards | Decline, unattended exact status, genuine absence, supervisor-directed skip, and `all-approved: no` remain distinct from green. |
| AC3 | Visual Verifier retains discovery and runs graphics-enabled PlayMode correctly | Complete | Visual Verifier, focused guards | Saved editor path is separate from the execution target; version discovery uses `<execution-unity-project>/ProjectSettings/ProjectVersion.txt`; command has `-batchmode`, no `-nographics`, no `-quit`, and absolute XML/logs. |
| AC4 | Unity Reviewer follows canonical test and import contracts | Complete | Unity Reviewer, focused guards | Test execution never pairs `-quit` with `-runTests`; `-quit` is permitted only for conditional canonical asset import; clean-import evidence remains bounded. |
| AC5 | Shared mechanics remain single-source | Complete | All three agents, focused guards | Consumers reference the skill; only Visual Verifier retains its verified discovery algorithm; none copies worktree commands. |
| AC6 | Guards derive all consumers and fail under targeted mutations | Complete | Focused guards | Initial red was 12 failed/4 passed; review red was 6 failed/24 passed. Final focused run is 30 passed, including nested-path and visual-bootstrap lifecycle mutations. |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `source_of_truth/agents/04-phase-execute.agent.md` | Modify | Replaced Unity user-run handoff with canonical ladder ownership and bounded non-green fallbacks; moved visual wiring before A1 and made missing post-wave inputs an explicit non-green blocker | AC1–AC3, AC5 |
| `source_of_truth/agents/04g-unity-visual-verification.agent.md` | Modify | Preserved editor discovery while binding the Unity-version file and command to the root/nested execution project, commit precondition, graphics-on PlayMode command, and absolute XML/logs | AC3, AC5 |
| `source_of_truth/agents/04h-unity-reviewer.agent.md` | Modify | Delegated tests and serialized-asset import to their distinct canonical sections and bounded batchmode/import evidence | AC4–AC5 |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| `tests/test_unity_consumer_contract.py` | Create | Added scoped parsers, three-consumer derivation, role-specific contract checks, duplication checks, nested version-path relation, commit-lifecycle guard, and semantic mutation/injection proof | AC1–AC6 |

## Test Results

- **Execution**: executed-failing
- **Command**: `uv run pytest tests/test_unity_consumer_contract.py -q --junitxml=dev/test-results/03-unity-consumer-alignment-review-focused.xml`; `uv run pytest tests/test_unity_consumer_contract.py tests/test_unity_skill_contract.py tests/test_agent_corpus_invariants.py tests/test_propagate_master_assets.py -k 'not test_committed_tree_is_at_a_propagation_fixed_point' -q --junitxml=dev/test-results/03-unity-consumer-alignment-review-regression.xml`; `uv run pytest tests/ -k 'not test_committed_tree_is_at_a_propagation_fixed_point' -q --junitxml=dev/test-results/03-unity-consumer-alignment-review-full-no-fixedpoint.xml`
- **Results artifact**: `dev/test-results/03-unity-consumer-alignment-review-focused.xml`; `dev/test-results/03-unity-consumer-alignment-review-regression.xml`; `dev/test-results/03-unity-consumer-alignment-review-full-no-fixedpoint.xml`
- **Baseline**: historical phase baseline 141 passed, 2 failed; focused red 4 passed, 12 failed
- **Final**: focused 30 passed, 0 failed; relevant regression 125 passed, 1 failed, 35 subtests passed; safe full 235 passed, 2 failed, 1 deselected, 63 subtests passed
- **New tests added**: 30 collected focused cases
- **Affected suites run**: Feature 03 consumer guards; upstream Unity skill guards; agent corpus invariants; propagation tests; safe full repository suite
- **Regressions**: No Feature 03 regression observed. The repository-wide run remains executed-failing only at the two recorded baseline defects: the PR-review display-name collision and wildcard `applyTo` target guard.

## Deviations from Plan

- Selected the proposed focused filename `tests/test_unity_consumer_contract.py`; no test class was needed because the repository uses module-level pytest functions.
- The generated-output-writing fixed-point test lives in `tests/test_retirement_reconciliation.py` and was excluded from the full run. Propagation was not run.
- The first full repository run observed concurrent Feature 04 work; the final safe full rerun occurred after its disjoint fixes and returned to the two-failure baseline.

## Gaps

- Maintainer propagation is pending. No generated port or `.github/` file was edited.
- Full-suite green evidence still depends on resolution or accepted carry-forward of the two pre-existing repository failures.
- Unity runtime execution was intentionally not performed; Features 01 and 02 own empirical Unity command evidence.
- Phase-document reconciliation is pending because the caller prohibited phase-document edits.

## Reviewer Focus Areas

- Phase Execute Step 2.5: confirm Unity `not-executed` cannot become green except through the preserved direct-supervisor attestation exception.
- Visual Verifier Step 1: confirm the discovery procedure remains authoritative and the long-form command keeps PlayMode graphics enabled with absolute main-checkout XML/logs.
- Phase Execute visual gate: confirm Visual Verification Wiring is owned before A1 and missing post-wave inputs remain non-green without dirty mutation.
- Unity Reviewer Phase 2: confirm batchmode remains restricted to tests and conditional serialized-asset import, and import does not overclaim runtime/reference evidence.
