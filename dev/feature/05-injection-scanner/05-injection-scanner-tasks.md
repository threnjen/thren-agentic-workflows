# Feature 05: Injection Scanner — Tasks

## Stage 1: PostToolUse Framework Contract

- [ ] Extend the verified normalized event contract to accept the Phase document's exact `tool_output`, `tool_output_truncated`, `agent_id`, and `agent_type` fields while preserving every existing PreToolUse tool-name, tool-input, and context alias. (AC1)
- [ ] Define and implement backward-compatible PostToolUse result validation/emission for output suppression and warning context without changing existing PreToolUse `allow|ask|deny` JSON or exit behavior. (AC1, AC5, AC6)
- [ ] Revalidate every directly constructible result value at the external emission boundary and retain the redacted `guard error`/exit fallback when serialization or output writing fails. (AC5, AC6, AC9)
- [ ] Add framework tests for valid raw and structured outputs, the truncation flag, main-agent and subagent metadata, preserved aliases, missing/invalid fields, and unchanged Phase 01 payload behavior. (AC1, AC10)
- [ ] Add response-shape tests proving a PostToolUse block suppresses original output and a PostToolUse warning appends context without replacing or normalizing the original logical output. Use harmless synthetic content only. (AC5, AC6)
- [ ] Run the existing framework tests after each contract change and confirm all verified PreToolUse tests retain their prior meaning. (AC1, AC10)

## Stage 2: Scanner Engine and Normalization

- [ ] Finalize the proposed scanner module, rule-loading API, output-scanning API, result representation, and public export names; record final names and keep the exported surface limited to Feature 06's needs. (AC3, AC4)
- [ ] Implement data-driven rule validation for severity, response action, category, redacted reason, matcher, and priority; reject missing, mistyped, duplicate/ambiguous, unsafe, or otherwise invalid configuration without reflecting configuration content. (AC3, AC9)
- [ ] Ensure response action comes from each rule and add tests proving severity does not trigger a hard-coded engine action policy. (AC3)
- [ ] Implement scan-copy Unicode NFKC normalization, explicit homoglyph folding, and invisible/zero-width stripping while proving the input/raw output object remains unchanged. (AC2, AC6)
- [ ] Implement bounded base64 and hex candidate recognition/decoding with explicit byte and candidate-count caps; skip malformed candidates safely and prevent recursive/unbounded decoding. (AC2, AC8, AC9)
- [ ] Implement bounded matcher evaluation and deterministic strongest-match selection across actions, severities, priorities, and equal-priority ties; document and test the stable tie-break rule selected during implementation. (AC3, AC8)
- [ ] Return only structured match metadata needed for category/rule/reason/action decisions; assert matched text, decoded content, and raw output are absent from returned diagnostic strings and logs. (AC4, AC5, AC6)
- [ ] Build scanner unit tests with temporary synthetic high/medium/low configurations covering plain, NFKC, homoglyph, zero-width, base64, hex, multiple-match, invalid-schema, unsafe-matcher, and raw-preservation cases. (AC2–AC4, AC8)
- [ ] Add representative size-limit and matcher-performance checks against the Phase 01 50 ms framework-budget baseline, recording scanner workload separately when the combined budget cannot be asserted reliably. (AC2, AC8, AC10)
- [ ] Audit runtime imports and engine source to confirm standard-library-only execution and no production injection phrases, copied regexes, severity policy, or surveyed fixture content. (AC2–AC4; code-review evidence)

## Stage 3: Entrypoint, Allowlist, and Failure Posture

- [ ] Finalize and create the thin scanner entrypoint/config filenames proposed by the plan; make direct execution independent of caller cwd and ambient `PYTHONPATH`, following the verified file-access entrypoint pattern. (AC9, AC10)
- [ ] Register PostToolUse coverage for successful `Read|Bash|Grep|WebFetch|WebSearch|Task` and `mcp__*` outputs without adding `PostToolUseFailure` behavior. (AC10)
- [ ] Add secret-free payload fixtures for every covered built-in, MCP serialized/JSON output, Task/subagent result, truncation case, empty output, malformed input, and runner-shaped binary/non-UTF8 representation. (AC8, AC10)
- [ ] Implement the configured high/block path so output is suppressed and the fixed redacted reason includes source, category, and rule identifier plus explicit no-retry and manual-user-inspection guidance. (AC5)
- [ ] Implement configured medium/low warning paths so original output remains byte-for-byte/raw-logically intact and one fixed-shape `additionalContext` warning includes only validated identifiers, category, and recommended posture. (AC6)
- [ ] Implement the empty-output fast allow path, structured-output serialization seam, binary/non-UTF8 notice behavior, scan-byte cap, available-content scanning, and low-tier unscanned-tail notice for `tool_output_truncated: true`. (AC8)
- [ ] Ensure a detected high/block match still wins when content is truncated or multiple tiers match, and combine/deduplicate lower-tier notices deterministically without claiming full coverage. (AC5, AC8)
- [ ] Finalize the protected allowlist configuration and permit bypass only for verified repository-owned corpus/fixture assets and `docs/inspiration/` paths; an absent source path must not qualify. (AC7)
- [ ] Reuse verified path normalization only where suitable, then independently test traversal, existing and broken symlinks, missing paths, outside-repository targets, case behavior, and configuration entries that attempt to broaden approved scope. (AC7)
- [ ] Add regression tests proving the existing `self-hook-assets` rule denies agent writes to the finalized allowlist, scanner configuration, current fixtures, and future corpus paths under `.github/hooks/**`; do not duplicate policy unless inherited coverage fails. (AC7)
- [ ] Induce payload, config-load, rule-validation, normalization, matcher, handler, and emitter failures and assert one redacted fail-closed result with no output/match/config reflection. (AC9)
- [ ] Verify only the project override's existing `guard.enabled` control can disable the scanner, that environment/process input cannot activate it, and that the documented kill-switch recovery path restores operation. (AC9)
- [ ] Parameterize entrypoint tests across all supported tools and assert each invocation emits exactly one valid result and never logs raw output, matched content, decoded candidates, or warning-shaped attacker text. (AC5, AC6, AC9, AC10)

## Stage 4: Scanner Verification

- [ ] Install the documented development dependencies if needed, then run `.venv/bin/python -m pytest tests/` and record the complete result. (AC1–AC10; automated regression evidence)
- [ ] Run `.venv/bin/python -m pytest tests/hooks/ --cov=.github/hooks/lib --cov-report=term-missing --cov-fail-under=50` and record coverage at or above the repository gate. (AC1–AC10; coverage evidence)
- [ ] Run `python3 -m unittest discover -s tests -v` and preserve the captured 14-test fallback baseline or document any intentional inventory change. (AC10; regression evidence)
- [ ] Review the diff for clean-room compliance, standard-library runtime imports, bounded regex/decoding work, deterministic ordering, immutable raw output, protected configuration, and complete absence of raw/matched-content observability. (AC2–AC9; code-review evidence)
- [ ] Replay secret-free synthetic payloads for one block, one warning, one empty result, one binary/non-UTF8 result, one truncation notice, one induced failure, and one project-only override recovery; record outputs without attacker-shaped content. (AC5–AC10; entrypoint evidence)
- [ ] In a disposable Claude Code session, verify one real high-tier suppression, one real warning attachment, the no-retry instruction's observed behavior, Task/subagent output handling, and truncation behavior; mark any unavailable runner checks `NOT RUN` rather than inferring success. (AC5, AC6, AC8, AC10; runner-constrained/manual evidence)
- [ ] Confirm the finalized public scanner APIs and configuration contract are recorded for `06-injection-pattern-corpus`, and notify the orchestrator before any unplanned shared-file edit changes the manifest dependency graph. (AC3, AC4; sibling handoff)
