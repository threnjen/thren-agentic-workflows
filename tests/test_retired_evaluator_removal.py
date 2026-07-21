"""Retirement guard for the five phase-shaped Phase Final Review evaluators.

The PR-Review rescope (see `.github/learnings/cross-phase-decisions.md`) retired
five evaluators whose premise was a multi-subphase phase: a PR has no subphases
and no acceptance criteria of its own. This module is the standing proof that
they are gone and stay gone -- from source, from all three generated roots, and
from every authored file that is not a historical record.

The retired names live here once, as `RETIRED_AGENTS`. Nothing in this module
re-lists them.
"""

import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

# The canonical five. (source slug, display name) -- the display name matters
# because the propagator's `_rewrite_agent_references` matches on it, so a
# surviving prose mention stops being rewritten and ships as a dangling literal.
RETIRED_AGENTS = (
    ("05c-qa-consolidator", "05c QA Consolidator"),
    ("05d-security-rollup", "05d Security Rollup"),
    ("05e-ac-regression", "05e AC Regression"),
    ("05f-seam-analyzer", "05f Seam Analyzer"),
    ("05i-learnings-harvester", "05i Learnings Harvester"),
)

RETIRED_SLUGS = tuple(slug for slug, _ in RETIRED_AGENTS)
RETIRED_DISPLAY_NAMES = tuple(name for _, name in RETIRED_AGENTS)


GITHUB_AGENTS_DIR = REPO_ROOT / "source_of_truth" / "agents"

# Paths allowed to keep retired names. Directory-scoped, and the single source of
# truth for the sweep -- an exception list that drifts from the thing it excepts
# is how a propagated copy of an exempt file sneaks through.
EXEMPT_PREFIXES = (
    # Historical phase records. They describe what was built and must retain it.
    "docs/phases/",
    # Decision history, and its propagated copy -- generated, not authored.
    "source_of_truth/learnings/",
    ".github/learnings/",
    "ports/claude/learnings/",
    "ports/github/learnings/",
    "ports/cursor/rules/",
    # Feature planning documents. They name the retired agents in order to
    # describe retiring them; same category as docs/phases/ -- a record of the
    # work, not live harness wiring.
    #
    # Scoped to `dev/feature/`, NOT all of `dev/`: `dev/phase-final-review/
    # fixtures/` is live wiring -- the surviving 05x evaluators and the
    # orchestrator name it as their fixture root -- so it must stay swept.
    "dev/feature/",
)

# `EXEMPT_SKILL_DIRS` lived here. It time-boxed the two skills whose report
# rosters named retired evaluators, because `03-pr-review-conventions-skills`
# owned those files and rewriting them from feature `02` would have collided.
# Feature `03` has landed: both directories are renamed (`phase-final-review-*`
# -> `pr-review-*`) and the retired-evaluator templates are dropped, so the
# exemption stopped excepting anything and became a hole in the sweep. Removed
# in that same pass, with `test_time_boxed_skill_exemption_is_still_load_bearing`
# -- exactly as both were designed to be. The renamed skills are now swept like
# any other authored file.

# This module defines the retired-name list.
EXEMPT_FILES = ("tests/test_retired_evaluator_removal.py",)


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


def test_retired_agents_are_absent_from_source() -> None:
    """AC1: no retired agent remains under `.github/agents/`."""
    for slug in RETIRED_SLUGS:
        source = GITHUB_AGENTS_DIR / f"{slug}.agent.md"
        assert not source.exists(), f"retired source agent still present: {source}"


def test_retired_agents_are_absent_from_every_generated_root() -> None:
    """AC2: propagation self-cleans all three roots via `01-propagator-orphan-pruning`.

    Nothing here was hand-deleted. If this fails, the pruner is the bug -- do not
    `git rm` the output, which would mask the defect until the next rename.
    """
    generated = {
        REPO_ROOT / "ports" / "claude" / "agents": "z-{stem}.md",
        REPO_ROOT / "ports" / "opencode" / "agents": "{slug}.md",
        REPO_ROOT / "ports" / "codex" / "agents": "z-{stem}.toml",
    }

    for root, template in generated.items():
        for slug in RETIRED_SLUGS:
            # `z-` outputs drop the numeric prefix: 05c-qa-consolidator -> z-qa-consolidator
            stem = slug.split("-", 1)[1]
            output = root / template.format(slug=slug, stem=stem)
            assert not output.exists(), f"retired generated output survived: {output}"


def test_security_scan_survives_and_still_propagates() -> None:
    """AC5: `Security Scan` outlives its retired `05d` parent.

    It is general-purpose and separately referenced; the diff-scoped check the
    rollup wrapped is delegated to `04e-diff-security-scan`, a different agent.
    Deleting it by association would remove working capability.

    Losing its only parent made it standalone rather than dead: it is
    user-invocable, so it keeps a slash command on every platform. It correctly
    loses its Claude *spawnable subagent* file (`claude/agents/z-security-scan.md`),
    because after `05d` no agent declares it as a child.
    """
    assert (REPO_ROOT / "source_of_truth" / "agents" / "security-scan.agent.md").exists()

    for output in (
        REPO_ROOT / "ports" / "claude" / "commands" / "security-scan.md",
        REPO_ROOT / "ports" / "opencode" / "agents" / "security-scan.md",
        REPO_ROOT / "ports" / "codex" / "agents" / "security-scan.toml",
        REPO_ROOT / "ports" / "codex" / "profiles" / "security-scan.config.toml",
    ):
        assert output.exists(), f"Security Scan stopped propagating to {output}"

    assert not (REPO_ROOT / "ports" / "claude" / "agents" / "z-security-scan.md").exists(), (
        "no agent declares Security Scan as a child, so it must not keep a "
        "spawnable subagent file"
    )


def test_no_tracked_file_references_a_retired_agent() -> None:
    """AC6: no retired slug or display name survives outside the exempt paths.

    Display names matter as much as slugs: the propagator's
    `_rewrite_agent_references` matches on the display name, so once a source
    agent is deleted it drops out of the reference map and any surviving prose
    saying "05d Security Rollup" silently ships as a literal. The propagator will
    not catch that. This is what does.
    """
    offenders: list[str] = []

    for path in _tracked_files():
        if _is_exempt(path):
            continue
        try:
            text = (REPO_ROOT / path).read_text(encoding="utf-8")
        except (UnicodeDecodeError, FileNotFoundError, IsADirectoryError):
            continue
        found = sorted(
            {name for name in RETIRED_SLUGS + RETIRED_DISPLAY_NAMES if name in text}
        )
        if found:
            offenders.append(f"{path}: {', '.join(found)}")

    assert not offenders, "retired agents still referenced:\n" + "\n".join(offenders)


def test_no_surviving_agent_declares_a_retired_child() -> None:
    """AC5b: no `agents:` frontmatter roster names a deleted agent.

    This is the mirror image of the `Security Scan` trap: deleting `05d`
    orphaned its child's parent claim, and deleting the five orphaned the
    orchestrator's entries for them.
    """
    for source in sorted(GITHUB_AGENTS_DIR.glob("*.agent.md")):
        frontmatter = source.read_text(encoding="utf-8")[4:].split("\n---\n", 1)[0]
        roster_lines = [
            line for line in frontmatter.splitlines() if line.startswith("agents:")
        ]
        for line in roster_lines:
            for name in RETIRED_DISPLAY_NAMES:
                assert name not in line, (
                    f"{source.name} declares deleted child {name!r} in its roster"
                )
