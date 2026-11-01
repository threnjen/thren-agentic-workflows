"""Focused Phase 02 contract guards for the Refiner final-check integration.

These checks intentionally stay separate from the generic corpus invariants: the
corpus suite validates frontmatter and topology, while this module validates the
semantic ordering and delegation boundary in one source agent.  The validators
return named obligations so mutation tests prove that each guard is live.
"""

from __future__ import annotations

import fnmatch
import re
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import propagate_master_assets as propagator  # noqa: E402


SOURCE_AGENTS = REPO_ROOT / "source_of_truth" / "agents"
SOURCE_INSTRUCTIONS = REPO_ROOT / "source_of_truth" / "instructions"
SOURCE_SKILLS = REPO_ROOT / "source_of_truth" / "skills"
REFINER_PATH = SOURCE_AGENTS / "02-phase-refiner.agent.md"
REVIEWER_PATH = SOURCE_AGENTS / "02a-phase-final-check.agent.md"
READ_ONLY_INSTRUCTION_PATH = SOURCE_INSTRUCTIONS / "read-only-agent.instructions.md"
SKILL_PATH = SOURCE_SKILLS / "phase-final-check" / "SKILL.md"

PHASE_6_HEADING = "### Phase 6: Finalize the Phase Document"
OFFER_HEADING = "#### 6B: Validate the Written Document (Entry A + Entry B)"
VALIDATOR_NAME = "Plan - Adversarial Validator"
VALIDATOR_PATH = SOURCE_AGENTS / "adversarial-validator.agent.md"
PLANNER_PATH = SOURCE_AGENTS / "01-project-planner.agent.md"
SYNC_HEADING = "#### 6C: Synchronize the Completed Phase"
PHASE_7_HEADING = "### Phase 7: Open Working Branch"


def _source_agents() -> dict[str, propagator.SourceAgent]:
    agents = {agent.source_slug: agent for agent in propagator.load_source_agents()}
    assert agents, "agent loader returned no source agents"
    return agents


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _section(text: str, heading: str, next_heading: str | None = None) -> str:
    start = text.find(heading)
    if start < 0:
        return ""
    end = len(text)
    if next_heading is not None:
        next_start = text.find(next_heading, start + len(heading))
        if next_start >= 0:
            end = next_start
    return text[start:end]


def _normalized(text: str) -> str:
    return " ".join(text.split())


def _topology_errors(
    *,
    refiner_text: str | None = None,
    reviewer_text: str | None = None,
    instruction_text: str | None = None,
) -> set[str]:
    errors: set[str] = set()
    agents = _source_agents()
    refiner = agents.get("02-phase-refiner")
    reviewer = agents.get("02a-phase-final-check")

    if refiner is None:
        errors.add("refiner topology")
        return errors
    if reviewer is None:
        errors.add("reviewer topology")
    elif not reviewer.user_invocable and not reviewer.subagents and reviewer.tools == ["read", "search"]:
        pass
    else:
        errors.add("reviewer hidden leaf")

    expected_name = reviewer.name if reviewer is not None else "02a Phase - Final-Check Reviewer"
    if expected_name not in refiner.subagents:
        errors.add("exact Refiner roster")
    if not {"Web Researcher", "Docs Writer"}.issubset(refiner.subagents):
        errors.add("existing Refiner roster")
    if "agent" not in refiner.tools:
        errors.add("Refiner agent tool")

    instruction_text = (
        _read(READ_ONLY_INSTRUCTION_PATH)
        if instruction_text is None
        else instruction_text
    )
    instruction_fm, _ = propagator._parse_frontmatter(instruction_text)
    apply_to = str(instruction_fm.get("applyTo", "")).strip().strip('"').strip("'")
    patterns = [pattern.strip() for pattern in apply_to.split(",") if pattern.strip()]
    reviewer_rel_path = (
        reviewer.rel_path if reviewer is not None else "source_of_truth/agents/02a-phase-final-check.agent.md"
    )
    if not any(fnmatch.fnmatch(reviewer_rel_path, pattern) for pattern in patterns):
        errors.add("read-only applicability")

    refiner_body = refiner_text if refiner_text is not None else refiner.body
    reviewer_body = reviewer_text if reviewer_text is not None else (reviewer.body if reviewer else "")
    skill_reference = "`phase-final-check`"
    if skill_reference not in refiner_body or skill_reference not in reviewer_body:
        errors.add("shared phase-final-check skill")
    if "# Phase Final-Check Contract" in refiner_body or "# Phase Final-Check Contract" in reviewer_body:
        errors.add("no copied contract body")
    if not SKILL_PATH.is_file():
        errors.add("phase-final-check skill exists")

    return errors


def _workflow_errors(text: str) -> set[str]:
    errors: set[str] = set()
    phase_6 = _section(text, PHASE_6_HEADING, PHASE_7_HEADING)
    offer = _section(phase_6, OFFER_HEADING, SYNC_HEADING)
    sync = _section(phase_6, SYNC_HEADING)
    normalized_phase_6 = _normalized(phase_6)
    normalized_phase_6_lower = normalized_phase_6.lower()
    normalized_offer = _normalized(offer)
    normalized_sync = _normalized(sync)

    if text.count(PHASE_6_HEADING) != 1 or not phase_6:
        errors.add("Phase 6 scope")
    if text.count(OFFER_HEADING) != 1 or not offer:
        errors.add("one shared offer")
    if text.count(SYNC_HEADING) != 1 or not sync:
        errors.add("one synchronization section")
    if "Entry A" not in normalized_offer or "Entry B" not in normalized_offer:
        errors.add("entry convergence")

    write_position = normalized_phase_6_lower.find("write the phase document")
    offer_position = normalized_phase_6_lower.find("validate the written document")
    if write_position < 0 or offer_position < 0 or write_position >= offer_position:
        errors.add("document write before offer")

    if "without asking the user" not in normalized_offer.lower():
        errors.add("mandatory validation")
    if "advisory" not in normalized_offer.lower():
        errors.add("advisory findings")
    if VALIDATOR_NAME not in offer:
        errors.add("validator delegation")

    offer_lines = [line.strip().lower() for line in offer.splitlines()]
    if not any(line.startswith("- repository path:") for line in offer_lines) or not any(
        line.startswith("- phase document path:") for line in offer_lines
    ):
        errors.add("exact reviewer paths")
    if "02a Phase - Final-Check Reviewer" not in offer:
        errors.add("reviewer delegation")
    forbidden_boundary_terms = (
        "conversation content",
        "session summary",
        "settled-area briefing",
        "Refiner assessment",
    )
    if any(term.lower() not in normalized_offer.lower() for term in forbidden_boundary_terms):
        errors.add("blindness boundary")
    if "conversation content is required" in normalized_offer.lower():
        errors.add("blindness boundary")

    failure_tokens = set(re.findall(r"[a-z]+(?:-[a-z]+)?", normalized_offer.lower()))
    if not {"error", "timeout", "unusable"}.issubset(failure_tokens):
        errors.add("reviewer failure states")
    if "failure in one line" not in normalized_offer.lower():
        errors.add("one-line failure report")
    if "do not retry" not in normalized_offer.lower() or "do not perform the review inline" not in normalized_offer.lower():
        errors.add("no retry or inline review")
    if "unchanged document" not in normalized_offer.lower():
        errors.add("failure unchanged continuation")

    if "usable findings, judge each finding" not in normalized_offer.lower():
        errors.add("orchestrator judges findings")
    if "justified and has one reasonable fix" not in normalized_offer.lower() or "apply it without asking" not in normalized_offer.lower():
        errors.add("justified findings auto-applied")
    if "every decision the user settled" not in normalized_offer.lower():
        errors.add("settled decisions protected")
    if "reverses a settled decision, changes scope, or has more than one workable form" not in normalized_offer.lower():
        errors.add("decide outcome triggers")
    if "relay each decide finding verbatim" not in normalized_offer.lower() or "as a decision under question triage" not in normalized_offer.lower():
        errors.add("decide findings escalated")
    if "each applied finding one line" not in normalized_offer.lower() or "each rejected finding one line" not in normalized_offer.lower():
        errors.add("applied and rejected findings reported")
    if "applied and user-accepted findings only" not in normalized_offer.lower():
        errors.add("accepted findings rewrite")
    if "clean current source of truth" not in normalized_offer.lower():
        errors.add("clean rewrite")
    if "never add change-log framing" not in normalized_offer.lower():
        errors.add("no change-log framing")
    if "no finding is applied or accepted" not in normalized_offer.lower() or "do not rewrite" not in normalized_offer.lower():
        errors.add("zero accepted findings")
    if "do not create a findings artifact" not in normalized_offer.lower():
        errors.add("no findings artifact")

    if normalized_sync.count("phase-scoped discovery-context") != 1:
        errors.add("discovery synchronization once")
    if normalized_sync.count("roadmap synchronization") != 1:
        errors.add("roadmap synchronization once")
    if "after validation and any fold-in" not in normalized_sync.lower():
        errors.add("sync after fold-in")
    phase_7_position = text.find(PHASE_7_HEADING)
    if phase_7_position < 0 or phase_7_position <= text.find(SYNC_HEADING):
        errors.add("branch after synchronization")
    phase_7 = _section(text, PHASE_7_HEADING)
    if "create or resume" not in _normalized(phase_7).lower():
        errors.add("branch create or resume")
    if "eval: phase-affirmed" not in phase_7:
        errors.add("phase-affirmed commit")
    return errors


def test_phase_final_check_topology_and_shared_skill() -> None:
    assert not _topology_errors()


def test_read_only_target_deletion_is_detected() -> None:
    instruction = _read(READ_ONLY_INSTRUCTION_PATH)
    mutated = instruction.replace(
        "**/02a-phase-final-check.agent.md", "**/02a-phase-final-check-removed.agent.md", 1
    )
    assert "read-only applicability" in _topology_errors(instruction_text=mutated)


def test_shared_skill_reference_deletion_is_detected() -> None:
    refiner = _read(REFINER_PATH)
    reviewer = _read(REVIEWER_PATH)
    mutated = refiner.replace("`phase-final-check`", "`missing-phase-final-check`", 1)
    assert "shared phase-final-check skill" in _topology_errors(
        refiner_text=mutated, reviewer_text=reviewer
    )


def test_phase_refiner_workflow_contract() -> None:
    errors = _workflow_errors(_read(REFINER_PATH))
    assert not errors, sorted(errors)


@pytest.mark.parametrize(
    ("needle", "replacement", "obligation"),
    [
        ("#### 6B: Validate the Written Document (Entry A + Entry B)", "#### 6B: Entry-specific notes", "one shared offer"),
        ("Write the phase document in place", "Review the draft before writing the phase document", "document write before offer"),
        ("without asking the user", "if the user accepts", "mandatory validation"),
        ("are advisory", "are blocking", "advisory findings"),
        ("and `Plan - Adversarial Validator` once each", "once", "validator delegation"),
        ("repository path", "conversation summary", "exact reviewer paths"),
        ("phase document path", "Refiner assessment", "exact reviewer paths"),
        ("conversation content", "conversation content is required", "blindness boundary"),
        ("error, timeout, or unusable output", "successful output", "reviewer failure states"),
        ("failure in one line", "failure in a detailed report", "one-line failure report"),
        ("Do not retry", "Retry as needed", "no retry or inline review"),
        ("usable findings, judge each finding", "usable findings, relay each finding", "orchestrator judges findings"),
        ("Apply it without asking", "Ask the user whether to apply it", "justified findings auto-applied"),
        ("every decision the user settled", "the current wording", "settled decisions protected"),
        ("reverses a settled decision, changes scope, or has more than one workable form", "is large", "decide outcome triggers"),
        ("Relay each Decide finding verbatim", "Summarize each Decide finding", "decide findings escalated"),
        ("each applied finding one line", "each applied finding no report", "applied and rejected findings reported"),
        ("each rejected finding one line", "each rejected finding no report", "applied and rejected findings reported"),
        ("applied and user-accepted findings only", "all findings", "accepted findings rewrite"),
        ("Never add change-log framing", "Add change-log framing", "no change-log framing"),
        ("no finding is applied or accepted", "every finding is applied or accepted", "zero accepted findings"),
        ("Do not create a findings artifact", "Create a findings artifact", "no findings artifact"),
        ("after validation and any fold-in", "before validation and fold-in", "sync after fold-in"),
        ("phase-scoped discovery-context", "phase-scoped notes", "discovery synchronization once"),
        ("roadmap synchronization", "roadmap update", "roadmap synchronization once"),
        ("eval: phase-affirmed", "eval: phase-draft", "phase-affirmed commit"),
    ],
)
def test_workflow_mutations_are_killed(
    needle: str, replacement: str, obligation: str
) -> None:
    text = _read(REFINER_PATH)
    assert needle in text, f"mutation target missing for {obligation}"
    assert obligation in _workflow_errors(text.replace(needle, replacement, 1))


def test_adversarial_validator_is_a_hidden_leaf_with_a_bounded_return() -> None:
    validator = _source_agents()["adversarial-validator"]
    assert validator.name == VALIDATOR_NAME
    assert not validator.user_invocable
    assert not validator.subagents
    assert validator.tools == ["read", "search"]
    assert "one to three reasons" in validator.body
    instruction_fm, _ = propagator._parse_frontmatter(_read(READ_ONLY_INSTRUCTION_PATH))
    assert "**/adversarial-validator.agent.md" in str(instruction_fm["applyTo"])


def test_planner_always_runs_the_adversarial_validator_after_writing() -> None:
    planner = _source_agents()["01-project-planner"]
    assert VALIDATOR_NAME in planner.subagents
    body = _normalized(planner.body)
    write_position = body.find("Write exactly one phase summary")
    validate_position = body.find("Validate the written documents")
    commit_position = body.find("eval: plan-affirmed")
    assert 0 <= write_position < validate_position < commit_position
    assert "every time the user approves a write, without asking the user" in body


def test_workflow_scope_non_vacuity_is_enforced() -> None:
    text = _read(REFINER_PATH)
    assert _workflow_errors(text.replace(PHASE_6_HEADING, "### Phase 6: Removed", 1))
    assert _workflow_errors(text.replace(OFFER_HEADING, "#### 6B: Removed", 1))
    assert _workflow_errors(text.replace(SYNC_HEADING, "#### 6C: Removed", 1))
