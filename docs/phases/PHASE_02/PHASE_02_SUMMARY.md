# Phase 02: Codex Platform Bootstrap

**Status**: Planned
**Depends on**: Phase 01
**Estimated complexity**: Medium
**Cross-references**: [`docs/phases/PHASES_OVERVIEW.md`](../PHASES_OVERVIEW.md), [`docs/ARCHITECTURE.md`](../../ARCHITECTURE.md), [`.github/agents/PORTING_GUIDE.md`](../../../.github/agents/PORTING_GUIDE.md), [`.codex/config.toml`](../../../.codex/config.toml)

## Objective

Establish the repository's Codex support model before any full Codex port is attempted. This phase should document Codex-native syntax, discovery rules, and macOS install locations, then define how the existing GitHub Copilot source of truth maps into Codex global instructions, custom agents, and skills.

## Scope

### In Scope

- Research-backed Codex platform documentation authored under `codex/`
- A Codex syntax and usage reference covering:
  - global AGENTS files
  - custom agent TOML files
  - skill directory structure
  - relevant `.codex/config.toml` settings
- A macOS setup and symlink guide for Codex that documents:
  - `~/.codex/config.toml`
  - `~/.codex/AGENTS.md`
  - `~/.codex/AGENTS.override.md`
  - `~/.codex/agents/`
  - `$HOME/.agents/skills/`
- A Codex porting guide that explains how:
  - `.github/instructions/` map to the global Codex AGENTS layer and agent `developer_instructions`
  - `.github/agents/` map to Codex custom-agent TOML files
  - `.github/skills/` map to Codex skill directories
- Definition of the repository-owned Codex source area under the existing `codex/` directory
- A pilot porting strategy that identifies one instruction slice, one custom agent, and one skill as the first validation targets for later implementation
- Roadmap and architecture notes needed to account for Codex as a supported platform surface

### Out of Scope

- Full porting of all agents into runnable Codex custom-agent files
- Full porting of all skills into installed `$HOME/.agents/skills` content
- Runtime installation into a real user home directory as part of this phase
- Replacing either repo's checked-in `AGENTS.md` with Codex instruction content
- Automation scripts that generate Codex copies from `.github/` source material
- Validation of the entire Codex surface beyond a single pilot slice

## Key Deliverables

| # | Deliverable | Description | Likely Features |
|---|-------------|-------------|-----------------|
| 1 | Codex platform reference | Codex-native syntax, discovery rules, and configuration model documented under the repo-owned Codex area | Feature 1 |
| 2 | macOS symlink/setup guide | A practical setup document for global Codex files, custom agents, and skills on macOS | Feature 2 |
| 3 | Codex porting guide | Explicit mapping from `.github/` source of truth into Codex global AGENTS, custom agents, and skills | Feature 3 |
| 4 | Source-area definition | A documented structure for how `codex/` will hold Codex-facing docs and future ported copies | Feature 4 |
| 5 | Pilot conversion plan | A first-slice plan naming the initial instruction, agent, and skill to validate before full parity work | Feature 5 |

## Technical Context

The current master platform model lives in `.github/agents/`, `.github/skills/`, and `.github/instructions/`. Existing derived platform copies live in `claude/` and `opencode/`, with supporting guidance already captured in `.github/agents/PORTING_GUIDE.md`.

Codex differs from those platforms in several important ways:

- Instructions are not a direct equivalent of `.github/instructions/`; AGENTS-style content must target the global Codex AGENTS layer, not repo-local AGENTS files for these repositories
- Custom agents are TOML files rather than markdown manifests
- Skills are directory-based and discovered from `.agents/skills` and `$HOME/.agents/skills`, with symlink support
- Project-local Codex config already exists in `.codex/config.toml`, but that hidden `.codex` surface is runtime configuration, not the intended source-of-truth destination for this planning work
- The current roadmap in `docs/phases/PHASES_OVERVIEW.md` and architecture notes in `docs/ARCHITECTURE.md` currently describe three platform variants; Codex support introduces a fourth platform surface and a different instruction-loading model

## Dependencies & Risks

- **Dependency**: Phase 01 should land first if its agent-definition changes are expected to keep touching the shared `.github/agents` source, otherwise the Codex mapping may be based on unstable upstream content
- **Dependency**: Official Codex behavior for AGENTS discovery, custom agents, skills, and config must be rechecked immediately before implementation so the docs do not fossilize stale syntax
- **Risk**: Treating Codex like Claude or OpenCode would create the wrong file layout and incorrect instructions handling. Mitigation: make the global AGENTS distinction explicit in the porting guide and setup guide.
- **Risk**: Confusing the repo-owned `codex/` directory with runtime `.codex` configuration will blur authoring versus installation concerns. Mitigation: document the separation directly and use it consistently across all Codex docs.
- **Risk**: The current architecture docs say the platform copies stay in sync across three directories. Adding Codex without updating that assumption creates future drift. Mitigation: include architecture and roadmap updates as explicit deliverables in this phase.
- **Risk**: AGENTS-derived content may not divide neatly into one global instructions file. Mitigation: classify content into global guidance, agent-specific `developer_instructions`, and non-portable GitHub-only behavior before any full copy effort starts.

## Success Criteria

- [ ] The repo has a Codex planning/documentation area defined under `codex/`
- [ ] Codex syntax and discovery behavior are documented clearly enough that a future implementation pass does not need to rediscover platform basics
- [ ] The macOS setup guide explicitly documents the correct global install locations for Codex AGENTS, custom agents, and skills
- [ ] The porting guide explicitly states that AGENTS-derived content maps to the global Codex AGENTS layer, not to either repository's checked-in AGENTS files
- [ ] The porting guide separates instructions, custom agents, and skills rather than treating them as a single copied surface
- [ ] The plan identifies one pilot instruction slice, one pilot custom agent, and one pilot skill for later validation
- [ ] Roadmap or architecture documentation required by the new platform model is identified as part of the phase scope
- [ ] No full-catalog Codex copy is attempted before the pilot slice and platform docs exist

## QA Considerations

- This phase is documentation and planning heavy, so QA is primarily validation of correctness and internal consistency rather than executable product behavior
- Command examples in the macOS setup guide should be checked for path correctness and idempotent symlink behavior
- The Codex porting guide should be read against the current `.github/` layout to confirm that each source surface has a documented Codex target
- The pilot slice should be chosen so later validation can exercise all three Codex-native surfaces: global AGENTS, custom agents, and skills
- Architecture and roadmap notes should be reviewed to ensure they no longer imply a three-platform-only model

## Notes for Feature - Decomposer

Suggested feature boundaries:

- **Feature 1: Codex platform reference**
  - Capture Codex-native syntax, discovery, and installation model
  - Keep this feature read-only with respect to runtime config outside the repo
- **Feature 2: macOS setup and symlink guide**
  - Focus on user-home install targets and symlink patterns
  - Keep shell examples minimal, explicit, and reversible
- **Feature 3: `.github/` to Codex mapping guide**
  - Separate instruction mapping, custom-agent mapping, and skill mapping
  - Make the global AGENTS rule a hard requirement, not an aside
- **Feature 4: repository-owned Codex source layout**
  - Define what belongs under `codex/` versus what belongs in runtime `.codex` or `$HOME/.agents`
- **Feature 5: pilot slice definition**
  - Choose one narrow example per Codex-native surface
  - Optimize for easy validation before any full parity effort

Sequencing guidance:

- The platform reference should land before the setup guide and porting guide
- The porting guide should land before any pilot conversion work
- The pilot slice definition should come last, because it depends on the documented mapping rules
- If this phase expands to include actual runnable Codex copies, that is likely a follow-on phase rather than an extension of this one