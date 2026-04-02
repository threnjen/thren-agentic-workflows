# Feature Tasks: plan-expander-create

## Stage 1: Create Plan Expander Agent File

- [ ] Create `.github/agents/feature-plan-expander.agent.md` with YAML frontmatter:
  - `name: Feature - Plan Expander`
  - `description:` — e.g., "Reads feature plan files and generates companion context and tasks files."
  - `tools: [read, search, edit, run in terminal]`
  - `model: <model>`
  - `user-invocable: false`
- [ ] Write agent body with role description: reads `-plan.md` files, generates `-context.md` and `-tasks.md`
- [ ] Write "Required Input" section: one or more `dev/feature/[task-name]/` paths containing `-plan.md` files
- [ ] Write workflow section:
  - Step 1: Read each provided `-plan.md` file
  - Step 2: Read the codebase to identify key files referenced in the plan's traceability matrix
  - Step 3: Generate `-context.md` with key files, architectural decisions from the plan, constraints, and sibling plan relationships
  - Step 4: Generate `-tasks.md` with an ordered checklist derived from the plan's stages and acceptance criteria
- [ ] Write "Return Value" section for subagent mode: list of files generated, summary of key decisions captured
- [ ] Add reference to `feature-plan-set` skill for template structure
- [ ] Include note that the agent operates autonomously in subagent mode (no user approval needed)

## Stage 2: Update feature-plan-set Skill

- [ ] In `.github/skills/feature-plan-set/SKILL.md`, update the opening paragraph to reflect split ownership: plan files produced by Feature - Decomposer, context and tasks files produced by Feature - Plan Expander
- [ ] Verify the Context File and Tasks File sections are clear enough for the Plan Expander to follow (no content changes expected — just verify)

## Stage 3: Update dev-task-folder Instruction

- [ ] In `.github/instructions/dev-task-folder.instructions.md`, change the Producer column for `-context.md` from `Feature - Decomposer` to `Feature - Plan Expander`
- [ ] In `.github/instructions/dev-task-folder.instructions.md`, change the Producer column for `-tasks.md` from `Feature - Decomposer` to `Feature - Plan Expander`
- [ ] Verify `-plan.md` row still shows `Feature - Decomposer` as producer
