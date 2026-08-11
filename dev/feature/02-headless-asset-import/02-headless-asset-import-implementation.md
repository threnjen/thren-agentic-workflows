# Implementation Record: Headless Asset Import

## Summary

Extended the canonical Unity skill with a terse headless asset-database import procedure, preserved Unity serializer authority and the separate Editor-API construction command, and corrected both invalid `Assets/Tests/EditMode` references to the verified `Assets/Tests/Editor` convention. Extended the shared guard module with 10 non-vacuous contract/sweep/mutation cases. AC5 remains `not-executed (reference project not clean)` because unrelated untracked planning artifacts made a controlled `.meta` mutation unsafe.

## Preflight

- Repository under implementation: Markdown agent/skill corpus with Python structural tests; not a Unity project itself.
- Reference target: `/Users/jennywadkins/github_repos/the-movies`; `ProjectSettings/ProjectVersion.txt` still reports Unity `6000.3.13f1`.
- Editor discovery: `/Applications/Unity/Hub/Editor/6000.3.13f1/Unity.app/Contents/MacOS/Unity` exists and is executable; no bare `Unity` assumption was used or persisted.
- Reference cleanliness: failed before mutation. `git status --short` reported unrelated untracked `dev/feature/09-production-sheet-contract/` through `14-production-planning-integration/` plus `dev/feature/PHASE_08O-execution-manifest.md`.
- External mutation: none. No asset or `.meta` file was moved, deleted, created, restored, or committed; Unity was not launched for import.
- Unity code preflight (`activeInputHandler`, `.asmdef` references, scene wiring, render pipeline): N/A; this feature changes no C#, assemblies, scenes, assets, or renderers.

## Sibling Features

- `01-unity-test-execution-contract` is committed upstream and selected `tests/test_unity_skill_contract.py` as the shared guard module. Its 32 focused cases remain green.
- `03-unity-consumer-alignment` consumes this feature's finalized import contract but owns all agent-definition edits.
- `04-unity-test-reference-assets` consumes the canonical contract in separate reference assets and was not modified.

## AC Coverage Matrix

| AC | Criterion ID | Planned Test ID | Planned Test Pattern | Status | Implementing Files | Evidence Paths | Implement Commit SHA | Review Commit SHA |
|----|--------------|-----------------|----------------------|--------|--------------------|----------------|----------------------|-------------------|
| AC1 | Headless import command | `HAI-AC1` | Scoped Serialized Assets parser verifies `-batchmode`, `-quit`, `-projectPath`, `-logFile -`, and absence of `-runTests` | Complete | `source_of_truth/skills/unity-development/SKILL.md`, `tests/test_unity_skill_contract.py` | `dev/test-results/02-headless-asset-import-focused.xml` | PENDING | PENDING |
| AC2 | Unity serializer authority | `HAI-AC2` | Preserve sole-authority/raw-YAML prohibition and separate `-executeMethod` command | Complete | Same | `dev/test-results/02-headless-asset-import-focused.xml` | PENDING | PENDING |
| AC3 | Source-wide contradiction sweep | `HAI-AC3` | Disk-derived non-empty source sweep distinguishes prohibited requirements from negative/authority language | Complete | `tests/test_unity_skill_contract.py` | `dev/test-results/02-headless-asset-import-focused.xml` | PENDING | PENDING |
| AC4 | EditMode path correction | `HAI-AC4` | Non-empty source sweep rejects `Assets/Tests/EditMode` and requires Editor/PlayMode conventions | Complete | Same | `dev/test-results/02-headless-asset-import-focused.xml` | PENDING | PENDING |
| AC5 | Reference-project import | `HAI-AC5-MANUAL` | Controlled missing-`.meta` import and clean restoration | `not-executed (reference project not clean)` | External QA only | This implementation record's Preflight; concurrent artifact: none | PENDING | PENDING |
| AC6 | Non-vacuous mutation guards | `HAI-AC6` | Six scoped asset-contract mutations plus injected GUI/path sweep regressions | Complete | `tests/test_unity_skill_contract.py` | `dev/test-results/02-headless-asset-import-focused.xml`, `dev/test-results/phase-01-wave-2.xml` | PENDING | PENDING |

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | Sanction plain headless import and missing `.meta`/GUID generation | Complete | Skill, shared guards | Exact phase command is scoped to Serialized Assets and excludes `-runTests`. |
| AC2 | Preserve Unity-generated authority and raw-YAML prohibition | Complete | Skill, shared guards | Existing authority text and construction procedure remain; a mutation weakening `sole authority` fails. |
| AC3 | Reject human/GUI-open requirements throughout `source_of_truth/` | Complete | Shared guards | Sweep enumerates real text files, asserts non-vacuity, permits legitimate Editor API/serializer language, and kills an injected positive requirement. |
| AC4 | Replace invalid EditMode paths while preserving PlayMode | Complete | Skill, shared guards | Both known occurrences now use discovery-friendly `Assets/Tests/Editor`; `Assets/Tests/PlayMode` remains. |
| AC5 | Empirically regenerate one missing `.meta` headlessly | `not-executed (reference project not clean)` | External QA only | Target/version/editor resolved, but the required clean-tree precondition failed before asset selection. No mutation or Unity import occurred; no artifact exists. |
| AC6 | Structural guards are non-vacuous and proven red | Complete | Shared guards | Initial red: 6 failed, 36 passed. Final focused suite: 42 passed; all Wave 1 guards remained green. |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `source_of_truth/skills/unity-development/SKILL.md` | Modify | Added one headless import rule and corrected two EditMode path references | Implements AC1–AC4 without changing Wave 1's Test Execution section |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| `tests/test_unity_skill_contract.py` | Modify | Added Serialized Assets extraction/validation, source GUI/path sweeps, and semantic mutation cases | AC1–AC4, AC6; retains all Feature 01 coverage |

## Test Results

- **Execution**: executed-failing
- **Command**: `uv run pytest tests/test_unity_skill_contract.py -q --junitxml=dev/test-results/02-headless-asset-import-focused.xml`; `uv run pytest tests/test_unity_skill_contract.py tests/test_agent_corpus_invariants.py tests/test_propagate_master_assets.py -q --junitxml=dev/test-results/phase-01-wave-2.xml`; `uv run pytest tests/ -k 'not test_committed_tree_is_at_a_propagation_fixed_point' -q --junitxml=dev/test-results/02-headless-asset-import-full-no-fixedpoint.xml`
- **Results artifact**: `dev/test-results/02-headless-asset-import-focused.xml`; `dev/test-results/phase-01-wave-2.xml`; `dev/test-results/02-headless-asset-import-full-no-fixedpoint.xml`
- **Baseline**: focused 32 passed, 0 failed; repository phase baseline 141 passed, 2 failed, 143 total before Phase 01
- **Final**: focused 42 passed, 0 failed; Wave 2 gate 92 passed, 1 failed, 35 subtests passed; safe full regression 182 passed, 2 failed, 1 deselected, 63 subtests passed
- **New tests added**: 10 collected cases
- **Affected suites run**: shared Unity skill guards; agent corpus invariants; propagation suite; full repository suite with only the generated-output-writing fixed-point test deselected
- **Regressions**: Unknown — executed suites remain failing only at the two recorded pre-phase baseline defects: the PR-review display-name collision and wildcard `applyTo` enumeration. The Wave 2 gate includes only the wildcard failure. No new unexplained failure appeared.
- **AC5 execution**: `not-executed (reference project not clean)`
- **AC5 command**: Not run; cleanliness check was `git -C /Users/jennywadkins/github_repos/the-movies status --short`
- **AC5 results artifact**: None — stopped before selecting or withholding any `.meta` file.

## Deviations from Plan

- The source enumeration uses the existing shared module's disk-derived text-file sweep rather than `git ls-files`; this preserves non-vacuity and sees newly authored files before staging.
- The full regression deselected `test_committed_tree_is_at_a_propagation_fixed_point` because that test writes generated outputs when propagation is pending. The required propagation suite still ran in the Wave 2 gate; propagation itself was not run.
- AC5 stopped at its documented safety boundary because the external project was not clean. No attempt was made to clean or alter unrelated files.

## Gaps

- AC5 is unverified. Re-run the controlled missing-`.meta` check only after `/Users/jennywadkins/github_repos/the-movies` is clean; record the selected tracked asset and restoration method before mutation.
- Maintainer propagation remains pending. No generated output was edited.

## Reviewer Focus Areas

- Confirm the new headless-import rule remains distinct from both `-runTests` and the `-executeMethod` construction procedure.
- Review the contradiction sweep's negation handling so legitimate “without a human-opened” and serializer-authority text cannot become false positives.
- Confirm the two path edits are discovery-friendly examples rather than a universal Unity layout rule.
- Treat AC5 as unverified; do not infer `.meta` regeneration from the documented command alone.
