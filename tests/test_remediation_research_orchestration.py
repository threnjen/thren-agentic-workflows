import re
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
AGENTS = REPO_ROOT / "source_of_truth" / "agents"
SKILLS = REPO_ROOT / "source_of_truth" / "skills"
INSTRUCTIONS = REPO_ROOT / "source_of_truth" / "instructions"


def _collapsed(path: Path) -> str:
    return re.sub(r"\s+", " ", path.read_text()).lower()


def test_delegation_depth_is_globally_one_level() -> None:
    text = (INSTRUCTIONS / "subagent-depth.instructions.md").read_text()

    assert "**/05-pr-review.agent.md" in text
    assert "**/auditor.md" in text
    assert "Delegation depth is one" in text
    assert "Child agents never spawn agents" in text

    hidden_with_spawn_tool = []
    for path in AGENTS.glob("*.md"):
        agent = path.read_text()
        if "user-invocable: false" in agent and re.search(
            r"^tools:\s*\[[^\]]*\bagent\b", agent, re.MULTILINE
        ):
            hidden_with_spawn_tool.append(path.name)
    assert hidden_with_spawn_tool == []


def test_auditor_owns_index_and_spawns_sibling_researchers_and_reconciler() -> None:
    text = (AGENTS / "auditor.md").read_text()

    assert "Auditor - Remediation Reconciler" in text
    assert "Stage 1: Prepare the draft index" in text
    assert "per `(delta, subsystem)`" in text
    assert "Stage 3: Reconcile the audit chain" in text
    assert "Stage 4: Finalize the index" in text
    assert "every researcher and reconciler below is your direct child" in text


def test_subsystem_researcher_has_exclusive_report_write_boundary() -> None:
    text = _collapsed(AGENTS / "auditor-remediation-research.agent.md")

    assert "exactly one subsystem" in text
    assert "write only the exclusive subsystem report path" in text
    assert "shared audit artifacts" in text
    assert "do not research an unassigned identifier" in text


def test_reconciler_is_the_shared_audit_artifact_writer() -> None:
    agent = _collapsed(AGENTS / "auditor-remediation-reconciler.agent.md")
    skill = _collapsed(
        SKILLS / "audit-remediation-research" / "SKILL.md"
    )

    assert "only the supplied current report, current summary, full delta, and queue" in agent
    assert "draft index, and subsystem reports are read-only" in agent
    assert "status: draft — unvalidated" in skill
    assert "status: final" in skill
    assert "only the reconciler writes shared audit artifacts" in skill
