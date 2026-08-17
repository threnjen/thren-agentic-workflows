"""Shared test harness: point the propagator's directory globals at a temp root.

`propagate_master_assets` resolves every source and output root from module-level
`Path` constants pinned to the real `REPO_ROOT` at import time. Isolated tests
redirect those constants at a throwaway tree so a propagation run — including its
file deletions — can never read from or write to this repository.
"""

import contextlib
import sys
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import propagate_master_assets as mod  # noqa: E402


def repo_dir_overrides(root: Path) -> dict:
    """Every directory global the propagator reads, rebased onto `root`."""
    root = Path(root)
    sot = root / "source_of_truth"
    ports = root / "ports"
    return {
        "REPO_ROOT": root,
        "SOT_DIR": sot,
        "PORTS_DIR": ports,
        "SOT_AGENTS_DIR": sot / "agents",
        "SOT_INSTRUCTIONS_DIR": sot / "instructions",
        "SOT_SKILLS_DIR": sot / "skills",
        "SOT_HOOKS_DIR": sot / "hooks",
        "CLAUDE_AGENTS_DIR": ports / "claude" / "agents",
        "CLAUDE_COMMANDS_DIR": ports / "claude" / "commands",
        "CLAUDE_SKILLS_DIR": ports / "claude" / "skills",
        "OPENCODE_AGENTS_DIR": ports / "opencode" / "agents",
        "OPENCODE_SKILLS_DIR": ports / "opencode" / "skills",
        "CODEX_AGENTS_DIR": ports / "codex" / "agents",
        "CODEX_PROFILES_DIR": ports / "codex" / "profiles",
        "CODEX_SKILLS_DIR": ports / "codex" / "skills",
        "CURSOR_AGENTS_DIR": ports / "cursor" / "agents",
        "CURSOR_COMMANDS_DIR": ports / "cursor" / "commands",
        "CURSOR_RULES_DIR": ports / "cursor" / "rules",
        "CURSOR_SKILLS_DIR": ports / "cursor" / "skills",
        "GITHUB_PORT_DIR": ports / "github",
        "DOT_GITHUB_DIR": root / ".github",
    }


def use(testcase, root: Path) -> None:
    """Redirect the propagator's roots at `root` for the rest of `testcase`."""
    patcher = mock.patch.multiple(mod, **repo_dir_overrides(root))
    patcher.start()
    testcase.addCleanup(patcher.stop)


@contextlib.contextmanager
def redirect(root: Path):
    """Context-manager form of `use`, for plain (non-``unittest``) test functions."""
    with mock.patch.multiple(mod, **repo_dir_overrides(root)):
        yield
