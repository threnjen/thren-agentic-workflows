# Feature 05: Injection Scanner

## Execution Metadata

- **Wave:** 1
- **Parallel safe:** yes
- **Depends on:** none
- **Key files modified:** `.github/hooks/lib/framework.py`, `.github/hooks/lib/__init__.py`, `.github/hooks/lib/injection_scanner.py` `[PROPOSED - name TBD]`, `.github/hooks/scripts/injection-scanner.py` `[PROPOSED - name TBD]`, `.github/hooks/injection-scanner.json` `[PROPOSED - name TBD]`, `.github/hooks/config/injection-allowlist.json` `[PROPOSED - name TBD]`, `tests/hooks/test_hook_framework.py`, `tests/hooks/test_injection_scanner.py` `[PROPOSED - name TBD]`, `tests/hooks/fixtures/injection/post-tool-use-payloads.json` `[PROPOSED - name TBD]`
- **Sequential reason:** n/a

## A. Requirements & Traceability

### Acceptance Criteria

1. **AC1 — PostToolUse framework contract:** The Phase 01 framework accepts the Phase document's exact `tool_output`, `tool_output_truncated`, `agent_id`, and `agent_type` fields while preserving all verified PreToolUse payload aliases and behavior.
2. **AC2 — Deterministic normalization:** A scan copy passes through Unicode NFKC normalization, homoglyph folding, zero-width/invisible-character stripping, and bounded base64/hex candidate decoding without changing the raw tool output.
3. **AC3 — Data-driven rule contract:** The engine validates rules whose severity, response action, category, reason, matcher, and priority are configuration data; no injection phrase or severity policy is hard-coded in engine control flow.
4. **AC4 — Reusable scanner API:** The engine exposes a narrow rule-loading API and output-scanning API, both `[PROPOSED - name TBD]`, that Feature 06 can call with configuration and normalized tool context and that return structured match metadata without echoing matched content.
5. **AC5 — High-tier suppression:** A configured `high` rule can emit PostToolUse `decision: block`, suppress the original output, and provide a structured source/category/rule reason that says not to retry the same call and asks the user to inspect the source manually.
6. **AC6 — Warn-and-continue:** Configured `medium` and `low` rules preserve the byte-for-byte/raw logical output and append redacted `hookSpecificOutput.additionalContext` containing category, rule identifier, and recommended posture.
7. **AC7 — Protected allowlist:** A config-driven source-path allowlist bypasses only verified repository-owned corpus, fixtures, and `docs/inspiration/` paths; path normalization prevents traversal/symlink broadening, missing source paths do not silently qualify, and the existing `self-hook-assets` policy is tested to protect the allowlist and future corpus from agent writes.
8. **AC8 — Output boundaries:** Empty output takes a fast allow path; binary/non-UTF8 content does not crash and produces a notice; multiple matches select the strongest tier deterministically; scan-byte caps and `tool_output_truncated: true` scan available content and add a low-tier unscanned-tail notice.
9. **AC9 — Security failure posture:** Scanner parsing, configuration, normalization, matching, or emission failures block with the existing redacted `guard error` posture, while the verified project-only `guard.enabled` override restores operation.
10. **AC10 — Tool coverage and regression:** The hook covers successful `Read|Bash|Grep|WebFetch|WebSearch|Task` and `mcp__*` outputs, including serialized structured output and subagent results, while the existing 101 hook tests and PreToolUse decision contract remain green.

### Non-Goals

- No production pattern corpus is authored here; Feature 06 owns rule content and benchmark tuning.
- No direct user-prompt scanning, semantic/LLM detection, or PostToolUseFailure support is added.
- No Codex/OpenCode equivalence claim or generated propagation output is produced; Feature 07 owns that evidence and wiring.
- No matched injection string or raw tool output is written to audit logs or warning text.
- No copied pattern, regex, code, or fixture from the surveyed repository is permitted.

### Traceability Matrix

| Acceptance Criteria | Code Areas/Modules | Planned Tests / Evidence |
|---|---|---|
| AC1 | Verified `HookEvent`, `parse_payload`, and framework emitters in `.github/hooks/lib/framework.py` | Existing `tests/hooks/test_hook_framework.py` plus new PostToolUse payload scenarios |
| AC2 | Scanner normalization module `[PROPOSED - name TBD]` | New scanner tests for NFKC, homoglyph, zero-width, base64, hex, and raw-output preservation |
| AC3 | Rule validator/loader `[PROPOSED - name TBD]` | New temporary-config schema, invalid-config, and engine-policy-separation tests |
| AC4 | Scanner public exports in `.github/hooks/lib/__init__.py` | New public-contract tests consumed conceptually by Feature 06 |
| AC5 | PostToolUse emitter and scanner entrypoint `[PROPOSED - name TBD]` | New high-tier suppression/no-retry reason tests using synthetic rules |
| AC6 | PostToolUse warning emitter `[PROPOSED - name TBD]` | New medium/low intact-output and redacted-context tests |
| AC7 | Allowlist config/mechanics and verified `self-hook-assets` rule | New traversal/symlink/scope/self-protection tests in the scanner module |
| AC8 | Scanner boundary handling and Phase 02 payload fixtures | Empty, binary, multi-match, scan-cap, and truncated-output tests |
| AC9 | Verified `security_guard`, `load_config`, and project override behavior | Induced exception, invalid config, emitter failure, and kill-switch recovery tests |
| AC10 | `.github/hooks/injection-scanner.json` `[PROPOSED - name TBD]` and recorded payloads | Parameterized tool/MCP/Task/subagent/JSON coverage plus full regression suite |

### Phase Fidelity and Exceptions

- Key Deliverable 1 remains the first Phase 02 deliverable and retains the Phase document's exact payload and response field names.
- Pattern content is intentionally moved to Feature 06, matching the Phase document's engine/config separation; this feature provides the reusable API Feature 06 requires.
- Existing `self-hook-assets` already matches `**/.github/hooks/**`, so the corpus and allowlist join the protected set by inheritance plus explicit verification rather than duplicate policy.
- No Phase requirement is deferred or renamed.

### Unverified Assumptions

- The narrow scanner API names are not present in the codebase and remain `[PROPOSED - name TBD]` until implementation.
- Binary/non-UTF8 representation in live PostToolUse payloads may already be serialized by the runner; tests must cover both direct bytes at the engine seam and runner-shaped strings.
- The Phase document's `tool_output_truncated` field is accepted as verified Claude Code input, but its exact behavior for structured MCP output remains runner-constrained.

## B. Correctness & Edge Cases

### Key Workflows

- Parse a successful PostToolUse payload, derive a normalized scan copy, load validated rules, and select the strongest match.
- Emit exactly one block or warning response through the shared framework without exposing matched text.
- Resolve a source path conservatively before evaluating the allowlist.
- Preserve the intact output on warn/allow paths and suppress it only for configured block actions.

### Failure Modes and Handling

- Malformed payloads, invalid rule schema, unsafe regex, invalid allowlist entries, or output failures fail closed with redacted guidance.
- Equal-priority matches use a documented deterministic tie-breaker `[PROPOSED - name TBD]` and never depend on mapping iteration order.
- Encoded-candidate decoding is bounded by configured size/count limits to avoid decompression-style or regex denial of service.
- A truncated output can still block on a detected high rule; otherwise the tail notice is appended without claiming complete coverage.
- Allowlist resolution errors do not convert an untrusted source into an allowed source.

## C. Consistency & Architecture Fit

### Existing Patterns to Follow

- Extend verified `HookEvent`, `parse_payload`, `load_config`, `security_guard`, and redacted decision patterns instead of creating a second framework.
- Keep runtime imports standard-library-only and entrypoints independent of cwd/PYTHONPATH, matching `.github/hooks/scripts/file-access-guard.py`.
- Keep policy in JSON configuration and immutable snapshots, matching `file_access.py` and `bash_analyzer.py`.
- Preserve the 50 ms framework budget as the baseline performance target while separately measuring scanner workload.

### Contracts and Decisions

- The framework gains an event/output representation compatible with both existing PreToolUse handlers and new PostToolUse handling; the exact new type name is `[PROPOSED - name TBD]`.
- Feature 06 will call the scanner's validated rule loader and output-scanning API `[PROPOSED - name TBD]`; those APIs are explicit upstream deliverables of AC4.
- Response action is read from each rule. Severity participates in ordering/reporting but is not translated to an action by hard-coded engine policy.
- Normalization creates one or more bounded scan representations; warn responses return the original payload output, never a normalized copy.

### Relationships to Sibling Plans

- Runs in parallel with `05-webfetch-exfiltration-guard`; their conservative file scopes are disjoint.
- `06-injection-pattern-corpus` depends on AC3–AC4 and owns production rule content.
- `07-multi-harness-integration` consumes this entrypoint and may later adjust verified harness metadata or adapter wiring.

## D. Clean Design & Maintainability

### Simplest Design

- Add the smallest PostToolUse-compatible extension to the shared event/response model.
- Implement normalization, validation, and matching in one focused scanner module with a thin command entrypoint.
- Use synthetic temporary rules in engine tests so production corpus tuning remains isolated.

### Complexity and Duplication Risks

- Separate PreToolUse and PostToolUse emitters can drift; share validation and redaction helpers.
- Homoglyph/encoding logic can become unbounded; use explicit tables and bounded candidate extraction.
- Allowlist and file-access normalization can diverge; reuse verified path normalization where its contract fits.

### Keep It Clean Checklist

- [ ] No production injection phrases appear in engine code.
- [ ] Existing PreToolUse tests remain unchanged in meaning.
- [ ] Raw output and matched text never enter logs or warning reasons.
- [ ] New public exports are minimal and documented for Feature 06.
- [ ] Runtime remains standard-library-only and deterministic.

## E. Completeness: Observability, Security, Operability

### Observability Decision

Do not add a normal-path log line. Existing redacted event recording may record only tool, rule identifier, category, and decision if needed for a diagnosable block; it must never record tool output, matched text, URL content, or prompt-shaped warnings.

### Security

- High-tier output is suppressed, not rewritten with attacker-controlled content.
- Warning text uses fixed templates plus validated identifiers and minimally descriptive reasons.
- Regex and decoding work are bounded; invalid configuration fails closed.
- Corpus/allowlist/wiring assets remain under existing self-protection and the project-only kill switch.

### Runbook

- Run framework and scanner tests, then the complete hook suite and coverage gate from `tests/hooks/README.md`.
- Replay one synthetic block, warning, truncation, and failure payload without network or secrets.
- Roll back by disabling the scanner only through the verified human-managed project override, repairing config outside the guarded session, then restoring protection.

## F. Test Plan

### Evidence Categories

- **Existing tests updated:** `tests/hooks/test_hook_framework.py` for PostToolUse payload/response compatibility.
- **Required new tests:** Scanner normalization, rule schema, response, allowlist, boundary, performance, and entrypoint coverage in `tests/hooks/test_injection_scanner.py` `[PROPOSED - name TBD]`.
- **Runner-constrained tests:** Live Claude Code output suppression, warning attachment, Task/subagent output, and truncation behavior.
- **Code-review evidence:** No embedded production patterns, no raw-output logs, bounded regex/decoding, and standard-library imports.
- **Manual QA:** One real block, one real warn, no-retry behavior, and kill-switch recovery in a disposable session.

### Top Five High-Value Checks

1. Given a synthetic high rule and malicious successful tool output, when the scanner runs, then the output is suppressed and only a redacted no-retry block reason reaches the model.
2. Given medium/low matches, when the scanner runs, then the original output is intact and one fixed-shape warning is appended without matched text.
3. Given plain, homoglyph, zero-width, base64, and hex variants, when normalized and scanned, then equivalent content resolves to the same synthetic rule.
4. Given allowlisted, traversed, symlinked, missing-source, truncated, binary, and empty cases, when scanned, then each follows its conservative documented outcome without crashing.
5. Given existing Phase 01 payloads and decisions, when the expanded framework suite runs, then every prior PreToolUse behavior remains green.

### Test Data and Fixtures

- Synthetic high/medium/low rule configs with harmless marker text.
- Recorded PostToolUse payloads for built-ins, `mcp__*`, Task/subagent results, structured JSON, truncation, and malformed input.
- Temporary repository trees for allowlist traversal and symlink checks.
- Oversized, empty, invalid-byte, and multiple-match outputs with secret-free sentinels.

## Stage 1: PostToolUse Framework Contract
**Goal**: Extend the shared hook framework with backward-compatible PostToolUse payload and response support
**Success Criteria**: AC1 and the framework portions of AC5–AC6 pass while all existing PreToolUse tests remain green
**Status**: Not Started

## Stage 2: Scanner Engine and Normalization
**Goal**: Implement bounded normalization, data-driven rule validation, reusable scanning, and deterministic strongest-match selection
**Success Criteria**: AC2–AC4 and multi-match/performance boundary tests pass
**Status**: Not Started

## Stage 3: Entrypoint, Allowlist, and Failure Posture
**Goal**: Wire the scanner entrypoint, protected allowlist, truncation handling, and fail-closed recovery behavior
**Success Criteria**: AC7–AC10 pass automated tests and the entrypoint emits exactly one redacted response
**Status**: Not Started

## Stage 4: Scanner Verification
**Goal**: Prove regression safety and record runner-constrained live behavior without production corpus content
**Success Criteria**: The hook suite and coverage gate pass; manual block/warn/no-retry/kill-switch checks are recorded or explicitly remain NOT RUN
**Status**: Not Started
