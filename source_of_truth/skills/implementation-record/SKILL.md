---
name: implementation-record
description: "Template for the implementation record artifact produced by the 04b-feature-implementer. Load when writing a task's [task-name]-implementation.md record."
---

# Implementation Record Template

Write `[task-name]-implementation.md` to `[plan-path]/` using this exact template. The orchestrator supplies both tokens; if it supplied none, default to the phase-pipeline shape `dev/feature/[0N-task-name]/` with `[0N-task-name]` as `[task-name]`, and say so in your return summary.

```markdown
# Implementation Record: [Task Name]

## Summary

## Sibling Features
<!-- siblings and shared modules -->

## AC Coverage Matrix

| AC | Criterion ID | Planned Test ID | Planned Test Pattern | Status | Implementing Files | Evidence Paths | Implement Commit SHA | Review Commit SHA |
|----|--------------|-----------------|----------------------|--------|--------------------|----------------|----------------------|-------------------|

Use exact rubric or plan criterion IDs when available. If a commit SHA is not known yet, write `PENDING`.

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|

## Test Results
- **Execution**: executed-green | executed-failing | not-executed (+ reason)
- **Command**: [exact command run]
- **Results artifact**: [path]
- **Baseline**: [X passed, Y failed] (before implementation)
- **Final**: [X passed, Y failed] (after implementation)
- **New tests added**: [count]
- **Affected suites run**: [list] | None
- **Regressions**: None | [describe] | Unknown — tests not executed

## Deviations from Plan
<!-- "None" or list -->

## Gaps
<!-- "None" or list -->

## Reviewer Focus Areas
<!-- 2-5 bullets -->
- [e.g., Validation logic in `src/foo.py:45-78` — complex conditional, verify edge cases]
- [e.g., New dependency on `rate-limiter` library — confirm it matches repo conventions]
```

Additional requirements:

- The `AC Coverage Matrix` must be filled for every planned AC, even if the current status is `Pending`.
- `Evidence Paths` should point to concrete source, test, or artifact locations that a grader can search locally.
- `Implement Commit SHA` and `Review Commit SHA` may start as `PENDING`, but the columns must exist so later pipeline stages can fill them in.
- Keep the `Acceptance Criteria Status` section aligned with the coverage matrix rather than inventing a second source of truth.
- `Regressions: None` requires `Execution: executed-green`. Anything else records `Unknown — tests not executed`. See the `test-execution-evidence` instruction.
