# Review Record: Unity Test Execution Contract

## Summary

Second review after the implementer retry confirms all source/test fixes remain intact and the focused contract suite is green. AC7/AC11 explicitly remain partial with `not-executed (main Editor-open condition unavailable)`. The earlier closed-Editor Unity XML is valid test output but is not concurrency or Editor-usability evidence.

## Verdict

Changes Requested

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1 | Verified | `source_of_truth/skills/unity-development/SKILL.md:173`; `tests/test_unity_skill_contract.py:44-45` | Mandatory `-batchmode` and source-wide optional-claim sweep pass. |
| AC2 | Verified | `source_of_truth/skills/unity-development/SKILL.md:179-186`; `tests/test_unity_skill_contract.py:46-57,171-177` | EditMode uses `-nographics`; PlayMode/visual retains graphics. |
| AC3 | Verified | `source_of_truth/skills/unity-development/SKILL.md:189-190`; `tests/test_unity_skill_contract.py:58-65` | No `-quit` with `-runTests`; affected-suite filtering semantics remain present. |
| AC4 | Verified after correction | `source_of_truth/skills/unity-development/SKILL.md:173-175`; `tests/test_unity_skill_contract.py:66-77` | The invalid authoring-only path was replaced with loading Step 1 of the deployed `Visual Verifier` definition by display name from the active harness catalog. Its algorithm remains single-source. |
| AC5 | Verified | `source_of_truth/skills/unity-development/SKILL.md:184-191`; `tests/test_unity_skill_contract.py:78-83,162-177` | XML and Unity log paths are absolute main-checkout artifacts; commands target the resolved Unity project. |
| AC6 | Verified structurally | `source_of_truth/skills/unity-development/SKILL.md:193,197`; `tests/test_unity_skill_contract.py:84-100` | Commit-before-test remains mandatory; reuse now rejects tracked, untracked, or non-Library ignored state rather than silently testing stale inputs. |
| AC7 | Partial — `not-executed (main Editor-open condition unavailable)` | `source_of_truth/skills/unity-development/SKILL.md:195-197`; implementation record lines 13-14, 50, 54 | Worktree lifecycle, nested path, cleanliness, and command are guarded. Retry preflight found no main Editor process or lockfile, so no concurrent run was launched. |
| AC8 | Verified structurally | `source_of_truth/skills/unity-development/SKILL.md:197,201`; `tests/test_unity_skill_contract.py:112-125,225-235` | Fixed path, indefinite persistence, Library retention, and manual-only teardown are guarded. |
| AC9 | Verified structurally | `source_of_truth/skills/unity-development/SKILL.md:198`; `tests/test_unity_skill_contract.py:126-131,236` | Licensing/lock fallback remains bounded and agent-run. It was not reached in external execution. |
| AC10 | Verified structurally | `source_of_truth/skills/unity-development/SKILL.md:199`; `tests/test_unity_skill_contract.py:132-138,237-238` | GUI/refusal prohibition and exact unattended status are mutation-tested. |
| AC11 | Partial — `not-executed (main Editor-open condition unavailable)` | Implementation record lines 73-80, 89-93 | The earlier closed-Editor XML is not concurrency evidence. The retry produced no concurrent-run artifact because the required Editor-open condition was absent. |
| AC12 | Verified | `tests/test_unity_skill_contract.py:16-248` | 32 focused cases pass, including 29 deletion/negation mutations; all-occurrence replacement closes the repeated fixed-path blind spot. |

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | Persistent worktree refresh preserved stale untracked/ignored state beyond `Library/`, undermining the committed-SHA claim. | High | `source_of_truth/skills/unity-development/SKILL.md:197` | AC6–AC7 | Fixed (applied during this review) |
| 2 | Commands conflated the Git worktree root with the Unity project root, breaking supported nested/monorepo layouts. | High | `source_of_truth/skills/unity-development/SKILL.md:177,184-186` | AC2, AC5, AC7 | Fixed (applied during this review) |
| 3 | Editor discovery referenced `source_of_truth/agents/...`, which does not exist in a normal consuming repository. | High | `source_of_truth/skills/unity-development/SKILL.md:175` | AC4 | Fixed (applied during this review) |
| 4 | The required main-Editor-open concurrency/usability scenario remains `not-executed (main Editor-open condition unavailable)`. | High | `dev/feature/01-unity-test-execution-contract/01-unity-test-execution-contract-implementation.md:13,33,50,54` | AC7, AC11 | Open (runtime condition unavailable) |
| 5 | The fixed-path mutation replaced only one repeated occurrence and survived, leaving the focused suite red. | High | `tests/test_unity_skill_contract.py:225,247` | AC12 | Fixed (applied during this review) |
| 6 | Canonical commands omitted deterministic `-logFile` artifacts needed to diagnose licensing/lock transitions. | Medium | `source_of_truth/skills/unity-development/SKILL.md:184-191` | AC5, AC7, AC11 | Fixed (applied during this review) |

## Fixes Applied

| File | What Changed | Issue # |
|------|--------------|---------|
| `source_of_truth/skills/unity-development/SKILL.md` | Added root/nested Unity path resolution, fail-closed persistent-worktree state validation, deployed Visual Verifier discovery loading, and absolute deterministic Unity logs. | 1, 2, 3, 6 |
| `tests/test_unity_skill_contract.py` | Added structural and command guards for the fixes, added semantic mutations, and changed mutation replacement to cover every repeated occurrence. | 1, 2, 3, 5, 6 |
| `dev/feature/01-unity-test-execution-contract/01-unity-test-execution-contract-implementation.md` | Corrected AC7/AC11 evidence statuses, test counts, artifact paths, deviations, and remaining gaps. | 4 |

## Remaining Concerns

- Issue #4: AC7/AC11 remain `not-executed (main Editor-open condition unavailable)` until the retained shadow worktree is exercised while the main Unity Editor is open and evidence records Unity Personal concurrency, GUI absence, and Editor usability.
- The external EditMode run remains `executed-failing`: 4,954 passed, 17 failed, 7 skipped, 4,978 total. This Markdown-only feature cannot establish whether those failures predate it because no reference baseline was captured.
- Maintainer propagation is pending. The review did not run propagation and restored generated mirrors modified by the fixed-point test.
- Phase-document reconciliation is pending because the caller explicitly prohibited phase-document edits.

## Test Coverage Assessment

- Covered: AC1–AC6, AC8–AC10, and AC12 through 32 focused structural/command/mutation cases.
- Partial: AC7 worktree mechanics are structurally covered, but the required open-Editor runtime condition is missing.
- Missing: AC11 concurrent Unity Personal and main-Editor usability evidence.

### Test Evidence

| Status | Command | Artifact | Counts |
|--------|---------|----------|--------|
| `executed-green` | `uv run pytest tests/test_unity_skill_contract.py -q --junitxml=dev/test-results/01-unity-test-execution-contract-second-review.xml` | `dev/test-results/01-unity-test-execution-contract-second-review.xml` | 32 passed, 0 failed, 32 total |
| `not-executed` | Main Editor-open Unity concurrency run | No artifact — required condition unavailable | AC7/AC11: `not-executed (main Editor-open condition unavailable)` |
| `executed-failing` | `uv run pytest tests/ -k 'not test_committed_tree_is_at_a_propagation_fixed_point' --junitxml=dev/test-results/01-unity-test-execution-contract-review-full-no-fixedpoint.xml` | `dev/test-results/01-unity-test-execution-contract-review-full-no-fixedpoint.xml` | 172 passed, 2 failed, 174 executed; 1 deliberately deselected; 175 collected |
| `executed-failing` | `uv run pytest tests/test_agent_corpus_invariants.py tests/test_propagate_master_assets.py --junitxml=dev/test-results/01-unity-test-execution-contract-review-regression.xml` | `dev/test-results/01-unity-test-execution-contract-review-regression.xml` | 50 passed, 1 failed, 51 total |
| `executed-failing` | `/Applications/Unity/Hub/Editor/6000.3.13f1/Unity.app/Contents/MacOS/Unity -batchmode -nographics -runTests -projectPath /Users/jennywadkins/github_repos/the-movies-agent-tests -testPlatform EditMode -testResults /Users/jennywadkins/github_repos/the-movies/dev/test-results/01-unity-test-execution-contract-editmode.xml -logFile /Users/jennywadkins/github_repos/the-movies/dev/test-results/01-unity-test-execution-contract-editmode.log` | `/Users/jennywadkins/github_repos/the-movies/dev/test-results/01-unity-test-execution-contract-editmode.xml` | 4,954 passed, 17 failed, 7 skipped, 4,978 total |

The two repository failures in the 174-test review run are the pre-existing agent-name/prose collision and wildcard `applyTo` failures. The intentionally deselected fixed-point test is known to fail while propagation is pending and writes generated outputs as part of reporting that failure.

## Risk Summary

- Second-review verdict remains Changes Requested: AC7/AC11 are partial because the required main Editor-open shadow-worktree run is `not-executed (main Editor-open condition unavailable)`.
- The reviewed contract is internally coherent for root and nested Unity layouts and now fails closed on contaminated persistent worktrees.
- Feature 03 must keep the Visual Verifier as the single deployed editor-discovery implementation when aligning consumers.
- External Unity tests produced real failing evidence; their attribution remains unknown without a pre-feature Unity baseline.
