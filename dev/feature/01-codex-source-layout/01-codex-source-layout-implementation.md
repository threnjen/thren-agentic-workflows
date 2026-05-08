# Implementation Record: 01 Codex Source Layout

## Summary

Created the repository-owned Codex layout contract in `codex/README.md` and aligned the shared architecture, codebase-context, and roadmap docs to describe Codex as a fourth platform surface with a different installation model. The updated docs now consistently separate repo-owned `codex/` authoring space from runtime `.codex/`, `~/.codex/`, and `$HOME/.agents/skills/` locations.

## Sibling Features

- `01-codex-platform-reference` runs in parallel and supplies Codex behavior facts without sharing edited files.
- `02-codex-macos-setup-guide` will rely on the new `codex/` versus runtime-path terminology when documenting install targets.
- `02-codex-porting-guide` will rely on the reserved Codex artifact categories and the new four-surface wording.
- `03-codex-pilot-slice-definition` will consume the `codex/` layout contract when naming future Codex landing areas.

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | `codex/README.md` defines the repository-owned Codex source area and distinguishes documentation files from future source artifacts. | Done | `codex/README.md` | Added a layout contract that defines the current docs-only state and separates it from future source categories. |
| AC2 | The layout definition explains what belongs under `codex/` versus runtime `.codex/` and `$HOME/.agents/skills/` locations. | Done | `codex/README.md`, `docs/ARCHITECTURE.md`, `docs/CODEBASE_CONTEXT.md` | Shared docs now use the same source-versus-runtime wording. |
| AC3 | `docs/ARCHITECTURE.md` and `docs/CODEBASE_CONTEXT.md` are updated so they no longer imply a three-platform-only model and instead describe Codex as a fourth, differently-shaped platform surface. | Done | `docs/ARCHITECTURE.md`, `docs/CODEBASE_CONTEXT.md` | Added Codex as a fourth platform surface and clarified that it is not a direct checked-in mirror. |
| AC4 | `docs/phases/PHASES_OVERVIEW.md` reflects Codex as an explicit Phase 02 concern and stays consistent with the new layout terminology. | Done | `docs/phases/PHASES_OVERVIEW.md` | Phase 02 now explicitly names the repository-owned `codex/` source layout. |
| AC5 | The documented Codex source layout reserves room for future global guidance, custom agents, and skill copies without forcing this phase to implement them. | Done | `codex/README.md` | Reserved future categories conceptually without creating new directories or runtime artifacts. |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `codex/README.md` | Create | Added the repository-owned Codex layout contract, current docs-only state, reserved future categories, and source-versus-runtime rules. | Satisfies the core layout definition requirements for AC1, AC2, and AC5. |
| `docs/ARCHITECTURE.md` | Modify | Reframed platform variants as four platform surfaces, added `codex/` to the platform-loading model, and clarified that Codex is mapped to runtime locations rather than mirrored directly. | Keeps the shared architecture model aligned with the new Codex layout contract for AC2 and AC3. |
| `docs/CODEBASE_CONTEXT.md` | Modify | Added `codex/` and `.codex/` to the repo inventory, documented the new Codex relationship rules, and added a maintenance rule to update `codex/README.md` first. | Keeps the inventory and maintenance guidance aligned with the layout contract for AC2 and AC3. |
| `docs/phases/PHASES_OVERVIEW.md` | Modify | Updated the Phase 02 description and architecture notes to call out the repository-owned `codex/` source layout explicitly. | Keeps the roadmap aligned with the new terminology for AC4. |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| None | N/A | No automated tests were added for this docs-only feature. | Manual cross-document validation and file diagnostics only. |

## Test Results
- **Baseline**: No automated tests configured; baseline recorded in feature context as `N/A` before implementation
- **Final**: No automated tests configured; manual cross-document review plus `get_errors` validation on all touched files
- **New tests added**: 0
- **Regressions**: None

## Deviations from Plan

- Red-Green-Refactor TDD was not executable for this docs-only repository because the feature context recorded no configured test runner and no automated tests; validation used manual cross-document review and file diagnostics instead.

## Gaps

- No executable regression test coverage exists for documentation-consistency changes at repo scope.

## Reviewer Focus Areas
- Verify that `codex/README.md` keeps the repository-owned `codex/` surface clearly separate from runtime `.codex/`, `~/.codex/`, and `$HOME/.agents/skills/` locations.
- Verify that `docs/ARCHITECTURE.md` accurately describes Codex as a fourth platform surface without implying a direct checked-in mirror.
- Verify that `docs/CODEBASE_CONTEXT.md` inventory and maintenance guidance match the new Codex terminology and do not overstate current Codex artifacts.
- Verify that `docs/phases/PHASES_OVERVIEW.md` Phase 02 wording stays aligned with the layout contract and Phase 02 summary scope.