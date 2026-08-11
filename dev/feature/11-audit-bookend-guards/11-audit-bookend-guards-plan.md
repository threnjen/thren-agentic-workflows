# Feature Plan: Audit Bookend Guards

## Execution Metadata

- **Wave:** 3
- **Parallel safe:** yes
- **Depends on:** `08-audit-comparison-contract`, `09-audit-delta-rewire`, `10-phase-execute-audit-bookend`
- **Key files modified:** `tests/[PROPOSED - name TBD: test_phase_execute_audit_bookend.py]`
- **Sequential reason:** n/a

## A. Requirements & Traceability

### Acceptance Criteria

1. **AC1:** A focused Phase 03 test module validates the new skill's frontmatter, both consumer references, and the single-home boundary for every extracted mechanical rule.
2. **AC2:** Guards prove the shared skill contains no interactive confirmation/question/offer and that `Audit - Delta` retains its type/target selection, matrix confirmation, conditional delta offer, fix-research offer, and remediation flow.
3. **AC3:** Parsed topology proves `Phase - Execute` declares the five exact existing leaf agents, can spawn them, and never delegates the bookend to the `Audit - Delta` orchestrator.
4. **AC4:** Workflow guards prove the Step 1 scope decision occurs once, the audits occur only after the wave loop and existing Step 5, and the bookend outcome reaches Step 6.
5. **AC5:** Prompt-contract guards cover the single-template/three-varying-field rule, manifest intent without excuse, documentation exclusion, Infra override, reduced test lens, current-side output root, and separate audit types.
6. **AC6:** Gate guards cover full-report totals before delta, no regression label before attribution, disjoint attribution batches and sum check, and worktree release after attribution.
7. **AC7:** Branch guards cover scoped/full/declined decisions, bookend-scope unusability after existing manifest/bundle validation, worktree failure, conditional infra, `all-approved: no`, and continuation to Step 6; separate guards preserve current hard-stops for missing/ambiguous manifests and incomplete bundles.
8. **AC8:** Remediation guards cover High-or-above plus phase attribution, one retry, current-side-only edits, targeted-file verification, and the explicitly non-comparable delta addendum.
9. **AC9:** Every content guard is demonstrated red by deleting or semantically negating its load-bearing mechanism, reports the named obligation, and returns green after restoration; non-vacuity assertions prove the scoped sections and mutation targets exist.
10. **AC10:** Focused and repository regression runs preserve the recorded baseline, and no test reads generated `ports/` as the source of Phase 03 truth.

### Non-Goals

- Do not test one exact prose rendering when a section-scoped structural assertion can enforce the obligation.
- Do not add exemptions to generic corpus sweeps for Phase 03.
- Do not test runtime byte identity as if static parsing could prove it; retain that as explicit manual QA.
- Do not modify the skill or consumers in this feature unless a guard exposes a contradiction that must be sent back to the owning upstream feature.
- Do not edit generated ports or run propagation.

### Traceability

| Acceptance Criteria | Code Areas/Modules | Test / Evidence Category |
|---|---|---|
| AC1–AC2 | Finalized audit-comparison skill and `source_of_truth/agents/delta-auditor.agent.md` | Must-have automated test |
| AC3–AC5 | `source_of_truth/agents/04-phase-execute.agent.md`, parsed corpus loader, finalized skill | Must-have automated test |
| AC6–AC9 | Focused validator helpers and mutation/negation parameter sets in `tests/[PROPOSED - name TBD: test_phase_execute_audit_bookend.py]` | Must-have automated test |
| AC10 | Focused module, `tests/test_agent_corpus_invariants.py`, `tests/test_unity_consumer_contract.py`, `tests/test_propagate_master_assets.py`, `tests/test_pr_review_orchestrator.py`, and full suite | Existing test to update: no update expected; run as regression evidence |

## B. Correctness & Edge Cases

- Validator helpers return named obligation sets so a mutation test proves the intended failure rather than any incidental assertion.
- Section extraction asserts headings exist before searching within them; a deleted section cannot make every scoped check vacuously pass.
- Whitespace is normalized for prose-contract checks so harmless wrapping does not break the suite.
- Guards distinguish a deleted mechanism from a changed sentence. Choice statements alone cannot satisfy tests for actual workflow ordering or spawn authority.
- Any roster check derives agent names from the corpus loader and exact frontmatter rather than maintaining a second hand-written existence list.
- Single-home checks scope skill and consumer sections precisely so repeated words in unrelated Phase 7/8 content cannot satisfy them.
- Mutation sweeps include semantic negation, not only typo perturbation.
- Runtime-only claims remain manual: captured prompt byte identity, baseline worktree survival during real attribution, and end-to-end `Audit - Delta` behavioral identity.

## C. Consistency & Architecture Fit

- Follow `tests/test_phase_refiner_final_check.py`: focused phase module, small parsers, named obligation sets, parameterized mutation cases, and explicit non-vacuity tests.
- Use `scripts/propagate_master_assets.py` parsing helpers only as imported read-only utilities; never invoke propagation.
- Follow `guard-integrity`: derive sets from disk where possible, anchor checks to owning sections, normalize whitespace, and prove each guard red then green.
- The proposed test filename remains `[PROPOSED - name TBD: test_phase_execute_audit_bookend.py]` until implementation confirms the final concise name.
- Relationship: this is the verification tail after all three deliverables. It integrates evidence across the skill and both consumers but does not take ownership of their implementation.

### Unverified Assumptions

- The final shared-skill slug and final Phase Execute bookend heading are chosen upstream. The test must derive or read the finalized names rather than hard-code a proposed placeholder.

## D. Clean Design & Maintainability

- One validator per contract domain: topology, shared ownership, Delta interaction, Phase Execute order, gates, remediation, and continuation branches.
- Keep mutation cases close to the obligation they kill.
- Prefer parsed frontmatter and bounded sections over repository-wide substring searches.
- Keep runtime-only acceptance in the manifest's manual checklist.

### Keep It Clean Checklist

- [ ] Every helper has a non-vacuity assertion.
- [ ] Every content guard is seen red for the intended reason.
- [ ] No fragile whole-document snapshots.
- [ ] No exemptions or generated-output dependencies.
- [ ] Baseline failures are compared, not absorbed.

## E. Completeness: Observability, Security, Operability

- **Observability decision:** Test output names the violated obligation. No additional logs or artifacts are required beyond retained pytest evidence and the manual QA artifacts listed in the phase manifest.
- **Security:** Tests read local source contracts only and do not create worktrees, run auditors, access secrets, or modify the analyzed corpus.
- **Runbook:** Run the focused module first, then corpus invariants and propagation tests, then the full suite. For each protected mechanism, retain delete/negate-red and restore-green evidence. Runtime manual QA is separate and must not be claimed by static tests.

## F. Test Plan

| Acceptance Criteria | Evidence | Category |
|---|---|---|
| AC1–AC8 | Focused Phase 03 validators over the skill and both agents | Must-have automated test |
| AC9 | Parameterized deletion/negation sweep plus section/mutation-target non-vacuity assertions | Must-have automated test |
| AC10 | Focused, corpus, propagation, and full-suite commands compared with the recorded 2026-08-11 baseline | Existing test to update: no update expected; run as regression evidence |
| Runtime prompt/worktree/behavior claims | Real Phase Execute and `Audit - Delta` exercises with captured prompts and artifact paths | Manual QA check |

### Top Five High-Value Checks

1. Given all three source contracts, when ownership is parsed, then each moved mechanism has exactly one home and both consumers reference it.
2. Given the Phase Execute prompt renderer contract, when a fourth per-snapshot field or snapshot-specific scope text is introduced, then the guard fails for prompt identity.
3. Given workflow mutations that move audit work before wave completion or cleanup before attribution, when validators run, then each fails for the named ordering obligation.
4. Given skip/failure branch negations that preserve `all-approved: yes` or block Step 6, when validators run, then branch guards fail.
5. Given every load-bearing guard target, when it is deleted or semantically inverted, then the focused suite goes red and returns green only after restoration.

### Fixtures and Test Impact

- No external fixture is required. Read finalized source files from repository-relative paths.
- Existing `tests/test_phase_refiner_final_check.py` is a read-only reference pattern, not an edit surface.
- Existing `tests/test_agent_corpus_invariants.py` and `tests/test_propagate_master_assets.py` remain regression inputs.
- Full-suite baseline on 2026-08-11: 268 collected; pytest reported 256 passed and 15 existing failures/subfailures. Phase 03 must add no new failure.
- No Stage 0 is required because the repository already has a focused phase-contract test pattern and broad structural coverage.

## Stage 1: Structural Validators
**Goal**: Implement non-vacuous parsers and named obligation validators for the skill, Delta rewire, Phase Execute topology, workflow, and evidence branches.
**Success Criteria**: AC1–AC8 pass against the completed upstream features.
**Status**: Not Started

## Stage 2: Mutation and Regression Evidence
**Goal**: Prove each guard can fail for its intended reason and preserve the repository's known test baseline.
**Success Criteria**: AC9–AC10 hold, all mutations are killed, and restoration returns the focused suite to green.
**Status**: Not Started
