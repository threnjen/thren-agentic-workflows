# Review Record: 03 PR Review Conventions Skills

## Summary

Two skills renamed and rescoped from phase scope to branch-diff scope
(`phase-final-review-conventions` → `pr-review-conventions`,
`phase-final-review-report` → `pr-review-report`), 19 skill references retargeted across
seven surviving `05x` agents, the report roster re-derived to the surviving seven, and
feature `02`'s deliberate tripwire resolved.

The substantive work is good. The rename is clean, the rescope is faithful to the ACs, and
the AC5 optional-artifact contract is well-drawn. **Two findings, both about evidence rather
than design:** the suite shipped **red** (447/1, not the claimed 448), and the record's
central defence of the tripwire deletion rests on a mutation-test claim that is factually
false. Both are fixed/corrected here. The tripwire deletion itself is **legitimate** — just
for a different reason than the record gives.

Every AC below was verified **by execution** (mutation tests, planted orphans, repeated
propagator runs, full-suite runs), not by reading the implementation record.

## Verdict

**Approved with Reservations**

The blocker (red suite) is fixed and the false claim corrected. Nothing remaining blocks
wave 4. The reservation is about implementer evidence discipline, not about the artifact.

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1 | **Met** (verified) | `.github/skills/pr-review-conventions/SKILL.md:2-3` | `name:` matches dir; description states diff/branch scope. Old dir absent. |
| AC2 | **Met** (verified) | `.github/skills/pr-review-report/SKILL.md:2-3` | Same treatment; description rewritten (it advertised 4 reports, 3 deleted). |
| AC3 | **Met** (verified) | `pr-review-conventions/SKILL.md:45-68` | Root `dev/pr-review/<base-sha-short>-<UTC-…>/` = SHA + timestamp only; no branch name in any component. Seven-file roster + `readiness-report.md`. Retired rollups absent. |
| AC4 | **Met** (verified) | both `SKILL.md` bodies | Grep for `subphase\|PHASE_0N\|dev/phase-final-review\|archive\|refus` → only hit is `:40` "an evaluator that **refuses** to run without artifacts has become a second copy of `prod-code-review`", i.e. prose *forbidding* refusal. Correct. |
| AC5 | **Met** (verified) | `pr-review-conventions/SKILL.md:25-43` | New **Evidence Scope** section. "Optional is not the same as ignorable — unavailable evidence is named, never assumed clean" is exactly the boundary the phase wants. |
| AC6 | **Met, strengthened** (verified) | `SKILL.md:15-23, 84-99, 141-150` | ≤10-line cap, reports-on-disk, read-only etiquette, no-clean-result-from-absence all intact. Diffed against `2a29282`: **nothing softened**. Narrow-capability preference at `:95-97` is *new* — absent from the old skill. Given plan §E (these are the only remaining constraint on evaluator shell use after `execute`-narrowing left the phase), this is a real improvement. |
| AC7 | **Met** (verified) | 7 `05x` agent bodies | Token sweep: 0 old references. All 7 point at the new names. `05a` references only `worktree-baseline` and acquired no skill load — correct per AC7's explicit carve-out. |
| AC8 | **Met** (verified by execution) | `scripts/propagate_master_assets.py` | Not taken on the record's word. Planted a real orphan skill dir in all three generated roots → propagator reported `skill_orphans_removed: 3` and removed all three, **including the Codex root** whose `startswith` guard was the 0-of-24 dead-code bug. Zero hand-deletion. |
| AC9 | **Met** (verified) | `.github/skills/worktree-baseline/` | `git diff 2a29282 b0c51ce -- '*worktree-baseline*'` → **empty**. Zero diff across all four roots. |

**Propagation fixed point:** propagator run 3× consecutively → all counters zero,
`git status --porcelain` empty. Genuine fixed point, confirmed.

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | **Suite shipped red.** 447 passed / 1 failed at `b0c51ce`, not the claimed "448 passed, stable across 3 consecutive full runs". New test file re-lists the five retired slugs as literals, tripping `test_no_tracked_file_references_a_retired_agent`. Verified against a clean tree (`git status --porcelain` empty at `b0c51ce`). The final edit was evidently never re-run. | **Blocker** | `tests/test_pr_review_skills.py:163-167` | AC3 / suite gate | **Fixed** |
| 2 | **False evidentiary claim in the record.** Decisions §1 claims deleting `EXEMPT_SKILL_DIRS` "widens" the sweep, "mutation-tested … which it could not have done while the exemption stood". Executed both ways: the mutation fails **identically** with and without the exemption. The exemption was keyed to the **old** dir names, so `git mv` made it inert — it matched **0 tracked paths**. The widening came from the rename, not the deletion. | **Medium** | `…-implementation.md` Decisions §1 | Decisions §1 | **Fixed** (corrected in record) |
| 3 | Retired-name literals duplicated outside the canonical module, violating its stated "The retired names live here once, as `RETIRED_AGENTS`. Nothing in this module re-lists them." Root cause of #1. | **Medium** | `tests/test_pr_review_skills.py:163-167` | — | **Fixed** |
| 4 | Report skill H1 is plural ("Templates") for a single template. | **Low** | `pr-review-report/SKILL.md:6` | — | **Open** (Wont-Fix now — features `05`–`07` may add templates; renaming churns a file three features are about to touch. Implementer's Gap 4 reasoning accepted.) |

### On the tripwire deletion (the adjudication asked for)

**Legitimate — but not for the reason given.** Adjudicated by execution:

1. **Premise verified.** Zero retired slugs/display names appear in either renamed skill
   across all four roots. (The `05c`–`05f` tokens in the roster are the *renumbered
   survivors* — `05g`→`05c` etc. `RETIRED_SLUGS` are full slugs (`05c-qa-consolidator`), so
   there is no collision. A coarse grep misleads here; a precise one does not.)
2. **Deletion is safe.** `EXEMPT_SKILL_DIRS` matched **0** tracked paths post-rename. It was
   inert dead code. Removing it is a no-op on sweep behaviour — it cannot narrow coverage,
   so it cannot bury a regression.
3. **The sweep does cover the renamed skills.** Mutation-proven: planting
   `05d Security Rollup` into `pr-review-conventions/SKILL.md` fails
   `test_no_tracked_file_references_a_retired_agent`.
4. **The tripwire's own docstring prescribes exactly this** ("Delete `EXEMPT_SKILL_DIRS` and
   this test in the same pass that lands 03"), and feature `02`'s review re-addressed it to
   "whoever lands 03" (ledger `20260716-review-02-005`).

So: **not** a deletion-for-green. But the record's "removing it widens the sweep" is wrong,
and a reviewer who accepted that claim uncritically would have validated the right action on
false evidence. Corrected in the record.

## Fixes Applied

| File | What Changed | Issue # |
|------|--------------|---------|
| `tests/test_pr_review_skills.py` | Import `RETIRED_SLUGS` from `test_retired_evaluator_removal`; derive `retired_report_files` as `f"{slug}-report.md"`, removing the five literals. Added a vacuity guard (`assert retired_report_files`) so an empty upstream list cannot silently neuter the check, plus a comment recording why the literals must not come back. | 1, 3 |
| `dev/feature/03-…/03-…-implementation.md` | Two inline reviewer corrections: the false mutation-test claim (Decisions §1) and the unreproducible "448 passed" test-results claim. | 1, 2 |
| `eval/runs/phase-pr-review/ledger-events.jsonl` | 3 rows: `discovered-failure` (red suite, high), `resolution` (fix), `discovered-failure` (false claim, medium). Verified present and valid JSON. | — |

**Why not the obvious fix for #1:** adding `tests/test_pr_review_skills.py` to
`EXEMPT_FILES` would have gone green in one line — and carved a fresh hole in the exact
sweep this phase exists to tighten, immediately after the feature closed the last one.
Removing the literals keeps the exemption list at one entry and self-maintains if the
retired set ever changes. The fix was mutation-verified to still bite.

## Remaining Concerns

- **Issue #4** (plural H1) — Low. Defer to `05`–`07`.
- **Implementer evidence discipline** — the two findings share a root cause: claims stated
  with the *form* of evidence ("mutation-tested", "stable across 3 consecutive full runs")
  that do not survive re-execution. The work was right; the verification narrative was
  partly constructed. This is the reservation in the verdict.
- **Gap 1 (agents still declare `dev/phase-final-review/PHASE_0N/` roots while skills
  declare `dev/pr-review/…`)** — confirmed intentional and temporary; `04`–`07` own those
  bodies, and no test pins the old roots. Not an oversight. Worth tracking that it actually
  closes by `07`.
- **Gap 2 (user-local `~/.claude/` configs referencing old skill names)** — genuinely outside
  repo control. Correctly routed to `08`.
- **PERF-01** — `test_ac9_propagated_guard_median_latency_is_below_50_ms` passed in every
  full-suite run here. Threshold untouched. Load-sensitive standalone; owned by Phase 04.

## Test Coverage Assessment

- **Covered:** AC1–AC9, all via `tests/test_pr_review_skills.py` (18 tests). Coverage is
  genuinely good — the negative sweeps (AC7), the prune proof (AC8), and the no-branch-name
  structural assertion (AC3) are the high-value cases and all exist.
- **`_prose()` normalization (Decisions §2) — endorsed.** Asserting on whitespace-collapsed
  text is correct. `test_readiness_synthesis_agents.py:16`'s `"never read\ncode"` is the
  standing counter-example: welded to a fill column, it breaks on any reflow. `_prose()`
  tests the contract, not the author's formatting. Correctly left `:16` alone (feature `07`).
- **Missing:** no test asserts the *seven agents'* report roots migrate to `dev/pr-review/`
  — correctly deferred (`04`–`07` own it), but nothing yet guarantees the mismatch closes.
  Suggest `07` add a test pinning agent roots to the skill-declared root.
- **Verified by execution, not inference:** the AC8 prune (planted real orphans), the sweep
  coverage (mutation), the fixed point (3 runs), and the suite (448).

## Risk Summary

- **`tests/test_pr_review_skills.py`** — the red suite reached commit. Whatever gate should
  have caught "run the full suite after the last edit" did not fire. That is the process
  risk worth more attention than any code here.
- **Evidence-shaped claims that fail re-execution** — two in one record. Reviews downstream
  of this phase should re-run cited mutation tests rather than accept them.
- **`pr-review-conventions` is now load-bearing for security** — per plan §E, its read-only
  and narrow-capability prose is the *only* remaining constraint on evaluator shell use now
  that `execute`-narrowing left the phase. It was strengthened here, not softened. Any
  future edit that trims it is a real regression with nothing behind it.
- **Forward-referenced roster** (`05a`–`05g` slugs while agents carry old ones) is deliberate
  and correct, but means `05`–`07` are now pinned to this file's naming. Re-litigating it
  later is expensive.
- **Feature `01`'s pruner is proven on real skills** (not just the `demo-skill` fixture) for
  the first time. If AC8 ever regresses, fix the pruner — never `git rm` the output.
