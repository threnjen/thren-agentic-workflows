# Feature 05: WebFetch Exfiltration Guard Tasks

## Stage 1: Shared URL Analyzer

- [ ] Add `tests/hooks/fixtures/url_exfiltration/recorded_payloads.json` `[PROPOSED - name TBD]` with a verified WebFetch URL field and synthetic deny, ask, allow, missing-field, non-string, and malformed cases using reserved `.invalid` hosts. (AC1, AC3-AC5, AC8)
- [ ] Define and validate data-driven URL policy in `.github/hooks/config/file-access-rules.json`, including rule identifiers, known-secret formats, minimum length/character-class/entropy gates, action, reason, safe alternative, priority, and bypass escalation. (AC3, AC4, AC7)
- [ ] Create the shared analyzer module `[PROPOSED - name TBD]` with bounded path/query extraction, bounded percent decoding, deterministic malformed-input handling, and no network or subprocess capability. (AC2, AC3-AC5, AC8)
- [ ] Resolve the verified priority-contract delta: make same-action URL/Bash collisions honor configured priority without silently breaking existing `BashMatch` consumers, and validate every structured match again before it reaches decision selection. (AC2, AC7, AC8)
- [ ] Extend `tests/hooks/test_file_access_guard.py` with direct analyzer scenarios for known credential formats, ambiguous high-entropy/base64/hex segments, realistic UUID/hash/encoded negative URLs, repeated keys, fragments, ports, userinfo, IPv6, and malformed escapes. (AC2-AC5, AC7, AC8)
- [ ] Keep the analyzer module-local and import it directly; do not modify `.github/hooks/lib/__init__.py` or broaden the exact package public-contract assertion in `tests/hooks/test_hook_framework.py`. (AC2)

## Stage 2: WebFetch PreToolUse Integration

- [ ] Add exact `WebFetch` matching to `.github/hooks/file-access-guard.json` while preserving every existing tool matcher and timeout. (AC1)
- [ ] Extend `.github/hooks/scripts/file-access-guard.py` to extract only the fixture-verified WebFetch URL field, invoke the shared analyzer, combine results by action strength and validated priority, and fail closed on missing/non-string input or unsafe configuration. (AC1-AC5, AC7, AC8)
- [ ] Reuse `security_guard`, `make_decision`, and `record_event`; emit generic rule guidance and pass no URL-derived value as `offending_path` or any other audit field. (AC3, AC4, AC8, AC9)
- [ ] Add recorded-payload entrypoint tests for deny, ask, allow, bypass escalation, malformed URL/input/config, and exact hook wiring behavior. (AC1, AC3-AC5, AC7-AC9)
- [ ] Add sentinel assertions proving the full URL, host, query name/value, path segment, secret marker, and payload do not appear in stdout, stderr, decision reasons, or NDJSON audit records. (AC3, AC9)

## Stage 3: Bash URL Inspection

- [ ] Extend `.github/hooks/lib/bash_analyzer.py` to identify literal URL operands for configured `curl` and `wget` invocations in direct, option-reordered, quoted, redirected, and piped command forms without executing or expanding shell state. (AC2, AC6, AC8)
- [ ] Route every extracted Bash URL through the same shared analyzer used by WebFetch; do not duplicate known-secret, entropy, normalization, validation, or bypass logic. (AC2, AC4, AC6, AC7)
- [ ] Preserve existing protected-file upload and destructive-command matches, ensure a deny cannot be weakened by an ask, and keep curl literal request bodies outside URL-exfiltration classification. (AC5, AC6, AC9)
- [ ] Extend `tests/hooks/fixtures/bash/commands.json` with covered and limited URL vectors using the established fixture schema and explicit limitation identifiers for unsupported dynamic forms. (AC6, AC8, AC9)
- [ ] Extend `tests/hooks/test_bash_command_analyzer.py` with equivalent WebFetch/Bash deny and ask assertions, ordinary URL negatives, same-tier priority collisions, multi-match strongest-action behavior, bypass behavior, and command/audit redaction regressions. (AC2-AC6, AC9)

## Stage 4: Redaction and Boundary Verification

- [ ] Update `docs/hooks/bash-command-limitations.md` for aliases, variables, substitutions, runtime-expanded URLs, unsupported program options, malformed forms, and any newly accepted boundary, including reproduction, risk, boundary, and safer alternative. (AC6, AC8)
- [ ] Run focused URL, Bash, and file-access suites and resolve all regressions before running the full suite. (AC6, AC9)
- [ ] Run `uv run --with-requirements requirements-dev.txt pytest -q` and preserve the 252-test green baseline plus all new tests. (AC9)
- [ ] Run the documented combined coverage command and keep total coverage at or above 50%; record exact pass/fail and coverage evidence in the implementation record. (AC9)
- [ ] Review runtime imports and call paths to prove standard-library-only, network-free, subprocess-free analysis and one shared classifier for WebFetch, curl, and wget. (AC2, AC7, AC8)
- [ ] Perform disposable manual WebFetch checks with `.invalid` URLs for one deny, one ask, and one allow outcome; verify no sensitive sentinel reaches console or audit output, or record each runner-constrained check explicitly as NOT RUN. (AC1, AC3-AC5, AC9)
