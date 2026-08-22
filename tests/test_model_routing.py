"""Structural guards for abstract agent tiers and harness model routing."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import propagate_master_assets as mod  # noqa: E402


PIPELINE_AGENT_SLUGS = (
    "04a-feature-plan-expander",
    "04b-feature-implementer",
    "04c-feature-review-and-fix",
    "04h-unity-reviewer",
    "04g-unity-visual-verification",
    "04d-feature-qa-writer",
    "04i-feature-qa-runner",
    "04e-diff-security-scan",
    "04f-prod-code-review",
    "auditor-code",
    "auditor-infra",
    "auditor-delta",
    "auditor-attribution",
    "05a-baseline-worktree",
    "05h-cleanliness-auditor",
    "05e-dependency-auditor",
    "05d-consistency-auditor",
    "05f-test-health",
    "auditor-refactor",
)


def _agent(slug: str):
    return next(agent for agent in mod.load_source_agents() if agent.source_slug == slug)


def test_routing_contains_every_tier_and_harness() -> None:
    routing = mod.load_model_routing()

    assert set(routing) == set(mod.MODEL_TIERS)
    for tier in mod.MODEL_TIERS:
        assert set(routing[tier]) == set(mod.MODEL_HARNESSES)
        for harness in mod.MODEL_HARNESSES:
            assert routing[tier][harness]["model"]


def test_tier_counts_are_inventory_counters() -> None:
    counters = {
        "source_agents": 23,
        "claude_tiered_agents": 19,
        "codex_tiered_agents": 19,
        "opencode_tiered_agents": 19,
        "cursor_tiered_agents": 19,
        "github_tiered_agents": 19,
        "claude_changed": 1,
    }

    assert mod.propagation_changes(counters) == {"claude_changed": 1}


def test_invalid_model_tier_names_the_agent_file() -> None:
    with pytest.raises(ValueError, match=r"source_of_truth/agents/example\.agent\.md"):
        mod._parse_model_tier("source_of_truth/agents/example.agent.md", "urgent")


def test_tier_coverage_uses_the_named_pipeline_roster() -> None:
    agents = {agent.source_slug: agent for agent in mod.load_source_agents()}
    missing = [slug for slug in PIPELINE_AGENT_SLUGS if not agents[slug].model_tier]
    assert not missing, f"pipeline agent tier coverage missing: {', '.join(missing)}"


def test_user_invocability_decides_whether_tier_is_present() -> None:
    unexpected_tiers = [
        agent.source_slug
        for agent in mod.load_source_agents()
        if agent.user_invocable and agent.model_tier
    ]
    assert not unexpected_tiers, (
        "user-invocable agents must omit model_tier because tier presence is decided by "
        "the agent's own invocability: "
        + ", ".join(unexpected_tiers)
    )

    docs_writer = _agent("docs-writer")
    assert docs_writer.user_invocable
    assert docs_writer.model_tier is None


def test_source_agent_bodies_do_not_contain_routed_model_identifiers() -> None:
    routed_models = {
        entry["model"]
        for tier in mod.load_model_routing().values()
        for entry in tier.values()
    }
    offenders = [
        agent.rel_path
        for agent in mod.load_source_agents()
        if any(model in agent.body for model in routed_models)
    ]
    assert not offenders, f"harness model identifier leaked into source agent body: {offenders}"


def test_renderers_emit_the_route_for_a_tiered_agent() -> None:
    agent = _agent("04c-feature-review-and-fix")
    docs = mod.applicable_instructions(agent, mod.load_instruction_docs())
    routing = mod.load_model_routing()
    claude_stems = mod._discover_existing_stems(mod.CLAUDE_AGENTS_DIR)
    opencode_stems = mod._discover_existing_stems(mod.OPENCODE_AGENTS_DIR)
    claude_refs = mod._build_agent_reference_map(
        mod.load_source_agents(),
        lambda candidate: mod._claude_identifier_for(candidate, claude_stems),
    )
    opencode_refs = mod._build_agent_reference_map(
        mod.load_source_agents(),
        lambda candidate: mod._opencode_identifier_for(candidate, opencode_stems),
    )
    codex_refs = mod._build_agent_reference_map(mod.load_source_agents(), mod._codex_identifier_for)
    medium = routing[agent.model_tier]["codex"]["model"]

    claude = mod.render_claude_agent(agent, docs, claude_refs, "z-feature-review-and-fix", routing)
    codex = mod.render_codex_agent(agent, docs, codex_refs, routing)
    opencode = mod.render_opencode_agent(agent, docs, opencode_refs, routing)
    cursor = mod.render_cursor_agent(agent, docs, claude_refs, "z-feature-review-and-fix", routing)
    github = mod._github_agent_bytes(agent.path, agent.path.read_bytes(), routing).decode("utf-8")

    assert f"model: {routing[agent.model_tier]['claude']['model']}" in claude
    assert f'model = "{medium}"' in codex
    assert f'model_reasoning_effort = "{routing[agent.model_tier]["codex"]["reasoning_effort"]}"' in codex
    assert f"model: {routing[agent.model_tier]['opencode']['model']}" in opencode
    assert f"model: {routing[agent.model_tier]['cursor']['model']}" in cursor
    assert f"model: {routing[agent.model_tier]['github']['model']}" in github


def test_missing_route_fails_before_output_directory_is_created(tmp_path: Path, monkeypatch) -> None:
    source_root = tmp_path / "source_of_truth"
    config_path = source_root / "config" / "model-routing.json"
    config_path.parent.mkdir(parents=True)
    routing = json.loads((REPO_ROOT / "source_of_truth/config/model-routing.json").read_text())
    del routing["high"]["codex"]
    config_path.write_text(json.dumps(routing), encoding="utf-8")
    monkeypatch.setattr(mod, "SOT_DIR", source_root)
    agent = mod.SourceAgent(
        path=tmp_path / "example.agent.md",
        rel_path="source_of_truth/agents/example.agent.md",
        source_slug="example",
        name="Example",
        description="Example",
        tools=[],
        subagents=[],
        user_invocable=False,
        body="",
        model_tier="high",
    )
    monkeypatch.setattr(mod, "load_source_agents", lambda: [agent])
    monkeypatch.setattr(mod, "load_instruction_docs", lambda: [])

    with pytest.raises(ValueError, match=r"model-routing\.json"):
        mod.propagate_once(verbose=False)

    assert not (tmp_path / "ports").exists()


def test_malformed_model_identifier_fails_before_execution(tmp_path: Path, monkeypatch) -> None:
    source_root = tmp_path / "source_of_truth"
    config_path = source_root / "config" / "model-routing.json"
    config_path.parent.mkdir(parents=True)
    routing = json.loads((REPO_ROOT / "source_of_truth/config/model-routing.json").read_text())
    routing["low"]["claude"]["model"] = "not a model identifier"
    config_path.write_text(json.dumps(routing), encoding="utf-8")
    monkeypatch.setattr(mod, "SOT_DIR", source_root)

    with pytest.raises(ValueError, match=r"invalid model"):
        mod.load_model_routing()

    assert not (tmp_path / "ports").exists()


def test_routing_file_contains_no_credential_shaped_value() -> None:
    text = (REPO_ROOT / "source_of_truth/config/model-routing.json").read_text(encoding="utf-8")
    assert not re.search(r"(?:sk-|ghp_|Bearer\s+|api[_-]?key\s*[:=])", text, re.IGNORECASE)
