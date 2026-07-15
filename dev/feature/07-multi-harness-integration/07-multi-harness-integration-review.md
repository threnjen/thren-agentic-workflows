# Review Record: Multi-Harness Integration

## Summary

Reviewed implementation commit `26274e1` plus the 2026-07-15 user-sign-off
evidence against the feature plan, context, tasks, implementation record,
generated wiring, propagation code, runtime adapters, tests, and operations
documentation. Six in-scope issues were found and fixed. Claude now uses the
documented MCP-specific replacement field and preserves valid redacted output
shapes on post-parse failures; Codex `apply_patch` is actually selected by the
generated matcher; OpenCode translates native tool names and Read arguments
without copying scanner policy; and propagation rejects internal as well as
escaping intermediate symlinks before writes. Generated outputs are stable on
a second propagation pass.

The user's approvals close the Codex limitation and PERF-01 decision gates
without changing the evidence: Codex remains `Partial`, PERF-01 remains `FAIL`,
and all disposable live harness checks remain `NOT RUN`.

## Verdict

Approved with Reservations

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1 | Verified | `docs/hooks/prompt-injection-defense.md`; `docs/hooks/manual-qa.md` | Runner versions, evidence date, current contract sources, automated observations, and live boundaries are recorded. |
| AC2 | Verified with accepted limitation | `docs/hooks/installation.md`; `docs/hooks/manual-qa.md` | Claude and OpenCode have automated replacement evidence. Codex 0.144.4 remains Partial; the user accepted its narrower Bash/`apply_patch`/MCP coverage on 2026-07-15. |
| AC3 | Verified after fixes | `.github/hooks/lib/framework.py`; `.github/hooks/scripts/injection-scanner.py`; `scripts/propagate_master_assets.py` | Claude built-ins use `updatedToolOutput`, Claude MCP uses `updatedMCPToolOutput`, Codex uses native block feedback, and OpenCode mutates `output.output` after thin shape translation. |
| AC4 | Verified | `scripts/propagate_master_assets.py`; `tests/test_propagate_master_assets.py` | Detached consumers receive the complete scanner, corpus, allowlist, URL guard, adapters, source definitions, and stable marker. |
| AC5 | Verified | `scripts/propagate_master_assets.py`; generated `.claude`, `.codex`, and `.opencode` outputs | Existing preservation/stale-cleanup tests pass; repeated propagation reports zero changes and byte-stable generated outputs. |
| AC6 | Verified after fix | `scripts/propagate_master_assets.py`; `tests/test_propagate_master_assets.py`; `tests/hooks/test_hook_distribution_integration.py` | Fresh-consumer and self-protection checks pass. Internal `.github`/`.opencode` symlink redirects and the external nested-config redirect are rejected before mutation. |
| AC7 | Verified | `tests/hooks/test_hook_distribution_integration.py`; `tests/test_propagate_master_assets.py` | Combined propagated scanner/WebFetch/Bash smoke passes; Bun proves OpenCode block, warn, fail-closed validation, and native Read allowlist translation. |
| AC8 | Verified with reservations | `.github/hooks/lib/framework.py`; hook tests; `docs/hooks/manual-qa.md` | Redaction tests include structured failures and MCP dynamic structured-content keys. PERF-01 remains failed and live no-retry evidence remains NOT RUN. |
| AC9 | Verified after documentation correction | Hook operations docs and documentation assertions | Support labels, recovery, rollback, limitations, approvals, and live states are consistent. The stale OpenCode “promoting beyond Partial” live note was removed. |
| AC10 | Verified with accepted prerequisite risk | Propagation symlink regressions; fixed latency tests; sign-off evidence | SEC-01 is green for external and internal intermediate-directory redirects. PERF-01 remains red at the unchanged 50 ms threshold; proceeding was explicitly approved. |

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | Claude emitted `updatedToolOutput` for MCP results even though the current PostToolUse contract requires `updatedMCPToolOutput`; a high MCP match could therefore leave the original output model-visible. | High | `.github/hooks/lib/framework.py:252` | AC3, AC8 | Fixed during review |
| 2 | Config/handler failures after parsing a structured result emitted scalar `"guard error"`; Claude can reject a schema-mismatched replacement and retain the original output. | High | `.github/hooks/lib/framework.py:429` | AC3, AC8 | Fixed during review |
| 3 | Documentation claimed Codex `apply_patch` scanning, but the generated scanner matcher omitted the canonical `apply_patch` name and its `Write`/`Edit` matcher aliases. | Medium | `.github/hooks/injection-scanner.json:5` | AC2, AC3 | Fixed during review |
| 4 | OpenCode forwarded lowercase/native tool names and `Read.filePath` unchanged, so the shared scanner could not apply its repository-owned source allowlist on native Read calls. | Medium | `scripts/propagate_master_assets.py:805` | AC3, AC7 | Fixed during review |
| 5 | Output-root checks rejected escaping redirects and final-directory symlinks but allowed an intermediate symlink such as `.github` or `.opencode` when it resolved elsewhere inside the consumer root. | High | `scripts/propagate_master_assets.py:1058` | AC6, AC10 | Fixed during review |
| 6 | Manual QA still said OpenCode needed promotion beyond Partial while the support matrix classified it fully supported by automated contract evidence. | Low | `docs/hooks/manual-qa.md:56` | AC9 | Fixed during review |

## Fixes Applied

| File | What Changed | Issue # |
|------|--------------|---------|
| `.github/hooks/lib/framework.py`; `.github/hooks/lib/__init__.py` | Added shared shape-preserving redaction, canonical MCP redaction, MCP-specific emission, and structured fail-closed replacement after payload parsing. | 1, 2 |
| `.github/hooks/scripts/injection-scanner.py` | Reused the shared redaction helper instead of maintaining a second implementation. | 1, 2 |
| `.github/hooks/injection-scanner.json`; generated Claude/Codex wiring | Added canonical `apply_patch` matcher coverage and regenerated the distribution marker. | 3 |
| `scripts/propagate_master_assets.py`; generated OpenCode plugin | Added native OpenCode tool-name/Read-argument translation only; all normalization, patterns, severity, scanning, and allowlist policy remain in the shared Python runtime. | 4 |
| `scripts/propagate_master_assets.py` | Applied nested-directory validation to every hook/settings/plugin output root before any propagation write. | 5 |
| Hook tests and propagation tests | Added MCP field/redaction, structured-failure, Codex matcher, OpenCode allowlist/no-policy-duplication, and internal symlink regressions. | 1–5 |
| `docs/hooks/manual-qa.md`; `docs/hooks/prompt-injection-defense.md` | Documented built-in versus MCP replacement fields and reconciled OpenCode automated/live status. | 1, 6 |

## Harness Parity and Support Evidence

| Harness | Reviewed evidence | Disposition |
|---------|-------------------|-------------|
| Claude Code 2.1.210 | Current official hooks contract states top-level `decision: block` alone does not hide original output; `updatedToolOutput` replaces built-in output and `updatedMCPToolOutput` replaces MCP output before model context. Both payload paths and redaction are now tested. | Fully supported by automated contract evidence; live UI/no-retry remains NOT RUN. |
| Codex 0.144.4 | Tagged runtime source opts Bash, `apply_patch`, and MCP handlers into PostToolUse and replaces model-visible output with hook feedback. The generated matcher now selects all three. Other phase tools remain outside Codex handler coverage. | Partial; narrower coverage explicitly accepted by the user on 2026-07-15. |
| OpenCode 1.16.2 / Bun 1.3.14 | Plugin types expose mutable `tool.execute.after` output. Bun proves high replacement, warning append, malformed-result fail-closed behavior, and native Read allowlisting. The JS adapter contains translation/validation only and no pattern, severity, URL, or scanning policy. | Fully supported by automated contract evidence; live OpenCode remains NOT RUN. |
| Cursor / GitHub Copilot | No adapter or parity claim was added. | Not supported. |

## SEC-01 and PERF-01 Disposition

- **SEC-01: PASS.** External `.github/hooks/config` redirects and internal
  intermediate `.github`/`.opencode` redirects are rejected before writes.
  Final-file replacement, output-root containment, user-entry preservation,
  stale cleanup, and repeated-propagation idempotence remain green.
- **PERF-01: FAIL, risk accepted.** The fixed 50 ms propagated-guard test
  reproduced a 135.42 ms median in the final full run. The threshold was not
  changed. The user's 2026-07-15 approval permits proceeding but does not turn
  the failed prerequisite into a pass.

## Live Evidence

- Disposable live Claude high suppression, warning pass-through, no-retry,
  Task/subagent, MCP, and kill-switch/UI checks: **NOT RUN**.
- Disposable live Codex Bash/`apply_patch`/MCP replacement checks: **NOT RUN**.
- Disposable live OpenCode replacement/warning checks: **NOT RUN**.
- Automated payload, detached-consumer, and Bun results are not represented as
  live observations anywhere in the reviewed documentation.

## Test Coverage Assessment

- Focused framework/scanner/propagation suite: `126 passed`, plus `2` symlink
  subtests.
- Full functional suite with only the two fixed timing assertions deselected:
  `382 passed, 2 deselected`, plus `2` symlink subtests.
- Full suite with timing assertions enforced: `383 passed, 1 failed`, plus `2`
  symlink subtests. The sole failure is PERF-01 at a 135.42 ms median versus
  50 ms; the representative corpus timing test passed.
- Combined coverage with the timing assertions deselected: `71.42%`, above the
  required 50% gate.
- Stdlib unittest discovery: `19 passed`.
- Corpus benchmark: `19` true positives, `0` misses, `0` false positives, and
  `0` high-tier false positives.
- Two consecutive propagation passes ended with zero generated changes on the
  second pass. `git diff --check` passed.

## Remaining Concerns

- The three live runner sessions are still required before automated contract
  evidence can be promoted to observed UI/no-retry evidence.
- Codex does not expose the phase's complete successful-output tool set. The
  accepted limitation remains a real coverage gap and the support label remains
  `Partial`.
- PERF-01 remains an inherited Phase 01 release risk despite the approval to
  proceed.
- A malformed PostToolUse payload that cannot be parsed provides no trustworthy
  tool name or output schema to the hook. The framework emits redacted blocking
  feedback, but schema-specific replacement can only be guaranteed after a
  valid event is normalized.

## Risk Summary

- Claude replacement behavior now follows the current documented contract for
  both built-in and MCP tools, and structured/dynamic MCP content is removed
  from replacement objects.
- Codex claims match its tagged 0.144.4 handler set and generated matcher. The
  explicit user approval records the missing-tool risk without overstating
  parity.
- OpenCode policy remains centralized: the generated plugin maps runner shapes,
  invokes the shared scanner, validates its small result contract, and mutates
  output; it contains no detection or severity policy.
- Propagation validates destination components before copy, retirement,
  settings, marker, or plugin writes and remains idempotent while preserving
  untagged/user-owned entries.
- Automated evidence supports approval with reservations; the live NOT RUN
  rows and unresolved fixed latency failure prevent an unqualified approval.
