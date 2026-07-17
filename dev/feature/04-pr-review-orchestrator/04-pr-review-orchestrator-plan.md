# 04 PR Review Orchestrator

## Execution Metadata

- **Wave:** 4
- **Parallel safe:** no
- **Depends on:** 01-propagator-orphan-pruning, 03-pr-review-conventions-skills
- **Key files modified:** `.github/agents/05-pr-review.agent.md` (renamed from `05-phase-final-review.agent.md`), `dev/pr-review/fixtures/` (new pinned SHA pair), `.gitignore`, `tests/test_pr_review_orchestrator.py` `[PROPOSED - name TBD]` (new), `tests/test_propagate_master_assets.py`, generated `claude/agents/`, `claude/commands/`, `opencode/agents/`, `codex/agents/`, `codex/profiles/`
- **Sequential reason:** runtime dependency on `03-pr-review-conventions-skills` (authored against its report contract); renaming the orchestrator orphans `claude/commands/phase-final-review.md`, which requires `01-propagator-orphan-pruning`; shares `tests/test_propagate_master_assets.py` with upstream features

## Scope Move from the Phase Document

The Phase document groups the pinned base/branch fixture into Deliverable 2
(skills + `05a`). It lands here instead. The fixture is a *base/branch SHA pair* —
it has meaning only in terms of base derivation, which this feature owns, and its
first consumer is this feature's dry run. Feature `03` owns contracts; this feature
owns the thing the contracts are exercised against.

The Phase document also groups the `04e-diff-security-scan` delegation seam into
Deliverable 5. It lands here: the seam *is* an orchestrator invocation, and the
orchestrator must declare its complete evaluator roster in one place. Splitting the
roster across two features would mean two features editing the same fan-out list.

## A. Requirements & Traceability

### Acceptance Criteria

- **AC1** — `.github/agents/05-phase-final-review.agent.md` is renamed to
  `.github/agents/05-pr-review.agent.md`, with `name:` updated from
  `05 Phase - Final Review` to a PR Review name and `description:` restated to the
  branch-diff scope.
- **AC2** — **Single upfront interaction.** All questions the run can ask are asked
  once, before any evaluator work, in one block: (a) the model-tier warning when
  the active model is not state of the art; (b) the suggested base and its
  derivation source, for confirmation or correction; (c) the PR-comment choice —
  post automatically / ask once the report is written / never. **After that block,
  no code path may introduce a new prompt** — including evaluator failure, timeout,
  absent `gh`, and no-PR-exists.
- **AC3** — **Base suggestion order** is `refs/remotes/origin/HEAD` → `origin/main`
  → `origin/master` → present candidate branches and require a selection. The
  derivation source is shown with the suggestion.
- **AC4** — **The suggester excludes the current branch and its own
  remote-tracking ref.** Both report HEAD as their own merge-base, so any ranking
  over candidates that omits this filter returns the branch under review. Verified
  on `repo_improvements_project` at `ae9823a`: `git merge-base HEAD main` →
  `e3398c7`, but `git merge-base HEAD repo_improvements_project` → `ae9823a`.
- **AC5** — The confirmation prompt names the three cases where the suggestion is
  actively wrong: a branch cut from another feature branch, a rebased branch, and a
  squash-merged base. Correction is first-class, not an escape hatch.
- **AC6** — A user-supplied base override replaces the suggestion, and the
  corrected `git merge-base HEAD <base>` reaches **every** downstream evaluator.
- **AC7** — Reports are written under
  `dev/pr-review/<base-sha-short>-<UTC-YYYYMMDDTHHMMSSZ>/`. No branch name appears
  in any path component.
- **AC8** — **Deleted, not rewritten:** subphase discovery and its refusal message;
  ledger reading (`eval/runs/*/ledger-commits.jsonl`), multi-run disambiguation,
  and the `eval:` commit-message fallback; the artifact-inventory refusal gate; the
  entire verdict write-back path (the two-file transactional edit of
  `PROJECT_ROADMAP.md` + `PHASE_0N_SUMMARY.md`, its unique-match ambiguity
  detection, and its restore-on-second-write-failure); and archive-before-overwrite.
  None of these may survive in any form.
- **AC9** — **The agent writes no status line** in `PROJECT_ROADMAP.md` or any
  phase summary on any path. Verdicts are issued by the user by hand.
- **AC10** — The orchestrator declares the full roster in **three distinct
  positions**, which "fans out to `05a`–`05g`" wrongly conflates:

  | Position | Agents | When |
  |---|---|---|
  | Preflight | `05a-baseline-worktree` | before fan-out; its failure stops the run |
  | Fan-out (concurrent) | `05b`, `05c`, `05d`, `05e`, `05f` + `04e-diff-security-scan` | **six**, after the base is confirmed |
  | Synthesis | `05g-readiness-synthesizer` | last; consumes reports + status records |

  `05a` is not a fan-out evaluator (nothing can run before the baseline exists) and
  `05g` is not one either (it consumes the others' output). Stating this as a flat
  range makes AC10 contradict AC11's partial-failure semantics, under which an
  evaluator failure never aborts the run — but an `05a` failure must.
  No new security agent is authored.
- **AC10b** — **`.gitignore` is updated so the fixture is trackable and run output
  is not.** `.gitignore` currently ignores `dev/*` and un-ignores only
  `dev/phase-final-review/fixtures/**`, so `dev/pr-review/fixtures/` would be
  silently untracked — AC13 fails invisibly, and the dry run's report output would
  otherwise pollute the tree and confound propagation-idempotency checks in
  `08-retirement-reconciliation`. Un-ignore the fixture path; keep
  `dev/pr-review/<sha>-<timestamp>/` run output ignored.
- **AC11** — Partial-failure semantics retained: an evaluator failure never aborts
  the run and never becomes a passing result; each gets an `evaluator-status.jsonl`
  record naming evaluator, check, reason, and report (`null` when none); the bounded
  wait is retained; **the verdict can never be GO while any check is missing.**
- **AC12** — The orchestrator never reads code or diffs; it inspects path metadata
  and reads only structured reports under the run's report root. Every subagent
  return is ≤10 lines.
- **AC13** — A pinned base/branch SHA pair from this repository's own history
  exists as a fixture, sufficient for a dry run of every evaluator.
- **AC14** — The renamed orchestrator propagates to all three roots, and
  `claude/commands/phase-final-review.md` is **absent** — via feature `01`'s
  pruning. A stale command file would leave a live slash command pointing at a
  deleted agent.

### Non-Goals

- Implementing `gh` posting. The *choice* is captured here (AC2c); the posting path
  is `07-synthesis-and-pr-posting`.
- Rescoping any evaluator's internals (features `05`–`07`).
- Narrowing any `execute` grant. Per-agent command scoping is not expressible on
  Claude; the phase's allowlist deliverable was deleted for that reason (recorded
  in `.github/learnings/cross-phase-decisions.md`). The orchestrator retains
  `execute` because base derivation needs `git`.
- Any hook work, including an enforcement hook on the verdict. Advisory only.
- Reading PR comments or any network-sourced text back into the agent. Output is
  one-way; ingestion is a prompt-injection surface.

### Traceability

| Acceptance Criteria | Code Areas/Modules | Test / Evidence Category |
|---|---|---|
| AC1, AC14 | `.github/agents/05-pr-review.agent.md`; generated roots | Must-have automated test (new) |
| AC2 | orchestrator body — upfront block | Must-have automated test (new) — contract assertions; **manual QA** for the live single-interaction proof |
| AC3, AC4, AC5, AC6 | orchestrator body — base derivation | Must-have automated test (new); **live QA in a scratch repo** for `origin/HEAD` unset |
| AC7 | orchestrator body — report root | Must-have automated test (new) |
| AC8, AC9 | orchestrator body — deletions | Must-have automated test (new) — absence assertions |
| AC10 | orchestrator body — roster | Must-have automated test (new) |
| AC11, AC12 | orchestrator body | Must-have automated test (new) |
| AC13 | `dev/pr-review/fixtures/` | Code-review evidence + dry-run |

## B. Correctness & Edge Cases

**Base derivation is the phase's central risk, and git cannot help.** A ref is a
SHA with no parentage. The reflog records `branch: Created from HEAD` — the SHA,
never the branch name — and is local-only, never cloned, and gc-pruned at 90 days.
`git symbolic-ref refs/remotes/origin/HEAD` names the remote's *default* branch,
not this branch's base, and is frequently unset in fresh clones. There is no
correct algorithm; there is only suggest-and-confirm.

**The self-exclusion trap (AC4) is the subtle one** because the naive heuristic
looks obviously right. "Pick the branch whose merge-base with HEAD is nearest"
ranks the current branch first, every time, with a merge-base of HEAD itself — and
a diff of nothing. A run that silently reviews an empty diff and reports no
findings is the worst possible failure: it looks like a pass.

### Failure modes

| Mode | Handling |
|---|---|
| `origin/HEAD` unset | Fall back `origin/main` → `origin/master` → present candidates. Never guess. **Live QA in a scratch repo.** |
| No remote at all | Fall through to candidate presentation over local branches, still excluding self |
| Suggested base is wrong (feature-branch parent, rebase, squash-merge) | Named in the prompt (AC5); correction is first-class (AC6) |
| Base has no merge-base with HEAD (unrelated histories, squash-merged base) | Report the condition; do not fabricate a range. This is a stop, not a silent empty diff |
| Evaluator fails / times out / dependency unavailable | AC11 — record, continue, cap the verdict below GO |
| Diff is enormous (long-lived branch) | AC12 — ≤10-line returns, reports on disk, orchestrator never reads code |
| Two runs in the same second | Report root is SHA + timestamp; a collision means the same base at the same second. Accept, or add a sequence suffix — decide and record |
| A question fires after the block | AC2 forbids it. This is the requirement most likely to erode silently |

## C. Consistency & Architecture Fit

Follow the numbered-orchestrator house style of `04-phase-execute` + lettered
subagents: coordinate subagents, fail loudly at preflight boundaries, never do
evaluator work inline. The existing `05-phase-final-review.agent.md` already
embodies this style — the preflight checklist, invocation shape, model-tier table,
`evaluator-status.jsonl` contract, and bounded-wait semantics are all reusable.
**Rescope it; do not rewrite it from scratch.** The parts that survive are the
parts that were never about phases.

The existing preflight is a four-step checklist (baseline, subphase discovery,
artifact inventory, model-tier). Steps 2 and 3 are deleted (AC8); step 1 is
replaced by base suggest-and-confirm; step 4 survives. The result is a two-step
preflight, and both remaining questions merge into the single upfront block.

Concrete names copied exactly from the Phase document: `05-pr-review`,
`dev/pr-review/<base-sha-short>-<UTC-YYYYMMDDTHHMMSSZ>/`, `04e-diff-security-scan`.
`[PROPOSED - name TBD]`: the agent's `name:` frontmatter value (`05 PR - Review`
follows the `05 Phase - Final Review` pattern but is not codebase-verified) and the
fixture file path under `dev/pr-review/fixtures/`.

**Renaming interacts with propagation identity.** `_claude_filename_for` resolves
an output filename against stems already on disk, and `_build_agent_reference_map`
rewrites agent *display names* in prose. Changing `name:` changes how every other
agent's references to it are rewritten. Verify all three roots after the rename
rather than assuming a clean regeneration.

## D. Clean Design & Maintainability

The simplest design is subtractive. The current orchestrator is ~180 lines of
preflight, ledger parsing, artifact inventory, and write-back; the rescoped one is
a base confirmation, a fan-out, and a report path. **Deleting the write-back path
is the single highest-value action in this phase** — it was the riskiest
implemented code (two-file transactional edits with restore-on-failure) and the
rescope leaves it with no reason to exist.

**Complexity risk**: the upfront block will attract "just one more question." Each
addition is individually reasonable and collectively fatal to the unattended-run
property. The rule is structural: after the block, the run reaches a report or it
records a failure — it never asks.

**Duplication risk**: report templates and severity levels live in
`pr-review-report` / `pr-review-conventions`. Do not restate them here.

### Keep-it-clean checklist

- [ ] Ledger, subphase, artifact-inventory, write-back, archive code all gone —
      not commented out, not behind a flag
- [ ] Preflight is two steps
- [ ] Exactly one interaction block
- [ ] No report templates restated in the orchestrator
- [ ] Model-tier table re-derived for the seven-evaluator roster

## E. Completeness: Observability, Security, Operability

**Observability decision** — Retain `evaluator-status.jsonl` exactly as specified;
it is the machine-readable record that stops a missing check from reading as a
clean one, and it is `05g`'s input for the `Checks Not Run` section. Add no other
logging. Do **not** record model or harness identity in retained reports — an
existing constraint in the current agent, and it survives the rescope.

**Security** —
- The orchestrator holds `execute`, which on Claude is unrestricted Bash. This is
  **not** narrowable: subagent frontmatter accepts only bare tool names, and
  `tools: Bash(git:*)` is an unresolved tool name that makes Claude Code refuse to
  launch the agent. It is required for base derivation. Recorded as a residual risk
  with routing to a hook-owning phase, per the recorded rule that a phase records a
  finding rather than redefining it to fit the scope.
- One-way output only. Never read PR comments or other network-sourced text back
  in.
- The report root is keyed by SHA and timestamp precisely so no branch name — an
  attacker-influenceable string — reaches a filesystem path. There is no sanitizer
  because there is nothing to sanitize.

**Runbook** — Verify: dry run against the pinned fixture reaches a report with one
interaction. Rollback: `git revert`; the agent is a static asset.

## F. Test Plan

**Existing tests to update**
- `tests/test_propagate_master_assets.py` — any reference to the orchestrator's old
  slug or display name.

**Must-have automated tests (new)** — contract assertions over the agent body, in
the style already established by `tests/test_readiness_synthesis_agents.py`.

Top-value cases:

1. **Deleted machinery stays deleted (AC8).** Assert the body contains no
   `ledger-commits.jsonl`, no `PROJECT_ROADMAP.md` write-back, no subphase
   discovery, no archive path. An absence test is the only thing that stops the
   riskiest deleted code from being helpfully reintroduced.
2. **Self-exclusion is declared (AC4).** Assert the body states that the current
   branch and its remote-tracking ref are excluded from base candidates.
3. **Fallback chain in order (AC3).** Assert `origin/HEAD`, `origin/main`,
   `origin/master`, and candidate presentation appear in that order.
4. **Single interaction (AC2).** Assert the body declares that no prompt occurs
   after the upfront block, and that all three questions are named within it.
5. **Report root has no branch component (AC7).** Assert the declared root is
   SHA + timestamp only.

**Manual QA checks** (behavioral; cannot be asserted from a Markdown body):
- Dry run against the pinned fixture: one interaction, then a report.
- **Live QA in a scratch consumer repo, never this one**: `origin/HEAD` unset;
  base correction accepted and propagated to evaluators; no-remote fallback.

**Test data / fixtures** — the pinned base/branch SHA pair (AC13).

**Fixture sizing correction.** The plan's "a PR fixture is two commits" understates
it. The pair implied by AC4's evidence, `e3398c7..ae9823a`, is **242 files and ~27k
insertions** — a whole-phase diff, not a PR-shaped one. Dry-running seven
evaluators against that is slow, expensive, and a poor proxy for the review this
agent is for. **Select a smaller, genuinely PR-shaped pair** with enough substance
for each evaluator to find something (a debug artifact, a convention drift, a
dependency change, a test delta) and record why the pair was chosen. Size the
fixture to the job; do not inherit `e3398c7..ae9823a` just because it appears in the
base-derivation evidence, where it served a different purpose.

## Unverified Assumptions

- That `05a`–`05g` slugs exist at the time this feature lands. They do **not** —
  features `05`–`07` renumber them. The orchestrator's roster is therefore a
  forward reference authored against feature `03`'s settled contract. Narrow, and
  resolved by the end of wave 6; `08-retirement-reconciliation` verifies it.
- That the `name:` change does not break `_rewrite_agent_references` for other
  agents referencing this orchestrator. Verify against all three generated roots
  after the rename.

## Relationship to Sibling Plans

- **Depends on `03-pr-review-conventions-skills`** — authored against its report
  roster, root, and return contract.
- **Depends on `01-propagator-orphan-pruning`** — AC14; the orphaned command file
  is the sharpest case, since it stays user-invocable.
- **Blocks `05`, `06`, `07`** — each evaluator is dry-run through this orchestrator
  as it lands.
- **`07-synthesis-and-pr-posting` edits this file again** to add the posting path,
  which is why that feature is `parallel_safe: no`.

## Stage 0: Test Prerequisites

**Goal**: Not required. Baseline 416 passed across 4 consecutive full runs
(2026-07-16).
**Success Criteria**: n/a
**Status**: Not required

## Stage 1: Pin the Fixture

**Goal**: Select and pin a base/branch SHA pair from this repo's history with a
non-trivial diff — enough for every evaluator to find something. Record why the
pair was chosen.
**Success Criteria**: AC13; `git merge-base` over the pair resolves to the pinned
base.
**Status**: Not Started

## Stage 2: Subtract

**Goal**: Delete subphase discovery, ledger parsing and fallback, artifact
inventory, verdict write-back, and archiving from the orchestrator body.
**Success Criteria**: AC8, AC9; the absence tests pass.
**Status**: Not Started

## Stage 3: Base Suggest-and-Confirm

**Goal**: Replace preflight step 1 with the suggestion chain, self-exclusion, the
three wrong-suggestion cases, and override propagation.
**Success Criteria**: AC3–AC6.
**Status**: Not Started

## Stage 4: One Interaction, One Roster

**Goal**: Merge the model-tier warning, base confirmation, and PR-comment choice
into a single upfront block; declare the seven-evaluator roster plus the `04e`
seam; re-derive the model-tier table.
**Success Criteria**: AC2, AC10, AC11, AC12.
**Status**: Not Started

## Stage 5: Rename, Propagate, Dry-Run

**Goal**: Rename the file and agent; propagate; confirm the stale command file is
pruned; dry-run against the fixture.
**Success Criteria**: AC1, AC7, AC14; one interaction to a report; suite green.
**Status**: Not Started
