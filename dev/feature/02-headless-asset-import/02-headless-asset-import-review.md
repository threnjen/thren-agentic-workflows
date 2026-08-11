# Review Record: Headless Asset Import

## Summary

Second review after the implementer retry confirms the editor/path, conditional evidence, GUI-negation, and owning-section path fixes remain intact. All 45 focused guards are green. AC5 remains `not-executed (reference project not clean)` with no Unity launch or external mutation, so the required controlled import has no runtime evidence and the feature cannot receive an approval verdict.

## Verdict

Changes Requested

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1 | Verified after correction | `source_of_truth/skills/unity-development/SKILL.md:281`; `tests/test_unity_skill_contract.py:105-134,320-372` | The import uses `"<resolved-unity-editor>"`, `<execution-unity-project>`, the main-checkout root/nested mapping, `-batchmode`, `-quit`, and `-logFile -`; it excludes `-runTests`. |
| AC2 | Verified after correction | `source_of_truth/skills/unity-development/SKILL.md:279-290`; `tests/test_unity_skill_contract.py:119-143,333-363` | Serializer authority and the separate Editor-API construction command remain intact. Regeneration is now explicitly unverified until a controlled run succeeds. |
| AC3 | Verified after correction | `tests/test_unity_skill_contract.py:60-102,307-309,375-399` | The source-wide sweep evaluates clauses, catches a positive GUI requirement followed by a negated clause, and accepts a scoped `without a human-opened or GUI-opened Editor` prohibition. |
| AC4 | Verified after correction | `source_of_truth/skills/unity-development/SKILL.md:25-26,162-164`; `tests/test_unity_skill_contract.py:40-57,147-158,312-317,401-419` | Both owning sections independently require `Assets/Tests/Editor`; the Refactor rules also preserve `Assets/Tests/PlayMode`. |
| AC5 | `not-executed (reference project not clean)` | `dev/feature/02-headless-asset-import/02-headless-asset-import-implementation.md` Preflight and AC matrices | The reference checkout still has unrelated untracked Feature 09–14 planning folders and a phase execution manifest. No `.meta` was withheld, Unity was not launched, and no external mutation occurred. |
| AC6 | Verified | `tests/test_unity_skill_contract.py:320-419` | Nine scoped asset-contract mutations plus positive, mixed-clause, prohibition, invalid-path, and per-section path cases are green. |

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | The Serialized Assets import example used a bare `Unity` executable and generic `<path>`, bypassing canonical editor discovery and nested-project resolution. | High | `source_of_truth/skills/unity-development/SKILL.md:281` | AC1 | Fixed (applied during this review) |
| 2 | The skill stated missing-`.meta`/GUID generation as established behavior although the required controlled reference import had not run. | High | `source_of_truth/skills/unity-development/SKILL.md:281` | AC2, AC5 | Fixed in the contract; runtime evidence remains open as issue #5 |
| 3 | Broad sentence-level negation allowed a positive human/GUI-open requirement to pass when a later clause contained `no`, `not`, `without`, or `never`. | Medium | `tests/test_unity_skill_contract.py:71-102` | AC3, AC6 | Fixed (applied during this review) |
| 4 | The path guard required `Assets/Tests/Editor` only somewhere in the corpus, so either owning skill reference could regress unnoticed. | Medium | `tests/test_unity_skill_contract.py:40-57,147-158` | AC4, AC6 | Fixed (applied during this review) |
| 5 | The controlled missing-`.meta` import remains unexecuted because the reference project is not clean. | High | `dev/feature/02-headless-asset-import/02-headless-asset-import-implementation.md` Preflight | AC5 | Open (`not-executed (reference project not clean)`) |

## Fixes Applied

| File | What Changed | Issue # |
|------|--------------|---------|
| `source_of_truth/skills/unity-development/SKILL.md` | Replaced the bare executable/generic path with the resolved editor, `<execution-unity-project>`, and main-checkout root/nested mapping. Changed the capability wording to require controlled empirical verification before treating regeneration as proven. | 1, 2 |
| `tests/test_unity_skill_contract.py` | Added editor/project/main-checkout obligations and mutations; changed the GUI sweep to clause-scoped negation; added legitimate-prohibition and mixed-clause controls; scoped path checks and mutations to both owning sections. | 1–4 |
| `dev/feature/02-headless-asset-import/02-headless-asset-import-implementation.md` | Updated the implementation summary, AC evidence, mutation counts, commands, artifacts, and final test counts while retaining the exact AC5 non-execution status. | 1–5 |

## Remaining Concerns

- AC5 remains `not-executed (reference project not clean)`. Re-run only after `/Users/jennywadkins/github_repos/the-movies` is clean, then record the selected tracked asset, the withheld `.meta`, the resolved editor command, generated GUID evidence, restoration, and final clean status.
- No external asset, `.meta`, GUID, or reference-project file was changed during this review. Unity was not launched.
- Maintainer propagation remains pending. This review did not run propagation or edit `ports/` or `.github/`.
- Phase-document reconciliation remains pending because the caller prohibited phase-document edits.

## Test Coverage Assessment

- Covered: AC1–AC4 and AC6 through 45 focused structural, source-sweep, command, and mutation cases.
- Missing: AC5's controlled Unity import and generated `.meta`/GUID evidence.
- Repository regression status is unchanged by this feature: the relevant suite retains one pre-existing wildcard `applyTo` failure, and the safe full suite retains that failure plus the pre-existing PR-review display-name collision.

### Test Evidence

| Status | Command | Artifact | Counts |
|--------|---------|----------|--------|
| `executed-green` | `uv run pytest tests/test_unity_skill_contract.py -q --junitxml=dev/test-results/02-headless-asset-import-second-review.xml` | `dev/test-results/02-headless-asset-import-second-review.xml` | 45 passed, 0 failed, 45 total |
| `executed-failing` | `uv run pytest tests/test_unity_skill_contract.py tests/test_agent_corpus_invariants.py tests/test_propagate_master_assets.py -q --junitxml=dev/test-results/02-headless-asset-import-review-regression.xml` | `dev/test-results/02-headless-asset-import-review-regression.xml` | 95 passed, 1 failed, 96 total; 35 subtests passed |
| `executed-failing` | `uv run pytest tests/ -k 'not test_committed_tree_is_at_a_propagation_fixed_point' -q --junitxml=dev/test-results/02-headless-asset-import-review-full-no-fixedpoint.xml` | `dev/test-results/02-headless-asset-import-review-full-no-fixedpoint.xml` | 185 passed, 2 failed, 187 executed; 1 deliberately deselected; 188 collected; 63 subtests passed |
| `not-executed` | Controlled missing-`.meta` Unity import; cleanliness check only: `git -C /Users/jennywadkins/github_repos/the-movies status --short` | No Unity XML/log or generated-asset artifact | AC5: `not-executed (reference project not clean)`; no external mutation |

The relevant regression failure is `InstructionApplyToTests.test_every_enumerated_applyto_target_exists`. The safe full run also retains `test_agent_name_does_not_collide_with_prose_in_any_source_asset`. Both are recorded pre-feature defects outside this feature's ownership. The fixed-point test was deliberately deselected because it writes generated outputs when propagation is pending.

## Risk Summary

- Second-review verdict remains Changes Requested because AC5 lacks the required clean-reference Unity import evidence.
- The authored contract is internally coherent for resolved editors, root and nested Unity layouts, main-checkout verification, serializer authority, and the separation between plain import and `-executeMethod` asset construction.
- The strengthened guards fail independently for stale editor/path wording, unconditional regeneration claims, mixed-clause GUI requirements, and either owning EditMode path reference.
- Consumer alignment may proceed against the corrected wording, but completion evidence must continue to identify AC5 as unverified rather than infer regeneration from the command.
