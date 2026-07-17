# Review Record: 01 Propagator Orphan Pruning

## Summary

The feature makes the propagator delete generated outputs whose source asset is gone,
across all eight pruned roots, and repairs the `codex/skills` guard that had matched
0 of 24 files since it was written. The implementation is disciplined: Option B was taken
as the plan recommended, the marker-emitting regeneration is exactly **146 files, +146/−0**
(verified — no content change), and every open decision the plan left to the implementer is
recorded with its rationale rather than silently taken.

The implementation record is unusually honest — it self-reports the incident where a
mutation test deleted real files, a pre-existing orphan the feature cannot fix, and a stale
watcher process. All three self-reports check out against the tree.

I verified the three items this review was asked to adjudicate by **execution, not reading**:

1. **AC4b deviation — sound, accept.** Judgement below.
2. **Isolation — airtight.** Instrumented every `unlink`/`rmtree` during the prune tests:
   25 deletions, all under `tmp*` roots, **0 escapes**. Code audit agrees — all 9 `REPO_ROOT`
   references are `repo_root or REPO_ROOT` defaults and no module `*_DIR` constant is read
   inside `propagate_once` any more.
3. **Fail-closed — confirmed, but it was fail-*open* in one realistic case, now fixed.**

**One real defect found and fixed.** `_is_generated_output` matched the marker *anywhere*
in the file. A hand-maintained doc that merely **quotes** the marker — e.g. a README
documenting the convention in a fenced code block — was classified as generated and deleted.
That is precisely `claude/agents/README.md`, the exact file AC5 exists to protect. I proved
this by restoring the old rule and watching the new test delete the README. Fixed by keying
the guard to the single line the emitter writes to.

**One environmental hazard reproduced, not merely reported.** Mid-review I appended to
`.github/learnings/` and accidentally triggered the record's Gap 2: the stale `--watch` process
stripped all 146 markers using pre-change code. I restored the tree. This upgrades that gap from
a documented caution to a **High** operational finding with a reproduction, and it exposed a real
coverage hole — AC7's inert-run test **cannot tell a correct pruner from a disarmed one**
(verified). I added the test that can.

## Verdict

**Approved with Reservations**

The code under review is correct and the one code defect is fixed with a regression test.
The reservations are all environmental or deferred, none of them defects in this diff:

1. **Restart the stale watcher (PID 15360) before the next `.github/` edit** — reproduced live;
   it silently disarms the feature.
2. The `single-feature.md` orphan — correctly out of scope, owned by `08`.
3. Harness parsing of the marker is unverified by any automated test (see Traceability).

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1 | **Met (verified)** | `propagate_master_assets.py:1553` | Orphaned `claude/agents/` pruned + counted. Test executed; deletion path instrumented. |
| AC2 | **Met (verified)** | `:1556` | Command prune; reclassification path at `:1515` preserved. Test executed. |
| AC3 | **Met (verified)** | `:1559` | `opencode/agents/` pruned. Test executed. |
| AC4a | **Met (verified)** | `_is_generated_output` `:186` | The dead guard is live: 24/24 `codex/skills` now match (was 0/24). Confirmed by direct grep + prune test. |
| AC4b | **Met via documented deviation** | `_prune_orphaned_skill_dirs` `:229` | Marker-guarded, not directory-name-only. Deviation judged **sound and safer** — see below. |
| AC5 | **Met (verified, hardened)** | `_prune_orphaned_outputs` `:226` | Guard is load-bearing: mutation-tested, 3 of 4 isolated tests catch its removal. **Was fail-open on marker-quoting docs — fixed (Issue #1).** |
| AC6 | **Met (verified)** | `:1550-1565` | All prunes sit after the emission loop; skills prune after the skills loop. Test executed. |
| AC7 | **Met (verified by execution)** | whole-run | Ran the **real** propagator: all six orphan counters `0`, `git status` clean across `claude/ opencode/ codex/`. Not inferred. |
| AC8 | **Met (verified by execution)** | `:1596-1606` | Ran the CLI; all six keys present in the JSON summary. |
| AC9 | **Met (verified by instrumentation)** | `propagate_once(..., repo_root)` `:1448` | 25 deletions traced, 0 outside temp roots. |

**Unverified (requires runtime/harness confirmation, not obtainable by static review or unit test):**
The Stage 2 load-bearing assumption is that the marker below the closing `---` does not break
**harness** parsing. What was actually verified — by the implementer and again by me — is that
the *repo's own* `_parse_frontmatter` still returns identical keys. That is not the same as
Claude Code, OpenCode, or Codex parsing the file at runtime. Risk is low (an HTML comment below
frontmatter, invisible when rendered) and the 146-file diff is provably content-free, but the
claim "harness parsing verified" is stronger than the evidence. **Requires loading one real
regenerated agent and one slash command in an actual Claude Code / OpenCode session.**

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | Marker guard matched the marker **anywhere** in the file, so a hand-maintained doc quoting the marker (e.g. a README documenting the convention) is deleted — defeating AC5 on the exact file it protects | Medium | `propagate_master_assets.py:186` | AC5 | **Fixed** |
| 2 | `GITHUB_AGENTS_DIR` / `GITHUB_INSTRUCTIONS_DIR` are now dead — only their definitions remain | Low | `:28-29` | — | Open (Wont-Fix here) |
| 3 | `claude/agents/single-feature.md` is a pre-existing orphan the pruner can never remove (unmarked → fails closed forever) | Low | `claude/agents/single-feature.md` | — | Open (deferred to `08`) |
| 4 | `test_real_repository_propagation_removes_nothing` runs against the real tree and writes to it (no-op when in sync, but deletes if the guard breaks) | Low | `tests/test_propagate_master_assets.py:1078` | AC7 | Open (mandated by plan test 3) |
| 5 | Stale `--watch` propagator (PID 15360) holds pre-change code; a `.github/` edit rewrites all 146 files **without** markers, silently disabling every prune | **High** (operational) | — | AC5, AC7 | **Open — REPRODUCED during this review; requires a watcher restart** |

### Issue #1 — detail

Not theoretical. I restored the pre-fix rule and ran the new regression test:

```
=== With the OLD whole-file guard restored ===
new test catches the hazard: True
AssertionError: False is not true : a doc quoting the marker was deleted
```

`claude/agents/README.md` today documents porting conventions and already contains fenced
YAML/Markdown examples of agent frontmatter. A future edit quoting the marker line — a very
natural thing for that specific README to do — would have caused the propagator to delete it.

The fix keys the guard to the one position the emitter writes to (line 0 for the TOML roots,
the line below the closing `---` otherwise), extracted into `_generated_marker_line_index` so
the writer and the guard share one definition and cannot drift.

**Side benefit:** this also retires the implementer's Deviation §3. The Codex guard had been
widened from `startswith` to whole-line containment; the positional rule restores strict
line-1 matching for the TOML roots, so the theoretical false positive that deviation accepted
no longer exists. One rule, and it is now the *tightest* of the three.

### Issue #5 — reproduced live during this review (upgraded Low → High)

I logged this as a theoretical operational risk, then **triggered it by accident within the
same review**. Appending to `.github/learnings/` woke the stale watcher (PID 15360, system
`python3`, holding pre-marker code). It immediately rewrote all 146 generated files and
**stripped every marker**:

```
=== marker counts after the stale watcher fired ===
claude/agents: 0      (was 33)
claude/commands: 0    (was 19)
opencode/agents: 0    (was 46)
```

The diff was exactly the marker line removed from each file, nothing else. **No deletions
occurred** — the stale code has no pruner for those roots, so the tree was silently
*disarmed* rather than damaged. That is the dangerous part: the pruner would have become a
no-op with no error, no failing test, and no visible symptom. `test_real_repository_propagation_removes_nothing`
would still have passed — because an inert pruner removes zero files, which is exactly what
AC7 asserts. **AC7 cannot distinguish "correctly inert" from "broken and inert."** That is
precisely the failure shape of the original `codex/skills` dead guard this feature exists to fix.

**Restored** by running the current propagator (`--once`): markers back to 33/19/46/24/24/24,
zero orphans removed, tree byte-identical to the committed state. Verified.

This moves the record's Gap 2 from a documented caution to a demonstrated failure with a
reproduction. It is not a defect in the code under review — the code is correct — but it is a
live hazard in the working environment that will silently undo the feature. **The watcher must
be restarted before the next `.github/` edit.** It is the user's process; I did not kill it,
per the implementer's same reasoning.

This incident is also the strongest argument for the new
`test_marker_guard_matches_every_real_generated_file` test I added. I verified this rather than
asserting it — simulating stripped markers across the whole suite:

```
CATCHES stripped markers <- test_marker_guard_matches_every_real_generated_file
MISSES  stripped markers <- test_real_repository_propagation_removes_nothing
```

The AC7 test — the plan's designated safety proof — **cannot detect a fully disarmed pruner.**
The new test is now the only thing in the suite that can. Before this review, a stale watcher
(or any future change that stopped emitting markers) would have silently disabled every prune
with a fully green suite.

## Fixes Applied

| File | What Changed | Issue # |
|------|--------------|---------|
| `scripts/propagate_master_assets.py` | Added `_generated_marker_line_index` as the shared definition of the marker's position; rewrote `_with_generated_marker` and `_is_generated_output` to both use it. Guard is now positional, not a whole-file search. | #1 |
| `tests/test_propagate_master_assets.py` | Added `test_hand_maintained_file_quoting_the_marker_survives` (pins the fail-open hazard) and `test_marker_guard_matches_every_real_generated_file` (pins the opposite failure — a guard tightened into inertness would pass AC7 for the wrong reason). | #1 |

**Verification after fixes:**
- Full suite: **428 passed, 22 subtests** (was 426/15; +2 tests, +7 subtests). No regressions.
- Real propagator run: **byte-identical output** — 0 changed, 0 orphans removed, `git status` clean.
- Guard still matches **all 163 real generated files** (33/19/46/46/19) — the fix did not make it inert.
- `PERF-01` (`test_ac9_propagated_guard_median_latency_is_below_50_ms`) **passed**; threshold untouched.

## AC4b Deviation — Adjudication

**The implementer is right. Accept the deviation.**

AC4b mandates directory-name-only pruning *on the stated premise* that "a marker guard is
unavailable" because the skill roots "are byte-identical copies of source `SKILL.md`". That
premise is a **factual claim about the tree, not a design intent** — and the tasks file's own
Stage 2 destroys it, requiring the marker be emitted into `claude/skills` and `opencode/skills`
("Without this, AC4 is unreachable"). Once the marker exists, the premise is simply false.

The deviation is strictly safer, not merely equivalent:

- AC4b's rule is `absent from expected set` → delete. The implemented rule is
  `absent from expected set` **AND** `marker-bearing` → delete. That is a strict **subset** of
  deletions. It cannot delete anything AC4b's rule would have spared.
- AC5 demands "no pruner deletes a file it did not generate", then **concedes** for skills that
  "(a) alone governs" — a documented weakening forced by the false premise. The deviation
  removes the concession and makes AC5 hold uniformly across all eight roots.
- The plan itself calls the asymmetry between roots "the deeper problem". AC4b would have
  preserved it; the deviation eliminates it.

**Did it defeat an intent AC4b encoded?** One thing AC4b's looser rule would catch that the
marker rule won't: a skill directory orphaned *before* the marker existed is unmarked forever
and unprunable. This is the same class as Gap 1 (`single-feature.md`), and the implementer
identified it. I verified the blast radius is **empirically zero** — 24/24 marked in each of
the three skill roots, 0 unexpected directories. The intent AC4b encoded (prune orphaned skill
dirs) is fully served; only an edge case that does not exist is given up, and giving it up is
what buys AC5 for the skill roots.

The deviation is well-reasoned, correctly recorded, and covered by
`test_unmarked_skill_directory_survives` — a test AC4b's design would fail.

## Remaining Concerns

- **Issue #5 (stale watcher) — the top action item. No longer hypothetical: I reproduced it.**
  It holds pre-marker code and strips all 146 markers on any `.github/` edit, disabling every
  prune while the code still reads as correct — the same failure shape as the original
  `codex/skills` dead guard. **Restart PID 15360 before the next `.github/` edit or propagation
  run.** I restored the tree; the process is still live and still stale.
- **Issue #3** (`single-feature.md`): correctly deferred to `08` per this feature's non-goals
  ("capability only"). No downstream impact — I confirm all five of feature `02`'s retired
  evaluators are marker-bearing and in the expected set, so `02` will prune cleanly.
- **Issue #2** (dead constants): left deliberately per Gap 4's rationale. Reasonable, but the
  module now has four unused `*_DIR` constants; worth one cleanup pass rather than four.
- **Harness parsing is unverified** (see Traceability). Low risk, but it is the assumption the
  whole 146-file regeneration rests on and no automated test can confirm it.
- **Issue #4**: AC7 inherently mandates a real-tree test. This is exactly how the implementer's
  mutation test deleted real files. Inherent to the AC as written, not a defect; `git checkout`
  is the documented rollback and the blast radius is bounded by version control.
- **Gap 3 in the record** (12 unreproducible deletions under `dev/phase-final-review/fixtures/`)
  remains unexplained. I could not reproduce it either across a full suite run. Nothing in this
  feature touches `dev/`. Flagged, not attributed.

## Test Coverage Assessment

- **Covered:** AC1, AC2, AC3, AC4a, AC4b, AC5, AC6, AC7, AC8, AC9 — 12 tests in
  `OrphanPruningTests` (10 original + 2 added by this review). Failure modes covered beyond the
  plan's table: symlinked orphans, unreadable files, missing roots.
- **Guard quality is genuinely proven, not asserted.** Mutation testing confirms 3 of 4 isolated
  survival tests fail when `_is_generated_output` is disabled. `test_symlinked_orphan_is_not_unlinked`
  correctly does *not* fail — the symlink check is a separate guard, so that is right behavior.
- **Added by this review:** a test pinning the guard's *lower* bound (must not match a quoted
  marker) and one pinning its *upper* bound (must still match all 163 real generated files).
  The pair brackets the guard from both directions; the original suite only tested one side,
  which is why the fail-open case slipped through.
- **The coverage hole the incident exposed.** Every original test asserts what the pruner
  *deletes*; none asserted that it still *recognises* real generated output. Verified
  consequence: with all markers stripped, the full suite stayed green — AC7 passes an inert
  pruner, because "removes zero files" is satisfied both by a correct pruner and a dead one.
  `test_marker_guard_matches_every_real_generated_file` closes this and is the only test that
  fails in that state.
- **Missing:** no test asserts the marker survives a real harness load (not automatable here).
  No test covers a source file with unterminated frontmatter (returns unmarked → unprunable;
  correct fail-closed behavior, but unpinned).

## Risk Summary

- `scripts/propagate_master_assets.py:186` — `_is_generated_output` is the single point on which
  every deletion in this repo now depends. It is 8 lines, positionally exact, fails closed on
  read errors, and is bracketed by tests from both directions. This is the right shape for the
  blast radius.
- **The feature's own failure mode is silence.** The original bug was a guard that read as
  implemented and did nothing for years. The new guard is proven live (24/24, 163/163) rather
  than assumed — but the stale watcher (Issue #5) can re-create exactly that silent-failure
  state by stripping markers, and nothing detects it automatically.
- **Deletion is bounded by version control** — all three generated roots are committed, so
  `git checkout` is a real rollback. This is why the inert-run proof is cheap to trust.
- Pre-marker orphans are permanently unprunable (Option B's structural limitation). Blast radius
  measured at exactly **1 file** across all 8 roots. Bounded and owned by `08`.
