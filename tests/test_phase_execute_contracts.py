"""Structural guards for the slim Phase - Execute contract."""

from __future__ import annotations

import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_PATH = REPO_ROOT / "source_of_truth/agents/03-phase-execute.agent.md"
IMPLEMENTER_PATH = REPO_ROOT / "source_of_truth/agents/03b-feature-implementer.agent.md"
LOOP_PATH = REPO_ROOT / "source_of_truth/skills/implementation-pipeline-loop/SKILL.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _gate_remediation_wiring_errors(loop: str, implementer: str) -> set[str]:
    errors: set[str] = set()
    if (
        "**Phase**" not in loop
        or "once in `gate-remediation` mode" not in loop
        or "A failed rerun blocks the feature and its dependents" not in loop
    ):
        errors.add("phase loop invokes bounded remediation")
    if (
        "### Gate Remediation Mode" not in implementer
        or "Reproduce every named failure" not in implementer
        or "run the supplied full gate once" not in implementer
        or "Return after this mode" not in implementer
    ):
        errors.add("implementer handles gate remediation")
    return errors


REMOVED_PHASE_AGENTS = (
    "03e Diff Security Scan",
    "03j Reviewer - Blast Radius",
    "03k Reviewer - Test Falsification",
    "03l Reviewer - Plan Blind",
    "03m Finding Consolidator",
    "03n Finding Validator",
    "03p Feature - Fixer",
    "04d Consistency Auditor",
    "04e Dependency Auditor",
    "04f Test Health",
    "04h Cleanliness Auditor",
    "Unity Reviewer",
)


def test_every_body_spawn_resolves_to_an_agent_on_disk() -> None:
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    import propagate_master_assets as mod

    known = {agent.name for agent in mod.load_source_agents()}
    body = _read(PHASE_PATH).split("---", 2)[2]
    spawned = set(re.findall(r"[Ss]pawn (?:the )?\*\*(.+?)\*\*", body))
    assert spawned
    assert not sorted(name for name in spawned if name not in known)


def test_phase_has_no_close_review_fleet() -> None:
    text = _read(PHASE_PATH)
    frontmatter = text.split("---", 2)[1]
    body = text.split("---", 2)[2]
    for name in REMOVED_PHASE_AGENTS:
        assert name not in frontmatter
        assert f"Spawn **{name}**" not in body
    assert "Phase-Close Review" not in body


def test_opening_interaction_is_one_block_with_conditional_resume() -> None:
    text = _read(PHASE_PATH)
    section = text.split("## Opening Interaction", 1)[1].split("## Step 1:", 1)[0]
    for token in (
        "model overrides",
        "run: plan-only | full",
        "qa: yes | no",
        "relevant uncommitted implementation files",
    ):
        assert token in section
    assert "A clean interrupted run resumes automatically" in section
    assert "Departure Preflight" in section


def test_phase_starts_green_or_does_not_start() -> None:
    text = _read(PHASE_PATH)
    section = text.split("## Step 1: Prove the Starting State", 1)[1].split("## Step 2:", 1)[0]
    for token in ("full authoritative test suite", "unfiltered", "stop immediately", "Do not spawn a single agent"):
        assert token in section
    assert "no baseline exemption list" in section


def test_phase_uses_plan_delta_and_manifest_only() -> None:
    text = _read(PHASE_PATH)
    schedule = text.split("## Step 2: Obtain the Schedule", 1)[1].split("## Step 3:", 1)[0]
    selection = text.split("### A. Select and Discover", 1)[1].split("### B.", 1)[0]
    assert "no `-context.md`, `-tasks.md`, or `-delta.md` files" in schedule
    assert "exactly one `-delta.md`" in selection
    assert "only when verified source contradicts" in selection


def test_plan_only_run_stops_before_implementation_and_full_run_adopts_it() -> None:
    text = _read(PHASE_PATH)
    opening = text.split("## Opening Interaction", 1)[1].split("## Step 1:", 1)[0]
    selection = text.split("### A. Select and Discover", 1)[1].split("### B.", 1)[0]
    assert "Use `full` as the default" in opening
    assert "Do not add a resume choice for that handoff" in opening
    assert "Skip the `select` spawn when the adopted selection is current" in selection
    for condition in (
        "`-delta.md` exists",
        "has no implementation record",
        "equals the current `HEAD` commit",
    ):
        assert condition in selection
    assert "When any condition fails, spawn `select` mode" in selection
    assert "On a `plan-only` run, stop here. Run no later step." in selection


def test_feature_loop_is_bounded_and_blocks_regressions() -> None:
    text = _read(PHASE_PATH)
    review = text.split("### C. Review and Repair Once", 1)[1].split("### D.", 1)[0]
    gate = text.split("##### D. Integration test gate", 1)[1].split("##### E.", 1)[0]
    assert "one review-and-repair pass" in review
    assert "Never spawn it twice" in review
    assert "once in `gate-remediation` mode" in gate
    assert "exact failing test names" in gate
    assert "Do not spawn the reviewer again" in gate
    assert "run the named failures first" in gate
    assert "If they pass, rerun the full integration command" in gate
    assert "Never open a second gate-remediation pass" in gate
    assert "If any rerun fails" in gate
    assert "Block every dependent feature" in gate
    assert "recorded revert commit" in gate
    assert "Never rewrite branch history" in gate


def test_gate_remediation_is_wired_to_the_implementer() -> None:
    errors = _gate_remediation_wiring_errors(_read(LOOP_PATH), _read(IMPLEMENTER_PATH))
    assert not errors, sorted(errors)


def test_gate_remediation_wiring_mutations_are_killed() -> None:
    loop = _read(LOOP_PATH)
    implementer = _read(IMPLEMENTER_PATH)

    mutated_loop = loop.replace(
        "once in `gate-remediation` mode",
        "without a remediation mode",
        1,
    )
    assert "phase loop invokes bounded remediation" in _gate_remediation_wiring_errors(
        mutated_loop, implementer
    )

    mutated_implementer = implementer.replace(
        "### Gate Remediation Mode",
        "### Generic Repair Mode",
        1,
    )
    assert "implementer handles gate remediation" in _gate_remediation_wiring_errors(
        loop, mutated_implementer
    )


def test_optional_qa_and_documentation_gates_are_explicit() -> None:
    text = _read(PHASE_PATH)
    qa = text.split("## Step 4: Optional Consolidated QA", 1)[1].split("## Step 5:", 1)[0]
    close = text.split("## Step 6: Documentation and Handoff", 1)[1]
    assert "qa: skipped (user choice)" in qa
    assert "Skipped QA is excluded from `all-approved`" in qa
    assert "GO` or `GO WITH CONDITIONS" in close
    assert "Never run it after `NO-GO`" in close
    assert "`phase-final-checks`" in close
