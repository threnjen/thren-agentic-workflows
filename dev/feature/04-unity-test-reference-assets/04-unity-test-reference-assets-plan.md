# Feature Plan: Unity Test Reference Assets

## Execution Metadata

- **Wave:** 3
- **Parallel safe:** yes
- **Depends on:** `01-unity-test-execution-contract`, `02-headless-asset-import`
- **Key files modified:** `source_of_truth/skills/unity-development/references/[PROPOSED - name TBD: GameCI workflow template].yml`, `docs/unity/[PROPOSED - name TBD: local Unity test runbook].md`, `tests/[PROPOSED - name TBD: Unity reference asset guards]`
- **Sequential reason:** n/a

## A. Requirements & Traceability

### Acceptance Criteria

1. **AC1:** A copyable, inert GameCI GitHub Actions workflow template exists under `source_of_truth/skills/unity-development/references/` and is not installed into any Unity repository.
2. **AC2:** The workflow is internally complete for a maintainer to adapt: it checks out the project, runs Unity tests through GameCI with explicit EditMode/PlayMode intent, references a caller-supplied Unity license secret convention without containing secrets, and publishes test artifacts; exact action versions and keys are verified from current GameCI documentation during implementation.
3. **AC3:** A human-facing local Unity test runbook exists under `docs/unity/`, opens with a TL;DR of five lines or fewer, then uses numbered one-action steps with exact commands and correct-result descriptions.
4. **AC4:** The runbook matches the finalized execution and import contracts: commit first; prune; create/reuse the detached sibling `<project-dir>-agent-tests/`; announce roughly 600 MB and a multi-minute first import for the reference project; refresh without deleting `Library/`; resolve the editor through the existing procedure; write results to an absolute main-checkout path; use the three-rung fallback; and never launch a GUI or ask the user to run tests.
5. **AC5:** The runbook documents manual teardown and makes clear that teardown is never automatic, CI installation is out of scope, and Unity Personal concurrent-process behavior must be confirmed on the target machine.
6. **AC6:** Structural guards verify placement, workflow shape, secret absence, runbook format, and required contract relationships; a GitHub-Actions-compatible validator proves parseability when available, otherwise parseability remains explicit review evidence rather than a false automated claim. Each content guard is proven red through deletion or negation and includes non-vacuity checks.

### Non-Goals

- Do not install the workflow under `.github/workflows/` here or in `/Users/jennywadkins/github_repos/the-movies`.
- Do not configure Unity license secrets, provision runners, or choose CI adoption policy.
- Do not duplicate the canonical skill in full; the runbook is an operator procedure, not a second machine-facing policy.
- Do not modify Features 01–03 files.
- Do not run propagation; the bundled workflow remains pending propagation with the skill.

### Traceability

| Acceptance Criteria | Code Areas/Modules | Test / Evidence Category |
|---|---|---|
| AC1–AC2 | `source_of_truth/skills/unity-development/references/[PROPOSED - name TBD: GameCI workflow template].yml` | Must-have automated test |
| AC3–AC5 | `docs/unity/[PROPOSED - name TBD: local Unity test runbook].md` | Must-have automated test; manual QA check |
| AC6 | `tests/[PROPOSED - name TBD: Unity reference asset guards]` | Must-have automated test |

## B. Correctness & Edge Cases

- GameCI inputs and action versions are temporally unstable. Implementation must verify current official documentation before finalizing the template.
- The template must remain inert and copyable. Paths and project locations need placeholders where repository-specific values vary.
- License material must be referenced as a secret input, never embedded. Guards must reject credential-like literal values.
- The runbook must distinguish EditMode `-nographics` from PlayMode/visual graphics-on execution.
- Teardown commands are destructive. The runbook must place target validation beside the command and use the explicit fixed worktree path, never a broad variable or recursive deletion.
- The runbook should explain the observed reference-project size in plain words first, then give the approximate 600 MB figure.

## C. Consistency & Architecture Fit

- Skill auxiliary files are verified to propagate recursively with the skill bundle; the workflow belongs under `source_of_truth/skills/unity-development/references/`.
- Human-facing docs are not propagated, so the local runbook belongs under `docs/unity/` and follows the repository's runbook style.
- Consume the canonical procedures from Features 01 and 02. If wording differs, the skill is authoritative and these assets must be updated before completion.
- No runtime API connects these files. The dependency is documentation fidelity, and no integration/bootstrap feature is warranted.
- Relationship: depends on Features 01 and 02; parallel-safe with `03-unity-consumer-alignment` due to disjoint file scope.

### Unverified Assumptions

- Current GameCI action names, versions, and required Unity Personal licensing inputs must be verified during implementation through current official documentation.
- The final asset filenames are intentionally `[PROPOSED - name TBD]`; the implementer selects terse repository-consistent names and records them in the implementation notes.

## D. Clean Design & Maintainability

- Keep the workflow minimal: checkout, test execution, artifacts. Avoid matrices, caching, deployment, and unrelated quality gates unless official GameCI requirements make them necessary.
- Keep the runbook action-first: TL;DR, numbered steps, exact command, correct result, warning at the destructive step.
- Reference canonical machine-facing rules where explanation would duplicate them, but include enough command detail for a human to succeed without opening the skill.
- Test workflow structure and relationships, not indentation trivia or arbitrary prose.

### Keep It Clean Checklist

- [ ] Workflow remains inert and contains no secret values.
- [ ] No CI installation or runner provisioning.
- [ ] TL;DR is five lines or fewer.
- [ ] Every numbered step has one action and a correct-result statement.
- [ ] Teardown warning is adjacent to the command.

## E. Completeness: Observability, Security, Operability

- **Observability decision:** The workflow uploads test results and logs. The local runbook directs the operator to the absolute results XML and Unity log; no extra normal-path logging is added.
- **Security:** Use secret references only, pin official action versions according to current guidance, minimize workflow permissions, and reject embedded license/credential material.
- **Runbook:** The new local runbook is the operability deliverable. Rollback means removing the inert reference files and their focused tests. Monitoring is limited to workflow artifacts or local XML/log evidence.
- **Baseline:** The full discovery baseline is 141 passes and two unrelated failures: the PR-review agent-name collision guard and the wildcard `applyTo` target guard. Pre-propagation sync failures are expected after the bundled reference is added.

## F. Test Plan

| Acceptance Criteria | Evidence | Category |
|---|---|---|
| AC1–AC2 | File placement, safe YAML parsing/shape, action/input verification, secret scan | Must-have automated test |
| AC3–AC5 | Runbook structure parser plus human dry-run review against finalized skill | Must-have automated test; manual QA check |
| AC6 | Deletion/negation mutations for workflow and runbook guards | Must-have automated test |

### Top Five High-Value Checks

1. Given the workflow template, when validated with the selected GitHub-Actions-compatible method, then it defines checkout, GameCI test execution, artifact publication, minimal permissions, and secret references without literal credentials; if no compatible validator is available, structural checks and parse review are reported separately.
2. Given the runbook, when headings and ordered steps are parsed, then the TL;DR is no more than five lines and each step includes an exact command and expected result.
3. Given both platform commands, when tokens are inspected, then EditMode uses `-nographics` while PlayMode/visual does not.
4. Given the teardown step, when reviewed, then it validates the explicit fixed worktree target and places the warning beside the command.
5. Given removal of artifact upload, worktree persistence, or the GUI prohibition, when focused guards run, then the relevant guard fails for that obligation.

### Fixtures and Test Impact

- Create `tests/[PROPOSED - name TBD: Unity reference asset guards]` with structural workflow checks and use an existing GitHub-Actions-compatible validator if available; do not call token checks a parser or add a runtime dependency solely for tests.
- Verify exact GameCI fields against current official documentation before encoding guards.
- Manually dry-run the runbook against the finalized skill and reference-project facts without installing CI.
- Run the focused module and propagation tests. The new bundled file should be covered by recursive skill propagation behavior; generated mirrors remain pending maintainer propagation.

## Stage 1: Current GameCI Contract Verification
**Goal**: Verify the current official GameCI workflow surface and choose final terse asset filenames.
**Success Criteria**: Action versions, inputs, permissions, license-secret references, and artifact behavior are evidence-backed before authoring.
**Status**: Not Started

## Stage 2: Reference Asset Guards
**Goal**: Add failing structural guards for workflow safety/shape and runbook format/contract fidelity.
**Success Criteria**: AC1–AC6 guards are non-vacuous and proven red through targeted deletion or negation.
**Status**: Not Started

## Stage 3: Workflow and Runbook Authoring
**Goal**: Write the inert GameCI template and concise operator runbook from the finalized canonical contracts.
**Success Criteria**: AC1–AC5 pass without installing CI, exposing secrets, or duplicating machine-facing policy.
**Status**: Not Started

## Stage 4: Verification
**Goal**: Parse the workflow, dry-run the runbook, and run focused/regression tests.
**Success Criteria**: New guards pass; docs remain actionable; unrelated and propagation-pending failures are separated.
**Status**: Not Started
