# Implementation Record: Unity Test Reference Assets

## Summary

Added an inert, copyable GameCI workflow reference and a human-facing local Unity testing runbook. Added 17 focused structural and mutation guards covering placement, current action versions, explicit EditMode and PlayMode execution, secret safety, runbook shape, worktree lifecycle, fallback ordering, command flags, and manual teardown. No active workflow was installed and propagation was not run.

## Preflight

- Confirmed Features 01 and 02 had finalized `source_of_truth/skills/unity-development/SKILL.md`; re-read its Test Execution and Serialized Assets contracts before authoring.
- Selected `gameci-test-workflow.yml`, `LOCAL_TESTING.md`, and `test_unity_reference_assets.py` as the final proposed filenames.
- Rechecked the official GameCI Test Runner documentation on 2026-08-10 at `https://game.ci/docs/github/test-runner/`. It documents `game-ci/unity-test-runner@v4`, `actions/checkout@v4`, `actions/upload-artifact@v4`, EditMode/PlayMode, Unity Personal secret references, `artifactsPath`, the step `artifactsPath` output, and optional `githubToken` behavior.
- Context7 returned an older `unity-test-runner@v2` example, so the current official GameCI page was treated as authoritative.
- `actionlint` was not installed. No GitHub-Actions-compatible validator was therefore available without adding tooling. Automated claims remain structural; parseability was reviewed explicitly. The existing environment's PyYAML successfully composed the file as generic YAML syntax, but that check is not claimed as GitHub Actions semantic validation.
- Confirmed the workflow is absent from `.github/workflows/`, no Unity repository was modified, and no propagation command was run.

## Sibling Features

- Depends on `01-unity-test-execution-contract` and `02-headless-asset-import`; their finalized canonical Unity skill is consumed read-only.
- Parallel-safe with `03-unity-consumer-alignment`; that sibling owns consumer agents and `tests/test_unity_consumer_contract.py`. Its concurrent edits were left untouched.

## AC Coverage Matrix

| AC | Criterion ID | Planned Test ID | Planned Test Pattern | Status | Implementing Files | Evidence Paths | Implement Commit SHA | Review Commit SHA |
|----|--------------|-----------------|----------------------|--------|--------------------|----------------|----------------------|-------------------|
| AC1 | AC1 | Reference assets exist only in inert locations | Placement and active-workflow absence | Complete | `source_of_truth/skills/unity-development/references/gameci-test-workflow.yml` | `tests/test_unity_reference_assets.py`; `dev/test-results/04-unity-test-reference-assets-focused.xml` | PENDING | PENDING |
| AC2 | AC2 | GameCI workflow contract; workflow mutations are killed | Action versions, explicit modes, distinct artifact linkage, permissions, secret references | Complete | `source_of_truth/skills/unity-development/references/gameci-test-workflow.yml` | `tests/test_unity_reference_assets.py`; `dev/test-results/04-unity-test-reference-assets-focused.xml` | PENDING | PENDING |
| AC3 | AC3 | Local runbook contract | TL;DR length, numbered one-command steps, correct-result statements | Complete | `docs/unity/LOCAL_TESTING.md` | `tests/test_unity_reference_assets.py`; `dev/test-results/04-unity-test-reference-assets-focused.xml` | PENDING | PENDING |
| AC4 | AC4 | Local runbook contract; runbook mutations are killed | Worktree lifecycle, costs, editor discovery, flags, results, import, ordered fallback | Complete | `docs/unity/LOCAL_TESTING.md` | `tests/test_unity_reference_assets.py`; `dev/test-results/04-unity-test-reference-assets-focused.xml` | PENDING | PENDING |
| AC5 | AC5 | Local runbook contract; runbook mutations are killed | Target-machine licensing caveat, manual teardown, fixed target, CI scope | Complete | `docs/unity/LOCAL_TESTING.md` | `tests/test_unity_reference_assets.py`; `dev/test-results/04-unity-test-reference-assets-focused.xml` | PENDING | PENDING |
| AC6 | AC6 | Workflow and runbook mutation tests | Non-vacuous structural checks plus deletion and negation mutations | Complete | `tests/test_unity_reference_assets.py` | `dev/test-results/04-unity-test-reference-assets-focused.xml`; `dev/test-results/04-unity-test-reference-assets-propagation.xml` | PENDING | PENDING |

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | Inert, copyable GameCI template under the Unity skill references tree | Complete | `source_of_truth/skills/unity-development/references/gameci-test-workflow.yml` | No active workflow path was created. |
| AC2 | Complete minimal GameCI test and artifact contract with current verified versions and secret references | Complete | `source_of_truth/skills/unity-development/references/gameci-test-workflow.yml` | Uses separate EditMode and PlayMode steps, read-only contents permission, and always-run uploads. |
| AC3 | Human-facing local runbook in the required format | Complete | `docs/unity/LOCAL_TESTING.md` | Four-line TL;DR; 14 numbered one-action steps with exact commands and correct-result checks. |
| AC4 | Runbook fidelity to finalized execution, worktree, import, evidence, and fallback contracts | Complete | `docs/unity/LOCAL_TESTING.md` | Manually compared line by line with the finalized canonical skill; guards pin the critical relationships. |
| AC5 | Manual teardown, CI boundary, and Unity Personal target-machine caveat | Complete | `docs/unity/LOCAL_TESTING.md` | Teardown requires adjacent fixed-path validation and is never automatic. |
| AC6 | Structural, safety, formatting, and mutation guards | Complete | `tests/test_unity_reference_assets.py` | 17 focused tests pass. GitHub Actions semantic validation remains explicit review evidence because no compatible validator is installed, as AC6 permits. |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `source_of_truth/skills/unity-development/references/gameci-test-workflow.yml` | Create | Added a minimal inert GameCI workflow with distinct EditMode/PlayMode runs and always-run artifact uploads. | Gives maintainers a safe, copyable CI starting point without activating CI. |
| `docs/unity/LOCAL_TESTING.md` | Create | Added the local worktree, test, import, fallback, evidence, and teardown runbook. | Makes the canonical machine-facing contract directly executable by a human. |
| `dev/feature/04-unity-test-reference-assets/04-unity-test-reference-assets-tasks.md` | Modify | Marked completed tasks and retained the unsafe exact-full-suite step as incomplete with its reason. | Keeps pipeline state aligned with executed evidence. |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| `tests/test_unity_reference_assets.py` | Create | Added non-vacuous structural checks and deletion/negation mutations for both reference assets. | AC1–AC6 |

## Test Results

- **Execution**: executed-failing
- **Command**: `uv run pytest tests/test_unity_reference_assets.py -q`
- **Results artifact**: terminal evidence only; red run produced 15 failed because both planned assets were absent
- **Baseline**: 0 passed, 15 failed (feature red state)
- **Final**: 17 passed, 0 failed
- **New tests added**: 17
- **Affected suites run**: `uv run pytest tests/test_unity_reference_assets.py -q --junitxml=dev/test-results/04-unity-test-reference-assets-focused.xml` — 17 passed; `uv run pytest tests/test_unity_consumer_contract.py tests/test_unity_reference_assets.py -q --junitxml=dev/test-results/phase-01-wave-3-focused.xml` — 42 passed; `python3 -c 'from pathlib import Path; import yaml; p=Path("source_of_truth/skills/unity-development/references/gameci-test-workflow.yml"); yaml.compose(p.read_text()); print("generic YAML syntax: PASS")'` — passed as generic YAML syntax only; `uv run pytest tests/test_propagate_master_assets.py -q --junitxml=dev/test-results/04-unity-test-reference-assets-propagation.xml` — 43 passed, 1 known unrelated failure, 35 subtests passed; `uv run pytest tests/ -q -k 'not test_committed_tree_is_at_a_propagation_fixed_point' --junitxml=dev/test-results/04-unity-test-reference-assets-regression.xml` — 227 passed, 2 known unrelated failures, 1 propagation-invoking test deselected, 63 subtests passed
- **Regressions**: Known pre-existing failures only: `test_agent_name_does_not_collide_with_prose_in_any_source_asset` and `InstructionApplyToTests.test_every_enumerated_applyto_target_exists`. The exact full suite was not run because `test_committed_tree_is_at_a_propagation_fixed_point` invokes propagation against the working tree, which repository instructions forbid during agent work.

## Deviations from Plan

- Chose the final filenames recorded in Preflight.
- No GitHub-Actions-compatible validator was installed. Per AC6, the implementation separates automated structural evidence, successful generic YAML syntax composition, and explicit GitHub Actions shape review instead of claiming semantic parse validation.
- The exact `uv run pytest tests/` command was replaced with a safe equivalent that deselected the single test known to invoke propagation against the working tree.
- The generic YAML library became importable by implementation time although discovery recorded it unavailable; no dependency or manifest change was made by this feature.

## Gaps

- The inert workflow has not been installed or executed in GitHub Actions. Installation, secrets, runners, and CI adoption are explicit non-goals.
- The copied workflow should be validated with a GitHub-Actions-compatible validator such as `actionlint` after repository-specific substitution and before activation.
- The new skill reference remains pending maintainer propagation. Propagation was not run.
- The repository regression suite remains red only for the two recorded baseline failures.

## Reviewer Focus Areas

- `source_of_truth/skills/unity-development/references/gameci-test-workflow.yml` — verify the separate GameCI v4 steps and artifact-output linkage against current official documentation.
- `docs/unity/LOCAL_TESTING.md` — verify command sequence fidelity to the canonical Unity skill, especially the fallback ladder and manual teardown boundary.
- `tests/test_unity_reference_assets.py` — verify content guards stay structural, non-vacuous, and capable of detecting deletion or semantic negation without pinning incidental prose.
