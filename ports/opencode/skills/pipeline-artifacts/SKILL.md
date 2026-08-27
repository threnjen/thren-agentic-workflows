---
name: pipeline-artifacts
description: "Producer/artifact table and consolidated-QA locations for the pipeline. Load when deciding where to write a pipeline artifact or what to name it — QA plan, coverage map, or pre-production analysis — when choosing between batch mode and per-feature mode QA placement, or when locating the artifacts another pipeline agent produced. Does not cover the client-deliverable engagement workspace or docs/QA_*.md."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->

# Pipeline Artifacts

Path tokens (`[0N-task-name]`, `[phase-name]`, `[audit-name]`, `[topic-name]`) are bound in
the auto-loaded path-token instruction. This file only says who writes what, and where.

## Standard File Naming

Inside `dev/feature/[0N-task-name]/`:

| Suffix | Producer | Content |
|--------|----------|---------|
| `-plan.md` | Phase - Execute | Plan with stages and acceptance criteria |
| `-context.md` | Feature - Plan Expander | Key files, decisions, constraints |
| `-tasks.md` | Feature - Plan Expander | Ordered checklist of work items |
| `-implementation.md` | Feature - Implementer | Files changed, AC traceability, test results |
| `-review.md` | 03c Reviewer - Plan Conformance | Verdict and issues found |
| `-qa.md` | Feature - QA Writer (per-feature mode) | Manual QA plan for a single feature |
| `-qa-automated.md` | Feature - QA Writer (per-feature mode) | Automated QA checks for a single feature, executed by Feature - QA Runner |
| `-coverage-map-qa.md` | Feature - QA Writer (per-feature mode) | AC coverage map for a single feature |
| `-report.md` | Auditor subagents, Web Researcher | Full structured audit findings or research findings with citations |
| `-summary.md` | Auditor subagents, Web Researcher | Executive summary with priority actions or recommendations |

Web Researcher writes to `dev/research/[topic-name]/`, not `dev/feature/`.

## Consolidated QA Documents

In **batch mode** the orchestrator produces one consolidated QA document after all
features/tasks are implemented and reviewed. In **per-feature mode** QA documents are produced
per-feature inside the feature's own directory (see the table above).

Every run produces three documents. `Feature - QA Writer` writes all three. `Feature - QA Runner`
executes the automated one and records results into it.

| Document | Phase pipeline (batch mode) | Audit pipeline | Fallback |
|----------|-----------------------------|----------------|----------|
| Manual QA Plan | `docs/phases/[phase-name]/[phase-name]_QA.md` | `dev/[audit-name]/[audit-name]-qa.md` | `dev/feature/[phase-name]-qa.md` |
| Automated QA | `docs/phases/[phase-name]/[phase-name]_QA_AUTOMATED.md` | `dev/[audit-name]/[audit-name]-qa-automated.md` | `dev/feature/[phase-name]-qa-automated.md` |
| Coverage Map | `docs/phases/[phase-name]/[phase-name]_QA_COVERAGE_MAP.md` | `dev/[audit-name]/[audit-name]-coverage-map-qa.md` | `dev/feature/[phase-name]-coverage-map-qa.md` |

The manual QA path keeps its existing name. Everything that already points at `_QA.md` still
resolves, and what it resolves to is now purely human work.

`docs/QA_AUTOMATED.md` is a different artifact with a different owner — a repository-wide runbook
written by `QA - Doc Generator` and executed by `QA - Runner` under the `qa-run` skill. Do not
conflate the two, and do not point `Feature - QA Runner` at it.

Prod Code Review writes its GO/NO-GO analysis to the path the caller supplies; only when no
path is supplied does it fall back to `[first task folder]/[0N-task-name]-qa-analysis.md`.
