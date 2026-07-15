"""Public hook-framework contract shared by security hook consumers."""

from .framework import (
    ConfigError,
    ConfigSnapshot,
    Decision,
    HookEvent,
    PayloadError,
    emit_decision,
    load_config,
    make_decision,
    observability_guard,
    parse_payload,
    record_event,
    security_guard,
)


__all__ = (
    "HookEvent",
    "Decision",
    "ConfigSnapshot",
    "PayloadError",
    "ConfigError",
    "parse_payload",
    "make_decision",
    "emit_decision",
    "load_config",
    "security_guard",
    "observability_guard",
    "record_event",
)
