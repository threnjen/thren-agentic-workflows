"""Contracts for the read-only review committee lanes."""

from __future__ import annotations

import fnmatch
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import propagate_master_assets as mod  # noqa: E402


AGENTS_DIR = REPO_ROOT / "source_of_truth" / "agents"
COMMITTEE_SLUGS = (
    "04c-feature-review-and-fix",
    "03j-reviewer-blast-radius",
    "03k-reviewer-test-falsification",
    "03l-reviewer-plan-blind",
    "03m-finding-consolidator",
)
NEW_REVIEWER_SLUGS = COMMITTEE_SLUGS[1:]

LANE_PROHIBITIONS = {
    "04c-feature-review-and-fix": "Review plan conformance only.",
    "03j-reviewer-blast-radius": "Never evaluate whether the changed feature satisfies its plan",
    "03k-reviewer-test-falsification": "Do not read implementation code.",
    "03l-reviewer-plan-blind": "Do not open or read the feature plan",
    "03m-finding-consolidator": "You are not the readiness synthesizer.",
}


def _agents() -> dict[str, mod.SourceAgent]:
    return {agent.source_slug: agent for agent in mod.load_source_agents()}


def _instruction(name: str):
    return next(doc for doc in mod.load_instruction_docs() if doc.path.name == name)


def test_committee_agents_are_hidden_medium_and_read_only() -> None:
    agents = _agents()
    for slug in COMMITTEE_SLUGS:
        agent = agents[slug]
        assert not agent.user_invocable, f"{slug} must remain hidden"
        assert agent.model_tier == "medium", f"{slug} must use the medium tier"
        assert not {"edit", "write"}.intersection(agent.tools), (
            f"{slug} has repository write authority: {agent.tools}"
        )


def test_each_committee_lane_has_a_load_bearing_prohibition() -> None:
    agents = _agents()
    for slug, prohibition in LANE_PROHIBITIONS.items():
        body = agents[slug].body
        assert prohibition in body, f"{slug} lost its lane prohibition: {prohibition}"
        assert "File findings only" in body
        assert "stay silent outside" in body


def test_committee_reports_and_fix_list_have_stable_paths_and_fields() -> None:
    agents = _agents()
    expected_paths = {
        "03j-reviewer-blast-radius": "03j-reviewer-blast-radius-report.md",
        "03k-reviewer-test-falsification": "03k-reviewer-test-falsification-report.md",
        "03l-reviewer-plan-blind": "03l-reviewer-plan-blind-report.md",
        "03m-finding-consolidator": "03m-finding-consolidator-fix-list.md",
    }
    expected_fields = {
        "03j-reviewer-blast-radius": "lane: blast-radius",
        "03k-reviewer-test-falsification": "lane: test-falsification",
        "03l-reviewer-plan-blind": "lane: plan-blind",
    }

    for slug, filename in expected_paths.items():
        body = agents[slug].body
        assert f"dev/feature/[0N-task-name]/{filename}" in body
        if slug in expected_fields:
            assert expected_fields[slug] in body
            assert "reviewer:" in body
            assert "severity" in body
            assert "evidence" in body

    consolidator = agents["03m-finding-consolidator"].body
    for field in ("id", "severity", "lane", "finding", "evidence", "reviewers", "action", "status: open"):
        assert field in consolidator


def test_new_committee_agents_use_reserved_post_renumber_identifiers() -> None:
    actual = {path.name.removesuffix(".agent.md") for path in AGENTS_DIR.glob("03[j-m]-*.agent.md")}
    assert actual == set(NEW_REVIEWER_SLUGS)
    for slug in NEW_REVIEWER_SLUGS:
        assert not slug.startswith(("04", "05"))
        assert not slug.startswith(tuple(f"03{letter}-" for letter in "abcdefghi"))


def test_required_instruction_membership_matches_each_lane() -> None:
    agent_paths = {agent.source_slug: agent.rel_path for agent in _agents().values()}
    read_only = _instruction("read-only-agent.instructions.md")
    autonomy = _instruction("subagent-autonomy.instructions.md")

    for slug in COMMITTEE_SLUGS:
        assert any(
            fnmatch.fnmatch(agent_paths[slug], pattern)
            for pattern in read_only.apply_to_patterns
        ), f"read-only instructions do not reach {slug}"
    for slug in NEW_REVIEWER_SLUGS:
        assert any(
            fnmatch.fnmatch(agent_paths[slug], pattern)
            for pattern in autonomy.apply_to_patterns
        ), f"subagent autonomy does not reach {slug}"

    for name in ("code-change-strategy.instructions.md", "language-standards.instructions.md"):
        instruction = _instruction(name)
        assert not any(
            fnmatch.fnmatch(agent_paths["04c-feature-review-and-fix"], pattern)
            for pattern in instruction.apply_to_patterns
        ), f"{name} still routes coding guidance to Reviewer A"

    for name in ("test-target-scope.instructions.md", "test-execution-evidence.instructions.md"):
        instruction = _instruction(name)
        assert any(
            fnmatch.fnmatch(agent_paths["04c-feature-review-and-fix"], pattern)
            for pattern in instruction.apply_to_patterns
        ), f"{name} stopped reaching Reviewer A's test gate"
