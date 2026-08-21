# Phase 1: Creative Writing Profile and Developmental Editor Toolkit

**Status**: Complete
**Depends on**: None (the profile gate mechanism it builds on is already merged on this branch)
**Estimated complexity**: Large
**Cross-references**: `/Users/jennywadkins/github_repos/copperforge/cf-app-crucible-harness-extension/creative-editor-toolkit-master-spec.md`

## What's New

A set of writing tools that live in this repo alongside the engineering agents but share nothing with them. You open a session in your Obsidian vault and get a developmental editor — one that interrogates and diagnoses your material without ever suggesting plot fixes or naming your characters. It cannot write to your canon or drafts, and that is not a promise it makes, it is a capability it does not have.

The technical corpus stays entirely out of these sessions. No Unity detection, no `dev/feature/` folders, no test-execution rules, no code-review graph.

## Objective

Deliver the corpus-native subset of the Creative Editor Toolkit spec — modes, compliance discipline, vault awareness, and pattern memory — using only guarantees this repo can actually enforce, and state plainly which of the spec's guarantees must wait for the standalone harness.

## Scope

### In Scope

- **Creative agent roster** (four agents, `creative-*` prefix, `profile: creative`):
  - `Creative - Developmental Editor` — user-invocable, `tools: [read, search, todo, agent]`. **No `edit`.**
  - `Creative - Scribe` — `tools: [read, edit]`. Sole holder of the write bit; appends to `_editor-notes/` and `scene-summaries/` only. Never reasons about the manuscript.
  - `Creative - Compliance Check` — `tools: [read]`. Scans a draft response against the active mode's rules.
  - `Creative - Vault Sync` — `tools: [execute]`. Resolves the vault's current git SHA, compares it to the one recorded in `context/index.md`, and returns the file-level diff. Read-only git subcommands only. **No `edit`.**
- **`creative-profile.instructions.md`** — `profile: creative`, `applyTo: **/creative-*.agent.md`. Carries the skill **allow-list** (load only the named creative skills; ignore every other catalog entry regardless of description match), the canon boundary, and the honest-limits statement.
- **Creative skills** (all `profile: creative`):
  - `creative-modes` — the six-mode gate (Interrogate, Reflect, Diagnose, Adversarial, Generate, Copyedit), permitted output per mode, delivery presets, mid-session switch commands, auto-exit from Generate, and the interpretive layer that sits across every mode and is off by default.
  - `creative-compliance` — per-mode violation rules plus three cross-mode ones (unrequested interpretation, prose that reads as generated, reading level in restatement), shared by the editor's inline self-check and the compliance agent.
  - `creative-vault` — vault detection, canon/notes boundary, session-log and `user-patterns.md` formats, scene-summary rollups, macro/micro zoom.
  - `creative-question-banks` — worldbuilding, plot, character, pacing, theme.
- **Baseline trim** (separable workstream) — remove the `context7` and `code-review-graph` **instruction sections** from `BASELINE_SECTIONS` (`deploy_agents.py:44`), and list them in `RETIRED_BASELINE_SECTIONS` so the blocks a previous deploy already wrote are deleted rather than left stale and from `source_of_truth/baseline/baseline-instructions.md`. Keep `phase-doc-sync`, `agent-discovery`, `know-the-audience`. The companion-tool bootstrap is deliberately untouched: `ensure_code_review_graph` (`deploy_agents.py:333`), `ensure_context7` (`deploy_agents.py:358`), their registration at lines 383-384, and the `--skip-tools` flag at line 503 all keep working exactly as they do now. A repository-local rule can only be honored if the tool it names is installed, so removing the global rule must not remove the tool.
- **Corpus guard tests** — derived, not enumerated: no `creative-*` agent except the scribe grants `edit`; the allow-list covers every creative skill on disk; creative instructions reach only creative agents.
- **Canon guard hook** — `source_of_truth/hooks/creative-canon-guard.py`, a `PreToolUse` hook the writer installs into their own vault's `.claude/`. Denies every write into `canon/` and `drafts/` from any tool, including a shell command that would reach them. Fails closed on an unreadable payload. This is what makes the canon boundary an enforcement rather than a promise, which matters because generated text carries provenance watermarking: one agent write into a manuscript can mark the writer's own prose as machine-authored with nothing visible afterward. Mirrors verbatim to `ports/github/hooks/` and `.github/hooks/` through the existing hook pipeline.
- **`docs/CREATIVE_TOOLKIT.md`** — the hard/soft guarantee table, vault setup, mode reference, and the hook's install steps.

### Out of Scope

- The standalone OpenCode-forked harness. Not built here, not started here.
- Multi-provider BYOK, per-role model assignment, API-key configuration — all harness concerns.
- Path-scoped filesystem permissions. This corpus grants tools all-or-nothing.
- A forced compliance pass. No agent definition can compel a subagent call every turn.
- Line editing as a primary purpose. Copyedit exists as a bounded mode, nothing more.
- Removing the stray `/Users/jennywadkins/CLAUDE.md`. Flagged, not this repository's file.
- Uninstalling or un-registering the Context7 and code-review-graph MCP servers. The trim removes instruction text, never tooling.

## Key Deliverables

| # | Deliverable | Description | Likely Features |
|---|-------------|-------------|-----------------|
| 1 | Creative agent roster | Three `creative-*.agent.md` under `profile: creative` | Agent authoring, tool grants |
| 2 | Profile instruction | Allow-list, canon boundary, honest limits | Instruction authoring |
| 3 | Creative skills | Four skills: modes, compliance, vault, question banks | Skill authoring |
| 4 | Baseline trim | Two sections cut from the global baseline | `deploy_agents.py`, baseline template |
| 5 | Guard tests | Derived structural tests over the creative family | `tests/` |
| 6 | User documentation | Guarantee table, vault setup, mode reference | `docs/` |

## Technical Context

- **Profile gate** — `scripts/propagate_master_assets.py:538` (`applicable_instructions`). Already merged on this branch. `DEFAULT_PROFILE` is implicit; `profile: creative` is the only opt-in token. Instruction bodies are inlined as literal text at propagation time, so isolation holds on every harness with no per-harness feature involved.
- **Flat agent glob** — `SOT_AGENTS_DIR.glob("*.md")` at `scripts/propagate_master_assets.py:477` does not recurse. The creative family is a filename prefix, not a subdirectory.
- **Forced `Skill` tool** — `map_tools_for_claude` (`scripts/propagate_master_assets.py:591`) hardcodes `Skill` at line 592 into every Claude agent. This is why skill isolation is an allow-list in prose rather than a tool grant, and why it stays soft.
- **Cursor rules** — `propagate_cursor_rules_once` already skips non-technical docs unconditionally, so a creative instruction can never deploy as a user-global Cursor rule.
- **Claude emission rule** (`docs/CODEBASE_CONTEXT.md:118-121`) — a user-invocable agent emits a slash command under `ports/claude/commands/`, and an agent file only when an orchestrator names it as a child. Hidden subagents emit under `ports/claude/agents/` renamed `z-*`. So the editor lands at `ports/claude/commands/creative-developmental-editor.md`; the scribe and compliance agents land at `ports/claude/agents/z-creative-scribe.md` and `ports/claude/agents/z-creative-compliance-check.md`.
- **Baseline splice** — `BASELINE_SECTIONS` (`deploy_agents.py:44`), spliced between sentinels into `~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, and a Cursor always-apply rule.

## Dependencies & Risks

- **Dependency**: profile gate — merged, tested (6 tests), propagation still pending on this branch.
- **Risk — the allow-list is prose, not a gate.** A technical skill whose description matches a creative prompt can still surface. *Mitigation*: allow-list phrased as "load only these, ignore all others regardless of match"; a guard test keeps it in sync with the skills on disk; `docs/CREATIVE_TOOLKIT.md` states this is soft.
- **Risk — the compliance pass cannot be forced.** *Mitigation*: inline mandatory self-check in the editor body **plus** the compliance subagent for substantive responses. Two soft layers, honestly labeled.
- **Risk — the scribe holds `edit` with no path scoping.** *Mitigation*: keep its body minimal and auditable, forbid manuscript reasoning, restrict it to append-only operations under `_editor-notes/` and `scene-summaries/`. Documented as the toolkit's one genuine write surface.
- **Risk — baseline trim degrades technical work.** Removing `context7` and `code-review-graph` globally means repositories wanting them must carry them locally, including this one. *Mitigation*: ship the trim with the replacement rules added to this repository's `AGENTS.md` in the same change. They go in `AGENTS.md`, not `CLAUDE.md` — the committed `CLAUDE.md` exists solely as a pointer and forbids restating `AGENTS.md` content, so duplicating rules there would violate its own contract.
- **Risk — vault detection guesses wrong.** *Mitigation*: walk up from the working directory for `.obsidian/`; on no match, ask for the path and never assume; on a match without a `canon/` directory, ask before treating anything as canon.

## Success Criteria

- [ ] `ports/claude/commands/creative-developmental-editor.md` exists, and `grep -c "Unity\|dev/feature\|code-review-graph"` against it returns `0`. Apply the same two checks to `ports/claude/agents/z-creative-scribe.md` and `ports/claude/agents/z-creative-compliance-check.md`. File existence is asserted first: `grep -c` on a missing file errors rather than returning `0`.
- [ ] No generated `creative-*` agent except the scribe lists `Edit` or `Write` in its tools, on any of the five ports.
- [ ] A creative session asked to write into `canon/` reports a missing capability, not a policy refusal.
- [ ] Each of the six modes has explicitly enumerated permitted output and at least one worked violation example.
- [ ] Generate mode returns to the prior mode automatically after one scoped answer.
- [ ] Vault detection resolves from a working directory inside a vault, and asks rather than guessing outside one.
- [ ] `creative-compliance` states, for each of the six modes, what counts as a violation and what the repair action is, and the compliance agent and the editor's inline self-check both cite it as their single source rather than restating the rules.
- [ ] `creative-question-banks` covers all five named areas — worldbuilding, plot, character, pacing, theme — and every question in it is answerable only by the writer, introducing no content of its own.
- [ ] `~/.claude/CLAUDE.md` contains no Context7 or code-review-graph section after deploy; the `phase-doc-sync`, `agent-discovery`, and `know-the-audience` sections survive intact, as does all content outside the splice sentinels.
- [ ] `deploy_agents.py` still installs and configures both companion tools after the trim, and `--skip-tools` still suppresses both.
- [ ] Guard tests derive their coverage from disk — adding a creative skill without allow-listing it fails a test.
- [ ] `docs/CREATIVE_TOOLKIT.md` states, per guarantee, whether it is hard or soft and why, and gives copy-paste install steps for the canon guard hook.
- [ ] The canon guard denies `Write`, `Edit`, and shell writes into `canon/` and `drafts/`, allows writes under `_editor-notes/` and `scene-summaries/`, allows every read of the manuscript, and denies an unreadable payload. Asserted by running the hook, not by reading its source.
- [ ] `_editor-notes/context/` is a directory of one file per content type — index, characters, setting, plot, scenes, style, open questions — and a change that touches one leaves the others unwritten.
- [ ] A vault holding the older single-file `_editor-notes/project-context.md` stays fully editable — the scribe accepts `replace` on it — and the editor offers a split rather than requiring one.
- [ ] `context/index.md` is the single file loaded on session trigger, holds one row per context file naming what it holds and when it was last written, carries no content of its own, and is updated in the same action as any file it points at.
- [ ] `_editor-notes/context/index.md` carries a `git_sha` trailer, and the editor's first session action is a sync against it, at the start of the conversation rather than the end.
- [ ] The interpretive layer is off by default in every session, has explicit on and off commands, does not persist across sessions, and is a named violation class in `creative-compliance` that covers offering and hinting as well as stating.
- [ ] `creative-compliance` names the prose tells that mark text as machine-written and gives the repair, and the rule covers `_editor-notes/` as well as Generate and Copyedit.
- [ ] `creative-compliance` states the reading-level floor for restatement with a worked example, and `creative-vault` carries the full rule.
- [ ] No `creative-*` agent except the vault-sync probe holds `execute`, and the probe holds no `edit`.

## QA Considerations

No UI. QA is structural (generated-output assertions over `ports/`) plus manual: a real writing session against a real vault, checking session logs for unrequested creative suggestions, per spec section 15.

Guard tests must be mutation-checked — a prose allow-list is exactly the assertion shape that goes inert on a reword. Load `guard-integrity` when writing them.

## Notes for Feature - Decomposer

Suggested boundaries, roughly in dependency order:

1. **Profile instruction + allow-list + guard tests** — nothing else works isolated without it.
2. **Creative skills** — four skills, no agent dependency; the largest authoring block, splittable if needed.
3. **Agent roster** — depends on 1 and 2; the three agents are one feature, since their tool-grant asymmetry is the point.
4. **Baseline trim** — fully independent, no ordering constraint.
5. **Documentation** — last, once the guarantee table reflects what shipped.

Keep the scribe's authoring separate in review even inside feature 3. It is the only creative asset that can modify a file, and it deserves scrutiny disproportionate to its size.
