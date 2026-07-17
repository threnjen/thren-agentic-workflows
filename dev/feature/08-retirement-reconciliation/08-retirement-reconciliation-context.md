# 08 Retirement Reconciliation — Context

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Markdown + YAML frontmatter source assets in `.github/` (agents, skills, instructions, learnings); Python 3 propagator (`scripts/propagate_master_assets.py`, ~58KB) generating `claude/`, `opencode/`, `codex/` roots |
| Test Runner | `.venv/bin/python -m pytest tests/ -q` — **system `python3` has no pytest; the venv interpreter is mandatory** |
| Test Baseline | 416 passed, 15 subtests passed — captured 2026-07-16 across 4 consecutive full runs, all green |
| Lint | Not configured |
| Format | Not configured |

**Baseline caveat (load-bearing for AC9):** PERF-01, a propagated-guard latency gate owned by Phase 04, is documented as failing probabilistically. It did not fire in 4 consecutive runs, but a single green run is not a baseline. If PERF-01 fires during this feature's suite runs, that is expected and **must not** be "fixed" by relaxing the budget. Capture repeated runs instead.

## Key Files

### Files being changed

| File | Role | Change Type |
|------|------|-------------|
| `.github/agents/README.md` | Agent catalogue. Carries the stale roster in orchestrator table (line 136), subagent table (lines 163-172), agent detail prose (lines 195-196), and the "Four orchestrators" note (line 412) | Modify |
| `docs/CODEBASE_CONTEXT.md` | Architecture summary. Line 89 names "Phase Final Review evaluators" and asserts an exact subagent count | Modify |
| `README.md` | Root readme. Line 130 names "Phase Final Review orchestration and evaluators" and asserts an exact source-agent count | Modify |
| `.gitignore` | **Lines 6-9 carry `dev/phase-final-review/` fixture-preservation rules.** See Discovery Delta DD-1 — this is both a dangling reference and a functional gap | Modify |
| `.github/learnings/cross-phase-decisions.md` | AC10 reconciliation target. PR-Review Rescope section starts line 49; the allowlist "forcing function" entry is line 57 with corrections at lines 58-59 | Modify |
| `tests/test_propagate_master_assets.py` | Final roster reconciliation + idempotency assertion (AC8). Contains `test_phase_review_agents_match_all_generated_harness_outputs` with an `expected_slugs` tuple | Modify |
| `tests/test_readiness_synthesis_agents.py` | Final consistency pass on the assembled roster | Modify |
| `[PROPOSED - name TBD]` reference-sweep test | Introduced by feature `02` (its AC6, itself marked `[PROPOSED - name TBD]`); this feature **extends** it to old slugs, skill names, and command names. The file does not exist yet — do not assume a filename | Modify (extend) |

### Read-only reference

| File | Role |
|------|------|
| `scripts/propagate_master_assets.py` | `_build_agent_reference_map` (line 412) rewrites references by `name:`, longest-first; `_claude_identifier_for` (line 408) derives the generated Claude command/agent filename. Read the propagator's *output* to learn the real command filename — do not assume it |
| `.github/agents/05-pr-review.agent.md` | The orchestrator under test (renamed by feature `04` from `05-phase-final-review.agent.md`) |
| `.github/agents/04e-diff-security-scan.agent.md` | Exists today. The delegated security scan required by AC1 |
| `dev/pr-review/fixtures/` | Pinned base/branch SHA pair created by feature `04`; the dry run's input |
| `claude/commands/` | AC7 target. `phase-final-review.md` exists today and must be absent after |
| `.github/skills/pr-review-conventions/`, `.github/skills/pr-review-report/` | Renamed by feature `03` from `phase-final-review-conventions` / `phase-final-review-report` |
| `docs/phases/**`, `.github/learnings/**` | Historical records — AC6-exempt |

## Discovery Delta

| Finding | Impact | Action |
|---------|--------|--------|
| **DD-1 — `.gitignore` lines 6-9 carry `dev/phase-final-review/` rules and no sibling plan owns the file.** The rules un-ignore `dev/phase-final-review/fixtures/` and ignore run outputs. `dev/phase-final-review/` is gone from disk, but feature `04` creates `dev/pr-review/fixtures/` and the orchestrator writes `dev/pr-review/<base-sha-short>-<timestamp>/`. **Neither path is covered:** dry-run outputs are not ignored and would be committed as repo noise, and the fixture has no preservation rule. This is a functional gap, not only a stale string. It also refines the plan's non-goal *"Retiring `dev/phase-final-review/` — verified absent from disk"*: the directory is absent, its gitignore rules are not | AC6 sweep hit that nobody's plan owns; AC1's dry run will pollute the working tree; AC8's "no unrelated diff noise" is harder to assess with untracked run output present | **Add task** (Stage 1). Warn Decomposer: `.gitignore` is missing from every feature's key-files list |
| **DD-2 — The AC6 exemption list is too narrow: `dev/**` is not exempt.** A sweep over "every tracked file outside `docs/phases/**` and `.github/learnings/**`" fires on all 10 feature plans plus 2 execution manifests — including `08-retirement-reconciliation-plan.md` itself, and `dev/feature/phase-03-phase-final-review-execution-manifest.md` whose *filename* carries the retired slug | The sweep test cannot pass as specified. Planning records are historical records for the same reason `docs/phases/**` is | **Update plan** — extend the exemption to `dev/**`. Warn Decomposer |
| **DD-3 — Propagated learnings roots are not exempt.** `claude/learnings/cross-phase-decisions.md` is tracked and is a generated copy of an exempt source. `.github/learnings/**` is exempt; `claude/learnings/**` is not | Sweep fires on a file whose content is not independently editable — fixing it means editing the exempt source, which contradicts the exemption | **Update plan** — exempt propagated learnings roots alongside their source |
| **DD-4 — The surviving prose form in the two AC6 doc surfaces is neither the slug nor the `name:` display name.** `README.md:130` reads "Phase Final Review orchestration and evaluators" and `docs/CODEBASE_CONTEXT.md:89` reads "Phase Final Review evaluators" — **no hyphens**. The `name:` display name is `05 Phase - Final Review`. A sweep matching slugs *or* `name:` display names misses **both** AC6 surfaces entirely | This sharpens the plan's own Section B point rather than contradicting it: the plan says "match display names, not just slugs," but display-name matching is still insufficient. A third pattern class — informal prose forms — is required | **Add task** (Stage 1). This is the highest-value refinement in this delta |
| **DD-5 — Both AC6 doc surfaces assert exact counts that feature `02` invalidates.** `README.md:130` says "43 source agent definitions"; `docs/CODEBASE_CONTEXT.md:89` says "24 hidden subagents". Feature `02` deletes 5 agents | Correct counts are part of AC6's "no dangling references," and a stale count is invisible to any name-based sweep | **Add task** (Stage 1) — recount from `.github/agents/` after propagation, do not arithmetic the old number |
| **DD-6 — The reference-sweep test file does not exist.** Feature `02`'s AC6 introduces it and its own plan marks the symbol `[PROPOSED - name TBD]`. Feature `08` Test Plan item 2 describes extending it | The implementer must read feature `02`'s implementation record for the chosen filename, not invent one | **None** — plan already avoids naming it. Recorded so the implementer does not guess |
| **DD-7 — `claude/commands/pr-review.md` correctly carries `[PROPOSED - name TBD]`.** Verified `_claude_identifier_for` exists at `scripts/propagate_master_assets.py:408` and derives the stem | Plan's marker is accurate | **None** |
| **DD-8 — AC10's target verified.** `.github/learnings/cross-phase-decisions.md:57` is the forcing-function entry; lines 58-59 already carry two corrections (per-agent scoping not expressible on Claude; the `gh` grant never cost anything). The plan's description matches the file | AC10 is verification, not authoring | **None** |
| **DD-9 — No phase-scoped test directory pattern exists.** `tests/` is flat plus `tests/hooks/`. No `Phase*/` convention | The consolidated-phase-test-file concern does not apply | **None** |
| **DD-10 — `dev/phase-final-review/` confirmed absent from disk** (2026-07-16), matching the plan's non-goal — but see DD-1 for the `.gitignore` residue | Non-goal is accurate as written about the directory | **None** |

## Architectural Decisions

- **No new patterns.** This feature verifies that features `01`–`07` produced a coherent whole. Its output is evidence, not runtime behavior.
- **The sweep is a test, not a checklist.** A checklist verifies once; a test verifies forever. This phase has established that stale references survive propagation silently — the propagator rewrites by `name:` via `_build_agent_reference_map`, so once a source agent is renamed, a surviving display name in prose stops being rewritten and ships as a literal string. Feature `02` introduces the sweep; this feature extends it to old slugs, skill names, and command names.
- **The dry run is required release evidence, not a nicety.** Recorded contract: *"Static contract review cannot observe runtime report creation, and a run whose required evaluators are recorded `not-run` is artifact-level, below-GO evidence — not a passing dry run."* A dry run in which five of seven evaluators report not-run does **not** satisfy AC1; it is evidence the wiring is broken.
- **Deliverable 7 is split deliberately.** Feature `02` performed the deletion early so the five doomed agents did not have to be dragged through every rename. This feature keeps the role the Phase document described: *the integration point where dangling references surface.*
- **Honest security accounting over reworded closure.** The phase set out to narrow every `05x` `execute` grant and **cannot** — per-agent command scoping is not expressible in Claude subagent frontmatter, works natively only on OpenCode, and does not exist per-profile on Codex. What was achieved is narrower and real: `execute` removed where unneeded (feature `05`), never added where absent (feature `06`), retained only where a named command has no non-shell equivalent. What remains open is recorded with routing (AC11) rather than reworded into looking closed.
- **No observability added.** This feature's output is evidence, not runtime behavior.

## Constraints

- **Verdicts are issued by the user, by hand.** An unverified verdict must not update `docs/phases/**` roadmap or summary status lines.
- **The forced-failure run must not produce `GO`.** This is a negative success criterion.
- **Every subagent return ≤10 lines**, full detail on disk (AC4).
- **Exactly one question block** for the whole run (AC2). The recorded rule: *a question asked after the work is on disk blocks nothing* — that is what makes "ask me once the report is written" both unattended and safe. This is the requirement most likely to erode silently, one reasonable-seeming question at a time.
- **Scratch-repo QA runs in a scratch consumer repo, never this one** (`origin/HEAD` unset; base correction; no PR open; `gh` unauthenticated).
- **Do not relax the PERF-01 budget to make a gate pass.** It is probabilistic and owned by Phase 04.
- **An unexplained test count is not a baseline.** The repo has already recorded a coin-flip green run being mistaken for one.
- Use `.venv/bin/python`, never system `python3`.

## Scope Boundaries

- **Do not delete the five retired evaluators** — done in feature `02`.
- **Do not rescope any agent** — done in features `03`–`07`.
- **Do not fix findings the dry run surfaces about *this* repository.** The dry run proves the machinery works; the findings it produces about the branch are outputs, not bugs. This is the easiest boundary to cross by accident.
- **Do not update `docs/phases/**` status lines.**
- **`docs/phases/**` and `.github/learnings/**` are AC6-exempt** as historical records — do not sweep them to extinction. Per DD-2 and DD-3, `dev/**` and propagated learnings roots should join them.
- **Do not retire `dev/phase-final-review/`** — already absent from disk. (Its `.gitignore` residue is in scope per DD-1.)
- Preserve `04e-diff-security-scan` and `security-scan.agent.md`; no new security agent is authored.

## Relationships to Sibling Plans

- **Wave 7. Depends on every prior feature** (`01`–`07`); directly declared on `07-synthesis-and-pr-posting`. **Not parallel safe.** It is the assembly test and cannot verify an assembly that does not exist yet.
- **Completes the Phase document's Deliverable 7**, whose deletion half landed in feature `02`.
- **Extends feature `02`'s reference sweep** (its AC6) from retired evaluators to old slugs, skill names, and command names, pointed at the documentation surfaces. See DD-6.
- **Consumes feature `04`'s fixture** at `dev/pr-review/fixtures/` and its renamed `05-pr-review` orchestrator.
- **Re-verifies feature `07`'s AC5** (no status-line write-back) on the assembled roster.
- **Depends on feature `07` for AC11's P5-SEC-02 status** — feature `07`'s AC6 either closes it or records it open.
- **Feeds `@project-planner`** — AC11's deferred capabilities need routing, and the adoption-readiness roadmap entry remains outstanding.

## Suggested Implementation Order

Stages are ordered by dependency and must run in sequence:

1. **Stage 1 (Sweep to Extinction)** before **Stage 2 (Verify Propagation)** — sweep fixes touch source assets that must then propagate.
2. **Stage 2** before **Stage 3 (End-to-End Dry Run)** — the dry run exercises the propagated family; running it against an unpropagated or stale roster tests nothing.
3. **Stage 3** before **Stage 4 (Reconcile the Record)** — the dry run's outcome is an input to AC11's deferred-capability routing and to AC9's count reconciliation.

Stage 0 is **not required**: baseline 416 passed across 4 consecutive full runs (2026-07-16), adjusted by features `01`–`07`.

## Relevant Learnings

From `.github/learnings/cross-phase-decisions.md`:

- **Line 16 — When the honest fix requires capability a phase has excluded, the phase records the finding; it does not redefine the finding to fit the scope.** Three Phase 04 High findings are unclosable without new capability, including **P5-SEC-02** (readiness-report trust boundary — the readiness path is agent Markdown with no code to attach a schema/reducer to; a prose constraint is exactly what the Phase 03 scan faulted, so tightening wording would make the record say closed without closing anything). Each is recorded open with routing. **Directly governs AC11.**
- **Lines 57-59 — the forcing-function entry and its two corrections.** The original claim (the propagator's missing `execute` allowlist syntax was the binding constraint) is **void**: per-agent command scoping is not expressible on Claude at all — `tools:` accepts only bare tool names and MCP patterns, `Bash(gh:*)` is an unresolved tool name and Claude Code refuses to launch the subagent. OpenCode supports real per-agent `permission.bash` globs; Codex has no per-profile command list. Native per-agent scoping exists on **one of three harnesses**; building it anyway would be *"partial protection that reads as total protection."* The sharper correction: the `gh` grant never cost anything — the orchestrator holds unrestricted Bash regardless for `git symbolic-ref`/`merge-base`/`branch`. **The lesson: "look for the forcing function rather than re-recording the risk" was good advice that found a fake one. A forcing function is only real if the feature is actually blocked without the capability.** **This is AC10's exact target.**
- **Line 60 — the rescope's recorded decisions:** no verdict write-back (the report file *is* the verdict); five phase-shaped evaluators deleted and seven survivors renumber contiguously to `05a`–`05g`; reports at `dev/pr-review/<base-sha-short>-<UTC-timestamp>/` keyed only by hex and digits so no branch name reaches a filesystem path; verdict advisory, with the `NO-GO` blocking hook deferred to a hook-owning phase; security delegated to existing `04e-diff-security-scan`.
- **Line 61 — If a rescope only relocates work, suspect the new scope is the old scope wearing a hat.** A good rescope deletes work.
- **Line 62 — One upfront interaction is a design outcome, not a politeness feature.** Base confirmation is the only blocking question left; the PR-comment choice joins it in the same block. **Guard this: AC2.**
- **Line 63 — When a deliverable is slated for rescope, verifying it as-built is archaeology.** Phase 03's verdict is NO-GO, superseded rather than repaired.
- **Line 82 — Report validation is metadata-only at the orchestrator** (readable, regular, non-empty, under the run's report root) **and must not be mistaken for validating a report's *claims*.** That is P5-SEC-02.

**Phase history warning (from the plan, corroborated by the record):** the whole-phase flow *never successfully ran against a real phase* — which is why little working code is lost in the rescope. That is a warning, not trivia: **this agent family has never demonstrably worked end to end. AC1 is the first time it would.**
