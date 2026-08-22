"""Contract guards for the execution manifest schema."""

from __future__ import annotations

import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_SKILL_PATH = REPO_ROOT / "source_of_truth/skills/feature-plan-set/SKILL.md"
MANIFEST_FIELDS = (
    "status",
    "dependency_level",
    "depends_on",
    "expected_read_set",
    "expected_write_set",
    "plan_revision",
    "last_validation_commit",
    "stale_reason",
    "resolved_model_status",
)
SCHEDULING_TOKEN = "wa" + "ve"
SCAN_ROOTS = (
    REPO_ROOT / "source_of_truth/skills",
    REPO_ROOT / "source_of_truth/instructions",
    REPO_ROOT / "tests",
)

# The scan excludes source_of_truth/agents/03-feature-decomposer.agent.md and
# source_of_truth/agents/04-phase-execute.agent.md because Feature 04 owns their rewrite.
# These test phrases target the same untouched agent and are exempted narrowly, not by file.
FEATURE_04_OWNED_TEST_PHRASES = {
    REPO_ROOT / "tests/test_phase_execute_audit_bookend.py": (
        SCHEDULING_TOKEN + " before bookend",
        "Run the accepted bookend only after all " + SCHEDULING_TOKEN + "s",
        "Run the accepted bookend before all " + SCHEDULING_TOKEN + "s",
    ),
    REPO_ROOT / "tests/test_unity_consumer_contract.py": (
        "Never create or modify capture inputs after the "
        + SCHEDULING_TOKEN
        + " checkpoints",
        "no dirty post-" + SCHEDULING_TOKEN + " bootstrap",
        "### Step 2.5: " + SCHEDULING_TOKEN.capitalize() + " Test Gate",
        "after the " + SCHEDULING_TOKEN + " checkpoints",
        "Create capture inputs after the " + SCHEDULING_TOKEN + " checkpoints",
    ),
}
SCHEDULING_TERM_PATTERN = re.compile(
    rf"\b{re.escape(SCHEDULING_TOKEN)}s?\b", re.IGNORECASE
)


def _read_manifest_skill() -> str:
    return MANIFEST_SKILL_PATH.read_text(encoding="utf-8")


def _missing_schema_fields(text: str) -> list[str]:
    return [field for field in MANIFEST_FIELDS if f"`{field}`" not in text]


def _in_scope_paths() -> list[Path]:
    paths = {
        path
        for root in SCAN_ROOTS
        for path in root.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    }
    paths.update(REPO_ROOT.glob("*.md"))
    return sorted(paths)


def _read_scan_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None


def _scheduling_term_errors(overrides: dict[Path, str] | None = None) -> list[str]:
    overrides = overrides or {}
    errors: list[str] = []
    for path in _in_scope_paths():
        text = overrides[path] if path in overrides else _read_scan_text(path)
        if text is None:
            continue
        for line_number, line in enumerate(text.splitlines(), start=1):
            scan_line = line
            for phrase in FEATURE_04_OWNED_TEST_PHRASES.get(path, ()):
                scan_line = scan_line.replace(phrase, "")
            if SCHEDULING_TERM_PATTERN.search(scan_line):
                relative_path = path.relative_to(REPO_ROOT)
                errors.append(f"{relative_path}:{line_number}")
    return errors


def test_manifest_schema_contains_all_per_feature_fields() -> None:
    missing = _missing_schema_fields(_read_manifest_skill())
    assert not missing, f"manifest schema missing fields: {', '.join(missing)}"


def test_manifest_schema_guard_names_a_removed_field() -> None:
    field = MANIFEST_FIELDS[0]
    text = _read_manifest_skill()
    mutated = text.replace(f"`{field}`", "", 1)
    assert _missing_schema_fields(mutated) == [field]


def test_manifest_is_a_living_schedule_with_execution_rewrite_events() -> None:
    text = _read_manifest_skill()
    required_phrases = (
        "living execution schedule",
        "rewritten during execution",
        "not frozen after decomposition",
        "selects a feature",
        "records an implementation result",
        "closes a dependency level",
        "completes revalidation of affected future features",
    )
    missing = [phrase for phrase in required_phrases if phrase not in text]
    assert not missing, f"manifest execution contract missing phrases: {', '.join(missing)}"


def test_quality_checklist_requires_a_dependency_level_schedule() -> None:
    text = _read_manifest_skill()
    checklist = text.split("## Quality Checklist", 1)[1]
    assert "includes the ordered feature list, dependency-level schedule" in checklist


def test_in_scope_files_have_no_retired_scheduling_term() -> None:
    errors = _scheduling_term_errors()
    assert not errors, f"retired scheduling term remains: {', '.join(errors)}"


def test_scheduling_term_scan_detects_an_in_scope_mutation() -> None:
    target = REPO_ROOT / "USAGE.md"
    original = target.read_text(encoding="utf-8")
    mutated = original + f"\nA {SCHEDULING_TOKEN} schedule is invalid.\n"
    errors = _scheduling_term_errors({target: mutated})
    assert any(error.startswith("USAGE.md:") for error in errors)


def test_scheduling_term_scan_keeps_feature_04_exemptions_narrow() -> None:
    target = REPO_ROOT / "tests/test_phase_execute_audit_bookend.py"
    original = target.read_text(encoding="utf-8")
    mutated = original + f"\nA {SCHEDULING_TOKEN} schedule is invalid.\n"
    errors = _scheduling_term_errors({target: mutated})
    assert any(error.startswith("tests/test_phase_execute_audit_bookend.py:") for error in errors)
