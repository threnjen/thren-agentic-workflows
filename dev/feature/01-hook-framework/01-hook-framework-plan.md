# Feature 01: Hook Framework

## Execution Metadata

- **Wave:** 1
- **Parallel safe:** yes
- **Depends on:** none
- **Key files modified:** `.github/hooks/lib/__init__.py` `[PROPOSED - name TBD]`, `.github/hooks/lib/framework.py` `[PROPOSED - name TBD]`, `.github/hooks/scripts/audit-log.py`, `.github/hooks/scripts/audit-log.sh`, `tests/hooks/conftest.py` `[PROPOSED - name TBD]`, `tests/hooks/fixtures/` `[PROPOSED - name TBD]`, `tests/hooks/test_hook_framework.py` `[PROPOSED - name TBD]`, `docs/hooks/hook-verification.md` `[PROPOSED - name TBD]`
- **Sequential reason:** n/a

## A. Requirements & Traceability

### Acceptance Criteria

1. **AC1 — Payload contract:** A Python 3 stdlib framework parses recorded hook payloads for every Phase 01 tool in `Read|Edit|Write|MultiEdit|NotebookEdit|Grep|Bash`, normalizes the existing `tool_name`/`name`/`toolName` and `tool_input`/`input`/`toolInput` aliases, and preserves enough event context for later hooks.
2. **AC2 — Structured decisions:** The framework emits valid structured `allow`, `ask`, and `deny` decisions with a reason and supports the exit-code-2 blocking fallback described by the Phase document.
3. **AC3 — Layered configuration:** Repo defaults and a project override layer are loaded deterministically, with override precedence and an mtime-checked cache that does not retain stale changes.
4. **AC4 — Failure posture:** Security hooks can fail closed with a structured `guard error` denial, while the complete observability path—including wrapper, directory creation, serialization, and log writes—fails open without blocking the caller.
5. **AC5 — Human-only kill switch:** The fail-closed guard can be disabled only through the protected project override file; no environment-variable activation path is introduced.
6. **AC6 — Redacted observability:** Framework and audit output records tool name, fired rule, and offending path when applicable, but never records full tool inputs, file bodies, command bodies, or secret content.
7. **AC7 — Public framework contract:** The framework exposes a narrow reusable contract for payload parsing, configuration access, decision emission, failure handling, and redacted event recording; exact symbols remain `[PROPOSED - name TBD]` until implementation selects idiomatic names.
8. **AC8 — Test and premise evidence:** Recorded payload fixtures and tests cover normal, malformed, and exception paths, and a verification checklist records live evidence for deny/ask behavior in bypass mode and hook execution for subagent tool calls.
9. **AC9 — Runtime budget:** Hook framework tests measure median invocation overhead below 50 ms without subprocesses in the hot path or runtime pip dependencies.

### Non-Goals

- No secret, protected-path, Bash, destructive-command, or exfiltration rule content is implemented here.
- No propagation, generated global wiring, legacy-hook retirement, or installation-guide work is performed here.
- No environment-variable kill switch or fail-open security default is allowed.
- No code or patterns are copied from `docs/inspiration/` repositories.

### Traceability Matrix

| Acceptance Criteria | Code Areas/Modules | Test / Evidence Category |
|---|---|---|
| AC1 | `.github/hooks/lib/framework.py` `[PROPOSED - name TBD]`; recorded payload fixtures `[PROPOSED - name TBD]` | Must-have automated tests for every matcher tool and malformed payloads |
| AC2 | Shared decision emitter `[PROPOSED - name TBD]` | Must-have automated JSON-shape and fallback tests |
| AC3 | Shared config loader/cache `[PROPOSED - name TBD]` | Must-have automated precedence, cache-hit, and mtime-invalidation tests |
| AC4 | Shared failure wrapper `[PROPOSED - name TBD]`; `.github/hooks/scripts/audit-log.py`; `.github/hooks/scripts/audit-log.sh` | Must-have automated fail-closed and induced filesystem/log-write fail-open tests |
| AC5 | Project override contract `[PROPOSED - name TBD]` | Automated configuration test plus code-review evidence that no environment path exists |
| AC6 | Redacted event recorder `[PROPOSED - name TBD]`; `.github/hooks/scripts/audit-log.py` | Must-have automated secret-sentinel absence tests; existing audit script updated |
| AC7 | `.github/hooks/lib/` `[PROPOSED - name TBD]` | Code-review evidence plus downstream import tests in Features 02–03 |
| AC8 | `tests/hooks/` `[PROPOSED - name TBD]`; verification checklist `[PROPOSED - name TBD]` | Automated payload tests plus runner-constrained live Claude Code checks |
| AC9 | Framework benchmark test `[PROPOSED - name TBD]` | Must-have automated benchmark evidence |

### Phase Fidelity and Exceptions

- Key Deliverable 1 is preserved as the first feature.
- No Phase requirement is moved, renamed, reordered, or deferred.
- Exact new filenames and symbols are proposals; the Phase document specified only `.github/hooks/lib/ or equivalent`.

### Unverified Assumptions

- The final framework can remain compact enough for one primary module; implementation may split it if tests show a clear cohesion boundary.
- Live Claude Code checks can capture bypass and subagent behavior without becoming part of the automated suite.
- Pytest may be introduced as a development/test dependency while hook runtime code remains stdlib-only.
- A stable stdlib-only entrypoint/import strategy can make sibling framework modules available without relying on the caller's working directory or ambient `PYTHONPATH`.

## B. Correctness & Edge Cases

### Key Workflows

- Parse native and mapped payload shapes without silently dropping tool or event identity.
- Normalize the inconsistent aliases already used by `audit-log.py`, `protect-files.py`, and `bash-safety.sh` into one internal event representation.
- Resolve repo-default and project-override configuration in a stable order.
- Emit exactly one decision result per invocation.
- Record only redacted metadata, including on denied Write payloads that may contain secret content.
- Apply the configured failure posture when parsing, configuration, or hook logic raises.

### Failure Modes and Handling

- Malformed or empty stdin on a security hook produces a fail-closed `guard error` decision.
- Malformed or empty stdin on an observability hook exits successfully without blocking and without logging raw input.
- Directory creation, serialization, open, and log-write errors in the observability path are contained even though the current shell wrapper uses `set -euo pipefail`.
- Invalid configuration fails closed for security hooks and identifies the configuration problem without echoing its content.
- Cache invalidation must observe file mtime changes and cannot leak configuration across repositories.
- Duplicate invocations are safe; duplicate-message suppression is completed in Feature 04 integration.
- The kill switch is read only from the protected override channel and must not be inferred from process environment state.

## C. Consistency & Architecture Fit

### Existing Patterns to Follow

- Keep `.github/hooks/` as source of truth and executable scripts under `.github/hooks/scripts/`.
- Use Python 3 stdlib and JSON payloads, matching the current hooks.
- Preserve structured `hookSpecificOutput` decisions used by current `protect-files.py` and `bash-safety.sh`.
- Keep observability fail-open, matching the intent of `audit-log.json`, while removing its current raw `tool_input` summary.

### Contracts and Decisions

- The framework provides conceptual contracts for payload parsing, decision construction, configuration access, failure handling, and redacted event recording. Exact public symbol names are `[PROPOSED - name TBD]`.
- Hook entrypoints use an explicit stdlib-only import/package strategy that works when invoked directly from `.github/hooks/scripts/`; they do not rely on the repository cwd or ambient `PYTHONPATH`.
- Feature 02 must consume these contracts for path guard decisions and configuration.
- Feature 03 must reuse the same configuration and decision contracts rather than building a separate engine.
- The project override is the only human kill-switch channel; Feature 02 will add that file to self-protection rules.
- Configuration caching is scoped by resolved configuration paths and mtime, preventing cross-project contamination.

### Relationships to Sibling Plans

- `02-file-access-guard` depends on this feature's framework contract.
- `03-bash-command-analyzer` depends transitively on the same framework and must not duplicate it.
- `04-hook-distribution-integration` propagates and smoke-tests the completed framework and consumers.

## D. Clean Design & Maintainability

### Simplest Design

- Use small stdlib helpers behind one narrow import surface.
- Keep policy data outside Python; the framework knows how to load and evaluate configuration shape, not which files or commands are forbidden.
- Centralize decision JSON and redaction so downstream hooks cannot drift.
- Keep live-harness premise checks documented rather than pretending they are reproducible unit tests.

### Complexity and Duplication Risks

- Over-generalizing for later phases could create an unnecessary framework; implement only contracts required by Phase 01 and obvious per-hook failure posture reuse.
- Multiple decision emitters or log serializers would risk inconsistent security behavior.
- Caching global mutable configuration without repository scoping could produce unsafe cross-project state.

### Keep It Clean Checklist

- [ ] Runtime imports remain Python stdlib only.
- [ ] Rule content remains absent from framework code.
- [ ] No raw payload or command body reaches logs or exception messages.
- [ ] Public surface stays narrow and is covered by downstream contract tests.
- [ ] Proposed names are finalized and recorded in implementation notes.

## E. Completeness: Observability, Security, Operability

### Observability Decision

Preserve auditability but remove normal-path raw input logging. Record only a timestamp, tool name, rule identifier, decision, and normalized offending path when applicable. Do not add console logs to the hot path. A diagnosable framework failure may emit a redacted reason.

### Security

- Fail closed for security hooks and fail open only for explicitly designated observability hooks.
- Never place the kill switch in environment variables.
- Treat configuration paths and logged paths as untrusted input; avoid reflecting configuration bodies or file contents.
- Ensure denied Write payload bodies cannot appear in logs or test failure snapshots.

### Runbook

- Verify with the automated hook suite and benchmark.
- Run the live bypass/subagent checklist in a disposable checkout.
- Roll back by reverting this feature before consumers land; after Feature 02, use the documented protected override kill switch for human recovery.
- Monitor only failures and rule decisions with redacted metadata; avoid new normal-path noise.

## F. Test Plan

### Evidence Categories

- **Must-have automated tests:** Payload variants, decision JSON, config precedence/cache invalidation, security fail-closed, audit fail-open, redaction sentinels, and latency benchmark.
- **Existing tests to update:** None in this feature; `tests/test_propagate_master_assets.py` belongs to Feature 04.
- **Runner-constrained tests:** Live Claude Code bypass-mode deny/ask behavior and subagent hook execution.
- **Code-review evidence only:** Runtime dependency audit showing stdlib-only imports and absence of rule content.
- **Manual QA checks:** Verify one clear structured result and inspect generated logs for secret-sentinel absence.

### Top Five High-Value Checks

1. Given valid payload fixtures for every matcher tool, when parsed and re-emitted, then tool identity and relevant path/command fields remain available without logging their bodies.
2. Given malformed stdin, when a security hook wrapper runs, then it returns a redacted `guard error` denial; the observability wrapper does not block.
3. Given repo defaults and a changed project override, when the mtime changes, then the next load reflects the override without restarting the process.
4. Given a payload containing a unique secret sentinel in a Write body and Bash command, when decisions and logs are produced, then the sentinel is absent from every output and log.
5. Given repeated representative payloads, when benchmarked, then median framework overhead remains below 50 ms.

### Test Data and Fixtures

- Recorded payloads for `Read`, `Edit`, `Write`, `MultiEdit`, `NotebookEdit`, `Grep`, and `Bash`.
- Malformed JSON, missing fields, alternate key names, and induced exception fixtures.
- Temporary repo defaults and override files with controlled mtimes.
- Secret sentinel strings that must never appear in output.
- Live-harness checklist evidence for bypass and subagent behavior.

## Stage 0: Test Prerequisites
**Goal**: Establish baseline test coverage using `@z-test-writer`
**Success Criteria**: A pytest-capable developer test environment is documented; the current 2-test unittest baseline remains green; hook framework test scaffolding exists; coverage for framework scope is at least 50%; all tests pass
**Status**: Required before implementation begins

## Stage 1: Framework Contracts
**Goal**: Implement payload, decision, configuration, caching, and failure-posture contracts without rule content
**Success Criteria**: AC1–AC5 and AC7 pass automated contract tests
**Status**: Not Started

## Stage 2: Redacted Observability
**Goal**: Centralize safe event recording and migrate audit behavior away from raw tool input summaries
**Success Criteria**: AC6 passes sentinel-based tests and audit behavior remains fail-open
**Status**: Not Started

## Stage 3: Verification and Performance
**Goal**: Complete payload fixtures, premise evidence, and latency measurement
**Success Criteria**: AC8–AC9 are satisfied; automated tests pass and runner-constrained checks are documented with observed results
**Status**: Not Started
