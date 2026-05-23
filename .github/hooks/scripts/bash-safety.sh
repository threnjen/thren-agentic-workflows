#!/usr/bin/env bash
# .github/hooks/scripts/bash-safety.sh
#
# PreToolUse hook: gate destructive bash commands behind user confirmation.
# Based on the Anthropic Claude hooks article example.
#
# Input (stdin): JSON with tool name and tool input
# Output (stdout): JSON with permissionDecision (allow | ask | deny)
#
# Exit codes:
#   0  success (output JSON is used)
#   2  blocking error

set -euo pipefail

# Read full stdin into a variable
INPUT="$(cat)"

# Extract the command string from the tool input
# Handles both {"command":"..."} and {"input":{"command":"..."}} shapes
COMMAND="$(echo "$INPUT" | python3 -c "
import json, sys
data = json.load(sys.stdin)
cmd = data.get('input', data).get('command', '')
print(cmd)
" 2>/dev/null || echo "")"

# Patterns that warrant user confirmation before proceeding
DESTRUCTIVE_PATTERNS=(
  "rm -rf"
  "rm -fr"
  "git push --force"
  "git push -f"
  "git reset --hard"
  "git clean -f"
  "git clean -fd"
  "chmod -R 777"
  "dd if="
  "mkfs"
  "> /dev/"
  "truncate"
  "shred"
  "wipefs"
  "DROP TABLE"
  "DROP DATABASE"
)

# Check the command against each pattern
for pattern in "${DESTRUCTIVE_PATTERNS[@]}"; do
  if echo "$COMMAND" | grep -qiF "$pattern"; then
    # Gate: ask the user to confirm before allowing
    python3 -c "
import json
print(json.dumps({
  'hookSpecificOutput': {
    'hookEventName': 'PreToolUse',
    'permissionDecision': 'ask',
    'permissionDecisionReason': 'Potentially destructive command detected: \"$pattern\". Please confirm you want to proceed.'
  }
}))
"
    exit 0
  fi
done

# No match — allow the command through silently
python3 -c "
import json
print(json.dumps({
  'hookSpecificOutput': {
    'hookEventName': 'PreToolUse',
    'permissionDecision': 'allow'
  }
}))
"
exit 0
