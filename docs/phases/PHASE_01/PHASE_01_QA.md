# Phase 01 QA

## TL;DR

- Run the three focused guard files; the correct result is 99 passes.
- The safe full suite should show only the two known baseline failures.
- Unity concurrency, clean `.meta` import, and `actionlint` still need suitable environments.
- Do not run propagation or edit `ports/` or `.github/` during this QA.

## Current status

The authored contracts and reference assets pass their focused automated checks. The phase is not fully accepted because the main-Editor-open Unity run and the controlled clean-project import have not been executed under their required conditions. The GameCI file has structural coverage, but GitHub Actions semantic validation is also pending because `actionlint` is not installed.

There are no visual acceptance criteria in this phase. Record `visual-verification: no visual ACs`; do not create screenshots or run capture tooling.

## Automated release checks

1. Run every manifest-listed focused guard.

   ```bash
   uv run pytest tests/test_unity_skill_contract.py tests/test_unity_consumer_contract.py tests/test_unity_reference_assets.py -q --junitxml=dev/test-results/phase-01-qa-focused.xml
   ```

   **Correct result:** `99 passed`, with zero failures. This covers all three final verification assets, including their deletion and semantic-negation mutation cases.

2. Run the safe full regression suite.

   ```bash
   uv run pytest tests/ -q -k 'not test_committed_tree_is_at_a_propagation_fixed_point' --junitxml=dev/test-results/phase-01-qa-full-no-fixedpoint.xml
   ```

   **Correct result:** `239 passed, 2 failed, 1 deselected`, with 63 subtests. The propagation fixed-point test is the one deselected test, and the failures are only these two known baseline failures:

   - `tests/test_pr_review_orchestrator.py::test_agent_name_does_not_collide_with_prose_in_any_source_asset`
   - `tests/test_propagate_master_assets.py::InstructionApplyToTests::test_every_enumerated_applyto_target_exists`

   The phase baseline was 141 passes and the same two failures. Any different failure is a regression.

   **Warning:** Do not run the fixed-point test in the working tree. It invokes propagation. Propagation is a maintainer-only step and remains pending for this phase.

3. Confirm the phase did not author generated output.

   ```bash
   git diff --name-only -- ports .github
   ```

   **Correct result:** No phase-authored generated-file changes are listed. If a source/generated sync check fails, report `maintainer propagation pending`; do not edit generated files and do not run `scripts/propagate_master_assets.py`.

## Manual and environment-dependent checks

4. Prove the persistent-worktree EditMode path while the main Editor is open.

   First confirm the retained worktree has no tracked changes, untracked files, or ignored content outside its Unity `Library/`:

   ```bash
   git -C /Users/jennywadkins/github_repos/the-movies-agent-tests status --short --untracked-files=all --ignored | awk '$2 !~ /^Library\//'
   ```

   **Correct result:** No output. If anything appears, stop without deleting it and record `not-executed (shadow worktree not clean)`.

   With `/Users/jennywadkins/github_repos/the-movies` open in Unity 6000.3.13f1, refresh the clean detached worktree to the committed main-checkout revision and run EditMode there:

   ```bash
   git -C /Users/jennywadkins/github_repos/the-movies worktree prune
   git -C /Users/jennywadkins/github_repos/the-movies-agent-tests checkout --detach "$(git -C /Users/jennywadkins/github_repos/the-movies rev-parse HEAD)"
   mkdir -p /Users/jennywadkins/github_repos/the-movies/dev/test-results
   /Applications/Unity/Hub/Editor/6000.3.13f1/Unity.app/Contents/MacOS/Unity -batchmode -nographics -runTests -projectPath /Users/jennywadkins/github_repos/the-movies-agent-tests -testPlatform EditMode -testResults /Users/jennywadkins/github_repos/the-movies/dev/test-results/phase-01-qa-editor-open-editmode.xml -logFile /Users/jennywadkins/github_repos/the-movies/dev/test-results/phase-01-qa-editor-open-editmode.log
   ```

   **Correct result:** No GUI appears, the mouse remains available, the already-open main Editor remains usable, and the absolute XML and log paths exist. The XML contains a root `<test-run>` with more than zero discovered tests. Record total, passed, failed, and skipped counts, every failing test name, and whether Unity Personal allowed the concurrent process.

   If licensing or locking blocks the worktree, follow the documented fallback: ask the operator to close the main Editor, then let the agent run the same command against the main checkout. If the operator declines or is unavailable, record exactly `not-executed: editor open, user unavailable`. Never launch a GUI or ask the operator to run the tests.

   **Current evidence:** `not-executed (main Editor-open condition unavailable)`. The earlier closed-Editor XML reported 4,978 total, 4,954 passed, 17 failed, and 7 skipped, but it does not prove concurrency or Editor usability.

5. Prove controlled missing-`.meta` regeneration in a clean reference checkout.

   ```bash
   git -C /Users/jennywadkins/github_repos/the-movies status --short
   ```

   **Correct result:** No output. If the checkout is not clean, stop before choosing an asset and record `not-executed (reference project not clean)`. Do not clean, overwrite, or remove unrelated work.

   After a maintainer identifies one safe tracked `.meta` fixture, substitute its exact repository-relative path below. Close the main Editor first. Keep the original file in a temporary directory so restoration is immediate and exact.

   ```bash
   QA_META_REL='Assets/<validated-safe-fixture>.meta'
   QA_META_BACKUP="$(mktemp -d)"
   git -C /Users/jennywadkins/github_repos/the-movies ls-files --error-unmatch "$QA_META_REL"
   mv "/Users/jennywadkins/github_repos/the-movies/$QA_META_REL" "$QA_META_BACKUP/original.meta"
   /Applications/Unity/Hub/Editor/6000.3.13f1/Unity.app/Contents/MacOS/Unity -batchmode -quit -projectPath /Users/jennywadkins/github_repos/the-movies -logFile /Users/jennywadkins/github_repos/the-movies/dev/test-results/phase-01-qa-asset-import.log
   test -f "/Users/jennywadkins/github_repos/the-movies/$QA_META_REL"
   rg '^guid: [0-9a-f]{32}$' "/Users/jennywadkins/github_repos/the-movies/$QA_META_REL"
   mv "$QA_META_BACKUP/original.meta" "/Users/jennywadkins/github_repos/the-movies/$QA_META_REL"
   git -C /Users/jennywadkins/github_repos/the-movies status --short
   ```

   **Correct result:** Unity stays headless, regenerates the selected `.meta` with a GUID, the original `.meta` is restored, and the final Git status is empty. Retain the import log and record the selected fixture. If any command fails after the move, restore the backup before doing anything else.

   **Current evidence:** `not-executed (reference project not clean)`. The checkout currently contains unrelated modified and untracked work, so no Unity import or external mutation was attempted.

6. Validate the inert GameCI workflow with a GitHub-Actions-aware validator.

   ```bash
   command -v actionlint
   actionlint source_of_truth/skills/unity-development/references/gameci-test-workflow.yml
   ```

   **Correct result:** Both commands exit zero and `actionlint` reports no diagnostics. If the first command has no output, record `not-executed (actionlint unavailable)`; generic YAML parsing is not equivalent evidence.

   Then compare `actions/checkout@v4`, `game-ci/unity-test-runner@v4`, `actions/upload-artifact@v4`, `projectPath`, `testMode`, `artifactsPath`, artifact outputs, read-only permissions, and the `UNITY_LICENSE`/`UNITY_EMAIL`/`UNITY_PASSWORD` convention with the current official GameCI test-runner and activation documentation.

   **Correct result:** Every version, key, output, permission, and secret convention matches the current official documentation. The workflow remains inert; do not install, activate, or run it in a Unity repository as part of this phase.

   **Current evidence:** Structural checks pass, but `actionlint` is unavailable. The versions and conventions were checked during implementation on 2026-08-10 and still require release-time reverification.

7. Dry-run the local Unity runbook against the canonical skill.

   ```bash
   sed -n '1,260p' docs/unity/LOCAL_TESTING.md
   sed -n '/## Test Execution/,/## /p' source_of_truth/skills/unity-development/SKILL.md
   ```

   **Correct result:** The runbook has a TL;DR of no more than five lines and 14 numbered, one-action steps. Each step has an exact command and a correct result. EditMode uses `-batchmode -nographics`; PlayMode keeps graphics; neither test command uses `-quit`; results and logs use absolute main-checkout paths; the agent runs tests; and teardown is manual only after the adjacent fixed-target check. The CI section says installation, secrets, runners, and activation are out of scope.

## Release decision

The phase is ready for final review only when checks 1–3 have the expected automated result and checks 4–7 have recorded evidence. Until checks 4 and 5 run under their required conditions, keep Features 01 and 02 partial. An unavailable `actionlint` remains an explicit Feature 04 reservation, not a pass.
