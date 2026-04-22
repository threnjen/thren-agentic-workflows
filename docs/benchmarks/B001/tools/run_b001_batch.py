#!/usr/bin/env python3
"""B001 batch benchmark runner.

Evaluates multiple candidates against one baseline and writes a ranked summary report.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

import run_b001 as single


def _score_entry(entry: dict[str, Any]) -> float:
    """Rank score for sorting candidates in summary output.

    Higher is better. We prioritize pass-rate and quality, then cost improvement.
    """
    return (
        float(entry.get("pass_rate_delta", 0.0)) * 0.6
        + float(entry.get("quality_delta", 0.0)) * 30.0
        + float(entry.get("cost_per_pass_delta", 0.0)) * 0.1
    )


def _resolve_path(repo_root: Path, raw: str) -> Path:
    path = Path(raw)
    return path if path.is_absolute() else (repo_root / path)


def _git(repo_root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo_root), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        stderr = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(f"git {' '.join(args)} failed: {stderr}")
    return result.stdout.strip()


def _current_branch(repo_root: Path) -> str:
    return _git(repo_root, "rev-parse", "--abbrev-ref", "HEAD")


def _is_worktree_dirty(repo_root: Path) -> bool:
    """Check if working tree has uncommitted changes."""
    output = _git(repo_root, "status", "--porcelain")
    return bool(output.strip())


def _checkout(repo_root: Path, branch: str) -> None:
    _git(repo_root, "checkout", branch)


def run_candidate(
    config: dict[str, Any],
    manifest: dict[str, Any],
    task_defs: list[dict[str, Any]],
    baseline_summary: dict[str, Any],
    candidate_name: str,
    candidate_results_path: Path,
) -> dict[str, Any]:
    payload = single.load_json(candidate_results_path)
    candidate_results = single.normalize_results(payload)
    candidate_summary = single.summarize(task_defs, candidate_results)

    verdict, gate_evaluation, deltas, regressions = single.compute_verdict(
        manifest,
        baseline_summary,
        candidate_summary,
    )

    return {
        "candidate_name": candidate_name,
        "candidate_results_path": str(candidate_results_path),
        "verdict": verdict,
        "pass_rate_delta": deltas["pass_rate_delta"],
        "quality_delta": deltas["quality_delta"],
        "compliance_violation_delta": deltas["compliance_violation_delta"],
        "cost_per_pass_delta": deltas["cost_per_pass_delta"],
        "p50_latency_delta": deltas["p50_latency_delta"],
        "p90_latency_delta": deltas["p90_latency_delta"],
        "regressions_by_family": regressions,
        "gate_evaluation": gate_evaluation,
        "candidate_summary": candidate_summary,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run B001 batch candidate evaluation")
    parser.add_argument("--config", required=True, help="Path to batch config YAML")
    parser.add_argument("--output", help="Override output report path")
    args = parser.parse_args()

    config_path = Path(args.config)
    config = single.load_yaml(config_path)

    benchmark_id = str(config.get("benchmark_id", "B001"))
    run_id = str(config.get("run_id", "B001-BATCH"))

    git_config = config.get("git", {}) if isinstance(config.get("git", {}), dict) else {}
    checkout_enabled = bool(git_config.get("checkout_enabled", False))
    restore_original = bool(git_config.get("restore_original_branch", True))
    repo_root = _resolve_path(Path.cwd(), str(git_config.get("repo_root", "."))).resolve()

    manifest_path = _resolve_path(repo_root, str(config["constraints"]["benchmark_manifest"]))
    tasks_path = _resolve_path(repo_root, str(config["constraints"]["core_tasks"]))
    baseline_path = _resolve_path(repo_root, str(config["baseline_results"]))
    output_path = _resolve_path(repo_root, str(args.output or config["output"]["report_path"]))

    baseline_branch = config.get("baseline_branch")
    if checkout_enabled and not isinstance(baseline_branch, str):
        raise ValueError("baseline_branch is required when git.checkout_enabled is true")

    manifest = single.load_yaml(manifest_path)
    task_defs = single.load_tasks(tasks_path)

    original_branch = _current_branch(repo_root) if checkout_enabled else None

    if checkout_enabled and _is_worktree_dirty(repo_root):
        raise RuntimeError(
            f"Cannot checkout branches: working tree has uncommitted changes.\n"
            f"Stash or commit changes and retry:\n"
            f"  git -C {repo_root} status\n"
            f"  git -C {repo_root} stash\n"
        )

    try:
        if checkout_enabled and isinstance(baseline_branch, str):
            _checkout(repo_root, baseline_branch)

        baseline_payload = single.load_json(baseline_path)
        baseline_results = single.normalize_results(baseline_payload)
        baseline_summary = single.summarize(task_defs, baseline_results)

        candidates = config.get("candidates", [])
        if not isinstance(candidates, list) or not candidates:
            raise ValueError("Batch config requires a non-empty candidates list")

        results: list[dict[str, Any]] = []
        for candidate in candidates:
            if not isinstance(candidate, dict):
                continue
            name = candidate.get("name")
            path = candidate.get("results_path")
            branch = candidate.get("branch")
            if not isinstance(name, str) or not isinstance(path, str):
                continue
            if checkout_enabled:
                if not isinstance(branch, str):
                    raise ValueError(
                        f"Candidate '{name}' must define branch when git.checkout_enabled is true"
                    )
                _checkout(repo_root, branch)

            results.append(
                run_candidate(
                    config=config,
                    manifest=manifest,
                    task_defs=task_defs,
                    baseline_summary=baseline_summary,
                    candidate_name=name,
                    candidate_results_path=_resolve_path(repo_root, path),
                )
            )
    finally:
        if checkout_enabled and restore_original and isinstance(original_branch, str):
            _checkout(repo_root, original_branch)

    results_sorted = sorted(results, key=_score_entry, reverse=True)

    report = {
        "benchmark_id": benchmark_id,
        "run_id": run_id,
        "baseline_variant": str(config.get("baseline_variant", "baseline")),
        "baseline_branch": baseline_branch if isinstance(baseline_branch, str) else None,
        "baseline_results_path": str(baseline_path),
        "candidate_count": len(results_sorted),
        "results": results_sorted,
        "winner": results_sorted[0]["candidate_name"] if results_sorted else None,
        "baseline_summary": baseline_summary,
        "git": {
            "checkout_enabled": checkout_enabled,
            "repo_root": str(repo_root),
            "original_branch": original_branch,
            "restore_original_branch": restore_original,
        },
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"Wrote batch report: {output_path}")
    if results_sorted:
        print(f"Top candidate: {results_sorted[0]['candidate_name']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
