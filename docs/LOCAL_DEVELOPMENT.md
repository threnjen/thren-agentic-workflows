# Local Development

## Purpose

This repository is maintained by editing source-of-truth files under
`source_of_truth/`, regenerating the derived `ports/` outputs, and (optionally)
deploying those outputs to your real harness config directories. There is no root
application to build or serve.

## Prerequisites

- `git`
- `python3` (standard library only — no third-party runtime dependencies)
- `uv` (or a virtualenv with `pytest`) to run the test suite
- Optional harness tooling depending on what you deploy to: Claude Code, Codex,
  OpenCode, Cursor, or GitHub Copilot in VS Code

## Clone And Open The Repo

```bash
git clone https://github.com/threnjen/thren-agentic-workflows.git
cd thren-agentic-workflows
```

Open the repository root in your editor. Both pipeline stages are driven from the command
line; no editor configuration is required.

## The Maintenance Loop

1. Edit source-of-truth files under `source_of_truth/{agents,skills,instructions}`.
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

It rewrites `ports/{claude,codex,opencode,cursor}`, plus `ports/github` and the real
`.github/` mirror.

### Propagation is yours, not an agent's

Run the transform yourself. A `PreToolUse` hook (`.claude/hooks/block-propagation.py`,
wired in `.claude/settings.json`) blocks an agent from executing the script and returns an
explanation instead — regenerating every file under `ports/` and `.github/` buries the
authored source diff you need to review. Agents may still read and grep the script.

An agent that edits `source_of_truth/` should stop and report that propagation is pending.
Sync tests, and any test that reads `ports/`, fail until you propagate. That failure is
correct, not something to fix by propagating.

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
| claude | `~/.claude` | `CLAUDE_CONFIG_DIR` | agents, commands, skills |
| codex | `~/.codex` + `~/.agents/skills` | `CODEX_HOME` | agents; skills |
| opencode | `~/.config/opencode` | `OPENCODE_CONFIG_DIR` | agents, skills |
| cursor | `~/.cursor` | — | agents, commands, rules, skills |
| github | `<repo>/.github` | — | verbatim mirror of `agents`, `hooks`, `instructions`, `skills` |

Learnings are not deployed at all. Agents read and write `docs/learnings/` in the
repository they are working in, and that directory is never seeded or propagated — a
repo's learnings are what its own agents recorded there.

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

The template is a manifest: deploy reads its bullet list, loads each named instruction
file from `source_of_truth/instructions/`, and splices that body under a
`<!-- <name> -->` sentinel. It adds one `<!-- baseline-canary -->` section naming every
section it wrote. Only sentinel blocks are replaced or appended; content outside them is
never touched, and a repeat run reports `unchanged`. The result appears under a
`baseline` key in the per-harness deploy output.

To add a section, add the instruction file with `baseline: true` in its frontmatter and
list its name in the template. To remove one, delete the bullet **and** add the name to
`RETIRED_BASELINE_SECTIONS` in `deploy_agents.py` — the bullet alone only stops rewriting
the block, leaving the stale one in every already-deployed file.

Deploy only ever overwrites or prunes files this system wrote (identified by a generated
marker, or membership in a marked skill directory). A hand-placed file at a destination
is left alone and reported under `skipped_paths` in the run output — delete it by hand if
you want it replaced.

## Editor Tasks (optional)

`.vscode/` is gitignored, so a fresh clone ships no editor tasks. If you want the watchers
to start on folder open, add your own `.vscode/tasks.json` wrapping
`propagate_master_assets.py --watch` and `deploy_agents.py --watch`. Nothing in the
maintenance loop depends on it.

## What To Verify After Changes

### After editing `source_of_truth/`

- Run the one-shot transform (or leave `--watch` running).
- Confirm the expected updates appear under `ports/{claude,opencode,codex,cursor}` and,
  for the mirrored subdirs, under `ports/github` and `.github/`.
- Check that filenames match platform conventions, including aliases and `z-` prefixes.

### After editing documentation

- Review `README.md`, `docs/ARCHITECTURE.md`, `docs/CODEBASE_CONTEXT.md`,
  `docs/LOCAL_DEVELOPMENT.md`, and `docs/TROUBLESHOOTING.md` together so counts, paths,
  and terminology stay aligned.

## Testing And Validation

Python regression tests live under `tests/` and cover the transform script, the deploy
script, and the agent corpus itself. Run them with the environment's Python:

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

`tests/test_agent_corpus_invariants.py` is the guard on the authored corpus: it catches a
roster entry naming an agent that no longer exists, malformed agent or skill frontmatter,
an `applyTo` glob that stopped matching anything (so the instruction silently ships to no
agent), and a large block duplicated across three or more agents. Every check is
structural — it reads frontmatter and paths, never agent prose, because a check keyed to
wording passes forever once someone rephrases the sentence it was watching.

Interpretation guidance:

- A clean transform with only expected updates is the normal success case.
- Large unexpected diffs in `ports/` usually mean a source rename, alias mismatch, or
  instruction-routing change.
- If the transform fails before writing files, fix that error first rather than editing
  generated outputs manually.

## Related References

- [docs/AUTHORING.md](AUTHORING.md) — authoring and deployment failure modes; read before
  editing an agent definition.
- [docs/porting/README.md](porting/README.md) — per-harness porting guides and tool mapping.
- [eval/deprecated/README.md](../eval/deprecated/README.md) — the archived eval-grader system.
