# 01 Propagator Orphan Pruning — Context

## Key Files

### Files being changed

| File | Role | Change Type |
|---|---|---|
| `scripts/propagate_master_assets.py` | The propagator. Holds `propagate_once` (:1329), `propagate_skills_once` (:1213), the Codex prune loops (:1409, :1417), the skills prune loop (:1293), and the render functions for all three roots. | Modify |
| `tests/test_propagate_master_assets.py` | 849 lines, class `PropagateMasterAssetsTests` (:16). Direct coverage of this module. New prune tests land here; existing result-dict assertions gain counter keys. | Modify |

### Read-only reference

| File | Role | Why it matters |
|---|---|---|
| `claude/agents/README.md` | The one verified hand-maintained file inside a pruned root. | AC5's regression target. Verified present; no non-`.md` files exist in `claude/agents/`, `claude/commands/`, or `opencode/agents/`. |
| `claude/README.md`, `codex/README.md` | Hand-maintained, but live at root level — outside every pruned directory. | Not at risk; do not add to any exclusion logic. |
| `claude/agents/z-artifact-sweeper.md`, `opencode/agents/05g-artifact-sweeper.md` | Both verified present. | The AC6 ordering test case (plan test #4) depends on this stem pair existing. |
| `.github/learnings/cross-phase-decisions.md` | "Propagation Contracts" section. | Directly governs the marker decision — see Relevant Learnings. |

### Verified symbols (plan references confirmed accurate)

`GENERATED_AGENT_HEADER` (:51), `GENERATED_SKILL_HEADER` (:52), `_discover_existing_stems` (:376), `_choose_existing_stem` (:382), `_claude_filename_for` (:389), `_opencode_filename_for` (:432), `_remove_retired_hook_assets` (:982), `propagate_skills_once` (:1213), `propagate_learnings_once` (:1311), `propagate_once` (:1329), `main` (:1522).

## Discovery Delta

| Finding | Impact | Action |
|---|---|---|
| **`propagate_agents_once` does not exist.** Grep across `scripts/` and `tests/` for `agents_once` returns zero hits. Agent propagation is inline inside `propagate_once(verbose: bool = True)` (:1329), which then calls `propagate_skills_once()`, `propagate_learnings_once()`, and `propagate_hooks_once()`. | **Critical.** AC1, AC2, AC3, AC7, AC8 and test cases 1–5 all name a function that isn't there. The plan presents it as fact, unmarked. | **Update plan.** Rewrite ACs against `propagate_once`. Decompose-level warning — raised to Decomposer. |
| **`propagate_once` takes no `repo_root`.** It reads module-level constants (`CLAUDE_AGENTS_DIR` :38, `CLAUDE_COMMANDS_DIR` :39, `OPENCODE_AGENTS_DIR` :40, `CODEX_AGENTS_DIR` :41) bound to the real `REPO_ROOT` (:27) at import time. | **High.** Plan F asserts new tests "use the existing `tempfile.TemporaryDirectory(dir=REPO_ROOT)` fixture idiom … so no new fixture machinery is needed." That idiom works at test :68 **only because** `propagate_skills_once(repo_root)` accepts a root. Agent-side prune tests (cases 1, 2, 4, 5) cannot use a temp repo as written — they would prune the real tree. | **Add task.** Implementer must either plumb `repo_root` through `propagate_once` (unplanned refactor touching every module constant) or monkeypatch the constants. Decide and record in Stage 1. |
| **`GENERATED_AGENT_HEADER` is a TOML comment, not a Markdown-safe one.** Value: `# Generated from .github/agents source-of-truth. Do not edit manually.` It is safe in `codex/agents/*.toml`. In Markdown it renders as an **H1 heading** at the top of every agent body. | **High.** Plan C recommends reusing it "verbatim if it renders acceptably; a second constant is a smell." It does not render acceptably in Markdown. | **Update plan.** `GENERATED_SKILL_HEADER` (:52) is already an HTML comment (`<!-- … -->`) and is the correct Markdown-safe precedent to reuse or mirror. |
| **AC4 has a hidden prerequisite.** `claude/skills/**/SKILL.md` and `opencode/skills/**/SKILL.md` carry **no marker: 0 of 24 each**. Only `codex/skills/` gets `GENERATED_SKILL_HEADER` prepended (:1275). | **High.** AC4 says "matching the behavior already implemented for `codex/skills/`" — but the Claude/OpenCode skill roots have nothing to guard by either. Stage 2's goal names only "agent and command rendering" and omits skill rendering. | **Add task.** Stage 2 must also emit the marker into Claude/OpenCode skill output, or AC4 is unreachable. |
| **CLI summary needs no separate change.** The CLI path is `print(json.dumps(result, indent=2))` (:1444) under `if verbose:`. | Low — simplifies AC8. | **None.** AC8's "result dict and CLI summary" is one change. Don't hunt for a second render site. |
| **Existing prune counters conflate deletions with writes.** The Codex prune loops increment the same `changed_codex` / `changed_codex_profiles` the emission path increments. | Medium. Reinforces AC8's rationale — today a deletion is *already* invisible. Precedent for a distinct key exists: `retired_hook_assets_removed` in the result dict. | **None.** Plan's `"orphans_removed"` key aligns with the `retired_hook_assets_removed` precedent. Follow that naming shape. |
| **Symlink handling is absent from the failure-mode table.** This module is deliberately symlink-hardened: `_write_if_changed` replaces self-referential symlinks (test :56), and there are five hook-asset symlink tests (:596, :622, :642, :347, :364). `review-learnings.md:173,177` records the rule. | Medium. A pruner that `unlink`s an orphan that is a symlink into a real tree is exactly the class of bug this module already defends against elsewhere. | **Add task.** Extend the Stage 3 failure-mode handling with a symlink case. |
| **Line-number drift in plan citations.** Cited `:1405`→actual `:1409`; `:1413`→`:1417`; `:1288`→`:1293`; `:1291`→`:1296`. Cited `:982`, `:51`, `:69` are exact. | Cosmetic. The prune shape the plan describes is real and at the cited region. | **None.** Drift is ~4 lines; navigate by symbol. |
| Plan's marker-absence evidence: "0 of 35, 19, and 46 files." | **Verified exactly.** `claude/agents/` 0/35, `claude/commands/` 0/19, `opencode/agents/` 0/46. | None — claim confirmed. |
| Plan's "Unverified Assumption" that `claude/agents/README.md` may not be the only hand-maintained file. | Partially resolved: **zero non-`.md` files** exist across `claude/agents/`, `claude/commands/`, `opencode/agents/`; the only `README*` inside a pruned root is `claude/agents/README.md`. | **Accepted risk narrowed.** Still enumerate `claude/skills/`, `opencode/skills/` in Stage 1 as the plan requires. |
| No phase-scoped test directory pattern. `tests/` is flat (`test_propagate_master_assets.py`, `test_readiness_synthesis_agents.py`, `tests/hooks/`). | None. | **None.** No consolidated phase test file is expected here. |

## Architectural Decisions

- **Mirror the Codex prune shape, don't invent a second idiom.** Accumulate `expected_*_files` during emission, sweep the directory, skip expected, verify the marker, `unlink`, increment. This exists twice already (:1409, :1417) and once for skills (:1293).
- **Option B — emit a generated marker, then guard by it — over Option A (expected-set + denylist).** Rationale: a denylist rots silently as new hand-maintained files appear; a marker guard cannot. Option B also makes the three roots consistent, which is the underlying defect. Cost is a one-time mechanical regeneration across three roots. Fall back to A with a tested exclusion list only if the marker breaks harness parsing.
- **One generic `_prune_orphaned_outputs(directory, expected, marker)` helper `[PROPOSED - name TBD]`, not three sweep loops.** Factor on first repetition.
- **Prune strictly after all emission.** `_claude_filename_for` / `_opencode_filename_for` resolve names against stems already on disk via `_discover_existing_stems`, so deletion order is load-bearing (AC6).
- **No `--dry-run` flag.** Deliberately excluded: AC7 (inert run) plus AC8 (counts) deliver the same operator safety without a second code path that can drift.
- **Aggregate counts only; no per-file logging on the normal path.** A clean run stays silent, matching every other propagator counter. `git status` is the real audit trail.
- **Fail closed on unreadable files.** An unreadable file is not a confirmed orphan; do not delete it.

## Constraints

- **Do not delete any agent, skill, or command in this feature.** This feature adds capability only.
- **Never delete a file not positively identified as generated** (AC5). Deletable requires both: absent from the expected set **and** marker-bearing.
- Marker must sit **after** the closing `---` of YAML frontmatter, never above the opening `---`.
- Do not touch `claude/learnings/` or any hook output — `_remove_retired_hook_assets` (:982) already owns hook assets.
- Do not change identifier/alias resolution rules.
- A missing generated root means nothing to prune; never create a directory in order to prune it.
- Test runner is `.venv/bin/python -m pytest` — **system `python3` has no pytest.**

## Scope Boundaries

- `claude/agents/README.md` — must survive every run. The primary safety property.
- `claude/README.md`, `codex/README.md` — outside pruned roots; leave alone.
- `claude/learnings/` and all hook outputs — owned by `_remove_retired_hook_assets`.
- Identifier/alias resolution (`_claude_identifier_for`, `_codex_identifier_for`, `_choose_existing_stem`) — read and respect; do not modify.
- The existing Codex prune loops — mirror their shape; refactoring them into the shared helper is in scope, changing their behavior is not.
- `--watch` mode — out of scope; the watcher already requires a restart for propagator edits.
- No new secret handling, network, or shell execution.

## Relationships to Sibling Plans

- **Depends on nothing.** Wave 1, parallel safe. It is first because every later feature deletes or renames a source asset and would otherwise leave orphans.
- **Enables `02-retired-evaluator-removal`** — the first real consumer, and the feature that proves this one works end to end.
- **Enables `03-pr-review-conventions-skills`** — renaming a skill directory orphans the Claude and OpenCode skill dirs; only Codex self-prunes today.
- **Enables `04-pr-review-orchestrator`** — renaming the orchestrator orphans `claude/commands/phase-final-review.md`, which would otherwise stay a live, user-invocable slash command for a deleted agent.
- **Enables renumbering features `05`, `06`, `07`** — OpenCode filenames key on source slug, so `05g-artifact-sweeper` → `05c-artifact-sweeper` orphans `opencode/agents/05g-artifact-sweeper.md`. Claude filenames key on agent *name* and mostly survive a renumber. That asymmetry makes OpenCode orphans easy to miss by eye.

## Suggested Implementation Order

This is feature `01` and gates the rest of the phase. Within it, follow the plan's stage order strictly — Stage 2 (emit marker) **must** precede Stage 3 (guarded prune), because the guard has nothing to match until the marker exists. Stage 4's inert-run proof (AC7) is the gate before any sibling feature consumes this capability.

## Environment State

| Property | Value |
|---|---|
| Tech Stack | Python 3 stdlib (hooks/propagator); pytest for tests |
| Test Runner | `.venv/bin/python -m pytest tests/ -q` |
| Test Baseline | 416 passed, 15 subtests passed — captured 2026-07-16 across 4 consecutive full runs, all green |
| Lint | Not configured (verified — `pyproject.toml` contains only `[tool.pytest.ini_options]`) |
| Format | Not configured |
| pytest config | `pyproject.toml` → `[tool.pytest.ini_options]`, `testpaths = ["tests"]` |

**Note:** system `python3` has no pytest installed. Always invoke `.venv/bin/python`.

## Relevant Learnings

From `.github/learnings/cross-phase-decisions.md` — "Propagation Contracts":

> The current master-asset propagator's generated roots are `claude/`, `opencode/`, and `codex/`; `.claude/skills/` and `.claude/agents/` are not generated destinations. Future feature plans must name the actual roots.

> `$source` metadata is guaranteed for propagated hook JSON entries, not for generated skill Markdown or agent Markdown/TOML. Downstream checks must not require that metadata on non-hook assets without a corresponding propagator change.

This second entry is the strongest available support for Option B: it records — as a prior decision — that generated agent/skill Markdown carries **no** provenance metadata, and that adding a requirement for it means changing the propagator. That is exactly this feature's Stage 2.

From `.github/learnings/review-learnings.md`:

> Artifact propagators must validate resolved source assets and resolved destination directories against their declared roots before reading or writing; replacing only a symlinked leaf file is not sufficient. (:173)

> A symlinked parent directory can redirect generated files outside the consumer root … Both cases break isolation and can overwrite or disclose unrelated files. (:177)

> Propagation regression tests must cover every newly added agent output. (:291)

The symlink entries apply directly to a `unlink`-based pruner and back the Discovery Delta symlink finding above.

From `.github/learnings/cross-phase-decisions.md` (general discipline, applies to AC7):

> A fixed budget must never be relaxed to make a gate pass. … If a budget is genuinely unachievable, the honest outcome is an explicit user-approved AC change, not a quietly edited threshold.

AC7 ("a real-tree run deletes zero files") is this feature's equivalent gate. If it fails, the correct response is to fix the guard or surface the finding — not to add an exclusion until the count reaches zero.
