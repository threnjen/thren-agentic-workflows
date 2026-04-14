# Implementation Record: Trim Template Bloat

## Summary

Reduced token usage in three agent template files by removing HTML comments (or reducing them to one-word hints), deleting example data rows from tables, and trimming a self-evident section description.

## Sibling Features

| Directory | Interaction |
|-----------|-------------|
| `dev/content-audit/canonical-tables/` | No shared files |
| `dev/content-audit/extract-shared-instructions/` | No shared files |
| `dev/content-audit/quick-wins/` | No shared files |

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | QA Writer template HTML comments reduced | Done | `.github/agents/feature-implementer.agent.md`, `.github/agents/feature-reviewer.agent.md` | QA Writer had no HTML comments; applied to Implementer and Reviewer where comments existed |
| AC2 | Implementer template example rows removed | Done | `.github/agents/feature-implementer.agent.md` | Removed 6 example rows across 3 tables |
| AC3 | Reviewer template example rows removed | Done | `.github/agents/feature-reviewer.agent.md` | Removed 5 example rows across 4 tables |
| AC4 | QA Writer self-evident descriptions trimmed | Done | `.github/agents/feature-qa-writer.agent.md` | Removed opening sentence of "What Requires Manual QA" section |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `.github/agents/feature-implementer.agent.md` | Modified | Removed 1 self-evident HTML comment (`Summary`), shortened 4 others to one-word hints, removed 6 example data rows from 3 tables | AC1 + AC2 |
| `.github/agents/feature-reviewer.agent.md` | Modified | Removed 2 self-evident HTML comments (`Summary`, `Test Coverage Assessment`), shortened 4 others to one-word hints, removed 5 example data rows from 4 tables | AC1 + AC3 |
| `.github/agents/feature-qa-writer.agent.md` | Modified | Removed self-evident opening sentence from "What Requires Manual QA" section | AC4 |

## Test Results
- **Baseline**: N/A — Markdown-only repository, no test suite
- **Final**: N/A
- **New tests added**: 0
- **Regressions**: N/A

## Deviations from Plan

- **AC1 file target**: Plan specified QA Writer for HTML comment trimming, but that file contained zero HTML comments. Applied AC1 to Implementer and Reviewer templates where the comments actually existed. This aligns with the plan's stated goal of reducing HTML comment bloat across templates.

## Gaps

None.

## Reviewer Focus Areas

- Verify the retained one-word hint comments (`<!-- "None" or list -->`, `<!-- 2-5 bullets -->`, `<!-- siblings and shared modules -->`) are sufficient for agent comprehension
- Confirm table headers and separator rows are intact after example row removal
- Check that the trimmed QA Writer sentence didn't remove important emphasis
