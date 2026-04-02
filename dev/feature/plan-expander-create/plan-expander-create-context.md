# Feature Context: plan-expander-create

## Key Files

| File | Role | Change Type |
|------|------|-------------|
| `.github/agents/feature-plan-expander.agent.md` | New hidden subagent | Create |
| `.github/skills/feature-plan-set/SKILL.md` | Defines the three-file plan convention | Edit (ownership attribution) |
| `.github/instructions/dev-task-folder.instructions.md` | Producer table for dev/feature/ files | Edit (producer column) |

### Reference Files (read-only, for pattern following)

| File | Why |
|------|-----|
| `.github/agents/feature-decomposer.agent.md` | Pattern: agent that reads phase docs and writes plan files |
| `.github/agents/feature-implementer.agent.md` | Pattern: hidden subagent frontmatter and tools |
| `.github/agents/feature-reviewer.agent.md` | Pattern: hidden subagent frontmatter and tools |

## Architectural Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Agent scope | Reads `-plan.md`, writes `-context.md` and `-tasks.md` only | Minimal responsibility — single-purpose agent following the subagent convention. The Decomposer already gathered codebase context for the plan; the Plan Expander translates that into structured companion files. |
| Tools list | `[read, search, edit, run in terminal]` | Needs `read` and `search` to read plan files and codebase; `edit` to write output files; `run in terminal` for file system operations. Same pattern as Decomposer. |
| Codebase reading | Plan Expander reads the codebase to populate "Key Files" in context | The plan's traceability matrix references files, but the Plan Expander should verify they exist and add any additional relevant files discovered during its own codebase scan. |
| Skill reference | Agent body references `feature-plan-set` skill for template structure | Avoids duplicating template content in the agent body. Single source of truth for file formats. |

## Constraints

- The `-context.md` template structure must match what's defined in `feature-plan-set/SKILL.md`
- The `-tasks.md` template structure must match what's defined in `feature-plan-set/SKILL.md`
- Agent must be hidden (`user-invocable: false`) — only invoked by orchestrators
- Agent must support `[SUBAGENT-MODE]` invocation pattern

## Relationships to Sibling Plans

- **`decomposer-promote`** (prerequisite): Must complete first so the Decomposer's scope is narrowed to plan-only before the Plan Expander takes ownership of context + tasks.
- **`executor-renumber`** (dependent): The executor will invoke the Plan Expander as a subagent. Must be listed in the executor's `agents:` frontmatter.

## Suggested Implementation Order

This feature is **second** in the sequence: `decomposer-promote` → `plan-expander-create` → `executor-renumber`
