# Feature Tasks: executor-renumber

## Stage 1: Update Executor Frontmatter

- [ ] In `.github/agents/phase-execute.agent.md`, change `name:` from `03 Phase - Execute` to `04 Phase - Execute`
- [ ] In `.github/agents/phase-execute.agent.md`, add `Feature - Plan Expander` to the `agents:` list
- [ ] In `.github/agents/phase-execute.agent.md`, update `description:` to reflect the new pipeline (checks for existing plans, invokes Decomposer if missing, invokes Plan Expander, then runs implementation loop)

## Stage 2: Update Pipeline — Plan Check and Conditional Decomposition

- [ ] Rewrite Step 1 to add a plan-check phase: scan `dev/feature/*/` for existing `-plan.md` files
- [ ] If plans found: log that existing plans were detected, skip decomposition, proceed to Plan Expander step
- [ ] If no plans found: invoke `03 Feature - Decomposer` as subagent (update the invocation prompt to use the new agent name)
- [ ] Update the Decomposer invocation prompt to reference `03 Feature - Decomposer` (not `Feature - Decomposer`)
- [ ] After decomposition (or plan detection), verify all `-plan.md` files exist before proceeding

## Stage 3: Add Plan Expander Invocation Step

- [ ] Add a new step (between decomposition and implementation loop) that invokes `Feature - Plan Expander`
- [ ] Write the Plan Expander invocation prompt: provide all `dev/feature/[task-name]/` paths, ask it to generate `-context.md` and `-tasks.md` for each
- [ ] After Plan Expander returns: verify `-context.md` and `-tasks.md` exist for each feature
- [ ] Renumber subsequent steps (implementation loop, QA, final review, etc.) to account for the new step

## Stage 4: Verify Orchestrator Instruction applyTo

- [ ] Inspect `orchestrator-conventions.instructions.md` `applyTo` — confirm `**/phase-execute.agent.md` is present
- [ ] No changes expected (file is not renamed on disk) — mark as verified

## Stage 5: Update Upstream Agent References

### project-planner.agent.md
- [ ] Change all `@03 Phase - Execute` references to `@04 Phase - Execute`
- [ ] Update the pipeline diagram to show `03 Feature - Decomposer` as a separate step before `04 Phase - Execute`
- [ ] Verify the "Relationship to Phase - Refiner and Phase - Execute" section reflects the new numbering
- [ ] Verify the "Pipeline Next Step" section references `@04 Phase - Execute` (or keep it referencing `@02 Phase - Refiner` if that's the direct handoff)

### phase-refiner.agent.md
- [ ] Change all `@03 Phase - Execute` references to `@04 Phase - Execute`
- [ ] Update the "Where You Sit in the Pipeline" section to show `04 Phase - Execute`
- [ ] Update the "Pipeline Next Step" handoff message to reference `@04 Phase - Execute`
- [ ] Verify Entry A and Entry B pipeline descriptions reference the updated numbering
