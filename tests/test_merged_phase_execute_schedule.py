"""Contract guards for the merged Phase - Execute schedule."""

from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_AGENT_ROOT = REPO_ROOT / "source_of_truth/agents"
INSTRUCTION_ROOT = REPO_ROOT / "source_of_truth/instructions"

REMOVED_AGENT_LABEL = "Feature - " + "Decomposer"
REMOVED_AGENT_SLUG = "03-feature-" + "decomposer"


def _corpus_paths() -> list[Path]:
    paths = [
        path
        for root in (REPO_ROOT / "source_of_truth", REPO_ROOT / "tests")
        for path in root.rglob("*")
        if path.is_file()
        and path.suffix in {".md", ".py"}
        and "__pycache__" not in path.parts
    ]
    paths.extend(REPO_ROOT.glob("*.md"))
    paths.append(REPO_ROOT / "docs/ARCHITECTURE.md")
    return sorted(set(paths))


def _agent_apply_to_patterns() -> list[tuple[Path, str]]:
    patterns: list[tuple[Path, str]] = []
    for path in INSTRUCTION_ROOT.glob("*.instructions.md"):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.startswith("applyTo:"):
                continue
            value = line.partition(":")[2].strip().strip('"')
            for pattern in value.split(","):
                pattern = pattern.strip()
                if ".agent.md" in pattern:
                    patterns.append((path, pattern))
    return patterns


def test_removed_decomposer_has_no_corpus_references() -> None:
    errors: list[str] = []
    for path in _corpus_paths():
        text = path.read_text(encoding="utf-8")
        if REMOVED_AGENT_SLUG in text.lower() or REMOVED_AGENT_LABEL in text:
            errors.append(str(path.relative_to(REPO_ROOT)))
    assert not errors, f"retired agent reference remains: {errors}"
    assert not (SOURCE_AGENT_ROOT / f"{REMOVED_AGENT_SLUG}.agent.md").exists()


def test_agent_apply_to_globs_resolve_to_existing_agents() -> None:
    agent_paths = [
        path.relative_to(REPO_ROOT).as_posix()
        for path in SOURCE_AGENT_ROOT.glob("*.agent.md")
    ]
    unresolved = [
        f"{path.relative_to(REPO_ROOT)}: {pattern}"
        for path, pattern in _agent_apply_to_patterns()
        if not any(Path(agent).match(pattern) for agent in agent_paths)
    ]
    assert not unresolved, f"applyTo glob resolves to no source agent: {unresolved}"


