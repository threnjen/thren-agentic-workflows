"""Structural and scenario checks for Phase - Execute review triggers."""

from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_PATH = REPO_ROOT / "source_of_truth/agents/03-phase-execute.agent.md"
VALIDATOR_PATH = REPO_ROOT / "source_of_truth/agents/03n-finding-validator.agent.md"

PER_FEATURE_AGENTS = {
    "03c Reviewer - Plan Conformance",
    "03j Reviewer - Blast Radius",
    "03k Reviewer - Test Falsification",
    "03l Reviewer - Plan Blind",
    "04h Cleanliness Auditor",
    "04e Dependency Auditor",
    "Unity Reviewer",
}
BOUNDARY_AGENTS = {
    "03e Diff Security Scan",
    "04d Consistency Auditor",
    "04f Test Health",
    "Prod Code Review",
}


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _table_rows(text: str, heading: str) -> list[tuple[str, str]]:
    start = text.index(heading) + len(heading)
    rows: list[tuple[str, str]] = []
    started = False
    for line in text[start:].splitlines():
        if line.startswith("|"):
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if len(cells) < 2 or set(cells[0]) <= {"-"}:
                continue
            if cells[0] == "Review agent":
                started = True
                continue
            if started:
                rows.append((cells[0], cells[1]))
            continue
        if started:
            break
    return rows


def _trigger_tables(text: str) -> tuple[list[tuple[str, str]], list[tuple[str, str]]]:
    return (
        _table_rows(text, "##### Per-feature review triggers"),
        _table_rows(text, "##### Boundary triggers"),
    )


def _table_coverage_errors(text: str) -> set[str]:
    per_rows, boundary_rows = _trigger_tables(text)
    per_names = [name for name, _ in per_rows]
    boundary_names = [name for name, _ in boundary_rows]
    errors: set[str] = set()

    if len(per_rows) != len(PER_FEATURE_AGENTS):
        errors.add("per-feature row count")
    if len(boundary_rows) != len(BOUNDARY_AGENTS):
        errors.add("boundary row count")
    if set(per_names) != PER_FEATURE_AGENTS:
        errors.add("per-feature roster")
    if set(boundary_names) != BOUNDARY_AGENTS:
        errors.add("boundary roster")
    for agent in PER_FEATURE_AGENTS | BOUNDARY_AGENTS:
        table_count = int(agent in per_names) + int(agent in boundary_names)
        if table_count != 1:
            errors.add(f"table ownership: {agent}")
    if any(not condition for _, condition in per_rows + boundary_rows):
        errors.add("empty trigger condition")
    return errors


def _matches_dependency(path: str) -> bool:
    return Path(path).name in {
        "package.json",
        "package-lock.json",
        "pnpm-lock.yaml",
        "yarn.lock",
        "pyproject.toml",
        "poetry.lock",
        "uv.lock",
        "requirements.txt",
        "go.mod",
        "go.sum",
        "Cargo.toml",
        "Cargo.lock",
    }


def _predicted_agents(
    text: str,
    changed_files: list[str],
    *,
    is_unity_project: bool = False,
) -> set[str]:
    predicted: set[str] = set()
    for agent, condition in _table_rows(text, "##### Per-feature review triggers"):
        if condition == "Always":
            predicted.add(agent)
        elif "package manifest" in condition and any(
            _matches_dependency(path) for path in changed_files
        ):
            predicted.add(agent)
        elif "`is-unity-project: yes`" in condition and is_unity_project and any(
            path.startswith("Assets/") and path.endswith(".cs") for path in changed_files
        ):
            predicted.add(agent)
    return predicted


def _predicted_boundary_agents(text: str, *, phase_closing: bool) -> set[str]:
    predicted: set[str] = set()
    for agent, condition in _table_rows(text, "##### Boundary triggers"):
        if "phase is closing" in condition and phase_closing:
            predicted.add(agent)
    return predicted


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


# Auditor - Refactor was cut from this pipeline. Its phase-close backstop became
# the phase-close audit pair, which keeps the property the backstop had and the
# level-closure rows never did: an absent result blocks all-approved.
PHASE_CLOSE_AUDIT_CONTRACT = (
    "phase-close-audits: executed",
    "phase-close-audits: absent",
)


def _missing_phase_close_audit_contract(text: str) -> set[str]:
    return {phrase for phrase in PHASE_CLOSE_AUDIT_CONTRACT if phrase not in text}


def test_trigger_tables_have_exact_rosters_and_conditions() -> None:
    errors = _table_coverage_errors(_read(PHASE_PATH))
    assert not errors, sorted(errors)


def test_changed_file_scenarios_resolve_the_predicted_agent_set() -> None:
    text = _read(PHASE_PATH)
    # 04h is unconditional: it fires on a docs-only diff too. It was widened
    # from a reference-graph condition and relabelled Always to match.
    always = {
        "03c Reviewer - Plan Conformance",
        "03j Reviewer - Blast Radius",
        "03k Reviewer - Test Falsification",
        "03l Reviewer - Plan Blind",
        "04h Cleanliness Auditor",
    }
    cases = (
        ("isolated", ["docs/new.md"], {}, always),
        ("imported symbol", ["src/core.py"], {}, always),
        ("lockfile", ["uv.lock"], {}, always | {"04e Dependency Auditor"}),
        ("authentication", ["src/auth.py"], {}, always),
        (
            "Unity C#",
            ["Assets/Runtime/Spawner.cs"],
            {"is_unity_project": True},
            always | {"Unity Reviewer"},
        ),
        ("non-Unity C#", ["Assets/Runtime/Spawner.cs"], {}, always),
    )
    for label, files, options, expected in cases:
        assert _predicted_agents(text, files, **options) == expected, label


def test_security_scan_has_one_entry_point() -> None:
    """Step 5 owns the only spawn of 03e; no feature stage may reintroduce one."""
    text = _read(PHASE_PATH)
    security_section = text.split("### Step 5: Phase-Close Review", 1)[1]
    security_section = security_section.split("### Step 6: Phase Final Review", 1)[0]
    assert "**03e Diff Security Scan** concurrently" in security_section
    assert "Spawn `03e` at `high`" in security_section
    # 03e cannot resolve its own scope, so Step 5 must hand it materialized inputs.
    assert "changed-files.txt" in security_section
    assert "range.diff" in security_section
    # The feature loop must not spawn it.
    feature_loop = text.split("#### Feature stage definitions", 1)[1]
    feature_loop = feature_loop.split("### Step 4: QA", 1)[0]
    assert "03e" not in feature_loop


def test_boundary_events_resolve_the_predicted_agent_set() -> None:
    text = _read(PHASE_PATH)
    assert _predicted_boundary_agents(text, phase_closing=False) == set()
    assert _predicted_boundary_agents(text, phase_closing=True) == {
        "03e Diff Security Scan",
        "04d Consistency Auditor",
        "04f Test Health",
        "Prod Code Review",
    }
    assert "Auditor - Refactor" not in text


def test_trigger_table_guard_fails_when_a_row_is_removed() -> None:
    original = _read(PHASE_PATH)
    row = "| 03j Reviewer - Blast Radius | Always |"
    assert row in original
    mutated = original.replace(row, "", 1)
    assert "per-feature roster" in _table_coverage_errors(mutated)


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


