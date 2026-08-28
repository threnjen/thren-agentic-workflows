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
    """Step 3 owns the only spawn of 03e; no feature stage may reintroduce one."""
    text = _read(PHASE_PATH)
    security_section = text.split("### Step 3: Phase-Close Review", 1)[1]
    security_section = security_section.split("### Step 5: Phase Final Review", 1)[0]
    assert "**03e Diff Security Scan** concurrently" in security_section
    assert "Spawn `03e` at `high`" in security_section
    # 03e cannot resolve its own scope, so Step 3 must hand it materialized inputs.
    assert "changed-files.txt" in security_section
    assert "range.diff" in security_section
    # The feature loop must not spawn it.
    feature_loop = text.split("#### Feature stage definitions", 1)[1]
    feature_loop = feature_loop.split("### Step 3: Phase-Close Review", 1)[0]
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


def test_every_body_spawn_resolves_to_an_agent_on_disk() -> None:
    """A spawn names an agent by its `name:`, never by its filename.

    `03h-unity-reviewer.agent.md` declares `name: "Unity Reviewer"`, so a body
    that writes `Spawn **03h Unity Reviewer**` names nothing. The frontmatter
    roster is checked elsewhere against the same set; this checks the prose that
    actually issues the spawn, which no other guard reads.
    """
    import re
    import sys

    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    import propagate_master_assets as mod

    known = {agent.name for agent in mod.load_source_agents()}
    body = _read(PHASE_PATH).split("---", 2)[2]
    spawned = set(re.findall(r"[Ss]pawn (?:the )?\*\*(.+?)\*\*", body))

    assert spawned, "no spawn directives found; the pattern stopped matching"
    unresolved = sorted(name for name in spawned if name not in known)
    assert not unresolved, (
        f"Phase - Execute spawns agents that match no `name:` on disk: {unresolved}"
    )


def test_phase_starts_green_or_does_not_start() -> None:
    """The preflight must stop the run, not record a status and continue.

    Every later gate in the file reasons that a failing test can only be a defect
    the current feature introduced. That inference is sound only because the phase
    refused to begin red. A preflight that degrades to a warning silently restores
    the baseline-exemption model the phase deleted.
    """
    body = _read(PHASE_PATH)
    preflight = body.split("#### Green-suite preflight", 1)
    assert len(preflight) == 2, "Step 1 lost its green-suite preflight"
    section = preflight[1].split("#### Verify the inputs", 1)[0]

    assert "stop the run immediately" in section, "preflight does not stop on a failing test"
    assert "Do not spawn a single agent." in section, (
        "preflight may not decompose or delegate before the suite is green"
    )
    assert "cannot run, stop the same way" in section, (
        "an unrunnable suite must stop the preflight, not pass it"
    )
    assert "unfiltered" in section, "preflight must run the full suite, not affected suites"


def test_no_test_may_be_excused_during_the_phase() -> None:
    """A single exempt test reopens the escape hatch the preflight closed."""
    body = " ".join(_read(PHASE_PATH).split())
    assert "There is no exempt test" in body, "the no-exemption rule left the feature gate"
    assert "no baseline exemption list" in body, "the no-exemption rule left the preflight"
    assert "named in the baseline is exempt" not in body, (
        "the baseline exemption clause is back"
    )


def test_orchestrator_opens_no_repair_round_of_its_own() -> None:
    """Two agents own reaching green; a third round is the orchestrator undoing that."""
    body = _read(PHASE_PATH)
    gate = body.split("##### D. Integration test gate", 1)[1].split("##### E.", 1)[0]
    assert "do not remediate here" in gate.lower(), "the gate reopened a repair round"
    assert "Re-spawn the **Feature - Implementer**" not in gate, (
        "the gate spawns a second repair agent for the same feature"
    )
    assert "always a production blocker" in gate, (
        "a gate left failing must block, never be recorded complete"
    )
