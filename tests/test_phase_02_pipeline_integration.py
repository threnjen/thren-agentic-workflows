"""Cross-feature contracts for the Phase 02 execution pipeline.

These checks use the propagator's loaders so the test scope matches the assets
that the repository actually ships. They check names and structure, not prose
quality or live harness behavior.
"""

from __future__ import annotations

import fnmatch
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import propagate_master_assets as propagator  # noqa: E402


PHASE_PATH = REPO_ROOT / "source_of_truth/agents/03-phase-execute.agent.md"
MANIFEST_SKILL_PATH = REPO_ROOT / "source_of_truth/skills/feature-plan-set/SKILL.md"
LOOP_SKILL_PATH = REPO_ROOT / "source_of_truth/skills/implementation-pipeline-loop/SKILL.md"
RECORD_SKILL_PATH = REPO_ROOT / "source_of_truth/skills/implementation-record/SKILL.md"
PREFLIGHT_INSTRUCTIONS_PATH = (
    REPO_ROOT / "source_of_truth/instructions/orchestrator-conventions.instructions.md"
)
ROUTING_PATH = REPO_ROOT / "source_of_truth/config/model-routing.json"
POST_GATE_QA_PATH = REPO_ROOT / "docs/phases/PHASE_02/PHASE_02_POST_GATE_QA.md"

MANIFEST_FIELDS = (
    "status",
    "execution_order",
    "prerequisites",
    "expected_read_set",
    "expected_write_set",
    "plan_revision",
    "last_validation_commit",
    "stale_reason",
    "resolved_model_status",
)
PREFLIGHT_FIELDS = (
    "requested_model",
    "user_override",
    "resolved_route",
    "resolution_status",
)
REPORT_PATHS = {
    "03j-reviewer-blast-radius": "03j-reviewer-blast-radius-report.md",
    "03k-reviewer-test-falsification": "03k-reviewer-test-falsification-report.md",
    "03l-reviewer-plan-blind": "03l-reviewer-plan-blind-report.md",
    "03m-finding-consolidator": "03m-finding-consolidator-candidates.md",
    "03n-finding-validator": "03n-finding-validator-fix-list.md",
}
FINDING_FIELDS = ("severity", "lane", "evidence", "reviewer")
FIX_LIST_FIELDS = (
    "id",
    "severity",
    "lane",
    "finding",
    "evidence",
    "reviewers",
    "action",
    "status",
)
PHASE_CREATED_AGENTS = set(REPORT_PATHS)
FILE_TYPE_PATTERNS = {
    "**/*.cs",
    "**/*.py",
    "**/pyproject.toml",
    "**/*.ts",
    "**/*.tsx",
    "**/*.mts",
    "**/*.cts",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _agents() -> dict[str, propagator.SourceAgent]:
    return {agent.source_slug: agent for agent in propagator.load_source_agents()}


def _source_agent_paths() -> set[str]:
    return {agent.rel_path for agent in propagator.load_source_agents()}


def _agent_targeting_patterns() -> list[tuple[Path, str]]:
    patterns: list[tuple[Path, str]] = []
    for document in propagator.load_instruction_docs():
        for pattern in document.apply_to_patterns:
            if pattern not in FILE_TYPE_PATTERNS:
                patterns.append((document.path, pattern))
    return patterns


def _unresolved_agent_references(
    agents: dict[str, propagator.SourceAgent],
) -> list[str]:
    names = {agent.name for agent in agents.values()}
    return [
        f"{agent.source_slug}: {child}"
        for agent in agents.values()
        for child in agent.subagents
        if child not in names
    ]


def _phase_emits(agent: propagator.SourceAgent, referenced_names: set[str]) -> bool:
    return not agent.user_invocable or agent.name in referenced_names


def _generated_names(directory: Path, suffix: str, marker: str) -> set[str]:
    return {
        path.name
        for path in directory.glob(f"*{suffix}")
        if propagator._is_generated_output(path, marker)
    }


def _missing_tokens(text: str, tokens: tuple[str, ...]) -> set[str]:
    return {token for token in tokens if token not in text}


def _pattern_matches_any(pattern: str, agent_paths: set[str]) -> bool:
    return any(fnmatch.fnmatch(agent_path, pattern) for agent_path in agent_paths)


def _unresolved_agent_targeting_patterns(
    patterns: list[tuple[Path, str]], agent_paths: set[str]
) -> list[str]:
    return [
        f"{path.relative_to(REPO_ROOT)}: {pattern}"
        for path, pattern in patterns
        if not _pattern_matches_any(pattern, agent_paths)
    ]


def test_phase_consumers_resolve_producer_contracts() -> None:
    """Every named Phase 02 handoff has a producer and a consumer."""
    agents = _agents()
    phase = _read(PHASE_PATH)
    manifest_skill = _read(MANIFEST_SKILL_PATH)
    loop_skill = _read(LOOP_SKILL_PATH)
    record_skill = _read(RECORD_SKILL_PATH)
    conventions = _read(PREFLIGHT_INSTRUCTIONS_PATH)

    assert not _missing_tokens(manifest_skill, tuple(f"`{field}`" for field in MANIFEST_FIELDS))
    assert not _missing_tokens(phase, tuple(f"`{field}`" for field in MANIFEST_FIELDS))

    assert not _missing_tokens(phase, tuple(f"`{field}`" for field in PREFLIGHT_FIELDS))
    assert not _missing_tokens(conventions, tuple(f"`{field}`" for field in PREFLIGHT_FIELDS))

    for slug, report_name in REPORT_PATHS.items():
        body = agents[slug].body
        assert report_name in body, f"{slug} does not produce {report_name}"
        assert report_name in phase, f"phase does not consume {report_name}"

    for slug in REPORT_PATHS:
        if slug == "03m-finding-consolidator":
            continue
        body = agents[slug].body
        assert not _missing_tokens(body, FINDING_FIELDS)

    validator = agents["03n-finding-validator"].body
    assert not _missing_tokens(validator, FIX_LIST_FIELDS)
    assert "final fix list" in phase
    assert "Review findings" in record_skill

    routing = propagator.load_model_routing()
    assert set(routing) == set(propagator.MODEL_TIERS)
    assert all(tier in phase for tier in propagator.MODEL_TIERS)
    assert "load_model_routing()" not in phase


def test_phase_spawn_roster_and_frontmatter_references_resolve() -> None:
    agents = _agents()
    assert not _unresolved_agent_references(agents)

    phase = agents["03-phase-execute"]
    assert set(phase.subagents) <= {agent.name for agent in agents.values()}

    for slug in PHASE_CREATED_AGENTS:
        assert slug in agents
        assert agents[slug].name in phase.subagents


def test_agent_targeting_apply_to_globs_resolve_and_mutation_fails() -> None:
    agent_paths = _source_agent_paths()
    patterns = _agent_targeting_patterns()
    unresolved = _unresolved_agent_targeting_patterns(patterns, agent_paths)
    assert not unresolved, f"agent-targeting applyTo glob resolves to no agent: {unresolved}"

    document, pattern = patterns[0]
    mutated = [
        candidate
        for candidate in propagator.load_instruction_docs()
        if candidate.path == document
    ][0]
    invalid_pattern = "source_of_truth/agents/does-not-exist.agent.md"
    mutated_patterns = [
        (document, invalid_pattern if candidate == pattern else candidate)
        for candidate in mutated.apply_to_patterns
        if candidate not in FILE_TYPE_PATTERNS
    ]
    mutated_errors = _unresolved_agent_targeting_patterns(mutated_patterns, agent_paths)
    assert f"{document.relative_to(REPO_ROOT)}: {invalid_pattern}" in mutated_errors


def test_all_generated_harness_agent_sets_and_routes_match_source() -> None:
    """The suite's generated tree contains the current source agent set and routes."""
    agents = list(propagator.load_source_agents())
    instructions = propagator.load_instruction_docs()
    routing = propagator.load_model_routing()
    referenced_names = {
        child for agent in agents for child in agent.subagents
    }

    claude_stems = propagator._discover_existing_stems(propagator.CLAUDE_AGENTS_DIR)
    opencode_stems = propagator._discover_existing_stems(propagator.OPENCODE_AGENTS_DIR)
    claude_refs = propagator._build_agent_reference_map(
        agents, lambda agent: propagator._claude_identifier_for(agent, claude_stems)
    )
    opencode_refs = propagator._build_agent_reference_map(
        agents, lambda agent: propagator._opencode_identifier_for(agent, opencode_stems)
    )
    codex_refs = propagator._build_agent_reference_map(agents, propagator._codex_identifier_for)
    cursor_refs = propagator._build_agent_reference_map(
        agents,
        lambda agent: propagator._cursor_agent_identifier_for(
            propagator._claude_identifier_for(agent, claude_stems)
        ),
    )

    expected_claude = set()
    expected_cursor = set()
    expected_opencode = set()
    expected_codex = set()
    for agent in agents:
        docs = propagator.applicable_instructions(agent, instructions)
        claude_id = propagator._claude_identifier_for(agent, claude_stems)
        opencode_name = propagator._opencode_filename_for(agent, opencode_stems)
        codex_name = propagator._codex_filename_for(agent)
        expected_opencode.add(opencode_name)
        expected_codex.add(codex_name)

        if _phase_emits(agent, referenced_names):
            expected_claude.add(f"{claude_id}.md")
            cursor_id = propagator._cursor_agent_identifier_for(claude_id)
            expected_cursor.add(f"{cursor_id}.md")

            claude_path = propagator.CLAUDE_AGENTS_DIR / f"{claude_id}.md"
            cursor_path = propagator.CURSOR_AGENTS_DIR / f"{cursor_id}.md"
            assert claude_path.read_text(encoding="utf-8") == propagator.render_claude_agent(
                agent, docs, claude_refs, claude_id, routing
            )
            assert cursor_path.read_text(encoding="utf-8") == propagator.render_cursor_agent(
                agent, docs, cursor_refs, cursor_id, routing
            )

        opencode_path = propagator.OPENCODE_AGENTS_DIR / opencode_name
        codex_path = propagator.CODEX_AGENTS_DIR / codex_name
        assert opencode_path.read_text(encoding="utf-8") == propagator.render_opencode_agent(
            agent, docs, opencode_refs, routing
        )
        assert codex_path.read_text(encoding="utf-8") == propagator.render_codex_agent(
            agent, docs, codex_refs, routing
        )

        if agent.model_tier:
            route = routing[agent.model_tier]
            if _phase_emits(agent, referenced_names):
                assert f"model: {route['claude']['model']}" in claude_path.read_text(encoding="utf-8")
                assert f"model: {route['cursor']['model']}" in cursor_path.read_text(encoding="utf-8")
            assert f"model: {route['opencode']['model']}" in opencode_path.read_text(encoding="utf-8")
            assert f"model = \"{route['codex']['model']}\"" in codex_path.read_text(encoding="utf-8")

    assert _generated_names(
        propagator.CLAUDE_AGENTS_DIR, ".md", propagator.GENERATED_AGENT_MARKDOWN_HEADER
    ) == expected_claude
    assert _generated_names(
        propagator.CURSOR_AGENTS_DIR, ".md", propagator.GENERATED_AGENT_MARKDOWN_HEADER
    ) == expected_cursor
    assert _generated_names(
        propagator.OPENCODE_AGENTS_DIR, ".md", propagator.GENERATED_AGENT_MARKDOWN_HEADER
    ) == expected_opencode
    assert _generated_names(
        propagator.CODEX_AGENTS_DIR, ".toml", propagator.GENERATED_AGENT_HEADER
    ) == expected_codex

    for subdir in propagator.GITHUB_MIRRORED_SUBDIRS:
        source_dir = propagator.SOT_DIR / subdir
        for source_path in sorted(source_dir.rglob("*")):
            if not source_path.is_file() or source_path.is_symlink():
                continue
            relative = source_path.relative_to(source_dir)
            source_bytes = source_path.read_bytes()
            for destination_root in (propagator.GITHUB_PORT_DIR, propagator.DOT_GITHUB_DIR):
                destination = destination_root / subdir / relative
                assert destination.is_file(), destination
                if subdir == "agents":
                    expected_bytes = propagator._github_agent_bytes(
                        source_path, source_bytes, routing
                    )
                    assert destination.read_bytes() == expected_bytes
                else:
                    assert destination.read_bytes() == source_bytes


def test_integration_guards_fail_on_the_exact_contract_removal() -> None:
    """Each cross-feature guard proves that its required token is load-bearing."""
    phase = _read(PHASE_PATH)
    manifest = _read(MANIFEST_SKILL_PATH)
    loop = _read(LOOP_SKILL_PATH)
    routing_text = _read(ROUTING_PATH)
    agents = _agents()

    cases = (
        ("manifest", manifest, tuple(f"`{field}`" for field in MANIFEST_FIELDS)),
        (
            "schedule",
            phase,
            ("`execution_order`", "`expected_write_set`", "`last_validation_commit`"),
        ),
        ("routing", routing_text, ('"low":', '"medium":', '"high":')),
        ("committee", phase, tuple(REPORT_PATHS.values())),
        (
            "phase-close roster",
            phase,
            (
                "The roster is nine reviewers in three classes.",
                "**Repair-eligible (four)**",
                "**Advisory only (three)**",
                "Eligibility is set by lane, by blast radius.",
                "Only a finding from a repair-eligible lane can open it.",
                "`04d` consistency drift in particular is never auto-repaired",
                "Give it only the candidates drawn from the four repair-eligible lanes.",
                "Do not re-run the audits.",
                "Never open a second round.",
            ),
        ),
        (
            "review and fix",
            phase,
            (
                "The reviewer gets one round.",
                "never open a fix round of your own",
                "An unfixed finding is not a blocker here",
                "Only a `production-blocker` can block dependents",
                "A failing test the baseline does not name is a regression",
            ),
        ),
    )
    for label, text, tokens in cases:
        assert not _missing_tokens(text, tokens), label
        for token in tokens:
            mutated = text.replace(token, "", 1)
            assert token in _missing_tokens(mutated, tokens), f"inert {label} guard: {token}"

    for slug, report_name in REPORT_PATHS.items():
        body = agents[slug].body
        assert report_name in body
        assert report_name in _missing_tokens(body.replace(report_name, "", 1), (report_name,))

    routing = propagator.load_model_routing()
    assert set(routing) == set(propagator.MODEL_TIERS)


def test_post_gate_checklist_covers_live_only_claims() -> None:
    checklist = _read(POST_GATE_QA_PATH)
    required_sections = (
        "Claude Code",
        "Codex",
        "OpenCode",
        "Cursor",
        "GitHub Copilot",
        "copilot-instructions.md",
        "version",
        "Observation",
        "unchanged",
        "resolution_status",
    )
    assert not _missing_tokens(checklist, required_sections)
    assert "deploy_agents.py" in checklist
    assert "Do not run this checklist inside the phase" not in checklist
