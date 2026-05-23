import sys, json, fnmatch, os, re

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

tool = data.get('tool_name', data.get('name', ''))
inp  = data.get('tool_input', data.get('input', {}))

# ── File path patterns ────────────────────────────────────────────────────────
# Glob-style names matched against both the file basename and the full path.
FILE_PATTERNS = [
    # .env files (any variant)
    ".env", ".env.*",
    # SSH keys — exact names and wildcard for any key type
    "id_rsa", "id_rsa.pub",
    "id_ed25519", "id_ed25519.pub",
    "id_ecdsa", "id_ecdsa.pub",
    "id_dsa", "id_dsa.pub",
    "id_*",
    # Certs and private keys
    "*.pem", "*.key", "*.p12", "*.pfx", "*.crt", "*.cer", "*.der",
    # Generic secrets / credential files
    "secrets.json", "credentials.json", "service-account.json",
    "auth.json", "token.json",
    ".netrc", ".npmrc", ".pypirc",
    "config/production.json", "config/secrets",
    # Kubernetes
    "kubeconfig", "*.kubeconfig",
]

# Path substrings that indicate a protected location regardless of filename.
PROTECTED_PATH_SUBSTRINGS = [
    "/.ssh/",
    "/.aws/credentials",
    "/.aws/config",
    "/.kube/config",
    "/.kube/",
    "/.gnupg/",
    "/secrets/",
]

# ── Bash command patterns ─────────────────────────────────────────────────────
# Each entry: (compiled_regex, human_readable_reason)
BASH_COMMAND_PATTERNS = [
    # Environment variable dumps
    (re.compile(r'\bprintenv\b'),
     'printenv dumps all environment variables'),
    (re.compile(r'(?:^|[;&|])\s*env\s*(?:$|[;&|])'),
     '"env" with no arguments dumps all environment variables'),
    (re.compile(r'(?:^|[;&|])\s*set\s*(?:$|[;&|])'),
     '"set" with no arguments exposes all shell variables'),
    (re.compile(r'(?:^|[;&|])\s*export\s*(?:$|[;&|])'),
     '"export" with no arguments lists all exported variables'),
    # Echoing secret-looking env vars (3+ uppercase chars = likely a secret)
    (re.compile(r'echo\s+["\']?\$[A-Z_]{3,}'),
     'echoing env var may expose a secret (e.g. echo $API_KEY)'),
    # Direct cat of .env
    (re.compile(r'\bcat\b.*\.env'),
     'reading .env file contents via cat'),
    # curl exfiltration
    (re.compile(r'\bcurl\b.*@\.env'),
     'curl exfiltration using .env contents'),
    (re.compile(r'\bcurl\b.*-d\s+@\S'),
     'curl -d @<file> may exfiltrate file contents'),
    (re.compile(r'\bcurl\b.*--data[-\s]+@\S'),
     'curl --data @<file> may exfiltrate file contents'),
    # wget exfiltration
    (re.compile(r'\bwget\b.*--post-file'),
     'wget --post-file may exfiltrate file contents'),
    # base64 encoding secrets (common exfil step)
    (re.compile(r'\bbase64\b.*\.env'),
     'base64 encoding of .env file (potential exfiltration)'),
]

def check_file_path(path):
    """Return matched pattern/substring string, or empty string if safe."""
    if not path:
        return ''
    basename = os.path.basename(path)
    for p in FILE_PATTERNS:
        if fnmatch.fnmatch(basename, p) or fnmatch.fnmatch(path, p):
            return p
    for s in PROTECTED_PATH_SUBSTRINGS:
        if s in path:
            return s
    return ''

def deny(reason):
    print(json.dumps({
        'hookSpecificOutput': {
            'hookEventName': 'PreToolUse',
            'permissionDecision': 'deny',
            'permissionDecisionReason': reason,
        }
    }))
    sys.exit(0)

# ── File tools ────────────────────────────────────────────────────────────────
if tool in ('Read', 'Write', 'Edit', 'MultiEdit'):
    path = inp.get('file_path', '')
    matched = check_file_path(path)
    if matched:
        deny(f'Protected file access blocked. Pattern "{matched}" matched: {path}')

# ── Bash tool ─────────────────────────────────────────────────────────────────
elif tool == 'Bash':
    command = inp.get('command', '')

    # 1. Does the command reference a protected file path?
    matched = check_file_path(command)
    if matched:
        deny(f'Bash command references a protected file. Pattern "{matched}" matched in command: {command}')

    # 2. Does the command match a dangerous pattern?
    for regex, reason in BASH_COMMAND_PATTERNS:
        if regex.search(command):
            deny(f'Dangerous command blocked: {reason}. Command: {command}')

sys.exit(0)