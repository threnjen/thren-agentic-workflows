# Local Development

## Purpose

This repository is maintained by editing source-of-truth files under
`source_of_truth/`, regenerating the derived `ports/` outputs, and (optionally)
deploying those outputs to your real harness config directories. There is no root
application to build or serve.

## Prerequisites

- `git`
- `python3` (standard library only — no third-party runtime dependencies)
- VS Code if you want the built-in workspace tasks
- Optional harness tooling depending on what you deploy to: Claude Code, Codex,
  OpenCode, Cursor, or GitHub Copilot in VS Code

## Clone And Open The Repo

```bash
git clone https://github.com/threnjen/thren-agentic-workflows.git
cd thren-agentic-workflows
```

If you use VS Code, open the repository root. The workspace defines three tasks in
`.vscode/tasks.json` (see below).

## The Maintenance Loop

1. Edit source-of-truth files under `source_of_truth/{agents,skills,instructions,learnings}`.
2. Transform: regenerate `ports/` and `.github/` from source.
3. Review the resulting diff before committing.
4. Deploy (optional): copy the generated outputs to your real harness directories.

## Stage 1 — Transform (propagate)

### One-shot run

```bash
python3 scripts/propagate_master_assets.py --once
```

Runs a single propagation to a fixed point (it converges, then exits). `--once` is the
default, so bare `python3 scripts/propagate_master_assets.py` behaves the same. Use this
after a batch of source edits when you want a deterministic refresh. The command prints a
JSON convergence summary; a second run reporting zero changes confirms a fixed point.

### Watch mode

```bash
python3 scripts/propagate_master_assets.py --watch
```

Watch mode monitors the source directories and re-propagates when files change:

- `source_of_truth/agents/`
- `source_of_truth/skills/`
- `source_of_truth/instructions/`
- `source_of_truth/learnings/`

It rewrites `ports/{claude,codex,opencode,cursor}`, plus `ports/github` and the real
`.github/` mirror.

## Stage 2 — Deploy

```bash
python3 deploy_agents.py            # use saved selection, or prompt (tty) and save
python3 deploy_agents.py --harness claude,cursor
python3 deploy_agents.py --all
python3 deploy_agents.py --list     # show harnesses and resolved destinations
python3 deploy_agents.py --watch    # maintainer: auto-deploy on ports/ change
python3 deploy_agents.py --no-save  # do not persist the harness selection
python3 deploy_agents.py --skip-tools  # skip companion-tool install/config
```

Unless `--skip-tools` is passed, deploy also bootstraps two optional companion tools:
code-review-graph (via `pip`/`pipx`, then `code-review-graph install`) and the Context7
MCP server (via `npx ctx7 setup`, requires Node.js). Both are best-effort — a failure
prints a `[tools] WARNING` with the reason and never blocks asset deployment.

`deploy_agents.py` lives at the repository root (not under `scripts/`). The first
interactive run asks which harnesses you use and saves the choice to
`.deploy-config.json` (gitignored). After that, bare `python3 deploy_agents.py` reuses
the saved selection. A non-interactive shell with no saved selection and no flag errors
out with a usage hint rather than guessing.

### Deploy destinations

| Harness | Destination (default) | Env override | Subdirs |
|---|---|---|---|
| claude | `~/.claude` | `CLAUDE_CONFIG_DIR` | agents, commands, skills, learnings |
| codex | `~/.codex` + `~/.agents/skills` | `CODEX_HOME` | agents; skills |
| opencode | `~/.config/opencode` | `OPENCODE_CONFIG_DIR` | agents, skills |
| cursor | `~/.cursor` | — | commands, rules |
| github | `<repo>/.github` | — | verbatim mirror of the source subdirs |

After the asset copy, deploy also splices a baseline instructions file per harness,
rendered from `source_of_truth/baseline/baseline-instructions.md` with the machine's
real home paths substituted at deploy time:

| Harness | Baseline destination |
|---|---|
| claude | `<claude config dir>/CLAUDE.md` |
| codex | `<CODEX_HOME>/AGENTS.md` |
| opencode | `<OPENCODE_CONFIG_DIR>/AGENTS.md` |
| cursor | `~/.cursor/rules/baseline-instructions.mdc` (`alwaysApply` rule) |
| github | `<repo>/.github/copilot-instructions.md` |

Only the three sentinel-delimited sections (`<!-- context7 -->`,
`<!-- code-review-graph -->`, `<!-- agent-discovery -->`) are replaced or appended;
content outside the sentinels is never touched, and a repeat run reports `unchanged`.
The result appears under a `baseline` key in the per-harness deploy output.

Deploy only ever overwrites or prunes files this system wrote (identified by a generated
marker, or membership in a marked skill directory). A hand-placed file at a destination
is left alone and reported under `skipped_paths` in the run output — delete it by hand if
you want it replaced.

## VS Code Tasks

`.vscode/tasks.json` provides three tasks:

- `propagate: master assets (once)` — one-shot transform
- `watch: propagate master assets` — transform watcher, starts on folder open
- `watch: deploy ports to real harness dirs` — deploy watcher, starts on folder open

The two watch tasks are configured with `runOn: folderOpen`, so VS Code starts them
automatically when the folder opens unless you disable task auto-run.

## What To Verify After Changes

### After editing `source_of_truth/`

- Run the one-shot transform if the watcher is not already running.
- Confirm the expected updates appear under `ports/{claude,opencode,codex,cursor}` and,
  for the mirrored subdirs, under `ports/github` and `.github/`.
- Check that filenames match platform conventions, including aliases and `z-` prefixes.

### After editing documentation

- Review `README.md`, `docs/ARCHITECTURE.md`, `docs/CODEBASE_CONTEXT.md`,
  `docs/LOCAL_DEVELOPMENT.md`, and `docs/TROUBLESHOOTING.md` together so counts, paths,
  and terminology stay aligned.

## Testing And Validation

Python regression tests live under `tests/` and cover both the transform and deploy
scripts. Run them with the environment's Python:

```bash
uv run pytest tests/
```

(`.venv/bin/python -m pytest tests/` works too; bare `python -m pytest` may fail if
pytest is not installed in your base interpreter.)

Validation sequence:

1. Run the transform once after editing `source_of_truth/`.
2. Run the tests for the changed transform or deploy behavior.
3. Inspect `git diff` for unexpected churn under `ports/` or `.github/`.
4. Optionally run `python3 deploy_agents.py --all` against a throwaway `HOME` to confirm
   deploy behavior without touching your real config dirs:
   `HOME=$(mktemp -d) python3 deploy_agents.py --all`.

Interpretation guidance:

- A clean transform with only expected updates is the normal success case.
- Large unexpected diffs in `ports/` usually mean a source rename, alias mismatch, or
  instruction-routing change.
- If the transform fails before writing files, fix that error first rather than editing
  generated outputs manually.

## Related References

- [docs/porting/README.md](porting/README.md) — per-harness porting guides and tool mapping.
- [eval/deprecated/README.md](../eval/deprecated/README.md) — the archived eval-grader system.
