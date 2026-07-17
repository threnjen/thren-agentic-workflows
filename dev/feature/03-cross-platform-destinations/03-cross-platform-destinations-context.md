# Feature Context: Cross-Platform Destinations

## Feature Boundary

This feature defines the read-only source-to-destination contract for user-global deployment. It converts the already-generated `claude/`, `codex/`, and `opencode/` asset rosters into normalized destination records for the current active user and current runtime environment. It does not copy, replace, classify ownership, or prune anything.

The resolver must run only after `02-propagation-convergence` verifies a repository fixed point. `04-managed-copy-reconciliation` consumes the records from this feature and owns all mutation and ownership decisions.

## Key Files and Modules

| Path | Status | Relevance |
|---|---|---|
| `scripts/propagate_master_assets.py` | Existing, verified | Current propagation entry point and generated-root roster. Integration must preserve `propagate_once`, `watch_loop`, and `main` behavior while adding the Feature 2 orchestration handoff. |
| `scripts/runtime_deployment.py` | `[PROPOSED - name TBD]` | Planned narrow home for platform classification, documented harness destination policy, source roster derivation, and normalized destination records. The implementer may choose a better repository-consistent name, but must update all references and tests together. |
| `tests/test_propagate_master_assets.py` | Existing, verified | Existing 42-test propagation suite. Update only where the propagator exposes the destination preflight or result records; retain existing containment and generated-output coverage. |
| `tests/test_phase04_runtime_deployment.py` | `[PROPOSED - name TBD]` | Proposed consolidated Phase 04 test file for the platform/harness/override matrix and cross-feature scratch-home behavior. |
| `docs/phases/PHASE_04/PHASE_04_SUMMARY.md` | Existing, verified; read-only input | Authoritative Phase requirements, ordering, destination behavior, and acceptance boundaries. |
| `docs/phases/PHASE_04/PHASE_04_DISCOVERY_CONTEXT.md` | Existing, verified; read-only input | Primary-documentation research and exact generated-root facts captured on 2026-07-16. |
| `claude/agents/`, `claude/commands/`, `claude/skills/`, `claude/learnings/` | Existing, verified; read-only sources | Claude generated asset classes eligible for destination records. Supporting hook deployment remains outside this feature. |
| `codex/agents/`, `codex/profiles/`, `codex/skills/`, `codex/instructions/` | Existing, verified; read-only sources | Codex generated outputs. The final deployable roster must follow the Phase document rather than assume every generated subtree has a documented runtime destination. |
| `opencode/agents/`, `opencode/skills/`, `opencode/instructions/` | Existing, verified; read-only sources | OpenCode generated outputs. Commands are documented runtime assets, but the repository currently has no generated `opencode/commands/` root; do not invent a source root without an explicit upstream propagation change. |

## Verified Existing Contracts

- `scripts/propagate_master_assets.py` uses `pathlib.Path`, dataclasses, injected `repo_root` parameters, and integer change-counter dictionaries.
- `propagate_once` emits all supported generated outputs before it prunes orphans and currently returns structured counters.
- The generated repository roots are exactly `claude/`, `codex/`, and `opencode/`; `.claude/` is not a generated root.
- Current emitted subtrees include Claude agents, commands, skills, instructions, and learnings; Codex agents, profiles, skills, and instructions; and OpenCode agents, skills, and instructions.
- Existing containment helpers protect repository-generation destinations, but no general user-global destination resolver or managed-copy deployment stage exists.
- `CLAUDE_CONFIG_DIR`, `CODEX_HOME`, and `OPENCODE_CONFIG_DIR` are copied exactly from the Phase document. No other relocation variable is authorized.

## Architectural Decisions

### One Resolver Contract

Choose one reusable destination-resolution API `[PROPOSED - name TBD]` rather than placing environment checks in copy loops. The API should accept injected repository root, active home, environment mapping, and platform facts, then return immutable or effectively immutable records. This keeps path policy testable without patching the author's real process environment.

Each record must carry enough information for Feature 4 to act without recomputing policy: harness, asset class, generated source root or file set, destination, active-home boundary, and any status needed for preflight reporting. Exact record and API names remain `[PROPOSED - name TBD]`.

### Current Environment Only

Classify each run as exactly one of macOS, Linux, native Windows, or WSL. WSL is Linux for destination purposes and uses the active distribution's Linux home. A run must never infer, enumerate, or mutate native Windows state from WSL, WSL state from Windows, another distribution, or another user's home.

### Documented Destination Policy

| Harness | Documented default | Documented override behavior |
|---|---|---|
| Claude | Active home plus `.claude`; agents under `agents/`, legacy commands under `commands/`, skills under `skills/` | `CLAUDE_CONFIG_DIR` relocates the Claude root. Repository-managed learning assets are included by the Phase contract. |
| Codex | Codex-owned agents and profiles/prompts beneath `${CODEX_HOME:-~/.codex}`; skills beneath the active-user shared `~/.agents/skills` root | `CODEX_HOME` relocates Codex-owned state only and, when custom, must already exist. It does not relocate the documented shared skill root. |
| OpenCode | Active home plus `.config/opencode`; agents under `agents/`, commands under `commands/`, skills under `skills/` or another documented shared skill root | `OPENCODE_CONFIG_DIR` covers documented config-owned asset classes, currently agents and commands. It is not documented as relocating skills. Do not infer `XDG_CONFIG_HOME` behavior. |

The implementer must reconcile the runtime-documentation roster with the generated source roster. A documented destination with no generated source is not permission to invent content, and a generated subtree without a documented runtime contract must not be silently deployed.

### Safe Normalization Without Leaf Dereference

Reject relative overrides, path traversal outside the active home, embedded NUL-like invalid values, and ambiguous cross-environment forms before any mutation. Normalization must not follow the destination leaf link, because Feature 4 needs to classify legacy symlinks and junctions as links. Parent-chain checks must still identify an escape through a symlinked or junction-based ancestor.

### Observability

Return or print a reviewable preflight inventory using the repository's structured-result style. Normal-path reporting should identify harness, asset class, and status while home-relativizing or redacting full paths where possible. Add no standalone per-file normal-path log unless a diagnosable failure mode requires it.

## Constraints and Edge Cases

- Resolve destinations without requiring a destination leaf to exist.
- Decide and test one consistent interpretation for an empty relocation variable. It may be treated as absent only if that matches the verified harness contract; otherwise fail preflight. Never resolve it relative to the repository.
- A custom `CODEX_HOME` must already exist per the Phase discovery research; default parents may be planned for creation by Feature 4.
- Keep native Windows path handling independent of POSIX string assumptions. Native Windows must use the active user profile without administrator privileges or Developer Mode.
- Keep WSL detection deterministic and mutually exclusive with native Windows classification.
- Never patch process-global environment variables in concurrently runnable tests; inject an environment mapping or use test cleanup that guarantees restoration.
- Never use the developer's live home for automated tests. Use temporary active-home and generated-root fixtures.
- Preserve the destination leaf for later link/junction ownership classification while validating all existing parents against the active-home boundary.
- Unsupported platform or cross-environment inputs fail before the mutation layer is invoked.

## Relationships to Sibling Plans

| Feature | Relationship |
|---|---|
| `01-interceptor-retirement` | Earlier independent retirement work; no resolver API dependency, but it changes the generated hook asset roster that must remain outside this deployment feature. |
| `02-propagation-convergence` | Runtime prerequisite. This feature is called only after the bounded fixed-point API `[PROPOSED - name TBD]` succeeds. Both features modify `scripts/propagate_master_assets.py`, `tests/test_propagate_master_assets.py`, and the proposed consolidated Phase 04 test, so execution is sequential. |
| `04-managed-copy-reconciliation` | Direct downstream consumer. It must use this feature's destination records and normalization results rather than recomputing paths. This feature does not determine ownership. |
| `05-deployment-guidance` | Documentation must later describe only the destination behavior actually implemented and verified here. |
| `06-runtime-verification` | Final integration verifies the destination contract in scratch homes and on available live platforms. |

## Environment State

| Property | Value |
|---|---|
| Tech Stack | Python 3.12.6; standard-library `pathlib`, `dataclasses`, `unittest`; Markdown/TOML generated assets |
| Host Captured | macOS Darwin arm64 on 2026-07-16 |
| Test Runner | `python3 -m unittest discover -s tests -v` |
| Focused Test Runner | `python3 -m unittest tests.test_propagate_master_assets` |
| Test Baseline | 42 passed, 0 failed in 2.197s for `tests.test_propagate_master_assets` — captured 2026-07-16 |
| Pytest Status | Declared in `requirements-dev.txt` and `pyproject.toml`, but unavailable in the active Python environment (`No module named pytest`) |
| Lint | Not configured |
| Format | Not configured |

Runner constraints: native Windows junction behavior and WSL-specific runtime discovery cannot be proven on the captured macOS host. Simulated path-policy unit tests are required here; real native Windows and WSL evidence belongs to Feature 6 and must be recorded as `NOT RUN` when unavailable.

## Relevant Learnings

### Generated-root and marker contracts

From `.github/learnings/cross-phase-decisions.md`:

- The generated roots are `claude/`, `opencode/`, and `codex/`; plans must not substitute `.claude/skills/` or `.claude/agents/` as repository sources.
- Generated Markdown and TOML assets carry type-specific ownership markers, and generated skills are not byte-identical to their `.github/skills/` sources because of the marker line.
- Long-running propagator watchers retain the code they started with and must be restarted after propagator changes.
- One propagation run does not prove convergence after an emission-class change; deployment must wait until all change counters reach zero.

### Destination containment

From `.github/learnings/review-learnings.md` and `.github/learnings/debugging-learnings.md`:

- Validate resolved source assets and resolved destination directories against declared roots before reading or writing.
- Checking or replacing only a symlinked leaf is insufficient; a symlinked parent can redirect writes or enumeration outside the intended boundary.
- Destructive enumeration must validate the containing root before walking it. Feature 3 supplies boundary-preserving records; Feature 4 owns the destructive checks.

### No unrelated retained-eval identity

`.github/learnings/project-learnings.md` contains no additional destination-resolution rule. Its retained-evaluation identity guidance is unrelated to this feature and should not influence the resolver design.

## Implementation Handoff Checklist

- Preserve every concrete destination variable and generated-root name from the Phase document.
- Keep all newly chosen symbols labeled or documented as proposed until implementation settles them.
- Keep resolution and inventory read-only.
- Keep platform/home/environment facts injectable.
- Preserve leaf-link classification and validate parent boundaries.
- Produce the downstream record contract required by Feature 4.
- Record simulated versus live-platform evidence distinctly.

