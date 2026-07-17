# 01 Propagator Orphan Pruning

## Execution Metadata

- **Wave:** 1
- **Parallel safe:** yes
- **Depends on:** none
- **Key files modified:** `scripts/propagate_master_assets.py`, `tests/test_propagate_master_assets.py`
- **Sequential reason:** n/a

## Why This Feature Exists (not in the Phase document)

The Phase document assumes retirement is a cleanup chore: delete five source
agents, run the propagator, done. Codebase discovery proves that is not how the
propagator behaves.

The propagator prunes **only Codex agents and profiles** — and one prune that looks
implemented is dead code:

| Generated root | Orphan pruned today? | Guard | Measured |
|---|---|---|---|
| `codex/agents/*.toml` | **yes** (`scripts/propagate_master_assets.py:1405`) | `GENERATED_AGENT_HEADER` prefix | **46/46 match** — works |
| `codex/profiles/*.config.toml` | **yes** (`:1413`) | `GENERATED_AGENT_HEADER` prefix | works |
| `codex/skills/*/` | **NO — dead code** (`:1288`) | `GENERATED_SKILL_HEADER` prefix | **0/24 match** — never fires |
| `claude/agents/*.md` | no | — | no marker (0/35) |
| `claude/commands/*.md` | no | — | no marker (0/19) |
| `claude/skills/*/` | no | — | no marker |
| `opencode/agents/*.md` | no | — | no marker (0/46) |
| `opencode/skills/*/` | no | — | no marker |

**The Codex skills prune has never once fired.** Its guard is
`_read_text(skill_md).startswith(GENERATED_SKILL_HEADER)`, but a generated Codex
`SKILL.md` begins with `---` YAML frontmatter and carries the marker on **line 5**
(verified 2026-07-16: 0 of 24 match; the equivalent check on `codex/agents/*.toml`
matches 46 of 46, which is why the agent prune does work). The block reads as
implemented, passes review, and does nothing. This is a latent bug this feature
must fix, not merely a root to copy from.

**Net: no generated root prunes skills at all**, and only Codex prunes agents.

The single existing removal path for Claude agents (`:1383`) fires only when an
agent is *reclassified* to command-only. It does not fire when a source agent is
deleted.

Consequence: deleting `.github/agents/05c-qa-consolidator.agent.md` leaves
`claude/agents/z-qa-consolidator.md` and `opencode/agents/05c-qa-consolidator.md`
on disk permanently. Renaming the two skills leaves `claude/skills/…` and
`opencode/skills/…` orphaned. Renaming `05-phase-final-review` leaves
`claude/commands/phase-final-review.md` orphaned and still user-invocable.

Phase Success Criterion — *"The five retired evaluators are absent from
`.github/agents/` and from all three generated roots"* — is therefore not
satisfiable by running the propagator today. This feature makes it satisfiable.

## A. Requirements & Traceability

### Naming correction (verified 2026-07-16)

**There is no `propagate_agents_once`.** Agent propagation is inline in
`propagate_once(verbose: bool = True)` at `scripts/propagate_master_assets.py:1329`;
`grep -rn "agents_once" scripts/ tests/` returns zero hits. The skill counterpart
`propagate_skills_once(repo_root)` **does** exist and does take a root. Every AC
below names the verified function.

### Acceptance Criteria

- **AC1** — `propagate_once` removes generated agent files in `claude/agents/` that
  no longer correspond to any source agent, and reports the count in its result
  dict.
- **AC2** — `propagate_once` removes generated command files in `claude/commands/`
  that no longer correspond to any `user-invocable: true` source agent.
- **AC3** — `propagate_once` removes generated agent files in `opencode/agents/`
  that no longer correspond to any source agent.
- **AC4** — `propagate_skills_once` removes orphaned generated skill directories in
  **all three** roots. This has two parts, and the first is a bug fix:
  - **AC4a** — The existing `codex/skills/` prune guard (`:1288`) is repaired so it
    actually matches. `startswith(GENERATED_SKILL_HEADER)` fails because the marker
    sits on line 5, below the frontmatter. Fix the guard (substring/line check, or
    emit the marker where the guard looks) — do not delete the guard to make the
    prune fire, which would remove the only safety this root has.
  - **AC4b** — `claude/skills/` and `opencode/skills/` gain pruning. These carry
    **no marker at all** (they are byte-identical copies of source `SKILL.md`), so
    a marker guard is unavailable and pruning must key on **directory-name
    expectation**: a skill directory is an orphan when its name is absent from the
    source skill set. This differs from the agent-side guard by necessity, and the
    difference must be stated in the code, not discovered later.
- **AC5** — **No pruner deletes a file it did not generate.** `claude/agents/README.md`
  is a real, hand-maintained file living inside a generated root; it must survive
  every propagation run. For agent and command files, a file is deletable only when
  it is both (a) absent from the expected set and (b) positively identified as
  generated. For skill directories, where no marker exists, (a) alone governs — so
  the expected set must be complete before the sweep is enabled.
- **AC6** — Pruning never changes the identifier assigned to a surviving agent.
  `_claude_filename_for` and `_opencode_filename_for` select an output filename by
  inspecting stems that already exist on disk (`_discover_existing_stems`), so
  deletion order is load-bearing: all emission completes before any pruning.
- **AC7** — A propagation run on the unmodified repository deletes **zero** files.
  The pruner is proven inert against the current tree before it is trusted against
  a changed one.
- **AC8** — Deleted-file counts surface in the propagator's result dict and CLI
  summary, so a run that removes files says so rather than removing them silently.
- **AC9** — **Agent-side pruning is testable without touching the real tree.**
  `propagate_once` accepts no `repo_root` and resolves `CLAUDE_AGENTS_DIR`,
  `OPENCODE_AGENTS_DIR`, `CLAUDE_COMMANDS_DIR` and friends from module constants
  bound to the real `REPO_ROOT` at import time. The temp-repo idiom at
  `tests/test_propagate_master_assets.py:68` works only because
  `propagate_skills_once(repo_root)` takes a root; the agent path has no equivalent.
  **A prune test written the obvious way would delete files from the real
  repository.** Either plumb `repo_root` through the agent path (mirroring
  `propagate_skills_once`) or monkeypatch the module constants — decide, and make
  the isolation explicit rather than incidental.

### Non-Goals

- Deleting any agent, skill, or command in this feature. This feature adds the
  *capability*; `02-retired-evaluator-removal` is its first consumer.
- Pruning `claude/learnings/` or any hook output. Hook assets already have
  `_remove_retired_hook_assets` (`:982`).
- Changing the identifier/alias resolution rules themselves.
- Adding a `--dry-run` flag to the propagator (see D, "Complexity risks").

### Traceability

| Acceptance Criteria | Code Areas/Modules | Test / Evidence Category |
|---|---|---|
| AC1, AC2, AC3 | `scripts/propagate_master_assets.py` — `propagate_agents_once` | Must-have automated test (new) |
| AC4 | `scripts/propagate_master_assets.py` — `propagate_skills_once` | Must-have automated test (new) |
| AC5 | new generated-marker guard | Must-have automated test (new); regression on `claude/agents/README.md` |
| AC6 | `_claude_filename_for`, `_opencode_filename_for`, `_discover_existing_stems` | Must-have automated test (new) |
| AC7 | whole-run behavior | Must-have automated test (new); existing suite regression |
| AC8 | result dict + CLI summary | Existing test to update — `tests/test_propagate_master_assets.py` |

## B. Correctness & Edge Cases

**The guard problem is the whole feature.** Codex prunes safely because every
generated Codex file begins with `GENERATED_AGENT_HEADER` or
`GENERATED_SKILL_HEADER`. Verified: **Claude and OpenCode agent/command outputs
carry no generated marker at all** — `grep -rl GENERATED claude/agents/
claude/commands/ opencode/agents/` returns zero of 35, 19, and 46 files
respectively. There is nothing to guard by today.

Two viable designs; the implementer must choose one and record the choice:

- **Option A — expected-set-only pruning.** Delete any file in the root that is
  not in the expected set. Simple, but `claude/agents/README.md` is not in the
  expected set and would be destroyed. Requires an explicit exclusion list, which
  is a hardcoded denylist that silently rots as new hand-maintained files appear.
- **Option B — emit a generated marker, then guard by it** (recommended; matches
  the existing Codex contract). Add a marker to Claude/OpenCode agent and command
  output, then prune only marker-bearing orphans. Costs a one-time regeneration
  touching every file in three roots — a large but mechanical diff. `README.md`
  survives because it has no marker, with no denylist to maintain.

Option B trades a big one-time diff for a guard that cannot rot. It also makes
the three roots consistent with each other, which is the deeper problem. Prefer B;
if the marker cannot be placed without breaking harness parsing (see Unverified
Assumptions), fall back to A with an explicit, tested exclusion list.

**Marker placement is constrained by consumers.** Claude agent files and command
files begin with YAML frontmatter that Claude Code parses. The marker must not
sit above the opening `---`. Place it immediately after the closing `---`, as the
Codex renderer already does for its own output.

### Failure modes

| Mode | Handling |
|---|---|
| A hand-maintained file sits in a generated root (`claude/agents/README.md`) | Never deleted — AC5. This is the primary safety property. |
| Prune runs before emission; a surviving agent's stem disappears; `_choose_existing_stem` picks a different filename | Prune strictly after all emission — AC6 |
| A generated root does not exist (fresh clone, partial checkout) | Treat as nothing to prune; never create the directory to prune it |
| A file is unreadable while reading its marker | Do not delete. An unreadable file is not a confirmed orphan. Fail closed. |
| An orphan is a directory where a file is expected | Do not delete recursively outside the skills path, which already has a tested recursive removal (`:1291`) |
| Propagator is running under `--watch` | Out of scope; the watcher already requires a restart for propagator edits (documented in `PROJECT_ROADMAP.md` Architecture Notes) |

## C. Consistency & Architecture Fit

Follow the established Codex prune shape at `scripts/propagate_master_assets.py:1405`:
accumulate an `expected_*_files` set during emission, then sweep the directory,
skip expected files, verify the generated marker, `unlink`, and increment a
counter. Mirror it for the other two roots rather than inventing a second idiom.

**Do not reuse `GENERATED_AGENT_HEADER` verbatim in Markdown.** It is
`# Generated from .github/agents source-of-truth. Do not edit manually.`
(`:51`) — a **TOML comment**, correct for `codex/agents/*.toml`, but in a Markdown
agent file that line renders as an **H1 heading** at the top of every agent body.
The right precedent is `GENERATED_SKILL_HEADER` (`:52`), which is already an HTML
comment (`<!-- … -->`) precisely because its target is Markdown. Follow the skill
constant's form, not the agent constant's name.

Proposed symbols, all `[PROPOSED - name TBD]`:

- `GENERATED_MARKDOWN_HEADER` — HTML-comment marker for Claude/OpenCode Markdown
  agent and command output, modeled on `GENERATED_SKILL_HEADER`.
- `_prune_orphaned_outputs(directory, expected, marker)` — one helper used by all
  roots.
- `"orphans_removed"` — result-dict key.

## D. Clean Design & Maintainability

Simplest design that satisfies the ACs: one generic pruning helper, called once
per root, after emission, guarded by a marker. The asymmetry is the bug; the fix
is to remove the asymmetry rather than add a fourth special case.

**Complexity risks.** A `--dry-run` flag is tempting for a deletion feature and is
deliberately excluded: AC7 (a no-op run on the current tree) plus AC8 (counts in
the summary) already give the operator the same safety without a second code path
that can drift from the real one.

**Duplication risk.** Three near-identical sweep loops. Factor into one helper on
first repetition, not third.

### Keep-it-clean checklist

- [ ] One prune helper, not three copies
- [ ] Prune strictly after emission in every path
- [ ] No hardcoded filename denylist if Option B is taken
- [ ] Counts reported, never silent
- [ ] Marker constant reused, not duplicated

## E. Completeness: Observability, Security, Operability

**Observability decision** — Add exactly one aggregate count per root to the
existing result dict and CLI summary. No per-file logging on the normal path: a
clean run should stay silent, matching every other counter the propagator emits.
A file that *is* deleted is visible in `git status`, which is the operator's real
audit trail. This is the diagnosable-failure-mode bar the phase's plan template
asks for, and per-file logs do not clear it.

**Security** — This feature deletes files. That is its entire risk surface. The
marker guard (AC5) and the inert-run proof (AC7) are the mitigations. There is no
secret handling, no network, and no new shell execution.

**Runbook** — Verify: `git status` after a propagation run on a clean tree shows
no deletions (AC7). Rollback: `git checkout -- claude/ opencode/ codex/`
restores any wrongly deleted generated file, since all three roots are committed.
This is why the inert-run proof is cheap to trust — the blast radius is bounded by
version control.

## F. Test Plan

**Existing tests to update**
- `tests/test_propagate_master_assets.py` — result-dict assertions gain the new
  counter keys.

**Must-have automated tests (new)** — all use the existing
`tempfile.TemporaryDirectory(dir=REPO_ROOT)` fixture idiom already established at
`tests/test_propagate_master_assets.py:69`, so no new fixture machinery is needed.

Top-value cases:

1. **Orphaned Claude agent is removed.** Given a temp repo with a generated
   `claude/agents/z-gone.md` bearing the marker and no matching source agent,
   when propagation runs, then the file is deleted and the count reports 1.
2. **Hand-maintained file survives (AC5 — the critical one).** Given
   `claude/agents/README.md` with no marker and no matching source agent, when
   propagation runs, then the file still exists. This is the test that protects a
   real file in the real repo; it must fail if the guard is removed.
3. **Inert on a clean tree (AC7).** Given the real repository state, when
   `propagate_agents_once` and `propagate_skills_once` run, then zero files are
   deleted.
4. **Emission-then-prune ordering (AC6).** Given a surviving agent whose Claude
   stem (`z-artifact-sweeper`) also matches an orphan candidate, when propagation
   runs, then the survivor keeps its stem and only the true orphan is removed.
5. **Orphaned command is removed.** Given a source agent flipped to
   `user-invocable: false`, when propagation runs, then its `claude/commands/`
   file is deleted while its subagent file is retained.

**Test data / fixtures** — none beyond temp repos.

## Unverified Assumptions

- That a generated marker can be placed after the closing `---` of a Claude agent
  file and a Claude command file **without breaking harness parsing or changing
  agent behavior**. This is the load-bearing assumption of Option B. Verify against
  one regenerated agent before regenerating all three roots. If it fails, take
  Option A with a tested exclusion list.
- That `claude/agents/README.md` is the *only* hand-maintained file across the
  three generated roots. Verified for `claude/agents/` by inspection; **not**
  verified exhaustively for `claude/commands/`, `claude/skills/`,
  `opencode/agents/`, or `opencode/skills/`. Enumerate before enabling the prune —
  AC7 is the backstop that catches a miss.

## Relationship to Sibling Plans

- **Depends on nothing.** It is the first feature because every later feature
  deletes or renames a source asset, and each of those leaves orphans behind
  without this capability.
- **Enables `02-retired-evaluator-removal`**, the first real consumer and the
  feature that proves this one works end to end.
- **Enables `03-pr-review-conventions-skills`** (renaming a skill directory
  orphans the Claude and OpenCode skill dirs; only Codex self-prunes) and
  **`04-pr-review-orchestrator`** (renaming the orchestrator orphans
  `claude/commands/phase-final-review.md`, which would otherwise remain a live,
  user-invocable slash command for a deleted agent).
- **Every renumbering feature** (`05`, `06`, `07`) depends on it too: OpenCode
  filenames are keyed on the source slug, so `05g-artifact-sweeper` →
  `05c-artifact-sweeper` orphans `opencode/agents/05g-artifact-sweeper.md`. Claude
  filenames are keyed on the agent *name* and mostly survive the renumber — an
  asymmetry that makes OpenCode orphans easy to miss by eye.

## Stage 0: Test Prerequisites

**Goal**: Not required. Baseline is 416 passed across 4 consecutive full runs
(2026-07-16), and `tests/test_propagate_master_assets.py` is 849 lines covering
this module directly. Coverage is well above the 50% bar.
**Success Criteria**: n/a
**Status**: Not required

## Stage 1: Enumerate and Prove the Gap

**Goal**: A failing test that deletes a source agent in a temp repo and asserts
its Claude and OpenCode outputs are gone. Enumerate every non-generated file
across the three roots and record the list in the implementation record.
**Success Criteria**: New test fails for the right reason; the hand-maintained
file inventory is written down.
**Status**: Not Started

## Stage 2: Emit the Generated Marker

**Goal**: Add the marker to Claude/OpenCode agent and command rendering; verify
one regenerated agent still parses and behaves before regenerating all roots.
**Success Criteria**: Marker present in regenerated output; harness parsing
verified against a real agent; full suite green.
**Status**: Not Started

## Stage 3: Implement Guarded Pruning

**Goal**: One prune helper applied to `claude/agents/`, `claude/commands/`,
`opencode/agents/`, and the two skill roots, strictly after emission.
**Success Criteria**: AC1–AC6 tests pass, including the `README.md` survival test.
**Status**: Not Started

## Stage 4: Prove Inert, Then Report

**Goal**: Confirm a real-tree run deletes nothing (AC7); add counts to the result
dict and CLI summary (AC8).
**Success Criteria**: `git status` clean after a real propagation run; counts
present; full suite green across repeated runs.
**Status**: Not Started
