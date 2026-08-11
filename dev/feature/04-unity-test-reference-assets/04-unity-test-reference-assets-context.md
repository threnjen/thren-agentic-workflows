# Feature Context: Unity Test Reference Assets

## Key Files

### Files to Change

| File / Module | Role | Change Type |
|---------------|------|-------------|
| `source_of_truth/skills/unity-development/references/[PROPOSED - name TBD: GameCI workflow template].yml` | New inert, copyable GitHub Actions workflow showing separate EditMode and PlayMode GameCI execution, caller-owned secret references, and artifact publication. No corresponding file or `references/` directory exists yet. | Create |
| `docs/unity/[PROPOSED - name TBD: local Unity test runbook].md` | New human-facing local execution/import procedure, fallback ladder, evidence locations, and manual teardown guidance. No corresponding file or `docs/unity/` directory exists yet. | Create |
| `tests/[PROPOSED - name TBD: Unity reference asset guards]` | New focused structural guard module for workflow placement/shape/safety and runbook format/contract fidelity. No corresponding file or test class exists yet. | Create |

### Read-Only References

| File / Module | Role | Change Type |
|---------------|------|-------------|
| `source_of_truth/skills/unity-development/SKILL.md` | Canonical Test Execution and Serialized Assets contracts finalized by Features 01 and 02; the runbook must consume these rules without forking them. | Read-only reference |
| `source_of_truth/agents/04g-unity-visual-verification.agent.md` | Existing Unity editor-discovery procedure that the runbook must reuse rather than duplicate. | Read-only reference |
| `scripts/propagate_master_assets.py` — `propagate_skills_once` | Verified recursive propagation mechanism for skill auxiliary files; copies nested reference files to Claude, OpenCode, and Codex skill bundles. | Read-only reference |
| `tests/test_propagate_master_assets.py` | Existing propagation regression suite and isolated-temp-repository testing patterns. | Read-only reference |
| `docs/AUTHORING.md` | Source-only authoring, propagation-pending, brevity, and generated-output conventions. | Read-only reference |
| `docs/phases/PHASE_01/PHASE_01_SUMMARY.md` | Phase scope, reference-asset deliverable, runbook requirements, risks, and success criteria. | Read-only reference |
| `docs/phases/PHASE_01/PHASE_01_DISCOVERY_CONTEXT.md` | Maintainer decisions and verified reference-project facts, including Unity `6000.3.13f1`, the 602 MB project size, and worktree lifecycle. | Read-only reference |
| `dev/feature/01-unity-test-execution-contract/01-unity-test-execution-contract-plan.md` and companions | Upstream public test-execution contract, worktree ladder, result-path rules, and manual verification ownership. | Read-only reference |
| `dev/feature/02-headless-asset-import/02-headless-asset-import-plan.md` and companions | Upstream public headless import contract and corrected EditMode path convention. | Read-only reference |
| `dev/feature/03-unity-consumer-alignment/03-unity-consumer-alignment-plan.md` | Parallel-safe sibling consuming the same finalized contracts through disjoint files. | Read-only reference |
| GameCI official Test Runner documentation (`https://game.ci/docs/github/test-runner/`) | Current external authority for the GameCI action, test modes, licensing inputs, artifact output, and workflow examples; recheck during implementation because this surface is versioned. | Read-only reference |

## Discovery Delta

| Finding | Impact | Action |
|---------|--------|--------|
| None of the three proposed deliverables exists. The `unity-development/references/` and `docs/unity/` directories are also absent, and no existing test class covers this feature. | The plan correctly treats all deliverables as new, but no concrete filename or test class is established. | Retain `[PROPOSED - name TBD]` in planning artifacts. The implementer chooses terse idiomatic filenames and scenario names and records them in the implementation notes. |
| The checked-in Unity skill still contains the pre-phase execution/import rules because Features 01 and 02 have not yet been implemented. | Authoring now would copy a stale contract into the runbook and violate the declared dependency. | Do not start guard expectations or reference-asset authoring until Features 01 and 02 are complete; re-read their finalized skill sections first. Decomposer attention required if Wave 3 scheduling does not enforce this gate. |
| Current official GameCI documentation identifies `game-ci/unity-test-runner@v4`, `testMode` values `EditMode` and `PlayMode`, the `artifactsPath` step output, Personal-license environment secret references, `actions/checkout@v4`, and `actions/upload-artifact@v4`. | The plan's general GameCI surface is viable and can be made explicit without inventing names. These versions and keys remain temporally unstable. | Reverify the official page during Stage 1, record the retrieval source/date in implementation evidence, and encode only then-current official fields. |
| The Python environment has no YAML library (`yaml` is not importable), and the repository has no YAML validation configuration. A token/indentation check cannot honestly prove full YAML parseability; generic YAML 1.1 parsers can also misinterpret GitHub's `on` key. | AC6's “parseable workflow shape” is underspecified relative to the available tooling. Adding an unplanned dependency or claiming a structural scan is a parser would be incorrect. | Choose and document a GitHub-Actions-compatible validation method during Stage 1, or narrow the automated claim to structural shape and keep full parse validation as explicit review evidence. Decomposer attention required. |
| `propagate_skills_once` recursively enumerates each source skill directory with `rglob("*")` and preserves relative paths in all three skill output roots. | The planned `references/` placement will propagate without a script change. | Keep the propagation script read-only; use an isolated focused assertion only if direct regression evidence for the new nested asset is needed. Never run propagation in this repository. |
| The full repository baseline on 2026-08-10 is 143 collected, 141 passed, and 2 failed. Failures are `tests/test_pr_review_orchestrator.py::test_agent_name_does_not_collide_with_prose_in_any_source_asset` and `tests/test_propagate_master_assets.py::InstructionApplyToTests::test_every_enumerated_applyto_target_exists`. | Verification must not attribute either current failure to this feature. | Resolved: the plan now records this baseline. Report focused results separately and compare the full suite with these two pre-existing failures. |
| No repository-local phase-scoped test directory or consolidated current-phase Python test module exists. Tests use flat `tests/test_*.py` modules. | The plan has not omitted a phase consolidation target. | Create one focused flat module using the final selected name; do not invent a phase test directory. |
| There is no existing human-facing Unity runbook under `docs/` to copy mechanically. Repository instructions nevertheless define the required form: TL;DR first, numbered one-action steps, exact commands, correct-result descriptions, and warnings adjacent to hazards. | The implementer must apply the repository-wide human-facing runbook contract directly. | Make the format mechanically testable without pinning arbitrary prose, then perform a human dry-run. |

## Architectural Decisions

- Keep the GameCI workflow inside the canonical `unity-development` skill's `references/` directory so normal recursive skill propagation carries it as an inert reference. Never install it in `.github/workflows/` or a Unity repository.
- Keep the local runbook under `docs/unity/` because it is human-facing and must not be copied into every harness skill directory.
- Treat the finalized Unity skill as authoritative for local execution and import. The runbook provides the commands and operator sequence needed to succeed, but does not duplicate the full machine-facing policy.
- Keep the workflow minimal and adaptable: checkout, explicit EditMode and PlayMode test execution, and always-run artifact upload. Avoid a matrix, caching, builds, deployment, and unrelated quality gates.
- Reference caller-supplied GitHub secrets only. Do not include license values, machine paths, or repository-specific project paths.
- Make EditMode and PlayMode intent structurally distinct. The local EditMode command includes `-batchmode -nographics`; PlayMode/visual execution includes `-batchmode` with graphics enabled and excludes `-nographics`.
- Keep worktree teardown manual and adjacent to explicit target validation. Never automate deletion of the persistent `<project-dir>-agent-tests/` worktree.
- Build guards around file placement, parsed or explicitly structural workflow relationships, scoped runbook sections, command-token relationships, and forbidden states. Normalize irrelevant whitespace, assert non-vacuity, and prove each obligation red through deletion or semantic negation.
- Add no runtime dependency, helper API, config schema, or normal-path logging. Workflow artifacts and local XML/log paths provide the required observability.

## Constraints

- Features `01-unity-test-execution-contract` and `02-headless-asset-import` must complete before this feature consumes their final text.
- Author only the new workflow under `source_of_truth/`, the new runbook under `docs/unity/`, and the focused guard module under `tests/`.
- Never edit generated `ports/` or `.github/` content, and never run `scripts/propagate_master_assets.py`; propagation remains a maintainer action.
- Keep every unverified new filename and test class marked `[PROPOSED - name TBD]` until implementation selects it. Use scenario descriptions rather than invented exact test method names.
- Reverify GameCI and GitHub Action versions, inputs, outputs, secret conventions, and required permissions from current official documentation during implementation.
- Do not add a runtime dependency solely to parse the workflow. Any validator must be justified as test/development tooling and must understand GitHub Actions YAML semantics.
- The workflow must remain inert, copyable, minimally permissioned, and free of literal credentials or license data.
- The runbook TL;DR is at most five lines. Every numbered step performs one action, gives an exact command, and states the correct result.
- The runbook must explain the disk impact in plain words before giving the approximate 600 MB reference-project figure and multi-minute first-import expectation.
- Commands must quote paths safely. Results go to an absolute path under the main checkout's `dev/test-results/`, never the shadow worktree.
- Teardown must validate the explicit fixed sibling target beside the destructive command; do not use a broad variable, glob, or recursive deletion.
- Structural content guards must be demonstrated red for the intended reason through deletion or semantic negation, restored, and rerun green.

## Scope Boundaries

- Do not modify the canonical Unity skill; Features 01 and 02 own it.
- Do not modify Phase Execute, Visual Verifier, Unity Reviewer, or other consumer agents; Feature 03 owns them.
- Do not install the workflow under `.github/workflows/` here or in `/Users/jennywadkins/github_repos/the-movies`.
- Do not configure license secrets, provision runners, choose an organizational CI policy, add caching, build players, or deploy artifacts.
- Do not create, refresh, remove, or otherwise alter an actual worktree while authoring these reference files.
- Do not automatically tear down the persistent worktree or imply that `Library/` should be deleted during refresh.
- Do not ask the user to execute Unity tests and do not introduce a GUI fallback.
- Do not modify Features 01–03 planning or implementation files.
- Do not treat the runbook as a second canonical skill or reproduce unrelated Unity-development guidance.

## Relationships to Sibling Plans

- `01-unity-test-execution-contract` is a hard prerequisite. It defines mandatory headless test flags, editor discovery reuse, absolute main-checkout results, the persistent worktree lifecycle, and the three-rung fallback.
- `02-headless-asset-import` is a hard prerequisite after Feature 01. It defines the sanctioned GUI-free import command and preserves Unity as the serialized-asset authority.
- `03-unity-consumer-alignment` consumes the same two contracts and may execute in parallel with this feature in Wave 3 because it modifies disjoint agent files and a separate focused test module.
- Feature 04 adds no runtime API and requires no integration/bootstrap feature. Its dependency is exact documentation fidelity to the two upstream contracts.

## Suggested Implementation Order

1. Complete and verify `01-unity-test-execution-contract`.
2. Complete and verify `02-headless-asset-import` against Feature 01's finalized skill.
3. In Wave 3, execute this feature in parallel with `03-unity-consumer-alignment`.
4. Within this feature, verify current GameCI contracts and validation tooling, choose final filenames, add red guards, author the two reference assets, then run focused and repository verification.

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Markdown/YAML asset corpus with Python 3.12.6 standard-library tooling and pytest 9.1.1; external contract targets Unity 6 and the reference project uses Unity `6000.3.13f1`. |
| Test Runner | `uv run pytest tests/` |
| Test Baseline | 143 collected: 141 passed, 2 failed — captured 2026-08-10. Existing failures: `test_agent_name_does_not_collide_with_prose_in_any_source_asset` and `InstructionApplyToTests::test_every_enumerated_applyto_target_exists`. |
| Lint | Not configured |
| Format | Not configured |

## Relevant Learnings

None applicable. No `docs/learnings/*.md` files exist in this repository. For the planned content guards, apply the loaded guard-integrity contract: derive enumerations where possible, assert non-vacuity, normalize irrelevant whitespace, and prove deletion and semantic-negation mutations fail for the intended obligation.
