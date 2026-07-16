# 06 Narrative and Test Health — Tasks

## Stage 0: Test Prerequisites

**Status: Not required.** Baseline 416 passed, 15 subtests passed across 4 consecutive full runs (2026-07-16).

- [ ] Confirm the baseline before starting: `.venv/bin/python -m pytest tests/ -q` reports 416 passed, 15 subtests passed (use `.venv/bin/python`; system `python3` has no pytest)
- [ ] Confirm feature `02-retired-evaluator-removal` has landed and `.github/agents/05f-seam-analyzer.agent.md` is gone — it frees the `05f` slug this feature claims (undeclared dependency; see Discovery Delta)

## Stage 1: Rename `05h` → `05f`

**Goal**: `git mv`; update `name:` and self-references; propagate; confirm the OpenCode orphan is pruned.
**Success Criteria**: AC1, AC8.

- [ ] `git mv .github/agents/05h-test-health.agent.md .github/agents/05f-test-health.agent.md` (AC1)
- [ ] Set `name: 05f Test Health` in frontmatter, following the established `05h Test Health` convention. This exact string is a cross-feature contract — feature `04`'s `agents:` roster forward-references it, and the propagator rewrites references by display name, so a near-miss ships as literal prose. Record the chosen value in implementation notes (AC1)
- [ ] Update every `05h` self-reference in the body — including the `Write only dev/phase-final-review/PHASE_0N/05h-test-health-report.md` line and the "You are the **05h Test Health** evaluator" opener (AC1)
- [ ] Verify no `execute` was introduced by the rename; `tools:` stays `[agent, read, search, edit]` and `agents:` stays `[Test - Analyst]` exactly (AC9)
- [ ] Run propagation to regenerate all three roots. Do not hand-edit or `git rm` any generated file (AC8)
- [ ] Verify `opencode/agents/05f-test-health.md` was created and `opencode/agents/05h-test-health.md` is absent via feature `01`'s pruning (AC8)
- [ ] Verify `claude/agents/z-test-health.md` and `codex/agents/z-test-health.toml` kept their filenames and only their bodies changed — the propagator's stem-matching and prefix-stripping make these stable across the rename; a new `05f-*` file in either root is a bug (AC8)
- [ ] Update `expected_slugs` in `tests/test_propagate_master_assets.py` (lines 90–99): `05h-test-health` → `05f-test-health` (AC8)
- [ ] Run the suite green. Note that lines 124–145 assert exact full-file render equality for all three roots, so this only passes after propagation (AC8)

## Stage 2: Rescope Test Health to a Delta

**Goal**: Reframe `05f` around coverage delta base→HEAD; confirm how `test-analyst` can produce the base side, and degrade honestly if it cannot.
**Success Criteria**: AC5, AC6; the delegation assertion passes; the baseline question is resolved and recorded.

- [ ] **Resolve first, before writing prose**: determine whether `Test - Analyst` can be pointed at a specific revision or worktree path to produce the base side of the coverage delta. Its current contract is suite-analysis at the working tree. Record the answer in implementation notes (Unverified Assumption)
- [ ] If it cannot: have `05f` report HEAD coverage plus a stated limitation rather than a delta. Do not grow a coverage runner inside `05f` (AC6)
- [ ] Reframe the report's three sections from phase-scoped to branch-scoped: coverage delta **base→HEAD**, test redundancy, flake candidates. Delete "cross-subphase" from the redundancy framing — a PR has no subphases (AC6)
- [ ] Have `05f` consume `05a-baseline-worktree`'s checkout for the base side; it must not create, switch, or remove a worktree itself (AC6)
- [ ] Preserve the existing delegation language verbatim through the rescope: `agents: [Test - Analyst]`, "analysis belongs to `Test - Analyst`", "do not reimplement the delegate's analysis procedure", and the instruction to consume the delegate's reduction-plan output as intermediate evidence rather than publishing it (AC5)
- [ ] Preserve the existing NOT RUN rule: if `Test - Analyst` is unavailable, errors, times out, or returns no usable analysis, write a NOT RUN entry with a concrete reason **and** an explicit below-GO verdict ceiling; never substitute a hand-rolled check (AC5)
- [ ] Preserve the not-measurable rule for repos with no coverage tooling — absence is a stated limitation, not a failure. This agent ships to consuming projects that may have none (AC6)
- [ ] Have the report name its coverage evidence source — tool and revision pair. A delta without a named source is unreconcilable later (Plan §E)
- [ ] Keep `05f` thin. Past a page of instructions, it is absorbing `test-analyst`'s job (Plan §D)
- [ ] Update the report path to feature `03`'s contract: `dev/pr-review/<base-sha-short>-<UTC-YYYYMMDDTHHMMSSZ>/05f-test-health-report.md`, and keep the ≤10-line return (AC7)
- [ ] Write the delegation-declared test: assert `05f`'s `agents:` frontmatter names `Test - Analyst` exactly and its body delegates rather than describing inline coverage analysis. Note this is a *declaration* assertion and cannot detect a runtime inline fallback — see the max_depth QA check in Stage 4 (AC5)
- [ ] Propagate and run the suite green

## Stage 3: Rescope the Narrator

**Goal**: Delete subphase attribution; reframe to `<merge-base>..HEAD`; add the "what is this branch trying to do" account; make chunking structural.
**Success Criteria**: AC2, AC3, AC4, AC7.

- [ ] Delete all subphase attribution from `05b`'s body: the "discovered subphase paths" input, the path→subphase mapping (Procedure step 1), the per-subphase partition and reporting (steps 2–3), the multi-subphase churn-hotspot definition (step 4), and the per-subphase report sections (AC2)
- [ ] Update `05b`'s `description:` frontmatter — it currently reads "whole-phase baseline-to-HEAD change narrative **with subphase attribution** and churn hotspots" and contradicts AC2. A body-only edit ships the deleted concept to all three roots (AC2)
- [ ] Reframe the comparison from whole-phase baseline→final to the branch diff over `<merge-base>..HEAD` (AC2)
- [ ] Keep churn hotspots, redefined without subphases — they were never a phase concept (AC2)
- [ ] Add the account of **what the branch is trying to do**, not merely what it changed. This is the narrative spine of the readiness report and the reason `05b` holds the top model tier (AC3)
- [ ] Keep the top-tier model requirement and the rule that a lower tier is an execution limitation to record, never a passing result (AC3)
- [ ] Keep chunking structural, not advisory: bounded chunks read one at a time, per-directory reader delegations as the pressure valve with serial fallback when the harness does not support them, full detail on disk. Re-anchor the chunk boundary on directories now that subphases are gone (AC4)
- [ ] Keep the added-line attribution discipline so the narrative does not attribute pre-existing code to the branch (Plan §B)
- [ ] Handle the empty-diff case explicitly: say so; do not report "no narrative findings" (Plan §B)
- [ ] Keep `05b` an evidence record, not a remediation plan — no verdict; `05g` decides (Non-Goals)
- [ ] Update the report path to `dev/pr-review/<base-sha-short>-<UTC-YYYYMMDDTHHMMSSZ>/05b-change-narrator-report.md` and keep the ≤10-line return (AC7)
- [ ] Verify `05b` gains no `execute`; `tools:` stays `[agent, read, search, edit]` (AC9)
- [ ] Write the no-subphase-attribution test: assert the `05b` **file** (not just the body — the `description:` lives in frontmatter) contains no subphase concepts and frames the narrative as `<merge-base>..HEAD` (AC2)
- [ ] Write the return-contract and chunking test: assert both agents declare the ≤10-line return and that `05b` declares internal chunking with detail on disk (AC4, AC7)
- [ ] Propagate and run the suite green

## Stage 4: Dry-Run and Reconcile the Roster

**Goal**: Dry-run both against the pinned fixture; reconcile `expected_slugs` with feature `05`.
**Success Criteria**: AC8, AC9; two reports produced; suite green.

- [ ] Reconcile `expected_slugs` with feature `05-mechanical-evaluators` — both features edit the same tuple; whichever lands second reconciles. Expect `05c-artifact-sweeper`, `05d-consistency-auditor`, `05e-dependency-auditor` from feature `05` alongside `05f-test-health` from this one (AC8)
- [ ] Confirm the existing per-slug `assertNotIn("execute", agent.tools)` at `tests/test_propagate_master_assets.py:118` now covers `05f-test-health` and still covers `05b-change-narrator`. **No new `execute` test is needed** — the plan labels AC9 "new", but this assertion already exists; only the roster changes (AC9)
- [ ] Write the old-OpenCode-slug-pruned test: assert `opencode/agents/05h-test-health.md` is absent after propagation (AC8)
- [ ] Dry-run `05b` against the pinned base/branch fixture; confirm a narrative report is produced at the feature `03` path with a ≤10-line return (AC7)
- [ ] Dry-run `05f` against the pinned fixture; confirm a test-health report is produced with the coverage-delta, redundancy, and flake sections and a named evidence source (AC6, AC7)
- [ ] **Manual QA (AC3)**: read `05b`'s dry-run report and judge whether the narrative is actually about what the branch is *for*, not just what it changed. No assertion covers this
- [ ] **Manual QA (AC5)**: force `Test - Analyst` unavailable and confirm `05f` reports NOT RUN with a below-GO ceiling rather than substituting its own analysis. **Force the `agents.max_depth = 1` case specifically** — `.github/learnings/debugging-learnings.md:25–38` records that a blocked spawn causes the model to silently do the work inline rather than fail, which is exactly AC5's failure mode and is invisible to the Stage 2 declaration assertion
- [ ] Verify `[agents] max_depth = 2` is required in `~/.codex/config.toml` for `05f` → `Test - Analyst` and `05b` → per-directory readers to spawn through the orchestrator (both sit at depth 2), and record that requirement where the family is operated. Do not raise it beyond 2 — the learning warns of runaway fan-out
- [ ] Walk the keep-it-clean checklist: no subphase attribution in `05b`; `05f` delegates with no inline coverage logic; `Test - Analyst` display name exact; neither agent gained `execute`; chunking structural in `05b`, not advisory
- [ ] Confirm no file outside this feature's scope was touched — `.github/agents/README.md` (feature `08`), `.github/agents/05-phase-final-review.agent.md` (feature `04`), and `.github/agents/test-analyst.agent.md` (non-goal) all stay unmodified
- [ ] Final propagation run; verify all three roots are clean and consistent
- [ ] Full suite green at or above the 416 passed / 15 subtests baseline
