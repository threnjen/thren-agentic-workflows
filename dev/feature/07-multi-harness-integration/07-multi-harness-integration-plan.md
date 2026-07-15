# Feature 07: Multi-Harness Integration

## Execution Metadata

- **Wave:** 3
- **Parallel safe:** no
- **Depends on:** `05-injection-scanner`, `05-webfetch-exfiltration-guard`, `06-injection-pattern-corpus`
- **Key files modified:** `scripts/propagate_master_assets.py`, `tests/test_propagate_master_assets.py`, `tests/hooks/test_hook_distribution_integration.py`, `tests/hooks/README.md` `(verify)`, `.github/hooks/.distribution-version`, `.github/hooks/injection-scanner.json` `[PROPOSED - name TBD]` `(verify)`, `.github/hooks/scripts/injection-scanner.py` `[PROPOSED - name TBD]` `(verify)`, `.github/hooks/config/file-access-rules.json` `(verify)`, `.claude/settings.json`, `.codex/hooks.json`, `.opencode/plugins/injection-scanner.js` `[PROPOSED - name TBD]`, `.opencode/plugins/file-access-guard.js` `(verify)`, harness adapter files `[PROPOSED - name TBD]`, `docs/hooks/installation.md`, `docs/hooks/manual-qa.md`, `docs/hooks/hook-verification.md`, `docs/hooks/prompt-injection-defense.md` `[PROPOSED - name TBD]`
- **Sequential reason:** shares `.github/hooks/injection-scanner.json` and `.github/hooks/scripts/injection-scanner.py` with upstream `05-injection-scanner`, and may share `.github/hooks/config/file-access-rules.json` with upstream `05-webfetch-exfiltration-guard`

## A. Requirements & Traceability

### Acceptance Criteria

1. **AC1 — Time-boxed contract investigation:** Current primary documentation and direct safe experiments determine whether Codex and OpenCode expose post-tool-output events and can suppress, replace, or annotate output before model context; runner version, date, method, and evidence are recorded.
2. **AC2 — Exhaustive harness outcome:** Claude Code, Codex, and OpenCode each end in exactly one Phase-approved state: passing equivalent block/warn enforcement, or a written evidence-backed platform limitation with explicit user sign-off; no unsupported parity claim or unresolved third state remains.
3. **AC3 — Equivalent enforcement where supported:** A capable harness receives the same successful-output tool coverage, strongest-match selection, high suppression, medium/low warning, truncation notice, failure posture, and redaction semantics as the Claude Code source contract.
4. **AC4 — Complete artifact propagation:** Verified `propagate_hooks_once` emits the scanner entrypoint, framework/scanner modules, pattern corpus, allowlist, WebFetch/Bash guard updates, source wiring, adapters, and updated version marker to a fresh consuming project.
5. **AC5 — Generated wiring integrity:** `.claude/settings.json`, `.codex/hooks.json`, and generated OpenCode plugins preserve unrelated untagged entries, remove stale generated entries, reference only emitted assets, and remain idempotent under re-propagation.
6. **AC6 — Fresh consumer and self-protection:** A temporary consumer operates without the source repository or pip setup, and every propagated scanner/corpus/allowlist/wiring asset is denied to agent writes by the Phase 01 guard while normal read-only inspection and configured allowlisting still work.
7. **AC7 — Combined integration smoke:** One automated smoke flow proves scanner high block, warn pass-through, truncation notice, allowlist behavior, WebFetch known-secret deny, ambiguous-entropy ask, ordinary URL allow, and Bash curl/wget parity in the propagated consumer.
8. **AC8 — Redaction, latency, and retry evidence:** Automated evidence confirms secret/prompt sentinels are absent from stdout, stderr, audit output, and generated warnings; representative scanner/guard invocation timing follows the Phase 01 budget approach; live Claude QA records block suppression, warning, and no-retry behavior.
9. **AC9 — Operations and honest support docs:** Installation, verification, manual QA, recovery, rollback, known regex/shell/failed-output limits, and Claude/Codex/OpenCode support classifications are updated; Cursor and GitHub Copilot remain Not supported, and the stale test-baseline count in `tests/hooks/README.md` is corrected if documentation review confirms it no longer describes a historical-only state.
10. **AC10 — Phase prerequisite gate:** Before propagation changes build on Phase 01 distribution, SEC-01 nested-destination containment—including symlinked intermediate runtime/config/settings/plugin directories—and PERF-01 latency stability are reproduced or reviewed; any still-open blocker is explicitly recorded and either resolved in its Phase 01 owning scope or accepted as a documented prerequisite risk rather than silently inherited.

### Non-Goals

- No Cursor or GitHub Copilot implementation is added.
- No vendor extension/plugin platform is built to manufacture a hook contract that the harness does not expose.
- No direct prompt injection, semantic detection, PostToolUseFailure, or Phase 03 edit-backup work is introduced.
- No Phase 01 release blocker is silently re-scoped into this feature; only the minimum integration correction may be made with documented ownership.
- No user sign-off is fabricated or inferred from automated evidence.

### Traceability Matrix

| Acceptance Criteria | Code Areas/Modules | Planned Tests / Evidence |
|---|---|---|
| AC1 | Harness investigation notes in docs `[PROPOSED - name TBD]` | Primary-source citations and versioned safe experiment record |
| AC2 | Support matrix and sign-off record | Exact three-harness state assertion plus explicit user decision evidence for limitations |
| AC3 | Source wiring/adapters `[PROPOSED - name TBD]`; generated harness files | Per-harness block/warn/truncation/redaction tests where contracts permit |
| AC4 | Verified `scripts/propagate_master_assets.py::propagate_hooks_once` | Extended `tests/test_propagate_master_assets.py` artifact/version tests |
| AC5 | Verified `_update_nested_settings_file`, `_render_opencode_plugin`, generated outputs | Preservation, stale cleanup, command-target, and idempotence tests |
| AC6 | Temporary consumer and existing self-protection policy | Expanded distribution integration self-protection/fresh-clone tests |
| AC7 | Existing `tests/hooks/test_hook_distribution_integration.py` | New Phase 02 consolidated propagated smoke scenarios |
| AC8 | Framework audit/redaction contracts and manual QA doc | Sentinel-absence, timing, live block/warn/no-retry evidence |
| AC9 | Existing hook docs, `tests/hooks/README.md` `(verify)`, plus prompt-injection defense doc `[PROPOSED - name TBD]` | Documentation review, fresh-baseline comparison, and exact support-classification tests |
| AC10 | Phase 01 QA/security/performance evidence and `tests/test_propagate_master_assets.py` | Prerequisite audit plus adversarial intermediate-directory symlink and fixed latency evidence before propagation implementation |

### Phase Fidelity and Exceptions

- Key Deliverable 4 remains final and is the required integration/bootstrap feature that makes Features 05–06 runnable together in consumers.
- Key Deliverable 3 executes in Wave 1 before Key Deliverable 2's Wave 2 implementation because WebFetch has no scanner dependency and is file-disjoint; the manifest carries the required ordering note.
- The Phase-approved limitation-plus-sign-off outcome is preserved exactly and is not reworded as parity.
- SEC-01/PERF-01 remain Phase 01-owned; AC10 makes their prerequisite status explicit without expanding Phase 02 scope.
- No Phase requirement is deferred or renamed.

### Unverified Assumptions

- Codex and OpenCode post-output interception/suppression capabilities remain deliberately unverified until Stage 1.
- Harness-specific adapter filenames and any source metadata changes are `[PROPOSED - name TBD]`.
- The existing generic PostToolUse event mapping in `scripts/propagate_master_assets.py` may map event names but not equivalent output-rewrite semantics; event presence alone is not parity evidence.
- Current Phase 01 evidence is contradictory for SEC-01/PERF-01, and existing propagation tests cover output-root/final-file symlinks but not every symlinked intermediate destination directory.

## B. Correctness & Edge Cases

### Key Workflows

- Investigate each harness before modifying adapters, then choose supported enforcement or evidenced limitation/sign-off.
- Propagate all Phase 02 source assets into a temporary consumer and regenerate each supported harness output.
- Run the combined scanner, WebFetch, and Bash smoke corpus against the propagated copy rather than source-tree imports.
- Preserve unrelated settings and make repeated propagation byte-stable.

### Failure Modes and Handling

- A nominal post-tool event that runs after model ingestion does not qualify as equivalent interception.
- A harness that can warn but not suppress must be classified partial/limited and requires explicit sign-off.
- Propagation fails if generated commands reference missing/escaping assets or if source/config/adapters are omitted.
- Generated wrappers must forward runner payloads correctly and must not pipe secret-bearing content through shell arguments or logs.
- An open Phase 01 containment/latency blocker is surfaced before deployment claims, not discovered after propagation.

## C. Consistency & Architecture Fit

### Existing Patterns to Follow

- Extend verified `propagate_hooks_once`, `_resolve_hook_events`, `_resolve_hook_command`, `_update_nested_settings_file`, `_render_opencode_plugin`, source tags, complete asset copying, and distribution hashing.
- Treat `.github/hooks/` as source of truth and `.claude`, `.codex`, and `.opencode` as generated outputs.
- Reuse the existing temporary-consumer distribution test and redacted manual evidence conventions.

### Contracts and Decisions

- The downstream integration calls upstream behavior through the scanner entrypoint/config contract from `05-injection-scanner` + `06-injection-pattern-corpus` and the file-access entrypoint from `05-webfetch-exfiltration-guard`.
- If a capable harness needs a translation adapter, the adapter translates payload/response shapes only and reuses upstream normalization, validation, generation, and scanning APIs; no policy duplication is allowed.
- If no upstream call is possible because a harness lacks interception, independence is intentional and documented as a platform limitation rather than simulated protection.
- Generated wiring changes are produced from source metadata and propagation, not hand-maintained as separate policy.

### Relationships to Sibling Plans

- Depends on all three earlier features and runs last.
- May touch scanner source metadata/entrypoint and WebFetch config after real harness discovery, so it is conservatively sequential and its discovery deltas must be reconciled with upstream acceptance criteria.
- Owns phase-level propagation, combined smoke coverage, harness evidence, documentation, and user sign-off capture.

## D. Clean Design & Maintainability

### Simplest Design

- Use existing generic propagation for asset copying and source-tagged generated wiring.
- Add only thin harness translation where current contracts prove it necessary.
- Extend the existing distribution integration module as the phase-level consolidated test asset instead of creating a parallel Phase02 test directory.

### Complexity and Duplication Risks

- Similar event names can mask different timing/response semantics; require behavioral evidence.
- Platform adapters can fork policy; limit them to shape translation and call shared upstream APIs.
- Generated files can drift when edited directly; regenerate and test source tags/idempotence.
- Sign-off can become an informal note; record an explicit status/evidence row.

### Keep It Clean Checklist

- [ ] Event existence is not treated as suppression evidence.
- [ ] Adapters contain no injection or secret policy.
- [ ] Fresh-consumer tests use propagated assets only.
- [ ] Generated files preserve unrelated entries and are idempotent.
- [ ] Every harness has exactly one honest supported/limited outcome.

## E. Completeness: Observability, Security, Operability

### Observability Decision

Do not add normal-path runtime logs. Investigation and QA artifacts record versions, commands, timestamps, redacted outcomes, counts, and timings. Runtime records remain allowlisted metadata only and exclude tool output, matched text, URLs, commands, and secrets.

### Security

- Safe experiments use disposable repositories, reserved hosts, and synthetic sentinels.
- Propagated configs, corpora, entrypoints, adapters, and wiring remain self-protected.
- A weaker harness is classified honestly and requires explicit risk acceptance.
- Recovery uses the human-only override outside the guarded session and a reviewed re-propagation.

### Runbook

- Audit Phase 01 prerequisite status, then run upstream feature suites before propagation work.
- Generate a fresh consumer, inspect generated diffs/commands, and run the combined automated smoke.
- Execute live Claude block/warn/no-retry/kill-switch checks and supported Codex/OpenCode checks in disposable sessions.
- Record limitations/sign-off, then verify rollback by restoring prior source assets and re-propagating.

## F. Test Plan

### Evidence Categories

- **Existing tests updated:** `tests/test_propagate_master_assets.py` and `tests/hooks/test_hook_distribution_integration.py`.
- **Required new tests:** Generated scanner/adapters, complete asset/version propagation, settings preservation, phase-level smoke, and self-protection.
- **Runner-constrained tests:** Real pre-context suppression/annotation behavior, Task/MCP coverage, retry behavior, and kill-switch recovery per harness.
- **Code-review evidence:** Honest support matrix, no policy duplication, no missing assets, no unredacted output, and prerequisite audit.
- **Manual QA:** Claude real block/warn/no-retry; supported Codex/OpenCode equivalent checks or explicit limitation sign-off.

### Top Five High-Value Checks

1. Given a clean temporary consumer, when propagation runs, then every scanner/corpus/allowlist/WebFetch/adaptor dependency and version marker is emitted and all commands resolve inside the consumer.
2. Given unrelated settings plus stale generated entries, when propagation runs twice, then unrelated entries remain, stale generated entries disappear, and the second run is byte-stable.
3. Given the propagated consumer, when the Phase 02 smoke corpus runs, then scanner block/warn/truncation/allowlist and WebFetch/Bash deny/ask/allow outcomes all match upstream behavior.
4. Given secret and prompt sentinels, when every automated and supported live path runs, then no sentinel appears in outputs/logs/warnings and timing evidence is recorded.
5. Given each harness, when contract evidence is reviewed, then it has passing equivalent enforcement or an evidence-backed limitation with explicit user sign-off—never an inferred third state.

### Test Data and Fixtures

- Temporary source/consumer repositories with tagged and untagged settings and stale generated artifacts.
- Selected harmless high/warn/truncation scanner fixtures and WebFetch/Bash deny/ask/allow fixtures.
- Synthetic secret/prompt sentinels checked across stdout, stderr, audit, docs, and generated files.
- Harness evidence template capturing runner/version/date/command/event timing/response/sign-off.

## Stage 1: Harness Contract Investigation
**Goal**: Establish current Codex/OpenCode output-interception and response semantics with primary evidence and safe experiments
**Success Criteria**: AC1–AC2 have a recorded outcome path for each harness before adapter implementation begins
**Status**: Not Started

## Stage 2: Harness Adapters and Source Wiring
**Goal**: Implement only supported payload/response translations while reusing upstream APIs and recording limitations for unsupported contracts
**Success Criteria**: AC2–AC3 pass supported-harness tests or have evidence-backed limitation entries awaiting explicit sign-off
**Status**: Not Started

## Stage 3: Propagation and Generated Outputs
**Goal**: Emit every Phase 02 artifact and coherent source-tagged wiring to fresh consumers
**Success Criteria**: AC4–AC6 and AC10 pass propagation, preservation, self-protection, prerequisite, and idempotence checks
**Status**: Not Started

## Stage 4: Combined Smoke and Security Evidence
**Goal**: Verify scanner, corpus, WebFetch, Bash, redaction, latency, and retry behavior together in propagated environments
**Success Criteria**: AC7–AC8 pass automated evidence and required live checks are recorded or explicitly remain NOT RUN
**Status**: Not Started

## Stage 5: Operations, Limitations, and Sign-Off
**Goal**: Publish accurate support, installation, recovery, rollback, and residual-risk guidance
**Success Criteria**: AC2 and AC9 are complete, including explicit user sign-off for every evidenced platform limitation
**Status**: Not Started
