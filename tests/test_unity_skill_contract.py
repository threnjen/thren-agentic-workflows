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


def _serialized_assets_section(text: str) -> str:
    match = re.search(
        r"^## Serialized Assets: Generate via Unity, Never Hand-Author\s*$\n(.*?)(?=^##\s|\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    assert match is not None, "Serialized Assets section is missing"
    section = match.group(1).strip()
    assert section, "Serialized Assets section is empty"
    return section


def _assembly_reference_section(text: str) -> str:
    match = re.search(
        r"^### 2\. Assembly reference graph\s*$\n(.*?)(?=^###\s|\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    assert match is not None, "Assembly reference graph section is missing"
    return match.group(1).strip()


def _refactor_test_preservation_section(text: str) -> str:
    match = re.search(
        r"^## Refactor / Rewire Test Preservation Rules\s*$\n(.*?)(?=^##\s|\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    assert match is not None, "Refactor / Rewire Test Preservation Rules section is missing"
    return match.group(1).strip()


def _source_texts() -> list[tuple[Path, str]]:
    text_suffixes = {".json", ".md", ".py", ".toml", ".yaml", ".yml"}
    files = sorted(
        path
        for path in SOURCE_ROOT.rglob("*")
        if path.is_file() and path.suffix in text_suffixes
    )
    assert files, "source_of_truth sweep is empty"
    return [(path, path.read_text(encoding="utf-8")) for path in files]


def _meta_gui_requirement_offenders(
    source_texts: list[tuple[Path, str]],
) -> list[Path]:
    offenders: list[Path] = []
    for path, text in source_texts:
        for sentence in re.split(r"(?<=[.!?])\s+", _normalize(text)):
            for clause in re.split(r"[;:—]|\s+-\s+", sentence):
                lower = clause.lower()
                if ".meta" not in sentence.lower():
                    continue
                if not re.search(r"\b(?:human|gui)\b", lower):
                    continue
                if not re.search(r"\b(?:must|need(?:s|ed)?|require(?:s|d)?)\b", lower):
                    continue
                if not re.search(r"\b(?:open|launch|run|use)\w*\b", lower):
                    continue
                scoped_negation = any(
                    re.search(pattern, lower)
                    for pattern in (
                        r"\b(?:no|without)\s+(?:a\s+)?(?:human|gui)",
                        r"\bnever\s+(?:requires?|needs?)",
                        r"\b(?:human|gui)\b.*\b(?:is\s+)?not\s+required",
                        r"\b(?:must|needs?|requires?)\s+not\b",
                    )
                )
                if scoped_negation:
                    continue
                offenders.append(path)
                break
            if offenders and offenders[-1] == path:
                break
    return offenders


def _asset_contract_errors(section: str) -> set[str]:
    normalized = _normalize(section)
    errors: set[str] = set()
    import_command = (
        '"<resolved-unity-editor>" -batchmode -quit '
        '-projectPath "<execution-unity-project>" -logFile -'
    )

    if import_command not in section:
        errors.add("plain import command")
    if "-runTests" in next(
        (line for line in section.splitlines() if import_command in line), ""
    ):
        errors.add("import excludes runTests")
    if "asks Unity's asset database to import and generate missing `.meta`/GUID files" not in normalized:
        errors.add("meta and GUID generation")
    if (
        "treat regeneration as unverified until a controlled missing-`.meta` run succeeds"
        not in normalized
    ):
        errors.add("conditional empirical claim")
    if "editor and root-or-nested Unity project path resolved by Test Execution" not in normalized:
        errors.add("canonical editor and project path")
    if (
        "`<execution-unity-project>` is `<main-repo-root>/<unity-project-relative-path>`"
        not in normalized
    ):
        errors.add("main-checkout project path")
    if "without a human-opened or GUI-opened Editor" not in normalized:
        errors.add("no GUI requirement")
    if (
        "Unity Editor's serializer" not in section
        or "sole authority" not in section
        or "do not hand-author serialized Unity assets" not in section
        or "raw YAML" not in section
    ):
        errors.add("serializer authority")
    if "`-batchmode -executeMethod <Type>.<Method> -quit`" not in section:
        errors.add("asset construction command")
    return errors


def _path_contract_errors(skill_text: str, combined_source: str) -> set[str]:
    errors: set[str] = set()
    if "Assets/Tests/EditMode" in combined_source:
        errors.add("invalid EditMode path")
    if "Assets/Tests/Editor" not in _assembly_reference_section(skill_text):
        errors.add("assembly graph Editor path")
    refactor_section = _refactor_test_preservation_section(skill_text)
    if "Assets/Tests/Editor" not in refactor_section:
        errors.add("refactor Editor path")
    if "Assets/Tests/PlayMode" not in refactor_section:
        errors.add("refactor PlayMode path")
    return errors


def _contract_errors(section: str) -> set[str]:
    normalized = _normalize(section)
    lower = normalized.lower()
    errors: set[str] = set()

    if "`-batchmode` is mandatory" not in normalized:
        errors.add("mandatory batchmode")
    if not re.search(r"\|\s*EditMode\s*\|[^|]*`-batchmode -nographics`[^|]*\|", section):
        errors.add("EditMode flags")
    playmode_row = re.search(
        r"\|\s*PlayMode\s*\|([^|]*)\|", section
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
        or "Gate runs (feature integration gate, phase end) are unfiltered" not in normalized
    ):
        errors.add("testFilter semantics")
    if (
        "VISUAL_VERIFICATION_UNITY" not in section
        or "dev/com.threnjen.visual-verification.local.json" not in section
        or "ProjectSettings/ProjectVersion.txt" not in section
        or "UnityHub" not in section
    ):
        errors.add("owned editor discovery")
    if "This skill is the single canonical implementation of editor discovery" not in section:
        errors.add("single canonical discovery")
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
    if (
        "<main-repo-root>" not in section
        or "<unity-project-relative-path>" not in section
        or "<execution-unity-project>" not in section
    ):
        errors.add("nested project path")
    if (
        "no tracked changes or untracked files" not in section
        or "no ignored content outside" not in section
        or "stop and report `not-executed`" not in section
    ):
        errors.add("clean execution state")
    if "-logFile" not in section or "<absolute-main-checkout>/dev/test-results/<unity.log>" not in section:
        errors.add("deterministic Unity log")

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
    assert all('-projectPath "<execution-unity-project>"' in line for line in test_commands)
    assert all('-logFile "<absolute-main-checkout>/dev/test-results/<unity.log>"' in line for line in test_commands)


def test_live_serialized_asset_contract() -> None:
    section = _serialized_assets_section(SKILL_PATH.read_text(encoding="utf-8"))
    assert not _asset_contract_errors(section), sorted(_asset_contract_errors(section))


def test_meta_generation_has_no_human_or_gui_requirement() -> None:
    offenders = _meta_gui_requirement_offenders(_source_texts())
    assert not offenders, [str(path.relative_to(REPO_ROOT)) for path in offenders]


def test_unity_test_paths_match_the_verified_convention() -> None:
    skill_text = SKILL_PATH.read_text(encoding="utf-8")
    source_texts = _source_texts()
    combined = "\n".join(text for _, text in source_texts)
    errors = _path_contract_errors(skill_text, combined)
    assert not errors, sorted(errors)


@pytest.mark.parametrize(
    ("needle", "replacement", "obligation"),
    [
        (
            '"<resolved-unity-editor>" -batchmode -quit -projectPath "<execution-unity-project>" -logFile -',
            '"<resolved-unity-editor>" -batchmode -projectPath "<execution-unity-project>"',
            "plain import command",
        ),
        (
            '"<resolved-unity-editor>" -batchmode -quit -projectPath "<execution-unity-project>" -logFile -',
            '"<resolved-unity-editor>" -batchmode -quit -projectPath "<execution-unity-project>" -logFile - -runTests',
            "import excludes runTests",
        ),
        (
            "asks Unity's asset database to import and generate missing `.meta`/GUID files",
            "asset refresh",
            "meta and GUID generation",
        ),
        (
            "treat regeneration as unverified until a controlled missing-`.meta` run succeeds",
            "regeneration is always proven",
            "conditional empirical claim",
        ),
        (
            "editor and root-or-nested Unity project path resolved by Test Execution",
            "editor and project path supplied by the caller",
            "canonical editor and project path",
        ),
        (
            "`<execution-unity-project>` is `<main-repo-root>/<unity-project-relative-path>`",
            "`<execution-unity-project>` is `<main-repo-root>`",
            "main-checkout project path",
        ),
        (
            "without a human-opened or GUI-opened Editor",
            "after a human opens the GUI Editor",
            "no GUI requirement",
        ),
        ("sole authority", "one possible authority", "serializer authority"),
        (
            "`-batchmode -executeMethod <Type>.<Method> -quit`",
            "`-executeMethod <Type>.<Method>`",
            "asset construction command",
        ),
    ],
)
def test_serialized_asset_contract_mutations_are_killed(
    needle: str, replacement: str, obligation: str
) -> None:
    section = _serialized_assets_section(SKILL_PATH.read_text(encoding="utf-8"))
    assert needle in section, f"mutation target missing for {obligation}"
    mutated = section.replace(needle, replacement)
    assert obligation in _asset_contract_errors(mutated)


def test_source_sweep_mutations_are_killed() -> None:
    source_texts = _source_texts()
    injected_gui_requirement = source_texts + [
        (Path("mutation.md"), "A human must open the GUI to generate a missing `.meta` file.")
    ]
    assert _meta_gui_requirement_offenders(injected_gui_requirement) == [
        Path("mutation.md")
    ]
    mixed_requirement = source_texts + [
        (
            Path("mixed-mutation.md"),
            "A human must open the GUI to generate a missing `.meta` file; do not run headlessly.",
        )
    ]
    assert _meta_gui_requirement_offenders(mixed_requirement) == [
        Path("mixed-mutation.md")
    ]

    legitimate_prohibition = source_texts + [
        (
            Path("legitimate.md"),
            "A missing `.meta` file must be generated without a human-opened or GUI-opened Editor.",
        )
    ]
    assert _meta_gui_requirement_offenders(legitimate_prohibition) == []

    skill_text = SKILL_PATH.read_text(encoding="utf-8")
    combined = "\n".join(text for _, text in source_texts)
    assert "invalid EditMode path" in _path_contract_errors(
        skill_text, f"{combined}\nAssets/Tests/EditMode"
    )

    assembly_mutation = skill_text.replace(
        "Assets/Tests/Editor/", "Assets/Tests/Alternate/", 1
    )
    assert "assembly graph Editor path" in _path_contract_errors(
        assembly_mutation, combined
    )

    refactor_marker = "verified reference convention: `Assets/Tests/Editor`"
    assert refactor_marker in skill_text
    refactor_mutation = skill_text.replace(
        refactor_marker, "verified reference convention: `Assets/Tests/Alternate`"
    )
    assert "refactor Editor path" in _path_contract_errors(refactor_mutation, combined)


@pytest.mark.parametrize(
    ("needle", "replacement", "obligation"),
    [
        ("`-batchmode` is mandatory", "`-batchmode` is optional", "mandatory batchmode"),
        ("`-batchmode -nographics`", "`-batchmode`", "EditMode flags"),
        ("exclude `-nographics`", "include `-nographics`", "PlayMode graphics"),
        ("Never pair `-quit` with `-runTests`", "Pair `-quit` with `-runTests`", "no quit with runTests"),
        (
            "semicolon-separated list of full test names or a regex",
            "one class name",
            "testFilter semantics",
        ),
        (
            "VISUAL_VERIFICATION_UNITY",
            "LOCAL_UNITY",
            "owned editor discovery",
        ),
        (
            "ProjectSettings/ProjectVersion.txt",
            "ProjectVersion",
            "owned editor discovery",
        ),
        (
            "This skill is the single canonical implementation of editor discovery",
            "Discovery lives elsewhere",
            "single canonical discovery",
        ),
        ("Never assume a bare `Unity` executable is on `PATH`", "Assume `Unity` is on `PATH`", "no bare Unity"),
        ("absolute path under the main checkout's `dev/test-results/`", "relative results path", "main-checkout results"),
        ("Commit before testing", "Testing a dirty checkout is allowed", "commit precondition"),
        ("<unity-project-relative-path>", "<repo-root-only>", "nested project path"),
        ("no tracked changes or untracked files", "untracked files are allowed", "clean execution state"),
        (
            "<absolute-main-checkout>/dev/test-results/<unity.log>",
            "<default-unity-log>",
            "deterministic Unity log",
        ),
        (
            "1. **Persistent shadow worktree",
            "4. **Persistent shadow worktree",
            "ordered ladder",
        ),
        ("git worktree prune", "git worktree list", "prune registrations"),
        ("git worktree add --detach", "git worktree add", "detached creation"),
        ("checkout --detach", "checkout", "detached refresh"),
        ("<project-dir>-agent-tests/", "<random-worktree>/", "fixed sibling path"),
        (
            "Its gitignored `Library/` remains in place",
            "Its import cache is deleted",
            "Library retention",
        ),
        ("approximate disk cost", "no cost information", "cost announcement"),
        ("multi-minute first import", "instant first import", "cold import announcement"),
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
    mutated = section.replace(needle, replacement)
    assert obligation in _contract_errors(mutated)
