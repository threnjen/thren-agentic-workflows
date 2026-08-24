"""Structural guards for the three cheap-tier mechanical PR Review sweeps.

Scoped to what is machine-checkable: the renumber landed in both directions, and
no body retains a retired identifier. The propagator's `_rewrite_agent_references`
keys on the display name, so a surviving retired name ships as a dangling literal.

Roster membership and tool grants are asserted in `test_propagate_master_assets.py`
alongside the propagation enumeration ledger they belong to.
"""

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = REPO_ROOT / ".github" / "agents"

MECHANICAL_EVALUATORS = (
    "04c-artifact-sweeper",
    "04d-consistency-auditor",
    "04e-dependency-auditor",
)


def _body(slug: str) -> str:
    return (AGENTS_DIR / f"{slug}.agent.md").read_text(encoding="utf-8")


class RenameTests(unittest.TestCase):
    """The renumber is complete, in both directions."""

    def test_renumbered_agents_exist_with_matching_name_frontmatter(self) -> None:
        expected_names = {
            "04c-artifact-sweeper": "04c Artifact Sweeper",
            "04d-consistency-auditor": "04d Consistency Auditor",
            "04e-dependency-auditor": "04e Dependency Auditor",
        }
        for slug, name in expected_names.items():
            with self.subTest(slug=slug):
                self.assertIn(f"name: {name}\n", _body(slug))

    def test_retired_slugs_are_gone_from_the_source_tree(self) -> None:
        for stem in ("05g-artifact-sweeper", "05j-consistency-auditor",
                     "05k-dependency-auditor"):
            with self.subTest(stem=stem):
                self.assertFalse((AGENTS_DIR / f"{stem}.agent.md").exists())

    def test_no_body_retains_an_old_self_reference(self) -> None:
        """The retired identifiers are checked as complete names, not prefixes."""
        retired = (
            "05g-artifact-sweeper", "05" + "g Artifact Sweeper",
            "05j-consistency-auditor", "05j Consistency Auditor",
            "05k-dependency-auditor", "05k Dependency Auditor",
        )
        for slug in MECHANICAL_EVALUATORS:
            body = _body(slug)
            for marker in retired:
                with self.subTest(slug=slug, marker=marker):
                    self.assertNotIn(marker, body)


if __name__ == "__main__":
    unittest.main()
