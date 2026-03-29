---
description: "Defines the dev/[task-name]/ output convention used by pipeline subagents. Loaded automatically when working with agent definitions."
applyTo: ".github/agents/**"
---

# Task Output Directory Convention

All pipeline subagents write their output to `dev/[task-name]/` directories. Use descriptive, kebab-case names for `[task-name]` (e.g., `auth-login`, `code-audit-payments`, `test-bootstrap`).

## Standard File Naming

| Suffix | Producer | Content |
|--------|----------|---------|
| `-plan.md` | Feature - Decomposer | Plan with stages and acceptance criteria |
| `-context.md` | Feature - Decomposer | Key files, decisions, constraints |
| `-tasks.md` | Feature - Decomposer | Ordered checklist of work items |
| `-implementation.md` | Feature - Implementer | Files changed, AC traceability, test results |
| `-review.md` | Feature - Reviewer | Verdict, issues found, fixes applied |
| `-qa.md` | Feature - QA Writer | Manual QA checklist |
| `-coverage-map-qa.md` | Feature - QA Writer | AC coverage map (automated vs manual) |
| `-report.md` | Auditor subagents | Full structured audit findings |
| `-summary.md` | Auditor subagents | Executive summary with priority actions |
