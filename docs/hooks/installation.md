# Hook Installation

`.github/hooks/` is the source of truth for the surviving shared framework,
prompt-injection scanner, audit hook, and completion notification hook. Run the
repository propagator to regenerate project wiring:

```bash
python3 scripts/propagate_master_assets.py --once
```

Run it again and require zero reported changes before treating generated output
as converged.

## Support matrix

| Harness | Status | Surviving behavior |
|---|---|---|
| Claude Code | Fully supported | Generated PostToolUse scanner, audit, and notification wiring |
| OpenCode | Partial | Generated scanner adapter; verify native runner behavior manually |
| Codex | Partial | Generated scanner wiring within the runner's hook surface |
| Cursor | Not supported | No native generated hook adapter |
| GitHub Copilot | Not supported | Source descriptors are not a live enforcement guarantee |

## Reduced security posture

The file-access guard, protected-file enforcement, Bash-command analyzer, and
automatic `rtk-rewrite.sh` registration were removed. Prompt-injection defense is
**not a replacement** for those controls. Direct file and Bash operations now
depend on the host harness, operating-system permissions, and human review.

RTK itself was not retired. Explicit `rtk`-prefixed commands remain valid and
recommended where the repository instructions call for them; only automatic
rewriting was removed.

## Project and global outputs

Project generation updates `.claude/settings.json`, `.codex/hooks.json`, and
`.opencode/plugins/` while preserving unrelated unowned entries. Generated
global installation must likewise preserve foreign content and remove only
ownership-proven stale outputs. Inspect changes before replacing user-global
configuration.

## Recovery and rollback

If a surviving generated hook fails, stop the affected runner, inspect the
generated command and source descriptor, regenerate once, and restart the
runner. Roll back the complete Phase 04 retirement unit if the removed
interceptor must be restored; do not resurrect a single stale registration.
