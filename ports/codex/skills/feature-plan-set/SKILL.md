---
name: feature-plan-set
description: "Write feature plan documents for implementation. Use when: decomposing phases into features, creating plan/context/tasks files, writing acceptance criteria, producing traceability matrices, defining test plans for features, or any task that outputs planning documents to dev/feature/[0N-task-name]/."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->
# Feature Plan Set

The three-file plan convention: `-plan.md` is produced by Phase - Execute; `-context.md` and `-tasks.md` are produced by the 03a-feature-plan-expander. All three files are consumed by 03b-feature-implementer, 03c-feature-review-and-fix, 03d-feature-qa-writer, and orchestrators.

When Phase - Execute decomposes a phase, it must also produce the phase-level execution manifest at `dev/feature/[phase-name]-execution-manifest.md`. This manifest is not part of any single feature bundle. It is the living schedule and dependency contract consumed by Phase - Execute.

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

The manifest must list the phase document path, ordered feature task names, dependency-level schedule, dependencies, parallel safety, key files modified, sequential reasons, expected bundle files, and verification assets.

The manifest is a living execution schedule. It is rewritten during execution, not frozen after decomposition. Phase - Execute rewrites it when it selects a feature, expands or changes its plan, records an implementation result, resolves the feature's model route, closes a dependency level, or completes revalidation of affected future features.

A dependency level is the set of features whose dependencies are all satisfied at the same point in the graph. It is a checkpoint unit, never a concurrency unit.

Each per-feature entry records:

| Field | Meaning |
|-------|---------|
| `status` | The feature's current lifecycle state. |
| `dependency_level` | The dependency level at which the feature is eligible for execution. |
| `depends_on` | The feature's direct dependency edges. |
| `expected_read_set` | The files the feature is expected to read during revalidation. |
| `expected_write_set` | The files the feature is expected to write during revalidation. |
| `plan_revision` | The revision identifier for the feature's current plan. |
| `last_validation_commit` | The commit used for the feature's most recent validation. |
| `stale_reason` | The reason the feature's plan or schedule entry is stale. |
| `resolved_model_status` | The preflight record's `resolution_status` for the Feature - Implementer tier: `enforced`, `fallback`, or `unverified`. |

Expected read and write sets are revalidation evidence only. They never authorize concurrent feature builds.

## Lightweight Plan

Before scheduling, Phase - Execute writes one lightweight `-plan.md` per candidate feature. Each plan carries acceptance criteria, scope, dependency hypotheses, and expected file impact. It contains no context or task document. Each plan also carries the required `visual_acceptance: yes | no` flag. Set it to `yes` when an acceptance criterion states what must appear on screen. The Plan Expander adds companion files only for the selected feature. A plan without the flag fails validation. The executor never defaults a missing flag to `no`.

**Naming**: `[0N-task-name]` is a zero-padded two-digit prefix followed by a short, descriptive, kebab-case identifier (e.g., `01-auth-login`, `02-rate-limiter`, `03-test-bootstrap`). The numeric prefix indicates recommended execution order. `[phase-name]` is always `PHASE_0N` — the literal `PHASE_` plus the zero-padded two-digit phase number (e.g., `PHASE_03`), matching the phase directory under `docs/phases/`.

**Numbering rules**:
- Start numbering at `01`
- Features that can be executed at the same dependency level may share that dependency-level number in execution metadata, but each feature directory still gets a unique sequential `0N-` prefix
- Features with prerequisites must have a higher directory prefix and a higher dependency-level number than their dependencies
- If only one feature exists, still use the `01-` prefix for consistency

## Plan Template (`-plan.md`)

### A. Requirements & Traceability (highest priority)

- Restate requirements as **numbered, testable acceptance criteria** (AC1, AC2, ...)
- Define explicit **non-goals** (what we are NOT doing)
- Create traceability scaffold. `Test / Evidence Category` must not present speculative test names as existing facts; label evidence precisely:

| Acceptance Criteria | Code Areas/Modules | Test / Evidence Category |
|---------------------|-------------------|--------------------------|
| AC1: ... | `src/module.py` | Must-have automated test; existing test to update; Unity EditMode/PlayMode constrained test; code-review evidence only; manual QA check |

Those five values are the evidence taxonomy for the whole plan set; §F reuses them.

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

- **Observability decision** — logging/metrics/tracing to add, preserve, or intentionally avoid, with why. Observability does not imply new logging. For local simulation, save/load, hot-loop, and test-sensitive paths, "no new normal-path logs" is often the correct operability decision. Add logs only when required by the phase, an existing pattern, or a diagnosable failure mode.
- **Security** — auth, secrets, data handling considerations
- **Runbook** — deploy, verify, rollback, monitor

### F. Test Plan (required)

- Map unit/integration tests to acceptance criteria, labelled with the §A evidence taxonomy
- Write top 5 high-value test cases or evidence checks (Given/When/Then where applicable)
- For refactors, rewires, API changes, or any behavior-changing work, include a dedicated note on impacted existing tests, new tests required, and any Unity EditMode/PlayMode or manual QA coverage still needed. Test maintenance is in scope, not a deferred follow-up.
- List test data, mocks, or fixtures needed
- A planned test method name is a concrete name under the Concrete Name Rule; the third option there is to omit the name and describe the scenario instead.

## Concrete Name Rule

This is the single definition. Every agent that writes or validates a plan applies it here; no other file restates it.

A concrete name is any file path, method, class, field, XML element, USS class, UXML element, config key, schema field, test helper, test method, or log API named in a plan. Every one must satisfy exactly one of:

- Verified to exist in the codebase — cite the exact existing name
- Copied exactly from the Phase document or the request, and preserved
- Labeled `[PROPOSED - name TBD]` when the name is neither verified nor copied

For a test method, a fourth option applies: omit the name and describe the scenario instead. Never present an invented name as established fact. The implementer chooses the final idiomatic name for a `[PROPOSED - name TBD]` symbol and records it in implementation notes.

## Phase-Level Discovery

Some discovery results describe the phase, not one feature, and are identical across every feature bundle. Phase - Execute captures each one **once** and passes it to every Plan Expander it spawns. An Expander writes the supplied values through and does not rediscover them:

| Result | Used in |
|---|---|
| Tech stack, test runner command, test pass/fail baseline, lint command, format command | `-context.md` **Environment State** |
| Phase-scoped test directory pattern found, and whether a current-phase consolidated test file is recommended | Discovery Delta, manifest verification assets |

Running the test suite once per feature to produce the same baseline table is waste. An Expander runs its own detection only when Phase - Execute supplied no block, and says so in its return.

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

This is the complete section inventory. Write **every** section; downstream agents read them by name, so an omitted section is a silent gap, not a shorter document.

- **Key Files** — table of files and modules relevant to this feature, each with its role and change type (Create, Modify, Read-only reference). Separate files being changed from read-only reference files.
- **Discovery Delta** — Plan Expander findings that validate, contradict, or refine the plan, including missing references, better existing API names, companion files, exact assertion tests, and framework constraints
- **Architectural Decisions** — decisions made during planning (what was chosen and why)
- **Constraints** — constraints from the Phase document, codebase conventions, or the plan's non-goals
- **Scope Boundaries** — files, systems, or behaviors the implementer should preserve or intentionally not touch
- **Relationships to Sibling Plans** — shared prerequisites and cross-feature dependencies
- **Suggested Implementation Order** — ordering relative to sibling features, when the plan specifies one
- **Environment State** — tech stack, test runner command, lint/format commands, and test baseline; pre-captured by the Plan Expander so the Implementer skips discovery
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

## Tasks File (`-tasks.md`)

An ordered checklist of concrete work items derived from the plan, **always grouped under stage headers** — one section per plan stage, in plan order. A flat, ungrouped task list is a format error. If the plan has no explicit stage boundaries, infer groupings from the AC structure (e.g. data/schema tasks as Stage 1, logic tasks as Stage 2, test-verification tasks as Stage 3).

```markdown
## Stage N: [Name]

- [ ] Task description derived from the stage goal and its acceptance criteria
- [ ] Another task
```

The `- [ ] ` checkbox syntax is consumed by the Implementer, which checks tasks off in place; do not vary it.

## Decomposition Rules

- **Independence criterion**: Two items are independent if they can be implemented, tested, and shipped without depending on each other
- Each independent item gets its own `dev/feature/[0N-task-name]/` folder
- If items share prerequisites, note the dependency in each context file but keep plans separate
- Only combine items when tightly coupled (implementing one without the other leaves the codebase broken)
- Assign numeric prefixes based on dependency order: prerequisites get lower numbers, dependents get higher numbers
- Sequential dependency chains must be represented as separate dependency levels. Do not rely on "sequential within one dependency level" for features where B depends on A; the dependency-level depth should match the dependency depth.
- **Integration feature rule**: When a phase produces multiple features that must work together at runtime (e.g., a data system, a renderer, and a UI that all need to be wired into a running application), the **final numbered feature** must be an integration/bootstrap task. This feature initializes and connects the other features into a runnable application entry point (e.g., a scene bootstrap script, an app startup module, a main entry point). Its acceptance criteria must include: the application launches and all features operate together, and a human or automated smoke test can verify the combined output. Without this, individual features may pass review in isolation but never actually run together.

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
- [ ] Observability and operability considered; any new normal-path logs are justified
- [ ] **Integration check**: If the phase has multiple features that must run together, an integration/bootstrap feature exists as the final numbered task with acceptance criteria verifying the combined output is launchable and observable
- [ ] **Manifest check**: For phase decomposition, `dev/feature/[phase-name]-execution-manifest.md` exists and includes the ordered feature list, dependency-level schedule, dependency graph, expected bundle files, and `## Verification Assets`
