---
name: implementation-pipeline-loop
description: "Standard feature development loop used by orchestrators. Defines the Implement → Review → (optional QA) → Mark Complete cycle, including invocation prompts, verification steps, and error handling. Use when: orchestrating the implementation pipeline for tasks or features."
---

# Implementation Pipeline Loop

The standard development cycle used by orchestrators to process tasks through subagents. Each task runs through the full loop before the next task begins.

## When to Use

- Phase - Execute orchestrating feature implementation
- Audit orchestrator driving remediation of findings
- Test orchestrator driving remediation of test findings

## Loop Steps

For **each task** (in priority order), run these steps sequentially. Complete ALL steps for one task before starting the next.

### Step A: Implement

Invoke the **Feature - Implementer** subagent:

> "Implement the plan at `[plan-path]`. Read the plan files, implement all acceptance criteria using Red-Green-Refactor TDD, and write the implementation record to `[plan-path]/[task-name]-implementation.md`. Return a summary of what was implemented and test results."

After the subagent returns:
- Verify `[plan-path]/[task-name]-implementation.md` exists
- Check the summary for any reported gaps or blockers

### Step B: Review

Invoke the **Feature - Reviewer** subagent:

> "Review the implementation at `[plan-path]`. Read the plan files and implementation record, review all changed code, apply fixes for any issues found, and write the review record to `[plan-path]/[task-name]-review.md`. Return the verdict and a summary of issues found and fixes applied."

After the subagent returns:
- Verify `[plan-path]/[task-name]-review.md` exists
- Check the verdict:
  - **Approved** or **Approved with Reservations** → proceed to Step C (if applicable) or Step D
  - **Changes Requested** → Re-invoke the Implementer with the review findings, then re-invoke the Reviewer. Retry once. If still "Changes Requested" after retry, log the issue and proceed

### Step C: QA Plan (when applicable)

**Include this step when:** the orchestrator's pipeline includes QA (Phase - Execute, Audit orchestrator). **Skip when:** the pipeline does not include QA (Test orchestrator).

Invoke the **Feature - QA Writer** subagent:

> "Write the release QA plan for the task at `[plan-path]`. Read all documents in the folder (plan, context, tasks, implementation record, review record) and the source code. Write the QA plan to `[plan-path]/[task-name]-qa.md`. Return a summary of what manual QA is needed."

After the subagent returns:
- Verify `[plan-path]/[task-name]-qa.md` exists

### Step D: Mark Complete

Update the todo list to mark this task as completed. Proceed to the next task.

## Path Conventions

- `[plan-path]` is the directory containing the task's plan files (e.g., `dev/[task-name]/` or `dev/[audit-name]/[task-name]/`)
- `[task-name]` is the kebab-case identifier for the task, matching the plan file prefix

## Test Failure Handling

If the Implementer reports test failures:
1. The Reviewer subagent will catch this and request fixes
2. If tests still fail after the review cycle, the final review (if present) will flag it as a blocker
