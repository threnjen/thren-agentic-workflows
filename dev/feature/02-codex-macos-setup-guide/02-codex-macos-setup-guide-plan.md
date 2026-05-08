# 02 Codex macOS Setup Guide

## Execution Metadata

- **Wave:** 2
- **Parallel safe:** yes
- **Depends on:** 01-codex-platform-reference, 01-codex-source-layout
- **Key files modified:** `codex/MACOS_SETUP_AND_SYMLINKS.md`
- **Sequential reason:** n/a

## A. Requirements & Traceability

### Acceptance Criteria

1. **AC1**: `codex/MACOS_SETUP_AND_SYMLINKS.md` documents the correct macOS install locations for global Codex AGENTS guidance, custom agents, skills, and config.
2. **AC2**: The guide includes explicit, reversible symlink examples for `~/.codex/AGENTS.md`, `~/.codex/AGENTS.override.md`, `~/.codex/agents/`, and `$HOME/.agents/skills/` that point back to repository-owned Codex artifacts rather than repo-local AGENTS files.
3. **AC3**: The guide explains how the repository-owned `codex/` area relates to runtime `.codex/` and `$HOME/.agents/skills/` targets on macOS.
4. **AC4**: The guide includes guardrails for idempotent setup, such as `ln -sfn`, parent-directory creation, and how to inspect or replace existing symlinks safely.
5. **AC5**: The guide makes the global AGENTS rule explicit: AGENTS-derived source content should be installed into the global Codex AGENTS layer, not either repository’s checked-in `AGENTS.md`.

### Non-Goals

- Do not perform any real installation into the user’s home directory.
- Do not create the actual Codex global AGENTS file or custom-agent TOML artifacts in this feature.
- Do not define `.github/` to Codex content mapping beyond what is necessary to explain setup targets.

### Traceability

| Acceptance Criteria | Code Areas/Modules | Planned Tests |
|---------------------|-------------------|---------------|
| AC1: macOS install locations documented | `codex/MACOS_SETUP_AND_SYMLINKS.md` | Path checklist review |
| AC2: reversible symlink examples included | `codex/MACOS_SETUP_AND_SYMLINKS.md` | Command-readback review for target/source paths |
| AC3: repo-owned vs runtime-owned relationship explained | `codex/MACOS_SETUP_AND_SYMLINKS.md`, `codex/README.md` | Terminology consistency check |
| AC4: idempotent setup guidance included | `codex/MACOS_SETUP_AND_SYMLINKS.md` | Manual command safety review |
| AC5: global AGENTS rule explicit | `codex/MACOS_SETUP_AND_SYMLINKS.md`, `docs/phases/PHASE_02/PHASE_02_SUMMARY.md` | Policy wording review |

## B. Correctness & Edge Cases

### Key Workflows

- A macOS user follows the guide to point runtime Codex locations at repository-owned artifacts with symlinks.
- A maintainer uses the guide to understand which future Codex files will need to exist before installation is meaningful.

### Failure Modes and Edge Cases

- Existing files at install targets can be overwritten unintentionally unless the guide explains inspection and replacement behavior.
- Skills can be linked into the wrong root if the guide treats `$HOME/.agents/skills` like a `.codex` subdirectory.
- AGENTS-derived content can land in repo-local `AGENTS.md` if the global-rule callout is not prominent.
- A guide that omits parent-directory creation will fail on a clean machine.

### Error-Handling Strategy

- Prefer explicit preflight checks: verify source files exist, create parent directories, then install symlinks.
- Prefer reversible examples and clear “remove or relink” steps over destructive replacement instructions.

## C. Consistency & Architecture Fit

### Existing Patterns To Follow

- Align with the Codex facts documented in `codex/CODEX_PLATFORM_REFERENCE.md`.
- Keep setup instructions in the repository-owned `codex/` area rather than expanding platform logic into shared repo docs.

### Interfaces and Contracts

- Input contract: Codex platform reference, Codex source layout, and Phase 02 discovery context.
- Output contract: one macOS-oriented setup guide that can later be executed manually once pilot artifacts exist.

### Sibling Feature Relationships

- Depends on `01-codex-platform-reference` for factual install/discovery rules.
- Depends on `01-codex-source-layout` so the guide points at the intended repository-owned artifact area.
- Runs in parallel with `02-codex-porting-guide` because the files are disjoint.
- Supplies installation and validation context for `03-codex-pilot-slice-definition`.

## D. Clean Design & Maintainability

### Simplest Design

- Author one guide with four parts: prerequisites, install targets, symlink examples, and rollback/inspection steps.
- Use placeholder repository paths that clearly point into the future `codex/` artifact area rather than pretending the live runtime files already exist.

### Complexity Risks

- Overly concrete examples will age badly if the future Codex artifact layout changes.
- Overly abstract examples will be useless for a real macOS setup pass.

### Keep It Clean Checklist

- [ ] Every install target uses the correct macOS path.
- [ ] Examples are idempotent and reversible.
- [ ] The guide never tells users to install Codex guidance into repo-local `AGENTS.md`.
- [ ] Setup steps remain documentation-only and do not imply they were executed.

## E. Completeness: Observability, Security, Operability

### Logging / Metrics / Tracing

- Observability is operational clarity: the guide should tell users how to inspect existing symlinks and verify target paths before replacing anything.

### Security

- Do not include machine-specific absolute paths beyond generic home-directory examples.
- Avoid destructive shell patterns; prefer symlink replacement guidance with explicit inspection steps.

### Runbook

- Recheck the guide against the final repository-owned Codex artifact paths before any real install.
- If the future Codex source layout changes, update this guide in the same change.
- Validate that each shell example is idempotent and leaves a clean rollback path.

## F. Test Plan

### Acceptance Criteria Test Mapping

| Acceptance Criteria | Test Type | Planned Verification |
|---------------------|-----------|----------------------|
| AC1 | Path checklist | Confirm all required macOS targets appear literally and correctly |
| AC2 | Command audit | Confirm each symlink example points from runtime location to repo-owned artifact path |
| AC3 | Terminology review | Confirm the doc distinguishes source-owned and runtime-owned surfaces |
| AC4 | Safety review | Confirm the guide documents parent-directory creation, `ln -sfn`, and verification steps |
| AC5 | Policy audit | Confirm the global AGENTS rule is called out directly and unambiguously |

### Top 5 High-Value Test Cases

1. Given a clean macOS machine, when a reader follows the guide, then they know which parent directories must exist before adding any symlink.
2. Given an existing `~/.codex/AGENTS.md` file or symlink, when the reader follows the guide, then they see how to inspect and replace it safely.
3. Given a future repository-owned Codex agent file, when the guide shows the custom-agent install path, then it targets `~/.codex/agents/` and not a repo-local directory.
4. Given a future repository-owned skill folder, when the guide shows the skill install path, then it targets `$HOME/.agents/skills` and not `.codex/skills`.
5. Given the user wants AGENTS-derived content installed, when they read the guide, then they understand it belongs in the global Codex AGENTS layer, not either repository’s checked-in `AGENTS.md`.

### Test Data, Mocks, or Fixtures Needed

- `codex/CODEX_PLATFORM_REFERENCE.md`
- `codex/README.md`
- `docs/phases/PHASE_02/PHASE_02_DISCOVERY_CONTEXT.md`

## Stage 0: Test Prerequisites
**Goal**: Establish baseline test coverage using `@z-test-writer`
**Success Criteria**: Test suite exists, coverage ≥ 50%, all tests pass
**Status**: Required before implementation begins

## Stage 1: Author the macOS Setup and Symlink Guide
**Goal**: Create `codex/MACOS_SETUP_AND_SYMLINKS.md` with correct install targets, symlink flow, and source-vs-runtime explanations.
**Success Criteria**: AC1, AC2, and AC3 are satisfied in a guide that remains documentation-only.
**Status**: Not Started

## Stage 2: Add Idempotency and Safety Guidance
**Goal**: Make the guide operationally safe by documenting preflight inspection, parent-directory creation, `ln -sfn`, and rollback steps.
**Success Criteria**: AC4 and AC5 are satisfied, and the guide is ready to support a later pilot installation exercise.
**Status**: Not Started