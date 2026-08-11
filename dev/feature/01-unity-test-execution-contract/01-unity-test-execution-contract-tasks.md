# Tasks: Unity Test Execution Contract

## Stage 1: Contract Guards

- [x] Choose a repository-consistent filename for `tests/[PROPOSED - name TBD: Unity skill contract guards]`, record the final name in the implementation notes, and keep the module focused on the `unity-development` Test Execution contract.
- [x] Add a non-vacuous parser that extracts only `## Test Execution`, normalizes irrelevant Markdown whitespace, and fails clearly if the section or required two-row platform table is missing. (AC12)
- [x] Add a structural guard proving every agent-driven test path requires `-batchmode`, the obsolete optional wording is absent from `source_of_truth/`, EditMode includes `-nographics`, and PlayMode/visual capture explicitly excludes `-nographics`. (AC1, AC2)
- [x] Add a command-relationship guard proving `-quit` is never paired with `-runTests`, while the existing affected-suite `-testFilter` semantics remain present and unchanged. (AC3)
- [x] Add a guard proving the section points to `source_of_truth/agents/04g-unity-visual-verification.agent.md` for editor discovery, does not add a second discovery algorithm, and does not assume a bare `Unity` executable is on `PATH`. (AC4)
- [x] Add a guard proving `-testResults` resolves to an absolute main-checkout path under `dev/test-results/`, the worktree is execution-only, and results are never read from the shadow copy. (AC5)
- [x] Add a guard proving commit-before-test is an explicit worktree precondition and explains that the normal per-feature commit usually satisfies it. (AC6)
- [x] Add ordered ladder guards for stale-registration pruning, detached fixed sibling creation/reuse, committed-SHA refresh, `Library/` retention, first-use path/disk/import announcements, and headless execution while the main Editor remains usable. (AC7)
- [x] Add lifecycle guards proving indefinite persistence, one worktree per project, per-run worktree creation as an anti-pattern, and an explicit manual-only teardown command. (AC8)
- [x] Add fallback guards proving licensing/lock failure transitions once to a request to close the Editor followed by an agent-run headless main-checkout test; reject any delegation of the run to the user. (AC9)
- [x] Add terminal-state guards forbidding GUI launch and silent refusal, distinguishing user decline from unattended silence, and requiring the exact unattended status `not-executed: editor open, user unavailable`. (AC10)
- [x] Build a mutation checklist covering every protected AC1–AC10 obligation; delete the mechanism and negate the load-bearing rule for each, confirm the focused guard fails with the intended obligation named, restore the source, and confirm green. (AC12)

## Stage 2: Test Execution Rule Rewrite

- [x] Rewrite only `source_of_truth/skills/unity-development/SKILL.md`'s `## Test Execution` section so `-batchmode` is mandatory for every agent-driven Unity test run and no optional claim remains under `source_of_truth/`. (AC1)
- [x] Add the required two-row platform table: EditMode uses `-batchmode -nographics`; PlayMode and visual capture use `-batchmode` with graphics enabled and explicitly exclude `-nographics`. (AC2)
- [x] Preserve the existing affected-suite `-testFilter` contract verbatim in meaning and preserve the prohibition on combining `-quit` with `-runTests`. (AC3)
- [x] Replace the bare executable assumption with a concise pointer to the verified editor-discovery procedure in `source_of_truth/agents/04g-unity-visual-verification.agent.md`; do not duplicate its environment/local-file/Hub search sequence. (AC4)
- [x] Require `-testResults` to receive an absolute path under the main checkout's `dev/test-results/`, state that the shadow worktree is execution-only, and forbid reading results from its copy. (AC5)
- [x] State commit-before-test as a hard precondition for shadow-worktree execution and explain tersely that the normal per-feature commit usually supplies the tested SHA. (AC6)
- [x] Document ladder rung 1 as one attempt: prune stale registrations; validate the fixed sibling path; create or reuse one detached `<project-dir>-agent-tests/` worktree; refresh it to the committed SHA without deleting gitignored `Library/`; announce path, approximate disk cost, and multi-minute cold import; then run headless while the main Editor remains usable. (AC7)
- [x] State that the worktree persists indefinitely, that per-run creation is an anti-pattern, and that teardown is a validated manual command which the agent never runs automatically. (AC8)
- [x] Document ladder rung 2 as one bounded licensing/lock fallback: ask the user to close the Editor, then have the agent run headless in the main checkout; never hand test execution to the user. (AC9)
- [x] Document ladder rung 3 with no GUI and no silent refusal: a decline reports `not-executed`, and unattended non-response reports exactly `not-executed: editor open, user unavailable`. (AC10)
- [x] Preserve the authoritative results-XML parser contract, including zero discovered tests as `not-executed` and exit code zero as insufficient evidence. (AC3, AC10)
- [x] Run the focused proposed guard module and confirm all AC1–AC10 contract checks are green after the rewrite. (AC1–AC10, AC12)

## Stage 3: Reference-Project Verification

- [x] Confirm `/Users/jennywadkins/github_repos/the-movies` is clean, still targets Unity `6000.3.13f1`, and has a committed SHA suitable for detached execution; stop rather than attempting to mirror dirty uncommitted changes. (AC6, AC11)
- [x] Resolve the Unity editor executable through the existing Visual Verifier discovery procedure and keep any machine-specific resolved path out of tracked files. (AC4, AC11)
- [ ] With the reference project's main Editor open, prune stale worktree registrations, validate ownership of `/Users/jennywadkins/github_repos/the-movies-agent-tests/`, then create or reuse it as a detached persistent worktree refreshed to the committed SHA without deleting its `Library/`. (AC7, AC8, AC11) — blocked in this pass because the main Editor was not open; the worktree was otherwise created and refreshed successfully.
- [x] Run the documented EditMode invocation in the shadow worktree with `-batchmode -nographics`, no `-quit`, and `-testResults` pointing to an absolute path under the main checkout's `dev/test-results/`. (AC2, AC3, AC5, AC11)
- [x] Record whether Unity Personal permits the concurrent process, whether any GUI appeared, whether the main Editor remained usable, the Unity log location, the absolute results path, and XML test counts; if licensing or locking blocks rung 1, record the transition honestly rather than calling the tests failed. (AC11)
- [x] If rung 1 encounters the expected licensing/lock condition, exercise rung 2 once after the user closes the Editor and let the agent run the same headless suite in the main checkout; if the user declines or is unavailable, record the applicable required `not-executed` status without opening a GUI or delegating the run. (AC9–AC11)
- [x] Verify the results XML reports at least one discovered test before classifying the run as executed; treat missing or zero-test XML as `not-executed` regardless of process exit code. (AC11)

## Stage 4: Regression Verification

- [x] Re-run every deletion and semantic-negation mutation from the Stage 1 checklist, verify each focused guard turns red for the intended reason, restore all protected content, and rerun the focused module green. (AC12)
- [x] Run `uv run pytest tests/[PROPOSED - name TBD: Unity skill contract guards]` using the final selected filename and record the exact pass/fail counts. (AC1–AC10, AC12)
- [x] Run `uv run pytest tests/test_agent_corpus_invariants.py tests/test_propagate_master_assets.py` and distinguish pre-existing failures from any feature-caused regression; do not edit generic corpus tests to pin prose. (AC12)
- [x] Run `uv run pytest tests/` and compare with the captured baseline of 141 passed and 2 unrelated failures, naming any changed outcome rather than relying on aggregate counts alone. (AC12)
- [x] Confirm `source_of_truth/skills/unity-development/SKILL.md` and the final focused guard module are the only authored feature changes; verify no worktree in this repository, consumer agent, serialized-asset section, `ports/`, or `.github/` file changed.
- [x] Report generated-output sync failures as propagation pending and stop without running `scripts/propagate_master_assets.py`.
