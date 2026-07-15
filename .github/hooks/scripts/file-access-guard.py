#!/usr/bin/env python3
"""PreToolUse entrypoint for data-driven file-access protection."""

import sys
from collections.abc import Mapping
from pathlib import Path


HOOKS_DIR = Path(__file__).resolve().parents[1]
if str(HOOKS_DIR) not in sys.path:
    sys.path.insert(0, str(HOOKS_DIR))

from lib import load_config, make_decision, record_event, security_guard
from lib.bash_analyzer import analyze_command
from lib.file_access import evaluate_path, load_rules


DEFAULT_RULES_PATH = HOOKS_DIR / "config" / "file-access-rules.json"
PROJECT_OVERRIDE_PATH = HOOKS_DIR / "config" / "file-access-overrides.json"
_FILE_TOOL_FIELDS = {
    "Read": "file_path",
    "Edit": "file_path",
    "Write": "file_path",
    "MultiEdit": "file_path",
    "NotebookEdit": "notebook_path",
}
_ACTION_STRENGTH = {"allow": 0, "ask": 1, "deny": 2}
_WRITE_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}


def _candidate_paths(event) -> tuple[str, ...]:
    field = _FILE_TOOL_FIELDS.get(event.tool_name)
    if field is not None:
        candidate = event.tool_input.get(field)
        if not isinstance(candidate, str) or not candidate.strip():
            raise ValueError("guarded file tool is missing its path")
        return (candidate,)
    if event.tool_name != "Grep":
        return ()

    candidates = []
    for grep_field in ("path", "glob"):
        if grep_field not in event.tool_input:
            continue
        candidate = event.tool_input[grep_field]
        if not isinstance(candidate, str) or not candidate.strip():
            raise ValueError("guarded Grep scope is invalid")
        candidates.append(candidate)
    return tuple(candidates)


def _event_cwd(event, fallback) -> Path:
    context_cwd = event.context.get("cwd")
    if context_cwd is not None:
        if not isinstance(context_cwd, str) or not context_cwd.strip():
            raise ValueError("hook working directory is invalid")
        return Path(context_cwd)
    return Path(fallback or Path.cwd())


def _is_bypass(event) -> bool:
    mode = event.context.get("permission_mode", event.context.get("permissionMode", ""))
    return isinstance(mode, str) and mode.replace("_", "-").casefold() in {
        "bypass-permissions",
        "bypasspermissions",
    }


def _guidance(match) -> str:
    target = f" {match.normalized_path}" if match.normalized_path else ""
    return (
        f"Rule {match.rule_id} matched{target}. {match.reason}. "
        f"Safe alternative: {match.safe_alternative}"
    )


def handle_event(
    event,
    config,
    *,
    cwd=None,
    home=None,
    case_sensitive=None,
    recorder=record_event,
):
    """Adapt a normalized hook event and return one framework decision."""

    rules = load_rules(config.data)
    root = _event_cwd(event, cwd)
    if event.tool_name == "Bash":
        command = event.tool_input.get("command")
        if not isinstance(command, str) or not command.strip():
            raise ValueError("guarded Bash tool is missing its command")
        matches = list(
            analyze_command(
                command,
                config.data,
                rules,
                cwd=root,
                home=home,
                case_sensitive=case_sensitive,
                bypass=_is_bypass(event),
            )
        )
    else:
        candidates = _candidate_paths(event)
        if not candidates:
            return make_decision("allow", "tool is outside file-access matching")
        matches = [
            match
            for candidate in candidates
            if (
                match := evaluate_path(
                    candidate,
                    rules,
                    cwd=root,
                    home=home,
                    case_sensitive=case_sensitive,
                    bypass=_is_bypass(event),
                    access="write" if event.tool_name in _WRITE_TOOLS else "read",
                )
            )
            is not None
        ]
    if not matches:
        return make_decision("allow", "no matching file-access rule")
    selected = max(matches, key=lambda match: _ACTION_STRENGTH[match.action])
    if selected.action == "allow":
        return make_decision("allow", f"Rule {selected.rule_id} allows this path")

    audit_log = config.data.get("audit_log")
    if not isinstance(audit_log, str) or not audit_log.strip():
        raise ValueError("file-access audit log is invalid")
    log_path = Path(audit_log)
    if not log_path.is_absolute():
        log_path = root / log_path
    recorder(
        log_path,
        event,
        rule=selected.rule_id,
        decision=selected.action,
        offending_path=selected.normalized_path or None,
    )
    return make_decision(selected.action, _guidance(selected))


def main(input_stream=None, output_stream=None, error_stream=None) -> int:
    """Run the security hook using the protected project override layer."""

    return security_guard(
        handle_event,
        input_stream=input_stream,
        output_stream=output_stream,
        error_stream=error_stream,
        config_loader=lambda: load_config(DEFAULT_RULES_PATH, PROJECT_OVERRIDE_PATH),
    )


if __name__ == "__main__":
    raise SystemExit(main())
