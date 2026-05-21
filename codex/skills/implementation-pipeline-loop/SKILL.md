<!-- Generated from .github/skills source-of-truth. Do not edit manually. -->
# Implementation Pipeline Loop

The standard development cycle used by orchestrators to process tasks through subagents. Each task runs through the full loop before the next task begins.

## Loop Steps

For **each task** (in priority order), run these steps sequentially. Complete ALL steps for one task before starting the next.

### Step A: Implement

Invoke the **z-feature-implementer** subagent:

> "[SUBAGENT-MODE] Implement the plan at `[plan-path]`. Read the plan files, implement all acceptance criteria using Red-Green-Refactor TDD, and write the implementation record to `[plan-path]/[task-name]-implementation.md`. Return a summary of what was implemented and test results."

After the subagent returns:
- Verify `[plan-path]/[task-name]-implementation.md` exists
- Check the summary for any reported gaps or blockers

### Step B: Review

Invoke the **z-feature-reviewer** subagent:

> "[SUBAGENT-MODE] Review the implementation at `[plan-path]`. Read the plan files and implementation record, review all changed code, apply fixes for any issues found, and write the review record to `[plan-path]/[task-name]-review.md`. Return the verdict and a summary of issues found and fixes applied."

After the subagent returns:
- Verify `[plan-path]/[task-name]-review.md` exists
- Check the verdict:
  - **Approved** or **Approved with Reservations** → proceed to Step C
  - **Changes Requested** → Re-invoke the Implementer with the review findings, then re-invoke the Reviewer. Retry once. If still "Changes Requested" after retry, log the issue and proceed

### Step C: Commit

Execute the commit directly — do not invoke a subagent for this step.

1. **Collect files to stage** — From the "Files Changed" table in `[plan-path]/[task-name]-implementation.md`, collect every source file and test file path listed. Also include all pipeline documents in `[plan-path]/` (plan, context, tasks, implementation, review files).

2. **Stage only those files**:
   ```bash
   git add <file1> <file2> ... [plan-path]/[task-name]-implementation.md [plan-path]/[task-name]-review.md
   ```
   Do NOT use `git add -A` — staging untracked files outside the implementation record risks including debug files or changes from adjacent features.

3. **Generate a commit message** using conventional commit format. Derive type, scope, and summary from the implementation record:
   ```
   <type>(<scope>): <short summary — 50 chars or fewer, imperative mood>

   <one paragraph: what changed and why, derived from implementation record summary>

   Implements: <AC refs, e.g., AC1, AC2, AC3>
   Reviewed-by: 04c-feature-reviewer
   Verdict: <Approved | Approved with Reservations>
   ```
   **Type:** `feat` (new capability) · `fix` (bug fix) · `refactor` (restructure) · `test` (tests only) · `docs` (docs only) · `chore` (config/build)

4. **Commit**:
   ```bash
   git commit -m "<message>"
   ```

5. **Verify**:
   ```bash
   git log --oneline -1
   ```
   Confirm the commit appears. If `git add` staged nothing, log "Nothing to commit" and proceed — this is not an error.

### Step D: Mark Complete

Update the todo list to mark this task as completed. Proceed to the next task.

> **Note:** In **batch mode**, QA is not produced per-task. The orchestrator runs a consolidated QA step after all tasks complete. In **per-feature mode**, QA and Final Review run after each individual feature. See the Phase - Execute agent for details.

## Path Conventions

- `[plan-path]` is the directory containing the task's plan files (e.g., `dev/feature/[0N-task-name]/` or `dev/[audit-name]/[task-name]/`)
- `[task-name]` is the kebab-case identifier for the task, matching the plan file prefix (including the `0N-` numeric prefix for feature directories)

## Test Failure Handling

If the Implementer reports test failures:
1. The Reviewer subagent will catch this and request fixes
2. If tests still fail after the review cycle, the final review (if present) will flag it as a blocker

## Post-Loop: Documentation Update

After all tasks are complete and reported to the user, invoke the **Docs Writer** subagent to update any documentation that may be stale:

> "[SUBAGENT-MODE] [Describe what was just completed — include the pipeline type (phase/audit/test), name/scope, and list of completed tasks/features]. Update any stale documentation across the repository. Return a summary of which documents were updated and what changed."

This step is best-effort. If the Docs Writer reports no changes needed, that is expected. Do not block the pipeline on this step.

**Conditional execution:** This step only runs when the implementation pipeline was actually executed (i.e., code changes were made). If the user declined remediation or implementation after the analysis/audit phase, skip this step — no code was changed, and no branch was created.
