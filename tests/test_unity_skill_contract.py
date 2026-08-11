"""Structural guards for the canonical Unity development skill contract."""

from __future__ import annotations

import re
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_PATH = REPO_ROOT / "source_of_truth/skills/unity-development/SKILL.md"
SOURCE_ROOT = REPO_ROOT / "source_of_truth"


def _normalize(text: str) -> str:
    return " ".join(text.split())


def _test_execution_section(text: str) -> str:
    match = re.search(r"^## Test Execution\s*$\n(.*?)(?=^##\s|\Z)", text, re.MULTILINE | re.DOTALL)
    assert match is not None, "Test Execution section is missing"
    section = match.group(1).strip()
    assert section, "Test Execution section is empty"
    return section


def _source_texts() -> list[tuple[Path, str]]:
    text_suffixes = {".json", ".md", ".py", ".toml", ".yaml", ".yml"}
    files = sorted(
        path
        for path in SOURCE_ROOT.rglob("*")
        if path.is_file() and path.suffix in text_suffixes
    )
    assert files, "source_of_truth sweep is empty"
    return [(path, path.read_text(encoding="utf-8")) for path in files]


def _contract_errors(section: str) -> set[str]:
    normalized = _normalize(section)
    lower = normalized.lower()
    errors: set[str] = set()

    if "`-batchmode` is mandatory" not in normalized:
        errors.add("mandatory batchmode")
    if not re.search(r"\|\s*EditMode\s*\|[^|]*`-batchmode -nographics`[^|]*\|", section):
        errors.add("EditMode flags")
    playmode_row = re.search(
        r"\|\s*PlayMode and visual capture\s*\|([^|]*)\|", section
    )
    if (
        playmode_row is None
        or "`-batchmode`" not in playmode_row.group(1)
        or "graphics enabled" not in playmode_row.group(1)
        or "exclude `-nographics`" not in playmode_row.group(1)
    ):
        errors.add("PlayMode graphics")
    if "never pair `-quit` with `-runtests`" not in lower:
        errors.add("no quit with runTests")
    if (
        "semicolon-separated list of full test names or a regex" not in normalized
        or "negation supported" not in normalized
        or "Gate runs (wave boundary, phase end) are unfiltered" not in normalized
    ):
        errors.add("testFilter semantics")
    if "source_of_truth/agents/04g-unity-visual-verification.agent.md" not in section:
        errors.add("editor discovery pointer")
    if "Never assume a bare `Unity` executable is on `PATH`" not in section:
        errors.add("no bare Unity")
    if (
        "absolute path under the main checkout's `dev/test-results/`" not in section
        or "execution target only" not in section
        or "Never read results from the shadow worktree" not in section
    ):
        errors.add("main-checkout results")
    if (
        "Commit before testing" not in section
        or "normal per-feature commit usually satisfies" not in section
    ):
        errors.add("commit precondition")

    ladder_markers = [
        "1. **Persistent shadow worktree",
        "2. **Licensing or lock fallback",
        "3. **Decline or unattended fallback",
    ]
    positions = [section.find(marker) for marker in ladder_markers]
    if any(position < 0 for position in positions) or positions != sorted(positions):
        errors.add("ordered ladder")
    for token, name in [
        ("git worktree prune", "prune registrations"),
        ("git worktree add --detach", "detached creation"),
        ("checkout --detach", "detached refresh"),
        ("<project-dir>-agent-tests/", "fixed sibling path"),
        ("Its gitignored `Library/` remains in place", "Library retention"),
        ("approximate disk cost", "cost announcement"),
        ("multi-minute first import", "cold import announcement"),
        ("persists indefinitely", "indefinite persistence"),
        ("Per-run worktree creation is an anti-pattern", "per-run anti-pattern"),
        ("worktree remove", "manual teardown"),
    ]:
        if token not in section:
            errors.add(name)
    if (
        "ask the user to close the Editor" not in section
        or "the agent runs the headless command" not in section
        or "Never delegate the test run to the user" not in section
    ):
        errors.add("agent-run fallback")
    if "Never launch a GUI and never refuse silently" not in section:
        errors.add("no GUI or silent refusal")
    if (
        "A decline reports `not-executed`" not in section
        or "not-executed: editor open, user unavailable" not in section
    ):
        errors.add("terminal statuses")
    if (
        "Root `<test-run total= passed= failed=>`" not in section
        or "`<test-case result=\"Failed\">`" not in section
        or "zero tests discovered is `not-executed`" not in section
    ):
        errors.add("results XML")
    return errors


def test_live_test_execution_contract() -> None:
    section = _test_execution_section(SKILL_PATH.read_text(encoding="utf-8"))
    assert not _contract_errors(section), sorted(_contract_errors(section))


def test_batchmode_optional_claim_is_absent_from_source() -> None:
    offenders = [
        str(path.relative_to(REPO_ROOT))
        for path, text in _source_texts()
        if re.search(r"`-batchmode`\s+is\s+optional", _normalize(text), re.IGNORECASE)
    ]
    assert not offenders, f"optional batchmode claim remains in: {offenders}"


def test_commands_are_scoped_and_safe() -> None:
    section = _test_execution_section(SKILL_PATH.read_text(encoding="utf-8"))
    commands = re.findall(r"```bash\n(.*?)\n```", section, re.DOTALL)
    assert commands, "Test Execution contains no command examples"
    command_lines = [line.strip() for block in commands for line in block.splitlines() if line.strip()]
    test_commands = [line for line in command_lines if "-runTests" in line]
    assert len(test_commands) == 2, "expected EditMode and PlayMode command examples"
    assert all(not line.startswith("Unity ") for line in test_commands), "bare Unity command found"
    assert all("-batchmode" in line and "-quit" not in line for line in test_commands)
    editmode = next(line for line in test_commands if "-testPlatform EditMode" in line)
    playmode = next(line for line in test_commands if "-testPlatform PlayMode" in line)
    assert "-nographics" in editmode
    assert "-nographics" not in playmode
    assert all("<absolute-main-checkout>/dev/test-results/" in line for line in test_commands)


@pytest.mark.parametrize(
    ("needle", "replacement", "obligation"),
    [
        ("`-batchmode` is mandatory", "`-batchmode` is optional", "mandatory batchmode"),
        ("`-batchmode -nographics`", "`-batchmode`", "EditMode flags"),
        ("exclude `-nographics`", "include `-nographics`", "PlayMode graphics"),
        ("Never pair `-quit` with `-runTests`", "Pair `-quit` with `-runTests`", "no quit with runTests"),
        ("source_of_truth/agents/04g-unity-visual-verification.agent.md", "another-discovery.md", "editor discovery pointer"),
        ("Never assume a bare `Unity` executable is on `PATH`", "Assume `Unity` is on `PATH`", "no bare Unity"),
        ("absolute path under the main checkout's `dev/test-results/`", "relative results path", "main-checkout results"),
        ("Commit before testing", "Testing a dirty checkout is allowed", "commit precondition"),
        ("git worktree prune", "git worktree list", "prune registrations"),
        ("git worktree add --detach", "git worktree add", "detached creation"),
        ("checkout --detach", "checkout", "detached refresh"),
        (
            "Its gitignored `Library/` remains in place",
            "Its import cache is deleted",
            "Library retention",
        ),
        ("persists indefinitely", "is deleted after every run", "indefinite persistence"),
        ("Per-run worktree creation is an anti-pattern", "Create a worktree per run", "per-run anti-pattern"),
        ("worktree remove", "worktree list", "manual teardown"),
        ("Never delegate the test run to the user", "Delegate the test run to the user", "agent-run fallback"),
        ("Never launch a GUI and never refuse silently", "Launch a GUI or refuse silently", "no GUI or silent refusal"),
        ("not-executed: editor open, user unavailable", "wait forever", "terminal statuses"),
        ("Root `<test-run total= passed= failed=>`", "Exit code zero", "results XML"),
    ],
)
def test_contract_mutations_are_killed(
    needle: str, replacement: str, obligation: str
) -> None:
    section = _test_execution_section(SKILL_PATH.read_text(encoding="utf-8"))
    assert needle in section, f"mutation target missing for {obligation}"
    mutated = section.replace(needle, replacement, 1)
    assert obligation in _contract_errors(mutated)
