#!/usr/bin/env python3
"""Deterministic, content-redacted benchmark for the production injection corpus."""

from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
HOOKS_DIR = REPO_ROOT / ".github" / "hooks"
SCANNER_PATH = HOOKS_DIR / "lib" / "injection_scanner.py"
DEFAULT_CONFIG = HOOKS_DIR / "config" / "injection-patterns.json"
DEFAULT_FIXTURES = Path(__file__).with_name("fixtures") / "injection"
DEFAULT_POSITIVE = DEFAULT_FIXTURES / "positive.json"
DEFAULT_MARKDOWN = DEFAULT_FIXTURES / "markdown-smuggling.json"
DEFAULT_NEGATIVE = DEFAULT_FIXTURES / "negative.json"
REQUIRED_CATEGORIES = (
    "context-manipulation",
    "encoding-obfuscation",
    "instruction-override",
    "instruction-smuggling",
    "persona-role-hijack",
)


def _scanner_module():
    spec = importlib.util.spec_from_file_location("injection_benchmark_scanner", SCANNER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("scanner-unavailable")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate-json-key")
        result[key] = value
    return result


def _read_json(path: Path) -> Any:
    return json.loads(
        path.read_text(encoding="utf-8"),
        object_pairs_hook=_reject_duplicate_keys,
    )


def run_benchmark(
    *,
    config_path: Path = DEFAULT_CONFIG,
    positive_path: Path = DEFAULT_POSITIVE,
    markdown_path: Path = DEFAULT_MARKDOWN,
    negative_path: Path = DEFAULT_NEGATIVE,
) -> dict[str, Any]:
    """Replay fixtures through the production APIs and return redacted counts."""

    scanner = _scanner_module()
    config = _read_json(config_path)
    rules = scanner.load_injection_rules(config)
    positives = _read_json(positive_path) + _read_json(markdown_path)
    negatives = _read_json(negative_path)
    categories = {rule.category for rule in rules}
    severities = {rule.severity for rule in rules}
    configured_ids = {rule.rule_id for rule in rules}
    evidenced_ids = {case.get("expected_rule") for case in positives}

    per_category = {
        category: {"true_positives": 0, "misses": 0, "false_positives": 0}
        for category in REQUIRED_CATEGORIES
    }
    tiers = {"high": 0, "medium": 0, "low": 0}
    misses = 0
    true_positives = 0
    false_positives = 0
    high_false_positives = 0
    skipped = 0

    for case in positives:
        expected_category = case.get("category")
        required = (
            "text",
            "expected_rule",
            "category",
            "severity",
            "response_action",
            "variant",
        )
        if any(field not in case for field in required) or expected_category not in per_category:
            skipped += 1
            misses += 1
            if expected_category in per_category:
                per_category[expected_category]["misses"] += 1
            continue
        result = scanner.scan_output(case["text"], rules, limits=config.get("scan_limits"))
        match = result.match
        correct = match is not None and (
            match.rule_id,
            match.category,
            match.severity,
            match.response_action,
        ) == (
            case["expected_rule"],
            case["category"],
            case["severity"],
            case["response_action"],
        )
        if correct:
            true_positives += 1
            per_category[expected_category]["true_positives"] += 1
            tiers[match.severity] += 1
        else:
            misses += 1
            per_category[expected_category]["misses"] += 1

    for case in negatives:
        if "text" not in case or "content_class" not in case:
            skipped += 1
            continue
        result = scanner.scan_output(case["text"], rules, limits=config.get("scan_limits"))
        if result.match is not None:
            false_positives += 1
            per_category[result.match.category]["false_positives"] += 1
            if result.match.severity == "high":
                high_false_positives += 1

    inventory_valid = (
        categories == set(REQUIRED_CATEGORIES)
        and severities == {"high", "medium", "low"}
        and all(
            rule.response_action == ("block" if rule.severity == "high" else "warn")
            for rule in rules
        )
        and configured_ids == evidenced_ids
        and bool(positives)
        and bool(negatives)
    )
    passed = (
        inventory_valid
        and misses == 0
        and false_positives == 0
        and high_false_positives == 0
        and skipped == 0
    )
    return {
        "passed": passed,
        "inventory_valid": inventory_valid,
        "fixtures": {
            "positive": len(positives),
            "negative": len(negatives),
            "skipped": skipped,
        },
        "totals": {
            "true_positives": true_positives,
            "misses": misses,
            "false_positives": false_positives,
            "high_false_positives": high_false_positives,
        },
        "per_category": per_category,
        "tier_counts": tiers,
    }


def _human_summary(summary: dict[str, Any]) -> str:
    status = "PASS" if summary["passed"] else "FAIL"
    totals = summary["totals"]
    lines = [
        f"Injection corpus benchmark: {status}",
        (
            "Totals: "
            f"true_positives={totals['true_positives']} "
            f"misses={totals['misses']} "
            f"false_positives={totals['false_positives']} "
            f"high_false_positives={totals['high_false_positives']}"
        ),
    ]
    for category, counts in summary["per_category"].items():
        lines.append(
            f"Category {category}: true_positives={counts['true_positives']} "
            f"misses={counts['misses']} false_positives={counts['false_positives']}"
        )
    lines.append("Tier counts: " + " ".join(
        f"{tier}={count}" for tier, count in summary["tier_counts"].items()
    ))
    lines.append("summary-json: " + json.dumps(summary, sort_keys=True))
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--positive", type=Path, default=DEFAULT_POSITIVE)
    parser.add_argument("--markdown", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--negative", type=Path, default=DEFAULT_NEGATIVE)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        summary = run_benchmark(
            config_path=args.config,
            positive_path=args.positive,
            markdown_path=args.markdown,
            negative_path=args.negative,
        )
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError):
        summary = {
            "passed": False,
            "error": "benchmark-input-invalid",
            "fixtures": {"positive": 0, "negative": 0, "skipped": 0},
            "totals": {
                "true_positives": 0,
                "misses": 0,
                "false_positives": 0,
                "high_false_positives": 0,
            },
            "per_category": {},
            "tier_counts": {"high": 0, "medium": 0, "low": 0},
        }
    print(json.dumps(summary, sort_keys=True) if args.json else _human_summary(summary))
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
