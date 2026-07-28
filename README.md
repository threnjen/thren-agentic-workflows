# thren-agentic-workflows

A ready-to-use library of AI development agents that work across Claude, Codex,
OpenCode, Cursor, and GitHub Copilot. Install once and you get a full software
development workflow — planning, implementation, review, testing, auditing, and
docs — driven by a handful of agents you talk to directly.

## Get Started

Install the agents into your own harness with one command from the repository root:

```bash
python3 deploy_agents.py
```

The first run asks which harnesses you use (Claude, Codex, OpenCode, Cursor, GitHub)
and remembers your choice. It only writes files this system generated — your
hand-maintained config is never touched.

**→ See [INSTALLATION.md](INSTALLATION.md) for full installation instructions, options,
and destinations.**

### Invoke a named agent in Codex

Put the agent name in the prompt. The `@name` form is a repository routing
convention, so it works after these assets are deployed:

```bash
codex '@feature-decomposer decompose Phase 08a into execution-ready feature bundles'
```

You can also say `Act as the feature-decomposer ...` in plain language. Do not
use `codex -p feature-decomposer`: `-p`/`--profile` selects a Codex configuration
profile and does not select a custom agent.

## What You Get

You interact with a small set of **primary agents**. Each one can drive a fleet of
automated helpers behind the scenes, so you stay focused on a few entry points.

### Core project workflow

A numbered pipeline you step through for building a project end to end:

| Step | Agent | You do |
|------|-------|--------|
| 1 | **Project - Planner** | Describe your project → get a phased roadmap |
| 2 | **Phase - Refiner** | Refine and stress-test one phase |
| 3 | **Feature - Decomposer** | Break the phase into ready-to-build features |
| 4 | **Phase - Execute** | Kick off — implementation, review, and QA run hands-free |
| 5 | **PR - Review** | Get a plain-language readiness report on your diff |

You drive these steps in order.

### On-demand specialists

Reach for these individually, whenever you need them — no pipeline required:

- **Single Feature - Agent** — a small, scoped change with an approval gate before it edits
- **Debugger** — diagnose and fix a frontend or backend error
- **Docs Writer** — create or update your repo's documentation
- **Web Researcher** — research a topic and produce a cited findings report
- **Audit - Code, Infra, Refactor, Security** — health-check your code, infra, structure, or
  security posture; audit two repos or two branches and get a reconciled delta of what changed
  between them
- **Test - Orchestrator** — analyze, write, or fix your test suite
- **QA - Bootstrapper** — generate a repo's QA_AUTOMATED and QA_USER package, then run it
- **Instructions Manager** — create and evaluate AI instruction files for a repository
- **Client Deliverable** — run a client engagement end to end (comparative audits, client
  narratives, compliance package) from an engagement configuration file

Behind these, a set of automated subagents and on-demand skills do the detailed work —
you never invoke them directly. The library ships 53 source agent definitions in
`source_of_truth/agents/`. For the complete catalog and how the pipeline flows,
see [USAGE.md](USAGE.md).

## How It Works

For users there are two steps, and the tool handles both:

1. **Pick your harnesses** — the first run of `deploy_agents.py` asks which tools you
   use and saves the choice.
2. **Deploy** — it copies the agents into the real config directories each harness reads
   (`~/.claude`, `~/.codex`, `~/.config/opencode`, `~/.cursor`, and this repo's `.github/`
   for Copilot).

Deploy is safe by construction: a destination file is only ever overwritten or removed
when it positively carries a generated marker (or lives inside a generated skill
directory). Hand-maintained files are never touched. Re-run `deploy_agents.py` anytime
to pull the latest.

Deploy also maintains a **baseline instructions file** per harness — `CLAUDE.md` for
Claude, `AGENTS.md` for Codex and OpenCode, an always-applied rule for Cursor, and
`.github/copilot-instructions.md` for Copilot. It carries three managed sections
(Context7 usage, code-review-graph usage, and agent/skill discovery) wrapped in HTML
sentinel comments; deploy splices only those sections, so anything you write outside
them in the same file is preserved.

## Prerequisites

- `python3` (standard library only — no third-party runtime dependencies)
- Optional harness tooling depending on what you deploy to: Claude Code, Codex,
  OpenCode, Cursor, or GitHub Copilot
- VS Code if you want the Copilot agent picker

The deploy script also installs and configures two optional companion tools the agents
use when present: [code-review-graph](https://github.com/tirth8205/code-review-graph)
(via `pip`/`pipx`) and the [Context7](https://context7.com) MCP server (via `npx`,
requires Node.js). Pass `--skip-tools` to opt out; a failed tool install never blocks
asset deployment.

## Deploy Commands

```bash
python3 deploy_agents.py                    # use saved selection, or prompt (tty) and save
python3 deploy_agents.py --harness claude,cursor
python3 deploy_agents.py --all
python3 deploy_agents.py --list             # show harnesses and resolved destinations
```

The first interactive run saves your choice to `.deploy-config.json` (gitignored);
subsequent runs are just `python3 deploy_agents.py`. Full details are in
[INSTALLATION.md](INSTALLATION.md).

## Related Documentation

- [INSTALLATION.md](INSTALLATION.md) — how to deploy the agents into your harness
- [docs/COPILOT_SETUP.md](docs/COPILOT_SETUP.md) — using the agents with GitHub Copilot
  (open this repo in your VS Code workspace alongside your project)
- [USAGE.md](USAGE.md) — the full agent
  catalog and pipeline flow
- [CONTRIBUTING.md](CONTRIBUTING.md) — for maintainers and contributors: how the repo is
  authored, transformed, and laid out

## Acknowledgements

- [code-review-graph](https://github.com/tirth8205/code-review-graph) by
  [tirth8205](https://github.com/tirth8205) — a local-first code knowledge graph
  (MCP + CLI) the agents use for token-efficient, structure-aware code review.
  The deploy script installs and configures it automatically.
- [Context7](https://context7.com) by [Upstash](https://upstash.com) — an MCP
  server providing current, version-accurate library documentation. Also
  auto-configured by the deploy script.
