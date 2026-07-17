# 01 Propagator Orphan Pruning — Tasks

**Status: complete.** All stages done; 426 passed, 15 subtests, stable across 3 runs.
See `01-propagator-orphan-pruning-implementation.md` for the four recorded decisions
(Option B, marker constant, test isolation, AC4b), the hand-maintained file inventory,
and two gaps: a pre-existing orphan (`claude/agents/single-feature.md`, deferred to
feature `08` per this feature's non-goals) and a stale `--watch` process needing restart.

Baseline before starting: `.venv/bin/python -m pytest tests/ -q` → 416 passed, 15 subtests passed.

> **Read the Discovery Delta in `-context.md` first.** The plan names a function
> (`propagate_agents_once`) that does not exist; the real entry point is
> `propagate_once` (`scripts/propagate_master_assets.py:1329`). Three further
> deltas change Stage 2 and Stage 3 scope.

## Stage 0: Test Prerequisites

**Status:** Not required. Baseline is 416 passed across 4 consecutive full runs (2026-07-16); `tests/test_propagate_master_assets.py` is 849 lines covering this module directly. Coverage is well above the 50% bar.

- [x] No action — prerequisite waived.

## Stage 1: Enumerate and Prove the Gap

**Goal:** A failing test that proves orphans survive, plus a written inventory of every non-generated file across the three roots.
**Success criteria:** New test fails for the right reason; hand-maintained file inventory recorded.

- [x] Reconcile the plan against the real API: confirm agent propagation lives inline in `propagate_once` (`:1329`) and record in the implementation notes that AC1/AC2/AC3/AC7/AC8 target `propagate_once`, not the non-existent `propagate_agents_once`.
- [x] **Decide the test-isolation strategy and record it.** `propagate_once` takes no `repo_root` and reads module constants (`CLAUDE_AGENTS_DIR` :38, `CLAUDE_COMMANDS_DIR` :39, `OPENCODE_AGENTS_DIR` :40, `CODEX_AGENTS_DIR` :41) bound to the real `REPO_ROOT` (:27) at import. Choose: (a) plumb a `repo_root` param through `propagate_once` mirroring `propagate_skills_once(repo_root=None)` (:1213), or (b) monkeypatch the constants per-test. The plan's claim that no new fixture machinery is needed is false for agent-side tests — resolve before writing any prune test.
- [x] Write a failing test: delete a source agent in an isolated repo, run propagation, assert its `claude/agents/` and `opencode/agents/` outputs are gone. Confirm it fails because the files survive, not because of a fixture error.
- [x] Enumerate every non-generated file across `claude/agents/`, `claude/commands/`, `claude/skills/`, `opencode/agents/`, `opencode/skills/`. Record the inventory in the implementation record. (Already verified: zero non-`.md` files in the three agent/command roots; `claude/agents/README.md` is the only `README*` inside a pruned root — the two skill roots remain unenumerated.)
- [x] Confirm the marker-absence baseline still holds: `claude/agents/` 0/35, `claude/commands/` 0/19, `opencode/agents/` 0/46, `claude/skills/` 0/24 SKILL.md, `opencode/skills/` 0/24 SKILL.md.

## Stage 2: Emit the Generated Marker

**Goal:** Add the marker to Claude/OpenCode agent, command, **and skill** rendering; verify one regenerated agent still parses before regenerating all roots.
**Success criteria:** Marker present in regenerated output; harness parsing verified against a real agent; full suite green.

- [x] **Choose the marker constant.** Do **not** reuse `GENERATED_AGENT_HEADER` (:51) verbatim — it is a bare `#` TOML comment and renders as an H1 heading in Markdown. `GENERATED_SKILL_HEADER` (:52) is already an HTML comment (`<!-- … -->`) and is the Markdown-safe precedent. Reuse it or mirror its form; record the choice and avoid a redundant third constant.
- [x] Add the marker to `render_claude_agent` (:527), placed immediately **after** the closing `---` of the YAML frontmatter, never above the opening `---`.
- [x] Add the marker to `render_claude_command` (:555), same placement rule.
- [x] Add the marker to `render_opencode_agent` (:597), same placement rule.
- [x] **Add the marker to Claude and OpenCode skill output** in `propagate_skills_once` (:1213), mirroring the Codex skill path that already prepends `GENERATED_SKILL_HEADER` (:1275). Without this, AC4 is unreachable — Claude/OpenCode `SKILL.md` files carry no marker (0/24 each).
- [x] **Verify the load-bearing assumption before mass regeneration:** regenerate exactly one Claude agent and one Claude command, then confirm the harness still parses the frontmatter and the agent behaves unchanged. If parsing breaks, stop and fall back to Option A (expected-set pruning with an explicit, tested exclusion list) — record the pivot.
- [x] Regenerate all three roots. Expect a large but mechanical diff touching every generated file.
- [x] Run the full suite; confirm green.

## Stage 3: Implement Guarded Pruning

**Goal:** One prune helper applied to `claude/agents/`, `claude/commands/`, `opencode/agents/`, and the two skill roots — strictly after emission.
**Success criteria:** AC1–AC6 tests pass, including the `README.md` survival test.

- [x] Implement one helper — `_prune_orphaned_outputs(directory, expected, marker)` `[PROPOSED - name TBD]` — mirroring the Codex prune shape at `:1409`: skip expected, verify the marker prefix, `unlink`, increment a counter. Do not write three sweep loops.
- [x] Refactor the two existing Codex prune loops (`:1409` agents, `:1417` profiles) to use the shared helper. Preserve their behavior exactly.
- [x] Accumulate `expected_claude_agent_files`, `expected_claude_command_files`, and `expected_opencode_files` sets during emission in `propagate_once`, mirroring the existing `expected_codex_files` / `expected_codex_profile_files` pattern.
- [x] **AC1:** Prune orphaned `claude/agents/*.md` — marker-bearing files with no corresponding source agent.
- [x] **AC2:** Prune orphaned `claude/commands/*.md` — marker-bearing files with no corresponding `user-invocable: true` source agent. Preserve the existing reclassification path at `:1383` that removes a subagent file when an agent flips to command-only.
- [x] **AC3:** Prune orphaned `opencode/agents/*.md`.
- [x] **AC4:** Prune orphaned skill directories in `claude/skills/` and `opencode/skills/`, mirroring the tested recursive removal for `codex/skills/` (:1293).
- [x] **AC6:** Place every prune call strictly after all emission completes. `_claude_filename_for` (:389) and `_opencode_filename_for` (:432) resolve names against on-disk stems via `_discover_existing_stems` (:376), so pruning early can silently rename a survivor.
- [x] Handle the failure modes: a missing generated root means nothing to prune (never create it to prune it); an unreadable file is not a confirmed orphan — fail closed, do not delete; do not recurse outside the skills path.
- [x] **Handle symlinked orphans.** Not in the plan's failure-mode table, but this module is deliberately symlink-hardened (`_write_if_changed` symlink test :56; hook-asset symlink tests :596, :622, :642) and `review-learnings.md:173,177` records the rule. Do not `unlink` through a symlink into a real tree.
- [x] **Test (AC1):** orphaned marker-bearing `claude/agents/` file with no source agent is deleted and counted.
- [x] **Test (AC5 — the critical one):** `claude/agents/README.md`, no marker, no matching source agent → still exists after propagation. This test must fail if the guard is removed.
- [x] **Test (AC6):** a surviving agent whose Claude stem (`z-artifact-sweeper.md`, verified present) also matches an orphan candidate keeps its stem; only the true orphan is removed. (`opencode/agents/05g-artifact-sweeper.md` also verified present.)
- [x] **Test (AC2):** a source agent flipped to `user-invocable: false` has its `claude/commands/` file deleted while its subagent file is retained.
- [x] **Test (AC4):** an orphaned skill directory is removed from `claude/skills/` and `opencode/skills/`.
- [x] Run the full suite; confirm green.

## Stage 4: Prove Inert, Then Report

**Goal:** Confirm a real-tree run deletes nothing (AC7); surface counts in the result dict and CLI summary (AC8).
**Success criteria:** `git status` clean after a real propagation run; counts present; full suite green across repeated runs.

- [x] **AC8:** Add an `"orphans_removed"` `[PROPOSED - name TBD]` count per root to the `propagate_once` result dict (:1429). Follow the `retired_hook_assets_removed` precedent — a distinct key, not folded into `changed_claude`/`changed_opencode`/`changed_codex`, which already conflate deletions with writes.
- [x] Confirm no separate CLI work is needed: the summary is `print(json.dumps(result, indent=2))` (:1444) under `if verbose:`, so a new result-dict key surfaces automatically. Do not add a second render site.
- [x] Update existing result-dict assertions in `tests/test_propagate_master_assets.py` (class `PropagateMasterAssetsTests`, :16) for the new counter keys.
- [x] **Test (AC7):** propagation against the real repository state deletes zero files.
- [x] **AC7 manual verification:** run a real propagation on a clean tree; confirm `git status` shows no deletions. If any file is deleted, fix the guard or surface the finding — do **not** add an exclusion until the count reaches zero.
- [x] Confirm no per-file logging was added on the normal path — a clean run stays silent, matching every other propagator counter.
- [x] Run the full suite repeatedly; confirm green and stable against the 416-passed baseline.

## Keep-it-clean checklist

- [x] One prune helper, not three copies
- [x] Prune strictly after emission in every path
- [x] No hardcoded filename denylist if Option B is taken
- [x] Counts reported, never silent
- [x] Marker constant reused, not duplicated
- [x] No agent, skill, or command deleted in this feature — capability only
- [x] Implementation record documents: the Option A/B choice, the final marker constant, the test-isolation strategy, and the hand-maintained file inventory
