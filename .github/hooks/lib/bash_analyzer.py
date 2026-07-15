"""Deterministic Bash command analysis without executing shell input."""

import os
import re
import shlex
from collections.abc import Mapping
from typing import Any, NamedTuple

from .file_access import evaluate_path, normalize_path


class BashConfigError(ValueError):
    """Raised when Bash analysis configuration is unsafe."""


class BashMatch(NamedTuple):
    """One configured Bash or protected-path match."""

    rule_id: str
    action: str
    reason: str
    safe_alternative: str
    normalized_path: str | None = None


class BashRule(NamedTuple):
    """Validated data-driven Bash matcher."""

    rule_id: str
    action: str
    reason: str
    matcher: str
    pattern: str
    priority: int
    safe_alternative: str
    escalate_in_bypass: bool
    allow_in_approved_roots: bool


_SEPARATORS = {"|", "||", "&", "&&", ";", "(", ")"}
_REDIRECTIONS = {"<": "read", ">": "write", ">>": "write"}
_ACTIONS = {"allow", "ask", "deny"}
_MATCHERS = {"fixed_string", "regex"}


def load_bash_rules(config: Mapping[str, Any]) -> tuple[BashRule, ...]:
    """Validate and freeze command rules from the shared hook configuration."""

    configured = config.get("bash_rules")
    if not isinstance(configured, Mapping):
        raise BashConfigError("Bash rules are missing")
    rules = []
    for key, raw_rule in configured.items():
        if not isinstance(key, str) or not key or not isinstance(raw_rule, Mapping):
            raise BashConfigError("invalid Bash rule")
        rule_id = raw_rule.get("id")
        action = raw_rule.get("action")
        reason = raw_rule.get("reason")
        matcher = raw_rule.get("matcher")
        pattern = raw_rule.get("pattern")
        priority = raw_rule.get("priority", 0)
        alternative = raw_rule.get("safe_alternative")
        escalation = raw_rule.get("escalate_in_bypass")
        approved_root_exemption = raw_rule.get("allow_in_approved_roots", False)
        if rule_id != key or action not in _ACTIONS:
            raise BashConfigError("invalid Bash rule tier")
        if not isinstance(reason, str) or not reason.strip():
            raise BashConfigError("invalid Bash rule reason")
        if matcher not in _MATCHERS or not isinstance(pattern, str) or not pattern:
            raise BashConfigError("invalid Bash rule matcher")
        if not isinstance(priority, int) or isinstance(priority, bool):
            raise BashConfigError("invalid Bash rule priority")
        if action != "allow" and (
            not isinstance(alternative, str) or not alternative.strip()
        ):
            raise BashConfigError("invalid Bash rule safe alternative")
        if escalation not in {None, "deny"}:
            raise BashConfigError("invalid Bash bypass escalation")
        if not isinstance(approved_root_exemption, bool):
            raise BashConfigError("invalid Bash approved-root exemption")
        if matcher == "regex":
            try:
                re.compile(pattern)
            except re.error as error:
                raise BashConfigError("invalid Bash rule regex") from error
        rules.append(
            BashRule(
                rule_id,
                action,
                reason.strip(),
                matcher,
                pattern,
                priority,
                alternative.strip() if isinstance(alternative, str) else "",
                escalation == "deny",
                approved_root_exemption,
            )
        )
    return tuple(rules)


def _rule_matches(rule: BashRule, command: str) -> bool:
    if rule.matcher == "fixed_string":
        return rule.pattern.casefold() in command.casefold()
    return re.search(rule.pattern, command) is not None


def _configured_names(value: Any, field: str) -> frozenset[str]:
    if not isinstance(value, (list, tuple)) or not all(
        isinstance(item, str) and item.strip() for item in value
    ):
        raise BashConfigError(f"invalid Bash {field}")
    return frozenset(item.casefold() for item in value)


def _analysis_config(config: Mapping[str, Any]) -> Mapping[str, Any]:
    analysis = config.get("bash_analysis")
    if not isinstance(analysis, Mapping):
        raise BashConfigError("Bash analysis configuration is missing")
    path_commands = analysis.get("path_commands")
    if not isinstance(path_commands, Mapping):
        raise BashConfigError("Bash path-command configuration is missing")
    _configured_names(path_commands.get("read"), "read commands")
    _configured_names(path_commands.get("read_write"), "read-write commands")
    _configured_names(analysis.get("symlink_commands"), "symlink commands")
    _configured_names(analysis.get("symlink_options"), "symlink options")
    _configured_names(analysis.get("xargs_commands"), "xargs commands")
    _configured_names(
        analysis.get("destructive_path_commands"), "destructive path commands"
    )
    approved_roots = analysis.get("approved_destructive_roots")
    if not isinstance(approved_roots, (list, tuple)) or not all(
        isinstance(root, str) and root.strip() for root in approved_roots
    ):
        raise BashConfigError("invalid approved destructive roots")
    exfiltration = analysis.get("exfiltration_options")
    if not isinstance(exfiltration, Mapping) or not all(
        isinstance(command, str)
        and command.strip()
        and isinstance(options, (list, tuple))
        and options
        and all(isinstance(option, str) and option.strip() for option in options)
        for command, options in exfiltration.items()
    ):
        raise BashConfigError("invalid Bash exfiltration configuration")
    return analysis


def _tokens(command: str) -> tuple[str, ...]:
    if not isinstance(command, str) or not command.strip():
        raise ValueError("Bash command is missing")
    try:
        lexer = shlex.shlex(command, posix=True, punctuation_chars="|&;()<>")
        lexer.whitespace_split = True
        lexer.commenters = ""
        return tuple(lexer)
    except ValueError as error:
        raise ValueError("Bash command is malformed") from error


def _operands(tokens: tuple[str, ...], start: int) -> tuple[str, ...]:
    values = []
    for token in tokens[start:]:
        if token in _SEPARATORS or token in _REDIRECTIONS or token == "<<":
            break
        if token.startswith("-") or "=" in token and not token.startswith(("./", "../")):
            continue
        values.append(token.rstrip("\\n"))
    return tuple(value for value in values if value)


def _candidate_paths(
    tokens: tuple[str, ...], analysis: Mapping[str, Any]
) -> tuple[tuple[str, str], ...]:
    path_commands = analysis["path_commands"]
    read_commands = _configured_names(path_commands["read"], "read commands")
    read_write_commands = _configured_names(
        path_commands["read_write"], "read-write commands"
    )
    symlink_commands = _configured_names(analysis["symlink_commands"], "symlink commands")
    symlink_options = _configured_names(analysis["symlink_options"], "symlink options")
    xargs_commands = _configured_names(analysis["xargs_commands"], "xargs commands")
    destructive_commands = _configured_names(
        analysis["destructive_path_commands"], "destructive path commands"
    )
    exfiltration_options = {
        command.casefold(): frozenset(option.casefold() for option in options)
        for command, options in analysis["exfiltration_options"].items()
    }
    candidates: list[tuple[str, str]] = []

    for index, token in enumerate(tokens):
        command_name = os.path.basename(token).casefold()
        if command_name in read_commands:
            candidates.extend((operand, "read") for operand in _operands(tokens, index + 1))
        elif command_name in read_write_commands:
            operands = _operands(tokens, index + 1)
            if operands:
                candidates.append((operands[0], "read"))
                candidates.extend((operand, "write") for operand in operands[1:])
        elif command_name in symlink_commands:
            operands = _operands(tokens, index + 1)
            if any(
                token.casefold() in symlink_options for token in tokens[index + 1 :]
            ) and operands:
                candidates.append((operands[0], "read"))
        elif command_name in xargs_commands:
            for candidate in tokens[:index]:
                candidate = candidate.rstrip("\\n")
                if (
                    candidate
                    and candidate not in _SEPARATORS
                    and not candidate.startswith("-")
                ):
                    candidates.append((candidate, "read"))
        if command_name in destructive_commands:
            candidates.extend(
                (operand, "write") for operand in _operands(tokens, index + 1)
            )

        if command_name in exfiltration_options:
            options = exfiltration_options[command_name]
            position = index + 1
            while position < len(tokens) and tokens[position] not in _SEPARATORS:
                token = tokens[position]
                option, separator, value = token.partition("=")
                if option.casefold() in options:
                    if separator:
                        upload = value
                    elif position + 1 < len(tokens):
                        upload = tokens[position + 1]
                        position += 1
                    else:
                        upload = ""
                    if upload.startswith("@"):
                        upload = upload[1:]
                    if upload and upload != "-":
                        candidates.append((upload, "read"))
                position += 1

        if token in _REDIRECTIONS and index + 1 < len(tokens):
            candidates.append((tokens[index + 1], _REDIRECTIONS[token]))

    seen = set()
    return tuple(
        candidate
        for candidate in candidates
        if candidate not in seen and not seen.add(candidate)
    )


def _inside_approved_roots(
    command: str,
    analysis: Mapping[str, Any],
    *,
    cwd=None,
    home=None,
    case_sensitive=None,
) -> bool:
    tokens = _tokens(command)
    commands = _configured_names(
        analysis["destructive_path_commands"], "destructive path commands"
    )
    targets = []
    for index, token in enumerate(tokens):
        if os.path.basename(token).casefold() in commands:
            targets.extend(_operands(tokens, index + 1))
    if not targets:
        return False
    roots = [
        normalize_path(
            root, cwd=cwd, home=home, case_sensitive=case_sensitive
        ).rstrip("/")
        for root in analysis["approved_destructive_roots"]
    ]
    normalized_targets = [
        normalize_path(
            target, cwd=cwd, home=home, case_sensitive=case_sensitive
        )
        for target in targets
    ]
    return all(
        any(target == root or target.startswith(f"{root}/") for root in roots)
        for target in normalized_targets
    )


def analyze_command(
    command: str,
    config: Mapping[str, Any],
    path_rules,
    *,
    cwd=None,
    home=None,
    case_sensitive=None,
    bypass: bool = False,
) -> tuple[BashMatch, ...]:
    """Return all protected-path and configured Bash matches."""

    analysis = _analysis_config(config)
    tokens = _tokens(command)
    matches = []
    for candidate, access in _candidate_paths(tokens, analysis):
        match = evaluate_path(
            candidate,
            path_rules,
            cwd=cwd,
            home=home,
            case_sensitive=case_sensitive,
            bypass=bypass,
            access=access,
        )
        if match is not None and match.action != "allow":
            matches.append(
                BashMatch(
                    match.rule_id,
                    match.action,
                    match.reason,
                    match.safe_alternative,
                    match.normalized_path,
                )
            )
    for rule in load_bash_rules(config):
        if _rule_matches(rule, command):
            if rule.allow_in_approved_roots and _inside_approved_roots(
                command,
                analysis,
                cwd=cwd,
                home=home,
                case_sensitive=case_sensitive,
            ):
                continue
            action = "deny" if bypass and rule.escalate_in_bypass else rule.action
            if action != "allow":
                matches.append(
                    BashMatch(
                        rule.rule_id,
                        action,
                        rule.reason,
                        rule.safe_alternative,
                    )
                )
    return tuple(matches)


__all__ = (
    "BashConfigError",
    "BashMatch",
    "BashRule",
    "analyze_command",
    "load_bash_rules",
)
