---
name: pipeline-artifacts
description: "Producer/artifact table and consolidated-QA locations for the pipeline. Load when deciding where to write a pipeline artifact or what to name it — QA plan, coverage map, or pre-production analysis — when choosing between batch mode and per-feature mode QA placement, or when locating the artifacts another pipeline agent produced. Does not cover the client-deliverable engagement workspace or docs/QA_*.md."
---

# Pipeline Artifacts

The auto-loaded path-token instruction binds these path tokens: `[0N-task-name]`, `[phase-name]`, `[audit-name]`, and `[topic-name]`.
This file identifies each artifact's producer, location, and content.

## Standard File Naming

Store the files inside `dev/feature/[0N-task-name]/`:

| Suffix | Producer | Content |
|--------|----------|---------|
| `-plan.md` | Feature - Plan Author for Phase; Audit or Test planner otherwise | Plan with stages and acceptance criteria |
| `-delta.md` | Feature - Plan Author in Phase selection mode | Selected feature's verified repository findings |
| `-context.md` | Audit or Test planner | Key files, decisions, constraints |
| `-tasks.md` | Audit or Test planner | Ordered checklist of work items |
| `-implementation.md` | Feature - Implementer | Files changed, AC traceability, test results |
| `-review.md` | 03c Reviewer - Plan Conformance | Verdict and issues found |
| `-qa.md` | Feature - QA Writer (per-feature mode) | Manual QA plan for a single feature |
| `-qa-automated.md` | Feature - QA Writer (per-feature mode) | Automated QA checks for a single feature, executed by Feature - QA Runner |
| `-coverage-map-qa.md` | Feature - QA Writer (per-feature mode) | AC coverage map for a single feature |
| `-report.md` | Auditor subagents, Web Researcher | Full structured audit findings or research findings with citations |
| `-summary.md` | Auditor subagents, Web Researcher | Executive summary with priority actions or recommendations |

Web Researcher writes to `dev/research/[topic-name]/`, not `dev/feature/`.

Phase pipeline agents require the plan, delta, and execution manifest. Audit and Test pipeline agents require the plan, context, and tasks. Shared agents receive `pipeline: phase | audit | test` and never infer the contract from present files.

## Consolidated QA Documents

In **batch mode**, the orchestrator produces one consolidated QA document after the pipeline implements and reviews all
features/tasks. In **per-feature mode**, place QA documents inside each feature's own directory (see the table above).

Every run produces three documents. `Feature - QA Writer` writes all three. `Feature - QA Runner`
executes the automated QA document and records results in that document.

| Document | Phase pipeline (batch mode) | Audit pipeline | Fallback |
|----------|-----------------------------|----------------|----------|
| Manual QA Plan | `docs/phases/[phase-name]/[phase-name]_QA.md` | `dev/[audit-name]/[audit-name]-qa.md` | `dev/feature/[phase-name]-qa.md` |
| Automated QA | `docs/phases/[phase-name]/[phase-name]_QA_AUTOMATED.md` | `dev/[audit-name]/[audit-name]-qa-automated.md` | `dev/feature/[phase-name]-qa-automated.md` |
| Coverage Map | `docs/phases/[phase-name]/[phase-name]_QA_COVERAGE_MAP.md` | `dev/[audit-name]/[audit-name]-coverage-map-qa.md` | `dev/feature/[phase-name]-coverage-map-qa.md` |

The manual QA path keeps its existing name. Existing references to `_QA.md` still resolve to the manual QA plan.
The resolved path now serves human work only.

`docs/QA_AUTOMATED.md` is a separate artifact with a separate owner. `QA - Doc Generator` writes it as a
repository-wide runbook. `QA - Runner` executes it under the `qa-run` skill. Do not conflate these documents,
and do not point `Feature - QA Runner` at `docs/QA_AUTOMATED.md`.

Prod Code Review writes its GO/NO-GO analysis to the path the caller supplies. If the caller supplies no path,
it falls back to `[first task folder]/[0N-task-name]-qa-analysis.md`.
