# 01 Codex Source Layout

## Execution Metadata

- **Wave:** 1
- **Parallel safe:** yes
- **Depends on:** none
- **Key files modified:** `codex/README.md`, `docs/ARCHITECTURE.md`, `docs/CODEBASE_CONTEXT.md`, `docs/phases/PHASES_OVERVIEW.md`
- **Sequential reason:** n/a

## A. Requirements & Traceability

### Acceptance Criteria

1. **AC1**: `codex/README.md` defines the repository-owned Codex source area and distinguishes documentation files from future source artifacts.
2. **AC2**: The layout definition explains what belongs under `codex/` versus runtime `.codex/` and `$HOME/.agents/skills/` locations.
3. **AC3**: `docs/ARCHITECTURE.md` and `docs/CODEBASE_CONTEXT.md` are updated so they no longer imply a three-platform-only model and instead describe Codex as a fourth, differently-shaped platform surface.
4. **AC4**: `docs/phases/PHASES_OVERVIEW.md` reflects Codex as an explicit Phase 02 concern and stays consistent with the new layout terminology.
5. **AC5**: The documented Codex source layout reserves room for future global guidance, custom agents, and skill copies without forcing this phase to implement them.

### Non-Goals

- Do not create full Codex custom-agent TOML files, skill directories, or global AGENTS deliverables in this feature.
- Do not author the detailed setup guide or porting guide in this feature.
- Do not change the live runtime `.codex/config.toml` or any user-home files.

### Traceability

| Acceptance Criteria | Code Areas/Modules | Planned Tests |
|---------------------|-------------------|---------------|
| AC1: `codex/README.md` defines the source area | `codex/README.md` | Manual layout readback and file-scope review |
| AC2: repo-owned vs runtime-owned surfaces separated | `codex/README.md`, `docs/CODEBASE_CONTEXT.md`, `docs/ARCHITECTURE.md` | Terminology consistency review |
| AC3: architecture and context docs reflect Codex as fourth platform | `docs/ARCHITECTURE.md`, `docs/CODEBASE_CONTEXT.md` | Cross-doc consistency review |
| AC4: roadmap reflects Phase 02 Codex work | `docs/phases/PHASES_OVERVIEW.md` | Summary-to-roadmap alignment check |
| AC5: future artifact areas reserved without premature implementation | `codex/README.md` | Manual structure audit against Phase 02 scope |

## B. Correctness & Edge Cases

### Key Workflows

- A maintainer opens `codex/README.md` and can tell where Phase 02 docs live now and where future Codex artifacts should live later.
- A contributor updating shared docs can describe Codex support without conflating repo-owned docs with runtime installation paths.

### Failure Modes and Edge Cases

- If the layout doc is too vague, later features may scatter Codex docs and source artifacts inconsistently.
- If architecture docs say “fourth platform surface” without explaining the different instruction model, the repo will still communicate the wrong mental model.
- If the layout reserves directories too aggressively, the phase may drift into premature structure creation.

### Error-Handling Strategy

- Prefer the narrowest layout that supports current docs and obvious future Codex artifacts.
- Reserve future folders conceptually in `codex/README.md`; create only what Phase 02 actually needs.

## C. Consistency & Architecture Fit

### Existing Patterns To Follow

- Treat `.github/` as master source of truth and `claude/` / `opencode/` as derived examples, as documented in `docs/ARCHITECTURE.md`.
- Match the repo’s existing documentation style: explicit folder-role explanations and architecture notes in shared docs.

### Interfaces and Contracts

- Input contract: current architecture docs, codebase context, Phase 02 summary, and the empty `codex/` directory.
- Output contract: a stable repository layout contract that downstream Phase 02 docs can cite without redefining where Codex material belongs.

### Sibling Feature Relationships

- `01-codex-platform-reference` runs in the same wave and provides factual Codex behavior without sharing files.
- `02-codex-macos-setup-guide` and `02-codex-porting-guide` depend on this feature so their document locations and terminology align with the new `codex/` layout contract.
- `03-codex-pilot-slice-definition` depends on this feature because the pilot plan must name the intended repository-owned landing areas for future Codex copies.

## D. Clean Design & Maintainability

### Simplest Design

- Use `codex/README.md` as the layout contract for the Codex area.
- Keep Phase 02 docs as root-level Codex documents for now, while reserving future conceptual areas for global guidance, agents, and skills.
- Update only the shared docs that currently communicate the platform model: architecture, codebase context, and phases overview.

### Complexity Risks

- Overdesigning the layout will create churn before the first pilot conversion exists.
- Under-documenting the layout will force the setup and porting guides to invent structure ad hoc.

### Keep It Clean Checklist

- [ ] `codex/README.md` defines current docs and future artifact areas separately.
- [ ] Shared docs describe Codex as a fourth platform surface with a distinct model.
- [ ] Runtime `.codex/` remains documented as installation/config, not source-of-truth.
- [ ] No premature Codex artifact directories are populated in this feature.

## E. Completeness: Observability, Security, Operability

### Logging / Metrics / Tracing

- Observability is cross-document consistency. The feature is complete when architecture, codebase context, roadmap, and Codex README all tell the same story.

### Security

- No secrets or local machine details beyond generic path conventions should appear in shared docs.

### Runbook

- Read `codex/README.md`, `docs/ARCHITECTURE.md`, `docs/CODEBASE_CONTEXT.md`, and `docs/phases/PHASES_OVERVIEW.md` together before closing the feature.
- If later Codex features need new subdirectories, update `codex/README.md` first so the structure remains intentional.

## F. Test Plan

### Acceptance Criteria Test Mapping

| Acceptance Criteria | Test Type | Planned Verification |
|---------------------|-----------|----------------------|
| AC1 | Manual document audit | Confirm `codex/README.md` names current docs and future artifact areas |
| AC2 | Terminology review | Confirm source-owned and runtime-owned locations are clearly separated |
| AC3 | Cross-doc consistency audit | Confirm architecture and codebase context both describe Codex accurately |
| AC4 | Roadmap alignment review | Confirm Phase 02 wording in roadmap matches Phase 02 summary and Codex README |
| AC5 | Structure review | Confirm layout reserves future areas without implementing them prematurely |

### Top 5 High-Value Test Cases

1. Given a new contributor opens the repo, when they read `codex/README.md`, then they can tell which Codex materials belong in the repo and which belong in runtime install paths.
2. Given an architecture reader previously knew only the three-platform model, when they read `docs/ARCHITECTURE.md`, then they understand Codex is a fourth platform with global AGENTS guidance, TOML agents, and directory skills.
3. Given a maintainer updates the roadmap, when they consult `docs/phases/PHASES_OVERVIEW.md`, then the Phase 02 description matches the new Codex terminology and scope.
4. Given a future feature needs to add a Codex agent copy, when the maintainer reads `codex/README.md`, then there is a reserved destination concept without requiring a folder reorganization.
5. Given the runtime `.codex/config.toml` already exists, when someone reads the layout docs, then they do not mistake `.codex/` for the repository-owned authoring area.

### Test Data, Mocks, or Fixtures Needed

- Empty `codex/` directory
- `docs/ARCHITECTURE.md`
- `docs/CODEBASE_CONTEXT.md`
- `docs/phases/PHASES_OVERVIEW.md`
- `docs/phases/PHASE_02/PHASE_02_SUMMARY.md`

## Stage 0: Test Prerequisites
**Goal**: Establish baseline test coverage using `@z-test-writer`
**Success Criteria**: Test suite exists, coverage ≥ 50%, all tests pass
**Status**: Required before implementation begins

## Stage 1: Define the Repository-Owned Codex Layout
**Goal**: Create `codex/README.md` that defines the Codex source area, current doc set, and reserved future artifact categories.
**Success Criteria**: AC1, AC2, and AC5 are satisfied without creating runnable Codex artifacts.
**Status**: Not Started

## Stage 2: Update Shared Architecture and Roadmap Docs
**Goal**: Bring the shared repo docs into alignment with the Codex source layout and four-platform model.
**Success Criteria**: AC3 and AC4 are satisfied across `docs/ARCHITECTURE.md`, `docs/CODEBASE_CONTEXT.md`, and `docs/phases/PHASES_OVERVIEW.md`.
**Status**: Not Started