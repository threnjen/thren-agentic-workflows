---
name: feature-plan-set
description: "Write feature plan documents for implementation. Use when: decomposing phases into features, creating plan/context/tasks files, writing acceptance criteria, producing traceability matrices, defining test plans for features, or any task that outputs planning documents to dev/feature/[0N-task-name]/."
---

# Feature Plan Set

The three-file plan convention: `-plan.md` is produced by the Feature - Decomposer; `-context.md` and `-tasks.md` are produced by the Feature - Plan Expander. All three files are consumed by Feature - Implementer, Feature - Reviewer, Feature - QA Writer, and orchestrators.

## File Structure

Each independent work item gets three files:

```
dev/feature/[0N-task-name]/
├── [0N-task-name]-plan.md       # The plan with stages and acceptance criteria
├── [0N-task-name]-context.md    # Key files, decisions, constraints
└── [0N-task-name]-tasks.md      # Checklist of work items
```

**Naming**: `[0N-task-name]` is a zero-padded two-digit prefix followed by a short, descriptive, kebab-case identifier (e.g., `01-auth-login`, `02-rate-limiter`, `03-test-bootstrap`). The numeric prefix indicates recommended execution order.

**Numbering rules**:
- Start numbering at `01`
- Features that can be executed in parallel share the same number
- Features with prerequisites must have a higher number than their dependencies
- If only one feature exists, still use the `01-` prefix for consistency

## Plan Template (`-plan.md`)

### A. Requirements & Traceability (highest priority)

- Restate requirements as **numbered, testable acceptance criteria** (AC1, AC2, ...)
- Define explicit **non-goals** (what we are NOT doing)
- Create traceability scaffold:

| Acceptance Criteria | Code Areas/Modules | Planned Tests |
|---------------------|-------------------|---------------|
| AC1: ... | `src/module.py` | `test_ac1_*` |

### B. Correctness & Edge Cases

- List key workflows and failure modes
- Identify: validation rules, retries/timeouts, idempotency, concurrency, race conditions
- Define error-handling strategy

### C. Consistency & Architecture Fit

- Identify existing patterns to follow (naming, structure, libraries)
- Call out any deviations and justify them
- Define interfaces/contracts (inputs, outputs, schemas, config)

### D. Clean Design & Maintainability

- Propose the **simplest design** that meets requirements
- Note complexity risks and duplication risks
- Provide a "keep it clean" checklist

### E. Completeness: Observability, Security, Operability

- **Logging/metrics/tracing** — what, where, why
- **Security** — auth, secrets, data handling considerations
- **Runbook** — deploy, verify, rollback, monitor

### F. Test Plan (required)

- Map unit/integration tests to acceptance criteria
- Write top 5 high-value test cases (Given/When/Then)
- List test data, mocks, or fixtures needed

## Stage Format

When tests are missing or coverage is below 50%, plans must lead with a prerequisite stage:

```markdown
## Stage 0: Test Prerequisites
**Goal**: Establish baseline test coverage using `@z-test-writer`
**Success Criteria**: Test suite exists, coverage ≥ 50%, all tests pass
**Status**: Required before implementation begins
```

All other stages:

```markdown
## Stage N: [Name]
**Goal**: [Specific deliverable]
**Success Criteria**: [Testable outcomes]
**Status**: Not Started
```

## Context File (`-context.md`)

The context file captures:

- Key files and modules relevant to this feature
- Architectural decisions made during planning (what was chosen and why)
- Constraints from the Phase document or codebase conventions
- Relationships to sibling plans (shared prerequisites, suggested implementation order)
- **Environment state** — tech stack, test runner command, lint/format commands, and test baseline; pre-captured by the Plan Expander so the Implementer skips discovery
- **Relevant learnings** — filtered excerpts from `.github/learnings/` applicable to this feature's domain

### Environment State section template

```markdown
## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | [e.g., Python 3.11 + FastAPI, Node 20 + React 18, Unity 6 + C#] |
| Test Runner | `[exact command]` |
| Test Baseline | [X passed, Y failed — captured YYYY-MM-DD] |
| Lint | `[command]` or Not configured |
| Format | `[command]` or Not configured |
```

### Relevant Learnings section template

```markdown
## Relevant Learnings

[Filtered excerpts from .github/learnings/*.md relevant to this feature's domain.
Record "None applicable" if no entries match.]
```

## Tasks File (`-tasks.md`)

An ordered checklist of concrete work items derived from the plan:

```markdown
- [ ] Task 1: [description]
- [ ] Task 2: [description]
```

## Decomposition Rules

- **Independence criterion**: Two items are independent if they can be implemented, tested, and shipped without depending on each other
- Each independent item gets its own `dev/feature/[0N-task-name]/` folder
- If items share prerequisites, note the dependency in each context file but keep plans separate
- Only combine items when tightly coupled (implementing one without the other leaves the codebase broken)
- Assign numeric prefixes based on dependency order: prerequisites get lower numbers, dependents get higher numbers
- **Integration feature rule**: When a phase produces multiple features that must work together at runtime (e.g., a data system, a renderer, and a UI that all need to be wired into a running application), the **final numbered feature** must be an integration/bootstrap task. This feature initializes and connects the other features into a runnable application entry point (e.g., a scene bootstrap script, an app startup module, a main entry point). Its acceptance criteria must include: the application launches and all features operate together, and a human or automated smoke test can verify the combined output. Without this, individual features may pass review in isolation but never actually run together.

## Quality Checklist

Before delivering plan documents, verify:

- [ ] All requirements restated as testable acceptance criteria
- [ ] Non-goals explicitly defined
- [ ] Traceability matrix complete (AC → code → tests)
- [ ] Edge cases and error handling addressed
- [ ] Existing patterns identified and followed
- [ ] Test plan covers all acceptance criteria
- [ ] Test coverage prerequisite assessed (≥ 50% or `@z-test-writer` recommended)
- [ ] Observability and operability considered
- [ ] **Integration check**: If the phase has multiple features that must run together, an integration/bootstrap feature exists as the final numbered task with acceptance criteria verifying the combined output is launchable and observable
