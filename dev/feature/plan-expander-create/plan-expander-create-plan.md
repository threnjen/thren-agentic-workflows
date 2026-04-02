# Feature Plan: plan-expander-create

**Phase**: Phase 01 — Split Feature Decomposer from Phase Execute
**Feature**: Create the new `feature-plan-expander.agent.md` hidden subagent
**Implementation order**: 2 of 3 (depends on `decomposer-promote` completing first)

---

## A. Requirements & Traceability

### Acceptance Criteria

| ID | Criterion |
|----|-----------|
| AC1 | `.github/agents/feature-plan-expander.agent.md` exists as a new file |
| AC2 | Frontmatter has `name: Feature - Plan Expander`, `user-invocable: false`, appropriate `description`, `tools`, and `model` fields |
| AC3 | Agent reads existing `-plan.md` files from `dev/feature/[task-name]/` and generates `-context.md` and `-tasks.md` in the same directory |
| AC4 | Agent body includes clear instructions for generating context file content (key files, decisions, constraints, sibling relationships) |
| AC5 | Agent body includes clear instructions for generating tasks file content (ordered checklist derived from plan stages) |
| AC6 | Agent supports subagent mode (invoked by `04 Phase - Execute` with `[SUBAGENT-MODE]` prefix) |
| AC7 | `feature-plan-set/SKILL.md` updated to reflect split ownership — plan by Decomposer, context+tasks by Plan Expander |
| AC8 | `dev-task-folder.instructions.md` producer table updated — `-context.md` and `-tasks.md` rows attribute producer to `Feature - Plan Expander` |

### Non-Goals

- Do NOT change the `-plan.md` template content (sections A–F)
- Do NOT change the `-context.md` or `-tasks.md` content templates (just changing who produces them)
- Do NOT modify the Decomposer agent (that was `decomposer-promote`)
- Do NOT modify the executor (that is `executor-renumber`)
- Do NOT update README.md or CODEBASE_CONTEXT.md

### Traceability Matrix

| Acceptance Criteria | Files to Modify/Create | Verification |
|---------------------|----------------------|--------------|
| AC1 | `.github/agents/feature-plan-expander.agent.md` (create) | File exists |
| AC2 | `.github/agents/feature-plan-expander.agent.md` (frontmatter) | Inspect frontmatter fields |
| AC3 | `.github/agents/feature-plan-expander.agent.md` (body) | Review workflow — reads plans, writes context + tasks |
| AC4 | `.github/agents/feature-plan-expander.agent.md` (body) | Context generation instructions present |
| AC5 | `.github/agents/feature-plan-expander.agent.md` (body) | Tasks generation instructions present |
| AC6 | `.github/agents/feature-plan-expander.agent.md` (body) | Subagent mode documented |
| AC7 | `.github/skills/feature-plan-set/SKILL.md` | Ownership attribution updated |
| AC8 | `.github/instructions/dev-task-folder.instructions.md` | Producer column updated for context + tasks rows |

## B. Correctness & Edge Cases

### Key Workflows

1. **Executor invokes Plan Expander after Decomposer** — Plan Expander receives path(s) to `-plan.md` files, reads each, generates corresponding `-context.md` and `-tasks.md`
2. **Multiple plans in one invocation** — Plan Expander should handle being given multiple `dev/feature/[task-name]/` paths and generate files for all of them
3. **Plan file references codebase files** — Plan Expander reads the plan's traceability matrix and file references to populate the context file's "Key Files" section

### Failure Modes

- If `-plan.md` doesn't exist at the specified path, the agent should report the missing file rather than generating empty documents
- If the plan is incomplete (e.g., missing sections), the agent should still generate best-effort context and tasks from available content

### Error Handling Strategy

- Report missing or malformed plan files to the invoking orchestrator
- Generate what's possible from available plan content

## C. Consistency & Architecture Fit

### Existing Patterns to Follow

- **Hidden subagent convention**: `user-invocable: false` in YAML frontmatter (same as Feature - Implementer, Feature - Reviewer, etc.)
- **Agent frontmatter fields**: `name`, `description`, `tools`, `model`, `user-invocable`
- **All agents use `<model>`** (except Docs Writer)
- **Tools pattern**: Read-oriented agents use `[read, search, edit, run in terminal]` — Plan Expander needs `edit` to write files
- **Subagent invocation**: Uses `[SUBAGENT-MODE]` prefix prompts
- **Context file pattern**: Follow the structure defined in `feature-plan-set` skill's "Context File" section
- **Tasks file pattern**: Follow the structure defined in `feature-plan-set` skill's "Tasks File" section

### Deviations

- None. This follows established hidden subagent patterns exactly.

### Interfaces

- **Input**: One or more `dev/feature/[task-name]/` paths containing `-plan.md` files
- **Output**: `-context.md` and `-tasks.md` files written to the same directories
- **Return value (subagent mode)**: List of files generated, summary of key decisions captured in context files

## D. Clean Design & Maintainability

### Simplest Design

The Plan Expander is intentionally minimal:
1. Read the plan file(s)
2. Read the codebase (to populate key files in context)
3. Generate context file from plan's decisions/constraints + codebase references
4. Generate tasks file as an ordered checklist derived from the plan's stages

No complex logic — it translates plan structure into two companion documents.

### Complexity Risks

- Low. The agent is a straightforward document generator.
- Risk of content drift between Decomposer plans and Expander context/tasks if the plan template changes. **Mitigation**: Both agents reference the `feature-plan-set` skill as single source of truth.

### Keep It Clean Checklist

- [ ] Agent body is minimal — no duplicated template content from the skill
- [ ] Agent references `feature-plan-set` skill for template structure
- [ ] No overlap with Decomposer responsibilities

## E. Completeness: Observability, Security, Operability

- **Logging/metrics/tracing**: Not applicable (Markdown docs)
- **Security**: Not applicable
- **Runbook**: Not applicable — verify by invoking from the executor pipeline

## F. Test Plan

### Test Approach

All verification is manual document review.

### Test Cases

| # | Test Case | Given | When | Then |
|---|-----------|-------|------|------|
| T1 | Agent file exists | After implementation | Check `.github/agents/` | `feature-plan-expander.agent.md` exists with correct frontmatter |
| T2 | Agent is hidden | Inspect frontmatter | Check `user-invocable` | Value is `false` |
| T3 | Context file generation | A `-plan.md` exists in `dev/feature/test-task/` | Plan Expander is invoked | `-context.md` is generated with key files, decisions, constraints |
| T4 | Tasks file generation | A `-plan.md` exists in `dev/feature/test-task/` | Plan Expander is invoked | `-tasks.md` is generated with ordered checklist matching plan stages |
| T5 | Skill updated | After implementation | Inspect `feature-plan-set/SKILL.md` | Ownership reflects Decomposer → plan, Plan Expander → context + tasks |
| T6 | Instruction updated | After implementation | Inspect `dev-task-folder.instructions.md` | Producer column shows Plan Expander for context and tasks rows |

### Test Data / Fixtures

- Use any existing `-plan.md` file in `dev/feature/` as input for manual verification

---

## Stage 1: Create Plan Expander Agent File

**Goal**: Create `.github/agents/feature-plan-expander.agent.md` with complete frontmatter and body
**Success Criteria**: File exists; frontmatter is correct; body contains workflow for reading plans and generating context + tasks files; subagent mode is supported
**Status**: Not Started

## Stage 2: Update feature-plan-set Skill

**Goal**: Update `.github/skills/feature-plan-set/SKILL.md` to reflect split ownership
**Success Criteria**: Skill clearly states that `-plan.md` is produced by Feature - Decomposer and `-context.md` / `-tasks.md` are produced by Feature - Plan Expander
**Status**: Not Started

## Stage 3: Update dev-task-folder Instruction

**Goal**: Update `.github/instructions/dev-task-folder.instructions.md` producer table
**Success Criteria**: `-context.md` row shows `Feature - Plan Expander` as producer; `-tasks.md` row shows `Feature - Plan Expander` as producer; `-plan.md` row still shows `Feature - Decomposer`
**Status**: Not Started
