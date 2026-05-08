# 02 Codex Porting Guide Context

## Key Files

### Files To Change

| File | Role | Change Type |
|------|------|-------------|
| `codex/CODEX_PORTING_GUIDE.md` | Primary deliverable that maps `.github/instructions/`, `.github/agents/`, and `.github/skills/` into Codex-native targets and transformation rules. | Create |

### Read-Only Reference Files

| File | Role | Change Type |
|------|------|-------------|
| `.github/instructions/` | Master source for instruction content that must map into global Codex AGENTS guidance and agent `developer_instructions`. | Read-only reference |
| `.github/agents/` | Master source for GitHub Copilot agent manifests that must map into Codex custom-agent TOML. | Read-only reference |
| `.github/skills/` | Master source for skills that must map into Codex skill directories and `SKILL.md` content. | Read-only reference |
| `.github/agents/PORTING_GUIDE.md` | Existing platform-porting precedent that reinforces transformation rather than file-for-file copying. | Read-only reference |
| `docs/phases/PHASE_02/PHASE_02_SUMMARY.md` | Phase-level scope, sequencing, and the hard requirement that AGENTS-derived content target the global Codex AGENTS layer. | Read-only reference |
| `README.md` | Current repository description of platform variants; the new guide should stay consistent with or explicitly inform later doc updates. | Read-only reference |
| `.codex/config.toml` | Runtime Codex config surface used as a contrast so the guide does not blur repo-owned authoring docs with runtime configuration. | Read-only reference |
| `codex/CODEX_PLATFORM_REFERENCE.md` | Planned sibling output that should hold Codex-native platform facts so this guide can reference them instead of duplicating them. | Planned sibling dependency |
| `codex/README.md` | Planned sibling output defining the repository-owned Codex landing zone and destination terminology referenced by AC6. | Planned sibling dependency |

At expansion time, the `codex/` directory is empty. Treat `codex/CODEX_PLATFORM_REFERENCE.md` and `codex/README.md` as sibling dependencies that should exist before or alongside implementation of this feature.

## Architectural Decisions

- Organize `codex/CODEX_PORTING_GUIDE.md` by source surface: instructions, agents, and skills. This mirrors the master `.github/` layout and makes destination rules easy to audit per surface.
- Use `.github/` vocabulary as the source-of-truth language. The guide should explain how the existing master assets translate into Codex, not invent a separate naming model.
- Treat `.github/instructions/` as a transformation problem, not a copy problem. Codex has no direct instruction-file system equivalent, so the guide must map content into the global AGENTS layer and agent `developer_instructions`, including split-destination cases.
- Keep Codex platform facts in `codex/CODEX_PLATFORM_REFERENCE.md` and use this guide for mapping rules. This avoids duplicating platform basics across multiple docs.
- Use explicit classification tables for portable, transformed, and non-portable behavior. Narrative-only guidance is too easy to misread during later pilot work.
- Keep the output contract narrow: one implementation-ready mapping guide that future conversion work can follow without rediscovering destination rules.

## Constraints

- Do not create actual Codex custom-agent TOML files or skill directories in this feature.
- Do not rewrite or mutate any `.github/` source assets.
- Make the global AGENTS rule explicit: AGENTS-derived content maps to the user's global Codex AGENTS layer, not to either repository's checked-in `AGENTS.md`.
- Preserve the separation between repo-owned `codex/` authoring docs and runtime surfaces such as `.codex/` and `$HOME/.agents/skills`.
- Classify GitHub-only or otherwise non-portable behavior explicitly instead of implying parity.
- Keep examples repository-local and generic; do not include secrets, private machine paths, or unverified runtime assumptions.
- Reference `codex/README.md` for landing-zone terminology once available rather than inventing ad hoc destination paths inside this guide.
- Manual mapping review is the primary verification surface for this feature until an automated docs-check baseline exists.

## Relationships To Sibling Plans

- Depends on `01-codex-platform-reference` for authoritative Codex-native syntax, discovery, and field behavior.
- Depends on `01-codex-source-layout` for the repository-owned `codex/` landing-zone definition and path terminology referenced by AC6.
- Can proceed in parallel with `02-codex-macos-setup-guide` because the deliverables have disjoint file scopes.
- Unblocks `03-codex-pilot-slice-definition`, which needs stable mapping rules before selecting a pilot conversion slice.

## Suggested Implementation Order

1. Land `01-codex-platform-reference` so Codex-native behavior is documented once.
2. Land `01-codex-source-layout` so `codex/README.md` defines the repo-owned destination area.
3. Implement `02-codex-porting-guide` using those two dependencies as references.
4. Land `03-codex-pilot-slice-definition` after the mapping rules are stable.

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Markdown-first documentation/config repository for GitHub Copilot agent definitions and skills; primary source surfaces are `.agent.md`, `.instructions.md`, `SKILL.md`, and TOML config. No package-managed application runtime was detected at repo root. |
| Test Runner | No tests found in repository config scan (`package.json`, `pyproject.toml`, `pytest.ini`, `jest.config.*`, `vitest.config.*` not present). |
| Test Baseline | No tests found — baseline: N/A (captured 2026-05-07). |
| Lint | Not configured |
| Format | Not configured |

## Relevant Learnings

- `.github/learnings/review-learnings.md`: When adding a new user-facing agent, update every inventory surface that carries agent counts or summarized agent lists. This matters here because Codex porting and platform-support docs should not leave README or architecture summaries in a stale three-platform state.
- `.github/learnings/cross-phase-decisions.md`: None applicable to this feature slice.
- `.github/learnings/project-learnings.md`: None applicable to this feature slice.