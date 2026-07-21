from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_codex_docs_use_prompt_routing_not_profiles() -> None:
    for relative_path in ("README.md", "INSTALLATION.md"):
        text = (REPO_ROOT / relative_path).read_text(encoding="utf-8")
        assert "codex '@feature-decomposer" in text
        assert "`-p`/`--profile`" in text
        assert "configuration" in text


def test_router_explains_profile_and_designator_semantics() -> None:
    text = (
        REPO_ROOT
        / "source_of_truth"
        / "skills"
        / "agent-designator-router"
        / "SKILL.md"
    ).read_text(encoding="utf-8")

    assert "`codex -p feature-decomposer ...` selects a configuration" in text
    assert "The designator is prompt text interpreted by this skill" in text


def test_feature_decomposition_cannot_finish_at_plan_files() -> None:
    agent = (
        REPO_ROOT / "source_of_truth" / "agents" / "03-feature-decomposer.agent.md"
    ).read_text(encoding="utf-8")
    skill = (
        REPO_ROOT / "source_of_truth" / "skills" / "feature-plan-set" / "SKILL.md"
    ).read_text(encoding="utf-8")

    assert "## Completion Contract" in agent
    assert "plans alone" in agent
    assert "same uninterrupted workflow" in skill


def test_codex_profiles_are_not_generated_agent_entry_points() -> None:
    profiles = REPO_ROOT / "ports" / "codex" / "profiles"
    assert not list(profiles.glob("*.config.toml"))
