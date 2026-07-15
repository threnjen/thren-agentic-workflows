# Phase 02 Hook Distribution Manual QA

Evidence date: 2026-07-15. No secret-bearing payloads are stored in this
artifact. Test payloads use synthetic paths and redacted sentinels only.

## Temporary consuming project

The installation path was exercised in an isolated temporary consuming project
by calling `propagate_hooks_once(repo_root=<temporary>, source_root=<checkout>)`,
then launching the exact relative command emitted in its
`.claude/settings.json` from the temporary project directory.

Input shape:

```json
{"tool_name":"Read","tool_input":{"file_path":".env"},"cwd":"<temporary-consumer>"}
```

Observed: deny, exit code `0`, one structured JSON line, empty stderr. The
consumer contained its own scripts, framework, analyzer, rules, override, and
version marker; it required no pip install, virtual environment, or symlink.
Automated evidence is in
`test_propagated_guard_runs_from_detached_consumer_without_dependencies` and
`tests/hooks/test_hook_distribution_integration.py`.

## Automated integration evidence

| Check | Result | Evidence |
|---|---|---|
| Upstream framework, path guard, and Bash parity | Pass | `uv run --with pytest pytest -q tests/hooks` — 220 passed after consolidation |
| Existing propagation suite plus new distribution cases | Pass | `python3 -m unittest discover -s tests -v` — 8 passed |
| Representative allow/ask/deny subprocess paths | Pass | Three real propagated entrypoint cases |
| Self-protection | Pass | Scripts, framework, analyzer, rules, override, Claude/Codex wiring, and OpenCode plugin all denied on Write |
| Redaction | Pass | Synthetic secret sentinel absent from stdout, stderr, and NDJSON audit output |
| Project plus global command forms | Pass | Both relative and absolute invocations returned the same decision with one output line each |
| Historical Phase 01 guard latency claim | Superseded | The fresh Phase 02 prerequisite reproduction below is authoritative |
| Phase 02 combined detached smoke | Pass | Scanner block/warn/truncation/allowlist plus WebFetch and Bash deny/ask/allow |
| Claude high-output replacement | Pass (payload level) | `updatedToolOutput` is redacted and the original sentinel is absent |
| Codex response alias | Pass (payload level) | `tool_response` normalizes and native block feedback is emitted |
| OpenCode adapter | Pass (Bun smoke) | High output is replaced; warnings preserve output and append redacted context |
| SEC-01 intermediate containment | Pass | Symlinked `.github/hooks/config` is rejected before an outside write |
| PERF-01 fixed 50 ms gate | **Fail** | 2026-07-15 runs observed 117–383 ms medians; threshold was not weakened |

## Runner-constrained live evidence

These checks were not inferred from payload-level tests.

| Check | Status | Reason / next action |
|---|---|---|
| Live Claude Code UI project hook | Not run | Requires launching an installed Claude Code runner in a disposable checkout. |
| `bypassPermissions` deny | Not run | Run the documented harmless `.env` read in a disposable live session and record runner version, timestamp, and redacted result. |
| `bypassPermissions` ask | Not run | Exercise a harmless ask-tier command separately; do not equate ask with deny. |
| Subagent tool call | Not run | Delegate a harmless protected Read and record only tool name, rule identifier, and decision. |
| Global plus project UI message clarity | Not run | Enable both layers in a disposable HOME and confirm the live runner presents one effective denial clearly. |
| Live Codex trust and decision handling | Not run | Review through `/hooks` and invoke synthetic deny cases. Current official docs already establish that `permissionDecision: "ask"` is unsupported and continues the call, and that `apply_patch` reports a command-shaped input this guard does not yet translate; keep Codex Partial until an adapter and live evidence close both gaps. |
| Live OpenCode blocking | Not run | Confirm native blocking/approval behavior before promoting OpenCode beyond Partial. |

## Current harness evidence and sign-off

| Harness | Runner | Automated state | Live state | Decision |
|---|---|---|---|---|
| Claude Code | 2.1.210 | Equivalent block/warn replacement passes | NOT RUN | Supported; no-retry confirmation pending |
| OpenCode | 1.16.2 / Bun 1.3.14 | Equivalent mutable-output adapter passes | NOT RUN | Supported by contract and adapter evidence |
| Codex | 0.144.4 | Bash/apply_patch/MCP replacement supported | NOT RUN | Full output-tool parity unavailable |

Required Codex residual-risk decision: **PENDING — no sign-off has been
inferred.** Acceptance must record the user, date, exact runner version, and:
“I accept that Codex Phase 02 scanning covers Bash, apply_patch, and MCP
PostToolUse results but not the phase's complete successful-output tool set.”
Without that record, AC2 remains incomplete.

The detailed live procedure remains in [Hook Verification Checklist](hook-verification.md).

## Recovery walkthrough

1. From a human-controlled shell outside the guarded session, set
   `{"guard":{"enabled":false}}` in the protected project override.
2. Verify the entrypoint returns `allow` with the reason `guard disabled by
   project override` for the synthetic protected payload.
3. Repair or roll back the source and rerun project/global propagation.
4. Restore `{}` (or `{"guard":{"enabled":true}}`) in the override.
5. Verify the same synthetic `.env` payload returns `deny` before resuming agent
   work.

This walkthrough is documented but was not performed by disabling the guard in
the active development checkout. The underlying kill-switch behavior is covered
by the framework and file-access-guard automated tests.
