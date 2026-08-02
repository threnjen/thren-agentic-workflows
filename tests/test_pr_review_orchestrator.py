"""Structural guards for the PR Review orchestrator and its pinned fixture.

Scoped to what is machine-checkable: the pinned base/head pair is a real,
PR-shaped, tracked commit range; the rename landed in source and in all three
generated roots with no stale output left behind; and the orchestrator's display
name stays collision-safe for the propagator's reference rewriting.

Style is pytest-style module-level `Path` constants and plain `assert`, not the
`unittest` classes of `tests/test_propagate_master_assets.py`.
"""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

ORCHESTRATOR = REPO_ROOT / "source_of_truth" / "agents" / "05-pr-review.agent.md"
RETIRED_ORCHESTRATOR = (
    REPO_ROOT / "source_of_truth" / "agents" / "05-phase-final-review.agent.md"
)

FIXTURE = REPO_ROOT / "tests" / "fixtures" / "pr-review" / "pinned-diff-range.md"

# The pinned base/head pair. Declared here once so the fixture document and the
# tests cannot drift apart: the tests read these out of the fixture rather than
# trusting that it says what it claims.
FIXTURE_BASE_SHA = "f5ab960e5697756538f94430327e2a68eb113822"
FIXTURE_HEAD_SHA = "e6ff28a36293697aebf62155ae0048115c4aecca"


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


# ---------------------------------------------------------------------------
# The pinned fixture
# ---------------------------------------------------------------------------


def test_fixture_pins_both_shas_of_a_real_base_head_pair() -> None:
    body = FIXTURE.read_text(encoding="utf-8")

    assert FIXTURE_BASE_SHA in body
    assert FIXTURE_HEAD_SHA in body


def test_fixture_shas_resolve_and_merge_base_is_the_pinned_base() -> None:
    """The pair is a genuine PR shape, not two arbitrary commits.

    `git merge-base head base` returning `base` is what makes this a base/head
    pair at all -- it proves the head branch descends from the base rather than
    merely differing from it.
    """
    assert _git("rev-parse", "--verify", f"{FIXTURE_BASE_SHA}^{{commit}}") == (
        FIXTURE_BASE_SHA
    )
    assert _git("rev-parse", "--verify", f"{FIXTURE_HEAD_SHA}^{{commit}}") == (
        FIXTURE_HEAD_SHA
    )
    assert _git("merge-base", FIXTURE_HEAD_SHA, FIXTURE_BASE_SHA) == FIXTURE_BASE_SHA


def test_fixture_range_is_pr_shaped_not_a_whole_phase() -> None:
    """The bound is deliberately generous: it fails the whole-phase shape, not a
    slightly-grown fixture."""
    files = _git(
        "diff", "--name-only", FIXTURE_BASE_SHA, FIXTURE_HEAD_SHA
    ).splitlines()
    commits = _git(
        "rev-list", "--count", f"{FIXTURE_BASE_SHA}..{FIXTURE_HEAD_SHA}"
    )

    assert 0 < len(files) <= 60, f"fixture spans {len(files)} files"
    assert 0 < int(commits) <= 10, f"fixture spans {commits} commits"


def test_fixture_is_actually_tracked_by_git() -> None:
    """The fixture lives under `tests/fixtures/`, outside the gitignored `dev/`
    tree, precisely so it cannot be silently untracked."""
    tracked = _git("ls-files", "tests/fixtures/pr-review/").splitlines()

    assert "tests/fixtures/pr-review/pinned-diff-range.md" in tracked


def test_run_output_root_stays_ignored() -> None:
    """The report root must NOT become trackable -- run output would pollute the
    tree and confound the propagation-idempotency checks."""
    result = subprocess.run(
        [
            "git",
            "check-ignore",
            "dev/pr-review/abc1234-20260716T120000Z/readiness-report.md",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, "run output root is not ignored"


# ---------------------------------------------------------------------------
# The rename, and its propagation to all three roots
# ---------------------------------------------------------------------------


def test_orchestrator_is_renamed_and_the_old_source_is_gone() -> None:
    assert ORCHESTRATOR.is_file()
    assert not RETIRED_ORCHESTRATOR.exists()


def test_frontmatter_declares_the_pr_review_name() -> None:
    body = ORCHESTRATOR.read_text(encoding="utf-8")

    assert "name: 05 PR - Review" in body
    assert "05 Phase - Final Review" not in body


def test_agent_name_does_not_collide_with_prose_in_any_source_asset() -> None:
    """`_rewrite_agent_references` does an unanchored `text.replace(agent.name,
    identifier)` across every agent body, so a `name:` that also occurs as
    ordinary prose gets rewritten wherever it appears. The ` - ` separator is
    what makes the name collision-safe -- load bearing, not stylistic.

    This reads the name out of the file rather than restating it, so renaming
    the agent to something collision-prone fails here instead of silently
    shipping mangled prose.
    """
    name = next(
        line.split("name:", 1)[1].strip()
        for line in ORCHESTRATOR.read_text(encoding="utf-8").splitlines()
        if line.startswith("name:")
    )

    assert " - " in name, f"{name!r} lacks the collision-safe separator"

    # Scope comes from the propagator's own loader, not a glob of the agents
    # directory. `_rewrite_agent_references` is applied to source-agent bodies;
    # `.github/agents/README.md` is deliberately NOT one (it carries no
    # frontmatter `name`/`description`, so `load_source_agents` skips it).
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    import propagate_master_assets as propagator

    for agent in propagator.load_source_agents():
        if agent.name == name:
            continue
        assert name not in agent.body, (
            f"{name!r} occurs in the body of {agent.rel_path}; "
            "propagation would rewrite it into an identifier"
        )


def test_renamed_orchestrator_reaches_all_three_generated_roots() -> None:
    expected_markers = {
        "ports/claude/commands/pr-review.md": "PR Review Orchestrator",
        "ports/opencode/agents/05-pr-review.md": "PR Review Orchestrator",
        "ports/codex/agents/05-pr-review.toml": 'name = "pr-review"',
    }

    for relative_path, marker in expected_markers.items():
        output = REPO_ROOT / relative_path
        assert output.is_file(), relative_path
        assert marker in output.read_text(encoding="utf-8"), relative_path


def test_stale_generated_outputs_are_absent_from_every_root() -> None:
    """`claude/commands/phase-final-review.md` is the sharpest case: it stays
    user-invocable, so a stale command file leaves a live slash command pointing
    at a deleted agent. These must disappear via pruning, never by hand-deletion
    -- hand-deleting hides whether pruning works.
    """
    stale = (
        "claude/commands/phase-final-review.md",
        "opencode/agents/05-phase-final-review.md",
        "codex/agents/05-phase-final-review.toml",
    )

    for relative_path in stale:
        assert not (REPO_ROOT / relative_path).exists(), relative_path
