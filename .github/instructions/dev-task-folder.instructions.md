---
description: "Defines the dev/feature/[0N-task-name]/ output convention used by pipeline subagents. Loaded automatically when working with agent definitions."
applyTo: ".github/agents/**"
---

# Task Output Directory Convention

All pipeline subagents write their output to `dev/feature/[0N-task-name]/` directories. Use a zero-padded two-digit prefix followed by descriptive, kebab-case names for `[task-name]` (e.g., `01-auth-login`, `02-code-audit-payments`, `03-test-bootstrap`). The numeric prefix indicates recommended execution order.

## Standard File Naming

| Suffix | Producer | Content |
|--------|----------|---------|
| `-plan.md` | Feature - Decomposer | Plan with stages and acceptance criteria |
| `-context.md` | Feature - Plan Expander | Key files, decisions, constraints |
| `-tasks.md` | Feature - Plan Expander | Ordered checklist of work items |
| `-implementation.md` | Feature - Implementer | Files changed, AC traceability, test results |
| `-review.md` | Feature - Reviewer | Verdict, issues found, fixes applied |
| `-qa.md` | Feature - QA Writer (per-feature mode) | QA plan for a single feature |
| `-coverage-map-qa.md` | Feature - QA Writer (per-feature mode) | AC coverage map for a single feature |
| `-qa-analysis.md` | Prod Code Review (per-feature mode) | GO/NO-GO verdict for a single feature |
| `-report.md` | Auditor subagents, Web Researcher | Full structured audit findings or research findings with citations |
| `-summary.md` | Auditor subagents, Web Researcher | Executive summary with priority actions or recommendations |

## Research Output Directory

Web Researcher documents are written to `dev/research/[topic-name]/` (not `dev/feature/`). Use descriptive, kebab-case names for `[topic-name]` (e.g., `react-19-suspense-breaking-changes`, `fastapi-auth-jwt-best-practices`).

## Consolidated QA Documents

In **batch mode**, QA documents are **not** produced per-feature. Instead, the orchestrator produces a single consolidated QA document after all features/tasks are implemented and reviewed.

In **per-feature mode**, QA documents are produced per-feature inside the feature's own directory (see Standard File Naming above).

| Document | Location (Phase pipeline — batch mode) | Location (Audit pipeline) | Location (Fallback) |
|----------|----------------------------------------|--------------------------|---------------------|
| QA Plan | `docs/phases/[phase-name]/[phase-name]_QA.md` | `dev/[audit-name]/[audit-name]-qa.md` | `dev/feature/[phase-name]-qa.md` |
| Coverage Map | `docs/phases/[phase-name]/[phase-name]_QA_COVERAGE_MAP.md` | `dev/[audit-name]/[audit-name]-coverage-map-qa.md` | `dev/feature/[phase-name]-coverage-map-qa.md` |
