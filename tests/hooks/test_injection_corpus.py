from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import time
from pathlib import Path
from statistics import median

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]
HOOKS_DIR = REPO_ROOT / ".github" / "hooks"
CONFIG_PATH = HOOKS_DIR / "config" / "injection-patterns.json"
SCANNER_PATH = HOOKS_DIR / "lib" / "injection_scanner.py"
SCRIPT_PATH = HOOKS_DIR / "scripts" / "injection-scanner.py"
BENCHMARK_PATH = Path(__file__).with_name("injection_benchmark.py")
FIXTURE_DIR = Path(__file__).with_name("fixtures") / "injection"
POSITIVE_PATH = FIXTURE_DIR / "positive.json"
NEGATIVE_PATH = FIXTURE_DIR / "negative.json"
MARKDOWN_PATH = FIXTURE_DIR / "markdown-smuggling.json"
REQUIRED_CATEGORIES = {
    "instruction-override",
    "persona-role-hijack",
    "encoding-obfuscation",
    "context-manipulation",
    "instruction-smuggling",
}


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def scanner():
    return _load_module(SCANNER_PATH, "phase02_corpus_scanner")


@pytest.fixture(scope="module")
def scanner_script():
    return _load_module(SCRIPT_PATH, "phase02_corpus_entrypoint")


@pytest.fixture(scope="module")
def benchmark():
    return _load_module(BENCHMARK_PATH, "phase02_injection_benchmark")


@pytest.fixture(scope="module")
def config() -> dict[str, object]:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def positives() -> list[dict[str, object]]:
    return json.loads(POSITIVE_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def markdown_cases() -> list[dict[str, object]]:
    return json.loads(MARKDOWN_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def negatives() -> list[dict[str, object]]:
    return json.loads(NEGATIVE_PATH.read_text(encoding="utf-8"))


def test_ac1_ac3_production_corpus_is_valid_complete_and_original(
    scanner, config
) -> None:
    rules = scanner.load_injection_rules(config)

    assert config["provenance"] == "phase-02-clean-room-taxonomy"
    assert config["clean_room"] is True
    assert {rule.category for rule in rules} == REQUIRED_CATEGORIES
    assert {rule.severity for rule in rules} >= {"high", "medium", "low"}
    assert all(rule.reason and rule.recommended_posture for rule in rules)
    assert len({rule.rule_id for rule in rules}) == len(rules)


@pytest.mark.parametrize(
    "mutation",
    [
        lambda cfg: cfg.update({"rules": {}}),
        lambda cfg: cfg["rules"][next(iter(cfg["rules"]))].update({"id": "wrong-id"}),
        lambda cfg: cfg["rules"][next(iter(cfg["rules"]))].update({"severity": "critical"}),
        lambda cfg: cfg["rules"][next(iter(cfg["rules"]))].update({"response_action": "replace"}),
        lambda cfg: cfg["rules"][next(iter(cfg["rules"]))].update({"matcher": "callable"}),
        lambda cfg: cfg["rules"][next(iter(cfg["rules"]))].pop("recommended_posture"),
        lambda cfg: cfg["rules"][next(iter(cfg["rules"]))].update({"recommended_posture": ""}),
        lambda cfg: cfg["rules"][next(iter(cfg["rules"]))].update({"pattern": "(a+)+$"}),
    ],
)
def test_ac3_invalid_schema_fails_redacted(scanner, config, mutation) -> None:
    candidate = json.loads(json.dumps(config))
    mutation(candidate)

    with pytest.raises(scanner.InjectionConfigError) as error:
        scanner.load_injection_rules(candidate)

    assert not any(rule["pattern"] in str(error.value) for rule in config["rules"].values())


def test_ac4_rule_fixture_inventory_is_bidirectionally_complete(
    scanner, config, positives, markdown_cases
) -> None:
    rules = scanner.load_injection_rules(config)
    fixtures = positives + markdown_cases
    configured = {rule.rule_id for rule in rules}
    evidenced = {case["expected_rule"] for case in fixtures}

    assert evidenced == configured
    assert all(
        {"expected_rule", "category", "severity", "response_action", "variant"}
        <= case.keys()
        for case in fixtures
    )


@pytest.mark.parametrize("fixture_name", ["positive.json", "markdown-smuggling.json"])
def test_ac2_ac4_ac8_positive_replay_uses_production_scanner(
    scanner, config, fixture_name
) -> None:
    rules = scanner.load_injection_rules(config)
    cases = json.loads((FIXTURE_DIR / fixture_name).read_text(encoding="utf-8"))

    for case in cases:
        result = scanner.scan_output(case["text"], rules, limits=config["scan_limits"])
        assert result.match is not None, case["id"]
        assert result.match.rule_id == case["expected_rule"], case["id"]
        assert result.match.category == case["category"], case["id"]
        assert result.match.severity == case["severity"], case["id"]
        assert result.match.response_action == case["response_action"], case["id"]


def test_ac2_markdown_smuggling_covers_every_required_channel(markdown_cases) -> None:
    assert {case["channel"] for case in markdown_cases} == {
        "link-title",
        "image-alt-text",
        "reference-definition",
        "html-comment",
        "code-comment",
        "html-attribute",
    }


def test_ac5_negative_corpus_is_realistic_and_has_no_matches(
    scanner, config, negatives
) -> None:
    rules = scanner.load_injection_rules(config)
    required_classes = {
        "security-documentation",
        "repository-hook-documentation",
        "prompt-discussion-code",
        "markdown-example",
        "ordinary-authority-prose",
        "ordinary-persona-prose",
        "encoded-non-imperative-data",
    }

    assert {case["content_class"] for case in negatives} == required_classes
    for case in negatives:
        assert scanner.scan_output(case["text"], rules).match is None, case["id"]


def test_ac7_each_rule_obeys_configured_response_contract(
    scanner, scanner_script, framework, config, positives, markdown_cases, tmp_path
) -> None:
    rules = scanner.load_injection_rules(config)
    cases = positives + markdown_cases
    first_case = {}
    for case in cases:
        first_case.setdefault(case["expected_rule"], case)
    snapshot = framework.ConfigSnapshot({**config, "source_allowlist": []}, True)

    for rule in rules:
        raw = first_case[rule.rule_id]["text"]
        event = framework.parse_payload({
            "hook_event_name": "PostToolUse",
            "tool_name": "WebFetch",
            "tool_input": {},
            "tool_output": raw,
            "tool_output_truncated": False,
        })
        result = scanner_script.handle_event(event, snapshot, repo_root=tmp_path)
        if rule.response_action == "block":
            assert result.action == "block"
            assert "Do not retry" in result.reason
            assert "inspect the source manually" in result.reason
            assert raw not in result.reason
        else:
            assert result.action == "warn"
            assert event.tool_output == raw
            assert rule.rule_id in result.additional_context
            assert raw not in result.additional_context


def test_ac6_benchmark_reports_deterministic_redacted_counts(
    benchmark, positives, markdown_cases, negatives
) -> None:
    first = benchmark.run_benchmark()
    second = benchmark.run_benchmark()

    assert first == second
    assert first["passed"] is True
    assert first["totals"]["misses"] == 0
    assert first["totals"]["false_positives"] == 0
    assert first["totals"]["high_false_positives"] == 0
    assert set(first["per_category"]) == REQUIRED_CATEGORIES
    serialized = json.dumps(first)
    assert "matched_span" not in serialized
    assert all(
        case["text"] not in serialized
        for case in positives + markdown_cases + negatives
    )


def test_ac6_benchmark_returns_nonzero_for_broken_expectation(tmp_path) -> None:
    broken = json.loads(POSITIVE_PATH.read_text(encoding="utf-8"))
    broken[0]["expected_rule"] = "missing-rule"
    broken_path = tmp_path / "broken.json"
    broken_path.write_text(json.dumps(broken), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            str(BENCHMARK_PATH),
            "--positive",
            str(broken_path),
            "--json",
        ],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    summary = json.loads(result.stdout)
    assert summary["passed"] is False
    assert summary["totals"]["misses"] >= 1
    assert broken[0]["text"] not in result.stdout


@pytest.mark.parametrize(
    "invalid_config,sentinel",
    [
        ('{"secret":"MALFORMED_SENTINEL"', "MALFORMED_SENTINEL"),
        ('{"rules":{"duplicate":{},"duplicate":{}}}', "duplicate-json-key"),
    ],
)
def test_ac3_ac6_benchmark_rejects_malformed_or_duplicate_json(
    tmp_path, invalid_config, sentinel
) -> None:
    config_path = tmp_path / "invalid.json"
    config_path.write_text(invalid_config, encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            str(BENCHMARK_PATH),
            "--config",
            str(config_path),
            "--json",
        ],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 1
    assert json.loads(result.stdout)["error"] == "benchmark-input-invalid"
    assert sentinel not in result.stdout


def test_ac2_ac6_benchmark_rejects_an_empty_required_category(
    benchmark, config, tmp_path
) -> None:
    candidate = json.loads(json.dumps(config))
    candidate["rules"] = {
        rule_id: rule
        for rule_id, rule in candidate["rules"].items()
        if rule["category"] != "persona-role-hijack"
    }
    config_path = tmp_path / "missing-category.json"
    config_path.write_text(json.dumps(candidate), encoding="utf-8")

    summary = benchmark.run_benchmark(config_path=config_path)

    assert summary["passed"] is False
    assert summary["inventory_valid"] is False


def test_ac6_benchmark_invocation_is_cwd_independent(tmp_path) -> None:
    result = subprocess.run(
        [sys.executable, str(BENCHMARK_PATH), "--json"],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert json.loads(result.stdout)["passed"] is True
    assert result.stderr == ""


def test_ac8_representative_large_output_stays_within_latency_budget(
    scanner, config
) -> None:
    rules = scanner.load_injection_rules(config)
    output = "ordinary repository documentation text " * 2_000
    samples = []
    for _ in range(25):
        started = time.perf_counter_ns()
        result = scanner.scan_output(output, rules, limits=config["scan_limits"])
        samples.append((time.perf_counter_ns() - started) / 1_000_000)
        assert result.match is None

    assert median(samples) < 50
