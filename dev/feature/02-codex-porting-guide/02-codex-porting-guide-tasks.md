# 02 Codex Porting Guide Tasks

## Stage 0: Test Prerequisites

- [ ] Verify whether any executable tests or docs checks exist for the repository and record the baseline verification approach for this feature slice.
- [ ] If automated coverage is missing or below the required threshold, invoke `@z-test-writer` to define the prerequisite validation surface for documentation changes.
- [ ] Align implementation and review on the manual mapping-audit checks that will verify the guide against the live `.github/` tree until automated coverage exists.

## Stage 1: Map `.github/` Source Surfaces to Codex Targets

- [ ] Create `codex/CODEX_PORTING_GUIDE.md` with top-level sections for instructions, agents, and skills.
- [ ] Document how `.github/instructions/` content maps into the global Codex AGENTS layer and agent `developer_instructions`, including split-destination cases.
- [ ] Document how `.github/agents/` definitions map into Codex custom-agent TOML files, including the required Codex fields and the major non-portable differences from Markdown agent manifests.
- [ ] Document how `.github/skills/` entries map into Codex skill directories, `SKILL.md`, and optional supporting assets rather than a standalone manifest model.
- [ ] Add a concise example or classification snippet for each source surface so a maintainer can choose the correct Codex destination without extra discovery.

## Stage 2: Classify Portability and Landing Zones

- [ ] Add a portability classification section that separates portable content, content that must be transformed, and GitHub-only or otherwise non-portable behavior.
- [ ] Make the global AGENTS policy explicit and durable: AGENTS-derived content goes to the global Codex AGENTS layer, not either repository's checked-in `AGENTS.md`.
- [ ] Reference `codex/README.md` as the repository-owned landing zone for future ported artifacts and keep runtime `.codex` concerns out of the guide.
- [ ] Cross-check the completed guide against `.github/instructions/`, `.github/agents/`, `.github/skills/`, and `docs/phases/PHASE_02/PHASE_02_SUMMARY.md` so every source surface has a documented destination rule.
- [ ] Perform a final acceptance-criteria audit covering AC4, AC5, and AC6 before handing the feature to implementation review.