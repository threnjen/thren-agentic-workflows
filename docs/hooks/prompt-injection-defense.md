# Prompt-Injection Defense

Phase 02 scans successful tool output with the shared, standard-library hook
runtime before the next model turn. The clean-room rule corpus lives in
`.github/hooks/config/injection-patterns.json`; normalization, bounded decoding,
strongest-match selection, and allowlisting live in the shared scanner module.

## Release status

**NO-GO:** Phase 02 is implemented but is not approved for release or promotion
to manual sign-off. The final security and production reviews found three
introduced High-severity bypasses:

- **P2-SEC-01:** attacker-controlled structured mapping keys can survive the
  nominal block replacement.
- **P2-SEC-02:** content beyond the scan-byte cap or encoded-candidate limit can
  remain model-visible without being assessed.
- **P2-SEC-03:** mutable directory-wide source allowlists can bypass scanning.

The accepted Codex coverage limitation and PERF-01 latency risk do not cover
these findings. Live Claude Code, Codex, and OpenCode QA remains `NOT RUN`. See
`../phases/PHASE_02/PHASE_02-qa-analysis.md` and
`../phases/PHASE_02/PHASE_02-security-scan.md` for authoritative evidence and
the required re-entry sequence.

## Intended and automated enforcement

- High-tier rules replace model-visible output with a redacted category/rule
  explanation and no-retry/manual-inspection guidance.
- Medium/low rules preserve logical output and append redacted warning context.
- Truncated or scan-capped inputs are assessed over available content and carry
  an unscanned-tail notice.
- Scanner/config/emission failures fail closed with `guard error`; the only
  recovery bypass is the protected, human-edited project override.
- Allowlisting is restricted to repository-owned, existing, non-symlinked paths
  under fixed approved roots. Runtime, corpus, allowlist, wiring, and generated
  plugins are protected from agent writes.

These bullets describe the intended behavior and passing automated contract
coverage, not a release guarantee. P2-SEC-01 through P2-SEC-03 identify cases
where the current implementation does not uphold that behavior.

## Current harness contract evidence

Evidence was captured 2026-07-15 with Claude Code 2.1.210, Codex 0.144.4,
OpenCode 1.16.2, and Bun 1.3.14.

| Harness | Contract and result | Classification |
|---|---|---|
| Claude Code | PostToolUse `updatedToolOutput` replaces built-in results, `updatedMCPToolOutput` replaces MCP results, and `additionalContext` warns. Payload-level replacement tests pass. | Fully supported; live UI/no-retry QA NOT RUN |
| OpenCode | `tool.execute.after` exposes mutable `output.output`. The Bun adapter passes replacement, warning, redaction, and fail-closed checks. | Fully supported by automated contract evidence; live QA NOT RUN |
| Codex | PostToolUse accepts `tool_response` and native block feedback replaces Bash/apply_patch/MCP results. Current handlers do not provide equivalent Read/Grep/WebFetch/WebSearch/Task coverage. | Partial platform limitation; residual risk APPROVED 2026-07-15 |
| Cursor | No adapter is emitted. | Not supported |
| GitHub Copilot | Source metadata is not claimed as a verified Copilot adapter. | Not supported |

Primary references: Claude Code hooks at
`https://code.claude.com/docs/en/hooks`, Codex hooks at
`https://learn.chatgpt.com/docs/hooks` and the `openai/codex` hook runtime, and
OpenCode plugin types at `anomalyco/opencode`'s `packages/plugin/src/index.ts`.

## Verification and benchmark

```bash
.venv/bin/python -m pytest tests/hooks/test_injection_scanner.py \
  tests/hooks/test_injection_corpus.py
.venv/bin/python tests/hooks/injection_benchmark.py
.venv/bin/python -m pytest tests/test_propagate_master_assets.py \
  tests/hooks/test_hook_distribution_integration.py
```

The fixed Phase 01 50 ms subprocess budget is still a release prerequisite.
Feature 07 reproduced failures from 117 to 383 ms median and did not weaken the
threshold. **User approval in phase-execute session** explicitly accepted
proceeding with this unresolved PERF-01 risk on 2026-07-15; the gate remains
failed. SEC-01 intermediate-directory containment is reproduced green.

## Known boundaries

- Detection is deterministic regex/fixed-string defense in depth, not semantic
  understanding; novel or sufficiently transformed instructions can evade it.
- Failed tool results use a separate event and are outside this phase.
- A pattern divided across the runner's truncation boundary cannot be detected.
- Bash URL analysis handles literal curl/wget operands, not arbitrary shell
  expansion or embedded interpreters.
- Codex full tool parity is unavailable. **User approval in phase-execute
  session** accepted this residual risk on 2026-07-15; the platform remains
  Partial and live checks remain NOT RUN.

## Recovery and rollback

A human outside the guarded session may disable the protected project override,
restore a reviewed source/runtime revision, rerun propagation, inspect the
generated diff and version marker, restore the override, and verify both a
protected-file denial and a high-tier replacement. Never edit generated wiring
directly or add an environment-variable bypass.
