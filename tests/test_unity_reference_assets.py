"""Structural guards for the inert Unity CI template and local runbook."""

from __future__ import annotations

import re
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = (
    REPO_ROOT
    / "source_of_truth/skills/unity-development/references/gameci-test-workflow.yml"
)
RUNBOOK_PATH = REPO_ROOT / "docs/unity/LOCAL_TESTING.md"


def _normalize(text: str) -> str:
    return " ".join(text.split())


def _workflow_errors(text: str) -> set[str]:
    normalized = _normalize(text)
    errors: set[str] = set()
    for token, obligation in [
        ("permissions: contents: read", "minimal permissions"),
        ("uses: actions/checkout@v4", "checkout action"),
        ("uses: game-ci/unity-test-runner@v4", "GameCI runner"),
        ("id: editmode-tests", "EditMode step identifier"),
        ("testMode: EditMode", "EditMode intent"),
        ("artifactsPath: artifacts/editmode", "EditMode artifact location"),
        ("path: ${{ steps.editmode-tests.outputs.artifactsPath }}", "EditMode artifact output"),
        ("id: playmode-tests", "PlayMode step identifier"),
        ("testMode: PlayMode", "PlayMode intent"),
        ("artifactsPath: artifacts/playmode", "PlayMode artifact location"),
        ("path: ${{ steps.playmode-tests.outputs.artifactsPath }}", "PlayMode artifact output"),
        ("uses: actions/upload-artifact@v4", "artifact action"),
        ("projectPath: <UNITY_PROJECT_PATH>", "project placeholder"),
    ]:
        if token not in normalized:
            errors.add(obligation)

    for secret in ("UNITY_LICENSE", "UNITY_EMAIL", "UNITY_PASSWORD"):
        expected = f"{secret}: ${{{{ secrets.{secret} }}}}"
        if expected not in normalized:
            errors.add(f"{secret} reference")
    if "UNITY_SERIAL:" in text:
        errors.add("Personal license only")
    if re.search(r"UNITY_(?:LICENSE|EMAIL|PASSWORD):\s*(?!\$\{\{ secrets\.)\S+", text):
        errors.add("literal credentials")
    if "githubToken:" in text:
        errors.add("unneeded token permission")
    if "matrix:" in text:
        errors.add("matrix-free reference")
    if normalized.count("uses: game-ci/unity-test-runner@v4") != 2:
        errors.add("two test executions")
    if normalized.count("uses: actions/upload-artifact@v4") != 2:
        errors.add("artifact action")
    if normalized.count("if: always()") != 2:
        errors.add("always upload")

    play_step = re.search(
        r"- name: Run PlayMode tests\n(.*?)(?=\n\s+- name:)",
        text,
        re.DOTALL,
    )
    if play_step is None or "if: ${{ !cancelled() }}" not in play_step.group(1):
        errors.add("PlayMode failure independence")
    return errors


def _numbered_steps(text: str) -> list[str]:
    return re.findall(r"^## \d+\. .*?\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)


def _runbook_errors(text: str) -> set[str]:
    normalized = _normalize(text)
    errors: set[str] = set()
    tldr = re.search(r"^## TL;DR\s*$\n(.*?)(?=^## )", text, re.MULTILINE | re.DOTALL)
    if tldr is None:
        errors.add("TLDR")
    else:
        lines = [line for line in tldr.group(1).splitlines() if line.strip()]
        if not lines or len(lines) > 5:
            errors.add("TLDR length")

    steps = _numbered_steps(text)
    if not steps:
        errors.add("numbered steps")
    for index, step in enumerate(steps, 1):
        if len(re.findall(r"```bash\n.*?\n```", step, re.DOTALL)) != 1:
            errors.add(f"step {index} command")
        if "**Correct result:**" not in step:
            errors.add(f"step {index} result")
    if steps and "git status --short" in steps[0]:
        errors.add("staging result describes its own command")

    for token, obligation in [
        (" commit -m ", "commit first"),
        (" worktree prune", "prune"),
        (" worktree add --detach", "detached worktree"),
        ("<project-dir>-agent-tests/", "fixed sibling"),
        ("roughly 600 MB", "plain disk cost"),
        ("multi-minute first import", "cold import"),
        ("checkout --detach", "refresh"),
        ("`Library/`", "Library retention"),
        (
            "no ignored content outside `<execution-unity-project>/Library/`",
            "strict ignored-content boundary",
        ),
        ("`unity-development` skill's Editor discovery", "editor discovery"),
        ("-batchmode -nographics -runTests", "EditMode flags"),
        ("-batchmode -runTests", "PlayMode flags"),
        ("absolute-main-checkout>/dev/test-results", "absolute results"),
        ("not-executed: editor open, user unavailable", "unattended status"),
        ("Never launch a GUI", "GUI prohibition"),
        ("Agent runs every test command itself", "agent-run tests"),
        ("worktree remove", "manual teardown"),
        ("Teardown is never automatic", "no automatic teardown"),
        ("CI installation is out of scope", "CI scope"),
        ("Unity Personal", "Personal concurrency"),
        ("-batchmode -quit", "headless import"),
        ("<test-run total= passed= failed=>", "root XML counts"),
        ("<test-case result=\"Failed\">", "failing test names"),
        ("zero discovered tests is `not-executed`", "zero-test status"),
        ("retain its Unity log", "failure log retention"),
    ]:
        if token not in normalized:
            errors.add(obligation)

    edit_command = next(
        (line for line in text.splitlines() if "-testPlatform EditMode" in line), ""
    )
    play_command = next(
        (line for line in text.splitlines() if "-testPlatform PlayMode" in line), ""
    )
    if "-nographics" not in edit_command:
        errors.add("EditMode nographics")
    if not play_command or "-nographics" in play_command:
        errors.add("PlayMode graphics")
    if "rm -rf" in text:
        errors.add("unsafe teardown")
    if any(
        token in text
        for token in ("worktree remove \"$", "worktree remove *", "worktree remove / ")
    ):
        errors.add("fixed teardown target")
    if "-quit" in edit_command or "-quit" in play_command:
        errors.add("test command quit flag")

    fallback_tokens = (
        "persistent detached worktree",
        "ask the user to close the main Unity Editor",
        "not-executed: editor open, user unavailable",
    )
    positions = [text.find(token) for token in fallback_tokens]
    if any(position < 0 for position in positions) or positions != sorted(positions):
        errors.add("fallback order")

    teardown = next(
        (step for step in steps if "worktree remove" in step),
        "",
    )
    if "Only run this after Step 13 confirms the exact path." not in teardown:
        errors.add("adjacent teardown warning")
    return errors


def test_reference_assets_exist_only_in_inert_locations() -> None:
    assert WORKFLOW_PATH.is_file(), f"missing {WORKFLOW_PATH.relative_to(REPO_ROOT)}"
    assert RUNBOOK_PATH.is_file(), f"missing {RUNBOOK_PATH.relative_to(REPO_ROOT)}"
    assert not (REPO_ROOT / ".github/workflows/gameci-test-workflow.yml").exists()


def test_gameci_workflow_contract() -> None:
    text = WORKFLOW_PATH.read_text(encoding="utf-8")
    assert text.strip(), "workflow template is empty"
    assert not _workflow_errors(text), sorted(_workflow_errors(text))


def test_local_runbook_contract() -> None:
    text = RUNBOOK_PATH.read_text(encoding="utf-8")
    assert text.strip(), "local runbook is empty"
    assert not _runbook_errors(text), sorted(_runbook_errors(text))


@pytest.mark.parametrize(
    ("needle", "replacement", "obligation"),
    [
        ("uses: actions/checkout@v4", "uses: actions/checkout@v3", "checkout action"),
        (
            "uses: game-ci/unity-test-runner@v4",
            "uses: game-ci/unity-test-runner@v2",
            "GameCI runner",
        ),
        ("testMode: PlayMode", "testMode: Standalone", "PlayMode intent"),
        (
            "uses: actions/upload-artifact@v4",
            "uses: actions/upload-artifact@v3",
            "artifact action",
        ),
        ("if: always()", "if: success()", "always upload"),
        (
            "UNITY_LICENSE: ${{ secrets.UNITY_LICENSE }}",
            "UNITY_LICENSE: literal-license",
            "UNITY_LICENSE reference",
        ),
        (
            "if: ${{ !cancelled() }}",
            "if: ${{ success() }}",
            "PlayMode failure independence",
        ),
    ],
)
def test_workflow_mutations_are_killed(
    needle: str, replacement: str, obligation: str
) -> None:
    text = WORKFLOW_PATH.read_text(encoding="utf-8")
    assert needle in text, f"mutation target missing for {obligation}"
    mutated = text.replace(needle, replacement)
    assert obligation in _workflow_errors(mutated)


def test_removing_all_artifact_uploads_is_detected() -> None:
    text = WORKFLOW_PATH.read_text(encoding="utf-8")
    mutated = text.replace("uses: actions/upload-artifact@v4", "")
    assert "artifact action" in _workflow_errors(mutated)


@pytest.mark.parametrize(
    ("needle", "replacement", "obligation"),
    [
        ("worktree prune", "worktree list", "prune"),
        ("roughly 600 MB", "an unknown amount", "plain disk cost"),
        ("multi-minute first import", "instant import", "cold import"),
        ("Never launch a GUI", "Launch a GUI", "GUI prohibition"),
        ("worktree remove", "worktree list", "manual teardown"),
        ("Teardown is never automatic", "Teardown is automatic", "no automatic teardown"),
        ("`Library/`", "the cache", "Library retention"),
        (
            "no ignored content outside `<execution-unity-project>/Library/`",
            "ignored content outside `<execution-unity-project>/Library/` is allowed",
            "strict ignored-content boundary",
        ),
        (
            "zero discovered tests is `not-executed`",
            "zero discovered tests is `executed-green`",
            "zero-test status",
        ),
        (
            "<test-run total= passed= failed=>",
            "a generic result summary",
            "root XML counts",
        ),
        (
            "<test-case result=\"Failed\">",
            "failed cases",
            "failing test names",
        ),
        (
            "retain its Unity log",
            "discard its Unity log",
            "failure log retention",
        ),
        (
            "The command exits with status 0 and reports no path or repository error.",
            "`git status --short` shows the intended files staged.",
            "staging result describes its own command",
        ),
    ],
)
def test_runbook_mutations_are_killed(
    needle: str, replacement: str, obligation: str
) -> None:
    text = RUNBOOK_PATH.read_text(encoding="utf-8")
    assert needle in text, f"mutation target missing for {obligation}"
    mutated = text.replace(needle, replacement)
    assert obligation in _runbook_errors(mutated)
