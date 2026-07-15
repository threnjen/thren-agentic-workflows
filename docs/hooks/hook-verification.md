# Hook Verification Checklist

This checklist separates deterministic framework evidence from checks that need
a live harness session. Run live checks only in a disposable checkout with
no credentials, secrets, network access, or writable paths outside the checkout.

## Automated checks

Run:

```bash
.venv/bin/python -m pytest tests/hooks/
.venv/bin/python -m pytest tests/test_propagate_master_assets.py \
  tests/hooks/test_hook_distribution_integration.py
```

The suite verifies structured `deny` and `ask` decisions, the exit code 2
blocking fallback, security fail-closed behavior, observability fail-open
behavior, payload aliases, and content redaction. They also verify complete
propagation, nested destination containment, Claude replacement, Codex payload
aliases, and the generated OpenCode adapter under Bun. These checks do not
establish how a particular live runner presents a decision.

Verify emitted targets non-silently:

```bash
for path in \
  .github/hooks/scripts/injection-scanner.py \
  .github/hooks/lib/injection_scanner.py \
  .github/hooks/config/injection-patterns.json \
  .github/hooks/config/injection-allowlist.json \
  .opencode/plugins/injection-scanner.js; do
  test -f "$path" || { echo "ERROR: missing $path" >&2; exit 1; }
done
grep -Fq '"$source": "injection-scanner"' .claude/settings.json || exit 1
grep -Fq '"$source": "injection-scanner"' .codex/hooks.json || exit 1
echo "Phase 02 scanner assets and generated wiring are present."
```

## Live bypass-permissions checklist

1. Create a disposable checkout and copy in a temporary PreToolUse hook that
   returns a structured `deny` for a harmless Read target.
2. Start Claude Code with
   `--permission-mode bypassPermissions --dangerously-skip-permissions` and ask
   it to read that target.
3. Confirm the Read does not occur and record the runner version, command,
   output, and timestamp below.
4. Replace the temporary result with structured `ask`, repeat the call, and
   record whether bypass mode allows, prompts, or blocks it. `ask` must not be
   reported as equivalent to `deny`.
5. Replace the temporary result with a redacted stderr message and exit code 2.
   Confirm the call blocks and only the redacted reason is shown.

## Live subagent checklist

1. In the same disposable checkout, register a harmless PreToolUse hook that
   records only tool name and rule identifier.
2. Ask the main session to delegate a Read call to a subagent.
3. Confirm the hook record contains the subagent's call, with no prompt, file,
   command, or response body.
4. Record the runner version, exact command, timestamp, and redacted result.

## Observed evidence

| Check | Status | Evidence |
|---|---|---|
| Payload-level structured `deny` and `ask` | PASS | `tests/hooks/test_hook_framework.py` decision-emitter tests |
| Payload-level exit code 2 fallback | PASS | `test_denial_can_use_exit_code_two_fallback` |
| Security malformed/exception path | PASS | `test_security_guard_fails_closed_with_redacted_denial` |
| Observability malformed/exception path | PASS | `test_observability_guard_fails_open_without_output` and audit-path tests |
| Bash protected-file `deny` | PASS | `test_ac8_guard_entrypoint_emits_one_strongest_decision` payload-level evidence |
| Bash `ask` in bypass-permissions mode | NOT RUN | Requires an explicitly isolated live Claude Code session; do not infer runner behavior |
| Bash decision redaction inspection | PASS | Bash analyzer malformed-input and exfiltration redaction tests |
| Live `deny` in bypass-permissions mode | NOT RUN | Requires an explicitly isolated live Claude Code session |
| Live `ask` in bypass-permissions mode | NOT RUN | Requires an explicitly isolated live Claude Code session |
| Live exit code 2 fallback | NOT RUN | Requires an explicitly isolated live Claude Code session |
| Live subagent tool call | NOT RUN | Requires an explicitly isolated live Claude Code session |
| Live OpenCode replacement/warning | NOT RUN | Bun adapter smoke passes; run OpenCode 1.16.2 in a disposable checkout |
| Live Codex Bash/MCP PostToolUse | NOT RUN | Codex 0.144.4 contract is supported; full phase tool coverage is unavailable |
| Codex full-parity sign-off | APPROVED | User approval in phase-execute session on 2026-07-15; Partial classification remains |
| PERF-01 fixed 50 ms budget | FAIL | Reproduced at 117–383 ms medians on 2026-07-15 |
| PERF-01 unresolved-risk acceptance | APPROVED | User approval in phase-execute session on 2026-07-15; failure remains unresolved |

Do not convert a `NOT RUN` row to `PASS` without attaching the observed command,
runner version, timestamp, and redacted outcome.
