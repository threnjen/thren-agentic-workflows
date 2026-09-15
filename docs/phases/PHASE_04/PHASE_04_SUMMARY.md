# Phase 4: Slim Phase Planning and Execution

**Status**: Implemented — maintainer propagation pending
**Depends on**: Phase 03
**Estimated complexity**: Large
**Cross-references**: `docs/phases/PHASE_03/PHASE_03_SUMMARY.md`, `docs/phases/PHASE_04/PHASE_04_DISCOVERY_CONTEXT.md`

## What's New

Phase execution becomes a schedule-and-build workflow. One planning agent owns decomposition, selection-time discovery, and later schedule revalidation without generating full context and task documents for every feature.

Phase Execute asks its questions once, builds features sequentially, and stops after optional QA and Prod Code Review. Local branch review moves to the separate Phase 05 command.

The obsolete planner and six orphaned closing-review agents are removed instead of remaining dormant.

## Problem

Phase Execute still coordinates more planning artifacts and closing review work than implementation needs. A selected feature receives a plan, context document, and task document whose responsibilities overlap, while the orchestrator carries a broad review roster after feature work ends.

The extra artifacts and review fan-out increase cost, duplicate evidence, and make the execution workflow harder to finish. They also mix implementation orchestration with the separate job of reviewing a completed branch.

## Objective

Reduce Phase Execute to one living feature schedule and a sequential build loop. Preserve the green-suite precondition, feature-level conformance review, integration gates, commit checkpoints, optional QA, and final production decision.

## Scope

### In Scope

- Consolidate Phase Execute planning under Feature Plan Author.
- Give Plan Author distinct `initial`, `select`, and `revalidate` modes.
- Write one lightweight `-plan.md` per feature during initial decomposition.
- Write one selection-time `-delta.md` for the chosen feature.
- Allow selection mode to patch only the selected plan when current source contradicts it.
- Restrict revalidation mode to execution-manifest fields and affected future features.
- Delete Feature Plan Expander from the agent corpus.
- Stop creating `-context.md` and `-tasks.md` for Phase Execute features.
- Update Phase Execute consumers to use the plan and delta pair.
- Preserve existing Audit and Test artifact contracts that still require context or task documents.
- Require shared consumers to select the Phase or Audit/Test artifact contract explicitly.
- Delete every orphaned Expander reference, route, test fixture, catalog entry, and contract clause.
- Ask session-model, QA, and applicable dirty-resume questions in one opening interaction.
- Preserve later questions required by the shared Departure Preflight, safety boundaries, or external blockers.
- Default optional phase QA to skipped unless the user selects it.
- Run the repository's full authoritative suite before planning or child-agent work.
- Stop immediately when the phase-start suite fails or cannot run.
- Build one feature at a time according to manifest prerequisites.
- Preserve implementation and review commit checkpoints.
- Run one Plan Conformance review-and-repair pass per feature.
- Run an integration gate after the review pass.
- Block a failing feature and its dependents without marking that feature complete.
- Restore the pre-feature green state before continuing an independent feature after a regression.
- Halt the phase when the pre-feature state cannot be restored without rewriting history.
- Remove the phase-close evaluator chorus, diff-security scan, consolidation, validation, and repair stages from Phase Execute.
- Delete each agent definition whose only caller was the removed Phase Execute stage.
- Generate and execute consolidated QA only when the user opted in.
- Ensure skipped QA does not set the final approval aggregate to failure.
- Run Prod Code Review after feature work and optional QA.
- Run Docs Writer only after `GO` or `GO WITH CONDITIONS`.
- Point the final user handoff at the existing `pr-review` command until Phase 05 replaces that surface.
- Update affected source definitions, shared skills, tests, and documentation.
- Recount the agent catalog from the completed source tree.

### Out of Scope

- Changing Audit or Test to use the plan-and-delta artifact pair.
- Keeping a dormant Feature Plan Expander or compatibility shim after its final caller is removed.
- Building features concurrently in one working tree.
- Removing the green-suite phase precondition.
- Treating a failing integration gate as a completed feature.
- Continuing independent work while a failed feature's changes remain in the shared working tree.
- Moving Prod Code Review outside Phase Execute.
- Making QA mandatory.
- Running local final checks from Phase Execute.
- Creating `phase-final-checks` or the `pr-review` alias.
- Changing the local-review evaluator roster.
- Posting or opening a merge request.
- Changing Bash standards or model-routing policy.
- Deleting agents merely to reach a count from another repository fork.
- Rewriting untouched agent families for prose style alone.
- Running source propagation as agent work.

## Key Deliverables

| # | Deliverable | Description | Likely Features |
|---|-------------|-------------|-----------------|
| 1 | Living plan and delta schedule | One planner owns initial decomposition, selected-feature discovery, and bounded revalidation; the superseded planner is deleted | Planning artifacts and manifest lifecycle |
| 2 | Schedule-and-build orchestrator | One opening interaction, sequential implementation, optional QA, Prod Code Review, conditional documentation, and no dormant close-review fleet | Execute loop and close behavior |

## Phase Artifact Responsibilities

| Artifact | Phase responsibility |
|----------|----------------------|
| Feature plan | Defines scope, acceptance criteria, dependencies, expected file impact, and verification intent. |
| Selection delta | Records verified key files, current constraints, existing verification assets, and discoveries that differ from the plan. |
| Execution manifest | Owns Environment State, verification assets, prerequisites, status, checkpoints, and bounded schedule revalidation. |
| Implementation record | Records completed acceptance criteria, changed files, test evidence, and unfinished work. |
| Review record | Records the single Plan Conformance pass, repairs, and unresolved findings. |

The Phase pipeline does not replace the task checklist with another checklist artifact. The implementer follows acceptance criteria and records progress in the implementation record. Durable checkpoints and manifest status own resume state.

Audit and Test keep their current plan, context, and task artifacts. Shared skills and agents must select their artifact contract from the invoking pipeline instead of inferring one universal bundle.

## User Flows

### Successful phase

1. The user attaches a refined phase document and answers the opening questions once.
2. Phase Execute proves the repository suite starts green.
3. Plan Author writes the feature plans and execution manifest.
4. Phase Execute selects one ready feature and requests its discovery delta.
5. The implementer and Plan Conformance reviewer complete one bounded feature loop.
6. Phase Execute runs the integration gate and revalidates the remaining schedule.
7. The loop continues until every unblocked feature finishes.
8. Optional QA runs only when selected.
9. Prod Code Review returns the phase verdict.
10. Docs Writer runs only after a positive production verdict.

### Red phase-start suite

1. Phase Execute runs the authoritative suite before planning.
2. The suite fails or cannot run.
3. Phase Execute reports the evidence and stops without spawning a child agent.

### Feature regression

1. A feature reaches its integration gate after its one conformance review pass.
2. The gate fails against the green phase baseline.
3. Phase Execute records the feature as blocked and leaves it incomplete.
4. Phase Execute restores and proves the pre-feature green state without rewriting branch history.
5. The manifest blocks the failed feature's dependents and may continue independent work.
6. Phase Execute halts when it cannot restore the pre-feature state.

### QA skipped

1. The user accepts the default `qa: no` choice in the opening block.
2. Phase Execute skips QA document generation and execution.
3. The missing QA artifacts do not count as failed approval evidence.
4. Prod Code Review evaluates the evidence the phase actually produced.

### Resume

1. Phase Execute reads the manifest and durable checkpoints for any in-progress feature.
2. A clean tree resumes automatically from the first incomplete checkpoint.
3. Relevant uncommitted implementation changes add a resume-or-restart choice to the opening block.
4. An inconsistent manifest or missing checkpoint stops with a concrete recovery requirement.

## Technical Context

- `source_of_truth/agents/03-phase-execute.agent.md` owns the current planning calls, feature schedule, review chorus, QA, Prod Code Review, and documentation handoff.
- `source_of_truth/agents/03o-feature-plan-author.agent.md` writes lightweight plans and the current execution manifest.
- `source_of_truth/agents/03a-feature-plan-expander.agent.md` was deleted after Plan Author absorbed its retained responsibilities.
- `source_of_truth/agents/03b-feature-implementer.agent.md`, `03c-reviewer-plan-conformance.agent.md`, `03d-feature-qa-writer.agent.md`, and `03f-prod-code-review.agent.md` consume feature planning artifacts.
- `source_of_truth/agents/03i-feature-qa-runner.agent.md` executes phase-scoped automated QA when present.
- `source_of_truth/skills/feature-plan-set/SKILL.md` defines the current plan, context, and task bundle.
- `source_of_truth/skills/implementation-pipeline-loop/SKILL.md` owns feature implementation, review, testing, commit checkpoints, and completion.
- `source_of_truth/skills/pipeline-artifacts/SKILL.md` maps pipeline producers to artifact names and consolidated QA locations.
- `source_of_truth/instructions/tech-stack-detection.instructions.md` and `read-only-agent.instructions.md` name planner and reviewer consumers that may change.
- `source_of_truth/instructions/learnings-bootstrap.instructions.md` also names Feature Plan Expander and must drop the dead target.
- The retired Phase-only close agents were `03j`, `03k`, `03l`, `03m`, `03n`, and `03p`. Their definitions and exclusive tests were deleted.
- `tests/test_merged_phase_execute_schedule.py`, `test_execution_manifest_schema.py`, `test_phase_02_pipeline_integration.py`, `test_phase_execute_contracts.py`, `test_session_model_preflight.py`, and `test_audit_comparison_contracts.py` guard the current pipeline.
- `tests/test_agent_renumbering.py`, `test_model_routing.py`, `test_agent_corpus_invariants.py`, `test_retirement_reconciliation.py`, and `test_propagate_master_assets.py` guard agent identity, routing, source relationships, and generated inventory.
- `source_of_truth/` is the only authoring surface. The maintainer owns propagation into `ports/` and `.github/`.

Suggested implementation shape, to be verified by Phase Execute against current source and tests: preserve stable agent identities unless a behavior requires a rename. Do not renumber the corpus for presentation alone.

## Dependencies & Risks

- **Dependency**: Phase 03 established the green phase-start suite, one conformance review pass, and the rule that failing features never complete.
- **Dependency**: shared implementer, reviewer, QA, and Prod Code Review agents must accept the plan-and-delta pair without breaking Audit or Test callers.
- **Risk**: changing shared artifact language can silently change Audit and Test. Mitigation: scope the new bundle by pipeline mode and retain their existing context and task contracts.
- **Risk**: removed task checkboxes can leave no durable progress signal. Mitigation: make implementation-record acceptance-criteria status, checkpoints, and manifest status the only Phase progress signals.
- **Risk**: removing the close stage can leave its agents dormant. Mitigation: delete every definition with no remaining caller and preserve needed local-review behavior through live Phase 05 agents.
- **Risk**: deleting Plan Expander can strand its environment-state or discovery responsibilities. Mitigation: assign every retained responsibility to Plan Author before deleting the agent.
- **Risk**: dead Expander references can survive in instructions, routing, tests, catalogs, or shared contract prose. Mitigation: search the full authored corpus and delete every reference that has no live consumer.
- **Risk**: revalidation can become an unbounded replanning loop. Mitigation: let Plan Author own one explicit graph-round bound and restrict output to manifest fields.
- **Risk**: removing the review chorus can leave dangling roster, prompt, approval, or staging references. Mitigation: remove each producer and consumer reference in the same feature.
- **Risk**: the external reference allows a failing feature to proceed. That conflicts with the repository's green-baseline rule. Mitigation: keep the feature incomplete, block dependents, and continue only independent work.
- **Risk**: a committed failing feature contaminates later independent work. Mitigation: require recorded, non-history-rewriting recovery to the pre-feature green state before the schedule continues.
- **Risk**: source edits make generated-sync tests fail until the maintainer propagates. Mitigation: inventory propagation-dependent checks and classify only proven source-to-generated divergence as pending propagation.
- **Risk**: skipped QA may still be inferred as missing evidence. Mitigation: exclude skipped QA explicitly wherever approval is computed, passed, and reported.
- **Risk**: Docs Writer may run after a negative verdict and make unrelated changes. Mitigation: gate it strictly on `GO` or `GO WITH CONDITIONS`.
- **Risk**: source and generated assets will diverge after authoring. Mitigation: stop with propagation pending and state which sync tests are expected to fail.

## Success Criteria

- [x] Initial planning writes one lightweight plan per feature and one execution manifest.
- [x] Initial planning does not write context, task, or delta files.
- [x] Selection mode writes exactly one delta for the chosen feature.
- [x] Selection mode may patch only the chosen plan and only when current source contradicts it.
- [x] The delta identifies key files, existing verification assets, and discoveries that differ from the plan.
- [x] The execution manifest owns Environment State, verification assets, prerequisites, checkpoints, and schedule status.
- [x] The implementation record owns acceptance-criteria progress and unfinished work without creating a replacement task checklist.
- [x] Revalidation changes only manifest fields for affected future features and their dependents.
- [x] Plan Author owns a finite graph-round bound, and Phase Execute handles a tripped bound without restating its value.
- [x] Phase Execute features consume their plan and delta without requiring context or task files.
- [x] Audit and Test retain their existing context and task artifact contracts.
- [x] Shared consumers select an explicit Phase, Audit, or Test artifact contract and never infer one universal bundle.
- [x] Feature Plan Expander's source definition is deleted.
- [x] No live instruction, route, test, catalog, plan contract, or orchestrator references Feature Plan Expander.
- [x] No compatibility shim or dormant replacement preserves the deleted agent's responsibility.
- [x] An end-to-end Phase Execute contract run completes from planning through Prod Code Review without a context or task file.
- [x] The opening interaction always covers session-model preflight and the optional QA choice.
- [x] The opening interaction shows resume only when an in-progress feature and relevant dirty implementation files both exist.
- [x] Phase Execute asks no later scope, configuration, or routine workflow questions after the opening interaction.
- [x] A later Departure Preflight, safety boundary, or external blocker may still require its shared-contract question.
- [x] The authoritative full suite runs before planning or child-agent work.
- [x] A failing or unrunnable phase-start suite stops the run before any child agent starts.
- [x] Phase Execute builds no more than one feature at a time.
- [x] Every selected feature follows implementation checkpoint, one conformance review checkpoint, integration gate, and completion recording in that order.
- [x] The conformance reviewer gets one review-and-repair pass and is not respawned for the same feature.
- [x] A failing integration gate leaves the feature incomplete and blocks its dependents.
- [x] Independent features continue only after Phase Execute restores and proves the pre-feature green state without rewriting history.
- [x] Failure to restore the pre-feature green state halts the phase.
- [x] A clean interrupted run resumes automatically from its first incomplete durable checkpoint.
- [x] A dirty interrupted run presents its resume choice in the opening interaction.
- [x] Phase Execute does not spawn phase-close blast-radius, test-falsification, plan-blind, cleanliness, consistency, dependency, test-health, security, consolidation, validation, or fixer agents.
- [x] QA generation and execution occur only when the user selects `qa: yes`.
- [x] Skipped QA does not set the approval aggregate to failure.
- [x] Prod Code Review runs after the feature loop and any selected QA.
- [x] Prod Code Review receives plan, delta, implementation, review, test, QA, and manifest evidence that exists for this run.
- [x] Docs Writer runs only after `GO` or `GO WITH CONDITIONS` and never after `NO-GO`.
- [x] Phase Execute's closer points to `pr-review` until Phase 05 changes the local command surface.
- [x] Contract tests fail when the green precondition, one-review bound, failure blocking, QA exclusion, or documentation gate is removed.
- [x] Catalog documentation reports counts measured from the completed source tree.
- [x] Authored changes stay within `source_of_truth/`, `tests/`, and repository documentation before maintainer propagation.
- [x] A post-change full-suite result distinguishes proven propagation-dependent failures from every other regression.
- [x] No generated file under `ports/` or `.github/` is edited by an agent.

## QA Considerations

- No product UI changes.
- Automated contract tests must distinguish Phase Execute artifacts from Audit and Test artifacts.
- Mutation-style guards must prove that the opening interaction, phase-start halt, single review pass, integration blocking, QA default, and Docs Writer gate can fail.
- Run focused pipeline, manifest, corpus, retirement, and propagation tests before the full suite.
- A manual dry read must follow successful, phase-start failure, feature-blocked, QA-skipped, QA-selected, and resume flows without inventing a later question.
- Port synchronization tests may remain red after source edits until the maintainer runs propagation.
- The run must name each propagation-dependent failure. Any unrelated failure blocks the feature.

## Implementation Evidence

- Feature Plan Author implements `initial`, `select`, and `revalidate` modes.
- Shared consumers require `pipeline: phase | audit | test` and select the matching artifact contract.
- Feature Plan Expander and six orphaned Phase-only review agents have no source definitions.
- Phase Execute contains no closing evaluator fleet and delegates one Plan Conformance pass per feature.
- Focused Phase, manifest, routing, retirement, preflight, and Unity contracts pass.
- The full suite has only propagation-dependent failures while generated outputs remain untouched.
