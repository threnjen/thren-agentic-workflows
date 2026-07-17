#!/usr/bin/env bash
# Generate user-scoped hook wiring with absolute source paths.
# The historical filename is retained for compatibility with existing setup docs.

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUTPUT="${HOOK_GLOBAL_OUTPUT_DIR:-$REPO/.generated-global-hooks}"

backup_once() {
  local target="$1"
  if [ -L "$target" ]; then
    rm "$target"
  elif [ -e "$target" ] && [ ! -e "$target.backup" ]; then
    cp -p "$target" "$target.backup"
    echo "  Backed up: $target.backup"
  fi
}

install_generated_file() {
  local source="$1"
  local target="$2"
  if [ ! -f "$source" ]; then
    echo "ERROR: generated hook output is missing: $source" >&2
    return 1
  fi
  mkdir -p "$(dirname "$target")"
  backup_once "$target"
  cp "$source" "$target"
  echo "  Installed: $target"
}

echo "==> Generating absolute hook wiring from: $REPO"
python3 "$REPO/scripts/propagate_master_assets.py" --global-output "$OUTPUT"

echo "==> Installing Claude Code and Codex settings"
install_generated_file "$OUTPUT/.claude/settings.json" "$HOME/.claude/settings.json"
install_generated_file "$OUTPUT/.codex/hooks.json" "$HOME/.codex/hooks.json"

echo "==> Installing OpenCode plugins"
mkdir -p "$HOME/.config/opencode/plugins"
for target in "$HOME/.config/opencode/plugins/"*.js; do
  [ -f "$target" ] || continue
  name="$(basename "$target")"
  if [ ! -f "$OUTPUT/.opencode/plugins/$name" ] \
    && head -n 1 "$target" | grep -q '^// Generated from .github/hooks source-of-truth'; then
    rm "$target"
    echo "  Removed stale generated plugin: $target"
  fi
done
for source in "$OUTPUT/.opencode/plugins/"*.js; do
  [ -f "$source" ] || continue
  install_generated_file "$source" "$HOME/.config/opencode/plugins/$(basename "$source")"
done

echo "==> Hook setup complete"
echo "    Local generated output: $OUTPUT"
echo "    Commands in installed wiring use absolute paths; no user files are symlinks."
