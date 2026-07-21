#!/usr/bin/env python3
"""Deploy ports/ outputs to real harness config directories.

Companion to `propagate_master_assets.py` (source_of_truth/ -> ports/); this
script covers the second hop, ports/ -> live harness config dirs, so installed
agents never go stale relative to the repo. Currently deploys the claude
harness: ports/claude/{agents,commands,skills,learnings} -> ~/.claude/.

Ownership rules (shared with propagation via asset_paths):
- A destination file is overwritten only if it does not exist or carries a
  generated-output marker at the expected position (it is ours).
- An existing unmarked destination file is never overwritten or deleted; it is
  reported as a conflict and skipped.
- Port files whose destination exists unmarked (e.g. binary skill assets we
  cannot prove we own) are skipped with a conflict warning unless byte-identical.
- Marked destination files with no corresponding port source are pruned.

Usage:
  python scripts/deploy_assets.py           # one-shot deploy
  python scripts/deploy_assets.py --watch   # deploy, then redeploy on changes
  python scripts/deploy_assets.py --dry-run # report actions without writing
"""

from __future__ import annotations

import argparse
import filecmp
import json
import shutil
import sys
from pathlib import Path
from typing import Dict, List

from asset_paths import PORTS_DIR, file_has_generated_marker, poll_watch

CLAUDE_HOME = Path.home() / ".claude"

# (port source dir, destination dir) pairs per harness.
DEPLOY_MAP = [
    (PORTS_DIR / "claude" / "agents", CLAUDE_HOME / "agents"),
    (PORTS_DIR / "claude" / "commands", CLAUDE_HOME / "commands"),
    (PORTS_DIR / "claude" / "skills", CLAUDE_HOME / "skills"),
    (PORTS_DIR / "claude" / "learnings", CLAUDE_HOME / "learnings"),
]


def deploy(dry_run: bool = False) -> Dict[str, List[str]]:
    result: Dict[str, List[str]] = {"deployed": [], "pruned": [], "conflicts": []}

    for src_root, dest_root in DEPLOY_MAP:
        if not src_root.exists():
            continue

        src_files = [p for p in src_root.rglob("*") if p.is_file()]
        src_rels = {p.relative_to(src_root) for p in src_files}

        for src in src_files:
            rel = src.relative_to(src_root)
            dest = dest_root / rel
            if dest.exists():
                if filecmp.cmp(src, dest, shallow=False):
                    continue
                if not file_has_generated_marker(dest):
                    result["conflicts"].append(str(dest))
                    continue
            if not dry_run:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dest)
            result["deployed"].append(str(dest))

        # Prune destination files we own whose port source is gone.
        if dest_root.exists():
            for dest in dest_root.rglob("*"):
                if not dest.is_file():
                    continue
                rel = dest.relative_to(dest_root)
                if rel in src_rels:
                    continue
                if file_has_generated_marker(dest):
                    if not dry_run:
                        dest.unlink()
                    result["pruned"].append(str(dest))

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--watch", action="store_true", help="redeploy when ports/ changes")
    parser.add_argument("--dry-run", action="store_true", help="report actions without writing")
    args = parser.parse_args()

    result = deploy(dry_run=args.dry_run)
    print(json.dumps({k: len(v) for k, v in result.items()} | {"dry_run": args.dry_run}, indent=2))
    for conflict in result["conflicts"]:
        print(f"conflict (unmarked destination left untouched): {conflict}", file=sys.stderr)

    if args.watch:
        def on_change(_changes: List[str]) -> None:
            summary = deploy()
            print(json.dumps({k: len(v) for k, v in summary.items()}, indent=2))

        poll_watch([src for src, _ in DEPLOY_MAP], on_change)

    return 0


if __name__ == "__main__":
    main()
