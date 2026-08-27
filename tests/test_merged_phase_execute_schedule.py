"""Contract guards for the merged Phase - Execute schedule."""

from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PHASE_EXECUTE_PATH = REPO_ROOT / "source_of_truth/agents/03-phase-execute.agent.md"
SOURCE_AGENT_ROOT = REPO_ROOT / "source_of_truth/agents"
INSTRUCTION_ROOT = REPO_ROOT / "source_of_truth/instructions"

REMOVED_AGENT_LABEL = "Feature - " + "Decomposer"
REMOVED_AGENT_SLUG = "03-feature-" + "decomposer"

REQUIRED_SCHEDULE_CONTRACT = {
    "lightweight plans": "create one lightweight plan per candidate feature before scheduling",
    "plan contents": "acceptance criteria, scope, prerequisite hypotheses, and expected file impact",
    "plan boundary": "Lightweight plans contain no context or task document",
    "prerequisite graph": "Build the prerequisite graph",
    "per-feature recomputation": "Recompute the graph and order after every completed feature",
    "just-in-time expansion": "Expand only the selected feature against the repository state at selection time",
    "single-feature execution": "Execute one feature at a time, in the manifest's execution order",
    "write-set evidence": "An expected write set is revalidation evidence only, never concurrency permission",
    "affected future revalidation": "identify every affected future feature and every downstream dependent",
    "recompute bound": "Bound recomputation to 25 rounds per level",
    "plan change evidence": "Record every plan rewrite, reorder, split, merge, or delay with evidence",
    "expander": "by spawning **Feature - Plan Expander** when its context or tasks are absent or stale",
    "interrupted run": "report an interrupted run and offer resumption",
    "mid-loop rebuild": "Discard and rebuild a feature interrupted mid-loop",
    "commit resume state": "Resume at the last completed feature using the status and validation commit the manifest records for it",
    "context drop": "After the plans are on disk, decomposition context may drop",
    "manifest memory": "Treat the manifest and the per-feature checkpoint commits as execution memory",
}


def _phase_text() -> str:
    return PHASE_EXECUTE_PATH.read_text(encoding="utf-8")


def _missing_schedule_contract(text: str) -> set[str]:
    return {
        label for label, phrase in REQUIRED_SCHEDULE_CONTRACT.items() if phrase not in text
    }


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


def test_merged_agent_carries_the_living_schedule_contract() -> None:
    missing = _missing_schedule_contract(_phase_text())
    assert not missing, f"merged schedule contract missing: {sorted(missing)}"


def test_schedule_guard_is_load_bearing() -> None:
    original = _phase_text()
    assert not _missing_schedule_contract(original)
    for label, phrase in REQUIRED_SCHEDULE_CONTRACT.items():
        mutated = original.replace(phrase, "", 1)
        assert label in _missing_schedule_contract(mutated), f"inert schedule guard: {label}"


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


def test_revalidation_contract_catches_a_shared_file_later_feature() -> None:
    text = _phase_text()
    signals = (
        "expected write set",
        "every affected future feature and every downstream dependent",
        "recompute the graph and order",
    )
    assert all(signal in text for signal in signals)
    mutated = text.replace(signals[1], "", 1)
    assert not all(signal in mutated for signal in signals)
