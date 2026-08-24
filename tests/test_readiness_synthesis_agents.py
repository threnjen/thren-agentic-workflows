"""Structural guards for the readiness synthesizer and the orchestrator roster.

Scoped to what is machine-checkable: the readiness synthesizer rename landed in source
and in all three generated roots (leaving no slug-keyed OpenCode orphan), and
every `agents:` roster entry on the orchestrator resolves to an agent that
actually declares that `name:` on disk.
"""

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = REPO_ROOT / "source_of_truth" / "agents"
READINESS_AGENT = AGENTS_DIR / "04g-readiness-synthesizer.agent.md"
RETIRED_READINESS_AGENT = AGENTS_DIR / "05l-readiness-synthesizer.agent.md"
ORCHESTRATOR = AGENTS_DIR / "04-pr-review.agent.md"


def _body(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _assert_once(haystack: str, needle: str, label: str) -> None:
    """Assert `needle` appears exactly once.

    Exactly-once, not at-least-once. A load-bearing declaration that appears
    twice can have its real occurrence deleted while a restatement keeps the
    test green.
    """
    count = haystack.count(needle)
    assert count == 1, (
        f"{label}: expected exactly 1 occurrence of {needle!r}, found {count}. "
        "Zero means the declaration is gone; more than one means this assertion "
        "no longer pins a single load-bearing statement."
    )


def test_readiness_synthesizer_uses_the_post_renumbered_slug() -> None:
    assert READINESS_AGENT.is_file(), "04g-readiness-synthesizer.agent.md is missing"
    assert not RETIRED_READINESS_AGENT.exists(), (
        "05l-readiness-synthesizer.agent.md survived the rename"
    )


def test_readiness_synthesizer_carries_no_05l_self_reference() -> None:
    """The rename is not done while the file still carries the `05l` identifier
    anywhere -- the propagator's reference rewriting keys on the display name."""
    body = _body(READINESS_AGENT)

    assert "05l" not in body, "a `05l` self-reference survived the rename"
    _assert_once(body, "name: 04g Readiness Synthesizer", "frontmatter name")


def test_readiness_synthesizer_propagates_to_all_three_roots() -> None:
    """OpenCode filenames key on the source slug, so the rename produces a
    `05l-*` orphan there and only there; Claude and Codex key on the stem
    (`z-readiness-synthesizer`) and survive the renumber with the filename
    intact.
    """
    opencode = REPO_ROOT / "ports" / "opencode" / "agents" / "04g-readiness-synthesizer.md"
    claude = REPO_ROOT / "ports" / "claude" / "agents" / "z-readiness-synthesizer.md"
    codex = REPO_ROOT / "ports" / "codex" / "agents" / "z-readiness-synthesizer.toml"

    for generated in (opencode, claude, codex):
        assert generated.is_file(), f"readiness synthesizer did not propagate to {generated}"

    assert not (REPO_ROOT / "ports" / "opencode" / "agents" / "05l-readiness-synthesizer.md").exists(), (
        "the slug-keyed OpenCode orphan survived the rename"
    )


def test_orchestrator_roster_entry_resolves_to_the_synthesizer_on_disk() -> None:
    """Reachability, not spelling.

    The propagator resolves `agents:` entries by display name, so a roster entry
    only dispatches if some agent on disk declares that exact `name:`. Asserting
    the name merely appears in the roster line cannot see this: the string can be
    there while it resolves to nothing.
    """
    agents_line = next(
        line for line in _body(ORCHESTRATOR).splitlines() if line.startswith("agents:")
    )
    entries = [
        e.strip() for e in agents_line.split(":", 1)[1].strip().strip("[]").split(",")
    ]

    declared_names = {
        next(
            (
                line.split(":", 1)[1].strip().strip('"')
                for line in path.read_text(encoding="utf-8").splitlines()
                if line.startswith("name:")
            ),
            None,
        )
        for path in AGENTS_DIR.glob("*.agent.md")
    }

    assert "04g Readiness Synthesizer" in entries, "the synthesis position left the roster"
    for entry in entries:
        assert entry in declared_names, (
            f"roster entry {entry!r} resolves to no agent on disk -- the "
            "orchestrator cannot dispatch it"
        )
