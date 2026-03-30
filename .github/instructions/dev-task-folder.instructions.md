---
description: "Defines the dev/feature/[task-name]/ output convention used by pipeline subagents. Loaded automatically when working with agent definitions."
applyTo: ".github/agents/**"
---

# Task Output Directory Convention

All pipeline subagents write their output to `dev/feature/[task-name]/` directories. Use descriptive, kebab-case names for `[task-name]` (e.g., `auth-login`, `code-audit-payments`, `test-bootstrap`).

## Standard File Naming

| Suffix | Producer | Content |
|--------|----------|---------|
| `-plan.md` | Feature - Decomposer | Plan with stages and acceptance criteria |
| `-context.md` | Feature - Decomposer | Key files, decisions, constraints |
| `-tasks.md` | Feature - Decomposer | Ordered checklist of work items |
| `-implementation.md` | Feature - Implementer | Files changed, AC traceability, test results |
| `-review.md` | Feature - Reviewer | Verdict, issues found, fixes applied |
| `-report.md` | Auditor subagents | Full structured audit findings |
| `-summary.md` | Auditor subagents | Executive summary with priority actions |

## Consolidated QA Documents

QA documents are **not** produced per-feature. Instead, the orchestrator produces a single consolidated QA document after all features/tasks are implemented and reviewed.

| Document | Location (Phase pipeline) | Location (Audit pipeline) | Location (Fallback) |
|----------|--------------------------|--------------------------|---------------------|
| QA Plan | `docs/phases/[phase-name]/[phase-name]_QA.md` | `dev/[audit-name]/[audit-name]-qa.md` | `dev/feature/[phase-name]-qa.md` |
| Coverage Map | `docs/phases/[phase-name]/[phase-name]_QA_COVERAGE_MAP.md` | `dev/[audit-name]/[audit-name]-coverage-map-qa.md` | `dev/feature/[phase-name]-coverage-map-qa.md` |
