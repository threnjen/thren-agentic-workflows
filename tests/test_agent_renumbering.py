"""Structural proof for the final agent-family renumbering."""

from __future__ import annotations

import fnmatch
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import propagate_master_assets as propagator  # noqa: E402


# Keep the map independent of the files under test. Split number and suffix
# literals so this guard cannot pass by finding its own old identifiers.
IDENTITIES = (
    ("04", "-phase-execute", "03", "-phase-execute", "Phase - Execute", True),
    ("04a", "-feature-plan-expander", "03a", "-feature-plan-expander", "Feature - Plan Expander", False),
    ("04b", "-feature-implementer", "03b", "-feature-implementer", "Feature - Implementer", False),
    ("04c", "-feature-review-and-fix", "03c", "-reviewer-plan-conformance", "Reviewer - Plan Conformance", True),
    ("04d", "-feature-qa-writer", "03d", "-feature-qa-writer", "Feature - QA Writer", False),
    ("04e", "-diff-security-scan", "03e", "-diff-security-scan", "Diff Security Scan", True),
    ("04f", "-prod-code-review", "03f", "-prod-code-review", "Prod Code Review", False),
    ("04g", "-unity-visual-verification", "03g", "-unity-visual-verification", "Visual Verifier", False),
    ("04h", "-unity-reviewer", "03h", "-unity-reviewer", "Unity Reviewer", False),
    ("04i", "-feature-qa-runner", "03i", "-feature-qa-runner", "Feature - QA Runner", False),
    ("05", "-pr-review", "04", "-pr-review", "PR - Review", True),
    ("05" + "a", "-baseline-worktree", "04a", "-baseline-worktree", "Baseline Worktree", False),
    ("05" + "b", "-change-narrator", "04b", "-change-narrator", "Change Narrator", True),
    ("05" + "c", "-artifact-sweeper", "04c", "-artifact-sweeper", "Artifact Sweeper", True),
    ("05" + "d", "-consistency-auditor", "04d", "-consistency-auditor", "Consistency Auditor", True),
    ("05" + "e", "-dependency-auditor", "04e", "-dependency-auditor", "Dependency Auditor", True),
    ("05" + "f", "-test-health", "04f", "-test-health", "Test Health", True),
    ("05" + "g", "-readiness-synthesizer", "04g", "-readiness-synthesizer", "Readiness Synthesizer", True),
    ("05" + "h", "-cleanliness-auditor", "04h", "-cleanliness-auditor", "Cleanliness Auditor", True),
)


def _slug(number: str, suffix: str) -> str:
    return number + suffix


def _display(number: str, label: str) -> str:
    return number + " " + label


def _identity_rows() -> list[tuple[str, str, str, str, str | None, str]]:
    rows = []
    for old_number, old_suffix, new_number, new_suffix, label, numbered in IDENTITIES:
        old_slug = _slug(old_number, old_suffix)
        new_slug = _slug(new_number, new_suffix)
        old_name = _display(old_number, label) if numbered else None
        new_name = _display(new_number, label) if numbered else label
        rows.append((old_slug, new_slug, old_name, new_name, old_name, label))
    return rows


IDENTITY_ROWS = _identity_rows()
OLD_SHORT_FORMS = tuple("05" + letter for letter in "abcdefgh") + ("05" + "x",)
OLD_IDENTIFIERS = tuple(
    sorted(
        {
            token
            for old_slug, _new_slug, old_name, _new_name, _display_name, _label in IDENTITY_ROWS
            for token in (old_slug, old_name, old_slug + "-report")
            if token
        }
        | set(OLD_SHORT_FORMS),
        key=len,
        reverse=True,
    )
)
OLD_IDENTIFIER_PATTERN = re.compile(
    r"(?<![A-Za-z0-9_-])(?:"
    + "|".join(re.escape(token) for token in OLD_IDENTIFIERS)
    + r")(?![A-Za-z0-9_-])"
)

FILE_TYPE_PATTERNS = {
    "**/*.cs",
    "**/*.py",
    "**/pyproject.toml",
    "**/*.ts",
    "**/*.tsx",
    "**/*.mts",
    "**/*.cts",
}


def _scoped_files() -> list[Path]:
    paths = [
        path
        for root in (REPO_ROOT / "source_of_truth", REPO_ROOT / "tests")
        for path in root.rglob("*")
        if path.is_file()
    ]
    paths.extend(path for path in REPO_ROOT.glob("*.md") if path.is_file())
    return sorted(set(paths))


def _identifier_errors(entries: list[tuple[str, str]]) -> list[str]:
    errors: list[str] = []
    for label, text in entries:
        for line_number, line in enumerate(text.splitlines(), start=1):
            for match in OLD_IDENTIFIER_PATTERN.finditer(line):
                errors.append(f"{label}:{line_number}: {match.group(0)}")
    return errors


def _corpus_entries() -> list[tuple[str, str]]:
    entries = []
    for path in _scoped_files():
        relative = path.relative_to(REPO_ROOT).as_posix()
        entries.append((relative, relative))
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        entries.append((relative, text))
    return entries


def _agent_paths() -> set[str]:
    return {agent.rel_path for agent in propagator.load_source_agents()}


def test_no_pre_renumber_identifier_survives_in_authored_scope() -> None:
    errors = _identifier_errors(_corpus_entries())
    assert not errors, "pre-renumber agent identifiers survived:\n  " + "\n  ".join(errors)


def test_identifier_scan_fails_on_one_restored_identifier() -> None:
    old_name = _display("05", "PR - Review")
    mutated = [("README.md", "clean\n" + old_name + "\n")]
    errors = _identifier_errors(mutated)
    assert any(error.startswith("README.md:2:") and old_name in error for error in errors)


def test_source_map_moves_files_and_numbered_names() -> None:
    agents = {agent.source_slug: agent for agent in propagator.load_source_agents()}
    source_root = REPO_ROOT / "source_of_truth" / "agents"

    assert not (source_root / ("03" + "-feature-decomposer.agent.md")).exists()
    for old_slug, new_slug, _old_name, new_name, _display_name, _label in IDENTITY_ROWS:
        with_target = source_root / f"{new_slug}.agent.md"
        assert with_target.is_file(), f"renamed source agent is missing: {new_slug}"
        assert not (source_root / f"{old_slug}.agent.md").exists(), (
            f"pre-renumber source agent survived: {old_slug}"
        )
        assert agents[new_slug].name == new_name


def test_frontmatter_and_in_body_agent_references_resolve() -> None:
    agents = propagator.load_source_agents()
    names = {agent.name for agent in agents}
    missing_roster = [
        f"{agent.source_slug}: {child}"
        for agent in agents
        for child in agent.subagents
        if child not in names
    ]
    assert not missing_roster, "unresolved frontmatter agent references: " + ", ".join(
        missing_roster
    )

    unresolved_at_refs: list[str] = []
    for agent in agents:
        for match in re.finditer(r"@", agent.body):
            tail = agent.body[match.end() :]
            if tail.startswith(("[", "(")):
                continue
            if any(
                tail.startswith(name)
                and (len(tail) == len(name) or tail[len(name)] not in "A-Za-z0-9_-")
                for name in sorted(names, key=len, reverse=True)
            ):
                continue
            if re.match(r"(?:\d+[a-z]?\s+)?[A-Z]", tail):
                unresolved_at_refs.append(f"{agent.source_slug}: @{tail.splitlines()[0][:60]}")
    assert not unresolved_at_refs, "unresolved in-body agent references: " + ", ".join(
        unresolved_at_refs
    )


def test_delta_body_has_no_sibling_display_name_collision() -> None:
    agents = propagator.load_source_agents()
    delta = next(agent for agent in agents if agent.source_slug == "delta-auditor")
    collisions = [agent.name for agent in agents if agent.name in delta.body]
    assert not collisions, "agent names leaked into delta prose: " + ", ".join(collisions)


def test_agent_targeting_globs_resolve_and_character_classes_cover_both_families() -> None:
    agent_paths = _agent_paths()
    targeting_patterns = [
        (document.path, pattern)
        for document in propagator.load_instruction_docs()
        for pattern in document.apply_to_patterns
        if pattern not in FILE_TYPE_PATTERNS
    ]
    unresolved = [
        f"{path.relative_to(REPO_ROOT)}: {pattern}"
        for path, pattern in targeting_patterns
        if not any(fnmatch.fnmatch(agent_path, pattern) for agent_path in agent_paths)
    ]
    assert not unresolved, "agent-targeting applyTo globs resolve to no agent:\n  " + "\n  ".join(
        unresolved
    )

    patterns = {pattern for _path, pattern in targeting_patterns}
    assert "**/05?-*.agent.md" not in patterns
    assert "**/03?-*.agent.md" in patterns
    assert "**/04?-*.agent.md" in patterns
    assert {path for path in agent_paths if fnmatch.fnmatch(path, "**/03?-*.agent.md")} >= {
        "source_of_truth/agents/03j-reviewer-blast-radius.agent.md",
        "source_of_truth/agents/03k-reviewer-test-falsification.agent.md",
        "source_of_truth/agents/03l-reviewer-plan-blind.agent.md",
        "source_of_truth/agents/03m-finding-consolidator.agent.md",
    }
    assert any(fnmatch.fnmatch(path, "**/04?-*.agent.md") for path in agent_paths)


def test_generated_tree_has_no_pre_renumber_output_orphan() -> None:
    ports = REPO_ROOT / "ports"
    github = REPO_ROOT / ".github"
    assert ports.is_dir()
    assert (github / "copilot-instructions.md").is_file()
    for subdir in ("agents", "hooks", "instructions", "skills"):
        assert (github / subdir).is_dir(), f"missing mirrored directory: {subdir}"

    opencode = ports / "opencode" / "agents"
    github_agents = ports / "github" / "agents"
    dot_github_agents = github / "agents"
    for old_slug, _new_slug, _old_name, _new_name, _display_name, _label in IDENTITY_ROWS:
        assert not (opencode / f"{old_slug}.md").exists()
        assert not (github_agents / f"{old_slug}.agent.md").exists()
        assert not (dot_github_agents / f"{old_slug}.agent.md").exists()

    for old_slug, new_slug, _old_name, _new_name, _display_name, _label in IDENTITY_ROWS:
        if old_slug in {"04" + "-phase-execute", "05" + "-pr-review"}:
            assert not (ports / "codex" / "agents" / f"{old_slug}.toml").exists()
            assert (ports / "codex" / "agents" / f"{new_slug}.toml").is_file()
        assert (opencode / f"{new_slug}.md").is_file()
        assert (github_agents / f"{new_slug}.agent.md").is_file()
        assert (dot_github_agents / f"{new_slug}.agent.md").is_file()


def test_unity_and_prod_review_stripped_stems_remain_stable() -> None:
    for new_slug, stem in (
        ("03f-prod-code-review", "prod-code-review"),
        ("03h-unity-reviewer", "unity-reviewer"),
    ):
        assert (REPO_ROOT / "ports" / "claude" / "agents" / f"z-{stem}.md").is_file()
        assert (REPO_ROOT / "ports" / "cursor" / "agents" / f"z-{stem}.md").is_file()
        assert (REPO_ROOT / "ports" / "codex" / "agents" / f"z-{stem}.toml").is_file()
        assert (REPO_ROOT / "ports" / "opencode" / "agents" / f"{new_slug}.md").is_file()


def test_post_renumber_committee_agents_remain_at_reserved_identifiers() -> None:
    agents = {agent.source_slug: agent for agent in propagator.load_source_agents()}
    expected = {
        "03j-reviewer-blast-radius",
        "03k-reviewer-test-falsification",
        "03l-reviewer-plan-blind",
        "03m-finding-consolidator",
    }
    assert expected <= set(agents)
    assert not any(slug.startswith(("04j", "05j")) for slug in agents)
