"""Structural checks for Phase - Execute's security entry point and 03n's frozen contracts."""

from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_PATH = REPO_ROOT / "source_of_truth/agents/03-phase-execute.agent.md"
VALIDATOR_PATH = REPO_ROOT / "source_of_truth/agents/03n-finding-validator.agent.md"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


POST_REBUILD_MATRIX_CONTRACT = (
    "cell_id",
    "supported_path",
    "invariant",
    "status",
    "severity",
    "lineage",
    "evidence",
    "Pass",
    "Block",
    "Escalate",
)

EVIDENCE_CLASSIFICATION_CONTRACT = (
    "The evidence-only rule applies on every validation",
    "historical RED/GREEN artifact",
    "verification-blocker",
    "Medium",
)


def test_security_scan_has_one_entry_point() -> None:
    """Step 4 owns the only spawn of 03e; no feature stage may reintroduce one."""
    text = _read(PHASE_PATH)
    security_section = text.split("### Step 4: Phase-Close Audits", 1)[1]
    security_section = security_section.split("### Step 5: Phase Final Review", 1)[0]
    assert "**03e Diff Security Scan** concurrently" in security_section
    assert "Spawn `03e` at `high`" in security_section
    # 03e cannot resolve its own scope, so Step 4 must hand it materialized inputs.
    assert "changed-files.txt" in security_section
    assert "range.diff" in security_section
    # The feature loop must not spawn it.
    feature_loop = text.split("#### Feature stage definitions", 1)[1]
    feature_loop = feature_loop.split("### Step 3: QA", 1)[0]
    assert "03e" not in feature_loop


def _convergence_section(text: str) -> str:
    """The 03n block that owns the frozen matrix, isolated from the rest of the agent."""
    start = text.index("## Post-Rebuild Convergence")
    rest = text.find("\n## ", start + 1)
    return text[start:] if rest == -1 else text[start:rest]


def test_frozen_matrix_contract_lives_in_the_validator() -> None:
    # 03n is the sole authority for convergence classes, so the matrix cell
    # fields and the three verdicts must be stated in its own section rather
    # than anywhere else in the agent.
    section = _convergence_section(_read(VALIDATOR_PATH))
    assert not {
        phrase for phrase in POST_REBUILD_MATRIX_CONTRACT if phrase not in section
    }


def test_evidence_classification_contract_lives_in_the_validator() -> None:
    text = _read(VALIDATOR_PATH)
    assert not {
        phrase for phrase in EVIDENCE_CLASSIFICATION_CONTRACT if phrase not in text
    }


def test_frozen_matrix_guard_fails_when_a_cell_field_is_dropped() -> None:
    original = _read(VALIDATOR_PATH)
    assert "`lineage`" in _convergence_section(original)
    mutated = _convergence_section(original.replace("`lineage`, ", "", 1))
    assert {phrase for phrase in POST_REBUILD_MATRIX_CONTRACT if phrase not in mutated}
