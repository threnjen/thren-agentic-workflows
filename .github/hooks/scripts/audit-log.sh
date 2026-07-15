#!/usr/bin/env bash
# .github/hooks/scripts/audit-log.sh
#
# PostToolUse hook: append one NDJSON line per tool call to dev/agent-audit.log.
# All logic lives in audit-log.py alongside this script.
#
# Input (stdin): JSON with tool_name, tool_input, tool_response
# Output: none (fire-and-forget; never blocks the agent)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

python3 "$SCRIPT_DIR/audit-log.py" || true

exit 0
