"""Contract guards for the unified local final-check workflow."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
AGENTS = REPO_ROOT / "source_of_truth/agents"
SKILLS = REPO_ROOT / "source_of_truth/skills"
ORCHESTRATOR = AGENTS / "04-phase-final-checks.agent.md"
FIXTURE = REPO_ROOT / "tests/fixtures/local-final-checks/pinned-diff-range.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=REPO_ROOT, capture_output=True, text=True, check=True
    ).stdout.strip()


def test_canonical_agent_and_alias_contract() -> None:
    body = _read(ORCHESTRATOR)
    assert "name: 04 Phase - Final Checks" in body
    assert "aliases: [pr-review]" in body
    assert not (AGENTS / ("04" + "-pr-review.agent.md")).exists()


def test_roster_resolves_and_dead_lanes_are_absent() -> None:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    import propagate_master_assets as mod

    agents = {agent.name: agent for agent in mod.load_source_agents()}
    root = next(agent for agent in agents.values() if agent.path == ORCHESTRATOR)
    assert set(root.subagents) <= set(agents)
    assert "04c " + "Artifact Sweeper" not in root.subagents
    assert "Test - Analyst" not in root.subagents
    assert "04i Local Review Fixer" in root.subagents
    assert not (AGENTS / ("04c" + "-artifact-sweeper.agent.md")).exists()


def test_range_lifecycle_and_empty_range_are_explicit() -> None:
    body = _read(ORCHESTRATOR)
    for token in (
        "Exclude the current branch and its remote-tracking ref",
        "A correction replaces the suggestion",
        "fixed base and head for every child",
        "If the confirmed range is empty",
        "completed no-change readiness report",
        "Baseline Worktree",
    ):
        assert token in body
    assert "dev/local-final-checks/<base-sha-short>-<UTC-YYYYMMDDTHHMMSSZ>/" in body


def test_evaluator_conditions_and_enrichment_isolation_are_explicit() -> None:
    body = _read(ORCHESTRATOR)
    for token in (
        "04e Dependency Auditor` only when a dependency manifest or lockfile",
        "04f Test Health` only when a test file changed or the user",
        "Unity Reviewer` only when the canonical\nUnity predicate matches",
        "A condition that does not hold is complete evidence",
        "go only to\n`04g Readiness Synthesizer`",
        "Coverage evidence is direct input to\n`04f Test Health`",
    ):
        assert token in body


def test_readiness_precedes_one_bounded_repair_pass() -> None:
    body = _read(ORCHESTRATOR)
    readiness = body.index("Require\n`readiness-report.md`")
    repair_question = body.index("ask whether the user wants one repair pass")
    assert readiness < repair_question
    assert "spawn `04i Local Review Fixer` once" in body
    assert "Do not rerun the evaluator roster" in body
    assert "Never commit repair changes" in body
    assert "Never push,\npost comments, create a merge request" in body


def test_surviving_agents_own_folded_checks_and_repair_candidates() -> None:
    narrator = _read(AGENTS / "04b-change-narrator.agent.md")
    cleanliness = _read(AGENTS / "04h-cleanliness-auditor.agent.md")
    test_health = _read(AGENTS / "04f-test-health.agent.md")
    synthesizer = _read(AGENTS / "04g-readiness-synthesizer.agent.md")
    fixer = _read(AGENTS / "04i-local-review-fixer.agent.md")

    assert "outward-impact" in narrator
    for token in ("Debug artifacts", "`TODO` and `FIXME`", "Commented-out code"):
        assert token in cleanliness
    assert "changed-test-falsification" in test_health
    for token in ("security", "outward-impact", "changed-test-falsification"):
        assert token in synthesizer
    for token in ("Plans, task names", "Run those commands before editing", "Do not re-review"):
        assert token in fixer


def test_local_review_skills_replace_pr_named_skills() -> None:
    for name in ("local-final-check-conventions", "local-final-check-report"):
        body = _read(SKILLS / name / "SKILL.md")
        assert f"name: {name}" in body
    for name in ("pr-review-" + "conventions", "pr-review-" + "report"):
        assert not (SKILLS / name / "SKILL.md").exists()


def test_github_native_agent_drops_command_alias_frontmatter() -> None:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    import propagate_master_assets as mod

    rendered = mod._github_agent_bytes(ORCHESTRATOR, ORCHESTRATOR.read_bytes(), None)
    assert b"name: 04 Phase - Final Checks" in rendered
    assert b"aliases:" not in rendered


def test_pinned_fixture_is_real_and_trackable() -> None:
    body = _read(FIXTURE)
    shas = re.findall(r"`([0-9a-f]{40})`", body)
    base, head = shas[:2]
    assert _git("merge-base", head, base) == base
    ignored = subprocess.run(
        ["git", "check-ignore", str(FIXTURE.relative_to(REPO_ROOT))],
        cwd=REPO_ROOT,
        capture_output=True,
    )
    assert ignored.returncode != 0


def test_retired_live_names_are_absent_from_authored_runtime_assets() -> None:
    retired = (
        "04" + "-pr-review.agent.md",
        "04c" + "-artifact-sweeper",
        "04c " + "Artifact Sweeper",
        "pr-review-" + "conventions",
        "pr-review-" + "report",
        "dev/" + "pr-review/",
    )
    offenders: list[str] = []
    for root in (REPO_ROOT / "source_of_truth/agents", REPO_ROOT / "source_of_truth/skills", REPO_ROOT / "source_of_truth/instructions"):
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            found = [token for token in retired if token in text or token in path.as_posix()]
            if found:
                offenders.append(f"{path.relative_to(REPO_ROOT)}: {found}")
    assert not offenders, "retired local-review wiring survives:\n" + "\n".join(offenders)
