# Phase 01 Hook Installation

The shareable installation is the repository-local deployment generated from
`.github/hooks/`. It contains the Python entrypoint, standard-library framework,
Bash analyzer, path evaluator, default rules, protected project override, and
platform wiring. No virtual environment or package installation is required at
runtime.

## Support matrix

| Harness | Status | What is supported in this phase |
|---|---|---|
| Claude Code | Fully supported | Project and user-scope `PreToolUse` wiring, structured allow/ask/deny decisions, bypass-resistant deny policy, and the complete self-contained runtime. Claude documents project hooks in `.claude/settings.json`, user hooks in `~/.claude/settings.json`, and most-restrictive decision merging. |
| Codex | Partial | Project and user `hooks.json` files are generated at documented Codex config layers. The command contract is subprocess-tested, but live Codex decision handling and trust review were not exercised in this implementation run. Do not treat it as verified enforcement until the live checklist passes. |
| OpenCode | Partial | Project and global plugins are generated in OpenCode's documented plugin directories and use `tool.execute.before`. The current adapter launches the guard, but a live OpenCode blocking result was not verified and the adapter does not yet translate every structured decision into native OpenCode permission behavior. |
| Cursor | Not supported | Cursor has its own hooks system, but this phase emits no Cursor adapter and does not translate Cursor event or decision schemas. |
| GitHub Copilot | Not supported | Copilot CLI and cloud agent support `.github/hooks/*.json`, but this phase does not claim that the consolidated Claude-oriented decision adapter satisfies the current Copilot event/output contract. Treat `.github/hooks/` as this repository's source metadata, not verified Copilot enforcement. |

Primary references: [Claude Code hooks](https://code.claude.com/docs/en/hooks-guide),
[Codex advanced configuration and hooks](https://developers.openai.com/codex/config-advanced#hooks),
[OpenCode plugins](https://opencode.ai/docs/plugins/),
[Cursor hooks](https://cursor.com/docs/hooks), and
[GitHub Copilot hooks reference](https://docs.github.com/en/copilot/reference/hooks-reference).

## Per-project installation

From the source repository, run:

```bash
python3 scripts/propagate_master_assets.py --once
```

Commit the resulting `.github/hooks/`, `.claude/settings.json`,
`.codex/hooks.json`, and `.opencode/plugins/` files with the consuming project.
The committed commands are repository-relative. Verify the complete unit before
sharing it:

```bash
if [ ! -f .github/hooks/.distribution-version ]; then
  echo "ERROR: hook distribution marker is missing" >&2
  exit 1
fi
if [ ! -f .github/hooks/scripts/file-access-guard.py ]; then
  echo "ERROR: consolidated guard entrypoint is missing" >&2
  exit 1
fi
printf '%s\n' '{"tool_name":"Read","tool_input":{"file_path":".env"}}' \
  | python3 .github/hooks/scripts/file-access-guard.py
```

The final command must return one structured `deny` decision without printing
the file contents or the input body. Claude Code users can also run `/hooks` to
confirm the `PreToolUse` registration.

## Generated global installation

Global wiring is optional local coverage. Run:

```bash
bash scripts/setup-hook-symlinks.sh
```

The compatibility-named script no longer creates symlinks. It generates
machine-local absolute-path wiring under `.generated-global-hooks/` (gitignored),
backs up an existing destination once as `*.backup`, and installs regular files
under `~/.claude/`, `~/.codex/`, and `~/.config/opencode/plugins/`. Codex users
must review changed non-managed hooks through `/hooks` before relying on them.

To verify without silent path checks:

```bash
if [ -L "$HOME/.claude/settings.json" ]; then
  echo "ERROR: expected generated settings, found a symlink" >&2
  exit 1
fi
if ! grep -Fq "$(pwd)/.github/hooks/scripts/file-access-guard.py" \
  "$HOME/.claude/settings.json"; then
  echo "ERROR: Claude global wiring does not reference this checkout" >&2
  exit 1
fi
echo "Global Claude wiring references this checkout with an absolute path."
```

### Double firing

If project and global layers are active, both matching hooks run. The guard is
stateless, so repeated allow/ask/deny evaluations are functionally identical
and each invocation emits one decision. Claude Code documents that matching
hooks all run and the most restrictive result wins. Duplicate audit rows can
therefore occur; they remain redacted. Disable one layer if a single audit row
per tool call is operationally important.

## Upgrade and re-propagate

After updating `.github/hooks/`, rerun project propagation and inspect the
version marker and generated diff:

```bash
python3 scripts/propagate_master_assets.py --once
git diff -- .github/hooks/.distribution-version .claude/settings.json \
  .codex/hooks.json .opencode/plugins
```

Then rerun `bash scripts/setup-hook-symlinks.sh` on machines using global
wiring. Unchanged inputs are idempotent; changed runtime assets produce a new
`phase-01-sha256:` marker.

## Kill-switch recovery

The only kill switch is the protected project override. A human, outside the
guarded agent session, may temporarily write this to
`.github/hooks/config/file-access-overrides.json`:

```json
{"guard": {"enabled": false}}
```

Perform the repair, then restore `"enabled": true` or `{}` and repeat the deny
verification. There is deliberately no environment-variable bypass. See the
[file-access guard contract](file-access-guard.md) for override rules.

## Rollback

Use a human-controlled shell outside the guarded session. Revert the Phase 01
distribution commit with `git revert <commit>`, rerun propagation from the
restored source definitions, review the generated diff, and rerun the complete
test suite. For global wiring, restore a reviewed `*.backup` file or regenerate
from the known-good checkout. Re-enable the guard and verify `.env` is denied
before returning the project to agent use.

## Policy changes and Known Bash limitations

Legacy environment-disclosure matches (`printenv`, bare `env`, bare `set`, bare
`export`, and variable echo) are intentionally re-tiered to `ask`. Protected
literal credential paths and unsafe exfiltration operands remain `deny`;
destructive operations remain confirmation-tier. Denials now identify the rule
and a safe alternative without echoing command bodies or file contents.

The analyzer does not execute shell expansion or embedded interpreters and
cannot infer every recursive program walk. Review
[Known Bash limitations](bash-command-limitations.md) before treating it as a
general shell sandbox.
