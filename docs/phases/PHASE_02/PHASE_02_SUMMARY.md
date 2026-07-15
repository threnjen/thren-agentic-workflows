# Phase 2: Prompt-Injection Defense

**Status**: Implemented — release blocked (NO-GO)
**Depends on**: Phase 01 (hook framework, config layering, propagation stage)
**Estimated complexity**: Large (upgraded from Medium — full multi-harness parity added during refinement)
**Cross-references**: `docs/phases/DISCOVERY_CONTEXT.md`, `docs/phases/PHASE_02/PHASE_02_DISCOVERY_CONTEXT.md`, `docs/inspiration/claude-hooks.md`, `.github/learnings/cross-phase-decisions.md`

## What's New

Phase 02 implemented a successful-output injection scanner, a clean-room severity-tiered pattern corpus and benchmark, WebFetch/curl URL-payload checks, and generated Claude Code, Codex, and OpenCode wiring. Automated contract evidence is strongest for Claude Code and OpenCode; Codex covers only Bash, `apply_patch`, and MCP PostToolUse results and remains Partial under an explicitly accepted residual risk. The implementation is not release-ready: final production review returned NO-GO because P2-SEC-01, P2-SEC-02, and P2-SEC-03 can leave high-tier content model-visible or bypass scanning.

## Objective

Ship a PostToolUse injection scanner with an original, severity-tiered pattern corpus that hard-blocks high-confidence indirect prompt injection and warns on the rest — beating the surveyed warn-only design — and close the WebFetch exfiltration gap deferred from Phase 01, with equivalent enforcement propagated to Codex and OpenCode.

## Confirmed Platform Facts (from refinement research)

These were verified against current Claude Code hooks documentation and anchor the design:

- PostToolUse `{"decision": "block", "reason": …}` **suppresses the tool output from context entirely**; the model receives only the hook's reason. Hard-block is real, not advisory.
- `hookSpecificOutput.updatedToolOutput` can replace tool output; `additionalContext` appends to it. The warn tier uses `additionalContext`.
- PostToolUse fires for built-in tools, `mcp__*` tools, and Task/subagent results (payload carries `agent_id`/`agent_type`), and runs regardless of permission mode, including bypass permissions.
- The payload includes `tool_output` plus a `tool_output_truncated` flag for oversized outputs.
- PostToolUse does **not** fire for failed tool calls (a separate PostToolUseFailure event exists) — stderr from failed commands is a documented coverage boundary (see Risks).

The implementation investigation found automated replacement support for OpenCode and only partial successful-output coverage for Codex. The Codex limitation was explicitly accepted on 2026-07-15 without changing its Partial classification. Live Claude Code, Codex, and OpenCode harness QA remains `NOT RUN`.

## Execution Outcome

- All four feature bundles were implemented and reviewed: `05-injection-scanner`, `05-webfetch-exfiltration-guard`, `06-injection-pattern-corpus`, and `07-multi-harness-integration`.
- Final production verdict: **NO-GO**. P2-SEC-01 preserves attacker-controlled structured keys during block redaction; P2-SEC-02 permits deterministic bypass beyond scan and encoded-candidate limits; P2-SEC-03 trusts mutable directory-wide allowlists.
- Codex successful-output coverage remains **Partial**. User approval accepted this known residual gap but did not supply missing coverage or passing live evidence.
- PERF-01 remains **FAIL** at the unchanged 50 ms gate, with observed medians of 117–383 ms. User approval accepted the risk but did not convert the result to pass.
- Live/manual harness QA remains **NOT RUN**. See `PHASE_02-qa-analysis.md`, `PHASE_02-security-scan.md`, `PHASE_02_QA.md`, and `PHASE_02_QA_COVERAGE_MAP.md` for the authoritative release evidence and re-entry sequence.

## Scope

### In Scope

- **Injection scanner hook** (PostToolUse; matcher `Read|Bash|Grep|WebFetch|WebSearch|Task` plus `mcp__*`), built on the Phase 01 framework (payload parsing, decision emission, config layering, redacted logging, fail-closed posture).
- **Original pattern corpus** (config data, not code — per project architecture): severity-tiered (`high`/`medium`/`low`) with per-pattern reason and category, covering at minimum:
  - Instruction override (ignore/forget previous instructions, fake system-prompt delimiters)
  - Persona/role-play hijack (DAN-style, "pretend you are", restriction-bypass phrasing)
  - Encoding and obfuscation — including the gaps the surveyed corpus misses: homoglyph substitution (with Unicode normalization before matching), zero-width/invisible characters, base64/hex-encoded imperatives, leetspeak
  - Context manipulation (fake Anthropic/admin/authority claims, fake `{"role":"system"}` fragments, fabricated prior-conversation claims)
  - Instruction smuggling — HTML/code comments, **plus markdown-native channels the surveyed corpus misses**: link titles, image alt text, reference-style link definitions, HTML attributes inside markdown
  - Clean-room constraint: the corpus is authored from the category taxonomy only; no regex is copied from the surveyed `patterns.yaml`.
- **Severity → response mapping** (decided during refinement):
  - `high` → `decision: block`: output suppressed entirely; structured reason states source, category, rule fired, and explicitly instructs the agent **not to retry the same call** and to ask the user to inspect the source manually.
  - `medium`/`low` → warn-and-continue via `additionalContext`: a structured warning (category, matched rule, recommended posture) appended to the intact output.
  - Mapping is declared per-rule in config; the engine contains no severity policy.
- **Pre-scan normalization pipeline**: Unicode NFKC + homoglyph folding + zero-width stripping applied to a scan copy before pattern matching, so obfuscated variants hit the same rules as plain-text ones. Raw output is never modified on the warn path.
- **WebFetch exfiltration guard** (PreToolUse on `WebFetch`, extending Phase 01's bash exfil rules): deny outbound URLs carrying secret-shaped payloads — long high-entropy/base64/hex query or path segments, known credential formats (AWS keys, tokens, private-key headers) — tiered per Phase 01 posture (`deny` for high-confidence secret formats, `ask` for ambiguous high-entropy payloads). Also extend the bash analyzer's existing `curl`/`wget` rules to inspect URL payloads, not only `-d @file`-style flags.
- **Self-false-positive handling**: a config-driven source-path allowlist so the scanner does not fire on this repo's own pattern config, test fixtures, and `docs/inspiration/` survey docs (which legitimately contain injection-pattern text). The allowlist file and pattern config join Phase 01's protected/self-protection path set — an agent must not be able to allowlist its way past the scanner or edit the corpus.
- **Fixture-driven measurable test corpus** (the improvement the surveyed repo lacks): positive fixtures per pattern (each rule has at least one triggering fixture), negative fixtures drawn from realistic legitimate content (security documentation, this repo's own docs, code discussing prompts), and a benchmark harness reporting detection/false-positive counts so corpus tuning is measurable, not anecdotal.
- **Truncation handling**: when `tool_output_truncated` is true, scan the available content and append a low-tier notice that the tail was not scanned; document that boundary-split patterns are undetectable.
- **Multi-harness parity (Codex + OpenCode)** — in-scope deliverable with an investigation gate:
  1. Verify each harness's post-tool-output hook contract: does an equivalent event exist, and can it suppress or rewrite tool output before the model sees it?
  2. Where the contract supports it: implement equivalent block/warn enforcement and propagation wiring.
  3. Where the harness provably cannot intercept output: document the platform limitation with evidence, downgrade that harness's classification honestly (as Phase 01 did), and obtain explicit user sign-off on the residual gap. The phase does not stall on limitations outside our control.
- **Propagation**: scanner script, pattern corpus, allowlist config, and per-harness wiring emitted by the existing `propagate_master_assets.py` hooks stage, with the version-marker convention from Phase 01.

### Out of Scope

- Direct prompt injection (instructions typed by the user) — indirect injection only, matching the threat model.
- LLM-based or semantic detection — pattern/regex + normalization only; deterministic, no API cost.
- Cursor and GitHub Copilot support (remain Not supported, per Phase 01 classification).
- Scanning outputs of **failed** tool calls (PostToolUseFailure integration) — documented boundary; candidate follow-up if it proves exploitable in practice.
- Pre-edit file backup layer (Phase 03 candidate per cross-phase decisions).
- Formatting/completion gates (Phase 03) and skill enforcement (Phase 04).
- Copying patterns, code, or fixtures from the surveyed repos (clean-room constraint).
- Resolving Phase 01's release blockers (SEC-01 propagation containment, PERF-01 latency) — Phase 02 consumes the framework but does not own that remediation.

## Key Deliverables

| # | Deliverable | Description | Likely Features |
|---|-------------|-------------|-----------------|
| 1 | Injection scanner hook | PostToolUse entrypoint on the Phase 01 framework: normalization pipeline, severity→response engine, block/warn emission, truncation notice, allowlist | scanner engine; normalization; response mapping |
| 2 | Pattern corpus + benchmark suite | Original tiered pattern config across 5+ categories with per-rule fixtures, negative corpus, and measurable detection/FP benchmark | corpus authoring; fixture harness; tuning |
| 3 | WebFetch exfiltration guard | PreToolUse URL-payload rules for WebFetch + extended bash `curl`/`wget` URL inspection, tiered deny/ask | outbound URL rules; bash analyzer extension |
| 4 | Multi-harness parity + propagation | Codex/OpenCode contract verification, equivalent enforcement or evidenced limitation sign-off, propagation emission for all artifacts | harness investigation; adapters; propagation wiring |

## Technical Context

- Phase 01 framework: `.github/hooks/lib/framework.py` (payload parsing, decisions, config layering, failure posture), `.github/hooks/lib/bash_analyzer.py` (extend for URL payload inspection), `.github/hooks/config/` (rule-config conventions to follow), `.github/hooks/scripts/file-access-guard.py` (reference consumer of the framework).
- Propagation: hooks stage of `scripts/propagate_master_assets.py`; `.github/hooks/.distribution-version` marker convention.
- Enforcement posture and self-protection rules follow `docs/phases/PHASE_01/PHASE_01_SUMMARY.md`; the scanner is a security hook → **fails closed** (scanner error blocks with a guard-error reason), recoverable via the Phase 01 human-only override-file kill switch.
- Design reference (requirements only, never code): `docs/inspiration/claude-hooks.md` and the local survey copy at `/Users/jennywadkins/github_repos/claude_skills/claude-hooks` — category taxonomy and weaknesses-to-beat documented in `PHASE_02_DISCOVERY_CONTEXT.md`.

## Dependencies & Risks

- **Dependency — Phase 01 framework**: features 1–3 of Phase 01 are implemented and tested; Phase 02 can build on them now. But Phase 01 is release-blocked (SEC-01 propagation containment, PERF-01 latency), and Phase 02's deliverable 4 rides the same propagation stage. *Mitigation*: scanner development proceeds independently; Phase 02's propagation acceptance inherits whatever containment fix Phase 01 lands — if still open when deliverable 4 starts, flag before building on it.
- **Risk — false positives suppressing legitimate content** (the highest-stakes failure: a hard block on a legitimate file halts real work). *Mitigation*: `high` tier reserved for patterns with essentially no legitimate use; benchmark suite enforces a zero-false-positive bar on the negative corpus for `high` rules specifically; soak period on this repo before propagating; allowlist escape hatch is human-only.
- **Risk — block-retry loop**: the agent responds to a suppressed Read by re-reading the same file, burning turns on repeated blocks. *Mitigation*: block reason explicitly instructs no-retry and names the human next step; manual QA includes a live retry-behavior check.
- **Risk — regex detection is bypassable**: determined attackers can evade any pattern set. *Mitigation*: normalization pipeline closes the cheap evasions (homoglyphs, zero-width, casing); document that this is defense-in-depth, not a security boundary — same honesty stance as Phase 01's bash-analysis limits doc.
- **Risk — latency**: scanning every tool output with a large corpus, potentially in an interpreter started per call. *Mitigation*: compile patterns once per invocation, cap scanned bytes (config-declared, with the truncation notice), stay within the Phase 01 latency-budget approach; benchmark with representative large outputs.
- **Risk — Codex/OpenCode cannot suppress output**: parity may be impossible on a harness that lacks post-output interception. *Mitigation*: the investigation gate (In Scope, deliverable 4) converts this from a stall risk into a bounded decision: implement, or document the limitation with evidence and get explicit sign-off.
- **Risk — scanner self-triggering**: pattern config, fixtures, and inspiration docs contain the very strings the scanner hunts. *Mitigation*: source-path allowlist (agent-protected) + negative fixtures asserting these paths scan clean.
- **Edge cases to carry into decomposition**: empty outputs (skip fast), binary/non-UTF8 output (skip with notice, don't crash), multiple matches across tiers in one output (highest tier wins), matches inside subagent results (block applies to the Task result), MCP tools with structured/JSON outputs (scan the serialized text), warn-tier `additionalContext` itself must never echo the matched injection text back verbatim in a follow-instructions-shaped way (state category + rule id, quote minimally).

## Success Criteria

- [ ] Every `high` pattern has a fixture proving `decision: block` suppresses the output and emits a structured no-retry reason; every `medium`/`low` pattern has a fixture proving intact output plus warning context.
- [ ] Homoglyph, zero-width, base64-imperative, and markdown-smuggling fixture variants of a plain-text pattern all trigger the same rule via the normalization pipeline.
- [ ] The benchmark harness runs the full positive and negative corpora and reports counts; `high`-tier rules produce zero false positives on the negative corpus.
- [ ] This repo's pattern config, fixtures, and `docs/inspiration/` docs scan clean via the allowlist, and the allowlist + corpus files are denied to agent edits by the Phase 01 guard.
- [ ] WebFetch calls carrying known-secret-format payloads in URLs are denied; ambiguous high-entropy payloads produce `ask`; ordinary URLs pass untouched — each with fixtures, including the extended bash `curl`/`wget` vectors.
- [ ] A scanner exception fails closed (block with guard-error reason) and the override-file kill switch restores operation.
- [ ] Truncated outputs are scanned with the unscanned-tail notice attached, with a fixture.
- [ ] Codex and OpenCode each have either (a) passing equivalent-enforcement evidence, or (b) a written, evidence-backed platform-limitation entry with recorded user sign-off — no third state.
- [ ] Propagation emits scanner, corpus, allowlist, and wiring to a consuming project with the version marker; live manual QA verifies a real block, a real warn, and retry behavior in a Claude Code session.

## QA Considerations

- No UI changes; manual QA is live-session behavioral: one real block (suppression + reason visible), one real warn, retry behavior after a block, kill-switch recovery, and per-harness behavior on Codex/OpenCode per the parity outcome.
- Integration behavior changes intentionally: tool outputs can now be suppressed or annotated; Phase 01's bash exfil rules gain URL-payload inspection (regression fixtures required so existing `deny`/`ask` behavior is preserved).
- Warn-tier context is agent-visible text — QA must confirm warnings are informative without amplifying the injection content itself.

## Notes for Feature - Decomposer

Suggested feature boundaries (4, ordered):

1. **Scanner engine + normalization + response mapping** — framework consumer, no pattern content: payload handling for PostToolUse (a new event for this codebase — extend the Phase 01 fixture harness for it), normalization pipeline, severity→response engine, allowlist mechanics, truncation/binary/empty handling, fail-closed wiring. Keep the engine free of rule content, mirroring Phase 01's engine/config split.
2. **Pattern corpus + benchmark suite** — pure config + fixtures: author the tiered corpus category by category, build the positive/negative benchmark harness, tune against the zero-FP bar for `high`. Depends on 1. This is where the clean-room constraint bites hardest: authors work from the taxonomy in `PHASE_02_DISCOVERY_CONTEXT.md`, never from the surveyed repo's pattern file.
3. **WebFetch exfiltration guard** — PreToolUse rules + `bash_analyzer.py` extension. Depends on Phase 01's rule engine only, not on features 1–2; can run in parallel with 2. Shares tier semantics with the existing exfil rules — extend that config, don't fork it.
4. **Multi-harness parity + propagation** — investigation gate first (Codex/OpenCode output-interception contracts), then adapters/wiring or evidenced limitation sign-off; propagation emission for all Phase 02 artifacts. Depends on 1–3. Time-box the investigation; the sign-off fallback is a legitimate completion state.

Integration points to watch: the scanner (1) and guard (3) both emit through the Phase 01 framework's decision path — no bespoke JSON emission; the allowlist and corpus files must be registered in the Phase 01 protected-path config (feature 1 owns registering them); warn-context formatting is a contract between engine (1) and corpus reasons (2) — define the message schema once.

Clean-room reminder: `docs/inspiration/` files and the local survey checkout describe *what to cover and what weaknesses to beat* — never open `patterns.yaml` or hook source to copy patterns.
