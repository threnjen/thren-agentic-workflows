#!/usr/bin/env python3
"""Block agent-initiated runs of scripts/propagate_master_assets.py.

Why: propagation is the maintainer's manual step. When an agent runs it, every
file under ports/ and .github/ is regenerated, which swamps the diff and makes
authored source changes impossible to review. See CLAUDE.md, "Agents: never run
propagation".

PreToolUse contract: the tool payload arrives as JSON on stdin. Exit 2 blocks the
call and returns stderr to the agent; exit 0 allows it.

Only EXECUTION is blocked. Reading, grepping, or otherwise inspecting the script
stays allowed, so agents can still reason about propagation behavior.
"""

import json
import re
import sys

MESSAGE = """\
BLOCKED: propagation is the maintainer's manual step and must not be run by an agent.

Running scripts/propagate_master_assets.py regenerates every file under ports/ and
.github/, which swamps the diff and makes authored source changes impossible to
review. See CLAUDE.md, 'Agents: never run propagation'.

Edit source_of_truth/ only, then STOP and report that propagation is pending.
Sync tests and any test reading ports/ will fail until the maintainer propagates.
That is expected and correct - say so plainly rather than propagating to go green.
"""

# An execution looks like an interpreter (or ./) reaching the script, optionally
# preceded by VAR=val assignments, at the start of the command or after a
# separator. Anchoring on the separator is what lets `grep ... propagate...` pass.
EXEC = re.compile(
    r"""(?:^|[|;&\n]|\$\(|`)\s*
        (?:[A-Za-z_][A-Za-z0-9_]*=\S+\s+)*
        (?:python3?|uv\s+run|uvx|poetry\s+run|pipenv\s+run|sh|bash|zsh|\./)
        [^|;&\n]*propagate_master_assets""",
    re.VERBOSE,
)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0  # unparseable payload: fail open, never wedge the session

    command = (payload.get("tool_input") or {}).get("command") or ""
    if "propagate_master_assets" not in command:
        return 0
    if not EXEC.search(command):
        return 0  # inspection, not execution

    sys.stderr.write(MESSAGE)
    return 2


if __name__ == "__main__":
    sys.exit(main())
