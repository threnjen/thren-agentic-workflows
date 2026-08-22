"""Structural and scenario checks for Phase - Execute review triggers."""

from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_PATH = REPO_ROOT / "source_of_truth/agents/03-phase-execute.agent.md"
PLAN_SKILL_PATH = REPO_ROOT / "source_of_truth/skills/feature-plan-set/SKILL.md"
LOOP_SKILL_PATH = REPO_ROOT / "source_of_truth/skills/implementation-pipeline-loop/SKILL.md"
RECORD_SKILL_PATH = REPO_ROOT / "source_of_truth/skills/implementation-record/SKILL.md"

PER_FEATURE_AGENTS = {
    "Feature - Review and Fix",
    "03j Reviewer - Blast Radius",
    "03k Reviewer - Test Falsification",
    "03l Reviewer - Plan Blind",
    "04h Cleanliness Auditor",
    "03e Diff Security Scan",
    "04e Dependency Auditor",
    "Unity Reviewer",
    "Visual Verifier",
}
BOUNDARY_AGENTS = {
    "Auditor - Refactor",
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

    if len(per_rows) != 9:
        errors.add("per-feature row count")
    if len(boundary_rows) != 5:
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


def _is_source_or_test(path: str) -> bool:
    return path.startswith("tests/") or Path(path).suffix in {
        ".py",
        ".cs",
        ".js",
        ".ts",
        ".tsx",
        ".go",
        ".rs",
    }


def _matches_security(path: str) -> bool:
    return any(token in path.lower() for token in ("auth", "input", "network", "secret"))


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
    imports_reference: bool = False,
    is_unity_project: bool = False,
    visual_acceptance: bool = False,
) -> set[str]:
    predicted: set[str] = set()
    for agent, condition in _table_rows(text, "##### Per-feature review triggers"):
        if condition == "Always":
            predicted.add(agent)
        elif "another file imports or references" in condition and imports_reference:
            predicted.add(agent)
        elif "source or test file" in condition and any(
            _is_source_or_test(path) for path in changed_files
        ):
            predicted.add(agent)
        elif "authentication" in condition and any(
            _matches_security(path) for path in changed_files
        ):
            predicted.add(agent)
        elif "package manifest" in condition and any(
            _matches_dependency(path) for path in changed_files
        ):
            predicted.add(agent)
        elif "`is-unity-project: yes`" in condition and is_unity_project and any(
            path.startswith("Assets/") and path.endswith(".cs") for path in changed_files
        ):
            predicted.add(agent)
        elif "visual_acceptance: yes" in condition and visual_acceptance:
            predicted.add(agent)
    return predicted


def _predicted_boundary_agents(
    text: str, *, dependency_level_closed: bool, phase_closing: bool
) -> set[str]:
    predicted: set[str] = set()
    for agent, condition in _table_rows(text, "##### Boundary triggers"):
        if "dependency level closed" in condition and dependency_level_closed:
            predicted.add(agent)
        if "phase is closing" in condition and phase_closing:
            predicted.add(agent)
    return predicted


FIX_LOOP_CONTRACT = (
    "Run the four committee reviewers concurrently at `medium`",
    "Only `Blocker` and `High` findings open a fix round",
    "Record `Medium` and `Low` findings as carry-forward evidence",
    "Run at most two fix rounds",
    "rewrite the feature plan once",
    "mark it and its dependents blocked",
)


def _missing_fix_loop_contract(text: str) -> set[str]:
    return {phrase for phrase in FIX_LOOP_CONTRACT if phrase not in text}


BACKSTOP_CONTRACT = (
    "architecture-backstop: executed",
    "architecture-backstop: absent",
    "committee-miss-record: absent",
)


def _missing_backstop_contract(text: str) -> set[str]:
    return {phrase for phrase in BACKSTOP_CONTRACT if phrase not in text}


def _visual_flag_errors(text: str) -> set[str]:
    errors: set[str] = set()
    if "`visual_acceptance: yes | no`" not in text:
        errors.add("visual flag field")
    if "A plan without the flag fails validation" not in text:
        errors.add("missing flag rejection")
    return errors


def test_trigger_tables_have_exact_rosters_and_conditions() -> None:
    errors = _table_coverage_errors(_read(PHASE_PATH))
    assert not errors, sorted(errors)


def test_changed_file_scenarios_resolve_the_predicted_agent_set() -> None:
    text = _read(PHASE_PATH)
    always = {
        "Feature - Review and Fix",
        "03k Reviewer - Test Falsification",
        "03l Reviewer - Plan Blind",
    }
    cases = (
        ("isolated", ["docs/new.md"], {}, always),
        (
            "imported symbol",
            ["src/core.py"],
            {"imports_reference": True},
            always | {"03j Reviewer - Blast Radius", "04h Cleanliness Auditor"},
        ),
        ("lockfile", ["uv.lock"], {}, always | {"04e Dependency Auditor"}),
        (
            "authentication",
            ["src/auth.py"],
            {},
            always | {"04h Cleanliness Auditor", "03e Diff Security Scan"},
        ),
        (
            "Unity C#",
            ["Assets/Runtime/Spawner.cs"],
            {"is_unity_project": True},
            always | {"04h Cleanliness Auditor", "Unity Reviewer"},
        ),
        (
            "non-Unity C#",
            ["Assets/Runtime/Spawner.cs"],
            {},
            always | {"04h Cleanliness Auditor"},
        ),
    )
    for label, files, options, expected in cases:
        assert _predicted_agents(text, files, **options) == expected, label


def test_visual_verifier_uses_the_required_plan_flag() -> None:
    text = _read(PHASE_PATH)
    without_flag = _predicted_agents(text, ["src/view.py"])
    with_flag = _predicted_agents(text, ["src/view.py"], visual_acceptance=True)
    assert "Visual Verifier" not in without_flag
    assert "Visual Verifier" in with_flag


def test_visual_and_security_rows_have_one_entry_point() -> None:
    text = _read(PHASE_PATH)
    visual_section = text.split("### Step 3: Visual Verification Gate (conditional)", 1)[1]
    visual_section = visual_section.split("### Step 4: QA", 1)[0]
    assert "per-feature trigger table is the sole entry condition" in visual_section
    assert "Run it only when ALL" not in visual_section

    security_section = text.split("### Step 5: Diff Security Review", 1)[1]
    security_section = security_section.split("### Step 5.5: Audit Bookend", 1)[0]
    assert "Collect the reports from every feature" in security_section
    assert "spawn the **03e Diff Security Scan**" not in security_section


def test_boundary_events_resolve_the_predicted_agent_set() -> None:
    text = _read(PHASE_PATH)
    assert _predicted_boundary_agents(
        text, dependency_level_closed=True, phase_closing=False
    ) == {"Auditor - Refactor", "04d Consistency Auditor", "04f Test Health"}
    assert _predicted_boundary_agents(
        text, dependency_level_closed=False, phase_closing=True
    ) == {"Auditor - Refactor", "Prod Code Review"}


def test_trigger_table_guard_fails_when_a_row_is_removed() -> None:
    original = _read(PHASE_PATH)
    row = "| 03j Reviewer - Blast Radius | The diff changes something another file imports or references |"
    assert row in original
    mutated = original.replace(row, "", 1)
    assert "per-feature roster" in _table_coverage_errors(mutated)


def test_visual_plan_flag_guard_is_load_bearing() -> None:
    original = _read(PLAN_SKILL_PATH)
    required = "`visual_acceptance: yes | no`"
    assert not _visual_flag_errors(original)
    mutated = original.replace(required, "", 1)
    assert "visual flag field" in _visual_flag_errors(mutated)


def test_fix_loop_and_record_contracts_are_present_and_load_bearing() -> None:
    loop = _read(LOOP_SKILL_PATH)
    assert not _missing_fix_loop_contract(loop)
    for phrase in FIX_LOOP_CONTRACT:
        mutated = loop.replace(phrase, "", 1)
        assert phrase in _missing_fix_loop_contract(mutated)

    record = _read(RECORD_SKILL_PATH)
    for field in (
        "Resolved review agents",
        "reviewer:",
        "Fix rounds",
        "Carry-forward findings",
        "Committee miss record",
    ):
        assert field in record


def test_phase_close_backstop_and_committee_miss_are_load_bearing() -> None:
    text = _read(PHASE_PATH)
    assert not _missing_backstop_contract(text)
    for phrase in BACKSTOP_CONTRACT:
        assert phrase in text
        assert phrase in _missing_backstop_contract(text.replace(phrase, "", 1))
