"""Focused guards for the audit-comparison skill and its Audit - Delta consumer.

The generic corpus tests cover frontmatter and generated topology.  These
guards own the semantic contract, keep checks bounded to the source sections
that carry each obligation, and exercise their load-bearing text in memory so
that a green result is not vacuous.

Phase - Execute was a third consumer until its audit bookend was removed.  The
guards below now assert the opposite: that the bookend has not crept back in.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import propagate_master_assets as propagator  # noqa: E402


SOURCE_AGENTS = REPO_ROOT / "source_of_truth" / "agents"
SOURCE_SKILLS = REPO_ROOT / "source_of_truth" / "skills"
SKILL_PATH = SOURCE_SKILLS / "audit-comparison" / "SKILL.md"
DELTA_PATH = SOURCE_AGENTS / "delta-auditor.agent.md"
PHASE_EXECUTE_PATH = SOURCE_AGENTS / "03-phase-execute.agent.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _normal(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _section(text: str, heading: str, next_heading: str | None = None) -> str:
    start = text.find(heading)
    assert start >= 0, f"missing named section: {heading}"
    end = len(text) if next_heading is None else text.find(next_heading, start + len(heading))
    assert end >= 0, f"missing section boundary after: {heading}"
    return text[start:end]


def _skill_errors(text: str) -> set[str]:
    errors: set[str] = set()
    normalized = _normal(text)
    assert text.count("---") >= 2, "audit-comparison frontmatter is missing"
    frontmatter = text.split("---", 2)[1]
    for field in ("name: audit-comparison", "description:"):
        if field not in frontmatter:
            errors.add(f"skill frontmatter: {field}")
    required = {
        "output-root ownership": "output_root",
        "output root confinement": "Every report, summary, delta, queue, and attribution update is written below this root.",
        "audit matrix": "audit_matrix",
        "single prompt template": "audit_prompt_template",
        "resolved references": "ref_targets",
        "report gate": "both snapshot artifacts are present",
        "provisional delta": "do not present it as a regression",
        "attribution sum": "sum exactly to the delta's unattributed total",
        "cleanup after attribution": "After the attribution stage completes",
    }
    for obligation, phrase in required.items():
        if _normal(phrase) not in normalized:
            errors.add(obligation)
    if "?" in text or re.search(r"\b(ask|offer|confirm)\b", text, re.I):
        errors.add("shared skill is interactive")
    return errors


def _delta_errors(text: str) -> set[str]:
    errors: set[str] = set()
    phase1 = _section(text, "### Phase 1: Determine Audit Types", "### Phase 2:")
    phase2 = _section(text, "### Phase 2: Confirm Targets and Scope", "### Phase 3:")
    phase5 = _section(text, "### Phase 5: Confirm the Audit Matrix", "### Phase 6:")
    phase6 = _section(text, "### Phase 6: Run the Shared Comparison", "### Phase 6b:")
    phase7 = _section(text, "### Phase 7: Fix Research for the Open-Items Queue", "### Phase 8:")
    phase8 = _section(text, "### Phase 8: Remediation")
    checks = {
        "delta type interaction": "What type of audit would you like to run?",
        "delta target interaction": "A target is either a **directory**",
        "delta matrix confirmation": "State the matrix back to the user",
        "delta skill handoff": "Load the `audit-comparison` skill",
        "delta conditional offer": "Would you like a delta document comparing the two audits?",
        "delta fix-research offer": "Would you like researched fix proposals for the open-items queue?",
        "delta remediation": "Load the `audit-remediation-pipeline` skill",
    }
    sections = {
        "delta type interaction": phase1,
        "delta target interaction": phase2,
        "delta matrix confirmation": phase5,
        "delta skill handoff": phase6,
        "delta conditional offer": phase6,
        "delta fix-research offer": phase7,
        "delta remediation": phase8,
    }
    for obligation, phrase in checks.items():
        if phrase not in sections[obligation]:
            errors.add(obligation)
    mechanics = (
        "Materialize ref targets",
        "Execute the audit matrix",
        "Gate and run each delta",
        "Settle attribution",
        "Release materialized worktrees",
    )
    for title in mechanics:
        if f"### {title}" in text:
            errors.add(f"delta duplicates shared mechanic: {title}")
    return errors


def _phase_errors(text: str) -> set[str]:
    """Phase - Execute must carry no audit bookend and must keep a phase-close audit.

    The bookend ran a two-snapshot audit matrix, a delta, and an attribution
    pass at every phase close. It was removed because it was declined every
    time. Auditor - Refactor's architecture backstop outlived it, then was cut
    too: it duplicated Prod Code Review as a second phase-close gate. What must
    survive is the property the backstop carried and the level-closure rows
    never did - a phase-close audit whose absence blocks all-approved.
    """
    errors: set[str] = set()
    for phrase in ("bookend", "audit-comparison", "Auditor - Delta", "Auditor - Attribution", "Baseline Worktree", "Auditor - Refactor"):
        if phrase in text:
            errors.add(f"audit bookend residue: {phrase}")
    heading = "### Step 3: Phase-Close Review"
    if heading not in text:
        errors.add("phase-close audit")
        return errors
    audits = _section(text, heading, "### Step 5:")
    if "Spawn **04d Consistency Auditor**, **04f Test Health**, and **03e Diff Security Scan** concurrently" not in audits:
        errors.add("phase-close audit")
    if "phase-close-audits: absent" not in audits:
        errors.add("absent audit is not clean")
    return errors


def _topology_errors() -> set[str]:
    agents = propagator.load_source_agents()
    assert agents, "source corpus loader returned no agents"
    by_name = {agent.name: agent for agent in agents}
    phase = by_name.get("03 Phase - Execute")
    assert phase is not None, "Phase Execute is absent from the source corpus"
    # Leaves the removed bookend owned. A roster entry with no prose to spawn it
    # is how a removed stage half-returns.
    removed = {
        "Auditor - Code",
        "Auditor - Infra",
        "Auditor - Refactor",
        "Auditor - Delta",
        "Auditor - Attribution",
        "Baseline Worktree",
    }
    errors: set[str] = set()
    stale = removed & set(phase.subagents)
    if stale:
        errors.add(f"Phase Execute still rosters bookend leaves: {sorted(stale)}")
    for leaf in ("04d Consistency Auditor", "04f Test Health"):
        if leaf not in set(phase.subagents):
            errors.add(f"Phase Execute dropped the phase-close audit leaf: {leaf}")
    return errors


def test_finalized_skill_and_consumers_have_no_contract_errors() -> None:
    skill = _read(SKILL_PATH)
    delta = _read(DELTA_PATH)
    phase = _read(PHASE_EXECUTE_PATH)
    assert not _skill_errors(skill)
    assert not _delta_errors(delta)
    assert not _phase_errors(phase)
    assert not _topology_errors()
    assert skill.count("name: audit-comparison") == 1
    assert delta.count("audit-comparison") == 1
    assert phase.count("audit-comparison") == 0


@pytest.mark.parametrize(
    ("label", "path", "anchor", "validator", "expected"),
    [
        ("skill output root", SKILL_PATH, "Every report, summary, delta, queue, and attribution update is written below\n  this root.", _skill_errors, "output root confinement"),
        ("skill cleanup", SKILL_PATH, "After the attribution stage completes", _skill_errors, "cleanup after attribution"),
        ("delta matrix", DELTA_PATH, "State the matrix back to the user", _delta_errors, "delta matrix confirmation"),
        ("phase-close audit", PHASE_EXECUTE_PATH, "Spawn **04d Consistency Auditor**, **04f Test Health**, and **03e Diff Security Scan** concurrently", _phase_errors, "phase-close audit"),
    ],
)
def test_load_bearing_deletion_is_red(
    label: str, path: Path, anchor: str, validator, expected: str,  # type: ignore[no-untyped-def]
) -> None:
    original = _read(path)
    assert anchor in original, f"mutation target missing: {label}"
    mutated = original.replace(anchor, "", 1)
    errors = validator(mutated)
    assert errors, f"inert guard for {label}"
    assert expected in errors, f"{label} mutation failed for an incidental obligation: {sorted(errors)}"
    assert not validator(original)


@pytest.mark.parametrize(
    ("label", "replacement", "mutation", "expected"),
    [
        (
            "bookend returns",
            "Spawn **04d Consistency Auditor**, **04f Test Health**, and **03e Diff Security Scan** concurrently",
            "Run the accepted audit bookend, then spawn `04d Consistency Auditor` and `04f Test Health` concurrently",
            "audit bookend residue: bookend",
        ),
        (
            "refactor auditor returns",
            "Spawn **04d Consistency Auditor**, **04f Test Health**, and **03e Diff Security Scan** concurrently",
            "Spawn **Auditor - Refactor** concurrently",
            "audit bookend residue: Auditor - Refactor",
        ),
        (
            "phase-close audit heading dropped",
            "### Step 3: Phase-Close Review",
            "### Step 3: Notes",
            "phase-close audit",
        ),
        (
            "absent audit reads clean",
            "phase-close-audits: absent",
            "phase-close-audits: fine",
            "absent audit is not clean",
        ),
    ],
)
def test_semantic_negation_kills_the_named_guard(
    label: str, replacement: str, mutation: str, expected: str,
) -> None:
    original = _read(PHASE_EXECUTE_PATH)
    assert replacement in original, f"mutation target missing: {label}"
    errors = _phase_errors(original.replace(replacement, mutation))
    assert expected in errors, f"{label} did not trip {expected}: {sorted(errors)}"
    assert not _phase_errors(original)


def test_focused_module_never_reads_generated_outputs() -> None:
    assert "ports" not in str(SKILL_PATH)
    assert ".github" not in str(SKILL_PATH)
    assert "source_of_truth" in str(SKILL_PATH)
