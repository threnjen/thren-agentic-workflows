# Feature 05: WebFetch Exfiltration Guard Context

## Key Files

### Files Created or Modified

| Path | Change Type | Role |
|---|---|---|
| `.github/hooks/lib/url_exfiltration.py` `[PROPOSED - name TBD]` | Create | Bounded, standard-library-only URL segment classifier shared by direct WebFetch and Bash consumers. |
| `.github/hooks/lib/bash_analyzer.py` | Modify | Extract deterministic `curl` and `wget` URL operands and return URL matches without regressing protected-path or command rules. |
| `.github/hooks/scripts/file-access-guard.py` | Modify | Route verified WebFetch input and Bash URL operands through one analyzer, select the strongest configured result, and emit a redacted framework decision. |
| `.github/hooks/config/file-access-rules.json` | Modify | Store URL secret shapes, entropy/length gates, action, reason, safe alternative, priority, and bypass escalation as validated data. |
| `.github/hooks/file-access-guard.json` | Modify | Add the Phase document's exact `WebFetch` matcher to the existing PreToolUse command hook. |
| `tests/hooks/test_bash_command_analyzer.py` | Modify | Extend existing analyzer and guard regressions for URL operands, action combination, bypass behavior, and redaction. |
| `tests/hooks/test_file_access_guard.py` | Modify | Add direct WebFetch and shared URL analyzer coverage, including malformed input/config and exact audit/decision redaction. |
| `tests/hooks/fixtures/bash/commands.json` | Modify | Add covered and explicitly limited `curl`/`wget` URL vectors while preserving the existing fixture schema. |
| `tests/hooks/fixtures/url_exfiltration/recorded_payloads.json` `[PROPOSED - name TBD]` | Create | Record verified WebFetch payload shape plus synthetic deny, ask, allow, and malformed cases using reserved `.invalid` hosts. |
| `docs/hooks/bash-command-limitations.md` | Modify | Document URL-specific deterministic parsing boundaries, risks, and safer alternatives. |

### Read-Only Reference Files

| Path | Role |
|---|---|
| `.github/hooks/lib/framework.py` | Verified `ConfigSnapshot`, `load_config`, `make_decision`, `security_guard`, and `record_event` contracts; config snapshots are recursively frozen. |
| `.github/hooks/lib/file_access.py` | Existing action/priority ordering and fail-closed rule-validation pattern to follow without folding URL policy into path matching. |
| `tests/hooks/fixtures/file_access/recorded_payloads.json` | Current recorded PreToolUse fixture shape; it contains no WebFetch example and therefore cannot establish the URL field. |
| `tests/hooks/README.md` | Canonical local test and coverage commands and standard-library-only runtime constraint. |
| `docs/phases/PHASE_02/PHASE_02_SUMMARY.md` | Source requirement for WebFetch plus Bash `curl`/`wget` URL inspection and tiered deny/ask behavior. |
| `docs/phases/PHASE_02/PHASE_02_DISCOVERY_CONTEXT.md` | Verified hook-event background and clean-room/security constraints. |
| `.github/learnings/cross-phase-decisions.md` | Records the Phase 01 WebFetch deferral that this feature must close. |

## Discovery Delta

| Finding | Impact | Action |
|---|---|---|
| No current fixture contains a `WebFetch` payload, so the URL input field remains unverified exactly as the plan states. | Guessing a field would make AC1 brittle and could turn malformed guarded input into an accidental allow. | Implement the recorded payload fixture first, verify the field, and keep missing/non-string input fail-closed. No plan contradiction. |
| Verified `BashMatch` has no priority field, and `file-access-guard.py` currently chooses among Bash matches by action strength only. The plan requires action strength plus configured priority. | A same-action collision cannot currently honor AC7's priority, and extending the public tuple may affect existing consumers. | Decomposer attention: refine the plan contract or accept the risk explicitly. Implementation must choose a backward-compatible structured-match/selection approach and add collision tests before wiring both consumers. |
| `tests/hooks/test_hook_framework.py` exactly asserts the package `lib.__all__` surface. | Exporting the URL API would create an unnecessary same-wave file conflict with `05-injection-scanner` and broaden the framework contract. | **Resolved:** use a direct module import, leave `.github/hooks/lib/__init__.py` and its exact public-contract test unchanged, and keep Wave 1 file scopes disjoint. |
| Existing Bash audit coverage exactly expects command-only matches to call `record_event` with `offending_path=None`; `record_event` can otherwise serialize a path. | Passing a WebFetch URL through `offending_path` would leak secret-bearing URL material despite using the existing logger. | Preserve `offending_path=None` for URL matches and add sentinel assertions across decision output, stderr, and audit output. |
| `.github/hooks/file-access-guard.json` currently matches `Read|Edit|Write|MultiEdit|NotebookEdit|Grep|Bash`, not `WebFetch`. | Analyzer logic alone would never protect direct WebFetch calls. | Update the verified matcher in Stage 2 and cover wiring with a recorded-payload entrypoint test. |
| No phase-scoped test directory pattern exists under `tests/`; current hook tests are organized by subsystem. | A new `tests/phase02/` consolidated file would conflict with the established local layout for this independent feature. | Extend the two mapped hook test modules and fixtures; leave cross-feature consolidation to the final integration feature. |
| Current baseline is healthy: 252 tests pass and combined measured coverage is 63.56%, above the 50% prerequisite threshold. | Stage 0 test bootstrapping is unnecessary. | Preserve the baseline and rerun the full suite and coverage gate after implementation. |

## Architectural Decisions

- Use one narrow URL analyzer `[PROPOSED - name TBD]` for direct WebFetch and Bash URL operands. This prevents classifiers and tuning thresholds from drifting between consumers.
- Keep policy in `.github/hooks/config/file-access-rules.json`; Python code validates, normalizes, and applies the policy but does not embed concrete credential formats or thresholds.
- Parse locally with the Python standard library, cap decoding and input work, and never make a network request or execute shell input.
- Preserve the existing Phase 01 security entrypoint and framework decision path. Direct WebFetch is an additional branch of `handle_event`, not a second hook runtime.
- Rank a denial above an ask and an ask above an allow; within the same action tier, honor validated configured priority using a contract that does not silently break existing Bash matches.
- Treat URL material as transient matching input. Guidance and audit evidence contain only the tool, rule identifier, action, and generic safe alternative.
- Add no normal-path URL logs. Only blocked or held events use the existing redacted audit channel because the URL itself is the sensitive object.

## Constraints

- Preserve the exact `WebFetch` tool name and the Phase posture: known credential formats deny, ambiguous high-entropy payloads ask, and ordinary URLs pass untouched.
- Verify the WebFetch URL field from a recorded Phase 02 fixture before coding the entrypoint branch.
- Runtime code remains Python 3.12 standard-library-only; pytest and coverage stay development-only dependencies.
- Configuration errors and malformed guarded WebFetch input fail closed through `security_guard` with the generic `guard error` reason.
- Percent decoding must be bounded; parsing must deterministically address userinfo, fragments, IPv6 hosts, repeated keys, malformed escapes, and multiple matches.
- Existing protected-file upload, destructive-command, bypass-escalation, and ordinary curl literal-body behavior must remain green.
- Use only synthetic markers and reserved `.invalid` hosts. Never place real credentials in fixtures or diagnostics.
- Follow the clean-room constraint: requirements and category taxonomy may inform original tests and rules, but inspiration hook code or pattern files must not be copied.

## Scope Boundaries

- Do not scan request bodies, DNS, redirect targets, response bodies, or failed tool output.
- Do not add outbound network calls, subprocess execution, shell expansion, aliases, variable evaluation, or a general shell interpreter.
- Do not change the PostToolUse injection scanner, injection corpus, or multi-harness propagation owned by sibling features.
- Do not broaden `record_event` to retain URLs, hosts, query names/values, commands, or matched secret substrings.
- Do not promise coverage for dynamic shell/runtime URL construction; document unsupported syntax with a reproduction, risk, boundary, and safer alternative.
- Do not modify unrelated generated agent/profile artifacts or the pre-existing dirty `codex/profiles/feature-decomposer.config.toml`.

## Relationships to Sibling Plans

- `05-injection-scanner` runs in the same Wave 1 with a disjoint mapped file scope; neither feature calls the other's runtime API.
- `06-injection-pattern-corpus` has no dependency on this guard. Prompt-injection output scanning and outbound secret-shaped URL detection remain separate policy domains.
- `07-multi-harness-integration` depends on this completed feature and is responsible for propagation and combined harness verification.

## Suggested Implementation Order

1. Establish the recorded WebFetch payload shape and analyzer-level deny/ask/allow fixtures.
2. Implement and validate the shared bounded URL classifier and same-tier priority semantics.
3. Wire direct WebFetch into the existing PreToolUse entrypoint and matcher with redacted audit behavior.
4. Extend deterministic Bash `curl`/`wget` operand extraction to call the same classifier.
5. Document unsupported syntax, run focused regressions, then run the full suite, coverage gate, and disposable manual checks.

## Environment State

| Property | Value |
|---|---|
| Tech Stack | Python 3.12.6; standard-library-only hook runtime; pytest 9 and pytest-cov 7 development tooling |
| Test Runner | `uv run --with-requirements requirements-dev.txt pytest -q` |
| Test Baseline | 252 passed in 1.99s; coverage gate also passed at 63.56% total — captured 2026-07-14 |
| Coverage | `uv run --with-requirements requirements-dev.txt pytest -q --cov=.github/hooks/lib --cov=.github/hooks/scripts --cov=scripts --cov-report=term-missing --cov-fail-under=50` |
| Lint | Not configured |
| Format | Not configured |

## Relevant Learnings

- `.github/learnings/cross-phase-decisions.md`: WebFetch was deliberately left unguarded in Phase 01 and explicitly moved into Phase 02. This feature closes that obligation; it is not optional follow-up work.
- `.github/learnings/review-learnings.md`: Public value types that can bypass a validating factory must be revalidated at security-sensitive emission or execution boundaries. Any new structured URL match must therefore be validated before it affects the framework decision.
- `.github/learnings/review-learnings.md`: Exact encoded suffixes must use exact suffix removal, not character-set trimming. Preserve the analyzer's verified `removesuffix` behavior when extending Bash token handling.
