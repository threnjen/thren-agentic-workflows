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
    assert "**/delta-auditor.md" in text
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


def test_both_audit_roots_own_the_index_and_spawn_researchers_and_reconciler() -> None:
    """The four research stages live in the shared skill, not duplicated in each root.

    Both audit orchestrators declare the same children and the same
    depth-one boundary; the skill holds the stage mechanics.
    """
    skill = (SKILLS / "audit-remediation-research" / "SKILL.md").read_text()
    for heading in (
        "## Stage 1 — Prepare the draft index",
        "## Stage 2 — Research one subsystem",
        "## Stage 3 — Reconcile shared artifacts",
        "## Stage 4 — Finalize the index",
    ):
        assert heading in skill

    for name in ("auditor.md", "delta-auditor.md"):
        text = (AGENTS / name).read_text()
        assert "Auditor - Remediation Reconciler" in text
        assert "audit-remediation-research" in text
        assert "every researcher and reconciler is your direct child" in text


def test_research_skill_supports_single_target_and_comparative_modes() -> None:
    skill = _collapsed(SKILLS / "audit-remediation-research" / "SKILL.md")

    assert "single-target" in skill
    assert "comparative" in skill
    assert "supplied as `not available`" in skill

    # Only the delta root runs comparative mode; only the plain auditor
    # builds a queue from a single report.
    auditor = _collapsed(AGENTS / "auditor.md")
    delta = _collapsed(AGENTS / "delta-auditor.md")
    assert "single-target mode" in auditor
    assert "comparative mode" in delta


def test_audit_roots_split_single_target_from_multi_target() -> None:
    auditor = (AGENTS / "auditor.md").read_text()
    delta = (AGENTS / "delta-auditor.md").read_text()

    # The multi-target machinery lives only in the delta root.
    for marker in ("worktree-baseline", "Auditor - Delta", "snapshot label"):
        assert marker in delta, marker
        assert marker not in auditor.replace("Audit - Delta", ""), marker

    # Each root hands off rather than guessing at the other's run shape.
    assert "Audit - Delta" in auditor
    assert "Audit - Code, Infra, Refactor, Security" in delta


def test_both_audit_roots_share_the_remediation_pipeline_skill() -> None:
    skill = (SKILLS / "audit-remediation-pipeline" / "SKILL.md").read_text()
    assert "implementation-pipeline-loop" in skill
    assert "Feature - QA Writer" in skill
    assert "Prod Code Review" in skill

    for name in ("auditor.md", "delta-auditor.md"):
        assert "audit-remediation-pipeline" in (AGENTS / name).read_text()


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
