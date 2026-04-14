# Review Record: Extract Shared Instructions

## Summary
Implementation is solid — all five acceptance criteria are met, extracted content preserves original behavioral intent, no remnant blocks or structural defects in agent files. One documentation sync gap found (ARCHITECTURE.md missing the two new instruction entries) and fixed during this review. High confidence in the result.

## Verdict
Approved with Reservations

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1 | Verified | `.github/instructions/challenge-assumptions.instructions.md` (created), `project-planner.agent.md`, `phase-refiner.agent.md` | Generic wording works for both contexts. `applyTo` glob matches `documentation-freshness-check` pattern. No remnant "Challenge User Assumptions" blocks in agents. |
| AC2 | Verified | `.github/instructions/proactive-research.instructions.md` (created), `project-planner.agent.md`, `phase-refiner.agent.md`, `debugger.agent.md` | Both "Whenever internet research..." and bold "Proactive research" paragraphs removed. Debugger Key Principles bullet removed. `applyTo` correctly targets all three agents. |
| AC3 | Verified | `phase-refiner.agent.md:8` | Opening condensed to single sentence preserving all semantic content (Phase Iteration Specialist, both entry points, key activities). |
| AC4 | Verified | `feature-decomposer.agent.md:20-22` | Code block + 4 bullet points replaced with single-line reference to `feature-plan-set` skill. Skill confirmed to contain identical numbering rules (lines 23-27). |
| AC5 | Verified | `feature-plan-expander.agent.md:10`, `git-commit.agent.md:10`, `test-analyst.agent.md` | Redundant "do not ask questions or wait for confirmation" removed where "autonomously" already conveys it. Scope limitation (not touching implementer/reviewer) is well-justified. |

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | ARCHITECTURE.md instructions table missing `challenge-assumptions` and `proactive-research` rows | High | `docs/ARCHITECTURE.md:180-186` | AC1, AC2 | Fixed |
| 2 | ARCHITECTURE.md mermaid diagram missing I6 and I7 instruction nodes | High | `docs/ARCHITECTURE.md:34-40` | AC1, AC2 | Fixed |
| 3 | AC1 says "replaced with reference" but no inline reference added in agent files | Low | `project-planner.agent.md`, `phase-refiner.agent.md` | AC1 | Wont-Fix |

**Status values**: Fixed (applied during this review) | Open (not addressed) | Wont-Fix (declined with rationale)

### Issue #3 Rationale (Wont-Fix)
The `applyTo` auto-load mechanism IS the reference — instructions inject automatically without agents needing to name them. Other always-on instructions (`codebase-context-bootstrap`, `read-only-agent`) follow the same pattern. Only `documentation-freshness-check` has an inline reference because it's triggered at a specific workflow step. The AC wording "replaced with reference" is satisfied by the `applyTo` glob mechanism itself.

## Fixes Applied

| File | What Changed | Issue # |
|------|--------------|---------|
| `docs/ARCHITECTURE.md` | Added `challenge-assumptions` (I6) and `proactive-research` (I7) to mermaid diagram | 2 |
| `docs/ARCHITECTURE.md` | Added two rows to instructions table for the new instruction files | 1 |

## Remaining Concerns
- Issue #3 (Low): No inline "see auto-loaded instructions" reference for challenge-assumptions or proactive-research in agent files. Deferred — consistent with how other always-on instructions work.

## Test Coverage Assessment
- N/A — Markdown-only repository with no runnable tests
- Verification performed via structural checks: grep for remnant blocks, awk for double blank lines, manual review of frontmatter patterns and content accuracy

## Risk Summary
- `docs/ARCHITECTURE.md` was not listed in the implementation record's changed files — suggests documentation sync is easy to miss when creating new instruction files. Future implementations should include ARCHITECTURE.md in the change list whenever instruction or skill files are added/removed.
- The generic wording in `challenge-assumptions.instructions.md` ("your role" / "planning documents") reads naturally for both planner and refiner contexts, but if a third agent type were added to `applyTo` the wording might need revisiting.
- The deviation in AC2 scope (removing "Whenever internet research..." paragraphs alongside the bold "Proactive research" paragraphs) was the correct call — leaving the similar paragraph would have been redundant with the extracted instruction.
