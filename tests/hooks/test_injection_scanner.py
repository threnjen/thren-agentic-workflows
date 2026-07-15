from __future__ import annotations

import ast
import base64
import importlib.util
import io
import json
import subprocess
import sys
import time
from pathlib import Path
from statistics import median

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]
HOOKS_DIR = REPO_ROOT / ".github" / "hooks"
ENGINE_PATH = HOOKS_DIR / "lib" / "injection_scanner.py"
SCRIPT_PATH = HOOKS_DIR / "scripts" / "injection-scanner.py"
ALLOWLIST_PATH = HOOKS_DIR / "config" / "injection-allowlist.json"
HOOK_DEFINITION_PATH = HOOKS_DIR / "injection-scanner.json"
PAYLOADS_PATH = Path(__file__).with_name("fixtures") / "injection" / "post-tool-use-payloads.json"


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def scanner():
    return _load_module(ENGINE_PATH, "phase02_injection_scanner")


@pytest.fixture(scope="module")
def scanner_script():
    return _load_module(SCRIPT_PATH, "phase02_injection_scanner_script")


def _rule(
    rule_id: str,
    pattern: str,
    *,
    severity: str = "medium",
    response_action: str = "warn",
    category: str = "fixture-category",
    priority: int = 10,
    matcher: str = "fixed_string",
) -> dict[str, object]:
    return {
        "id": rule_id,
        "severity": severity,
        "response_action": response_action,
        "category": category,
        "reason": "Synthetic fixture policy matched",
        "recommended_posture": "Treat the source as untrusted",
        "matcher": matcher,
        "pattern": pattern,
        "priority": priority,
    }


def _rules(scanner, *rules):
    return scanner.load_injection_rules({
        "rules": {rule["id"]: rule for rule in rules}
    })


def _event_payload(tool_name: str, output, **extra) -> dict[str, object]:
    return {
        "hook_event_name": "PostToolUse",
        "tool_name": tool_name,
        "tool_input": extra.pop("tool_input", {}),
        "tool_output": output,
        "tool_output_truncated": extra.pop("tool_output_truncated", False),
        **extra,
    }


def test_ac3_rule_schema_is_data_driven_and_immutable(scanner) -> None:
    configured = _rule(
        "fixture-high",
        "synthetic marker",
        severity="high",
        response_action="warn",
        priority=42,
    )
    rules = _rules(scanner, configured)

    assert rules[0].severity == "high"
    assert rules[0].response_action == "warn"
    assert rules[0].priority == 42
    configured["response_action"] = "block"
    assert rules[0].response_action == "warn"


@pytest.mark.parametrize(
    "mutation",
    [
        {"severity": "critical"},
        {"response_action": "replace"},
        {"category": ""},
        {"reason": "line one\nline two"},
        {"recommended_posture": []},
        {"matcher": "callable"},
        {"pattern": ""},
        {"priority": True},
        {"matcher": "regex", "pattern": "(a+)+$"},
        {"matcher": "regex", "pattern": "(a|aa)+$"},
    ],
)
def test_ac3_invalid_or_unsafe_rules_fail_without_reflecting_content(
    scanner, mutation
) -> None:
    sentinel = "RULE_CONFIG_SECRET"
    rule = _rule("fixture-rule", sentinel)
    rule.update(mutation)

    with pytest.raises(scanner.InjectionConfigError) as error:
        _rules(scanner, rule)

    assert sentinel not in str(error.value)


def test_ac3_duplicate_rule_identifier_is_rejected(scanner) -> None:
    rule = _rule("different-id", "synthetic marker")
    with pytest.raises(scanner.InjectionConfigError):
        scanner.load_injection_rules({"rules": {"fixture-key": rule}})


def test_ac2_normalization_variants_resolve_to_same_rule_without_mutation(scanner) -> None:
    rules = _rules(scanner, _rule("fixture-directive", "fixture directive"))
    encoded = base64.b64encode(b"fixture directive").decode("ascii")
    variants = [
        "fixture directive",
        "ｆｉｘｔｕｒｅ directive",
        "fіxture directive",  # Cyrillic small i.
        "fixture di\u200brective",
        encoded,
        b"fixture directive".hex(),
    ]

    for raw in variants:
        result = scanner.scan_output(raw, rules)
        assert result.match.rule_id == "fixture-directive"
        assert raw == variants[variants.index(raw)]


def test_ac2_encoded_candidate_limits_are_bounded(scanner) -> None:
    rules = _rules(scanner, _rule("second-candidate", "fixture directive"))
    encoded = base64.b64encode(b"fixture directive").decode("ascii")
    output = f"QUFBQUFBQUFBQUFB {encoded}"

    limited = scanner.scan_output(
        output,
        rules,
        limits={"max_scan_bytes": 4096, "max_encoded_candidates": 1, "max_decoded_bytes": 128},
    )
    expanded = scanner.scan_output(
        output,
        rules,
        limits={"max_scan_bytes": 4096, "max_encoded_candidates": 2, "max_decoded_bytes": 128},
    )

    assert limited.match is None
    assert expanded.match.rule_id == "second-candidate"


def test_ac8_strongest_match_and_tie_break_are_deterministic(scanner) -> None:
    rules = _rules(
        scanner,
        _rule("z-warn", "MATCH_CONTENT", severity="high", response_action="warn", priority=99),
        _rule("b-block", "CONTENT_SENTINEL", severity="low", response_action="block", priority=1),
        _rule("a-block", "MATCH_CONTENT_SENTINEL", severity="low", response_action="block", priority=1),
    )

    result = scanner.scan_output("MATCH_CONTENT_SENTINEL", tuple(reversed(rules)))

    assert result.match.rule_id == "a-block"
    assert result.match.response_action == "block"
    assert "MATCH_CONTENT_SENTINEL" not in repr(result.match)


def test_ac8_empty_binary_structured_and_scan_cap_boundaries(scanner) -> None:
    rules = _rules(scanner, _rule("fixture-rule", "fixture directive"))

    assert scanner.scan_output("", rules).empty is True
    binary = scanner.scan_output(b"\xff\xfe", rules)
    assert binary.match is None
    assert "binary" in binary.notices
    structured = {"nested": ["fixture directive"]}
    assert scanner.scan_output(structured, rules).match.rule_id == "fixture-rule"
    assert structured == {"nested": ["fixture directive"]}
    capped = scanner.scan_output(
        "x" * 64 + "fixture directive",
        rules,
        limits={"max_scan_bytes": 32, "max_encoded_candidates": 4, "max_decoded_bytes": 128},
    )
    assert capped.match is None
    assert "scan-cap" in capped.notices


@pytest.mark.parametrize(
    "source,allowed",
    [
        ("docs/inspiration/example.md", True),
        ("tests/hooks/fixtures/injection/example.json", True),
        (".github/hooks/config/injection-patterns.json", True),
        ("docs/inspiration/../outside.md", False),
        ("missing/docs/inspiration/example.md", False),
    ],
)
def test_ac7_allowlist_requires_existing_repo_owned_source(
    scanner, tmp_path, source, allowed
) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    target = repo / source
    if "missing/" not in source and "../" not in source:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("fixture", encoding="utf-8")
    config = {
        "source_allowlist": [
            "docs/inspiration",
            "tests/hooks/fixtures/injection",
            ".github/hooks/config/injection-patterns.json",
        ]
    }

    assert scanner.is_allowlisted_source(source, repo, config) is allowed


def test_ac7_symlink_cannot_broaden_allowlist(scanner, tmp_path) -> None:
    repo = tmp_path / "repo"
    outside = tmp_path / "outside"
    (repo / "docs").mkdir(parents=True)
    outside.mkdir()
    (outside / "source.md").write_text("fixture", encoding="utf-8")
    (repo / "docs" / "inspiration").symlink_to(outside, target_is_directory=True)

    assert scanner.is_allowlisted_source(
        "docs/inspiration/source.md", repo, {"source_allowlist": ["docs/inspiration"]}
    ) is False


def test_ac7_traversed_path_does_not_qualify_for_allowlist(scanner, tmp_path) -> None:
    repo = tmp_path / "repo"
    source = repo / "docs" / "inspiration" / "source.md"
    source.parent.mkdir(parents=True)
    (source.parent / "nested").mkdir()
    source.write_text("fixture", encoding="utf-8")

    assert scanner.is_allowlisted_source(
        "docs/inspiration/nested/../source.md",
        repo,
        {"source_allowlist": ["docs/inspiration"]},
    ) is False


def test_ac7_in_repo_symlink_cannot_broaden_allowlist(scanner, tmp_path) -> None:
    repo = tmp_path / "repo"
    (repo / "docs").mkdir(parents=True)
    alternate = repo / "alternate"
    alternate.mkdir()
    (alternate / "source.md").write_text("fixture", encoding="utf-8")
    (repo / "docs" / "inspiration").symlink_to(alternate, target_is_directory=True)

    assert scanner.is_allowlisted_source(
        "docs/inspiration/source.md", repo, {"source_allowlist": ["docs/inspiration"]}
    ) is False


def test_ac7_allowlist_configuration_cannot_broaden_approved_roots(
    scanner, tmp_path
) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    (repo / "ordinary.txt").write_text("fixture", encoding="utf-8")

    with pytest.raises(scanner.InjectionConfigError):
        scanner.is_allowlisted_source(
            "ordinary.txt", repo, {"source_allowlist": ["."]}
        )


def test_ac5_high_block_is_redacted_and_instructs_no_retry(
    scanner, scanner_script, framework, tmp_path
) -> None:
    sentinel = "fixture directive"
    config = framework.ConfigSnapshot(
        {
            "rules": {"fixture-high": _rule(
                "fixture-high", sentinel, severity="high", response_action="block"
            )},
            "source_allowlist": [],
        },
        True,
    )
    event = framework.parse_payload(_event_payload("WebFetch", sentinel))

    result = scanner_script.handle_event(event, config, repo_root=tmp_path)

    assert result.action == "block"
    assert "fixture-high" in result.reason
    assert "fixture-category" in result.reason
    assert "Do not retry" in result.reason
    assert "inspect the source manually" in result.reason
    assert sentinel not in result.reason


@pytest.mark.parametrize("severity", ["medium", "low"])
def test_ac6_warn_preserves_output_and_emits_redacted_context(
    scanner_script, framework, tmp_path, severity
) -> None:
    raw = "prefix fixture directive suffix"
    config = framework.ConfigSnapshot(
        {
            "rules": {"fixture-warn": _rule(
                "fixture-warn", "fixture directive", severity=severity
            )},
            "source_allowlist": [],
        },
        True,
    )
    event = framework.parse_payload(_event_payload("Read", raw))

    result = scanner_script.handle_event(event, config, repo_root=tmp_path)

    assert event.tool_output == raw
    assert result.action == "warn"
    assert "fixture-warn" in result.additional_context
    assert "fixture-category" in result.additional_context
    assert "Treat the source as untrusted" in result.additional_context
    assert raw not in result.additional_context


def test_ac8_truncation_notice_combines_with_warning(scanner_script, framework, tmp_path) -> None:
    config = framework.ConfigSnapshot(
        {
            "rules": {"fixture-warn": _rule("fixture-warn", "fixture directive")},
            "source_allowlist": [],
        },
        True,
    )
    event = framework.parse_payload(_event_payload(
        "Grep", "fixture directive", tool_output_truncated=True
    ))

    result = scanner_script.handle_event(event, config, repo_root=tmp_path)

    assert result.action == "warn"
    assert "unscanned tail" in result.additional_context


def test_ac8_binary_notice_does_not_crash(scanner_script, framework, tmp_path) -> None:
    config = framework.ConfigSnapshot(
        {"rules": {"fixture": _rule("fixture", "fixture directive")}, "source_allowlist": []},
        True,
    )
    event = framework.parse_payload(_event_payload("Read", b"\xff"))

    result = scanner_script.handle_event(event, config, repo_root=tmp_path)

    assert result.action == "warn"
    assert "binary" in result.additional_context


def test_ac8_empty_output_takes_fast_allow_path(scanner_script, framework, tmp_path) -> None:
    config = framework.ConfigSnapshot({"rules": {}, "source_allowlist": []}, True)
    event = framework.parse_payload(_event_payload("Read", ""))

    result = scanner_script.handle_event(event, config, repo_root=tmp_path)

    assert result.action == "allow"


def test_ac7_allowlisted_read_bypasses_scanning(scanner_script, framework, tmp_path) -> None:
    source = tmp_path / "docs" / "inspiration" / "survey.md"
    source.parent.mkdir(parents=True)
    source.write_text("fixture directive", encoding="utf-8")
    config = framework.ConfigSnapshot(
        {
            "rules": {"fixture-high": _rule(
                "fixture-high", "fixture directive", response_action="block", severity="high"
            )},
            "source_allowlist": ["docs/inspiration"],
        },
        True,
    )
    event = framework.parse_payload(_event_payload(
        "Read", "fixture directive", tool_input={"file_path": str(source)}
    ))

    result = scanner_script.handle_event(event, config, repo_root=tmp_path)

    assert result.action == "allow"


def test_ac9_entrypoint_failure_and_project_override_postures(
    scanner_script, framework
) -> None:
    payload = json.dumps(_event_payload("Read", "fixture directive"))
    failed = io.StringIO()
    scanner_script.run(
        input_stream=io.StringIO(payload),
        output_stream=failed,
        config_loader=lambda: (_ for _ in ()).throw(RuntimeError("SECRET")),
    )
    disabled = io.StringIO()
    scanner_script.run(
        input_stream=io.StringIO(payload),
        output_stream=disabled,
        config_loader=lambda: framework.ConfigSnapshot({}, False),
    )

    assert json.loads(failed.getvalue()) == {"decision": "block", "reason": "guard error"}
    assert json.loads(disabled.getvalue()) == {}


def test_ac9_scanner_processing_failure_is_redacted(
    scanner_script, framework, monkeypatch
) -> None:
    sentinel = "SCANNER_PROCESSING_SECRET"
    config = framework.ConfigSnapshot(
        {"rules": {"fixture": _rule("fixture", "fixture directive")}, "source_allowlist": []},
        True,
    )
    monkeypatch.setattr(
        scanner_script,
        "scan_output",
        lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError(sentinel)),
    )
    output = io.StringIO()

    scanner_script.run(
        input_stream=io.StringIO(json.dumps(_event_payload("Read", "ordinary"))),
        output_stream=output,
        config_loader=lambda: config,
    )

    assert json.loads(output.getvalue()) == {"decision": "block", "reason": "guard error"}
    assert sentinel not in output.getvalue()


def test_ac10_recorded_payloads_cover_supported_tools_and_entrypoint(
    scanner_script, framework, tmp_path
) -> None:
    payloads = json.loads(PAYLOADS_PATH.read_text(encoding="utf-8"))
    assert {case["tool_name"] for case in payloads} == {
        "Read", "Bash", "Grep", "WebFetch", "WebSearch", "Task", "mcp__fixture__read"
    }
    config = framework.ConfigSnapshot(
        {"rules": {"fixture": _rule("fixture", "fixture directive")}, "source_allowlist": []},
        True,
    )
    for index, payload in enumerate(payloads):
        output = io.StringIO()
        exit_code = scanner_script.run(
            input_stream=io.StringIO(json.dumps(payload)),
            output_stream=output,
            config_loader=lambda: config,
            repo_root=tmp_path,
        )
        assert exit_code == 0, index
        assert len(output.getvalue().splitlines()) == 1, index
        assert "fixture directive" not in output.getvalue(), index


def test_ac10_hook_registration_is_post_tool_use_only() -> None:
    definition = json.loads(HOOK_DEFINITION_PATH.read_text(encoding="utf-8"))
    assert set(definition["hooks"]) == {"PostToolUse"}
    matcher = definition["hooks"]["PostToolUse"][0]["matcher"]
    for tool in ("Read", "Bash", "Grep", "WebFetch", "WebSearch", "Task"):
        assert tool in matcher
    assert "mcp__" in matcher


def test_ac7_self_hook_assets_protect_new_scanner_configuration(framework, tmp_path) -> None:
    hooks_dir = HOOKS_DIR
    sys.path.insert(0, str(hooks_dir))
    try:
        from lib.file_access import evaluate_path, load_rules
    finally:
        sys.path.pop(0)
    config = json.loads((HOOKS_DIR / "config" / "file-access-rules.json").read_text(encoding="utf-8"))
    rules = load_rules(config)
    for path in (
        ALLOWLIST_PATH,
        HOOKS_DIR / "config" / "injection-patterns.json",
        HOOKS_DIR / "config" / "injection-future-corpus.json",
    ):
        decision = evaluate_path(path, rules, cwd=REPO_ROOT, access="write")
        assert decision is not None
        assert (decision.rule_id, decision.action) == ("self-hook-assets", "deny")


def test_scanner_runtime_is_stdlib_only_and_contains_no_production_policy() -> None:
    tree = ast.parse(ENGINE_PATH.read_text(encoding="utf-8"))
    imported_roots = set()
    literals = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_roots.add(node.module.split(".")[0])
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            literals.add(node.value.casefold())

    assert imported_roots <= sys.stdlib_module_names
    assert not any("ignore previous" in value for value in literals)
    assert not any("system prompt" in value for value in literals)


def test_scanner_representative_workload_median_is_below_budget(scanner) -> None:
    rules = _rules(scanner, _rule("fixture", "fixture directive"))
    output = "ordinary fixture text " * 2_000
    samples = []
    for _ in range(100):
        started = time.perf_counter_ns()
        scanner.scan_output(output, rules)
        samples.append((time.perf_counter_ns() - started) / 1_000_000)

    assert median(samples) < 50


def test_entrypoint_imports_without_cwd_or_pythonpath(tmp_path) -> None:
    code = (
        "import importlib.util,io,json,pathlib;"
        f"p=pathlib.Path({str(SCRIPT_PATH)!r});"
        "s=importlib.util.spec_from_file_location('isolated_scanner',p);"
        "m=importlib.util.module_from_spec(s);s.loader.exec_module(m);"
        "cfg=m.ConfigSnapshot({'rules':{},'source_allowlist':[]},True);"
        "payload=json.dumps({'hook_event_name':'PostToolUse','tool_name':'Read',"
        "'tool_input':{},'tool_output':'','tool_output_truncated':False});"
        "raise SystemExit(m.run(io.StringIO(payload),config_loader=lambda:cfg))"
    )

    result = subprocess.run(
        [sys.executable, "-I", "-c", code],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert json.loads(result.stdout) == {}
    assert result.stderr == ""
