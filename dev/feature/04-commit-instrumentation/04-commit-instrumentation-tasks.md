# 04 Commit Instrumentation Tasks

Plan note: the source plan does not include a Stage 0 test-bootstrap section. This repo is docs-only and currently has no configured automated test or lint runner, so validation for these tasks is targeted readback of the touched Markdown files.

## Stage 1: Add checkpoint to `01 Project - Planner`

- [ ] Insert a `Plan Affirmation` checkpoint in `.github/agents/01-project-planner.agent.md` after the user approval/finalization section.
- [ ] Use the exact message `eval: affirm plan` and scope the checkpoint to `docs/phases/` files created or modified in the current session.
- [ ] Keep the planner change additive; do not restructure unrelated instructions.
- [ ] Read back the planner file and confirm the checkpoint appears after the plan-approval flow.

## Stage 2: Add checkpoint to `02 Phase - Refiner`

- [ ] Locate the branch-open block introduced by `03-branch-lifecycle-migration` in `.github/agents/02-phase-refiner.agent.md`.
- [ ] Append the checkpoint `eval: affirm phase <slug>` at the end of that block without duplicating branch creation or hook-install steps.
- [ ] Document how to derive `<slug>` from the current phase branch name.
- [ ] Read back the refiner file and confirm the checkpoint appears after the branch-open guidance.

## Stage 3: Add checkpoint to `03 Feature - Decomposer`

- [ ] Add a `Feature Decomposition` checkpoint after the plan-writing section in `.github/agents/03-feature-decomposer.agent.md`.
- [ ] Use the exact message `eval: decompose <slug>` and include the branch-name derivation plus fallback behavior when not on a phase branch.
- [ ] Keep staging scoped to the `dev/feature/` files created in the active decomposition session.
- [ ] Read back the decomposer file and confirm the checkpoint follows the plan-writing guidance.

## Stage 4: Add sub-step commits to `04 Phase - Execute`

- [ ] Update `.github/agents/04-phase-execute.agent.md` so the feature loop emits checkpoints after implement, review, optional QA, and final review.
- [ ] Use the exact messages `eval: implement <task>`, `eval: review <task>`, `eval: qa <task>`, and `eval: final-review`.
- [ ] Replace the former end-of-feature Step D commit with the `eval: final-review` checkpoint instead of duplicating commits.
- [ ] Add explicit staging guidance that limits each checkpoint to the current feature directory and the source files changed by that feature.
- [ ] Note that the QA checkpoint is conditional and is skipped when QA generation is not requested.
- [ ] Read back the execute-loop section and confirm all four checkpoints are present in the correct order.

## Stage 5: Propagate to all copy files

- [ ] Propagate the finalized master-file edits to the matching OpenCode copies: `opencode/agents/01-project-planner.md`, `opencode/agents/02-phase-refiner.md`, `opencode/agents/03-feature-decomposer.md`, and `opencode/agents/04-phase-execute.md`.
- [ ] Propagate the finalized master-file edits to the matching Claude copies: `claude/agents/project-planner.md`, `claude/agents/phase-refiner.md`, `claude/agents/feature-decomposer.md`, and `claude/agents/phase-execute.md`.
- [ ] Verify all derived copies preserve platform-specific formatting while matching the master checkpoint behavior.
- [ ] Validate propagation against the live repo inventory, which currently contains eight derived files even though the plan text says "six copies."