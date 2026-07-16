# 03 PR Review Conventions Skills — Context

## Key Files

### Files being changed

| File | Role | Change type |
|---|---|---|
| `.github/skills/phase-final-review-conventions/SKILL.md` | 152-line evaluator contract: report root, severity, read-only etiquette, model tiers, incomplete-run semantics, ≤10-line return contract | **Rename** → `.github/skills/pr-review-conventions/SKILL.md` + rescope (AC1, AC4, AC5, AC6) |
| `.github/skills/phase-final-review-report/SKILL.md` | 218-line template skill: four hand-off report templates (master QA, security rollup, AC regression, readiness) | **Rename** → `.github/skills/pr-review-report/SKILL.md` + rescope (AC2, AC3, AC4) |
| `.github/agents/05a-baseline-worktree.agent.md` | Baseline worktree specialist | **Modify — prose only.** Line 8 `"for the Phase Final Review family"`. Carries **no** old-skill reference (see Discovery Delta D3) |
| `.github/agents/05-phase-final-review.agent.md` | Orchestrator | Modify — skill refs at lines 21, 22, 60, 156, 214–215 |
| `.github/agents/05b-change-narrator.agent.md` | Survivor evaluator | Modify — skill refs at lines 15, 58 |
| `.github/agents/05g-artifact-sweeper.agent.md` | Survivor evaluator | Modify — skill refs at lines 15, 16 |
| `.github/agents/05h-test-health.agent.md` | Survivor evaluator | Modify — skill refs at lines 15, 16 |
| `.github/agents/05j-consistency-auditor.agent.md` | Survivor evaluator | Modify — skill refs at lines 15, 16 |
| `.github/agents/05k-dependency-auditor.agent.md` | Survivor evaluator | Modify — skill refs at lines 15, 16 |
| `.github/agents/05l-readiness-synthesizer.agent.md` | Survivor evaluator | Modify — skill refs at lines 14, 15, 22, 75 |
| `tests/test_readiness_synthesis_agents.py` | Asserts old skill names in `05l` body at lines 12–13 | **Modify** — existing test to update |
| `claude/skills/`, `opencode/skills/`, `codex/skills/` | Generated roots | Regenerate via propagation; old dirs removed **by feature `01` pruning, never by hand** |

### Read-only reference files

| File | Why it matters |
|---|---|
| `.github/skills/worktree-baseline/SKILL.md` | **AC9 — must not change.** Already generic; its own text declares independence from Phase Final Review and reuse by grading agents. Already propagated to all three roots |
| `.github/skills/auditor-conventions/SKILL.md` | Both skills build on it for shared audit norms. Explicit non-goal — do not change |
| `scripts/propagate_master_assets.py` | `propagate_skills_once` at lines 1225–1300. Owned by feature `01`; read here to understand AC8 |
| `.github/agents/05c/05d/05e/05f/05i-*.agent.md` | Deleted by feature `02` (wave 2) before this feature runs. Do not update their skill refs |
| `dev/feature/05-mechanical-evaluators/`, `06-narrative-and-test-health/`, `07-synthesis-and-pr-posting/` plans | Source of the renumbering map that AC3's report roster depends on (see D1) |

## Discovery Delta

| Finding | Impact | Action |
|---|---|---|
| **D1 — The `05a`–`05g` renumber map AC3 depends on is settled in sibling plans, not in this plan.** Plan §C writes the roster as `05a-baseline-worktree-report.md … 05g-readiness-synthesizer-report.md` with an ellipsis and labels the filenames `[PROPOSED - name TBD]`. The middle five are fully determined by features `05`/`06`/`07`: `05g-artifact-sweeper`→`05c`, `05j-consistency-auditor`→`05d`, `05k-dependency-auditor`→`05e`, `05h-test-health`→`05f`, `05l-readiness-synthesizer`→`05g`; `05a` and `05b` unchanged. | Without this map the implementer invents an ordering for `05c`–`05f` and features `05`–`07` then contradict it — the exact re-litigation §B says settling the roster here prevents. | **Resolved — roster fixed below.** Names are no longer TBD; they are derived from sibling plans. Use the Report Roster section verbatim. |
| **D2 — The codex skill prune is dead code; the plan's §B premise is wrong in effect.** §B states `propagate_skills_once` "prunes `codex/skills/` only (verified `scripts/propagate_master_assets.py:1288`)." The prune block exists (lines 1288–1300) but its guard is `_read_text(skill_md).startswith(GENERATED_SKILL_HEADER)` — and the generated codex `SKILL.md` starts with `---` frontmatter, with the marker on **line 5** (written at line 1273–1277 as frontmatter + header + body). Verified: **0 of 24** codex skills satisfy `startswith(header)`. The prune has never removed anything. | The plan's dependency on feature `01` is **larger than stated**. It is not "add pruning for Claude and OpenCode"; it is also "fix the broken codex prune." Without that, the rename orphans `codex/skills/phase-final-review-conventions/` **too** — all three roots, not two. AC8 as written ("absent from all three generated roots") is still the right AC and still catches this; the plan's reasoning under it is what is stale. | **Warning to Decomposer.** Feature `01`'s AC4 must cover the codex guard bug, not just Claude/OpenCode coverage. Verify `01` before this feature starts; add a task here to assert codex pruning explicitly rather than assuming it works. |
| **D3 — `05a-baseline-worktree` carries no old-skill reference; AC7's first sentence is unsatisfiable for it as written.** Plan §Discovery says `05a`'s "only phase-coupling is the prose 'for the Phase Final Review family' **and its skill reference**." Verified: `05a` references only `worktree-baseline` (lines 12, 30, 38, 40). It never loads `phase-final-review-conventions` or `-report`. AC7 says "**Every** surviving `05x` agent references the renamed skills." | Read literally, AC7 forces adding a `pr-review-conventions` load line to `05a` — new scope the plan never intended, and a step toward touching `worktree-baseline`, which AC9 forbids. | **Interpret AC7 as its second sentence** (the negative sweep) for `05a`. `05a`'s only change is the line 8 prose. Do **not** add a skill load to `05a`. Flagged for Decomposer to reword AC7. |
| **D4 — Claude and OpenCode generated skills carry no generated marker at all.** Lines 1242 and 1255 write `_read_text(source_skill_md)` verbatim — byte-identical to source, no `GENERATED_SKILL_HEADER`. Only codex gets a marker (line 1275). Corroborated by `.github/learnings/cross-phase-decisions.md:71-73`. | Feature `01`'s AC5 ("no pruner deletes a file it did not generate") cannot use a header marker for the Claude/OpenCode skill roots. Pruning there must key on directory-name expectation against the source set. This feature's AC8 depends on `01` getting that right. | **Warning to Decomposer** — routes to feature `01`. No action inside this feature. |
| **D5 — The AC7 sweep must match exact skill names, not the substring `phase-final-review`.** Every survivor also hardcodes the report root `dev/phase-final-review/PHASE_0N/`, and the orchestrator's own filename is `05-phase-final-review.agent.md`. | A substring sweep on `phase-final-review` fails against strings this feature is explicitly not allowed to change (report roots belong to features `04`–`07` per the non-goals). | Sweep on the exact tokens `phase-final-review-conventions` and `phase-final-review-report` only. Recorded as a task. |
| **D6 — Report roots inside agent bodies are out of scope here.** Survivors carry `dev/phase-final-review/PHASE_0N/...-report.md` write targets (e.g. `05b:17`, `05g:20`, `05h:20`, `05j:20`, `05k:20`, `05l:18`). | The skills declare the new root while the agents still declare the old one — an intentional, temporary inconsistency until features `04`–`07` land. | Accepted risk, matches the plan's "forward references" reasoning in §B. Do not fix agent report roots here. |
| **D7 — `tests/test_propagate_master_assets.py` skill coverage is a generic `demo-skill` fixture** (lines 68–85) asserting mirroring to all three roots. No assertion on real skill directory names. | AC8's new prune test has no existing pattern to extend for named skills; it is genuinely new. | Add a new test rather than extending the `demo-skill` case. |
| Retired set verified: `05c`, `05d`, `05e`, `05f`, `05i` deleted by feature `02`. Survivors: `05a`, `05b`, `05g`, `05h`, `05j`, `05k`, `05l` = **seven**. | Confirms the plan's "seven surviving report filenames" count. | None — plan is correct. |
| `worktree-baseline` verified present and identical across `.github/skills/`, `claude/skills/`, `opencode/skills/`, `codex/skills/`. | Confirms AC9's premise: zero changes required. | None — plan is correct. |

### Report Roster (resolved — settle this in Stage 1)

Report root: `dev/pr-review/<base-sha-short>-<UTC-YYYYMMDDTHHMMSSZ>/` (copied exactly from the Phase document; contains no branch name — AC3).

```text
dev/pr-review/<base-sha-short>-<UTC-YYYYMMDDTHHMMSSZ>/
├── 05a-baseline-worktree-report.md      # 05a unchanged
├── 05b-change-narrator-report.md        # 05b unchanged
├── 05c-artifact-sweeper-report.md       # was 05g  (feature 05)
├── 05d-consistency-auditor-report.md    # was 05j  (feature 05)
├── 05e-dependency-auditor-report.md     # was 05k  (feature 05)
├── 05f-test-health-report.md            # was 05h  (feature 06)
├── 05g-readiness-synthesizer-report.md  # was 05l  (feature 07)
└── readiness-report.md                  # canonical hand-off — survives
```

Removed rollups (produced by retired evaluators): `master-qa.md` (`05c-qa-consolidator`), `security-rollup.md` (`05d-security-rollup`), `ac-regression-matrix.md` (`05e-ac-regression`). `readiness-report.md` is the only survivor of the four.

Correspondingly, `pr-review-report` drops templates 1 (Master QA), 2 (Security Rollup), and 3 (AC Regression Matrix), retaining template 4 (Go/No-Go Readiness) retargeted from whole-phase to branch-diff.

## Architectural Decisions

- **Rename + rescope, not authoring.** Both skills exist. Discovery contradicted the Phase document's framing of Deliverable 2 as three new skills; two are renames and the third (`worktree-baseline`) needs zero changes. Design is two `git mv` operations plus content rescope.
- **Settle the report contract first (Stage 1).** Every later feature consumes the roster and root. Deriving it once here prevents features `04`–`07` from each re-litigating filenames.
- **Report filenames use the existing `<evaluator-slug>-report.md` convention.** Preserve the convention rather than inventing one; it already yields the correct names once the roster is settled at seven contiguous slugs.
- **Forward references are intentional.** The skills name `05a`–`05g` slugs before the agents carry them. The skill is the contract each evaluator is subsequently written against.
- **Pipeline artifacts are optional enrichment (AC5).** A run proceeds on the diff alone and names unavailable evidence. This is the recorded boundary keeping PR Review from duplicating `prod-code-review` — a contract, not a preference.
- **Keep the `auditor-conventions` split.** Both skills build on it for shared audit norms and declare only review-family contracts.
- **The conventions skill's scope is the evaluator contract only**: report locations, severity, return size, read-only etiquette, model tiers, incomplete-run semantics. Base derivation, PR posting, and the orchestrator's upfront question block are orchestrator concerns. Evaluators never ask questions.
- **Never hand-delete generated files.** Old skill dirs leave the generated roots via feature `01`'s pruning. This is a standing architectural commitment across the phase.

## Constraints

- **Retain verbatim in force** (plan §E — these are security-relevant and are the *only* remaining constraint on evaluator shell use, since the `execute`-narrowing deliverable was deleted from this phase as inexpressible on Claude):
  - the ≤10-line return-summary contract and reports-on-disk rule (AC6),
  - read-only worktree etiquette,
  - "never treat an unavailable evaluator, dependency, or worktree as a clean result,"
  - a narrowly scoped capability is always preferred to a broad grant.
  Softening any of these while rewriting the surrounding prose is a real regression with nothing behind it.
- **No branch name in any report path component** (AC3). The key is a SHA plus a timestamp, so no sanitizer is needed.
- **Strip all subphase concepts** (AC4): no `PHASE_0N` report root, no subphase attribution, no per-subphase subdirectories, no artifact-inventory refusal, no archive-before-overwrite. Note the orchestrator's archive-before-overwrite lives at `05-phase-final-review.agent.md:214-217` — remove the concept from the *skill*; the agent body is feature `04`'s.
- Depends on feature `01` (hard — AC8) and feature `02` (the five doomed agents would otherwise need skill-ref updates before deletion). Both must be merged first.
- Test baseline must stay green; expect `tests/test_readiness_synthesis_agents.py` to be the only existing test requiring an update.

## Scope Boundaries

- **`.github/skills/worktree-baseline/SKILL.md` — do not touch (AC9).** Deliberately generic and shared with `eval-grader`. Any modification must be justified in the implementation record. Resist rescoping it "for consistency."
- **`.github/skills/auditor-conventions/SKILL.md` — do not touch.** Explicit non-goal.
- **Do not rescope any evaluator's behavior.** This feature updates skill references and `05a`'s one prose line only. Features `05`–`07` rescope evaluator content.
- **Do not renumber agents.** `05g`/`05h`/`05j`/`05k`/`05l` keep their current slugs in this feature and renumber in their own.
- **Do not rename the orchestrator.** Feature `04-pr-review-orchestrator` owns that; the file is still `05-phase-final-review.agent.md` when this feature runs.
- **Do not update report roots inside agent bodies** (see D6) — features `04`–`07` own those.
- **Do not hand-delete anything from `claude/`, `opencode/`, or `codex/`.**
- **Do not add a third skill.** Two renames only.
- **Do not migrate orchestrator concerns into the conventions skill** — it is a natural dumping ground for anything "shared." Base derivation and PR posting stay out.

## Relationships to Sibling Plans

- **Depends on `01-propagator-orphan-pruning`** — hard, via AC8. The rename is a delete-plus-create to the propagator; there is no rename detection. **Per D2, `01`'s scope must include fixing the broken codex prune guard, not only adding Claude/OpenCode pruning.** Per D4, `01` cannot use a header marker for Claude/OpenCode skills.
- **Depends on `02-retired-evaluator-removal`** — the five retired agents (`05c`, `05d`, `05e`, `05f`, `05i`) would otherwise need skill-ref updates before deletion.
- **Blocks `04`–`07`.** Every evaluator and the orchestrator are authored against these contracts; the report roster and filenames settled here are their inputs.
- **Shares files with `04`–`07`** — touches each surviving `05x` agent's skill-reference line; those features then rewrite the same files. This is the sequential reason.
- **`07-synthesis-and-pr-posting`** further rewrites `tests/test_readiness_synthesis_agents.py`; this feature only retargets its two skill-name assertions (lines 12–13).
- **`08-retirement-reconciliation`** should record the unverified assumption below.

## Suggested Implementation Order

Wave 3, sequential, after `01` and `02` are merged. Within the feature: Stage 1 (settle the contract) → Stage 2 (conventions skill) → Stage 3 (report skill) → Stage 4 (references + prove pruning). Stage 1 first because every later feature consumes its output.

## Environment State

| Property | Value |
|---|---|
| Tech Stack | Markdown skills (`SKILL.md`) with YAML frontmatter in `.github/skills/`, propagated to `claude/skills/`, `opencode/skills/`, `codex/skills/` by `scripts/propagate_master_assets.py` (Python) |
| Test Runner | `.venv/bin/python -m pytest tests/ -q` — **system `python3` has no pytest; the `.venv` interpreter is required** |
| Test Baseline | 416 passed, 15 subtests passed — captured 2026-07-16 across 4 consecutive full runs, all green |
| Lint | Not configured (`pyproject.toml` contains only `[tool.pytest.ini_options]`) |
| Format | Not configured |

## Relevant Learnings

From `.github/learnings/cross-phase-decisions.md`:

- **Propagation contracts (line 67–73):** "The current master-asset propagator's generated roots are `claude/`, `opencode/`, and `codex/`; `.claude/skills/` and `.claude/agents/` are [not]. `$source` metadata is guaranteed for propagated hook JSON entries, **not for generated skill Markdown** or agent Markdown/TOML. Downstream checks must not require that metadata on non-hook assets without a corresponding propagator change." — Directly corroborates **D4**: the Claude/OpenCode skill roots have no provenance marker to prune on.
- **Line 56:** "the propagation-enumeration gap omitting `05g`/`05j`/`05k` (**only correct once the roster is settled at seven contiguous slugs**)." — This feature is what settles that roster. The enumeration fix is downstream but depends on Stage 1's output.
- **Line 58:** Per-agent command scoping is not expressible on Claude; the `execute`-narrowing deliverable was deleted from this phase. This is *why* the conventions skill's prose constraints on shell use (plan §E) are load-bearing and must not be softened.
- **Line 12:** "A fixed budget must never be relaxed to make a gate pass." — Generalizes here: do not weaken a retained contract (the ≤10-line cap, the no-clean-result-from-absence rule) to make the rescope read more cleanly.
- **Line 16:** "when the honest fix requires capability a phase has excluded, the phase records the finding — it does not redefine the finding to fit the scope." — Applies to D2/D3: record, route, and do not silently reinterpret.

From `.github/learnings/review-learnings.md`:

- **Line 291:** "Propagation regression tests must cover every newly added agent output" — extends to renamed skill outputs here (AC8).
- **Line 263:** Flags "propagation tests that verify only unrelated hooks or skills instead of the new agent outputs" as a known review failure. **D7** notes the existing skill test uses a generic `demo-skill` fixture — AC8's test must assert on the real renamed skill directories, not that fixture.

From `.github/learnings/debugging-learnings.md`:

- **Lines 7–13:** A rename in the propagator previously left broken `~/.codex/agents/` symlinks because outputs were renamed without the consumers following. "Both the symlink filename and the TOML `name` value must match exactly." — The same failure shape as this rename: AC1/AC2 require the `name:` frontmatter to move with the directory, and AC7 requires every consumer to follow.

## Unverified Assumptions (carried from the plan)

- That no consumer outside `.github/agents/05*` loads either skill by name. Verified for `.github/`, `tests/`, and `scripts/` by grep (2026-07-16); **not** verified for user-local configuration outside this repository (e.g. a personal `~/.claude/` setup referencing the old skill name). Out of the repo's control — route to `08-retirement-reconciliation`'s notes.
