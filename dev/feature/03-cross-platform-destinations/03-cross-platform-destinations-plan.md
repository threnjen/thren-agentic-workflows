# Feature Plan: Cross-Platform Destinations

## Execution Metadata

- **Wave:** 3
- **Parallel safe:** no
- **Depends on:** `02-propagation-convergence`
- **Key files modified:** `scripts/propagate_master_assets.py`, `scripts/runtime_deployment.py` `[PROPOSED - name TBD]`, `tests/test_propagate_master_assets.py`, `tests/test_phase04_runtime_deployment.py` `[PROPOSED - name TBD]`
- **Sequential reason:** shares `scripts/propagate_master_assets.py`, `tests/test_propagate_master_assets.py`, and the proposed phase integration test with upstream `02-propagation-convergence`

## A. Requirements & Traceability

### Acceptance Criteria

1. **AC1:** A reusable destination-resolution API `[PROPOSED - name TBD]` returns explicit source and active-user destination records for each supported Claude, Codex, and OpenCode asset class.
2. **AC2:** Claude destinations honor `CLAUDE_CONFIG_DIR`; otherwise they resolve beneath the active user's `.claude` directory for generated agents, commands, skills, and repository-managed learning assets. Existing user-global hook deployment remains outside the new managed-copy stage.
3. **AC3:** Codex-owned runtime destinations honor `CODEX_HOME`, while skill destinations use the documented active-user skill location unless verified runtime support provides a configured alternative.
4. **AC4:** OpenCode destinations honor `OPENCODE_CONFIG_DIR` for documented asset classes, while skills use their documented user location unless verified runtime support provides a configured alternative.
5. **AC5:** macOS and Linux defaults remain inside the active POSIX user's home, and native Windows defaults remain inside the active Windows user profile without administrator privileges or Developer Mode.
6. **AC6:** WSL is detected and treated as the current independent Linux environment; a WSL run never targets the native Windows profile, another distribution, or another user's home.
7. **AC7:** Unsupported cross-environment requests and ambiguous or relative relocation values fail before mutation with a diagnosable, content-safe error.
8. **AC8:** Destination records are normalized without following a destination leaf link and are suitable for the parent-boundary and ownership checks required by `04-managed-copy-reconciliation`.

### Non-Goals

- Deploying from Windows into WSL, WSL into Windows, or across WSL distributions.
- Discovering or modifying other users' homes.
- Creating runtime links or requiring elevated link privileges.
- Deciding whether an existing destination is owned; Feature 4 owns classification.
- Adding undocumented relocation variables.
- Folding existing user-global hook deployment into the new asset-copy stage.

### Traceability Matrix

| Acceptance Criteria | Code Areas/Modules | Planned Tests |
|---|---|---|
| AC1 | `[PROPOSED - name TBD]` runtime deployment support module; propagator integration | Complete asset-class roster and stable record-shape scenarios |
| AC2–AC4 | Harness destination adapters | Default and environment-override matrix for Claude, Codex, and OpenCode |
| AC5–AC7 | Platform/environment detection and active-home validation | macOS, Linux, native Windows, WSL, malformed override, and cross-environment rejection scenarios |
| AC8 | Normalization and parent-boundary handoff | Leaf-link and symlinked-parent scratch-path scenarios shared with Feature 4 |

## B. Correctness & Edge Cases

- Treat empty relocation variables as invalid or as documented absence consistently; do not silently resolve relative paths against the repository.
- Normalize platform path syntax without requiring the destination to exist.
- Do not use `Path.resolve()` in a way that follows the destination leaf before classification.
- Detect symlinked or junction-based parents and pass enough information for Feature 4 to reject escapes.
- Keep native Windows and WSL detection mutually exclusive for a single run.
- Asset rosters must include generated agents, commands/profiles, skills, hook/settings outputs, and supported learning assets without inventing project-local targets.

## C. Consistency & Architecture Fit

- Use the repository's existing `pathlib.Path` and dataclass-oriented patterns where applicable.
- Keep platform policy in one narrow resolver API rather than scattering environment-variable checks through copy loops.
- Public downstream contract: `04-managed-copy-reconciliation` consumes destination records from this feature and must not recompute paths.
- Upstream contract: call the bounded orchestration API `[PROPOSED - name TBD]` supplied by `02-propagation-convergence` only after repository fixed-point verification.
- Relationship: Feature 4 depends on this feature at runtime and shares its proposed support module and integration tests.

## D. Clean Design & Maintainability

- Prefer a data table plus small harness adapters over platform-specific copy implementations.
- Keep source roster derivation separate from destination policy.
- Make active-home/platform context injectable for tests; never patch the author's real home.
- Keep it clean checklist: documented variables only, one platform classification, absolute destinations, no cross-user scan, no link creation.

## E. Completeness: Observability, Security, Operability

- Observability: report harness, asset class, and status; redact or home-relativize paths in normal output where full paths are unnecessary.
- Security: reject path traversal, relative overrides, NUL-like invalid values, and normalized destinations outside the active home.
- Operability: preflight prints or returns a reviewable inventory before Feature 4 mutates scratch or live homes.
- Rollback: resolution is read-only and needs no rollback; callers preserve the inventory used for any later mutation.

## F. Test Plan

- Add a platform/harness/override matrix in the proposed consolidated phase test file.
- Update propagation tests where CLI arguments or result records expose resolved destinations.
- Use injected homes and platform identifiers; do not mutate live environment variables globally across concurrent tests.
- Native Windows junction behavior may be runner-constrained on non-Windows hosts and must be separately recorded.

### Top 5 High-Value Test Cases

1. **Given** no overrides on macOS/Linux, **when** destinations resolve, **then** every target remains beneath the injected active home.
2. **Given** documented Claude, Codex, and OpenCode overrides, **when** destinations resolve, **then** only the owning harness asset classes relocate.
3. **Given** a WSL environment, **when** resolution runs, **then** Linux-home destinations are returned and Windows-profile paths are absent.
4. **Given** a relative or outside-home override, **when** preflight resolves it, **then** it fails before any mutation.
5. **Given** a destination leaf that is a repository link and a parent that escapes through a symlink, **when** records are built, **then** the leaf remains classifiable and the parent escape is rejected.

## Stage 1: Harness Destination Contracts
**Goal**: Define complete source-to-destination records for all supported asset classes.
**Success Criteria**: AC1–AC4 pass roster and override tests.
**Status**: Not Started

## Stage 2: Platform Isolation
**Goal**: Resolve safe defaults for macOS, Linux, native Windows, and WSL.
**Success Criteria**: AC5–AC7 pass the platform matrix and rejection tests.
**Status**: Not Started

## Stage 3: Reconciliation Handoff
**Goal**: Provide normalized records that preserve link classification and parent safety.
**Success Criteria**: AC8 passes shared scratch-path tests with Feature 4.
**Status**: Not Started

## Unverified Assumptions

- Exact documented OpenCode skill override behavior must be verified from the repository's current platform guides before implementation; no new variable may be inferred.
- The generated `codex/profiles/` outputs do not yet have a verified one-to-one mapping to the documented Codex runtime `prompts/` destination; resolve this explicitly before freezing the deployable roster and do not silently rename or omit either concrete class.
