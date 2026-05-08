# 01 Codex Source Layout Tasks

## Stage 0: Test Prerequisites

- [ ] Confirm there is no repo-level automated test runner configured for this docs-only repository and record the baseline as "No tests found - baseline: N/A".
- [ ] Use manual cross-document review as the verification method for this feature's acceptance criteria.

## Stage 1: Define the Repository-Owned Codex Layout

- [ ] Create `codex/README.md` as the layout contract for the repository-owned Codex source area.
- [ ] Document the current Phase 02 Codex documents that belong under `codex/` today.
- [ ] Reserve future repository-owned artifact categories for global guidance, custom agents, and skill copies without creating runnable Codex artifacts.
- [ ] Explain what belongs under `codex/` versus runtime `.codex/` and user-home `$HOME/.agents/skills/` locations.
- [ ] Verify the layout wording satisfies AC1, AC2, and AC5 without drifting into setup-guide or porting-guide scope.

## Stage 2: Update Shared Architecture and Roadmap Docs

- [ ] Update `docs/ARCHITECTURE.md` so it no longer implies a three-platform-only model and instead describes Codex as a fourth, differently shaped platform surface.
- [ ] Update `docs/CODEBASE_CONTEXT.md` so the repository inventory and maintenance guidance stay consistent with the new Codex layout terminology.
- [ ] Update `docs/phases/PHASES_OVERVIEW.md` so Phase 02 explicitly reflects the Codex source-layout concern and the four-platform model.
- [ ] Confirm the shared docs distinguish repository-owned `codex/` content from runtime `.codex/` and `$HOME/.agents/skills/` locations.
- [ ] Read `codex/README.md`, `docs/ARCHITECTURE.md`, `docs/CODEBASE_CONTEXT.md`, and `docs/phases/PHASES_OVERVIEW.md` together to verify AC3 and AC4 through terminology and roadmap consistency.