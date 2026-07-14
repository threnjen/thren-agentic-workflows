# Feature 01: Hook Framework — Tasks

## Stage 0: Test Prerequisites

- [ ] Use `@z-test-writer` to establish a pytest-capable developer test environment without adding any runtime hook dependency, and document the exact setup and invocation command. (Prerequisite for AC1–AC9)
- [ ] Create the hook test scaffolding at the finalized equivalents of `tests/hooks/conftest.py`, `tests/hooks/fixtures/`, and `tests/hooks/test_hook_framework.py` `[PROPOSED - name TBD]`; record final names in implementation notes. (AC8)
- [ ] Add initial contract tests that can measure framework-scope coverage and raise that coverage to at least 50% before implementation proceeds. (Stage 0 success criterion)
- [ ] Run `python3 -m unittest discover -s tests -v` and preserve the existing two passing propagation tests while the new pytest suite is introduced. (Regression baseline)
- [ ] Record the finalized pytest command, coverage command, Python version, and baseline results for downstream implementers and reviewers. (Stage 0 success criterion)

## Stage 1: Framework Contracts

- [ ] Finalize the narrow framework package/module and public symbol names proposed for `.github/hooks/lib/`, record the choices in implementation notes, and make the entrypoint/import strategy independent of caller working directory and ambient `PYTHONPATH`. (AC7)
- [ ] Implement payload parsing and normalization for `Read`, `Edit`, `Write`, `MultiEdit`, `NotebookEdit`, `Grep`, and `Bash`, preserving tool/event identity and needed path or command fields. (AC1)
- [ ] Support and test the existing alias families `tool_name`/`toolName`/`name`, `tool_input`/`toolInput`/`input`, plus standard `tool_input.command`; reject or classify empty, malformed, and missing-field payloads according to hook posture. (AC1, AC4)
- [ ] Implement one-result structured decision construction/emission for `allow`, `ask`, and `deny`, including reason handling and the exit-code-2 blocking fallback required by the phase. (AC2)
- [ ] Implement deterministic repo-default then project-override configuration loading with schema/error reporting that never reflects configuration content. (AC3, AC4)
- [ ] Implement a cache keyed by resolved configuration paths and mtimes; cover cache hits, mtime invalidation, repository isolation, missing files, and invalid configuration. (AC3)
- [ ] Implement explicit security and observability execution wrappers: security exceptions yield a redacted `guard error` denial, while observability exceptions exit successfully without blocking. (AC4)
- [ ] Implement the kill-switch contract so it is read only from the project override layer, and add code-review/test evidence that environment variables cannot activate it. (AC5)
- [ ] Add automated contract tests for every Stage 1 behavior, including exactly one output per invocation, valid decision JSON shape, exception paths, stale-cache prevention, and chosen public imports. (AC1–AC5, AC7)
- [ ] Audit the framework module to confirm it contains no file, secret, Bash, destructive-command, env-dump, or exfiltration rule content and imports only Python stdlib modules at runtime. (AC7; code-review evidence)

## Stage 2: Redacted Observability

- [ ] Implement the centralized redacted event recorder with an allowlist for timestamp, tool name, rule identifier, decision, and normalized offending path when applicable. (AC6)
- [ ] Migrate `.github/hooks/scripts/audit-log.py` away from `input_summary` and complete-payload serialization to the shared redacted recorder without adding normal-path console logging. (AC6)
- [ ] Ensure malformed payload, directory creation, serialization, file-open, and file-write failures are all consumed by the observability fail-open wrapper so `.github/hooks/scripts/audit-log.sh` cannot block through `set -euo pipefail`. (AC4, AC6)
- [ ] Add sentinel-based tests using Write bodies, Bash command bodies, nested payload data, configuration content, and induced exceptions; assert the sentinel is absent from stdout, stderr, log files, exception messages, and test snapshots. (AC6)
- [ ] Verify audit records still contain the required diagnosable metadata and are valid NDJSON without storing a full input or response body. (AC6)

## Stage 3: Verification and Performance

- [ ] Add recorded payload fixtures for every Phase 01 matcher tool and each observed alias shape, plus malformed JSON, empty stdin, missing fields, alternate keys, and induced exceptions. (AC8)
- [ ] Add end-to-end payload-level checks showing the security wrapper denies and the observability wrapper allows on equivalent malformed or exceptional inputs. (AC4, AC8)
- [ ] Create the finalized equivalent of `docs/hooks/hook-verification.md` `[PROPOSED - name TBD]` with disposable-checkout steps for live `deny` and `ask` behavior in bypass-permissions mode. (AC8; runner-constrained/manual evidence)
- [ ] Execute the live bypass-mode checklist and record observed results rather than assumptions, including the exit-code-2 fallback where the harness permits it. (AC2, AC8)
- [ ] Execute and record a live PreToolUse check initiated by a subagent tool call to verify hooks fire outside the main agent loop. (AC8; runner-constrained/manual evidence)
- [ ] Add a representative repeated-invocation benchmark that isolates framework overhead and asserts a median below 50 ms. (AC9)
- [ ] Verify the measured hot path starts no subprocess and requires no runtime pip dependency. (AC9; code-review and benchmark evidence)
- [ ] Run the full pytest suite and the existing unittest baseline; record all commands and passing results, and confirm framework-scope coverage remains at least 50%. (AC1–AC9)
- [ ] Inspect generated decisions and logs for one clear structured result, required redacted metadata, and complete secret-sentinel absence. (AC2, AC6, AC8; manual QA)
