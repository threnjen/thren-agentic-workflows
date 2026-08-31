#!/usr/bin/env python3
"""Deploy generated ports/ assets to real harness config directories.

Copies `ports/<harness>/` outputs to the user-level directories each harness
reads (`~/.claude`, `~/.codex`, `~/.config/opencode`, `~/.cursor`). Safe by
construction: a destination file is only ever overwritten or pruned when it
positively carries a generated marker (or lives inside a generated skill
directory) — hand-maintained files are never touched.

Usage:
  deploy_agents.py                       # use saved selection; prompt if none (tty)
  deploy_agents.py --harness claude,cursor
  deploy_agents.py --all
  deploy_agents.py --watch               # maintainer: auto-deploy on ports/ change
  deploy_agents.py --list                # show harnesses and resolved destinations

The selection is saved to `.deploy-config.json` (gitignored) so re-runs are just
`python3 deploy_agents.py`.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, List, Mapping, Sequence, Tuple

from scripts.asset_paths import (
    GENERATED_AGENT_MARKDOWN_HEADER,
    PORTS_DIR,
    REPO_ROOT,
    file_has_generated_marker,
    generated_marker_line_index,
    poll_watch,
)

CONFIG_PATH = REPO_ROOT / ".deploy-config.json"

HARNESSES = ("claude", "codex", "opencode", "cursor", "github")
COMMS_PROFILE_KEY = "comms_profile"
REGISTRATION_OWNERSHIP_TAG = "<!-- crosswire-comms-registration -->"
PROBE_SUCCESS_TOKEN = "CROSSWIRE_HOOK_PROBE_OK"
PROBE_FAILURE_TOKEN = "CROSSWIRE_HOOK_PROBE_FAILED"
PROBE_TIMEOUT_SECONDS = 10


@dataclass(frozen=True)
class DeployConfig:
    """Normalized persisted deployment selection."""

    harnesses: List[str]
    comms_profile: bool = False


@dataclass(frozen=True)
class RegistrationAdapter:
    """Format-specific seams consumed by the shared registration lifecycle."""

    target_path: Callable[[Path], Path]
    config_path: Callable[[Path], Path]
    upsert: Callable[[bytes, Path], bytes]
    remove: Callable[[bytes], Tuple[bytes, str]]

# `code-review-graph install --platform` vocabulary, keyed by our harness name.
# Only the harnesses this repo ports to get configured; the tool's other
# platforms are reachable by running its CLI directly.
CRG_PLATFORMS = {
    "claude": "claude-code",
    "codex": "codex",
    "opencode": "opencode",
    "cursor": "cursor",
    "github": "copilot",
}

# Baseline user-global instructions (CLAUDE.md / AGENTS.md / Cursor rule).
# Rendered at deploy time so the discovery paths reflect this machine's real
# home directory, then spliced into the destination file between sentinel
# comments — content outside the sentinels is never touched.
BASELINE_TEMPLATE = REPO_ROOT / "source_of_truth" / "baseline" / "baseline-instructions.md"
BASELINE_INSTRUCTIONS_DIR = REPO_ROOT / "source_of_truth" / "instructions"
# Sections this repo used to splice and no longer does. Dropping a name from the
# baseline list only stops rewriting the block; the stale one already in a
# deployed file would sit there forever. Listing it here deletes it on the next
# deploy. A name stays here until every machine has deployed past it.
RETIRED_BASELINE_SECTIONS = ("context7", "phase-doc-sync", "know-the-audience")
# Cursor has no user-global AGENTS.md; its native global channel is a rule file.
CURSOR_BASELINE_FRONTMATTER = "---\nalwaysApply: true\n---\n\n"

# The github "harness" deploys into this repository, not the home directory: it
# mirrors ports/github verbatim into .github/ so GitHub-side tooling reads the
# same source of truth. Its files carry no generated marker (they are exact
# copies), so the whole mirrored tree is treated as managed.
GITHUB_MIRRORED_SUBDIRS = ("agents", "hooks", "instructions", "learnings", "skills")


def _environment_root(
    env_var: str,
    default: str | Path,
    *,
    home: Path,
    environ: Mapping[str, str],
) -> Path:
    raw = environ.get(env_var, "")
    return Path(raw).expanduser() if raw else home / default


def harness_root(
    harness: str,
    *,
    home: Path | None = None,
    environ: Mapping[str, str] | None = None,
) -> Path:
    """Resolve the configuration root using the same rules as asset deployment."""
    home = Path(home).expanduser() if home else Path.home()
    environ = os.environ if environ is None else environ
    if harness == "claude":
        return _environment_root("CLAUDE_CONFIG_DIR", ".claude", home=home, environ=environ)
    if harness == "codex":
        return _environment_root("CODEX_HOME", ".codex", home=home, environ=environ)
    if harness == "opencode":
        return _environment_root(
            "OPENCODE_CONFIG_DIR", Path(".config") / "opencode", home=home, environ=environ
        )
    if harness == "cursor":
        return home / ".cursor"
    if harness == "github":
        return REPO_ROOT / ".github"
    raise ValueError(f"unknown harness: {harness}")


def harness_mappings(
    harness: str,
    *,
    home: Path | None = None,
    environ: Mapping[str, str] | None = None,
) -> List[Tuple[Path, Path]]:
    """(port source dir, real destination dir) pairs for one harness."""
    home = Path(home).expanduser() if home else Path.home()
    environ = os.environ if environ is None else environ

    port = PORTS_DIR / harness
    if harness == "claude":
        base = harness_root(harness, home=home, environ=environ)
        # learnings/ has no runtime destination under the config dir: every
        # consumer reads `.github/learnings/` in the working repo, so a copy
        # here would be read by nothing. Cursor is the exception - its
        # learnings ship as agent-requested rules under rules/.
        return [(port / sub, base / sub) for sub in ("agents", "commands", "skills")]
    if harness == "codex":
        base = harness_root(harness, home=home, environ=environ)
        # codex profiles/ has no documented runtime destination and is not
        # deployed; neither does learnings/ (see the claude branch above).
        return [
            (port / "agents", base / "agents"),
            (port / "skills", home / ".agents" / "skills"),
        ]
    if harness == "opencode":
        base = harness_root(harness, home=home, environ=environ)
        return [(port / sub, base / sub) for sub in ("agents", "skills")]
    if harness == "cursor":
        base = harness_root(harness, home=home, environ=environ)
        return [
            (port / sub, base / sub)
            for sub in ("agents", "commands", "rules", "skills")
        ]
    if harness == "github":
        base = harness_root(harness, home=home, environ=environ)
        return [(port / sub, base / sub) for sub in GITHUB_MIRRORED_SUBDIRS]
    raise ValueError(f"unknown harness: {harness}")


def _is_managed(dest_file: Path, dest_root: Path) -> bool:
    """Whether `dest_file` is provably ours: marked, or inside a marked skill dir.

    Skill auxiliary files carry no marker of their own; ownership of the whole
    directory is proven by its SKILL.md. Anything else unmarked is foreign and
    must never be overwritten or pruned.
    """
    if file_has_generated_marker(dest_file):
        return True
    if dest_root not in dest_file.parents:
        return False
    for parent in dest_file.parents:
        if parent == dest_root:
            break
        if file_has_generated_marker(parent / "SKILL.md"):
            return True
    return False


def deploy_harness(
    harness: str,
    *,
    home: Path | None = None,
    environ: Mapping[str, str] | None = None,
) -> Dict[str, object]:
    """Copy one harness's ports/ outputs to its real directories and prune stale copies."""
    copied = 0
    pruned = 0
    skipped: List[str] = []
    # Verbatim mirror: every file in the mapped subtrees is ours by definition.
    unconditional = harness == "github"

    for source_root, dest_root in harness_mappings(harness, home=home, environ=environ):
        expected: set[Path] = set()

        # The pre-split deployment linked destination roots straight into this
        # repository. Those links are ours: replace them (dangling or not) with a
        # real directory so managed copies can land. A symlink pointing anywhere
        # else is foreign — leave it alone and skip the mapping.
        if dest_root.is_symlink():
            target = Path(os.readlink(dest_root))
            points_into_repo = REPO_ROOT == target or REPO_ROOT in target.parents
            if points_into_repo or not dest_root.exists():
                dest_root.unlink()
            else:
                skipped.append(str(dest_root))
                continue

        if source_root.is_dir():
            for source_file in sorted(source_root.rglob("*")):
                if not source_file.is_file() or source_file.is_symlink():
                    continue
                dest_file = dest_root / source_file.relative_to(source_root)
                expected.add(dest_file)
                data = source_file.read_bytes()

                if dest_file.is_symlink():
                    skipped.append(str(dest_file))
                    continue
                if dest_file.is_file():
                    try:
                        if dest_file.read_bytes() == data:
                            continue
                    except OSError:
                        skipped.append(str(dest_file))
                        continue
                    if not unconditional and not _is_managed(dest_file, dest_root):
                        skipped.append(str(dest_file))
                        continue
                try:
                    dest_file.parent.mkdir(parents=True, exist_ok=True)
                    dest_file.write_bytes(data)
                except OSError:
                    skipped.append(str(dest_file))
                    continue
                copied += 1

        if dest_root.is_dir() and not dest_root.is_symlink():
            for path in sorted(dest_root.rglob("*"), reverse=True):
                if path in expected or path.is_symlink():
                    continue
                if path.is_file() and (unconditional or _is_managed(path, dest_root)):
                    path.unlink()
                    pruned += 1
                elif path.is_dir() and not any(path.iterdir()):
                    path.rmdir()

    result: Dict[str, object] = {"copied": copied, "pruned": pruned, "skipped_unmanaged": len(skipped)}
    if skipped:
        # Surfaced so a fail-closed skip is a visible decision for the user, not
        # a silent one. These files exist at the destination without a generated
        # marker; delete them by hand if they are stale copies you want replaced.
        result["skipped_paths"] = skipped
    return result


def baseline_destination(
    harness: str,
    *,
    home: Path | None = None,
    environ: Mapping[str, str] | None = None,
) -> Path | None:
    """User-global instructions file for one harness; None when it has none."""
    home = Path(home).expanduser() if home else Path.home()
    environ = os.environ if environ is None else environ

    if harness == "claude":
        return harness_root(harness, home=home, environ=environ) / "CLAUDE.md"
    if harness == "codex":
        return harness_root(harness, home=home, environ=environ) / "AGENTS.md"
    if harness == "opencode":
        return harness_root(harness, home=home, environ=environ) / "AGENTS.md"
    if harness == "cursor":
        return harness_root(harness, home=home, environ=environ) / "rules" / "baseline-instructions.mdc"
    if harness == "github":
        # Copilot's repo-wide instructions file; .github/AGENTS.md would only
        # scope to files under .github/ (nearest-file precedence).
        return REPO_ROOT / ".github" / "copilot-instructions.md"
    return None


def _baseline_substitutions(
    harness: str,
    *,
    home: Path,
    environ: Mapping[str, str],
) -> Dict[str, str]:
    """Placeholder values for the agent-discovery section, per harness."""
    if harness == "github":
        # Copilot's cloud agent runs inside the repository; discovery paths are
        # repo-relative and there is no user-global location.
        return {
            "{harness_title}": "Copilot",
            "{agent_paths}": "1. The repository's `.github/agents/`",
            "{skill_paths}": "1. The repository's `.github/skills/`",
        }
    dests = dict(
        (source.name, dest) for source, dest in harness_mappings(harness, home=home, environ=environ)
    )
    project_dirs = {
        "claude": (".claude/agents", ".claude/skills"),
        "codex": (".codex/agents", ".agents/skills"),
        "opencode": (".opencode/agents", ".opencode/skills"),
        "cursor": (".cursor/commands", ".cursor/rules"),
    }[harness]
    agent_global = dests.get("agents") or dests.get("commands")
    skill_global = dests.get("skills") or dests.get("rules")

    def numbered(project_dir: str, global_dir: Path) -> str:
        return f"1. The project's `{project_dir}`\n2. `{global_dir}`"

    return {
        "{harness_title}": harness.capitalize(),
        "{agent_paths}": numbered(project_dirs[0], agent_global),
        "{skill_paths}": numbered(project_dirs[1], skill_global),
    }


def baseline_section_names(template: str | None = None) -> Tuple[str, ...]:
    """Instruction names listed in the baseline template, in listed order.

    The template is a prose file with a bullet list; only the bullets are read,
    so the surrounding explanation can change freely without affecting deploys.
    """
    if template is None:
        template = BASELINE_TEMPLATE.read_text(encoding="utf-8")
    return tuple(re.findall(r"^- ([a-z0-9-]+)$", template, re.MULTILINE))


def _instruction_body(name: str) -> str:
    """Body of one baseline instruction, ready to splice.

    Strips the frontmatter, drops the trailing Load Canary section, and demotes
    the leading H1 to an H2. A per-instruction canary proves that instruction was
    inlined into one agent. Firing every one of them from the always-loaded global
    file would say nothing about routing and would cost a line per section, so the
    baseline carries a single aggregate canary instead. See `_baseline_canary_body`.
    """
    text = (BASELINE_INSTRUCTIONS_DIR / f"{name}.instructions.md").read_text(encoding="utf-8")
    if text.startswith("---\n"):
        end = text.index("\n---\n", 3) + len("\n---\n")
        text = text[end:]
    lines = text.splitlines()
    marker_index = generated_marker_line_index(text)
    if marker_index >= 0 and marker_index < len(lines):
        if lines[marker_index] == GENERATED_AGENT_MARKDOWN_HEADER:
            del lines[marker_index]
            text = "\n".join(lines) + "\n"
    text = re.sub(r"\n#{2,}\s*Load Canary\s*\n.*\Z", "\n", text, flags=re.DOTALL)
    text = re.sub(r"\A\s*# ", "## ", text)
    return text.strip("\n")


BASELINE_CANARY_SECTION = "baseline-canary"


def _baseline_canary_body(names: Sequence[str]) -> str:
    """One canary covering the whole baseline, naming every section it deployed.

    Per-instruction canaries are stripped on the way in, so without this the
    baseline loads silently and a stale global file is indistinguishable from a
    current one. Listing the count and the names makes that visible: a deploy the
    user forgot to run reports a section list that does not match the manifest.
    """
    listed = ", ".join(names)
    return (
        "## Baseline Load Canary\n\n"
        "When this file is loaded, state once, before your first substantive "
        f"output: *\"Baseline loaded: {len(names)} sections - {listed}.\"* "
        "Then proceed normally."
    )


def _parse_baseline_sections(template: str) -> Dict[str, str]:
    """Body of every instruction the baseline template lists, keyed by name."""
    return {name: _instruction_body(name) for name in baseline_section_names(template)}


def _strip_section(existing: str, name: str) -> str:
    """Remove a retired sentinel-delimited section, and the blank line it left."""
    sentinel = f"<!-- {name} -->"
    pattern = re.compile(r"\n*" + re.escape(sentinel) + r"\n?.*?" + re.escape(sentinel) + r"\n*", re.DOTALL)
    if not pattern.search(existing):
        return existing
    match = pattern.search(existing)
    assert match is not None
    replacement = "\n" if match.end() == len(existing) else "\n\n"
    stripped = existing[: match.start()] + replacement + existing[match.end() :]
    return stripped.lstrip("\n")


def _splice_section(existing: str, name: str, body: str) -> str:
    """Replace the sentinel-delimited section in `existing`, or append it."""
    sentinel = f"<!-- {name} -->"
    block = f"{sentinel}\n{body}\n{sentinel}"
    pattern = re.compile(re.escape(sentinel) + r"\n?.*?" + re.escape(sentinel), re.DOTALL)
    if pattern.search(existing):
        return pattern.sub(lambda _match: block, existing, count=1)
    if existing and not existing.endswith("\n"):
        existing += "\n"
    separator = "\n" if existing else ""
    return f"{existing}{separator}{block}\n"


def deploy_baseline(
    harness: str,
    *,
    home: Path | None = None,
    environ: Mapping[str, str] | None = None,
    comms_enabled: bool = False,
) -> Dict[str, str]:
    """Splice the rendered baseline sections into the harness's global file."""
    comms_enabled = _normalize_comms_profile(comms_enabled)
    home = Path(home).expanduser() if home else Path.home()
    environ = os.environ if environ is None else environ

    dest = baseline_destination(harness, home=home, environ=environ)
    if dest is None:
        return {"status": "not-applicable"}
    try:
        template = BASELINE_TEMPLATE.read_text(encoding="utf-8")
    except OSError as exc:
        return {"status": "failed", "detail": f"cannot read template: {exc}"}

    substitutions = _baseline_substitutions(harness, home=home, environ=environ)
    try:
        sections = _parse_baseline_sections(template)
    except OSError as exc:
        # A listed name with no instruction file must fail loudly: splicing the
        # rest would deploy a silently partial baseline.
        return {"status": "failed", "detail": f"cannot read baseline instruction: {exc}"}
    if dest.is_symlink():
        return {"status": "skipped", "detail": f"{dest} is a symlink"}
    try:
        existing = dest.read_text(encoding="utf-8") if dest.is_file() else ""
    except OSError as exc:
        return {"status": "failed", "detail": str(exc)}

    created = not dest.is_file()
    updated = existing
    if created and harness == "cursor":
        updated = CURSOR_BASELINE_FRONTMATTER
    for name in RETIRED_BASELINE_SECTIONS:
        updated = _strip_section(updated, name)
    if not comms_enabled:
        sections.pop("comms-protocol", None)
        updated = _strip_section(updated, "comms-protocol")
    updated = _splice_section(
        updated, BASELINE_CANARY_SECTION, _baseline_canary_body(tuple(sections))
    )
    for name, body in sections.items():
        for placeholder, value in substitutions.items():
            body = body.replace(placeholder, value)
        updated = _splice_section(updated, name, body)

    if updated == existing:
        return {"status": "unchanged", "path": str(dest)}
    try:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(updated, encoding="utf-8")
    except OSError as exc:
        return {"status": "failed", "detail": str(exc)}
    return {"status": "created" if created else "updated", "path": str(dest)}


def _reject_nonstandard_json_constant(value: str) -> object:
    raise ValueError(f"non-standard JSON constant: {value}")


_CLAUDE_JSON_DECODER = json.JSONDecoder(parse_constant=_reject_nonstandard_json_constant)


def _claude_json_skip_whitespace(text: str, index: int) -> int:
    while index < len(text) and text[index] in " \t\r\n":
        index += 1
    return index


def _claude_json_object_members(text: str, start: int) -> List[Tuple[str, int, int]]:
    if text[start] != "{":
        raise ValueError("JSON value is not an object")
    members: List[Tuple[str, int, int]] = []
    index = _claude_json_skip_whitespace(text, start + 1)
    if index < len(text) and text[index] == "}":
        return members
    keys: set[str] = set()
    while True:
        index = _claude_json_skip_whitespace(text, index)
        key, index = _CLAUDE_JSON_DECODER.raw_decode(text, index)
        if not isinstance(key, str):
            raise ValueError("JSON object key is not a string")
        if key in keys:
            raise ValueError(f"duplicate JSON object key: {key}")
        keys.add(key)
        index = _claude_json_skip_whitespace(text, index)
        if index >= len(text) or text[index] != ":":
            raise ValueError("JSON object member has no colon")
        value_start = _claude_json_skip_whitespace(text, index + 1)
        _, value_end = _CLAUDE_JSON_DECODER.raw_decode(text, value_start)
        members.append((key, value_start, value_end))
        index = _claude_json_skip_whitespace(text, value_end)
        if index >= len(text):
            raise ValueError("unterminated JSON object")
        if text[index] == "}":
            return members
        if text[index] != ",":
            raise ValueError("JSON object member has no separator")
        index += 1


def _claude_json_array_items(text: str, start: int) -> List[Tuple[int, int]]:
    if text[start] != "[":
        raise ValueError("JSON value is not an array")
    items: List[Tuple[int, int]] = []
    index = _claude_json_skip_whitespace(text, start + 1)
    if index < len(text) and text[index] == "]":
        return items
    while True:
        value_start = _claude_json_skip_whitespace(text, index)
        _, value_end = _CLAUDE_JSON_DECODER.raw_decode(text, value_start)
        items.append((value_start, value_end))
        index = _claude_json_skip_whitespace(text, value_end)
        if index >= len(text):
            raise ValueError("unterminated JSON array")
        if text[index] == "]":
            return items
        if text[index] != ",":
            raise ValueError("JSON array item has no separator")
        index += 1


def _claude_json_member(
    text: str, object_start: int, name: str
) -> Tuple[int, int] | None:
    for key, value_start, value_end in _claude_json_object_members(text, object_start):
        if key == name:
            return value_start, value_end
    return None


def _claude_settings_document(existing: bytes) -> Tuple[str, Dict[str, object]]:
    if not existing:
        return "", {}
    text = existing.decode("utf-8")
    document = _CLAUDE_JSON_DECODER.decode(text)
    if not isinstance(document, dict):
        raise ValueError("Claude settings root must be an object")
    hooks = document.get("hooks")
    if "hooks" in document and not isinstance(hooks, dict):
        raise ValueError("Claude settings hooks must be an object")
    if isinstance(hooks, dict):
        for event, groups in hooks.items():
            if not isinstance(event, str) or not isinstance(groups, list):
                raise ValueError("Claude hook event collections must be arrays")
            for group in groups:
                if not isinstance(group, dict):
                    raise ValueError("Claude hook groups must be objects")
                nested_hooks = group.get("hooks")
                if not isinstance(nested_hooks, list):
                    raise ValueError("Claude hook group hooks must be an array")
                if any(not isinstance(hook, dict) for hook in nested_hooks):
                    raise ValueError("Claude hook entries must be objects")
    return text, document


def _claude_command(config_path: Path) -> str:
    quoted_path = shlex.quote(str(config_path))
    return (
        f"crosswire-turn-hook --adapter claude --config {quoted_path} "
        f"# {REGISTRATION_OWNERSHIP_TAG}"
    )


def _claude_group(config_path: Path) -> Dict[str, object]:
    return {
        "matcher": "",
        "hooks": [
            {
                "type": "command",
                "command": _claude_command(config_path),
                "timeout": 10,
            }
        ],
    }


def _claude_json_compact(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def _claude_json_insert_member(
    text: str, object_start: int, object_end: int, key: str, value: object
) -> str:
    member = f"{json.dumps(key)}:{_claude_json_compact(value)}"
    content_start = object_start + 1
    content_end = object_end - 1
    trimmed_end = content_end
    while trimmed_end > content_start and text[trimmed_end - 1] in " \t\r\n":
        trimmed_end -= 1
    if trimmed_end == content_start:
        return text[:content_start] + member + text[content_start:]
    return text[:trimmed_end] + "," + member + text[trimmed_end:]


def _claude_json_append_array_item(text: str, array_start: int, value: object) -> str:
    _, array_end = _CLAUDE_JSON_DECODER.raw_decode(text, array_start)
    items = _claude_json_array_items(text, array_start)
    item = _claude_json_compact(value)
    if items:
        trailing = text[items[-1][1] : array_end - 1]
        return text[: items[-1][1]] + "," + trailing + item + text[array_end - 1 :]
    insertion = _claude_json_skip_whitespace(text, array_start + 1)
    return text[:insertion] + item + text[insertion:]


def _owned_command_span(
    text: str, group_start: int
) -> Tuple[int, int, str] | None:
    nested_member = _claude_json_member(text, group_start, "hooks")
    if nested_member is None:
        return None
    nested_start, _ = nested_member
    for hook_start, _ in _claude_json_array_items(text, nested_start):
        command_member = _claude_json_member(text, hook_start, "command")
        if command_member is None:
            continue
        command_start, command_end = command_member
        command, _ = _CLAUDE_JSON_DECODER.raw_decode(text, command_start)
        if isinstance(command, str) and REGISTRATION_OWNERSHIP_TAG in command:
            return command_start, command_end, command
    return None


def _claude_stop_array(text: str) -> Tuple[int, List[Tuple[int, int]]] | None:
    root_start = _claude_json_skip_whitespace(text, 0)
    hooks_member = _claude_json_member(text, root_start, "hooks")
    if hooks_member is None:
        return None
    hooks_start, _ = hooks_member
    stop_member = _claude_json_member(text, hooks_start, "Stop")
    if stop_member is None:
        return None
    stop_start, _ = stop_member
    return stop_start, _claude_json_array_items(text, stop_start)


def _remove_owned_stop_groups(
    text: str, stop_start: int, items: List[Tuple[int, int]]
) -> Tuple[str, str, int]:
    owned: List[int] = []
    removed: List[str] = []
    for index, (item_start, item_end) in enumerate(items):
        if _owned_command_span(text, item_start) is not None:
            owned.append(index)
            removed.append(text[item_start:item_end])
    if not owned:
        return text, "", 0

    edits: List[Tuple[int, int]] = []
    cluster_start = cluster_end = owned[0]
    clusters: List[Tuple[int, int]] = []
    for index in owned[1:]:
        if index == cluster_end + 1:
            cluster_end = index
        else:
            clusters.append((cluster_start, cluster_end))
            cluster_start = cluster_end = index
    clusters.append((cluster_start, cluster_end))
    for first, last in clusters:
        if first > 0:
            edits.append((items[first - 1][1], items[last][1]))
        elif last + 1 < len(items):
            edits.append((items[first][0], items[last + 1][0]))
        else:
            edits.append((items[first][0], items[last][1]))
    updated = text
    for start, end in reversed(edits):
        updated = updated[:start] + updated[end:]
    return updated, "\n".join(removed), len(owned)


def _claude_upsert(existing: bytes, config_path: Path) -> bytes:
    text, _ = _claude_settings_document(existing)
    owned_group = _claude_group(config_path)
    if not text:
        return (json.dumps({"hooks": {"Stop": [owned_group]}}, indent=2) + "\n").encode(
            "utf-8"
        )
    stop_data = _claude_stop_array(text)
    if stop_data is None:
        root_start = _claude_json_skip_whitespace(text, 0)
        hooks_member = _claude_json_member(text, root_start, "hooks")
        if hooks_member is None:
            _, root_end = _CLAUDE_JSON_DECODER.raw_decode(text, root_start)
            updated = _claude_json_insert_member(
                text, root_start, root_end, "hooks", {"Stop": [owned_group]}
            )
            return updated.encode("utf-8")
        hooks_start, hooks_end = hooks_member
        updated = _claude_json_insert_member(
            text, hooks_start, hooks_end, "Stop", [owned_group]
        )
        return updated.encode("utf-8")

    stop_start, items = stop_data
    owned_info: List[Tuple[int, int, str]] = []
    owned_indices: List[int] = []
    for index, (item_start, item_end) in enumerate(items):
        command_span = _owned_command_span(text, item_start)
        if command_span is not None:
            owned_indices.append(index)
            owned_info.append(command_span)
    desired = str(owned_group["hooks"][0]["command"])
    if len(owned_indices) == 1 and owned_info[0][2] == desired:
        return existing
    if len(owned_indices) == 1:
        command_start, command_end, _ = owned_info[0]
        updated = text[:command_start] + json.dumps(desired) + text[command_end:]
        return updated.encode("utf-8")
    if owned_indices:
        updated, _, _ = _remove_owned_stop_groups(text, stop_start, items)
        stop_data = _claude_stop_array(updated)
        if stop_data is None:
            raise ValueError("Claude Stop collection disappeared")
        stop_start, _ = stop_data
        updated = _claude_json_append_array_item(updated, stop_start, owned_group)
        return updated.encode("utf-8")
    updated = _claude_json_append_array_item(text, stop_start, owned_group)
    return updated.encode("utf-8")


def _claude_remove(existing: bytes) -> Tuple[bytes, str]:
    if not existing:
        return existing, ""
    text, _ = _claude_settings_document(existing)
    stop_data = _claude_stop_array(text)
    if stop_data is None:
        return existing, ""
    stop_start, items = stop_data
    updated, removed, _ = _remove_owned_stop_groups(text, stop_start, items)
    return updated.encode("utf-8"), removed


def _claude_target_path(root: Path) -> Path:
    return root / "settings.json"


def _claude_config_path(root: Path) -> Path:
    # [PROPOSED - name TBD] Portable default until the host config contract
    # supplies a user-global location. Callers can always inject config_path.
    return root / "hook-config.json"


REGISTRATION_ADAPTERS: Dict[str, RegistrationAdapter] = {
    "claude": RegistrationAdapter(
        target_path=_claude_target_path,
        config_path=_claude_config_path,
        upsert=_claude_upsert,
        remove=_claude_remove,
    )
}


def _normalize_comms_profile(value: object) -> bool:
    return value if type(value) is bool else False


def _has_symlink_component(path: Path) -> bool:
    """Whether any existing component of a path is a symlink."""
    current = path.absolute()
    while True:
        if current.is_symlink():
            return True
        parent = current.parent
        if parent == current:
            return False
        current = parent


def _safe_replace(path: Path, data: bytes) -> None:
    """Replace a registration file without truncating an existing target."""
    if _has_symlink_component(path):
        raise OSError("target path contains a symlink")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except Exception:
        try:
            temporary.unlink()
        except OSError:
            pass
        raise


def probe_crosswire(
    config_path: Path,
    *,
    probe_runner: Callable[..., object] | None = None,
    timeout: float = PROBE_TIMEOUT_SECONDS,
) -> Dict[str, str]:
    """Run the explicit Crosswire probe and classify its exact stdout token."""
    if isinstance(timeout, bool):
        return {"status": "failed", "reason": "invalid-probe-timeout"}
    try:
        bounded_timeout = min(float(timeout), PROBE_TIMEOUT_SECONDS)
    except (TypeError, ValueError):
        return {"status": "failed", "reason": "invalid-probe-timeout"}
    if not math.isfinite(bounded_timeout) or bounded_timeout <= 0:
        return {"status": "failed", "reason": "invalid-probe-timeout"}
    command = ["crosswire-turn-hook", "--probe", "--config", str(config_path)]
    runner = subprocess.run if probe_runner is None else probe_runner
    try:
        completed = runner(
            command, capture_output=True, text=True, timeout=bounded_timeout, check=False
        )
    except (FileNotFoundError, OSError):
        return {"status": "failed", "reason": "probe-launch-failed"}
    except (subprocess.TimeoutExpired, TimeoutError):
        return {"status": "failed", "reason": "probe-timeout"}
    except Exception:
        return {"status": "failed", "reason": "probe-launch-failed"}

    returncode = getattr(completed, "returncode", None)
    stdout = getattr(completed, "stdout", "")
    if returncode == 0 and stdout == f"{PROBE_SUCCESS_TOKEN}\n":
        return {"status": "ok", "token": PROBE_SUCCESS_TOKEN}
    if returncode == 0 and stdout == f"{PROBE_FAILURE_TOKEN}\n":
        return {"status": "failed", "reason": "probe-reported-failure"}
    return {"status": "failed", "reason": "probe-contract-mismatch"}


def run_registration(
    harness: str,
    adapter: RegistrationAdapter,
    *,
    enabled: bool,
    config_path: Path | None = None,
    home: Path | None = None,
    environ: Mapping[str, str] | None = None,
    probe_runner: Callable[..., object] | None = None,
    timeout: float = PROBE_TIMEOUT_SECONDS,
) -> Dict[str, object]:
    """Run one format adapter through the shared probe-first lifecycle."""
    enabled = _normalize_comms_profile(enabled)
    try:
        root = harness_root(harness, home=home, environ=environ)
        target = Path(adapter.target_path(root))
    except Exception:
        return {
            "harness": harness,
            "enabled": enabled,
            "status": "failed",
            "detail": "invalid-registration-path",
        }
    result: Dict[str, object] = {
        "harness": harness,
        "target_path": str(target),
        "enabled": enabled,
    }
    explicit_config: Path | None = None
    if enabled or config_path is not None:
        try:
            explicit_config = Path(
                config_path if config_path is not None else adapter.config_path(root)
            )
        except Exception:
            result.update(status="failed", detail="invalid-registration-path")
            return result
        result["config_path"] = str(explicit_config)
    if enabled:
        if explicit_config is None:
            result.update(status="failed", detail="invalid-registration-path")
            return result
        probe = probe_crosswire(explicit_config, probe_runner=probe_runner, timeout=timeout)
        result["probe"] = probe.get("token", probe.get("reason", "failed"))
        if probe["status"] != "ok":
            result.update(status="failed", detail=probe.get("reason", "probe-failed"))
            return result

    if _has_symlink_component(target):
        result.update(status="failed", detail="target-is-symlink")
        return result
    existed = target.is_file()
    try:
        existing = target.read_bytes() if target.is_file() else b""
    except OSError:
        result.update(status="failed", detail="target-read-failed")
        return result
    try:
        if enabled:
            updated = adapter.upsert(existing, explicit_config)
            removed = ""
        else:
            updated, removed = adapter.remove(existing)
    except Exception:
        result.update(status="failed", detail="adapter-failed")
        return result
    if not isinstance(updated, bytes):
        result.update(status="failed", detail="adapter-returned-invalid-bytes")
        return result
    if updated == existing:
        result.update(status="unchanged")
        if not enabled:
            result["removed_content"] = removed
        return result
    try:
        _safe_replace(target, updated)
    except OSError:
        result.update(status="failed", detail="target-write-failed")
        return result
    if enabled:
        result["status"] = "updated" if existed else "created"
    else:
        result["status"] = "removed"
    if not enabled:
        result["removed_content"] = removed
    return result


def ensure_code_review_graph(harnesses: Sequence[str] = ()) -> Dict[str, str]:
    """Install and configure code-review-graph (tirth8205/code-review-graph) if absent.

    The agents lean on its MCP knowledge graph, but asset deployment must never
    depend on it: every failure path returns a status instead of raising.

    `code-review-graph install` defaults to every platform it can detect, which
    scatters config for harnesses this repo does not port to (`.kiro/`,
    `.qoder/`, `.windsurfrules`, ...) into the working repository. Scope it to
    the harness selection instead, so the saved selection is the only place a
    user picks harnesses.
    """
    if shutil.which("code-review-graph"):
        return {"status": "already-installed"}

    installed = False
    for installer in (("pip", "install", "code-review-graph"), ("pipx", "install", "code-review-graph")):
        if not shutil.which(installer[0]):
            continue
        if subprocess.run(installer).returncode == 0:
            installed = True
            break
    if not installed:
        return {"status": "install-failed", "detail": "pip and pipx both unavailable or failed"}
    if not shutil.which("code-review-graph"):
        return {"status": "install-failed", "detail": "installed but binary not on PATH"}

    platforms = [
        CRG_PLATFORMS[name] for name in dict.fromkeys(harnesses) if name in CRG_PLATFORMS
    ]
    if not platforms:
        return {"status": "skipped", "detail": "no selected harness maps to a code-review-graph platform"}
    failed = [
        platform
        for platform in platforms
        if subprocess.run(["code-review-graph", "install", "-y", "--platform", platform]).returncode != 0
    ]
    if failed:
        return {
            "status": "configure-failed",
            "detail": f"'code-review-graph install' failed for: {', '.join(failed)}",
        }
    return {"status": "installed-and-configured"}


def context7_is_configured(*, home: Path | None = None) -> bool:
    """Whether the Context7 MCP server is registered for Claude Code.

    `ctx7 setup` has two modes and only one of them satisfies the agents.
    MCP mode registers a `context7` server in `~/.claude.json`; CLI + Skills
    mode writes a rule file instead and registers no server, so the
    `resolve-library-id` and `query-docs` tools the baseline instructions call
    would not exist. A CLI-mode install therefore does not count as configured.
    """
    home = Path(home).expanduser() if home else Path.home()
    try:
        return "context7" in (home / ".claude.json").read_text(encoding="utf-8")
    except OSError:
        return False


def ensure_context7(*, home: Path | None = None) -> Dict[str, str]:
    """Configure the Context7 MCP server (context7.com) if not already present.

    MCP mode is pinned because the agents call Context7's MCP tools by name;
    bare `ctx7 setup` picks a mode interactively and can land on CLI + Skills,
    which registers no server. `-y` keeps the deploy non-interactive — a
    bootstrap step must never stop to ask. As with the graph tool, every failure
    path returns a status instead of raising.
    """
    if context7_is_configured(home=home):
        return {"status": "already-configured"}

    if not shutil.which("npx"):
        return {"status": "install-failed", "detail": "npx not on PATH (Node.js required)"}
    if subprocess.run(["npx", "ctx7", "setup", "--claude", "--mcp", "-y"]).returncode != 0:
        return {"status": "configure-failed", "detail": "'npx ctx7 setup' returned nonzero"}
    return {"status": "installed-and-configured"}


def ensure_external_tools(harnesses: Sequence[str] = ()) -> Dict[str, Dict[str, str]]:
    """Bootstrap each companion tool; no outcome here may abort deployment."""
    results: Dict[str, Dict[str, str]] = {}
    for name, bootstrap in (
        ("code-review-graph", lambda: ensure_code_review_graph(harnesses)),
        ("context7", ensure_context7),
    ):
        try:
            results[name] = bootstrap()
        except Exception as exc:  # noqa: BLE001 — deployment must survive any tool failure
            results[name] = {"status": "install-failed", "detail": str(exc)}
    return results


def report_external_tools(results: Dict[str, Dict[str, str]]) -> None:
    for name, result in results.items():
        status = result.get("status", "")
        if status in ("already-installed", "already-configured"):
            print(f"[tools] {name}: already set up")
        elif status == "installed-and-configured":
            print(f"[tools] {name}: installed and configured")
        elif status == "skipped":
            print(f"[tools] {name}: skipped ({result.get('detail', '')})")
        else:
            detail = result.get("detail", "unknown error")
            print(
                f"[tools] WARNING: {name} could not be set up ({detail}). "
                f"Continuing without it — agent deployment is unaffected.",
                file=sys.stderr,
            )


def deploy(
    harnesses: List[str],
    *,
    home: Path | None = None,
    environ: Mapping[str, str] | None = None,
    verbose: bool = True,
    comms_profile: bool = False,
    registration_adapters: Mapping[str, RegistrationAdapter] | None = None,
) -> Dict[str, Dict[str, object]]:
    comms_profile = _normalize_comms_profile(comms_profile)
    results: Dict[str, Dict[str, object]] = {}
    adapters = REGISTRATION_ADAPTERS if registration_adapters is None else registration_adapters
    for name in harnesses:
        results[name] = deploy_harness(name, home=home, environ=environ)
        baseline = deploy_baseline(
            name, home=home, environ=environ, comms_enabled=comms_profile
        )
        if baseline["status"] != "not-applicable":
            results[name]["baseline"] = baseline
        adapter = adapters.get(name)
        if adapter is not None:
            results[name]["registration"] = run_registration(
                name,
                adapter,
                enabled=comms_profile,
                home=home,
                environ=environ,
            )
    if verbose:
        print(json.dumps(results, indent=2))
    return results


def _read_config_data(path: Path) -> Mapping[str, object]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def _normalize_config_data(data: Mapping[str, object]) -> DeployConfig:
    selected = data.get("harnesses", [])
    if not isinstance(selected, list):
        selected = []
    harnesses = [name for name in selected if isinstance(name, str) and name in HARNESSES]
    return DeployConfig(harnesses, _normalize_comms_profile(data.get(COMMS_PROFILE_KEY, False)))


def load_config(path: Path = CONFIG_PATH) -> List[str]:
    return _normalize_config_data(_read_config_data(path)).harnesses


def load_comms_profile(path: Path = CONFIG_PATH) -> bool:
    return _normalize_config_data(_read_config_data(path)).comms_profile


def load_config_state(path: Path = CONFIG_PATH) -> DeployConfig:
    return _normalize_config_data(_read_config_data(path))


def save_config(
    harnesses: List[str],
    path: Path = CONFIG_PATH,
    *,
    comms_profile: bool = False,
) -> None:
    comms_profile = _normalize_comms_profile(comms_profile)
    path.write_text(
        json.dumps({"harnesses": harnesses, COMMS_PROFILE_KEY: comms_profile}, indent=2) + "\n",
        encoding="utf-8",
    )


def parse_harness_arg(raw: str) -> List[str]:
    names = [name.strip() for name in raw.split(",") if name.strip()]
    unknown = [name for name in names if name not in HARNESSES]
    if unknown:
        raise ValueError(f"unknown harness(es): {', '.join(unknown)} (choose from {', '.join(HARNESSES)})")
    return names


def prompt_for_harnesses() -> List[str]:
    print("Which harnesses do you use? (comma-separated numbers, or 'all')")
    for index, name in enumerate(HARNESSES, start=1):
        print(f"  {index}. {name}")
    while True:
        raw = input("> ").strip().lower()
        if raw == "all":
            return list(HARNESSES)
        try:
            picks = [int(part) for part in raw.replace(",", " ").split()]
            if picks and all(1 <= p <= len(HARNESSES) for p in picks):
                return [HARNESSES[p - 1] for p in dict.fromkeys(picks)]
        except ValueError:
            pass
        print("Enter numbers like '1,3', or 'all'.")


def list_harnesses(selected: List[str]) -> None:
    for name in HARNESSES:
        mark = "*" if name in selected else " "
        print(f"{mark} {name}")
        for source_root, dest_root in harness_mappings(name):
            print(f"    {source_root.relative_to(REPO_ROOT)} -> {dest_root}")
        baseline = baseline_destination(name)
        if baseline is not None:
            print(f"    {BASELINE_TEMPLATE.relative_to(REPO_ROOT)} -> {baseline}")
    if selected:
        print(f"\nSaved selection: {', '.join(selected)}")
    else:
        print("\nNo saved selection (.deploy-config.json missing).")


def watch(harnesses: List[str], *, comms_profile: bool = False) -> None:
    comms_profile = _normalize_comms_profile(comms_profile)
    print(f"Starting ports deploy watcher for {{{','.join(harnesses)}}} ...")
    deploy(harnesses, comms_profile=comms_profile)

    def _on_change(changes: List[str]) -> None:
        sample = ", ".join(Path(c).name for c in changes[:5])
        more = "" if len(changes) <= 5 else f" (+{len(changes) - 5} more)"
        print(f"Detected change in ports: {sample}{more}")
        deploy(harnesses, comms_profile=comms_profile)

    poll_watch([PORTS_DIR / name for name in harnesses], _on_change)


def main() -> int:
    parser = argparse.ArgumentParser(description="Deploy ports/ assets to real harness config directories.")
    parser.add_argument("--harness", help="Comma-separated harnesses to deploy (e.g. claude,cursor).")
    parser.add_argument("--all", action="store_true", help="Deploy every supported harness.")
    parser.add_argument("--watch", action="store_true", help="Watch ports/ and auto-deploy on changes.")
    parser.add_argument("--list", action="store_true", help="Show harnesses and resolved destinations.")
    parser.add_argument("--no-save", action="store_true", help="Do not persist the harness selection.")
    parser.add_argument(
        "--skip-tools",
        action="store_true",
        help="Do not install/configure external tools (code-review-graph, Context7).",
    )
    args = parser.parse_args()
    saved_state = load_config_state(CONFIG_PATH)

    if args.list:
        list_harnesses(saved_state.harnesses)
        print(f"Comms profile: {'enabled' if saved_state.comms_profile else 'disabled'}")
        return 0

    if args.all:
        selected = list(HARNESSES)
    elif args.harness:
        try:
            selected = parse_harness_arg(args.harness)
        except ValueError as exc:
            parser.error(str(exc))
    else:
        selected = saved_state.harnesses
        if not selected:
            if sys.stdin.isatty():
                selected = prompt_for_harnesses()
            else:
                parser.error(
                    "no saved harness selection; pass --harness claude,codex,opencode,cursor or --all"
                )

    comms_profile = saved_state.comms_profile
    if not args.no_save:
        save_config(selected, CONFIG_PATH, comms_profile=comms_profile)

    if not args.skip_tools:
        report_external_tools(ensure_external_tools(selected))

    if args.watch:
        watch(selected, comms_profile=comms_profile)
        return 0

    deploy(selected, comms_profile=comms_profile)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
