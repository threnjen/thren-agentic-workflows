# Review Record: executor-renumber

## Summary
Implementation correctly renumbers the executor from `03` to `04`, adds Plan Expander to the pipeline, and updates all upstream agent references. One significant gap found: `.github/agents/README.md` retained 6 stale `03 Phase - Execute` references — all fixed during this review. Confidence: High.

## Verdict
Approved with Reservations

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1 | Verified | `.github/agents/phase-execute.agent.md:2` | `name: 04 Phase - Execute` |
| AC2 | Verified | `.github/agents/phase-execute.agent.md:4` | `agents:` includes `03 Feature - Decomposer` and `Feature - Plan Expander` |
| AC3 | Verified | `.github/agents/phase-execute.agent.md:22-40` | Step 1 checks for existing plans, conditionally invokes Decomposer |
| AC4 | Verified | `.github/agents/phase-execute.agent.md:42-55` | Step 2 invokes Plan Expander, verifies outputs |
| AC5 | Verified | `.github/instructions/orchestrator-conventions.instructions.md:3` | `applyTo` still matches `**/phase-execute.agent.md` — no change needed |
| AC6 | Verified | `.github/agents/project-planner.agent.md:9,14,19,57` | All references now `@04 Phase - Execute` |
| AC7 | Verified | `.github/agents/phase-refiner.agent.md:8,12,13,173` | All references now `@04 Phase - Execute` |
| AC8 | Verified | `.github/agents/project-planner.agent.md:21-28` | 4-column pipeline diagram shows Feature - Decomposer between Refiner and Execute |

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | 6 stale `03 Phase - Execute` references in README.md | High | `.github/agents/README.md:37,80,108,120,158,349` | AC6 (broader scope) | Fixed |
| 2 | Implementation record claimed "zero remaining `@03 Phase - Execute`" — technically true with `@` prefix but missed 6 non-`@` references in README.md | Medium | `dev/feature/executor-renumber/executor-renumber-implementation.md:45` | — | Open |
| 3 | README.md description of Phase - Execute was stale ("decomposes the phase") — didn't mention plan check or Plan Expander | Medium | `.github/agents/README.md:158-159` | AC3/AC4 | Fixed |
| 4 | README.md hidden subagents table still shows `Feature - Decomposer` (not `03 Feature - Decomposer`) and is missing `Feature - Plan Expander` entry | Low | `.github/agents/README.md:141` | — | Open (from prior tasks: decomposer-promote, plan-expander-create) |

**Status values**: Fixed (applied during this review) | Open (not addressed) | Wont-Fix (declined with rationale)

## Fixes Applied

| File | What Changed | Issue # |
|------|--------------|---------|
| `.github/agents/README.md` | Updated 6 `03 Phase - Execute` → `04 Phase - Execute` references (ASCII diagram, tables, prose, integration notes) | 1 |
| `.github/agents/README.md` | Updated Phase - Execute description to mention plan check and Plan Expander | 3 |

## Remaining Concerns
- Issue #2: Implementation record's manual verification claim was narrowly scoped (`@03` only) and missed non-`@` references — low impact since the review caught it, but worth correcting for traceability accuracy.
- Issue #4: README.md hidden subagents table is out of date with respect to the `03 Feature - Decomposer` rename and `Feature - Plan Expander` addition. These are gaps from the `decomposer-promote` and `plan-expander-create` tasks, not executor-renumber. Recommend a follow-up Docs Writer pass on `.github/agents/README.md`.

## Test Coverage Assessment
- **No automated tests** — docs-only repository
- Covered: AC1–AC8 verified via manual inspection and grep
- Missing: No remaining gaps — all stale references eliminated from `.github/agents/`

## Risk Summary
- `.github/agents/README.md` was excluded from all three task plans' scope ("Do NOT update README.md") but contained stale references that would confuse users — now fixed
- Implementation record's verification claim at line 45 is slightly misleading but low risk since review caught the gap
- Hidden subagents table in README.md still needs updating for Decomposer rename and Plan Expander addition (from prior tasks)
