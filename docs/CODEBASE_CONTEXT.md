# Codebase Context

Quick-reference for AI agents working in this repository.

## What This Repo Is

- Single source-of-truth repository for multi-harness agent assets.
- Authoring surface is `source_of_truth/`. Everything else derived from it is generated.
- Two-stage pipeline: transform (`source_of_truth/` → `ports/`) then deploy (`ports/` → real harness dirs).
- Mostly Markdown plus two Python scripts (stdlib only) and a shared module.
- No root `package.json` or `pyproject.toml` runtime deps; Python tests live under `tests/`.

## Current Counts

- 56 source agent definitions in `source_of_truth/agents/` (53 `*.agent.md` + `auditor.md` + `docs-writer.md` + `04f-prod-code-review.md`), of which 37 hidden subagents (`user-invocable: false`) and 19 user-invocable.
- 34 skills in `source_of_truth/skills/`.
- 16 instructions in `source_of_truth/instructions/`.
- 4 learnings in `source_of_truth/learnings/`.
- 1 defunct hook artifact set in `source_of_truth/hooks/`.

## Key Paths

```text
AGENTS.md                                  # code-review-graph MCP workflow guidance
INSTALLATION.md                            # deploy pointer
source_of_truth/                           # THE authoring surface
  agents/
    README.md                              # full agent catalog and pipeline docs
    *.agent.md                             # 53, plus the three plain .md agents below (56 total definitions)
    auditor.md                             # plain .md agent (audit orchestrator)
    docs-writer.md                         # plain .md agent (loaded by frontmatter)
    04f-prod-code-review.md                # plain .md agent (loaded by frontmatter)
  skills/                                  # 34 skill dirs, each rooted at SKILL.md
  instructions/                            # 16 applyTo-glob instruction files
  learnings/                               # 4 learnings files
  hooks/                                   # defunct injection scanner (DEFUNCT.md)
  baseline/baseline-instructions.md        # sentinel-sectioned baseline template, rendered at deploy time
ports/                                     # GENERATED — do not hand-edit
  claude/  {agents, commands, skills, learnings}
  codex/   {agents, skills, learnings}             # TOML agents
  opencode/{agents, skills}
  cursor/  {commands, rules}               # commands=*.md, rules=*.mdc
  github/  {agents, hooks, instructions, learnings, skills}   # verbatim mirror
.github/                                   # real deployed mirror of ports/github
scripts/
  propagate_master_assets.py               # transform entry point (--once | --watch)
  asset_paths.py                           # shared markers + poll_watch
  extract_pdfs.py, setup-hook-symlinks.sh  # utilities
deploy_agents.py                           # deploy entry point (root, not scripts/)
docs/ ARCHITECTURE.md CODEBASE_CONTEXT.md COPILOT_SETUP.md LOCAL_DEVELOPMENT.md TROUBLESHOOTING.md
docs/porting/ docs/inspiration/
eval/ benchmarks/ packages/ tests/
.deploy-config.json                        # gitignored; saved harness selection
.vscode/tasks.json                         # propagate once/watch + deploy watch
```

## Pipeline Model

- Edit `source_of_truth/{agents,skills,instructions,learnings,hooks}` first.
- Transform: `python3 scripts/propagate_master_assets.py --once` (default) or `--watch`.
  Runs to a fixed point via `propagate_until_converged` (max 25 passes).
- Transform targets: `ports/{claude,codex,opencode,cursor}` plus `ports/github` and `.github/`.
- Deploy: `python3 deploy_agents.py [--harness a,b | --all | --watch | --list | --no-save | --skip-tools]`.
- Deploy also bootstraps companion tools (code-review-graph via pip/pipx, Context7 via
  `npx ctx7 setup`) unless `--skip-tools`; failures warn and never block deployment.
- Deploy destinations:
  - claude → `$CLAUDE_CONFIG_DIR` or `~/.claude` (agents, commands, skills, learnings)
  - codex → `$CODEX_HOME` or `~/.codex` (agents) + `~/.agents/skills` (skills)
  - opencode → `$OPENCODE_CONFIG_DIR` or `~/.config/opencode` (agents, skills)
  - cursor → `~/.cursor` (commands, rules)
  - github → `<repo>/.github` (verbatim mirror of the 5 subdirs)
- Deploy selection persists to `.deploy-config.json` (gitignored) unless `--no-save`.
- Deploy also splices a baseline instructions file per harness (`deploy_baseline`),
  rendered from `source_of_truth/baseline/baseline-instructions.md` with real home
  paths substituted at deploy time (no OS branching — `Path.home()` handles it):
  - claude → `<claude config dir>/CLAUDE.md`
  - codex → `<CODEX_HOME>/AGENTS.md`
  - opencode → `<OPENCODE_CONFIG_DIR>/AGENTS.md`
  - cursor → `~/.cursor/rules/baseline-instructions.mdc` (`alwaysApply: true` frontmatter)
  - github → `<repo>/.github/copilot-instructions.md` (a `.github/AGENTS.md` would only
    scope to files under `.github/`)
- Baseline splice model: three sections delimited by sentinel comments
  (`<!-- context7 -->`, `<!-- code-review-graph -->`, `<!-- agent-discovery -->`);
  only sentinel blocks are replaced/appended, content outside them is never touched;
  idempotent (second run → `unchanged`); every failure returns a status, never raises.
- The cursor baseline `.mdc` deliberately carries NO generated marker so the
  `~/.cursor/rules` prune pass treats it as foreign and leaves it alone.

## Important Script Facts

- Both scripts are stdlib-only and share `scripts/asset_paths.py`.
- `deploy_agents.py` lives at the repo root, not in `scripts/`; it imports `scripts.asset_paths`.
- Generated-marker ownership: a destination file is overwritten/pruned only if it
  carries a marker at the emitter's exact write position (line 0 for no-frontmatter
  output, the line after the closing `---` otherwise). A file merely quoting a marker
  in prose stays inert.
- Legacy `.github`-text markers are still honored so the source_of_truth marker-text
  change did not orphan previously generated files.
- Skill auxiliary files carry no marker of their own; the whole skill dir is owned via
  its marked `SKILL.md`.
- The `github` harness is a verbatim mirror: its files carry no marker and are treated
  as unconditionally managed within the 5 mirrored subdirs.
- Deploy heals debris from the old symlink deployment: destination roots that are
  symlinks pointing into this repo (or dangling) are unlinked and replaced with real
  dirs; foreign symlinks are left alone and skipped.
- Known filename aliases: `docs-writer` → `docs-writer`, `web-research-specialist` →
  `web-researcher`, `audit-code-or-infra` → `audit-code-infra-refactor` (legacy: the
  source file is now `auditor.md`, which emits under its own name).
- Hidden (non-user-invocable) subagents become `z-*` in Claude and Codex outputs.

## Platform Surface Rules

- `source_of_truth/` is the only shared source-of-truth for agents, skills, instructions, learnings.
- `ports/*` and `.github/` are generated outputs, not authoring surfaces.
- Make the logical change in `source_of_truth/` first; do not mirror it manually into `ports/`.
- Rerun propagation rather than hand-editing generated outputs.

## Testing

- Python regression tests under `tests/` cover both scripts.
- Run with `uv run pytest tests/` (or `.venv/bin/python -m pytest tests/`); bare
  `python -m pytest` may lack pytest.
- `tests/_propagate_env.py` redirects the propagator's directory globals to a temp tree
  so tests never read/write the real repo.

## Do Not

- Do not treat this repo as Markdown-only; the two scripts are the maintenance flow.
- Do not edit generated `ports/*` or `.github/*` first unless intentionally repairing generation.
- Do not assume filename parity across platforms; aliases and `z-` prefixes are intentional.
- Do not reference removed surfaces: `nodejs/`, `python/`, `HARNESS_SETUP.md`, `.mcp.json`,
  `codex/README.md`, and `scripts/runtime_deployment.py` no longer exist.
- Do not treat `04f-prod-code-review.md`, `auditor.md`, or `docs-writer.md` as non-agent content
  just because they lack the `.agent.md` suffix.
- Do not document a root `dev/` beyond `dev/pr-review/` (its fixtures are tracked; run output is gitignored).
