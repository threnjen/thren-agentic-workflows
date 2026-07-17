# Harness Managed-Copy Setup

Claude, Codex, and OpenCode user-global assets are deployed as regular managed copies. The former runtime-link setup model is retired.

## Canonical Sequence

1. Edit `.github/` sources and restart any long-running propagation watcher.
2. Run `python3 scripts/propagate_master_assets.py --once`. Continue only when repository outputs converge and the immediate verification pass reports zero changes.
3. Pass that convergence result to `resolve_destinations_after_convergence`.
4. Review the active home and relocation variables on the destination records, then review `runtime_deployment.destination_inventory(records)` for the harness and asset-class roster plus every destination.
5. After explicit review, pass the same result and records to `deploy_managed_copies_after_convergence`.
6. Inspect the returned per-harness result for collision, copy, replacement, pruning, failure, and reconciliation-skipped outcomes.
7. Repeat the sequence and require a fixed point, then start fresh harness sessions and verify runtime discovery.

Do not replace the deployment APIs with manual copy commands. They own staging, atomic replacement, repository-link migration, metadata, collision preservation, and stale managed-copy pruning.

## Harness Coverage

| Harness | Managed asset classes | Default destination owner |
|---|---|---|
| Claude | agents, commands, skills, learnings | `CLAUDE_CONFIG_DIR` or `~/.claude` |
| Codex | agents, skills | `CODEX_HOME` for agents; documented active-user skill root for skills |
| OpenCode | agents, skills | `OPENCODE_CONFIG_DIR` or documented defaults |

Profiles, project-local assets, and generated hook/settings outputs are not manual escape hatches. If they are not in the current destination roster, report them as unsupported by this deployment run rather than installing them ad hoc.

## GitHub Copilot (VS Code)

Copilot reads `.github/agents/`, `.github/skills/`, and `.github/instructions/` from every folder open in the VS Code workspace. To use this repository's assets in another project, open both repositories in one multi-root workspace.

Create a `.code-workspace` file containing both folders:

```json
{
  "folders": [
    { "path": "/absolute/path/to/your-project" },
    { "path": "/absolute/path/to/github-agents-source-of-truth" }
  ]
}
```

Alternatively, use **File → Add Folder to Workspace…** and select this repository. This workspace-based Copilot setup does not deploy user-global generated runtime assets and does not require a link.

The `.github/instructions/` files use `applyTo` globs automatically. To use only a language-specific `AGENTS.md` template, copy `nodejs/AGENTS.md` or `python/AGENTS.md` into the target project.

## Context7 MCP

Skills such as `context7-mcp` require the Context7 MCP server. Retain the existing client-specific configuration for the active harness; setup and removal are documented at <https://context7.com/docs/resources/all-clients>. Context7 configuration is independent of managed-copy asset deployment.

## Platform Evidence

Run macOS, Linux, native Windows, and WSL in their own active environments. Native Windows and WSL are separate runs; one cannot deploy into or prove the other. Report an unavailable environment as `NOT RUN`. Any failure or `NOT RUN` blocks full cross-platform GO.

For each harness report convergence, preflight review, collision results, regular-copy freshness, expected roster coverage, reconciliation, and fresh-session runtime discovery. A failed harness remains partial and skips destructive reconciliation; successful harnesses remain independently valid.

## Troubleshooting And Rollback

Restart stale watchers, resolve the reported collision or platform category, and rerun the canonical workflow. Foreign files, package/plugin content, Git-hook links, and debug pointers remain untouched. Roll back owned content using deployment metadata and version control, never by restoring retired runtime links.
