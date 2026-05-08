# 02 Codex macOS Setup Guide Context

## Key Files

### Files To Change

| File | Role | Change Type |
|------|------|-------------|
| `codex/MACOS_SETUP_AND_SYMLINKS.md` | Primary deliverable for this feature: the macOS setup guide covering install targets, symlink examples, runtime-versus-source explanations, and safety guidance. | Create |

### Read-Only References

| File | Role | Change Type |
|------|------|-------------|
| `dev/feature/02-codex-macos-setup-guide/02-codex-macos-setup-guide-plan.md` | Controlling plan for acceptance criteria, non-goals, and stage boundaries. | Read-only reference |
| `docs/phases/PHASE_02/PHASE_02_SUMMARY.md` | Phase-level scope, explicit macOS install targets, and the global AGENTS policy requirement. | Read-only reference |
| `docs/phases/PHASE_02/PHASE_02_DISCOVERY_CONTEXT.md` | Verified Codex discovery rules and macOS runtime locations used to ground the guide. | Read-only reference |
| `dev/feature/01-codex-platform-reference/01-codex-platform-reference-plan.md` | Upstream dependency describing the platform facts this guide is expected to apply. | Read-only reference |
| `dev/feature/01-codex-source-layout/01-codex-source-layout-plan.md` | Upstream dependency defining the intended repository-owned Codex source area this guide should point at. | Read-only reference |
| `dev/feature/02-codex-porting-guide/02-codex-porting-guide-plan.md` | Parallel sibling that must use the same source-versus-runtime terminology and AGENTS policy. | Read-only reference |
| `dev/feature/03-codex-pilot-slice-definition/03-codex-pilot-slice-definition-plan.md` | Downstream sibling that will consume the installation and validation model described here. | Read-only reference |

Referenced but currently missing in the workspace: `codex/CODEX_PLATFORM_REFERENCE.md` and `codex/README.md`. Treat them as planned upstream outputs, not files to fabricate as part of this feature.

## Architectural Decisions

- Keep authored setup guidance in the repository-owned `codex/` area while documenting runtime targets under `~/.codex/` and `$HOME/.agents/skills/`.
- Use one guide organized around prerequisites, install targets, symlink examples, and rollback or inspection steps rather than splitting setup guidance across multiple docs.
- Point all symlink examples from runtime locations back to repository-owned Codex artifacts, never to either repository's checked-in `AGENTS.md`.
- Use clearly labeled placeholder or future-facing repository source paths when needed because the sibling source-layout and platform-reference outputs are not present yet.

## Constraints

- Do not perform any real installation into a user home directory.
- Do not create actual global Codex AGENTS files, override files, or custom-agent TOML artifacts in this feature.
- Do not expand the `.github/` to Codex mapping beyond what is required to explain setup targets.
- Make the global AGENTS rule explicit: AGENTS-derived source content belongs in the global Codex AGENTS layer, not in either repository's checked-in `AGENTS.md`.
- Preserve the distinction between repository-owned authoring surfaces (`codex/`) and runtime install surfaces (`~/.codex/` and `$HOME/.agents/skills/`).
- Because upstream Codex source docs are not present yet, avoid implying that referenced repository-owned artifacts already exist; label example sources accordingly.

## Relationships to Sibling Plans

- `01-codex-platform-reference` is an upstream prerequisite for Codex install and discovery facts.
- `01-codex-source-layout` is an upstream prerequisite for the repository-owned source paths used in symlink examples.
- `02-codex-porting-guide` can proceed in parallel because it touches different files, but both features need consistent terminology around global AGENTS, custom agents, and skills.
- `03-codex-pilot-slice-definition` depends on this guide for installation-path and validation expectations.

## Suggested Implementation Order

1. Reconfirm the expected repository-owned source paths from the Feature 01 plans and the Phase 02 discovery context.
2. Create the guide scaffold with prerequisites, install targets, and the source-versus-runtime explanation.
3. Add reversible symlink examples for AGENTS, AGENTS override, custom agents, and skills.
4. Add safety and rollback guidance, then review wording against the phase summary and discovery context.

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Markdown documentation plus VS Code Copilot agent-definition content; no root application framework or package manifest detected. |
| Test Runner | No tests found at the repository root for this documentation slice. |
| Test Baseline | No tests found - baseline: N/A (captured 2026-05-07). |
| Lint | Not configured at the repository root. |
| Format | Not configured at the repository root. |

## Relevant Learnings

None applicable. The current entries in `.github/learnings/` cover eval-ledger behavior and review-workflow pitfalls rather than Markdown-based Codex setup documentation.