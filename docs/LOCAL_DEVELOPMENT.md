# Local Development

## Purpose

This repository is maintained by editing source-of-truth Markdown and agent files, then regenerating the derived platform outputs. There is no root application to build or serve.

## Prerequisites

- `git`
- `python3`
- VS Code if you want the built-in workspace tasks
- Optional harness tooling depending on what you need to validate:
  - GitHub Copilot in VS Code
  - Claude Code
  - OpenCode
  - Codex
- Optional `uvx` if you want the configured code-review-graph MCP server to resolve from `.mcp.json` or `.codex/config.toml`

## Clone And Open The Repo

```bash
git clone https://github.com/threnjen/github-agents-source-of-truth.git
cd github-agents-source-of-truth
```

If you use VS Code, open the repository root. The workspace defines two useful tasks in `.vscode/tasks.json`.

## Standard Editing Loop

1. Edit source-of-truth files under `.github/`, `nodejs/`, `python/`, `docs/`, or other repo-owned documentation areas.
2. Regenerate downstream agent outputs when you change `.github/agents/`, `.github/skills/`, or `.github/instructions/`.
3. Review the resulting diff before committing.

## Regenerate Derived Agent Outputs

### One-shot run

```bash
python3 scripts/propagate_master_assets.py --once
```

Use this after a batch of source edits when you want a deterministic refresh of generated outputs.

### Watch mode

```bash
python3 scripts/propagate_master_assets.py --watch
```

Watch mode monitors these directories:

- `.github/agents/`
- `.github/skills/`
- `.github/instructions/`

It rewrites generated outputs when files in those folders change.

## VS Code Tasks

The repository provides these tasks:

- `propagate: master assets (once)`
- `watch: propagate master assets`

The watch task is configured with `runOn: folderOpen`, so VS Code will start it automatically when the folder opens unless you disable task auto-run in your environment.

## What To Verify After Changes

### After updating `.github/` source files

- Run the one-shot propagation command if the watcher is not already running.
- Confirm the expected updates appear under `claude/agents/`, `opencode/agents/`, and `codex/agents/`.
- Check that filenames match platform conventions, including any aliases or `z-` prefixes.

### After updating documentation

- Review `README.md`, `docs/ARCHITECTURE.md`, `docs/CODEBASE_CONTEXT.md`, `docs/LOCAL_DEVELOPMENT.md`, and `docs/TROUBLESHOOTING.md` together so counts, paths, and terminology stay aligned.
- Re-read command examples to ensure they refer to files and tasks that actually exist in the repo.

### After updating template packs

- Confirm both copied paths still make sense in a target repository:
  - `AGENTS.md` at project root
  - `docs/STYLE_GUIDE.md` under the destination repo's `docs/` folder

## Testing And Validation

Python regression tests live under `tests/`. The repository has no package manifest,
so invoke the runner available in the active development environment rather than
assuming an installed project package.

Use this validation sequence:

1. Run `python3 scripts/propagate_master_assets.py --once` when `.github/` source files changed.
2. Run the focused Python tests for the changed propagation, hook, or runtime-deployment behavior.
3. Inspect `git diff` for unexpected generated output churn.
4. If you changed harness setup or porting docs, compare the documented paths against the checked-in directories and config files.

Interpretation guidance:

- A clean propagation run with only expected file updates is the normal success case.
- Large unexpected diffs in generated outputs usually mean a source rename, alias mismatch, or instruction-routing change.
- If the propagation command fails before writing files, fix that error first rather than editing generated outputs manually.

## Reviewed Runtime Deployment

Runtime deployment is not part of the ordinary source-edit loop. When it is explicitly
required, restart any long-running watcher and follow [HARNESS_SETUP.md](../HARNESS_SETUP.md):
converge repository outputs, generate and review the active-home inventory, then rerun
with the reviewed digest and watcher-restart confirmation. Never test this path against
an unreviewed live home or replace it with ad hoc links or copy commands.

## Harness-Specific Setup References

- See [HARNESS_SETUP.md](../HARNESS_SETUP.md) for multi-root VS Code, Claude Code, and OpenCode setup.
- See [docs/porting/README.md](porting/README.md) for the porting docs index.
- See [codex/README.md](../codex/README.md) for the separation between repository-owned Codex content and runtime `.codex/` configuration.
