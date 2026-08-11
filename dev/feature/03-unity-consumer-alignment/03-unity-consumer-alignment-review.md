# Review Record: Unity Consumer Alignment

## Summary

Both High Unity review findings were fixed. Visual Verifier now resolves `ProjectVersion.txt` from the selected root-or-nested execution project, and Phase Execute assigns visual wiring to the Feature Implementer before the A1 commit. The post-wave gate no longer creates dirty inputs it cannot test; missing inputs produce an explicit non-green blocker. All 30 focused guards pass, and the safe full suite returned to its two known baseline failures.

## Verdict

Approved with Reservations

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1 | Verified | `source_of_truth/agents/04-phase-execute.agent.md:103-112`; `tests/test_unity_consumer_contract.py:40-77,211-214,241-282` | Step 2.5 delegates to the canonical ladder, targets `<execution-unity-project>`, writes absolute main-checkout XML/logs, keeps one retry and attestation, and never delegates Unity execution to the user. |
| AC2 | Verified | `source_of_truth/agents/04-phase-execute.agent.md:108-112`; `tests/test_unity_consumer_contract.py:57-76,249-273` | `executed-green`, `executed-failing`, and `not-executed` remain distinct. Decline, unattended status, genuine missing evidence, and supervisor-directed skip remain non-green. |
| AC3 | Verified after correction | `source_of_truth/agents/04-phase-execute.agent.md:67-69,121-125`; `source_of_truth/agents/04g-unity-visual-verification.agent.md:35-67`; `tests/test_unity_consumer_contract.py:80-153,217-227,285-333,390-420` | Discovery order and saved path remain; version discovery is bound to `<execution-unity-project>`. PlayMode has graphics, no `-nographics`/`-quit`, and absolute main-checkout evidence. Capture inputs are committed at A1 or the gate fails non-green. |
| AC4 | Verified | `source_of_truth/agents/04h-unity-reviewer.agent.md:20-34`; `tests/test_unity_consumer_contract.py:156-182,230-233,336-372` | Tests use the canonical ladder without `-quit`; conditional serialized-asset validation uses the canonical import contract and preserves clean-import evidence limits. |
| AC5 | Verified | All three consumer agents; `tests/test_unity_consumer_contract.py:185-200,236-238,375-387` | Consumers reference canonical mechanics. Only Visual Verifier owns editor discovery; no consumer copies worktree commands. |
| AC6 | Verified | `tests/test_unity_consumer_contract.py:203-420` | Thirty focused cases include consumer enumeration, scoped obligations, semantic mutations, nested-path relation, lifecycle mutations, and duplicate-mechanics injections. |

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | Visual Verifier read `ProjectSettings/ProjectVersion.txt` as a root-only path, so editor discovery could fail for supported nested Unity projects. | High | `source_of_truth/agents/04g-unity-visual-verification.agent.md:53` | AC3, AC5 | Fixed (applied during review) |
| 2 | Phase Execute could create capture inputs after wave commits and immediately invoke a verifier that correctly refuses to test uncommitted shadow-worktree inputs; no checkpoint/resume branch existed. | High | `source_of_truth/agents/04-phase-execute.agent.md:69,124`; `source_of_truth/agents/04g-unity-visual-verification.agent.md:40` | AC3, AC5 | Fixed with an explicit non-green limitation (applied during review) |

## Fixes Applied

| File | What Changed | Issue # |
|------|--------------|---------|
| `source_of_truth/agents/04g-unity-visual-verification.agent.md` | Bound Unity version discovery to `<execution-unity-project>/ProjectSettings/ProjectVersion.txt`, preserving the existing environment/override/Hub order. | 1 |
| `source_of_truth/agents/04-phase-execute.agent.md` | Assigned Visual Verification Wiring to the Feature Implementer before A1; prohibited post-wave capture-input mutation; added an exact non-green status and `all-approved: no` for missing committed inputs. | 2 |
| `tests/test_unity_consumer_contract.py` | Added a structural root/nested path relationship guard, a Phase Execute implementation/checkpoint lifecycle guard, and five targeted mutation cases. | 1, 2 |
| `dev/feature/03-unity-consumer-alignment/03-unity-consumer-alignment-implementation.md` | Updated the AC evidence, test counts/artifacts, sibling status, lifecycle limitation, and final regression results. | 1, 2 |

## Remaining Concerns

- Reservation: the post-wave visual gate intentionally cannot repair missing capture package/config inputs. It records `visual-verification: not configured (capture inputs missing at implementation checkpoint)`, sets `all-approved: no`, and carries the blocker to final review. A later implementation/review cycle must add and commit those inputs before rerunning the gate.
- Maintainer propagation remains pending. No generated `ports/` or `.github/` file was edited, and propagation was not run.
- The full repository suite remains red only at the two recorded baseline defects: the PR-review display-name collision and wildcard `applyTo` target guard.
- Unity runtime execution was not required for this Markdown consumer-alignment feature; Features 01 and 02 retain empirical command-evidence ownership.
- Phase-document reconciliation remains pending because the caller prohibited phase-document edits.

## Test Coverage Assessment

- Covered: AC1–AC6 through 30 focused structural, relationship, command, status, and mutation cases.
- Covered: upstream Unity skill compatibility, generic agent corpus invariants, and propagation behavior in the relevant regression suite.
- Not applicable: C# compilation, Unity lifecycle/runtime wiring, and external Unity execution; this feature changes agent contracts only.
- Reservation: structural guards prove the missing-input branch is safe and non-green, not that every future visual feature supplies capture inputs before A1.

### Test Evidence

| Status | Command | Artifact | Counts |
|--------|---------|----------|--------|
| `executed-green` | `uv run pytest tests/test_unity_consumer_contract.py -q --junitxml=dev/test-results/03-unity-consumer-alignment-review-focused.xml` | `dev/test-results/03-unity-consumer-alignment-review-focused.xml` | 30 passed, 0 failed, 30 total |
| `executed-failing` | `uv run pytest tests/test_unity_consumer_contract.py tests/test_unity_skill_contract.py tests/test_agent_corpus_invariants.py tests/test_propagate_master_assets.py -k 'not test_committed_tree_is_at_a_propagation_fixed_point' -q --junitxml=dev/test-results/03-unity-consumer-alignment-review-regression.xml` | `dev/test-results/03-unity-consumer-alignment-review-regression.xml` | 125 passed, 1 failed, 126 executed; 35 subtests passed |
| `executed-failing` | `uv run pytest tests/ -k 'not test_committed_tree_is_at_a_propagation_fixed_point' -q --junitxml=dev/test-results/03-unity-consumer-alignment-review-full-no-fixedpoint.xml` | `dev/test-results/03-unity-consumer-alignment-review-full-no-fixedpoint.xml` | 235 passed, 2 failed, 237 executed; 1 deliberately deselected; 238 collected; 63 subtests passed |

The relevant regression failure is `InstructionApplyToTests.test_every_enumerated_applyto_target_exists`. The safe full run also retains `test_agent_name_does_not_collide_with_prose_in_any_source_asset`. Both match the recorded pre-feature baseline. The deliberately deselected fixed-point test writes generated outputs when propagation is pending.

## Risk Summary

- Both High review findings are fixed and protected by semantic mutations.
- PlayMode remains graphics-enabled; EditMode's `-nographics` rule did not leak into Visual Verifier.
- Root and nested Unity layouts now share one explicit version-file relationship and one execution-project vocabulary.
- Missing visual inputs fail closed and remain visible to final review rather than blocking indefinitely or being treated as pass.
- Verdict is Approved with Reservations because the repository baseline remains red and late missing visual inputs require another committed implementation cycle rather than in-gate repair.
