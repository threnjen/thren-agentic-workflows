"""Shared, standard-library-only contracts for repository hooks."""

import json
import sys
from collections.abc import Mapping
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from types import MappingProxyType
from typing import Any, NamedTuple


_TOOL_NAME_KEYS = ("tool_name", "name", "toolName")
_TOOL_INPUT_KEYS = ("tool_input", "input", "toolInput")
HOOK_RUNTIME_BUDGET_MS = 50
_CONTEXT_KEYS = (
    "hook_event_name",
    "hookEventName",
    "session_id",
    "sessionId",
    "transcript_path",
    "transcriptPath",
    "cwd",
    "permission_mode",
    "permissionMode",
)


class PayloadError(ValueError):
    """Raised when a hook payload cannot be normalized safely."""


class ConfigError(ValueError):
    """Raised when hook configuration cannot be loaded safely."""


class HookEvent(NamedTuple):
    """Normalized hook event consumed by security and audit hooks."""

    tool_name: str
    tool_input: Mapping[str, Any]
    context: Mapping[str, Any]


class Decision(NamedTuple):
    """Structured PreToolUse permission decision."""

    action: str
    reason: str


class ConfigSnapshot(NamedTuple):
    """Merged configuration and its protected-override guard posture."""

    data: Mapping[str, Any]
    guard_enabled: bool


_CONFIG_CACHE: dict[
    tuple[Path, Path | None],
    tuple[tuple[tuple[int, int] | None, tuple[int, int] | None], ConfigSnapshot],
] = {}
_CONFIG_CACHE_LOCK = Lock()


def _first_present(payload: Mapping[str, Any], keys: tuple[str, ...]) -> Any:
    for key in keys:
        if key in payload:
            return payload[key]
    return None


def _decode_payload(source: Any) -> Mapping[str, Any]:
    if isinstance(source, Mapping):
        payload = source
    else:
        if hasattr(source, "read"):
            source = source.read()
        if isinstance(source, bytes):
            try:
                source = source.decode("utf-8")
            except UnicodeDecodeError as error:
                raise PayloadError("hook payload is malformed") from error
        if not isinstance(source, str) or not source.strip():
            raise PayloadError("hook payload is empty")
        try:
            payload = json.loads(source)
        except json.JSONDecodeError as error:
            raise PayloadError("hook payload is malformed") from error

    if not isinstance(payload, Mapping):
        raise PayloadError("hook payload must be a JSON object")
    return payload


def parse_payload(source: Any) -> HookEvent:
    """Normalize the payload aliases observed across supported hook runners."""

    payload = _decode_payload(source)
    tool_name = _first_present(payload, _TOOL_NAME_KEYS)
    tool_input = _first_present(payload, _TOOL_INPUT_KEYS)

    if not isinstance(tool_name, str) or not tool_name.strip():
        raise PayloadError("hook payload is missing a tool name")
    if not isinstance(tool_input, Mapping):
        raise PayloadError("hook payload is missing a tool input object")

    context = {key: payload[key] for key in _CONTEXT_KEYS if key in payload}
    return HookEvent(tool_name.strip(), dict(tool_input), context)


def make_decision(action: str, reason: str) -> Decision:
    """Create a validated allow, ask, or deny decision."""

    if action not in {"allow", "ask", "deny"}:
        raise ValueError("decision action must be allow, ask, or deny")
    if not isinstance(reason, str) or not reason.strip():
        raise ValueError("decision reason must be non-empty")
    return Decision(action, reason.strip())


def emit_decision(
    decision: Decision,
    *,
    output_stream=None,
    error_stream=None,
    use_exit_code_fallback: bool = False,
) -> int:
    """Emit one structured decision, or a blocking exit-code-2 fallback."""

    output_stream = output_stream or sys.stdout
    error_stream = error_stream or sys.stderr
    if use_exit_code_fallback:
        error_stream.write(f"{decision.reason}\n")
        return 2

    payload = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": decision.action,
            "permissionDecisionReason": decision.reason,
        }
    }
    output_stream.write(json.dumps(payload, separators=(",", ":")) + "\n")
    return 0


def _file_signature(path: Path | None) -> tuple[int, int] | None:
    if path is None:
        return None
    try:
        stat = path.stat()
    except FileNotFoundError:
        return None
    except OSError as error:
        raise ConfigError("configuration metadata is unavailable") from error
    return stat.st_mtime_ns, stat.st_size


def _read_config_layer(path: Path | None, layer_name: str) -> dict[str, Any]:
    if path is None or not path.exists():
        return {}
    try:
        content = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ConfigError(f"invalid {layer_name} configuration") from error
    if not isinstance(content, dict):
        raise ConfigError(f"invalid {layer_name} configuration")
    return content


def _merge_config(base: dict[str, Any], override: Mapping[str, Any]) -> dict[str, Any]:
    merged = deepcopy(base)
    for key, value in override.items():
        current = merged.get(key)
        if isinstance(current, dict) and isinstance(value, Mapping):
            merged[key] = _merge_config(current, value)
        else:
            merged[key] = deepcopy(value)
    return merged


def _project_guard_enabled(override: Mapping[str, Any]) -> bool:
    guard = override.get("guard")
    if guard is None:
        return True
    if not isinstance(guard, Mapping):
        raise ConfigError("invalid project override configuration")
    enabled = guard.get("enabled", True)
    if not isinstance(enabled, bool):
        raise ConfigError("invalid project override configuration")
    return enabled


def _freeze_config(value: Any) -> Any:
    if isinstance(value, dict):
        return MappingProxyType({key: _freeze_config(item) for key, item in value.items()})
    if isinstance(value, list):
        return tuple(_freeze_config(item) for item in value)
    return value


def load_config(defaults_path, override_path=None) -> ConfigSnapshot:
    """Load defaults then overrides, reusing only mtime-current snapshots."""

    defaults = Path(defaults_path).expanduser().resolve()
    override = (
        Path(override_path).expanduser().resolve() if override_path is not None else None
    )
    key = defaults, override
    signatures = _file_signature(defaults), _file_signature(override)

    with _CONFIG_CACHE_LOCK:
        cached = _CONFIG_CACHE.get(key)
        if cached is not None and cached[0] == signatures:
            return cached[1]

        defaults_layer = _read_config_layer(defaults, "defaults")
        override_layer = _read_config_layer(override, "project override")
        merged = _merge_config(defaults_layer, override_layer)
        snapshot = ConfigSnapshot(
            _freeze_config(merged), _project_guard_enabled(override_layer)
        )
        _CONFIG_CACHE[key] = signatures, snapshot
        return snapshot


def security_guard(
    handler,
    *,
    input_stream=None,
    output_stream=None,
    error_stream=None,
    config_loader=None,
) -> int:
    """Run a security hook, converting every operational error into denial."""

    input_stream = sys.stdin if input_stream is None else input_stream
    output_stream = sys.stdout if output_stream is None else output_stream
    error_stream = sys.stderr if error_stream is None else error_stream
    try:
        event = parse_payload(input_stream)
        config = config_loader() if config_loader is not None else ConfigSnapshot({}, True)
        if not config.guard_enabled:
            decision = make_decision("allow", "guard disabled by project override")
        else:
            decision = handler(event, config)
        if not isinstance(decision, Decision):
            raise TypeError("security hook handler must return a Decision")
    except Exception:
        decision = make_decision("deny", "guard error")

    try:
        return emit_decision(decision, output_stream=output_stream)
    except Exception:
        try:
            error_stream.write("guard error\n")
        except Exception:
            pass
        return 2


def observability_guard(handler, *, input_stream=None, config_loader=None) -> int:
    """Run an observability hook without ever blocking its caller."""

    input_stream = sys.stdin if input_stream is None else input_stream
    try:
        event = parse_payload(input_stream)
        config = config_loader() if config_loader is not None else ConfigSnapshot({}, True)
        handler(event, config)
    except Exception:
        pass
    return 0


def record_event(
    log_path,
    event: HookEvent,
    *,
    rule: str | None = None,
    decision: str | None = None,
    offending_path: str | None = None,
) -> None:
    """Append one NDJSON record containing only explicitly allowed metadata."""

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds").replace(
            "+00:00", "Z"
        ),
        "tool": event.tool_name,
    }
    if rule is not None:
        entry["rule"] = rule
    if decision is not None:
        entry["decision"] = decision
    if offending_path is not None:
        entry["path"] = offending_path

    path = Path(log_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as log_file:
        log_file.write(json.dumps(entry, separators=(",", ":")) + "\n")
