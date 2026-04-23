---
name: implementation-record
description: "Template for the implementation record artifact produced by the Feature - Implementer. Load when writing [0N-task-name]-implementation.md."
---

# Implementation Record Template

Write `[0N-task-name]-implementation.md` to `dev/feature/[0N-task-name]/` using this exact template:

```markdown
# Implementation Record: [Task Name]

## Summary

## Sibling Features
<!-- siblings and shared modules -->

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
- **Baseline**: [X passed, Y failed] (before implementation)
- **Final**: [X passed, Y failed] (after implementation)
- **New tests added**: [count]
- **Regressions**: None | [describe]

## Deviations from Plan
<!-- "None" or list -->

## Gaps
<!-- "None" or list -->

## Reviewer Focus Areas
<!-- 2-5 bullets -->
- [e.g., Validation logic in `src/foo.py:45-78` — complex conditional, verify edge cases]
- [e.g., New dependency on `rate-limiter` library — confirm it matches repo conventions]
```
