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
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Mapping, Tuple

from scripts.asset_paths import PORTS_DIR, REPO_ROOT, file_has_generated_marker, poll_watch

CONFIG_PATH = REPO_ROOT / ".deploy-config.json"

HARNESSES = ("claude", "codex", "opencode", "cursor", "github")

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
        return [(port / sub, base / sub) for sub in ("agents", "commands", "skills", "learnings")]
    if harness == "codex":
        base = root("CODEX_HOME", ".codex")
        # codex profiles/ has no documented runtime destination and is not deployed.
        return [
            (port / "agents", base / "agents"),
            (port / "skills", home / ".agents" / "skills"),
            (port / "learnings", base / "learnings"),
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
    results = {name: deploy_harness(name, home=home, environ=environ) for name in harnesses}
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
