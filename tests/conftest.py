"""Suite-wide guard: no test may propagate into this repository.

`ports/` and `.github/` are generated trees. Propagating them is the maintainer's
deliberate step, because a run rewrites every file in both and buries whatever
source change was under review. A test that propagates without redirecting the
propagator's roots does exactly that as a side effect, and the damage is silent:
the run repairs whatever it was supposed to be checking, so the assertion passes
and the working tree is left dirty for reasons no one can trace back to a test.

Redirect the roots instead. `tests/_propagate_env.use` and `.redirect` do it for
a temp tree, and the propagator's own `retarget` backs both.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]

# The generated roots a propagation run writes to.
GUARDED_TREES = ("ports", ".github")


def _fingerprint() -> dict[str, str]:
    """Content hash of every file in the guarded trees, keyed by relative path."""
    prints: dict[str, str] = {}
    for name in GUARDED_TREES:
        root = REPO_ROOT / name
        if not root.is_dir():
            continue
        for path in root.rglob("*"):
            if path.is_file():
                key = str(path.relative_to(REPO_ROOT))
                prints[key] = hashlib.sha256(path.read_bytes()).hexdigest()
    return prints


def _describe(before: dict[str, str], after: dict[str, str]) -> str:
    added = sorted(set(after) - set(before))
    removed = sorted(set(before) - set(after))
    changed = sorted(k for k in set(before) & set(after) if before[k] != after[k])
    lines = []
    for label, paths in (("changed", changed), ("added", added), ("removed", removed)):
        if paths:
            shown = ", ".join(paths[:5])
            more = f" (+{len(paths) - 5} more)" if len(paths) > 5 else ""
            lines.append(f"{len(paths)} {label}: {shown}{more}")
    return "; ".join(lines)


@pytest.fixture(scope="session", autouse=True)
def generated_trees_are_never_propagated():
    """Fail the session if any test wrote to `ports/` or `.github/`."""
    before = _fingerprint()
    yield
    after = _fingerprint()
    if before != after:
        raise AssertionError(
            "a test propagated into this repository: "
            f"{_describe(before, after)}. Redirect the propagator's roots at a "
            "temp tree with tests/_propagate_env.use or .redirect, then run "
            "`git checkout -- ports .github` to undo this run."
        )
