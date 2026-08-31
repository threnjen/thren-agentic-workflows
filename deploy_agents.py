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
import os
import re
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


REGISTRATION_ADAPTERS: Dict[str, RegistrationAdapter] = {}


def _safe_replace(path: Path, data: bytes) -> None:
    """Replace a registration file without truncating an existing target."""
    if path.is_symlink():
        raise OSError("target is a symlink")
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
    command = ["crosswire-turn-hook", "--probe", "--config", str(config_path)]
    runner = subprocess.run if probe_runner is None else probe_runner
    try:
        completed = runner(command, capture_output=True, text=True, timeout=timeout, check=False)
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
    try:
        root = harness_root(harness, home=home, environ=environ)
        target = adapter.target_path(root)
        explicit_config = config_path or adapter.config_path(root)
    except (OSError, ValueError, TypeError):
        return {
            "harness": harness,
            "enabled": enabled,
            "status": "failed",
            "detail": "invalid-registration-path",
        }
    result: Dict[str, object] = {
        "harness": harness,
        "target_path": str(target),
        "config_path": str(explicit_config),
        "enabled": enabled,
    }
    if enabled:
        probe = probe_crosswire(explicit_config, probe_runner=probe_runner, timeout=timeout)
        result["probe"] = probe.get("token", probe.get("reason", "failed"))
        if probe["status"] != "ok":
            result.update(status="failed", detail=probe.get("reason", "probe-failed"))
            return result

    if target.is_symlink():
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


def load_config(path: Path = CONFIG_PATH) -> List[str]:
    data = _read_config_data(path)
    selected = data.get("harnesses", [])
    if not isinstance(selected, list):
        selected = []
    return [name for name in selected if name in HARNESSES]


def load_comms_profile(path: Path = CONFIG_PATH) -> bool:
    value = _read_config_data(path).get(COMMS_PROFILE_KEY, False)
    return value if isinstance(value, bool) else False


def load_config_state(path: Path = CONFIG_PATH) -> DeployConfig:
    return DeployConfig(load_config(path), load_comms_profile(path))


def save_config(
    harnesses: List[str],
    path: Path = CONFIG_PATH,
    *,
    comms_profile: bool = False,
) -> None:
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


def watch(harnesses: List[str]) -> None:
    print(f"Starting ports deploy watcher for {{{','.join(harnesses)}}} ...")
    deploy(harnesses)

    def _on_change(changes: List[str]) -> None:
        sample = ", ".join(Path(c).name for c in changes[:5])
        more = "" if len(changes) <= 5 else f" (+{len(changes) - 5} more)"
        print(f"Detected change in ports: {sample}{more}")
        deploy(harnesses)

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
        watch(selected)
        return 0

    deploy(selected, comms_profile=comms_profile)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
