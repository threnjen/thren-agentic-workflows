"""Shared test harness: point the propagator's directory globals at a temp root.

`propagate_master_assets` resolves every source and output root from module-level
`Path` constants pinned to the real `REPO_ROOT` at import time. Isolated tests
redirect those constants at a throwaway tree so a propagation run — including its
file deletions — can never read from or write to this repository.
"""

import atexit
import contextlib
import functools
import shutil
import sys
import tempfile
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


@functools.lru_cache(maxsize=1)
def propagated_tree() -> Path:
    """A converged propagation of this repository's `source_of_truth/`, built once.

    `ports/` is a temporary landing zone that `deploy_agents.py` deletes after
    every run, so it is not in the repository for a test to read. A test that
    asserts on generated output builds the output it asserts on.

    The tree holds `source_of_truth/`, `ports/` and `.github/`. It is built on
    first use and shared for the rest of the session, because propagating the
    whole corpus per test module is the expensive part.
    """
    root = Path(tempfile.mkdtemp(prefix="propagated-tree-")).resolve()
    atexit.register(shutil.rmtree, root, True)
    shutil.copytree(REPO_ROOT / "source_of_truth", root / "source_of_truth")
    with redirect(root):
        mod.propagate_until_converged()
    return root


def propagated_ports() -> Path:
    """`ports/` inside the shared propagated tree."""
    return propagated_tree() / "ports"


def propagated_github() -> Path:
    """`.github/` inside the shared propagated tree."""
    return propagated_tree() / ".github"
