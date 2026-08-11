# Feature Context: Headless Asset Import

## Key Files

### Files to Change

| File / Module | Role | Change Type |
|---|---|---|
| `source_of_truth/skills/unity-development/SKILL.md` | Canonical Unity guidance; extend `## Serialized Assets: Generate via Unity, Never Hand-Author`, correct both invalid EditMode-path references, and preserve the Feature 01 test-execution contract. | Modify |
| `tests/[PROPOSED - name TBD: Unity skill contract guards]` | Shared structural guard module expected to be created and named by `01-unity-test-execution-contract`; add import-command, contradiction-sweep, path-sweep, non-vacuity, and mutation-proof coverage. | Modify after Feature 01 creates it; otherwise Create with final idiomatic name recorded by the implementer |

### Read-Only References and Verification Targets

| File / Module | Role | Change Type |
|---|---|---|
| `dev/feature/01-unity-test-execution-contract/01-unity-test-execution-contract-plan.md` and its completed companion files | Upstream ownership and finalized `## Test Execution` contract; Feature 02 must not undo its flags, ladder, worktree, result-path, or editor-discovery rules. | Read-only reference |
| `dev/feature/03-unity-consumer-alignment/03-unity-consumer-alignment-plan.md` | Downstream consumer of the finalized headless-import contract. | Read-only reference |
| `docs/phases/PHASE_01/PHASE_01_SUMMARY.md` | Phase requirements, success criteria, risks, and feature boundary for Deliverable 3. | Read-only reference |
| `docs/phases/PHASE_01/PHASE_01_DISCOVERY_CONTEXT.md` | Verified reference-project version, test layout, and manual-QA constraints. | Read-only reference |
| `docs/phases/DISCOVERY_CONTEXT.md` | Project-level diagnosis that `.meta` generation does not inherently require a GUI. | Read-only reference |
| `docs/AUTHORING.md` | Source-authoring, brevity, generated-output, and validation conventions. | Read-only reference |
| `source_of_truth/agents/04g-unity-visual-verification.agent.md` | Existing Unity editor-discovery procedure owned outside this feature; do not duplicate or edit it. | Read-only reference |
| `tests/test_agent_corpus_invariants.py` | Existing structural corpus tests; its contract excludes guards keyed to agent/skill prose, so do not place this feature's content guards here. | Read-only reference |
| `/Users/jennywadkins/github_repos/the-movies/ProjectSettings/ProjectVersion.txt` | Confirms the manual-QA target uses Unity `6000.3.13f1`. | Read-only reference |
| `/Users/jennywadkins/github_repos/the-movies/Assets/Tests/Editor` | Verified actual EditMode test convention in the reference project. | Read-only reference |
| `/Users/jennywadkins/github_repos/the-movies/Assets/Tests/PlayMode` | Verified PlayMode path whose guidance must remain unchanged. | Read-only reference |

## Discovery Delta

| Finding | Impact | Action |
|---|---|---|
| Both planned invalid-path occurrences exist in `source_of_truth/skills/unity-development/SKILL.md`: the assembly example at current line 26 and Refactor/Rewire inventory at current line 164. The serialized-assets section begins at current line 257. | Confirms the planned edit surface and that no additional source file currently needs the path correction. | Scope guards by derived section boundaries or source-wide enumeration, not fragile line numbers. |
| The shared Unity guard module does not yet exist, and no existing test class or file name matching the plan was found. | Feature 02 cannot treat a concrete guard filename or test class as established. | Retain `tests/[PROPOSED - name TBD: Unity skill contract guards]` everywhere until Feature 01 creates and names it; use scenario descriptions rather than invented test method/class names. |
| The current `source_of_truth/` scan found no claim that a human-opened or GUI-opened Editor is required to generate `.meta` files. The existing references to the Editor serializer and Editor API describe authority, not GUI operation. | AC3 is preventive as well as corrective; a negative assertion alone could become vacuous. | Enumerate tracked source files from disk, assert the enumeration is non-empty, and test contradiction shapes without banning legitimate “Editor API” terminology. |
| `/Users/jennywadkins/github_repos/the-movies` exists, is clean at discovery time, reports Unity `6000.3.13f1`, and contains `Assets/Tests/Editor`, `Assets/Tests/PlayMode`, and phase-scoped Editor test directories. | Confirms the plan's reference-project facts and path correction. The external phase-scoped suites are not implementation targets in this corpus feature. | Preserve the external project as manual-QA-only; do not modify its tests or create a phase-consolidated test file there. |
| No Unity executable was found under the standard macOS Hub location `/Applications/Unity/Hub/Editor/*/Unity.app/Contents/MacOS/Unity`. | AC5 cannot be assumed executable from the repository expansion environment, even though the project version is verified. | During Stage 3, use the finalized editor-discovery procedure; if no executable or safe controlled mutation is available, record AC5 as unverified rather than claiming success. |
| The full repository baseline on 2026-08-10 is `141 passed, 2 failed`, not the plan's earlier `50 passed, 1 failed` snapshot. Failures are `tests/test_pr_review_orchestrator.py::test_agent_name_does_not_collide_with_prose_in_any_source_asset` and `tests/test_propagate_master_assets.py::InstructionApplyToTests::test_every_enumerated_applyto_target_exists`. | Both failures pre-exist this feature's implementation and must not be attributed to it. The second is the wildcard `applyTo` failure named by the plan; the first is additional baseline drift. | Capture focused guard results separately, compare repository regressions against this two-failure baseline, and report propagation-pending failures without running propagation. |
| No repository-local phase-scoped Python test directory or consolidated phase test file pattern was found under `tests/`. | No omitted current-phase consolidated test file is required for this feature. | Keep the structural guards in the shared Feature 01 module rather than inventing a phase test location. |

## Architectural Decisions

- Extend the existing `## Serialized Assets: Generate via Unity, Never Hand-Author` section. The plain asset-database import command is a distinct sanctioned operation beside the existing `-batchmode -executeMethod <Type>.<Method> -quit` asset-construction procedure.
- Preserve Unity as the sole author of serialized assets and GUIDs. Headless execution removes the GUI requirement; it does not authorize hand-authored YAML or fabricated `.meta` content.
- Use `source_of_truth/` as both the authoring surface and contradiction/path sweep boundary. Generated ports are deliberately excluded until maintainer-run propagation.
- Correct the verified reference-project convention to `Assets/Tests/Editor` while keeping the guidance discovery-friendly rather than claiming every Unity repository uses that layout. Preserve `Assets/Tests/PlayMode` unchanged.
- Derive sweep inputs from disk and assert non-vacuity. Normalize whitespace and inspect scoped command-token relationships instead of pinning whole prose sentences.
- Reuse the shared guard module established by Feature 01. Do not add prose-sensitive assertions to `tests/test_agent_corpus_invariants.py` and do not invent a second guard module without first resolving the upstream artifact.
- Add no new normal-path corpus logging. `-logFile -`, command outcome, and reference-project cleanliness are the manual-QA evidence.

## Constraints

- Feature 01 must complete first because both features modify `source_of_truth/skills/unity-development/SKILL.md` and the same proposed guard module.
- Do not alter Feature 01's Test Execution ladder, platform flags, `-testFilter` behavior, editor discovery, or result-path contract. In particular, `-quit` is valid for import but must remain forbidden with `-runTests`.
- Do not update consumer agents; `03-unity-consumer-alignment` owns them.
- Do not change the reference project's test assertions, test directory names, or tracked content.
- Do not hand-author or commit a `.meta` file to manufacture evidence.
- Any controlled external `.meta` mutation must target one validated file, be recoverable, and leave `git -C /Users/jennywadkins/github_repos/the-movies status --short` clean.
- Do not expose Unity license information or persist machine-specific executable paths.
- `source_of_truth/` definitions are runtime context and must remain terse: state the rule once without duplicating explanations or commands.
- Never edit `ports/` or `.github/`, and never run `scripts/propagate_master_assets.py`; maintainer propagation remains pending after source edits.

## Scope Boundaries

- Change only the Serialized Assets guidance and the two verified EditMode-path references in the Unity skill, plus the shared structural guard module.
- Preserve all unrelated Unity implementation, rendering, UI Toolkit, test-authenticity, and visual-verification guidance.
- Preserve `Assets/Tests/PlayMode` guidance exactly in meaning.
- Treat “Editor API,” “Unity Editor serializer,” and Unity's serialization authority as valid terminology; only claims requiring human or GUI opening are contradictory.
- Keep the external `the-movies` repository a verification target, not an authoring surface.
- Do not create helpers, schemas, config keys, serialized assets, CI workflows, runbooks, or consumer-agent changes in this feature.
- Generated outputs may remain out of sync until the maintainer propagates; do not repair them manually.

## Relationships to Sibling Plans

- `01-unity-test-execution-contract` is a hard prerequisite and owns the adjacent Test Execution rewrite plus initial creation/naming of the shared Unity skill contract guards. Feature 02 must rebase its assumptions on the completed Feature 01 artifacts before editing.
- `03-unity-consumer-alignment` depends on the finalized import contract from this feature. Feature 02 provides the canonical rule but does not edit consumers.
- `04-unity-test-reference-assets` is parallel-safe at the phase level because it creates separate reference assets, but Feature 02 does not own those files.

## Suggested Implementation Order

1. Complete and verify `01-unity-test-execution-contract`; resolve the actual shared guard filename and current skill section boundaries.
2. Add red structural guards for AC1–AC4 and AC6, including non-vacuity and targeted deletion/negation proofs.
3. Extend the Serialized Assets section and correct both invalid EditMode path references without changing Feature 01's Test Execution section.
4. Run the focused guards and confirm each protected mechanism has demonstrated red-to-green behavior.
5. Perform the safe external headless-import check only if the editor executable and a recoverable single-file `.meta` scenario are available; otherwise record the result as unverified.
6. Confirm the reference project is clean, then run the repository regression suite and separate new failures from the recorded baseline and propagation-pending state.

## Environment State

| Property | Value |
|---|---|
| Tech Stack | Markdown agent/skill corpus with Python 3.12.6 maintenance and pytest tests; external manual-QA target is Unity 6000.3.13f1 |
| Test Runner | `uv run pytest tests/` |
| Test Baseline | 141 passed, 2 failed — captured 2026-08-10. Existing failures: `tests/test_pr_review_orchestrator.py::test_agent_name_does_not_collide_with_prose_in_any_source_asset` and `tests/test_propagate_master_assets.py::InstructionApplyToTests::test_every_enumerated_applyto_target_exists` |
| Lint | Not configured |
| Format | Not configured |

## Relevant Learnings

None applicable. No `docs/learnings/*.md` files exist in this repository.
