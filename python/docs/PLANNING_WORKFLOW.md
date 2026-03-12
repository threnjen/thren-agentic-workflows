# Phase-Based Planning

For large migrations or multi-stage projects, use phase-based documentation in `docs/phases/`

## Phase Document Requirements

Each phase document MUST be:
- *Self-containted* - readable in a fresh context without prior conversation
- *Clearly Scoped* - Specific deliberables and success criteria
- *Status Tracked* - Clear status indicators (Complete, In Progress, Planned, Deferred)
- *Cross-referenced* Links to any backend or frontend counterparts

## QA Documentation

QA manual test documents are required for phases that include frontend/UI changes. For pure backend work, QA focs are optional but recommended when:
- API contracts change (breaking changes to request/response formats)
- Integration behavior changes (different error codes, timing, etc)
- Changes affect user-visible behavior through the frontend

When backend changes require frontend testing, coordinate with any frontent repos to create corresponding manual QA docs.

## Phase Planning Workflow

1. Create `PHASES_OVERVIEW.md` with phase tables and dependencies
2. Create `MIGRATION_PHASE_N.md` for each phase
3. Coordinate QA documentation with frontend or backend repos when applicable
4. Update overview status as phases complete
5. Archive completed phase docs (don't delete)

