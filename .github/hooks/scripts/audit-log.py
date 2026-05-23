import sys, json, datetime, os

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)  # malformed input — skip silently

tool_name  = data.get('tool_name',  data.get('toolName',  'unknown'))
tool_input = data.get('tool_input', data.get('toolInput', {}))
tool_resp  = data.get('tool_response', data.get('toolResponse', {}))

# Resolve log path relative to repo root (this script lives in .github/hooks/scripts/)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT  = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..'))
LOG_FILE   = os.path.join(REPO_ROOT, 'dev', 'agent-audit.log')

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)


def truncate(obj, max_len=200):
    """Serialise obj to JSON and truncate if too long."""
    s = json.dumps(obj)
    return s if len(s) <= max_len else s[:max_len] + '…'


# # Extract a useful exit/status code if present
# exit_code = (
#     tool_resp.get('exit_code') or
#     tool_resp.get('exitCode') or
#     tool_resp.get('status')
# )

entry = {
    'ts':            datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    'tool':          tool_name,
    'input_summary': truncate(tool_input),
}
# if exit_code is not None:
#     entry['exit_code'] = exit_code

with open(LOG_FILE, 'a') as f:
    f.write(json.dumps(entry) + '\n')

sys.exit(0)
