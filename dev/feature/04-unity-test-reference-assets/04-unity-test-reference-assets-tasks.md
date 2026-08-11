# Feature Tasks: Unity Test Reference Assets

## Stage 1: Current GameCI Contract Verification

- [x] Confirm `01-unity-test-execution-contract` and `02-headless-asset-import` are complete, then read the finalized Test Execution and Serialized Assets sections before encoding workflow or runbook expectations. (AC2, AC4)
- [x] Recheck the current official GameCI Test Runner documentation and record the implementation-time source/date for the supported action version, `testMode` values, Personal-license secret inputs, artifact path/output, and GitHub token behavior. (AC2)
- [x] Recheck the official versions and required fields for checkout and artifact upload, and determine the smallest workflow permissions compatible with the chosen GameCI configuration. (AC2)
- [x] Decide whether the workflow uses separate EditMode and PlayMode steps or another equally explicit non-matrix form; preserve distinct artifact paths and uploads for both modes. (AC2)
- [x] Choose terse final filenames for `source_of_truth/skills/unity-development/references/[PROPOSED - name TBD: GameCI workflow template].yml`, `docs/unity/[PROPOSED - name TBD: local Unity test runbook].md`, and `tests/[PROPOSED - name TBD: Unity reference asset guards]`; record the selected names in implementation notes. (AC1, AC3, AC6)
- [x] Select a GitHub-Actions-compatible workflow validation method. If no parser/validator is available without adding unjustified tooling, explicitly separate structural automated checks from full parse review evidence rather than claiming token checks prove parseability. (AC6)

## Stage 2: Reference Asset Guards

- [x] Create `tests/[PROPOSED - name TBD: Unity reference asset guards]` using scenario-based test names; derive required paths from the repository root and assert every file and scoped section enumeration is non-empty. (AC1, AC3, AC6)
- [x] Add a placement/inertness guard proving the workflow exists only under the Unity skill's `references/` subtree and is not installed under this repository's `.github/workflows/` or represented as an active workflow path. (AC1, AC6)
- [x] Add the selected parse/shape validation and assert the workflow contains a minimally permissioned job, checkout, explicit EditMode and PlayMode GameCI runs, and always-run artifact publication tied to each test step's artifact path. (AC2, AC6)
- [x] Add a secret-safety guard that permits GitHub secret expressions but rejects literal Unity license, email, password, serial, token, or credential-like values; assert the scan inspected all relevant workflow scalar values. (AC2, AC6)
- [x] Add a runbook-format guard proving the TL;DR is no more than five lines, numbered steps follow it, and every step contains one exact command plus a correct-result description. Avoid pinning incidental prose. (AC3, AC6)
- [x] Add scoped runbook guards for commit-before-test, prune-before-reuse, fixed detached sibling creation/reuse, committed-SHA refresh with `Library/` retention, first-use cost/delay announcement, editor discovery reuse, and absolute main-checkout result paths. (AC4, AC6)
- [x] Add command-relationship guards proving EditMode uses `-batchmode -nographics`, PlayMode/visual uses `-batchmode` without `-nographics`, test runs do not pair `-quit` with `-runTests`, and headless import uses the finalized import contract. (AC4, AC6)
- [x] Add fallback and operability guards proving all three ladder rungs remain ordered, the agent retains responsibility for test execution, GUI launch and user-run handoff are forbidden, Unity Personal concurrency remains target-machine-dependent, and teardown is manual only. (AC4, AC5, AC6)
- [x] Add teardown safety guards proving the warning and explicit fixed-target validation are adjacent to the command and rejecting broad variables, globs, or recursive deletion targets. (AC5, AC6)
- [x] Delete or semantically negate each protected workflow/runbook mechanism in an isolated fixture or reversible mutation; confirm the relevant guard fails with the obligation named, restore it, and confirm green. Include deletion of artifact upload, worktree persistence, and GUI prohibition. (AC6)

## Stage 3: Workflow and Runbook Authoring

- [x] Create the final `source_of_truth/skills/unity-development/references/` workflow file without adding anything under `.github/workflows/`; keep it clearly inert and copyable with placeholders for repository-specific project values. (AC1)
- [x] Add the verified checkout and GameCI Test Runner actions with separate explicit EditMode and PlayMode intent, caller-supplied Unity secret references, and only the permissions required by the selected configuration. (AC2)
- [x] Give each GameCI test step a distinct identifier/artifact location and publish its results with an always-run verified artifact action so failed tests still leave evidence. (AC2)
- [x] Keep the workflow free of literal credentials, machine-specific paths, matrices, caching, build/deploy jobs, runner provisioning, and unrelated quality gates. (AC1–AC2)
- [x] Create the final `docs/unity/` runbook with a five-lines-or-fewer TL;DR followed by numbered one-action steps; give every step its exact command and correct-result description. (AC3)
- [x] Document the finalized local sequence: require a committed SHA, prune stale registrations, validate and create/reuse the detached `<project-dir>-agent-tests/` sibling, announce that it consumes substantial disk space (about 600 MB for the reference project) and that first import takes several minutes, then refresh without deleting `Library/`. (AC4)
- [x] Direct the operator to resolve the Unity executable through the existing Visual Verifier procedure and write test XML and Unity logs to absolute paths under the main checkout's `dev/test-results/`. (AC4)
- [x] Document EditMode, PlayMode/visual, and asset-import commands with their distinct flag relationships, plus the finalized three-rung fallback that never opens a GUI and never asks the user to run tests. (AC4)
- [x] Document Unity Personal concurrent-process behavior as a target-machine verification, not a guarantee, and explain how a license/lock result transitions to rung 2. (AC5)
- [x] Add manual teardown only after explicit fixed-path ownership validation, with the warning beside the destructive command; state that teardown is never automatic and `Library/` persistence is intentional. (AC5)
- [x] State plainly that the bundled CI workflow is not installed, license secrets and runners are not configured, and CI adoption policy remains outside this feature. (AC5)
- [x] Review the runbook against the canonical skill and remove duplicated machine-facing rationale while retaining every command and result needed for a human to complete the procedure. (AC3–AC5)

## Stage 4: Verification

- [x] Run the selected GitHub Actions workflow parser/validator and the focused structural guards using the final filename; record separately which evidence proves parseability and which proves repository-specific relationships. (AC1–AC2, AC6)
- [x] Run `uv run pytest tests/[PROPOSED - name TBD: Unity reference asset guards]` using the selected final module name and record the exact pass/fail result. (AC1–AC6)
- [x] Manually dry-run the runbook line by line against the finalized skill and Phase 01 reference-project facts without installing CI, creating a GUI fallback, or performing automatic teardown. (AC3–AC5)
- [x] Run `uv run pytest tests/test_propagate_master_assets.py` without running propagation; identify the pre-existing wildcard `applyTo` failure separately and report any source/generated sync failure as propagation pending. (AC1, AC6)
- [ ] Run `uv run pytest tests/` and compare with the captured baseline of 141 passed and 2 failed, reporting both known unrelated failures separately from any feature regression. (AC1–AC6) — Not run because the suite contains a test that invokes propagation against the working tree; the safe equivalent excluded that one test and reproduced only the two known failures.
- [x] Inspect the final diff to confirm only the selected workflow, runbook, and focused guard module were authored; no Feature 01–03 file, generated port, active workflow, dependency manifest, or external Unity repository changed. (AC1–AC6)
- [x] Record that the new skill reference file is pending maintainer propagation and that no propagation command was run. (AC1)
