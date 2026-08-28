# Phase 3: Phase Execute Loop Simplification

**Status**: Complete
**Depends on**: Phase 02
**Estimated complexity**: Medium
**Cross-references**: `docs/phases/PHASE_02/PHASE_02_SUMMARY.md`

## What's New

Running a phase used to take about a day and often never finished. The pipeline reviewed every feature with a committee of seven agents, argued with itself about the findings, repaired, then reviewed again — and the second review always reported more problems than the first, because reviewers subdivided the same issues rather than finding new ones. Runs commonly stalled on the first feature and never reached the second.

After this phase, each feature is built, reviewed once by a single agent that also applies its own fixes, and tested. Anything that agent cannot fix in its one round is written down and looked at again when the phase closes. The full review committee runs once, at the end, over the finished phase. There is one repair round, then QA, then a go/no-go. The feature loop costs about a quarter of the agents it used to, and a whole four-feature phase costs less than half.

## Problem

`03 Phase - Execute` does not finish. Runs stall during remediation on the first feature and never reach the second. A phase that completes takes about twenty-four hours.

The stall has one cause. Every per-feature review cycle produces more findings than the last, and the increase is granularity, not defects — the same problems restated more finely. A reviewer's only exit condition is having written a report, which it can satisfy at any level of detail. Nothing bounds how many findings are produced. Four separate fixes have been applied downstream of that leak — a Consolidator to deduplicate, a Validator to prove, a supported-path matrix to bound retries, immutable cycle directories to compare across rounds. Each filtered findings after production and each added an agent to the critical path.

The end-of-phase repair step has a second form of the same problem. It repairs, then re-materializes the phase diff and re-runs every auditor against a diff its own repair just changed.

Users are frustrated, and so is the maintainer.

## Objective

Give every review step in the pipeline a natural stopping point, and delete the machinery that existed to manage steps that had none. Per-feature review becomes one agent with a finite checklist. The committee runs once, at phase close, where running once is its natural shape.

## Scope

### In Scope

- Collapse the per-feature review committee and fix loop into a single review-and-fix agent, running one round per feature
- Grant `edit` to `03c Reviewer - Plan Conformance` in place, and detach the read-only-agent instruction from it. The agent keeps its number, its name, and all seventeen existing references
- Give that agent one round per feature. A defect it finds and cannot fix in that round is written into the implementation record in a form the phase-close Consolidator can match, and the feature completes. The reviewer never blocks a feature on its own unrepaired finding
- Retire the rule "the implementer never applies its own review findings" for the feature loop only. The reviewer and the implementer stay separate agents there; the reviewer now applies what it finds. The rule stands unchanged at phase close, where `03p Feature - Fixer` remains a distinct agent from every reviewer
- Move the full reviewer roster to phase close, running once. The roster is nine agents in three classes:
  - **Repair-eligible (four)**: `03e Diff Security`, `03j Blast Radius`, `03k Test Falsification`, `03l Plan Blind`
  - **Conditional (two)**: `04e Dependency Auditor`, `03h Unity Reviewer` — each fires only when its trigger condition holds
  - **Advisory only (three)**: `04h Cleanliness`, `04d Consistency`, `04f Test Health` — reported, never auto-repaired
- Consolidate all nine phase-close reports into one deduplicated candidate list; validate only the four repair-eligible lanes
- Run one phase-close repair round with no re-run of the audits. Two gates apply in order: a lane is repair-eligible by blast radius, and within an eligible lane a finding enters the fix list only at Validator-confirmed Critical, Blocker, or High. The blast-radius rule recorded in `cross-phase-decisions.md` is preserved, not superseded — the advisory-only class is that rule expressed as a roster class, and `04d` consistency drift stays excluded because its fix spans every feature's files
- Verify the phase-close repair with the orchestrator's own regression run over the affected suites. Running tests is not re-running the audits, and a fixer self-report is not evidence
- Reorder QA to run after the phase-close repair, so it measures final code
- Define the feature test gate as a baseline comparison: no test that passed before a feature may fail after it. Record the phase-start baseline, naming every already-failing test, and repair the test environment before the first feature runs
- Retire the per-feature review-cycle directory scheme, the two-round fix loop, the plan rewrite, the rebuild, the post-rebuild review pass, and the second audit pass
- Update guard tests that assert on the retired pipeline structure
- Update `PROJECT_ROADMAP.md`, including Phase 02's now-superseded description

### Out of Scope

- The user-facing reporting language. Deferred deliberately — a simpler pipeline has fewer state tokens to leak, and the remaining density should be measured after this phase rather than guessed at now
- Step 1 schedule establishment, `Feature - Plan Author`, and the manifest format
- Step 7 documentation update
- Any change to `04 PR Review` or `audit-remediation-pipeline`, which have their own reviewer scopes

## Key Deliverables

| # | Deliverable | Description | Likely Features |
|---|-------------|-------------|-----------------|
| 1 | Review-and-fix agent | `03c` gains `edit`, loses the read-only instruction, and gains the one-round and unfixed-defect-record contract | Agent authoring |
| 2 | Simplified feature loop | Stages collapse to expand, implement, review-and-fix, test gate, complete | `03-phase-execute` Step 2 |
| 3 | Phase-close chorus | Nine reviewers, Consolidator over all, Validator over four, one repair round, no re-run | `03-phase-execute` Steps 3–4 |
| 4 | QA reorder | QA moves after the repair round | `03-phase-execute` step order |
| 5 | Roster and guards | Orchestrator frontmatter, structural guard tests, roadmap and learnings synced. No agent is deleted — every chorus member, the Consolidator, the Validator, and the Fixer all survive | Corpus cleanup |

## Technical Context

- `source_of_truth/agents/03-phase-execute.agent.md` — the orchestrator. Step 2 runs A implement, B review-and-fix, D test gate, E complete. Step 3 is the phase-close review: 3a spawns the nine-agent roster in three classes, 3b consolidates all nine and validates four, 3c repairs once with no audit re-run. Step 4 is QA, so it measures the repaired code. Step 5 is unchanged
- `source_of_truth/agents/03c-reviewer-plan-conformance.agent.md` — the review-and-fix agent. It holds `tools: [read, edit, search, execute, todo]` and sits outside the read-only-agent enumeration, mirroring `03p Feature - Fixer`. Seventeen files reference it, five of them instruction `applyTo` globs, which is why it changed in place rather than moving to a new number
- `source_of_truth/agents/03l-reviewer-plan-blind.agent.md` — stays, moves to phase close
- `03m Finding Consolidator`, `03n Finding Validator`, `03p Feature - Fixer` — survive at phase close only
- `source_of_truth/skills/implementation-pipeline-loop` — defines the checkpoint scheme the feature loop emits. Its Committee Review and Fix Loop section is retired; Step B is one review-and-fix call
- `scripts/propagate_master_assets.py` — agents author under `source_of_truth/` only, then run this script to convergence. The regenerated `ports/` and `.github/` output is committed with the source change
- `docs/learnings/project-learnings.md` — contains the four prior diagnoses this phase supersedes
- `.venv` is gitignored and rebuilt with `uv venv .venv --python 3.12` plus `requirements-dev.txt`. The phase-start baseline is recorded in `docs/phases/PHASE_03/PHASE_03_TEST_BASELINE.md` and is fully green, with no exempt tests
- Any edit under `source_of_truth/` requires a propagation run before the suite passes. `test_retirement_reconciliation.py::test_committed_tree_is_at_a_propagation_fixed_point` fails until `scripts/propagate_master_assets.py` has run to convergence and the regenerated `ports/` and `.github/` output is committed

## Dependencies & Risks

- **Dependency**: the Phase 03 numbering rule in `cross-phase-decisions.md`. Any agent authored here uses post-renumber numbering. This phase authors no new agent identity, so the rename surface stays empty
- **Dependency**: a runnable test environment. Three success criteria are measured only by a live run
- **Risk**: guard tests may pass against retired pipeline text. `project-learnings.md` records that a contract test locating its section by heading string cannot tell a live section from a commented-out one. Mitigation: delete retired sections outright rather than commenting them, and confirm each affected guard goes red before it goes green
- **Risk**: removing the per-feature committee removes the only early catch for accretive defects. Mitigation: the per-feature integration test gate stays, and Plan Conformance repairs contract failures at the feature where they enter
- **Risk**: an unfixed per-feature defect is recorded and then never re-found by the chorus, so it ships. Mitigation: the record is written in the Consolidator's finding shape, and the chorus reviews the same code at phase close
- **Risk**: the baseline exemption list goes stale and silently widens, exempting failures a feature actually caused. Mitigation: the baseline is empty, so any failing test during this phase is a regression. Nothing is added to the list during the phase
- **Risk**: one repair round means a wasted fix is a fix not available elsewhere. Mitigation: the Validator gates the fix list to independently confirmed Critical, Blocker, and High production defects
- **Risk**: with the audit re-run removed, the phase-close fix has no auditor to re-measure it. Mitigation: the orchestrator's regression run over the affected suites is the check, and Prod Code Review sees the fix-list outcome alongside the consolidated findings
- **Risk**: the orchestrator's `agents:` list names twenty agents by mixed conventions, some numbered and some not. No entry went stale, because no agent was deleted. The exposure is that a body may spawn an agent by its filename rather than its `name:`, which resolves to nothing. Mitigation: a guard resolves every `Spawn **X**` in the orchestrator against the agent names on disk

## Success Criteria

- [ ] A phase with three or more features runs to completion without stalling on any feature
- [ ] The test suite starts and runs to a verdict from a clean checkout
- [ ] A feature passes its gate when the suite is red only with tests named in the phase-start baseline, and fails when any other test fails
- [ ] `03c` grants `edit` and no longer carries the read-only-agent instruction
- [ ] `03c`'s contract states one round per feature and names the record where an unfixed defect is written
- [ ] A guard test fails if the one-round bound or the unfixed-defect record is removed from `03c`'s text
- [ ] A feature whose reviewer leaves a defect unfixed still completes, and the defect appears in the phase-close candidate list
- [ ] No step in the pipeline runs a second time against input its own repair modified
- [ ] Per-feature agent count is four: expander, implementer, review-and-fix, revalidation
- [ ] Phase-close review runs exactly once, with no second audit pass
- [ ] The phase-close repair round accepts only Validator-confirmed Critical, Blocker, and High findings drawn from the four repair-eligible lanes
- [ ] No advisory-only lane's findings reach the fix list, and `04d` consistency drift in particular is never auto-repaired
- [ ] The orchestrator runs the affected suites itself after the phase-close repair, and records the result
- [ ] Prod Code Review receives one deduplicated finding list covering all nine lanes, not nine reports
- [ ] QA results describe the code that Prod Code Review evaluates
- [ ] Every guard test asserting on the retired structure fails before the change and passes after
- [ ] Total agent spawns for a four-feature phase drop by at least half against the count recorded in the baseline run below
- [ ] Per-feature spawns for the same phase drop by at least three quarters

## QA Considerations

- No UI. Manual QA is limited to reading a completed run's outputs
- The real acceptance test is a live phase run against a real repository. Structural guard tests confirm the agent text, not that the pipeline terminates
- Propagation to `ports/` and `.github/` is a manual maintainer step and is not verified by this phase's tests
- Three success criteria — completion without stalling, per-feature spawn count, and total spawn count — are measured only by a live run. Record a baseline first: run one phase of three or more features on the current pipeline, or read the spawn counts from the most recent completed run's manifest and checkpoints. Count a spawn as one agent invocation logged by the orchestrator. Compare the same phase shape after the change

## Notes for Phase - Execute

Suggested feature boundaries, in dependency order:

1. **Repair the environment, record the baseline, and change `03c`.** Rebuild the virtualenv so the suite runs, record the phase-start baseline naming every already-failing test, then grant `03c` its edit bit and its one-round contract. The environment work comes first because every later feature's gate is measured against that baseline
2. **Rewrite Step 2.** Collapse stages B and C to a single review-and-fix call. Delete the review-cycle directory scheme and the rebuild path
3. **Rewrite Steps 3 and 4.** Chorus, consolidation split, one repair round, QA reorder. Renumber the orchestrator's own steps
4. **Roster and guards.** Orchestrator frontmatter, guard tests, roadmap, learnings. No agent deletions

Keep features 2 and 3 separate. They touch the same file but change different responsibilities, and merging them makes the diff unreadable at review.

Feature 4 must run last. Guard tests cannot be updated until the text they assert on is final.
