# Review Record: 02 Codex macOS Setup Guide

## Summary

`codex/MACOS_SETUP_AND_SYMLINKS.md` satisfies all five acceptance criteria. All five runtime install locations are documented and correctly match `codex/CODEX_PLATFORM_REFERENCE.md`. Shell examples use `ln -sfn` throughout, are idempotent, and are paired with preflight, parent-directory, and rollback sections. The source-versus-runtime separation is clearly explained. The global AGENTS policy callout is prominently placed at document top and correctly names both repositories' `AGENTS.md` files as non-targets.

One Low issue was found and fixed: bare `test -e` checks in the preflight block gave no indication that failure is expected until future source artifacts exist. A comment and `|| echo` fallback were added for clarity.

## Verdict

Approved

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1: macOS install locations documented | ✅ Done | `codex/MACOS_SETUP_AND_SYMLINKS.md` — Runtime Targets table | All five paths present; cross-checked against `CODEX_PLATFORM_REFERENCE.md` Config And Runtime Locations table |
| AC2: Reversible symlink examples for four locations | ✅ Done | `codex/MACOS_SETUP_AND_SYMLINKS.md` — Idempotent Symlink Examples section | `ln -sfn` used for all four targets; all source paths start with `$REPO_ROOT/codex/...`; directory-level vs file-level agents deviation is intentional and documented in implementation record |
| AC3: Repo-owned `codex/` vs runtime `.codex/` explained | ✅ Done | `codex/MACOS_SETUP_AND_SYMLINKS.md` — Source Versus Runtime On macOS table | Four-row table covering all relevant surfaces; consistent with CODEX_PLATFORM_REFERENCE Source Versus Runtime Split table |
| AC4: Idempotent guardrails: `ln -sfn`, parent dirs, inspect/replace | ✅ Done | `codex/MACOS_SETUP_AND_SYMLINKS.md` — Preflight Checks, Parent Directories, Idempotent Symlink Examples, Replace Or Roll Back Safely sections | All guardrails present; `ln -sfn` caveat about non-symlink destinations correctly noted |
| AC5: Global AGENTS rule explicit | ✅ Done | `codex/MACOS_SETUP_AND_SYMLINKS.md` — Global AGENTS Policy section | Top-of-document callout; names both `github-agents-source-of-truth/AGENTS.md` and `the-movies/AGENTS.md` as non-targets |

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | Bare `test -e` checks in Preflight had no indicator that failure is expected for future-facing placeholder paths; copy-pasting in a shell session without `set -e` produces silent non-zero exits | Low | `codex/MACOS_SETUP_AND_SYMLINKS.md` — Preflight Checks block | AC4 | Fixed |
| 2 | AC2 lists `~/.codex/agents/` as a symlink target; implementation symlinks individual TOML files instead of the directory. Implementation record acknowledges this as intentional — agents are discrete files and file-level symlinks are more maintainable. Plan wording is ambiguous and the chosen approach is correct per the platform model. | Low | `codex/MACOS_SETUP_AND_SYMLINKS.md` — Idempotent Symlink Examples; `codex/CODEX_PLATFORM_REFERENCE.md` — Custom Agents section | AC2 | Open (intentional, documented in implementation record) |

**Status values**: Fixed (applied during this review) | Open (not addressed) | Wont-Fix (declined with rationale)

## Fixes Applied

| File | What Changed | Issue # |
|------|--------------|---------|
| `codex/MACOS_SETUP_AND_SYMLINKS.md` | Added a two-line comment before `test -e` block explaining failure is expected until source artifacts exist; added `\|\| echo "not yet: ..."` to each check so failure is visible rather than silent | 1 |

## Remaining Concerns

- Issue #2: `~/.codex/agents/` directory-level vs file-level symlinks — Low severity, documented design choice, defer to implementation once real source artifacts exist.

## Test Coverage Assessment

- Covered: AC1, AC2, AC3, AC4, AC5 via manual path/policy review (as specified by the plan's stated QA approach)
- Missing: No automated tests applicable for this documentation-only slice. Future validation can mechanically cross-check path strings in this file against `codex/CODEX_PLATFORM_REFERENCE.md` with a simple grep/diff.

## Risk Summary

- `codex/MACOS_SETUP_AND_SYMLINKS.md` — all runtime paths are future-facing placeholders; if Phase 02 work lands source artifacts in different subdirectory names (e.g., not `codex/global-agents/`), the symlink examples here and the preflight checks will both need updating.
- `ln -sfn` macOS behavior for directory destinations: if `$HOME/.agents/skills/example-skill` ever exists as a real directory (not a symlink), `ln -sfn` would create the link *inside* the directory rather than replacing it. The guide's existing warning covers this case, but it is a macOS-specific footgun worth keeping in mind during future real-install documentation passes.
