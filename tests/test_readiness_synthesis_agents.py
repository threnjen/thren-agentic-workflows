from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
READINESS_AGENT = REPO_ROOT / ".github" / "agents" / "05l-readiness-synthesizer.agent.md"
LEARNINGS_AGENT = REPO_ROOT / ".github" / "agents" / "05i-learnings-harvester.agent.md"


def test_readiness_synthesizer_declares_report_only_synthesis_contract() -> None:
    body = READINESS_AGENT.read_text(encoding="utf-8")

    assert "phase-final-review-conventions" in body
    assert "phase-final-review-report" in body
    assert ".github/agents/prod-code-review.md" in body
    assert "evaluator report" in body.lower()
    assert "never read\ncode" in body.lower()
    assert "readiness-report.md" in body
    assert "Critical" in body
    assert "High" in body
    assert "Medium" in body
    assert "Low" in body


def test_readiness_synthesizer_caps_verdict_when_checks_are_missing() -> None:
    body = READINESS_AGENT.read_text(encoding="utf-8").lower()

    assert "missing," in body
    assert "unreadable" in body
    assert "not-run" in body or "not run" in body
    assert "no blockers found, coverage incomplete" in body
    assert "never" in body and "go" in body
    assert "checks not run" in body


def test_learnings_harvester_declares_history_mining_and_draft_only_outputs() -> None:
    body = LEARNINGS_AGENT.read_text(encoding="utf-8").lower()

    assert "phase-final-review-conventions" in body
    assert "05i-learnings-harvester-report.md" in body
    assert ".github/learnings/" in body
    assert "instructions-writer" in body
    assert "instructions-evaluator" in body
    assert "git history" in body
    assert "4dd01e9" in body
    assert "pr #19" in body
    assert "pr #20" in body
    assert "ledger-commits.jsonl" in body
    assert "never edits `.github/instructions/`" in body
    assert "never commits" in body
    assert "none found" in body


def test_both_agents_honor_shared_return_contract_and_readiness_tier() -> None:
    readiness_body = READINESS_AGENT.read_text(encoding="utf-8").lower()
    learnings_body = LEARNINGS_AGENT.read_text(encoding="utf-8").lower()

    assert "at most 10 lines" in readiness_body
    assert "at most 10 lines" in learnings_body
    assert "top available" in readiness_body
    assert "state-of-the-art" in readiness_body
