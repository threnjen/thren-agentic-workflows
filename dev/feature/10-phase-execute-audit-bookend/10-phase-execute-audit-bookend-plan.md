# Feature Plan: Phase Execute Audit Bookend

## Execution Metadata

- **Wave:** 2
- **Parallel safe:** yes
- **Depends on:** `08-audit-comparison-contract`
- **Key files modified:** `source_of_truth/agents/04-phase-execute.agent.md`
- **Sequential reason:** n/a

## A. Requirements & Traceability

### Acceptance Criteria

1. **AC1:** `Phase - Execute` frontmatter adds the existing leaf agents `Auditor - Code`, `Auditor - Infra`, `Auditor - Delta`, `Auditor - Attribution`, and `Baseline Worktree`; the bookend spawns no orchestrator and introduces no new agent.
2. **AC2:** The agent loads the finalized audit-comparison skill from `08-audit-comparison-contract` and adds thin bookend wiring between existing Step 5 Diff Security Review and Step 6 Phase Final Review without copying the shared sequence.
3. **AC3:** During Step 1 manifest validation, scope resolution starts with every manifest `key files modified` path and adds exactly one uncapped hop of reference-search dependents: files that name a modified path, import its module, or use names it defines.
4. **AC4:** An empty dependent search falls back to the modified files alone and records that limitation for audit Coverage and Limitations. After existing manifest/bundle validation succeeds, an unusable `key files modified` set records a bookend-scope reason, sets `all-approved: no`, and continues toward Step 6; the existing hard-stops for a missing/ambiguous manifest or incomplete feature bundles remain unchanged.
5. **AC5:** Scope treats all files under `source_of_truth/` and `tests/` as source, excludes standalone documentation such as `docs/` and README-style prose, and explicitly tells `Auditor - Infra` that this run overrides its Documentation category.
6. **AC6:** Step 1 asks exactly once whether to run the resolved scoped bookend, run a full-codebase alternative, or decline. The question states the resolved file count and audit types; the chosen state and any decline reason are recorded, and no later step asks again.
7. **AC7:** The code audit is always selected. The infra audit is selected if and only if the manifest touches CI, Docker, IaC, or build configuration, and the run or skip reason is recorded.
8. **AC8:** After all feature waves and existing gates complete, the baseline side is materialized at `<phase-baseline>` through `Baseline Worktree`, then baseline and current audits run back to back. No baseline audit runs before the wave loop finishes.
9. **AC9:** Baseline and current auditors receive one rendered prompt template whose only varying fields are target root, snapshot label, and output directory.
10. **AC10:** The rendered prompt states that the manifest supplies scope and intent, that stated intent never excuses a finding, that standalone documentation is excluded, and that tests receive only `Auditor - Code` categories 2, 5, 8, and 9.
11. **AC11:** Every bookend artifact is written under the working checkout in `dev/[audit-name]/` using short-sha snapshot labels; no report or output is written into the baseline worktree.
12. **AC12:** Code and infra use separate reports, deltas, queues, and counts. No security or refactor audit is added and no cross-type delta is produced.
13. **AC13:** `Auditor - Delta` is spawned only after both corresponding full findings reports exist and state their totals; no provisional finding is reported as a regression before attribution.
14. **AC14:** `Auditor - Attribution` probes every provisional current-side finding against both trees in disjoint subsystem batches whose item counts sum to the delta's unattributed total.
15. **AC15:** The baseline worktree cleanup handshake occurs only after delta and attribution finish; a worktree-materialization failure records a reason, sets `all-approved: no`, and continues toward Step 6.
16. **AC16:** Auto-remediation runs at most once, only for High-or-above findings attributed to the phase, only on the working checkout, and uses the established bounded prose re-spawn shape from Steps 2.5 and 3.
17. **AC17:** Remediation is followed by targeted verification over only remediation-touched files. Results are appended to the existing delta, marked not comparable with the full end audit, and never supplied as a new delta snapshot.
18. **AC18:** Declining the bookend records a stated reason, sets `all-approved: no`, performs no audits, and still allows Phase Final Review to run.
19. **AC19:** The bookend decision, audit/delta/attribution outcome, remediation result, verification status, artifact paths, and missing-evidence reasons are passed into the Step 6 Prod Code Review prompt.
20. **AC20:** Existing Step 1 bundle validation, wave execution, wave test gate, visual gate, QA, diff security review, final review, reporting, and documentation behavior remain intact except for the explicit bookend integration points.
21. **AC21:** The feature adds no normal-path application logging or new persistent state outside existing audit artifacts and pipeline evidence fields.

### Non-Goals

- Do not run a full-codebase audit by default or infer it from scope size.
- Do not add security or refactor bookend audits; existing Step 5 diff security remains unchanged.
- Do not audit standalone documentation or expand dependents beyond one hop.
- Do not fix Medium/Low findings or pre-existing findings not attributed to the phase.
- Do not spawn `Audit - Delta`; it is an orchestrator. Spawn only the named leaf agents.
- Do not write into or remediate the baseline worktree.
- Do not weaken the existing Step 1 hard-stops for a missing/ambiguous execution manifest or incomplete three-file feature bundles.
- Do not edit tests in this feature; `11-audit-bookend-guards` owns consolidated verification.
- Do not edit generated outputs or run propagation.

### Traceability

| Acceptance Criteria | Code Areas/Modules | Test / Evidence Category |
|---|---|---|
| AC1–AC2 | Frontmatter and new shared-skill call in `source_of_truth/agents/04-phase-execute.agent.md` | Must-have automated topology and single-home guards |
| AC3–AC7 | Existing Step 1 plus new scope/decision state | Must-have automated workflow guards; manual QA check for scope count and one-time decision |
| AC8–AC15 | New post-Step-5 bookend wiring, finalized skill, `source_of_truth/agents/05a-baseline-worktree.agent.md` as read-only reference | Must-have automated ordering/gate guards; manual QA check for runtime prompt identity and worktree lifetime |
| AC16–AC19 | Remediation, verification addendum, `all-approved`, and Step 6 prompt handoff | Must-have automated branch and ordering guards; manual QA check for bounded remediation behavior |
| AC20–AC21 | Full existing `04-phase-execute.agent.md` workflow | Existing test to update: no current focused Phase Execute test; code-review evidence plus full-suite regression |

## B. Correctness & Edge Cases

- Duplicate manifest paths and paths outside the repository are not silently accepted into audit scope; the existing manifest validation/failure path records unusable input.
- A modified file with zero dependents remains in scope and produces an explicit limitation rather than an empty audit.
- A highly referenced file may resolve most of the corpus. The uncapped count is shown at Step 1 so the user decides between scoped, full-codebase, or declined.
- Deleted or renamed files may not be searchable in the current tree. Path/name references and the manifest starting set preserve the best available scope, with gaps reported as limitations.
- Infra classification is derived from manifest paths, not auditor availability or user intuition. Ambiguous build configuration is recorded rather than silently skipped.
- A declined run, failed worktree, unusable manifest, partial auditor return, unreconciled delta, or attribution arithmetic failure is missing evidence, never a pass.
- Code and infra failures are handled independently; one type's successful delta cannot satisfy the other type's gate.
- No remediation occurs until attribution identifies phase-caused High/Critical findings. A zero-item remediation set is a valid recorded result.
- One remediation retry is the cap. Remaining drift is reported to final review rather than triggering an audit loop.
- The targeted verification addendum cannot replace or overwrite the full comparable reports.
- Worktree cleanup preserves pre-existing worktrees and runs only for a worktree created by this bookend.

## C. Consistency & Architecture Fit

- Follow the existing `all-approved` evidence pattern: a non-green or missing gate sets `no` and continues to the final production review.
- Reuse `<phase-baseline>` already resolved for Step 5 instead of deriving a second baseline.
- Reuse the Step 2.5/Step 3 bounded implementer re-spawn shape for remediation; do not define a new plan-driven feature flow for one repair set.
- Load the exact finalized skill slug from Feature 08. The new skill owns sequencing; `auditor-conventions` owns comparability; `audit-delta-report` owns documents.
- Cross-feature API contract consumed from Feature 08: caller supplies the finalized audit types, scoped/full decision, identical prompt body, roots, labels, output paths, and continuation policy; the skill returns report/delta/attribution/cleanup state for `all-approved` and Step 6.
- Existing exact names are copied from the Phase document and verified in source frontmatter: `Auditor - Code`, `Auditor - Infra`, `Auditor - Delta`, `Auditor - Attribution`, and `Baseline Worktree`.
- Relationship: this feature depends only on the skill contract, so it may run beside `09-audit-delta-rewire` in Wave 2. `11-audit-bookend-guards` waits for both consumers and validates the integrated topology and order.

### Unverified Assumptions

- The precise heading label/number for the inserted bookend step must fit the existing numbered sequence while remaining between Step 5 and Step 6. The phase specifies the position, not the final sub-step name.
- The exact machine-readable field names used to carry bookend evidence into Step 6 are implementation choices and must not be presented as established APIs unless already present.

## D. Clean Design & Maintainability

- Keep Step 1 responsible for cheap, up-front scope and decision work.
- Keep the new end-of-run step responsible only for phase-specific inputs, leaf spawns, remediation policy, and evidence recording.
- Reference shared sequence and document contracts rather than restating them.
- Use one prompt template and explicit parameter slots.
- Keep audit-type branches independent and bounded.

### Keep It Clean Checklist

- [ ] Five exact leaf names in frontmatter; no orchestrator spawn.
- [ ] One skill reference; no copied sequence.
- [ ] One Step 1 question; no late prompt.
- [ ] One-hop scope with no numeric cap.
- [ ] One remediation attempt; no audit loop.
- [ ] Existing steps preserved.
- [ ] No generated-output edits.

## E. Completeness: Observability, Security, Operability

- **Observability decision:** Add no normal-path logs. Persist decision state, scope count, audit-type reasons, report paths, reconciliation/attribution status, remediation outcome, verification addendum, and explicit skip/failure reasons in the existing phase evidence flow.
- **Security:** Target trees are read-only, outputs stay in the working checkout, and remediation touches only attributed phase-caused High/Critical findings. The existing diff security scan remains an independent input.
- **Runbook:** Run focused Phase 03 guards and the full suite, then manually exercise scoped run, decline, and one failure branch. Verify rendered prompts byte-for-byte except the three permitted fields, preserve the baseline worktree until attribution completes, and run one real `Audit - Delta` separately for the extraction. Roll back by removing Phase Execute wiring/frontmatter and the shared skill reference together. Propagation remains pending for the maintainer.

## F. Test Plan

| Acceptance Criteria | Evidence | Category |
|---|---|---|
| AC1–AC7 | Parse frontmatter and Step 1 sections; mutate roster, scope, audit-type, and decision obligations | Must-have automated test |
| AC8–AC15 | Validate workflow ordering, prompt parameterization, artifact root, delta gate, attribution arithmetic, and cleanup order | Must-have automated test; manual QA check for runtime identity/lifetime |
| AC16–AC19 | Negate severity/attribution/retry/addendum/`all-approved`/Step 6 clauses and require named failures | Must-have automated test; manual QA check for real bounded remediation |
| AC20 | Run corpus invariants and full repository suite against the recorded baseline | Existing test to update: no update expected; run as regression evidence |
| AC21 | Review for absence of new normal-path logging/state and confirm only planned artifacts are introduced | Code-review evidence only |

### Top Five High-Value Checks

1. Given a manifest with source and test paths, when Step 1 resolves scope, then it includes modified files plus exactly one uncapped reference hop, excludes standalone docs, and announces the count once.
2. Given baseline and current audit spawns, when rendered prompts are captured, then their bytes differ only at target root, snapshot label, and output directory.
3. Given a missing/partial report or unattributed provisional item, when the bookend reaches delta/presentation, then it refuses the invalid transition and marks evidence incomplete.
4. Given attributed Medium or pre-existing High findings, when remediation is selected, then neither is sent to the implementer; only phase-caused High/Critical findings are eligible once.
5. Given remediation output, when targeted verification completes, then the delta receives an explicitly non-comparable addendum and Step 6 receives the full outcome.

### Fixtures and Test Impact

- `11-audit-bookend-guards` creates the focused structural module and owns mutation/negation evidence for every new mechanism.
- `tests/test_agent_corpus_invariants.py`, `tests/test_unity_consumer_contract.py`, `tests/test_propagate_master_assets.py`, and `tests/test_pr_review_orchestrator.py` are existing regression inputs. They are not Phase 03 edit surfaces unless discovery during implementation proves a structural compatibility change is unavoidable.
- No Stage 0 is required. The current suite collected 268 tests and its red baseline is caused by existing corpus-name, generated-count/applyTo, and missing Unity reference-asset failures rather than missing Phase 03 test infrastructure.

## Stage 1: Frontmatter and Step 1 Decision
**Goal**: Add exact leaf availability, resolve audit scope, classify audit types, and record the one up-front user decision.
**Success Criteria**: AC1 and AC3–AC7 hold without changing existing bundle-validation behavior.
**Status**: Not Started

## Stage 2: End Audit and Attribution
**Goal**: Wire the shared comparison sequence after Step 5 using the phase baseline, working checkout, and identical prompt template.
**Success Criteria**: AC2 and AC8–AC15 hold with all artifacts under the working checkout.
**Status**: Not Started

## Stage 3: Bounded Remediation and Final Review Evidence
**Goal**: Repair eligible phase-caused drift once, verify it narrowly, and carry the complete outcome into Step 6.
**Success Criteria**: AC16–AC21 hold and every missing-evidence branch remains non-blocking but sets `all-approved: no`.
**Status**: Not Started
