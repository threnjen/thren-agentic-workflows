# Prompt-Injection Defense

The surviving PostToolUse scanner evaluates untrusted tool output using the
rules in `.github/hooks/config/injection-patterns.json` and the source allowlist
in `.github/hooks/config/injection-allowlist.json`. It can suppress or redact
matched output before that output returns to model context.

## Release status

The scanner, shared framework, source descriptor, audit hook, and notification
hook remain active after Phase 04 interceptor retirement. Their focused
regression suites are the automated evidence; live harness checks remain manual.

## Reduced security posture

The file-access guard, protected-file policy, Bash analyzer, guard-only URL
exfiltration logic, and automatic RTK rewrite hook were removed. Prompt-injection
defense is **not a replacement** for file authorization, Bash-command enforcement,
credential controls, sandboxing, or operating-system permissions.

The scanner judges output, not whether a requested file or command should be
allowed. A benign scanner result therefore says nothing about file sensitivity or
command safety.

## Verification

- Run the scanner unit and corpus suites.
- Propagate twice and inspect scanner wiring in Claude, Codex, and OpenCode.
- Verify malicious synthetic output is redacted without retaining sentinels.
- Verify benign output remains usable.
- Confirm no documentation or generated wiring claims the scanner restores the
  retired file-access boundary.

Rollback the scanner independently only for a scanner defect. Restoring the
retired file-access system requires reverting its complete retirement unit.
