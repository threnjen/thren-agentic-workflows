# Codex macOS Setup And Symlinks

This guide documents the macOS runtime targets that Codex uses and shows how to point those runtime locations back to repository-owned source artifacts under `codex/`.

This feature is documentation-only. It does not create any live files in a user home directory, and the repository-owned source examples below are future-facing placeholders until later Phase 02 work lands the corresponding artifacts.

## Global AGENTS Policy

If you later port AGENTS-derived guidance into Codex, install that content into the global Codex AGENTS layer under `~/.codex/AGENTS.md` or `~/.codex/AGENTS.override.md`.

Do not install Codex guidance by pointing either runtime location at this repository's checked-in `AGENTS.md` or the sibling repository's checked-in `AGENTS.md`. Those files are not the runtime destination for Codex guidance in this phase.

## Source Versus Runtime On macOS

Keep the authoring surface and the runtime surfaces separate:

| Surface | Role |
|---------|------|
| `codex/` | Repository-owned authoring area for Codex docs and future source artifacts |
| `.codex/` | Repo-scoped runtime config or installed runtime assets |
| `~/.codex/` | User-scoped runtime config, global AGENTS guidance, and custom agents |
| `$HOME/.agents/skills/` | User-scoped installed Codex skills |

The symlink direction in this guide always flows from a runtime destination back to a repository-owned source path under `codex/`.

## Runtime Targets

These are the macOS locations that matter for this setup flow.

| Runtime target | Scope | Purpose | Repository-owned source example |
|----------------|-------|---------|---------------------------------|
| `~/.codex/config.toml` | User | Global Codex config | Not linked in this feature |
| `~/.codex/AGENTS.md` | User | Global Codex guidance when no home override exists | `$REPO_ROOT/codex/global-agents/AGENTS.md` |
| `~/.codex/AGENTS.override.md` | User | Higher-precedence global Codex guidance | `$REPO_ROOT/codex/global-agents/AGENTS.override.md` |
| `~/.codex/agents/example-agent.toml` | User | Installed custom-agent TOML file | `$REPO_ROOT/codex/agents/example-agent.toml` |
| `$HOME/.agents/skills/example-skill` | User | Installed skill directory | `$REPO_ROOT/codex/skills/example-skill` |

The source examples are intentionally placeholders. Replace them with the real repository-owned Codex artifact paths once those files or directories exist.

## Preflight Checks

Before replacing anything under `~/.codex/` or `$HOME/.agents/skills/`, inspect the current state and verify that the future source path exists.

```sh
REPO_ROOT=/absolute/path/to/github-agents-source-of-truth

ls -ld "$HOME/.codex" "$HOME/.codex/agents" "$HOME/.agents" "$HOME/.agents/skills" 2>/dev/null || true
ls -l "$HOME/.codex/AGENTS.md" "$HOME/.codex/AGENTS.override.md" "$HOME/.codex/agents/example-agent.toml" "$HOME/.agents/skills/example-skill" 2>/dev/null || true
readlink "$HOME/.codex/AGENTS.md" 2>/dev/null || true
readlink "$HOME/.codex/AGENTS.override.md" 2>/dev/null || true
readlink "$HOME/.codex/agents/example-agent.toml" 2>/dev/null || true
readlink "$HOME/.agents/skills/example-skill" 2>/dev/null || true

test -e "$REPO_ROOT/codex/global-agents/AGENTS.md"
test -e "$REPO_ROOT/codex/global-agents/AGENTS.override.md"
test -e "$REPO_ROOT/codex/agents/example-agent.toml"
test -e "$REPO_ROOT/codex/skills/example-skill"
```

If any runtime target is a real file or directory instead of a symlink, move it aside manually before relinking so the replacement is explicit and reversible.

## Parent Directories For A Clean Machine

Create parent directories first so the later symlink commands work on a clean macOS machine.

```sh
mkdir -p "$HOME/.codex"
mkdir -p "$HOME/.codex/agents"
mkdir -p "$HOME/.agents/skills"
```

## Idempotent Symlink Examples

The following examples use `ln -sfn` so rerunning the command updates an existing symlink target without creating duplicate links. Replace the placeholder source paths with the real repository-owned Codex artifact paths before using them.

```sh
REPO_ROOT=/absolute/path/to/github-agents-source-of-truth

ln -sfn "$REPO_ROOT/codex/global-agents/AGENTS.md" \
  "$HOME/.codex/AGENTS.md"

ln -sfn "$REPO_ROOT/codex/global-agents/AGENTS.override.md" \
  "$HOME/.codex/AGENTS.override.md"

ln -sfn "$REPO_ROOT/codex/agents/example-agent.toml" \
  "$HOME/.codex/agents/example-agent.toml"

ln -sfn "$REPO_ROOT/codex/skills/example-skill" \
  "$HOME/.agents/skills/example-skill"
```

These commands are idempotent only when the destination is absent or already a symlink. If the destination is a regular file or directory, inspect it first and replace it deliberately rather than relying on `ln -sfn` to decide for you.

## Replace Or Roll Back Safely

If a destination already exists as a non-symlink, back it up first.

```sh
mv "$HOME/.codex/AGENTS.md" "$HOME/.codex/AGENTS.md.backup"
mv "$HOME/.codex/AGENTS.override.md" "$HOME/.codex/AGENTS.override.md.backup"
mv "$HOME/.codex/agents/example-agent.toml" "$HOME/.codex/agents/example-agent.toml.backup"
mv "$HOME/.agents/skills/example-skill" "$HOME/.agents/skills/example-skill.backup"
```

If you want to undo the symlinked setup later, remove the symlink and either restore the backup or create a new link to a different repository-owned source path.

```sh
rm "$HOME/.codex/AGENTS.md"
rm "$HOME/.codex/AGENTS.override.md"
rm "$HOME/.codex/agents/example-agent.toml"
rm "$HOME/.agents/skills/example-skill"
```

After any relink or rollback step, verify the target again.

```sh
ls -l "$HOME/.codex/AGENTS.md" "$HOME/.codex/AGENTS.override.md" "$HOME/.codex/agents/example-agent.toml" "$HOME/.agents/skills/example-skill"
readlink "$HOME/.codex/AGENTS.md"
readlink "$HOME/.codex/AGENTS.override.md"
readlink "$HOME/.codex/agents/example-agent.toml"
readlink "$HOME/.agents/skills/example-skill"
```

## What This Guide Does Not Do

- It does not create the future repository-owned Codex artifacts under `codex/`.
- It does not install anything automatically into `~/.codex/` or `$HOME/.agents/skills/`.
- It does not treat `codex/` as a runtime mirror of either repository's checked-in `AGENTS.md` files.

Use this guide as the installation contract once later Phase 02 work creates the actual repository-owned Codex sources that these runtime symlinks should target.