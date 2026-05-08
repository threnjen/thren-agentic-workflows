# 01 Codex Source Layout Context

## Key Files

### Files To Change

| File | Role | Change Type |
|------|------|-------------|
| `codex/README.md` | Defines the repository-owned Codex source area, current Phase 02 docs, and reserved future artifact categories | Create |
| `docs/ARCHITECTURE.md` | Updates the shared platform model so Codex is described as a fourth platform surface with a distinct instruction model | Modify |
| `docs/CODEBASE_CONTEXT.md` | Aligns codebase inventory and platform-language summaries with the Codex source-layout contract | Modify |
| `docs/phases/PHASES_OVERVIEW.md` | Reflects Codex source-layout work as an explicit Phase 02 concern and keeps roadmap terminology aligned | Modify |

### Read-Only Reference Files

| File | Role | Change Type |
|------|------|-------------|
| `docs/phases/PHASE_02/PHASE_02_SUMMARY.md` | Phase-level source for scope, non-goals, and the requirement to distinguish `codex/` from runtime install paths | Read-only reference |
| `docs/phases/PHASE_02/PHASE_02_DISCOVERY_CONTEXT.md` | Discovery-backed Codex facts that reinforce the source-vs-runtime split and current empty `codex/` state | Read-only reference |
| `.codex/config.toml` | Existing runtime Codex configuration surface that must remain untouched and must not be confused with the repo-owned source area | Read-only reference |
| `.github/agents/PORTING_GUIDE.md` | Existing cross-platform mapping guidance that informs how Codex should be framed alongside other platform surfaces | Read-only reference |

## Architectural Decisions

- Use `codex/README.md` as the single layout contract for the repository-owned Codex area rather than scattering layout rules across multiple docs.
- Keep the initial Codex source area narrow: document current Phase 02 docs and reserve future artifact categories conceptually without creating runnable Codex agents, skills, or global guidance files.
- Treat `.github/` as the master source of truth and describe Codex as a fourth platform surface with a different shape from `claude/` and `opencode/`, not as another direct mirror.
- Preserve the distinction between repository-owned authoring space (`codex/`) and runtime installation/configuration space (`.codex/`, `~/.codex/`, and `$HOME/.agents/skills/`).
- Limit shared-doc updates to the existing platform-model surfaces named in the plan: architecture, codebase context, and phases overview.

## Constraints

- Do not create full Codex custom-agent TOML files, skill directories, or global AGENTS deliverables in this feature.
- Do not author the detailed setup guide or the porting guide in this feature.
- Do not modify the live runtime `.codex/config.toml` or any user-home files.
- Reserve future artifact areas conceptually in `codex/README.md`; create only what this feature needs now.
- Keep the wording consistent across `codex/README.md`, `docs/ARCHITECTURE.md`, `docs/CODEBASE_CONTEXT.md`, and `docs/phases/PHASES_OVERVIEW.md` so the repo no longer implies a three-platform-only model.

## Relationships To Sibling Plans

- `01-codex-platform-reference` runs in the same wave and can proceed in parallel because it writes a separate file while supplying factual Codex behavior that complements this layout contract.
- `02-codex-macos-setup-guide` depends on this feature so installation examples can point at intentional repository-owned Codex locations.
- `02-codex-porting-guide` depends on this feature so mapping guidance can reference a stable `codex/` landing area and terminology.
- `03-codex-pilot-slice-definition` depends on this feature because the pilot plan must name repository-owned destinations for future Codex copies.

## Suggested Implementation Order

1. Create `codex/README.md` and define the repository-owned Codex area, including the current document set and reserved future artifact categories.
2. Update `docs/ARCHITECTURE.md` so the shared platform model describes Codex as a fourth platform surface with a distinct instruction-loading model.
3. Update `docs/CODEBASE_CONTEXT.md` to keep the repository inventory and maintenance guidance aligned with the new Codex terminology.
4. Update `docs/phases/PHASES_OVERVIEW.md` so Phase 02 language matches the new layout contract.
5. Perform a final cross-document readback across all four touched files to confirm consistent separation of `codex/`, `.codex/`, and `$HOME/.agents/skills/`.

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Markdown documentation repository with YAML-frontmatter Copilot agent definitions; no runnable application or package-managed runtime detected at repo scope |
| Test Runner | Not configured |
| Test Baseline | No tests found - baseline: N/A (captured 2026-05-07) |
| Lint | Not configured |
| Format | Not configured |

## Relevant Learnings

- From `.github/learnings/review-learnings.md`: when adding a new user-facing platform or changing summarized inventory language, update every inventory surface that carries counts, summary bullets, or platform-model descriptions rather than only the primary doc. For this feature, that means keeping `codex/README.md`, `docs/ARCHITECTURE.md`, `docs/CODEBASE_CONTEXT.md`, and `docs/phases/PHASES_OVERVIEW.md` aligned so the repository does not present conflicting platform counts or terminology.
