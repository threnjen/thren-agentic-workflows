"""Structural guard for the two PR Review skills.

    phase-final-review-conventions -> pr-review-conventions
    phase-final-review-report      -> pr-review-report

The rename is a delete-plus-create to the propagator -- there is no rename
detection -- so the old directories only leave the three generated roots via the
marker-guarded pruner. Never `git rm` a generated skill directory to make these
pass: that masks a broken pruner until the next rename.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

SOURCE_SKILLS_DIR = REPO_ROOT / "source_of_truth" / "skills"

# (old directory name, new directory name)
RENAMED_SKILLS = (
    ("phase-final-review-conventions", "pr-review-conventions"),
    ("phase-final-review-report", "pr-review-report"),
)

NEW_SKILL_NAMES = tuple(new for _, new in RENAMED_SKILLS)
OLD_SKILL_NAMES = tuple(old for old, _ in RENAMED_SKILLS)

GENERATED_SKILL_ROOTS = (
    REPO_ROOT / "ports" / "claude" / "skills",
    REPO_ROOT / "ports" / "opencode" / "skills",
    REPO_ROOT / "ports" / "codex" / "skills",
)


def _skill_body(skill_name: str) -> str:
    return (SOURCE_SKILLS_DIR / skill_name / "SKILL.md").read_text(encoding="utf-8")


def _frontmatter(text: str) -> str:
    return text[4:].split("\n---\n", 1)[0]


def _surviving_evaluator_agents() -> list[Path]:
    return sorted((REPO_ROOT / "source_of_truth" / "agents").glob("05*.agent.md"))


# --- the rename itself ------------------------------------------------------


def test_renamed_skills_exist_and_old_ones_do_not() -> None:
    for old, new in RENAMED_SKILLS:
        assert (SOURCE_SKILLS_DIR / new / "SKILL.md").is_file(), (
            f"renamed skill missing: source_of_truth/skills/{new}/SKILL.md"
        )
        assert not (SOURCE_SKILLS_DIR / old).exists(), (
            f"old skill directory survived the rename: source_of_truth/skills/{old}"
        )


def test_frontmatter_name_matches_directory() -> None:
    """A `name:` that disagrees with its directory silently fails to load."""
    for skill_name in NEW_SKILL_NAMES:
        frontmatter = _frontmatter(_skill_body(skill_name))
        assert f"name: {skill_name}" in frontmatter, (
            f"{skill_name}/SKILL.md frontmatter `name:` does not match its directory"
        )


# --- the reference sweep ----------------------------------------------------


def test_no_surviving_agent_references_a_retired_skill_name() -> None:
    """A stale skill reference is a silently missing skill at runtime, not an
    error. Matched on the exact skill tokens only."""
    agents = _surviving_evaluator_agents()
    assert agents, "no 05x agents found -- the sweep would pass vacuously"

    offenders: list[str] = []
    for agent in agents:
        body = agent.read_text(encoding="utf-8")
        found = sorted({name for name in OLD_SKILL_NAMES if name in body})
        if found:
            offenders.append(f"{agent.name}: {', '.join(found)}")

    assert not offenders, "agents still load retired skill names:\n" + "\n".join(
        offenders
    )


# --- propagation and pruning ------------------------------------------------


def test_renamed_skills_propagate_to_all_three_generated_roots() -> None:
    for root in GENERATED_SKILL_ROOTS:
        for skill_name in NEW_SKILL_NAMES:
            generated = root / skill_name / "SKILL.md"
            assert generated.is_file(), f"renamed skill did not propagate to {generated}"


def test_old_skill_dirs_are_pruned_from_all_three_generated_roots() -> None:
    """Proves pruning covers skills, not just agents.

    Codex is asserted explicitly rather than assumed: its prune block existed
    for the whole life of the repo but matched 0 of 24 skills, because the guard
    read `startswith(GENERATED_SKILL_HEADER)` while the marker sits on line 5,
    behind the frontmatter.

    If this fails, the pruner is the bug. Do not hand-delete the directory.
    """
    for root in GENERATED_SKILL_ROOTS:
        for old in OLD_SKILL_NAMES:
            orphan = root / old
            assert not orphan.exists(), (
                f"orphaned skill directory survived propagation: {orphan} -- fix "
                "the pruner, never `git rm` the output"
            )
