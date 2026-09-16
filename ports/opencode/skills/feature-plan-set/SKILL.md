---
name: feature-plan-set
description: "Write feature plan documents for implementation. Use when: decomposing phases into features, creating plan/context/tasks files, writing acceptance criteria, producing traceability matrices, defining test plans for features, or any task that outputs planning documents to dev/feature/[0N-task-name]/."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->

# Feature Plan Set

The invoking pipeline selects one artifact contract explicitly:

| Pipeline | Required planning artifacts |
|----------|-----------------------------|
| Phase | `-plan.md`, selection-time `-delta.md`, and the phase execution manifest |
| Audit or Test | `-plan.md`, `-context.md`, and `-tasks.md` |

Shared consumers never infer a contract from existing files.

The Feature - Plan Author produces Phase plans, deltas, and the execution manifest. Audit and Test keep their existing producers for context and task files.

## File Structure

Each Phase work item gets two files over its lifecycle:

```
dev/feature/[0N-task-name]/
├── [0N-task-name]-plan.md       # The plan with stages and acceptance criteria
└── [0N-task-name]-delta.md      # Selection-time repository findings
```

Each decomposed phase also gets one manifest:

```
dev/feature/[phase-name]-execution-manifest.md
```

The manifest must list the phase document path, feature task names in order, and each feature's prerequisites. It must also list modified key files, reasons for sequential execution, expected artifacts, and verification assets.

The manifest is a living execution schedule. It is rewritten during execution, not frozen after decomposition. Feature - Plan Author rewrites it when Phase - Execute selects a feature, records an implementation result, resolves the feature's model route, completes a feature, or completes revalidation of affected future features.

The manifest also contains the Phase Environment State, test baseline, lint and format commands, phase test pattern, durable checkpoints, and verification assets for each feature.

The prerequisite graph orders the features. A feature is eligible once every feature it names as a prerequisite is complete. The graph sets order and drives revalidation. It never authorizes two concurrent feature builds.

Each per-feature entry records:

| Field | Meaning |
|-------|---------|
| `status` | The feature's current lifecycle state. |
| `execution_order` | The feature's position in the phase's execution order. |
| `prerequisites` | The features that must be complete before this feature is eligible. |
| `expected_read_set` | The files the feature is expected to read during revalidation. |
| `expected_write_set` | The files the feature is expected to write during revalidation. |
| `plan_revision` | The revision identifier for the feature's current plan. |
| `last_validation_commit` | The commit used for the feature's most recent validation. |
| `stale_reason` | The reason the feature's plan or schedule entry is stale. |
| `resolved_model_status` | The preflight record's `resolution_status` for the Feature - Implementer tier: `enforced`, `fallback`, or `unverified`. |

Expected read and write sets are revalidation evidence only. They never authorize concurrent feature builds.

## Lightweight Plan

Before scheduling, Feature - Plan Author writes one lightweight `-plan.md` per candidate feature. Each plan defines acceptance criteria, scope, dependency hypotheses, and expected file impact. Initial mode writes no context, task, or delta file.

**Naming**: `[0N-task-name]` is a zero-padded two-digit prefix followed by a short, descriptive, kebab-case identifier (e.g., `01-auth-login`, `02-rate-limiter`, `03-test-bootstrap`). The numeric prefix indicates recommended execution order. `[phase-name]` is always `PHASE_0N` — the literal `PHASE_` plus the zero-padded two-digit phase number (e.g., `PHASE_03`), matching the phase directory under `docs/phases/`.

**Numbering rules**:
- Start numbering at `01`
- Each feature directory gets a unique sequential `0N-` prefix
- A feature must have a higher directory prefix and a later execution order than every feature it names as a prerequisite
- If only one feature exists, still use the `01-` prefix for consistency

## Plan Template (`-plan.md`)

### A. Requirements & Traceability (highest priority)

- Restate requirements as **numbered, testable acceptance criteria** (AC1, AC2, ...)
- Define explicit **non-goals** (what we are NOT doing)
- Create traceability scaffold. The `Test / Evidence Category` column must not present speculative test names as existing facts. Label evidence precisely:

| Acceptance Criteria | Code Areas/Modules | Test / Evidence Category |
|---------------------|-------------------|--------------------------|
| AC1: ... | `src/module.py` | Must-have automated test; existing test to update; Unity EditMode/PlayMode constrained test; code-review evidence only; manual QA check |

Those five values are the evidence taxonomy for the whole plan set. Section §F reuses them.

### B. Correctness & Edge Cases

- List key workflows and failure modes
- Identify: validation rules, retries/timeouts, idempotency, concurrency, race conditions
- Define error-handling strategy

### C. Consistency & Architecture Fit

- Identify existing patterns to follow (naming, structure, libraries)
- Call out any deviations and justify them
- Define interfaces/contracts (inputs, outputs, schemas, config)
- Name every concrete symbol under the Concrete Name Rule below
- When a downstream feature depends on a new public API from a sibling feature, include that API contract in the upstream feature's acceptance criteria. Do not leave cross-feature API requirements only in relationship notes.
- For compatibility, import/export, migration, or backfill features, identify the upstream generation, normalization, or validation API the downstream feature should reuse. If that API is new, include it in the upstream feature's acceptance criteria.

### D. Clean Design & Maintainability

- Propose the **simplest design** that meets requirements
- Note complexity risks and duplication risks
- Provide a "keep it clean" checklist

### E. Completeness: Observability, Security, Operability

- **Observability decision** — logging/metrics/tracing to add, preserve, or intentionally avoid, and why. Observability does not imply new logging. For local simulation, save/load, hot-loop, and test-sensitive paths, "no new normal-path logs" is often the correct operability decision. Add logs only when required by the phase, an existing pattern, or a diagnosable failure mode.
- **Security** — auth, secrets, data handling considerations
- **Runbook** — deploy, verify, rollback, monitor

### F. Test Plan (required)

- Map unit/integration tests to acceptance criteria, using the §A evidence taxonomy
- Write the top 5 high-value test cases or evidence checks (Given/When/Then where applicable)
- For refactors, rewires, API changes, or any behavior-changing work, include a dedicated note. The note must cover impacted existing tests, required new tests, and any Unity EditMode/PlayMode or manual QA coverage still needed. Test maintenance is in scope. Do not defer it.
- List test data, mocks, or fixtures needed
- A planned test method name is a concrete name under the Concrete Name Rule. The third option under that rule is to omit the name and describe the scenario instead.

## Concrete Name Rule

This is the single definition. Every agent that writes or validates a plan applies it here. No other file restates it.

A concrete name is any named file path, method, class, field, XML element, USS class, UXML element, config key, or schema field. It also includes any named test helper, test method, or log API. Every one must satisfy exactly one of:

- Verified to exist in the codebase — cite the exact existing name
- Copied exactly from the Phase document or the request, and preserved
- Labeled `[PROPOSED - name TBD]` when the name is neither verified nor copied

For a test method, a fourth option applies: omit the name and describe the scenario instead. Never present an invented name as established fact. The implementer chooses the final idiomatic name for a `[PROPOSED - name TBD]` symbol. The implementer records that name in implementation notes.

## Selection Delta (`-delta.md`)

Feature - Plan Author writes one delta only when Phase - Execute selects a feature. The delta contains:

- **Key Files** — verified files and symbols the feature reads or changes.
- **Current Constraints** — applicable repository rules, plan non-goals, and relevant learnings.
- **Verification Assets** — existing tests and commands that exercise the selected scope.
- **Discoveries** — facts that validate or contradict the plan.

Selection mode may patch only the selected plan. It patches the plan only when verified source contradicts it. The delta records the contradiction and the patch.

## Phase-Level Discovery

Feature - Plan Author captures Phase Environment State once in initial mode. It writes the results into the manifest, not a per-feature file.

| Result | Manifest location |
|---|---|
| Tech stack, test runner command, test baseline, lint command, format command | `## Environment State` |
| Phase test pattern and shared or feature verification assets | `## Verification Assets` and the relevant feature entry |

## Stage Format

When tests are missing or coverage is below 50%, plans must start with a prerequisite stage:

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

## Audit and Test Context File (`-context.md`)

This is the complete section inventory. Write **every** section. Downstream agents read sections by name. An omitted section creates a silent gap. It does not shorten the document.

- **Key Files** — table of files and modules relevant to this feature, each with its role and change type (Create, Modify, Read-only reference). Separate files being changed from read-only reference files.
- **Discovery Delta** — findings that validate, contradict, or refine the plan, including missing references, better existing API names, companion files, exact assertion tests, and framework constraints
- **Architectural Decisions** — decisions made during planning (what was chosen and why)
- **Constraints** — constraints from the Phase document, codebase conventions, or the plan's non-goals
- **Scope Boundaries** — files, systems, or behaviors the implementer should preserve or intentionally not touch
- **Relationships to Sibling Plans** — shared prerequisites and cross-feature dependencies
- **Suggested Implementation Order** — ordering relative to sibling features, when the plan specifies one
- **Environment State** — tech stack, test runner command, lint and format commands, and test baseline
- **Relevant Learnings** — filtered excerpts from `docs/learnings/` applicable to this feature's domain

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

[Filtered excerpts from docs/learnings/*.md relevant to this feature's domain.
Record "None applicable" if no entries match.]
```

## Audit and Test Tasks File (`-tasks.md`)

Use an ordered checklist of concrete work items derived from the plan. Group all work items under **stage headers**. Use one section per plan stage, in plan order. A flat, ungrouped task list is a format error. If the plan has no explicit stage boundaries, infer groupings from the AC structure. For example, group data/schema tasks as Stage 1, logic tasks as Stage 2, and test-verification tasks as Stage 3.

```markdown
## Stage N: [Name]

- [ ] Task description derived from the stage goal and its acceptance criteria
- [ ] Another task
```

Audit and Test implementer runs consume the `- [ ] ` checkbox syntax. Do not vary it.

## Decomposition Rules

- **Independence criterion**: Two items are independent if they can be implemented, tested, and shipped without depending on each other
- Each independent item gets its own `dev/feature/[0N-task-name]/` folder
- If items share prerequisites, record the dependency in the Phase manifest or each Audit/Test context file
- Only combine items when tightly coupled (implementing one without the other leaves the codebase broken)
- Assign numeric prefixes based on dependency order: prerequisites get lower numbers, dependents get higher numbers
- Where B needs A, B must name A in its prerequisites. Do not rely on execution order alone. A reorder would silently drop the constraint.
- **Integration feature rule**: When a phase produces multiple features that must work together at runtime, the **final numbered feature** must be an integration/bootstrap task. For example, a data system, a renderer, and a UI may all need to be wired into a running application. This feature initializes and connects the other features through a runnable application entry point. Examples include a scene bootstrap script, an app startup module, or a main entry point. Its acceptance criteria must include these outcomes. The application launches. All features operate together. A human or automated smoke test can verify the combined output. Without this feature, individual features may pass review in isolation but never actually run together.

## Quality Checklist

Before delivering plan documents, verify:

- [ ] All requirements restated as testable acceptance criteria
- [ ] Non-goals explicitly defined
- [ ] Traceability matrix complete (AC → code → tests)
- [ ] Every concrete name in the plan — symbols, paths, config keys, test methods — is verified existing, copied from the Phase document, labeled `[PROPOSED - name TBD]`, or replaced with a scenario description
- [ ] Cross-feature API contracts required by downstream plans appear in upstream acceptance criteria
- [ ] Edge cases and error handling addressed
- [ ] Existing patterns identified and followed
- [ ] Test plan covers all acceptance criteria using evidence categories, not unverified test names
- [ ] Test coverage prerequisite assessed (≥ 50% or `@z-test-writer` recommended)
- [ ] Refactor/rewire changes include an explicit test-impact plan and maintenance tasks for affected tests
- [ ] Observability and operability considered. Any new normal-path logs are justified
- [ ] **Integration check**: If the phase has multiple features that must run together, the final numbered task is an integration/bootstrap feature. Its acceptance criteria verify that the combined output is launchable and observable.
- [ ] **Manifest check**: For phase decomposition, `dev/feature/[phase-name]-execution-manifest.md` exists. It includes the ordered feature list, each feature's prerequisites, the prerequisite graph, expected artifacts, `## Environment State`, and `## Verification Assets`.
