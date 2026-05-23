#!/usr/bin/env bash
# setup-hook-symlinks.sh
# Wire .claude/settings.json, .codex/hooks.json, and .opencode/plugins/*.js
# from this repo into their user-scoped runtime locations.
# Idempotent — safe to rerun.

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "==> Repo root: $REPO"

# ---------------------------------------------------------------------------
# 1. Claude: ~/.claude/settings.json -> <repo>/.claude/settings.json
# ---------------------------------------------------------------------------
echo ""
echo "--- Claude settings.json ---"
mkdir -p "$HOME/.claude"
target="$HOME/.claude/settings.json"
if [ -e "$target" ] && ! [ -L "$target" ]; then
  echo "  Backing up real file: $target.backup"
  mv "$target" "$target.backup"
fi
ln -sfn "$REPO/.claude/settings.json" "$target"
echo "  Linked: $target -> $(readlink "$target")"

# ---------------------------------------------------------------------------
# 2. Codex: ~/.codex/hooks.json -> <repo>/.codex/hooks.json
# ---------------------------------------------------------------------------
echo ""
echo "--- Codex hooks.json ---"
mkdir -p "$HOME/.codex"
target="$HOME/.codex/hooks.json"
if [ -e "$target" ] && ! [ -L "$target" ]; then
  echo "  Backing up real file: $target.backup"
  mv "$target" "$target.backup"
fi
ln -sfn "$REPO/.codex/hooks.json" "$target"
echo "  Linked: $target -> $(readlink "$target")"

# ---------------------------------------------------------------------------
# 3. OpenCode: ~/.config/opencode/plugins/<name>.js -> <repo>/.opencode/plugins/<name>.js
# ---------------------------------------------------------------------------
echo ""
echo "--- OpenCode plugins ---"
mkdir -p "$HOME/.config/opencode/plugins"
for js in "$REPO/.opencode/plugins/"*.js; do
  [ -f "$js" ] || continue
  name="$(basename "$js")"
  target="$HOME/.config/opencode/plugins/$name"
  if [ -e "$target" ] && ! [ -L "$target" ]; then
    echo "  Backing up real file: $target.backup"
    mv "$target" "$target.backup"
  fi
  ln -sfn "$js" "$target"
  echo "  Linked: $target -> $(readlink "$target")"
done

echo ""
echo "==> Done. Verify with:"
echo "    readlink ~/.claude/settings.json"
echo "    readlink ~/.codex/hooks.json"
echo "    ls -la ~/.config/opencode/plugins/"
