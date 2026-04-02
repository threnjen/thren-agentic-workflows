# Feature Plan: decomposer-promote

**Phase**: Phase 01 — Split Feature Decomposer from Phase Execute
**Feature**: Promote `feature-decomposer.agent.md` to user-facing `03 Feature - Decomposer` (plan-only)
**Implementation order**: 1 of 3 (no dependencies)

---

## A. Requirements & Traceability

### Acceptance Criteria

| ID | Criterion |
|----|-----------|
| AC1 | `feature-decomposer.agent.md` frontmatter `name` is `03 Feature - Decomposer` |
| AC2 | `feature-decomposer.agent.md` frontmatter removes `user-invocable: false` (making it user-invocable by default) |
| AC3 | Agent body scopes output to `-plan.md` only — all references to producing `-context.md` and `-tasks.md` are removed |
| AC4 | Standalone mode messaging references `@04 Phase - Execute` (not `@03 Phase - Execute`) |
| AC5 | Subagent mode return value describes plan-only output (no context/tasks references) |
| AC6 | `read-only-agent.instructions.md` `applyTo` still includes `**/feature-decomposer.agent.md` (no change needed — just verify) |
| AC7 | Quality Checklist reference to `feature-plan-set` skill remains intact |

### Non-Goals

- Do NOT change the plan template content (sections A–F stay the same)
- Do NOT create the Plan Expander agent (that is `plan-expander-create`)
- Do NOT rename or renumber the executor (that is `executor-renumber`)
- Do NOT update `dev-task-folder.instructions.md` producer table (that is `plan-expander-create`)
- Do NOT update README.md or CODEBASE_CONTEXT.md (Docs Writer handles that)

### Traceability Matrix

| Acceptance Criteria | Files to Modify | Verification |
|---------------------|----------------|--------------|
| AC1 | `.github/agents/feature-decomposer.agent.md` (frontmatter) | Inspect `name:` field |
| AC2 | `.github/agents/feature-decomposer.agent.md` (frontmatter) | Confirm `user-invocable: false` line removed |
| AC3 | `.github/agents/feature-decomposer.agent.md` (body) | Grep for `-context.md` and `-tasks.md` — should not appear as deliverables |
| AC4 | `.github/agents/feature-decomposer.agent.md` (body) | Grep for `@03 Phase - Execute` — should be `@04 Phase - Execute` |
| AC5 | `.github/agents/feature-decomposer.agent.md` (body) | Review Return Value section |
| AC6 | `.github/instructions/read-only-agent.instructions.md` | Inspect `applyTo` — `feature-decomposer.agent.md` must be present |
| AC7 | `.github/agents/feature-decomposer.agent.md` (body) | Quality Checklist reference exists |

## B. Correctness & Edge Cases

### Key Workflows

1. **User invokes `@03 Feature - Decomposer` directly** — agent runs in standalone mode, produces only `-plan.md` files, tells user to hand off to `@04 Phase - Execute`
2. **`04 Phase - Execute` invokes Decomposer as subagent** — agent runs in subagent mode, produces only `-plan.md` files, returns structured summary to orchestrator
3. **Read-only constraint still applies** — Decomposer must still operate under read-only-agent constraints (plan docs only, no source code modification)

### Failure Modes

- If the frontmatter still has `user-invocable: false`, the agent won't appear in the VS Code picker
- If body still references producing `-context.md` / `-tasks.md`, the agent will attempt to write files that the Plan Expander should produce
- If standalone mode message still says `@03 Phase - Execute`, users will invoke the wrong agent

### Error Handling Strategy

- Not applicable (Markdown-only changes; no runtime error handling)

## C. Consistency & Architecture Fit

### Existing Patterns to Follow

- **Dual-use agent precedent**: `Docs Writer` is both user-invocable and a subagent — follow the same pattern (no `user-invocable` field = user-invocable by default)
- **Numbering convention**: User-facing agents use `NN Name` format (e.g., `01 Project - Planner`, `02 Phase - Refiner`)
- **Agent frontmatter fields**: `name`, `description`, `tools`, `model`, optionally `agents` and `user-invocable`
- **All agents use `<model>`** (except Docs Writer)

### Deviations

- None. This follows the established dual-use pattern exactly.

### Interfaces

- **Input**: A refined Phase document path (same as current)
- **Output**: Only `-plan.md` files in `dev/feature/[task-name]/` (narrower than current 3-file output)
- **Return value (subagent mode)**: Structured summary listing feature task names and plan summaries

## D. Clean Design & Maintainability

### Simplest Design

The change is subtractive — remove references to producing `-context.md` and `-tasks.md`, update the name/number, and update the standalone handoff message. No new sections or logic needed.

### Complexity Risks

- Low. This is a straightforward edit to a single agent file plus a verification of one instruction file.

### Keep It Clean Checklist

- [ ] No orphaned references to 3-file output remain in the agent body
- [ ] Frontmatter is minimal and follows the established pattern
- [ ] Standalone message is consistent with the new pipeline numbering

## E. Completeness: Observability, Security, Operability

- **Logging/metrics/tracing**: Not applicable (Markdown docs)
- **Security**: Not applicable
- **Runbook**: Not applicable — verify by opening VS Code and checking the agent picker

## F. Test Plan

### Test Approach

All verification is manual document review — this repo has no automated tests.

### Test Cases

| # | Test Case | Given | When | Then |
|---|-----------|-------|------|------|
| T1 | Agent appears in picker | `feature-decomposer.agent.md` is updated | User opens VS Code agent picker | `03 Feature - Decomposer` is listed |
| T2 | Plan-only output | User invokes `@03 Feature - Decomposer` with a Phase doc | Agent completes | Only `-plan.md` files are produced (no `-context.md`, no `-tasks.md`) |
| T3 | Standalone handoff message | User invokes `@03 Feature - Decomposer` standalone | Agent finishes and presents handoff | Message references `@04 Phase - Execute` |
| T4 | Subagent mode works | `04 Phase - Execute` invokes Decomposer | Agent completes | Returns structured summary with task names |
| T5 | Read-only constraint | Inspect `read-only-agent.instructions.md` | Check `applyTo` | `feature-decomposer.agent.md` is included |

### Test Data / Fixtures

- Use any existing refined Phase document (e.g., `docs/phases/PHASE_01/PHASE_01_SUMMARY.md`) as input

---

## Stage 1: Update Frontmatter

**Goal**: Promote `feature-decomposer.agent.md` to user-facing `03 Feature - Decomposer`
**Success Criteria**: `name` is `03 Feature - Decomposer`, `user-invocable: false` line is removed, `description` updated to reflect plan-only scope
**Status**: Not Started

## Stage 2: Update Agent Body to Plan-Only Output

**Goal**: Remove all references to producing `-context.md` and `-tasks.md`; scope deliverables to `-plan.md` only
**Success Criteria**: No remaining references to producing context or tasks files; "What You Do" section lists only `-plan.md`; file structure diagram shows only `-plan.md`; Phase 3 instructions produce only plan files
**Status**: Not Started

## Stage 3: Update Standalone and Subagent Messaging

**Goal**: Update standalone handoff to reference `@04 Phase - Execute`; update subagent return value to describe plan-only output
**Success Criteria**: Standalone message says `@04 Phase - Execute`; subagent return value lists only plan files
**Status**: Not Started

## Stage 4: Verify Read-Only Instruction

**Goal**: Confirm `read-only-agent.instructions.md` applyTo includes `feature-decomposer.agent.md`
**Success Criteria**: `applyTo` glob matches the file; no changes needed (verification only)
**Status**: Not Started
