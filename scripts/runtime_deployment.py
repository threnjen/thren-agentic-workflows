#!/usr/bin/env python3
"""Resolve generated assets to safe, current-user runtime destinations."""

from __future__ import annotations

import ntpath
import hashlib
import json
import os
import posixpath
import shutil
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path, PurePath, PurePosixPath, PureWindowsPath
from typing import Callable, Mapping, Sequence


SUPPORTED_PLATFORMS = frozenset({"darwin", "linux", "windows"})
MANAGED_METADATA = ".github-agents-managed.json"
GENERATED_MARKERS = frozenset(
    {
        "# Generated from .github/agents source-of-truth. Do not edit manually.",
        "<!-- Generated from .github/agents source-of-truth. Do not edit manually. -->",
        "<!-- Generated from .github/skills source-of-truth. Do not edit manually. -->",
    }
)


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
class HarnessManagedCopyResult:
    """Aggregated, content-safe managed-copy outcome for one harness."""

    status: str
    inventoried: int = 0
    staged: int = 0
    copied: int = 0
    replaced: int = 0
    removed: int = 0
    unchanged: int = 0
    collisions: int = 0
    failed: int = 0
    reconciliation_skipped: bool = False
    failures: tuple[str, ...] = ()


@dataclass(frozen=True)
class ManagedCopyResult:
    harnesses: Mapping[str, HarnessManagedCopyResult]


@dataclass
class _MutableHarnessResult:
    inventoried: int = 0
    staged: int = 0
    copied: int = 0
    replaced: int = 0
    removed: int = 0
    unchanged: int = 0
    collisions: int = 0
    failed: int = 0
    reconciliation_skipped: bool = False
    failures: list[str] | None = None

    def freeze(self) -> HarnessManagedCopyResult:
        return HarnessManagedCopyResult(
            status="failed" if self.failed else "verified",
            inventoried=self.inventoried,
            staged=self.staged,
            copied=self.copied,
            replaced=self.replaced,
            removed=self.removed,
            unchanged=self.unchanged,
            collisions=self.collisions,
            failed=self.failed,
            reconciliation_skipped=self.reconciliation_skipped,
            failures=tuple(self.failures or ()),
        )


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


def managed_copy_inventory(
    records: Sequence[DestinationRecord],
) -> tuple[dict[str, str], ...]:
    """Classify the current runtime state without following destination links."""
    generated_roots = tuple(Path(record.source).absolute() for record in records)
    inventory: list[dict[str, str]] = []
    for record in records:
        source, destination, home = _validate_record(record)
        relative = destination.relative_to(home).as_posix()
        source_fingerprint = hashlib.sha256(
            json.dumps(_tree_manifest(source), sort_keys=True).encode("utf-8")
        ).hexdigest()
        if not _entry_exists(destination):
            status = "planned_replacement"
        elif _is_link(destination):
            status = (
                "planned_replacement"
                if _link_is_owned(destination, generated_roots)
                else "collision"
            )
        elif not destination.is_dir() or not _metadata_entry_is_managed(destination):
            status = "collision"
        else:
            source_manifest = _tree_manifest(source)
            destination_manifest = {
                name: value
                for name, value in _tree_manifest(destination).items()
                if name != MANAGED_METADATA
            }
            metadata = _read_metadata(destination)
            generated_roots = tuple(Path(item.source).absolute() for item in records)
            has_collision = any(
                _entry_exists(destination / child.name)
                and not _entry_is_owned(
                    destination / child.name,
                    child.name,
                    metadata,
                    generated_roots,
                )
                for child in source.iterdir()
            )
            if has_collision:
                status = "collision"
            elif source_manifest == destination_manifest:
                status = "unchanged_managed_copy"
            else:
                status = "planned_replacement"
        inventory.append(
            {
                "harness": record.harness,
                "asset_class": record.asset_class,
                "status": status,
                "destination": "~/" + relative,
                "source_fingerprint": source_fingerprint,
            }
        )

        if destination.is_dir() and not _is_link(destination):
            expected = {path.name for path in source.iterdir()}
            metadata = _read_metadata(destination)
            for path in sorted(destination.iterdir(), key=lambda item: item.name):
                if path.name == MANAGED_METADATA or path.name in expected:
                    continue
                owned = _entry_is_owned(
                    path, path.name, metadata, generated_roots
                )
                inventory.append(
                    {
                        "harness": record.harness,
                        "asset_class": record.asset_class,
                        "status": (
                            "obsolete_owned_removal" if owned else "preserved_foreign"
                        ),
                        "destination": "~/" + path.relative_to(home).as_posix(),
                        "source_fingerprint": source_fingerprint,
                    }
                )
    return tuple(inventory)


def _entry_exists(path: Path) -> bool:
    """Test the directory entry without following a dangling link."""
    return os.path.lexists(path)


def _is_link(path: Path) -> bool:
    return path.is_symlink() or path.is_junction()


def _remove_entry(path: Path) -> None:
    """Remove exactly one entry; link targets are never traversed."""
    if _is_link(path) or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()


def _copy_source(source: Path, target: Path) -> None:
    """Copy one complete generated source tree into an absent staging path."""
    shutil.copytree(source, target, symlinks=False)


def _file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(128 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _tree_manifest(root: Path) -> dict[str, tuple[str, str]]:
    """Describe a regular staged/source tree; reject links and special files."""
    manifest: dict[str, tuple[str, str]] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if _is_link(path):
            raise OSError("generated_source_link")
        if path.is_dir():
            manifest[relative] = ("directory", "")
        elif path.is_file():
            manifest[relative] = ("file", _file_digest(path))
        else:
            raise OSError("unsupported_generated_entry")
    return manifest


def _validate_record(record: DestinationRecord) -> tuple[Path, Path, Path]:
    """Validate source and active-home boundaries before any enumeration."""
    if not all(isinstance(value, Path) for value in (record.source, record.destination, record.active_home)):
        raise DestinationResolutionError("non_native_destination")
    source = record.source.absolute()
    destination = record.destination.absolute()
    home = record.active_home.absolute()
    if home.is_symlink() or home.is_junction():
        raise DestinationResolutionError("linked_active_home")
    if not home.is_dir():
        raise DestinationResolutionError("invalid_active_home")
    try:
        destination.relative_to(home)
    except ValueError as exc:
        raise DestinationResolutionError("outside_active_home") from exc
    _check_existing_parents(destination, home)
    if not source.is_dir() or _is_link(source):
        raise DestinationResolutionError("generated_source_missing")
    return source, destination, home


def _recorded_target(path: Path) -> Path | None:
    """Return a link's recorded target without requiring that target to exist."""
    if not _is_link(path):
        return None
    try:
        raw = os.readlink(path)
    except OSError:
        # Native Windows junctions may not expose readlink consistently.
        try:
            return path.resolve(strict=False)
        except OSError:
            return None
    target = Path(raw)
    if not target.is_absolute():
        target = path.parent / target
    return target.resolve(strict=False)


def _inside_generated_roots(path: Path, generated_roots: Sequence[Path]) -> bool:
    target = path.resolve(strict=False)
    for root in generated_roots:
        try:
            target.relative_to(root.resolve())
            return True
        except ValueError:
            continue
    return False


def _link_is_owned(path: Path, generated_roots: Sequence[Path]) -> bool:
    target = _recorded_target(path)
    return target is not None and _inside_generated_roots(target, generated_roots)


def _generated_marker_line_index(text: str) -> int:
    if not text.startswith("---\n"):
        return 0
    lines = text.splitlines()
    for index in range(1, len(lines)):
        if lines[index] == "---":
            return index + 1
    return -1


def _file_has_generated_marker(path: Path) -> bool:
    if not path.is_file() or _is_link(path):
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return False
    index = _generated_marker_line_index(text)
    lines = text.splitlines()
    return index >= 0 and index < len(lines) and lines[index] in GENERATED_MARKERS


def _has_generated_marker(path: Path) -> bool:
    try:
        if _file_has_generated_marker(path):
            return True
        if path.is_dir() and not _is_link(path):
            return _file_has_generated_marker(path / "SKILL.md")
    except (OSError, PermissionError):
        return False
    return False


def _entry_fingerprint(path: Path) -> str | None:
    try:
        if path.is_file() and not _is_link(path):
            return "file:" + _file_digest(path)
        if path.is_dir() and not _is_link(path):
            encoded = json.dumps(_tree_manifest(path), sort_keys=True).encode("utf-8")
            return "directory:" + hashlib.sha256(encoded).hexdigest()
    except OSError:
        return None
    return None


def _read_metadata(destination: Path) -> dict[str, str]:
    metadata = destination / MANAGED_METADATA
    if not metadata.is_file() or _is_link(metadata):
        return {}
    try:
        payload = json.loads(metadata.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return {}
    if payload.get("schema") != 1 or not isinstance(payload.get("owned"), dict):
        return {}
    return {
        name: fingerprint
        for name, fingerprint in payload["owned"].items()
        if isinstance(name, str)
        and isinstance(fingerprint, str)
        and "/" not in name
        and name not in {"", ".", "..", MANAGED_METADATA}
    }


def _metadata_entry_is_managed(destination: Path) -> bool:
    metadata = destination / MANAGED_METADATA
    if not _entry_exists(metadata):
        return True
    if not metadata.is_file() or _is_link(metadata):
        return False
    try:
        payload = json.loads(metadata.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return False
    return payload.get("schema") == 1 and isinstance(payload.get("owned"), dict)


def _write_metadata(destination: Path, owned: set[str]) -> None:
    fingerprints = {
        name: fingerprint
        for name in sorted(owned)
        if (fingerprint := _entry_fingerprint(destination / name)) is not None
    }
    payload = json.dumps({"schema": 1, "owned": fingerprints}, indent=2) + "\n"
    metadata = destination / MANAGED_METADATA
    if not _metadata_entry_is_managed(destination):
        raise OSError("metadata_collision")
    expected_identity = _entry_identity(metadata)
    descriptor, stage_name = tempfile.mkstemp(
        prefix=f".{MANAGED_METADATA}.", suffix=".tmp", dir=destination
    )
    stage = Path(stage_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(payload)
        if _entry_identity(metadata) != expected_identity:
            raise OSError("metadata_changed")
        os.replace(stage, metadata)
    finally:
        if _entry_exists(stage):
            stage.unlink()


def _same_entry(left: Path, right: Path) -> bool:
    if _is_link(left) or _is_link(right):
        return False
    try:
        if left.is_file() and right.is_file():
            return _file_digest(left) == _file_digest(right)
        if left.is_dir() and right.is_dir():
            return _tree_manifest(left) == _tree_manifest(right)
    except OSError:
        return False
    return False


def _entry_is_owned(
    path: Path,
    name: str,
    metadata_owned: Mapping[str, str],
    generated_roots: Sequence[Path],
) -> bool:
    """Require positive, current ownership evidence for one destination entry."""
    return (
        (
            name in metadata_owned
            and _entry_fingerprint(path) == metadata_owned[name]
        )
        or _has_generated_marker(path)
        or (_is_link(path) and _link_is_owned(path, generated_roots))
    )


def _entry_identity(path: Path) -> tuple[int, int, int, int, int] | None:
    try:
        state = path.lstat()
    except FileNotFoundError:
        return None
    return (state.st_mode, state.st_dev, state.st_ino, state.st_size, state.st_mtime_ns)


def _replace_preserving_old(
    staged: Path,
    destination: Path,
    expected_identity: tuple[int, int, int, int, int] | None,
) -> None:
    """Install a verified stage, restoring the old entry if installation fails."""
    backup = destination.parent / f".{destination.name}.managed-backup"
    if _entry_exists(backup):
        raise OSError("backup_collision")
    if _entry_identity(destination) != expected_identity:
        raise OSError("destination_changed")
    had_old = _entry_exists(destination)
    if had_old:
        os.replace(destination, backup)
    try:
        os.replace(staged, destination)
    except Exception:
        if had_old and _entry_exists(backup) and not _entry_exists(destination):
            os.replace(backup, destination)
        raise
    if had_old and _entry_exists(backup):
        _remove_entry(backup)


def _install_staged_record(
    record: DestinationRecord,
    staged: Path,
    generated_roots: Sequence[Path],
    result: _MutableHarnessResult,
) -> set[str] | None:
    destination = Path(record.destination)
    if not _entry_exists(destination):
        destination.parent.mkdir(parents=True, exist_ok=True)
        owned = {child.name for child in staged.iterdir() if child.name != MANAGED_METADATA}
        _write_metadata(staged, owned)
        _replace_preserving_old(staged, destination, None)
        result.copied += 1
        return owned

    if _is_link(destination):
        identity = _entry_identity(destination)
        if not _link_is_owned(destination, generated_roots):
            result.collisions += 1
            _remove_entry(staged)
            return None
        owned = {child.name for child in staged.iterdir() if child.name != MANAGED_METADATA}
        _write_metadata(staged, owned)
        _replace_preserving_old(staged, destination, identity)
        result.replaced += 1
        return owned

    if not destination.is_dir():
        result.collisions += 1
        _remove_entry(staged)
        return None
    if not _metadata_entry_is_managed(destination):
        result.collisions += 1
        _remove_entry(staged)
        return None

    previous_owned = _read_metadata(destination)
    owned = set(previous_owned)
    for candidate in tuple(staged.iterdir()):
        final = destination / candidate.name
        identity = _entry_identity(final)
        if not _entry_exists(final):
            _replace_preserving_old(candidate, final, identity)
            result.copied += 1
            owned.add(candidate.name)
        elif _entry_is_owned(
            final, candidate.name, previous_owned, generated_roots
        ) and _same_entry(candidate, final):
            result.unchanged += 1
            owned.add(candidate.name)
            _remove_entry(candidate)
        elif _entry_is_owned(
            final, candidate.name, previous_owned, generated_roots
        ):
            _replace_preserving_old(candidate, final, identity)
            result.replaced += 1
            owned.add(candidate.name)
        else:
            result.collisions += 1
            owned.discard(candidate.name)
            _remove_entry(candidate)
    _remove_entry(staged)
    _write_metadata(destination, owned)
    return owned


def _prune_record(
    record: DestinationRecord,
    expected: set[str],
    managed: set[str],
    generated_roots: Sequence[Path],
    result: _MutableHarnessResult,
) -> None:
    destination = Path(record.destination)
    if not destination.is_dir() or _is_link(destination):
        return
    metadata_owned = _read_metadata(destination)
    retained = set(managed)
    for path in tuple(destination.iterdir()):
        if path.name == MANAGED_METADATA or path.name in expected:
            continue
        identity = _entry_identity(path)
        owned = _entry_is_owned(
            path, path.name, metadata_owned, generated_roots
        )
        if owned:
            if _entry_identity(path) == identity:
                _remove_entry(path)
                result.removed += 1
            else:
                result.collisions += 1
        else:
            result.collisions += 1
    _write_metadata(destination, retained)


def deploy_managed_copies(
    records: Sequence[DestinationRecord],
    *,
    copy_tree: Callable[[Path, Path], None] = _copy_source,
) -> ManagedCopyResult:
    """Stage, verify, install, then reconcile generated runtime copies.

    All records for a harness must stage successfully before that harness mutates
    destinations. Pruning starts only after every install for the harness succeeds.
    """
    grouped: dict[str, list[DestinationRecord]] = {}
    for record in records:
        grouped.setdefault(record.harness, []).append(record)
    generated_roots = tuple(Path(record.source).absolute() for record in records)
    final: dict[str, HarnessManagedCopyResult] = {}

    for harness, harness_records in grouped.items():
        outcome = _MutableHarnessResult(failures=[])
        stages: list[tuple[DestinationRecord, Path]] = []
        try:
            for record in harness_records:
                source, destination, _ = _validate_record(record)
                outcome.inventoried += 1
                destination.parent.mkdir(parents=True, exist_ok=True)
                stage = Path(tempfile.mkdtemp(prefix=f".{destination.name}.managed-stage-", dir=destination.parent))
                stage.rmdir()
                try:
                    source_manifest = _tree_manifest(source)
                    copy_tree(source, stage)
                    if source_manifest != _tree_manifest(stage):
                        raise OSError("stage_verification_failed")
                except Exception:
                    if _entry_exists(stage):
                        _remove_entry(stage)
                    raise
                stages.append((record, stage))
                outcome.staged += 1
        except Exception:
            for _, stage in stages:
                if _entry_exists(stage):
                    _remove_entry(stage)
            outcome.failed += 1
            outcome.reconciliation_skipped = True
            outcome.failures.append("staging_failed")
            final[harness] = outcome.freeze()
            continue

        expected_by_record: list[
            tuple[DestinationRecord, set[str], set[str] | None]
        ] = []
        try:
            for record, stage in stages:
                _validate_record(record)
                expected = {child.name for child in stage.iterdir()}
                installed = _install_staged_record(record, stage, generated_roots, outcome)
                expected_by_record.append((record, expected, installed))
        except Exception:
            for _, stage in stages:
                if _entry_exists(stage):
                    _remove_entry(stage)
            outcome.failed += 1
            outcome.reconciliation_skipped = True
            outcome.failures.append("replacement_failed")
            final[harness] = outcome.freeze()
            continue

        try:
            for record, expected, managed in expected_by_record:
                if managed is not None:
                    _prune_record(
                        record, expected, managed, generated_roots, outcome
                    )
        except Exception:
            outcome.failed += 1
            outcome.reconciliation_skipped = True
            outcome.failures.append("reconciliation_failed")
        final[harness] = outcome.freeze()

    return ManagedCopyResult(final)
