#!/usr/bin/env python3
"""Run a repository's test suite at most once per code state.

State lives in <git-common-dir>/test-gate/, so it never dirties the working
tree and every worktree of a repository shares it. Stdlib only. POSIX only.

Exit status: 0 green, 1 failing or triage stopped, 2 not executed or refused,
3 run still active (repeat the same command to reattach).
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import logging
import math
import os
import re
import secrets
import shlex
import signal
import statistics
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger("test_gate")

CONFIG_NAME = ".test-gate.json"
CLEAN = "clean"
ALWAYS_IGNORED = ("dev/",)  # Pipeline working state. Tests never target it.
HISTORY_SIZE = 5
TIMEOUT_MULTIPLIER = 1.5
MIN_TIMEOUT_SECONDS = 300
DEFAULT_INITIAL_TIMEOUT_SECONDS = 3600
WRAPPER_GRACE_SECONDS = 60  # The wrapper's own limit fires first and names its reason.
START_GRACE_SECONDS = 15
RUNS_KEPT = 20
MAX_ITERATIONS = 3
CLASSES = ("product-bug", "test-bug", "fixture-problem", "environment-issue")

EXIT_GREEN, EXIT_FAILING, EXIT_NOT_EXECUTED, EXIT_RUNNING = 0, 1, 2, 3
GREEN, FAILING, NOT_EXECUTED = "executed-green", "executed-failing", "not-executed"


class Refusal(Exception):
    """The gate cannot proceed. The message is the user-facing reason."""


def _git(repo: Path, *args: str) -> str:
    done = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    if done.returncode != 0:
        raise Refusal(f"not-executed: git {' '.join(args)} failed: {done.stderr.strip()}")
    return done.stdout


def _store(repo: Path) -> Path:
    common = Path(_git(repo, "rev-parse", "--git-common-dir").strip())
    store = (common if common.is_absolute() else repo / common).resolve() / "test-gate"
    (store / "runs").mkdir(parents=True, exist_ok=True)
    (store / "triage").mkdir(exist_ok=True)
    return store


def _write_json(path: Path, data: dict[str, Any]) -> None:
    temporary = path.with_name(f"{path.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# --- Code state ---


def _matches(path: str, patterns: list[str]) -> bool:
    for pattern in patterns:
        if pattern.endswith("/") and path.startswith(pattern):
            return True
        if fnmatch.fnmatch(path, pattern):
            return True
    return False


def _is_ignored(path: str, patterns: list[str]) -> bool:
    return _matches(path, [*ALWAYS_IGNORED, *patterns])


def code_state(repo: Path, ignore: list[str]) -> dict[str, Any]:
    """Describe the code by content, so a squash merge of an identical tree still matches."""
    digest = hashlib.sha256()
    for entry in sorted(_git(repo, "ls-tree", "-r", "-z", "HEAD").split("\0")):
        if entry and not _is_ignored(entry.split("\t", 1)[1], ignore):
            digest.update(entry.encode())
    changed = _git(repo, "diff", "--name-only", "-z", "HEAD").split("\0")
    untracked = _git(repo, "ls-files", "-o", "--exclude-standard", "-z").split("\0")
    dirty = sorted({p for p in (*changed, *untracked) if p and not _is_ignored(p, ignore)})
    dirty_hash = CLEAN
    if dirty:
        dirty_digest = hashlib.sha256()
        for path in dirty:
            target = repo / path
            content = target.read_bytes() if target.is_file() else b"<absent-or-directory>"
            dirty_digest.update(path.encode() + b"\0" + content + b"\0")
        dirty_hash = dirty_digest.hexdigest()
    return {
        "commit": _git(repo, "rev-parse", "HEAD").strip(),
        "tree_fingerprint": digest.hexdigest(),
        "dirty_hash": dirty_hash,
        "dirty_paths": dirty,
    }


def _held_locks(repo: Path, config: dict[str, Any]) -> list[str]:
    paths = config.get("lock_paths")
    if paths is None:
        # No declared runner: Unity runs in this checkout, so its Editor lock applies.
        candidates = [repo, *(p for p in repo.iterdir() if p.is_dir() and not p.name.startswith("."))]
        paths = [
            str(c / "Temp" / "UnityLockfile") for c in candidates if (c / "ProjectSettings").is_dir()
        ]
    held = []
    for raw in paths:
        lock = (repo / raw).resolve()
        if not lock.exists():
            continue
        try:
            has_holder = subprocess.run(["lsof", "--", str(lock)], capture_output=True).returncode == 0
        except FileNotFoundError:
            logger.warning("lsof is unavailable, treating %s as held", lock)
            has_holder = True
        if has_holder:
            held.append(str(lock))
        else:
            logger.info("lock %s has no live holder, treating it as abandoned", lock)
    return held


# --- Results ---


def parse_results(path: Path) -> dict[str, Any] | None:
    """Read NUnit or JUnit XML. Return None when the file proves no execution."""
    try:
        root = ET.parse(path).getroot()
    except (OSError, ET.ParseError) as error:
        logger.warning("cannot read results %s: %s", path, error)
        return None
    cases: dict[str, str] = {}
    messages: dict[str, str] = {}
    if root.tag == "test-run" or root.find(".//test-case") is not None:
        for case in root.iter("test-case"):
            name = case.get("fullname") or case.get("name") or "?"
            result = case.get("result", "")
            cases[name] = {"Passed": "passed", "Failed": "failed"}.get(result, "skipped")
            if result == "Failed":
                messages[name] = (case.findtext("failure/message") or "").strip()[:500]
    else:
        for case in root.iter("testcase"):
            name = f"{case.get('classname', '')}.{case.get('name', '?')}".lstrip(".")
            problem = case.find("failure")
            problem = problem if problem is not None else case.find("error")
            if problem is not None:
                cases[name] = "failed"
                messages[name] = (problem.get("message") or problem.text or "").strip()[:500]
            else:
                cases[name] = "skipped" if case.find("skipped") is not None else "passed"
    values = list(cases.values())
    counts = {
        "total": len(values),
        "passed": values.count("passed"),
        "failed": values.count("failed"),
        "skipped": values.count("skipped"),
    }
    if counts["passed"] + counts["failed"] == 0:
        return None
    # A suite-level failure such as a setup error can fail the run with no failed case.
    suite_failed = root.get("result", "").startswith("Failed") and counts["failed"] == 0
    return {"counts": counts, "cases": cases, "messages": messages, "suite_failed": suite_failed}


# --- Time budget ---


def time_budget(config: dict[str, Any], history: list[dict[str, Any]], repo: Path) -> dict[str, Any]:
    """Derive the limit from recorded durations and confirm any wrapper honors it."""
    completed = [r for r in history if r["status"] in (GREEN, FAILING)][-HISTORY_SIZE:]
    durations = [r["duration_seconds"] for r in completed]
    if durations:
        limit = max(MIN_TIMEOUT_SECONDS, math.ceil(max(durations) * TIMEOUT_MULTIPLIER))
        basis = f"{TIMEOUT_MULTIPLIER} x slowest of {len(durations)} recorded runs"
    else:
        limit = int(config.get("initial_timeout_seconds", DEFAULT_INITIAL_TIMEOUT_SECONDS))
        basis = "initial limit, no recorded runs"
    last_time = max((r["finished_at"] for r in completed), default="")
    for run in history:
        if run.get("reason") == "run-timeout" and run["finished_at"] > last_time:
            limit = max(limit, run["limit_seconds"] * 2)
            basis += "; doubled after a timeout with no later completed run"

    env_name, source = config.get("timeout_env"), config.get("timeout_source")
    confirmed, wrapper_note = True, "no wrapper limit declared, gate limit applies"
    if env_name:
        text = ""
        if source and (repo / source).is_file():
            text = (repo / source).read_text(encoding="utf-8", errors="replace")
        match = re.search(rf"{re.escape(env_name)}:-(\d+)", text)
        confirmed = env_name in text
        if confirmed:
            default = match.group(1) if match else "none"
            wrapper_note = f"{source} reads {env_name} (default {default}s), gate sets it to {limit}s"
        else:
            wrapper_note = f"could not confirm that {source} reads {env_name}"
    estimate = round(statistics.median(durations)) if durations and confirmed else None
    return {
        "limit_seconds": limit,
        "basis": basis,
        "limit_confirmed": confirmed,
        "wrapper_note": wrapper_note,
        "estimate_seconds": estimate,
    }


def _budget_lines(budget: dict[str, Any]) -> list[str]:
    lines = [
        f"limit: {budget['limit_seconds']}s ({budget['basis']})",
        f"limit-check: {budget['wrapper_note']}",
    ]
    if budget["estimate_seconds"] is not None:
        lines.append(f"estimate: about {budget['estimate_seconds']}s (median of recorded runs)")
    else:
        lines.append("estimate: none, state no time estimate")
    return lines


# --- Runs ---


def _all_runs(store: Path) -> list[dict[str, Any]]:
    runs = []
    for directory in sorted((store / "runs").iterdir()):
        try:
            runs.append(_read_json(directory / "run.json"))
        except (OSError, ValueError) as error:
            logger.warning("skipping unreadable run %s: %s", directory, error)
    return runs


def _process_start(pid: int) -> str:
    done = subprocess.run(["ps", "-o", "lstart=", "-p", str(pid)], capture_output=True, text=True)
    return done.stdout.strip()


def _alive(pid: int | None, started: str | None) -> bool:
    return bool(pid) and _process_start(pid) == started


def _is_active(run: dict[str, Any]) -> bool:
    if run["status"] != "running":
        return False
    if run.get("supervisor_pid") is None:
        return time.time() - run["started_epoch"] < START_GRACE_SECONDS
    return _alive(run["supervisor_pid"], run["supervisor_started"]) or _alive(
        run.get("child_pid"), run.get("child_started")
    )


def _active_run(store: Path) -> dict[str, Any] | None:
    for run in _all_runs(store):
        if run["status"] == "running":
            if _is_active(run):
                return run
            logger.warning("run %s lost its processes, marking it abandoned", run["run_id"])
            run.update(status=NOT_EXECUTED, reason="abandoned", finished_at=_now())
            _write_json(store / "runs" / run["run_id"] / "run.json", run)
    (store / "active.lock").unlink(missing_ok=True)
    return None


def _prune(store: Path) -> None:
    finished = [r for r in _all_runs(store) if r["status"] != "running"]
    for run in finished[:-RUNS_KEPT]:
        directory = store / "runs" / run["run_id"]
        for child in directory.iterdir():
            child.unlink()
        directory.rmdir()
        logger.info("pruned run %s", run["run_id"])


def find_reusable(
    store: Path, scope: str, template: str, state: dict[str, Any]
) -> tuple[dict[str, Any] | None, str]:
    """Return the newest trustworthy run for this code state, and why others did not match."""
    runs = [r for r in _all_runs(store) if r["scope"] == scope and r["command_template"] == template]
    if not runs:
        return None, "no recorded run for this scope and command"
    why = "no executed run"
    for run in reversed(runs):
        if run["status"] not in (GREEN, FAILING):
            continue
        if run["tree_fingerprint"] != state["tree_fingerprint"]:
            why = f"code changed since run {run['run_id']} at commit {run['commit']}"
            return None, why
        if run["dirty_hash"] != state["dirty_hash"]:
            return None, f"working tree differs from run {run['run_id']}"
        if run.get("code_changed_during_run"):
            return None, f"code changed during run {run['run_id']}"
        parsed = parse_results(Path(run["results_artifact"]))
        if parsed is None or parsed["counts"] != run["counts"]:
            return None, f"results artifact of run {run['run_id']} is missing or altered"
        return run, "match"
    return None, why


def _start(
    repo: Path, store: Path, scope: str, template: str, config: dict[str, Any], state: dict[str, Any]
) -> dict[str, Any]:
    lock = store / "active.lock"
    run_id = f"{time.time_ns():020d}-{secrets.token_hex(2)}"
    try:
        os.close(os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY))
    except FileExistsError as error:
        raise Refusal("not-executed: another gate process is starting a run, retry") from error
    history = [
        r for r in _all_runs(store)
        if r["scope"] == scope and r["command_template"] == template and r["status"] != "running"
    ]
    budget = time_budget(config, history, repo)
    run_dir = store / "runs" / run_id
    run_dir.mkdir()
    results, log = run_dir / "results.xml", run_dir / "runner.log"
    command = template
    for key, value in (("{results}", str(results)), ("{log}", str(log)), ("{sha}", state["commit"])):
        command = command.replace(key, shlex.quote(value))
    run = {
        "run_id": run_id,
        "status": "running",
        "scope": scope,
        "command_template": template,
        "command": command,
        "repo": str(repo),
        "ignore_paths": config.get("ignore_paths", []),
        "commit": state["commit"],
        "tree_fingerprint": state["tree_fingerprint"],
        "dirty_hash": state["dirty_hash"],
        "timestamp": _now(),
        "started_epoch": time.time(),
        "results_artifact": str(results),
        "timeout_env": config.get("timeout_env"),
        **budget,
    }
    _write_json(run_dir / "run.json", run)
    # A new session detaches the run from the caller, so a lost shell cannot reap it.
    subprocess.Popen(
        [sys.executable, str(Path(__file__).resolve()), "_supervise", str(run_dir)],
        start_new_session=True,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        cwd=repo,
    )
    logger.info("started run %s: %s", run_id, command)
    return run


def supervise(run_dir: Path) -> None:
    """Own one run from detached start to its final manifest."""
    manifest = run_dir / "run.json"
    run = _read_json(manifest)
    logging.basicConfig(filename=run_dir / "supervisor.log", level=logging.INFO, force=True)
    run.update(supervisor_pid=os.getpid(), supervisor_started=_process_start(os.getpid()))
    _write_json(manifest, run)

    env = dict(os.environ)
    if run["timeout_env"]:
        env[run["timeout_env"]] = str(run["limit_seconds"])
    deadline = time.monotonic() + run["limit_seconds"] + (WRAPPER_GRACE_SECONDS if run["timeout_env"] else 0)
    started = time.monotonic()
    output_path = run_dir / "output.log"
    timed_out = False
    with output_path.open("wb") as output:
        child = subprocess.Popen(
            run["command"], shell=True, cwd=run["repo"], env=env,
            stdin=subprocess.DEVNULL, stdout=output, stderr=subprocess.STDOUT, start_new_session=True,
        )
        run.update(child_pid=child.pid, child_started=_process_start(child.pid))
        _write_json(manifest, run)
        while child.poll() is None:
            if time.monotonic() > deadline:
                timed_out = True
                logger.error("run %s hit the %ss limit", run["run_id"], run["limit_seconds"])
                _kill_group(child)
                break
            time.sleep(0.2)
    duration = round(time.monotonic() - started, 1)

    text = output_path.read_text(encoding="utf-8", errors="replace")
    reasons = re.findall(r"not-executed: (\S+)", text)
    parsed = None if timed_out else parse_results(Path(run["results_artifact"]))
    run.update(duration_seconds=duration, exit_code=child.returncode, finished_at=_now())
    run.update(counts={"total": 0, "passed": 0, "failed": 0, "skipped": 0})
    if timed_out or "run-timeout" in reasons:
        run.update(status=NOT_EXECUTED, reason="run-timeout")
    elif parsed is None:
        run.update(status=NOT_EXECUTED, reason=reasons[-1] if reasons else "no-results")
    else:
        failing = parsed["counts"]["failed"] > 0 or parsed["suite_failed"]
        run.update(counts=parsed["counts"], status=FAILING if failing else GREEN)
        if not failing and child.returncode != 0:
            reason = reasons[-1] if reasons else f"command-exit-{child.returncode}-with-green-results"
            run.update(status=NOT_EXECUTED, reason=reason)
    after = code_state(Path(run["repo"]), run["ignore_paths"])
    run["code_changed_during_run"] = (
        after["tree_fingerprint"] != run["tree_fingerprint"] or after["dirty_hash"] != run["dirty_hash"]
    )
    _write_json(manifest, run)
    logger.info("run %s finished: %s %s", run["run_id"], run["status"], run["counts"])
    (run_dir.parent.parent / "active.lock").unlink(missing_ok=True)
    _prune(run_dir.parent.parent)


def _kill_group(child: subprocess.Popen[bytes]) -> None:
    for signum, wait in ((signal.SIGTERM, 10), (signal.SIGKILL, 10)):
        try:
            os.killpg(child.pid, signum)
        except ProcessLookupError:
            return
        try:
            child.wait(timeout=wait)
            return
        except subprocess.TimeoutExpired:
            logger.warning("process group %s survived signal %s", child.pid, signum)


# --- Commands ---


def _report(run: dict[str, Any], reused: bool) -> int:
    print(f"status: {run['status']}" + (f" ({run['reason']})" if run.get("reason") else ""))
    print(f"run: {run['run_id']}")
    if reused:
        print(
            f"evidence: REUSED from run {run['run_id']} at {run['timestamp']}, "
            f"commit {run['commit']}. The code state matches, so no tests ran now."
        )
    elif run["status"] in (GREEN, FAILING):
        print("evidence: this run executed the suite")
    else:
        print("evidence: none, the suite did not produce usable results")
    print(f"scope: {run['scope']}")
    print(f"command: {run['command']}")
    print(f"commit: {run['commit']}")
    print(f"tree-fingerprint: {run['tree_fingerprint']}")
    print(f"dirty-hash: {run['dirty_hash']}")
    print(f"timestamp: {run['timestamp']}")
    print(f"duration: {run.get('duration_seconds')}s")
    print(f"results-artifact: {run['results_artifact']}")
    counts = run.get("counts", {})
    print(
        f"total={counts.get('total')} passed={counts.get('passed')} "
        f"failed={counts.get('failed')} skipped={counts.get('skipped')}"
    )
    if run.get("code_changed_during_run"):
        print("warning: code changed during this run, so later runs will not reuse it")
    return {GREEN: EXIT_GREEN, FAILING: EXIT_FAILING}.get(run["status"], EXIT_NOT_EXECUTED)


def _await(store: Path, run: dict[str, Any], wait_seconds: float) -> int:
    manifest = store / "runs" / run["run_id"] / "run.json"
    deadline = time.monotonic() + wait_seconds
    while True:
        current = _read_json(manifest)
        if current["status"] != "running":
            return _report(current, reused=False)
        if not _is_active(current):
            _active_run(store)
            return _report(_read_json(manifest), reused=False)
        if time.monotonic() >= deadline:
            print(f"status: running\nrun: {run['run_id']}")
            print("next: repeat this exact command to reattach. Do not start another run.")
            return EXIT_RUNNING
        time.sleep(min(1.0, max(0.05, wait_seconds / 20)))


def _load_config(repo: Path) -> dict[str, Any]:
    path = repo / CONFIG_NAME
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except ValueError as error:
        raise Refusal(f"not-executed: {path} is not valid JSON: {error}") from error


def _scope_config(config: dict[str, Any], scope: str, command: str | None) -> dict[str, Any]:
    merged = {**config, **config.get("scopes", {}).get(scope, {})}
    merged.pop("scopes", None)
    if command:
        merged["command"] = command
    if not merged.get("command"):
        raise Refusal(f"not-executed: no command for scope {scope}. Pass --command or add {CONFIG_NAME}.")
    if "{results}" not in merged["command"]:
        raise Refusal("not-executed: the command must write NUnit or JUnit XML to the {results} placeholder")
    return merged


def cmd_ensure(args: argparse.Namespace, repo: Path, store: Path) -> int:
    active = _active_run(store)
    config = _scope_config(_load_config(repo), args.scope, args.command)
    template = config["command"]
    state = code_state(repo, config.get("ignore_paths", []))
    if active is not None:
        same = (
            active["scope"] == args.scope
            and active["command_template"] == template
            and active["tree_fingerprint"] == state["tree_fingerprint"]
        )
        if not same:
            raise Refusal(
                f"not-executed: active-run. Run {active['run_id']} is testing scope {active['scope']} "
                f"at commit {active['commit']}. Wait for it before starting another run."
            )
        print(f"attached: run {active['run_id']} is already active for this code state")
        for line in _budget_lines(active):
            print(line)
        return _await(store, active, args.wait_seconds)

    if state["dirty_hash"] != CLEAN:
        shown = ", ".join(state["dirty_paths"][:20])
        raise Refusal(
            f"not-executed: dirty-working-tree. Commit or remove these paths, then rerun: {shown}"
        )
    if args.force:
        print("reuse: skipped by --force")
    else:
        reusable, why = find_reusable(store, args.scope, template, state)
        if reusable is not None:
            return _report(reusable, reused=True)
        print(f"reuse: none ({why})")
    held = _held_locks(repo, config)
    if held:
        raise Refusal(
            f"not-executed: unity-project-locked. A live process holds {', '.join(held)}. "
            "Close that Editor or wait for its run to end."
        )
    run = _start(repo, store, args.scope, template, config, state)
    for line in _budget_lines(run):
        print(line)
    return _await(store, run, args.wait_seconds)


def cmd_status(args: argparse.Namespace, repo: Path, store: Path) -> int:
    active = _active_run(store)
    if active is not None:
        print(f"active: run {active['run_id']} scope {active['scope']} commit {active['commit']}")
        for line in _budget_lines(active):
            print(line)
        return EXIT_RUNNING
    runs = _all_runs(store)
    if not runs:
        print("no recorded runs")
        return EXIT_NOT_EXECUTED
    print("active: none\nlatest:")
    return _report(runs[-1], reused=False)


# --- Triage ---


def _ledger_path(store: Path, baseline: str | None) -> Path:
    if baseline:
        return store / "triage" / f"{baseline}.json"
    ledgers = sorted((store / "triage").glob("*.json"))
    if not ledgers:
        raise Refusal("no triage ledger. Run: triage open")
    return ledgers[-1]


def _load_run(store: Path, run_id: str) -> dict[str, Any]:
    path = store / "runs" / run_id / "run.json"
    if not path.is_file():
        raise Refusal(f"unknown run {run_id}")
    return _read_json(path)


def cmd_triage_open(args: argparse.Namespace, repo: Path, store: Path) -> int:
    if args.run:
        run = _load_run(store, args.run)
    else:
        failing = [r for r in _all_runs(store) if r["status"] == FAILING]
        if not failing:
            raise Refusal("no failing run to triage")
        run = failing[-1]
    parsed = parse_results(Path(run["results_artifact"]))
    if parsed is None or run["status"] != FAILING:
        raise Refusal(f"run {run['run_id']} has no failing results to triage")
    path = store / "triage" / f"{run['run_id']}.json"
    if path.exists():
        print(path.read_text(encoding="utf-8"))
        return EXIT_GREEN
    failures = {n: parsed["messages"].get(n, "") for n, r in parsed["cases"].items() if r == "failed"}
    ledger = {
        "baseline_run": run["run_id"],
        "baseline_scope": run["scope"],
        "baseline_counts": run["counts"],
        "failures": failures,
        "root_causes": {},
    }
    _write_json(path, ledger)
    print(json.dumps(ledger, indent=2, sort_keys=True))
    return EXIT_GREEN


def cmd_triage_classify(args: argparse.Namespace, repo: Path, store: Path) -> int:
    path = _ledger_path(store, args.baseline)
    ledger = _read_json(path)
    unknown = [t for t in args.test if t not in ledger["failures"]]
    if unknown:
        raise Refusal(f"not failures in baseline run: {', '.join(unknown)}")
    existing = ledger["root_causes"].get(args.root_cause)
    if existing and existing["iterations"]:
        raise Refusal(f"root cause {args.root_cause} already has iterations and cannot change")
    for other, cause in ledger["root_causes"].items():
        overlap = set(cause["tests"]) & set(args.test)
        if other != args.root_cause and overlap:
            raise Refusal(f"already classified under {other}: {', '.join(sorted(overlap))}")
    ledger["root_causes"][args.root_cause] = {
        "classification": args.classification,
        "evidence": args.evidence,
        "tests": sorted(args.test),
        "iterations": [],
        "decision": "open",
    }
    _write_json(path, ledger)
    print(f"classified {len(args.test)} tests under {args.root_cause} as {args.classification}")
    return EXIT_GREEN


def decide_iteration(ledger: dict[str, Any], cause: dict[str, Any], run: dict[str, Any], parsed: dict[str, Any]) -> dict[str, Any]:
    """Judge one repair attempt from results alone, not from the repairer's report."""
    cases = parsed["cases"]
    remaining = sorted(t for t in cause["tests"] if cases.get(t) == "failed")
    vanished = sorted(t for t in cause["tests"] if t not in cases)
    skipped = sorted(t for t in cause["tests"] if cases.get(t) == "skipped")
    integrity = [f"test no longer present: {t}" for t in vanished]
    integrity += [f"test now skipped: {t}" for t in skipped]
    new_failures: list[str] = []
    if run["scope"] == ledger["baseline_scope"]:
        base, counts = ledger["baseline_counts"], parsed["counts"]
        if counts["total"] < base["total"]:
            integrity.append(f"suite shrank from {base['total']} to {counts['total']} tests")
        if counts["skipped"] > base["skipped"]:
            integrity.append(f"skips rose from {base['skipped']} to {counts['skipped']}")
        new_failures = sorted(
            n for n, r in cases.items() if r == "failed" and n not in ledger["failures"]
        )
    previous = cause["iterations"][-1]["remaining"] if cause["iterations"] else cause["tests"]
    number = len(cause["iterations"]) + 1
    if integrity:
        decision = "stopped-integrity"
    elif new_failures or (remaining and len(remaining) >= len(previous)):
        decision = "stopped-no-progress"
    elif not remaining:
        decision = "resolved"
    elif number >= MAX_ITERATIONS:
        decision = "stopped-limit"
    else:
        decision = "continue"
    return {
        "iteration": number,
        "run": run["run_id"],
        "remaining": remaining,
        "new_failures": new_failures,
        "integrity": integrity,
        "decision": decision,
    }


def cmd_triage_iterate(args: argparse.Namespace, repo: Path, store: Path) -> int:
    path = _ledger_path(store, args.baseline)
    ledger = _read_json(path)
    cause = ledger["root_causes"].get(args.root_cause)
    if cause is None:
        raise Refusal(f"unknown root cause {args.root_cause}. Classify it first.")
    if cause["decision"] != "open":
        raise Refusal(f"root cause {args.root_cause} is closed: {cause['decision']}")
    run = _load_run(store, args.run)
    parsed = parse_results(Path(run["results_artifact"]))
    if run["status"] not in (GREEN, FAILING) or parsed is None:
        raise Refusal(f"run {args.run} did not execute, so it proves nothing about this repair")
    outcome = decide_iteration(ledger, cause, run, parsed)
    cause["iterations"].append(outcome)
    if outcome["decision"] != "continue":
        cause["decision"] = outcome["decision"]
    _write_json(path, ledger)
    print(json.dumps(outcome, indent=2, sort_keys=True))
    return EXIT_FAILING if outcome["decision"].startswith("stopped") else EXIT_GREEN


def _scoped_close_problems(
    repo: Path, config: dict[str, Any], ledger: dict[str, Any], baseline: dict[str, Any],
    run: dict[str, Any], parsed: dict[str, Any],
) -> list[str]:
    """A scoped run closes a failed full run only when every repair touched test code alone."""
    test_only = config.get("test_only_paths") or []
    if not test_only:
        return [f"no test_only_paths in {CONFIG_NAME}, so no repair qualifies for a scoped close"]
    full_rerun = config.get("full_rerun_paths") or []
    ignored = config.get("ignore_paths") or []
    diff = _git(repo, "diff", "--name-status", "--no-renames", baseline["commit"], run["commit"])
    changes = [line.split("\t", 1) for line in diff.splitlines() if line.strip()]
    logger.info("scoped close: %d paths changed between %s and %s", len(changes), baseline["commit"], run["commit"])
    problems = []
    if not any(not _is_ignored(path, ignored) for _, path in changes):
        problems.append("no repair landed since the failing run; a pass proves nothing")
    for status, path in changes:
        if _is_ignored(path, ignored):
            continue
        if not _matches(path, test_only):
            problems.append(f"repair touched non-test path {path}; run the full gate")
        elif _matches(path, full_rerun):
            problems.append(f"repair touched shared test code {path}; run the full gate")
        elif status == "D":
            problems.append(f"repair deleted test file {path}; run the full gate")
    problems += [f"scoped run did not run failing test {n}" for n in ledger["failures"] if n not in parsed["cases"]]
    problems += [f"failing test now skipped: {n}" for n in ledger["failures"] if parsed["cases"].get(n) == "skipped"]
    for suite in config.get("scoped_always") or []:
        if not any(name.startswith(suite + ".") for name in parsed["cases"]):
            problems.append(f"scoped run did not include required suite {suite}")
    problems += [f"still failing: {n}" for n, r in parsed["cases"].items() if r == "failed"]
    if parsed["suite_failed"]:
        problems.append("scoped run root result is Failed")
    return problems


def cmd_triage_close(args: argparse.Namespace, repo: Path, store: Path) -> int:
    """Compare the closing full run with the baseline, since narrow reruns cannot see the suite."""
    ledger = _read_json(_ledger_path(store, args.baseline))
    run = _load_run(store, args.run)
    parsed = parse_results(Path(run["results_artifact"]))
    if args.scoped:
        if run["status"] not in (GREEN, FAILING) or parsed is None:
            raise Refusal(f"run {args.run} did not execute")
        baseline = _load_run(store, ledger["baseline_run"])
        problems = _scoped_close_problems(repo, _load_config(repo), ledger, baseline, run, parsed)
        for problem in problems:
            print(f"REPORT TO USER: {problem}")
        if not problems:
            print(
                f"closed: scoped run {args.run} is green over failing run {ledger['baseline_run']}, "
                "and every repair touched test code only"
            )
        return EXIT_FAILING if problems else EXIT_GREEN
    if run["scope"] != ledger["baseline_scope"] or parsed is None:
        raise Refusal(f"run {args.run} is not an executed {ledger['baseline_scope']} run")
    base, counts = ledger["baseline_counts"], parsed["counts"]
    problems = [f"still failing: {n}" for n, r in parsed["cases"].items() if r == "failed"]
    problems += [f"test no longer present: {n}" for n in ledger["failures"] if n not in parsed["cases"]]
    if counts["total"] < base["total"]:
        problems.append(f"suite shrank from {base['total']} to {counts['total']} tests")
    if counts["skipped"] > base["skipped"]:
        problems.append(f"skips rose from {base['skipped']} to {counts['skipped']}")
    for problem in problems:
        print(f"REPORT TO USER: {problem}")
    if not problems:
        print(f"closed: run {args.run} is green with no lost tests")
    return EXIT_FAILING if problems else EXIT_GREEN


def cmd_triage_report(args: argparse.Namespace, repo: Path, store: Path) -> int:
    ledger = _read_json(_ledger_path(store, args.baseline))
    classified = {t for c in ledger["root_causes"].values() for t in c["tests"]}
    unclassified = sorted(set(ledger["failures"]) - classified)
    print(f"baseline-run: {ledger['baseline_run']}")
    for name, cause in sorted(ledger["root_causes"].items()):
        print(
            f"{name}: {cause['classification']} {cause['decision']} "
            f"iterations={len(cause['iterations'])} tests={len(cause['tests'])}"
        )
        for iteration in cause["iterations"]:
            for problem in iteration["integrity"]:
                print(f"  REPORT TO USER: {problem}")
            for test in iteration["new_failures"]:
                print(f"  new failure: {test}")
    if unclassified:
        print(f"unclassified: {', '.join(unclassified)}")
    settled = not unclassified and all(c["decision"] == "resolved" for c in ledger["root_causes"].values())
    return EXIT_GREEN if settled else EXIT_FAILING


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a test suite at most once per code state.")
    parser.add_argument("--repo", default=".", help="any path inside the target repository")
    commands = parser.add_subparsers(dest="action", required=True)

    ensure = commands.add_parser("ensure", help="reattach, reuse, or start a run")
    ensure.add_argument("--scope", default="full")
    ensure.add_argument("--command", help="command with a {results} placeholder; overrides the config")
    ensure.add_argument("--wait-seconds", type=float, default=540)
    ensure.add_argument("--force", action="store_true", help="ignore reusable results")
    ensure.set_defaults(handler=cmd_ensure)

    status = commands.add_parser("status", help="report the active or latest run")
    status.set_defaults(handler=cmd_status)

    triage = commands.add_parser("triage", help="record failure classification and repair attempts")
    triage.add_argument("--baseline", help="baseline run id; defaults to the newest ledger")
    steps = triage.add_subparsers(dest="step", required=True)
    opened = steps.add_parser("open")
    opened.add_argument("--run")
    opened.set_defaults(handler=cmd_triage_open)
    classify = steps.add_parser("classify")
    classify.add_argument("--root-cause", required=True)
    classify.add_argument("--class", dest="classification", choices=CLASSES, required=True)
    classify.add_argument("--evidence", required=True)
    classify.add_argument("--test", action="append", required=True)
    classify.set_defaults(handler=cmd_triage_classify)
    iterate = steps.add_parser("iterate")
    iterate.add_argument("--root-cause", required=True)
    iterate.add_argument("--run", required=True)
    iterate.set_defaults(handler=cmd_triage_iterate)
    close = steps.add_parser("close")
    close.add_argument("--run", required=True)
    close.add_argument("--scoped", action="store_true", help="close with a scoped run after a test-only repair")
    close.set_defaults(handler=cmd_triage_close)
    report = steps.add_parser("report")
    report.set_defaults(handler=cmd_triage_report)
    return parser


def main(argv: list[str] | None = None) -> int:
    arguments = sys.argv[1:] if argv is None else argv
    if arguments[:1] == ["_supervise"]:
        supervise(Path(arguments[1]))
        return EXIT_GREEN
    if os.name != "posix":
        print("not-executed: test_gate requires a POSIX system", file=sys.stderr)
        return EXIT_NOT_EXECUTED
    args = build_parser().parse_args(arguments)
    logging.basicConfig(stream=sys.stderr, level=logging.WARNING, format="%(levelname)s %(message)s")
    try:
        repo = Path(_git(Path(args.repo), "rev-parse", "--show-toplevel").strip())
        return args.handler(args, repo, _store(repo))
    except Refusal as refusal:
        print(str(refusal))
        return EXIT_NOT_EXECUTED


if __name__ == "__main__":
    sys.exit(main())
