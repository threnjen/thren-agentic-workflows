# Review Record: 01 Codex Source Layout

## Summary

Reviewed the feature plan, implementation record, and the four scoped documentation files. The Codex layout contract and shared documentation updates satisfy AC1 through AC5. One medium-severity documentation drift issue was found during review: the architecture table still described `.github` agent files as if they carried pinned `model:` frontmatter. That mismatch was fixed in `docs/ARCHITECTURE.md`, and the targeted follow-up checks were clean.

## Verdict
Approved

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1 | Implemented | `codex/README.md:1`; `codex/README.md:9`; `codex/README.md:20`; `codex/README.md:30` | The layout contract defines the repository-owned Codex area, current docs-only contents, reserved future categories, and layout rules. |
| AC2 | Implemented | `codex/README.md:5`; `codex/README.md:33`; `docs/ARCHITECTURE.md:219`; `docs/CODEBASE_CONTEXT.md:123`; `docs/CODEBASE_CONTEXT.md:158` | The docs clearly separate repo-owned `codex/` from runtime `.codex/`, `~/.codex/`, and `$HOME/.agents/skills/` locations. |
| AC3 | Implemented | `docs/ARCHITECTURE.md:219`; `docs/ARCHITECTURE.md:234`; `docs/ARCHITECTURE.md:241`; `docs/ARCHITECTURE.md:249`; `docs/CODEBASE_CONTEXT.md:10`; `docs/CODEBASE_CONTEXT.md:22`; `docs/CODEBASE_CONTEXT.md:145` | Both shared docs now describe Codex as a fourth platform surface with a source-to-runtime mapping model instead of a direct checked-in mirror. |
| AC4 | Implemented | `docs/phases/PHASES_OVERVIEW.md:12`; `docs/phases/PHASES_OVERVIEW.md:24` | Phase 02 explicitly calls out the repository-owned `codex/` layout and the distinct Codex runtime model. |
| AC5 | Implemented | `codex/README.md:20`; `codex/README.md:24`; `codex/README.md:27` | The README reserves future guidance, custom-agent, and skill-copy categories without creating premature directories or runtime artifacts. |

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | The architecture doc still claimed `.github` agent files carried pinned `model:` frontmatter and showed a pinned GitHub Copilot model row, which drifted from the live agent-file contract after model unpinning. | Medium | `docs/ARCHITECTURE.md:234`; `docs/ARCHITECTURE.md:249` | AC3 | Fixed |

**Status values**: Fixed (applied during this review) | Open (not addressed) | Wont-Fix (declined with rationale)

## Fixes Applied

| File | What Changed | Issue # |
|------|--------------|---------|
| `docs/ARCHITECTURE.md` | Replaced the stale `.github` agent-file format description with the actual frontmatter keys and updated the model row to state that GitHub Copilot model selection is runtime-selected rather than pinned in frontmatter. | 1 |

## Remaining Concerns
None

## Test Coverage Assessment
- Covered: AC1, AC2, AC3, AC4, AC5 via targeted readback, focused searches, and post-fix diagnostics on the four scoped files.
- Missing: No automated or executable test suite exists for this docs-only slice, so validation remains documentation-scoped.

## Risk Summary
- Shared architecture and context tables remain a drift surface whenever agent frontmatter contracts or platform-shape rules change.
- Codex is still a documentation-and-source-layout surface in this phase; later phases will need runtime validation to confirm the documented mapping behaves as described.