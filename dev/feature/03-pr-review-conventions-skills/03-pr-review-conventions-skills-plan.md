# 03 PR Review Conventions Skills

## Execution Metadata

- **Wave:** 3
- **Parallel safe:** no
- **Depends on:** 01-propagator-orphan-pruning, 02-retired-evaluator-removal
- **Key files modified:** `.github/skills/pr-review-conventions/SKILL.md` (renamed from `phase-final-review-conventions`), `.github/skills/pr-review-report/SKILL.md` (renamed from `phase-final-review-report`), `.github/agents/05a-baseline-worktree.agent.md`, `.github/agents/05b-change-narrator.agent.md` (skill reference only), `.github/agents/05g-artifact-sweeper.agent.md` (skill reference only), `.github/agents/05h-test-health.agent.md` (skill reference only), `.github/agents/05j-consistency-auditor.agent.md` (skill reference only), `.github/agents/05k-dependency-auditor.agent.md` (skill reference only), `.github/agents/05l-readiness-synthesizer.agent.md` (skill reference only), `.github/agents/05-phase-final-review.agent.md` (skill reference only), `tests/test_readiness_synthesis_agents.py`, generated `claude/skills/`, `opencode/skills/`, `codex/skills/`
- **Sequential reason:** runtime dependency on `01-propagator-orphan-pruning` (a skill directory rename orphans the Claude and OpenCode skill dirs, which only pruning removes); shares every surviving `05x` agent file with downstream features `04`–`07`

## Discovery Corrections to the Phase Document

The Phase document lists three skills under Deliverable 2 as though all three are
new authoring work. Codebase discovery contradicts that on two of three:

| Phase document says | Reality (verified 2026-07-16) |
|---|---|
| Author `pr-review-conventions` | **Rename + rescope** of the existing 152-line `.github/skills/phase-final-review-conventions/SKILL.md` |
| Author `pr-review-report` | **Rename + rescope** of the existing 218-line `.github/skills/phase-final-review-report/SKILL.md` |
| Author `worktree-baseline`, "candidate for reuse by `eval-grader`" | **Already exists, already generic, already propagated** to all three roots. Its own text states it is "intentionally independent of Phase Final Review and may be reused by evaluation or grading agents." **Zero changes required.** |

Likewise `05a-baseline-worktree` already accepts a *caller-specified* baseline
commit — it is not phase-shaped. The Phase document's framing ("check out the
confirmed merge-base commit in a git worktree; return the path") describes what it
already does. Its only phase-coupling is the prose "for the Phase Final Review
family" and its skill reference.

Net effect: Deliverable 2 is materially smaller than planned. This feature is a
rename and a rescope, not an authoring effort.

## A. Requirements & Traceability

### Acceptance Criteria

- **AC1** — `.github/skills/phase-final-review-conventions/` is renamed to
  `.github/skills/pr-review-conventions/`, with the `name:` frontmatter field
  updated to match. The skill's `description` states the diff/branch scope, not the
  phase/subphase scope.
- **AC2** — `.github/skills/phase-final-review-report/` is renamed to
  `.github/skills/pr-review-report/`, same treatment.
- **AC3** — The conventions skill's **Report Locations and Naming** section
  declares the report root `dev/pr-review/<base-sha-short>-<UTC-YYYYMMDDTHHMMSSZ>/`
  and the seven surviving report filenames. No path component may contain a branch
  name. The current tree of twelve report files plus four named rollups
  (`master-qa.md`, `security-rollup.md`, `ac-regression-matrix.md`) is replaced —
  three of those four rollups belonged to retired evaluators.
- **AC4** — Both skills are free of subphase concepts: no `PHASE_0N` report root,
  no subphase attribution, no per-subphase subdirectories, no artifact-inventory
  refusal, no archive-before-overwrite.
- **AC5** — The conventions skill states that **pipeline artifacts are optional
  enrichment**: a run proceeds on the diff alone and the report names which
  evidence was unavailable. This is the recorded boundary that keeps PR Review from
  duplicating `prod-code-review`, and it is a contract, not a preference.
- **AC6** — The ≤10-line return-summary contract and the reports-on-disk rule are
  retained verbatim in force. They are the phase's only defense against a
  long-lived branch blowing out context.
- **AC7** — **No surviving `05x` agent body references `phase-final-review-conventions`
  or `phase-final-review-report`.** The negative sweep is the operative clause.
  Agents that reference these skills today are retargeted to the renamed ones;
  agents that do not are left alone. In particular `05a-baseline-worktree`
  references only `worktree-baseline` and must **not** acquire a new skill load —
  the earlier phrasing ("every surviving agent references the renamed skills") read
  literally would force one, contradicting AC9.
- **AC8** — Both skills propagate cleanly to `claude/skills/`, `opencode/skills/`,
  and `codex/skills/`, and **the old skill directories are absent from all three
  generated roots** — via feature `01`'s pruning, not by hand.
- **AC9** — `worktree-baseline` is unchanged. If this feature modifies it, the
  change must be justified in the implementation record.

### Non-Goals

- Rescoping any evaluator's *behavior*. This feature updates skill references only;
  features `05`–`07` rescope evaluator content.
- Renumbering agents. `05g`/`05h`/`05j`/`05k`/`05l` keep their current slugs here
  and renumber in their own features.
- Renaming the orchestrator (`04-pr-review-orchestrator` owns that).
- Authoring `worktree-baseline` (it exists).
- Changing `auditor-conventions`, which both skills build on.

### Traceability

| Acceptance Criteria | Code Areas/Modules | Test / Evidence Category |
|---|---|---|
| AC1, AC2 | `.github/skills/pr-review-conventions/SKILL.md`, `.github/skills/pr-review-report/SKILL.md` | Must-have automated test (new) — skill existence + frontmatter |
| AC3, AC4, AC5, AC6 | both SKILL.md bodies | Must-have automated test (new) — content contract assertions |
| AC7 | all surviving `05x` agent bodies | Must-have automated test (new) — reference sweep |
| AC8 | `scripts/propagate_master_assets.py` prune | Must-have automated test (new) |
| AC9 | `.github/skills/worktree-baseline/SKILL.md` | Code-review evidence |

## B. Correctness & Edge Cases

**The skill rename is a delete-plus-create to the propagator, and no root prunes
skills today.** There is no rename detection. The `codex/skills/` prune at
`scripts/propagate_master_assets.py:1288` *looks* implemented but is **dead code**:
its guard is `startswith(GENERATED_SKILL_HEADER)` while a generated Codex `SKILL.md`
begins with `---` frontmatter and carries the marker on line 5 — **0 of 24 match**
(verified 2026-07-16). `claude/skills/` and `opencode/skills/` have no prune at all
and carry no marker whatsoever.

So without feature `01`, this rename strands
`phase-final-review-conventions/` and `phase-final-review-report/` in **all three**
generated roots — live, loadable skills for a scope that no longer exists. Feature
`01`'s AC4 owns both halves: repairing the dead Codex guard and adding
directory-name-keyed pruning for Claude and OpenCode. That is the hard dependency,
and it is larger than "two roots lack a prune."

**The report-file roster changes shape, not just names.** The conventions skill
currently names twelve `05x` report files plus four rollups. After retirement and
renumbering the roster is seven. Three of the four named rollups (`master-qa.md`,
`security-rollup.md`, `ac-regression-matrix.md`) were produced by retired
evaluators and must go; `readiness-report.md` survives. Renaming files without
re-deriving the roster would leave the skill promising artifacts nothing produces.

**Report filenames are forward references.** AC3 names the seven surviving reports
using their *new* `05a`–`05g` slugs, but the agents still carry old slugs until
features `05`–`07` land. This is intentional: the skill is the contract each
evaluator is then written against. The naming must be settled here or every
evaluator feature re-litigates it.

### Failure modes

| Mode | Handling |
|---|---|
| Old skill dirs survive in Claude/OpenCode roots | AC8, enforced by feature `01`; never hand-delete |
| An agent body still loads the old skill name | AC7 reference sweep; a stale reference is a silently missing skill at runtime, not an error |
| Report roster promises retired rollups | AC3 re-derives the roster from the surviving seven |
| A branch name reaches a report path | AC3 forbids it structurally — the key is a SHA and a timestamp, so no sanitizer is needed |
| `worktree-baseline` gets rescoped "for consistency" | AC9 — it is deliberately generic and shared with `eval-grader` |

## C. Consistency & Architecture Fit

Both skills already follow the house pattern: build on `auditor-conventions` for
shared audit norms, declare only the review-family contracts. Preserve that split.
`pr-review-report` mirrors `implementation-record` as a template skill.

Concrete names copied exactly from the Phase document: `pr-review-conventions`,
`pr-review-report`, `worktree-baseline`,
`dev/pr-review/<base-sha-short>-<UTC-YYYYMMDDTHHMMSSZ>/`.

Report filenames `[PROPOSED - name TBD]` — the existing convention is
`<evaluator-slug>-report.md`, which yields `05a-baseline-worktree-report.md` …
`05g-readiness-synthesizer-report.md`, plus `readiness-report.md` as the canonical
hand-off. Preserve the existing convention rather than inventing one.

## D. Clean Design & Maintainability

Simplest design: two `git mv` operations plus a content rescope. Resist expanding
the skills to cover the new orchestrator's interaction model — the upfront
question block belongs to the orchestrator, not to a shared evaluator contract.
Evaluators never ask questions.

**Complexity risk**: the conventions skill is a natural dumping ground for anything
"shared." Its scope is the evaluator contract: report locations, severity, return
size, read-only etiquette, model tiers, incomplete-run semantics. Base derivation
and PR posting are orchestrator concerns and must not migrate here.

### Keep-it-clean checklist

- [ ] Two renames, no third skill
- [ ] `worktree-baseline` untouched
- [ ] No orchestrator concerns in the conventions skill
- [ ] Report roster derived from the surviving seven, not edited from twelve
- [ ] Old skill dirs gone from all three roots by pruning

## E. Completeness: Observability, Security, Operability

**Observability decision** — None; skills are prose contracts with no runtime.

**Security** — The retained contracts *are* security-relevant and must not be
softened while the surrounding text is rewritten: read-only etiquette, "never treat
an unavailable evaluator as a clean result," and the recorded rule that a narrowly
scoped capability is always preferred to a broad grant. The `execute`-narrowing
deliverable was deleted from this phase (per-agent command scoping is not
expressible on Claude), which makes these prose contracts the *only* remaining
constraint on evaluator shell use. Weakening them here would be a real regression
with nothing behind it.

**Runbook** — Verify: propagation regenerates both skills in all three roots and
removes both old dirs. Rollback: `git revert`; skills are static assets.

## F. Test Plan

**Existing tests to update**
- `tests/test_readiness_synthesis_agents.py:11,12` assert
  `"phase-final-review-conventions"` and `"phase-final-review-report"` appear in
  `05l`'s body. They must assert the new names. (This file is further rewritten by
  `07-synthesis-and-pr-posting`.)

**Must-have automated tests (new)**

Top-value cases:

1. **Renamed skills exist and old ones do not.** Given the source tree, then
   `.github/skills/pr-review-conventions/SKILL.md` and
   `.github/skills/pr-review-report/SKILL.md` exist, and neither
   `phase-final-review-*` directory does.
2. **Old skill dirs pruned from all three generated roots (AC8).** The test that
   proves feature `01` handles skills, not just agents.
3. **No surviving agent references a retired skill name (AC7).** Sweep every
   `.github/agents/05*.agent.md` body.
4. **Report root contains no branch name (AC3).** Assert the declared root pattern
   is composed only of a SHA placeholder and a timestamp placeholder.
5. **Optional-artifact contract present (AC5).** Assert the conventions skill
   states artifacts are optional enrichment and that unavailable evidence is named
   in the report — the recorded boundary against `prod-code-review`.

**Test data / fixtures** — none.

## Unverified Assumptions

- That no consumer outside `.github/agents/05*` loads either skill by name.
  Verified for `.github/` and `tests/` by grep; **not** verified for
  user-local configuration outside this repository (e.g. a personal
  `~/.claude/` setup referencing the old skill name). Out of the repo's control;
  worth a line in the reconciliation feature's notes.

## Relationship to Sibling Plans

- **Depends on `01-propagator-orphan-pruning`** (hard: AC8) and
  **`02-retired-evaluator-removal`** (the five doomed agents would otherwise need
  their skill references updated before deletion).
- **Blocks `04`–`07`.** Every evaluator and the orchestrator are authored against
  these contracts; the report roster and filenames settled here are their inputs.
- **Shares files with `04`–`07`** — this feature touches each surviving `05x`
  agent's skill reference line; those features then rewrite the same files.
  Sequential for that reason.

## Stage 0: Test Prerequisites

**Goal**: Not required. Baseline 416 passed across 4 consecutive full runs
(2026-07-16).
**Success Criteria**: n/a
**Status**: Not required

## Stage 1: Settle the Report Contract

**Goal**: Derive the seven-report roster and the report root from the surviving
evaluator set; decide the fate of the four named rollups. Write it into
`pr-review-report` first, because every later feature consumes it.
**Success Criteria**: Roster and root documented; retired rollups removed; AC3.
**Status**: Not Started

## Stage 2: Rename and Rescope the Conventions Skill

**Goal**: `git mv` to `pr-review-conventions`; strip subphase concepts; add the
optional-artifact contract; retain the return-size, read-only, and
no-clean-result-from-absence rules verbatim.
**Success Criteria**: AC1, AC4, AC5, AC6.
**Status**: Not Started

## Stage 3: Rename and Rescope the Report Skill

**Goal**: `git mv` to `pr-review-report`; retarget templates from whole-phase to
branch-diff; drop retired-evaluator templates.
**Success Criteria**: AC2, AC4.
**Status**: Not Started

## Stage 4: Reconcile References and Prove Pruning

**Goal**: Update every surviving `05x` agent's skill reference and `05a`'s
phase-family prose; run propagation; confirm old skill dirs are gone from all three
roots.
**Success Criteria**: AC7, AC8, AC9; suite green.
**Status**: Not Started
