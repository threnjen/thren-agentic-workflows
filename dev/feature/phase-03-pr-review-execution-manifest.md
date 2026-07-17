# Phase 03 — PR Review Agent Family: Execution Manifest

**Phase document:** `docs/phases/PHASE_03/PHASE_03_SUMMARY.md`
**Discovery context:** `docs/phases/PHASE_03/PHASE_03_DISCOVERY_CONTEXT.md`
**Decomposed:** 2026-07-16

This manifest is the single source of truth for `@phase-execute`. Consume it as-is;
do not reconstruct the schedule from the plan files.

> **Supersedes `phase-03-phase-final-review-execution-manifest.md`**, which predates
> the rescope. Feature `08` deletes it.

## Ordered Feature List

1. `01-propagator-orphan-pruning`
2. `02-retired-evaluator-removal`
3. `03-pr-review-conventions-skills`
4. `04-pr-review-orchestrator`
5. `05-mechanical-evaluators`
6. `06-narrative-and-test-health`
7. `07-synthesis-and-pr-posting`
8. `08-retirement-reconciliation`

## Ordering note

Feature order departs from the Phase document's Key Deliverables sequence in three
ways. All three are recorded here rather than absorbed silently.

1. **Deliverable 1 (propagator command-allowlist + scoped `execute` grants) is
   deleted, not implemented.** User decision, 2026-07-16, after decomposition
   research disproved its premise. A Claude subagent's `tools:` frontmatter accepts
   only bare tool names; `tools: Bash(gh:*)` is an *unresolved tool name* that makes
   Claude Code refuse to launch the agent. There is no per-subagent `permissions` key.
   Per-agent command scoping is native on **OpenCode only**, absent per-profile on
   **Codex**, and on **Claude** requires a PreToolUse hook — which this phase
   excludes. The allowlist would have been real on one of three harnesses and
   decorative on two.

   The premise also failed on its own terms: the orchestrator needs
   `git symbolic-ref` / `git merge-base` / `git branch` for base derivation, so it
   holds unrestricted Bash regardless; adding `gh` widens nothing. Per-agent command
   scoping is deferred to a hook-owning phase and recorded with routing in
   `.github/learnings/cross-phase-decisions.md`. **The narrowing that survives is
   removal**: `execute` is dropped from evaluators that do not need it (`05`), never
   added to those that never had it (`06`), and declared where genuinely required
   (`05a`, orchestrator).

2. **Deliverable 7 (retirement) is split, and its deletion half moved first.**
   The Phase document sequences retirement last as "the integration point where
   dangling references surface." That rationale applies to *reconciliation*, which
   stays last as feature `08`. The *deletion* moved to feature `02` because every
   surviving `05x` agent references the two skills feature `03` renames — leaving
   the five doomed agents in place would mean updating files about to be deleted,
   and carrying them through the blast radius of features `03`–`07`.

3. **A propagator feature was added that the Phase document does not contain**
   (`01-propagator-orphan-pruning`), and it is first. The Phase's success criterion
   *"the five retired evaluators are absent from all three generated roots"* is not
   satisfiable by running the propagator today. Measured 2026-07-16:

   | Root | Prunes orphans? | Evidence |
   |---|---|---|
   | `codex/agents/*.toml` | yes | 46/46 carry the guard marker |
   | `codex/profiles/*.config.toml` | yes | works |
   | `codex/skills/*/` | **no — dead code** | **0/24** match its `startswith` guard; marker sits on line 5, below frontmatter |
   | `claude/agents/*.md` | no | 0/35 carry any marker |
   | `claude/commands/*.md` | no | 0/19 carry any marker |
   | `opencode/agents/*.md` | no | 0/46 carry any marker |
   | `claude/skills/`, `opencode/skills/` | no | no marker at all |

   Every later feature deletes or renames a source asset, so this must land first.

Minor scope moves, recorded in the affected plans: the pinned fixture moved from
Deliverable 2 to feature `04` (it is a base/branch SHA pair, meaningful only in
terms of base derivation); the `04e-diff-security-scan` delegation seam moved from
Deliverable 5 to feature `04` (it is an orchestrator invocation, and the roster must
live in one place).

## Deferred from the Phase document, with rationale

| Phase requirement | Disposition |
|---|---|
| Deliverable 1 — propagator command-allowlist, scoped `execute` per agent | **Deleted** (ordering note 1). Deferred to a hook-owning phase; recorded with routing. |
| Success criterion *"no agent in `.github/agents/` carries an unrestricted shell grant"* | **Narrowed to the PR Review family.** As written it contradicts the Phase's own Out of Scope line: **26 agents** declare `execute`, including `04-phase-execute` and its subagents, which the Phase explicitly refuses to touch — and `debugger`, `test-writer`, `single-feature-agent`, whose purpose is running commands. The remaining 21 are out of scope and deferred. |
| `05a-baseline-worktree`'s unconstrained `execute` | **Declared, not closed.** `git worktree` has no non-shell equivalent; recorded as unclosable. Feature `05` AC8b forces it into the propagation roster with an explicit expected-tools list, so the grant is visible rather than hidden by omission from the test tuple. |
| P5-SEC-02 (readiness-report trust boundary) | **Owned by feature `07`, expected to remain open.** The recorded finding says it closes by rebuilding the readiness path *in code*; this phase ships agent Markdown. Feature `07` must record it open with an owner rather than close it by firming up prose. |
| Retire `dev/phase-final-review/fixtures/PHASE_05/` and `dev/phase-final-review/PHASE_05/` | **Moot** — verified 2026-07-16, the directory does not exist. Only the stale `.gitignore` rules remain (feature `08`). |
| Author `worktree-baseline` skill | **Already exists**, already generic, already propagated. Zero work; feature `03` AC9 forbids touching it. |

## Feature Table

| Feature | Wave | Parallel Safe | Depends On | Key Files Modified | Sequential Reason |
|---|---|---|---|---|---|
| `01-propagator-orphan-pruning` | 1 | yes | none | `scripts/propagate_master_assets.py`, `tests/test_propagate_master_assets.py` | n/a |
| `02-retired-evaluator-removal` | 2 | no | `01` | 5 × `.github/agents/05{c,d,e,f,i}-*.agent.md` (delete), `.github/agents/05-phase-final-review.agent.md`, `.github/agents/README.md`, `tests/test_propagate_master_assets.py`, `tests/test_readiness_synthesis_agents.py`, generated roots | runtime dependency on `01` (generated outputs unremovable without it); shares `tests/test_propagate_master_assets.py` with `01` |
| `03-pr-review-conventions-skills` | 3 | no | `01`, `02` | `.github/skills/pr-review-conventions/SKILL.md`, `.github/skills/pr-review-report/SKILL.md`, skill-reference lines in 7 × `.github/agents/05*.agent.md`, `tests/test_readiness_synthesis_agents.py`, generated skill roots | runtime dependency on `01` (rename orphans all three skill roots); shares every surviving `05x` agent file with `04`–`07` |
| `04-pr-review-orchestrator` | 4 | no | `01`, `02`, `03` | `.github/agents/05-pr-review.agent.md`, `dev/pr-review/fixtures/`, `.gitignore`, `tests/test_pr_review_orchestrator.py` (new), `tests/test_propagate_master_assets.py`, generated roots incl. `claude/commands/` | runtime dependency on `03`'s report contract; shares `.github/agents/05-phase-final-review.agent.md` with `02` and `07`; shares `tests/test_propagate_master_assets.py` |
| `05-mechanical-evaluators` | 5 | no | `02`, `03`, `04` | `.github/agents/05c-artifact-sweeper.agent.md`, `05d-consistency-auditor.agent.md`, `05e-dependency-auditor.agent.md`, `tests/test_propagate_master_assets.py`, generated roots | shares `tests/test_propagate_master_assets.py` roster with `06-narrative-and-test-health` in the same wave |
| `06-narrative-and-test-health` | 5 | no | `02`, `03`, `04` | `.github/agents/05b-change-narrator.agent.md`, `.github/agents/05f-test-health.agent.md`, `tests/test_propagate_master_assets.py`, generated roots | shares `tests/test_propagate_master_assets.py` roster with `05-mechanical-evaluators` in the same wave |
| `07-synthesis-and-pr-posting` | 6 | no | `04`, `05`, `06` | `.github/agents/05g-readiness-synthesizer.agent.md`, `.github/agents/05-pr-review.agent.md`, `tests/test_readiness_synthesis_agents.py`, `tests/test_propagate_master_assets.py`, generated roots | shares `.github/agents/05-pr-review.agent.md` with upstream `04`; shares both test files with upstream features |
| `08-retirement-reconciliation` | 7 | no | `07` (transitively all) | `.github/agents/README.md`, `docs/CODEBASE_CONTEXT.md`, `README.md`, `.gitignore`, `tests/test_propagate_master_assets.py`, `tests/test_readiness_synthesis_agents.py`, `.github/learnings/cross-phase-decisions.md`, `dev/feature/phase-03-phase-final-review-execution-manifest.md` (delete) | runtime dependency on every prior feature — it is the integration point and cannot verify an assembly that does not exist |

## Dependency Graph

```
01-propagator-orphan-pruning          (no deps)
   └── 02-retired-evaluator-removal   (runtime: needs pruning; file: test_propagate)
          └── 03-pr-review-conventions-skills  (runtime: needs pruning + retirement)
                 └── 04-pr-review-orchestrator (runtime: report contract; file: orchestrator, test_propagate)
                        ├── 05-mechanical-evaluators      (file: test_propagate roster)
                        └── 06-narrative-and-test-health  (file: test_propagate roster)
                               └── 07-synthesis-and-pr-posting (runtime: reports; file: orchestrator)
                                      └── 08-retirement-reconciliation (integration)
```

Reasons per edge:
- `02 → 01`: **runtime** — generated outputs cannot be removed without pruning.
- `03 → 01`: **runtime** — a skill rename orphans all three skill roots.
- `03 → 02`: **file/economy** — avoids updating five agents about to be deleted.
- `04 → 03`: **runtime** — the orchestrator is authored against `03`'s report roster,
  root, and return contract.
- `05, 06 → 04`: **runtime** — each evaluator is dry-run through the orchestrator.
- `05 ↔ 06`: **file** — both edit the `expected_slugs` roster. Same wave, sequential.
- `07 → 05, 06`: **runtime** — their reports are `05g`'s inputs.
- `07 → 04`: **file** — adds the posting path to the orchestrator.
- `08 → all`: **runtime** — the end-to-end assembly test.

## Execution Schedule

- **Wave 1 (parallel):** `01-propagator-orphan-pruning`
- **Wave 2 (sequential):** `02-retired-evaluator-removal`
- **Wave 3 (sequential):** `03-pr-review-conventions-skills`
- **Wave 4 (sequential):** `04-pr-review-orchestrator`
- **Wave 5 (sequential):** `05-mechanical-evaluators`, then `06-narrative-and-test-health`
- **Wave 6 (sequential):** `07-synthesis-and-pr-posting`
- **Wave 7 (sequential):** `08-retirement-reconciliation`

**This phase is almost entirely sequential, and that is a finding rather than a
scheduling failure.** Three files thread through nearly every feature —
`scripts/propagate_master_assets.py`, `tests/test_propagate_master_assets.py`, and
the orchestrator — and the roster assertion in the propagation test is touched by
five of eight features. Manufacturing parallelism here would mean concurrent edits
to the same roster tuple.

## Expected Bundle Files

Each feature directory contains exactly three files:

```
dev/feature/[0N-task-name]/
├── [0N-task-name]-plan.md
├── [0N-task-name]-context.md
└── [0N-task-name]-tasks.md
```

Verified present for all eight features (24 files), each plan carrying an
`## Execution Metadata` section.

## Verification Assets

### New Test Files

| Path | Associated Feature(s) | Purpose |
|---|---|---|
| `tests/test_pr_review_orchestrator.py` `[PROPOSED - name TBD]` | `04-pr-review-orchestrator` | Contract assertions over the orchestrator body: deleted-machinery absence (ledger, subphase discovery, write-back, archive), base-suggestion fallback order, self-exclusion, single-interaction, report-root shape. No existing test file covers the orchestrator. |

### Existing Test Files Updated By Multiple Features

| Path | Associated Feature(s) | Purpose |
|---|---|---|
| `tests/test_propagate_master_assets.py` | `01`, `02`, `04`, `05`, `06`, `07`, `08` | The phase's serialization spine. Carries pruning coverage (`01`), the `expected_slugs` roster (`02`, `05`, `06`, `07`, `08`), per-agent tool expectations replacing the blanket `assertNotIn("execute", ...)` at `:118`, and the `05d-security-rollup` conditional that feature `07` must **delete rather than re-key** (the new `05d` is a consistency auditor). |
| `tests/test_readiness_synthesis_agents.py` | `02`, `03`, `07`, `08` | `02` deletes its three `05i-learnings-harvester` tests and narrows a fourth; `03` retargets the skill-name assertions; `07` rewrites the rest for `05g`. Note `:16`'s `"never read\ncode"` is coupled to exact line-wrap position and breaks on any rewrap. |

### Manual QA Checklist

Behavioral properties that no assertion over a Markdown body can establish. The
recorded contract: *a fixture dry-run is required release evidence; a run whose
required evaluators are recorded `not-run` is below-GO evidence, not a passing run.*

- [ ] **End-to-end dry run** (`08` AC1): all seven reports plus the `04e` security
      report land under one `dev/pr-review/<sha>-<timestamp>/` directory
- [ ] **Single-interaction contract holds end to end** (`08` AC2): one question
      block, then a written report, no further prompt. The requirement most likely
      to erode silently, one reasonable question at a time
- [ ] **Forced-failure run** (`08` AC3): run completes, `Checks Not Run` names the
      missing check and reason, verdict is not `GO`
- [ ] **Every subagent return ≤10 lines** (`08` AC4)
- [ ] **Codex delegation actually happens** (`06` AC5b): `max_depth` defaults to
      **1** and a blocked spawn causes a **silent inline fallback**. `05f`→`Test -
      Analyst` and `05b`→per-directory readers both sit at **depth 2**. The agent
      body will correctly say "delegate" while the runtime does not — verify from
      the transcript, not the prompt text
- [ ] **PR-comment consent** (`07`): with *ask when ready*, the report exists on
      disk **before** the prompt; with *never*, no network call is made
- [ ] **In a scratch consumer repo, never this one:** `origin/HEAD` unset; base
      correction propagates to evaluators; no PR open; `gh` unauthenticated
- [ ] **Graph MCP unavailable** (`05`): `05c`/`05d` report not-run with a reason
      rather than silently degrading to a grep
- [ ] **All three harnesses load the propagated family** without error

### Test Baseline

**416 passed, 15 subtests — captured 2026-07-16 across 4 consecutive full runs, all
green.** Runner: `.venv/bin/python -m pytest tests/ -q` (the system `python3` has no
pytest).

Two cautions:

- **PERF-01 is probabilistic and did not fire in 4 runs.** It is a propagated-guard
  latency gate owned by Phase 04. This repo has already recorded a coin flip landing
  heads being mistaken for a clean baseline. Capture repeated runs before claiming a
  regression, and **never relax a fixed budget to make a gate pass** — that was done
  once (PR #22, 50→90 ms) and reverted.
- **Feature `02` is expected to reduce the count to 413 passed / 10 subtests** before
  new tests are added: three whole `05i` tests deleted, and five retired slugs leave
  the `expected_slugs` subtest tuple. A count that does not land there is a signal.
