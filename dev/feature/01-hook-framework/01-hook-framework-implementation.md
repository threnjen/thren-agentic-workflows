# Implementation Record: Hook Framework

## Summary

Implemented a Python 3 standard-library hook framework with normalized payloads,
structured decisions, layered immutable configuration caching, explicit security
and observability failure postures, a protected-override-only kill switch, and
allowlisted NDJSON event recording. Migrated the audit entrypoint away from raw
input summaries and added an isolated pytest/coverage setup, recorded payloads,
failure-path tests, a latency assertion, and the live-runner checklist.

## Sibling Features

- `02-file-access-guard` consumes the payload, configuration, decision, security,
  and redacted-recording contracts. It owns path normalization and file rules.
- `03-bash-command-analyzer` reuses the same contracts and owns Bash policy; no
  Bash rule content was added here.
- `04-hook-distribution-integration` owns propagation, generated wiring, legacy
  retirement, double-fire handling, and the final live/integration pass.
- Shared public runtime modules are `.github/hooks/lib/framework.py` and
  `.github/hooks/lib/__init__.py`.

## AC Coverage Matrix

| AC | Criterion ID | Planned Test ID | Planned Test Pattern | Status | Implementing Files | Evidence Paths | Implement Commit SHA | Review Commit SHA |
|----|--------------|-----------------|----------------------|--------|--------------------|----------------|----------------------|-------------------|
| AC1 | Payload contract | `test_recorded_payload_aliases_are_normalized`; `test_invalid_payloads_raise_payload_error` | Recorded aliases for seven tools plus malformed, empty, invalid UTF-8, and missing fields | Complete | `.github/hooks/lib/framework.py` | `tests/hooks/fixtures/recorded_payloads.json`; `tests/hooks/test_hook_framework.py` | PENDING | PENDING |
| AC2 | Structured decisions | `test_decision_emitter_writes_one_structured_result`; `test_denial_can_use_exit_code_two_fallback` | All three decisions, one JSON result, and exit-code-2 fallback | Complete | `.github/hooks/lib/framework.py` | `tests/hooks/test_hook_framework.py`; `docs/hooks/hook-verification.md` | PENDING | PENDING |
| AC3 | Layered configuration | `test_config_override_precedence_uses_recursive_merge`; `test_config_cache_hits_and_invalidates_on_mtime_change`; `test_config_cache_is_scoped_by_resolved_paths` | Precedence, cache hit, mtime refresh, isolation, missing and invalid files, immutable snapshots | Complete | `.github/hooks/lib/framework.py` | `tests/hooks/test_hook_framework.py` | PENDING | PENDING |
| AC4 | Failure posture | `test_security_guard_fails_closed_with_redacted_denial`; `test_observability_guard_fails_open_without_output`; `test_complete_audit_path_fails_open` | Payload/config/handler failures, output fallback, and audit directory/serialization/open/write failures | Complete | `.github/hooks/lib/framework.py`; `.github/hooks/scripts/audit-log.py` | `tests/hooks/test_hook_framework.py` | PENDING | PENDING |
| AC5 | Human-only kill switch | `test_only_project_override_can_disable_security_guard`; `test_disabled_security_guard_skips_handler_and_allows` | Defaults and environment cannot disable; protected override can | Complete | `.github/hooks/lib/framework.py` | `tests/hooks/test_hook_framework.py` | PENDING | PENDING |
| AC6 | Redacted observability | `test_redacted_event_record_contains_only_allowlisted_metadata`; `test_audit_script_records_redacted_ndjson_without_console_output` | Write/Bash/nested/config/response sentinels absent from streams and NDJSON | Complete | `.github/hooks/lib/framework.py`; `.github/hooks/scripts/audit-log.py` | `tests/hooks/test_hook_framework.py` | PENDING | PENDING |
| AC7 | Public framework contract | `test_public_framework_contract_is_exposed`; `test_framework_package_exposes_only_documented_public_contract`; `test_audit_entrypoint_imports_without_cwd_or_pythonpath` | Narrow exports and isolated direct-script import | Complete | `.github/hooks/lib/__init__.py`; `.github/hooks/lib/framework.py`; `.github/hooks/scripts/audit-log.py` | `tests/hooks/test_hook_framework.py` | PENDING | PENDING |
| AC8 | Test and premise evidence | `test_recorded_fixtures_cover_every_phase_one_tool_and_event_context`; `test_runner_constrained_verification_checklist_is_recorded` | Recorded payloads and automated malformed/exception posture; live checklist recorded | Partial | `tests/hooks/`; `docs/hooks/hook-verification.md` | `tests/hooks/fixtures/recorded_payloads.json`; `docs/hooks/hook-verification.md` | PENDING | PENDING |
| AC9 | Runtime budget | `test_median_framework_invocation_overhead_is_below_budget`; `test_framework_runtime_imports_are_stdlib_only_and_no_subprocess` | 1,000 direct invocations, median under 50 ms, stdlib-only import audit | Complete | `.github/hooks/lib/framework.py` | `tests/hooks/test_hook_framework.py`; coverage output recorded below | PENDING | PENDING |

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | Normalize recorded Phase 01 payload aliases and preserve event context. | Complete | `.github/hooks/lib/framework.py` | Covers all seven matcher tools and malformed variants. |
| AC2 | Emit structured allow/ask/deny decisions and support exit code 2. | Complete | `.github/hooks/lib/framework.py` | Every structured decision includes a reason and one output line. |
| AC3 | Load defaults and overrides with deterministic, mtime-current caching. | Complete | `.github/hooks/lib/framework.py` | Cache is path-scoped, locked, and returns immutable snapshots. |
| AC4 | Fail security closed and all observability operations open. | Complete | `.github/hooks/lib/framework.py`; `.github/hooks/scripts/audit-log.py` | Security output failure uses redacted exit-code-2 fallback. |
| AC5 | Restrict the kill switch to the protected project override. | Complete | `.github/hooks/lib/framework.py` | Contract is `guard.enabled: false` in the override only. |
| AC6 | Record diagnosable metadata without raw input or secret content. | Complete | `.github/hooks/lib/framework.py`; `.github/hooks/scripts/audit-log.py` | Audit schema is timestamp/tool/rule/decision plus optional path. |
| AC7 | Expose a narrow reusable stdlib-only public contract. | Complete | `.github/hooks/lib/__init__.py`; `.github/hooks/lib/framework.py` | Final public symbols are listed in `lib.__all__`. |
| AC8 | Supply fixtures/tests and observed live-runner premise evidence. | Partial | `tests/hooks/`; `docs/hooks/hook-verification.md` | Automated evidence passes; four external live checks remain `NOT RUN`. |
| AC9 | Keep median framework overhead below 50 ms without subprocess or pip runtime dependencies. | Complete | `.github/hooks/lib/framework.py` | Repeated direct-call benchmark and AST dependency audit pass. |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `.github/hooks/lib/framework.py` | Create | Payload, decision, config/cache, failure posture, kill switch, and redacted record contracts | Shared Phase 01 runtime foundation |
| `.github/hooks/lib/__init__.py` | Create | Narrow public re-export surface | Stable contract for sibling features |
| `.github/hooks/scripts/audit-log.py` | Modify | Import-safe `main`, shared parser/recorder, complete fail-open behavior | Remove raw `input_summary` and prevent audit failures from blocking |
| `pyproject.toml` | Create | Pytest discovery configuration | Establish the planned developer test runner |
| `requirements-dev.txt` | Create | Bounded pytest and pytest-cov development dependencies | Keep test tools separate from stdlib-only hook runtime |
| `.gitignore` | Modify | Ignore `.venv/` and `.coverage` | Keep developer test artifacts local |
| `docs/hooks/hook-verification.md` | Create | Automated evidence plus disposable live-runner checklist/status | Record runner-constrained premise checks honestly |
| `tests/hooks/README.md` | Create | Environment setup, pytest, coverage, and regression commands | Reproducible developer verification |
| `dev/feature/01-hook-framework/01-hook-framework-tasks.md` | Modify | Mark completed tasks while leaving live checks open | Keep plan execution status accurate |
| `dev/feature/01-hook-framework/01-hook-framework-implementation.md` | Create | Traceability, evidence, deviations, and gaps | Reviewer handoff artifact |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| `tests/hooks/conftest.py` | Create | Dynamic framework loader and recorded fixture loader | Framework test harness |
| `tests/hooks/fixtures/recorded_payloads.json` | Create | Payloads for Read/Edit/Write/MultiEdit/NotebookEdit/Grep/Bash and all observed alias families | AC1, AC8 |
| `tests/hooks/test_hook_framework.py` | Create | 47 collected framework, audit, failure, redaction, import, config, and benchmark cases | AC1–AC9 automated scope |

## Test Results
- **Baseline**: 2 passed, 0 failed via unittest; pytest unavailable before Stage 0 (`No module named pytest`)
- **Final**: 49 passed, 0 failed via full pytest; 47 hook tests passed at 93.89% framework coverage; 2 passed, 0 failed via legacy unittest
- **New tests added**: 47 collected hook-framework cases
- **Regressions**: None

Commands:

```text
/tmp/phase01-hook-tests-venv/bin/python -m pytest tests/
/tmp/phase01-hook-tests-venv/bin/python -m pytest tests/hooks/ --cov=.github/hooks/lib --cov-report=term-missing --cov-fail-under=50
python3 -m unittest discover -s tests -v
python3 -m compileall -q .github/hooks/lib .github/hooks/scripts/audit-log.py tests/hooks
git diff --check
```

## Deviations from Plan

- Stage 0 could establish the intended failing contract suite, but framework
  coverage could not exceed 50% before the planned framework module existed.
  Coverage reached 93.89% in the completed implementation.
- Finalized the proposed package as `.github/hooks/lib/` and the public symbols
  as `HookEvent`, `Decision`, `ConfigSnapshot`, `PayloadError`, `ConfigError`,
  `parse_payload`, `make_decision`, `emit_decision`, `load_config`,
  `security_guard`, `observability_guard`, and `record_event`.
- Live Claude Code execution was not launched because it requires an explicitly
  isolated external session. The checklist and `NOT RUN` evidence rows are
  present rather than claiming inferred success.

## Gaps

- Live `deny`, `ask`, and exit-code-2 behavior in bypass-permissions mode remains
  `NOT RUN`.
- Live PreToolUse execution initiated by a subagent remains `NOT RUN`.

## Reviewer Focus Areas

- `.github/hooks/lib/framework.py` configuration cache and recursive immutable
  merge — verify override precedence and the protected-only kill-switch contract.
- `.github/hooks/lib/framework.py` security output failure path — verify every
  exception produces a structured denial or redacted exit-code-2 fallback.
- `.github/hooks/scripts/audit-log.py` — graph tooling cannot infer the dynamic
  test link, but direct tests cover `main` and its nested audit callback across
  success, malformed, directory, serialization, open, and write paths.
- `docs/hooks/hook-verification.md` — confirm the four live checks remain gated
  and are completed during an isolated integration pass rather than assumed.
