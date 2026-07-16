from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
READINESS_AGENT = REPO_ROOT / ".github" / "agents" / "05l-readiness-synthesizer.agent.md"


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

    assert "missing" in body
    assert "unreadable" in body
    assert "not-run" in body or "not run" in body
    assert "failed" in body
    assert "canonical hand-off report" in body
    assert "no blockers found, coverage incomplete" in body
    assert "never" in body and "go" in body
    assert "checks not run" in body


def test_readiness_synthesizer_honors_shared_return_contract_and_top_tier() -> None:
    readiness_body = READINESS_AGENT.read_text(encoding="utf-8").lower()

    assert "at most 10 lines" in readiness_body
    assert "top available" in readiness_body
    assert "state-of-the-art" in readiness_body
