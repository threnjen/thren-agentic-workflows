# Refactor Brevity Audit — Executive Summary

**Date:** 2026-03-30
**Scope:** `.github/agents/`, `.github/skills/`, `.github/instructions/` (31 files)

## Verdict

The agent/skill/instruction architecture is well-designed — orchestrators delegate, skills extract shared formats, and instructions inject cross-cutting conventions. However, the **extraction is structurally incomplete**: shared files exist but agents still restate the content they provide. Three structural patterns account for most of the reducible content: (1) two auditor skills that should be one, (2) orchestrator-conventions instruction that doesn't own all shared orchestrator behavior, and (3) auditor exclusion lists that are inverse mirrors of each other.

**Relationship to Code Audit:** The [code-brevity-audit](../code-brevity-audit/code-brevity-audit-report.md) identified ~1,550 words of reducible prose and DRY violations. This audit identifies **~735 additional words** addressable through structural reorganization, of which ~400–500 words are net-new savings beyond what the code audit covers.

## Findings by Severity

| Severity | Count | Key Themes |
|----------|-------|------------|
| **High** | 3 | Auditor skill split creates transitive loading; orchestrator-conventions underutilized; auditor exclusion lists are inverse mirrors needing shared taxonomy |
| **Medium** | 6 | read-only instruction under-enriched; GO/NO-GO templates unextracted; skill "When to Use" vestigial; README duplicates dev-task-folder; decomposition rules duplicated; phase-refiner extraction candidate |
| **Low** | 4 | Broad applyTo globs; README tables incomplete; transitive skill chain; phase-refiner size |
| **Total** | **13** | |

## Top 5 Priority Actions

1. **Merge `auditor-shared-conventions` + `audit-report-format` into one skill** — These are always loaded together by the same 3 agents via a transitive chain. Merge eliminates 1 skill directory, removes the two-hop loading, and saves ~70 words. **Effort: Low. Risk: Low.**

2. **Enrich `orchestrator-conventions.instructions.md` to absorb shared orchestrator content** — Move common constraints ("DO NOT write source code/tests/config") and the full branch creation procedure into the instruction. Then trim all 3 orchestrators. Saves ~240 words. **Effort: Medium. Risk: Low.**

3. **Restructure auditor file-type scoping into category-based selection** — Define file-type categories (source code, infra, docs, config, tests, deps) in the merged auditor skill. Each auditor selects included categories (~3 lines) instead of maintaining exclusion lists (~20 lines each). Saves ~50 lines across 3 auditors. **Effort: Medium. Risk: Low-Medium.**

4. **Enrich `read-only-agent.instructions.md` with commonly restated constraints** — Add "no code blocks" and "no code-level details" to the instruction. Trim 4 agents that restate these. Saves ~160 words. **Effort: Low. Risk: Low.**

5. **Add GO/NO-GO reporting template to shared infrastructure** — Move the ~15-line reporting pattern to `orchestrator-conventions.instructions.md` or `implementation-pipeline-loop` skill. Saves ~100 words across 2 orchestrators. **Effort: Low. Risk: Low.**

## Dependency Highlights

- **Highest fan-in:** `auditor-shared-conventions` skill (3 auditors + transitive skill), `read-only-agent` instruction (8 agents)
- **Highest fan-out:** `audit-code-or-infra.agent.md` (13 dependencies: 9 subagents + 1 skill + 3 instructions)
- **Only transitive chain:** `auditor-shared-conventions` → `audit-report-format` (merging resolves this)
- **Orphaned files:** None
- **Overly broad loading:** 2 instructions loaded into all 20 agents when ~12 need them (acceptable tradeoff)

## Estimated Impact

| Tier | Word Savings | Files Touched |
|------|-------------|---------------|
| Quick wins | ~185 words | 9 files |
| Important restructurings | ~550 words | 10 files |
| **Total actionable** | **~735 words** | **~19 files** |

## Full Report

See [refactor-brevity-audit-report.md](refactor-brevity-audit-report.md) for all 13 findings with dependency graphs, structural analysis, risk matrix, and migration plans.
