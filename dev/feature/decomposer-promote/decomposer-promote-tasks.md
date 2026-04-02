# Feature Tasks: decomposer-promote

## Stage 1: Update Frontmatter

- [ ] In `.github/agents/feature-decomposer.agent.md`, change `name:` from `Feature - Decomposer` to `03 Feature - Decomposer`
- [ ] In `.github/agents/feature-decomposer.agent.md`, remove the `user-invocable: false` line
- [ ] In `.github/agents/feature-decomposer.agent.md`, update `description:` to reflect plan-only scope (e.g., "Breaks a refined Phase document into independent features, producing a plan file per feature.")

## Stage 2: Update Agent Body to Plan-Only Output

- [ ] In "What You Do and Don't Do" section, change the deliverables line to reference only `-plan.md` files
- [ ] Remove `-context.md` and `-tasks.md` from the `You create:` list
- [ ] Update the file structure diagram to show only `[task-name]-plan.md` (remove context and tasks entries)
- [ ] In Phase 3 ("Make Decisions and Write Documents"), update instructions to produce only `-plan.md` per feature
- [ ] Remove or update any references to writing context files (e.g., "Note what you chose and why in the plan's context file" → move decision documentation into the plan itself or note it's for the Plan Expander)
- [ ] Update "When writing multiple plans" note — sibling plan relationships should be noted in the plan file itself since context files are no longer produced by this agent

## Stage 3: Update Standalone and Subagent Messaging

- [ ] In "Return Value > Standalone mode" block quote, change `@03 Phase - Execute` to `@04 Phase - Execute`
- [ ] In "Return Value > Standalone mode" block quote, update the message to reflect plan-only output (remove references to context/tasks handoff)
- [ ] In "Return Value > Subagent mode" list, update to describe returning plan file names only (no context/tasks)

## Stage 4: Verify Read-Only Instruction

- [ ] Inspect `read-only-agent.instructions.md` `applyTo` field — confirm `**/feature-decomposer.agent.md` is present
- [ ] No changes expected — mark as verified
