#!/usr/bin/env python3
"""Resolve generated assets to safe, current-user runtime destinations."""

from __future__ import annotations

import ntpath
import os
import posixpath
import sys
from dataclasses import dataclass
from pathlib import Path, PurePath, PurePosixPath, PureWindowsPath
from typing import Mapping, Sequence


SUPPORTED_PLATFORMS = frozenset({"darwin", "linux", "windows"})


class DestinationResolutionError(ValueError):
    """A content-safe destination-policy failure."""

    def __init__(self, category: str) -> None:
        self.category = category
        super().__init__(category)


@dataclass(frozen=True)
class PlatformFacts:
    """Injectable facts used to classify exactly one current environment."""

    system: str
    is_wsl: bool = False

    @classmethod
    def current(cls) -> "PlatformFacts":
        system = sys.platform.lower()
        if system.startswith("win"):
            return cls("windows")
        if system == "darwin":
            return cls("darwin")
        if system.startswith("linux"):
            release = ""
            try:
                release = os.uname().release.lower()
            except AttributeError:  # pragma: no cover - unavailable on Windows
                pass
            return cls("linux", "microsoft" in release or "wsl" in release)
        return cls(system)


@dataclass(frozen=True)
class DestinationRecord:
    """Read-only handoff consumed by managed-copy reconciliation."""

    harness: str
    asset_class: str
    source: Path
    destination: PurePath
    active_home: PurePath
    status: str = "planned"


@dataclass(frozen=True)
class _AssetPolicy:
    harness: str
    asset_class: str
    source_relative: str
    destination_relative: str
    root_kind: str


# Deliberately excludes generated instructions and Codex profiles: Phase 04's
# primary-documentation research established no runtime destination for either.
_ASSET_POLICIES: Sequence[_AssetPolicy] = (
    _AssetPolicy("claude", "agents", "claude/agents", "agents", "claude"),
    _AssetPolicy("claude", "commands", "claude/commands", "commands", "claude"),
    _AssetPolicy("claude", "skills", "claude/skills", "skills", "claude"),
    _AssetPolicy("claude", "learnings", "claude/learnings", "learnings", "claude"),
    _AssetPolicy("codex", "agents", "codex/agents", "agents", "codex"),
    _AssetPolicy("codex", "skills", "codex/skills", ".agents/skills", "home"),
    _AssetPolicy("opencode", "agents", "opencode/agents", "agents", "opencode"),
    _AssetPolicy(
        "opencode",
        "skills",
        "opencode/skills",
        ".config/opencode/skills",
        "home",
    ),
)


def classify_platform(facts: PlatformFacts) -> str:
    """Return one of darwin, linux, windows, or wsl."""
    system = facts.system.strip().lower()
    if system not in SUPPORTED_PLATFORMS:
        raise DestinationResolutionError("unsupported_platform")
    if facts.is_wsl and system != "linux":
        raise DestinationResolutionError("ambiguous_platform")
    return "wsl" if facts.is_wsl else system


def _path_type(platform: str):
    return PureWindowsPath if platform == "windows" else PurePosixPath


def _normalize(path: PurePath | Path | str, platform: str) -> PurePath:
    raw = os.fspath(path)
    if "\x00" in raw:
        raise DestinationResolutionError("invalid_override")
    if platform == "windows":
        normalized = ntpath.normpath(raw)
        return Path(normalized) if os.name == "nt" else PureWindowsPath(normalized)
    return Path(posixpath.normpath(raw))


def _validate_override(
    variable: str,
    environment: Mapping[str, str],
    *,
    active_home: PurePath,
    platform: str,
) -> PurePath | None:
    if variable not in environment:
        return None
    raw = environment[variable]
    if not isinstance(raw, str) or "\x00" in raw:
        raise DestinationResolutionError("invalid_override")
    if not raw:
        raise DestinationResolutionError("empty_override")

    if platform != "windows":
        windows_form = PureWindowsPath(raw)
        if windows_form.drive or "\\" in raw:
            raise DestinationResolutionError("cross_environment_path")
    elif raw.startswith("/"):
        raise DestinationResolutionError("cross_environment_path")

    normalized = _normalize(raw, platform)
    if not normalized.is_absolute():
        raise DestinationResolutionError("relative_override")
    if platform == "wsl" and len(normalized.parts) >= 3:
        if normalized.parts[1] == "mnt" and len(normalized.parts[2]) == 1:
            raise DestinationResolutionError("cross_environment_path")
    try:
        normalized.relative_to(active_home)
    except ValueError as exc:
        raise DestinationResolutionError("outside_active_home") from exc
    return normalized


def _check_existing_parents(destination: PurePath, active_home: PurePath) -> None:
    """Validate concrete parent entries without dereferencing the leaf."""
    if not isinstance(destination, Path) or not isinstance(active_home, Path):
        return

    declared_home = active_home.absolute()
    resolved_home = declared_home.resolve()
    try:
        relative_parent = destination.parent.relative_to(declared_home)
    except ValueError as exc:
        raise DestinationResolutionError("outside_active_home") from exc

    current = declared_home
    for part in relative_parent.parts:
        current = current / part
        if current.is_symlink():
            raise DestinationResolutionError("symlinked_parent")
        if current.is_junction():
            raise DestinationResolutionError("junction_parent")
        if current.exists() and not current.is_dir():
            raise DestinationResolutionError("parent_not_directory")
        if current.exists():
            try:
                current.resolve().relative_to(resolved_home)
            except ValueError as exc:
                raise DestinationResolutionError("outside_active_home") from exc


def resolve_runtime_destinations(
    *,
    repo_root: Path,
    active_home: PurePath | Path | None = None,
    environment: Mapping[str, str] | None = None,
    platform_facts: PlatformFacts | None = None,
    require_sources: bool = True,
) -> tuple[DestinationRecord, ...]:
    """Build the complete normalized destination inventory without mutation."""
    facts = platform_facts or PlatformFacts.current()
    platform = classify_platform(facts)
    home_input = active_home if active_home is not None else Path.home()
    normalized_home = _normalize(home_input, platform)
    if not normalized_home.is_absolute():
        raise DestinationResolutionError("relative_active_home")

    env = environment if environment is not None else os.environ
    claude_override = _validate_override(
        "CLAUDE_CONFIG_DIR", env, active_home=normalized_home, platform=platform
    )
    codex_override = _validate_override(
        "CODEX_HOME", env, active_home=normalized_home, platform=platform
    )
    opencode_override = _validate_override(
        "OPENCODE_CONFIG_DIR", env, active_home=normalized_home, platform=platform
    )

    claude_root = claude_override or normalized_home / ".claude"
    codex_root = codex_override or normalized_home / ".codex"
    opencode_root = opencode_override or normalized_home / ".config/opencode"

    if codex_override is not None and require_sources:
        concrete_codex_home = Path(os.fspath(codex_override))
        if not concrete_codex_home.is_dir():
            raise DestinationResolutionError("codex_home_not_directory")

    roots = {
        "home": normalized_home,
        "claude": claude_root,
        "codex": codex_root,
        "opencode": opencode_root,
    }
    records: list[DestinationRecord] = []
    concrete_repo = repo_root.absolute()
    for policy in _ASSET_POLICIES:
        source = concrete_repo / policy.source_relative
        if require_sources and not source.is_dir():
            raise DestinationResolutionError("generated_source_missing")
        destination = _normalize(
            roots[policy.root_kind] / policy.destination_relative, platform
        )
        try:
            destination.relative_to(normalized_home)
        except ValueError as exc:
            raise DestinationResolutionError("outside_active_home") from exc
        _check_existing_parents(destination, normalized_home)
        records.append(
            DestinationRecord(
                harness=policy.harness,
                asset_class=policy.asset_class,
                source=source,
                destination=destination,
                active_home=normalized_home,
            )
        )
    return tuple(records)


def destination_inventory(
    records: Sequence[DestinationRecord],
) -> tuple[dict[str, str], ...]:
    """Return a reviewable inventory without exposing the full active-home path."""
    inventory: list[dict[str, str]] = []
    for record in records:
        relative = record.destination.relative_to(record.active_home)
        inventory.append(
            {
                "harness": record.harness,
                "asset_class": record.asset_class,
                "status": record.status,
                "destination": "~/" + relative.as_posix(),
            }
        )
    return tuple(inventory)
