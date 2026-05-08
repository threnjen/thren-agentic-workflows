# Implementation Record: 02 Codex Porting Guide

## Summary

Created `codex/CODEX_PORTING_GUIDE.md` as the repository-owned mapping guide for porting `.github/instructions/`, `.github/agents/`, and `.github/skills/` into Codex-native destinations. The guide makes the global AGENTS rule explicit, documents split-destination instruction routing, names required custom-agent TOML fields, explains Codex skill-directory expectations, and adds a portability classification model tied back to the `codex/` landing zone.

## Sibling Features

- `01-codex-platform-reference`: establishes Codex runtime behavior and required fields that this guide references.
- `01-codex-source-layout`: defines the `codex/` source-area contract and runtime-vs-authoring split that this guide depends on.
- `02-codex-macos-setup-guide`: parallel doc slice with disjoint output scope.
- `03-codex-pilot-slice-definition`: depends on this guide to choose a pilot that exercises the documented mapping rules.
- `02-codex-source-layout`: sibling directory exists in `dev/feature/` but contains no plan file yet, so it did not affect this implementation.

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | `codex/CODEX_PORTING_GUIDE.md` maps `.github/instructions/` content into Codex global AGENTS guidance and agent `developer_instructions` rather than treating instructions as a repo-local file-for-file copy surface. | Done | `codex/CODEX_PORTING_GUIDE.md` | Includes split-destination routing and `applyTo` rewrite guidance. |
| AC2 | The guide maps `.github/agents/` into Codex custom-agent TOML files and explains the required Codex fields and the main non-portable differences from Markdown agent manifests. | Done | `codex/CODEX_PORTING_GUIDE.md` | Names required fields `name`, `description`, and `developer_instructions`, plus field-model differences. |
| AC3 | The guide maps `.github/skills/` into Codex skill directories and explains how directory-based skills differ from the current master skill structure. | Done | `codex/CODEX_PORTING_GUIDE.md` | Covers required `SKILL.md`, optional assets, runtime discovery roots, and source-vs-runtime separation. |
| AC4 | The guide classifies what content is portable, what content must be transformed, and what content is GitHub-only or otherwise non-portable. | Done | `codex/CODEX_PORTING_GUIDE.md` | Adds a dedicated portability classification table and per-surface portability notes. |
| AC5 | The guide makes the global AGENTS rule explicit and durable: AGENTS-derived content maps to the global Codex AGENTS layer, not either repository's checked-in `AGENTS.md`. | Done | `codex/CODEX_PORTING_GUIDE.md` | Elevated into the guide's core rule and repeated in final guardrails. |
| AC6 | The guide references the repository-owned Codex source area defined in `codex/README.md` so future ported artifacts have a documented landing zone. | Done | `codex/CODEX_PORTING_GUIDE.md` | Landing-zone section and workflow both point back to `codex/README.md`. |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `codex/CODEX_PORTING_GUIDE.md` | Create | Added the new Codex mapping guide covering instructions, agents, skills, portability classes, landing-zone rules, and guardrails. | Satisfies all planned acceptance criteria for the feature slice. |
| `dev/feature/02-codex-porting-guide/02-codex-porting-guide-implementation.md` | Create | Added the implementation record for reviewer handoff. | Required artifact for the feature-review stage. |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| None | N/A | No automated test files exist for this docs-only slice. | Validation used the planned manual mapping audit. |

## Test Results
- **Baseline**: N/A, no executable tests or docs-check harness present in repository context before implementation
- **Final**: N/A, no executable tests or docs-check harness present after implementation
- **New tests added**: 0
- **Regressions**: None

## Deviations from Plan

- Automated Red-Green-Refactor execution was not possible because the repository context for this slice has no test runner, no docs-check harness, and a recorded baseline of no tests found. Validation used the planned manual mapping audit against the live `.github/` tree, `codex/CODEX_PLATFORM_REFERENCE.md`, `codex/README.md`, and the Phase 02 summary.

## Gaps

- No automated documentation validation was added; review remains a manual acceptance-criteria audit for this feature.

## Reviewer Focus Areas
- Confirm the instructions section preserves the hard rule that AGENTS-derived content maps to the global Codex AGENTS layer rather than checked-in repository `AGENTS.md` files.
- Confirm the agents section names the correct required Codex fields and does not imply Markdown manifest parity.
- Confirm the skills section draws the right boundary between repository-owned `codex/` sources and installed runtime skill directories.
- Confirm the portability matrix is strict enough to prevent file-for-file copying of `.github/instructions/` or GitHub-only metadata.