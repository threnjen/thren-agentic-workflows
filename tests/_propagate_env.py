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
    return {
        "REPO_ROOT": root,
        "GITHUB_AGENTS_DIR": root / ".github" / "agents",
        "GITHUB_INSTRUCTIONS_DIR": root / ".github" / "instructions",
        "GITHUB_SKILLS_DIR": root / ".github" / "skills",
        "GITHUB_LEARNINGS_DIR": root / ".github" / "learnings",
        "CLAUDE_AGENTS_DIR": root / "claude" / "agents",
        "CLAUDE_COMMANDS_DIR": root / "claude" / "commands",
        "CLAUDE_SKILLS_DIR": root / "claude" / "skills",
        "CLAUDE_LEARNINGS_DIR": root / "claude" / "learnings",
        "OPENCODE_AGENTS_DIR": root / "opencode" / "agents",
        "OPENCODE_SKILLS_DIR": root / "opencode" / "skills",
        "CODEX_AGENTS_DIR": root / "codex" / "agents",
        "CODEX_PROFILES_DIR": root / "codex" / "profiles",
        "CODEX_SKILLS_DIR": root / "codex" / "skills",
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
