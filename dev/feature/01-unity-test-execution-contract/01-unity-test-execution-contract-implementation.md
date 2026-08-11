# Implementation Record: Unity Test Execution Contract

## Summary

Implemented the canonical headless Unity test-execution contract in `unity-development`: mandatory platform-specific batch flags, editor discovery reuse, absolute main-checkout results, commit-before-test, a persistent detached sibling worktree, a bounded three-rung fallback, manual-only teardown, and preserved `-testFilter`/XML evidence semantics. Added 22 focused structural and mutation-test cases. The external EditMode command produced authoritative failing XML; concurrency/usability remains unverified because the main Editor was not open.

## Preflight

- Repository under implementation: Markdown agent/skill corpus with Python structural tests; it is not itself a Unity project.
- Reference project: `/Users/jennywadkins/github_repos/the-movies`, clean at commit `2af127e4d8cd1f551344886b9686eb391ea4565a`, Unity `6000.3.13f1`.
- Editor discovery: resolved `/Applications/Unity/Hub/Editor/6000.3.13f1/Unity.app/Contents/MacOS/Unity` from the project version plus Unity Hub default layout.
- Unity project preflight fields (`activeInputHandler`, `.asmdef` references, MonoBehaviour wiring, render pipeline): N/A; this feature changes no Unity C# code, assemblies, scenes, assets, or runtime renderers.
- Main Editor state: not running and no `Temp/UnityLockfile`; therefore AC11's concurrent-process and Editor-usability observations remain unverified.
- Persistent worktree: created detached at `/Users/jennywadkins/github_repos/the-movies-agent-tests/`, refreshed to `2af127e4`, retained after the run, current disk use 276 MB.

## Sibling Features

- `02-headless-asset-import` runs next and shares `source_of_truth/skills/unity-development/SKILL.md` plus `tests/test_unity_skill_contract.py`; it must preserve this section and extend the selected guard module.
- `03-unity-consumer-alignment` consumes the finalized Test Execution contract when updating the three Unity-facing agents.
- `04-unity-test-reference-assets` consumes the same contract for its runbook and inert workflow assets.
- No sibling files were modified.

## AC Coverage Matrix

| AC | Criterion ID | Planned Test ID | Planned Test Pattern | Status | Implementing Files | Evidence Paths | Implement Commit SHA | Review Commit SHA |
|----|--------------|-----------------|----------------------|--------|--------------------|----------------|----------------------|-------------------|
| AC1 | Mandatory batchmode | `UTEC-AC1` | Live contract plus source-wide non-vacuous optional-claim sweep | Complete | `source_of_truth/skills/unity-development/SKILL.md`, `tests/test_unity_skill_contract.py` | `dev/test-results/01-unity-test-execution-contract-focused.xml` | PENDING | PENDING |
| AC2 | Platform flag table | `UTEC-AC2` | Parse two rows and inspect EditMode/PlayMode command tokens | Complete | Same | `dev/test-results/01-unity-test-execution-contract-focused.xml` | PENDING | PENDING |
| AC3 | No quit; preserved filtering | `UTEC-AC3` | Scoped command relationships and preserved semantic fragments | Complete | Same | `dev/test-results/01-unity-test-execution-contract-focused.xml` | PENDING | PENDING |
| AC4 | Existing editor discovery | `UTEC-AC4` | Require canonical agent pointer and reject bare `Unity` command | Complete | Same | `dev/test-results/01-unity-test-execution-contract-focused.xml` | PENDING | PENDING |
| AC5 | Absolute main results | `UTEC-AC5` | Require absolute-main placeholder, execution-only worktree, and no shadow read | Complete | Same | `dev/test-results/01-unity-test-execution-contract-focused.xml` | PENDING | PENDING |
| AC6 | Commit-before-test | `UTEC-AC6` | Require hard precondition and normal per-feature commit explanation | Complete | Same | `dev/test-results/01-unity-test-execution-contract-focused.xml` | PENDING | PENDING |
| AC7 | Persistent worktree rung | `UTEC-AC7` | Ordered ladder/token validation plus external detached worktree run | Complete | Same | `/Users/jennywadkins/github_repos/the-movies/dev/test-results/01-unity-test-execution-contract-editmode.xml` | PENDING | PENDING |
| AC8 | Persistence and teardown | `UTEC-AC8` | Lifecycle tokens and deletion/negation mutation cases | Complete | Same | `dev/test-results/01-unity-test-execution-contract-focused.xml` | PENDING | PENDING |
| AC9 | Agent-run fallback | `UTEC-AC9` | Require close-Editor request and forbid delegating execution | Complete | Same | `dev/test-results/01-unity-test-execution-contract-focused.xml` | PENDING | PENDING |
| AC10 | Terminal behavior | `UTEC-AC10` | Ordered terminal rung, exact unattended status, GUI/refusal negation | Complete | Same | `dev/test-results/01-unity-test-execution-contract-focused.xml` | PENDING | PENDING |
| AC11 | Reference-project execution | `UTEC-AC11-MANUAL` | Real Unity EditMode command and XML/log inspection | Partial — blocked | External QA only | `/Users/jennywadkins/github_repos/the-movies/dev/test-results/01-unity-test-execution-contract-editmode.xml`, `/Users/jennywadkins/github_repos/the-movies/dev/test-results/01-unity-test-execution-contract-editmode.log` | PENDING | PENDING |
| AC12 | Structural/mutation guards | `UTEC-AC12` | Scoped parser, non-vacuity, 19 semantic mutation cases, focused/full pytest | Complete | `tests/test_unity_skill_contract.py` | `dev/test-results/01-unity-test-execution-contract-focused.xml`, `dev/test-results/01-unity-test-execution-contract-pytest.xml` | PENDING | PENDING |

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | Mandatory `-batchmode`; obsolete optional claim removed | Complete | Skill, focused guards | Source-wide text sweep is non-empty and green. |
| AC2 | Two-row EditMode versus PlayMode/visual flags | Complete | Skill, focused guards | Two command examples also prove token separation. |
| AC3 | No `-quit` with tests; filtering unchanged | Complete | Skill, focused guards | Existing filter sentence retained; XML parser preserved and strengthened with exit-code warning. |
| AC4 | Reuse editor discovery; no bare executable | Complete | Skill, focused guards | External run resolved the exact versioned Hub executable. |
| AC5 | Absolute main-checkout results path | Complete | Skill, focused guards | External XML landed under the reference main checkout, not the worktree. |
| AC6 | Commit-before-test precondition | Complete | Skill, focused guards | Reference worktree tested committed SHA `2af127e4`. |
| AC7 | Persistent detached worktree procedure | Complete | Skill, focused guards | Worktree created once, refreshed detached, retained; first run completed in 465.8 seconds. |
| AC8 | Indefinite persistence and manual teardown | Complete | Skill, focused guards | No teardown was run. |
| AC9 | Licensing/lock fallback remains agent-run | Complete | Skill, focused guards | Licensing succeeded in this non-concurrent run, so rung 2 was not reached. |
| AC10 | No GUI/silent refusal; exact unattended status | Complete | Skill, focused guards | Semantic negations fail with named obligations. |
| AC11 | Run with main Editor open and record concurrency/usability | Partial — blocked | External QA only | Unity ran headless and produced XML, licensing succeeded, and no GUI process was observed. The main Editor was not open, so concurrent Unity Personal behavior and Editor usability were not tested. XML: 4,978 total, 4,954 passed, 17 failed, 7 skipped. |
| AC12 | Structural guards with deletion/negation proof | Complete | Focused guards | 22 cases pass, including 19 mutation cases; initial red run was 21 failed/1 passed against the old section. |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `source_of_truth/skills/unity-development/SKILL.md` | Modify | Replaced `## Test Execution` with the complete mandatory headless execution contract and ladder | Implements AC1–AC10 while keeping the canonical rule in one source-only section |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| `tests/test_unity_skill_contract.py` | Create | Added section extraction, whitespace normalization, source sweep, command checks, contract validator, and 19 mutation cases | AC1–AC10, AC12; shared extension surface for Feature 02 |

## Test Results

- **Execution**: executed-failing
- **Command**: `uv run pytest tests/test_unity_skill_contract.py --junitxml=dev/test-results/01-unity-test-execution-contract-focused.xml`; `uv run pytest tests/ --junitxml=dev/test-results/01-unity-test-execution-contract-pytest.xml`; `/Applications/Unity/Hub/Editor/6000.3.13f1/Unity.app/Contents/MacOS/Unity -batchmode -nographics -runTests -projectPath /Users/jennywadkins/github_repos/the-movies-agent-tests -testPlatform EditMode -testResults /Users/jennywadkins/github_repos/the-movies/dev/test-results/01-unity-test-execution-contract-editmode.xml -logFile /Users/jennywadkins/github_repos/the-movies/dev/test-results/01-unity-test-execution-contract-editmode.log`
- **Results artifact**: `dev/test-results/01-unity-test-execution-contract-focused.xml`; `dev/test-results/01-unity-test-execution-contract-pytest.xml`; `/Users/jennywadkins/github_repos/the-movies/dev/test-results/01-unity-test-execution-contract-editmode.xml`
- **Baseline**: 141 passed, 2 failed, 143 total (before implementation)
- **Final**: repository 162 passed, 3 failed, 165 total; focused guards 22 passed, 0 failed; reference Unity EditMode 4,954 passed, 17 failed, 4,978 total, 7 skipped
- **New tests added**: 22 collected cases
- **Affected suites run**: focused Unity skill guards; full repository pytest suite; external reference-project Unity EditMode suite
- **Regressions**: Unknown — the repository suite remains executed-failing: its two baseline failures remain, and `test_committed_tree_is_at_a_propagation_fixed_point` is the expected source/generated mismatch while maintainer propagation is pending. The external Unity suite has 17 failures but no pre-change run in this pass, so they cannot be attributed to this Markdown-only feature.

## Deviations from Plan

- Selected `tests/test_unity_skill_contract.py` as the final proposed shared guard filename.
- The reference worktree currently uses 276 MB rather than the phase's approximate 600 MB estimate; the contract requires announcing an estimate, not pinning the observed size.
- Full pytest's fixed-point test wrote generated mirrors while demonstrating pending propagation. Those four generated skill changes were restored; propagation was not invoked. The test also removed eight pre-existing generated-agent diffs observed at baseline, which could not be reconstructed safely and was reported to the orchestrator.
- Added `dev/test-results/` to the external reference project's local `.git/info/exclude` so the required main-checkout artifacts remain available without dirtying its tracked working tree.

## Gaps

- AC11 concurrency is blocked: the reference project's main Editor was not open, so Unity Personal concurrent-process permission and main-Editor usability remain unverified. Repeat only that manual condition with the retained worktree and existing command.
- The external EditMode suite is executed-failing (17 failures). This feature changes no reference-project code or tests; failure diagnosis is outside scope.
- Maintainer propagation is pending. No generated output was authored or committed by this feature.

## Reviewer Focus Areas

- Confirm the Test Execution section is terse enough for an always-loaded machine-facing skill while retaining all three ladder rungs.
- Check the focused validator for accidental prose pinning versus required command/token relationships, especially the repeated `Library/` mutation case.
- Verify `-testFilter` and XML parsing semantics remained unchanged apart from the explicit exit-code warning.
- Treat AC11 as partial until a run occurs while the main Editor is open; do not infer concurrency from the successful non-concurrent license connection.
