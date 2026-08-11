# Review Record: Unity Test Reference Assets

## Summary

Review-and-fix resolved all four Unity review findings. PlayMode now runs after an EditMode failure unless the workflow is cancelled, both artifact uploads remain always-run, shadow-worktree cleanliness permits only the execution project's `Library/`, local XML evidence is classified from counts and failing test names, zero discovery is `not-executed`, failure logs are retained, and the staging step describes evidence produced by its own command. Focused and Wave 3 guards are green. No propagation or external workflow/Unity execution occurred.

## Verdict

Approved with Reservations

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1 | Verified | `source_of_truth/skills/unity-development/references/gameci-test-workflow.yml:1-15`; `tests/test_unity_reference_assets.py:170-173` | The reference remains inert under the skill `references/` subtree; no active workflow was installed. |
| AC2 | Verified structurally | `source_of_truth/skills/unity-development/references/gameci-test-workflow.yml:17-57`; `tests/test_unity_reference_assets.py:23-70,188-228` | Current v4 actions, caller secret references, two explicit mode runs, failure-independent PlayMode, distinct outputs, and two always-run uploads are guarded. |
| AC3 | Verified | `docs/unity/LOCAL_TESTING.md:3-16`; `tests/test_unity_reference_assets.py:77-97` | Four-line TL;DR and 14 numbered one-command/result steps remain intact. Staging now uses one safely quoted file path and reports its own exit result. |
| AC4 | Verified structurally | `docs/unity/LOCAL_TESTING.md:18-124`; `tests/test_unity_reference_assets.py:99-167,231-279` | Worktree cleanliness, Editor discovery, EditMode/PlayMode flags, absolute artifacts, XML interpretation, headless import, and fallback behavior match the canonical skill. |
| AC5 | Verified structurally | `docs/unity/LOCAL_TESTING.md:124-148` | Unity Personal concurrency remains target-machine-dependent, teardown is fixed-path/manual only, and CI installation is out of scope. |
| AC6 | Verified | `tests/test_unity_reference_assets.py:23-279` | Twenty-four focused structural and mutation cases pass, including new PlayMode failure-independence, ignored-content boundary, XML evidence, failure-log, zero-test status, and staging-result mutations. GitHub Actions semantic validation remains explicit review evidence because `actionlint` is unavailable. |

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | A failing EditMode step prevented PlayMode from running because the later test retained GitHub's default `success()` condition. | High | `source_of_truth/skills/unity-development/references/gameci-test-workflow.yml:39-40` | AC2, AC6 | Fixed (applied during this review) |
| 2 | The runbook permitted ignored generated content outside the Unity project's `Library/`, weakening the canonical fail-closed worktree state. | High | `docs/unity/LOCAL_TESTING.md:68` | AC4, AC6 | Fixed (applied during this review) |
| 3 | Test-result checks omitted root counts, failing test names, zero-discovery handling, and deterministic failure-log retention. | Medium | `docs/unity/LOCAL_TESTING.md:94,102` | AC4, AC6 | Fixed (applied during this review) |
| 4 | Step 1's correct-result text referenced `git status --short` although the step only ran `git add`. | Medium | `docs/unity/LOCAL_TESTING.md:13-16` | AC3, AC6 | Fixed (applied during this review) |

## Fixes Applied

| File | What Changed | Issue # |
|------|--------------|---------|
| `source_of_truth/skills/unity-development/references/gameci-test-workflow.yml` | Added `if: ${{ !cancelled() }}` to the PlayMode execution while retaining separate `if: always()` artifact uploads. | 1 |
| `docs/unity/LOCAL_TESTING.md` | Tightened ignored-state acceptance to `<execution-unity-project>/Library/` only with fail-closed `not-executed`; added XML counts, failing names, zero-test status, and failure-log retention; made staging's result match its own safely quoted command. | 2–4 |
| `tests/test_unity_reference_assets.py` | Scoped the PlayMode condition to its step; required exactly two runner and upload actions; added failure-independence, strict cleanliness, evidence, and usability guards plus semantic mutations. | 1–4 |

## Remaining Concerns

- `actionlint` is not installed. Generic YAML composition and structural review do not prove GitHub Actions semantic validity; AC6 permits this to remain explicit review evidence.
- The reference workflow is intentionally inert and has no GitHub Actions or Unity Personal runtime evidence. Installation, secrets, runners, and CI adoption are out of scope.
- The safe repository regression run retains only the two documented pre-existing failures: PR-review display-name collision and wildcard `applyTo` resolution.
- The new skill reference remains pending maintainer propagation. No propagation command was run.

## Test Coverage Assessment

- Covered: AC1–AC6 through 24 focused cases, including seven workflow mutations, thirteen runbook mutations, artifact deletion, placement/inertness, command relationships, exact counts, and non-vacuity.
- Integration: Feature 03 and Feature 04 combined focused guards pass 54/54.
- Missing by accepted fallback: GitHub-Actions-compatible semantic parsing because `actionlint` is unavailable.

### Test Evidence

| Status | Command | Artifact | Counts |
|--------|---------|----------|--------|
| `executed-green` | `uv run pytest tests/test_unity_reference_assets.py -q --junitxml=dev/test-results/04-unity-test-reference-assets-review-fix.xml` | `dev/test-results/04-unity-test-reference-assets-review-fix.xml` | 24 passed, 0 failed, 24 total |
| `executed-green` | `uv run pytest tests/test_unity_consumer_contract.py tests/test_unity_reference_assets.py -q --junitxml=dev/test-results/phase-01-wave-3-review-fix.xml` | `dev/test-results/phase-01-wave-3-review-fix.xml` | 54 passed, 0 failed, 54 total |
| `executed-failing` | `uv run pytest tests/test_unity_reference_assets.py tests/test_agent_corpus_invariants.py tests/test_propagate_master_assets.py -q --junitxml=dev/test-results/04-unity-test-reference-assets-review-regression.xml` | `dev/test-results/04-unity-test-reference-assets-review-regression.xml` | 74 passed, 1 pre-existing failure, 75 total; 35 subtests passed |
| `executed-failing` | `uv run pytest tests/ -q -k 'not test_committed_tree_is_at_a_propagation_fixed_point' --junitxml=dev/test-results/04-unity-test-reference-assets-review-full-no-fixedpoint.xml` | `dev/test-results/04-unity-test-reference-assets-review-full-no-fixedpoint.xml` | 239 passed, 2 pre-existing failures, 1 propagation-invoking test deselected; 63 subtests passed |
| `not-executed` | `actionlint source_of_truth/skills/unity-development/references/gameci-test-workflow.yml` | No artifact — `actionlint` is not installed | GitHub Actions semantic validation unavailable |

## Risk Summary

- All High and Medium findings are fixed and mutation-guarded.
- The only validation reservation is the plan-permitted absence of a GitHub-Actions-compatible validator and external runtime execution for an intentionally inert reference.
- Repository-wide red results are unchanged baseline failures outside Feature 04 ownership.
