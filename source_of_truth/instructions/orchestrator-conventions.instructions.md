---
description: "Shared conventions for orchestrator agents that coordinate subagent pipelines, including the end-of-run graph rebuild (merged from graph-rebuild-hook). Audience is ENUMERATED deliberately - the four pipeline orchestrators are an arbitrary subset with no filename family. Add any new agent that coordinates a subagent pipeline, and inline this file into its claude/agents/ counterpart."
applyTo: "**/auditor.agent.md,**/delta-auditor.agent.md,**/04-phase-execute.agent.md,**/test-orchestrator.agent.md"
---

# Orchestrator Conventions

Orchestrators coordinate subagents — they do not perform work directly. These conventions apply to all orchestrator agents.

## Common Constraints

- DO NOT write source code, test files, or configuration directly
- Orchestrators normally delegate plan documents, review records, and QA plans. `04 Phase - Execute` may write its lightweight plans and living manifest because it owns decomposition and scheduling. It still delegates context, tasks, review records, and QA plans.
- ALWAYS ask the user before proceeding to the fix/remediation phase

## Working Branch

Before modifying any files, create a dedicated Git branch for the pipeline run so all changes are isolated from the default branch.

- Use type-based prefixes: `phase/<name>`, `audit/<type>-<name>`, `test/<operation>-<name>`
- Use kebab-case for the branch name, derived from the task/phase/audit name
- Run `git checkout -b <branch-name>` to create and switch to the branch
- **If the branch already exists, resume it: `git checkout <branch-name>`.** An existing branch means an upstream agent already opened it for this work (the Phase Refiner commits the planning docs onto `phase/<slug>` before handing off). Never create a variant name such as `-2` — that splits planning documents and implementation commits across two branches
- If the checkout fails for any other reason (e.g., uncommitted changes), report the error to the user and **stop** — do not proceed with the pipeline until the user resolves it

## Progress Tracking

- ALWAYS track progress using the todo tool — create an entry for each task/feature before starting, mark in-progress when starting, mark completed immediately after finishing

## Subagent Output Verification

- ALWAYS verify subagent outputs exist on disk before proceeding to the next pipeline step
- If a subagent returns but the expected output file doesn't exist: re-spawn once with an explicit reminder about the expected output path. If still missing after retry, report the failure to the user and stop

## Pipeline Discipline

- DO NOT skip steps or reorder the pipeline — the sequence matters. Phase - Execute may recompute dependency order only at its documented level-closure boundary.
- DO NOT proceed past a subagent failure without attempting remediation
- Complete ALL steps for one task/feature before starting the next

## Review Reject Loop

This is the complete rule; other documents reference it rather than restating it.

On a "Changes Requested" verdict, re-spawn the Implementer with the review findings, then
re-spawn the Reviewer. **Retry once.** If the second review is also "Changes Requested":
1. Log both review summaries
2. Continue to the next pipeline step — the final review (if present) will surface unresolved issues
3. Note the unresolved review in the final report to the user

## Pipeline Completion Report

After the final review subagent returns, present results using this structure. Adapt field labels to your domain (Phase/Audit/Operation, Features/Tasks).

**If GO or GO WITH CONDITIONS:**

> **[Pipeline type] complete.**
>
> **[Scope label]:** [name]
> **[Items label] completed:** [count]
> **Final verdict:** [GO / GO WITH CONDITIONS]
>
> | [Item] | Impl | Review |
> |--------|------|--------|
> | [item-1] | Done | Approved |
>
> **Graph rebuild:** [OK, or the non-zero exit and its error]
>
> **Next step:** Push the branch and open a PR for review.
>
> [If GO WITH CONDITIONS: list the conditions]

**If NO-GO:**

Report the blocking items from the Final Review and recommend specific remediation. Do NOT retry automatically — the user should review the NO-GO findings before deciding how to proceed.

## Graph Rebuild Hook

Immediately after printing the user-facing completion report — whichever step produces it, including an aborted, partial, or NO-GO run — run this once via the `execute` tool, without asking for confirmation:

```
code-review-graph build
```

Exactly once per run, after the report is printed. Never before it, never a second time.

**On non-zero exit:** record it in the completion report's `Graph rebuild` field above and continue. Do not fail the pipeline and do not re-run any step — the rebuild is a best-effort index update.

## Load Canary

When this file is loaded, state once, before your first substantive output: *"Instruction loaded: orchestrator-conventions."* Then proceed normally. Also state *"Graph rebuild queued."* when you queue a graph rebuild.
