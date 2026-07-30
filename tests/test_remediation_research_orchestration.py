import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
AGENTS = REPO_ROOT / "source_of_truth" / "agents"


def test_hidden_agents_hold_no_spawn_tool() -> None:
    """Delegation depth is one, enforced structurally rather than in prose: a
    `user-invocable: false` subagent that is granted the `agent` tool can spawn
    a second level."""
    hidden_with_spawn_tool = []
    for path in AGENTS.glob("*.md"):
        agent = path.read_text()
        if "user-invocable: false" in agent and re.search(
            r"^tools:\s*\[[^\]]*\bagent\b", agent, re.MULTILINE
        ):
            hidden_with_spawn_tool.append(path.name)
    assert hidden_with_spawn_tool == []
