# Codebase Context

Quick-reference for AI agents working in this repository.

## What This Repo Is

- Single source-of-truth repository for multi-harness agent assets.
- Authoring surface is `source_of_truth/`. Everything else derived from it is generated.
- Two-stage pipeline: transform (`source_of_truth/` → `ports/`) then deploy (`ports/` → real harness dirs).
- Mostly Markdown plus two Python scripts (stdlib only) and a shared module.
- No runtime dependencies. Root `pyproject.toml` is gitignored and carries pytest config only; no `package.json`. Python tests live under `tests/`.

## Current Counts

- 66 source agent definitions in `source_of_truth/agents/` (all `*.agent.md`), of which 50 hidden subagents (`user-invocable: false`) and 16 user-invocable.
- 50 skills in `source_of_truth/skills/`.
- 24 instructions in `source_of_truth/instructions/`.
- 1 installable hook in `source_of_truth/hooks/`, mirrored verbatim to `ports/github/hooks/` and `.github/hooks/`. `creative-canon-guard.py` is installed by the writer into their own vault's `.claude/`; see `docs/CREATIVE_TOOLKIT.md`.
- `ports/claude/agents` = 52, `ports/claude/commands` = 16.
- Four of the agents, five of the skills, and one of the instructions belong to the
  creative writing family (`profile: creative`); see **Authoring profiles** below.

## Key Paths

```text
AGENTS.md                                  # repo-wide guidelines (layout, style, testing, comms)
CLAUDE.md                                  # pointer to AGENTS.md
README.md USAGE.md CONTRIBUTING.md         # overview, agent catalog, contributor rules
INSTALLATION.md                            # deploy pointer
source_of_truth/                           # THE authoring surface
  agents/
    *.agent.md                             # 66 agent definitions
  skills/                                  # 50 skill dirs, each rooted at SKILL.md
  instructions/                            # 24 applyTo-glob instruction files
  baseline/baseline-instructions.md        # sentinel-sectioned baseline template, rendered at deploy time
ports/                                     # GENERATED — do not hand-edit
  claude/  {agents, commands, skills}
  codex/   {agents, skills}             # TOML agents; profiles/ = retired cleanup root
  opencode/{agents, skills}
  cursor/  {agents, commands, rules, skills}  # commands/agents=*.md, rules=*.mdc
  github/  {agents, instructions, skills}          # verbatim mirror
.github/                                   # real deployed mirror of ports/github; gitignored
scripts/
  propagate_master_assets.py               # transform entry point (--once | --watch)
  asset_paths.py                           # shared markers + poll_watch
  extract_pdfs.py                          # utility
deploy_agents.py                           # deploy entry point (root, not scripts/)
.claude/hooks/block-propagation.py         # PreToolUse hook: agents may not RUN propagation
docs/ ARCHITECTURE.md AUTHORING.md CODEBASE_CONTEXT.md COPILOT_SETUP.md LOCAL_DEVELOPMENT.md TROUBLESHOOTING.md
docs/ ai-instruction-framework.md UNDERSTANDING_AGENTIC_ECOSYSTEM.md
docs/porting/                              # CLAUDE/CODEX/OPENCODE guides + TOOL_MAPPING
dev/                                       # gitignored scratch; nothing here is tracked
tests/fixtures/pr-review/                  # tracked PR-review fixtures (NOT under dev/)
eval/                                      # past benchmark artifacts; deprecated/ = archived grader
benchmarks/ packages/ tests/
.deploy-config.json                        # gitignored; saved harness selection
.vscode/                                   # gitignored; no tasks shipped in a clone
```

## Pipeline Model

- Edit `source_of_truth/{agents,skills,instructions}` first.
- Transform: `python3 scripts/propagate_master_assets.py --once` (default) or `--watch`.
  Runs to a fixed point via `propagate_until_converged` (max 25 passes).
- Agents must NOT run the transform — the maintainer does it by hand. `.claude/settings.json`
  wires a `PreToolUse` Bash hook (`.claude/hooks/block-propagation.py`) that exits 2 on any
  command executing the script; inspection commands (grep, read) pass. After editing source,
  report that propagation is pending. Sync tests fail until it runs; that is expected.
- Transform targets: `ports/{claude,codex,opencode,cursor}` plus `ports/github` and `.github/`.
- Deploy: `python3 deploy_agents.py [--harness a,b | --all | --watch | --list | --no-save | --skip-tools]`.
- Deploy also bootstraps companion tools (code-review-graph via pip/pipx, Context7 via
  `npx ctx7 setup`) unless `--skip-tools`; failures warn and never block deployment.
- Deploy destinations:
  - claude → `$CLAUDE_CONFIG_DIR` or `~/.claude` (agents, commands, skills)
  - codex → `$CODEX_HOME` or `~/.codex` (agents) + `~/.agents/skills` (skills)
  - opencode → `$OPENCODE_CONFIG_DIR` or `~/.config/opencode` (agents, skills)
  - cursor → `~/.cursor` (agents, commands, rules, skills; needs Cursor 2.4+)
  - github → `<repo>/.github` (verbatim mirror of the mirrored subdirs)
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
- Baseline splice model: the template is a **manifest**, not a body. `baseline_section_names`
  reads its bullet list with `^- ([a-z0-9-]+)$`, so surrounding prose can change freely.
  Each bullet names `source_of_truth/instructions/<name>.instructions.md`, which must carry
  `baseline: true`. `_instruction_body` strips the frontmatter, drops the trailing Load Canary
  section, and demotes the H1 to an H2. Currently 11 sections: `agent-discovery`,
  `challenge-assumptions`, `code-change-strategy`, `code-review-graph`,
  `codebase-context-bootstrap`, `language-standards`, `learnings-bootstrap`,
  `output-verbosity-policy`, `proactive-research`, `prose-standards`, `question-hygiene`.
- Deploy also splices `<!-- baseline-canary -->`, one aggregate canary naming the count and
  every section it wrote. Per-instruction canaries are stripped on the way in, so without it
  a stale global file reads identically to a current one. A canary whose section list does
  not match the template means that machine has not deployed since the template changed.
- Only sentinel blocks are replaced/appended, content outside them is never touched;
  idempotent (second run → `unchanged`); every failure returns a status, never raises.
- `RETIRED_BASELINE_SECTIONS` (`deploy_agents.py`) names sections this repo no longer splices
  and actively deletes. Dropping a name from the template only stops rewriting the block;
  listing it as retired removes the stale one a previous deploy already wrote, and it stays
  listed until every machine has deployed past it. Retired: `context7`, `phase-doc-sync`,
  `know-the-audience`. Context7's rules live in this repo's own `AGENTS.md` instead, and the
  companion-tool bootstrap installs the MCP server regardless — the retirement drops text, not tooling.
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
  as unconditionally managed within the mirrored subdirs.
- Deploy heals debris from the old symlink deployment: destination roots that are
  symlinks pointing into this repo (or dangling) are unlinked and replaced with real
  dirs; foreign symlinks are left alone and skipped.
- Known filename aliases: `docs-writer` → `docs-writer`, `web-research-specialist` →
  `web-researcher`, `audit-code-or-infra` → `audit-code-infra-refactor` (legacy: the
  source file is now `auditor.agent.md`, which emits under its own name).
- Hidden (non-user-invocable) subagents become `z-*` in Claude and Codex outputs, except
  where a pre-existing generated stem is reused: `03f-prod-code-review` stays
  `prod-code-review.md` and `03h-unity-reviewer` stays `unity-reviewer.md` in
  `ports/claude/agents` for that reason.
- Claude emission rule: hidden -> subagent file only; user-invocable -> slash command,
  plus a subagent file only if an orchestrator names it as a child (dual-use). So
  `ports/claude/agents` = 50 hidden subagents plus two dual-use agents = 52, while
  `ports/claude/commands` = 16.
- Codex and OpenCode emit every source agent; only Claude and Cursor split commands out.
- Cursor subagent names are the Claude identifier with a `z-` prefix always applied, because
  Cursor resolves commands and subagents from one `/name` namespace.
- `ports/cursor/rules` = any instruction whose `applyTo` globs are
  not all agent-targeted. Agent-targeted instructions are excluded because they ship
  inside the agents; the exclusion test in `propagate_cursor_rules_once` matches patterns
  ending in `.agent.md` or `agents`. Every source agent now carries the `.agent.md`
  suffix, so any glob naming an agent is recognized as agent-targeted.
- `applyTo` globs are matched with `fnmatch` against each agent's repo-relative path, so
  `**/x.agent.md` only matches when a `/` immediately precedes `x`. Numbered agents must
  be named in full (`**/03b-feature-implementer.agent.md`). A pattern that matches nothing
  fails silently — no error, the instruction simply ships to no agent.
- `GITHUB_MIRRORED_SUBDIRS` (`deploy_agents.py`) lists `learnings`, which has no source dir.
  The entry is a cleanup root so a past deploy's mirrored tree stays prunable.
- Agents read and write a working repo's learnings at `docs/learnings/` in that repo —
  durable project knowledge belongs beside the other docs, not in `.github/`, which is
  GitHub's own machine-config surface. Nothing seeds or propagates that directory.

## Authoring Profiles

- `profile:` frontmatter partitions the corpus. `technical` is the default and is **never
  written down** — an absent key means technical, so contributors adding engineering assets
  need to know nothing about this. `creative` is the only opt-in token.
- The gate lives in `applicable_instructions` (`scripts/propagate_master_assets.py`) and is
  symmetric: a technical instruction is never inlined into a creative agent, and a creative
  instruction is never inlined into a technical one. An unrecognized value raises rather than
  falling back, so a typo cannot ship a creative asset into the technical set.
- `propagate_cursor_rules_once` skips every non-technical doc unconditionally, so a creative
  instruction can never deploy as a user-global Cursor rule.
- Because instruction bodies are inlined as literal text at propagation time, the isolation
  holds on every harness with no per-harness feature involved.
- Creative agents are named `creative-*.agent.md` — the agent glob is flat, so the family is a
  filename prefix and not a subdirectory. `creative-profile.instructions.md` carries the skill
  allow-list. Skill isolation stays soft: `map_tools_for_claude` hardcodes `Skill` into every
  Claude agent. `docs/CREATIVE_TOOLKIT.md` states which guarantees are hard and which are soft.
- `tests/test_creative_profile_family.py` holds the family's guards, derived from disk rather
  than enumerated: adding a creative skill without allow-listing it fails.

## Platform Surface Rules

- `source_of_truth/` is the only shared source-of-truth for agents, skills, and instructions.
- `ports/*` and `.github/` are generated outputs, not authoring surfaces.
- Make the logical change in `source_of_truth/` first; do not mirror it manually into `ports/`.
- Rerun propagation rather than hand-editing generated outputs.

## Testing

- 28 Python test modules under `tests/` cover both scripts plus the agent corpus. The Unity contract
  modules are `test_unity_skill_contract.py`, `test_unity_consumer_contract.py`, and
  `test_unity_reference_assets.py`; Phase 02 uses `test_phase_refiner_final_check.py`.
- Run with `uv run pytest tests/` (or `.venv/bin/python -m pytest tests/`); bare
  `python -m pytest` may lack pytest.
- `tests/_propagate_env.py` redirects the propagator's directory globals to a temp tree
  so tests never read/write the real repo.
- `tests/test_agent_corpus_invariants.py` holds the corpus guards: every frontmatter
  roster entry names a real agent and is spawnable, frontmatter is well-formed for agents
  and skills, every instruction declares an `applyTo` that matches at least one real file,
  and no large block is duplicated across three or more agents.
- `tests/test_creative_profile_family.py` guards the creative writing family: the filename
  prefix and `profile: creative` must agree in both directions, only the scribe holds a write
  tool, no instruction crosses the profile boundary, and the allow-list matches the creative
  skills on disk.
- Corpus checks are structural only — they compare frontmatter, paths, and tool grants.
  Never add a check keyed to agent prose; it goes inert the moment someone rewords.

## Do Not

- Do not treat this repo as Markdown-only; the two scripts are the maintenance flow.
- Do not edit generated `ports/*` or `.github/*` first unless intentionally repairing generation.
- Do not assume filename parity across platforms; aliases and `z-` prefixes are intentional.
- Do not reference removed surfaces: `nodejs/`, `python/`, `HARNESS_SETUP.md`, `.mcp.json`,
  `codex/README.md`, and `scripts/runtime_deployment.py` no longer exist.
- Do not assume the `.agent.md` suffix is what makes a file an agent: loading keys off
  `name`/`description` frontmatter, and `source_of_truth/agents/*.md` is globbed wholesale.
- Do not reintroduce `source_of_truth/learnings/`. Durable repo-agnostic rules are
  skills; this repository's own authoring knowledge is `docs/AUTHORING.md`; a working
  repo's findings belong in its own `docs/learnings/`.
- Do not document anything under root `dev/` as part of the repo. `dev/*` is gitignored
  in full — it is local scratch (audit write-ups, inspiration notes, PR-review run output).
  Tracked PR-review fixtures live at `tests/fixtures/pr-review/`. Agent *runtime* output
  paths like `dev/feature/` are conventions agents create in a target repo, not here.
- Do not tell contributors to use VS Code tasks: `.vscode/` is gitignored and a clone has none.
