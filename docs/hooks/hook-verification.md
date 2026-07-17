# Hook Verification Checklist

## Automated checks

- Run framework, injection-scanner, corpus, distribution, and propagation tests.
- Assert the retired guard, rules, analyzers, rewrite hook, and generated plugin
  are absent.
- Assert Claude, Codex, and OpenCode retain the injection scanner and unrelated
  wiring.
- Run propagation twice and require a no-change second pass.
- Verify a same-named unowned file or symlink survives retirement cleanup.

## Manual checks — NOT RUN by automation

- Launch each supported harness and inspect its live hook roster.
- Send synthetic benign output and confirm no file-access decision or audit row
  is produced.
- Send a synthetic injection fixture and confirm the PostToolUse scanner blocks
  or redacts it without exposing the sentinel.
- Run an explicitly prefixed `rtk` command and confirm RTK remains available;
  confirm an unprefixed command is not automatically rewritten.

Prompt-injection scanning is **not a replacement** for the removed protected-file
or Bash-command enforcement.

## Observed evidence

The surviving framework still has independent regression coverage for structured
`deny` and `ask` decisions, the `exit code 2` fallback, `bypass-permissions`
payloads, and `subagent` context. Those framework contracts remain tested even
though no active repository file-access hook currently emits them.
