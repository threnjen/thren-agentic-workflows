from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_codex_profiles_are_not_generated_agent_entry_points() -> None:
    profiles = REPO_ROOT / "ports" / "codex" / "profiles"
    assert not list(profiles.glob("*.config.toml"))
