"""Focused Phase 03 guards for the audit-comparison bookend contracts.

The generic corpus tests cover frontmatter and generated topology.  These
guards own the semantic contract, keep checks bounded to the source sections
that carry each obligation, and exercise their load-bearing text in memory so
that a green result is not vacuous.
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
    errors: set[str] = set()
    step1 = _section(text, "### Step 1: Research, Decompose, and Validate the Schedule", "### Step 2:")
    step5 = _section(text, "### Step 5: Diff Security Review", "### Step 5.5:")
    bookend = _section(text, "### Step 5.5: Audit Bookend", "### Step 6:")
    step6 = _section(text, "### Step 6: Phase Final Review", "### Step 7:")
    required = {
        "one-time choice": (step1, "This is the only bookend decision"),
        "scope resolution": (step1, "one uncapped reference-search hop"),
        "code selection": (step1, "Always select `Auditor - Code`"),
        "infra conditional": (step1, "Auditor - Infra` if and only if"),
        "dependency level before bookend": (
            text,
            "Run the accepted bookend only after all dependency levels",
        ),
        "step five before bookend": (text, "existing Step 5 Diff Security Review have completed"),
        "skill handoff": (bookend, "Load the exact `audit-comparison` skill"),
        "prompt identity": (bookend, "only snapshot-varying fields are `target_root`, `snapshot_label`, and `output_directory`"),
        "manifest intent": (bookend, "manifest supplies scope and intent"),
        "docs exclusion": (bookend, "standalone documentation is excluded"),
        "test lens": (bookend, "Categories 2, 5, 8, and 9"),
        "full report gate": (bookend, "Require both corresponding full findings reports"),
        "attribution gate": (bookend, "disjoint subsystem batches whose assigned counts sum"),
        "pre-attribution regression": (bookend, "Do not present a regression before attribution"),
        "cleanup ordering": (bookend, "release only a worktree created by this run after attribution"),
        "bounded remediation": (bookend, "only High/Critical findings settled as caused by this phase"),
        "non-comparable addendum": (bookend, "explicitly non-comparable verification addendum"),
        "step six evidence": (step6, "complete Step 5.5 bookend evidence"),
        "fast-track branch": (step6, "Complete pipeline `all-approved: yes`"),
        "standard fallback": (step6, "Complete pipeline `all-approved: no`"),
    }
    for obligation, (scope, phrase) in required.items():
        if phrase not in scope:
            errors.add(obligation)
    if step1.count("The resolved audit bookend contains") != 1:
        errors.add("scope choice appears exactly once")
    if text.find("### Step 5.5:") < text.find("### Step 5: Diff Security Review"):
        errors.add("bookend precedes Step 5")
    if re.search(r"\b(?:spawn|delegate|delegates|dispatch)\b[^\n]*Audit - Delta", bookend):
        errors.add("bookend delegates to Audit - Delta")
    return errors


def _topology_errors() -> set[str]:
    agents = propagator.load_source_agents()
    assert agents, "source corpus loader returned no agents"
    by_name = {agent.name: agent for agent in agents}
    phase = by_name.get("03 Phase - Execute")
    assert phase is not None, "Phase Execute is absent from the source corpus"
    expected = {
        "Auditor - Code",
        "Auditor - Infra",
        "Auditor - Delta",
        "Auditor - Attribution",
        "Baseline Worktree",
    }
    errors: set[str] = set()
    if set(phase.subagents) & {"Audit - Delta"}:
        errors.add("Phase Execute delegates to Audit - Delta")
    if not expected <= set(phase.subagents):
        errors.add("Phase Execute leaf roster")
    for name in expected:
        leaf = by_name.get(name)
        if leaf is None or leaf.user_invocable:
            errors.add(f"hidden leaf topology: {name}")
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
    assert phase.count("audit-comparison") == 1


@pytest.mark.parametrize(
    ("label", "path", "anchor", "validator", "expected"),
    [
        ("skill output root", SKILL_PATH, "Every report, summary, delta, queue, and attribution update is written below\n  this root.", _skill_errors, "output root confinement"),
        ("skill cleanup", SKILL_PATH, "After the attribution stage completes", _skill_errors, "cleanup after attribution"),
        ("delta matrix", DELTA_PATH, "State the matrix back to the user", _delta_errors, "delta matrix confirmation"),
        ("phase scope choice", PHASE_EXECUTE_PATH, "The resolved audit bookend contains", _phase_errors, "scope choice appears exactly once"),
        ("phase report gate", PHASE_EXECUTE_PATH, "Require both corresponding full findings reports", _phase_errors, "full report gate"),
        ("phase remediation", PHASE_EXECUTE_PATH, "only High/Critical findings settled as caused by this phase", _phase_errors, "bounded remediation"),
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
    ("label", "replacement", "expected"),
    [
        (
            "premature audit",
            "Run the accepted bookend only after all dependency levels",
            "dependency level before bookend",
        ),
        ("early cleanup", "release only a worktree created by this run after attribution", "cleanup ordering"),
        ("regression before attribution", "Do not present a regression before attribution", "pre-attribution regression"),
        ("false fast track", "Complete pipeline `all-approved: yes`", "fast-track branch"),
        ("broad remediation", "only High/Critical findings settled as caused by this phase", "bounded remediation"),
    ],
)
def test_semantic_negation_kills_the_named_guard(
    label: str, replacement: str, expected: str,
) -> None:
    original = _read(PHASE_EXECUTE_PATH)
    assert replacement in original, f"mutation target missing: {label}"
    if label == "premature audit":
        mutated = original.replace(
            replacement,
            "Run the accepted bookend before all dependency levels",
            1,
        )
    elif label == "early cleanup":
        mutated = original.replace(replacement, "release only a worktree created by this run before attribution", 1)
    elif label == "regression before attribution":
        mutated = original.replace(replacement, "Present a regression before attribution", 1)
    elif label == "false fast track":
        mutated = original.replace(replacement, "Complete pipeline `all-approved: no`", 1)
    else:
        mutated = original.replace(replacement, "all findings settled as caused by this phase", 1)
    errors = _phase_errors(mutated)
    assert expected in errors, f"{label} did not trip {expected}: {sorted(errors)}"
    assert not _phase_errors(original)


def test_focused_module_never_reads_generated_outputs() -> None:
    assert "ports" not in str(SKILL_PATH)
    assert ".github" not in str(SKILL_PATH)
    assert "source_of_truth" in str(SKILL_PATH)
