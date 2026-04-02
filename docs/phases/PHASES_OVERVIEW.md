# Project Roadmap: Agent Pipeline Restructuring

## Vision
Restructure the agent pipeline to give users a review gate between feature decomposition and execution, improving plan quality and user control.

## Phases

| Phase | Name | Status | Depends On | Complexity | Description |
|-------|------|--------|------------|------------|-------------|
| 01    | Split Feature Decomposer from Phase Execute | Planned | None | Medium | Extract decomposition into user-facing `03 Feature - Decomposer` (plan-only), renumber executor to `04`, add hidden `Feature - Plan Expander` subagent |

## Constraints & Non-Goals
- Do not change the `-plan.md` template content (sections A–F)
- Do not modify audit or test orchestrator pipelines
- Do not change the implementation pipeline loop (Implement → Review → Commit)
- README.md and CODEBASE_CONTEXT.md updates handled separately via Docs Writer

## Architecture Notes
- Follows the existing dual-use agent pattern (like Docs Writer)
- New hidden subagent (`Feature - Plan Expander`) keeps the context+tasks generation scoped and minimal
- `04 Phase - Execute` auto-detects whether plans already exist, maintaining backward compatibility
