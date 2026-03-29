---
name: feature-plan-set
description: "Write feature plan documents for implementation. Use when: decomposing phases into features, creating plan/context/tasks files, writing acceptance criteria, producing traceability matrices, defining test plans for features, or any task that outputs planning documents to dev/[task-name]/."
---

# Feature Plan Set

The three-file plan convention used by the Feature - Decomposer and consumed by Feature - Implementer, Feature - Reviewer, Feature - QA Writer, and orchestrators.

## When to Use

- Decomposing a phase into implementable features
- Creating plan documents for a work item
- Any agent producing planning output to `dev/[task-name]/`

## File Structure

Each independent work item gets three files:

```
dev/[task-name]/
├── [task-name]-plan.md       # The plan with stages and acceptance criteria
├── [task-name]-context.md    # Key files, decisions, constraints
└── [task-name]-tasks.md      # Checklist of work items
```

**Naming**: `[task-name]` is a short, descriptive, kebab-case identifier (e.g., `auth-login`, `rate-limiter`, `test-bootstrap`).

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
**Goal**: Establish baseline test coverage using `@test-writer`
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

## Tasks File (`-tasks.md`)

An ordered checklist of concrete work items derived from the plan:

```markdown
- [ ] Task 1: [description]
- [ ] Task 2: [description]
```

## Decomposition Rules

- **Independence criterion**: Two items are independent if they can be implemented, tested, and shipped without depending on each other
- Each independent item gets its own `dev/[task-name]/` folder
- If items share prerequisites, note the dependency in each context file but keep plans separate
- Only combine items when tightly coupled (implementing one without the other leaves the codebase broken)

## Quality Checklist

Before delivering plan documents, verify:

- [ ] All requirements restated as testable acceptance criteria
- [ ] Non-goals explicitly defined
- [ ] Traceability matrix complete (AC → code → tests)
- [ ] Edge cases and error handling addressed
- [ ] Existing patterns identified and followed
- [ ] Test plan covers all acceptance criteria
- [ ] Test coverage prerequisite assessed (≥ 50% or `@test-writer` recommended)
- [ ] Observability and operability considered
