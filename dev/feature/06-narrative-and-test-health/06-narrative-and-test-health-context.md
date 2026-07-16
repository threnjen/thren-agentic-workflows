# 06 Narrative and Test Health — Context

## Key Files

### Files being changed

| File | Role | Change Type |
|---|---|---|
| `.github/agents/05h-test-health.agent.md` | Delegating adapter; `name: 05h Test Health`, `tools: [agent, read, search, edit]`, `agents: [Test - Analyst]`. Source of the rename (AC1) and the delta rescope (AC5, AC6). | Rename (`git mv` → `05f-test-health.agent.md`) + Modify |
| `.github/agents/05b-change-narrator.agent.md` | Deep-judgment narrator; `name: 05b Change Narrator`, `tools: [agent, read, search, edit]`, no `agents:` frontmatter. Slug unchanged; body rescoped (AC2–AC4). | Modify |
| `tests/test_propagate_master_assets.py` | `expected_slugs` tuple at lines 90–99; per-slug `assertNotIn("execute", agent.tools)` at line 118; full-render equality assertions for all three roots at lines 124–145. | Modify |
| `opencode/agents/05h-test-health.md` | Old generated OpenCode slug; becomes an orphan after the rename and must be pruned by feature `01` (AC8). | Deleted via propagation (no manual `git rm`) |
| `opencode/agents/05f-test-health.md` | New generated OpenCode output. | Create (via propagation) |
| `claude/agents/z-test-health.md`, `codex/agents/z-test-health.toml` | Generated outputs. **Filenames do not change across the rename** — see Discovery Delta. | Modify (regenerate body) |
| `claude/agents/z-change-narrator.md`, `opencode/agents/05b-change-narrator.md`, `codex/agents/z-change-narrator.toml` | Generated `05b` outputs. | Modify (regenerate body) |

### Read-only reference files

| File | Why it matters |
|---|---|
| `.github/agents/test-analyst.agent.md` | The delegation target. **Verified**: `name: Test - Analyst` (exact), `tools: [read, search, edit, fetch]`, `user-invocable: false`. Its native deliverable is a reduction-plan file set in `dev/feature/`. Explicit non-goal: do not modify. |
| `scripts/propagate_master_assets.py` | `_claude_filename_for` (L389), `_opencode_filename_for` (L432), `_codex_identifier_for` (L452), `_choose_existing_stem` (L382), `_build_agent_reference_map` (L412). Governs every AC8 outcome. |
| `docs/phases/PHASE_03/PHASE_03_SUMMARY.md` | The Phase document. Deliverable 5 (L177); evaluator roster (L105–120). Source of the exact slugs `05b-change-narrator`, `05f-test-health`, `test-analyst`. |
| `.github/agents/05-phase-final-review.agent.md` | L5 `agents:` frontmatter names `05b Change Narrator` and `05h Test Health`. Owned by feature `04`, not this feature. |
| `.github/agents/README.md` | L163 (`05b`) and L170 (`05h`) catalogue rows. Owned by feature `08`'s reference sweep, not this feature. |
| `.github/agents/05a-baseline-worktree.agent.md` | Supplies the base-side checkout `05f` consumes for the coverage delta (AC6). |

## Discovery Delta

| Finding | Impact | Action |
|---|---|---|
| **Undeclared dependency on feature `02`.** `.github/agents/05f-seam-analyzer.agent.md` and `opencode/agents/05f-seam-analyzer.md` exist today. The `05f` slug this feature claims is freed only by feature `02-retired-evaluator-removal` (AC1 deletes the seam analyzer). Feature 06's `Depends on:` names only `03` and `04`. Wave 2 < wave 5 so execution order is safe in practice, but the dependency is unrecorded. | Plan's dependency graph is incomplete; a re-ordering or a feature-02 failure silently produces a slug collision. | **Update plan** — add `02-retired-evaluator-removal` to `Depends on:` and to Relationship to Sibling Plans. |
| **AC9's test already exists; it is not new.** `tests/test_propagate_master_assets.py:118` already runs `self.assertNotIn("execute", agent.tools)` for every slug in `expected_slugs`. The traceability table labels AC9 "Must-have automated test (new)". | AC9 needs no new test — only the roster rename carries it. Writing a second `execute` assertion duplicates existing coverage. | **Update plan** — reclassify AC9 as "existing test to update". Task written accordingly. |
| **The rename changes only the OpenCode filename.** Verified against the propagator: `_claude_filename_for` tries `[source_slug, alias, stripped, z-stripped]` against existing stems and matches the existing `z-test-health` → `claude/agents/z-test-health.md` is **stable**. `_codex_identifier_for` strips the numeric prefix → `z-test-health.toml` is **stable**. Only `_opencode_filename_for` prefers `source_slug`, so `05h-test-health.md` orphans and `05f-test-health.md` is created. | Confirms AC8's OpenCode-only framing is correct and precise. No claude/codex orphan will appear; do not go looking for one. | **None** — plan validated. |
| **`tests/test_propagate_master_assets.py` asserts exact full-file render equality** (L124–145) for all three roots per slug. Any body edit to `05b` or `05f` fails the suite until propagation regenerates all three roots. | Every stage that edits an agent body must run propagation before the suite can pass. This is not optional cleanup at Stage 4. | **Add task** — propagate + verify after each body edit, not only at the end. |
| **`05b`'s `description:` frontmatter contradicts AC2.** It reads "Builds a whole-phase baseline-to-HEAD change narrative **with subphase attribution** and churn hotspots." AC2 deletes subphase attribution but names only the body. | A subphase-attribution test scoped to the body passes while the description still ships the deleted concept to all three roots. | **Add task** — rescope `description:` too; scope the AC2 assertion to the whole file, not just the body. |
| **`max_depth` is a live framework constraint on AC4 and AC5.** `.github/learnings/debugging-learnings.md:25–38` records that Codex `agents.max_depth` defaults to `1`, and that when a spawn is blocked **the model silently falls back to doing the work inline** rather than failing. Through the orchestrator, `05-pr-review` (0) → `05f` (1) → `Test - Analyst` (2) and `05b` (1) → per-directory reader (2) both require `max_depth = 2`. | This is the *mechanism* behind AC5's named failure ("silent reimplementation… looks like success") — and AC5's evidence is a static frontmatter/body assertion, which **cannot detect a runtime inline fallback**. The declaration passes while the behavior reimplements. Same exposure for AC4's readers. | **Update plan** — AC5's static assertion is necessary but not sufficient; the manual QA check must force the `max_depth = 1` case specifically, and the `max_depth = 2` requirement should be stated where the family is operated. |
| **Existing `05h` body already satisfies AC5's degradation rule.** It states: if `Test - Analyst` is unavailable, errors, or returns no usable analysis, write a NOT RUN entry with a concrete reason and a stated below-GO verdict ceiling; "Do not… reimplement the delegate's analysis procedure." It also already carries the three required sections (coverage delta / redundancy / flake candidates). | The rescope is genuinely thin — reframe phase→branch, not a rewrite. Matches learnings `review-learnings.md:267–271`. | **None** — preserve this language verbatim through the rename; do not regress it. |
| **`05b`'s existing chunking already degrades correctly.** Its Narrative Procedure step 2 says to use per-directory reader delegations "when the harness supports them. Otherwise process the same chunks serially in this context." | AC4's structural-chunking requirement is largely already met; the work is deleting subphase partitioning from the chunk boundary, not inventing chunking. | **None** — plan validated. |
| **Phase Deliverable 5 groups three items; this feature covers two.** `PHASE_03_SUMMARY.md:177` pairs `05b` and `05f` with "the `04e-diff-security-scan` invocation seam". Feature `04`'s plan (L19, L65) explicitly claims that seam. | Not a gap — the seam is owned upstream. Recorded so a reviewer comparing this feature to Deliverable 5 does not read it as missing scope. | **None** — recorded as a scope boundary. |
| **The exact `name:` value `05f Test Health` is not pinned anywhere.** The Phase doc names the slug `05f-test-health`; neither the Phase doc nor feature `04`'s plan states the display-name string. Feature `04` authors its roster as an acknowledged forward reference (its Unverified Assumptions, L247–250). | The propagator rewrites agent references by display name, so a near-miss ships as literal prose — the exact hazard the plan flags for `Test - Analyst` but not for its own `name:`. | **Add task** — set `name: 05f Test Health` following the established `05h Test Health` convention, and record it in implementation notes as the value feature `04`'s roster must match. |

## Architectural Decisions

- **`05f` is a delegating adapter; `05b` is a deep-judgment agent.** These are two established patterns in the family, not one. `05f` declares `agents: [Test - Analyst]`, delegates, and adapts. `05b` takes the top model tier, chunks internally, and forms a judgment. (Plan §C)
- **`05f` stays thin — adaptation, not analysis.** Its value is turning suite analysis into a branch-scoped delta. Growing past a page of instructions signals it is absorbing `test-analyst`'s job. (Plan §D)
- **`05b` is allowed to be the largest evaluator prompt in the family.** It carries the judgment and earns the top tier. (Plan §D)
- **Subphase attribution is deleted outright, not adapted.** A PR has no subphases. Churn hotspots survive because they were never a phase concept. (Plan §A/AC2)
- **Chunking is structural, not advisory.** AC4 is a mitigation for the phase's worst context-blowout risk; "be concise" is not an acceptable implementation. (Plan §B)
- **Coverage delta degrades honestly.** If `test-analyst` cannot be pointed at the base revision, `05f` reports HEAD coverage plus a stated limitation rather than growing its own coverage runner. (Plan Unverified Assumptions)
- **`05f` consumes `05a-baseline-worktree`'s checkout; it does not create its own.** (Plan §B)
- **Report must name its evidence source (tool + revision pair).** A coverage delta without a named source is unreconcilable later. (Plan §E, citing the recorded revision-naming lesson)
- **Both agents are evidence producers, never verdict producers.** `05g` decides. (Plan Non-Goals)

## Constraints

- **Neither agent acquires `execute`** (AC9). Both hold `[agent, read, search, edit]` today; the rescope creates no need for more. Enforced by the existing assertion at `tests/test_propagate_master_assets.py:118`.
- **`Test - Analyst` must be exact.** Verified existing display name in `test-analyst.agent.md:2`. The propagator matches on display name; a near-miss silently ships as literal prose.
- **Both return ≤10 lines**; full detail on disk (AC7).
- **Report path**: `dev/pr-review/<base-sha-short>-<UTC-YYYYMMDDTHHMMSSZ>/<evaluator-slug>-report.md`, per feature `03`'s contract.
- **Generated outputs are never hand-edited or `git rm`'d.** They come from a propagation run; orphans are removed by feature `01`'s pruning (AC8).
- **`05h`/`05f` and `05b` bodies reference the `phase-final-review-conventions` / `phase-final-review-report` skills**, which feature `03` renames to `pr-review-conventions` / `pr-review-report`. Feature `03` lands at wave 3 and owns that edit on the pre-rename filename; the `git mv` here carries it forward.
- **Sequential with feature `05`** — both edit `expected_slugs` in `tests/test_propagate_master_assets.py`. Whichever lands second reconciles.
- **Test baseline must stay green**: 416 passed, 15 subtests passed.

## Scope Boundaries

- **Do not modify `.github/agents/test-analyst.agent.md`.** Explicit non-goal.
- **Do not implement flake detection.** `05f` reports candidates from `test-analyst`'s output; it never runs the suite repeatedly.
- **Do not rescope the mechanical evaluators** (`05c`/`05d`/`05e` — feature `05`) **or synthesis** (`05g` — feature `07`).
- **Do not produce a verdict** in either agent. `05g` decides.
- **Do not touch the `04e-diff-security-scan` invocation seam** — feature `04` owns it despite the Phase doc grouping it into Deliverable 5.
- **Do not edit `.github/agents/README.md`** — feature `08`'s reference sweep owns L163/L170.
- **Do not edit `.github/agents/05-phase-final-review.agent.md`'s roster** — feature `04` owns it.
- **Do not rename `05b-change-narrator`.** Its slug is already correct; only its body and `description:` change.
- **Do not delete `05b`'s churn hotspots** — they are not a phase concept and survive the rescope.
- **Preserve `05h`'s existing NOT RUN / below-GO-ceiling language and its three report sections** through the rename.
- **Do not add `execute` to either agent** — the one place in the phase where security posture improves by default.

## Relationships to Sibling Plans

- **Depends on `03-pr-review-conventions-skills`** — report root, `<evaluator-slug>-report.md` naming, and the ≤10-line return contract. Also owns the skill-reference edit inside `05h-test-health.agent.md`.
- **Depends on `04-pr-review-orchestrator`** — confirmed base and roster. Feature `04` authors `05f Test Health` into its roster as an acknowledged forward reference; **this feature resolves that reference**, so the `name:` value is a cross-feature contract.
- **Depends on `02-retired-evaluator-removal`** *(undeclared in the plan — see Discovery Delta)* — deletes `05f-seam-analyzer`, freeing the `05f` slug.
- **Depends on `01-propagator-orphan-pruning`** *(transitively, via AC8)* — the orphan pruning that removes `opencode/agents/05h-test-health.md`.
- **Same wave as `05-mechanical-evaluators`, sequential with it** — both edit `expected_slugs`.
- **Consumes `05a-baseline-worktree`** for the base-side checkout (AC6).
- **Feeds `07-synthesis-and-pr-posting`** through report files only.
- **`08-retirement-reconciliation` verifies** that no `05h`–`05l` slug survives anywhere and sweeps `README.md` / `CODEBASE_CONTEXT.md`.

## Suggested Implementation Order

Follow the plan's stages: **Stage 1** (rename + propagate + confirm the OpenCode orphan is pruned) → **Stage 2** (`05f` delta rescope; resolve the `test-analyst` baseline question) → **Stage 3** (`05b` narrator rescope) → **Stage 4** (dry-run both; reconcile `expected_slugs` with feature `05`).

Stage 1 first is right: it settles the slug and the generated-root shape before any body rewrite, so a propagation failure is attributable to the rename rather than to prose. Resolve Stage 2's `test-analyst` baseline question **before** writing `05f`'s delta prose — the answer determines whether the report states a delta or a stated limitation.

Because the propagation test asserts exact full-file render equality, run propagation at the end of **every** stage that edits a body, not only Stage 4.

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Agent definitions as Markdown + YAML frontmatter in `.github/agents/`, propagated by `scripts/propagate_master_assets.py` to `claude/`, `opencode/`, `codex/`. Python test suite. |
| Test Runner | `.venv/bin/python -m pytest tests/ -q` — **system `python3` has no pytest; the `.venv` interpreter is required** |
| Test Baseline | 416 passed, 15 subtests passed — captured 2026-07-16 across 4 consecutive full runs, all green |
| Lint | Not configured |
| Format | Not configured |

## Relevant Learnings

**`.github/learnings/debugging-learnings.md:25–38` — Codex `agents.max_depth` and silent inline fallback.** The default `max_depth = 1` blocks depth-2 spawns, and when a spawn tool is unavailable *the model does not fail — it does the work inline*. Through the orchestrator, both `05f` → `Test - Analyst` and `05b` → per-directory readers sit at depth 2 and require `[agents] max_depth = 2` in `~/.codex/config.toml`. The learning also warns that going beyond 2 risks runaway fan-out. Directly load-bearing for AC4 and AC5 — see Discovery Delta.

**`.github/learnings/review-learnings.md:267–271` — NOT RUN needs a visible readiness ceiling.** "When a delegated evaluator fails after dispatch, record both the concrete NOT RUN reason and an explicit NO-GO or below-GO readiness ceiling. A not-run marker without a visible readiness ceiling can be mistaken for neutral coverage." The existing `05h` body already does this; preserve it.

**`.github/learnings/review-learnings.md:255–259` — delegating wrappers and generated mirrors.** "Delegating or read-only wrapper agents should receive only the capabilities needed for input collection, child delegation, and report writing; generated harness outputs should be checked against the source renderer. Unneeded shell or execution permissions weaken prompt-level read-only boundaries, while untested generated mirrors can silently lose delegation or safety constraints in one platform." Supports AC9 and AC8.

**`.github/learnings/cross-phase-decisions.md:15` — every evidence artifact must name its revision.** "Any evidence artifact that does not name its revision cannot be reconciled against later work." This is the cited basis for the plan's §E requirement that `05f`'s report name its coverage tool and revision pair.

**`.github/learnings/cross-phase-decisions.md:53` — the roster split.** `05b-change-narrator` and `05h-test-health` are among the seven diff-shaped survivors; `05f-seam-analyzer` is among the five retired. Confirms the `05f` slug is freed by retirement, not contested.

**`.github/learnings/cross-phase-decisions.md:60` — refinement decisions (2026-07-16).** Pipeline artifacts are optional enrichment; no verdict write-back — the report file *is* the verdict; the seven survivors renumber contiguously to `05a`–`05g`; reports land at `dev/pr-review/<base-sha-short>-<UTC-timestamp>/`, keyed only by hex and digits so no branch name reaches a filesystem path; the verdict is advisory; security is delegated to `04e-diff-security-scan`.
