# Feature 04: Hook Distribution Integration

## Execution Metadata

- **Wave:** 4
- **Parallel safe:** yes
- **Depends on:** `01-hook-framework`, `02-file-access-guard`, `03-bash-command-analyzer`
- **Key files modified:** `scripts/propagate_master_assets.py`, `tests/test_propagate_master_assets.py`, `scripts/setup-hook-symlinks.sh`, `.gitignore`, generated-global output path `[PROPOSED - name TBD]`, `.github/hooks/bash-safety.json`, `.github/hooks/protect-files.json`, `.github/hooks/scripts/bash-safety.sh`, `.github/hooks/scripts/protect-files.sh`, `.github/hooks/scripts/protect-files.py`, `.claude/settings.json`, `.codex/hooks.json`, `.opencode/plugins/bash-safety.js`, `.opencode/plugins/protect-files.js`, `.opencode/plugins/file-access-guard.js` `[PROPOSED - name TBD]`, `tests/hooks/test_hook_distribution_integration.py` `[PROPOSED - name TBD]`, `docs/hooks/installation.md` `[PROPOSED - name TBD]`, `docs/hooks/manual-qa.md` `[PROPOSED - name TBD]`
- **Sequential reason:** n/a

## A. Requirements & Traceability

### Acceptance Criteria

1. **AC1 — Per-project artifact propagation:** The existing hooks stage in `scripts/propagate_master_assets.py` gains the smallest compatible target-root/testability seam and emits the completed guard scripts, framework modules, rule/default and override configuration, and relative-path wiring into consuming projects with a version marker.
2. **AC2 — Fresh-clone operation:** A consuming project produced by propagation contains everything required for the Claude Code guard to operate after clone without manual installation or a pip/venv step.
3. **AC3 — Generated global setup:** The superseding user-global setup flow generates absolute-path user-scope wiring for supported harnesses, leaves machine-specific output local and gitignored, and does not rely on the current broken relative-command symlink model.
4. **AC4 — Legacy consolidation:** Only after Feature 03's regression matrix passes, legacy `bash-safety` and `protect-files` definitions/scripts are retired from source wiring and generated outputs without losing any current block or intentional ask behavior.
5. **AC5 — Harness outputs:** Propagation regenerates coherent Claude Code, Codex, and OpenCode outputs from the single guard source, removes stale generated legacy plugins/entries, and preserves unrelated untagged hook wiring.
6. **AC6 — Double-fire tolerance:** With per-project and generated-global layers both active, allow/ask/deny behavior is functionally idempotent and one blocked call yields a clear, non-conflicting outcome with duplicate deny messaging suppressed where practical.
7. **AC7 — Installation guide:** A user-facing guide covers Claude Code, OpenCode, Codex, Cursor, and GitHub Copilot with current support classified as fully supported, partial, or not supported and a reason; uncertain Cursor/Copilot capability is researched during implementation rather than assumed.
8. **AC8 — Verified installation path:** The Claude Code instructions are followed verbatim in a clean checkout/temporary consuming project and the observed result is recorded; the guide also documents kill-switch recovery and re-propagation.
9. **AC9 — Integration verification:** An end-to-end smoke test launches the propagated guard, exercises representative file-tool and Bash allow/ask/deny paths, confirms self-protection and redacted logs, and measures the combined median hook latency below 50 ms.
10. **AC10 — Change communication and rollback:** Documentation records the intentional env-rule re-tiering, improved deny messages, known Bash limitations, generated-global behavior, upgrade/re-propagation steps, and a safe rollback/recovery procedure.

### Non-Goals

- No propagation emission for Cursor or GitHub Copilot is added beyond what their verified current mechanisms support; the guide must state limitations honestly.
- No plugin package distribution target is introduced.
- No Windows support is tested.
- No new guard policy or parser scope is introduced except integration fixes required to make accepted upstream behavior operate together.
- No inspiration repository code or patterns are copied.

### Traceability Matrix

| Acceptance Criteria | Code Areas/Modules | Test / Evidence Category |
|---|---|---|
| AC1 | `scripts/propagate_master_assets.py`; source guard/framework artifacts | New must-have hook-propagation and target-root tests in existing `tests/test_propagate_master_assets.py` (the file currently has no hook coverage) |
| AC2 | Temporary consuming-project fixture `[PROPOSED - name TBD]` | Must-have integration test plus clean-clone manual evidence |
| AC3 | `scripts/setup-hook-symlinks.sh`; `.gitignore`; generated wiring `[PROPOSED - name TBD]` | Must-have path-generation tests where practical; manual user-scope verification |
| AC4 | Legacy hook definitions/scripts and generated entries | Existing regression evidence from Feature 03 plus code-review deletion audit |
| AC5 | `.claude/settings.json`, `.codex/hooks.json`, `.opencode/plugins/`; propagation helpers | Must-have generated-output and preservation tests |
| AC6 | Guard/framework integration and deployment fixtures | Must-have double-invocation test; manual live double-fire check |
| AC7 | `docs/hooks/installation.md` `[PROPOSED - name TBD]` | Current official-documentation research evidence plus documentation review |
| AC8 | Installation and manual QA docs `[PROPOSED - name TBD]` | Manual clean-checkout checklist with recorded result |
| AC9 | Distribution integration test `[PROPOSED - name TBD]` | Must-have automated smoke/latency tests plus live harness checks |
| AC10 | Installation, QA, limitations, and migration documentation | Code-review evidence and manual rollback walkthrough |

### Phase Fidelity and Exceptions

- Key Deliverable 4 remains fourth and serves as the final integration/bootstrap feature required by the feature-plan-set rules.
- Propagation emission remains limited to Claude/Codex/OpenCode exactly as specified; Cursor/Copilot are documentation/research targets.
- The existing propagation stage is extended, not rebuilt.
- No Phase requirement is renamed, reordered, moved, or deferred.

### Unverified Assumptions

- Current Codex and OpenCode hook schemas generated by the repository remain valid at implementation time and may require official-doc verification.
- Cursor or GitHub Copilot may lack a PreToolUse-equivalent; the guide must report the verified result without expanding the Phase into extension development.
- Duplicate-message suppression can be achieved without persisting secret-bearing request data.

## B. Correctness & Edge Cases

### Key Workflows

- Discover source hook metadata and copy its dependent scripts/modules/config rather than wiring only the entrypoint.
- Generate platform wiring while preserving untagged user entries and deleting only stale generated outputs.
- Create absolute-path global wiring without committing machine-specific paths.
- Validate a temporary consuming project as if freshly cloned.
- Retire legacy definitions only after regression and integration gates pass.

### Failure Modes and Handling

- Propagation cannot produce wiring that references files it did not emit.
- Re-running propagation must be idempotent and update the version marker when source assets change.
- Existing untagged settings entries remain untouched; `$source`-tagged stale entries are removed deterministically.
- Global generation must preserve or safely back up existing user configuration rather than blindly overwrite it.
- If a harness lacks equivalent blocking semantics, documentation must not call it fully supported.
- Double firing must not create contradictory `ask`/`deny` outcomes or duplicate content-bearing logs.
- Rollback must not require an agent to edit a self-protected file from inside the guarded session.

## C. Consistency & Architecture Fit

### Existing Patterns to Follow

- Extend `propagate_hooks_once`, `_update_nested_settings_file`, `_render_opencode_plugin`, `$source` tagging, and event mapping in `scripts/propagate_master_assets.py` rather than creating a parallel propagator.
- Continue treating `.github/hooks/` as source of truth and `.claude`, `.codex`, and `.opencode` as generated outputs.
- Preserve the current `tests/test_propagate_master_assets.py` unittest baseline while adding pytest-compatible tests.

### Contracts and Decisions

- Upstream guard assets form one deployable unit: entrypoint, shared framework, analyzer, default rules, and project override contract.
- Feature 04 calls upstream behavior through the completed guard entrypoint and does not invent another public API.
- Generated global wiring uses absolute paths, while per-project wiring uses repository-relative paths.
- Version-marker format and duplicate-suppression mechanism are `[PROPOSED - name TBD]` until implementation verifies the narrowest compatible design.
- The hook propagator receives a narrow target-root/dependency seam, following the existing `propagate_skills_once` testability pattern where practical, so tests never monkeypatch the developer's real output paths.
- Legacy deletion is gated on automated parity, not merely file replacement.

### Relationships to Sibling Plans

- Depends on all three upstream features and executes last.
- Consumes Feature 01's framework, Feature 02's path guard/self-protection, and Feature 03's Bash analyzer/parity evidence.
- Owns all generated outputs, legacy retirement, installation docs, and cross-feature smoke verification.
- No upstream source file is expected to be modified; any necessary upstream integration correction must be recorded as a discovery delta and sequencing risk before implementation.

## D. Clean Design & Maintainability

### Simplest Design

- Teach the existing propagation stage to copy declared hook dependencies alongside generated wiring.
- Replace the symlink installer with generated absolute-path wiring using existing per-platform shapes.
- Keep documentation beside hook-specific docs under one proposed `docs/hooks/` area.
- Use one temporary consuming-project fixture for propagation and end-to-end checks.

### Complexity and Duplication Risks

- Platform-specific handling can diverge; retain shared source metadata and small translation adapters.
- Machine-specific global files can accidentally be committed; enforce gitignore and tests for path locality.
- Legacy and new hooks firing together can produce duplicate decisions during transition; make the migration atomic at generated-output level.
- Documentation can overstate platform support; require current primary-source verification.

### Keep It Clean Checklist

- [ ] Existing propagation helpers are extended rather than duplicated.
- [ ] Propagated wiring references only emitted files.
- [ ] Machine-specific absolute paths remain uncommitted.
- [ ] Legacy files are removed only after parity passes.
- [ ] Support claims are backed by current official documentation or direct verification.

## E. Completeness: Observability, Security, Operability

### Observability Decision

Do not add propagation or guard normal-path telemetry. The setup/propagation CLI may report changed artifact counts and verification failures. Double-fire tests must prove that audit/deny output remains redacted and understandable without logging raw payloads.

### Security

- Propagated guard assets, wiring, and override files must all be covered by upstream self-protection rules.
- Generated global configuration may contain absolute local paths but no secrets and must remain local/gitignored.
- Preserve deny guarantees in per-project Claude Code deployment; clearly classify weaker harnesses.
- Installation instructions must not recommend bypassing protection through agent-editable files.

### Runbook

- Run upstream suites, legacy parity, propagation tests, and consuming-project smoke tests in order.
- Re-propagate from source after upgrades and verify generated diffs contain no absolute paths in committed outputs.
- Validate the Claude Code guide in a clean checkout and record bypass/ask/double-fire observations.
- Recover via the human-only override outside an agent session; rollback by restoring the prior source definitions and rerunning propagation.

## F. Test Plan

### Evidence Categories

- **Must-have automated tests:** Artifact copying, relative wiring, source tags, stale-output cleanup, untagged-entry preservation, idempotence, fresh-project smoke, double invocation, and combined latency.
- **Existing tests to update:** `tests/test_propagate_master_assets.py` is the existing test module but has no current hook assertions; add entirely new hook propagation, target-root, and generated-output coverage while keeping its two current tests green.
- **Runner-constrained tests:** Live Claude Code clean-checkout installation, bypass deny/ask behavior, subagent execution, and global+project double-fire.
- **Code-review evidence only:** Legacy deletion gate, no committed absolute paths, and accurate harness support citations.
- **Manual QA checks:** Five-harness guide review, kill-switch recovery, re-propagation, rollback, and message clarity.

### Top Five High-Value Checks

1. Given a temporary consuming project, when hook propagation runs, then all guard dependencies and relative wiring are emitted and work without the source repository or pip setup.
2. Given existing untagged settings plus stale generated legacy entries, when propagation reruns, then untagged settings remain and stale generated entries/plugins disappear.
3. Given global generation from this repository, when setup completes, then user-scope wiring contains absolute paths, local output is gitignored, and committed project outputs contain no machine-specific path.
4. Given both deployment layers active, when one allow, ask, and deny payload is replayed, then outcomes are consistent, redacted, idempotent, and not confusingly duplicated.
5. Given the installation guide in a clean checkout, when followed verbatim for Claude Code, then the guard blocks a representative protected access and the recorded support table matches verified harness capabilities.

### Test Data and Fixtures

- Temporary source and consuming repositories with tagged and untagged settings.
- Complete guard dependency tree and stale legacy generated files.
- Representative file-tool/Bash allow, ask, and deny payloads from upstream fixtures.
- Temporary HOME/user-config directory for generated-global tests.
- Manual QA evidence template for harness support and clean-checkout verification.

## Stage 0: Test Prerequisites
**Goal**: Establish baseline test coverage using `@z-test-writer`
**Success Criteria**: Features 01–03 suites and legacy parity are green; propagation integration scaffolding exists; the two existing unittest tests still pass; coverage for this feature is at least 50%; all tests pass
**Status**: Required before implementation begins

## Stage 1: Per-Project Propagation
**Goal**: Add a narrow target-root test seam and extend the existing hooks stage to emit the complete guard unit with relative wiring and a version marker
**Success Criteria**: AC1–AC2 and AC5 pass automated propagation and fresh-project tests
**Status**: Not Started

## Stage 2: Global Setup and Consolidation
**Goal**: Generate absolute user-global wiring and atomically retire legacy hooks after parity
**Success Criteria**: AC3–AC4 pass automated and manual safety gates; no committed machine-specific paths remain
**Status**: Not Started

## Stage 3: Cross-Feature Integration
**Goal**: Verify the complete guard under propagated, double-fire, and representative allow/ask/deny scenarios
**Success Criteria**: AC6 and AC9 pass smoke, redaction, idempotence, and latency checks
**Status**: Not Started

## Stage 4: Installation and Operations Guide
**Goal**: Publish verified multi-harness installation, migration, recovery, and rollback guidance
**Success Criteria**: AC7–AC8 and AC10 are satisfied with a recorded clean-checkout Claude Code walkthrough and honest support classifications
**Status**: Not Started
