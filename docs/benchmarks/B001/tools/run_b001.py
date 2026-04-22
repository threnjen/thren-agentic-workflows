#!/usr/bin/env python3
"""B001 benchmark runner.

Reads benchmark config + task definitions, ingests baseline/candidate task result JSON,
and emits a gate verdict report.
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
from pathlib import Path
from typing import Any


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        import yaml  # type: ignore
    except Exception as exc:  # pragma: no cover
        raise RuntimeError(
            "PyYAML is required. Install with: python3 -m pip install pyyaml"
        ) from exc

    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping at top-level YAML: {path}")
    return data


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"Expected object JSON at top-level: {path}")
    return data


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    rank = (len(ordered) - 1) * pct
    low = math.floor(rank)
    high = math.ceil(rank)
    if low == high:
        return ordered[low]
    low_val = ordered[low]
    high_val = ordered[high]
    frac = rank - low
    return low_val * (1 - frac) + high_val * frac


def safe_mean(values: list[float]) -> float:
    return statistics.fmean(values) if values else 0.0


def load_tasks(task_path: Path) -> list[dict[str, Any]]:
    data = load_yaml(task_path)
    tasks = data.get("tasks", [])
    if not isinstance(tasks, list):
        raise ValueError(f"Expected tasks list in {task_path}")
    normalized: list[dict[str, Any]] = []
    for task in tasks:
        if not isinstance(task, dict):
            continue
        task_id = task.get("task_id")
        family = task.get("family")
        if isinstance(task_id, str) and isinstance(family, str):
            normalized.append({"task_id": task_id, "family": family})
    return normalized


def normalize_results(payload: dict[str, Any]) -> dict[str, dict[str, float]]:
    tasks = payload.get("tasks", [])
    if not isinstance(tasks, list):
        raise ValueError("Result payload must contain tasks: []")

    by_task: dict[str, list[dict[str, float]]] = {}
    for row in tasks:
        if not isinstance(row, dict):
            continue
        task_id = row.get("task_id")
        if not isinstance(task_id, str):
            continue

        normalized = {
            "hard_pass": float(bool(row.get("hard_pass", False))),
            "quality_score": float(row.get("quality_score", 0.0)),
            "compliance_score": float(row.get("compliance_score", 0.0)),
            "latency_ms": float(row.get("latency_ms", 0.0)),
            "cost_usd": float(row.get("cost_usd", 0.0)),
            "tokens_total": float(row.get("tokens_total", 0.0)),
        }
        by_task.setdefault(task_id, []).append(normalized)

    aggregated: dict[str, dict[str, float]] = {}
    for task_id, rows in by_task.items():
        aggregated[task_id] = {
            "hard_pass": safe_mean([r["hard_pass"] for r in rows]),
            "quality_score": safe_mean([r["quality_score"] for r in rows]),
            "compliance_score": safe_mean([r["compliance_score"] for r in rows]),
            "latency_ms": safe_mean([r["latency_ms"] for r in rows]),
            "cost_usd": safe_mean([r["cost_usd"] for r in rows]),
            "tokens_total": safe_mean([r["tokens_total"] for r in rows]),
        }
    return aggregated


def summarize(
    task_defs: list[dict[str, Any]], results: dict[str, dict[str, float]]
) -> dict[str, Any]:
    rows = [results[t["task_id"]] for t in task_defs if t["task_id"] in results]

    hard_passes = [r["hard_pass"] for r in rows]
    quality = [r["quality_score"] for r in rows]
    compliance = [r["compliance_score"] for r in rows]
    latency = [r["latency_ms"] for r in rows]
    costs = [r["cost_usd"] for r in rows]

    pass_rate = safe_mean(hard_passes) * 100.0
    quality_mean = safe_mean(quality)
    compliance_violations = sum(1 for score in compliance if score < 4.0)
    total_cost = sum(costs)
    passed_count = sum(1 for p in hard_passes if p >= 0.5)
    cost_per_pass = total_cost / passed_count if passed_count > 0 else float("inf")

    by_family: dict[str, dict[str, float]] = {}
    for task in task_defs:
        task_id = task["task_id"]
        family = task["family"]
        if task_id not in results:
            continue
        entry = results[task_id]
        fam = by_family.setdefault(
            family,
            {
                "task_count": 0.0,
                "pass_sum": 0.0,
                "quality_sum": 0.0,
            },
        )
        fam["task_count"] += 1.0
        fam["pass_sum"] += entry["hard_pass"]
        fam["quality_sum"] += entry["quality_score"]

    for fam in by_family.values():
        count = fam["task_count"]
        fam["pass_rate"] = (fam["pass_sum"] / count) * 100.0 if count else 0.0
        fam["quality_mean"] = fam["quality_sum"] / count if count else 0.0

    return {
        "task_coverage": len(rows),
        "task_total": len(task_defs),
        "pass_rate": pass_rate,
        "quality_mean": quality_mean,
        "compliance_violations": compliance_violations,
        "cost_per_pass": cost_per_pass,
        "p50_latency_ms": percentile(latency, 0.50),
        "p90_latency_ms": percentile(latency, 0.90),
        "by_family": by_family,
    }


def compute_verdict(
    manifest: dict[str, Any],
    baseline_summary: dict[str, Any],
    candidate_summary: dict[str, Any],
) -> tuple[str, dict[str, Any], dict[str, float], list[dict[str, Any]]]:
    thresholds = manifest.get("thresholds", {})
    non_inf = (
        thresholds.get("non_inferiority", {}) if isinstance(thresholds, dict) else {}
    )

    hard_drop_fail = float(thresholds.get("hard_pass_drop_fail_percent", 2.0))
    max_quality_drop = float(non_inf.get("max_quality_drop", -0.10))
    max_hard_drop = float(non_inf.get("max_hard_pass_drop_percent", -1.0))
    min_cost_improvement = float(
        non_inf.get("min_cost_per_pass_improvement_percent", 15.0)
    )

    pass_rate_delta = candidate_summary["pass_rate"] - baseline_summary["pass_rate"]
    quality_delta = candidate_summary["quality_mean"] - baseline_summary["quality_mean"]
    compliance_violation_delta = (
        candidate_summary["compliance_violations"]
        - baseline_summary["compliance_violations"]
    )

    base_cpp = baseline_summary["cost_per_pass"]
    cand_cpp = candidate_summary["cost_per_pass"]
    if math.isfinite(base_cpp) and base_cpp > 0 and math.isfinite(cand_cpp):
        cost_per_pass_delta = ((base_cpp - cand_cpp) / base_cpp) * 100.0
    else:
        cost_per_pass_delta = 0.0

    p50_latency_delta = (
        candidate_summary["p50_latency_ms"] - baseline_summary["p50_latency_ms"]
    )
    p90_latency_delta = (
        candidate_summary["p90_latency_ms"] - baseline_summary["p90_latency_ms"]
    )

    gate_evaluation = {
        "hard_fail_pass_drop": pass_rate_delta < -hard_drop_fail,
        "non_inferiority_quality": quality_delta >= max_quality_drop,
        "non_inferiority_pass_rate": pass_rate_delta >= max_hard_drop,
        "non_inferiority_cost_per_pass": cost_per_pass_delta >= min_cost_improvement,
    }

    regressions_by_family: list[dict[str, Any]] = []
    baseline_families = baseline_summary["by_family"]
    candidate_families = candidate_summary["by_family"]
    for family, base_data in baseline_families.items():
        cand_data = candidate_families.get(family)
        if not cand_data:
            continue
        fam_pass_delta = cand_data["pass_rate"] - base_data["pass_rate"]
        fam_quality_delta = cand_data["quality_mean"] - base_data["quality_mean"]
        if fam_pass_delta < 0 or fam_quality_delta < 0:
            regressions_by_family.append(
                {
                    "family": family,
                    "pass_rate_delta": round(fam_pass_delta, 4),
                    "quality_delta": round(fam_quality_delta, 4),
                }
            )

    if gate_evaluation["hard_fail_pass_drop"]:
        verdict = "FAIL"
    elif all(
        [
            gate_evaluation["non_inferiority_quality"],
            gate_evaluation["non_inferiority_pass_rate"],
            gate_evaluation["non_inferiority_cost_per_pass"],
        ]
    ):
        verdict = "PASS"
    else:
        verdict = "REVIEW_REQUIRED"

    deltas = {
        "pass_rate_delta": round(pass_rate_delta, 4),
        "quality_delta": round(quality_delta, 4),
        "compliance_violation_delta": float(compliance_violation_delta),
        "cost_per_pass_delta": round(cost_per_pass_delta, 4),
        "p50_latency_delta": round(p50_latency_delta, 4),
        "p90_latency_delta": round(p90_latency_delta, 4),
    }

    return verdict, gate_evaluation, deltas, regressions_by_family


def build_skeleton_report(
    run_id: str, benchmark_id: str, task_defs: list[dict[str, Any]], output_path: Path
) -> dict[str, Any]:
    return {
        "benchmark_id": benchmark_id,
        "run_id": run_id,
        "verdict": "REVIEW_REQUIRED",
        "reason": "No result payloads provided. This is a skeleton report.",
        "expected_tasks": [t["task_id"] for t in task_defs],
        "output_path": str(output_path),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run B001 benchmark gate evaluation")
    parser.add_argument("--config", required=True, help="Path to run-config YAML")
    parser.add_argument("--baseline-results", help="Path to baseline results JSON")
    parser.add_argument("--candidate-results", help="Path to candidate results JSON")
    parser.add_argument("--output", help="Override output report path")
    args = parser.parse_args()

    config_path = Path(args.config)
    config = load_yaml(config_path)

    manifest_path = Path(config["constraints"]["benchmark_manifest"])
    tasks_path = Path(config["constraints"]["core_tasks"])
    output_path = Path(args.output or config["output"]["report_path"])

    manifest = load_yaml(manifest_path)
    task_defs = load_tasks(tasks_path)

    run_id = str(config.get("run_id", "unknown-run"))
    benchmark_id = str(
        config.get("benchmark_id", manifest.get("benchmark_id", "unknown"))
    )

    if not args.baseline_results or not args.candidate_results:
        report = build_skeleton_report(run_id, benchmark_id, task_defs, output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(f"Wrote skeleton report: {output_path}")
        return 0

    baseline_payload = load_json(Path(args.baseline_results))
    candidate_payload = load_json(Path(args.candidate_results))
    baseline_results = normalize_results(baseline_payload)
    candidate_results = normalize_results(candidate_payload)

    baseline_summary = summarize(task_defs, baseline_results)
    candidate_summary = summarize(task_defs, candidate_results)

    verdict, gate_evaluation, deltas, regressions_by_family = compute_verdict(
        manifest, baseline_summary, candidate_summary
    )

    report = {
        "benchmark_id": benchmark_id,
        "run_id": run_id,
        "verdict": verdict,
        "baseline_variant": config.get("baseline_variant", {}).get("name", "baseline"),
        "candidate_variant": config.get("candidate_variant", {}).get(
            "name", "candidate"
        ),
        "task_coverage": {
            "baseline": baseline_summary["task_coverage"],
            "candidate": candidate_summary["task_coverage"],
            "total": baseline_summary["task_total"],
        },
        "pass_rate_delta": deltas["pass_rate_delta"],
        "quality_delta": deltas["quality_delta"],
        "compliance_violation_delta": deltas["compliance_violation_delta"],
        "cost_per_pass_delta": deltas["cost_per_pass_delta"],
        "p50_latency_delta": deltas["p50_latency_delta"],
        "p90_latency_delta": deltas["p90_latency_delta"],
        "regressions_by_family": regressions_by_family,
        "gate_evaluation": gate_evaluation,
        "baseline_summary": baseline_summary,
        "candidate_summary": candidate_summary,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Wrote report: {output_path}")
    print(f"Verdict: {verdict}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
