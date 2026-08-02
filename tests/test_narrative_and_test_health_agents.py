"""Structural guards for the two judgment-shaped PR Review evaluators.

Scoped to what is machine-checkable: the `05h` -> `05f` rename landed in source,
in frontmatter, and in the slug-keyed OpenCode output; and the root's delegation
target resolves to an agent that actually declares that display name (the
propagator rewrites agent references by display name, so a near-miss ships to all
three roots as literal prose and the delegation quietly stops existing).
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = REPO_ROOT / "source_of_truth" / "agents"

NARRATOR = AGENTS_DIR / "05b-change-narrator.agent.md"
TEST_HEALTH = AGENTS_DIR / "05f-test-health.agent.md"
PR_REVIEW = AGENTS_DIR / "05-pr-review.agent.md"
RETIRED_TEST_HEALTH = AGENTS_DIR / "05h-test-health.agent.md"

OPENCODE_AGENTS_DIR = REPO_ROOT / "ports" / "opencode" / "agents"


def _prose(path: Path) -> str:
    """The whole file, lowercased, whitespace collapsed -- used only for
    identifier sweeps, which must cover frontmatter as well as the body."""
    return re.sub(r"\s+", " ", path.read_text(encoding="utf-8")).lower()


def test_test_health_is_renamed_to_the_05f_slug() -> None:
    assert TEST_HEALTH.is_file()
    assert not RETIRED_TEST_HEALTH.exists()


def test_test_health_declares_the_cross_feature_display_name() -> None:
    """`name:` is a cross-feature contract: the orchestrator's `agents:` roster
    resolves this exact value."""
    assert "name: 05f Test Health" in TEST_HEALTH.read_text(encoding="utf-8")


def test_no_retired_test_health_identifier_survives_in_either_agent() -> None:
    for path in (TEST_HEALTH, NARRATOR):
        assert "05h" not in _prose(path), f"retired 05h identifier survives in {path.name}"


def test_retired_test_health_slug_left_no_opencode_orphan() -> None:
    """OpenCode agent files key on the source slug, so a rename orphans one.
    Claude and Codex resolve output names against stems already on disk and
    survive the rename untouched.
    """
    source_slugs = {path.name[: -len(".agent.md")] for path in AGENTS_DIR.glob("*.agent.md")}
    assert "05h-test-health" not in source_slugs, "fixture: 05h must be retired"
    assert "05f-test-health" in source_slugs

    assert not (OPENCODE_AGENTS_DIR / "05h-test-health.md").exists(), (
        "the retired OpenCode slug survived the rename as a dispatchable duplicate"
    )
    assert (OPENCODE_AGENTS_DIR / "05f-test-health.md").is_file()


def test_root_delegation_target_display_name_is_exact() -> None:
    """The propagator resolves agent references by display name. A near-miss
    (`Test Analyst`, `test-analyst`) does not fail loudly -- it ships to all
    three roots as literal prose.
    """
    assert "Test - Analyst" in PR_REVIEW.read_text(encoding="utf-8")
    assert "agents:" not in TEST_HEALTH.read_text(encoding="utf-8").split("---", 2)[1]

    target = (AGENTS_DIR / "test-analyst.agent.md").read_text(encoding="utf-8")
    assert "name: Test - Analyst" in target, "the delegate's display name moved"
