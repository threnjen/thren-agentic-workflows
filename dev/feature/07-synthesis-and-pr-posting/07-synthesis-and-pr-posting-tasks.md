# 07 Synthesis and PR Posting — Tasks

## Stage 0: Test Prerequisites

**Status:** Not required — baseline 416 passed across 4 consecutive full runs (2026-07-16). Count will have dropped from feature `02`'s deletions.

- [ ] Record the current baseline before starting: run `.venv/bin/python -m pytest tests/ -q` and note the pass count post-feature-`02` (use `.venv/bin/python`, not system `python3`)
- [ ] Confirm upstream dependencies have landed: `.github/agents/05-pr-review.agent.md` exists (feature `04`), `.github/agents/05g-artifact-sweeper.agent.md` is **gone** (feature `05` renamed it to `05c-artifact-sweeper`), and `.github/skills/pr-review-report/` exists (feature `03`)

## Stage 1: Rename and Retarget the Synthesizer

**Goal:** `git mv` `05l` → `05g`; retarget the report root and roster; preserve the report-only, `Checks Not Run`, and GO-ceiling contracts verbatim.
**Success Criteria:** AC1, AC2, AC3, AC4, AC5, AC12.

- [ ] Verify the `05g` slug is free — `.github/agents/05g-artifact-sweeper.agent.md` must not exist before the move (see Discovery Delta; this is feature `05`'s deliverable)
- [ ] `git mv .github/agents/05l-readiness-synthesizer.agent.md .github/agents/05g-readiness-synthesizer.agent.md` (AC1)
- [ ] Update the `name:` frontmatter field from `05l Readiness Synthesizer` to `05g Readiness Synthesizer` (AC1)
- [ ] Update every `05l` self-reference in the body — the opening line ("You are the **05l Readiness Synthesizer**"), the `prod-code-review` relationship paragraph, and the closing boundaries paragraph ("05l is synthesis only") (AC1)
- [ ] Retarget the report root from `dev/phase-final-review/PHASE_0N/readiness-report.md` to `dev/pr-review/<base-sha-short>-<UTC-YYYYMMDDTHHMMSSZ>/readiness-report.md`, including the "current report root" language in Scope and Inputs (AC3)
- [ ] Update the skill loads from `phase-final-review-conventions` / `phase-final-review-report` to `pr-review-conventions` / `pr-review-report` if feature `03` has not already done so — verify rather than assume; feature `03` lists this file as one it modifies (AC2)
- [ ] Retarget the input roster: remove the canonical hand-off reports `master-qa.md`, `security-rollup.md`, and `ac-regression-matrix.md` from Scope and Inputs, and remove the Synthesis Rule 1 clause about a hand-off report satisfying a missing evaluator report — all three producing agents (`05c-qa-consolidator`, `05d-security-rollup`, `05e-ac-regression`) are retired (AC2)
- [ ] Pin the inputs to the `pr-review-report` templates from feature `03` plus the `evaluator-status.jsonl` records from feature `04` (AC2)
- [ ] Preserve verbatim: the report-only prohibition ("never read code, diffs, worktrees, or other agents' internals"), the metadata-only validation rule (readable, regular, non-empty, under the current report root), and the "an evaluator's claim that a report was written" refusal (AC2)
- [ ] Preserve verbatim the `Checks Not Run` section requirement and the rule that every missing or incomplete evaluator/check is named with a concrete reason (AC4)
- [ ] Preserve verbatim the no-GO-with-missing-checks rule and the exact ceiling string **no blockers found, coverage incomplete** (AC4)
- [ ] Preserve verbatim: the `.github/agents/prod-code-review.md` reference, the four severity levels (Critical, High, Medium, Low), `at most 10 lines`, `top available`, and `state-of-the-art` — each is locked by an existing test assertion
- [ ] Reframe the `prod-code-review` relationship from "one level up" (a multi-subphase framing the rescope removes) to a different-axis complement: `prod-code-review` gates a feature set from pipeline documents; `05g` gates a branch diff from evaluator reports. Do not modify `prod-code-review` itself
- [ ] Delete the verdict write-back clause from the closing boundaries paragraph — "the orchestrator owns verdict write-back and the learnings agent owns draft proposals" names two retired concepts and directly contradicts AC5 (AC5)
- [ ] Confirm no reference to `PROJECT_ROADMAP.md`, phase summaries, or any status line survives anywhere in the `05g` body, on any path (AC5)
- [ ] Add the requirement that the report names the revision it examined — an evidence artifact that does not name its revision cannot be reconciled against later work
- [ ] Set the `tools:` frontmatter grant correctly for the rebuilt agent rather than carrying the existing grant forward unexamined; `05g` synthesizes reports and needs no `execute`
- [ ] Run propagation and confirm `05g` reaches all three roots: `opencode/agents/05g-readiness-synthesizer.md` (renamed from `05l-*`), `claude/agents/z-readiness-synthesizer.md` and `codex/agents/z-readiness-synthesizer.toml` (stem-keyed — filenames unchanged, bodies updated) (AC12)
- [ ] Confirm `opencode/agents/05l-readiness-synthesizer.md` is absent after feature `01`'s pruning runs (AC12)

## Stage 2: Resolve P5-SEC-02

**Goal:** Decide and record whether the rebuilt readiness path carries a strict schema and deterministic status reducer, or whether P5-SEC-02 stays open. Record the decision with an owner either way.
**Success Criteria:** AC6 — an explicit, recorded outcome. "Tightened the wording" is not an outcome.

- [ ] Re-read the recorded finding: `.github/learnings/cross-phase-decisions.md` lines 16 and 82, and `docs/phases/PHASE_04/PHASE_04_SUMMARY.md` line 68. The record states P5-SEC-02 "is closed by rebuilding the readiness path **in code** rather than asserting it in prose"
- [ ] Determine whether this feature adds a strict schema and a deterministic status reducer over structured records. If it ships agent Markdown only, the finding is **not closed** — tightening the prose does not close it, and the Phase 03 scan already faulted exactly that move
- [ ] Record the outcome explicitly as closed or open, with an owner and routing either way. Do not redefine the finding to fit the scope — when the honest fix requires capability a phase has excluded, the phase records the finding
- [ ] Resolve the recorded tension openly: a "strict schema and deterministic reducer" implies code, and this phase ships agent Markdown. Resolve it as a decision with an owner, not by rewording the finding
- [ ] Write the decision into the implementation record and, if the finding remains open, into `.github/learnings/cross-phase-decisions.md` with its routing (AC6)

## Stage 3: Posting Path

**Goal:** Implement auto / ask-when-ready / never against the choice captured upfront; handle no-PR, absent `gh`, and unauthenticated `gh` as reported conditions; decide the oversized-comment behavior.
**Success Criteria:** AC7, AC8, AC10.

- [ ] Read feature `04`'s upfront consent block in `.github/agents/05-pr-review.agent.md` and confirm the three captured settings — *post automatically*, *ask once the report is written*, *never* — before wiring anything to them (AC7)
- [ ] Implement the posting path in `.github/agents/05-pr-review.agent.md` as **one command with three outcomes**: posted / no PR / unavailable. Do not add retries, formatting modes, or fallback ladders — this is the named complexity risk (AC7)
- [ ] Wire *post automatically*: post the readiness report to the PR once written, with no further interaction (AC7)
- [ ] Wire *ask once the report is written*: the report must exist on disk **before** the confirmation prompt appears — this is the property that makes the option both unattended and safe (AC7, AC10)
- [ ] Wire *never*: declare explicitly that **no `gh` invocation and no network call is made** on this path (AC7)
- [ ] Handle no PR open for the branch: report the condition, leave the local report as the deliverable. **Not an error, not a run failure** (AC8)
- [ ] Handle `gh` absent or unauthenticated: report alongside the local report. **Not an error, not a run failure** (AC8)
- [ ] Handle mid-way posting failure (network, rate limit, permissions): report the failure; the local report is the deliverable. **Never retry into a prompt** (AC8, AC10)
- [ ] Decide and record the oversized-comment behavior: truncate with a pointer to the local report path, or post a summary. Record the decision — a silently truncated verdict is a misreported verdict
- [ ] Confirm the posting path introduces **no new prompt** beyond the upfront block, with the single designed exception of the *ask when ready* confirmation, which blocks nothing (AC10)
- [ ] Confirm the upfront prompt states plainly that *auto* means a `NO-GO` with a severity-ordered blocking list appears on a colleague's PR before the author has read it (AC7)
- [ ] Confirm no attempt is made to narrow the orchestrator's `execute` to `gh` — not expressible on Claude, and the orchestrator already holds unrestricted Bash for base derivation, so `gh` widens nothing
- [ ] Confirm neither the posting path nor the orchestrator reads PR comments or any network-sourced text back in — output is one-way; ingesting PR discussion is a prompt-injection surface and is out of scope (AC9)
- [ ] Run propagation for the orchestrator and confirm the posting path reaches `claude/`, `opencode/`, and `codex/`

## Stage 4: Rewrite the Synthesis Tests and Prove It

**Goal:** Rewrite `tests/test_readiness_synthesis_agents.py`; add the posting and one-way assertions; dry-run all three consent settings.
**Success Criteria:** AC9, AC11; suite green; report-before-prompt verified.

- [ ] Retarget the `READINESS_AGENT` path constant in `tests/test_readiness_synthesis_agents.py` to `.github/agents/05g-readiness-synthesizer.agent.md` (AC11)
- [ ] Remove the `LEARNINGS_AGENT` path constant and confirm the three `05i-learnings-harvester` tests are gone — feature `02` deletes them, along with the literal ``never use `execute` `` assertions at lines 63 and 90; verify rather than re-delete (AC11)
- [ ] Rewrite `test_both_agents_honor_shared_return_contract_and_readiness_tier` — it currently reads both agents; retarget it to `05g` alone, keeping the `at most 10 lines`, `top available`, and `state-of-the-art` assertions (AC11)
- [ ] Replace the line-wrap-coupled assertion `assert "never read\ncode" in body.lower()` with a wrap-independent assertion for the report-only contract — the current form depends on the exact newline position and will break on any rewrap of the rescoped body (AC2, AC11)
- [ ] Retarget or drop the `"canonical hand-off report"` assertion — the hand-off reports are produced by retired agents and leave the body in Stage 1 (AC11)
- [ ] Retarget the `"readiness-report.md"` assertion to also cover the new report root `dev/pr-review/` (AC3, AC11)
- [ ] Retarget the skill-name assertions from `phase-final-review-conventions` / `phase-final-review-report` to `pr-review-conventions` / `pr-review-report` (AC11)
- [ ] Retain the assertion that `05g` never reads code — it exists today and must survive the rescope (AC2)
- [ ] Retain the assertions on `.github/agents/prod-code-review.md` and the four severity levels (AC11)
- [ ] Add a test that `Checks Not Run` is mandatory and `GO` is capped: assert the body declares that any not-run or incomplete record makes `GO` invalid and that missing checks are named with concrete reasons. **This is the phase's central safety property** (AC4)
- [ ] Add a test that no write-back occurs on any path: assert neither `05g` nor `05-pr-review.agent.md` references `PROJECT_ROADMAP.md` or a phase summary status line (AC5)
- [ ] Add a test that *never* makes no network call: assert the posting path declares the *never* setting performs no `gh` invocation (AC7)
- [ ] Add a test for one-way output: assert no body reads PR comments or network-sourced text back in — an absence assertion (AC9)
- [ ] Add a test asserting `05g` propagates to all three roots (AC12)
- [ ] Reconcile `expected_slugs` in `tests/test_propagate_master_assets.py` (lines 90–99) to the settled seven contiguous slugs `05a`–`05g`; remove the four retired slugs and the renamed `05h`/`05i`/`05l` entries
- [ ] Delete the `05d-security-rollup` conditional block asserting `NO-GO` and `NOT RUN` (lines 119–121) — `05d` is now `05d-consistency-auditor`, a different agent; re-keying rather than deleting would assert the wrong contract
- [ ] Check feature `05`'s `opencode/agents/05g-*` absence assertion against this feature's newly created `opencode/agents/05g-readiness-synthesizer.md` — if the assertion is glob-shaped it will now fail; narrow it to the exact stem `05g-artifact-sweeper.md` (see Discovery Delta; escalated to the Decomposer for ownership)
- [ ] Run the full suite green: `.venv/bin/python -m pytest tests/ -q`
- [ ] Dry-run all three consent settings (AC7)
- [ ] Verify with *ask when ready* that the report file exists on disk **before** the prompt appears (AC7, AC10)
- [ ] Manual QA in a **scratch consumer repo, never this one**: post with a real PR open; post with no PR open; post with `gh` unauthenticated; run with *never* and confirm no network call (AC7, AC8)
- [ ] Verify the unverified assumption that `gh pr comment` resolves the PR for the current branch without the caller knowing the PR number — test in the scratch repo rather than assuming; the no-PR-exists path is the documented failure (AC8)
- [ ] Verify the unverified assumption that a readiness report fits in a PR comment — GitHub comment bodies have a size limit; confirm the Stage 3 truncation decision holds
- [ ] Walk the keep-it-clean checklist: `05g` reads reports only; `Checks Not Run` cannot be omitted; no status-line write-back anywhere; `never` makes no network call; P5-SEC-02 explicitly closed or explicitly recorded open; posting stays one command with three outcomes
