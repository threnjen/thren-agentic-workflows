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
from pathlib import Path
from typing import Dict, List, Mapping, Tuple

from scripts.asset_paths import PORTS_DIR, REPO_ROOT, file_has_generated_marker, poll_watch

CONFIG_PATH = REPO_ROOT / ".deploy-config.json"

HARNESSES = ("claude", "codex", "opencode", "cursor", "github")

# Baseline user-global instructions (CLAUDE.md / AGENTS.md / Cursor rule).
# Rendered at deploy time so the discovery paths reflect this machine's real
# home directory, then spliced into the destination file between sentinel
# comments — content outside the sentinels is never touched.
BASELINE_TEMPLATE = REPO_ROOT / "source_of_truth" / "baseline" / "baseline-instructions.md"
BASELINE_SECTIONS = ("context7", "code-review-graph", "agent-discovery")
# Cursor has no user-global AGENTS.md; its native global channel is a rule file.
CURSOR_BASELINE_FRONTMATTER = "---\nalwaysApply: true\n---\n\n"

# The github "harness" deploys into this repository, not the home directory: it
# mirrors ports/github verbatim into .github/ so GitHub-side tooling reads the
# same source of truth. Its files carry no generated marker (they are exact
# copies), so the whole mirrored tree is treated as managed.
GITHUB_MIRRORED_SUBDIRS = ("agents", "hooks", "instructions", "learnings", "skills")


def harness_mappings(
    harness: str,
    *,
    home: Path | None = None,
    environ: Mapping[str, str] | None = None,
) -> List[Tuple[Path, Path]]:
    """(port source dir, real destination dir) pairs for one harness."""
    home = Path(home).expanduser() if home else Path.home()
    environ = os.environ if environ is None else environ

    def root(env_var: str, default: str | Path) -> Path:
        raw = environ.get(env_var, "")
        return Path(raw).expanduser() if raw else home / default

    port = PORTS_DIR / harness
    if harness == "claude":
        base = root("CLAUDE_CONFIG_DIR", ".claude")
        # learnings/ has no runtime destination under the config dir: every
        # consumer reads `.github/learnings/` in the working repo, so a copy
        # here would be read by nothing. Cursor is the exception - its
        # learnings ship as agent-requested rules under rules/.
        return [(port / sub, base / sub) for sub in ("agents", "commands", "skills")]
    if harness == "codex":
        base = root("CODEX_HOME", ".codex")
        # codex profiles/ has no documented runtime destination and is not
        # deployed; neither does learnings/ (see the claude branch above).
        return [
            (port / "agents", base / "agents"),
            (port / "skills", home / ".agents" / "skills"),
        ]
    if harness == "opencode":
        base = root("OPENCODE_CONFIG_DIR", Path(".config") / "opencode")
        return [(port / sub, base / sub) for sub in ("agents", "skills")]
    if harness == "cursor":
        base = home / ".cursor"
        return [(port / sub, base / sub) for sub in ("commands", "rules")]
    if harness == "github":
        base = REPO_ROOT / ".github"
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

    def root(env_var: str, default: str | Path) -> Path:
        raw = environ.get(env_var, "")
        return Path(raw).expanduser() if raw else home / default

    if harness == "claude":
        return root("CLAUDE_CONFIG_DIR", ".claude") / "CLAUDE.md"
    if harness == "codex":
        return root("CODEX_HOME", ".codex") / "AGENTS.md"
    if harness == "opencode":
        return root("OPENCODE_CONFIG_DIR", Path(".config") / "opencode") / "AGENTS.md"
    if harness == "cursor":
        return home / ".cursor" / "rules" / "baseline-instructions.mdc"
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


def _parse_baseline_sections(template: str) -> Dict[str, str]:
    """Extract each sentinel-delimited section body from the template."""
    sections: Dict[str, str] = {}
    for name in BASELINE_SECTIONS:
        sentinel = f"<!-- {name} -->"
        match = re.search(re.escape(sentinel) + r"\n(.*?)" + re.escape(sentinel), template, re.DOTALL)
        if match:
            sections[name] = match.group(1).strip("\n")
    return sections


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
    sections = _parse_baseline_sections(template)
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


def ensure_code_review_graph() -> Dict[str, str]:
    """Install and configure code-review-graph (tirth8205/code-review-graph) if absent.

    The agents lean on its MCP knowledge graph, but asset deployment must never
    depend on it: every failure path returns a status instead of raising.
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

    if subprocess.run(["code-review-graph", "install"]).returncode != 0:
        return {"status": "configure-failed", "detail": "'code-review-graph install' returned nonzero"}
    return {"status": "installed-and-configured"}


def ensure_context7(*, home: Path | None = None) -> Dict[str, str]:
    """Configure the Context7 MCP server (context7.com) if not already present.

    Presence is probed in Claude Code's config (`~/.claude.json`), the one
    registry `npx ctx7 setup` always writes when Claude Code is detected. As
    with the graph tool, every failure path returns a status instead of raising.
    """
    home = Path(home).expanduser() if home else Path.home()
    try:
        if "context7" in (home / ".claude.json").read_text(encoding="utf-8"):
            return {"status": "already-configured"}
    except OSError:
        pass

    if not shutil.which("npx"):
        return {"status": "install-failed", "detail": "npx not on PATH (Node.js required)"}
    if subprocess.run(["npx", "ctx7", "setup"]).returncode != 0:
        return {"status": "configure-failed", "detail": "'npx ctx7 setup' returned nonzero"}
    return {"status": "installed-and-configured"}


def ensure_external_tools() -> Dict[str, Dict[str, str]]:
    """Bootstrap each companion tool; no outcome here may abort deployment."""
    results: Dict[str, Dict[str, str]] = {}
    for name, bootstrap in (
        ("code-review-graph", ensure_code_review_graph),
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
) -> Dict[str, Dict[str, object]]:
    results: Dict[str, Dict[str, object]] = {}
    for name in harnesses:
        results[name] = deploy_harness(name, home=home, environ=environ)
        baseline = deploy_baseline(name, home=home, environ=environ)
        if baseline["status"] != "not-applicable":
            results[name]["baseline"] = baseline
    if verbose:
        print(json.dumps(results, indent=2))
    return results


def load_config(path: Path = CONFIG_PATH) -> List[str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return []
    selected = data.get("harnesses", []) if isinstance(data, dict) else []
    return [name for name in selected if name in HARNESSES]


def save_config(harnesses: List[str], path: Path = CONFIG_PATH) -> None:
    path.write_text(json.dumps({"harnesses": harnesses}, indent=2) + "\n", encoding="utf-8")


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

    if args.list:
        list_harnesses(load_config(CONFIG_PATH))
        return 0

    if args.all:
        selected = list(HARNESSES)
    elif args.harness:
        try:
            selected = parse_harness_arg(args.harness)
        except ValueError as exc:
            parser.error(str(exc))
    else:
        selected = load_config(CONFIG_PATH)
        if not selected:
            if sys.stdin.isatty():
                selected = prompt_for_harnesses()
            else:
                parser.error(
                    "no saved harness selection; pass --harness claude,codex,opencode,cursor or --all"
                )

    if not args.no_save:
        save_config(selected, CONFIG_PATH)

    if not args.skip_tools:
        report_external_tools(ensure_external_tools())

    if args.watch:
        watch(selected)
        return 0

    deploy(selected)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
