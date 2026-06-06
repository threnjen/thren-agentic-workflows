---
name: auditor-conventions
description: "Shared conventions for all auditor subagents (Code, Infra, Refactor). Defines standard constraints, deliverables, scope determination, file-type taxonomy, common exclusions, process flow, report structure, severity levels, and output format. Each auditor extends this with domain-specific content. Use when: performing any type of audit."
---
<!-- Generated from .github/skills source-of-truth. Do not edit manually. -->
# Auditor Conventions

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

When spawnd, determine scope with the user:
- **Full codebase** — All in-scope files (default if unspecified)
- **Specific files/directories** — As specified by the user
- **Single file or module** — Deep audit of one area

Your agent definition specifies which file-type categories are in scope.

## File-Type Taxonomy

All auditable files fall into these categories. Each auditor declares which categories are in scope.

| Category | File Types |
|----------|-----------|
| **Source code** | `.py`, `.js`, `.mjs`, `.cjs`, `.ts`, `.tsx`, `.jsx`, `.java`, `.kt`, `.kts` |
| **Test files** | `tests/`, `test_*.py`, `*_test.py`, `*.test.js`, `*.test.ts`, `*.spec.js`, `*.spec.ts` |
| **Dependency manifests** | `requirements.txt`, `pyproject.toml`, `package.json`, `pom.xml`, lock files |
| **Infrastructure (IaC)** | `.tf`, `.tfvars`, `template.yaml`, `samconfig.toml`, Kubernetes manifests |
| **Docker** | `Dockerfile`, `docker-compose.yml`, `.dockerignore` |
| **CI/CD** | `.github/workflows/*.yml`, `Jenkinsfile`, `buildspec.yml` |
| **Build scripts** | `.sh`, `.ps1`, `.bat`, `Makefile`, `build.mjs` |
| **Configuration** | `.toml`, `.cfg`, `.ini`, `.env`, `.env.*`, `.editorconfig`, `.eslintrc`, `.prettierrc`, `tsconfig.json` |
| **Documentation** | `.md`, `.rst`, `.txt`, `docs/` directories |
| **Agent/customization** | `.github/agents/`, `.github/instructions/`, `.github/prompts/`, `AGENTS.md`, `copilot-instructions.md` |

### Always Excluded

Regardless of audit domain, exclude generated and cached directories:
- `__pycache__/`, `.venv/`, `node_modules/`, `target/`, `build/`, `dist/`
- Generated files and build artifacts

## Process

Discover all in-scope files → Read each thoroughly → Evaluate against all audit categories → Cross-reference for patterns → Classify severity → Report.

## Report Structure

### 1. Executive Summary

- Total files audited
- Findings by severity (Critical / High / Medium / Low)
- Top 5 highest-priority items

### 2. Findings by Category

For each audit category, present a table:

| # | File(s) | Line(s) | Severity | Finding | Detail |
|---|---------|---------|----------|---------|--------|
| 1 | `path/to/file.py` | L12-L15 | Medium | [Short title] | [Specific explanation with context] |

**Column guidelines:**
- **File(s)**: Comma-separated paths when a finding spans multiple files
- **Line(s)**: Specific line numbers or ranges. Use `—` when structural
- **Severity**: Critical, High, Medium, or Low (see Severity Levels below)
- **Finding**: Short descriptive title
- **Detail**: Specific, actionable explanation

### 3. Cross-Cutting Observations

Patterns spanning multiple files: consistency issues, DRY violations with locations, patterns to standardize.

### 4. Recommended Priority Order

1. **Quick wins** — Low effort, high impact
2. **Important fixes** — Security, correctness, or safety items
3. **Improvement pass** — Best practices, DRY cleanup, documentation, style

## Severity Levels

All auditors use this 4-level structure. Each auditor defines domain-specific meanings in its agent file.

| Level | General Guideline |
|-------|-------------------|
| **Critical** | Security vulnerability, data loss, crash, or deployment-breaking defect |
| **High** | Likely bug, missing safety controls, or significant misconfiguration |
| **Medium** | Missing best practices, DRY violations, documentation gaps, readability |
| **Low** | Style inconsistency, minor cleanup, formatting |

## Domain-Specific Extensions

Your agent definition may add sections beyond this common format (e.g., Auditor - Refactor adds Dependency Graph Observations and Risk Matrix).
