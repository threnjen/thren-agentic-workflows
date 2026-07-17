"""Bounded, data-driven normalization and indirect-injection matching."""

import base64
import binascii
import json
import re
import unicodedata
from collections.abc import Mapping
from pathlib import Path
from typing import Any, NamedTuple


class InjectionConfigError(ValueError):
    """Raised when scanner policy or limits are unsafe."""


class InjectionRule(NamedTuple):
    """Validated immutable scanner rule."""

    rule_id: str
    severity: str
    response_action: str
    category: str
    reason: str
    recommended_posture: str
    matcher: str
    pattern: str
    priority: int


class MatchMetadata(NamedTuple):
    """Redacted metadata for the strongest matching rule."""

    rule_id: str
    severity: str
    response_action: str
    category: str
    reason: str
    recommended_posture: str
    priority: int


class ScanResult(NamedTuple):
    """Bounded scan outcome without raw or matched content."""

    match: MatchMetadata | None
    notices: tuple[str, ...]
    empty: bool
    bytes_scanned: int


_SEVERITIES = {"low", "medium", "high"}
_ACTIONS = {"warn", "block"}
_MATCHERS = {"fixed_string", "regex"}
_ACTION_STRENGTH = {"warn": 0, "block": 1}
_SEVERITY_STRENGTH = {"low": 0, "medium": 1, "high": 2}
_IDENTIFIER = re.compile(r"[a-z0-9][a-z0-9._-]{0,79}\Z")
_BASE64_CANDIDATE = re.compile(r"(?<![A-Za-z0-9+/])[A-Za-z0-9+/]{12,}={0,2}(?![A-Za-z0-9+/=])")
_HEX_CANDIDATE = re.compile(r"(?<![0-9A-Fa-f])(?:[0-9A-Fa-f]{2}){6,}(?![0-9A-Fa-f])")
_DEFAULT_LIMITS = {
    "max_scan_bytes": 262_144,
    "max_encoded_candidates": 32,
    "max_decoded_bytes": 16_384,
}
_APPROVED_ALLOWLIST = {
    ".github/hooks/config/injection-patterns.json": False,
    "tests/hooks/fixtures/injection": True,
    "docs/inspiration": True,
}
_HOMOGLYPHS = str.maketrans(
    {
        "Α": "A", "Β": "B", "Ε": "E", "Ζ": "Z", "Η": "H", "Ι": "I",
        "Κ": "K", "Μ": "M", "Ν": "N", "Ο": "O", "Ρ": "P", "Τ": "T",
        "Υ": "Y", "Χ": "X", "а": "a", "е": "e", "о": "o", "р": "p",
        "с": "c", "х": "x", "у": "y", "і": "i", "ј": "j", "ѕ": "s",
        "А": "A", "В": "B", "Е": "E", "К": "K", "М": "M", "Н": "H",
        "О": "O", "Р": "P", "С": "C", "Т": "T", "Х": "X", "І": "I",
    }
)


def _safe_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InjectionConfigError(f"injection rule {field} is invalid")
    cleaned = value.strip()
    if len(cleaned) > 200 or any(character in cleaned for character in "\r\n\x00"):
        raise InjectionConfigError(f"injection rule {field} is invalid")
    return cleaned


def _validate_regex(pattern: str) -> None:
    if len(pattern) > 512:
        raise InjectionConfigError("injection rule matcher is invalid")
    unsafe = (
        r"\\[1-9]",
        r"\(\?([=!]|<[=!])",
        r"\([^)]*[+*{][^)]*\)[+*{]",
        r"\([^()]*(?:\|[^()]*)+\)(?:[+*]|\{\d+(?:,\d*)?\})",
        r"(?:\+\+|\*\*|\+\*|\*\+|\}\+|\}\*)",
    )
    if any(re.search(check, pattern) for check in unsafe):
        raise InjectionConfigError("injection rule matcher is invalid")
    try:
        re.compile(pattern)
    except re.error as error:
        raise InjectionConfigError("injection rule matcher is invalid") from error


def load_injection_rules(config: Mapping[str, Any]) -> tuple[InjectionRule, ...]:
    """Validate and freeze configured injection rules for repeated scans."""

    configured = config.get("rules")
    if not isinstance(configured, Mapping) or not configured:
        raise InjectionConfigError("injection rules are missing")
    rules = []
    signatures = set()
    for key, raw in configured.items():
        if not isinstance(key, str) or not isinstance(raw, Mapping):
            raise InjectionConfigError("injection rule is invalid")
        rule_id = raw.get("id")
        severity = raw.get("severity")
        response_action = raw.get("response_action")
        category = raw.get("category")
        reason = raw.get("reason")
        posture = raw.get("recommended_posture")
        matcher = raw.get("matcher")
        pattern = raw.get("pattern")
        priority = raw.get("priority")
        if rule_id != key or not isinstance(rule_id, str) or not _IDENTIFIER.fullmatch(rule_id):
            raise InjectionConfigError("injection rule identifier is invalid")
        if severity not in _SEVERITIES:
            raise InjectionConfigError("injection rule severity is invalid")
        if response_action not in _ACTIONS:
            raise InjectionConfigError("injection rule response action is invalid")
        category = _safe_text(category, "category")
        if not _IDENTIFIER.fullmatch(category):
            raise InjectionConfigError("injection rule category is invalid")
        reason = _safe_text(reason, "reason")
        posture = _safe_text(posture, "recommended posture")
        if matcher not in _MATCHERS:
            raise InjectionConfigError("injection rule matcher is invalid")
        pattern = _safe_text(pattern, "pattern")
        if matcher == "regex":
            _validate_regex(pattern)
        if not isinstance(priority, int) or isinstance(priority, bool):
            raise InjectionConfigError("injection rule priority is invalid")
        signature = matcher, _normalize(pattern)
        if signature in signatures:
            raise InjectionConfigError("injection rule matcher is ambiguous")
        signatures.add(signature)
        rules.append(
            InjectionRule(
                rule_id,
                severity,
                response_action,
                category,
                reason,
                posture,
                matcher,
                pattern,
                priority,
            )
        )
    return tuple(rules)


def _limits(configured: Mapping[str, Any] | None) -> dict[str, int]:
    if configured is None:
        return dict(_DEFAULT_LIMITS)
    if not isinstance(configured, Mapping):
        raise InjectionConfigError("scanner limits are invalid")
    result = dict(_DEFAULT_LIMITS)
    if any(key not in result for key in configured):
        raise InjectionConfigError("scanner limits are invalid")
    for key in result:
        if key in configured:
            value = configured[key]
            if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
                raise InjectionConfigError("scanner limits are invalid")
            result[key] = value
    return result


def _normalize(text: str) -> str:
    normalized = unicodedata.normalize("NFKC", text).translate(_HOMOGLYPHS)
    return "".join(
        character for character in normalized if unicodedata.category(character) != "Cf"
    ).casefold()


def _decoded_candidates(
    text: str, limits: Mapping[str, int]
) -> tuple[tuple[str, ...], bool]:
    """Decode encoded candidates, reporting whether any assessable one was skipped.

    Candidates that cannot decode to text at all are not a bypass channel and
    do not consume the candidate budget. Candidates skipped for size or budget
    reasons are unassessed content and must be reported so callers can fail
    closed instead of passing them through (P2-SEC-02).
    """

    candidates: dict[tuple[int, int], tuple[str, str]] = {}
    for match in _BASE64_CANDIDATE.finditer(text):
        candidates[match.span()] = ("base64", match.group(0))
    for match in _HEX_CANDIDATE.finditer(text):
        candidates[match.span()] = ("hex", match.group(0))

    decoded: list[str] = []
    exhausted = False
    for _, (encoding, candidate) in sorted(candidates.items()):
        try:
            if encoding == "hex":
                raw = bytes.fromhex(candidate)
            else:
                padded = candidate + "=" * (-len(candidate) % 4)
                raw = base64.b64decode(padded, validate=True)
        except (ValueError, binascii.Error):
            continue
        if len(raw) > limits["max_decoded_bytes"]:
            exhausted = True
            continue
        try:
            value = raw.decode("utf-8")
        except UnicodeDecodeError:
            continue
        if len(decoded) >= limits["max_encoded_candidates"]:
            exhausted = True
            break
        decoded.append(value)
    return tuple(decoded), exhausted


def _text_output(output: Any) -> tuple[str | None, tuple[str, ...]]:
    if isinstance(output, str):
        return output, (("binary",) if "\ufffd" in output else ())
    if isinstance(output, bytes):
        try:
            return output.decode("utf-8"), ()
        except UnicodeDecodeError:
            return None, ("binary",)
    try:
        return json.dumps(
            output,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ), ()
    except (TypeError, ValueError, UnicodeError) as error:
        raise ValueError("tool output cannot be serialized safely") from error


def _metadata(rule: InjectionRule) -> MatchMetadata:
    return MatchMetadata(
        rule.rule_id,
        rule.severity,
        rule.response_action,
        rule.category,
        rule.reason,
        rule.recommended_posture,
        rule.priority,
    )


def _selection_key(rule: InjectionRule) -> tuple[int, int, int, str]:
    return (
        -_ACTION_STRENGTH[rule.response_action],
        -_SEVERITY_STRENGTH[rule.severity],
        -rule.priority,
        rule.rule_id,
    )


def scan_output(
    output: Any,
    rules: tuple[InjectionRule, ...],
    *,
    limits: Mapping[str, Any] | None = None,
) -> ScanResult:
    """Scan a bounded normalized copy and return only redacted match metadata."""

    if not isinstance(rules, tuple) or any(not isinstance(rule, InjectionRule) for rule in rules):
        raise TypeError("scanner rules must be loaded by load_injection_rules")
    active_limits = _limits(limits)
    text, notices = _text_output(output)
    if text is None:
        return ScanResult(None, notices, False, 0)
    if not text:
        return ScanResult(None, notices, True, 0)

    encoded = text.encode("utf-8")
    if len(encoded) > active_limits["max_scan_bytes"]:
        encoded = encoded[: active_limits["max_scan_bytes"]]
        text = encoded.decode("utf-8", errors="ignore")
        notices = notices + ("scan-cap",)
    decoded, exhausted = _decoded_candidates(text, active_limits)
    if exhausted:
        notices = notices + ("candidate-cap",)
    representations = (_normalize(text),) + tuple(
        _normalize(candidate) for candidate in decoded
    )
    matching = []
    for rule in rules:
        if rule.matcher == "fixed_string":
            matched = any(_normalize(rule.pattern) in candidate for candidate in representations)
        else:
            expression = re.compile(rule.pattern, re.IGNORECASE)
            matched = any(expression.search(candidate) is not None for candidate in representations)
        if matched:
            matching.append(rule)
    selected = min(matching, key=_selection_key) if matching else None
    return ScanResult(
        _metadata(selected) if selected is not None else None,
        tuple(dict.fromkeys(notices)),
        False,
        len(encoded),
    )


def is_allowlisted_source(
    source_path: str,
    repo_root: str | Path,
    config: Mapping[str, Any],
) -> bool:
    """Allow only existing in-repository sources under approved configured roots."""

    configured = config.get("source_allowlist")
    if not isinstance(configured, (list, tuple)):
        raise InjectionConfigError("source allowlist is invalid")
    for entry in configured:
        if entry not in _APPROVED_ALLOWLIST:
            raise InjectionConfigError("source allowlist is invalid")
    if not isinstance(source_path, str) or not source_path.strip() or "\x00" in source_path:
        return False
    try:
        root = Path(repo_root).resolve(strict=True)
        candidate_path = Path(source_path)
        if ".." in candidate_path.parts:
            return False
        if not candidate_path.is_absolute():
            candidate_path = root / candidate_path
        candidate = candidate_path.resolve(strict=True)
        candidate.relative_to(root)
    except (OSError, RuntimeError, ValueError):
        return False

    for entry in configured:
        lexical_expected = root / entry
        expected = lexical_expected.resolve(strict=False)
        if expected != lexical_expected:
            continue
        try:
            if _APPROVED_ALLOWLIST[entry]:
                candidate.relative_to(expected)
            elif candidate != expected:
                continue
        except ValueError:
            continue
        try:
            expected.relative_to(root)
        except ValueError:
            continue
        return True
    return False


__all__ = (
    "InjectionConfigError",
    "InjectionRule",
    "MatchMetadata",
    "ScanResult",
    "load_injection_rules",
    "scan_output",
    "is_allowlisted_source",
)
