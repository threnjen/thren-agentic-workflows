# Implementation Record: 01 Codex Platform Reference

## Summary

Created `codex/CODEX_PLATFORM_REFERENCE.md` as the repository-owned Codex platform reference for Phase 02. The document captures verified AGENTS discovery precedence, custom-agent TOML requirements, skill discovery roots, the literal macOS install locations required by the plan, and an explicit source-versus-runtime split between `codex/`, `.codex/`, `~/.codex/`, and `$HOME/.agents/skills/`. It also includes provenance and a revalidation note so downstream features can treat it as a maintained prerequisite rather than a permanent platform contract.

## Sibling Features

- `01-codex-source-layout`: already establishes `codex/` as the repository-owned authoring area; this implementation stays aligned with that split and does not redefine layout beyond the new reference doc.
- `02-codex-macos-setup-guide`: depends on the verified path set and runtime-location roles documented here.
- `02-codex-porting-guide`: depends on the AGENTS precedence rules, custom-agent TOML model, skill discovery roots, and source-versus-runtime separation documented here.
- `03-codex-pilot-slice-definition`: will consume this reference indirectly through the setup and porting guidance; no direct implementation changes were made for it.

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | `codex/CODEX_PLATFORM_REFERENCE.md` documents Codex-native discovery and authoring behavior for global AGENTS guidance, custom agents, skills, and relevant `.codex/config.toml` settings. | Done | `codex/CODEX_PLATFORM_REFERENCE.md` | Added dedicated sections for discovery, custom agents, skills, and config/runtime locations. |
| AC2 | The reference states the verified macOS-relevant install and discovery locations: `~/.codex/config.toml`, `~/.codex/AGENTS.md`, `~/.codex/AGENTS.override.md`, `~/.codex/agents/`, and `$HOME/.agents/skills/`. | Done | `codex/CODEX_PLATFORM_REFERENCE.md` | All five paths are listed literally in the config/runtime table and supporting narrative. |
| AC3 | The reference distinguishes clearly between repository-owned source material under `codex/` and runtime-installed surfaces under `.codex/` and the user home directory. | Done | `codex/CODEX_PLATFORM_REFERENCE.md` | Added explicit source-versus-runtime tables and repository policy notes. |
| AC4 | The reference captures Codex precedence rules accurately enough that a future implementation pass does not need to rediscover AGENTS precedence, custom-agent file format, or skill discovery roots. | Done | `codex/CODEX_PLATFORM_REFERENCE.md` | Included an implementation-ready precedence summary covering AGENTS lookup, TOML agent roots, and skill roots. |
| AC5 | The document includes source-backed provenance notes or an explicit “last verified” section so future maintainers know to recheck upstream Codex behavior before implementation. | Done | `codex/CODEX_PLATFORM_REFERENCE.md` | Added a dated last-verified section, source categories, and explicit revalidation guidance. |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `codex/CODEX_PLATFORM_REFERENCE.md` | Created | Added the Codex platform reference with discovery rules, runtime locations, source-vs-runtime guidance, and provenance. | Satisfies AC1-AC5 and provides the factual prerequisite for later Codex setup and porting features. |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| None | None | No automated test files exist for this docs-only feature. | Manual verification checklist for AC1-AC5 |

## Test Results
- **Baseline**: N/A, 0 automated tests configured or discovered for this docs-only feature before implementation
- **Final**: N/A, manual verification complete against the Phase 02 discovery context and feature checklist
- **New tests added**: 0
- **Regressions**: None

## Deviations from Plan

- No executable Red-Green-Refactor cycle was available because the feature context records no repo-level automated test runner or tests for this documentation-only scope; manual acceptance verification was used instead.

## Gaps

- None

## Reviewer Focus Areas

- Confirm the AGENTS precedence wording in `codex/CODEX_PLATFORM_REFERENCE.md` matches the Phase 02 discovery record exactly and does not overstate repo-local behavior.
- Confirm the source-versus-runtime split stays consistent with `codex/README.md` and does not accidentally bless `.codex/` as an authoring area.
- Confirm the document includes all five required macOS paths literally and assigns each to the correct scope and role.
- Confirm the provenance section is explicit enough that downstream implementers will revalidate upstream Codex behavior before treating the reference as a stable contract.