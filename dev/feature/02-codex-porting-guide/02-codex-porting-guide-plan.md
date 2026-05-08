# 02 Codex Porting Guide

## Execution Metadata

- **Wave:** 2
- **Parallel safe:** yes
- **Depends on:** 01-codex-platform-reference, 01-codex-source-layout
- **Key files modified:** `codex/CODEX_PORTING_GUIDE.md`
- **Sequential reason:** n/a

## A. Requirements & Traceability

### Acceptance Criteria

1. **AC1**: `codex/CODEX_PORTING_GUIDE.md` maps `.github/instructions/` content into Codex global AGENTS guidance and agent `developer_instructions` rather than treating instructions as a repo-local file-for-file copy surface.
2. **AC2**: The guide maps `.github/agents/` into Codex custom-agent TOML files and explains the required Codex fields and the main non-portable differences from Markdown agent manifests.
3. **AC3**: The guide maps `.github/skills/` into Codex skill directories and explains how directory-based skills differ from the current master skill structure.
4. **AC4**: The guide classifies what content is portable, what content must be transformed, and what content is GitHub-only or otherwise non-portable.
5. **AC5**: The guide makes the global AGENTS rule explicit and durable: AGENTS-derived content maps to the global Codex AGENTS layer, not either repository’s checked-in `AGENTS.md`.
6. **AC6**: The guide references the repository-owned Codex source area defined in `codex/README.md` so future ported artifacts have a documented landing zone.

### Non-Goals

- Do not create actual Codex TOML agent files or skill directories in this feature.
- Do not author the pilot conversion selection itself in this feature.
- Do not rewrite existing `.github/` source assets.

### Traceability

| Acceptance Criteria | Code Areas/Modules | Planned Tests |
|---------------------|-------------------|---------------|
| AC1: instructions mapped to global AGENTS and developer instructions | `codex/CODEX_PORTING_GUIDE.md`, `.github/instructions/`, `.github/agents/` | Manual mapping review against Phase 02 summary |
| AC2: agents mapped to Codex TOML custom agents | `codex/CODEX_PORTING_GUIDE.md`, `.github/agents/` | Field-by-field mapping audit |
| AC3: skills mapped to Codex skill directories | `codex/CODEX_PORTING_GUIDE.md`, `.github/skills/` | Directory-model comparison review |
| AC4: portable vs transformed vs non-portable classification | `codex/CODEX_PORTING_GUIDE.md` | Classification completeness review |
| AC5: global AGENTS rule explicit | `codex/CODEX_PORTING_GUIDE.md`, `docs/phases/PHASE_02/PHASE_02_SUMMARY.md` | Policy wording review |
| AC6: landing zone references current Codex layout | `codex/CODEX_PORTING_GUIDE.md`, `codex/README.md` | Cross-link and path review |

## B. Correctness & Edge Cases

### Key Workflows

- A maintainer reads the guide before porting a `.github/` asset and can classify the correct Codex destination immediately.
- A future implementer uses the guide to split one source asset into multiple Codex surfaces when necessary, such as global guidance plus agent-specific instructions.

### Failure Modes and Edge Cases

- `.github/instructions/` could be copied too literally unless the guide explains that Codex has no direct equivalent to this repo’s instruction-file system.
- GitHub-specific agent metadata can be carried over incorrectly unless the guide calls out TOML field translation and dropped behavior explicitly.
- Skills can be mishandled if the guide assumes current master skill organization maps 1:1 without directory and optional-asset differences.
- Some guidance may belong partly in global AGENTS and partly in agent `developer_instructions`; the guide must support split mapping rather than forcing one destination.

### Error-Handling Strategy

- Prefer explicit classification tables over narrative-only guidance.
- When a source behavior is not clearly portable, mark it as “requires Codex-specific rewrite” rather than implying parity.

## C. Consistency & Architecture Fit

### Existing Patterns To Follow

- Use `.github/` as master source-of-truth vocabulary, matching the current architecture docs.
- Build on `codex/CODEX_PLATFORM_REFERENCE.md` instead of repeating platform basics.

### Interfaces and Contracts

- Input contract: `.github/instructions/`, `.github/agents/`, `.github/skills/`, Phase 02 summary, and the Codex platform reference.
- Output contract: one mapping guide that future implementation work can use to create Codex copies without rediscovering destination rules.

### Sibling Feature Relationships

- Depends on `01-codex-platform-reference` for Codex-native behavior and on `01-codex-source-layout` for destination terminology.
- Runs in parallel with `02-codex-macos-setup-guide` because the file scopes are disjoint.
- `03-codex-pilot-slice-definition` depends on this guide because the pilot must exercise the documented mapping rules.

## D. Clean Design & Maintainability

### Simplest Design

- Structure the guide by source surface: instructions, agents, skills.
- For each surface, include destination, transformation rules, non-portable concerns, and a short example classification.

### Complexity Risks

- Mixing repository policy with Codex platform facts will duplicate the platform reference.
- Failing to classify non-portable behavior will make later pilot work unstable and argumentative.

### Keep It Clean Checklist

- [ ] Each `.github/` source surface has a single documented Codex target model.
- [ ] Split-destination cases are called out explicitly.
- [ ] Non-portable GitHub-only behavior is documented rather than silently omitted.
- [ ] The guide references `codex/README.md` for destination paths.

## E. Completeness: Observability, Security, Operability

### Logging / Metrics / Tracing

- Observability is mapping clarity: a reader should be able to trace any `.github/` artifact family to its Codex destination without extra discovery.

### Security

- Do not include secrets, private machine paths, or unverified runtime assumptions.
- Keep examples generic and repository-local.

### Runbook

- Re-read the guide against the live `.github/` tree before any pilot or full conversion work.
- If a new `.github/` source surface is added later, extend the mapping guide before porting that surface.
- If Codex changes field names or discovery rules, update the platform reference first, then revise this guide.

## F. Test Plan

### Acceptance Criteria Test Mapping

| Acceptance Criteria | Test Type | Planned Verification |
|---------------------|-----------|----------------------|
| AC1 | Mapping audit | Confirm instructions map to global AGENTS guidance and/or `developer_instructions` |
| AC2 | Field translation review | Confirm the guide names required Codex custom-agent fields and major format differences |
| AC3 | Structure review | Confirm skills are mapped to Codex directory assets rather than standalone manifests |
| AC4 | Classification review | Confirm portable / transformed / non-portable categories all exist and are populated |
| AC5 | Policy audit | Confirm the global AGENTS rule is explicit and central |
| AC6 | Cross-link review | Confirm the guide references the repository-owned Codex area consistently |

### Top 5 High-Value Test Cases

1. Given a maintainer wants to port a `.github/instructions/` file, when they read the guide, then they understand it becomes global guidance and/or agent `developer_instructions`, not a repo-local instruction file.
2. Given a maintainer wants to port a `.github/agents/*.agent.md` file, when they read the guide, then they know a Codex custom agent is TOML-based and which required fields must be supplied.
3. Given a maintainer wants to port a `.github/skills/` entry, when they read the guide, then they understand the Codex destination is a directory skill with `SKILL.md` and optional assets.
4. Given an existing GitHub-only behavior has no direct Codex equivalent, when the guide addresses it, then it is classified explicitly rather than carried over implicitly.
5. Given the user’s global AGENTS policy, when the guide discusses AGENTS-derived content, then it directs that content to the global Codex AGENTS layer and never to checked-in repo AGENTS files.

### Test Data, Mocks, or Fixtures Needed

- `.github/instructions/`
- `.github/agents/`
- `.github/skills/`
- `codex/CODEX_PLATFORM_REFERENCE.md`
- `codex/README.md`

## Stage 0: Test Prerequisites
**Goal**: Establish baseline test coverage using `@z-test-writer`
**Success Criteria**: Test suite exists, coverage ≥ 50%, all tests pass
**Status**: Required before implementation begins

## Stage 1: Map `.github/` Source Surfaces to Codex Targets
**Goal**: Create `codex/CODEX_PORTING_GUIDE.md` with distinct mapping sections for instructions, agents, and skills.
**Success Criteria**: AC1, AC2, and AC3 are satisfied with explicit destination and transformation rules.
**Status**: Not Started

## Stage 2: Classify Portability and Landing Zones
**Goal**: Make the guide implementation-ready by classifying portable vs transformed vs non-portable content and tying each mapping to the repository-owned Codex area.
**Success Criteria**: AC4, AC5, and AC6 are satisfied, and the guide can drive later pilot conversion work.
**Status**: Not Started