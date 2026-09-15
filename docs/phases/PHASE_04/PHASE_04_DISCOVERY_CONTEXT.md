# Phase 04 Discovery Context

## Source Material

- `slim-implementation-pipeline.md` is a behavioral reference copied from another project fork.
- The reference document is not an acceptance contract for this repository.
- Its branch status, fixed agent counts, phase links, and implementation history do not apply here.
- The branch `phase/phase-05e-descendant-ownership-closure-05d-phase-close` belongs to that external fork and is outside this phase's evidence.

## Current Repository Baseline

- Phase 03 is complete and is this phase's direct dependency.
- Feature Plan Author now owns lightweight plans, selected-feature deltas, and manifest revalidation.
- Phase Execute now owns sequential implementation, one conformance pass, optional QA, and Prod Code Review.
- The repository begins phase execution from a green full-suite precondition.
- A feature regression blocks that feature and its dependents. Independent features may continue only after the shared tree returns to its pre-feature green state.
- Agent counts must be derived from the finished source tree. No external count is a deletion target.

## Decisions Carried Into This Phase

- Split execution slimming and local-review unification into Phase 04 and Phase 05.
- Keep Phase 04 limited to planning and execution.
- Delete Feature Plan Expander after its final Phase Execute caller is removed.
- Delete every closing-review agent left without a caller after Phase Execute is slimmed.
- Delete all dead files, references, routes, fixtures, and contract text created by consolidation.
- Do not retain dormant agents or compatibility shims for responsibilities with no live caller.
- Preserve Audit and Test artifact contracts.
- Move Phase Environment State and verification assets into the execution manifest.
- Move Phase acceptance-criteria progress and unfinished work into the implementation record.
- Do not replace the deleted task file with another checklist artifact.
- Preserve sequential implementation and existing commit checkpoints.
- Make QA opt-in with a default of no.
- Run Docs Writer only after a positive Prod Code Review verdict.
- Exclude unrelated Bash standards, model-routing changes, and wholesale prose rewrites.
- Defer Phase Final Checks, review aliasing, and local-review roster work to Phase 05.

## Verification Guidance

- Verify every behavior against the current source before implementation.
- Search every shared artifact suffix across agents, skills, instructions, tests, and documentation.
- Search the full authored corpus for Feature Plan Expander before deleting it, then prove no live reference remains.
- Treat a retained but unspawned agent as failed consolidation, not harmless compatibility.
- Treat a failing integration gate as a blocker, even where the external reference suggests proceeding.
- Distinguish propagation-dependent synchronization failures from production or contract regressions after source edits.
- Resume a clean interrupted feature from durable checkpoints. Ask only when relevant uncommitted changes create a real choice.
- Reconcile each removed phase-close producer with its roster, consumer, approval, staging, and documentation references.
- Stop after source edits with propagation pending.
