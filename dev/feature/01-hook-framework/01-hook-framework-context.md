# Feature 01: Hook Framework — Context

## Key Files

### Files to Create or Modify

| File | Role | Change Type |
|------|------|-------------|
| `.github/hooks/lib/__init__.py` `[PROPOSED - name TBD]` | Narrow import surface for the shared hook framework | Create |
| `.github/hooks/lib/framework.py` `[PROPOSED - name TBD]` | Payload parsing, decision construction/emission, configuration loading and caching, failure posture, and redacted event recording | Create |
| `.github/hooks/scripts/audit-log.py` | Existing PostToolUse audit implementation that must stop retaining raw `tool_input` summaries and use the observability fail-open contract | Modify |
| `tests/hooks/conftest.py` `[PROPOSED - name TBD]` | Pytest hook harness and shared fixtures | Create |
| `tests/hooks/fixtures/` `[PROPOSED - name TBD]` | Recorded and synthetic payload fixtures for all Phase 01 matcher tools and error cases | Create |
| `tests/hooks/test_hook_framework.py` `[PROPOSED - name TBD]` | Automated framework contract, redaction, failure-posture, cache, and latency evidence | Create |
| `docs/hooks/hook-verification.md` `[PROPOSED - name TBD]` | Runner-constrained checklist and observed evidence for bypass-mode and subagent hook behavior | Create |

### Read-Only Reference Files

| File | Role | Change Type |
|------|------|-------------|
| `docs/phases/PHASE_01/PHASE_01_SUMMARY.md` | Authoritative Phase 01 requirements, failure posture, latency budget, premise checks, and clean-room boundary | Read-only reference |
| `.github/hooks/audit-log.json` | Existing PostToolUse command registration and fail-open intent | Read-only reference |
| `.github/hooks/bash-safety.json` | Existing structured `ask` decision registration and matcher convention | Read-only reference |
| `.github/hooks/protect-files.json` | Existing PreToolUse matcher and structured deny registration | Read-only reference |
| `.github/hooks/scripts/audit-log.sh` | Existing `set -euo pipefail` wrapper whose child exit status makes complete Python-side fail-open handling necessary | Read-only reference |
| `.github/hooks/scripts/bash-safety.sh` | Existing `allow`/`ask` `hookSpecificOutput` JSON shape and top-level/`input` payload handling | Read-only reference |
| `.github/hooks/scripts/protect-files.py` | Existing `tool_name`/`name` and `tool_input`/`input` aliases, fail-open behavior, and raw-command reflection to replace in later consumers | Read-only reference |
| `.github/hooks/scripts/protect-files.sh` | Existing Python wrapper and exit-code contract | Read-only reference |
| `tests/test_propagate_master_assets.py` | Current two-test unittest baseline; propagation changes remain Feature 04 scope | Read-only reference |

## Discovery Delta

| Finding | Impact | Action |
|---------|--------|--------|
| The proposed `.github/hooks/lib/`, `tests/hooks/`, and `docs/hooks/` paths do not exist; every concrete new path in the plan is correctly marked `[PROPOSED - name TBD]`. | The implementer must select and record idiomatic final names rather than treating proposals as fixed existing APIs. | Finalize names during implementation and record them in implementation notes; preserve the narrow public contract required by AC7. |
| Python 3.12.6 is available, but no `pyproject.toml`, pytest configuration, requirements manifest, lint config, or format config exists. `python3 -m pytest tests/` fails with `No module named pytest`. | Stage 0 is a real blocker, and the plan's pytest/coverage assumptions are not yet supported by the repository. | Establish and document a pytest-capable developer setup before framework implementation; keep runtime hook code stdlib-only. **Warning for Decomposer attention.** |
| `python3 -m unittest discover -s tests -v` passes the two existing propagation tests. No hook tests or phase-scoped test directory pattern exists. | There is no existing hook behavior safety net or consolidated Phase 01 test file to update. | Preserve the two-test baseline and create the proposed hook-focused pytest suite; no current-phase consolidated test omission was found. |
| Existing scripts accept different payload aliases: `audit-log.py` handles `tool_name`/`toolName` and `tool_input`/`toolInput`; `protect-files.py` handles `tool_name`/`name` and `tool_input`/`input`; `bash-safety.sh` looks for `input.command` or a top-level `command` and does not directly handle standard `tool_input.command`. | A parser that validates only one recorded shape can regress existing mapped harness inputs or retain the current Bash parsing gap. | Add explicit alias and standard-shape fixtures to AC1 tasks and define one normalized event representation. |
| `audit-log.py` currently writes a truncated JSON serialization of the complete `tool_input` into `input_summary`. | AC6 addresses an observed secret-retention defect, not merely a new feature. | Add sentinel tests against every emitted stream/file and replace the summary with allowlisted metadata only. |
| `audit-log.py` exits successfully for malformed JSON but open, directory-creation, serialization, or write errors can propagate through `audit-log.sh` because the wrapper uses `set -euo pipefail`. | The current observability path is not fully fail-open as required by AC4. | Add induced filesystem/log-write failure coverage and ensure the entire audit operation is contained by the observability failure posture. **Warning for Decomposer attention.** |
| Executing `.github/hooks/scripts/audit-log.py` directly places the `scripts/` directory, not `.github/hooks/`, on Python's default import path. | A sibling `lib` package is not automatically importable from the current entrypoint shape. | Choose and test an explicit stdlib-only import/entrypoint strategy; do not rely on the caller's working directory or ambient `PYTHONPATH`. **Warning for Decomposer attention.** |
| Existing hooks already emit `hookSpecificOutput` with `hookEventName: PreToolUse`, `permissionDecision`, and a reason for `ask`/`deny`; there are no existing automated assertions for that schema. | The planned structured decision contract fits the repository, but exact schema preservation needs new tests. | Treat existing scripts as read-only behavioral references and assert schema/one-result semantics in the framework suite. |
| The upstream AC7 explicitly requires a reusable public contract for Features 02–03, while leaving symbol names proposed. | The sibling dependency is represented in an upstream acceptance criterion as required. | No plan correction needed; add tasks to exercise the chosen public surface and document it. |

## Architectural Decisions

- Use Python 3 stdlib only in hook runtime code. Development-only test tooling may be added during Stage 0, but runtime execution must not require a virtual environment or pip install.
- Centralize payload normalization, decision serialization, configuration access, failure posture, and redacted event recording behind one narrow import surface. Do not implement secret, path, Bash, destructive-command, or exfiltration rules in this feature.
- Normalize the currently observed payload aliases into one event representation while retaining the tool identity and only the fields later consumers need.
- Prefer structured JSON decisions and support the Phase 01 exit-code-2 blocking fallback. Each invocation emits at most one result.
- Scope cached configuration by resolved configuration paths and mtimes. Repo defaults load first and project overrides take deterministic precedence; changes and repository switches must not reuse stale configuration.
- Make failure posture explicit per hook category: security hooks fail closed with a redacted `guard error` denial; observability hooks consume their own failures and do not block the caller.
- Read the human kill switch only from the project override contract. Do not add an environment-variable activation path.
- Record only allowlisted metadata: timestamp, tool name, rule identifier, decision, and normalized offending path when applicable. Never record full payloads, command bodies, file bodies, configuration bodies, or secret content.
- Keep live bypass-mode and subagent premise verification as runner-constrained evidence rather than representing it as an automated unit-test guarantee.

## Constraints

- `.github/hooks/` remains the source of truth and executable entrypoints remain under `.github/hooks/scripts/`.
- The framework must support `Read`, `Edit`, `Write`, `MultiEdit`, `NotebookEdit`, `Grep`, and `Bash` payloads required by Phase 01.
- Median framework invocation overhead must remain below 50 ms, with no subprocess in the hot path.
- The guard-facing failure default is fail closed; only explicitly observability-facing execution may fail open.
- The project override is the sole human kill-switch channel and will be self-protected by Feature 02.
- No raw tool input, command body, file body, configuration body, or secret sentinel may appear in decisions, logs, exception text, or test snapshots.
- Do not copy code or patterns from `docs/inspiration/`; those documents are requirements references only.
- Keep POSIX portability where practical, but Windows support and testing are outside this phase.
- The final public API and new filenames remain `[PROPOSED - name TBD]` until implementation records the selected idiomatic names.

## Scope Boundaries

- Do not add file, secret, protected-path, Bash, destructive-command, env-dump, or exfiltration rule content.
- Do not implement path normalization or guard policy evaluation owned by Features 02–03.
- Do not modify propagation, generated user-global wiring, legacy-hook retirement, duplicate-message suppression, or multi-harness installation guidance owned by Feature 04.
- Do not modify `tests/test_propagate_master_assets.py`; it is extended with propagation behavior in Feature 04.
- Do not guard Glob or WebFetch, add prompt-injection scanning, add pre-edit backup, or package the hooks as a plugin.
- Do not introduce an environment-variable kill switch or change security hooks to fail open.
- Do not broaden observability into normal-path console logging.

## Relationships to Sibling Plans

- `02-file-access-guard` directly depends on the payload, configuration, decision, failure, and redacted-event contracts established here. It also protects the project override that this feature recognizes as the kill-switch channel.
- `03-bash-command-analyzer` transitively depends on the same contracts and must reuse them instead of creating a second engine.
- `04-hook-distribution-integration` propagates and smoke-tests the framework and its consumers, handles duplicate messaging, retires legacy wiring, and updates propagation tests.

## Suggested Implementation Order

1. Complete Stage 0 and establish the pytest/coverage environment while retaining the current two-test unittest baseline.
2. Implement and test the narrow framework contracts without policy data.
3. Migrate audit recording to the redacted fail-open contract.
4. Complete recorded fixtures, live premise evidence, dependency audit, and latency verification.
5. Land this feature before `02-file-access-guard`; Features 03 and 04 follow their manifest dependencies.

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Python 3.12.6 hook/runtime scripts plus POSIX Bash wrappers; Python runtime is stdlib-only |
| Test Runner | Required target: `python3 -m pytest tests/` (currently unavailable); existing baseline: `python3 -m unittest discover -s tests -v` |
| Test Baseline | `unittest`: 2 passed, 0 failed; `pytest`: cannot start (`No module named pytest`) — captured 2026-07-14 |
| Lint | Not configured |
| Format | Not configured |

## Relevant Learnings

- `.github/learnings/cross-phase-decisions.md`: pre-edit backup was removed from Phase 01 and is a Phase 03 candidate; WebFetch exfiltration coverage is deferred to Phase 02; plugin packaging should wait until Hooks Phases 01–03 stabilize. Preserve these boundaries.
- No other learning entry matches this feature's Python hook-framework, configuration, redaction, or test-harness scope.
