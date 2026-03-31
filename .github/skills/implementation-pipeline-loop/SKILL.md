---
name: implementation-pipeline-loop
description: "Standard feature development loop used by orchestrators. Defines the Implement → Review → Commit → Mark Complete cycle, including invocation prompts, verification steps, and error handling. Use when: orchestrating the implementation pipeline for tasks or features."
---

# Implementation Pipeline Loop

The standard development cycle used by orchestrators to process tasks through subagents. Each task runs through the full loop before the next task begins.

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
  - **Approved** or **Approved with Reservations** → proceed to Step C
  - **Changes Requested** → Re-invoke the Implementer with the review findings, then re-invoke the Reviewer. Retry once. If still "Changes Requested" after retry, log the issue and proceed

### Step C: Commit

Invoke the **Git Commit** subagent:

> "Create an atomic commit for the completed task. The plan path is `[plan-path]` and the task name is `[task-name]`. Read the implementation and review records, stage all changes, and commit with a conventional commit message."

After the subagent returns:
- Confirm it reports a successful commit (or "Nothing to commit" if no changes were staged)

### Step D: Mark Complete

Update the todo list to mark this task as completed. Proceed to the next task.

> **Note:** QA is not produced per-task. The orchestrator runs a consolidated QA step after all tasks complete. See the Phase - Execute or Audit orchestrator agents for details.

## Path Conventions

- `[plan-path]` is the directory containing the task's plan files (e.g., `dev/feature/[task-name]/` or `dev/[audit-name]/[task-name]/`)
- `[task-name]` is the kebab-case identifier for the task, matching the plan file prefix

## Test Failure Handling

If the Implementer reports test failures:
1. The Reviewer subagent will catch this and request fixes
2. If tests still fail after the review cycle, the final review (if present) will flag it as a blocker

## Post-Loop: Documentation Update

After all tasks are complete and reported to the user, invoke the **Docs Writer** subagent to update any documentation that may be stale:

> "[SUBAGENT-MODE] [Describe what was just completed — include the pipeline type (phase/audit/test), name/scope, and list of completed tasks/features]. Update any stale documentation across the repository. Return a summary of which documents were updated and what changed."

This step is best-effort. If the Docs Writer reports no changes needed, that is expected. Do not block the pipeline on this step.

**Conditional execution:** This step only runs when the implementation pipeline was actually executed (i.e., code changes were made). If the user declined remediation or implementation after the analysis/audit phase, skip this step — no code was changed, and no branch was created.
