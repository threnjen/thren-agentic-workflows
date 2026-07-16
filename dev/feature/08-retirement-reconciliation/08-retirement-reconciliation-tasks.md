# 08 Retirement Reconciliation — Tasks

Baseline: 416 passed, 15 subtests (2026-07-16). Runner: `.venv/bin/python -m pytest tests/ -q`.
Stages are sequential — see the context file's Suggested Implementation Order.

## Stage 0: Test Prerequisites

**Status: Not required.** Baseline established across 4 consecutive full runs (2026-07-16), adjusted by features `01`–`07`. No tasks.

## Stage 1: Sweep to Extinction

*Success criteria: AC6, AC7.*

- [ ] Read feature `02`'s implementation record to learn the **actual filename** the reference-sweep test shipped under — it is `[PROPOSED - name TBD]` in every plan and must not be guessed (DD-6)
- [ ] Extend the sweep's pattern set to cover **three** classes, not two: retired/old **slugs** (`05h`–`05l`, deleted `05c`–`05f`, `05i`), `name:` **display names** (e.g. `05 Phase - Final Review`), and **informal prose forms** with no hyphens (e.g. `Phase Final Review`). Display-name matching alone misses both AC6 doc surfaces (DD-4)
- [ ] Extend the sweep to `phase-final-review` **skill names** (`phase-final-review-conventions`, `phase-final-review-report`) and **command names** (`phase-final-review.md`)
- [ ] Widen the sweep's exemption list from `docs/phases/**` + `.github/learnings/**` to also exempt `dev/**` — planning records are historical records, and the sweep otherwise fires on this feature's own plan and on `dev/feature/phase-03-phase-final-review-execution-manifest.md` (DD-2)
- [ ] Exempt propagated learnings roots (`claude/learnings/**` and any equivalent) alongside their exempt source (DD-3)
- [ ] Point the sweep at the three documentation surfaces: `.github/agents/README.md`, `docs/CODEBASE_CONTEXT.md`, root `README.md`
- [ ] Fix `.github/agents/README.md`: orchestrator table (line ~136), subagent table (lines ~163-172), agent detail prose (lines ~195-196), and the **"Four orchestrators" note (line ~412)** which names `05 Phase - Final Review` literally
- [ ] Fix `docs/CODEBASE_CONTEXT.md` line ~89 — replace "Phase Final Review evaluators" and **recount** the "24 hidden subagents" claim from `.github/agents/` rather than arithmetic-ing the old number (DD-4, DD-5)
- [ ] Fix root `README.md` line ~130 — replace "Phase Final Review orchestration and evaluators" and **recount** the "43 source agent definitions" claim from disk (DD-4, DD-5)
- [ ] **Fix `.gitignore` lines 6-9** (DD-1): the `dev/phase-final-review/` fixture-preservation rules are stale, and `dev/pr-review/fixtures/` has no preservation rule while `dev/pr-review/<base-sha-short>-<timestamp>/` run outputs are not ignored. Retarget the rules to `dev/pr-review/` so the fixture is tracked and run outputs are not. Do this **before** Stage 3, or the dry run pollutes the working tree and confounds AC8
- [ ] Verify `claude/commands/phase-final-review.md` is **absent** (AC7) — a stale command is the sharpest dangling reference in the repo: it stays user-invocable and points at a deleted agent
- [ ] Verify the propagator-derived replacement command exists. Read the real filename from the propagator's **output** (`_claude_identifier_for`, `scripts/propagate_master_assets.py:408`); do not assume `pr-review.md` (AC7, DD-7)
- [ ] Add the stale-command-absent / new-command-present assertion to the sweep test (AC7)
- [ ] Run the sweep to extinction — zero hits outside the exemption list

## Stage 2: Verify Propagation

*Success criteria: AC5, AC8.*

- [ ] Assert `05a`–`05g` exist in `.github/agents/` and that **no** `05h`–`05l` slug survives in source or in any of the three generated roots (AC5)
- [ ] Reconcile `expected_slugs` in `tests/test_propagate_master_assets.py` (`test_phase_review_agents_match_all_generated_harness_outputs`) against the final seven-agent roster
- [ ] Confirm the roster propagates to all three roots — `claude/`, `opencode/`, `codex/` (AC5)
- [ ] Add the **idempotency** assertion to `tests/test_propagate_master_assets.py`: two consecutive propagation runs, the second reports zero changes (AC8)
- [ ] Run propagation and inspect the diff for **unrelated noise** — noise usually means an identifier resolution changed; investigate before accepting (AC8)
- [ ] Final consistency pass on `tests/test_readiness_synthesis_agents.py` against the assembled roster
- [ ] Re-verify feature `07`'s AC5 on the assembled roster: **no status-line write-back anywhere in the family**

## Stage 3: End-to-End Dry Run

*Success criteria: AC1, AC2, AC3, AC4. Negative criterion: the forced-failure run must not produce `GO`.*

- [ ] Run the `05-pr-review` orchestrator against the pinned base/branch fixture in `dev/pr-review/fixtures/`
- [ ] Verify one `dev/pr-review/<base-sha-short>-<timestamp>/` directory contains: a change narrative, artifact/consistency/dependency findings, a test-health report, a diff-scoped security report from `04e-diff-security-scan`, and a severity-ordered readiness report (AC1)
- [ ] **Verify the reports are real, not not-run records.** Seven reports on disk. A run whose required evaluators report `not-run` does **not** satisfy AC1 — it is evidence the wiring is broken. This family has never demonstrably worked end to end; this is the first time it would
- [ ] Verify **exactly one question block**, then a written report with no further prompt (AC2). Verified on the assembled system, not per feature
- [ ] Verify **every** subagent return is ≤10 lines with full detail on disk (AC4)
- [ ] Re-run with **one evaluator forced to fail**: the run completes, the readiness report names the missing check and its reason under `Checks Not Run`, and the verdict is **not** `GO` (AC3)
- [ ] **In a scratch consumer repo, never this one:** verify behavior with `origin/HEAD` unset, base correction, no PR open, and `gh` unauthenticated
- [ ] Verify Claude, OpenCode, and Codex each load the propagated family without error
- [ ] **Do not fix findings the dry run surfaces about this repository.** They are outputs, not bugs

## Stage 4: Reconcile the Record

*Success criteria: AC9, AC10, AC11.*

- [ ] Run the full suite and reconcile the count against the 416 baseline: account for deletions from feature `02` and additions from features `01`–`07`. **A number that cannot be explained is not a baseline** (AC9)
- [ ] If PERF-01 fires, capture repeated runs and record it as the expected probabilistic Phase-04-owned gate. **Do not relax the budget to make it pass**
- [ ] Verify `.github/learnings/cross-phase-decisions.md` line 57's allowlist "forcing function" entry — already annotated with corrections at lines 58-59 — is **consistent with what actually shipped**. Correct any PR-Review Rescope claim that decomposition falsified (AC10)
- [ ] Record deferred capability: **per-agent command scoping** — needs a PreToolUse hook; not expressible on Claude via frontmatter; native only on OpenCode; absent per-profile on Codex. Record with routing, not as closed (AC11)
- [ ] Record deferred capability: the **`NO-GO` enforcement hook** — needs a hook-owning phase (AC11)
- [ ] Record **P5-SEC-02** with routing if feature `07` left it open (AC11)
- [ ] Confirm the security accounting reads honestly: `execute` removed where unneeded (feature `05`), never added where absent (feature `06`), retained only where a named command has no non-shell equivalent — with the remainder recorded open, not reworded into looking closed
- [ ] Confirm no `docs/phases/**` status line was written. Verdicts are issued by the user by hand

## Keep-it-clean checklist

- [ ] Dry run genuinely ran — seven reports on disk, not seven not-run records
- [ ] Sweep covers display names *and* informal prose forms, not only slugs
- [ ] Sweep is a test, not a one-time grep
- [ ] Propagation idempotent across two consecutive runs
- [ ] Deferred capabilities recorded with routing, not dropped
- [ ] Test count delta explained
