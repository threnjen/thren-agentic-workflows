# Harness Managed-Copy Setup

Claude, Codex, and OpenCode user-global assets are deployed as regular managed copies.

## Canonical Sequence

Deployment is driven entirely through the `--runtime-deploy` flag on `scripts/propagate_master_assets.py` — a two-invocation review-then-deploy flow, not a sequence of manual Python calls.

1. Edit `.github/` sources and restart any long-running propagation watcher (a stale `--watch` process runs pre-edit propagation code — see Troubleshooting).
2. Run `python3 scripts/propagate_master_assets.py --runtime-deploy --active-home <path>` with no `--reviewed-inventory`. This converges repository outputs (aborting if they cannot reach a fixed point), computes the destination inventory, and prints it as JSON with an `inventory_digest`. No runtime mutation happens on this call; it exits `2` (`status: "review_required"`).

   > **What `<path>` should be**: your actual current-user home directory on the machine you're deploying to — the same value `$HOME` (`echo $HOME`) resolves to on macOS/Linux/WSL, or `%USERPROFILE%` on native Windows — passed as an **absolute** path (a relative path is rejected). If omitted, it defaults to `Path.home()`, so most single-user runs can skip the flag entirely and let it default. Pass an explicit `--active-home` only when deploying for a different user or into a scratch/QA home (e.g. a throwaway directory for dry-run testing before touching your live home) — never point it at a path inside this repository, and never at a symlink, since destinations are validated to resolve underneath it. `CLAUDE_CONFIG_DIR`, `CODEX_HOME`, and `OPENCODE_CONFIG_DIR`, if set, override individual harness roots but are still validated against this same home.
3. Review the printed `inventory` — the harness/asset-class roster and every destination path — and note the `inventory_digest`.
4. After explicit review, and after confirming the watcher was restarted, rerun the same command with `--reviewed-inventory <digest-from-step-2>` and `--watcher-restarted`. This re-checks convergence and re-verifies the digest before any write (aborting on drift), then deploys managed copies, reconciles only the harnesses that deployed successfully, and verifies regular-copy freshness.
5. Inspect the printed `harnesses` map (status, copied, replaced, removed, unchanged, collisions, failed, reconciliation_skipped per harness) and `verification` map (regular-copy freshness, remaining repository links) for the outcome. Exit `0` means `status: "go"`; exit `1` means `failed` or `partial`.
6. Repeat step 2 and require it to report a fixed point (zero further changes) before trusting step 4's result, then start fresh harness sessions and verify runtime discovery.

Do not replace `--runtime-deploy` with manual copy commands or by calling `propagate_master_assets.py`'s internal functions directly. The flag owns staging, atomic replacement, repository-link migration, metadata, collision preservation, and stale managed-copy pruning.

## Harness Coverage

| Harness | Managed asset classes | Default destination owner |
|---|---|---|
| Claude | agents, commands, skills, learnings | `CLAUDE_CONFIG_DIR` or `~/.claude` |
| Codex | agents, skills | `CODEX_HOME` for agents; documented active-user skill root for skills |
| OpenCode | agents, skills | `OPENCODE_CONFIG_DIR` or documented defaults |

Profiles, project-local assets, and generated settings outputs are not manual escape hatches. If they are not in the current destination roster, report them as unsupported by this deployment run rather than installing them ad hoc.

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
