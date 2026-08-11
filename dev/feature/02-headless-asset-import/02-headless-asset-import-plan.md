# Feature Plan: Headless Asset Import

## Execution Metadata

- **Wave:** 2
- **Parallel safe:** no
- **Depends on:** `01-unity-test-execution-contract`
- **Key files modified:** `source_of_truth/skills/unity-development/SKILL.md`, `tests/[PROPOSED - name TBD: Unity skill contract guards]`
- **Sequential reason:** shares `source_of_truth/skills/unity-development/SKILL.md` and `tests/[PROPOSED - name TBD: Unity skill contract guards]` with upstream `01-unity-test-execution-contract`

## A. Requirements & Traceability

### Acceptance Criteria

1. **AC1:** The Serialized Assets guidance sanctions `Unity -batchmode -quit -projectPath <path> -logFile -` for headless asset-database import and missing `.meta`/GUID generation without implying that a human must open the Editor.
2. **AC2:** The new import procedure remains consistent with the existing rule that Unity, not an agent, authors serialized assets and GUIDs; it does not weaken the prohibition on hand-authored serialized YAML.
3. **AC3:** Every `source_of_truth/` file is swept for claims that a human-opened Editor is required to generate `.meta` files, and no contradictory claim remains.
4. **AC4:** The verified invalid path `Assets/Tests/EditMode` is removed from the skill's Preflight and Refactor/Rewire guidance and replaced with the reference project's actual EditMode convention, `Assets/Tests/Editor`, without changing `Assets/Tests/PlayMode` guidance.
5. **AC5:** The headless import invocation is executed against `/Users/jennywadkins/github_repos/the-movies` on Unity 6000.3.13f1, and evidence records that the import ran without a GUI and that a controlled missing `.meta` file was regenerated or, if safe mutation cannot be arranged, records the claim as unverified rather than fabricating success.
6. **AC6:** Structural guards cover the import command relationship, the source-wide contradiction sweep, and the path sweep; each guard includes a non-vacuity assertion and is proven red by negating/removing its protected mechanism.

### Non-Goals

- Do not alter the Test Execution ladder or platform flags owned by `01-unity-test-execution-contract`.
- Do not change what Unity tests assert or rename the reference project's test directories.
- Do not hand-author or commit `.meta` files in the reference project merely to manufacture evidence.
- Do not update consumer agents; `03-unity-consumer-alignment` owns those files.
- Do not run propagation or edit generated outputs.

### Traceability

| Acceptance Criteria | Code Areas/Modules | Test / Evidence Category |
|---|---|---|
| AC1–AC2 | `source_of_truth/skills/unity-development/SKILL.md` — Serialized Assets | Must-have automated test |
| AC3–AC4 | `source_of_truth/` sweep and skill Preflight/Refactor sections | Must-have automated test |
| AC5 | `/Users/jennywadkins/github_repos/the-movies` | Manual QA check |
| AC6 | `tests/[PROPOSED - name TBD: Unity skill contract guards]` | Must-have automated test |

## B. Correctness & Edge Cases

- The import command legitimately uses `-quit`; the test-run command must continue to forbid `-quit` with `-runTests`. Scope guards by section and command purpose.
- A source-wide negative sweep must assert it inspected at least one tracked source file and must not be satisfied by an empty enumeration.
- The terms “Editor API” and “Unity Editor serializer” are not contradictions. The prohibited claim is that a human or GUI-opened Editor is required.
- Manual verification must use a recoverable, controlled missing `.meta` scenario and must restore the reference project to a clean tree. If that cannot be done safely, stop at unverified evidence.
- The path correction applies to the two verified skill occurrences, including the assembly-definition example at line 26 and the Refactor/Rewire inventory at line 164.

## C. Consistency & Architecture Fit

- Extend the existing Serialized Assets section instead of adding a competing top-level policy.
- Preserve the existing `-batchmode -executeMethod <Type>.<Method> -quit` guidance for asset-construction scripts; the plain import command is a separate sanctioned operation.
- Use `source_of_truth/` as the sweep boundary and authoring surface. Generated ports are excluded because propagation is pending by design.
- Relationship: depends on `01-unity-test-execution-contract` because both modify the same skill and shared guard module. `03-unity-consumer-alignment` depends on this feature's finalized import contract.

### Unverified Assumptions

- Headless import will regenerate a deliberately absent `.meta` in Unity 6000.3.13f1. AC5 must resolve this empirically.
- The reference project's `Assets/Tests/Editor` convention is project evidence, not a claim that every Unity repository uses that exact path; wording should avoid presenting it as universal where discovery is required.

## D. Clean Design & Maintainability

- Add one concise import procedure adjacent to the existing serialized-asset authority rule.
- Keep path guidance discovery-friendly: name the verified `Assets/Tests/Editor` convention without hard-coding a universal repository layout.
- Derive source files from disk for contradiction sweeps; do not hand-maintain an allowlist.
- Normalize whitespace and inspect scoped command tokens instead of pinning a whole prose sentence.

### Keep It Clean Checklist

- [ ] One asset-import procedure, not duplicate commands in multiple sections.
- [ ] No exception to Unity-generated asset authority.
- [ ] No `Assets/Tests/EditMode` occurrence under `source_of_truth/`.
- [ ] No GUI or human-open requirement.
- [ ] No generated-output edits.

## E. Completeness: Observability, Security, Operability

- **Observability decision:** Add no normal-path corpus logging. The import procedure streams Unity output through `-logFile -`; manual QA records command outcome and project cleanliness.
- **Security:** Operate only on the maintainer-supplied reference project. Do not expose license data or delete broad asset trees. Any controlled `.meta` mutation must target one validated file and be restored.
- **Runbook:** Run the focused guards, perform the controlled import check, verify `git -C /Users/jennywadkins/github_repos/the-movies status --short` returns clean, then run regression tests. Roll back by reverting only this feature's skill-section and guard changes.
- **Baseline:** Inherit the full discovery baseline of 141 passes and two unrelated failures: the PR-review agent-name collision guard and the wildcard `applyTo` target guard. Do not treat either as caused by this feature.

## F. Test Plan

| Acceptance Criteria | Evidence | Category |
|---|---|---|
| AC1–AC2 | Parse the Serialized Assets section and verify the import command token set and serializer-authority boundary | Must-have automated test |
| AC3 | Derived source-wide negation sweep with non-vacuity assertion | Must-have automated test |
| AC4 | Derived source-wide path sweep plus positive evidence for `Assets/Tests/Editor` and PlayMode preservation | Must-have automated test |
| AC5 | Controlled reference-project import and cleanliness evidence | Manual QA check |
| AC6 | Mutation proof for each content guard | Must-have automated test |

### Top Five High-Value Checks

1. Given the Serialized Assets section, when command tokens are parsed, then the headless import includes `-batchmode`, `-quit`, `-projectPath`, and `-logFile -` without `-runTests`.
2. Given all tracked `source_of_truth/` files, when contradiction shapes are scanned, then no human/GUI-open requirement for `.meta` generation remains and the scan is non-empty.
3. Given all tracked `source_of_truth/` files, when test-path references are scanned, then `Assets/Tests/EditMode` is absent and the corrected guidance remains discoverable.
4. Given a negated import obligation or reintroduced invalid path, when the guard runs, then it fails with the protected rule named.
5. Given a safe controlled missing `.meta` in the reference project, when headless import runs, then Unity recreates it without a GUI and the project is restored clean.

### Fixtures and Test Impact

- Extend `tests/[PROPOSED - name TBD: Unity skill contract guards]` created by Feature 01; shared ownership is why this feature is sequential.
- Use repository-derived file enumeration with explicit non-vacuity assertions.
- Do not modify the external project's tests or commit any verification mutation there.
- Run the focused guard module and existing corpus/propagation suites. Report sync failures as propagation pending.

## Stage 1: Asset Contract Guards
**Goal**: Add failing structural guards for the import command, contradiction sweep, and test-path correction.
**Success Criteria**: AC1–AC4 and AC6 guards fail under targeted negation/removal and pass only with non-vacuous source enumeration.
**Status**: Not Started

## Stage 2: Serialized Asset and Test-Path Guidance
**Goal**: Extend the existing asset-authority section and correct both verified invalid EditMode path references.
**Success Criteria**: AC1–AC4 guards pass without altering Feature 01's Test Execution contract.
**Status**: Not Started

## Stage 3: Headless Import Verification
**Goal**: Empirically verify the import and `.meta` behavior against Unity 6000.3.13f1.
**Success Criteria**: AC5 has honest evidence and the reference project finishes clean; unsafe verification is explicitly unverified.
**Status**: Not Started

## Stage 4: Regression Verification
**Goal**: Re-run focused and repository checks with generated outputs untouched.
**Success Criteria**: New guards pass, Feature 01 guards remain green, and unrelated or propagation-pending failures are separated.
**Status**: Not Started
