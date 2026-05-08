# Implementation Record: 02 Codex macOS Setup Guide

## Summary

`codex/MACOS_SETUP_AND_SYMLINKS.md` was authored and verified against all five acceptance criteria. The guide covers macOS runtime install targets, the source-versus-runtime separation, idempotent symlink examples for all four runtime locations, preflight inspection steps, parent-directory creation, rollback guidance, and the global AGENTS policy. The file was already present in the `codex/` directory as a wave-2 output; this record confirms it satisfies the full AC set.

## Sibling Features

| Sibling | Wave | Relationship |
|---------|------|--------------|
| `01-codex-platform-reference` | 1 | Upstream dependency — provides verified macOS install paths and discovery rules used to ground the guide |
| `01-codex-source-layout` | 1 | Upstream dependency — defines `codex/` as the repository-owned authoring area; the guide's symlink source paths point there |
| `02-codex-porting-guide` | 2 | Parallel sibling — disjoint files; terminology (global AGENTS layer, custom agents, skills) aligned across both guides |
| `03-codex-pilot-slice-definition` | 3 | Downstream — will consume the install-path and validation model described in this guide |

No shared modules were touched that could conflict with sibling features.

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | macOS install locations documented for global AGENTS, custom agents, skills, and config | ✅ Done | `codex/MACOS_SETUP_AND_SYMLINKS.md` | Runtime Targets table covers all five paths |
| AC2 | Explicit, reversible symlink examples for `~/.codex/AGENTS.md`, `~/.codex/AGENTS.override.md`, `~/.codex/agents/`, and `$HOME/.agents/skills/` pointing to repo-owned Codex artifacts | ✅ Done | `codex/MACOS_SETUP_AND_SYMLINKS.md` | "Idempotent Symlink Examples" section; examples use `ln -sfn` and repo-owned source paths |
| AC3 | Relationship between repo-owned `codex/` and runtime `.codex/` / `$HOME/.agents/skills/` explained | ✅ Done | `codex/MACOS_SETUP_AND_SYMLINKS.md` | "Source Versus Runtime On macOS" table with four-row separation |
| AC4 | Guardrails for idempotent setup: `ln -sfn`, parent-directory creation, inspect/replace | ✅ Done | `codex/MACOS_SETUP_AND_SYMLINKS.md` | Preflight Checks, Parent Directories, Idempotent Symlink Examples, Replace Or Roll Back Safely sections |
| AC5 | Global AGENTS rule explicit: content installs into global Codex AGENTS layer, not repo-local AGENTS files | ✅ Done | `codex/MACOS_SETUP_AND_SYMLINKS.md` | "Global AGENTS Policy" section at top of guide |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `codex/MACOS_SETUP_AND_SYMLINKS.md` | Created | Full macOS setup guide: runtime targets table, source-versus-runtime explanation, preflight checks, parent-dir creation, idempotent symlink examples, rollback steps, global AGENTS policy, and scope disclaimer | Primary deliverable for AC1–AC5 |

### Test Files

No test files — this is a documentation-only feature. Validation is manual path/policy review per the plan's stated QA approach.

## Test Results

- **Baseline**: N/A — no automated tests; documentation slice (captured 2026-05-07)
- **Final**: N/A
- **New tests added**: 0
- **Regressions**: None

## Deviations from Plan

None. The guide uses `ln -sfn` with individual TOML filenames for the `~/.codex/agents/` examples (e.g., `example-agent.toml`) rather than symlinking the whole directory. This matches AC2's intent — symlinking individual agent files into the agents directory — and aligns with the platform reference model where agents are discrete TOML files.

## Gaps

None. All five ACs are satisfied. The upstream `codex/CODEX_PLATFORM_REFERENCE.md` (wave 1) was present and used to verify install paths. Source artifact paths in the guide are explicitly labeled as future-facing placeholders per the non-goals constraint ("Do not create actual global Codex AGENTS files or custom-agent TOML artifacts in this feature").

## Reviewer Focus Areas

- **Global AGENTS Policy section** — Confirm wording makes clear that neither `github-agents-source-of-truth/AGENTS.md` nor `the-movies/AGENTS.md` should be the symlink target.
- **Idempotent Symlink Examples** — Verify that every `ln -sfn` source path starts with `$REPO_ROOT/codex/...` and no path accidentally points into `.github/` or a checked-in `AGENTS.md`.
- **Preflight `test -e` checks** — Confirm each expected future source path is a reasonable placeholder rather than an assumed-to-exist file, consistent with the documentation-only constraint.
- **Runtime Targets table** — Cross-check each row against `codex/CODEX_PLATFORM_REFERENCE.md` Config And Runtime Locations table for path accuracy.
