# Project Roadmap: Token Reduction Workstream

## Vision
Establish a disciplined token-efficiency baseline and reduce full pipeline token consumption while preserving planning and delivery quality.

## Phases

| Phase | Name | Status | Depends On | Complexity | Description |
|-------|------|--------|------------|------------|-------------|
| 01 | Token Efficiency Optimization | Planned | None | Medium | Reduce full-run token usage by at least 30% through prompt compaction, concise response defaults, and benchmark-validated quality gates. |

## Constraints & Non-Goals
- Preserve decomposition accuracy, test/review rigor, and edge-case discovery quality.
- Keep existing tool scope model unchanged.
- Do not introduce a new hook framework in this phase.

## Architecture Notes
This phase targets prompt and instruction layers first, using one consolidated PR and benchmark comparison against baseline behavior on the active branch.
