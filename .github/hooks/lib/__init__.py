"""Public hook-framework contract shared by security hook consumers."""

from .framework import (
    ConfigError,
    ConfigSnapshot,
    Decision,
    HookEvent,
    PostToolResult,
    PayloadError,
    emit_decision,
    emit_post_tool_result,
    load_config,
    make_decision,
    make_post_tool_result,
    observability_guard,
    parse_payload,
    post_tool_security_guard,
    record_event,
    security_guard,
)
__all__ = (
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
    "InjectionConfigError",
    "InjectionRule",
    "MatchMetadata",
    "ScanResult",
    "load_injection_rules",
    "scan_output",
)

_SCANNER_EXPORTS = frozenset(
    {
        "InjectionConfigError",
        "InjectionRule",
        "MatchMetadata",
        "ScanResult",
        "load_injection_rules",
        "scan_output",
    }
)


def __getattr__(name):
    """Load scanner exports only for consumers that request them."""

    if name not in _SCANNER_EXPORTS:
        raise AttributeError(name)
    from importlib import import_module

    return getattr(import_module(f"{__name__}.injection_scanner"), name)
