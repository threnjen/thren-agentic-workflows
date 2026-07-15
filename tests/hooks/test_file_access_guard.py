from __future__ import annotations

import ast
import importlib.util
import io
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]
HOOKS_DIR = REPO_ROOT / ".github" / "hooks"
ENGINE_PATH = HOOKS_DIR / "lib" / "file_access.py"
URL_ANALYZER_PATH = HOOKS_DIR / "lib" / "url_exfiltration.py"
SCRIPT_PATH = HOOKS_DIR / "scripts" / "file-access-guard.py"
RULES_PATH = HOOKS_DIR / "config" / "file-access-rules.json"
OVERRIDES_PATH = HOOKS_DIR / "config" / "file-access-overrides.json"
HOOK_DEFINITION_PATH = HOOKS_DIR / "file-access-guard.json"
DOC_PATH = REPO_ROOT / "docs" / "hooks" / "file-access-guard.md"
URL_FIXTURE_PATH = (
    Path(__file__).with_name("fixtures")
    / "url_exfiltration"
    / "recorded_payloads.json"
)


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def file_access():
    return _load_module(ENGINE_PATH, "phase01_file_access")


@pytest.fixture(scope="module")
def guard_script():
    return _load_module(SCRIPT_PATH, "phase01_file_access_guard")


@pytest.fixture(scope="module")
def default_config():
    return json.loads(RULES_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def url_exfiltration():
    return _load_module(URL_ANALYZER_PATH, "phase02_url_exfiltration")


def test_ac1_default_rules_have_data_driven_tier_schema(default_config) -> None:
    rules = default_config["rules"]

    assert rules
    for rule_id, rule in rules.items():
        assert rule["id"] == rule_id
        assert rule["action"] in {"allow", "ask", "deny"}
        assert rule["reason"].strip()
        assert rule["matcher"] in {"basename", "basename_glob", "path_suffix", "path_glob"}
        assert rule["pattern"].strip()
        assert isinstance(rule["priority"], int)
        if "escalate_in_bypass" in rule:
            assert rule["escalate_in_bypass"] == "deny"


@pytest.mark.parametrize(
    "rule",
    [
        {"id": "bad", "action": "allow", "matcher": "basename", "pattern": "x"},
        {
            "id": "bad",
            "action": "permit",
            "reason": "invalid action",
            "matcher": "basename",
            "pattern": "x",
        },
    ],
)
def test_ac1_invalid_rule_configuration_is_rejected(file_access, rule) -> None:
    with pytest.raises(file_access.RuleConfigError):
        file_access.load_rules({"rules": {"bad": rule}})


def test_ac1_engine_contains_no_concrete_protected_file_policy() -> None:
    tree = ast.parse(ENGINE_PATH.read_text(encoding="utf-8"))
    string_literals = {
        node.value for node in ast.walk(tree) if isinstance(node, ast.Constant) and isinstance(node.value, str)
    }

    assert ".env" not in string_literals
    assert "id_rsa" not in string_literals
    assert ".ssh" not in string_literals


def _decision_for(guard_script, framework, tool_name, tool_input, tmp_path, **context):
    event = framework.parse_payload(
        {"tool_name": tool_name, "tool_input": tool_input, **context}
    )
    config = framework.load_config(RULES_PATH, OVERRIDES_PATH)
    return guard_script.handle_event(
        event,
        config,
        cwd=tmp_path,
        home=tmp_path,
        case_sensitive=True,
        recorder=lambda *args, **kwargs: None,
    )


@pytest.mark.parametrize(
    ("tool_name", "path_field"),
    [
        ("Read", "file_path"),
        ("Edit", "file_path"),
        ("Write", "file_path"),
        ("MultiEdit", "file_path"),
        ("NotebookEdit", "notebook_path"),
    ],
)
@pytest.mark.parametrize("protected_name", [".env", ".env.local", ".env.production"])
def test_ac2_all_file_tools_deny_environment_variants(
    guard_script, framework, tmp_path, tool_name, path_field, protected_name
) -> None:
    decision = _decision_for(
        guard_script, framework, tool_name, {path_field: protected_name}, tmp_path
    )

    assert decision.action == "deny"
    assert "environment-file" in decision.reason


@pytest.mark.parametrize("template", [".env.sample", ".env.example"])
def test_ac2_exact_environment_templates_are_allowed(
    guard_script, framework, tmp_path, template
) -> None:
    decision = _decision_for(
        guard_script, framework, "Read", {"file_path": template}, tmp_path
    )

    assert decision.action == "allow"


def test_ac2_template_prefix_does_not_broaden_exception(
    guard_script, framework, tmp_path
) -> None:
    decision = _decision_for(
        guard_script,
        framework,
        "Write",
        {"file_path": ".env.sample.extra", "content": "secret"},
        tmp_path,
    )

    assert decision.action == "deny"


@pytest.mark.parametrize(
    "protected_path",
    [
        "id_rsa",
        "id_ed25519",
        "id_ecdsa",
        "id_dsa",
        "client.pem",
        "client.key",
        "client.p12",
        "client.pfx",
        "credentials.json",
        "secrets.json",
        "service-account.json",
        "auth.json",
        "token.json",
        ".netrc",
        ".npmrc",
        ".pypirc",
        ".ssh/config",
        ".aws/credentials",
        ".kube/config",
        "kubeconfig",
        "cluster.kubeconfig",
        ".gnupg/private-keys-v1.d/key",
    ],
)
def test_ac3_credential_names_patterns_and_directories_are_denied(
    guard_script, framework, tmp_path, protected_path
) -> None:
    decision = _decision_for(
        guard_script, framework, "Read", {"file_path": protected_path}, tmp_path
    )

    assert decision.action == "deny"


def test_ac3_unrelated_id_prefix_is_allowed(
    guard_script, framework, tmp_path
) -> None:
    decision = _decision_for(
        guard_script, framework, "Read", {"file_path": "src/id_generator.py"}, tmp_path
    )

    assert decision.action == "allow"


@pytest.mark.parametrize("lock_path", ["package-lock.json", "yarn.lock", "poetry.lock"])
def test_ac4_lock_files_use_configured_ask_tier(
    guard_script, framework, tmp_path, lock_path
) -> None:
    decision = _decision_for(
        guard_script, framework, "Write", {"file_path": lock_path}, tmp_path
    )

    assert decision.action == "ask"
    assert "package manager" in decision.reason


def test_ac4_unrelated_name_containing_lock_is_allowed(
    guard_script, framework, tmp_path
) -> None:
    decision = _decision_for(
        guard_script, framework, "Read", {"file_path": "src/clock.py"}, tmp_path
    )

    assert decision.action == "allow"


@pytest.mark.parametrize(
    "production_path", ["config/production.json", "config/application.production.json"]
)
def test_ac4_production_configuration_is_denied(
    guard_script, framework, tmp_path, production_path
) -> None:
    decision = _decision_for(
        guard_script, framework, "Edit", {"file_path": production_path}, tmp_path
    )

    assert decision.action == "deny"
    assert "Production" in decision.reason


def test_ac4_project_override_can_add_user_rule_with_its_action_and_reason(
    guard_script, framework, tmp_path
) -> None:
    defaults = tmp_path / "defaults.json"
    override = tmp_path / "override.json"
    defaults.write_text(RULES_PATH.read_text(encoding="utf-8"), encoding="utf-8")
    override.write_text(
        json.dumps(
            {
                "rules": {
                    "project-personal-data": {
                        "id": "project-personal-data",
                        "action": "ask",
                        "reason": "Project owners require review",
                        "matcher": "path_suffix",
                        "pattern": "private/team.csv",
                        "priority": 80,
                        "safe_alternative": "Use a sanitized team fixture",
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    event = framework.parse_payload(
        {"tool_name": "Read", "tool_input": {"file_path": "private/team.csv"}}
    )

    decision = guard_script.handle_event(
        event,
        framework.load_config(defaults, override),
        cwd=tmp_path,
        case_sensitive=True,
        recorder=lambda *args, **kwargs: None,
    )

    assert decision.action == "ask"
    assert "project-personal-data" in decision.reason
    assert "Project owners require review" in decision.reason


def test_ac5_traversal_and_symlink_are_resolved_before_matching(
    guard_script, framework, tmp_path
) -> None:
    protected = tmp_path / "protected" / ".env"
    protected.parent.mkdir()
    protected.write_text("secret", encoding="utf-8")
    link = tmp_path / "safe-looking"
    link.symlink_to(protected)

    traversal = _decision_for(
        guard_script,
        framework,
        "Read",
        {"file_path": "nested/../protected/.env"},
        tmp_path,
    )
    symlink = _decision_for(
        guard_script, framework, "Read", {"file_path": str(link)}, tmp_path
    )

    assert traversal.action == symlink.action == "deny"
    assert str(protected.resolve()) in symlink.reason


def test_ac5_broken_symlink_resolves_conservatively(
    file_access, default_config, tmp_path
) -> None:
    broken = tmp_path / "apparently-safe"
    broken.symlink_to(tmp_path / ".env")

    match = file_access.evaluate_path(
        broken,
        file_access.load_rules(default_config),
        case_sensitive=True,
    )

    assert match is not None
    assert match.action == "deny"
    assert match.normalized_path.endswith("/.env")


def test_ac5_tilde_expands_against_supplied_home(file_access, tmp_path) -> None:
    normalized = file_access.normalize_path(
        "~/.aws/credentials", home=tmp_path, case_sensitive=True
    )

    assert normalized == (tmp_path / ".aws" / "credentials").resolve().as_posix()


def test_ac5_case_folding_is_controlled_by_filesystem_mode(
    file_access, default_config, tmp_path
) -> None:
    rules = file_access.load_rules(default_config)

    sensitive = file_access.evaluate_path(
        ".ENV", rules, cwd=tmp_path, case_sensitive=True
    )
    insensitive = file_access.evaluate_path(
        ".ENV", rules, cwd=tmp_path, case_sensitive=False
    )

    assert sensitive is None
    assert insensitive is not None and insensitive.action == "deny"


@pytest.mark.parametrize(
    "tool_input",
    [
        {"pattern": "token", "path": ".env"},
        {"pattern": "token", "glob": ".env*"},
        {"pattern": "token", "glob": "*.env"},
        {"pattern": "token", "path": "src", "glob": "*.pem"},
    ],
)
def test_ac6_grep_protected_path_or_glob_is_denied(
    guard_script, framework, tmp_path, tool_input
) -> None:
    decision = _decision_for(
        guard_script, framework, "Grep", tool_input, tmp_path
    )

    assert decision.action == "deny"


@pytest.mark.parametrize(
    "tool_input", [{"pattern": "needle", "path": "src"}, {"pattern": "needle"}]
)
def test_ac6_grep_without_protected_explicit_scope_is_allowed(
    guard_script, framework, tmp_path, tool_input
) -> None:
    decision = _decision_for(
        guard_script, framework, "Grep", tool_input, tmp_path
    )

    assert decision.action == "allow"


@pytest.mark.parametrize("protected_directory", [".ssh", ".aws", ".kube", ".gnupg"])
def test_ac6_grep_exact_protected_directory_scope_is_denied(
    guard_script, framework, tmp_path, protected_directory
) -> None:
    decision = _decision_for(
        guard_script,
        framework,
        "Grep",
        {"pattern": "needle", "path": protected_directory},
        tmp_path,
    )

    assert decision.action == "deny"


@pytest.mark.parametrize("protected_glob", ["prod*.*", "config/prod*.json"])
def test_ac6_grep_overlapping_protected_glob_is_denied(
    guard_script, framework, tmp_path, protected_glob
) -> None:
    decision = _decision_for(
        guard_script,
        framework,
        "Grep",
        {"pattern": "needle", "glob": protected_glob},
        tmp_path,
    )

    assert decision.action == "deny"


def test_ac6_ordinary_source_glob_remains_allowed(
    guard_script, framework, tmp_path
) -> None:
    decision = _decision_for(
        guard_script,
        framework,
        "Grep",
        {"pattern": "needle", "path": "src", "glob": "**/*.py"},
        tmp_path,
    )

    assert decision.action == "allow"


def test_ac6_malformed_guarded_grep_input_fails_closed(guard_script) -> None:
    output = io.StringIO()

    exit_code = guard_script.main(
        io.StringIO(
            json.dumps(
                {"tool_name": "Grep", "tool_input": {"pattern": "x", "path": [".env"]}}
            )
        ),
        output_stream=output,
    )

    result = json.loads(output.getvalue())["hookSpecificOutput"]
    assert exit_code == 0
    assert result["permissionDecision"] == "deny"
    assert result["permissionDecisionReason"] == "guard error"


def test_ac6_glob_tool_remains_outside_file_matcher(
    guard_script, framework, tmp_path
) -> None:
    decision = _decision_for(
        guard_script, framework, "Glob", {"pattern": ".env"}, tmp_path
    )
    definition = json.loads(HOOK_DEFINITION_PATH.read_text(encoding="utf-8"))
    matcher = definition["hooks"]["PreToolUse"][0]["matcher"]

    assert decision.action == "allow"
    assert "Glob" not in matcher.split("|")
    assert matcher == "Read|Edit|Write|MultiEdit|NotebookEdit|Grep|Bash|WebFetch"


@pytest.mark.parametrize(
    "self_protected_path",
    [
        ".github/hooks/scripts/file-access-guard.py",
        ".github/hooks/config/file-access-rules.json",
        ".github/hooks/config/file-access-overrides.json",
        ".github/hooks/file-access-guard.json",
        ".claude/settings.json",
        ".claude/settings.local.json",
        ".codex/hooks.json",
        ".opencode/plugins/file-access-guard.js",
    ],
)
def test_ac7_consuming_project_hook_assets_are_self_protected(
    guard_script, framework, tmp_path, self_protected_path
) -> None:
    decision = _decision_for(
        guard_script,
        framework,
        "Edit",
        {"file_path": self_protected_path},
        tmp_path,
    )

    assert decision.action == "deny"
    assert "self-" in decision.reason


def test_ac7_self_protection_does_not_block_read_only_inspection(
    guard_script, framework, tmp_path
) -> None:
    decision = _decision_for(
        guard_script,
        framework,
        "Read",
        {"file_path": ".github/hooks/config/file-access-rules.json"},
        tmp_path,
    )

    assert decision.action == "allow"


def test_ac7_symlink_alias_to_wiring_file_is_denied(
    guard_script, framework, tmp_path
) -> None:
    settings = tmp_path / ".codex" / "hooks.json"
    settings.parent.mkdir()
    settings.write_text("{}", encoding="utf-8")
    alias = tmp_path / "apparently-safe.json"
    alias.symlink_to(settings)

    decision = _decision_for(
        guard_script, framework, "Write", {"file_path": str(alias)}, tmp_path
    )

    assert decision.action == "deny"
    assert str(settings.resolve()) in decision.reason


@pytest.mark.parametrize(
    ("path", "expected_action", "expected_rule"),
    [(".env", "deny", "environment-file"), ("poetry.lock", "ask", "lock-file")],
)
def test_ac8_blocked_or_held_guidance_is_structured_and_actionable(
    guard_script, framework, tmp_path, path, expected_action, expected_rule
) -> None:
    decision = _decision_for(
        guard_script, framework, "Write", {"file_path": path}, tmp_path
    )

    assert decision.action == expected_action
    assert f"Rule {expected_rule}" in decision.reason
    assert str((tmp_path / path).resolve()) in decision.reason
    assert "Safe alternative:" in decision.reason


def test_ac8_decision_and_log_never_reflect_file_content_or_full_payload(
    guard_script, file_access, tmp_path
) -> None:
    sentinel = "FILE_BODY_SECRET_SENTINEL"
    output = io.StringIO()
    payload = {
        "tool_name": "Write",
        "tool_input": {
            "file_path": ".env",
            "content": sentinel,
            "nested": {"token": sentinel},
        },
        "cwd": str(tmp_path),
    }

    exit_code = guard_script.main(io.StringIO(json.dumps(payload)), output_stream=output)

    log_path = tmp_path / ".agent" / "logs" / "file-access-guard.ndjson"
    raw_log = log_path.read_text(encoding="utf-8")
    entry = json.loads(raw_log)
    assert exit_code == 0
    assert sentinel not in output.getvalue() + raw_log
    assert entry == {
        "timestamp": entry["timestamp"],
        "tool": "Write",
        "rule": "environment-file",
        "decision": "deny",
        "path": file_access.normalize_path(tmp_path / ".env"),
    }


def test_ac9_induced_evaluator_exception_becomes_redacted_guard_error(
    guard_script, monkeypatch
) -> None:
    sentinel = "EVALUATOR_EXCEPTION_SECRET"
    output = io.StringIO()
    monkeypatch.setattr(
        guard_script,
        "evaluate_path",
        lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError(sentinel)),
    )

    exit_code = guard_script.main(
        io.StringIO(json.dumps({"tool_name": "Read", "tool_input": {"file_path": ".env"}})),
        output_stream=output,
    )

    result = json.loads(output.getvalue())["hookSpecificOutput"]
    assert exit_code == 0
    assert result == {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "guard error",
    }
    assert sentinel not in output.getvalue()


def test_ac9_only_protected_override_can_disable_guard(
    guard_script, framework, tmp_path, monkeypatch
) -> None:
    defaults = tmp_path / "defaults.json"
    override = tmp_path / "override.json"
    defaults.write_text(RULES_PATH.read_text(encoding="utf-8"), encoding="utf-8")
    monkeypatch.setenv("HOOK_GUARD_ENABLED", "0")
    input_payload = json.dumps(
        {"tool_name": "Read", "tool_input": {"file_path": ".env"}, "cwd": str(tmp_path)}
    )

    environment_output = io.StringIO()
    framework.security_guard(
        guard_script.handle_event,
        input_stream=io.StringIO(input_payload),
        output_stream=environment_output,
        config_loader=lambda: framework.load_config(defaults, override),
    )
    override.write_text(json.dumps({"guard": {"enabled": False}}), encoding="utf-8")
    override_output = io.StringIO()
    framework.security_guard(
        guard_script.handle_event,
        input_stream=io.StringIO(input_payload),
        output_stream=override_output,
        config_loader=lambda: framework.load_config(defaults, override),
    )

    assert json.loads(environment_output.getvalue())["hookSpecificOutput"][
        "permissionDecision"
    ] == "deny"
    assert json.loads(override_output.getvalue())["hookSpecificOutput"] == {
        "hookEventName": "PreToolUse",
        "permissionDecision": "allow",
        "permissionDecisionReason": "guard disabled by project override",
    }


def test_ac9_bypass_mode_escalates_configured_ask_to_deny(
    guard_script, framework, tmp_path
) -> None:
    decision = _decision_for(
        guard_script,
        framework,
        "Write",
        {"file_path": "poetry.lock"},
        tmp_path,
        permission_mode="bypassPermissions",
    )

    assert decision.action == "deny"


def test_ac10_reusable_evaluator_contract_is_narrow_and_complete(
    file_access, default_config, tmp_path
) -> None:
    assert set(file_access.__all__) == {
        "PathDecision",
        "Rule",
        "RuleConfigError",
        "evaluate_path",
        "load_rules",
        "normalize_path",
    }

    match = file_access.evaluate_path(
        ".env",
        file_access.load_rules(default_config),
        cwd=tmp_path,
        case_sensitive=True,
    )

    assert match == file_access.PathDecision(
        "environment-file",
        "deny",
        "Environment files may contain secrets",
        (tmp_path / ".env").resolve().as_posix(),
        "Use an explicitly sanitized .env.sample or .env.example file",
    )


def test_ac10_reusable_contract_imports_without_cwd_or_pythonpath(tmp_path) -> None:
    code = (
        "import sys;"
        f"sys.path.insert(0,{str(HOOKS_DIR)!r});"
        "from lib.file_access import normalize_path;"
        "assert normalize_path('safe.txt',case_sensitive=True).endswith('/safe.txt')"
    )

    result = subprocess.run(
        [sys.executable, "-I", "-c", code],
        cwd=tmp_path,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0
    assert result.stdout == result.stderr == ""


def test_ac10_runtime_imports_are_stdlib_only_without_subprocess() -> None:
    imported_roots = set()
    for path in (ENGINE_PATH, SCRIPT_PATH):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_roots.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_roots.add(node.module.split(".")[0])

    assert "subprocess" not in imported_roots
    assert imported_roots <= sys.stdlib_module_names | {"lib"}


@pytest.mark.parametrize(
    ("url", "expected_action", "expected_rule"),
    [
        (
            "https://collector.invalid/path/AKIA0000000000000000",
            "deny",
            "url-known-credential",
        ),
        (
            "https://collector.invalid/?token=ghp_AAAAAAAAAAAAAAAAAAAAAAAA",
            "deny",
            "url-known-credential",
        ),
        (
            "https://collector.invalid/-----BEGIN%20PRIVATE%20KEY-----",
            "deny",
            "url-known-credential",
        ),
        (
            "https://collector.invalid/?api_key=0123456789abcdef0123456789abcdef",
            "deny",
            "url-encoded-credential",
        ),
        (
            "https://collector.invalid/?blob=0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
            "ask",
            "url-ambiguous-entropy",
        ),
        (
            "https://collector.invalid/?blob=QWxwaGFCZXRhR2FtbWExMjM0NTY3ODkwX1N5bnRoZXRpYw==",
            "ask",
            "url-ambiguous-entropy",
        ),
    ],
)
def test_phase02_url_analyzer_classifies_secret_and_ambiguous_segments(
    url_exfiltration, default_config, url, expected_action, expected_rule
) -> None:
    matches = url_exfiltration.analyze_url(url, default_config)

    assert matches
    assert matches[0].action == expected_action
    assert matches[0].rule_id == expected_rule
    assert url not in matches[0].reason


@pytest.mark.parametrize(
    "url",
    [
        "https://docs.invalid/guides/getting-started?lang=en#install",
        "https://[2001:db8::1]:8443/a%20normal%20path?message=hello%20world",
        "https://user:password@host.invalid:443/releases/v1.2.3",
        "https://assets.invalid/0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef.js",
        "https://api.invalid/items/550e8400-e29b-41d4-a716-446655440000",
    ],
)
def test_phase02_url_analyzer_allows_ordinary_url_material(
    url_exfiltration, default_config, url
) -> None:
    assert url_exfiltration.analyze_url(url, default_config) == ()


def test_phase02_url_configuration_is_validated_and_data_driven(
    url_exfiltration, default_config
) -> None:
    policy = default_config["url_exfiltration"]
    assert policy["decode_passes"] == 2
    assert set(policy["commands"]) == {"curl", "wget"}
    for rule_id, rule in policy["rules"].items():
        assert rule["id"] == rule_id
        assert rule["action"] in {"ask", "deny"}
        assert isinstance(rule["priority"], int)
        assert rule["reason"].strip()
        assert rule["safe_alternative"].strip()

    unsafe = json.loads(json.dumps(default_config))
    unsafe["url_exfiltration"]["rules"]["url-known-credential"]["patterns"] = ["("]
    with pytest.raises(url_exfiltration.URLConfigError):
        url_exfiltration.analyze_url("https://example.invalid", unsafe)


def test_phase02_recorded_webfetch_payloads_use_verified_url_field_and_posture(
    guard_script, framework, tmp_path
) -> None:
    fixtures = json.loads(URL_FIXTURE_PATH.read_text(encoding="utf-8"))
    assert fixtures
    for case in fixtures:
        payload = case["payload"]
        assert payload["tool_name"] == "WebFetch"
        event = framework.parse_payload(payload)
        if case["expected_action"] == "guard-error":
            with pytest.raises((ValueError, TypeError)):
                guard_script.handle_event(
                    event,
                    framework.load_config(RULES_PATH, OVERRIDES_PATH),
                    cwd=tmp_path,
                    recorder=lambda *args, **kwargs: None,
                )
        else:
            decision = guard_script.handle_event(
                event,
                framework.load_config(RULES_PATH, OVERRIDES_PATH),
                cwd=tmp_path,
                recorder=lambda *args, **kwargs: None,
            )
            assert decision.action == case["expected_action"]


def test_phase02_webfetch_bypass_escalates_ambiguous_url_to_deny(
    guard_script, framework, tmp_path
) -> None:
    decision = _decision_for(
        guard_script,
        framework,
        "WebFetch",
        {
            "url": "https://collector.invalid/?blob=0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
        },
        tmp_path,
        permission_mode="bypassPermissions",
    )

    assert decision.action == "deny"
    assert "url-ambiguous-entropy" in decision.reason


@pytest.mark.parametrize(
    "tool_input",
    [
        {},
        {"url": ["WEBFETCH_INPUT_SECRET_SENTINEL"]},
        {"url": "https://collector.invalid/%ZZWEBFETCH_INPUT_SECRET_SENTINEL"},
    ],
)
def test_phase02_malformed_webfetch_input_fails_closed_without_reflection(
    guard_script, tool_input
) -> None:
    output = io.StringIO()
    error = io.StringIO()

    exit_code = guard_script.main(
        io.StringIO(json.dumps({"tool_name": "WebFetch", "tool_input": tool_input})),
        output_stream=output,
        error_stream=error,
    )

    result = json.loads(output.getvalue())["hookSpecificOutput"]
    assert exit_code == 0
    assert result["permissionDecision"] == "deny"
    assert result["permissionDecisionReason"] == "guard error"
    assert "WEBFETCH_INPUT_SECRET_SENTINEL" not in output.getvalue() + error.getvalue()


def test_phase02_webfetch_decision_and_audit_are_fully_redacted(tmp_path) -> None:
    url = "https://secret-host.invalid/private/AKIA0000000000000000?secret_query_name_sentinel=SECRET_QUERY_SENTINEL"
    payload = {
        "tool_name": "WebFetch",
        "tool_input": {"url": url},
        "cwd": str(tmp_path),
    }
    output = io.StringIO()
    error = io.StringIO()
    guard_script = _load_module(SCRIPT_PATH, "phase02_redaction_guard")

    exit_code = guard_script.main(
        io.StringIO(json.dumps(payload)), output_stream=output, error_stream=error
    )

    audit = (tmp_path / ".agent/logs/file-access-guard.ndjson").read_text(
        encoding="utf-8"
    )
    rendered = output.getvalue() + error.getvalue() + audit
    assert exit_code == 0
    for sentinel in (
        url,
        "secret-host.invalid",
        "private",
        "secret_query_name_sentinel",
        "SECRET_QUERY_SENTINEL",
        "AKIA0000000000000000",
    ):
        assert sentinel not in rendered
    entry = json.loads(audit)
    assert set(entry) == {"timestamp", "tool", "rule", "decision"}
    assert entry["tool"] == "WebFetch"
    assert entry["rule"] == "url-known-credential"
    assert entry["decision"] == "deny"


def test_phase02_webfetch_matcher_is_exactly_wired() -> None:
    definition = json.loads(HOOK_DEFINITION_PATH.read_text(encoding="utf-8"))
    hook = definition["hooks"]["PreToolUse"][0]

    assert hook["matcher"].split("|") == [
        "Read",
        "Edit",
        "Write",
        "MultiEdit",
        "NotebookEdit",
        "Grep",
        "Bash",
        "WebFetch",
    ]
    assert hook["timeout"] == 10


def test_phase02_url_analyzer_is_stdlib_only_and_network_free() -> None:
    tree = ast.parse(URL_ANALYZER_PATH.read_text(encoding="utf-8"))
    imported_roots = set()
    calls = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_roots.add(node.module.split(".")[0])
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            calls.add(node.func.id)

    assert imported_roots <= sys.stdlib_module_names
    assert not {"urlopen", "socket", "system", "popen", "run"} & calls
