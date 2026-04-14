# Implementation Record: Canonical Documentation Tables

## Summary

Replaced duplicated Skills tables, Instructions tables, Agent inventory breakdowns, and Pipeline descriptions across 3 files with brief summaries + links to the established canonical sources (`docs/ARCHITECTURE.md` and `.github/agents/README.md`). Canonical sources were not modified.

## Sibling Features

- `dev/content-audit/extract-shared-instructions/` — Extracts duplicated agent instruction blocks into shared instruction files. No overlap with this feature (different content being deduplicated).
- `dev/content-audit/trim-template-bloat/` — Reduces token usage in agent templates. No overlap (operates on `.agent.md` files, not documentation).
- `dev/content-audit/quick-wins/` — Already implemented. No conflicts.

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | Agent inventory canonical in `.github/agents/README.md`; README.md, CODEBASE_CONTEXT.md replaced with brief summary + link | Done | `README.md`, `docs/CODEBASE_CONTEXT.md` | ARCHITECTURE.md had no agent inventory table to replace (only Mermaid diagrams) |
| AC2 | Skills table canonical in `docs/ARCHITECTURE.md`; README.md, CODEBASE_CONTEXT.md, agents/README.md replaced with brief summary + link | Done | `README.md`, `docs/CODEBASE_CONTEXT.md`, `.github/agents/README.md` | |
| AC3 | Instructions table canonical in `docs/ARCHITECTURE.md`; README.md, CODEBASE_CONTEXT.md, agents/README.md replaced with brief summary + link | Done | `README.md`, `docs/CODEBASE_CONTEXT.md`, `.github/agents/README.md` | |
| AC4 | Pipeline description canonical in `.github/agents/README.md`; README.md shortened to brief overview + link | Done | `README.md` | Removed Standalone Agents table and verbose descriptions; kept 3-step summary |
| AC5 | All cross-references use relative links that work from each file's location | Done | All modified files | Links verified: README.md→`docs/ARCHITECTURE.md#skills`, CODEBASE_CONTEXT.md→`ARCHITECTURE.md#skills` (same dir), agents/README.md→`../../docs/ARCHITECTURE.md#skills` |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `README.md` | Modified | Replaced Skills table (5-row), Instructions table (5-row), Agent Definitions breakdown (3-bullet list), and Pipeline section (3-step + Standalone Agents table) with brief summaries + links | AC1–AC4: eliminate duplicated tables |
| `docs/CODEBASE_CONTEXT.md` | Modified | Replaced Agent Definitions (8-bullet detailed list), Skills listing (8-bullet), and Instructions listing (5-bullet) with condensed summaries + links | AC1–AC3: eliminate duplicated inventory |
| `.github/agents/README.md` | Modified | Replaced Skills table (4-row) and Instructions table (5-row) with links to ARCHITECTURE.md; kept header/explanation text | AC2–AC3: eliminate duplicated tables |

### Test Files

N/A — Markdown-only repository with no test suite.

## Test Results
- **Baseline**: N/A (no runnable code or tests)
- **Final**: N/A
- **New tests added**: 0
- **Regressions**: None

## Deviations from Plan

- AC1 originally listed ARCHITECTURE.md as needing replacement, but ARCHITECTURE.md contains no agent inventory table — it has a Mermaid diagram showing agent architecture. The Mermaid diagram was left untouched as part of the canonical ARCHITECTURE.md content. Only README.md and CODEBASE_CONTEXT.md had duplicate agent inventories to replace.

## Gaps

None.

## Reviewer Focus Areas

- Verify relative links work from each file's location (especially `docs/CODEBASE_CONTEXT.md` → `../.github/agents/README.md` which navigates up from `docs/`)
- Confirm the condensed Agent Definitions in CODEBASE_CONTEXT.md still provides enough context for agent orientation without the full per-agent bullet list
- Check that the Pipeline section removal in README.md (Standalone Agents table) doesn't leave a gap — standalone agents are now only discoverable via agents/README.md link
