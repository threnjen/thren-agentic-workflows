import _propagate_env as env


def test_codex_profiles_are_not_generated_agent_entry_points() -> None:
    profiles = env.propagated_ports() / "codex" / "profiles"
    assert profiles.is_dir(), "propagation did not create the codex profiles directory"
    assert not list(profiles.glob("*.config.toml"))
