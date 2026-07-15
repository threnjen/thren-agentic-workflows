"""Bounded, data-driven URL payload analysis without network access."""

import math
import re
from collections import Counter
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, NamedTuple
from urllib.parse import unquote, urlsplit


class URLConfigError(ValueError):
    """Raised when URL-exfiltration configuration is unsafe."""


class URLMatch(NamedTuple):
    """One redacted URL policy match."""

    rule_id: str
    action: str
    reason: str
    safe_alternative: str
    priority: int


@dataclass(frozen=True)
class _URLRule:
    rule_id: str
    action: str
    reason: str
    matcher: str
    priority: int
    safe_alternative: str
    escalate_in_bypass: bool
    patterns: tuple[re.Pattern[str], ...] = ()
    query_names: frozenset[str] = frozenset()
    shapes: tuple[tuple[str, int], ...] = ()
    min_length: int = 0
    max_length: int = 0
    min_entropy: float = 0.0
    min_character_classes: int = 0
    hex_query_min_length: int = 0


@dataclass(frozen=True)
class _URLPolicy:
    max_url_length: int
    max_segments: int
    max_segment_length: int
    decode_passes: int
    rules: tuple[_URLRule, ...]


_ACTIONS = {"ask", "deny"}
_MATCHERS = {"regex", "encoded_query", "entropy"}
_MALFORMED_ESCAPE = re.compile(r"%(?![0-9A-Fa-f]{2})")
_HEX = re.compile(r"[0-9A-Fa-f]+")
_BASE64 = re.compile(r"[A-Za-z0-9+/_=-]+")
_ACTION_STRENGTH = {"ask": 1, "deny": 2}


def _positive_int(value: Any, field: str, *, maximum: int) -> int:
    if (
        not isinstance(value, int)
        or isinstance(value, bool)
        or value <= 0
        or value > maximum
    ):
        raise URLConfigError(f"invalid URL {field}")
    return value


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _strings(value: Any, field: str) -> tuple[str, ...]:
    if not isinstance(value, (list, tuple)) or not value or not all(
        _nonempty(item) for item in value
    ):
        raise URLConfigError(f"invalid URL {field}")
    return tuple(item.strip() for item in value)


def _load_rule(key: str, raw: Any) -> _URLRule:
    if not _nonempty(key) or not isinstance(raw, Mapping):
        raise URLConfigError("invalid URL rule")
    rule_id = raw.get("id")
    action = raw.get("action")
    reason = raw.get("reason")
    matcher = raw.get("matcher")
    priority = raw.get("priority")
    alternative = raw.get("safe_alternative")
    escalation = raw.get("escalate_in_bypass")
    if rule_id != key or action not in _ACTIONS or matcher not in _MATCHERS:
        raise URLConfigError("invalid URL rule tier")
    if not _nonempty(reason) or not _nonempty(alternative):
        raise URLConfigError("invalid URL rule guidance")
    if not isinstance(priority, int) or isinstance(priority, bool):
        raise URLConfigError("invalid URL rule priority")
    if escalation not in {None, "deny"}:
        raise URLConfigError("invalid URL bypass escalation")

    common = {
        "rule_id": rule_id,
        "action": action,
        "reason": reason.strip(),
        "matcher": matcher,
        "priority": priority,
        "safe_alternative": alternative.strip(),
        "escalate_in_bypass": escalation == "deny",
    }
    if matcher == "regex":
        patterns = []
        for pattern in _strings(raw.get("patterns"), "regex patterns"):
            try:
                patterns.append(re.compile(pattern))
            except re.error as error:
                raise URLConfigError("invalid URL rule regex") from error
        return _URLRule(**common, patterns=tuple(patterns))

    if matcher == "encoded_query":
        query_names = frozenset(
            name.casefold() for name in _strings(raw.get("query_names"), "query names")
        )
        raw_shapes = raw.get("shapes")
        if not isinstance(raw_shapes, (list, tuple)) or not raw_shapes:
            raise URLConfigError("invalid URL encoded shapes")
        shapes = []
        for shape in raw_shapes:
            if not isinstance(shape, Mapping) or shape.get("alphabet") not in {
                "hex",
                "base64",
            }:
                raise URLConfigError("invalid URL encoded shape")
            shapes.append(
                (
                    shape["alphabet"],
                    _positive_int(
                        shape.get("min_length"), "encoded minimum length", maximum=4096
                    ),
                )
            )
        return _URLRule(
            **common, query_names=query_names, shapes=tuple(shapes)
        )

    min_length = _positive_int(
        raw.get("min_length"), "entropy minimum length", maximum=4096
    )
    max_length = _positive_int(
        raw.get("max_length"), "entropy maximum length", maximum=4096
    )
    minimum_entropy = raw.get("min_entropy")
    if (
        not isinstance(minimum_entropy, (int, float))
        or isinstance(minimum_entropy, bool)
        or not 0 < minimum_entropy <= 8
    ):
        raise URLConfigError("invalid URL entropy threshold")
    character_classes = _positive_int(
        raw.get("min_character_classes"), "character-class threshold", maximum=4
    )
    hex_minimum = _positive_int(
        raw.get("hex_query_min_length"), "hex query minimum length", maximum=4096
    )
    if max_length < min_length:
        raise URLConfigError("invalid URL entropy length range")
    return _URLRule(
        **common,
        min_length=min_length,
        max_length=max_length,
        min_entropy=float(minimum_entropy),
        min_character_classes=character_classes,
        hex_query_min_length=hex_minimum,
    )


def _load_policy(config: Mapping[str, Any]) -> _URLPolicy:
    configured = config.get("url_exfiltration")
    if not isinstance(configured, Mapping):
        raise URLConfigError("URL exfiltration configuration is missing")
    rules_config = configured.get("rules")
    if not isinstance(rules_config, Mapping) or not rules_config:
        raise URLConfigError("URL exfiltration rules are missing")
    rules = tuple(_load_rule(key, raw) for key, raw in rules_config.items())
    if {rule.matcher for rule in rules} != _MATCHERS:
        raise URLConfigError("URL exfiltration rule coverage is incomplete")
    return _URLPolicy(
        _positive_int(configured.get("max_url_length"), "length limit", maximum=65536),
        _positive_int(configured.get("max_segments"), "segment limit", maximum=1024),
        _positive_int(
            configured.get("max_segment_length"), "segment length limit", maximum=16384
        ),
        _positive_int(configured.get("decode_passes"), "decode-pass limit", maximum=3),
        rules,
    )


def _decode(value: str, policy: _URLPolicy) -> str:
    if _MALFORMED_ESCAPE.search(value):
        raise ValueError("guarded URL is malformed")
    decoded = value
    for _ in range(policy.decode_passes):
        next_value = unquote(decoded)
        if len(next_value) > policy.max_segment_length:
            raise ValueError("guarded URL segment is too long")
        if next_value == decoded:
            break
        decoded = next_value
        if _MALFORMED_ESCAPE.search(decoded):
            raise ValueError("guarded URL is malformed")
    return decoded


def _url_parts(
    url: str, policy: _URLPolicy
) -> tuple[tuple[str, ...], tuple[tuple[str, str], ...]]:
    if not isinstance(url, str) or not url.strip():
        raise ValueError("guarded URL is missing")
    if len(url) > policy.max_url_length or "\x00" in url:
        raise ValueError("guarded URL is invalid")
    try:
        parsed = urlsplit(url)
        hostname = parsed.hostname
    except ValueError as error:
        raise ValueError("guarded URL is malformed") from error
    if parsed.scheme.casefold() not in {"http", "https"} or not hostname:
        raise ValueError("guarded URL is unsupported")
    raw_paths = tuple(part for part in parsed.path.split("/") if part)
    raw_queries = tuple(
        field.partition("=")[::2] for field in parsed.query.split("&") if field
    )
    if len(raw_paths) + len(raw_queries) > policy.max_segments:
        raise ValueError("guarded URL has too many segments")
    paths = tuple(_decode(value, policy) for value in raw_paths)
    queries = tuple(
        (_decode(name, policy), _decode(value, policy))
        for name, value in raw_queries
    )
    return paths, queries


def _shape_matches(value: str, alphabet: str, minimum: int) -> bool:
    if len(value) < minimum:
        return False
    expression = _HEX if alphabet == "hex" else _BASE64
    return expression.fullmatch(value) is not None


def _entropy(value: str) -> float:
    counts = Counter(value)
    length = len(value)
    return -sum((count / length) * math.log2(count / length) for count in counts.values())


def _character_classes(value: str) -> int:
    return sum(
        (
            any(character.islower() for character in value),
            any(character.isupper() for character in value),
            any(character.isdigit() for character in value),
            any(not character.isalnum() for character in value),
        )
    )


def _matches(
    rule: _URLRule,
    paths: tuple[str, ...],
    queries: tuple[tuple[str, str], ...],
) -> bool:
    values = paths + tuple(value for _, value in queries)
    if rule.matcher == "regex":
        return any(pattern.search(value) for pattern in rule.patterns for value in values)
    if rule.matcher == "encoded_query":
        return any(
            name.casefold() in rule.query_names
            and any(
                _shape_matches(value, alphabet, minimum)
                for alphabet, minimum in rule.shapes
            )
            for name, value in queries
        )

    for value in values:
        if not rule.min_length <= len(value) <= rule.max_length:
            continue
        if (
            _BASE64.fullmatch(value)
            and _character_classes(value) >= rule.min_character_classes
            and _entropy(value) >= rule.min_entropy
        ):
            return True
    return any(
        len(value) >= rule.hex_query_min_length
        and _HEX.fullmatch(value)
        and _entropy(value) >= rule.min_entropy
        for _, value in queries
    )


def analyze_url(
    url: str, config: Mapping[str, Any], *, bypass: bool = False
) -> tuple[URLMatch, ...]:
    """Return redacted matches for decoded URL path and query values."""

    if not isinstance(bypass, bool):
        raise ValueError("URL bypass state is invalid")
    policy = _load_policy(config)
    paths, queries = _url_parts(url, policy)
    matches = []
    for rule in policy.rules:
        if not _matches(rule, paths, queries):
            continue
        action = "deny" if bypass and rule.escalate_in_bypass else rule.action
        matches.append(
            URLMatch(
                rule.rule_id,
                action,
                rule.reason,
                rule.safe_alternative,
                rule.priority,
            )
        )
    return tuple(
        sorted(
            matches,
            key=lambda match: (
                _ACTION_STRENGTH[match.action],
                match.priority,
                match.rule_id,
            ),
            reverse=True,
        )
    )


__all__ = ("URLConfigError", "URLMatch", "analyze_url")
