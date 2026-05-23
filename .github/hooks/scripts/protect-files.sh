#!/usr/bin/env bash
# .github/hooks/scripts/protect-files.sh
#
# PreToolUse hook: block read, write, edit, or bash access to protected files
# and dangerous commands that can expose secrets.
#
# Covers:
#   - .env files and variants
#   - SSH keys (~/.ssh/id_*)
#   - AWS credentials (~/.aws/credentials, ~/.aws/config)
#   - Kubernetes configs (~/.kube/config, *.kubeconfig)
#   - Common secrets/credential file patterns
#   - Bash commands that dump or exfiltrate secrets (printenv, env, echo $VAR, curl exfil, etc.)
#
# Input (stdin): JSON with tool name and tool input
# Output (stdout): JSON with permissionDecision deny, or nothing (allow)
#
# Exit codes:
#   0  success (output JSON is used)
#   2  blocking error

set -euo pipefail

# All matching logic is done in Python to avoid BSD/GNU shell differences.
# Python reads the full tool input, checks file patterns and bash command patterns,
# and either prints a deny JSON object or nothing (allow).
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

DENY_OUTPUT="$(cat | python3 "$SCRIPT_DIR/protect-files.py")"

if [ -n "$DENY_OUTPUT" ]; then
  echo "$DENY_OUTPUT"
  exit 0
fi

exit 0
