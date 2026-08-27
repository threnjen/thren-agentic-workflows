---
name: implementation-pipeline-loop
description: "Standard feature development loop used by orchestrators. Defines the Implement → Review → Commit → Mark Complete cycle, including invocation prompts, verification steps, and error handling. Use when: orchestrating the implementation pipeline for tasks or features."
---

# Implementation Pipeline Loop

The standard development cycle used by orchestrators to process tasks through subagents. Each task runs through the full loop before the next task begins.

## Loop Steps

For **each task** (in priority order), run these steps sequentially. Complete ALL steps for one task before starting the next.

### Step A: Implement

spawn the **z-feature-implementer** subagent:

> "[SUBAGENT-MODE] Implement the plan at `[plan-path]`. Read the plan files, implement all acceptance criteria using Red-Green-Refactor TDD, and write the implementation record to `[plan-path]/[task-name]-implementation.md`. Manifest verification assets — run these affected suites if the change touches a shared contract: [verification-assets, or `not provided`]. Return a summary of what was implemented, the test-execution status with its results artifact path, and any gaps or blockers."

After the subagent returns:
- Verify `[plan-path]/[task-name]-implementation.md` exists
- Check the summary for any reported gaps or blockers

### Step B: Review

spawn the **z-feature-review-and-fix** subagent:

> "[SUBAGENT-MODE] Review the implementation at `[plan-path]`. Read the plan files and implementation record, review all changed code, apply fixes for any issues found, and write the review record to `[plan-path]/[task-name]-review.md`. Manifest verification assets — run these affected suites if the change touches a shared contract: [verification-assets, or `not provided`]. Return the verdict, the test-execution status with its results artifact path, and a summary of issues found and fixes applied."

After the subagent returns:
- Verify `[plan-path]/[task-name]-review.md` exists
- Check the verdict:
  - **Approved** or **Approved with Reservations** → apply the Test Execution Gate below
  - **Changes Requested** → apply the Review Reject Loop from the auto-loaded orchestrator conventions (retry once, then log both summaries, proceed, and note the unresolved review in the final report)

### Committee Review and Fix Loop

When a phase caller supplies review trigger tables, keep the implementer addressable from Step A through review and fixes. Resolve the tables against the changed-file list and plan metadata. Run Reviewers A through D concurrently at `medium`. Wait for every report. Store each pass in a new `reviews/[review-cycle]/` directory and never overwrite a completed cycle.

Spawn `03m Finding Consolidator` with all four report paths. It writes a deduplicated candidate list. Then spawn `03n Finding Validator` with that list, the raw reports, validated plan, accepted contracts, changed code, tests, and run evidence. The validator proves or rejects every serious candidate and writes the final fix list.

Pass only confirmed findings to `03p Feature - Fixer`, spawned at `medium` for the fix round. Give it the validated fix list, the implementation record, and the resolved paths of every file the fix list cites. The implementer never applies its own review findings, because every confirmed finding marks a place where its model of its own code was wrong.

Require the fixer to read the cited code before it edits. Never instruct it to skip that read. Avoiding rediscovery means never re-planning a finished feature. It never means editing code you have not looked at.

Only independently confirmed `Critical`, `Blocker`, and `High` production defects open a fix round. A `not-proven` candidate becomes a Medium verification blocker. It never opens a fix round or rebuild.

A verification blocker never opens a fix round or rebuild.

Record `Medium` and `Low` findings as carry-forward evidence for phase final review. Run at most two production fix rounds.

The fixer returns that round's baseline pass set and its regression result. Pass it a recorded test baseline when the caller holds one.

After each repair round returns, run the affected suites yourself before you spawn any reviewer. The fixer's own re-run tells it whether its repair held. Your run decides whether the round is admissible, and a self-report is not evidence.

- On a regression — a test that passed at the round baseline now fails — the round failed. Return the failing test names to the fixer once. If the suite is still regressed, instruct the fixer to revert the round, then record it as a failed repair. A failed repair round never counts as a converging cycle.
- On no regression, rerun Reviewers A through D, consolidation, and validation in a new review cycle.
- When the runner is unavailable, record `regression-check: not-executed (<reason>)` and carry the round as verification pending. An unrunnable suite is never a clean regression check.

Record the baseline pass set and the regression result in the review cycle directory. Reviewers judge findings, never regressions. A repair that closes a finding and breaks a passing test is a net loss, and only the suite can see it.

After two unsuccessful rounds, rewrite the feature plan once using the fix list. Validate the rewritten plan before the rebuild.

Ensure every RED task precedes its production change. Ensure every baseline selector reaches its intended assertion without an import or setup failure.

Correct every validation failure before implementation. A correction that makes the rewritten plan executable does not count as another rewrite.

After the rebuilt implementation returns, rerun Reviewers A through D. Run post-rebuild consolidation and validation before classifying the rebuilt feature.

The post-rebuild validator is the sole authority for convergence classes. The orchestrator must not rank, merge, validate, or classify the fresh findings itself.

On the first full post-rebuild consolidation, freeze and record a finite supported-path matrix from the validated plan and accepted contracts.

Each matrix cell records its path, invariant, severity, lineage, evidence, and pass or fail status.

Later reviewers must not expand the frozen matrix silently.

Pass when no `Critical`, `Blocker`, or `High` production cells remain.

Block when one repair cycle closes no failing production cells, increases the failing high-severity count, or repeats one cell twice.

Block when a repair cycle regresses a test that passed at that cycle's baseline, whatever the matrix shows. The frozen matrix holds supported paths only, so it cannot see collateral damage.

Escalate when a reviewer identifies a new requirement or supported path outside the frozen matrix. The user decides whether to expand scope.

Otherwise, return the failing cells to `03p Feature - Fixer` and continue targeted repairs while the failing cell count strictly decreases.

Re-run Reviewers A through D, post-rebuild consolidation and validation after each repair round. Store every pass in a new review cycle.

Do not rewrite or rebuild a second time. Use the matrix decision to determine dependency status.

Only a `production-blocker` can block dependents. A missing test artifact or unavailable runner leaves implementation complete with verification pending.

### Test Execution Gate

Read the Implementer's and Reviewer's reported test-execution status. Statuses are defined in the `test-execution-evidence` instruction.

- **`executed-green`** → proceed to Step C.
- **`executed-failing`** → re-spawn the Implementer with the failing test names, then re-spawn the Reviewer. Retry once. If still failing, record it as a blocking status and proceed — the final review surfaces it.
- **`not-executed`** → do NOT treat this as green. Record `test-execution: not-executed (<reason>)` for the task and report it to the orchestrator as a blocking status. A task with unrun tests cannot be reported complete. The direct-supervisor-attestation exception in the Test Execution Evidence instruction applies only when the user-invocable root orchestrator itself receives an explicit supervisor assertion; subagents still report `not-executed` without an artifact.

Carry the per-task status forward: the orchestrator gates feature and phase completion on it.

### Step C: Commit

This step is the only commit contract in the pipeline. A caller never defines its own commit
scheme, message format, or staging rule — it runs these checkpoints. Execute every commit
directly. Never spawn a subagent for a commit.

Four checkpoints exist. Two land per unit of work, two land once per run.

| Checkpoint | When | Stages |
|---|---|---|
| Implement | After Step A returns, before review starts | The unit's source and test changes plus its pipeline documents |
| Review | After the review and any fix rounds close | The unit's directory plus any source files the fixes touched |
| QA | Once, after the consolidated QA stage runs | The QA documents and any run-level pipeline documents that stage updated |
| Final review | Once, after the final review stage returns | The final review artifact and any run-level reports it aggregates |

A caller with no consolidated QA stage or no final review stage skips that checkpoint. Skipping
one is not a missing commit.

**1. Collect files to stage.** For a unit checkpoint, read the "Files Changed" table in
`[plan-path]/[task-name]-implementation.md` and collect every source and test path it lists, plus
the pipeline documents in `[plan-path]/` — plan, context, tasks, implementation, review, and, only
if the caller ran a per-task security scan, security. For a run-level checkpoint, collect the artifacts that stage produced.

**2. Stage only those files.**

```bash
git add <file1> <file2> ... [plan-path]/[task-name]-implementation.md [plan-path]/[task-name]-review.md
# append [plan-path]/[task-name]-security.md only if the caller ran a per-task security scan
```

Do NOT use `git add -A` — staging untracked files outside the implementation record risks
including debug files or changes from adjacent tasks.

Three staging rules hold at every checkpoint:

- Never stage files from another unit's directory. A checkpoint commits one unit's work.
- Never stage untracked run output such as an evidence directory. Output is not a deliverable.
- Never stage an artifact another checkpoint owns. When a stage writes a report that a later
  checkpoint aggregates, that later checkpoint stages it.

**3. Generate a commit message** using conventional commit format. Derive type, scope, and summary
from the implementation record for a unit checkpoint, or from the stage's own artifacts for a
run-level one:

```
<type>(<scope>): <short summary — 50 chars or fewer, imperative mood>

<one paragraph: what changed and why, derived from implementation record summary>

Implements: <AC refs, e.g., AC1, AC2, AC3>
Reviewed-by: z-feature-review-and-fix
Verdict: <Approved | Approved with Reservations>
```

**Type:** `feat` (new capability) · `fix` (bug fix) · `refactor` (restructure) · `test` (tests only) · `docs` (docs only) · `chore` (config/build)

Use `test` or `chore` for a QA checkpoint and `docs` for a final review checkpoint, and drop the
`Implements:` and `Verdict:` trailers when the checkpoint commits no code.

**4. Commit.**

```bash
git commit -m "<message>"
```

**5. Verify.**

```bash
git log --oneline -1
```

Confirm the commit appears. If `git add` staged nothing, log "Nothing to commit" and proceed —
this is not an error.

### Step D: Mark Complete

Update the todo list to mark this task as completed. Proceed to the next task.

> **Note:** QA placement depends on the pipeline mode. Batch mode and per-feature mode are defined in the `pipeline-artifacts` skill; load it and follow that definition.

## Path Conventions

The orchestrator supplies both tokens in its spawn prompt.

- `[plan-path]` — the directory containing the task's plan files (phase pipeline: `dev/feature/[0N-task-name]/`; audit and test pipelines supply their own)
- `[task-name]` — the kebab-case identifier for the task, matching the plan file prefix (including the `0N-` numeric prefix for feature directories)

Token bindings are owned by the `dev-task-folder` instruction.

## Working Against a Plan

- **A plan's claim about existing code is a hypothesis.** Verify it before building to match — implementing to satisfy a false claim manufactures a dependency that never existed. Reporting the plan's error is the correct move, not working around it.
- **Checkpoint-commit steps must stage every artifact they mutate**, and resumable scopes are described as created *or modified*. Keep the checkpoint contract at the same scope as the artifacts it commits.

## Post-Loop: Documentation Update

After all tasks are complete and reported to the user, spawn the **Docs Writer** subagent to update any documentation that may be stale:

> "[SUBAGENT-MODE] [Describe what was just completed — include the pipeline type (phase/audit/test), name/scope, and list of completed tasks/features]. Update any stale documentation across the repository. Return a summary of which documents were updated and what changed."

This step is best-effort. If the Docs Writer reports no changes needed, that is expected. Do not block the pipeline on this step.

**Conditional execution:** This step only runs when the implementation pipeline was actually executed (i.e., code changes were made). If the user declined remediation or implementation after the analysis/audit phase, skip this step — no code was changed, and no branch was created.
