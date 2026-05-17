# Troubleshooting

## Local Setup

### Symptom

`pyenv: cannot rehash: couldn't acquire lock ...` or `cannot overwrite existing file`

### Cause

Your shell startup is hitting a blocked or stale `pyenv` rehash operation before repo commands run. This is external to the repository, but it can break local propagation commands because they rely on a working `python3` in the shell.

### Fix

- Confirm no other `pyenv` process is actively running.
- Clear the stale `pyenv` lock or shim file only after verifying it is not in use.
- Open a fresh shell and verify `python3` resolves before rerunning repo commands.

## Propagation And Generated Outputs

### Symptom

Changes under `.github/` do not appear in `claude/agents/`, `opencode/agents/`, or `codex/agents/`.

### Cause

The propagation watcher is not running, or you changed source-of-truth files without rerunning the one-shot generation command.

### Fix

- Run `python3 scripts/propagate_master_assets.py --once`.
- In VS Code, confirm the `watch: propagate master assets` task is running.
- If you edited generated files directly, rerun propagation and recheck the diff from the `.github/` source.

### Symptom

Generated filenames do not match the source agent slug.

### Cause

The propagation script intentionally rewrites some names for target platforms. It also uses `z-` prefixes for hidden Claude and Codex subagents.

### Fix

- Check the alias rules in `scripts/propagate_master_assets.py` before assuming a file is missing.
- Expect these built-in aliases:
  - `documentation-architect` -> `docs-writer`
  - `web-research-specialist` -> `web-researcher`
  - `audit-code-or-infra` -> `audit-code-infra-refactor`
- Expect non-user-invocable agents to become `z-*` files in Claude and Codex outputs.

### Symptom

An agent exists in `.github/agents/` but is skipped by downstream tooling.

### Cause

The source file may not have valid agent frontmatter. The propagation script loads agent definitions by checking for `name` and `description`, not strictly by extension.

### Fix

- Verify the file has frontmatter with `name` and `description`.
- Do not rename `prod-code-review.md` just because it lacks `.agent.md`; it is intentionally part of the source set.

## VS Code And Harness Loading

### Symptom

GitHub Copilot does not show the agents from this repository.

### Cause

The repository is not open as part of the current VS Code workspace, so Copilot cannot discover `.github/agents/`, `.github/skills/`, and `.github/instructions/`.

### Fix

- Open this repository as a workspace folder.
- If you are working in another repo, use a multi-root workspace as described in [HARNESS_SETUP.md](../HARNESS_SETUP.md).

### Symptom

Claude or OpenCode cannot see skills or agents that should be symlinked from this repo.

### Cause

The global or project-local symlinks were not created, or the host platform checked symlinks out as plain files.

### Fix

- Recreate the symlinks using the instructions in [HARNESS_SETUP.md](../HARNESS_SETUP.md).
- On Windows, verify symlink support is enabled before re-checking out or recreating the linked directories.

### Symptom

Code-review-graph tools are unavailable even though the repo documents them.

### Cause

The MCP server configuration exists in `.mcp.json` and `.codex/config.toml`, but the runtime that should load it is not active or cannot resolve `uvx`.

### Fix

- Verify `uvx` is installed and available on your `PATH`.
- Confirm the active harness is loading the repo's MCP configuration file.
- Retry after restarting the harness session so it reloads MCP configuration.

## Documentation Drift

### Symptom

Counts in `README.md`, `docs/ARCHITECTURE.md`, and `docs/CODEBASE_CONTEXT.md` disagree.

### Cause

Agent, skill, or instruction inventories changed without updating the standard docs as a set.

### Fix

- Update all three standard overview docs in the same change.
- Recount the actual files in `.github/agents/`, `.github/skills/`, and `.github/instructions/` before finalizing the docs.

### Symptom

Docs mention paths like `dev/` that do not exist in this repository.

### Cause

Older documentation was copied forward from agent expectations for downstream project repos rather than this repository's actual checked-in structure.

### Fix

- Prefer the real workspace layout over inferred agent output paths when documenting this repo.
- Keep repository docs focused on checked-in directories and explicitly label downstream project conventions when they appear.