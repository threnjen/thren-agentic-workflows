# Implementation Record: Extract Shared Instructions

## Summary

Extracted two duplicated content blocks ("Challenge User Assumptions" and "Proactive research over asking the user") from agent files into shared instruction files with `applyTo` targeting. Also shortened the phase-refiner opening, replaced the decomposer numbering section with a skill reference, and condensed subagent autonomy declarations.

## Sibling Features

| Directory | Interaction |
|-----------|-------------|
| `dev/content-audit/canonical-tables/` | No overlap — canonical-tables deals with documentation tables, not agent content blocks |
| `dev/content-audit/quick-wins/` | No overlap — quick-wins targets style guides, README, and QA writer |
| `dev/content-audit/trim-template-bloat/` | No overlap — trim-template-bloat targets template HTML comments and example rows |

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | Extract "Challenge User Assumptions" to shared instruction | Done | `.github/instructions/challenge-assumptions.instructions.md` (created), `project-planner.agent.md`, `phase-refiner.agent.md` | Merged planner/refiner variants into generic wording ("your role" instead of role-specific) |
| AC2 | Extract "Proactive research" to shared instruction | Done | `.github/instructions/proactive-research.instructions.md` (created), `project-planner.agent.md`, `phase-refiner.agent.md`, `debugger.agent.md` | Removed both "Whenever internet research..." and "Proactive research over asking the user" paragraphs from planner/refiner; removed bullet from debugger Key Principles |
| AC3 | Shorten phase-refiner opening paragraph | Done | `phase-refiner.agent.md` | Condensed from 42 words to 28 words, preserved all semantic content |
| AC4 | Replace decomposer numbering section with skill reference | Done | `feature-decomposer.agent.md` | Replaced code block + 4 bullet points with single-line reference to `feature-plan-set` skill |
| AC5 | Condense subagent autonomy declarations | Done | `feature-plan-expander.agent.md`, `git-commit.agent.md`, `test-analyst.agent.md` | Removed redundant "do not ask questions or wait for confirmation" where "autonomously" already implies it |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `.github/instructions/challenge-assumptions.instructions.md` | Created | Shared instruction with `applyTo` for planner + refiner | AC1: extract duplicated challenge-assumptions block |
| `.github/instructions/proactive-research.instructions.md` | Created | Shared instruction with `applyTo` for planner + refiner + debugger | AC2: extract duplicated proactive-research block |
| `.github/agents/project-planner.agent.md` | Modified | Removed "Challenge User Assumptions" section; removed "Whenever internet research..." and "Proactive research over asking the user" paragraphs from Phase 1 Discovery | AC1, AC2 |
| `.github/agents/phase-refiner.agent.md` | Modified | Shortened opening paragraph; removed "Challenge User Assumptions" section; removed proactive research paragraphs from Phase 2A | AC1, AC2, AC3 |
| `.github/agents/debugger.agent.md` | Modified | Removed "Proactive research over asking the user" bullet from Key Principles | AC2 |
| `.github/agents/feature-decomposer.agent.md` | Modified | Replaced "Directory Numbering Convention" section body with skill reference | AC4 |
| `.github/agents/feature-plan-expander.agent.md` | Modified | Condensed autonomy declaration | AC5 |
| `.github/agents/git-commit.agent.md` | Modified | Condensed autonomy declaration | AC5 |
| `.github/agents/test-analyst.agent.md` | Modified | Condensed dual-mode autonomy explanation | AC5 |
| `docs/CODEBASE_CONTEXT.md` | Modified | Updated instruction file count (5→7) and added new instruction entries to folder structure | Kept documentation in sync |

### Test Files

N/A — Markdown-only repository with no test suite.

## Test Results

N/A — No runnable code or tests in this repository.

## Deviations from Plan

- **AC2 scope**: The "Whenever internet research would improve your understanding..." paragraphs in planner and refiner were also removed (not just the bold "Proactive research" paragraphs). These were redundant with the extracted instruction and removing only the bold paragraph would leave nearly-duplicate guidance in place.
- **AC5 scope**: `feature-implementer.agent.md` and `feature-reviewer.agent.md` were not modified because their autonomy declarations include role-specific context ("Make sensible defaults" / "apply fixes directly") that serves a distinct purpose beyond the generic autonomy statement.

## Gaps

None.

## Reviewer Focus Areas

- Verify `applyTo` globs in the two new instruction files match the correct agent filenames
- Confirm the generic wording in `challenge-assumptions.instructions.md` ("your role" / "planning documents") works for both planner and refiner contexts
- Check that the phase-refiner Phase 2A still reads naturally after removing two consecutive paragraphs
- Confirm the decomposer numbering section now correctly references the skill (the skill does contain the same numbering rules)
