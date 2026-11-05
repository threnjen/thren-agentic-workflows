"""Behavior tests for the test gate, driven through its CLI against throwaway repositories."""

from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

import pytest

GATE = (
    Path(__file__).resolve().parents[1]
    / "source_of_truth/skills/test-gate/scripts/test_gate.py"
)

# A fake suite. It counts launches, optionally sleeps, and writes NUnit XML.
RUNNER = """#!/usr/bin/env bash
results="$1"
echo run >> "$COUNT_FILE"
[ -n "${SUITE_SLEEP:-}" ] && sleep "$SUITE_SLEEP"
[ -f "$RESULT_XML" ] && cp "$RESULT_XML" "$results"
exit 0
"""
COMMAND = "bash runner.sh {results}"


def _xml(**results: str) -> str:
    cases = "".join(f'<test-case fullname="{n}" result="{r}"/>' for n, r in results.items())
    return f"<test-run>{cases}</test-run>"


@pytest.fixture
def env(tmp_path: Path) -> dict[str, str]:
    result_xml = tmp_path / "suite.xml"
    result_xml.write_text(_xml(A="Passed", B="Passed"))
    values = dict(os.environ)
    values.update(COUNT_FILE=str(tmp_path / "count"), RESULT_XML=str(result_xml))
    return values


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    path = tmp_path / "repo"
    path.mkdir()
    (path / "runner.sh").write_text(RUNNER)
    (path / "code.txt").write_text("one\n")
    _git(path, "init", "-q")
    _git(path, "add", ".")
    _commit(path, "start")
    return path


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


def _commit(repo: Path, message: str) -> None:
    _git(repo, "add", ".")
    _git(repo, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", message)


def _gate(
    repo: Path, env: dict[str, str], *args: str, extra: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(GATE), "--repo", str(repo), *args],
        capture_output=True,
        text=True,
        env={**env, **(extra or {})},
    )


def _ensure(repo: Path, env: dict[str, str], *args: str, **kwargs):
    return _gate(repo, env, "ensure", "--command", COMMAND, *args, **kwargs)


def _launches(env: dict[str, str]) -> int:
    path = Path(env["COUNT_FILE"])
    return len(path.read_text().splitlines()) if path.exists() else 0


def _runs(repo: Path) -> list[dict]:
    root = repo / ".git/test-gate/runs"
    return [json.loads((d / "run.json").read_text()) for d in sorted(root.iterdir())]


def _field(output: str, name: str) -> str:
    return next(line.split(": ", 1)[1] for line in output.splitlines() if line.startswith(name + ": "))


def test_run_saves_a_complete_manifest(repo: Path, env: dict[str, str]) -> None:
    done = _ensure(repo, env)
    assert done.returncode == 0, done.stdout
    run = _runs(repo)[0]
    head = subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "HEAD"], capture_output=True, text=True
    ).stdout.strip()
    assert run["commit"] == head
    assert run["dirty_hash"] == "clean"
    assert run["timestamp"] and run["scope"] == "full" and run["duration_seconds"] >= 0
    assert run["counts"] == {"total": 2, "passed": 2, "failed": 0, "skipped": 0}
    assert run["status"] == "executed-green"


def test_unchanged_code_reuses_and_names_the_evidence(repo: Path, env: dict[str, str]) -> None:
    first = _ensure(repo, env)
    second = _ensure(repo, env)
    assert second.returncode == 0
    assert _launches(env) == 1
    assert f"REUSED from run {_field(first.stdout, 'run')}" in second.stdout
    assert "total=2 passed=2 failed=0 skipped=0" in second.stdout


def test_new_commit_with_identical_tree_reuses(repo: Path, env: dict[str, str]) -> None:
    _ensure(repo, env)
    _git(repo, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "--allow-empty", "-m", "empty")
    assert "REUSED" in _ensure(repo, env).stdout
    assert _launches(env) == 1


def test_code_commit_invalidates(repo: Path, env: dict[str, str]) -> None:
    _ensure(repo, env)
    (repo / "code.txt").write_text("two\n")
    _commit(repo, "change")
    done = _ensure(repo, env)
    assert "reuse: none (code changed since run" in done.stdout
    assert _launches(env) == 2


def test_ignored_paths_do_not_invalidate_when_configured(repo: Path, env: dict[str, str]) -> None:
    (repo / ".test-gate.json").write_text(json.dumps({"ignore_paths": ["docs/"]}))
    _commit(repo, "config")
    _ensure(repo, env)
    (repo / "docs").mkdir()
    (repo / "docs/note.md").write_text("note\n")
    _commit(repo, "docs")
    assert "REUSED" in _ensure(repo, env).stdout


def test_docs_invalidate_without_configuration(repo: Path, env: dict[str, str]) -> None:
    _ensure(repo, env)
    (repo / "note.md").write_text("note\n")
    _commit(repo, "docs")
    _ensure(repo, env)
    assert _launches(env) == 2


def test_different_command_does_not_reuse(repo: Path, env: dict[str, str]) -> None:
    _ensure(repo, env)
    _gate(repo, env, "ensure", "--command", "bash ./runner.sh {results}")
    assert _launches(env) == 2


def test_force_ignores_reuse(repo: Path, env: dict[str, str]) -> None:
    _ensure(repo, env)
    _ensure(repo, env, "--force")
    assert _launches(env) == 2


def test_failing_results_are_reused_as_failing(repo: Path, env: dict[str, str]) -> None:
    Path(env["RESULT_XML"]).write_text(_xml(A="Failed", B="Passed"))
    assert _ensure(repo, env).returncode == 1
    second = _ensure(repo, env)
    assert second.returncode == 1 and "REUSED" in second.stdout
    assert _launches(env) == 1


def test_altered_artifact_is_not_reused(repo: Path, env: dict[str, str]) -> None:
    _ensure(repo, env)
    Path(_runs(repo)[0]["results_artifact"]).write_text(_xml(A="Passed"))
    assert "missing or altered" in _ensure(repo, env).stdout
    assert _launches(env) == 2


@pytest.mark.parametrize(
    "content",
    ["<test-run></test-run>", "not xml", _xml(A="Skipped")],
    ids=["zero-tests", "corrupt", "all-skipped"],
)
def test_results_proving_no_execution_are_not_green_or_reused(
    repo: Path, env: dict[str, str], content: str
) -> None:
    Path(env["RESULT_XML"]).write_text(content)
    assert _ensure(repo, env).returncode == 2
    _ensure(repo, env)
    assert _launches(env) == 2


def test_nonzero_exit_with_green_results_is_not_green(repo: Path, env: dict[str, str]) -> None:
    done = _gate(repo, env, "ensure", "--command", COMMAND + "; exit 7")
    assert done.returncode == 2
    assert "command-exit-7" in done.stdout


@pytest.mark.parametrize("kind", ["tracked", "untracked"])
def test_dirty_tree_refuses_and_names_the_path(repo: Path, env: dict[str, str], kind: str) -> None:
    (repo / ("code.txt" if kind == "tracked" else "new.txt")).write_text("dirty\n")
    done = _ensure(repo, env)
    assert done.returncode == 2
    assert "dirty-working-tree" in done.stdout
    assert ("code.txt" if kind == "tracked" else "new.txt") in done.stdout
    assert _launches(env) == 0


def test_dev_directory_does_not_dirty_the_tree(repo: Path, env: dict[str, str]) -> None:
    (repo / "dev").mkdir()
    (repo / "dev/plan.md").write_text("plan\n")
    assert _ensure(repo, env).returncode == 0


def test_held_unity_lock_refuses_but_abandoned_lock_does_not(repo: Path, env: dict[str, str], tmp_path: Path) -> None:
    (repo / ".gitignore").write_text("Temp/\n")
    (repo / "ProjectSettings").mkdir()
    (repo / "ProjectSettings/ProjectVersion.txt").write_text("6000\n")
    _commit(repo, "unity")
    (repo / "Temp").mkdir()
    lock = repo / "Temp/UnityLockfile"
    lock.write_text("")
    with lock.open("r"):
        held = _ensure(repo, env)
    assert held.returncode == 2 and "unity-project-locked" in held.stdout
    assert _launches(env) == 0
    assert _ensure(repo, env).returncode == 0


def test_recorded_duration_sets_limit_and_estimate(repo: Path, env: dict[str, str]) -> None:
    _ensure(repo, env)
    manifest = repo / ".git/test-gate/runs" / _runs(repo)[0]["run_id"] / "run.json"
    run = json.loads(manifest.read_text())
    run["duration_seconds"] = 400
    manifest.write_text(json.dumps(run))
    (repo / "code.txt").write_text("two\n")
    _commit(repo, "change")
    done = _ensure(repo, env)
    assert "limit: 600s (1.5 x slowest of 1 recorded runs)" in done.stdout
    assert "estimate: about 400s" in done.stdout


def test_first_run_states_no_estimate_and_timeout_is_not_executed(repo: Path, env: dict[str, str]) -> None:
    (repo / ".test-gate.json").write_text(json.dumps({"initial_timeout_seconds": 1}))
    _commit(repo, "config")
    done = _ensure(repo, env, extra={"SUITE_SLEEP": "30"})
    assert "limit: 1s (initial limit" in done.stdout
    assert "estimate: none" in done.stdout
    assert done.returncode == 2 and "run-timeout" in done.stdout
    # The next limit grows from the timed-out one, and that run stays unreusable.
    second = _ensure(repo, env)
    assert "limit: 2s" in second.stdout and "doubled" in second.stdout
    assert "REUSED" not in second.stdout


def test_wrapper_limit_is_confirmed_and_set(repo: Path, env: dict[str, str]) -> None:
    (repo / "wrap.sh").write_text(
        'L="${WRAP_LIMIT:-2400}"\necho "$L" > "$(dirname "$COUNT_FILE")/seen"\nbash runner.sh "$1"\n'
    )
    config = {"initial_timeout_seconds": 5400, "timeout_env": "WRAP_LIMIT", "timeout_source": "wrap.sh"}
    (repo / ".test-gate.json").write_text(json.dumps(config))
    _commit(repo, "wrap")
    done = _gate(repo, env, "ensure", "--command", "bash wrap.sh {results}")
    assert "wrap.sh reads WRAP_LIMIT (default 2400s), gate sets it to 5400s" in done.stdout
    assert (Path(env["COUNT_FILE"]).parent / "seen").read_text().strip() == "5400"


def test_unconfirmed_wrapper_limit_withholds_the_estimate(repo: Path, env: dict[str, str]) -> None:
    config = {"timeout_env": "WRAP_LIMIT", "timeout_source": "missing.sh"}
    (repo / ".test-gate.json").write_text(json.dumps(config))
    _commit(repo, "config")
    _ensure(repo, env)
    (repo / "code.txt").write_text("two\n")
    _commit(repo, "change")
    done = _ensure(repo, env)
    assert "could not confirm" in done.stdout
    assert "estimate: none" in done.stdout


def test_active_run_is_reattached_not_restarted(repo: Path, env: dict[str, str]) -> None:
    slow = {"SUITE_SLEEP": "3"}
    first = _ensure(repo, env, "--wait-seconds", "0.2", extra=slow)
    assert first.returncode == 3 and "repeat this exact command" in first.stdout
    assert _gate(repo, env, "status").returncode == 3
    second = _ensure(repo, env, "--wait-seconds", "30")
    assert "attached: run" in second.stdout and second.returncode == 0
    assert _launches(env) == 1


def test_run_survives_the_caller_being_killed(repo: Path, env: dict[str, str]) -> None:
    caller = subprocess.Popen(
        [sys.executable, str(GATE), "--repo", str(repo), "ensure", "--command", COMMAND],
        env={**env, "SUITE_SLEEP": "2"},
        stdout=subprocess.DEVNULL,
    )
    time.sleep(0.7)
    caller.send_signal(signal.SIGKILL)
    caller.wait()
    done = _ensure(repo, env, "--wait-seconds", "30")
    assert done.returncode == 0
    assert _launches(env) == 1


def test_dead_supervisor_marks_the_run_abandoned_and_unreusable(repo: Path, env: dict[str, str]) -> None:
    _ensure(repo, env, "--wait-seconds", "0.5", extra={"SUITE_SLEEP": "60"})
    run = _runs(repo)[0]
    os.killpg(run["child_pid"], signal.SIGKILL)
    os.kill(run["supervisor_pid"], signal.SIGKILL)
    time.sleep(0.3)
    assert _gate(repo, env, "status").returncode == 2
    assert _runs(repo)[0]["reason"] == "abandoned"
    assert _ensure(repo, env).returncode == 0
    assert _launches(env) == 2


# --- Triage ---


def _start_triage(repo: Path, env: dict[str, str], **results: str) -> None:
    Path(env["RESULT_XML"]).write_text(_xml(**results))
    assert _ensure(repo, env).returncode == 1
    assert _gate(repo, env, "triage", "open").returncode == 0


def _classify(repo: Path, env: dict[str, str], *tests: str, cause: str = "rc1", kind: str = "product-bug"):
    flags = [arg for test in tests for arg in ("--test", test)]
    return _gate(
        repo, env, "triage", "classify", "--root-cause", cause, "--class", kind, "--evidence", "why", *flags
    )


def _attempt(repo: Path, env: dict[str, str], cause: str = "rc1", **results: str):
    """Land a code change, rerun, and record the attempt against the root cause."""
    Path(env["RESULT_XML"]).write_text(_xml(**results))
    with (repo / "code.txt").open("a") as handle:
        handle.write("fix\n")
    _commit(repo, "attempt")
    _ensure(repo, env)
    return _gate(repo, env, "triage", "iterate", "--root-cause", cause, "--run", _runs(repo)[-1]["run_id"])


def _decision(done: subprocess.CompletedProcess[str]) -> str:
    return json.loads(done.stdout)["decision"]


def test_classification_rejects_unknown_class_and_non_failures(repo: Path, env: dict[str, str]) -> None:
    _start_triage(repo, env, A="Failed", B="Passed")
    assert _classify(repo, env, "A", kind="flaky").returncode == 2
    assert _classify(repo, env, "B").returncode == 2
    for kind in ("product-bug", "test-bug", "fixture-problem", "environment-issue"):
        assert _classify(repo, env, "A", kind=kind).returncode == 0


def test_repair_resolves(repo: Path, env: dict[str, str]) -> None:
    _start_triage(repo, env, A="Failed", B="Passed")
    _classify(repo, env, "A")
    done = _attempt(repo, env, A="Passed", B="Passed")
    assert _decision(done) == "resolved" and done.returncode == 0
    assert _gate(repo, env, "triage", "report").returncode == 0


def test_no_progress_stops_after_the_first_attempt(repo: Path, env: dict[str, str]) -> None:
    _start_triage(repo, env, A="Failed", B="Passed")
    _classify(repo, env, "A")
    done = _attempt(repo, env, A="Failed", B="Passed")
    assert _decision(done) == "stopped-no-progress" and done.returncode == 1
    closed = _attempt(repo, env, A="Passed", B="Passed")
    assert closed.returncode == 2 and "is closed" in closed.stdout


def test_reused_run_counts_as_no_progress(repo: Path, env: dict[str, str]) -> None:
    _start_triage(repo, env, A="Failed", B="Passed")
    _classify(repo, env, "A")
    done = _gate(repo, env, "triage", "iterate", "--root-cause", "rc1", "--run", _runs(repo)[-1]["run_id"])
    assert _decision(done) == "stopped-no-progress"


def test_third_attempt_is_the_limit(repo: Path, env: dict[str, str]) -> None:
    _start_triage(repo, env, A="Failed", B="Failed", C="Failed", D="Failed", E="Passed")
    _classify(repo, env, "A", "B", "C", "D")
    assert _decision(_attempt(repo, env, A="Passed", B="Failed", C="Failed", D="Failed", E="Passed")) == "continue"
    assert _decision(_attempt(repo, env, A="Passed", B="Passed", C="Failed", D="Failed", E="Passed")) == "continue"
    assert _decision(_attempt(repo, env, A="Passed", B="Passed", C="Passed", D="Failed", E="Passed")) == "stopped-limit"
    assert _gate(repo, env, "triage", "report").returncode == 1


@pytest.mark.parametrize(
    ("after", "problem"),
    [
        ({"A": "Skipped", "B": "Passed"}, "test now skipped: A"),
        ({"B": "Passed"}, "test no longer present: A"),
    ],
    ids=["skipped", "deleted"],
)
def test_skipping_or_deleting_a_test_never_counts_as_fixed(
    repo: Path, env: dict[str, str], after: dict[str, str], problem: str
) -> None:
    _start_triage(repo, env, A="Failed", B="Passed")
    _classify(repo, env, "A")
    done = _attempt(repo, env, **after)
    assert _decision(done) == "stopped-integrity"
    report = _gate(repo, env, "triage", "report")
    assert f"REPORT TO USER: {problem}" in report.stdout and report.returncode == 1


def test_deleting_an_unrelated_test_is_reported(repo: Path, env: dict[str, str]) -> None:
    _start_triage(repo, env, A="Failed", B="Passed")
    _classify(repo, env, "A")
    assert _decision(_attempt(repo, env, A="Passed")) == "stopped-integrity"


def test_new_failure_is_not_progress(repo: Path, env: dict[str, str]) -> None:
    _start_triage(repo, env, A="Failed", B="Passed")
    _classify(repo, env, "A")
    assert _decision(_attempt(repo, env, A="Passed", B="Failed")) == "stopped-no-progress"


def test_not_executed_run_uses_no_iteration(repo: Path, env: dict[str, str]) -> None:
    _start_triage(repo, env, A="Failed", B="Passed")
    _classify(repo, env, "A")
    done = _attempt(repo, env)  # Empty results: nothing executed.
    assert done.returncode == 2 and "did not execute" in done.stdout
    assert _decision(_attempt(repo, env, A="Passed", B="Passed")) == "resolved"


def test_close_reports_tests_lost_outside_the_named_rerun(repo: Path, env: dict[str, str]) -> None:
    _start_triage(repo, env, A="Failed", B="Passed", C="Skipped")
    Path(env["RESULT_XML"]).write_text(_xml(A="Passed", D="Skipped", E="Skipped"))
    (repo / "code.txt").write_text("two\n")
    _commit(repo, "fix")
    _ensure(repo, env)
    closed = _gate(repo, env, "triage", "close", "--run", _runs(repo)[-1]["run_id"])
    assert closed.returncode == 1 and "skips rose from 1 to 2" in closed.stdout


def test_close_accepts_a_green_full_run(repo: Path, env: dict[str, str]) -> None:
    _start_triage(repo, env, A="Failed", B="Passed")
    Path(env["RESULT_XML"]).write_text(_xml(A="Passed", B="Passed"))
    (repo / "code.txt").write_text("two\n")
    _commit(repo, "fix")
    _ensure(repo, env)
    closed = _gate(repo, env, "triage", "close", "--run", _runs(repo)[-1]["run_id"])
    assert closed.returncode == 0


def test_junit_results_are_supported(repo: Path, env: dict[str, str]) -> None:
    Path(env["RESULT_XML"]).write_text(
        '<testsuites><testsuite><testcase classname="m" name="ok"/>'
        '<testcase classname="m" name="bad"><failure message="boom"/></testcase>'
        '<testcase classname="m" name="off"><skipped/></testcase></testsuite></testsuites>'
    )
    done = _ensure(repo, env)
    assert done.returncode == 1 and "total=3 passed=1 failed=1 skipped=1" in done.stdout
    opened = json.loads(_gate(repo, env, "triage", "open").stdout)
    assert opened["failures"] == {"m.bad": "boom"}


SCOPED_CONFIG = {
    "test_only_paths": ["tests/"],
    "full_rerun_paths": ["tests/shared/"],
    "scoped_always": ["Policy"],
}


def _scoped_setup(repo: Path, env: dict[str, str], config: dict | None = SCOPED_CONFIG) -> None:
    """Fail a full run with test A failing, over a repo that declares its test-only paths."""
    (repo / "tests/shared").mkdir(parents=True)
    (repo / "tests/a_test.txt").write_text("a\n")
    (repo / "tests/shared/harness.txt").write_text("h\n")
    if config is not None:
        (repo / ".test-gate.json").write_text(json.dumps(config))
    _commit(repo, "tests")
    _start_triage(repo, env, A="Failed", B="Passed", **{"Policy.Guard": "Passed"})


def _scoped_close(repo: Path, env: dict[str, str], change, **results: str):
    """Land one repair, run a scoped rerun, and close the gate against it."""
    change(repo)
    _commit(repo, "repair")
    Path(env["RESULT_XML"]).write_text(_xml(**results))
    _ensure(repo, env, "--scope", "rerun")
    return _gate(repo, env, "triage", "close", "--scoped", "--run", _runs(repo)[-1]["run_id"])


def _edit_test(repo: Path) -> None:
    (repo / "tests/a_test.txt").write_text("fixed\n")


GREEN_SCOPED = {"A": "Passed", "Policy.Guard": "Passed"}


def test_scoped_close_accepts_a_test_only_repair(repo: Path, env: dict[str, str]) -> None:
    _scoped_setup(repo, env)
    closed = _scoped_close(repo, env, _edit_test, **GREEN_SCOPED)
    assert closed.returncode == 0, closed.stdout
    assert "every repair touched test code only" in closed.stdout


@pytest.mark.parametrize(
    ("change", "problem"),
    [
        (lambda r: (r / "code.txt").write_text("prod fix\n"), "repair touched non-test path code.txt"),
        (lambda r: (r / "tests/shared/harness.txt").write_text("x\n"), "shared test code tests/shared/harness.txt"),
        (lambda r: (r / "tests/a_test.txt").unlink(), "repair deleted test file tests/a_test.txt"),
    ],
)
def test_scoped_close_refuses_a_repair_outside_test_only_code(
    repo: Path, env: dict[str, str], change, problem: str
) -> None:
    _scoped_setup(repo, env)
    closed = _scoped_close(repo, env, change, **GREEN_SCOPED)
    assert closed.returncode == 1 and problem in closed.stdout


def test_scoped_close_refuses_a_run_missing_a_failing_test(repo: Path, env: dict[str, str]) -> None:
    _scoped_setup(repo, env)
    closed = _scoped_close(repo, env, _edit_test, **{"Policy.Guard": "Passed", "B": "Passed"})
    assert closed.returncode == 1 and "did not run failing test A" in closed.stdout


def test_scoped_close_refuses_a_skipped_failing_test(repo: Path, env: dict[str, str]) -> None:
    _scoped_setup(repo, env)
    closed = _scoped_close(repo, env, _edit_test, A="Skipped", **{"Policy.Guard": "Passed"})
    assert closed.returncode == 1 and "failing test now skipped: A" in closed.stdout


def test_scoped_close_refuses_a_run_missing_a_required_suite(repo: Path, env: dict[str, str]) -> None:
    _scoped_setup(repo, env)
    closed = _scoped_close(repo, env, _edit_test, A="Passed")
    assert closed.returncode == 1 and "did not include required suite Policy" in closed.stdout


def test_scoped_close_refuses_a_still_failing_run(repo: Path, env: dict[str, str]) -> None:
    _scoped_setup(repo, env)
    closed = _scoped_close(repo, env, _edit_test, A="Failed", **{"Policy.Guard": "Passed"})
    assert closed.returncode == 1 and "still failing: A" in closed.stdout


def test_scoped_close_refuses_when_no_repair_landed(repo: Path, env: dict[str, str]) -> None:
    _scoped_setup(repo, env)
    Path(env["RESULT_XML"]).write_text(_xml(**GREEN_SCOPED))
    _ensure(repo, env, "--scope", "rerun")
    closed = _gate(repo, env, "triage", "close", "--scoped", "--run", _runs(repo)[-1]["run_id"])
    assert closed.returncode == 1 and "no repair landed" in closed.stdout


def test_scoped_close_is_refused_without_test_only_paths(repo: Path, env: dict[str, str]) -> None:
    _scoped_setup(repo, env, config=None)
    closed = _scoped_close(repo, env, _edit_test, **GREEN_SCOPED)
    assert closed.returncode == 1 and "no test_only_paths" in closed.stdout


def test_unscoped_close_still_refuses_a_scoped_run(repo: Path, env: dict[str, str]) -> None:
    _scoped_setup(repo, env)
    _edit_test(repo)
    _commit(repo, "repair")
    Path(env["RESULT_XML"]).write_text(_xml(**GREEN_SCOPED))
    _ensure(repo, env, "--scope", "rerun")
    closed = _gate(repo, env, "triage", "close", "--run", _runs(repo)[-1]["run_id"])
    assert closed.returncode == 2 and "is not an executed full run" in closed.stdout
