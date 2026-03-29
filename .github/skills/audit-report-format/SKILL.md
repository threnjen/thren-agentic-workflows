---
name: audit-report-format
description: "Format audit findings as structured reports. Use when: writing audit reports, producing audit findings tables, creating executive summaries for audits, formatting severity-classified findings, or any task that outputs audit deliverables to dev/[audit-name]/."
---

# Audit Report Format

Shared report structure for all audit subagents (Code, Infra, Refactor). Defines the common deliverable format, findings table, severity levels, and report sections. Individual auditors extend this with domain-specific content.

## When to Use

- Writing audit findings to `dev/[audit-name]/`
- Formatting any structured audit report
- Producing an executive summary of audit findings

## Deliverable Structure

Each audit produces two files in `dev/[audit-name]/`:

- `[audit-name]-report.md` — Full structured findings by category
- `[audit-name]-summary.md` — Executive summary with priority action items

## Report Sections

### 1. Executive Summary

- Total files audited
- Findings by severity (Critical / High / Medium / Low)
- Top 5 highest-priority items

### 2. Findings by Category

For each audit category, present a table:

#### [Category Name]

| # | File(s) | Line(s) | Severity | Finding | Detail |
|---|---------|---------|----------|---------|--------|
| 1 | `path/to/file.py` | L12-L15 | Medium | [Short title] | [Specific explanation with context] |

**Column guidelines:**
- **File(s)**: One or more files. Use comma-separated paths when a finding spans multiple files (e.g., `services/user.py`, `api/routes.py`)
- **Line(s)**: Specific line numbers or ranges (e.g., `L12`, `L12-L15`). Use `—` when the finding is structural and no single line applies
- **Severity**: One of Critical, High, Medium, Low (see Severity Levels below)
- **Finding**: Short descriptive title
- **Detail**: Specific explanation — must be actionable, not vague

### 3. Cross-Cutting Observations

Patterns that span multiple files:
- Consistency issues observed across modules or configuration files
- DRY violations with locations of each duplicate
- Patterns that should be standardized

### 4. Recommended Priority Order

Numbered list of what to address first, grouped by effort level:

1. **Quick wins** — Low effort, high impact
2. **Important fixes** — Security, correctness, or safety items
3. **Improvement pass** — Best practices, DRY cleanup, documentation, style

## Severity Levels

All auditors use this 4-level structure. The *meanings* are domain-specific — each auditor defines what Critical/High/Medium/Low means for its domain in its own agent file.

| Level | General Guideline |
|-------|-------------------|
| **Critical** | Security vulnerability, data loss, crash, or deployment-breaking defect |
| **High** | Likely bug, missing safety controls, or significant misconfiguration |
| **Medium** | Missing best practices, DRY violations, documentation gaps, readability |
| **Low** | Style inconsistency, minor cleanup, formatting |

## Domain-Specific Extensions

Individual auditors add sections beyond this common format:

- **Auditor - Refactor** adds: Dependency Graph Observations, Risk Matrix, Architectural Health Score
- **Auditor - Code** and **Auditor - Infra** use the common format as-is

These extensions are defined in each auditor's agent file, not in this skill.
