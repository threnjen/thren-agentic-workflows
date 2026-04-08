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
| `-context.md` | Feature - Plan Expander | Key files, decisions, constraints |
| `-tasks.md` | Feature - Plan Expander | Ordered checklist of work items |
| `-implementation.md` | Feature - Implementer | Files changed, AC traceability, test results |
| `-review.md` | Feature - Reviewer | Verdict, issues found, fixes applied |
| `-report.md` | Auditor subagents, Web Researcher | Full structured audit findings or research findings with citations |
| `-summary.md` | Auditor subagents, Web Researcher | Executive summary with priority actions or recommendations |

## Research Output Directory

Web Researcher documents are written to `dev/research/[topic-name]/` (not `dev/feature/`). Use descriptive, kebab-case names for `[topic-name]` (e.g., `react-19-suspense-breaking-changes`, `fastapi-auth-jwt-best-practices`).

## Consolidated QA Documents

QA documents are **not** produced per-feature. Instead, the orchestrator produces a single consolidated QA document after all features/tasks are implemented and reviewed.

| Document | Location (Phase pipeline) | Location (Audit pipeline) | Location (Fallback) |
|----------|--------------------------|--------------------------|---------------------|
| QA Plan | `docs/phases/[phase-name]/[phase-name]_QA.md` | `dev/[audit-name]/[audit-name]-qa.md` | `dev/feature/[phase-name]-qa.md` |
| Coverage Map | `docs/phases/[phase-name]/[phase-name]_QA_COVERAGE_MAP.md` | `dev/[audit-name]/[audit-name]-coverage-map-qa.md` | `dev/feature/[phase-name]-coverage-map-qa.md` |
