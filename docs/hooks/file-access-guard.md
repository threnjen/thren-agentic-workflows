# File-Access Guard Retirement

The repository file-access guard was removed in Phase 04. Direct file operations
and Bash commands are no longer inspected, prompted, denied, or audited by a
repository-owned protected-file policy.

The prompt-injection scanner remains active after tool execution. It assesses
untrusted tool output for indirect-injection patterns; it is **not a replacement**
for file-access authorization, protected-file enforcement, or Bash-command
policy.

Automatic command rewriting through `rtk-rewrite.sh` was also retired. The RTK
executable itself remains supported, and commands may still be explicitly
prefixed with `rtk` where repository guidance recommends it.

## Verification

- Generated Claude, Codex, and OpenCode wiring has no `file-access-guard` source.
- The retired runtime, rules, overrides, Bash analyzer, URL-exfiltration helper,
  automatic RTK hook, and guard-only tests are absent.
- Framework, injection-scanner, audit, and notification tests continue to run.
- Repeated propagation reaches a no-change pass without deleting unowned files.

Rollback requires reverting the Phase 04 retirement commit as one unit. Do not
restore only a descriptor or entrypoint: the retired integration depended on its
runtime libraries, policy configuration, generated wiring, and tests.
