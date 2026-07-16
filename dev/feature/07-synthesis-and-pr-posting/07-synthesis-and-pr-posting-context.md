# 07 Synthesis and PR Posting — Context

## Key Files

### Files being changed

| File | Role | Change Type |
|---|---|---|
| `.github/agents/05l-readiness-synthesizer.agent.md` | The existing synthesizer (86 lines). Source of the `git mv` to `05g-readiness-synthesizer.agent.md`. Already carries report-only synthesis, `Checks Not Run`, the "no blockers found, coverage incomplete" ceiling, ≤10-line return, and top-tier model assignment. | Rename + Modify |
| `.github/agents/05-pr-review.agent.md` | Orchestrator. **Does not exist yet** — feature `04` creates it by renaming `05-phase-final-review.agent.md`. Feature `07` adds the posting path to it. | Modify (after `04`) |
| `tests/test_readiness_synthesis_agents.py` | 101 lines. Six tests; three target `05i-learnings-harvester` and are deleted by feature `02`. The remaining three retarget to `05g`. | Modify (rewrite) |
| `tests/test_propagate_master_assets.py` | `test_phase_review_agents_match_all_generated_harness_outputs` holds the `expected_slugs` roster at lines 90–99. Currently 8 slugs, 4 of which name retired agents. | Modify |
| `opencode/agents/05l-readiness-synthesizer.md` | Generated. The only root whose **filename** carries the numeric slug — becomes `05g-readiness-synthesizer.md`. Old file orphans; feature `01` prunes it. | Regenerate (rename) |
| `claude/agents/z-readiness-synthesizer.md` | Generated. Stem-keyed, so the filename is **unchanged** by the rename; body content updates. | Regenerate |
| `codex/agents/z-readiness-synthesizer.toml` | Generated. Stem-keyed, filename unchanged; body content updates. | Regenerate |

### Read-only reference files

| File | Role |
|---|---|
| `.github/agents/prod-code-review.md` | The precedent gate whose conventions `05g` extends. **Explicitly a non-goal to modify.** The current `05l` body references it at line 67; that reference must survive (a test asserts it). |
| `.github/skills/pr-review-conventions/SKILL.md` | Renamed by feature `03` from `phase-final-review-conventions`. Supplies the severity vocabulary. |
| `.github/skills/pr-review-report/SKILL.md` | Renamed by feature `03` from `phase-final-review-report`. Supplies the readiness report template — the pinned input for AC2. |
| `.github/learnings/cross-phase-decisions.md` | Records the Review Contracts and the P5-SEC-02 resolution shape. |
| `docs/phases/PHASE_03/PHASE_03_SUMMARY.md` | The phase document. Lines 102–117 fix the `05a`–`05g` roster; line 178 fixes Wave 6's scope. |
| `scripts/propagate_master_assets.py` | The propagator. Filenames are keyed on the source slug for OpenCode and on the stem for Claude/Codex. |

## Discovery Delta

| Finding | Impact | Action |
|---|---|---|
| **`05g` slug is currently occupied.** `.github/agents/05g-artifact-sweeper.agent.md` exists today. Feature `05` renames it to `05c-artifact-sweeper`, freeing the slug. `07` depends on `05`, so ordering resolves it — but the plan never names the collision. | The `git mv` in Stage 1 fails or silently clobbers if feature `05` has not landed. This is a hard prerequisite the plan states only implicitly via `Depends on: 05`. | Add task — verify `05g-artifact-sweeper.agent.md` is gone before the `git mv`. |
| **WARNING — cross-feature test conflict.** Feature `05`'s plan (line 180) specifies a test asserting `opencode/agents/05g-*` is **absent** after pruning. Feature `07` then **creates** `opencode/agents/05g-readiness-synthesizer.md` (AC12). A glob-shaped absence assertion on `05g-*` will fail once `07` lands. | Feature `05`'s test passes in wave 4 and breaks in wave 6. Either `05`'s assertion must be narrowed to the exact stem `05g-artifact-sweeper.md`, or `07` must update it. | **Escalate to Decomposer** — decide which feature owns the narrowing. Task added to `07` as fallback. |
| **`.github/agents/05-pr-review.agent.md` does not exist.** Verified absent. Feature `04` creates it by renaming `05-phase-final-review.agent.md`. | Stage 3 cannot begin until `04` lands. Consistent with the declared dependency; recorded so the Implementer does not create the file. | None — dependency already declared. |
| **Brittle line-wrap-coupled assertion.** `tests/test_readiness_synthesis_agents.py:16` asserts `"never read\ncode" in body.lower()` — it depends on the exact newline position between "read" and "code" in the agent body (`05l` lines 31–32). Any rewrap of the rescoped body breaks it. | AC11 names only the lines 63/90 `execute` assertions as departing. This one survives the rescope and is a hidden tripwire. | Add task — replace with a wrap-independent assertion for the report-only contract (AC2/AC11). |
| **The canonical hand-off reports no longer exist.** `05l` lines 29–30 read `master-qa.md`, `security-rollup.md`, and `ac-regression-matrix.md`; `test:31` asserts `"canonical hand-off report"` in the body. All three are produced by `05c-qa-consolidator`, `05d-security-rollup`, and `05e-ac-regression` — **all retired** per `PHASE_03_SUMMARY.md:138`. | The plan's AC11 says "retarget to `05g`, the renamed skills, and the new report root" but never mentions removing the hand-off-report concept from body and test. It is a required part of the roster retarget. | Add tasks — strip hand-off reports from the body; drop/retarget the `test:31` assertion. |
| **Retired write-back sentence in the body.** `05l` lines 82–84 state "the orchestrator owns verdict write-back and the learnings agent owns draft proposals." Both concepts are retired (no write-back per AC5; `05i` deleted by feature `02`). | AC5 requires no write-back reference on any path. This sentence is the literal counterexample sitting in the file being renamed. | Add task — delete both clauses in Stage 1. |
| **`expected_slugs` roster is stale in 4 of 8 entries.** `tests/test_propagate_master_assets.py:90–99` lists `05c-qa-consolidator`, `05d-security-rollup`, `05e-ac-regression`, `05f-seam-analyzer` (all retired) and `05h`/`05i`/`05l` (all renamed or deleted). Lines 119–121 assert `05d-security-rollup` contains `NO-GO` and `NOT RUN`. | The roster must land at `05a`–`05g`. The `05d-security-rollup` conditional block must be removed, not just re-keyed — the new `05d` is `05d-consistency-auditor`, a different agent. Silently re-keying would assert `NO-GO` against the wrong agent. | Add task — reconcile roster to seven contiguous slugs; delete the `05d-security-rollup` conditional. |
| **P5-SEC-02's honest outcome is near-determined by the record.** `.github/learnings/cross-phase-decisions.md:82` states the finding "is closed by rebuilding the readiness path **in code** rather than asserting it in prose." This feature ships agent Markdown. Line 16 records the governing rule: when the honest fix requires excluded capability, record the finding, do not redefine it. | AC6 is satisfiable either way, but "tightened the prose" is pre-emptively disqualified by two recorded entries. The plan (Section B) already anticipates this; the learnings make the default outcome **remains open, recorded with an owner**. | None — plan is correct. Recorded so Stage 2 does not relitigate. |
| **Rename does not touch Claude/Codex filenames.** `claude/agents/z-readiness-synthesizer.md` and `codex/agents/z-readiness-synthesizer.toml` are stem-keyed; only `opencode/agents/` carries the numeric slug. | AC12's "propagates to all three roots" is real, but only OpenCode produces an orphan. Narrows the pruning surface. | None — refines AC12 scope. |
| **`.github/agents/prod-code-review.md` verified present.** The `05l:67` reference and `test:14`'s assertion on the path string are both live. | The rescope must preserve the literal string `.github/agents/prod-code-review.md`. | None — confirms plan Section C. |
| **No execution manifest covers features 01–08.** `dev/feature/` holds manifests for phases 01, 02, 03, and 04, but none lists `07-synthesis-and-pr-posting`. The `phase-03-*-execution-manifest.md` predates the rescope. | Not this feature's deliverable, but the Wave-6 schedule this plan depends on is unrecorded in any manifest. | **Note to Decomposer** — manifest for the rescoped phase appears absent. |

## Architectural Decisions

- **Rescope, don't rewrite** (plan Section C). The existing `05l` is close to correct: report-only synthesis, `Checks Not Run`, the GO ceiling, ≤10-line return, top tier. All are verified present in the current body and locked by the current tests. What changes is the report root, the roster it reads, and the deletion of verdict write-back. Preserve the rest verbatim.
- **`05g` extends `prod-code-review` on a different axis, not one level up.** `prod-code-review` gates a phase's feature set from pipeline documents; `05g` gates a branch diff from evaluator reports. The current body says "one level up" (line 67) — the multi-subphase framing, which the rescope removes. The reference stays; the framing changes to a complement, not a superset.
- **The report file is the verdict.** No status-line write-back anywhere, by anyone (AC5). This is the recorded decision that deleted the two-file transactional status-line edit — the phase's riskiest code, now with no reason to exist. In this project verdicts are issued by the user by hand.
- **The verdict is advisory.** No hook blocks push or merge on `NO-GO`; deferred to a hook-owning phase.
- **The `gh` grant costs nothing.** The orchestrator already holds unrestricted Bash for base derivation (`git symbolic-ref`, `git merge-base`, `git branch`). Adding `gh` widens no exposure. The phase's original premise — that granting `gh` meant granting every shell command and therefore needed an allowlist first — was recorded as false. Per-agent command scoping is not expressible on Claude at all.
- **Posting is one command with three outcomes**: posted / no PR / unavailable. Retries, formatting modes, and fallbacks accreting inside an agent prompt is the named complexity risk.
- **A question asked after the work is on disk blocks nothing.** This is why *ask when ready* is the recommended default and why the report must exist before the prompt.
- **The readiness report is the observability artifact.** `evaluator-status.jsonl` from feature `04` is its input. Add nothing else. The report must name the revision it examined.

## Constraints

- `05g` reads **report files only** — never code, diffs, worktrees, or other agents' internals.
- The `Checks Not Run` section cannot be omitted on any path.
- `GO` is invalid while any check is missing, unreadable, not-run, or failed. The ceiling is the exact string **no blockers found, coverage incomplete**.
- Every evaluator failure gets a record naming the evaluator, the check, and a concrete reason. A later evaluator's success never repairs an earlier one's failure.
- **Output to the PR is one-way** (AC9). Never read PR comments or any network-sourced text back in — this is a prompt-injection boundary, not a preference.
- With *never*, **no network call is made**.
- No new prompt beyond the upfront block, except the designed *ask when ready* confirmation.
- Never restore unrestricted shell permissions to satisfy an acceptance criterion.
- Severity vocabulary and ordering come from `pr-review-conventions`: Critical, High, Medium, Low; source order preserved within a severity.
- Report validation is metadata-only: readable, regular, non-empty, under the current run root. This is **not** validation of a report's claims.
- Concrete names copied exactly from the Phase document — do not rename: `05g-readiness-synthesizer`, `readiness-report.md`, `GO`, `GO WITH CONDITIONS`, `NO-GO`, `Checks Not Run`, `dev/pr-review/<base-sha-short>-<UTC-YYYYMMDDTHHMMSSZ>/`.

## Scope Boundaries

- **Do not modify `.github/agents/prod-code-review.md`** or `claude/agents/prod-code-review.md`. `05g` extends its conventions; it does not rewrite the existing gate.
- **Do not add hook-based enforcement** of the verdict. No hook blocks push or merge on `NO-GO`.
- **Do not implement auto-remediation** of findings.
- **Do not add PR-comment ingestion** on any path, including "just to check whether we already posted."
- **Do not attempt to narrow the orchestrator's `execute` to `gh`.** Not expressible on Claude; the allowlist deliverable was deleted from this phase.
- **Do not rename or rescope `05a`–`05f`.** Feature `05` owns `05c`/`05d`/`05e`; feature `06` owns `05b`/`05f`.
- **Do not create `.github/agents/05-pr-review.agent.md`.** Feature `04` creates it; `07` only adds the posting path to it.
- **Do not run live `gh` posting against this repository.** Live QA belongs in a scratch consumer repo.
- Preserve verbatim in the `05g` body: the `.github/agents/prod-code-review.md` reference, the four severity levels, the "no blockers found, coverage incomplete" string, `at most 10 lines`, `top available`, and `state-of-the-art`.

## Relationships to Sibling Plans

- **Depends on `04-pr-review-orchestrator`** — edits the same `.github/agents/05-pr-review.agent.md` file to add the posting path. This is the reason `parallel_safe: no`. Feature `04` captures the three-way consent choice in the upfront block (its AC2c) but explicitly defers the posting implementation here.
- **Depends on `05-mechanical-evaluators`** — its reports are `05g` inputs, **and** it frees the `05g` slug by renaming `05g-artifact-sweeper` → `05c-artifact-sweeper`.
- **Depends on `06-narrative-and-test-health`** — its reports are `05g` inputs.
- **Consumes `03-pr-review-conventions-skills`** — the `pr-review-report` templates are pinned inputs (AC2). Note feature `03` also edits `05l-readiness-synthesizer.agent.md` (skill references) **and** `tests/test_readiness_synthesis_agents.py`. Feature `07` must build on those edits, not revert them.
- **Depends on `01-propagator-orphan-pruning`** — prunes `opencode/agents/05l-readiness-synthesizer.md` after the rename (AC12).
- **Depends on `02-retired-evaluator-removal`** — deletes the three `05i-learnings-harvester` tests from `tests/test_readiness_synthesis_agents.py`, including the lines 63/90 `execute` assertions. This feature finishes the rewrite.
- **Blocks `08-retirement-reconciliation`**, which verifies the whole assembly: `05a`–`05g` exist in all three roots and no `05h`–`05l` slug survives anywhere.

## Suggested Implementation Order

Stage 1 → Stage 2 → Stage 3 → Stage 4, as written in the plan. Stage 1 (rename) must precede Stage 3 (posting) only loosely — they touch different files — but Stage 4's suite rewrite depends on both. Stage 2 is a recorded decision and can proceed in parallel with Stage 3.

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Agent definitions as Markdown with YAML frontmatter in `.github/agents/`; propagated to `claude/`, `opencode/`, `codex/` by `scripts/propagate_master_assets.py`. Tests are Python (pytest + unittest). |
| Test Runner | `.venv/bin/python -m pytest tests/ -q` — **system `python3` has no pytest; the `.venv` interpreter is required** |
| Test Baseline | 416 passed, 15 subtests passed — captured 2026-07-16 across 4 consecutive full runs, all green. Expect a lower count at this feature's start: feature `02` deletes tests. |
| Lint | Not configured |
| Format | Not configured |

## Relevant Learnings

From `.github/learnings/cross-phase-decisions.md`:

**Review Contracts** (scope-independent; carry into PR Review unchanged):
- Missing or incomplete required checks are a hard readiness gate: the canonical verdict is `NO-GO`. An unverified verdict must not update roadmap or summary status lines. **In this project verdicts are issued by the user by hand; no agent writes a status line.** (→ AC5)
- A failed, hung, or unavailable evaluator never becomes a passing result, and a later evaluator's success never repairs an earlier one's failure. Every such case gets a record naming the evaluator, the check, and a concrete reason, and the readiness report must enumerate them by name. (→ AC4)
- Report validation is metadata-only at the orchestrator (readable, regular, non-empty, under the run's report root) and must not be mistaken for validating a report's *claims*. Validating claims requires a strict schema and a deterministic status reducer over structured records — **this is P5-SEC-02, and it is closed by rebuilding the readiness path in code rather than asserting it in prose.** (→ AC6)
- Fixture dry-runs remain required release evidence for agent wiring and degradation behavior. Static contract review cannot observe runtime report creation. (→ Stage 4)
- **Never restore unrestricted shell/Bash permissions to satisfy an evaluator acceptance criterion.** This bound `05i`'s history mining, which is retired; the rule outlives it and now governs the `gh` grant. The correct move is a narrowly scoped capability — never a broad grant with a comment explaining why it is fine. (→ Stage 3)

**On P5-SEC-02 specifically:**
- Some High findings are not closable without new capability, and recording them honestly is the correct outcome. P5-SEC-02: no code to attach a schema/reducer to, because the readiness path is agent Markdown; **a prose constraint is exactly what the Phase 03 scan faulted, so tightening wording would make the record say closed without closing anything.** The general rule: **when the honest fix requires capability a phase has excluded, the phase records the finding — it does not redefine the finding to fit the scope.**
- The rescope rebuilds that path, so the validator arrives with the rebuild instead of being new capability bolted onto prose.

**On the `gh` grant:**
- **The `gh` grant never cost anything.** The premise was "grant `gh` = grant every shell command." But the orchestrator needs `git symbolic-ref`/`git merge-base`/`git branch` for base derivation, so it holds unrestricted Bash *regardless*. Adding `gh` widens nothing.
- Per-agent command scoping is **not expressible on Claude at all**: `tools: Bash(gh:*)` is an unresolved tool name, and Claude Code refuses to launch the subagent. OpenCode supports real per-agent `permission.bash` globs; Codex has none. Native scoping exists on one of three harnesses.

**On the upfront interaction:**
- **A question asked after the work is on disk blocks nothing.** That is what makes "ask me once the report is written" both unattended and safe — the user sees the content before it is published. **Guard this: it is the requirement most likely to erode silently, one reasonable-seeming question at a time.** (→ AC7, AC10)

**On the rescope shape:**
- **No verdict write-back**: the report file is the verdict, which deletes the two-file transactional status-line edit, its unique-match ambiguity detection, and its restore-on-second-write-failure path — the riskiest implemented code in the phase, now with no reason to exist. The five phase-shaped evaluators are deleted from source and all three generated roots; the seven survivors renumber contiguously to `05a`–`05g`. The verdict is advisory.

**On propagation:**
- The propagator's generated roots are `claude/`, `opencode/`, and `codex/`. Generated filenames are keyed on the source slug for OpenCode, so `05l-readiness-synthesizer` → `05g-readiness-synthesizer` orphans `opencode/agents/05l-readiness-synthesizer.md`. Claude and Codex are stem-keyed and unaffected.
