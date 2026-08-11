"""Contract guards for Unity execution consumers."""

from __future__ import annotations

import re
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
AGENT_ROOT = REPO_ROOT / "source_of_truth/agents"
CONSUMER_PATHS = {
    "phase_execute": AGENT_ROOT / "04-phase-execute.agent.md",
    "visual_verifier": AGENT_ROOT / "04g-unity-visual-verification.agent.md",
    "unity_reviewer": AGENT_ROOT / "04h-unity-reviewer.agent.md",
}


def _section(text: str, heading: str, next_heading_level: int) -> str:
    marker = rf"^{re.escape(heading)}\s*$\n"
    next_heading = rf"(?=^{'#' * next_heading_level}\s|\Z)"
    match = re.search(marker + rf"(.*?){next_heading}", text, re.MULTILINE | re.DOTALL)
    assert match is not None, f"missing section: {heading}"
    section = match.group(1).strip()
    assert section, f"empty section: {heading}"
    return section


def _consumer_texts() -> dict[str, str]:
    assert len(CONSUMER_PATHS) == 3
    missing = [str(path) for path in CONSUMER_PATHS.values() if not path.is_file()]
    assert not missing, f"missing Unity consumers: {missing}"
    return {
        name: path.read_text(encoding="utf-8")
        for name, path in CONSUMER_PATHS.items()
    }


def _phase_execute_errors(section: str) -> set[str]:
    normalized = " ".join(section.split())
    lower = normalized.lower()
    errors: set[str] = set()

    if "`unity-development` skill's Test Execution section and Execution Ladder" not in normalized:
        errors.add("canonical test execution ladder")
    if (
        "<execution-unity-project>" not in section
        or "absolute main-checkout" not in lower
        or "results XML and Unity log" not in normalized
    ):
        errors.add("canonical execution and artifact paths")
    if "Never delegate a Unity test command to the user" not in section:
        errors.add("orchestrator-owned Unity execution")
    if re.search(r"ask (?:them|the user) to run the (?:Unity )?suite", section, re.IGNORECASE):
        errors.add("no user-run Unity handoff")
    if (
        "executed-green" not in section
        or "executed-failing" not in section
        or "not-executed" not in section
        or "do not treat it as green" not in lower
        or "all-approved: no" not in section
    ):
        errors.add("non-green evidence statuses")
    if (
        "declines the main-checkout fallback" not in lower
        or "not-executed: editor open, user unavailable" not in section
    ):
        errors.add("decline or unattended fallback")
    if (
        "direct-supervisor-attestation exception" not in section
        or "supervisor-attested (no artifact exported)" not in section
    ):
        errors.add("supervisor attestation")
    if "Retry at most once" not in section:
        errors.add("one retry")
    return errors


def _visual_verifier_errors(section: str) -> set[str]:
    normalized = " ".join(section.split())
    errors: set[str] = set()

    for token in (
        "VISUAL_VERIFICATION_UNITY",
        "dev/com.threnjen.visual-verification.local.json",
        "UnityHub",
        ".gitignore",
    ):
        if token not in section:
            errors.add("editor discovery and saved path")
    if (
        "`unity-development` skill's Test Execution section and Execution Ladder"
        not in normalized
    ):
        errors.add("canonical test execution ladder")
    if (
        "<main-repo-root>" not in section
        or "<unity-project-relative-path>" not in section
        or "<execution-unity-project>" not in section
    ):
        errors.add("root or nested project path")
    if "<execution-unity-project>/ProjectSettings/ProjectVersion.txt" not in section:
        errors.add("nested editor version path")
    if "capture inputs are committed" not in normalized:
        errors.add("committed capture inputs")

    command = next(
        (
            line
            for line in normalized.split("`")
            if "-runTests" in line and '"<resolved-unity-editor>"' in line
        ),
        "",
    )
    required_tokens = (
        '"<resolved-unity-editor>"',
        "-batchmode",
        "-runTests",
        "-testPlatform PlayMode",
        '-projectPath "<execution-unity-project>"',
        '-testResults "<absolute-main-checkout>/dev/test-results/<results.xml>"',
        '-logFile "<absolute-main-checkout>/dev/test-results/<unity.log>"',
    )
    if not command or any(token not in command for token in required_tokens):
        errors.add("PlayMode capture command")
    if "-nographics" in command or "-quit" in command:
        errors.add("graphics enabled without quit")
    if "graphics enabled" not in normalized:
        errors.add("graphics enabled without quit")
    return errors


def _phase_visual_gate_errors(section: str, full_text: str) -> set[str]:
    normalized = " ".join(section.split())
    errors: set[str] = set()

    if (
        "Visual Verification Wiring" not in full_text
        or "before returning so the A1 checkpoint commits those inputs" not in full_text
    ):
        errors.add("implementation-owned visual wiring")
    if "Never create or modify capture inputs after the wave checkpoints" not in normalized:
        errors.add("no dirty post-wave bootstrap")
    if (
        "visual-verification: not configured (capture inputs missing at implementation checkpoint)"
        not in normalized
        or "all-approved: no" not in section
    ):
        errors.add("missing-input non-green status")
    if "perform the minimal wiring yourself" in normalized:
        errors.add("no dirty post-wave bootstrap")
    return errors


def _unity_reviewer_errors(section: str) -> set[str]:
    normalized = " ".join(section.split())
    lower = normalized.lower()
    errors: set[str] = set()

    if (
        "`unity-development` skill's Test Execution section and Execution Ladder"
        not in normalized
        or "resolved editor, root-or-nested `<execution-unity-project>`" not in normalized
        or "absolute main-checkout XML and log paths" not in normalized
    ):
        errors.add("canonical test execution")
    if "Never pair `-quit` with `-runTests`" not in section:
        errors.add("test excludes quit")
    if (
        "Serialized Assets: Generate via Unity, Never Hand-Author" not in section
        or "Headless asset-database import" not in section
        or "permits `-quit` only for that import" not in section
    ):
        errors.add("canonical serialized asset import")
    if (
        "batchmode remains limited to Test Execution and Serialized Assets" not in normalized
    ):
        errors.add("no broadened batchmode")
    if "clean import does not prove" not in lower or "static Serialized Asset Integrity audit" not in section:
        errors.add("import evidence boundary")
    return errors


def _duplication_errors(texts: dict[str, str]) -> set[str]:
    errors: set[str] = set()
    copied_mechanics = (
        "git worktree add --detach",
        "git worktree prune",
        "checkout --detach",
        "<project-dir>-agent-tests/",
    )
    for name, text in texts.items():
        if any(token in text for token in copied_mechanics):
            errors.add(f"{name} duplicates worktree mechanics")
    for name in ("phase_execute", "unity_reviewer"):
        text = texts[name]
        if "VISUAL_VERIFICATION_UNITY" in text or "ProjectSettings/ProjectVersion.txt" in text:
            errors.add(f"{name} duplicates editor discovery")
    return errors


def test_required_unity_consumers_are_present() -> None:
    assert set(_consumer_texts()) == {
        "phase_execute",
        "visual_verifier",
        "unity_reviewer",
    }


def test_phase_execute_wave_gate_contract() -> None:
    text = _consumer_texts()["phase_execute"]
    section = _section(text, "### Step 2.5: Wave Test Gate", 3)
    assert not _phase_execute_errors(section), sorted(_phase_execute_errors(section))


def test_phase_execute_visual_gate_commit_contract() -> None:
    text = _consumer_texts()["phase_execute"]
    section = _section(text, "### Step 3: Visual Verification Gate (conditional)", 3)
    errors = _phase_visual_gate_errors(section, text)
    assert not errors, sorted(errors)


def test_visual_verifier_invocation_contract() -> None:
    text = _consumer_texts()["visual_verifier"]
    section = _section(text, "## Step 1 — Resolve the capture invocation", 2)
    assert not _visual_verifier_errors(section), sorted(_visual_verifier_errors(section))


def test_unity_reviewer_compilation_contract() -> None:
    text = _consumer_texts()["unity_reviewer"]
    section = _section(text, "### Phase 2: Compilation Check", 3)
    assert not _unity_reviewer_errors(section), sorted(_unity_reviewer_errors(section))


def test_consumers_do_not_duplicate_canonical_mechanics() -> None:
    texts = _consumer_texts()
    assert not _duplication_errors(texts), sorted(_duplication_errors(texts))


@pytest.mark.parametrize(
    ("needle", "replacement", "obligation"),
    [
        (
            "`unity-development` skill's Test Execution section and Execution Ladder",
            "local Unity instructions",
            "canonical test execution ladder",
        ),
        (
            "Never delegate a Unity test command to the user",
            "Ask the user to run the Unity suite",
            "orchestrator-owned Unity execution",
        ),
        (
            "do not treat it as green",
            "treat it as green",
            "non-green evidence statuses",
        ),
        (
            "direct-supervisor-attestation exception",
            "ordinary subagent report",
            "supervisor attestation",
        ),
        (
            "results XML and Unity log",
            "test output",
            "canonical execution and artifact paths",
        ),
        (
            "declines the main-checkout fallback",
            "skips the preferred command",
            "decline or unattended fallback",
        ),
    ],
)
def test_phase_execute_mutations_are_killed(
    needle: str, replacement: str, obligation: str
) -> None:
    text = _consumer_texts()["phase_execute"]
    section = _section(text, "### Step 2.5: Wave Test Gate", 3)
    assert needle in section, f"mutation target missing for {obligation}"
    assert obligation in _phase_execute_errors(section.replace(needle, replacement))


@pytest.mark.parametrize(
    ("needle", "replacement", "obligation"),
    [
        ("-batchmode", "-interactive", "PlayMode capture command"),
        ("graphics enabled", "graphics disabled", "graphics enabled without quit"),
        (
            '-projectPath "<execution-unity-project>"',
            '-projectPath "."',
            "PlayMode capture command",
        ),
        (
            '"<absolute-main-checkout>/dev/test-results/<results.xml>"',
            '"results.xml"',
            "PlayMode capture command",
        ),
        (
            "VISUAL_VERIFICATION_UNITY",
            "LOCAL_UNITY",
            "editor discovery and saved path",
        ),
        (
            "`unity-development` skill's Test Execution section and Execution Ladder",
            "local execution notes",
            "canonical test execution ladder",
        ),
        (
            '"<resolved-unity-editor>" -batchmode',
            '"<resolved-unity-editor>" -batchmode -quit',
            "graphics enabled without quit",
        ),
        (
            "capture inputs are committed",
            "capture inputs may remain dirty",
            "committed capture inputs",
        ),
        (
            "<execution-unity-project>/ProjectSettings/ProjectVersion.txt",
            "ProjectSettings/ProjectVersion.txt",
            "nested editor version path",
        ),
    ],
)
def test_visual_verifier_mutations_are_killed(
    needle: str, replacement: str, obligation: str
) -> None:
    text = _consumer_texts()["visual_verifier"]
    section = _section(text, "## Step 1 — Resolve the capture invocation", 2)
    assert needle in section, f"mutation target missing for {obligation}"
    assert obligation in _visual_verifier_errors(section.replace(needle, replacement))


@pytest.mark.parametrize(
    ("needle", "replacement", "obligation"),
    [
        (
            "Never pair `-quit` with `-runTests`",
            "Pair `-quit` with `-runTests`",
            "test excludes quit",
        ),
        (
            "Headless asset-database import",
            "generic batch import",
            "canonical serialized asset import",
        ),
        (
            "batchmode remains limited to Test Execution and Serialized Assets",
            "batchmode may be used for any operation",
            "no broadened batchmode",
        ),
        (
            "`unity-development` skill's Test Execution section and Execution Ladder",
            "local test instructions",
            "canonical test execution",
        ),
        (
            "A clean import does not prove",
            "A clean import proves",
            "import evidence boundary",
        ),
    ],
)
def test_unity_reviewer_mutations_are_killed(
    needle: str, replacement: str, obligation: str
) -> None:
    text = _consumer_texts()["unity_reviewer"]
    section = _section(text, "### Phase 2: Compilation Check", 3)
    assert needle in section, f"mutation target missing for {obligation}"
    assert obligation in _unity_reviewer_errors(section.replace(needle, replacement, 1))


def test_canonical_mechanics_duplication_mutations_are_killed() -> None:
    texts = _consumer_texts()
    worktree_mutation = dict(texts)
    worktree_mutation["phase_execute"] += "\ngit worktree add --detach"
    assert "phase_execute duplicates worktree mechanics" in _duplication_errors(
        worktree_mutation
    )

    discovery_mutation = dict(texts)
    discovery_mutation["unity_reviewer"] += "\nProjectSettings/ProjectVersion.txt"
    assert "unity_reviewer duplicates editor discovery" in _duplication_errors(
        discovery_mutation
    )


@pytest.mark.parametrize(
    ("needle", "replacement", "obligation"),
    [
        (
            "before returning so the A1 checkpoint commits those inputs",
            "after the wave checkpoints",
            "implementation-owned visual wiring",
        ),
        (
            "Never create or modify capture inputs after the wave checkpoints",
            "Create capture inputs after the wave checkpoints",
            "no dirty post-wave bootstrap",
        ),
        (
            "visual-verification: not configured (capture inputs missing at implementation checkpoint)",
            "visual-verification: Pass",
            "missing-input non-green status",
        ),
    ],
)
def test_phase_visual_gate_mutations_are_killed(
    needle: str, replacement: str, obligation: str
) -> None:
    text = _consumer_texts()["phase_execute"]
    section = _section(text, "### Step 3: Visual Verification Gate (conditional)", 3)
    assert needle in text, f"mutation target missing for {obligation}"
    mutated_text = text.replace(needle, replacement, 1)
    mutated_section = _section(
        mutated_text, "### Step 3: Visual Verification Gate (conditional)", 3
    )
    assert obligation in _phase_visual_gate_errors(mutated_section, mutated_text)
