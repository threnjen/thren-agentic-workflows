# 04 PR Review Orchestrator — Tasks

## Stage 0: Test Prerequisites

**Status:** Not required — baseline 416 passed across 4 consecutive full runs (2026-07-16).

- [x] Confirm the baseline before starting: `.venv/bin/python -m pytest tests/ -q` → 416 passed, 15 subtests passed (system `python3` has no pytest)
- [x] Confirm features `01`, `02`, and `03` have landed — this feature is authored against `03`'s report contract and depends on `01`'s pruning for AC14
- [x] Note the working tree is **not** clean: `dev/phase-final-review/fixtures/**` (14 tracked files) are deleted but uncommitted, and `.github/learnings/cross-phase-decisions.md` is modified. Confirm whether the old fixture's deletion belongs to feature `02`/`08` before touching it here

## Stage 1: Pin the Fixture

**Goal:** Select and pin a base/branch SHA pair from this repo's history with a non-trivial diff. **Success Criteria:** AC13; `git merge-base` over the pair resolves to the pinned base.

- [x] Add un-ignore rules to `.gitignore` for `dev/pr-review/`, mirroring the existing four-rule `dev/phase-final-review/` pattern (`!dev/pr-review/`, `dev/pr-review/*`, `!dev/pr-review/fixtures/`, `!dev/pr-review/fixtures/**`). **Without this, AC13's fixture cannot be committed** — `dev/*` at `.gitignore:5` ignores it. The pattern correctly keeps the AC7 report root `dev/pr-review/<sha>-<ts>/` ignored while tracking fixtures
- [x] Verify the rules work: `git check-ignore -v dev/pr-review/fixtures/<file>` returns no match, and `git check-ignore -v dev/pr-review/abc1234-20260716T120000Z/report.md` still matches
- [x] Select a base/branch SHA pair from this repository's history with a **bounded** diff — non-trivial enough that every evaluator finds something, small enough for a cheap dry run. Do **not** default to `e3398c7..ae9823a` (5 commits, 242 files, 27,041 insertions); the plan's Section F expects roughly two commits
- [x] Pin the pair under `dev/pr-review/fixtures/` `[PROPOSED - name TBD]`, recording both SHAs, the commit count, and the diffstat
- [x] Record **why** the pair was chosen — which evaluators it exercises and what each should find
- [x] Verify `git merge-base <branch-sha> <base-sha>` resolves to the pinned base
- [x] Confirm the fixture files are actually tracked: `git status --porcelain dev/pr-review/fixtures/` shows them as added, not ignored

## Stage 2: Subtract

**Goal:** Delete subphase discovery, ledger parsing and fallback, artifact inventory, verdict write-back, and archiving. **Success Criteria:** AC8, AC9; absence tests pass.

- [x] Delete preflight step 2 (subphase discovery) and its refusal message from the orchestrator body
- [x] Delete preflight step 3 (artifact inventory) and its `MISSING — ...` refusal gate
- [x] Delete all ledger reading from preflight step 1: `eval/runs/*/ledger-commits.jsonl`, `ledger-events.jsonl`, multi-run disambiguation, and the `eval:` commit-message fallback
- [x] Delete the entire **Verdict Lifecycle and Write-back** section: the two-file transactional edit of `PROJECT_ROADMAP.md` + `PHASE_0N_SUMMARY.md`, its unique-match ambiguity detection, and its restore-on-second-write-failure path (AC9)
- [x] Delete archive-before-overwrite from **Re-invocation and Report Retention** — every run owns its own directory, so archiving has no reason to exist
- [x] Verify none of the deleted machinery survives **in any form** — not commented out, not behind a flag, not as a "deprecated" note (AC8)
- [x] Write absence tests asserting the body contains no `ledger-commits.jsonl`, no `PROJECT_ROADMAP.md` write-back, no subphase discovery, and no archive path. **This is the only thing that stops the riskiest deleted code from being helpfully reintroduced**
- [x] Decide the home for this feature's new contract assertions — `tests/test_pr_review_orchestrator.py` `[PROPOSED - name TBD]` or an addition to an existing file — and record the choice in the implementation record. Follow the pytest style of `tests/test_readiness_synthesis_agents.py` (module-level `Path` constants + plain `assert`), not the `unittest` style of `tests/test_propagate_master_assets.py`

## Stage 3: Base Suggest-and-Confirm

**Goal:** Replace preflight step 1 with the suggestion chain, self-exclusion, the three wrong-suggestion cases, and override propagation. **Success Criteria:** AC3–AC6.

- [x] Replace preflight step 1 with the base suggestion chain in order: `refs/remotes/origin/HEAD` → `origin/main` → `origin/master` → present candidate branches and require a selection (AC3)
- [x] State that the derivation source is shown alongside the suggestion (AC3)
- [x] Declare explicitly that **the suggester excludes the current branch and its own remote-tracking ref** from base candidates, because both report HEAD as their own merge-base (AC4)
- [x] Record the verified evidence for the self-exclusion rule: on `repo_improvements_project` at HEAD `ae9823a`, `git merge-base HEAD main` → `e3398c7`, but `git merge-base HEAD repo_improvements_project` → `ae9823a` (HEAD itself, a diff of nothing)
- [x] Name the three cases where the suggestion is actively wrong in the confirmation prompt: a branch cut from another feature branch, a rebased branch, and a squash-merged base. Frame correction as first-class, not an escape hatch (AC5)
- [x] Specify that a user-supplied base override replaces the suggestion and that the corrected `git merge-base HEAD <base>` reaches **every** downstream evaluator (AC6)
- [x] Handle the no-remote case: fall through to candidate presentation over local branches, still excluding self
- [x] Handle the no-merge-base case (unrelated histories, squash-merged base): report the condition and **do not fabricate a range**. This is a stop, not a silent empty diff
- [x] Write tests asserting the fallback chain appears in order (AC3) and that self-exclusion is declared (AC4)

## Stage 4: One Interaction, One Roster

**Goal:** Merge the three questions into a single upfront block; declare the roster; re-derive the model-tier table. **Success Criteria:** AC2, AC10, AC11, AC12.

- [x] Merge all three questions into one upfront block before any evaluator work: (a) the model-tier warning when the active model is not state of the art, (b) the suggested base and its derivation source, (c) the PR-comment choice — post automatically / ask once the report is written / never (AC2)
- [x] State structurally that **after the block, no code path may introduce a new prompt** — including evaluator failure, timeout, absent `gh`, and no-PR-exists. After the block the run reaches a report or records a failure; it never asks (AC2)
- [x] Declare the full evaluator roster in one place and the `04e-diff-security-scan` seam, invoked with the confirmed diff range. **No new security agent is authored** (AC10)
- [x] Preserve the three-tier structure the existing agent encodes — `05a` (baseline worktree, preflight delegate) → concurrent fan-out → synthesizer. **The concurrent fan-out set is `05b`–`05f` plus `04e` (six), not `05a`–`05g`**; `05a` is a preflight delegate and `05g` consumes the others' reports. See the Discovery Delta — AC10's flat "fans out to `05a`–`05g`" conflates the three roles and a literal reading breaks AC11
- [x] Use display names, not slugs, in the `agents:` frontmatter list. Note **`05a`'s name is `Baseline Worktree`** — no numeric prefix, unlike every other `05x` — and `04e`'s is `04e Diff Security Scan`
- [x] Accept that the roster is a forward reference: the renumbering (`05g`→`05c`, `05j`→`05d`, `05k`→`05e`, `05h`→`05f`, `05l`→`05g`) does not land until waves 5–6, so the `agents:` list names agents that do not yet exist. `08-retirement-reconciliation` verifies it
- [x] Re-derive the model-tier table for the new roster — the existing table maps the retired twelve (`05b`/`05e`/`05f`/`05l` top tier; `05g`/`05j`/`05k` cheap; `05a`/`05c`/`05d`/`05h`/`05i` delegated)
- [x] Retain partial-failure semantics verbatim in force: an evaluator failure never aborts the run and never becomes a passing result; each gets an `evaluator-status.jsonl` record naming evaluator, check, reason, and report (`null` when none); the bounded wait is retained (AC11)
- [x] State that **the verdict can never be GO while any check is missing** (AC11)
- [x] Retain the read-only contract: the orchestrator never reads code or diffs, inspects path metadata only, and reads only structured reports under the run's report root; every subagent return is ≤10 lines (AC12)
- [x] Retain the constraint that model and harness identity never appear in retained reports
- [x] Verify no report templates or severity levels are restated in the orchestrator — they live in `pr-review-report` / `pr-review-conventions` (feature 03)
- [x] Write tests asserting the single-interaction declaration and that all three questions are named within the block (AC2), and that the roster names `04e` (AC10)

## Stage 5: Rename, Propagate, Dry-Run

**Goal:** Rename the file and agent; propagate; confirm the stale command file is pruned; dry-run against the fixture. **Success Criteria:** AC1, AC7, AC14; one interaction to a report; suite green.

- [x] `git mv .github/agents/05-phase-final-review.agent.md .github/agents/05-pr-review.agent.md` (AC1)
- [x] Update `name:` from `05 Phase - Final Review` to the new value `[PROPOSED - name TBD]`. **The name must not be a substring of common prose** — `_rewrite_agent_references` (`scripts/propagate_master_assets.py:423`) does unanchored `text.replace(agent.name, identifier)` across every agent body, so a generic name like `PR Review` would rewrite that phrase throughout this phase's agent and skill prose. The ` - ` separator in the old name is what made it collision-safe; `05 PR - Review` preserves that property
- [x] Restate `description:` to the branch-diff scope, dropping the multi-subphase and verdict-write-back framing (AC1)
- [x] Declare the report root as `dev/pr-review/<base-sha-short>-<UTC-YYYYMMDDTHHMMSSZ>/` and verify **no branch name appears in any path component** (AC7)
- [x] Decide and record the two-runs-in-the-same-second policy: accept the collision (same base, same second) or add a sequence suffix
- [x] Update `tests/test_propagate_master_assets.py:198–202` — all five pinned strings change: `.github/agents/05-phase-final-review.agent.md` → `name: 05 Phase - Final Review`, `claude/commands/phase-final-review.md`, `opencode/agents/05-phase-final-review.md`, `codex/agents/05-phase-final-review.toml`, `codex/profiles/phase-final-review.config.toml`. Note the Claude output is a **command**, not an agent — the orchestrator is user-invocable
- [x] Leave `expected_slugs` (`tests/test_propagate_master_assets.py:87`) alone — it omits `execute` holders including this orchestrator, which retains `execute` for base derivation. Feature `05` closes that enumeration gap
- [x] Update `.github/agents/README.md:136` (the orchestrator's own row) and the parent column of every surviving `05x` row at `:163+`, which still read `05 Phase - Final Review`. **Feature 02's AC5 covers only retired-agent rows, so these survive it** — confirm ownership with `08-retirement-reconciliation` if it belongs there instead
- [x] Run propagation and verify the renamed orchestrator reaches all three roots: `claude/commands/`, `opencode/agents/`, `codex/agents/`, `codex/profiles/` (AC14)
- [x] Confirm `claude/commands/phase-final-review.md` is **absent** — removed by feature `01`'s pruning, **not** hand-deleted. A stale command file would leave a live slash command pointing at a deleted agent (AC14)
- [x] Confirm the old `opencode/agents/05-phase-final-review.md`, `codex/agents/05-phase-final-review.toml`, and `codex/profiles/phase-final-review.config.toml` are also gone from the generated roots
- [x] Verify the `name:` change did not corrupt other agents' prose in any of the three roots. Scope note: the literal `05 Phase - Final Review` appears in **no other source agent body** — only `.github/agents/README.md` and `tests/test_propagate_master_assets.py:198` carry it, so this check is narrower than the plan implies. `04-phase-execute.agent.md` Step 6 is *titled* "Phase Final Review" but spawns **Prod Code Review** and does not list this orchestrator in its `agents:` — nothing dangles there
- [x] Work through the plan's keep-it-clean checklist: ledger/subphase/artifact-inventory/write-back/archive all gone; preflight is two steps; exactly one interaction block; no report templates restated; model-tier table re-derived
- [ ] Dry-run against the pinned fixture: confirm **one interaction, then a report** (AC13, runbook verification)
- [x] Run the full suite: `.venv/bin/python -m pytest tests/ -q` — expect ≥416 passed plus the new contract assertions, no regressions

## Manual QA (behavioral — cannot be asserted from a Markdown body)

- [ ] Dry run against the pinned fixture: one interaction, then a report
- [ ] **Live QA in a scratch consumer repo, never this one** — `origin/HEAD` unset. Note `origin/HEAD` **is** set in this repo (`refs/remotes/origin/main`), so this path cannot be exercised locally without unsetting it
- [ ] Live QA: base correction accepted and propagated to every evaluator (AC6)
- [ ] Live QA: no-remote fallback presents local candidates, still excluding self
