# Feature Tasks: Unity Consumer Alignment

## Stage 1: Consumer Contract Guards

- [x] Confirm the authored Test Execution and Serialized Assets contracts from Features `01-unity-test-execution-contract` and `02-headless-asset-import` are finalized, then read them before encoding consumer expectations; their external runtime evidence remains independently tracked.
- [x] Create `tests/test_unity_consumer_contract.py` and derive the three required source consumer paths with a non-vacuity assertion.
- [x] Add a scoped Phase Execute Step 2.5 scenario guard proving Unity invocation mechanics delegate to the canonical skill, result artifacts use the absolute main-checkout path, and the user is not asked to execute the suite. (AC1)
- [x] Add Phase Execute branch guards proving `executed-green`, `executed-failing`, and `not-executed` remain distinct; `not-executed` cannot become green; `all-approved: no` is preserved; and the direct-supervisor-attestation exception remains intact. (AC1–AC2)
- [x] Add a scoped Visual Verifier Steps 1–2 guard proving editor discovery order and saved local-path behavior remain present while PlayMode capture uses `-batchmode`, graphics enabled, and no `-quit` with `-runTests`. (AC3)
- [x] Add a scoped Unity Reviewer Phase 2 guard that distinguishes test execution from serialized-asset import: tests delegate to Test Execution and exclude `-quit` with `-runTests`; asset import delegates to Serialized Assets and permits the documented headless import shape. (AC4)
- [x] Add guards proving consumers reference canonical contracts without duplicating the full worktree ladder or creating another editor-discovery algorithm. (AC5)
- [x] Demonstrate each consumer guard turns red when its protected reference, token relationship, fallback, or preserved escape hatch is removed or negated; restore the fixture/source after every mutation. (AC6)

## Stage 2: Phase Execute Alignment

- [x] Update `source_of_truth/agents/04-phase-execute.agent.md` Step 2.5 to consume the finalized canonical Test Execution ladder and absolute main-checkout results path without copying the ladder. (AC1, AC5)
- [x] Replace the Unity user-run handoff with the canonical decline/unattended fallback while keeping the orchestrator responsible for execution whenever evidence can be obtained. (AC1–AC2)
- [x] Preserve the direct-supervisor-attestation exception, supervisor-directed skip behavior, one-retry limit, results-artifact recording, and `all-approved: no` outcome for every final non-green status. (AC1–AC2)
- [x] Verify the generic non-Unity `not-executed` evidence gate remains valid and does not silently proceed as green. (AC2)
- [x] Run the focused Phase Execute consumer scenarios and confirm the targeted mutation cases are green after restoration. (AC1–AC2, AC6)

## Stage 3: Visual Verifier and Unity Reviewer Alignment

- [x] Update `source_of_truth/agents/04g-unity-visual-verification.agent.md` to use the shared execution ladder's project target while retaining the existing editor-discovery order and saved machine-local editor path. (AC3, AC5)
- [x] Keep Visual Verifier PlayMode capture on `-batchmode` with graphics enabled; explicitly prevent `-nographics` and `-quit` from pairing with the `-runTests` capture invocation. (AC3)
- [x] Preserve Visual Verifier evidence checks for passed test results, expected images, manifest presence, and honest `Fail`/`Unverified` reporting. (AC3)
- [x] Update `source_of_truth/agents/04h-unity-reviewer.agent.md` to delegate test execution to the finalized Test Execution section and serialized-asset validation to the finalized Serialized Assets section. (AC4–AC5)
- [x] Preserve Unity Reviewer's static serialized-asset integrity audit and its warning that a clean import does not prove reference resolution or rendering. (AC4)
- [x] Confirm neither specialist contains a copied worktree procedure, a second editor-discovery algorithm, a blanket `-nographics` rule, or broadened batchmode permission. (AC3–AC5)
- [x] Run the focused Visual Verifier and Unity Reviewer consumer scenarios and confirm all targeted mutation cases are green after restoration. (AC3–AC6)

## Stage 4: Regression Verification

- [x] Run `uv run pytest tests/test_unity_consumer_contract.py` and record the exact pass/fail result. (AC1–AC6)
- [x] Run `uv run pytest tests/test_agent_corpus_invariants.py` and verify frontmatter, rosters, `applyTo`, and duplicate-block invariants remain intact. (AC5–AC6)
- [x] Run `uv run pytest tests/test_propagate_master_assets.py`; identify the pre-existing wildcard `applyTo` failure separately and report generated-port sync failures as propagation pending rather than editing generated output. (AC5–AC6)
- [x] Run the policy-safe full suite with `test_committed_tree_is_at_a_propagation_fixed_point` deselected and compare against the captured 141-pass/2-failure baseline, reporting both known unrelated failure signatures separately from any new regression. (AC1–AC6)
- [x] Inspect the final diff to confirm only the three source agent files and the focused guard module changed, no generated port was edited, no propagation command ran, and all frontmatter/personality-canary content is preserved. (AC1–AC6)
- [x] Record that Unity runtime command verification was not required for this feature and remains owned by Features 01 and 02. (AC3–AC4)
