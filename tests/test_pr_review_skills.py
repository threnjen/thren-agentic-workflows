"""Contract guard for the two PR Review skills.

`03-pr-review-conventions-skills` renamed and rescoped the two skills that carry
the evaluator contract:

    phase-final-review-conventions -> pr-review-conventions
    phase-final-review-report      -> pr-review-report

The rename is a delete-plus-create to the propagator -- there is no rename
detection -- so the old directories only leave the three generated roots via
`01-propagator-orphan-pruning`'s marker-guarded pruner. Never `git rm` a
generated skill directory to make AC8 pass: that masks a broken pruner until the
next rename.

The report roster these tests pin uses the *new* `05a`-`05g` slugs while the
agents still carry their old ones. That forward reference is deliberate -- the
skill is the contract features `05`-`07` are then written against.
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

SOURCE_SKILLS_DIR = REPO_ROOT / ".github" / "skills"

# (old directory name, new directory name)
RENAMED_SKILLS = (
    ("phase-final-review-conventions", "pr-review-conventions"),
    ("phase-final-review-report", "pr-review-report"),
)

NEW_SKILL_NAMES = tuple(new for _, new in RENAMED_SKILLS)
OLD_SKILL_NAMES = tuple(old for old, _ in RENAMED_SKILLS)

GENERATED_SKILL_ROOTS = (
    REPO_ROOT / "claude" / "skills",
    REPO_ROOT / "opencode" / "skills",
    REPO_ROOT / "codex" / "skills",
)

# The seven survivors of the retirement, under the slugs features 05-07 give
# them. Derived from the surviving evaluator set, not edited down from twelve.
SURVIVING_REPORTS = (
    "05a-baseline-worktree-report.md",
    "05b-change-narrator-report.md",
    "05c-artifact-sweeper-report.md",
    "05d-consistency-auditor-report.md",
    "05e-dependency-auditor-report.md",
    "05f-test-health-report.md",
    "05g-readiness-synthesizer-report.md",
)

# Produced by retired evaluators. `readiness-report.md` is the only survivor of
# the original four named rollups.
RETIRED_ROLLUPS = ("master-qa.md", "security-rollup.md", "ac-regression-matrix.md")

REPORT_ROOT = "dev/pr-review/<base-sha-short>-<UTC-YYYYMMDDTHHMMSSZ>/"


def _skill_body(skill_name: str) -> str:
    return (SOURCE_SKILLS_DIR / skill_name / "SKILL.md").read_text(encoding="utf-8")


def _prose(skill_name: str) -> str:
    """Skill body with whitespace runs collapsed, for multi-word prose assertions.

    Asserting on wrapped prose against the raw text welds the test to the
    author's line-wrap position: reflowing a paragraph then breaks a contract
    check that the contract itself still satisfies. `test_readiness_synthesis
    _agents.py:16` (`"never read\\ncode"`) is the standing example of that
    coupling. Normalizing here keeps these assertions about the contract.
    """
    return " ".join(_skill_body(skill_name).split())


def _frontmatter(text: str) -> str:
    return text[4:].split("\n---\n", 1)[0]


def _surviving_evaluator_agents() -> list[Path]:
    return sorted((REPO_ROOT / ".github" / "agents").glob("05*.agent.md"))


# --- AC1, AC2: the rename itself -------------------------------------------


def test_renamed_skills_exist_and_old_ones_do_not() -> None:
    """AC1, AC2: both skills moved; neither old directory survives in source."""
    for old, new in RENAMED_SKILLS:
        assert (SOURCE_SKILLS_DIR / new / "SKILL.md").is_file(), (
            f"renamed skill missing: .github/skills/{new}/SKILL.md"
        )
        assert not (SOURCE_SKILLS_DIR / old).exists(), (
            f"old skill directory survived the rename: .github/skills/{old}"
        )


def test_frontmatter_name_matches_directory() -> None:
    """AC1, AC2: a `name:` that disagrees with its directory silently fails to load.

    This is the same failure shape as the propagator rename that left broken
    `~/.codex/agents/` symlinks: the identifier and the path must move together.
    """
    for skill_name in NEW_SKILL_NAMES:
        frontmatter = _frontmatter(_skill_body(skill_name))
        assert f"name: {skill_name}" in frontmatter, (
            f"{skill_name}/SKILL.md frontmatter `name:` does not match its directory"
        )


def test_descriptions_state_diff_scope_not_phase_scope() -> None:
    """AC1, AC2: the description is the load trigger -- a phase-shaped one mis-fires."""
    for skill_name in NEW_SKILL_NAMES:
        frontmatter = _frontmatter(_skill_body(skill_name)).lower()
        description = next(
            line for line in frontmatter.splitlines() if line.startswith("description:")
        )
        assert "phase final review" not in description
        assert "subphase" not in description
        assert "05x" not in description
        assert "pr review" in description or "pull request" in description


# --- AC3: the report contract ----------------------------------------------


def test_report_root_is_declared_and_contains_no_branch_name() -> None:
    """AC3: the root key is a SHA plus a timestamp, so no branch sanitizer is needed."""
    for skill_name in NEW_SKILL_NAMES:
        body = _skill_body(skill_name)
        assert REPORT_ROOT in body, f"{skill_name} does not declare the report root"

    # Structural proof rather than a spot check: the only placeholders in the
    # root are the SHA and the timestamp. A `<branch>`-shaped component would
    # survive the substring check above but not this one.
    variable_part = REPORT_ROOT[len("dev/pr-review/") :].rstrip("/")
    assert variable_part == "<base-sha-short>-<UTC-YYYYMMDDTHHMMSSZ>"
    for forbidden in ("branch", "ref", "head-name", "PHASE_0N"):
        assert forbidden not in variable_part


def test_conventions_declares_exactly_the_surviving_report_roster() -> None:
    """AC3: the roster is re-derived from the surviving seven, not edited from twelve."""
    body = _skill_body("pr-review-conventions")

    for report in SURVIVING_REPORTS:
        assert report in body, f"roster is missing surviving report {report}"

    assert "readiness-report.md" in body, (
        "readiness-report.md is the canonical hand-off and must survive"
    )

    for rollup in RETIRED_ROLLUPS:
        assert rollup not in body, (
            f"roster still promises {rollup}, produced by a retired evaluator -- "
            "nothing writes it any more"
        )


def test_no_retired_evaluator_report_filename_survives_in_either_skill() -> None:
    """AC3: the five retired evaluators' report files are gone from both skills."""
    retired_report_files = (
        "05c-qa-consolidator-report.md",
        "05d-security-rollup-report.md",
        "05e-ac-regression-report.md",
        "05f-seam-analyzer-report.md",
        "05i-learnings-harvester-report.md",
    )
    for skill_name in NEW_SKILL_NAMES:
        body = _skill_body(skill_name)
        for report in retired_report_files:
            assert report not in body, f"{skill_name} still names retired report {report}"


# --- AC4: subphase concepts are gone ---------------------------------------


def test_skills_are_free_of_subphase_concepts() -> None:
    """AC4: a PR has no subphases; every subphase-shaped concept is out."""
    for skill_name in NEW_SKILL_NAMES:
        body = _skill_body(skill_name).lower()
        for concept in ("subphase", "phase_0n", "dev/phase-final-review/"):
            assert concept not in body, (
                f"{skill_name} still carries the subphase concept {concept!r}"
            )


def test_conventions_drops_artifact_refusal_and_archive_before_overwrite() -> None:
    """AC4: both are phase-run mechanics with no PR analogue."""
    body = _skill_body("pr-review-conventions").lower()
    assert "archive" not in body
    assert "preflight must list each missing category" not in body


# --- AC5: the optional-artifact contract -----------------------------------


def test_optional_artifact_contract_is_present() -> None:
    """AC5: the recorded boundary against duplicating `prod-code-review`.

    This is a contract, not a preference: a run proceeds on the diff alone and
    the report names which evidence was unavailable. Without it, PR Review
    becomes a second pipeline gate that refuses to run outside the pipeline.
    """
    prose = _prose("pr-review-conventions").lower()

    assert "pipeline artifacts are optional enrichment" in prose, (
        "the conventions skill must state that pipeline artifacts are optional "
        "enrichment"
    )
    assert "proceeds on the diff alone" in prose, "a run must proceed on the diff alone"
    assert "prod-code-review" in prose, (
        "the boundary against prod-code-review must be recorded, not assumed"
    )
    assert "contract, not a preference" in prose, (
        "the optional-artifact rule is a contract, not a preference"
    )
    # The other half of the contract: optional is not the same as ignorable.
    assert "names which evidence was unavailable" in prose


# --- AC6: the retained contracts --------------------------------------------


def test_return_summary_contract_is_retained_in_force() -> None:
    """AC6: the phase's only defense against a long-lived branch blowing out context."""
    body = _skill_body("pr-review-conventions")
    prose = _prose("pr-review-conventions")

    assert "Return Summary Contract" in body
    assert "at most **10 lines**" in prose, "the 10-line return cap must remain explicit"
    assert "Full findings belong in the report file, not in the return message" in prose, (
        "the reports-on-disk rule must survive the rescope"
    )


def test_read_only_and_no_clean_result_from_absence_are_retained() -> None:
    """AC6 / plan section E: prose is the only remaining constraint on evaluator shell use.

    The `execute`-narrowing deliverable was deleted from this phase because
    per-agent command scoping is not expressible on Claude. Softening these
    while rewriting the surrounding text would be a real regression with nothing
    behind it.
    """
    body = _skill_body("pr-review-conventions")
    prose = _prose("pr-review-conventions").lower()

    assert "Read-Only Worktree Etiquette" in body
    assert "as read-only inputs" in prose
    assert (
        "do not treat an unavailable evaluator, dependency, or worktree as a "
        "clean result" in prose
    ), "the no-clean-result-from-absence rule must be retained in force"
    assert (
        "a narrowly scoped capability is always preferred to a broad grant" in prose
    ), "the preference for a narrow capability over a broad grant must be retained"
    assert "worktree-baseline" in body, (
        "the reference to the unchanged worktree-baseline skill must survive (AC9)"
    )


def test_conventions_still_builds_on_auditor_conventions() -> None:
    """The house split: shared audit norms there, review-family contracts here."""
    assert "auditor-conventions" in _skill_body("pr-review-conventions")


def test_conventions_holds_no_orchestrator_concerns() -> None:
    """Plan section D: the conventions skill is a natural dumping ground for anything
    'shared'. Base derivation and PR posting are orchestrator concerns.
    Evaluators never ask questions."""
    lowered = _skill_body("pr-review-conventions").lower()
    for concern in ("merge-base", "gh pr comment", "post the report", "ask the user"):
        assert concern not in lowered, (
            f"orchestrator concern {concern!r} migrated into the conventions skill"
        )


# --- AC7: the reference sweep -----------------------------------------------


def test_no_surviving_agent_references_a_retired_skill_name() -> None:
    """AC7 -- the operative clause is the negative sweep.

    Matched on the exact skill tokens only. A substring sweep on
    `phase-final-review` would fail against the report roots inside agent bodies
    and the orchestrator's own filename -- both explicitly out of scope here and
    owned by features `04`-`07`.

    A stale reference is a silently missing skill at runtime, not an error.
    """
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


def test_agents_that_load_the_skills_reference_the_renamed_ones() -> None:
    """AC7's positive half, applied only where a reference already existed.

    Deliberately not asserted for `05a-baseline-worktree`: it references only
    `worktree-baseline` and must not acquire a new skill load. Forcing one would
    contradict AC9.
    """
    for agent in _surviving_evaluator_agents():
        body = agent.read_text(encoding="utf-8")
        if "pr-review-report" in body or "pr-review-conventions" in body:
            assert "pr-review-conventions" in body, (
                f"{agent.name} loads the report skill without the conventions skill"
            )


def test_baseline_worktree_agent_acquires_no_skill_load() -> None:
    """AC9's boundary: `05a` carried no old-skill reference, so it gains none."""
    body = (
        REPO_ROOT / ".github" / "agents" / "05a-baseline-worktree.agent.md"
    ).read_text(encoding="utf-8")

    assert "worktree-baseline" in body, "05a must keep its only skill reference"
    for skill_name in NEW_SKILL_NAMES:
        assert skill_name not in body, (
            f"05a must not acquire a {skill_name} load -- AC7's negative sweep "
            "governs it, not the positive clause"
        )
    assert "Phase Final Review family" not in body, (
        "05a's phase-family prose is this feature's only change to it"
    )


# --- AC8: propagation and pruning -------------------------------------------


def test_renamed_skills_propagate_to_all_three_generated_roots() -> None:
    """AC8: the rename reaches Claude, OpenCode, and Codex."""
    for root in GENERATED_SKILL_ROOTS:
        for skill_name in NEW_SKILL_NAMES:
            generated = root / skill_name / "SKILL.md"
            assert generated.is_file(), f"renamed skill did not propagate to {generated}"


def test_old_skill_dirs_are_pruned_from_all_three_generated_roots() -> None:
    """AC8: proves `01`'s pruning covers skills, not just agents.

    Codex is asserted explicitly rather than assumed: its prune block existed
    for the whole life of the repo but matched 0 of 24 skills, because the guard
    read `startswith(GENERATED_SKILL_HEADER)` while the marker sits on line 5,
    behind the frontmatter. Feature `01` repaired it. This test is what proves
    the repair is live for a real, named skill rather than a fixture.

    If this fails, the pruner is the bug. Do not hand-delete the directory.
    """
    for root in GENERATED_SKILL_ROOTS:
        for old in OLD_SKILL_NAMES:
            orphan = root / old
            assert not orphan.exists(), (
                f"orphaned skill directory survived propagation: {orphan} -- fix "
                "the pruner, never `git rm` the output"
            )
