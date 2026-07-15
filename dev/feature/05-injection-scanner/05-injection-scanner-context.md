# Feature 05: Injection Scanner — Context

## Key Files

### Files to Create or Modify

| File | Role | Change Type |
|------|------|-------------|
| `.github/hooks/lib/framework.py` | Verified shared payload, decision-emission, configuration, and security-failure contracts; extend for backward-compatible PostToolUse input/output handling | Modify |
| `.github/hooks/lib/__init__.py` | Verified public hook-framework import surface; expose only the scanner contracts needed by Feature 06 | Modify |
| `.github/hooks/lib/injection_scanner.py` `[PROPOSED - name TBD]` | Bounded normalization, rule validation/loading, matching, strongest-match selection, and redacted result metadata | Create |
| `.github/hooks/scripts/injection-scanner.py` `[PROPOSED - name TBD]` | Thin cwd-independent PostToolUse security-hook entrypoint | Create |
| `.github/hooks/injection-scanner.json` `[PROPOSED - name TBD]` | Hook registration and matcher coverage for successful built-in, Task, and MCP outputs | Create |
| `.github/hooks/config/injection-allowlist.json` `[PROPOSED - name TBD]` | Protected, repository-scoped source-path allowlist and scanner limits | Create |
| `tests/hooks/test_hook_framework.py` | Existing framework regression suite; add PostToolUse payload and response compatibility evidence | Modify |
| `tests/hooks/test_injection_scanner.py` `[PROPOSED - name TBD]` | Scanner engine, normalization, response, allowlist, boundary, failure, performance, and entrypoint coverage | Create |
| `tests/hooks/fixtures/injection/post-tool-use-payloads.json` `[PROPOSED - name TBD]` | Secret-free recorded and synthetic payloads for supported tools, structured output, truncation, and malformed cases | Create |

### Read-Only Reference Files

| File | Role |
|------|------|
| `docs/phases/PHASE_02/PHASE_02_SUMMARY.md` | Authoritative Phase 02 scope, exact PostToolUse fields, response posture, clean-room boundary, and success criteria |
| `docs/phases/PHASE_02/PHASE_02_DISCOVERY_CONTEXT.md` | Pre-captured Claude Code contract facts and allowed category-level inspiration; do not re-open surveyed pattern sources |
| `.github/hooks/lib/file_access.py` | Verified immutable rule-loading style and public `normalize_path` path-normalization helper to reuse only where its contract fits |
| `.github/hooks/lib/bash_analyzer.py` | Verified data-driven, standard-library rule-module pattern; WebFetch/Bash URL changes remain the sibling feature's scope |
| `.github/hooks/scripts/file-access-guard.py` | Verified cwd-independent entrypoint, `security_guard`, config layering, and strongest-action consumer pattern |
| `.github/hooks/config/file-access-rules.json` | Verified `self-hook-assets` write-deny rule covering `**/.github/hooks/**`; this feature verifies inherited protection rather than duplicating policy |
| `tests/hooks/test_file_access_guard.py` | Existing path traversal, symlink, self-protection, and project-override testing patterns |
| `tests/hooks/fixtures/recorded_payloads.json` | Existing Phase 01 payload fixture conventions and aliases |
| `tests/hooks/README.md` | Developer environment, pytest, coverage-gate, and unittest commands |
| `pyproject.toml` | Verified pytest test-root configuration |
| `requirements-dev.txt` | Verified development-only pytest and pytest-cov version ranges |
| `dev/feature/06-injection-pattern-corpus/06-injection-pattern-corpus-plan.md` | Downstream consumer of the validated rule loader and output-scanning API |
| `dev/feature/07-multi-harness-integration/07-multi-harness-integration-plan.md` | Downstream propagation and harness-integration consumer |

## Discovery Delta

| Finding | Impact | Action |
|---------|--------|--------|
| All four scanner-specific production/config paths and both proposed scanner test/fixture paths are absent; the plan correctly labels their exact names `[PROPOSED - name TBD]`. | Implementers must not treat proposed filenames or public APIs as established codebase contracts. | Finalize idiomatic names during implementation, preserve the plan's file-scope intent, and record final names in the implementation record. |
| The verified framework currently parses only tool identity/input/context, its `Decision` contract covers `allow|ask|deny`, and `emit_decision` emits a PreToolUse-only shape. | PostToolUse output fields and block/warn emission require a backward-compatible framework extension; reusing the existing emitter unchanged would be incorrect. | Add event-aware PostToolUse handling and keep every existing PreToolUse schema assertion green. This is already required by AC1 and AC5–AC6. |
| `file_access.normalize_path` is an existing public helper that resolves and anchors paths, but it uses non-strict resolution and does not by itself prove that a source exists or is an approved repository-owned asset. | Path normalization alone cannot authorize an allowlist bypass. | Reuse the helper where suitable, then separately require existence, repository ownership/scope, and conservative failure behavior for allowlist qualification. |
| The repository defines 101 hook test functions, but `.venv/bin/python -m pytest` cannot start because pytest is not installed in the current environment. The fallback unittest discovery passes 14 tests, while `tests/hooks/README.md` still describes an older two-test unittest baseline. | Existing hook-suite pass/fail and coverage cannot be freshly measured in this workspace; the README's baseline count is stale. | Use the documented dependency install and exact pytest/coverage commands before implementation verification; treat the 101 count as inventory, not a passing baseline. No plan correction is required because the plan already classifies this evidence as runner-constrained. |
| No lint or format configuration is tracked. | There is no repository-specific lint/format gate to invent for this feature. | Use test, coverage, targeted code review, and manual QA evidence; keep formatting consistent with adjacent Python files. |

## Architectural Decisions

- Extend the verified Phase 01 `HookEvent`, payload parser, security wrapper, and emitters instead of creating a parallel hook framework. Preserve all existing PreToolUse aliases and decision behavior.
- Represent PostToolUse fields without mutating the original output. Normalization and decoded candidates exist only as bounded scan copies; warn and allow paths return the original logical output intact.
- Keep the scanner engine data-driven. Rules carry severity, response action, category, reason, matcher, and priority; engine control flow validates and applies those values but contains no production injection phrases or severity-to-action policy.
- Finalize a narrow rule-loading API and output-scanning API `[PROPOSED - name TBD]`, export only what Feature 06 needs, and return structured identifiers/metadata without matched text.
- Select the strongest match deterministically. Action, severity, priority, and the final stable tie-break rule must be documented and tested; iteration order must never decide the result.
- Apply Unicode NFKC, a bounded explicit homoglyph fold, invisible/zero-width stripping, and bounded base64/hex candidate extraction. Cap candidate count and size before regex work.
- Treat regex validity and resource safety as configuration validity. Invalid schemas, unsafe/unbounded matchers, normalization failures, matching failures, and emission failures use the existing redacted fail-closed posture.
- Resolve allowlist candidates conservatively. A missing, traversed, symlink-broadened, outside-repository, or otherwise unverifiable source does not qualify. Allow only verified repository-owned corpus/fixture assets and `docs/inspiration/` paths declared by protected configuration.
- Preserve security-boundary validation at emission. The existing `Decision` value type is directly constructible, so PostToolUse result values must be revalidated immediately before external emission as the current PreToolUse emitter does.
- Do not add a normal-path log. If existing event recording is used for a diagnosable block, record only tool, rule identifier, category, and decision; never record output, matched text, decoded candidates, or warning content.

## Constraints

- Runtime code remains Python-standard-library-only, deterministic, independent of cwd/PYTHONPATH, and compatible with the verified project-only `guard.enabled` override.
- Preserve the Phase document's exact `tool_output`, `tool_output_truncated`, `agent_id`, `agent_type`, `decision`, `reason`, `hookSpecificOutput.updatedToolOutput`, and `hookSpecificOutput.additionalContext` names.
- Cover successful `Read|Bash|Grep|WebFetch|WebSearch|Task`, `mcp__*`, serialized structured output, and Task/subagent results. `PostToolUseFailure` remains out of scope.
- High configured block actions suppress output and use fixed redacted no-retry/manual-inspection guidance. Medium/low configured warning actions preserve output and append fixed-shape redacted context.
- Empty output takes the fast allow path. Binary/non-UTF8 representations do not crash. Scan caps and runner truncation scan available content and disclose incomplete tail coverage without claiming completeness.
- Production corpus rules, positive/negative corpus fixtures, and corpus tuning belong to Feature 06. Engine tests use harmless synthetic marker rules only.
- WebFetch URL-exfiltration policy and Bash `curl`/`wget` URL inspection belong to `05-webfetch-exfiltration-guard` and must not be introduced here.
- Codex/OpenCode parity claims, propagation, version markers, and user limitation sign-off belong to Feature 07.
- Do not copy patterns, regexes, source, or fixtures from surveyed repositories. Use only the Phase document's category taxonomy and synthetic test markers.
- No direct user-prompt scanning, semantic/LLM detection, or raw/matched-content observability is added.

## Scope Boundaries

- Do not author the Phase 02 production injection corpus or benchmark tuning data.
- Do not change WebFetch/Bash exfiltration analysis or its rule configuration.
- Do not modify propagation scripts, generated harness assets, Codex/OpenCode adapters, or distribution markers.
- Do not broaden the existing `self-hook-assets` rule unless verification proves the inherited `**/.github/hooks/**` coverage insufficient; record such a discovery before changing scope.
- Do not expose proposed API/type/test method names as established until implementation finalizes and records them.
- Do not claim live suppression, Task/subagent behavior, or truncation semantics from unit tests alone; retain runner-constrained/manual evidence labels.

## Relationships to Sibling Plans

- Runs in Wave 1 in parallel with `05-webfetch-exfiltration-guard`; the plans have disjoint conservative file scopes.
- `06-injection-pattern-corpus` depends on this feature's validated rule-loading and output-scanning API. This feature must make the reusable API explicit; Feature 06 supplies and benchmarks production rule content.
- `07-multi-harness-integration` depends on the completed scanner entrypoint and configuration artifacts for propagation and supported harness wiring or evidenced limitation handling.
- If implementation discovers a need to touch a sibling-owned file, stop parallel work and report the shared-file dependency to the orchestrator before editing.

## Suggested Implementation Order

1. Extend and regression-test the framework's PostToolUse payload/response contract while retaining PreToolUse behavior.
2. Finalize the proposed scanner module and narrow public API, then implement rule validation, normalization, bounded decoding, and deterministic matching with synthetic rules.
3. Wire the thin entrypoint, protected allowlist, output-boundary behavior, tool coverage, and fail-closed recovery.
4. Run the complete automated gates, inspect security properties, and record runner-constrained live block/warn/no-retry/override evidence separately.

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Python 3.12.6; standard-library-only Python hook runtime, JSON configuration, and POSIX Bash wrappers |
| Test Runner | `.venv/bin/python -m pytest tests/`; hook coverage: `.venv/bin/python -m pytest tests/hooks/ --cov=.github/hooks/lib --cov-report=term-missing --cov-fail-under=50`; fallback regression: `python3 -m unittest discover -s tests -v` |
| Test Baseline | Pytest/coverage NOT RUN: `.venv` lacks pytest; 101 hook test functions inventoried. Unittest: 14 passed, 0 failed. Captured 2026-07-14 |
| Lint | Not configured |
| Format | Not configured |
| Branch | `phase/prompt-injection-defense` |

## Relevant Learnings

- `.github/learnings/review-learnings.md`: a public value type that callers can construct directly must be validated again at every security-sensitive emission boundary. Preserve the framework's boundary revalidation when adding PostToolUse results.
- `.github/learnings/cross-phase-decisions.md`: WebFetch exfiltration was explicitly moved into Phase 02 and is satisfied by sibling `05-webfetch-exfiltration-guard`; keep it outside this scanner feature while preserving the integration dependency.
- No entries in `.github/learnings/debugging-learnings.md` or `.github/learnings/project-learnings.md` change this feature's scanner implementation contract.
