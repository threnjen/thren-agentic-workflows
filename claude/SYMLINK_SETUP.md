# Claude Managed-Copy Setup

This legacy filename now documents the supported Claude deployment model. Runtime symlink setup is retired.

## Deploy

1. Edit sources under `.github/` and restart any long-running propagation watcher.
2. Run `python3 scripts/propagate_master_assets.py --once` and require the JSON result to show `converged: true` with zero `verification_changes`.
3. Use `resolve_destinations_after_convergence` with that convergence result. Confirm the active `CLAUDE_CONFIG_DIR` (or `~/.claude`) on the destination records, then review `runtime_deployment.destination_inventory(records)` for expected agents, commands, skills, learnings, and destinations.
4. After review, invoke `deploy_managed_copies_after_convergence`. Inspect its returned per-harness result for collision and reconciliation outcomes. It stages and reconciles regular managed copies using ownership evidence; do not substitute manual copy recipes.

## Verify

- Agents, commands, skills, and learnings are regular files/directories, not runtime links.
- Content matches the repository-generated Claude roster and current source generation.
- Foreign collisions remain preserved and reported.
- A second convergence and deployment run is a fixed point.
- A fresh Claude session discovers the expected agents and commands.

If deployment is partial, keep the failed harness status visible, restart stale watchers, resolve the reported collision or platform error, and rerun the canonical workflow. Roll back owned content through deployment metadata and version control; do not restore the retired link model.
