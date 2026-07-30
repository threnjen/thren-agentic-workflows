"""Retirement guard for the eval-grader benchmarking system.

The grader could not run on its own. Producing its inputs required standing
instrumentation in agents that had nothing to do with grading: a post-commit hook
symlinked into every target repo, install steps carried by `02 Phase - Refiner`,
ledger-annotation sections in `04b`, `04c`, and `Debugger`, and a
`remediation-ledger-contract` instruction whose `applyTo` matched every `.py`,
`.ts`, `.js`, and `.cs` file -- so it loaded into context on nearly every coding
task. The benchmarking value did not justify that standing cost.

The four agents, two skills, and the hook were archived to `eval/deprecated/`
(outside `source_of_truth/`, so propagation does not see them). The
instrumentation was deleted outright, because archiving a thing whose whole cost
was being loaded everywhere buys nothing.

This module is the standing proof the instrumentation stays gone. It deliberately
does NOT assert the archived files are absent from `eval/deprecated/` -- they are
supposed to be there, and `eval/runs/` keeps the historical run artifacts.

Modeled on `test_retired_evaluator_removal.py`, which guards the five retired
phase-shaped evaluators the same way.
"""

import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SOT = REPO_ROOT / "source_of_truth"
ARCHIVE = REPO_ROOT / "eval" / "deprecated"

# The archived assets, by their source-of-truth path relative to `source_of_truth/`.
ARCHIVED_AGENTS = (
    "eval-grader.agent.md",
    "eval-metric-grader.agent.md",
    "eval-score-recorder.agent.md",
    "eval-feature-decomposition.agent.md",
)
ARCHIVED_SKILLS = (
    "eval-score-table-output",
    "eval-feature-decomposition-report",
)

# Display names. These matter for the same reason they do in the evaluator guard:
# the propagator's `_rewrite_agent_references` matches on the display name, so a
# surviving prose mention stops being rewritten and ships as a dangling literal.
ARCHIVED_DISPLAY_NAMES = (
    "Eval - Grader",
    "Eval - Metric Grader",
    "Eval - Score Recorder",
    "Eval - Feature Decomposition",
)

# The instrumentation tokens. A reappearance of any of these under
# `source_of_truth/` means the standing context cost came back.
LEDGER_TOKENS = (
    "ledger-commits.jsonl",
    "ledger-events.jsonl",
    "remediation-ledger-contract",
    "eval/runs/",
    "eval/scoring/",
    "post-commit.sh",
    "eval-score-table-output",
    "eval-feature-decomposition-report",
)

# Paths allowed to keep these names. Directory-scoped, same rationale as the
# evaluator guard: an exception list that drifts from the thing it excepts is how
# a propagated copy of an exempt file sneaks through.
EXEMPT_PREFIXES = (
    # The archive itself and the historical run artifacts it documents.
    "eval/",
    # Historical phase records -- they describe what was built.
    "docs/phases/",
    # Decision history and its propagated copies. `05-pr-review` records its own
    # earlier ledger removal there; that note is the reason, not a regression.
    "source_of_truth/learnings/",
    ".github/learnings/",
    "ports/claude/learnings/",
    "ports/github/learnings/",
    "ports/cursor/rules/",
    "dev/feature/",
)

EXEMPT_FILES = (
    # This module defines the token list.
    "tests/test_eval_grader_retirement.py",
    # `eval/runs/` is gitignored here (0 tracked files), so the rule keeps local
    # run output from being committed. Deleting the line would surface every
    # local run directory as a commit candidate.
    ".gitignore",
    # Documents this guard, including the token names it fires on.
    "docs/TROUBLESHOOTING.md",
)


def _is_exempt(path: str) -> bool:
    return path.startswith(EXEMPT_PREFIXES) or path in EXEMPT_FILES


def _tracked_files() -> list[str]:
    listing = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    return [path for path in listing.split("\0") if path]


def test_archived_agents_are_absent_from_the_authoring_surface() -> None:
    """The four eval agents no longer live under `source_of_truth/agents/`."""
    for name in ARCHIVED_AGENTS:
        assert not (SOT / "agents" / name).exists(), (
            f"archived eval agent is back on the authoring surface: {name}. "
            "Restoring it also restores the instrumentation cost -- see "
            "eval/deprecated/README.md before reviving it."
        )


def test_archived_skills_are_absent_from_the_authoring_surface() -> None:
    """Both grader-only skills are gone from `source_of_truth/skills/`."""
    for name in ARCHIVED_SKILLS:
        assert not (SOT / "skills" / name).exists(), (
            f"archived eval skill is back on the authoring surface: {name}"
        )


def test_the_ledger_contract_instruction_stays_deleted() -> None:
    """The always-on instruction was the single largest cost and is not archived.

    Its `applyTo` matched every `.py`, `.ts`, `.js`, and `.cs` file, so it loaded
    on nearly every coding task in every repo the agents run against. Unlike the
    agents, it was deleted rather than parked -- archiving something whose only
    cost is being loaded everywhere buys nothing.
    """
    contract = SOT / "instructions" / "remediation-ledger-contract.instructions.md"
    assert not contract.exists(), (
        "the remediation-ledger-contract instruction is back. If ledger capture "
        "is genuinely wanted again, make it opt-in per run rather than an "
        "always-applied instruction -- that breadth is why it was removed."
    )


def test_archived_agents_are_absent_from_every_generated_root() -> None:
    """Propagation self-cleans the generated roots via orphan pruning.

    Nothing here was hand-deleted. If this fails the pruner is the bug -- do not
    `git rm` the output, which would mask the defect until the next rename.
    """
    stems = tuple(name.removesuffix(".agent.md") for name in ARCHIVED_AGENTS)
    generated = {
        REPO_ROOT / "ports" / "claude" / "agents": ("{stem}.md", "z-{stem}.md"),
        REPO_ROOT / "ports" / "claude" / "commands": ("{stem}.md",),
        REPO_ROOT / "ports" / "opencode" / "agents": ("{stem}.md",),
        REPO_ROOT / "ports" / "codex" / "agents": ("{stem}.toml", "z-{stem}.toml"),
        REPO_ROOT / "ports" / "cursor" / "commands": ("{stem}.md",),
    }

    for root, templates in generated.items():
        for stem in stems:
            for template in templates:
                output = root / template.format(stem=stem)
                assert not output.exists(), (
                    f"archived eval agent still propagates: {output}"
                )


def test_the_post_commit_hook_is_archived_not_live() -> None:
    """`eval/hooks/` was the install source named by `02 Phase - Refiner`."""
    assert not (REPO_ROOT / "eval" / "hooks").exists(), (
        "eval/hooks/ is back at its old path -- `02 Phase - Refiner` used to "
        "symlink from exactly there"
    )
    assert (ARCHIVE / "hooks" / "post-commit.sh").exists(), (
        "the archived hook vanished; eval/deprecated/README.md documents it"
    )


def test_no_ledger_instrumentation_survives_on_the_authoring_surface() -> None:
    """The sweep. No authored source file may reference the ledger machinery.

    This is the guard that actually holds the line: individual file assertions
    catch a wholesale revert, but instrumentation crept in one agent section at a
    time and would creep back the same way.
    """
    offenders: list[str] = []
    for path in _tracked_files():
        if _is_exempt(path):
            continue
        full = REPO_ROOT / path
        if not full.is_file():
            continue
        try:
            body = full.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        hits = [token for token in LEDGER_TOKENS if token in body]
        if hits:
            offenders.append(f"{path}: {', '.join(hits)}")

    assert not offenders, (
        "ledger instrumentation reappeared:\n  " + "\n  ".join(offenders) + "\n"
        "The grader is archived and nothing consumes these files. See "
        "eval/deprecated/README.md."
    )


def test_the_archive_is_intact_and_documented() -> None:
    """An empty archive means someone deleted the history the README describes."""
    assert (ARCHIVE / "README.md").exists(), "eval/deprecated/README.md is missing"
    for name in ARCHIVED_AGENTS:
        assert (ARCHIVE / "agents" / name).exists(), f"archived agent lost: {name}"
    for name in ARCHIVED_SKILLS:
        assert (ARCHIVE / "skills" / name / "SKILL.md").exists(), (
            f"archived skill lost: {name}"
        )
