# Harness Managed-Copy Setup

Claude, Codex, and OpenCode user-global assets are deployed as regular managed copies. The former runtime-link setup model is retired.

## Canonical Sequence

1. Edit `.github/` sources and restart any long-running propagation watcher.
2. Run `python3 scripts/propagate_master_assets.py --once`. Continue only when repository outputs converge and the immediate verification pass reports zero changes.
3. Pass that convergence result to `resolve_destinations_after_convergence`.
4. Review `runtime_deployment.destination_inventory(records)`: active home, relocation variables, harness and asset-class roster, collision outcomes, and ownership evidence.
5. After explicit review, pass the same result and records to `deploy_managed_copies_after_convergence`.
6. Repeat the sequence and require a fixed point, then start fresh harness sessions and verify runtime discovery.

Do not replace the deployment APIs with manual copy commands. They own staging, atomic replacement, repository-link migration, metadata, collision preservation, and stale managed-copy pruning.

## Harness Coverage

| Harness | Managed asset classes | Default destination owner |
|---|---|---|
| Claude | agents, commands, skills, learnings | `CLAUDE_CONFIG_DIR` or `~/.claude` |
| Codex | agents, skills | `CODEX_HOME` for agents; documented active-user skill root for skills |
| OpenCode | agents, skills | `OPENCODE_CONFIG_DIR` or documented defaults |

Profiles, project-local assets, and generated hook/settings outputs are not manual escape hatches. If they are not in the current destination roster, report them as unsupported by this deployment run rather than installing them ad hoc.

## Platform Evidence

Run macOS, Linux, native Windows, and WSL in their own active environments. Native Windows and WSL are separate runs; one cannot deploy into or prove the other. Report an unavailable environment as `NOT RUN`. Any failure or `NOT RUN` blocks full cross-platform GO.

For each harness report convergence, preflight review, collision results, regular-copy freshness, expected roster coverage, reconciliation, and fresh-session runtime discovery. A failed harness remains partial and skips destructive reconciliation; successful harnesses remain independently valid.

## Troubleshooting And Rollback

Restart stale watchers, resolve the reported collision or platform category, and rerun the canonical workflow. Foreign files, package/plugin content, Git-hook links, and debug pointers remain untouched. Roll back owned content using deployment metadata and version control, never by restoring retired runtime links.
