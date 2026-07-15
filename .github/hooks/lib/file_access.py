"""Data-driven path normalization and file-access rule evaluation."""

import fnmatch
import os
from collections.abc import Mapping
from pathlib import Path
from typing import Any, NamedTuple


class RuleConfigError(ValueError):
    """Raised when file-access rule configuration is unsafe."""


class Rule(NamedTuple):
    """Validated file-access rule."""

    rule_id: str
    action: str
    reason: str
    matcher: str
    pattern: str
    priority: int
    safe_alternative: str
    escalate_in_bypass: bool
    access: str


class PathDecision(NamedTuple):
    """Result of matching one normalized path against configured rules."""

    rule_id: str
    action: str
    reason: str
    normalized_path: str
    safe_alternative: str


_ACTIONS = {"allow", "ask", "deny"}
_MATCHERS = {"basename", "basename_glob", "path_suffix", "path_glob"}
_ACTION_STRENGTH = {"allow": 0, "ask": 1, "deny": 2}
_GLOB_MARKERS = "*?["


def _nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def load_rules(config: Mapping[str, Any]) -> tuple[Rule, ...]:
    """Validate and freeze the merged rule mapping from framework config."""

    configured = config.get("rules")
    if not isinstance(configured, Mapping) or not configured:
        raise RuleConfigError("file-access rules are missing")

    rules = []
    for key, raw_rule in configured.items():
        if not _nonempty_string(key) or not isinstance(raw_rule, Mapping):
            raise RuleConfigError("file-access rule is invalid")
        rule_id = raw_rule.get("id")
        action = raw_rule.get("action")
        reason = raw_rule.get("reason")
        matcher = raw_rule.get("matcher")
        pattern = raw_rule.get("pattern")
        priority = raw_rule.get("priority", 0)
        alternative = raw_rule.get("safe_alternative", "")
        escalation = raw_rule.get("escalate_in_bypass")
        access = raw_rule.get("access", "any")
        if rule_id != key or not _nonempty_string(rule_id):
            raise RuleConfigError("file-access rule identifier is invalid")
        if action not in _ACTIONS or not _nonempty_string(reason):
            raise RuleConfigError("file-access rule tier is invalid")
        if matcher not in _MATCHERS or not _nonempty_string(pattern):
            raise RuleConfigError("file-access rule matcher is invalid")
        if not isinstance(priority, int) or isinstance(priority, bool):
            raise RuleConfigError("file-access rule priority is invalid")
        if action != "allow" and not _nonempty_string(alternative):
            raise RuleConfigError("file-access safe alternative is missing")
        if escalation not in {None, "deny"}:
            raise RuleConfigError("file-access bypass escalation is invalid")
        if access not in {"any", "read", "write"}:
            raise RuleConfigError("file-access rule access scope is invalid")
        rules.append(
            Rule(
                rule_id,
                action,
                reason.strip(),
                matcher,
                pattern.strip(),
                priority,
                alternative.strip() if isinstance(alternative, str) else "",
                escalation == "deny",
                access,
            )
        )
    return tuple(rules)


def _expand_home(path: str, home: str | os.PathLike[str] | None) -> str:
    if home is not None and (path == "~" or path.startswith("~/")):
        suffix = path[2:] if path.startswith("~/") else ""
        return str(Path(home) / suffix)
    return os.path.expanduser(path)


def _case_sensitive_for(path: Path) -> bool:
    candidate = path if path.exists() else path.parent
    while not candidate.exists() and candidate != candidate.parent:
        candidate = candidate.parent
    for current in (candidate, *candidate.parents):
        if not current.name:
            continue
        alternate = current.with_name(current.name.swapcase())
        if alternate == current or not alternate.exists():
            continue
        try:
            return not os.path.samefile(current, alternate)
        except OSError:
            continue
    return True


def _normalize_path(
    path: str | os.PathLike[str],
    *,
    cwd: str | os.PathLike[str] | None,
    home: str | os.PathLike[str] | None,
    case_sensitive: bool | None,
) -> tuple[str, bool]:
    if not isinstance(path, (str, os.PathLike)):
        raise ValueError("candidate path must be text")
    raw_path = os.fspath(path)
    if not raw_path or "\x00" in raw_path:
        raise ValueError("candidate path must be non-empty text")
    expanded = Path(_expand_home(raw_path, home))
    if not expanded.is_absolute():
        expanded = Path(cwd or Path.cwd()) / expanded
    try:
        resolved = expanded.resolve(strict=False)
    except (OSError, RuntimeError) as error:
        raise ValueError("candidate path cannot be normalized") from error
    sensitive = _case_sensitive_for(resolved) if case_sensitive is None else case_sensitive
    normalized = resolved.as_posix()
    return (normalized if sensitive else normalized.casefold()), sensitive


def normalize_path(
    path: str | os.PathLike[str],
    *,
    cwd: str | os.PathLike[str] | None = None,
    home: str | os.PathLike[str] | None = None,
    case_sensitive: bool | None = None,
) -> str:
    """Expand, anchor, collapse, and resolve a candidate path once."""

    normalized, _ = _normalize_path(
        path, cwd=cwd, home=home, case_sensitive=case_sensitive
    )
    return normalized


def _glob_sample(pattern: str, star_value: str) -> str:
    sample = []
    index = 0
    while index < len(pattern):
        character = pattern[index]
        if character == "*":
            sample.append(star_value)
        elif character == "?":
            sample.append("x")
        elif character == "[":
            closing = pattern.find("]", index + 1)
            if closing == -1:
                sample.append(character)
            else:
                choices = pattern[index + 1 : closing].lstrip("!^")
                sample.append(choices[0] if choices else "x")
                index = closing
        else:
            sample.append(character)
        index += 1
    return "".join(sample)


def _glob_patterns_overlap(first: str, second: str) -> bool:
    samples = {
        _glob_sample(first, ""),
        _glob_sample(first, "x"),
        _glob_sample(second, ""),
        _glob_sample(second, "x"),
    }
    return any(
        fnmatch.fnmatchcase(sample, first) and fnmatch.fnmatchcase(sample, second)
        for sample in samples
    )


def _matches(
    rule: Rule, normalized_path: str, case_sensitive: bool, access: str
) -> bool:
    if rule.access not in {"any", access}:
        return False
    pattern = rule.pattern if case_sensitive else rule.pattern.casefold()
    basename = normalized_path.rsplit("/", 1)[-1]
    if rule.matcher == "basename":
        if any(marker in basename for marker in _GLOB_MARKERS):
            return _glob_patterns_overlap(basename, pattern)
        return basename == pattern
    if rule.matcher == "basename_glob":
        return _glob_patterns_overlap(basename, pattern)
    if rule.matcher == "path_suffix":
        suffix = pattern.lstrip("/")
        return normalized_path == suffix or normalized_path.endswith(f"/{suffix}")
    return fnmatch.fnmatchcase(normalized_path, pattern) or fnmatch.fnmatchcase(
        normalized_path, f"*/{pattern.lstrip('/')}"
    )


def evaluate_path(
    path: str | os.PathLike[str],
    rules: tuple[Rule, ...],
    *,
    cwd: str | os.PathLike[str] | None = None,
    home: str | os.PathLike[str] | None = None,
    case_sensitive: bool | None = None,
    bypass: bool = False,
    access: str = "read",
) -> PathDecision | None:
    """Return the strongest, most-specific configured decision for a path."""

    if access not in {"read", "write"}:
        raise ValueError("candidate access must be read or write")
    normalized, sensitive = _normalize_path(
        path, cwd=cwd, home=home, case_sensitive=case_sensitive
    )
    matches = [
        rule for rule in rules if _matches(rule, normalized, sensitive, access)
    ]
    if not matches:
        return None
    candidate_has_glob = any(marker in os.fspath(path) for marker in _GLOB_MARKERS)
    if candidate_has_glob:
        ordering = lambda rule: (
            _ACTION_STRENGTH[rule.action],
            rule.priority,
            rule.rule_id,
        )
    else:
        ordering = lambda rule: (
            rule.priority,
            _ACTION_STRENGTH[rule.action],
            rule.rule_id,
        )
    selected = max(
        matches,
        key=ordering,
    )
    action = "deny" if bypass and selected.escalate_in_bypass else selected.action
    return PathDecision(
        selected.rule_id,
        action,
        selected.reason,
        normalized,
        selected.safe_alternative,
    )


__all__ = (
    "PathDecision",
    "Rule",
    "RuleConfigError",
    "evaluate_path",
    "load_rules",
    "normalize_path",
)
