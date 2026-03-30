---
description: "Shared conventions for orchestrator agents that coordinate subagent pipelines. Loaded automatically for orchestrator agent definitions."
applyTo: "**/audit-code-or-infra.agent.md,**/phase-execute.agent.md,**/test-orchestrator.agent.md"
---

# Orchestrator Conventions

Orchestrators coordinate subagents — they do not perform work directly. These conventions apply to all orchestrator agents.

## Progress Tracking

- ALWAYS track progress using the todo tool — create an entry for each task/feature before starting, mark in-progress when starting, mark completed immediately after finishing

## Subagent Output Verification

- ALWAYS verify subagent outputs exist on disk before proceeding to the next pipeline step
- If a subagent returns but the expected output file doesn't exist: re-invoke once with an explicit reminder about the expected output path. If still missing after retry, report the failure to the user and stop

## Pipeline Discipline

- DO NOT skip steps or reorder the pipeline — the sequence matters
- DO NOT proceed past a subagent failure without attempting remediation
- Complete ALL steps for one task/feature before starting the next

## Working Branch

Before modifying any files, create a dedicated Git branch for the pipeline run so all changes are isolated from the default branch.

- Use type-based prefixes: `phase/<name>`, `audit/<type>-<name>`, `test/<operation>-<name>`
- Use kebab-case for the branch name, derived from the task/phase/audit name
- Run `git checkout -b <branch-name>` to create and switch to the branch
- If the branch name already exists, append a numeric suffix (`-2`, `-3`, etc.) and retry
- If the checkout fails for any other reason (e.g., uncommitted changes), report the error to the user and **stop** — do not proceed with the pipeline until the user resolves it

## Review Reject Loop

If the Reviewer returns "Changes Requested" twice for the same task:
1. Log both review summaries
2. Continue to the next pipeline step — the final review (if present) will surface unresolved issues
3. Note the unresolved review in the final report to the user
