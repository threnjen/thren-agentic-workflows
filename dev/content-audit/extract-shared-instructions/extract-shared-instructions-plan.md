# Plan: Extract Shared Instructions

Extract content blocks duplicated across 2+ agents into shared instruction files.

## Acceptance Criteria

- AC1: "Challenge User Assumptions" block extracted to `.github/instructions/challenge-assumptions.instructions.md` with `applyTo` for planner + refiner; inline blocks removed from both agents, replaced with reference
- AC2: "Proactive research over asking the user" paragraph extracted to `.github/instructions/proactive-research.instructions.md` with `applyTo` for planner + refiner + debugger; inline paragraphs removed
- AC3: Verbose phrasing in phase-refiner.agent.md opening paragraph shortened
- AC4: Feature-decomposer.agent.md "Directory Numbering Convention" section replaced with reference to feature-plan-set skill
- AC5: Subagent autonomy declarations condensed where possible

## Non-Goals

- Do not change agent behavior or intent
- Do not extract content that is intentionally customized per-agent
