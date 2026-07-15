from __future__ import annotations

import ast
import importlib.util
import io
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from statistics import median

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]
AUDIT_SCRIPT_PATH = REPO_ROOT / ".github" / "hooks" / "scripts" / "audit-log.py"
AUDIT_WRAPPER_PATH = REPO_ROOT / ".github" / "hooks" / "scripts" / "audit-log.sh"
VERIFICATION_DOC_PATH = REPO_ROOT / "docs" / "hooks" / "hook-verification.md"

PUBLIC_API = (
    "HookEvent",
    "Decision",
    "PostToolResult",
    "ConfigSnapshot",
    "PayloadError",
    "ConfigError",
    "parse_payload",
    "make_decision",
    "emit_decision",
    "make_post_tool_result",
    "emit_post_tool_result",
    "load_config",
    "security_guard",
    "post_tool_security_guard",
    "observability_guard",
    "record_event",
)
SCANNER_PUBLIC_API = (
    "InjectionConfigError",
    "InjectionRule",
    "MatchMetadata",
    "ScanResult",
    "load_injection_rules",
    "scan_output",
)


def _load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_public_framework_contract_is_exposed(framework) -> None:
    missing = [name for name in PUBLIC_API if not hasattr(framework, name)]

    assert missing == []


def test_recorded_payload_aliases_are_normalized(framework, recorded_payloads) -> None:
    normalized = [
        (event.tool_name, event.tool_input)
        for event in (framework.parse_payload(case["payload"]) for case in recorded_payloads)
    ]
    expected = [
        (case["expected_tool"], case["expected_input"]) for case in recorded_payloads
    ]

    assert normalized == expected


def test_recorded_fixtures_cover_every_phase_one_tool_and_event_context(
    framework, recorded_payloads
) -> None:
    assert {case["expected_tool"] for case in recorded_payloads} == {
        "Read", "Edit", "Write", "MultiEdit", "NotebookEdit", "Grep", "Bash"
    }

    event = framework.parse_payload(recorded_payloads[0]["payload"])
    assert event.context["session_id"] == "fixture-session"


@pytest.mark.parametrize("source_kind", ["json-text", "text-stream"])
def test_payload_parser_accepts_serialized_input(
    framework, recorded_payloads, source_kind
) -> None:
    serialized = json.dumps(recorded_payloads[0]["payload"])
    source = serialized if source_kind == "json-text" else io.StringIO(serialized)

    event = framework.parse_payload(source)

    assert (event.tool_name, event.tool_input) == (
        recorded_payloads[0]["expected_tool"],
        recorded_payloads[0]["expected_input"],
    )


def test_post_tool_payload_preserves_raw_and_structured_output(framework) -> None:
    raw = framework.parse_payload({
        "hook_event_name": "PostToolUse",
        "tool_name": "Read",
        "tool_input": {"file_path": "fixture.txt"},
        "tool_output": "raw fixture output",
        "tool_output_truncated": False,
    })
    structured_output = {"items": ["one", {"two": 2}]}
    structured = framework.parse_payload({
        "hook_event_name": "PostToolUse",
        "tool_name": "mcp__fixture__read",
        "tool_input": {},
        "tool_output": structured_output,
        "tool_output_truncated": True,
        "agent_id": "fixture-agent",
        "agent_type": "subagent",
    })

    assert raw.tool_output == "raw fixture output"
    assert raw.tool_output_truncated is False
    assert structured.tool_output == structured_output
    assert structured.tool_output is not structured_output
    assert structured.tool_output_truncated is True
    assert (structured.agent_id, structured.agent_type) == (
        "fixture-agent", "subagent"
    )


@pytest.mark.parametrize(
    "field,value",
    [
        ("tool_output", None),
        ("tool_output_truncated", "false"),
        ("agent_id", 12),
        ("agent_type", []),
    ],
)
def test_invalid_post_tool_fields_raise_payload_error(framework, field, value) -> None:
    payload = {
        "hook_event_name": "PostToolUse",
        "tool_name": "Read",
        "tool_input": {},
        "tool_output": "fixture output",
        "tool_output_truncated": False,
    }
    if field == "tool_output":
        payload.pop(field)
    else:
        payload[field] = value

    with pytest.raises(framework.PayloadError):
        framework.parse_payload(payload)


@pytest.mark.parametrize(
    "payload",
    ["", "{not-json", b"\xff", {}, {"tool_name": "Read"}, {"tool_input": {}}],
    ids=[
        "empty", "malformed", "invalid-utf8", "empty-object", "missing-input",
        "missing-tool",
    ],
)
def test_invalid_payloads_raise_payload_error(framework, payload) -> None:
    with pytest.raises(framework.PayloadError):
        framework.parse_payload(payload)


@pytest.mark.parametrize("action", ["allow", "ask", "deny"])
def test_decision_factory_supports_each_action(framework, action) -> None:
    decision = framework.make_decision(action, "fixture reason")

    assert (decision.action, decision.reason) == (action, "fixture reason")


@pytest.mark.parametrize("action", ["allow", "ask", "deny"])
def test_decision_emitter_writes_one_structured_result(framework, action) -> None:
    output = io.StringIO()

    exit_code = framework.emit_decision(
        framework.make_decision(action, "fixture reason"), output_stream=output
    )

    lines = output.getvalue().splitlines()
    assert exit_code == 0
    assert len(lines) == 1
    assert json.loads(lines[0]) == {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": action,
            "permissionDecisionReason": "fixture reason",
        }
    }


def test_denial_can_use_exit_code_two_fallback(framework) -> None:
    output = io.StringIO()
    error_output = io.StringIO()

    exit_code = framework.emit_decision(
        framework.make_decision("deny", "guard unavailable"),
        output_stream=output,
        error_stream=error_output,
        use_exit_code_fallback=True,
    )

    assert exit_code == 2
    assert output.getvalue() == ""
    assert error_output.getvalue() == "guard unavailable\n"


def test_decision_emitter_rejects_invalid_direct_decision(framework) -> None:
    with pytest.raises(ValueError, match="decision action"):
        framework.emit_decision(
            framework.Decision("permit", "invalid action"),
            output_stream=io.StringIO(),
        )


def test_post_tool_block_suppresses_output_with_redacted_reason(framework) -> None:
    output = io.StringIO()

    exit_code = framework.emit_post_tool_result(
        framework.make_post_tool_result("block", reason="redacted fixture reason"),
        output_stream=output,
    )

    assert exit_code == 0
    assert json.loads(output.getvalue()) == {
        "decision": "block",
        "reason": "redacted fixture reason",
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "updatedToolOutput": "redacted fixture reason",
        },
    }


def test_post_tool_warning_appends_context_without_replacing_output(framework) -> None:
    output = io.StringIO()

    exit_code = framework.emit_post_tool_result(
        framework.make_post_tool_result(
            "warn", additional_context="redacted fixture warning"
        ),
        output_stream=output,
    )

    assert exit_code == 0
    assert json.loads(output.getvalue()) == {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": "redacted fixture warning",
        }
    }


def test_post_tool_emitter_revalidates_directly_constructed_result(framework) -> None:
    with pytest.raises(ValueError, match="post-tool action"):
        framework.emit_post_tool_result(
            framework.PostToolResult("replace", "bad", "bad"),
            output_stream=io.StringIO(),
        )


def test_post_tool_security_guard_fails_closed_without_reflecting_failure(
    framework,
) -> None:
    output = io.StringIO()
    sentinel = "POST_TOOL_FAILURE_SECRET"

    exit_code = framework.post_tool_security_guard(
        lambda event, config: (_ for _ in ()).throw(RuntimeError(sentinel)),
        input_stream=io.StringIO(json.dumps({
            "hook_event_name": "PostToolUse",
            "tool_name": "Read",
            "tool_input": {},
            "tool_output": sentinel,
            "tool_output_truncated": False,
        })),
        output_stream=output,
    )

    assert exit_code == 0
    assert json.loads(output.getvalue()) == {
        "decision": "block",
        "reason": "guard error",
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "updatedToolOutput": "guard error",
        },
    }
    assert sentinel not in output.getvalue()


def test_post_tool_output_failure_uses_blocking_fallback(framework) -> None:
    class FailingOutput:
        def write(self, _content):
            raise OSError("POST_OUTPUT_SECRET")

    error_output = io.StringIO()
    exit_code = framework.post_tool_security_guard(
        lambda event, config: framework.make_post_tool_result("allow"),
        input_stream=io.StringIO(json.dumps({
            "hook_event_name": "PostToolUse",
            "tool_name": "Read",
            "tool_input": {},
            "tool_output": "ordinary",
            "tool_output_truncated": False,
        })),
        output_stream=FailingOutput(),
        error_stream=error_output,
    )

    assert exit_code == 2
    assert error_output.getvalue() == "guard error\n"


def _write_json(path, payload) -> None:
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_config_override_precedence_uses_recursive_merge(framework, tmp_path) -> None:
    defaults = tmp_path / "defaults.json"
    override = tmp_path / "override.json"
    _write_json(
        defaults,
        {"rules": {"alpha": {"action": "deny", "reason": "default"}}, "mode": "base"},
    )
    _write_json(override, {"rules": {"alpha": {"reason": "project"}}})

    snapshot = framework.load_config(defaults, override)

    assert snapshot.data == {
        "rules": {"alpha": {"action": "deny", "reason": "project"}},
        "mode": "base",
    }


def test_config_cache_hits_and_invalidates_on_mtime_change(framework, tmp_path) -> None:
    defaults = tmp_path / "defaults.json"
    override = tmp_path / "override.json"
    _write_json(defaults, {"version": 1})

    first = framework.load_config(defaults, override)
    cached = framework.load_config(defaults, override)
    _write_json(defaults, {"version": 2})
    stat = defaults.stat()
    os.utime(defaults, ns=(stat.st_atime_ns, stat.st_mtime_ns + 1_000_000_000))
    refreshed = framework.load_config(defaults, override)

    assert cached is first
    assert refreshed is not first
    assert refreshed.data["version"] == 2


def test_config_cache_is_scoped_by_resolved_paths(framework, tmp_path) -> None:
    first_defaults = tmp_path / "first" / "defaults.json"
    second_defaults = tmp_path / "second" / "defaults.json"
    first_defaults.parent.mkdir()
    second_defaults.parent.mkdir()
    _write_json(first_defaults, {"project": "first"})
    _write_json(second_defaults, {"project": "second"})

    first = framework.load_config(first_defaults)
    second = framework.load_config(second_defaults)

    assert first.data == {"project": "first"}
    assert second.data == {"project": "second"}


def test_cached_config_snapshot_cannot_be_mutated(framework, tmp_path) -> None:
    defaults = tmp_path / "defaults.json"
    _write_json(defaults, {"rules": {"alpha": {"action": "deny"}}})
    snapshot = framework.load_config(defaults)

    with pytest.raises(TypeError):
        snapshot.data["rules"]["alpha"]["action"] = "allow"


def test_missing_config_files_load_as_empty_layers(framework, tmp_path) -> None:
    snapshot = framework.load_config(
        tmp_path / "missing-defaults.json", tmp_path / "missing-override.json"
    )

    assert snapshot.data == {}
    assert snapshot.guard_enabled is True


def test_invalid_config_error_never_reflects_content(framework, tmp_path) -> None:
    sentinel = "CONFIG_SECRET_SENTINEL"
    defaults = tmp_path / "defaults.json"
    defaults.write_text(f'{{"token":"{sentinel}"', encoding="utf-8")

    with pytest.raises(framework.ConfigError) as error:
        framework.load_config(defaults)

    assert sentinel not in str(error.value)


@pytest.mark.parametrize("failure_stage", ["payload", "config", "handler"])
def test_security_guard_fails_closed_with_redacted_denial(
    framework, failure_stage
) -> None:
    sentinel = "SECURITY_EXCEPTION_SECRET"
    output = io.StringIO()
    input_stream = io.StringIO("{broken" if failure_stage == "payload" else json.dumps({
        "tool_name": "Read", "tool_input": {"file_path": "safe.txt"}
    }))

    def config_loader():
        if failure_stage == "config":
            raise RuntimeError(sentinel)
        return framework.ConfigSnapshot({}, True)

    def handler(event, config):
        if failure_stage == "handler":
            raise RuntimeError(sentinel)
        return framework.make_decision("allow", "safe")

    exit_code = framework.security_guard(
        handler,
        input_stream=input_stream,
        output_stream=output,
        config_loader=config_loader,
    )

    result = json.loads(output.getvalue())
    assert exit_code == 0
    assert result["hookSpecificOutput"]["permissionDecision"] == "deny"
    assert result["hookSpecificOutput"]["permissionDecisionReason"] == "guard error"
    assert sentinel not in output.getvalue()


def test_security_output_failure_uses_blocking_fallback(framework) -> None:
    class FailingOutput:
        def write(self, _content):
            raise OSError("OUTPUT_SECRET_SENTINEL")

    error_output = io.StringIO()
    exit_code = framework.security_guard(
        lambda event, config: framework.make_decision("allow", "safe"),
        input_stream=io.StringIO(json.dumps({
            "tool_name": "Read", "tool_input": {"file_path": "safe.txt"}
        })),
        output_stream=FailingOutput(),
        error_stream=error_output,
    )

    assert exit_code == 2
    assert error_output.getvalue() == "guard error\n"


def test_security_guard_fails_closed_for_invalid_direct_decision(framework) -> None:
    output = io.StringIO()

    exit_code = framework.security_guard(
        lambda event, config: framework.Decision("permit", "invalid action"),
        input_stream=io.StringIO(json.dumps({
            "tool_name": "Read", "tool_input": {"file_path": "safe.txt"}
        })),
        output_stream=output,
    )

    result = json.loads(output.getvalue())["hookSpecificOutput"]
    assert exit_code == 0
    assert result["permissionDecision"] == "deny"
    assert result["permissionDecisionReason"] == "guard error"


def test_post_tool_payload_accepts_codex_response_alias_without_truncation_flag(
    framework,
) -> None:
    sentinel = "CODEX_TOOL_RESPONSE_SENTINEL"

    event = framework.parse_payload(
        {
            "hook_event_name": "PostToolUse",
            "turn_id": "turn-1",
            "tool_name": "Bash",
            "tool_input": {"command": "printf fixture"},
            "tool_response": {"output": sentinel},
        }
    )

    assert event.tool_output == {"output": sentinel}
    assert event.tool_output_truncated is False


def test_claude_post_tool_block_replaces_original_output(framework) -> None:
    sentinel = "CLAUDE_BLOCKED_OUTPUT_SENTINEL"
    output = io.StringIO()

    exit_code = framework.post_tool_security_guard(
        lambda event, config: framework.make_post_tool_result(
            "block",
            reason="redacted block reason",
            updated_tool_output={"stdout": "redacted block reason", "stderr": ""},
        ),
        input_stream=io.StringIO(
            json.dumps(
                {
                    "hook_event_name": "PostToolUse",
                    "tool_name": "Bash",
                    "tool_input": {"command": "printf fixture"},
                    "tool_output": {"stdout": sentinel, "stderr": ""},
                    "tool_output_truncated": False,
                }
            )
        ),
        output_stream=output,
    )

    emitted = json.loads(output.getvalue())
    assert exit_code == 0
    assert emitted["decision"] == "block"
    assert emitted["hookSpecificOutput"]["updatedToolOutput"] == {
        "stdout": "redacted block reason",
        "stderr": "",
    }
    assert sentinel not in output.getvalue()


def test_codex_post_tool_block_uses_native_feedback_replacement_without_claude_field(
    framework,
) -> None:
    output = io.StringIO()

    framework.post_tool_security_guard(
        lambda event, config: framework.make_post_tool_result(
            "block",
            reason="redacted block reason",
            updated_tool_output={"output": "redacted block reason"},
        ),
        input_stream=io.StringIO(
            json.dumps(
                {
                    "hook_event_name": "PostToolUse",
                    "turn_id": "turn-1",
                    "tool_name": "Bash",
                    "tool_input": {"command": "printf fixture"},
                    "tool_response": {"output": "CODEX_SENTINEL"},
                }
            )
        ),
        output_stream=output,
    )

    emitted = json.loads(output.getvalue())
    assert emitted == {"decision": "block", "reason": "redacted block reason"}


@pytest.mark.parametrize("failure_stage", ["payload", "config", "handler"])
def test_observability_guard_fails_open_without_output(framework, failure_stage) -> None:
    sentinel = "OBSERVABILITY_EXCEPTION_SECRET"
    input_stream = io.StringIO("{broken" if failure_stage == "payload" else json.dumps({
        "tool_name": "Read", "tool_input": {"file_path": "safe.txt"}
    }))
    calls = []

    def config_loader():
        if failure_stage == "config":
            raise RuntimeError(sentinel)
        return framework.ConfigSnapshot({}, True)

    def handler(event, config):
        calls.append(event.tool_name)
        if failure_stage == "handler":
            raise RuntimeError(sentinel)

    exit_code = framework.observability_guard(
        handler, input_stream=input_stream, config_loader=config_loader
    )

    assert exit_code == 0
    assert calls == (["Read"] if failure_stage == "handler" else [])


def test_only_project_override_can_disable_security_guard(
    framework, tmp_path, monkeypatch
) -> None:
    defaults = tmp_path / "defaults.json"
    override = tmp_path / "override.json"
    _write_json(defaults, {"guard": {"enabled": False}})
    monkeypatch.setenv("HOOK_GUARD_ENABLED", "0")

    defaults_only = framework.load_config(defaults)
    _write_json(override, {"guard": {"enabled": False}})
    project_disabled = framework.load_config(defaults, override)

    assert defaults_only.guard_enabled is True
    assert project_disabled.guard_enabled is False


def test_invalid_project_kill_switch_value_is_rejected(framework, tmp_path) -> None:
    defaults = tmp_path / "defaults.json"
    override = tmp_path / "override.json"
    _write_json(defaults, {})
    _write_json(override, {"guard": {"enabled": "no"}})

    with pytest.raises(framework.ConfigError):
        framework.load_config(defaults, override)


def test_disabled_security_guard_skips_handler_and_allows(framework) -> None:
    output = io.StringIO()
    calls = []

    def handler(event, config):
        calls.append(event.tool_name)
        return framework.make_decision("deny", "should not run")

    exit_code = framework.security_guard(
        handler,
        input_stream=io.StringIO(json.dumps({
            "tool_name": "Read", "tool_input": {"file_path": "safe.txt"}
        })),
        output_stream=output,
        config_loader=lambda: framework.ConfigSnapshot({}, False),
    )

    result = json.loads(output.getvalue())["hookSpecificOutput"]
    assert exit_code == 0
    assert calls == []
    assert result["permissionDecision"] == "allow"
    assert result["permissionDecisionReason"] == "guard disabled by project override"


@pytest.mark.parametrize("tool_name", ["Write", "Bash"])
def test_redacted_event_record_contains_only_allowlisted_metadata(
    framework, tmp_path, tool_name
) -> None:
    sentinel = "NEVER_RECORD_THIS_SECRET"
    event = framework.parse_payload({
        "tool_name": tool_name,
        "tool_input": {
            "file_path": ".env",
            "content": sentinel,
            "command": f"printf {sentinel}",
            "nested": {"token": sentinel},
        },
        "configuration": {"token": sentinel},
    })
    log_file = tmp_path / "logs" / "audit.ndjson"

    framework.record_event(
        log_file,
        event,
        rule="protected-file",
        decision="deny",
        offending_path="/repo/.env",
    )

    raw = log_file.read_text(encoding="utf-8")
    entry = json.loads(raw)
    assert entry == {
        "timestamp": entry["timestamp"],
        "tool": tool_name,
        "rule": "protected-file",
        "decision": "deny",
        "path": "/repo/.env",
    }
    assert sentinel not in raw


def test_audit_script_records_redacted_ndjson_without_console_output(
    tmp_path, capsys
) -> None:
    audit = _load_module(AUDIT_SCRIPT_PATH, "phase01_audit_log")
    sentinel = "AUDIT_BODY_SECRET"
    log_file = tmp_path / "agent-audit.log"
    payload = {
        "toolName": "Write",
        "toolInput": {"file_path": ".env", "content": sentinel},
        "toolResponse": {"body": sentinel},
    }

    exit_code = audit.main(io.StringIO(json.dumps(payload)), log_file=log_file)

    captured = capsys.readouterr()
    raw = log_file.read_text(encoding="utf-8")
    entry = json.loads(raw)
    assert exit_code == 0
    assert captured.out == captured.err == ""
    assert sentinel not in raw
    assert entry == {
        "timestamp": entry["timestamp"],
        "tool": "Write",
        "rule": "audit-log",
        "decision": "observed",
    }


@pytest.mark.parametrize(
    "failure_kind", ["malformed", "directory", "serialization", "open", "write"]
)
def test_complete_audit_path_fails_open(
    tmp_path, capsys, monkeypatch, failure_kind
) -> None:
    audit = _load_module(AUDIT_SCRIPT_PATH, f"phase01_audit_log_{failure_kind}")
    sentinel = "AUDIT_FAILURE_SECRET"
    payload = "{broken" if failure_kind == "malformed" else json.dumps({
        "tool_name": "Read", "tool_input": {"file_path": "safe.txt"}
    })
    log_file = tmp_path / "audit.log"
    if failure_kind == "directory":
        parent_file = tmp_path / "not-a-directory"
        parent_file.write_text("occupied", encoding="utf-8")
        log_file = parent_file / "audit.log"
    elif failure_kind == "serialization":
        def fail_serialization(*args, **kwargs):
            raise RuntimeError(sentinel)

        monkeypatch.setattr(
            audit.record_event.__globals__["json"], "dumps", fail_serialization
        )
    elif failure_kind == "open":
        def fail_open(*args, **kwargs):
            raise OSError(sentinel)

        monkeypatch.setattr(Path, "open", fail_open)
    elif failure_kind == "write":
        class FailingLog:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

            def write(self, _content):
                raise OSError(sentinel)

        monkeypatch.setattr(Path, "open", lambda *args, **kwargs: FailingLog())

    exit_code = audit.main(io.StringIO(payload), log_file=log_file)

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == captured.err == ""
    assert sentinel not in captured.out + captured.err


def test_audit_wrapper_fails_open_when_python_entrypoint_fails(tmp_path) -> None:
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    fake_python = fake_bin / "python3"
    fake_python.write_text("#!/bin/sh\nexit 23\n", encoding="utf-8")
    fake_python.chmod(0o755)
    environment = os.environ.copy()
    environment["PATH"] = f"{fake_bin}:/usr/bin:/bin"

    result = subprocess.run(
        ["/bin/bash", str(AUDIT_WRAPPER_PATH)],
        input="{}",
        text=True,
        capture_output=True,
        check=False,
        env=environment,
    )

    assert result.returncode == 0
    assert result.stdout == result.stderr == ""


def test_framework_package_exposes_only_documented_public_contract(
    monkeypatch
) -> None:
    hooks_dir = REPO_ROOT / ".github" / "hooks"
    monkeypatch.syspath_prepend(str(hooks_dir))
    package = __import__("lib")

    expected = set(PUBLIC_API + SCANNER_PUBLIC_API)
    assert set(package.__all__) == expected
    assert all(getattr(package, name) is not None for name in expected)


def test_audit_entrypoint_imports_without_cwd_or_pythonpath(tmp_path) -> None:
    log_file = tmp_path / "audit.ndjson"
    payload = json.dumps({
        "tool_name": "Read", "tool_input": {"file_path": "safe.txt"}
    })
    code = (
        "import importlib.util,io,pathlib;"
        f"p=pathlib.Path({str(AUDIT_SCRIPT_PATH)!r});"
        "s=importlib.util.spec_from_file_location('isolated_audit',p);"
        "m=importlib.util.module_from_spec(s);s.loader.exec_module(m);"
        f"raise SystemExit(m.main(io.StringIO({payload!r}),log_file=pathlib.Path({str(log_file)!r})))"
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
    assert json.loads(log_file.read_text(encoding="utf-8"))["tool"] == "Read"


def test_runner_constrained_verification_checklist_is_recorded() -> None:
    content = VERIFICATION_DOC_PATH.read_text(encoding="utf-8")

    assert "bypass-permissions" in content
    assert "deny" in content
    assert "ask" in content
    assert "exit code 2" in content
    assert "subagent" in content
    assert "Observed evidence" in content


def test_median_framework_invocation_overhead_is_below_budget(framework) -> None:
    payload = json.dumps({
        "tool_name": "Read", "tool_input": {"file_path": "safe.txt"}
    })

    def handler(event, config):
        return framework.make_decision("allow", "no matching rule")

    samples = []
    for _ in range(1_000):
        started = time.perf_counter_ns()
        framework.security_guard(
            handler,
            input_stream=io.StringIO(payload),
            output_stream=io.StringIO(),
        )
        samples.append((time.perf_counter_ns() - started) / 1_000_000)

    assert median(samples) < framework.HOOK_RUNTIME_BUDGET_MS


def test_framework_runtime_imports_are_stdlib_only_and_no_subprocess() -> None:
    framework_path = REPO_ROOT / ".github" / "hooks" / "lib" / "framework.py"
    tree = ast.parse(framework_path.read_text(encoding="utf-8"))
    imported_roots = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_roots.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_roots.add(node.module.split(".")[0])

    assert "subprocess" not in imported_roots
    assert imported_roots <= sys.stdlib_module_names
