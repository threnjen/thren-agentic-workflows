# Local Unity Testing

## TL;DR

Commit the code you intend to test, then use the persistent detached test worktree.
Resolve the Unity Editor through the `unity-development` skill's Editor discovery procedure.
Run EditMode and PlayMode from the command line and save results in the main checkout.
Remove the test worktree only when you deliberately choose to reclaim it.

## 1. Stage the files to test

```bash
git -C "<main-repo-root>" add -- "<file-to-test>"
```

**Correct result:** The command exits with status 0 and reports no path or repository error. Repeat this step for each file that belongs in the testable commit.

## 2. Commit the testable state

```bash
git -C "<main-repo-root>" commit -m "test: checkpoint Unity changes"
```

**Correct result:** Git prints the new commit identifier. The test worktree can now use that exact state.

## 3. Prune stale worktree registrations

```bash
git -C "<main-repo-root>" worktree prune
```

**Correct result:** The command exits successfully. It does not remove a valid test worktree.

## 4. Inspect registered worktrees

```bash
git -C "<main-repo-root>" worktree list --porcelain
```

**Correct result:** The main checkout is listed. Reuse `<project-dir>-agent-tests/` if it is already listed.

## 5. Create the detached test worktree when missing

The first checkout uses roughly 600 MB before Unity's cache grows. Its first Unity import is normally a multi-minute first import.

```bash
git -C "<main-repo-root>" worktree add --detach "<project-dir>-agent-tests/" HEAD
```

**Correct result:** Git reports a detached checkout at `<project-dir>-agent-tests/`. Skip this step when that worktree already exists.

## 6. Refresh the existing test worktree

This keeps the Unity project's `Library/` directory so later imports are faster.

```bash
git -C "<project-dir>-agent-tests/" checkout --detach "$(git -C "<main-repo-root>" rev-parse HEAD)"
```

**Correct result:** Both checkouts report the same commit. The persistent worktree and its `Library/` directory remain in place.

## 7. Check the test worktree before running Unity

```bash
git -C "<project-dir>-agent-tests/" status --short --untracked-files=all --ignored
```

**Correct result:** There are no tracked changes or untracked files and no ignored content outside `<execution-unity-project>/Library/`. If any other path appears, stop and report `not-executed` without deleting or overwriting anything.

## 8. Resolve the Unity Editor executable

Follow the `unity-development` skill's Test Execution section, Editor discovery. Use its resolution order, then verify the resolved path.

```bash
test -x "<resolved-unity-editor>"
```

**Correct result:** The command exits with status 0.

## 9. Create the main-checkout results directory

```bash
mkdir -p "<absolute-main-checkout>/dev/test-results"
```

**Correct result:** `<absolute-main-checkout>/dev/test-results` exists in the main checkout.

## 10. Run EditMode tests

```bash
"<resolved-unity-editor>" -batchmode -nographics -runTests -projectPath "<project-dir>-agent-tests/<unity-project-relative-path>" -testPlatform EditMode -testResults "<absolute-main-checkout>/dev/test-results/editmode-results.xml" -logFile "<absolute-main-checkout>/dev/test-results/editmode-unity.log"
```

**Correct result:** `editmode-results.xml` exists. Record the root `<test-run total= passed= failed=>` counts and every `<test-case result="Failed">` name. A run with zero discovered tests is `not-executed`. On any failure, retain its Unity log at `editmode-unity.log` with the XML.

## 11. Run PlayMode tests

```bash
"<resolved-unity-editor>" -batchmode -runTests -projectPath "<project-dir>-agent-tests/<unity-project-relative-path>" -testPlatform PlayMode -testResults "<absolute-main-checkout>/dev/test-results/playmode-results.xml" -logFile "<absolute-main-checkout>/dev/test-results/playmode-unity.log"
```

**Correct result:** `playmode-results.xml` exists. Record the root `<test-run total= passed= failed=>` counts and every `<test-case result="Failed">` name. A run with zero discovered tests is `not-executed`. On any failure, retain its Unity log at `playmode-unity.log` with the XML.

## 12. Run a controlled headless import when required

Use this only when the target project needs an asset refresh, such as generating a missing `.meta` file. Treat regeneration as unverified until a real clean fixture proves it.

```bash
"<resolved-unity-editor>" -batchmode -quit -projectPath "<project-dir>-agent-tests/<unity-project-relative-path>" -logFile -
```

**Correct result:** Unity exits successfully and the test worktree contains only the expected import changes. Do not copy unexpected generated changes into the main checkout.

## When the detached worktree cannot run

Use this fallback ladder in order:

1. Keep using the persistent detached worktree when its Unity project is available.
2. If licensing or a project lock blocks it, ask the user to close the main Unity Editor. Then the agent runs the same headless commands against `<main-repo-root>/<unity-project-relative-path>`.
3. If the Editor is open and the user cannot close it, stop with `not-executed: editor open, user unavailable` and preserve the logs already written.

Never launch a GUI. Agent runs every test command itself; it does not delegate execution to the user.

Unity Personal licensing may limit concurrent Editor processes. Confirm the target machine's license behavior before relying on simultaneous main-Editor and test-worktree execution.

## 13. Verify the worktree target before teardown

Teardown is never automatic. Confirm the exact fixed sibling path before removing anything.

```bash
git -C "<main-repo-root>" worktree list --porcelain
```

**Correct result:** The output identifies `<project-dir>-agent-tests/` as the detached worktree you intend to remove.

## 14. Remove the test worktree manually

Only run this after Step 13 confirms the exact path.

```bash
git -C "<main-repo-root>" worktree remove "<project-dir>-agent-tests/"
```

**Correct result:** The detached worktree registration and directory are gone. The main checkout remains unchanged.

## CI reference

The inert GameCI example lives at `source_of_truth/skills/unity-development/references/gameci-test-workflow.yml`. CI installation is out of scope. Repository secrets, runner setup, and workflow activation are also out of scope. Copy the reference deliberately, replace `<UNITY_PROJECT_PATH>`, validate it, and review Unity Personal licensing before enabling it.
