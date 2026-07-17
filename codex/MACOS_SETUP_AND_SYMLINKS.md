# Codex Managed-Copy Setup

This legacy filename is retained for incoming references. Runtime symlink and junction installation is retired.

## Supported Workflow

1. Regenerate repository outputs with `python3 scripts/propagate_master_assets.py --once` and require fixed-point convergence.
2. Call `resolve_destinations_after_convergence`. Confirm the active home and `CODEX_HOME` on the destination records, then review `runtime_deployment.destination_inventory(records)` for the agent roster, skill roster, and destinations.
3. After review, call `deploy_managed_copies_after_convergence` to stage and reconcile regular managed copies, then inspect its returned per-harness result for collision and reconciliation outcomes.
4. Repeat the workflow and require no changes.

The managed roster currently deploys custom agents under `CODEX_HOME` (default `~/.codex/agents`) and skills to the documented active-user skill root (default `$HOME/.agents/skills`). Profiles and global AGENTS guidance are not silently mapped into this roster; retain repository outputs until their runtime destinations are explicitly supported.

## Verification

- Every managed agent and skill is a regular file or directory with current content.
- Expected roster coverage, collision outcomes, and stale-copy reconciliation are reported.
- Foreign files and package/plugin-managed assets are unchanged.
- A fresh Codex session discovers the deployed agents and skills.

Native Windows and WSL require separate runs. An unavailable environment is `NOT RUN`, not evidence from the other environment. Partial deployment remains partial and blocks full cross-platform GO.

The deployment engine may discuss hostile symlinks and junction containment because migration must reject unsafe parents and classify legacy repository-owned links without traversing them. Those security rules are not operational installation instructions.
