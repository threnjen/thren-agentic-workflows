# Implementation Record: Unity Consumer Alignment

## Summary

Aligned all three Unity consumers to the finalized canonical contracts without copying the worktree or editor-discovery algorithms. Phase Execute now owns Unity execution through the canonical ladder and keeps `not-executed` non-green. Visual Verifier preserves its machine-local editor discovery while targeting root or nested shadow projects with graphics-on PlayMode commands and absolute main-checkout evidence. Unity Reviewer now separates canonical test execution from conditional serialized-asset import. Added 25 focused structural and semantic-mutation guards.

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
- `04-unity-test-reference-assets` is executing concurrently in disjoint files. Its currently failing runbook guards are reported as sibling-in-progress evidence, not Feature 03 regressions.

## AC Coverage Matrix

| AC | Criterion ID | Planned Test ID | Planned Test Pattern | Status | Implementing Files | Evidence Paths | Implement Commit SHA | Review Commit SHA |
|----|--------------|-----------------|----------------------|--------|--------------------|----------------|----------------------|-------------------|
| AC1 | Phase Execute canonical execution | `UCA-AC1` | Scoped Step 2.5 guard checks canonical ladder reference, execution project, absolute XML/logs, orchestrator-owned execution, retry, and attestation | Complete | `source_of_truth/agents/04-phase-execute.agent.md`, `tests/test_unity_consumer_contract.py` | `dev/test-results/03-unity-consumer-alignment-focused.xml` | PENDING | PENDING |
| AC2 | Non-green `not-executed` | `UCA-AC2` | Branch guard and semantic mutations preserve three statuses, decline/unattended reasons, and `all-approved: no` | Complete | Same | `dev/test-results/03-unity-consumer-alignment-focused.xml` | PENDING | PENDING |
| AC3 | Visual Verifier PlayMode execution | `UCA-AC3` | Scoped Step 1 guard checks discovery order, saved path, committed inputs, root/nested execution target, graphics-on flags, and absolute artifacts | Complete | `source_of_truth/agents/04g-unity-visual-verification.agent.md`, `tests/test_unity_consumer_contract.py` | `dev/test-results/03-unity-consumer-alignment-focused.xml` | PENDING | PENDING |
| AC4 | Reviewer test/import distinction | `UCA-AC4` | Scoped Phase 2 guard distinguishes no-quit tests from canonical import-only quit and preserves evidence limits | Complete | `source_of_truth/agents/04h-unity-reviewer.agent.md`, `tests/test_unity_consumer_contract.py` | `dev/test-results/03-unity-consumer-alignment-focused.xml` | PENDING | PENDING |
| AC5 | Canonical single-source mechanics | `UCA-AC5` | All-consumer sweep rejects copied worktree mechanics and duplicate editor discovery outside Visual Verifier | Complete | All three agents, focused guard | `dev/test-results/03-unity-consumer-alignment-focused.xml` | PENDING | PENDING |
| AC6 | Non-vacuous consumer guards | `UCA-AC6` | Derived three-path roster plus deletion/negation/injection mutations for each role-specific obligation | Complete | `tests/test_unity_consumer_contract.py` | `dev/test-results/03-unity-consumer-alignment-focused.xml` | PENDING | PENDING |

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | Phase Execute consumes the canonical ladder and never hands Unity execution to the user | Complete | Phase Execute, focused guards | Absolute main-checkout XML/logs and `<execution-unity-project>` are explicit; direct-supervisor attestation and one retry remain. |
| AC2 | `not-executed` remains non-green and honestly bounded | Complete | Phase Execute, focused guards | Decline, unattended exact status, genuine absence, supervisor-directed skip, and `all-approved: no` remain distinct from green. |
| AC3 | Visual Verifier retains discovery and runs graphics-enabled PlayMode correctly | Complete | Visual Verifier, focused guards | Saved editor path is separate from root/nested execution target; command has `-batchmode`, no `-nographics`, no `-quit`, and absolute XML/logs. Dirty capture inputs block for an orchestrator commit before shadow execution. |
| AC4 | Unity Reviewer follows canonical test and import contracts | Complete | Unity Reviewer, focused guards | Test execution never pairs `-quit` with `-runTests`; `-quit` is permitted only for conditional canonical asset import; clean-import evidence remains bounded. |
| AC5 | Shared mechanics remain single-source | Complete | All three agents, focused guards | Consumers reference the skill; only Visual Verifier retains its verified discovery algorithm; none copies worktree commands. |
| AC6 | Guards derive all consumers and fail under targeted mutations | Complete | Focused guards | Initial red was 12 failed/4 passed. Final focused run is 25 passed, including per-role mutations and duplication injections. |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `source_of_truth/agents/04-phase-execute.agent.md` | Modify | Replaced Unity user-run handoff with canonical ladder ownership, absolute artifact paths, and bounded non-green fallbacks | AC1–AC2, AC5 |
| `source_of_truth/agents/04g-unity-visual-verification.agent.md` | Modify | Preserved editor discovery while adding canonical root/nested project targeting, commit precondition, graphics-on PlayMode command, and absolute XML/logs | AC3, AC5 |
| `source_of_truth/agents/04h-unity-reviewer.agent.md` | Modify | Delegated tests and serialized-asset import to their distinct canonical sections and bounded batchmode/import evidence | AC4–AC5 |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| `tests/test_unity_consumer_contract.py` | Create | Added scoped parsers, three-consumer derivation, role-specific contract checks, duplication checks, and semantic mutation/injection proof | AC1–AC6 |

## Test Results

- **Execution**: executed-failing
- **Command**: `uv run pytest tests/test_unity_consumer_contract.py -q --junitxml=dev/test-results/03-unity-consumer-alignment-focused.xml`; `uv run pytest tests/test_agent_corpus_invariants.py -q --junitxml=dev/test-results/03-unity-consumer-alignment-corpus.xml`; `uv run pytest tests/test_propagate_master_assets.py -k 'not test_committed_tree_is_at_a_propagation_fixed_point' -q --junitxml=dev/test-results/03-unity-consumer-alignment-propagation.xml`; `uv run pytest tests/test_unity_consumer_contract.py tests/test_unity_skill_contract.py tests/test_agent_corpus_invariants.py tests/test_propagate_master_assets.py -k 'not test_committed_tree_is_at_a_propagation_fixed_point' -q --junitxml=dev/test-results/03-unity-consumer-alignment-regression.xml`; `uv run pytest tests/ -k 'not test_committed_tree_is_at_a_propagation_fixed_point' -q --junitxml=dev/test-results/03-unity-consumer-alignment-full-no-fixedpoint.xml`
- **Results artifact**: `dev/test-results/03-unity-consumer-alignment-focused.xml`; `dev/test-results/03-unity-consumer-alignment-corpus.xml`; `dev/test-results/03-unity-consumer-alignment-propagation.xml`; `dev/test-results/03-unity-consumer-alignment-regression.xml`; `dev/test-results/03-unity-consumer-alignment-full-no-fixedpoint.xml`
- **Baseline**: historical phase baseline 141 passed, 2 failed; focused red 4 passed, 12 failed
- **Final**: focused 25 passed, 0 failed; corpus invariants 7 passed, 0 failed; propagation suite 43 passed, 1 failed, 35 subtests passed; relevant regression 120 passed, 1 failed, 35 subtests passed; safe full 223 passed, 4 failed, 1 deselected, 63 subtests passed
- **New tests added**: 25 collected focused cases
- **Affected suites run**: Feature 03 consumer guards; upstream Unity skill guards; agent corpus invariants; propagation tests; safe full repository suite
- **Regressions**: Unknown — the Feature 03 focused and relevant suites introduce no unexplained failure, but the repository-wide run is failing. Two failures are the recorded baseline PR-review display-name collision and wildcard `applyTo` target defect. Two additional failures belong to the concurrently incomplete Feature 04 local-runbook guards (`test_local_runbook_contract` and its prune mutation); they are outside this feature's ownership.

## Deviations from Plan

- Selected the proposed focused filename `tests/test_unity_consumer_contract.py`; no test class was needed because the repository uses module-level pytest functions.
- The generated-output-writing fixed-point test lives in `tests/test_retirement_reconciliation.py` and was excluded from the full run. Propagation was not run.
- The full repository run observed concurrent Feature 04 work. Its failures were left untouched and attributed explicitly.

## Gaps

- Maintainer propagation is pending. No generated port or `.github/` file was edited.
- Full-suite green evidence depends on Feature 04 completing its concurrently authored runbook and guards, plus resolution or accepted carry-forward of the two pre-existing repository failures.
- Unity runtime execution was intentionally not performed; Features 01 and 02 own empirical Unity command evidence.
- Phase-document reconciliation is pending because the caller prohibited phase-document edits.

## Reviewer Focus Areas

- Phase Execute Step 2.5: confirm Unity `not-executed` cannot become green except through the preserved direct-supervisor attestation exception.
- Visual Verifier Step 1: confirm the discovery procedure remains authoritative and the long-form command keeps PlayMode graphics enabled with absolute main-checkout XML/logs.
- Visual Verifier dirty-input branch: confirm returning for an orchestrator commit is coherent with the shadow worktree's committed-code precondition.
- Unity Reviewer Phase 2: confirm batchmode remains restricted to tests and conditional serialized-asset import, and import does not overclaim runtime/reference evidence.
