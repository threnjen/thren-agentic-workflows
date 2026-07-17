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
```

Deploy copies from `ports/`. If you have edited anything under `source_of_truth/`, first
regenerate the outputs:

```bash
python3 scripts/propagate_master_assets.py --once
```

See [docs/LOCAL_DEVELOPMENT.md](docs/LOCAL_DEVELOPMENT.md) for the full command reference
and destination table, and [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for failure
modes.
