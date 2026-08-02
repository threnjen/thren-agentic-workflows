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
| `-plan.md` | Feature - Decomposer | Plan with stages and acceptance criteria |
| `-context.md` | Feature - Plan Expander | Key files, decisions, constraints |
| `-tasks.md` | Feature - Plan Expander | Ordered checklist of work items |
| `-implementation.md` | Feature - Implementer | Files changed, AC traceability, test results |
| `-review.md` | Feature - Review and Fix | Verdict, issues found, fixes applied |
| `-qa.md` | Feature - QA Writer (per-feature mode) | QA plan for a single feature |
| `-coverage-map-qa.md` | Feature - QA Writer (per-feature mode) | AC coverage map for a single feature |
| `-report.md` | Auditor subagents, Web Researcher | Full structured audit findings or research findings with citations |
| `-summary.md` | Auditor subagents, Web Researcher | Executive summary with priority actions or recommendations |

Web Researcher writes to `dev/research/[topic-name]/`, not `dev/feature/`.

## Consolidated QA Documents

In **batch mode** the orchestrator produces one consolidated QA document after all
features/tasks are implemented and reviewed. In **per-feature mode** QA documents are produced
per-feature inside the feature's own directory (see the table above).

| Document | Phase pipeline (batch mode) | Audit pipeline | Fallback |
|----------|-----------------------------|----------------|----------|
| QA Plan | `docs/phases/[phase-name]/[phase-name]_QA.md` | `dev/[audit-name]/[audit-name]-qa.md` | `dev/feature/[phase-name]-qa.md` |
| Coverage Map | `docs/phases/[phase-name]/[phase-name]_QA_COVERAGE_MAP.md` | `dev/[audit-name]/[audit-name]-coverage-map-qa.md` | `dev/feature/[phase-name]-coverage-map-qa.md` |

Prod Code Review writes its GO/NO-GO analysis to the path the caller supplies; only when no
path is supplied does it fall back to `[first task folder]/[0N-task-name]-qa-analysis.md`.
