# Phase 1: Creative Writing Profile and Developmental Editor Toolkit

**Status**: Planned
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

- **Creative agent roster** (three agents, `creative-*` prefix, `profile: creative`):
  - `Creative - Developmental Editor` — user-invocable, `tools: [read, search, todo, agent]`. **No `edit`.**
  - `Creative - Scribe` — `tools: [read, edit]`. Sole holder of the write bit; appends to `_editor-notes/` and `scene-summaries/` only. Never reasons about the manuscript.
  - `Creative - Compliance Check` — `tools: [read]`. Scans a draft response against the active mode's rules.
- **`creative-profile.instructions.md`** — `profile: creative`, `applyTo: **/creative-*.agent.md`. Carries the skill **allow-list** (load only the named creative skills; ignore every other catalog entry regardless of description match), the canon boundary, and the honest-limits statement.
- **Creative skills** (all `profile: creative`):
  - `creative-modes` — the six-mode gate (Interrogate, Reflect, Diagnose, Adversarial, Generate, Copyedit), permitted output per mode, delivery presets, mid-session switch commands, auto-exit from Generate.
  - `creative-compliance` — per-mode violation rules, shared by the editor's inline self-check and the compliance agent.
  - `creative-vault` — vault detection, canon/notes boundary, session-log and `user-patterns.md` formats, scene-summary rollups, macro/micro zoom.
  - `creative-question-banks` — worldbuilding, plot, character, pacing, theme.
- **Baseline trim** (separable workstream) — remove `context7` and `code-review-graph` from `BASELINE_SECTIONS` in `deploy_agents.py:44` and from `source_of_truth/baseline/baseline-instructions.md`. Keep `phase-doc-sync`, `agent-discovery`, `know-the-audience`.
- **Corpus guard tests** — derived, not enumerated: no `creative-*` agent except the scribe grants `edit`; the allow-list covers every creative skill on disk; creative instructions reach only creative agents.
- **`docs/CREATIVE_TOOLKIT.md`** — the hard/soft guarantee table, vault setup, mode reference.

### Out of Scope

- The standalone OpenCode-forked harness. Not built here, not started here.
- Multi-provider BYOK, per-role model assignment, API-key configuration — all harness concerns.
- Path-scoped filesystem permissions. This corpus grants tools all-or-nothing.
- A forced compliance pass. No agent definition can compel a subagent call every turn.
- Line editing as a primary purpose. Copyedit exists as a bounded mode, nothing more.
- Removing the stray `/Users/jennywadkins/CLAUDE.md`. Flagged, not this repository's file.

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

- **Profile gate** — `scripts/propagate_master_assets.py:506` (`applicable_instructions`). Already merged on this branch. `DEFAULT_PROFILE` is implicit; `profile: creative` is the only opt-in token. Instruction bodies are inlined as literal text at propagation time, so isolation holds on every harness with no per-harness feature involved.
- **Flat agent glob** — `SOT_AGENTS_DIR.glob("*.md")` at line 448 does not recurse. The creative family is a filename prefix, not a subdirectory.
- **Forced `Skill` tool** — `map_tools_for_claude:556` hardcodes `Skill` into every Claude agent. This is why skill isolation is an allow-list in prose rather than a tool grant, and why it stays soft.
- **Cursor rules** — `propagate_cursor_rules_once` already skips non-technical docs unconditionally, so a creative instruction can never deploy as a user-global Cursor rule.
- **Baseline splice** — `deploy_agents.py:44`, `BASELINE_SECTIONS`, spliced between sentinels into `~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, and a Cursor always-apply rule.

## Dependencies & Risks

- **Dependency**: profile gate — merged, tested (6 tests), propagation still pending on this branch.
- **Risk — the allow-list is prose, not a gate.** A technical skill whose description matches a creative prompt can still surface. *Mitigation*: allow-list phrased as "load only these, ignore all others regardless of match"; a guard test keeps it in sync with the skills on disk; `docs/CREATIVE_TOOLKIT.md` states this is soft.
- **Risk — the compliance pass cannot be forced.** *Mitigation*: inline mandatory self-check in the editor body **plus** the compliance subagent for substantive responses. Two soft layers, honestly labeled.
- **Risk — the scribe holds `edit` with no path scoping.** *Mitigation*: keep its body minimal and auditable, forbid manuscript reasoning, restrict it to append-only operations under `_editor-notes/` and `scene-summaries/`. Documented as the toolkit's one genuine write surface.
- **Risk — baseline trim degrades technical work.** Removing `context7` and `code-review-graph` globally means repositories wanting them must carry them locally, including this one. *Mitigation*: ship the trim with the replacement rules added to this repository's `CLAUDE.md` in the same change.
- **Risk — vault detection guesses wrong.** *Mitigation*: walk up from the working directory for `.obsidian/`; on no match, ask for the path and never assume; on a match without a `canon/` directory, ask before treating anything as canon.

## Success Criteria

- [ ] `grep -c "Unity\|dev/feature\|code-review-graph" ports/claude/agents/creative-developmental-editor.md` returns `0`.
- [ ] No generated `creative-*` agent except the scribe lists `Edit` or `Write` in its tools, on any of the five ports.
- [ ] A creative session asked to write into `canon/` reports a missing capability, not a policy refusal.
- [ ] Each of the six modes has explicitly enumerated permitted output and at least one worked violation example.
- [ ] Generate mode returns to the prior mode automatically after one scoped answer.
- [ ] Vault detection resolves from a working directory inside a vault, and asks rather than guessing outside one.
- [ ] `~/.claude/CLAUDE.md` contains no Context7 or code-review-graph section after deploy; the other three survive intact.
- [ ] Guard tests derive their coverage from disk — adding a creative skill without allow-listing it fails a test.
- [ ] `docs/CREATIVE_TOOLKIT.md` states, per guarantee, whether it is hard or soft and why.

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
