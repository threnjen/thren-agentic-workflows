# Installation

Deploy the generated agent assets to your real harness config directories with one
command from the repository root:

```bash
python3 deploy_agents.py
```

The first run asks which harnesses you use (Claude, Codex, OpenCode, Cursor, GitHub) and
saves the choice to `.deploy-config.json` (gitignored). Subsequent runs reuse it.

Common variants:

```bash
python3 deploy_agents.py --harness claude,cursor   # deploy specific harnesses
python3 deploy_agents.py --all                      # deploy everything
python3 deploy_agents.py --list                     # show resolved destinations
python3 deploy_agents.py --skip-tools               # skip companion-tool setup
```

## Baseline Instructions

Alongside the agent assets, deploy renders a per-harness baseline instructions file from
`source_of_truth/baseline/baseline-instructions.md`, substituting your machine's real
home paths at deploy time (so it works unchanged on Mac, Windows, or Linux):

| Harness | Baseline destination |
|---|---|
| claude | `~/.claude/CLAUDE.md` (respects `CLAUDE_CONFIG_DIR`) |
| codex | `~/.codex/AGENTS.md` (respects `CODEX_HOME`) |
| opencode | `~/.config/opencode/AGENTS.md` (respects `OPENCODE_CONFIG_DIR`) |
| cursor | `~/.cursor/rules/baseline-instructions.mdc` (an `alwaysApply` rule) |
| github | `<repo>/.github/copilot-instructions.md` |

The baseline contains three sections — Context7 usage, code-review-graph usage, and
agent/skill discovery — each wrapped in HTML sentinel comments (for example
`<!-- context7 -->`). Deploy only replaces content between matching sentinels (or
appends a missing section); everything else in the file is yours and is never touched.
Re-running deploy is idempotent and reports the file as `unchanged`.

## Using Named Agents in Codex

After deploying the Codex harness, request the agent in the prompt:

```bash
codex '@feature-decomposer decompose Phase 08a into execution-ready feature bundles'
```

The `@feature-decomposer` text activates the installed agent-designator router;
it is not a Codex CLI option. A natural-language request such as `Act as the
feature-decomposer ...` works as well.

Do not use `codex -p feature-decomposer` to select an agent. Codex defines
`-p`/`--profile` as configuration-profile selection, so that command starts the
ordinary session with a profile layer rather than adopting the feature
decomposer workflow.

## Companion Tools

Unless `--skip-tools` is passed, deploy also installs and configures two optional
companion tools the agents use when present:

- [code-review-graph](https://github.com/tirth8205/code-review-graph) — installed via
  `pip` or `pipx`, then configured with `code-review-graph install`.
- [Context7](https://context7.com) — configured via `npx ctx7 setup` (requires Node.js).

Both are best-effort: if a tool cannot be set up (for example, no Node.js on PATH for
Context7), deploy prints a warning explaining why and continues — a failed tool install
never blocks asset deployment.

Deploy copies from `ports/`. If you have edited anything under `source_of_truth/`, first
regenerate the outputs:

```bash
python3 scripts/propagate_master_assets.py --once
```

**GitHub Copilot users**: the github harness deploys into this repo's own `.github/`;
to use the agents from another project, open this repo in your VS Code workspace
alongside that project — see [docs/COPILOT_SETUP.md](docs/COPILOT_SETUP.md).

See [docs/LOCAL_DEVELOPMENT.md](docs/LOCAL_DEVELOPMENT.md) for the full command reference
and destination table, and [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for failure
modes.
