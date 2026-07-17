"""Shared constants and primitives for the propagate/deploy scripts.

`propagate_master_assets.py` (source_of_truth/ -> ports/) and `deploy_assets.py`
(ports/ -> real harness config dirs) both need the generated-output markers, the
marker-ownership check, and the poll-based watch loop. They live here so the two
scripts cannot drift apart.
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
SOT_DIR = REPO_ROOT / "source_of_truth"
PORTS_DIR = REPO_ROOT / "ports"

GENERATED_AGENT_HEADER = "# Generated from source_of_truth/agents. Do not edit manually."
# Markdown counterpart to GENERATED_AGENT_HEADER. That constant is a TOML comment,
# correct for codex agents/profiles *.toml but rendered as an H1 heading by Markdown,
# so it cannot be reused for Markdown outputs.
GENERATED_AGENT_MARKDOWN_HEADER = "<!-- Generated from source_of_truth/agents. Do not edit manually. -->"
GENERATED_SKILL_HEADER = "<!-- Generated from source_of_truth/skills. Do not edit manually. -->\n"

# Markers written before the source_of_truth/ restructure. Files carrying these are
# still ours: pruning and deploy-ownership honor them so the marker-text change does
# not orphan every previously generated file.
LEGACY_GENERATED_MARKERS = (
    "# Generated from .github/agents source-of-truth. Do not edit manually.",
    "<!-- Generated from .github/agents source-of-truth. Do not edit manually. -->",
    "<!-- Generated from .github/skills source-of-truth. Do not edit manually. -->",
)

GENERATED_MARKERS = frozenset(
    marker.strip("\n")
    for marker in (
        GENERATED_AGENT_HEADER,
        GENERATED_AGENT_MARKDOWN_HEADER,
        GENERATED_SKILL_HEADER,
        *LEGACY_GENERATED_MARKERS,
    )
)


def generated_marker_line_index(text: str) -> int:
    """The one line index at which a generated marker is written, or -1 for none.

    Line 0 for output with no YAML frontmatter (the TOML outputs), and the line
    immediately below the closing `---` otherwise. Text whose frontmatter is opened
    but never closed has no valid position and returns -1: it is never marked, and
    therefore never treated as owned.
    """
    if not text.startswith("---\n"):
        return 0
    lines = text.splitlines()
    for index in range(1, len(lines)):
        if lines[index] == "---":
            return index + 1
    return -1


def marker_at_expected_position(text: str) -> str | None:
    """The generated marker found at the emitter's write position, if any."""
    index = generated_marker_line_index(text)
    if index < 0:
        return None
    lines = text.splitlines()
    if index < len(lines) and lines[index] in GENERATED_MARKERS:
        return lines[index]
    return None


def file_has_generated_marker(path: Path) -> bool:
    """Whether `path` is a regular file positively identified as generated output.

    Positional rather than a whole-file search: a hand-maintained file that merely
    *quotes* a marker (e.g. a README documenting the convention) must stay inert.
    Symlinks are never something these scripts wrote. Unreadable files report False
    — an unreadable file is not confirmed ours, and False is the direction that
    never deletes or overwrites.
    """
    if path.is_symlink() or not path.is_file():
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return False
    return marker_at_expected_position(text) is not None


def collect_file_state(paths: Iterable[Path]) -> Dict[str, Tuple[float, int]]:
    state: Dict[str, Tuple[float, int]] = {}
    for root in paths:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            try:
                stat = path.stat()
            except FileNotFoundError:
                continue
            state[str(path)] = (stat.st_mtime, stat.st_size)
    return state


def compute_changes(
    old: Dict[str, Tuple[float, int]],
    new: Dict[str, Tuple[float, int]],
) -> List[str]:
    changed: List[str] = []
    for path in sorted(set(old) | set(new)):
        if path not in old or path not in new or old[path] != new[path]:
            changed.append(path)
    return changed


def poll_watch(
    dirs: Iterable[Path],
    on_change: Callable[[List[str]], None],
    *,
    interval_seconds: float = 1.0,
    settle_seconds: float = 0.8,
) -> None:
    """Poll `dirs` for file changes and invoke `on_change` after edits settle.

    Changes are debounced: a burst of saves triggers one callback once
    `settle_seconds` pass without further changes.
    """
    watched = list(dirs)
    last_state = collect_file_state(watched)
    pending_since: float | None = None
    pending_changes: List[str] = []

    while True:
        time.sleep(interval_seconds)
        current_state = collect_file_state(watched)
        changes = compute_changes(last_state, current_state)

        if changes:
            pending_changes = changes
            pending_since = time.time()
            last_state = current_state

        if pending_since is None:
            continue
        if time.time() - pending_since < settle_seconds:
            continue

        on_change(pending_changes)
        pending_since = None
        pending_changes = []
