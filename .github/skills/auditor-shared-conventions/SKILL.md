---
name: auditor-shared-conventions
description: "Shared conventions for all auditor subagents (Code, Infra, Refactor). Defines standard constraints, deliverables, scope determination, common exclusions, process flow, and output format. Each auditor extends this with domain-specific content. Use when: performing any type of audit."
---

# Auditor Shared Conventions

Common conventions for Auditor - Code, Auditor - Infra, and Auditor - Refactor. Load this skill first, then follow domain-specific instructions in your agent definition.

## Standard Constraints

- Complete the FULL audit before producing any deliverables
- DO NOT suggest fixes inline — only report findings with file:line references
- DO NOT skip any audit category — be comprehensive across all in-scope files
- DO NOT give vague feedback — every finding must cite specific files and locations
- DO NOT edit source files — you only create report documents

Your agent definition adds domain-specific constraints (scope focus, additional prohibitions).

## Deliverables

Your output is a report document saved to `dev/[audit-name]/`:
- `[audit-name]-report.md` — Full structured findings
- `[audit-name]-summary.md` — Executive summary with priority action items

Present your findings in chat first, then write the deliverables.

## Scope Determination

When invoked, determine scope with the user:
- **Full codebase** — All in-scope files (default if unspecified)
- **Specific files/directories** — As specified by the user
- **Single file or module** — Deep audit of one area

Your agent definition specifies which file types are in scope.

## Common Exclusions

Always exclude generated and cached directories regardless of audit domain:
- `__pycache__/`, `.venv/`, `node_modules/`, `target/`, `build/`, `dist/`
- Generated files and build artifacts

Your agent definition adds domain-specific exclusions.

## Source Code File Types

When auditing application source code (used by Code and Refactor auditors), detect relevant file types from the project's language:

- **Python**: `.py`
- **Node.js**: `.js`, `.mjs`, `.cjs`
- **TypeScript**: `.ts`, `.tsx`, `.jsx`
- **Java**: `.java`
- **Kotlin**: `.kt`, `.kts`

If the project uses multiple languages, include relevant types for each.

## Test File Patterns

Standard test file detection patterns:
- `tests/` directories
- `test_*.py`, `*_test.py`
- `*.test.js`, `*.test.ts`, `*.spec.js`, `*.spec.ts`

Your agent definition specifies which audit categories apply to test files.

## Process

Discover all in-scope files → Read each thoroughly → Evaluate against all audit categories → Cross-reference for patterns → Classify severity → Report.

## Output Format

Load the `audit-report-format` skill and follow its report structure:
- Executive Summary
- Findings by Category table
- Cross-Cutting Observations
- Recommended Priority Order

Use the severity meanings defined in your agent definition. Your agent definition may add domain-specific sections beyond the common format.
