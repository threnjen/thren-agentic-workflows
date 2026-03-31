# DRY Audit — Executive Summary

**Date:** 2026-03-30
**Scope:** 28 files (20 agents, 4 skills, 4 instructions)

## Headline

~327 lines of duplicated content can be eliminated across agent definitions by creating 1 new skill, 3 new instructions, extending 1 existing skill, and wiring 3 orchestrators to an existing skill they currently ignore.

## Findings by Severity

| Severity | Count | Key Area |
|----------|-------|----------|
| **High** | 4 | Orchestrators don't reference existing pipeline skill; auditor triad shares ~40% identical text; docs freshness check pasted 4 times |
| **Medium** | 7 | Overlapping exclusion lists, duplicated invocation prompts, shared report templates, repeated planning conventions |
| **Low** | 2 | Structural patterns (section heading conventions) — document as convention, don't extract |

## Top 5 Priority Actions

| # | Action | Type | Impact | Effort | Lines Saved |
|---|--------|------|--------|--------|-------------|
| 1 | Wire 3 orchestrators to existing `implementation-pipeline-loop` skill | Fix wiring | Highest | Low | ~165 |
| 2 | Create `auditor-shared-conventions` skill | New skill | High | Medium | ~90 |
| 3 | Extend `implementation-pipeline-loop` with post-loop steps (Docs Writer, report template, error handling) | Extend skill | High | Medium | ~60 |
| 4 | Create `documentation-freshness-check.instructions.md` | New instruction | Medium | Low | ~45 |
| 5 | Create `no-code-blocks-planning.instructions.md` and `test-only-modification.instructions.md` | New instructions | Low-Medium | Low | ~7 |

## Proposed New Extractions

### 1 New Skill

- **`auditor-shared-conventions`** — Constraints, deliverables, scope, exclusions, process, output format shared by all 3 auditors. Complements existing `audit-report-format` (which covers output structure only).

### 3 New Instructions

- **`documentation-freshness-check.instructions.md`** → `project-planner`, `phase-refiner` — Check for README.md and CODEBASE_CONTEXT.md, recommend @Docs Writer
- **`no-code-blocks-planning.instructions.md`** → `project-planner`, `phase-refiner`, `feature-decomposer` — Link to files and reference symbols; no code blocks
- **`test-only-modification.instructions.md`** → `test-fixer`, `test-writer` — Only modify test code, never source code

### 1 Existing Skill Extension

- **`implementation-pipeline-loop`** — Add: Docs Writer step, report-to-user template, QA/Prod invocation templates, error handling section

### 1 Existing Wiring Fix

- **3 orchestrators** (`phase-execute`, `audit-code-or-infra`, `test-orchestrator`) — Replace inlined dev loop with `Load the implementation-pipeline-loop skill`

## Architectural Health: DRY Score

| Area | Score | Notes |
|------|-------|-------|
| Orchestrators | ⚠️ Poor | Pipeline loop skill exists but is orphaned; post-loop steps duplicated |
| Auditors | ⚠️ Poor | ~40% identical content across 3 files; only output format extracted |
| Planning agents | 🟡 Fair | Docs freshness check is the main violation; "no code blocks" is minor |
| Test agents | 🟡 Fair | Source-code prohibition could be extracted; otherwise clean |
| Skills & Instructions | ✅ Good | Existing extractions are well-structured; just need adoption and extension |

## Quick Reference: Which Agents Are Affected

| Proposed Extraction | Agents That Would Consume It |
|--------------------|-----------------------------|
| Wire to `implementation-pipeline-loop` | phase-execute, audit-code-or-infra, test-orchestrator |
| `auditor-shared-conventions` skill | auditor-code, auditor-infra, auditor-refactor |
| Extend `implementation-pipeline-loop` | phase-execute, audit-code-or-infra, test-orchestrator |
| `documentation-freshness-check` instruction | project-planner, phase-refiner |
| `no-code-blocks-planning` instruction | project-planner, phase-refiner, feature-decomposer |
| `test-only-modification` instruction | test-fixer, test-writer |
