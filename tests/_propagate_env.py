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
    """Every directory global the propagator reads, rebased onto `root`.

    Delegates to the propagator's own `directory_overrides`, so the redirect map
    and the `--target` flag can never disagree about which roots exist.
    """
    return mod.directory_overrides(root)


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
