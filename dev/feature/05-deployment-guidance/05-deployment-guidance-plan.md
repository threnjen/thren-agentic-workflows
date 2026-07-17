# Feature Plan: Deployment Guidance

## Execution Metadata

- **Wave:** 5
- **Parallel safe:** no
- **Depends on:** `04-managed-copy-reconciliation`
- **Key files modified:** `.github/agents/evangelize.agent.md`, `claude/commands/evangelize.md`, `codex/agents/evangelize.toml`, `codex/profiles/evangelize.config.toml`, `opencode/agents/evangelize.md`, `claude/README.md`, `claude/SYMLINK_SETUP.md`, `claude/agents/README.md`, `codex/MACOS_SETUP_AND_SYMLINKS.md`, `codex/PILOT_SLICE_PLAN.md`, `opencode/SYMLINK_SETUP.md`, `HARNESS_SETUP.md`, `docs/TROUBLESHOOTING.md`, `README.md`, `scripts/propagate_master_assets.py` `(verify)`, `tests/test_propagate_master_assets.py`, `tests/test_phase04_runtime_deployment.py` `[PROPOSED - name TBD]`
- **Sequential reason:** consumes the managed-copy API from upstream `04-managed-copy-reconciliation` and shares `scripts/propagate_master_assets.py` `(verify)` plus propagation/integration tests with upstream features

## A. Requirements & Traceability

### Acceptance Criteria

1. **AC1:** `.github/agents/evangelize.agent.md` requires repository convergence followed by the managed-copy deployment API from Features 2 and 4 and contains no behavior that creates, repairs, recommends, or validates runtime symlinks or junctions.
2. **AC2:** Evangelize preflight and completion checks verify regular-copy freshness, expected roster coverage, collision outcomes, per-harness status, and runtime discovery without treating a link as successful deployment.
3. **AC3:** Generated Claude, Codex, and OpenCode Evangelize variants are regenerated from the corrected source and preserve the same managed-copy contract.
4. **AC4:** Supported Claude, Codex, and OpenCode setup guides replace runtime link-creation procedures with safe managed-copy deployment and verification guidance.
5. **AC5:** Supported guidance contains no runtime link-creation path for generated agents, commands, skills, profiles, hook/settings outputs, or learning assets.
6. **AC6:** Legitimate historical discussion and security guidance about symlink attacks, containment, or retired behavior remains distinguishable from prohibited operational setup instructions.
7. **AC7:** Documentation regression checks fail when operational `ln -s`, `New-Item -ItemType SymbolicLink`, `mklink`, junction creation, or equivalent runtime-link repair instructions return to supported deployment surfaces.
8. **AC8:** Guidance explicitly treats native Windows and WSL as separate runs, reports unavailable platforms as `NOT RUN`, and never claims cross-platform readiness based on another platform's evidence.

### Non-Goals

- Removing every occurrence of the words symlink or junction from historical/security records.
- Rewriting application-managed, package-manager, plugin-cache, debug-pointer, or Git-hook installation guidance unrelated to generated runtime assets.
- Adding plugin packaging or public distribution.
- Hand-editing generated Evangelize outputs without regenerating from source.

### Traceability Matrix

| Acceptance Criteria | Code Areas/Modules | Planned Tests |
|---|---|---|
| AC1–AC2 | `.github/agents/evangelize.agent.md`; upstream orchestration/deployment contract | Source-agent declaration and workflow assertions; managed-copy invocation scenario |
| AC3 | Generated Evangelize files in `claude/`, `codex/`, and `opencode/` | Existing cross-harness propagation equality/intent checks updated for Evangelize |
| AC4–AC6 | Platform setup guides, `HARNESS_SETUP.md`, `docs/TROUBLESHOOTING.md`, and active README surfaces | Operational-instruction audit with allowlisted historical/security contexts |
| AC7 | Proposed consolidated phase regression checks | Negative fixture containing prohibited link-creation instructions |
| AC8 | Evangelize output matrix and setup guidance | Static readiness-status assertions and manual cross-platform review |

## B. Correctness & Edge Cases

- Do not replace link commands with vague manual-copy steps that bypass ownership, convergence, or collision checks.
- Ensure every generated Evangelize variant names the platform-valid managed deployment entry point after propagation rewriting.
- Classify text by operational intent so documentation tests do not ban security discussion of symlink threats.
- Include profiles, commands, skills, settings/hooks, and learnings in regression coverage rather than checking agents only.
- Remove stale per-platform setup claims even when they live in pilot or README surfaces rather than the main setup file.

## C. Consistency & Architecture Fit

- `.github/agents/evangelize.agent.md` remains the source of truth; generated variants must not be hand-maintained.
- Call the Feature 2 orchestration API, which in turn uses Feature 3 destination records and Feature 4 managed-copy operations; do not restate copy algorithms in prose.
- Follow existing propagation-based agent generation and marker conventions.
- Relationship: Feature 6 verifies these instructions against actual scratch-home and live runtime behavior.
- `scripts/propagate_master_assets.py` is `(verify)`: it should change only if regeneration or a supported invocation adapter requires it.

## D. Clean Design & Maintainability

- Prefer one canonical deployment command/workflow referenced by each guide.
- Replace platform-specific link recipes with platform-specific verification notes only where behavior genuinely differs.
- Keep regression checks focused on executable/setup language, not incidental nouns.
- Keep it clean checklist: source-first edit, regenerate all variants, no hand drift, no link repair, no readiness overclaim.

## E. Completeness: Observability, Security, Operability

- Observability: Evangelize reports structured propagation, collision, copy, freshness, and runtime-discovery results; it must not add normal-path per-file chatter.
- Security: documentation must preserve collision review and preflight before any live-home mutation.
- Operability: setup guidance includes deploy, verify, partial failure, rerun, watcher restart, and rollback references.
- Rollback: use managed-copy ownership records and version control; never restore the retired runtime-link model as rollback.

## F. Test Plan

- Update propagation tests that compare Evangelize across generated harnesses.
- Add documentation regression scenarios to the proposed consolidated Phase 04 test file rather than relying on manual grep alone.
- Retain security/historical symlink discussion fixtures as allowed examples.
- Manual review must inspect rendered/generated agent bodies, not only filenames.

### Top 5 High-Value Test Cases

1. **Given** corrected Evangelize source, **when** propagation converges, **then** every generated variant requires managed-copy deployment and contains no runtime-link repair workflow.
2. **Given** a supported setup guide containing an operational `ln -s` example for generated skills, **when** documentation regression runs, **then** it fails.
3. **Given** a security paragraph explaining a hostile symlink, **when** regression runs, **then** the paragraph remains allowed.
4. **Given** a partial Codex deployment failure, **when** Evangelize reports completion, **then** Codex is blocked/partial and other verified harnesses are reported separately.
5. **Given** a Windows or WSL platform is unavailable, **when** readiness is summarized, **then** it is `NOT RUN` and the overall result is not full cross-platform GO.

## Stage 1: Rewrite Evangelize Source
**Goal**: Replace runtime-link behavior with the shared managed-copy workflow.
**Success Criteria**: AC1 and AC2 pass source-agent contract review.
**Status**: Not Started

## Stage 2: Regenerate Harness Variants
**Goal**: Propagate the corrected Evangelize behavior to Claude, Codex, and OpenCode.
**Success Criteria**: AC3 passes generated-output comparison and convergence tests.
**Status**: Not Started

## Stage 3: Reconcile Setup Guidance
**Goal**: Remove supported runtime-link creation and add regression protection.
**Success Criteria**: AC4–AC8 pass documentation tests and manual review.
**Status**: Not Started

## Unverified Assumptions

- `codex/PILOT_SLICE_PLAN.md` remains a supported setup surface rather than purely historical context; implementation must classify it explicitly before editing.
