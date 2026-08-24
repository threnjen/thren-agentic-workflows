## What This Repo Is

A library of AI development agents (planning, implementation, review, testing, auditing, docs) deployed across five harnesses: Claude Code, Codex, OpenCode, Cursor, and GitHub Copilot. There is no application to build or serve — the workflow is: edit source, propagate, review the diff, deploy.

## The One Rule That Matters

**`source_of_truth/` is the only authoring surface.** Everything under `ports/` and the real `.github/` directory is generated output — never hand-edit them. If generated output looks wrong, fix the source and re-propagate. A sync-test failure means "rerun propagation," not "edit the output."

## Know The Audience

Every piece of English here has a reader. Pick the mode from the reader, not from the surrounding
style. Style-matching applies to **code, not prose.**

**Strict** — procedures, error messages, tool and agent descriptions, agent-to-agent instructions,
safety text. Anything parsed without a human present to resolve ambiguity.

**Flavored** — READMEs, PR descriptions, changelogs, explanatory prose, replies to a human. Same
sentence discipline, but word choice stays free.

**Neither** — client-facing deliverables, marketing copy, creative writing. Never apply these rules
there. Voice and persuasion are the point, and this removes both. Client deliverables follow
`engagement-client-voice` instead.

Dense is still correct for machine-facing planning docs — phase summaries, discovery context,
roadmaps, feature plan/context/tasks bundles. The agentic workflow consumes these to decompose
work, and spelling out every constraint helps it. Dense is never an excuse for ambiguous.

A runbook's only job is that someone follows it and succeeds. If it has to be parsed, it failed.

**BAD**: "prose is the one thing this corpus needs to be free to reword"
**GOOD**: "We need to be able to rewrite the words freely"

If the reader has to ask for a simpler version, the first version was wrong.

Write to a colleague who is sharp, busy, and has not read the rest of the phase.

To rewrite existing text, load the `prose-rewrite` skill for a full pass with per-violation findings.

### Sentence Rules — Both Modes

- **Active voice.** One instruction per sentence.
- **20 words for an instruction, 25 for a description.**
- **No semicolons.** An em dash is allowed, but usually marks a sentence that wants splitting.
- **Plain verbs.** Start, not spin up. Contact, not reach out. Read, not dive into.
- **Three words maximum in a noun stack.** "The handler that sets task-queue priority", not
  "the agent task queue priority handler".
- **Keep the subject, verb, and article explicit** even when dropping them would read shorter.
- **Simple tenses**, unless the compound tense carries information the simple one cannot —
  "the job has completed" says its output is available now; "the job completed" does not.

Strict mode adds: one word per action (never rotate check / verify / confirm), one name per thing,
verbs over noun forms ("analyze the log", not "perform an analysis of the log"), and every domain
term unpacked inline on first use.

**Never weaken or strengthen a hedge to save words.** "May have failed" is not "failed", and
confidence is content. A length cap is exactly what tempts you to cut it.

### Concrete Rules — Replies And Human-Facing Docs Alike

- **Answer first, evidence second.** Open with the conclusion and what it changes for the reader.
  Tables, spreads, and citations come after — or go in an appendix with a link.
- **Unpack every term on first use, inline.** "monotone (moves one direction, no zigzag)."
  Especially: monotone, spread, saturated, inverted, pooled, per-path, degenerate, control.
- **Translate any number that drives a decision.** "0.0034 spread" is not an answer; "too small
  to pick a winner from" is. Give both, in that order.
- **One caveat, not three.** State the claim, then the single caveat that could change what the
  reader does.
- **Reach for a physical analogy** when explaining whether a measurement or instrument is
  trustworthy. Analogies land, abstractions do not.
- **Bold the decision, not the vocabulary.**
- **Lead with the plain version even when a precise version follows.** If a summary is needed
  after the fact, the first pass was too dense.

### Extra Rules For Runbooks, QA Docs, And Checklists

- **Open with a TL;DR of five lines or fewer**: what this page is for, and the first thing to do.
- **The steps are the page.** Numbered, in order, one action each, with the exact command and what
  a correct result looks like. Rationale goes below the steps or behind a link — never between two
  steps the reader is trying to follow.
- **One screen per step.** If a step needs more, it is two steps.
- **Put warnings where the mistake happens**, not in a preamble the reader has already scrolled past.
- **No correction logs in the body.** When a step changes, rewrite the step. Historical
  "corrected on <date>" narration belongs in an appendix or the commit message; it doubles the
  length of the thing the reader has to parse.
- **Prose blocks over ~6 lines are a smell.** Convert to a list, a table, or delete.

### Before Sending Or Committing

- Is the first sentence the answer, or a windup?
- Any term used but not unpacked?
- Could the reader act on this after one read, without backtracking?
- For a runbook: could someone follow it start to finish without stopping to interpret anything?

## Companion tools

These rules used to ship in the user-global baseline. They now live here, so they apply to
this repository and not to every repository on the machine.

**Context7.** Fetch current documentation through the Context7 MCP whenever the question is
about a library, framework, SDK, API, CLI tool, or cloud service — including well-known ones.
Resolve the library ID first, then query with the full question scoped to one concept. Use it
even when you think you know the answer. Do not use it for refactoring, business-logic
debugging, code review, or general programming concepts.

**code-review-graph.** Use the code-review-graph MCP tools before Grep, Glob, and Read when
exploring this codebase. `semantic_search_nodes` or `query_graph` to find code,
`get_impact_radius` for blast radius, `detect_changes` plus `get_review_context` for review,
`get_architecture_overview` for structure. Fall back to file search when the graph does not
cover what you need.

`deploy_agents.py` still installs and configures both servers; `--skip-tools` suppresses that.


## Agents: never run propagation

**Propagation is the maintainer's manual step. Do not run `scripts/propagate_master_assets.py` (`--once` or `--watch`) as part of agent work**, even to make tests pass. It regenerates every file under `ports/` and `.github/`, which swamps the diff and makes authored source changes impossible to review.

Edit `source_of_truth/` only, then stop and report that propagation is pending. Sync tests and any test reading `ports/` will fail until the maintainer propagates — say so plainly rather than propagating to go green.


## Commands

```bash
# Transform: regenerate ports/ and .github/ from source_of_truth/
python3 scripts/propagate_master_assets.py --once

# Watch mode: re-propagate on every save under source_of_truth/
python3 scripts/propagate_master_assets.py --watch

# Deploy generated ports/ to real harness config dirs (~/.claude, ~/.codex, etc.)
python3 deploy_agents.py                     # uses saved selection in .deploy-config.json
python3 deploy_agents.py --harness claude,cursor
python3 deploy_agents.py --list              # show harnesses and resolved destinations
python3 deploy_agents.py --skip-tools        # skip companion-tool bootstrap

# Tests (pytest is a dev dep, not in the base interpreter)
uv run pytest tests/
uv run pytest tests/test_propagate_master_assets.py            # one file
uv run pytest tests/test_deploy_assets.py -k <test_name>       # one test
```

No third-party runtime dependencies — both scripts are stdlib-only Python.

## Architecture

Two-stage pipeline, two scripts:

1. **Transform** — `scripts/propagate_master_assets.py` reads `source_of_truth/{agents,skills,instructions}` and regenerates per-harness variants under `ports/{claude,codex,opencode,cursor}` (Claude/OpenCode markdown agents, Codex TOML agents + profiles, Cursor subagents, commands, `.mdc` rules, and skills). It also mirrors the source verbatim to `ports/github` and the real `.github/` (read by Copilot). Runs to a fixed point; prints a JSON convergence summary — a second run reporting zero changes confirms convergence. `scripts/asset_paths.py` holds shared markers and watch primitives.

2. **Deploy** — `deploy_agents.py` (repo root, not `scripts/`) copies `ports/` outputs into the real harness config dirs (`~/.claude`, `~/.codex` + `~/.agents/skills`, `~/.config/opencode`, `~/.cursor`; env overrides `CLAUDE_CONFIG_DIR`, `CODEX_HOME`, `OPENCODE_CONFIG_DIR`). It also splices a baseline instructions file per harness (rendered from `source_of_truth/baseline/baseline-instructions.md`), replacing only the five sentinel-delimited sections (`<!-- context7 -->`, `<!-- code-review-graph -->`, `<!-- phase-doc-sync -->`, `<!-- agent-discovery -->`, `<!-- know-the-audience -->`) and leaving user content outside sentinels untouched. `BASELINE_SECTIONS` must stay in sync with the template's sentinels — a test derives the expected set from the template.

Both stages are safe by construction: a destination file is only overwritten or pruned when it carries a generated marker (or lives inside a generated skill directory). Hand-placed files are skipped and reported under `skipped_paths`.

### Content model

- **Agents** (`source_of_truth/agents/`) — 64 definitions (16 user-invocable, 48 hidden) following an orchestrator + subagent pattern: user-invocable primary agents (planner → refiner → phase-execute pipeline, PR review, audits, test orchestrator, standalone specialists) plus hidden `user-invocable: false` subagents (deployed with a `z-` prefix) that orchestrators spawn. Full catalog: `USAGE.md`.
- Pipeline subagents carry an abstract `model_tier` of `low`, `medium`, or `high`. Exact harness model identifiers live only in `source_of_truth/config/model-routing.json`; user-invocable agents inherit the session model by omitting the field.
- **Skills** (`source_of_truth/skills/`) — directory-based capabilities, each rooted at `SKILL.md`, loaded on demand by agents. Skills are agent capabilities, never user commands: propagation injects `user-invocable: false` into the Claude and Cursor copies, which hides the skill from both slash menus while leaving its description in context so the model still auto-invokes it. Do not author the flag in source — it is a Claude/Cursor extension, not an Agent Skills spec field, and the source ships verbatim to Codex, OpenCode, and `.github/`. Authoring it explicitly overrides the injected default. Codex has no hide flag and lists skills under `/skills`; OpenCode and Copilot have no slash surface.
- **Instructions** (`source_of_truth/instructions/`) — cross-cutting guidance matched by `applyTo` globs. Agent-targeted instructions are inlined into the rendered agent body for every harness; source-file-glob instructions reach Cursor (`.mdc` rules) and Copilot (native) only.

**Skill or instruction?** Not a style choice. A skill is loaded once the agent knows what work it is doing; an instruction is inlined unconditionally, before the agent knows anything. The test is timing: **does this apply from the first turn, or only once the work is scoped?** `orchestrator-conventions` governs how an orchestrator spawns before any work exists, so it is an instruction; `auditor-conventions` governs a report the agent has already decided to write, so it is a skill. The second test is failure mode: if forgetting to load it produces the exact defect the content exists to prevent, it must be an instruction.

The three language files (`python`, `typescript`, `csharp`) are deliberately duplicated by their `*-standards` skills — the glob path serves Cursor and Copilot when a source file is open, the skill path serves the harnesses that inline into agents. Change both halves together; do not "deduplicate" them.

There is deliberately no learnings asset. Durable, repo-agnostic rules are skills. A working repository's own findings live in its `docs/learnings/`, written by the agents working there and never seeded from here. This repository's authoring and deployment failure modes are in [docs/AUTHORING.md](docs/AUTHORING.md) — read it before editing an agent definition.

**Brevity constraint on authored agent and skill definitions**: the agent and skill files written to `source_of_truth/` are loaded into model context at runtime — every unnecessary word is wasted context. Definitions must be terse: state the behavior, the constraints, and the output contract once each, and stop. No restating context the agent already has, no motivational preamble, no repeating a rule in different words, no exhaustive examples where one suffices. Carry this into every feature's AC: a definition that says the same thing twice fails review.

### Tests

`tests/` are regression tests over both scripts — they verify source↔generated sync, deploy safety (marker respect), naming conventions (aliases, `z-` prefixes), and per-harness invocation contracts. After editing `source_of_truth/`, sync tests fail until propagation runs — which the maintainer does manually (see "Agents: never run propagation"). Agents should report the pending propagation, not trigger it.

### Other areas

- `eval/` — past benchmark run artifacts; `eval/deprecated/` holds the archived eval-grader system (see `eval/deprecated/README.md`)
- `packages/com.threnjen.visual-verification/` — Unity UPM package paired with the Visual Verifier agent
- `docs/` — ARCHITECTURE, CODEBASE_CONTEXT, LOCAL_DEVELOPMENT, TROUBLESHOOTING, porting references; keep counts/paths in these aligned with README and CONTRIBUTING when editing docs
