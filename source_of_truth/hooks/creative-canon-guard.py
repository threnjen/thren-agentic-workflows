#!/usr/bin/env python3
"""Deny every programmatic write into a writer's canon/ or drafts/.

Why: the creative toolkit's central promise is that no agent ever touches the
writer's actual prose. Tool grants are all-or-nothing and cannot be scoped to a
path, so the grant alone cannot carry that promise. This hook carries it.

Generated text now ships with provenance watermarking. A single agent write into
a manuscript can mark the writer's own work as machine-authored, and the writer
has no way to see that it happened. That is the failure this hook exists to make
impossible rather than merely forbidden.

PreToolUse contract: the tool payload arrives as JSON on stdin. Exit 2 blocks the
call and returns stderr to the agent; exit 0 allows it.

This hook FAILS CLOSED. An unreadable payload is denied, because the cost of a
wrongly allowed write is unrecoverable and the cost of a wrongly denied one is a
retry. Register it on write-capable tools only, so a bad payload never wedges an
ordinary read.

Reading canon is untouched. The editor must read the manuscript to do its job.
"""

import json
import re
import shlex
import sys

# Directory names that hold the writer's own prose. A path is protected when any
# of its components matches, so nested vaults and absolute paths both resolve.
PROTECTED_DIRS = ("canon", "drafts")

WRITE_TOOLS = ("Edit", "Write", "NotebookEdit", "MultiEdit")

MESSAGE = """\
BLOCKED: {detail}

The writer's canon/ and drafts/ are read-only to every agent, enforced here rather
than promised. Generated text carries provenance watermarking, so one agent write
into a manuscript can mark the writer's own prose as machine-authored with no
visible trace.

Agent-authored text belongs under _editor-notes/, or under scene-summaries/ on the
writer's explicit request. If the writer asked for a change to their manuscript,
give them the text and let them paste it themselves.
"""

# Shell constructs that can modify a file. Pure readers (cat, grep, ls, git log,
# git diff) carry none of these and pass through.
MUTATING_BINARIES = frozenset(
    {
        "rm", "mv", "cp", "tee", "touch", "mkdir", "rmdir", "chmod", "chown",
        "ln", "install", "dd", "truncate", "shred", "unlink", "rsync", "patch",
        "sponge",
    }
)

# Subcommands that write into the working tree. `git log`, `git diff`, and
# `git rev-parse` are exactly the read-only calls the vault-sync agent needs.
MUTATING_GIT_SUBCOMMANDS = frozenset(
    {"checkout", "restore", "apply", "reset", "clean", "stash", "switch", "rm", "mv"}
)

REDIRECT = re.compile(r">>?\s*\S")
SED_IN_PLACE = re.compile(r"\bsed\b[^|;&]*\s-\S*i")


def _is_protected(path: str) -> bool:
    """Whether `path` points inside a protected directory."""
    parts = [part for part in re.split(r"[/\\]", path.strip().strip("'\"")) if part]
    return any(part in PROTECTED_DIRS for part in parts)


def _bash_writes_to_canon(command: str) -> bool:
    """Whether a shell command both mentions protected prose and can modify it.

    Both halves are required. `grep -r x canon/` mentions canon and mutates
    nothing; `rm -rf build/` mutates and touches no prose. Only the intersection
    is denied, so the guard stays out of the way of ordinary reads.
    """
    if not any(f"{name}/" in command or f"/{name}" in command for name in PROTECTED_DIRS):
        return False

    if REDIRECT.search(command) or SED_IN_PLACE.search(command):
        return True

    try:
        tokens = shlex.split(command)
    except ValueError:
        return True  # unparseable shell that names canon: deny

    for index, token in enumerate(tokens):
        binary = token.rsplit("/", 1)[-1]
        if binary in MUTATING_BINARIES:
            return True
        if binary == "git":
            rest = tokens[index + 1 :]
            if any(sub in MUTATING_GIT_SUBCOMMANDS for sub in rest):
                return True
    return False


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.stderr.write(MESSAGE.format(detail="unreadable tool payload, denied by default"))
        return 2

    tool = payload.get("tool_name") or ""
    tool_input = payload.get("tool_input") or {}

    if tool in WRITE_TOOLS:
        target = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
        if _is_protected(str(target)):
            return _deny(f"{tool} targets {target}, which is inside the writer's prose.")
        return 0

    if tool == "Bash":
        command = str(tool_input.get("command") or "")
        if _bash_writes_to_canon(command):
            return _deny("this shell command can modify a file inside the writer's prose.")
        return 0

    return 0


def _deny(detail: str) -> int:
    sys.stderr.write(MESSAGE.format(detail=detail))
    return 2


if __name__ == "__main__":
    sys.exit(main())
