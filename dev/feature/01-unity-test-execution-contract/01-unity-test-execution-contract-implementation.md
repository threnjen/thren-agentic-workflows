# Implementation Record: Unity Test Execution Contract

## Summary

Implemented the canonical headless Unity test-execution contract in `unity-development`: mandatory platform-specific batch flags, deployed Visual Verifier discovery reuse, root/nested Unity project resolution, absolute main-checkout XML/log artifacts, commit-before-test, a persistent detached sibling worktree with bounded cleanliness checks, a three-rung fallback, manual-only teardown, and preserved `-testFilter`/XML evidence semantics. Review expanded the focused suite to 32 structural and mutation-test cases. The external EditMode command produced authoritative failing XML with the Editor closed. A retry preflight again found no running main Editor, so the required open-Editor run is `not-executed (main Editor-open condition unavailable)`; Unity Personal concurrency and Editor usability remain unverified.

## Preflight

- Repository under implementation: Markdown agent/skill corpus with Python structural tests; it is not itself a Unity project.
- Reference project: `/Users/jennywadkins/github_repos/the-movies`, clean at commit `2af127e4d8cd1f551344886b9686eb391ea4565a`, Unity `6000.3.13f1`.
- Editor discovery: resolved `/Applications/Unity/Hub/Editor/6000.3.13f1/Unity.app/Contents/MacOS/Unity` from the project version plus Unity Hub default layout.
- Unity project preflight fields (`activeInputHandler`, `.asmdef` references, MonoBehaviour wiring, render pipeline): N/A; this feature changes no Unity C# code, assemblies, scenes, assets, or runtime renderers.
- Main Editor retry state: not running and no `/Users/jennywadkins/github_repos/the-movies/Temp/UnityLockfile` on 2026-08-10. The agent did not launch a GUI. AC7/AC11 retry status is `not-executed (main Editor-open condition unavailable)`.
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
| AC4 | Deployed editor discovery | `UTEC-AC4` | Require loading the deployed Visual Verifier definition, reject authoring-only paths and duplicated discovery, and reject bare `Unity` commands | Complete | Same | `dev/test-results/01-unity-test-execution-contract-review-focused.xml` | PENDING | PENDING |
| AC5 | Absolute main results | `UTEC-AC5` | Require absolute-main placeholder, execution-only worktree, and no shadow read | Complete | Same | `dev/test-results/01-unity-test-execution-contract-focused.xml` | PENDING | PENDING |
| AC6 | Commit-before-test | `UTEC-AC6` | Require hard precondition and normal per-feature commit explanation | Complete | Same | `dev/test-results/01-unity-test-execution-contract-focused.xml` | PENDING | PENDING |
| AC7 | Persistent worktree rung | `UTEC-AC7` | Ordered ladder/token validation plus external detached worktree run while the main Editor remains usable | Partial — `not-executed (main Editor-open condition unavailable)` | Same | Prior closed-Editor evidence only: `/Users/jennywadkins/github_repos/the-movies/dev/test-results/01-unity-test-execution-contract-editmode.xml`; concurrent-run artifact: none | PENDING | PENDING |
| AC8 | Persistence and teardown | `UTEC-AC8` | Lifecycle tokens and deletion/negation mutation cases | Complete | Same | `dev/test-results/01-unity-test-execution-contract-focused.xml` | PENDING | PENDING |
| AC9 | Agent-run fallback | `UTEC-AC9` | Require close-Editor request and forbid delegating execution | Complete | Same | `dev/test-results/01-unity-test-execution-contract-focused.xml` | PENDING | PENDING |
| AC10 | Terminal behavior | `UTEC-AC10` | Ordered terminal rung, exact unattended status, GUI/refusal negation | Complete | Same | `dev/test-results/01-unity-test-execution-contract-focused.xml` | PENDING | PENDING |
| AC11 | Reference-project execution | `UTEC-AC11-MANUAL` | Real Unity EditMode command and XML/log inspection while the main Editor is open | Partial — `not-executed (main Editor-open condition unavailable)` | External QA only | Prior closed-Editor evidence only: `/Users/jennywadkins/github_repos/the-movies/dev/test-results/01-unity-test-execution-contract-editmode.xml`, `/Users/jennywadkins/github_repos/the-movies/dev/test-results/01-unity-test-execution-contract-editmode.log`; concurrent-run artifact: none | PENDING | PENDING |
| AC12 | Structural/mutation guards | `UTEC-AC12` | Scoped parser, non-vacuity, 29 semantic mutation cases, focused/full pytest | Complete | `tests/test_unity_skill_contract.py` | `dev/test-results/01-unity-test-execution-contract-review-focused.xml`, `dev/test-results/01-unity-test-execution-contract-review-full-no-fixedpoint.xml` | PENDING | PENDING |

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | Mandatory `-batchmode`; obsolete optional claim removed | Complete | Skill, focused guards | Source-wide text sweep is non-empty and green. |
| AC2 | Two-row EditMode versus PlayMode/visual flags | Complete | Skill, focused guards | Two command examples also prove token separation. |
| AC3 | No `-quit` with tests; filtering unchanged | Complete | Skill, focused guards | Existing filter sentence retained; XML parser preserved and strengthened with exit-code warning. |
| AC4 | Deployed editor discovery; no bare executable | Complete | Skill, focused guards | Review replaced the authoring-only path with instructions to load Step 1 of the deployed `Visual Verifier` definition by display name from the active harness catalog, without copying its algorithm. External execution resolved the exact versioned Hub executable. |
| AC5 | Absolute main-checkout results and log paths | Complete | Skill, focused guards | Commands now write both XML and deterministic Unity logs under the main checkout. External XML/log artifacts landed there, not in the worktree. |
| AC6 | Commit-before-test and authentic checkout precondition | Complete | Skill, focused guards | Reference worktree tested committed SHA `2af127e4`; review added a fail-closed check for tracked, untracked, and ignored content outside the retained Unity `Library/`. |
| AC7 | Persistent detached worktree procedure | Partial — `not-executed (main Editor-open condition unavailable)` | Skill, focused guards | Creation, refresh, nested-project targeting, cleanliness, and retention are implemented. The 465.8-second run occurred with the main Editor closed. Retry preflight again found no main Editor process or lockfile, so no concurrent run was launched. |
| AC8 | Indefinite persistence and manual teardown | Complete | Skill, focused guards | No teardown was run. |
| AC9 | Licensing/lock fallback remains agent-run | Complete | Skill, focused guards | Licensing succeeded in this non-concurrent run, so rung 2 was not reached. |
| AC10 | No GUI/silent refusal; exact unattended status | Complete | Skill, focused guards | Semantic negations fail with named obligations. |
| AC11 | Run with main Editor open and record concurrency/usability | Partial — `not-executed (main Editor-open condition unavailable)` | External QA only | The prior closed-Editor run produced XML: 4,978 total, 4,954 passed, 17 failed, 7 skipped. It is not evidence for concurrency. Retry preflight found no main Editor process or lockfile; no new XML/log artifact exists for the required condition. |
| AC12 | Structural guards with deletion/negation proof | Complete | Focused guards | 32 cases pass, including 29 mutation cases. Review reproduced the fixed-path mutation failure, then restored green with non-vacuous all-occurrence mutation. |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `source_of_truth/skills/unity-development/SKILL.md` | Modify | Replaced `## Test Execution` with the mandatory headless contract, deployed editor discovery, nested-project path model, deterministic artifacts, clean worktree boundary, and execution ladder | Implements AC1–AC10 while keeping the runtime contract in the propagated skill |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| `tests/test_unity_skill_contract.py` | Create | Added section extraction, whitespace normalization, source sweep, command checks, contract validator, and 29 mutation cases | AC1–AC10, AC12; shared extension surface for Feature 02 |

## Test Results

- **Execution**: executed-failing
- **AC7/AC11 concurrent-run execution**: `not-executed (main Editor-open condition unavailable)`
- **Concurrent-run condition check**: `ps -ax -o pid=,command= | rg '/Applications/Unity/Hub/Editor/6000.3.13f1/Unity.app/Contents/MacOS/Unity'`; `test -f /Users/jennywadkins/github_repos/the-movies/Temp/UnityLockfile`
- **Concurrent-run results artifact**: None — the required main Editor-open condition was absent, so no Unity command was launched. The existing XML/log below belong only to the prior closed-Editor run.
- **Wave 1 integrated gate**: `executed-failing` — `uv run pytest tests/test_unity_skill_contract.py tests/test_agent_corpus_invariants.py tests/test_propagate_master_assets.py -q --junitxml=dev/test-results/phase-01-wave-1.xml`
- **Wave 1 integrated gate artifact**: `dev/test-results/phase-01-wave-1.xml` — 82 passed, 1 failed, 35 subtests passed. The sole failure is the phase-baseline `InstructionApplyToTests.test_every_enumerated_applyto_target_exists` wildcard-enumeration defect recorded before this feature; no remediation was made because it is unrelated to Phase 01.
- **Command**: `uv run pytest tests/test_unity_skill_contract.py --junitxml=dev/test-results/01-unity-test-execution-contract-review-focused.xml`; `uv run pytest tests/ -k 'not test_committed_tree_is_at_a_propagation_fixed_point' --junitxml=dev/test-results/01-unity-test-execution-contract-review-full-no-fixedpoint.xml`; `/Applications/Unity/Hub/Editor/6000.3.13f1/Unity.app/Contents/MacOS/Unity -batchmode -nographics -runTests -projectPath /Users/jennywadkins/github_repos/the-movies-agent-tests -testPlatform EditMode -testResults /Users/jennywadkins/github_repos/the-movies/dev/test-results/01-unity-test-execution-contract-editmode.xml -logFile /Users/jennywadkins/github_repos/the-movies/dev/test-results/01-unity-test-execution-contract-editmode.log`
- **Results artifact**: `dev/test-results/01-unity-test-execution-contract-review-focused.xml`; `dev/test-results/01-unity-test-execution-contract-review-full-no-fixedpoint.xml`; `/Users/jennywadkins/github_repos/the-movies/dev/test-results/01-unity-test-execution-contract-editmode.xml`; `/Users/jennywadkins/github_repos/the-movies/dev/test-results/01-unity-test-execution-contract-editmode.log`
- **Baseline**: 141 passed, 2 failed, 143 total (before implementation)
- **Final after review fixes**: repository 172 passed, 2 failed, 1 propagation-fixed-point test deliberately deselected to avoid modifying generated outputs, 175 collected; focused guards 32 passed, 0 failed; reference Unity EditMode 4,954 passed, 17 failed, 4,978 total, 7 skipped
- **New tests added**: 32 collected cases
- **Affected suites run**: focused Unity skill guards; full repository pytest suite; external reference-project Unity EditMode suite
- **Regressions**: Unknown — the repository suite remains executed-failing: its two baseline failures remain, and `test_committed_tree_is_at_a_propagation_fixed_point` is the expected source/generated mismatch while maintainer propagation is pending. The external Unity suite has 17 failures but no pre-change run in this pass, so they cannot be attributed to this Markdown-only feature.

## Deviations from Plan

- Selected `tests/test_unity_skill_contract.py` as the final proposed shared guard filename.
- Review replaced the authoring-only editor-discovery path with a harness-neutral instruction to load the deployed `Visual Verifier` definition by display name, preserving it as the single algorithm. Feature 03 must keep that consumer relationship aligned.
- Review distinguished the Git repository/worktree root from the root-or-nested Unity project path, added a fail-closed persistent-worktree cleanliness boundary, and required deterministic main-checkout Unity logs.
- The reference worktree currently uses 276 MB rather than the phase's approximate 600 MB estimate; the contract requires announcing an estimate, not pinning the observed size.
- Full pytest's fixed-point test wrote generated mirrors while demonstrating pending propagation. Those four generated skill changes were restored; propagation was not invoked. The test also removed eight pre-existing generated-agent diffs observed at baseline, which could not be reconstructed safely and was reported to the orchestrator.
- Added `dev/test-results/` to the external reference project's local `.git/info/exclude` so the required main-checkout artifacts remain available without dirtying its tracked working tree.

## Gaps

- AC7/AC11 concurrency is `not-executed (main Editor-open condition unavailable)`: retry preflight found neither the main Editor process nor its lockfile. Unity Personal concurrent-process permission and main-Editor usability remain unverified. Repeat only that condition with the retained worktree and reviewed command shape.
- The external EditMode suite is executed-failing (17 failures). This feature changes no reference-project code or tests; failure diagnosis is outside scope.
- Maintainer propagation is pending. No generated output was authored or committed by this feature.
- Phase-document reconciliation is pending because the review caller explicitly prohibited edits outside this feature's source/test files and feature folder.

## Reviewer Focus Areas

- Confirm the Test Execution section is terse enough for an always-loaded machine-facing skill while retaining all three ladder rungs.
- Check the focused validator for accidental prose pinning versus required command/token relationships, especially the repeated `Library/` mutation case.
- Verify `-testFilter` and XML parsing semantics remained unchanged apart from the explicit exit-code warning.
- Treat AC11 as partial until a run occurs while the main Editor is open; do not infer concurrency from the successful non-concurrent license connection.
