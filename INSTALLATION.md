# Installation

Deploy the generated agent assets to your real harness config directories with one
command from the repository root:

```bash
python3 deploy_agents.py
```

The first run asks which harnesses you use (Claude, Codex, OpenCode, Cursor, GitHub) and
saves the choice to `.deploy-config.json` (gitignored). Subsequent runs reuse it.
The saved file also carries `"comms_profile": false` by default. Set it to `true` only
after installing and probing Crosswire.

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

The baseline contains eleven technical sections by default. The opt-in communications
profile adds the `comms-protocol` section for a twelve-section enabled baseline.
Each section is wrapped in an HTML sentinel comment, and deploy only replaces content
between matching sentinels. Everything else in the file remains yours.

With communications enabled, selected harnesses run the explicit
`crosswire-turn-hook --probe --config PATH` check before a registration writer mutates
its configuration. Only the exact `CROSSWIRE_HOOK_PROBE_OK` output permits a write.
The deployment report includes each target path and lifecycle status.

To roll back, set `"comms_profile": false` in `.deploy-config.json` and run
`python3 deploy_agents.py`. The deployment removes owned registrations and the contract
section while preserving foreign content. It reports removed owned content for recovery.

## Claude Code Registration

When the communications profile is enabled, Claude receives one owned `Stop` hook in
`settings.json` under the resolved Claude root:

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "crosswire-turn-hook --adapter claude --config PATH # <!-- crosswire-comms-registration -->",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

`CLAUDE_CONFIG_DIR` selects the Claude root. Without it, deployment uses `~/.claude`.
The default Crosswire config path is `hook-config.json` under that root until a host
configuration contract establishes a user-global path. Pass an explicit path to the
registration lifecycle when embedding deployment.

Deployment runs `crosswire-turn-hook --probe --config PATH` before it writes. Only
the exact `CROSSWIRE_HOOK_PROBE_OK` line permits a write. The report identifies the
target and returns `created`, `updated`, `unchanged`, `removed`, or `failed` status.

With the profile disabled, deployment removes every `Stop` group carrying the exact
ownership tag, including hand-edited commands. The verbose report includes the removed
JSON group so an operator can recover edits. Foreign groups and unrelated settings stay
untouched. Agents do not run propagation. A maintainer must run it after source changes.

## Codex Registration

When the communications profile is enabled, deployment adds one owned top-level `notify`
assignment to `config.toml` under the resolved Codex root:

```toml
notify = ["crosswire-turn-hook", "--adapter", "codex", "--config", "/path/to/hook-config.json"] # <!-- crosswire-comms-registration -->
```

`CODEX_HOME` selects the Codex root. Without it, deployment uses `~/.codex`. The
registration preserves unrelated TOML bytes and owns only the one physical assignment
line with the exact trailing comment. A foreign top-level `notify` assignment is left
untouched and causes a bounded deployment failure rather than a duplicate key.

Before an enabled write, deployment runs `crosswire-turn-hook --probe --config PATH`.
Only a zero exit status with the exact `CROSSWIRE_HOOK_PROBE_OK` line permits mutation.
Failure output, unexpected output, timeout, launch failure, or a nonzero exit leaves the
target unchanged. The default Crosswire host configuration is `hook-config.json` under
the resolved Codex root, unless deployment supplies an explicit path.

To roll back Codex registration, set `"comms_profile": false` and deploy again. The
report prints every removed owned line, including hand-edited content, for recovery.
Foreign TOML remains unchanged. Agents do not run propagation. A maintainer must run it
after source changes.

## OpenCode Registration

When the communications profile is enabled, deployment writes one owned TypeScript plugin
to `plugins/crosswire-comms.ts` below the resolved OpenCode root:

```text
~/.config/opencode/plugins/crosswire-comms.ts
```

`OPENCODE_CONFIG_DIR` selects the OpenCode root. Without it, deployment uses
`~/.config/opencode`. The plugin handles `session.idle`, preserves the session and project
context, and invokes `crosswire-turn-hook --adapter opencode --config PATH` with an argument
vector and JSON on standard input. The configuration path is serialized as a TypeScript
string literal, so shell characters remain data.

Before an enabled write, deployment runs the shared probe and accepts only the exact
`CROSSWIRE_HOOK_PROBE_OK` line. Failure output, unexpected output, timeout, launch failure,
invalid paths, symlinked paths, or an unowned target leave the target unchanged. Foreign
plugin files remain byte-identical.

To roll back OpenCode registration, set `"comms_profile": false` and deploy again. The
deployment removes only `crosswire-comms.ts` when it carries the exact
`<!-- crosswire-comms-registration -->` marker, and prints the raw removed content for
recovery. Agents do not run propagation. A maintainer must run it after source changes.

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

## Using Named Agents in Cursor

Cursor needs version 2.4 or later: subagents arrived in 2.0 and skills in 2.4.

Deploy writes four directories under `~/.cursor`:

| Directory | Contents |
|-----------|----------|
| `commands/` | The user-facing agents. Type `/agent-name` to adopt that role. |
| `agents/` | The worker subagents an orchestrator delegates to, each named `z-...`. |
| `skills/` | Shared skills, loaded on demand by name. |
| `rules/` | Instruction files with source-file globs, plus the baseline rule. |

Subagent names carry a `z-` prefix because Cursor invokes commands and subagents
alike as `/name`. An agent that is both user-facing and spawned as a child would
otherwise claim the same name twice.

Cursor also reads `~/.claude/skills` and `~/.claude/agents` for compatibility, so
deploying both harnesses lands each asset twice. The copies are identical and
`~/.cursor` wins, but Cursor's Claude-compatible view of `~/.claude/agents` exposes
dual-use agents under their unprefixed names as well.

## Companion Tools

Unless `--skip-tools` is passed, deploy also installs and configures two optional
companion tools the agents use when present:

- [code-review-graph](https://github.com/tirth8205/code-review-graph) — installed via
  `pip` or `pipx`, then configured with `code-review-graph install --platform <p>`, run
  once per harness in your saved selection. Its bare `install` targets every platform it
  can detect and litters the repository with config for harnesses you do not use, so the
  selection scopes it. To configure a platform this repo does not port to (windsurf, zed,
  kiro, qoder, ...), run that CLI yourself.
- [Context7](https://context7.com) — its MCP server, configured via
  `npx ctx7 setup --claude --mcp -y` (requires Node.js). MCP mode is pinned because the
  agents call Context7's `resolve-library-id` and `query-docs` tools by name; the CLI +
  Skills mode of `ctx7 setup` registers no server. Presence is probed by looking for a
  `context7` entry in `~/.claude.json`.

Both are best-effort: if a tool cannot be set up (for example, no Node.js on PATH for
Context7), deploy prints a warning explaining why and continues — a failed tool install
never blocks asset deployment.

Deploy copies from `ports/`. If you have edited anything under `source_of_truth/`, ask a
maintainer to regenerate the outputs:

```bash
python3 scripts/propagate_master_assets.py --once
```

Agents do not run propagation. The maintainer must run it after source changes.

**GitHub Copilot users**: the github harness deploys into this repo's own `.github/`;
to use the agents from another project, open this repo in your VS Code workspace
alongside that project — see [docs/COPILOT_SETUP.md](docs/COPILOT_SETUP.md).

See [docs/LOCAL_DEVELOPMENT.md](docs/LOCAL_DEVELOPMENT.md) for the full command reference
and destination table, and [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for failure
modes.
