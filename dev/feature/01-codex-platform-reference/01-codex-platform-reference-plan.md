# 01 Codex Platform Reference

## Execution Metadata

- **Wave:** 1
- **Parallel safe:** yes
- **Depends on:** none
- **Key files modified:** `codex/CODEX_PLATFORM_REFERENCE.md`
- **Sequential reason:** n/a

## A. Requirements & Traceability

### Acceptance Criteria

1. **AC1**: `codex/CODEX_PLATFORM_REFERENCE.md` documents Codex-native discovery and authoring behavior for global AGENTS guidance, custom agents, skills, and relevant `.codex/config.toml` settings.
2. **AC2**: The reference states the verified macOS-relevant install and discovery locations: `~/.codex/config.toml`, `~/.codex/AGENTS.md`, `~/.codex/AGENTS.override.md`, `~/.codex/agents/`, and `$HOME/.agents/skills/`.
3. **AC3**: The reference distinguishes clearly between repository-owned source material under `codex/` and runtime-installed surfaces under `.codex/` and the user home directory.
4. **AC4**: The reference captures Codex precedence rules accurately enough that a future implementation pass does not need to rediscover AGENTS precedence, custom-agent file format, or skill discovery roots.
5. **AC5**: The document includes source-backed provenance notes or an explicit “last verified” section so future maintainers know to recheck upstream Codex behavior before implementation.

### Non-Goals

- Do not create runnable Codex agents, skills, or global AGENTS files in this feature.
- Do not update shared architecture or roadmap documents in this feature.
- Do not define the repository-owned Codex folder structure beyond what is needed to author this single reference document.

### Traceability

| Acceptance Criteria | Code Areas/Modules | Planned Tests |
|---------------------|-------------------|---------------|
| AC1: Codex-native discovery and authoring behavior documented | `codex/CODEX_PLATFORM_REFERENCE.md`, `.codex/config.toml`, `docs/phases/PHASE_02/PHASE_02_DISCOVERY_CONTEXT.md` | Manual reference readback against discovery context and local config |
| AC2: macOS locations are explicit | `codex/CODEX_PLATFORM_REFERENCE.md` | Path checklist review against discovery context |
| AC3: source-vs-runtime distinction is explicit | `codex/CODEX_PLATFORM_REFERENCE.md`, `docs/phases/PHASE_02/PHASE_02_SUMMARY.md` | Manual terminology consistency review |
| AC4: precedence rules are implementation-ready | `codex/CODEX_PLATFORM_REFERENCE.md` | Scenario-based readback for AGENTS, agents, and skills discovery |
| AC5: provenance or verification notes included | `codex/CODEX_PLATFORM_REFERENCE.md` | Manual section presence check |

## B. Correctness & Edge Cases

### Key Workflows

- A maintainer reads the reference before authoring any Codex copy and can answer where global guidance, custom agents, and skills belong on macOS.
- A future implementer uses the reference to distinguish repository docs from install-time locations and avoids writing Codex content into the wrong tree.

### Failure Modes and Edge Cases

- AGENTS precedence can be misread if the document fails to distinguish global home discovery from project-root walk-up discovery.
- The local `.codex/config.toml` file can be mistaken for the intended authoring destination unless the doc calls out the runtime/source-of-truth split explicitly.
- Codex skills can be mislocated if the doc omits that user-scoped skills live in `$HOME/.agents/skills` rather than under `~/.codex/skills`.
- Upstream Codex behavior may drift. The document must make revalidation before implementation a first-class requirement.

### Error-Handling Strategy

- Prefer fail-fast wording: if an install location or precedence rule is not verified by current docs, the reference should say so instead of extrapolating.
- Treat ambiguous behavior as “recheck before implementation,” not as settled contract.

## C. Consistency & Architecture Fit

### Existing Patterns To Follow

- Follow the repository’s documentation-first style from `docs/CODEBASE_CONTEXT.md` and `docs/ARCHITECTURE.md`: concise headings, explicit file paths, and clear source-of-truth language.
- Keep Codex guidance as repository-owned documentation under `codex/`, not as live runtime configuration under `.codex/`.

### Interfaces and Contracts

- Input contract: Phase 02 summary, discovery context, local `.codex/config.toml`, and current repository platform model.
- Output contract: one self-contained reference doc that future features can cite without repeating platform basics.

### Sibling Feature Relationships

- `01-codex-source-layout` runs in the same wave and stays disjoint by defining where Codex artifacts belong in the repo.
- `02-codex-macos-setup-guide` depends on this feature’s factual platform reference.
- `02-codex-porting-guide` depends on this feature’s documented Codex model before mapping `.github/` sources to Codex targets.

## D. Clean Design & Maintainability

### Simplest Design

- Author a single reference document with four sections: discovery model, custom agents, skills, and config/runtime locations.
- Use repository-specific callouts only where local context matters, such as the existing `.codex/config.toml` and empty `codex/` directory.

### Complexity Risks

- Mixing normative upstream behavior with this repo’s policy decisions will make the document hard to trust.
- Repeating porting decisions here would duplicate Feature 2’s guide and invite drift.

### Keep It Clean Checklist

- [ ] Separate verified Codex behavior from repository policy.
- [ ] Use literal paths for all macOS locations.
- [ ] Call out source-vs-runtime separation explicitly.
- [ ] Include a revalidation note for upstream behavior.

## E. Completeness: Observability, Security, Operability

### Logging / Metrics / Tracing

- Observability is documentation provenance: include the source categories consulted and a last-verified note.
- No runtime metrics or tracing are required for this docs-only feature.

### Security

- Do not include any user-specific secrets, tokens, or machine-local values beyond generic macOS home-directory paths.
- Keep examples generic and non-destructive.

### Runbook

- Verify the reference against `docs/phases/PHASE_02/PHASE_02_DISCOVERY_CONTEXT.md` before closing the feature.
- Recheck upstream Codex docs immediately before any later implementation feature uses this document as a contract.
- If upstream behavior changes, update this reference first, then update downstream Codex docs that depend on it.

## F. Test Plan

### Acceptance Criteria Test Mapping

| Acceptance Criteria | Test Type | Planned Verification |
|---------------------|-----------|----------------------|
| AC1 | Manual document audit | Confirm discovery, agents, skills, and config sections all exist and match discovery context |
| AC2 | Path checklist | Confirm all five macOS locations appear literally and in the correct role |
| AC3 | Terminology review | Confirm the doc distinguishes `codex/`, `.codex/`, and `$HOME/.agents/skills` without overlap |
| AC4 | Scenario readback | Walk through AGENTS, agent, and skill lookup scenarios using the document alone |
| AC5 | Section presence check | Confirm provenance / last-verified guidance is present |

### Top 5 High-Value Test Cases

1. Given a reader starting from this repo alone, when they read the reference, then they can identify the correct home-directory destination for each Codex surface without consulting external docs.
2. Given the local `.codex/config.toml` exists, when the reference describes runtime config, then it does not imply `.codex/` is the source-of-truth destination for authored platform docs.
3. Given a future agent author wants to port AGENTS-style behavior, when they read the precedence section, then they understand global Codex AGENTS guidance loads before project-local AGENTS files.
4. Given a future skill author wants to install a Codex skill, when they read the skills section, then they place user-scoped skills under `$HOME/.agents/skills` instead of inventing a `.codex/skills` location.
5. Given upstream Codex behavior changes later, when a maintainer reads the provenance note, then they know the document must be revalidated before use as an implementation contract.

### Test Data, Mocks, or Fixtures Needed

- Existing local `.codex/config.toml`
- `docs/phases/PHASE_02/PHASE_02_DISCOVERY_CONTEXT.md`
- `docs/phases/PHASE_02/PHASE_02_SUMMARY.md`

## Stage 0: Test Prerequisites
**Goal**: Establish baseline test coverage using `@z-test-writer`
**Success Criteria**: Test suite exists, coverage ≥ 50%, all tests pass
**Status**: Required before implementation begins

## Stage 1: Author the Codex Platform Reference
**Goal**: Create `codex/CODEX_PLATFORM_REFERENCE.md` with verified sections for AGENTS discovery, custom agents, skills, and config/runtime locations.
**Success Criteria**: AC1, AC2, and AC3 are satisfied in a single self-contained document.
**Status**: Not Started

## Stage 2: Add Provenance and Revalidation Guidance
**Goal**: Make the document safe for future reuse by adding explicit source provenance and a recheck-before-implementation note.
**Success Criteria**: AC4 and AC5 are satisfied, and the doc can serve as a stable prerequisite for the setup and porting guides.
**Status**: Not Started