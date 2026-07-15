# Implementation Record: WebFetch Exfiltration Guard

## Summary

Implemented a bounded, standard-library-only URL exfiltration analyzer shared by direct `WebFetch` handling and literal `curl`/`wget` operands. Known credential formats and credential-named encoded values deny, ambiguous high-entropy values ask, bypass mode escalates according to configuration, ordinary URLs pass, and all decisions/audit records remain redacted. The existing PreToolUse entrypoint now selects by action strength and configured priority without changing the `BashMatch` tuple contract.

## Sibling Features

- `05-injection-scanner` executes in the same wave with a disjoint source and fixture scope.
- The shared hook framework/package files owned by that sibling were not modified by this feature.
- `07-multi-harness-integration` consumes this guard's completed hook wiring later in the phase.

## AC Coverage Matrix

| AC | Criterion ID | Planned Test ID | Planned Test Pattern | Status | Implementing Files | Evidence Paths | Implement Commit SHA | Review Commit SHA |
|----|--------------|-----------------|----------------------|--------|--------------------|----------------|----------------------|-------------------|
| AC1 | AC1 | `test_phase02_recorded_webfetch_payloads_use_verified_url_field_and_posture` | Replay recorded PreToolUse payloads using exact `WebFetch` and `tool_input.url` fields | Complete | `.github/hooks/scripts/file-access-guard.py`, `.github/hooks/file-access-guard.json` | `tests/hooks/fixtures/url_exfiltration/recorded_payloads.json`, `tests/hooks/test_file_access_guard.py` | PENDING | PENDING |
| AC2 | AC2 | `test_phase02_curl_and_wget_literal_urls_reuse_known_secret_denial` | Direct and Bash consumers call one module-local `analyze_url` API | Complete | `.github/hooks/lib/url_exfiltration.py`, `.github/hooks/lib/bash_analyzer.py`, `.github/hooks/scripts/file-access-guard.py` | `tests/hooks/test_bash_command_analyzer.py`, `tests/hooks/test_file_access_guard.py` | PENDING | PENDING |
| AC3 | AC3 | `test_phase02_url_analyzer_classifies_secret_and_ambiguous_segments` | AWS-style key, token, private-key header, and encoded credential deny cases | Complete | `.github/hooks/lib/url_exfiltration.py`, `.github/hooks/config/file-access-rules.json` | `tests/hooks/test_file_access_guard.py` | PENDING | PENDING |
| AC4 | AC4 | `test_phase02_bash_ambiguous_url_asks`, `test_phase02_webfetch_bypass_escalates_ambiguous_url_to_deny` | Ambiguous base64/hex asks in both consumers and escalates in bypass | Complete | `.github/hooks/lib/url_exfiltration.py`, `.github/hooks/lib/bash_analyzer.py` | `tests/hooks/test_bash_command_analyzer.py`, `tests/hooks/test_file_access_guard.py` | PENDING | PENDING |
| AC5 | AC5 | `test_phase02_url_analyzer_allows_ordinary_url_material`, `test_phase02_ordinary_urls_and_literal_request_bodies_are_allowed` | Ordinary hosts, ports, fragments, percent encoding, UUID/hash assets, and request bodies pass | Complete | `.github/hooks/lib/url_exfiltration.py`, `.github/hooks/lib/bash_analyzer.py` | `tests/hooks/test_file_access_guard.py`, `tests/hooks/test_bash_command_analyzer.py` | PENDING | PENDING |
| AC6 | AC6 | `test_phase02_action_strength_then_priority_selects_deterministically` | Direct, quoted, option-reordered, redirected, and piped curl/wget URLs preserve strongest action and priority | Complete | `.github/hooks/lib/bash_analyzer.py`, `.github/hooks/scripts/file-access-guard.py` | `tests/hooks/fixtures/bash/commands.json`, `tests/hooks/test_bash_command_analyzer.py` | PENDING | PENDING |
| AC7 | AC7 | `test_phase02_url_configuration_is_validated_and_data_driven` | Validate rules, patterns, thresholds, action, guidance, priority, and escalation from JSON | Complete | `.github/hooks/config/file-access-rules.json`, `.github/hooks/lib/url_exfiltration.py` | `tests/hooks/test_file_access_guard.py` | PENDING | PENDING |
| AC8 | AC8 | `test_phase02_recorded_webfetch_payloads_use_verified_url_field_and_posture` | Missing/non-string/malformed inputs fail closed; dynamic syntax boundary is documented | Complete | `.github/hooks/lib/url_exfiltration.py`, `.github/hooks/scripts/file-access-guard.py`, `docs/hooks/bash-command-limitations.md` | `tests/hooks/fixtures/url_exfiltration/recorded_payloads.json`, `docs/hooks/bash-command-limitations.md` | PENDING | PENDING |
| AC9 | AC9 | `test_phase02_webfetch_decision_and_audit_are_fully_redacted`, `test_phase02_bash_url_bypass_and_audit_redaction` | Assert URL, host, query, path, command, and secret sentinels never reach decision or audit output | Complete | `.github/hooks/scripts/file-access-guard.py` | `tests/hooks/test_file_access_guard.py`, `tests/hooks/test_bash_command_analyzer.py` | PENDING | PENDING |

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | Cross-phase WebFetch obligation | Complete | `.github/hooks/scripts/file-access-guard.py`, `.github/hooks/file-access-guard.json` | Recorded fixture verifies `tool_input.url` and exact `WebFetch` matcher. |
| AC2 | Shared URL analyzer | Complete | `.github/hooks/lib/url_exfiltration.py`, `.github/hooks/lib/bash_analyzer.py` | One `analyze_url` classifier; package `lib.__all__` was not broadened. |
| AC3 | Known-secret denial | Complete | `.github/hooks/lib/url_exfiltration.py`, `.github/hooks/config/file-access-rules.json` | Credential regex and credential-named encoded shapes deny. |
| AC4 | Ambiguous entropy confirmation | Complete | `.github/hooks/lib/url_exfiltration.py` | Base64/high-entropy and query hex values ask; configured bypass escalates to deny. |
| AC5 | Ordinary URL pass-through | Complete | `.github/hooks/lib/url_exfiltration.py`, `.github/hooks/lib/bash_analyzer.py` | Negative corpus includes fragments, userinfo, IPv6, ports, encoding, UUIDs, hashes, and request bodies. |
| AC6 | Bash extension and priority | Complete | `.github/hooks/lib/bash_analyzer.py`, `.github/hooks/scripts/file-access-guard.py` | Literal URL extraction covers requested deterministic forms; selection is action then priority. |
| AC7 | Data-driven policy | Complete | `.github/hooks/config/file-access-rules.json` | Concrete patterns, thresholds, action, reason, alternative, priority, and escalation are configuration. |
| AC8 | Conservative parsing and failures | Complete | `.github/hooks/lib/url_exfiltration.py`, `docs/hooks/bash-command-limitations.md` | URL length/segments/decoding are bounded; malformed guarded inputs raise into the fail-closed framework. |
| AC9 | Redaction and measurable regression | Complete | `.github/hooks/scripts/file-access-guard.py`, mapped tests/fixtures | URL matches always record `offending_path=None`; full suite and coverage gate pass. |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `.github/hooks/lib/url_exfiltration.py` | Created | Added bounded URL parsing, policy validation, secret-shape matching, entropy analysis, bypass escalation, and redacted structured matches | Supply one reusable classifier for WebFetch, curl, and wget |
| `.github/hooks/lib/bash_analyzer.py` | Modified | Added configured literal curl/wget URL operand extraction and shared analyzer calls | Extend Bash coverage without shell execution or classifier duplication |
| `.github/hooks/scripts/file-access-guard.py` | Modified | Added WebFetch routing, structured match revalidation, action/priority selection, and URL-safe audit handling | Integrate direct WebFetch and deterministic cross-source decisions safely |
| `.github/hooks/config/file-access-rules.json` | Modified | Added URL limits, command/body-option metadata, credential formats, entropy gates, actions, guidance, priorities, and bypass posture | Keep concrete security policy out of engine code |
| `.github/hooks/file-access-guard.json` | Modified | Added exact `WebFetch` PreToolUse matcher while retaining timeout and existing tools | Activate direct WebFetch protection |
| `docs/hooks/bash-command-limitations.md` | Modified | Documented dynamic URL, runtime expansion, request-body, DNS, and redirect boundaries | State deterministic coverage limits and safer alternatives |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| `tests/hooks/test_file_access_guard.py` | Modified | Added analyzer, WebFetch fixture, failure, bypass, configuration, matcher, redaction, negative URL, and import-safety cases | AC1-AC5, AC7-AC9 |
| `tests/hooks/test_bash_command_analyzer.py` | Modified | Added curl/wget command forms, ordinary/body negatives, action/priority, bypass, and audit redaction cases | AC2, AC4-AC6, AC9 |
| `tests/hooks/fixtures/bash/commands.json` | Modified | Added covered curl/wget URLs and documented dynamic URL limitation | AC6, AC8, AC9 |
| `tests/hooks/fixtures/url_exfiltration/recorded_payloads.json` | Created | Added synthetic `.invalid` deny/ask/allow and malformed WebFetch payloads | AC1, AC3-AC5, AC8 |

## Test Results

- **Baseline**: 169 passed, 0 failed (focused Bash and file-access suites before implementation)
- **Final**: 202 passed, 0 failed (focused suites); 333 passed, 0 failed (full repository suite); combined coverage gate passed at 70.56% total
- **New tests added**: 33 collected focused cases
- **Regressions**: None

## Deviations from Plan

- Resolved the proposed module/API name as `.github/hooks/lib/url_exfiltration.py::analyze_url`.
- Preserved the five-field `BashMatch` public tuple instead of adding a priority field. The guard retrieves and validates priority by rule identifier from the immutable configuration immediately before final selection, proving same-action priority without breaking existing consumers.

## Gaps

- Disposable entrypoint behavior is covered with recorded `.invalid` payloads, but an actual interactive WebFetch runner invocation was NOT RUN because no live runner is available in the implementation environment.
- Dynamic shell URL construction remains intentionally unsupported and is documented under `LIMIT-DYNAMIC-URLS`.

## Reviewer Focus Areas

- `.github/hooks/lib/url_exfiltration.py` — confirm bounded decoding and entropy/encoded-shape thresholds avoid both secret leakage and ordinary hash false positives.
- `.github/hooks/lib/bash_analyzer.py::_url_candidates` — verify body-option skipping and literal URL boundaries across curl/wget forms.
- `.github/hooks/scripts/file-access-guard.py::_selection_key` — confirm revalidation and action-first/priority-second ordering preserve every existing path/Bash decision.
- Redaction paths — URL matches must continue to pass `offending_path=None` and generic configuration guidance only.
