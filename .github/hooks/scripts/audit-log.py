"""Fail-open PostToolUse audit entrypoint."""

import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
HOOKS_DIR = SCRIPT_DIR.parent
REPO_ROOT = HOOKS_DIR.parents[1]
LOG_FILE = REPO_ROOT / "dev" / "agent-audit.log"

try:
    sys.path.insert(0, str(HOOKS_DIR))
    from lib.framework import observability_guard, record_event
except Exception:
    observability_guard = None
    record_event = None


def main(input_stream=None, *, log_file=LOG_FILE) -> int:
    """Record allowlisted metadata and consume every observability failure."""

    if observability_guard is None or record_event is None:
        return 0

    def audit(event, _config) -> None:
        record_event(log_file, event, rule="audit-log", decision="observed")

    return observability_guard(audit, input_stream=input_stream)


if __name__ == "__main__":
    raise SystemExit(main())
