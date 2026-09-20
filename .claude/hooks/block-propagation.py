#!/usr/bin/env python3
"""Block agent-initiated propagation and deployment.

Two scripts propagate: scripts/propagate_master_assets.py, and deploy_agents.py,
which propagates into ports/ before copying out of it. Both are the maintainer's
manual step. deploy_agents.py additionally writes outside this repository, into
the user's live harness config directories (~/.claude, ~/.codex, ~/.cursor,
~/.config/opencode) and rewrites their global instruction files. See CLAUDE.md,
"Agents: never run propagation".

PreToolUse contract: the tool payload arrives as JSON on stdin. Exit 2 blocks the
call and returns stderr to the agent; exit 0 allows it.

Only EXECUTION is blocked. Reading, grepping, or otherwise inspecting either
script stays allowed, so agents can still reason about their behavior.
"""

import json
import re
import sys

MESSAGE = """\
BLOCKED: propagation and deployment are the maintainer's manual step and must not
be run by an agent.

scripts/propagate_master_assets.py regenerates every file under ports/ and
.github/. deploy_agents.py does that too, and then writes outside this repository
into the user's live harness config directories, rewriting their global
instruction files. Neither is reversible from inside a session. See CLAUDE.md,
'Agents: never run propagation'.

Edit source_of_truth/ only, then STOP and report that deployment is pending. To
see what propagation would produce, propagate into a scratch directory instead:
scripts/propagate_master_assets.py --target DIR. The tests build their own
propagated tree, so they do not need a propagated ports/ in this repository.
"""

# An execution looks like an interpreter (or ./) reaching either script,
# optionally preceded by VAR=val assignments, at the start of the command or
# after a separator. Anchoring on the separator is what lets
# `grep ... propagate...` pass.
EXEC = re.compile(
    r"""(?:^|[|;&\n]|\$\(|`)\s*
        (?:[A-Za-z_][A-Za-z0-9_]*=\S+\s+)*
        (?:python3?|uv\s+run|uvx|poetry\s+run|pipenv\s+run|sh|bash|zsh|\./)
        [^|;&\n]*(?:propagate_master_assets|deploy_agents)""",
    re.VERBOSE,
)


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0  # unparseable payload: fail open, never wedge the session

    command = (payload.get("tool_input") or {}).get("command") or ""
    if not any(name in command for name in ("propagate_master_assets", "deploy_agents")):
        return 0
    if not EXEC.search(command):
        return 0  # inspection, not execution

    sys.stderr.write(MESSAGE)
    return 2


if __name__ == "__main__":
    sys.exit(main())
