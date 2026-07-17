---
name: feature-plan-set
description: "Write feature plan documents for implementation. Use when: decomposing phases into features, creating plan/context/tasks files, writing acceptance criteria, producing traceability matrices, defining test plans for features, or any task that outputs planning documents to dev/feature/[0N-task-name]/."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->

# Feature Plan Set

The three-file plan convention: `-plan.md` is produced by the Feature - Decomposer; `-context.md` and `-tasks.md` are produced by the 04a-feature-plan-expander. All three files are consumed by 04b-feature-implementer, 04c-feature-reviewer, 04d-feature-qa-writer, and orchestrators.

When decomposing a phase, the Feature - Decomposer must also produce the phase-level execution manifest at `dev/feature/[phase-name]-execution-manifest.md`. This manifest is not part of any single feature bundle; it is the schedule and dependency contract consumed by Phase - Execute.

## File Structure

Each independent work item gets three files:

```
dev/feature/[0N-task-name]/
├── [0N-task-name]-plan.md       # The plan with stages and acceptance criteria
├── [0N-task-name]-context.md    # Key files, decisions, constraints
└── [0N-task-name]-tasks.md      # Checklist of work items
```

Each decomposed phase also gets one manifest:

```
dev/feature/[phase-name]-execution-manifest.md
```

The manifest must list the phase document path, ordered feature task names, wave schedule, dependencies, parallel safety, key files modified, sequential reasons, expected bundle files, and verification assets.

**Naming**: `[0N-task-name]` is a zero-padded two-digit prefix followed by a short, descriptive, kebab-case identifier (e.g., `01-auth-login`, `02-rate-limiter`, `03-test-bootstrap`). The numeric prefix indicates recommended execution order.

**Numbering rules**:
- Start numbering at `01`
- Features that can be executed in parallel may share the same wave number in execution metadata, but each feature directory still gets a unique sequential `0N-` prefix
- Features with prerequisites must have a higher directory prefix and a higher wave number than their dependencies
- If only one feature exists, still use the `01-` prefix for consistency

## Plan Template (`-plan.md`)

### A. Requirements & Traceability (highest priority)

- Restate requirements as **numbered, testable acceptance criteria** (AC1, AC2, ...)
- Define explicit **non-goals** (what we are NOT doing)
- Create traceability scaffold. `Test / Evidence Category` must not present speculative test names as existing facts; label evidence precisely:

| Acceptance Criteria | Code Areas/Modules | Test / Evidence Category |
|---------------------|-------------------|--------------------------|
| AC1: ... | `src/module.py` | Must-have automated test; existing test to update; Unity EditMode/PlayMode constrained test; code-review evidence only; manual QA check |

For refactors, rewires, or behavior-changing work, explicitly note which existing tests are likely to break or need updates and which new tests are required. Treat test maintenance as part of the scope, not a deferred follow-up.

### B. Correctness & Edge Cases

- List key workflows and failure modes
- Identify: validation rules, retries/timeouts, idempotency, concurrency, race conditions
- Define error-handling strategy

### C. Consistency & Architecture Fit

- Identify existing patterns to follow (naming, structure, libraries)
- Call out any deviations and justify them
- Define interfaces/contracts (inputs, outputs, schemas, config)
- For any new concrete API, file, config key, schema field, or test helper name that is not verified in the codebase and not copied exactly from the phase/request, label it `[PROPOSED - name TBD]`. Use this marker to signal that the implementer must choose the final idiomatic name and record it in implementation notes.
- When a downstream feature depends on a new public API from a sibling feature, include that API contract in the upstream feature's acceptance criteria. Do not leave cross-feature API requirements only in relationship notes.
- For compatibility, import/export, migration, or backfill features, identify the upstream generation, normalization, or validation API the downstream feature should reuse. If that API is new, include it in the upstream feature's acceptance criteria.

### D. Clean Design & Maintainability

- Propose the **simplest design** that meets requirements
- Note complexity risks and duplication risks
- Provide a "keep it clean" checklist

### E. Completeness: Observability, Security, Operability

- **Observability decision** — logging/metrics/tracing to add, preserve, or intentionally avoid, with why. Observability does not imply new logging. For local simulation, save/load, hot-loop, and test-sensitive paths, "no new normal-path logs" is often the correct operability decision. Add logs only when required by the phase, an existing pattern, or a diagnosable failure mode.
- **Security** — auth, secrets, data handling considerations
- **Runbook** — deploy, verify, rollback, monitor

### F. Test Plan (required)

- Map unit/integration tests to acceptance criteria
- Split planned evidence into categories:
  - Must-have automated tests
  - Existing tests to update
  - Tests requiring Unity Test Runner / PlayMode / EditMode or other runner constraints
  - Code-review evidence only
  - Manual QA checks
- Write top 5 high-value test cases or evidence checks (Given/When/Then where applicable)
- For refactors, rewires, or API changes, include a dedicated note on impacted existing tests, new tests required, and any Unity EditMode/PlayMode or manual QA coverage still needed.
- List test data, mocks, or fixtures needed
- When listing planned test method names, either confirm the method exists in the codebase, label it `[PROPOSED - name TBD]`, or omit the method name and describe the scenario. Do not present new test method names as existing facts.

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
- **Discovery Delta** — Plan Expander findings that validate, contradict, or refine the plan, including missing references, better existing API names, companion files, exact assertion tests, and framework constraints
- Architectural decisions made during planning (what was chosen and why)
- Constraints from the Phase document or codebase conventions
- Scope boundaries that the implementer should preserve, including important files, systems, or behaviors intentionally left untouched
- Relationships to sibling plans (shared prerequisites, suggested implementation order)
- **Environment state** — tech stack, test runner command, lint/format commands, and test baseline; pre-captured by the Plan Expander so the Implementer skips discovery
- **Relevant learnings** — filtered excerpts from `.github/learnings/` applicable to this feature's domain

### Discovery Delta section template

```markdown
## Discovery Delta

| Finding | Impact | Action |
|---------|--------|--------|
| [No contradictions found / missing file / better API name / companion file / exact assertion / framework constraint] | [How this affects the plan] | [Update plan / add task / accepted risk / none] |
```

### Scope Boundaries section template

```markdown
## Scope Boundaries

- [Constraint, file, subsystem, or behavior intentionally not changed]
- [Another important non-touch area or preserved invariant]
```

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
- Sequential dependency chains must be represented as separate waves. Do not rely on "sequential within one wave" for features where B depends on A; the wave depth should match the dependency depth.
- **Integration feature rule**: When a phase produces multiple features that must work together at runtime (e.g., a data system, a renderer, and a UI that all need to be wired into a running application), the **final numbered feature** must be an integration/bootstrap task. This feature initializes and connects the other features into a runnable application entry point (e.g., a scene bootstrap script, an app startup module, a main entry point). Its acceptance criteria must include: the application launches and all features operate together, and a human or automated smoke test can verify the combined output. Without this, individual features may pass review in isolation but never actually run together.

## Quality Checklist

Before delivering plan documents, verify:

- [ ] All requirements restated as testable acceptance criteria
- [ ] Non-goals explicitly defined
- [ ] Traceability matrix complete (AC → code → tests)
- [ ] Concrete symbols and file paths are verified existing, copied exactly from the Phase document, or labeled `[PROPOSED - name TBD]`
- [ ] Cross-feature API contracts required by downstream plans appear in upstream acceptance criteria
- [ ] Planned test method names are verified existing, explicitly proposed, or replaced with scenario descriptions
- [ ] Edge cases and error handling addressed
- [ ] Existing patterns identified and followed
- [ ] Test plan covers all acceptance criteria using evidence categories, not unverified test names
- [ ] Test coverage prerequisite assessed (≥ 50% or `@z-test-writer` recommended)
- [ ] Refactor/rewire changes include an explicit test-impact plan and maintenance tasks for affected tests
- [ ] Observability and operability considered; any new normal-path logs are justified
- [ ] **Integration check**: If the phase has multiple features that must run together, an integration/bootstrap feature exists as the final numbered task with acceptance criteria verifying the combined output is launchable and observable
- [ ] **Manifest check**: For phase decomposition, `dev/feature/[phase-name]-execution-manifest.md` exists and includes the ordered feature list, wave schedule, dependency graph, expected bundle files, and `## Verification Assets`
