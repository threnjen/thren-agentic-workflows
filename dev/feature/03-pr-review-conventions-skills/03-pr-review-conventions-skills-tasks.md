# 03 PR Review Conventions Skills — Tasks

Read `03-pr-review-conventions-skills-context.md` before starting. The Discovery Delta
resolves the report roster (D1) and flags two upstream issues in feature `01` (D2, D4).

## Stage 0: Test Prerequisites

**Status: Not required.** Baseline 416 passed, 15 subtests passed across 4 consecutive full runs (2026-07-16).

- [x] Confirm features `01-propagator-orphan-pruning` and `02-retired-evaluator-removal` are merged before starting — both are hard dependencies
- [x] Confirm feature `01` actually prunes skill directories from **all three** generated roots, including `codex/`. Per Discovery Delta D2 the pre-existing codex prune guard at `scripts/propagate_master_assets.py:1293` is dead code (`startswith(GENERATED_SKILL_HEADER)` is never true; the marker sits on line 5, behind frontmatter). If `01` did not fix it, stop and escalate — AC8 cannot pass
- [x] Run `.venv/bin/python -m pytest tests/ -q` and record the starting count (it will differ from 416 — feature `02` deletes retired-agent tests)

## Stage 1: Settle the Report Contract

**Goal**: Derive the seven-report roster and report root from the surviving evaluator set; decide the fate of the four named rollups. Write it into `pr-review-report` first — every later feature consumes it.
**Success Criteria**: Roster and root documented; retired rollups removed; AC3.

- [x] Confirm the surviving evaluator set is exactly seven: `05a`, `05b`, `05g`, `05h`, `05j`, `05k`, `05l` (verified — `05c`/`05d`/`05e`/`05f`/`05i` deleted by feature `02`)
- [x] Adopt the resolved report roster from the context file's **Report Roster** section. Do not re-derive it and do not invent the `05c`–`05f` ordering — the map is fixed by sibling plans `05`/`06`/`07` (`05g`→`05c`, `05j`→`05d`, `05k`→`05e`, `05h`→`05f`, `05l`→`05g`)
- [x] Declare the report root `dev/pr-review/<base-sha-short>-<UTC-YYYYMMDDTHHMMSSZ>/` — copied exactly from the Phase document. No path component may contain a branch name (AC3)
- [x] Remove `master-qa.md`, `security-rollup.md`, and `ac-regression-matrix.md` from the roster — all three were produced by retired evaluators. Retain `readiness-report.md` as the canonical hand-off
- [x] Preserve the existing `<evaluator-slug>-report.md` filename convention rather than inventing a new one
- [x] Verify the roster was re-derived from the surviving seven, not edited down from the current twelve

## Stage 2: Rename and Rescope the Conventions Skill

**Goal**: `git mv` to `pr-review-conventions`; strip subphase concepts; add the optional-artifact contract; retain the return-size, read-only, and no-clean-result-from-absence rules verbatim.
**Success Criteria**: AC1, AC4, AC5, AC6.

- [x] `git mv .github/skills/phase-final-review-conventions .github/skills/pr-review-conventions` (AC1)
- [x] Update the `name:` frontmatter field to `pr-review-conventions` to match the directory (AC1) — per the debugging learning, the directory and the `name:` value must match exactly or the skill silently fails to load
- [x] Rewrite the `description:` frontmatter to state the **diff/branch** scope, not the phase/subphase scope, and retarget its `Use when:` clause off "05x Phase Final Review evaluator" (AC1)
- [x] Retitle the body and rewrite the intro (currently "Load this skill before performing work for a multi-subphase phase" / "defines only the whole-phase review contracts") for branch-diff scope (AC4)
- [x] Replace the **Report Locations and Naming** section with the Stage 1 roster and root (AC3)
- [x] Strip all subphase concepts (AC4): the `dev/phase-final-review/PHASE_0N/` root, subphase attribution, per-subphase subdirectories, the artifact-inventory refusal, and archive-before-overwrite. Includes the "A report for a discovered subphase may use a subdirectory" allowance and the subphase columns in the **Missing Artifacts and Preflight** section
- [x] Rescope the **Severity Levels** table header from "Meaning in a whole-phase review" to branch-diff scope, keeping the four levels and their meanings intact (AC4)
- [x] Add the **optional-artifact contract** (AC5): pipeline artifacts are optional enrichment, a run proceeds on the diff alone, and the report names which evidence was unavailable. Record it as the boundary against duplicating `prod-code-review` — it is a contract, not a preference
- [x] Retain **verbatim in force** (AC6, and plan §E — these are the only remaining constraint on evaluator shell use now that `execute`-narrowing is out of the phase):
  - [x] the ≤10-line **Return Summary Contract** and the reports-on-disk rule
  - [x] the **Read-Only Worktree Etiquette** section
  - [x] "Do not treat an unavailable evaluator, dependency, or worktree as a clean result"
  - [x] the preference for a narrowly scoped capability over a broad grant
- [x] Keep the `auditor-conventions` build-on reference and the split it implies — declare only review-family contracts (explicit non-goal: do not change `auditor-conventions`)
- [x] Keep the `worktree-baseline` reference in **Read-Only Worktree Etiquette** pointing at the unchanged skill name (AC9)
- [x] Verify no orchestrator concerns migrated in — base derivation, PR posting, and the upfront question block belong to the orchestrator. Evaluators never ask questions
- [x] Update the **Handoff Checklist** report-root line and the **Process** step 1 ("Confirm the assigned phase, subphase scope...")

## Stage 3: Rename and Rescope the Report Skill

**Goal**: `git mv` to `pr-review-report`; retarget templates from whole-phase to branch-diff; drop retired-evaluator templates.
**Success Criteria**: AC2, AC4.

- [x] `git mv .github/skills/phase-final-review-report .github/skills/pr-review-report` (AC2)
- [x] Update the `name:` frontmatter to `pr-review-report` and rewrite the `description:` — it currently advertises "the four Phase Final Review hand-off reports: master QA, security rollup, AC regression, and readiness," three of which are being deleted (AC2)
- [x] Update the body's `phase-final-review-conventions` load reference to `pr-review-conventions` (AC2, AC7)
- [x] Delete template **1. Master QA Document** — produced by retired `05c-qa-consolidator` (AC3)
- [x] Delete template **2. Security Rollup** — produced by retired `05d-security-rollup` (AC3)
- [x] Delete template **3. Acceptance-Criteria Regression Matrix** — produced by retired `05e-ac-regression` (AC3)
- [x] Retain template **4. Go/No-Go Readiness Report**, retargeted from whole-phase to branch-diff: replace `<PHASE_0N>` tokens, the report root, and the subphase-keyed fields with base/head diff equivalents (AC2, AC4)
- [x] Update the readiness template's **Coverage and Evidence** table — its Master QA / Security rollup / AC regression matrix rows reference reports that will no longer exist (AC3)
- [x] Retarget the **Output Rules** section's `dev/phase-final-review/PHASE_0N/` write path to the Stage 1 root (AC3, AC4)
- [x] Preserve the severity-ordering rule, the `Not run` rule, the 10-line return cap reference, and "missing evidence is never an implicit clean result" (AC6)
- [x] Confirm the skill still mirrors `implementation-record` as a template skill

## Stage 4: Reconcile References and Prove Pruning

**Goal**: Update every surviving `05x` agent's skill reference and `05a`'s phase-family prose; run propagation; confirm old skill dirs are gone from all three roots.
**Success Criteria**: AC7, AC8, AC9; suite green.

- [x] Update skill references in each surviving agent (skill-reference lines **only** — rescoping evaluator behavior is an explicit non-goal owned by features `05`–`07`):
  - [x] `05-phase-final-review.agent.md` — lines 21, 22, 60, 156, 214–215
  - [x] `05b-change-narrator.agent.md` — lines 15, 58
  - [x] `05g-artifact-sweeper.agent.md` — lines 15, 16
  - [x] `05h-test-health.agent.md` — lines 15, 16
  - [x] `05j-consistency-auditor.agent.md` — lines 15, 16
  - [x] `05k-dependency-auditor.agent.md` — lines 15, 16
  - [x] `05l-readiness-synthesizer.agent.md` — lines 14, 15, 22, 75
- [x] Update `05a-baseline-worktree.agent.md` **line 8 prose only** ("the Phase Final Review family"). Per Discovery Delta D3, `05a` references only `worktree-baseline` — it has no old-skill reference. **Do not add** a `pr-review-conventions` load line to `05a`, and do not touch its `worktree-baseline` references (AC9)
- [x] Do **not** update `dev/phase-final-review/PHASE_0N/` report roots inside agent bodies (D6) — features `04`–`07` own those. The skills-vs-agents root mismatch is intentional and temporary
- [x] Update `tests/test_readiness_synthesis_agents.py:12-13` to assert `"pr-review-conventions"` and `"pr-review-report"` in `05l`'s body (this file is rewritten again by `07-synthesis-and-pr-posting`)
- [x] Verify `.github/skills/worktree-baseline/SKILL.md` is byte-identical to its pre-feature state (AC9). If it changed, justify in the implementation record
- [x] Verify `.github/skills/auditor-conventions/SKILL.md` is unchanged
- [x] Run propagation and confirm both renamed skills regenerate in `claude/skills/`, `opencode/skills/`, and `codex/skills/` (AC8)
- [x] Confirm `phase-final-review-conventions/` and `phase-final-review-report/` are absent from all three generated roots — **via feature `01`'s pruning, never by hand-deleting** (AC8)
- [x] Run `.venv/bin/python -m pytest tests/ -q`; suite green. Explain any count change rather than merely observing it

### Tests to add

- [x] **Renamed skills exist and old ones do not (AC1, AC2).** `.github/skills/pr-review-conventions/SKILL.md` and `.github/skills/pr-review-report/SKILL.md` exist; neither `phase-final-review-*` skill directory does
- [x] **Frontmatter matches directory (AC1, AC2).** Each renamed skill's `name:` equals its directory name
- [x] **Old skill dirs pruned from all three generated roots (AC8).** The test that proves feature `01` handles skills, not just agents. Per D2, assert `codex/` explicitly — do not assume the pre-existing codex prune works. Per D7, write a new test rather than extending the generic `demo-skill` fixture in `tests/test_propagate_master_assets.py`
- [x] **No surviving agent references a retired skill name (AC7).** Sweep every `.github/agents/05*.agent.md` body. Per D5, match the **exact tokens** `phase-final-review-conventions` and `phase-final-review-report` — a substring sweep on `phase-final-review` will fail against report-root strings and the orchestrator filename, which are out of scope here
- [x] **Report root contains no branch name (AC3).** Assert the declared root pattern is composed only of a SHA placeholder and a timestamp placeholder
- [x] **Optional-artifact contract present (AC5).** Assert the conventions skill states artifacts are optional enrichment and that unavailable evidence is named in the report — the recorded boundary against `prod-code-review`
- [x] **Retained contracts survive (AC6).** Assert the ≤10-line return cap, read-only etiquette, and the no-clean-result-from-absence rule are still present in the conventions skill

No test data or fixtures required.

## Keep-it-clean Checklist (from plan §D)

- [x] Two renames, no third skill
- [x] `worktree-baseline` untouched
- [x] No orchestrator concerns in the conventions skill
- [x] Report roster derived from the surviving seven, not edited from twelve
- [x] Old skill dirs gone from all three roots by pruning

## Implementation Record Notes

- [x] Record any deviation from the resolved report roster and why
- [x] Record the test-count delta and its cause
- [x] If `worktree-baseline` changed at all, justify it (AC9)
- [x] Carry forward the unverified assumption: no consumer outside `.github/agents/05*` loads either skill by name — verified for `.github/`, `tests/`, and `scripts/`, **not** for user-local config outside this repo (e.g. a personal `~/.claude/`). Route to `08-retirement-reconciliation`
