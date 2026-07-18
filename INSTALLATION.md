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

See [docs/LOCAL_DEVELOPMENT.md](docs/LOCAL_DEVELOPMENT.md) for the full command reference
and destination table, and [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for failure
modes.
