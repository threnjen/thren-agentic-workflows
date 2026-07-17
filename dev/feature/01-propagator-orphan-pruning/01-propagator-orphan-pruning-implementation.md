# Implementation Record: 01 Propagator Orphan Pruning

## Summary

The propagator now removes generated outputs whose source asset no longer exists,
across all eight pruned roots (`claude/agents`, `claude/commands`, `opencode/agents`,
`codex/agents`, `codex/profiles`, and the three `*/skills` roots). Before this change
only Codex agents and profiles were pruned; the `codex/skills` prune existed but had
never once fired.

Four decisions the plan left open, all resolved and recorded below:

1. **Option B (emit a marker, guard by it)** over Option A (expected-set + denylist).
2. **Marker constant**: one new `GENERATED_AGENT_MARKDOWN_HEADER`; `GENERATED_SKILL_HEADER`
   reused verbatim for the skill roots. No third constant.
3. **Test isolation (AC9)**: `repo_root` plumbed through `propagate_once`, not monkeypatching.
4. **AC4b superseded**: skill roots are marker-guarded rather than directory-name-only.

The load-bearing assumption (a marker can sit below the closing `---` without breaking
harness parsing) was verified against one real agent and one real command before the mass
regeneration. The regeneration is exactly **146 files, 146 lines added, 0 removed** — one
marker line each, zero content change.

`propagate_master_assets.py:1288` (the dead guard) is fixed and now proven live by test.

## Sibling Features

Read the first 5 lines of each sibling plan. This is feature `01`, wave 1, depends on nothing,
and gates every later wave. No sibling files were modified.

| Sibling | Relationship |
|---|---|
| `02-retired-evaluator-removal` (wave 2) | First real consumer. **Verified ready**: all five retired evaluators' Claude/OpenCode outputs now carry the marker and sit in the expected set, so deleting their source agents will prune them. Evidence below. |
| `03-pr-review-conventions-skills` (wave 3) | Skill renames now prune in all three skill roots (previously zero). |
| `04-pr-review-orchestrator` (wave 4) | `claude/commands/` pruning added, so a renamed orchestrator no longer leaves a live slash command. |
| `05`, `06`, `07` (waves 5–6) | OpenCode agent pruning added; renumbered slugs orphan `opencode/agents/*.md`, now swept. |
| `08-retirement-reconciliation` (wave 7) | **Owns the one gap this feature found** — see Gaps: `claude/agents/single-feature.md`. |

**Shared module**: `scripts/propagate_master_assets.py` is touched by every sibling that adds
or removes a source asset. This feature changed its public surface — `propagate_once`,
`load_source_agents`, and `load_instruction_docs` each gained an optional `repo_root`
parameter (all backwards compatible, default `REPO_ROOT`), and the result dict gained six keys.

## AC Coverage Matrix

| AC | Criterion ID | Planned Test ID | Planned Test Pattern | Status | Implementing Files | Evidence Paths | Implement Commit SHA | Review Commit SHA |
|----|--------------|-----------------|----------------------|--------|--------------------|----------------|----------------------|-------------------|
| AC1 | Prune orphaned `claude/agents/` + report count | Plan test 1 | Orphaned marker-bearing Claude agent is removed and counted | Done | `scripts/propagate_master_assets.py:1533` | `tests/test_propagate_master_assets.py::OrphanPruningTests::test_orphaned_claude_and_opencode_agents_are_pruned` | PENDING | PENDING |
| AC2 | Prune orphaned `claude/commands/` | Plan test 5 | Agent flipped to `user-invocable: false` loses its command file, keeps subagent file | Done | `scripts/propagate_master_assets.py:1536` | `tests/test_propagate_master_assets.py::OrphanPruningTests::test_orphaned_command_is_pruned_and_subagent_file_retained` | PENDING | PENDING |
| AC3 | Prune orphaned `opencode/agents/` | Plan test 1 | Orphaned OpenCode agent is removed | Done | `scripts/propagate_master_assets.py:1539` | `tests/test_propagate_master_assets.py::OrphanPruningTests::test_orphaned_claude_and_opencode_agents_are_pruned` | PENDING | PENDING |
| AC4a | Repair the dead `codex/skills` guard | (new) | Orphaned codex skill dir is actually removed | Done | `_is_generated_output` `scripts/propagate_master_assets.py:189` | `tests/test_propagate_master_assets.py::OrphanPruningTests::test_orphaned_skill_directories_are_pruned_in_all_three_roots` | PENDING | PENDING |
| AC4b | Prune `claude/skills` + `opencode/skills` | (new) | Orphaned skill dir removed from all three roots | Done | `_prune_orphaned_skill_dirs` `:229`; `propagate_skills_once:1414` | same test as AC4a | PENDING | PENDING |
| AC5 | No pruner deletes a file it did not generate | Plan test 2 | `claude/agents/README.md` survives every run | Done | `_prune_orphaned_outputs` `:206` | `::test_hand_maintained_file_in_generated_root_survives`; `::test_unmarked_skill_directory_survives`; `::test_unreadable_orphan_is_not_deleted`; `::test_symlinked_orphan_is_not_unlinked` | PENDING | PENDING |
| AC6 | Pruning never changes a survivor's identifier | Plan test 4 | Survivor keeps `z-artifact-sweeper` stem; only true orphan removed | Done | `scripts/propagate_master_assets.py:1530-1545` (prune strictly after emission loop) | `tests/test_propagate_master_assets.py::OrphanPruningTests::test_emission_completes_before_pruning` | PENDING | PENDING |
| AC7 | Real-repo run deletes zero files | Plan test 3 | Propagation on the unmodified tree removes nothing | Done | whole-run behavior | `::test_real_repository_propagation_removes_nothing`; manual: two consecutive `--once` runs, `git status` shows 0 deletions | PENDING | PENDING |
| AC8 | Counts in result dict + CLI summary | Existing test update | Result dict carries the new counter keys | Done | `scripts/propagate_master_assets.py:1576-1586` | `::test_real_repository_propagation_removes_nothing` asserts all six keys; CLI is `print(json.dumps(result))` | PENDING | PENDING |
| AC9 | Agent-side pruning testable without touching the real tree | (new) | Every prune test runs against a temp repo | Done | `propagate_once(verbose, repo_root)` `:1448` | All 9 isolated tests in `OrphanPruningTests` pass `repo_root=` | PENDING | PENDING |

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | Remove orphaned `claude/agents/` files; report count | Done | `scripts/propagate_master_assets.py` | Key `claude_orphans_removed`. |
| AC2 | Remove orphaned `claude/commands/` files | Done | `scripts/propagate_master_assets.py` | Key `claude_command_orphans_removed`. Existing reclassification path at `:1515` preserved untouched. |
| AC3 | Remove orphaned `opencode/agents/` files | Done | `scripts/propagate_master_assets.py` | Key `opencode_orphans_removed`. |
| AC4a | Repair `codex/skills` guard so it actually matches | Done | `scripts/propagate_master_assets.py` | Guard changed from `startswith` to whole-line containment. Guard **repaired, not deleted** — the marker requirement is intact. Was 0/24 matching; now 24/24. |
| AC4b | `claude/skills` + `opencode/skills` gain pruning | Done | `scripts/propagate_master_assets.py` | **Deviation**: implemented marker-guarded, not directory-name-only. See Deviations. |
| AC5 | No pruner deletes a file it did not generate | Done | `scripts/propagate_master_assets.py` | Mutation-tested: removing the guard makes 3 tests fail. See Reviewer Focus. |
| AC6 | Pruning never changes a survivor's identifier | Done | `scripts/propagate_master_assets.py` | All five prunes sit after the emission loop; skills prune after the skills loop. |
| AC7 | Real-repo run deletes zero files | Done | whole-run behavior | Verified by test **and** manually across two runs. Enumeration below proves why. |
| AC8 | Counts surface in result dict + CLI | Done | `scripts/propagate_master_assets.py` | Six distinct keys. No separate CLI work needed (confirmed: `:1444` prints the dict). |
| AC9 | Agent-side pruning testable in isolation | Done | `scripts/propagate_master_assets.py` | `repo_root` plumbed. See Decisions. |

## Decisions (required by the tasks checklist)

### 1. Option A vs Option B → **Option B** (emit marker, guard by it)

Taken as the plan recommends. The load-bearing assumption was verified *before* the mass
regeneration, exactly as instructed: one real agent (`05g-artifact-sweeper`) and one real
command were rendered and re-parsed. `_parse_frontmatter` returned identical keys with the
marker present, and the marker landed below the closing `---` as an HTML comment (invisible
when rendered). No fallback to Option A was needed.

Result: **no hardcoded filename denylist exists anywhere in this change.**

### 2. Marker constant → one new constant, `GENERATED_SKILL_HEADER` reused

| Root | Marker | Rationale |
|---|---|---|
| `claude/agents`, `claude/commands`, `opencode/agents` | **`GENERATED_AGENT_MARKDOWN_HEADER`** (new, `:52`) | `GENERATED_AGENT_HEADER` is a TOML comment and renders as an H1 in Markdown — not reusable. Mirrors `GENERATED_SKILL_HEADER`'s HTML-comment form but names the correct source root (`.github/agents`). |
| `claude/skills`, `opencode/skills`, `codex/skills` | `GENERATED_SKILL_HEADER` (existing, reused verbatim) | Source root really is `.github/skills`. No new constant. |
| `codex/agents`, `codex/profiles` | `GENERATED_AGENT_HEADER` (existing, unchanged) | TOML output; correct as-is. |

Named `GENERATED_AGENT_MARKDOWN_HEADER` rather than the plan's `[PROPOSED - name TBD]`
`GENERATED_MARKDOWN_HEADER`, because `GENERATED_SKILL_HEADER` is *also* Markdown — the
distinction is the source root, not the format.

### 3. Test isolation (AC9) → **plumb `repo_root`**, not monkeypatch

`propagate_once` gained `repo_root: Path | None = None`, mirroring the idiom **already used by
`propagate_skills_once`, `propagate_learnings_once`, and `propagate_hooks_once`** — three of its
four sibling functions. `load_source_agents` and `load_instruction_docs` gained the same
parameter (they read `GITHUB_AGENTS_DIR` / `REPO_ROOT` directly). Monkeypatching would leave
isolation incidental and per-test; plumbing makes it explicit and impossible to forget.

`load_source_agents` also now derives `rel_path` from the passed root, so `applicable_instructions`
glob patterns resolve correctly in a temp repo rather than against a `tmpXXXX/`-prefixed path.

**This was not theoretical.** During mutation testing of the AC5 guard, the AC7 test — which by
design runs against the real repository — executed with the guard disabled and deleted
`claude/agents/README.md` and `claude/agents/single-feature.md` from the working tree. Both were
restored via `git checkout` (the plan's documented rollback). That is precisely the hazard AC9
exists to prevent, and it confirms the plan's warning was not paranoia.

### 4. AC4b → **marker-guarded, superseding directory-name-only**

See Deviations.

## Hand-maintained file inventory (Stage 1 requirement)

Enumerated programmatically by rebuilding each expected set and diffing against disk. **All
eight pruned roots** — the plan only required the two unenumerated skill roots, but the
expected-set reconstruction covered every root at no extra cost.

| Root | Files/dirs | Unexpected | Detail |
|---|---|---|---|
| `claude/agents` | 35 | **2** | `README.md` [unmarked], `single-feature.md` [unmarked] |
| `claude/commands` | 19 | 0 | — |
| `opencode/agents` | 46 | 0 | — |
| `codex/agents` | 46 | 0 | — |
| `codex/profiles` | 19 | 0 | — |
| `claude/skills` | 24 | 0 | — |
| `opencode/skills` | 24 | 0 | — |
| `codex/skills` | 24 | 0 | — |

Also verified: **zero symlinks** anywhere under `claude/`, `opencode/`, `codex/`; zero non-`.md`
files in the agent/command roots; every skill dir has a `SKILL.md`.

Both unexpected files are unmarked, so both survive the guard — this is *why* AC7 holds.
`README.md` is genuinely hand-maintained. `single-feature.md` is **not** — it is a stale orphan
(see Gaps). The plan's "unverified assumption" that `README.md` was the only hand-maintained file
is therefore **confirmed**, but only because the second file turned out to be an orphan rather
than a hand-maintained file.

### Marker-absence baseline (confirmed before the change)

`claude/agents` 0/35, `claude/commands` 0/19, `opencode/agents` 0/46, `claude/skills` 0/24,
`opencode/skills` 0/24 — all exactly as the plan documented. `codex/skills` 24/24 *contain* the
marker but 0/24 matched `startswith`, which is the AC4a bug, reproduced and confirmed directly.

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `scripts/propagate_master_assets.py` | Modify | Added `GENERATED_AGENT_MARKDOWN_HEADER`; added `_with_generated_marker`, `_is_generated_output`, `_prune_orphaned_outputs`, `_prune_orphaned_skill_dirs`; emitted the marker from the three Markdown renderers and the two skill copy paths; accumulated three new expected sets; replaced the two Codex prune loops and the dead skills loop with the shared helpers; plumbed `repo_root` through `propagate_once`/`load_source_agents`/`load_instruction_docs`; added six result keys. | AC1–AC9. |
| `claude/agents/*.md` (33) | Modify (generated) | +1 marker line each | Stage 2 regeneration. |
| `claude/commands/*.md` (19) | Modify (generated) | +1 marker line each | Stage 2 regeneration. |
| `claude/skills/*/SKILL.md` (24) | Modify (generated) | +1 marker line each | AC4b prerequisite. |
| `opencode/agents/*.md` (46) | Modify (generated) | +1 marker line each | Stage 2 regeneration. |
| `opencode/skills/*/SKILL.md` (24) | Modify (generated) | +1 marker line each | AC4b prerequisite. |

`codex/` outputs are unchanged (0 files) — they already carried their markers.
Generated-file totals: **146 files, +146 / −0 lines.** No content changed.

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| `tests/test_propagate_master_assets.py` | Modify | Added class `OrphanPruningTests` (10 tests) with `_write_source_agent` / `_write_source_skill` fixture helpers. | AC1–AC9 |

No existing test needed its result-dict assertions updated: the new keys are additive and no
existing test asserts on the full dict. The planned "existing tests to update" item was therefore
a no-op — recorded rather than silently skipped.

## Test Results

- **Baseline**: 416 passed, 15 subtests passed (matches the documented baseline).
- **Final**: **426 passed, 15 subtests passed** — stable across 3 consecutive full runs.
- **New tests added**: 10
- **Regressions**: None.

### Pre-existing failure, not caused by this feature

The **first** baseline run showed `1 failed, 415 passed` —
`tests/hooks/test_hook_distribution_integration.py::test_ac9_propagated_guard_median_latency_is_below_50_ms`
(median 107 ms vs a 50 ms budget). It failed 4 consecutive times under load, then passed on every
subsequent run including all final runs. It is a **load-sensitive performance gate** measuring
subprocess/interpreter startup, is untouched by this feature (which adds no code to the hook path),
and is unrelated to propagation. Per the learnings note that a budget must never be relaxed to make
a gate pass, **no threshold was changed**. Flagged for visibility only.

## Deviations from Plan

1. **AC4b implemented marker-guarded, not directory-name-only.** AC4b specifies that skill pruning
   "must key on **directory-name expectation**" because "a marker guard is unavailable" for
   `claude/skills` / `opencode/skills`. That premise is dissolved by the tasks file's own Stage 2
   requirement to emit the marker into those roots (which AC4 is otherwise unreachable without).
   Once the marker exists, a marker guard *is* available, so I applied the same two-condition rule
   (absent from expected set **AND** marker-bearing) uniformly to all three skill roots. This is
   **strictly safer** than AC4b's rule, satisfies AC5's "no pruner deletes a file it did not
   generate" for the skill roots too, and removes the asymmetry the plan itself calls "the deeper
   problem". Covered by `test_unmarked_skill_directory_survives`, which AC4b's design would fail.

2. **Orphan counts are *not* folded into the `changed_*` counters.** Task 47 says preserve the
   Codex loops' behavior "exactly", but AC8 and the Discovery Delta both call the existing
   conflation of deletions with writes a defect. I read "exactly" as governing *which files get
   deleted* (the guard semantics), not the bookkeeping AC8 exists to fix. Deletions now report on
   six dedicated keys only, per the `retired_hook_assets_removed` precedent. Net effect:
   `changed_*` now means "files written". No test asserted the old conflated values.

3. **Codex guard semantics widened from prefix to whole-line.** One rule for all roots beats two.
   All 46 Codex agent files and 19 profiles keep matching (their marker is line 1), so behavior is
   unchanged in practice; the theoretical difference is a hand-written TOML containing that exact
   comment line below line 1, which does not exist in this repo (0 unexpected files in either root).
   Two guard modes would have been the alternative — rejected as complexity for no gain.

4. **Skill removal uses `shutil.rmtree`** instead of the previous manual `rglob`-unlink +
   reverse-`rmdir` walk. Equivalent, far simpler, and *safer*: the old walk would follow a symlinked
   subdirectory, which `rmtree` does not. The old code was dead, so there was no live behavior to
   preserve.

5. **Marker constant named `GENERATED_AGENT_MARKDOWN_HEADER`**, not the plan's proposed
   `GENERATED_MARKDOWN_HEADER` (explicitly `[PROPOSED - name TBD]`). Rationale in Decisions §2.

6. **Helper signature is `_prune_orphaned_outputs(directory, pattern, expected, marker)`** — the
   plan proposed `(directory, expected, marker)`. A glob `pattern` is required because the roots
   differ (`*.md`, `*.toml`, `*.config.toml`).

## Gaps

1. **`claude/agents/single-feature.md` is a pre-existing orphan that this pruner will never
   remove.** Found via the AC7 enumeration — the plan's context asserts `README.md` is the only
   unexpected file in that root; there are two.

   Root cause: its source is `single-feature-agent.agent.md`, which has **no `user-invocable` key**
   → defaults to `true` → it emits only a command (`claude/commands/single-feature-agent.md`,
   present and correct). Its expected subagent path would be `single-feature-agent.md`, so the
   existing reclassification unlink at `:1515` never fires on the differently-named
   `single-feature.md`. It is a stale artifact of an agent rename in commit `1a0925c`.

   **Why the pruner cannot fix it:** Option B prunes only marker-bearing files. Regeneration marks
   only files in the *expected* set, so a file that was already an orphan before the marker existed
   is unmarked forever and is indistinguishable from `README.md`. The guard correctly fails closed.

   **This is a limitation of Option B the plan did not anticipate**, but its blast radius is exactly
   one file (proven by the enumeration: 2 unexpected files across all 8 roots, one being README).

   **Not fixed here** — the plan's non-goals forbid deleting any agent/skill/command in this
   feature ("capability only"). Belongs to `08-retirement-reconciliation`; a one-line
   `git rm claude/agents/single-feature.md` resolves it. **No downstream impact**: verified that
   all five of feature `02`'s retired evaluators are marker-bearing and in the expected set, so they
   will prune correctly.

2. **A live `--watch` propagator process is running** (PID 15360, system `python3`), holding
   pre-change code in memory. It only fires on `.github/` changes, and this feature touched only
   `scripts/` and `tests/`, so it stayed inert — the final tree was re-verified clean. **It must be
   restarted before it is trusted again**, or a `.github/` edit would rewrite all 146 generated
   files *without* markers using stale code, silently disabling the pruner. The plan documents that
   the watcher needs a restart for propagator edits; this run is a live instance of that condition.
   Left running — it is the user's process, not mine to kill.

3. **Unrelated, non-reproducible observation**: during the first full-suite run, 12 files under
   `dev/phase-final-review/fixtures/PHASE_05/` showed as deleted. Restored via `git checkout`.
   Could not be reproduced across 5 subsequent full-suite runs; no test references those paths;
   nothing in this feature touches `dev/`. Recorded for visibility, cause unidentified.

4. **`GITHUB_AGENTS_DIR` and `GITHUB_INSTRUCTIONS_DIR` are now unused** module constants (the
   plumbing replaced their only readers). Deliberately left: `GITHUB_SKILLS_DIR` and
   `CODEX_SKILLS_DIR` were *already* unused before this feature, so the module treats these as a
   declarative index of roots, and `CLAUDE_AGENTS_DIR` / `OPENCODE_AGENTS_DIR` / `CODEX_AGENTS_DIR`
   remain part of the public surface used by tests. Removing them is a separate cleanup, out of
   scope here.

## Reviewer Focus Areas

- **`_is_generated_output` (`scripts/propagate_master_assets.py:189`) — the whole feature's safety
  rests here.** It uses whole-line containment, not `startswith`. Confirm the widening from prefix
  to line matching is acceptable for the two TOML roots (Deviations §3). This function is also the
  AC4a bug fix: the old guard read as implemented and matched 0/24 files for years.
- **AC5 guard is mutation-tested, not just asserted.** Deleting the two `_is_generated_output`
  lines from `_prune_orphaned_outputs` makes exactly 3 tests fail
  (`test_hand_maintained_file_in_generated_root_survives`, `test_unreadable_orphan_is_not_deleted`,
  `test_real_repository_propagation_removes_nothing`). The plan requires the README test to fail if
  the guard is removed — verified, not assumed. **Caution: that mutation deletes real files via the
  AC7 test; `git checkout -- claude/agents/` restores them.**
- **AC4b deviation (Deviations §1)** is the one place I did not implement the AC as literally
  written. The reasoning is that Stage 2 invalidates AC4b's stated premise. Worth a second opinion
  on whether that reading is right.
- **Prune ordering (AC6)** — all five agent-side prunes sit after the `for agent in agents:` loop
  (`:1530`), and the skills prune after the skills loop (`:1414`). `_claude_filename_for` resolves
  names against on-disk stems, so any reordering silently renames survivors.
- **The 146-file regeneration** is mechanical (+146/−0, one marker line per file) and safe to skim,
  but Gap §2 (stale watcher) is the thing that could silently undo it.
