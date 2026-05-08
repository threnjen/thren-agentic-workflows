# 01 Codex Platform Reference Tasks

## Stage 0: Test Prerequisites

- [ ] Confirm and record that this docs-only feature has no discovered repo-level automated test runner, so manual verification will be the baseline unless the pipeline requires a separate test bootstrap step.
- [ ] Define the manual verification checklist for AC1-AC5 using `docs/phases/PHASE_02/PHASE_02_DISCOVERY_CONTEXT.md`, `docs/phases/PHASE_02/PHASE_02_SUMMARY.md`, and `.codex/config.toml` before implementation starts.

## Stage 1: Author the Codex Platform Reference

- [ ] Create `codex/CODEX_PLATFORM_REFERENCE.md` as a single self-contained reference document under the repository-owned `codex/` directory.
- [ ] Add a discovery section that explains Codex AGENTS guidance lookup and precedence clearly enough for a future implementation pass to reuse without rediscovery.
- [ ] Add a custom agents section that documents the Codex TOML model, required fields, and the distinction between repo-scoped and user-scoped agent locations.
- [ ] Add a skills section that documents directory-based skill structure and the correct discovery roots, including `$HOME/.agents/skills`.
- [ ] Add a config and runtime locations section that includes the five verified macOS paths literally and explains the role of each.
- [ ] Make the distinction between repository-owned source material under `codex/` and runtime-installed surfaces under `.codex/` and the user home directory explicit throughout the document.
- [ ] Read the completed draft back against AC1, AC2, and AC3 to confirm the document is self-contained and terminology is consistent.

## Stage 2: Add Provenance and Revalidation Guidance

- [ ] Add a provenance or last-verified section that identifies the discovery context and upstream source categories used to author the reference.
- [ ] Add an explicit recheck-before-implementation note so future maintainers know Codex behavior must be revalidated before they treat the reference as a stable contract.
- [ ] Validate the final document against AGENTS, custom-agent, and skill lookup scenarios to confirm AC4 is satisfied.
- [ ] Confirm the finished reference satisfies AC5 and is safe to use as a prerequisite for the setup and porting guide features.