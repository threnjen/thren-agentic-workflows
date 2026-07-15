# Feature 05: WebFetch Exfiltration Guard

## Execution Metadata

- **Wave:** 1
- **Parallel safe:** yes
- **Depends on:** none
- **Key files modified:** `.github/hooks/lib/url_exfiltration.py` `[PROPOSED - name TBD]`, `.github/hooks/lib/bash_analyzer.py`, `.github/hooks/scripts/file-access-guard.py`, `.github/hooks/config/file-access-rules.json`, `.github/hooks/file-access-guard.json`, `tests/hooks/test_bash_command_analyzer.py`, `tests/hooks/test_file_access_guard.py`, `tests/hooks/fixtures/bash/commands.json`, `tests/hooks/fixtures/url_exfiltration/recorded_payloads.json` `[PROPOSED - name TBD]`, `docs/hooks/bash-command-limitations.md`
- **Sequential reason:** n/a

## A. Requirements & Traceability

### Acceptance Criteria

1. **AC1 — Cross-phase WebFetch obligation:** The deferred Phase 01 WebFetch exfiltration channel is implemented as a PreToolUse guard using the Phase document's exact `WebFetch` tool name and verified URL input from Phase 02 fixtures rather than a guessed field.
2. **AC2 — Shared URL analyzer:** One narrow module-local URL-payload analysis API `[PROPOSED - name TBD]` is reused by direct WebFetch handling and Bash `curl`/`wget` inspection; duplicate secret/entropy classifiers are not introduced and the verified package-level `lib.__all__` contract is not broadened.
3. **AC3 — Known-secret denial:** URL query or path segments containing configured known credential formats, including AWS-style keys, tokens, private-key headers, and high-confidence base64/hex secret shapes, produce `deny` without echoing the URL or secret.
4. **AC4 — Ambiguous entropy confirmation:** Long ambiguous high-entropy/base64/hex URL segments produce `ask`, including in Bash URLs, while configured bypass escalation follows the existing Phase 01 rule posture.
5. **AC5 — Ordinary URL pass-through:** Normal URLs, short identifiers, percent-encoded ordinary text, fragments, hosts, ports, and curl literal request bodies pass without a URL-exfiltration decision.
6. **AC6 — Bash extension and priority:** Verified `analyze_command` handling inspects URL operands for `curl` and `wget` in direct, option-reordered, quoted, redirected, and piped command forms while preserving all existing protected-file upload and destructive-command results; structured matches and final selection are extended compatibly so action strength wins first and configured priority deterministically breaks same-action collisions.
7. **AC7 — Data-driven policy:** Secret formats, entropy/length thresholds, action, reason, safe alternative, priority, and bypass escalation live in the existing `.github/hooks/config/file-access-rules.json` configuration rather than concrete policy in engine code.
8. **AC8 — Conservative parsing and failures:** Malformed/missing WebFetch URLs and unsafe configuration fail closed through the verified framework; unsupported or unparsable URL forms do not crash, and the limitations document states any syntax that cannot be covered deterministically.
9. **AC9 — Redaction and measurable regression:** Decisions and audit records contain only rule identifiers, action, and safe guidance; new fixtures cover deny/ask/allow paths and the existing Bash/file-access suites remain green.

### Non-Goals

- No outbound network request is executed during analysis or tests.
- No request-body, DNS, redirect-target, response-body, or failed-tool-output scanning is added.
- No general DLP engine, semantic secret classifier, or arbitrary shell execution is introduced.
- No change is made to Feature 05's PostToolUse scanner or Feature 06's injection corpus.
- No guarantee is made for shell syntax outside the explicitly tested deterministic boundary.

### Traceability Matrix

| Acceptance Criteria | Code Areas/Modules | Planned Tests / Evidence |
|---|---|---|
| AC1 | Verified `.github/hooks/scripts/file-access-guard.py` and `.github/hooks/file-access-guard.json` | New recorded WebFetch PreToolUse payload tests |
| AC2 | URL analyzer module/API `[PROPOSED - name TBD]` | Direct analyzer tests plus integration from WebFetch and verified `analyze_command` |
| AC3 | URL rule config in `.github/hooks/config/file-access-rules.json` | Credential-format and encoded-secret deny fixtures with redaction assertions |
| AC4 | URL analyzer and existing bypass context | Ambiguous entropy ask and configured bypass tests |
| AC5 | URL parser/classifier | Negative corpus of realistic ordinary URLs and curl literal-data regressions |
| AC6 | Verified `.github/hooks/lib/bash_analyzer.py::analyze_command`, `BashMatch`, and `.github/hooks/scripts/file-access-guard.py` selection | Extended command matrix plus same-action priority collision and backward-compatibility tests |
| AC7 | Existing immutable config loader and file-access rule file | Schema validation and source-policy-separation tests |
| AC8 | Verified `security_guard` failure posture; limitations doc | Missing/malformed URL/config tests plus documented unsupported forms |
| AC9 | Verified `record_event` and hook suites | Secret sentinel absence across stdout/stderr/audit plus full regression suite |

### Phase Fidelity and Exceptions

- Key Deliverable 3 is execution-scheduled in Wave 1, before the Wave 2 corpus, because it depends only on Phase 01 and has a disjoint file scope. The manifest must record this ordering exception.
- The exact `WebFetch` name and deny/ask/allow posture are preserved from the Phase document.
- The `.github/learnings/cross-phase-decisions.md` WebFetch deferral is explicitly closed by AC1.
- No Phase requirement is deferred or renamed.

### Unverified Assumptions

- The exact WebFetch URL input field is not represented in current Phase 01 fixtures and must be verified from the Phase 02 recorded payload before implementation.
- The reusable URL analysis API name is `[PROPOSED - name TBD]`.
- Verified `BashMatch` currently has no priority field and the guard selects by action strength only; implementation must choose the narrowest backward-compatible structured-match change and prove existing consumers remain green.
- Shell aliases, variables, command substitutions, and runtime-expanded URLs cannot be fully resolved without executing code and remain a documented deterministic-analysis boundary.

## B. Correctness & Edge Cases

### Key Workflows

- Extract a direct WebFetch URL from a verified payload and classify its decoded path/query segments without contacting the host.
- Tokenize Bash through the existing `shlex`-based path, identify curl/wget URL operands, and call the same analyzer.
- Combine URL matches with existing path and Bash matches, returning the strongest configured action.

### Failure Modes and Handling

- Missing or non-string guarded WebFetch input fails closed without reflecting payload content.
- Percent decoding is bounded and performed at most a documented number of passes to avoid expansion attacks.
- Userinfo, fragments, IPv6 hosts, repeated query keys, and malformed escape sequences receive deterministic documented handling.
- Multiple URL and existing Bash matches select by action strength and configured priority; a deny cannot be weakened by an ask.
- Entropy thresholds use minimum length and character-class gates so ordinary UUIDs, hashes, and asset paths do not become blanket asks.

## C. Consistency & Architecture Fit

### Existing Patterns to Follow

- Extend verified `analyze_command`, `BashMatch`, immutable configuration, and the single strongest-decision entrypoint.
- Reuse `security_guard`, `make_decision`, and redacted `record_event`; do not emit bespoke hook JSON.
- Extend `file-access-rules.json` as required by the Phase document instead of forking URL policy into an unrelated configuration system.

### Contracts and Decisions

- The URL analyzer accepts a URL plus validated config and returns structured matches compatible with Bash action/priority selection; its exact symbol is `[PROPOSED - name TBD]` and it is imported from its module rather than added to the verified package `__all__` surface.
- Both WebFetch and Bash call the same generation/normalization/validation logic intentionally, satisfying the Phase's reuse requirement.
- URL content is used only transiently for matching and is never stored or reflected in guidance.
- The existing file-access entrypoint remains the one PreToolUse security entrypoint for direct WebFetch and Bash.

### Relationships to Sibling Plans

- Runs in parallel with `05-injection-scanner`; no mapped source/test file is shared.
- Does not depend on `06-injection-pattern-corpus`; injection-output patterns and outbound secret detection remain separate policies.
- `07-multi-harness-integration` consumes the completed guard and verifies propagation/harness behavior.

## D. Clean Design & Maintainability

### Simplest Design

- Add one deterministic module-local URL analyzer and invoke it from two existing consumers.
- Keep secret-shape and entropy thresholds in the current rule configuration.
- Extend the existing Bash fixture matrix rather than create a second shell analyzer.

### Complexity and Duplication Risks

- Direct and Bash parsing may drift; both must terminate in the same analyzer contract.
- Entropy rules can overblock hashes and IDs; require realistic negative URLs and minimum-length gates.
- Shell coverage can expand indefinitely; document boundaries rather than emulate a shell.

### Keep It Clean Checklist

- [ ] No network calls or command execution occur.
- [ ] No URL/secret appears in decisions or audit records.
- [ ] One URL classifier serves WebFetch, curl, and wget.
- [ ] Existing Bash protected-path and destructive behavior remains green.
- [ ] Unsupported shell forms are documented honestly.

## E. Completeness: Observability, Security, Operability

### Observability Decision

Do not add normal-path URL logs. A blocked/held event may record only tool, rule identifier, and action through the existing redacted audit contract. The secret-bearing URL, host, query key/value, path segment, and command body are excluded.

### Security

- URL parsing is local, deterministic, bounded, and network-free.
- Known secret formats deny; ambiguous entropy asks; ordinary URLs allow.
- Unsafe config and malformed guarded input fail closed.
- Existing human-only override and self-protected config rules remain the recovery path.

### Runbook

- Run URL, Bash, file-access, full hook, and coverage suites in that order.
- Replay fixtures only with reserved `.invalid` hosts and non-secret sentinels.
- Review redaction across stdout, stderr, and audit output.
- Roll back the URL rules and WebFetch matcher together so no half-wired state remains.

## F. Test Plan

### Evidence Categories

- **Existing tests updated:** `tests/hooks/test_bash_command_analyzer.py` and `tests/hooks/test_file_access_guard.py`.
- **Required new fixtures:** Recorded WebFetch payloads and expanded Bash URL commands.
- **Runner-constrained tests:** Live WebFetch deny/ask/allow behavior and bypass-mode ask handling.
- **Code-review evidence:** No network/subprocess calls, one shared URL API, data-driven thresholds, and redacted outputs.
- **Manual QA:** Disposable WebFetch calls using `.invalid` URLs for deny, ask, and allow outcomes.

### Top Five High-Value Checks

1. Given a WebFetch URL containing each configured known-secret shape, when the guard runs, then it denies and no secret-bearing substring appears in any output.
2. Given long ambiguous base64/hex/high-entropy segments, when WebFetch or Bash analysis runs, then both consumers return the same ask rule and guidance.
3. Given realistic ordinary URLs, UUID/hash asset paths, percent encoding, and curl literal bodies, when analyzed, then no URL-exfiltration match is produced.
4. Given option-reordered, quoted, piped, and redirected curl/wget commands plus same-action collisions, when `analyze_command` and the guard run, then URL matches combine correctly with existing path/Bash matches and configured priority resolves ties without weakening stronger actions.
5. Given malformed payload/config/URL input, when the entrypoint runs, then it fails closed with `guard error` and never reflects the input.

### Test Data and Fixtures

- Reserved `.invalid` URLs with synthetic AWS/token/private-key markers and ambiguous entropy strings.
- Negative URLs containing UUIDs, hashes, signed-looking but harmless parameters, ports, fragments, and percent encoding.
- Existing Bash command fixtures extended with direct and pipeline curl/wget vectors.
- Recorded WebFetch tool payloads with verified URL field, cwd, and permission mode.

## Stage 1: Shared URL Analyzer
**Goal**: Add a bounded, data-driven URL secret/entropy classifier reusable by direct and Bash consumers
**Success Criteria**: AC2–AC5 and AC7 pass analyzer-level deny/ask/allow and negative tests
**Status**: Not Started

## Stage 2: WebFetch PreToolUse Integration
**Goal**: Extend the existing security entrypoint and matcher with verified WebFetch payload handling
**Success Criteria**: AC1, AC3–AC5, and AC8 pass entrypoint and failure-posture tests
**Status**: Not Started

## Stage 3: Bash URL Inspection
**Goal**: Extend curl/wget analysis to reuse the URL classifier without regressing existing command policy
**Success Criteria**: AC6 and AC9 pass the extended Bash matrix and all prior Bash tests
**Status**: Not Started

## Stage 4: Redaction and Boundary Verification
**Goal**: Prove no secret/URL leakage and record deterministic-analysis limits and live runner evidence
**Success Criteria**: Full hook/coverage suites pass; limitations and live checks are recorded or explicitly remain NOT RUN
**Status**: Not Started
