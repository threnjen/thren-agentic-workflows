#!/usr/bin/env python3
"""Deploy generated ports/ assets to real harness config directories.

Copies `ports/<harness>/` outputs to the user-level directories each harness
reads (`~/.claude`, `~/.codex`, `~/.config/opencode`, `~/.cursor`). Safe by
construction: a destination file is only ever overwritten or pruned when it
positively carries a generated marker (or lives inside a generated skill
directory) — hand-maintained files are never touched.

Usage:
  deploy_assets.py                       # use saved selection; prompt if none (tty)
  deploy_assets.py --harness claude,cursor
  deploy_assets.py --all
  deploy_assets.py --watch               # maintainer: auto-deploy on ports/ change
  deploy_assets.py --list                # show harnesses and resolved destinations

The selection is saved to `.deploy-config.json` (gitignored) so re-runs are just
`python3 scripts/deploy_assets.py`.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Mapping, Tuple

from asset_paths import PORTS_DIR, REPO_ROOT, file_has_generated_marker, poll_watch

CONFIG_PATH = REPO_ROOT / ".deploy-config.json"

HARNESSES = ("claude", "codex", "opencode", "cursor")
# ports/github is deliberately absent: it deploys into this repository's .github/
# and is handled by propagate_master_assets.py.


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
        return [(port / "agents", base / "agents"), (port / "skills", home / ".agents" / "skills")]
    if harness == "opencode":
        base = root("OPENCODE_CONFIG_DIR", Path(".config") / "opencode")
        return [(port / sub, base / sub) for sub in ("agents", "skills")]
    if harness == "cursor":
        base = home / ".cursor"
        return [(port / sub, base / sub) for sub in ("commands", "rules")]
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
) -> Dict[str, int]:
    """Copy one harness's ports/ outputs to its real directories and prune stale copies."""
    copied = 0
    pruned = 0
    skipped = 0

    for source_root, dest_root in harness_mappings(harness, home=home, environ=environ):
        expected: set[Path] = set()

        if source_root.is_dir():
            for source_file in sorted(source_root.rglob("*")):
                if not source_file.is_file() or source_file.is_symlink():
                    continue
                dest_file = dest_root / source_file.relative_to(source_root)
                expected.add(dest_file)
                data = source_file.read_bytes()

                if dest_file.is_symlink():
                    skipped += 1
                    continue
                if dest_file.is_file():
                    try:
                        if dest_file.read_bytes() == data:
                            continue
                    except OSError:
                        skipped += 1
                        continue
                    if not _is_managed(dest_file, dest_root):
                        skipped += 1
                        continue
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                dest_file.write_bytes(data)
                copied += 1

        if dest_root.is_dir() and not dest_root.is_symlink():
            for path in sorted(dest_root.rglob("*"), reverse=True):
                if path in expected or path.is_symlink():
                    continue
                if path.is_file() and _is_managed(path, dest_root):
                    path.unlink()
                    pruned += 1
                elif path.is_dir() and not any(path.iterdir()):
                    path.rmdir()

    return {"copied": copied, "pruned": pruned, "skipped_unmanaged": skipped}


def deploy(
    harnesses: List[str],
    *,
    home: Path | None = None,
    environ: Mapping[str, str] | None = None,
    verbose: bool = True,
) -> Dict[str, Dict[str, int]]:
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
    args = parser.parse_args()

    if args.list:
        list_harnesses(load_config())
        return 0

    if args.all:
        selected = list(HARNESSES)
    elif args.harness:
        try:
            selected = parse_harness_arg(args.harness)
        except ValueError as exc:
            parser.error(str(exc))
    else:
        selected = load_config()
        if not selected:
            if sys.stdin.isatty():
                selected = prompt_for_harnesses()
            else:
                parser.error(
                    "no saved harness selection; pass --harness claude,codex,opencode,cursor or --all"
                )

    if not args.no_save:
        save_config(selected)

    if args.watch:
        watch(selected)
        return 0

    deploy(selected)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
