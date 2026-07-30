---
description: "Producer/artifact table and consolidated-QA locations for the agents that actually write pipeline artifacts. Audience is DERIVED by family: the numbered pipeline (0*), the auditor family, plus the three named producers outside both. Agents writing to other layouts (the client-deliverable engagement workspace, docs/QA_*.md) are deliberately excluded."
applyTo: "source_of_truth/agents/0*.md,source_of_truth/agents/auditor*.md,**/delta-auditor.md,**/test-analyst.agent.md,**/test-orchestrator.agent.md,**/web-research-specialist.agent.md"
---

# Pipeline Artifacts

Path tokens are bound in the auto-loaded path-token instruction; this file only says who
writes what, and where.

## Standard File Naming

Inside `dev/feature/[0N-task-name]/`:

| Suffix | Producer | Content |
|--------|----------|---------|
| `-plan.md` | Feature - Decomposer | Plan with stages and acceptance criteria |
| `-context.md` | Feature - Plan Expander | Key files, decisions, constraints |
| `-tasks.md` | Feature - Plan Expander | Ordered checklist of work items |
| `-implementation.md` | Feature - Implementer | Files changed, AC traceability, test results |
| `-review.md` | Feature - Reviewer | Verdict, issues found, fixes applied |
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
