# 06 Narrative and Test Health

## Execution Metadata

- **Wave:** 5
- **Parallel safe:** no
- **Depends on:** 02-retired-evaluator-removal, 03-pr-review-conventions-skills, 04-pr-review-orchestrator
- **Key files modified:** `.github/agents/05b-change-narrator.agent.md`, `.github/agents/05f-test-health.agent.md` (renamed from `05h-test-health.agent.md`), `tests/test_propagate_master_assets.py`, generated `claude/agents/`, `opencode/agents/`, `codex/agents/`
- **Sequential reason:** shares `tests/test_propagate_master_assets.py` with `05-mechanical-evaluators` in the same wave, and with upstream features

## A. Requirements & Traceability

The two evaluators the Phase document says "differ enough to warrant individual
design." `05b` is the family's deep-judgment agent; `05f` is a delegating adapter.
They are one feature because neither is large alone and both are simple renames
plus an input rescope.

| Old slug | New slug | Kind |
|---|---|---|
| `05b-change-narrator` | `05b-change-narrator` (unchanged) | deep judgment, top tier |
| `05h-test-health` | `05f-test-health` | delegating adapter → `test-analyst` |

Neither holds `execute` today (`05b`: `[agent, read, search, edit]`; `05h`:
`[agent, read, search, edit]`), so the grant question that dominates feature `05`
does not arise here.

### Acceptance Criteria

- **AC1** — `05h-test-health.agent.md` is renamed to `05f-test-health.agent.md`,
  with `name:` and body self-references updated. `05b-change-narrator` keeps its
  slug and needs no rename.
- **AC2** — `05b` is rescoped from a **whole-phase, subphase-attributed** narrative
  to a **branch-diff narrative** over `<merge-base>..HEAD`. Subphase attribution is
  deleted outright — a PR has no subphases. Churn hotspots survive; they were never
  a phase concept.
- **AC3** — `05b` produces an account of **what the branch is trying to do**, not
  merely what it changed. This is the agent that gives the readiness report its
  narrative spine and is the reason it holds the top model tier.
- **AC4** — `05b` chunks diffs internally and may spawn per-directory readers. A
  long-lived branch can produce a diff the size of a whole phase; this agent is the
  one most exposed to it, and the ≤10-line return with full detail on disk is a hard
  requirement, not a style note.
- **AC1b** — `05h`'s **`description:` frontmatter** is rescoped alongside its body.
  `05b-change-narrator`'s description reads "with subphase attribution" — a body-only
  rescope leaves the deleted concept shipping in frontmatter, and a body-scoped test
  passes while it does. Both agents' descriptions are in scope.
- **AC5** — `05f` **demonstrably delegates** to the existing `test-analyst` agent
  rather than reimplementing coverage analysis, and adapts the result into a
  branch-scoped report. The delegation is an explicit acceptance criterion because
  a delegating adapter is the easiest kind of agent to quietly turn into a
  reimplementation.
- **AC5b** — **The Codex `max_depth` fallback is named and handled.**
  `.github/learnings/debugging-learnings.md:25–38` records that Codex `max_depth`
  defaults to **1**, and that a blocked spawn causes a **silent inline fallback** —
  the agent does the work itself instead of delegating, and reports success.
  `05f`→`Test - Analyst` and `05b`→per-directory readers both sit at **depth 2**.
  This is the concrete mechanism behind AC5's "silent reimplementation," and AC5's
  static declaration assertion **cannot detect it** — the body will correctly say
  "delegate" while the runtime does not. Required: state the depth requirement in
  the agent, and verify delegation actually occurred at runtime during the dry run
  rather than inferring it from the prompt text.
- **AC6** — `05f` reports the **coverage delta base→HEAD**, test redundancy, and
  flake candidates. The delta framing is the rescope: `test-analyst` analyzes a
  suite; `05f` reports what the branch did to it.
- **AC7** — Both write reports to
  `dev/pr-review/<base-sha-short>-<timestamp>/<slug>-report.md` per feature `03`'s
  contract and return ≤10 lines.
- **AC8** — Both appear in `tests/test_propagate_master_assets.py`'s re-derived
  `expected_slugs` roster and propagate cleanly to all three roots, with the old
  `opencode/agents/05h-test-health.md` absent via feature `01`'s pruning.
- **AC9** — Neither agent acquires `execute`. They do not have it now and the
  rescope gives them no reason to; adding it would be a widening at exactly the
  moment the phase lost its ability to narrow.

### Non-Goals

- Modifying `test-analyst` itself.
- Adding a flake-detection implementation — `05f` reports candidates from
  `test-analyst`'s output; it does not run the suite repeatedly.
- Rescoping the mechanical sweeps (feature `05`) or synthesis (feature `07`).
- Producing a verdict. Both are evidence producers; `05g` decides.

### Traceability

| Acceptance Criteria | Code Areas/Modules | Test / Evidence Category |
|---|---|---|
| AC1, AC8 | two agent files; generated roots | Must-have automated test (new) |
| AC2, AC3, AC4 | `05b` body | Must-have automated test (new) — contract assertions; **manual QA** for narrative quality |
| AC5, AC6 | `05f` body; `agents:` frontmatter | Must-have automated test (new) — delegation declared |
| AC5b | `05f`/`05b` bodies; Codex runtime | **Manual QA only** — a static assertion provably cannot detect the inline fallback |
| AC7 | both bodies | Must-have automated test (new) |
| AC9 | both frontmatter `tools:` | **Existing test to update** — `tests/test_propagate_master_assets.py:118` already asserts `assertNotIn("execute", agent.tools)` per slug; this is a roster edit, not a new test |

## B. Correctness & Edge Cases

**`05b` is the context-blowout risk of the whole phase.** Every other evaluator is
mechanical, delegating, or report-only. This one reads the diff and forms a
judgment about it, and a six-month branch can hand it a diff larger than any single
context. AC4 is the mitigation and it must be structural — chunk, spawn readers,
write to disk, return ten lines — rather than a request to be concise.

**`05f`'s failure mode is silent reimplementation.** `test-analyst` exists and is
good at suite analysis. An adapter that "just does a quick coverage check itself"
produces a plausible report that diverges from the project's actual test analysis.
AC5 exists because this failure looks like success.

**Coverage delta needs a baseline checkout.** Comparing coverage at base vs HEAD
implies running or reading coverage at two revisions. `05a-baseline-worktree`
provides the base checkout; `05f` should consume it rather than checking out its
own. Whether `test-analyst` can be pointed at a worktree path is not verified —
see Unverified Assumptions.

### Failure modes

| Mode | Handling |
|---|---|
| Diff too large for context | AC4 — internal chunking, per-directory readers, disk-backed detail |
| `05f` reimplements coverage analysis | AC5 — delegation is an asserted contract |
| `test-analyst` unavailable | Report not-run with a stated reason; verdict ceiling drops below GO; never substitute a hand-rolled check |
| Coverage tooling absent in the target repo | Report the condition. This agent ships to consuming projects that may have no coverage tooling at all — absence is a stated limitation, not a failure |
| Empty diff | Say so; do not report "no narrative findings" |
| Narrative attributes pre-existing code to the branch | Same added-line attribution discipline as feature `05` |

## C. Consistency & Architecture Fit

`05f` follows the delegating-adapter pattern already established by `05h` today:
declare `agents: [Test - Analyst]`, delegate, adapt the result to the family's
report template. `05b` follows the deep-judgment pattern: top tier, internal
chunking, narrative output.

Concrete names copied exactly from the Phase document: `05b-change-narrator`,
`05f-test-health`, `test-analyst`. The `agents:` frontmatter value `Test - Analyst`
is the **verified existing display name** used by `05h-test-health.agent.md` today
— preserve it exactly; the propagator rewrites agent references by display name,
so a near-miss silently ships as literal prose.

## D. Clean Design & Maintainability

`05f` should stay thin. Its value is adaptation — turning suite analysis into a
branch-scoped delta — not analysis. If it grows past a page of instructions, that
is a signal it is absorbing `test-analyst`'s job.

`05b` is allowed to be the largest evaluator prompt in the family. It carries the
judgment.

### Keep-it-clean checklist

- [ ] No subphase attribution in `05b`
- [ ] `05f` delegates; no inline coverage logic
- [ ] `Test - Analyst` display name exact
- [ ] Neither agent gains `execute`
- [ ] Chunking is structural in `05b`, not advisory

## E. Completeness: Observability, Security, Operability

**Observability decision** — None beyond reports and ≤10-line returns. `05f`
should surface *which* coverage evidence it had (tool, revision pair) inside its
report, because a coverage delta without a named source is unreconcilable later —
the recorded lesson that any evidence artifact not naming its revision cannot be
reconciled against later work.

**Security** — AC9 is the whole of it: neither agent holds `execute` and neither
gains it. This is the one place in the phase where the security posture *improves*
by default rather than by argument, because the rescope needs no new capability.

**Runbook** — Verify: dry run against the pinned fixture yields a narrative report
and a test-health report. Rollback: `git revert`.

## F. Test Plan

**Existing tests to update**
- `tests/test_propagate_master_assets.py` — `expected_slugs` roster (shared with
  feature `05`; whichever lands second reconciles).

**Must-have automated tests (new)**

Top-value cases:

1. **Delegation declared (AC5).** Assert `05f`'s `agents:` frontmatter names
   `Test - Analyst` and its body delegates rather than describing inline coverage
   analysis.
2. **No subphase attribution in `05b` (AC2).** Assert the body contains no subphase
   concepts and frames the narrative as `<merge-base>..HEAD`.
3. **Return contract and chunking (AC4, AC7).** Assert both declare the ≤10-line
   return and that `05b` declares internal chunking with detail on disk.
4. **Per-agent tool expectation (AC9).** Assert neither `tools:` list contains
   `execute`. A widening becomes a deliberate test edit.
5. **Old OpenCode slug pruned (AC8).** Assert `opencode/agents/05h-test-health.md`
   is absent after propagation.

**Manual QA checks**
- Dry run against the pinned fixture: is the narrative actually about what the
  branch is *for* (AC3)? This is a judgment quality check that no assertion covers.
- Force `test-analyst` unavailable; confirm `05f` reports not-run rather than
  substituting its own analysis.
- **On Codex specifically (AC5b): confirm `05f` actually spawned `Test - Analyst`
  rather than silently falling back to inline work.** With `max_depth` at its
  default of 1, the depth-2 spawn is blocked and the fallback is silent, so the
  only evidence is runtime: check the transcript for the child invocation. A green
  static assertion here means nothing.

## Unverified Assumptions

- That `test-analyst` can be pointed at a specific revision or worktree path to
  produce the *base* side of the coverage delta. Its current contract is
  suite-analysis at the working tree. If it cannot, `05f` reports HEAD coverage
  plus a stated limitation rather than a delta — an honest degradation, and
  preferable to `05f` growing its own coverage runner. Resolve in Stage 2; narrow.
- That the consuming repository has coverage tooling at all. This repo does
  (`pytest`), but the family propagates to projects that may not.

## Relationship to Sibling Plans

- **Depends on `03`** (report contract) and **`04`** (confirmed base, roster).
- **Same wave as `05-mechanical-evaluators`, sequential with it** — both edit the
  `expected_slugs` roster in `tests/test_propagate_master_assets.py`.
- **Consumes `05a-baseline-worktree`** for the base-side checkout (AC6). `05a`
  itself is unchanged by this phase beyond feature `03`'s prose touch.
- **Feeds `07-synthesis-and-pr-posting`** through report files only.

## Stage 0: Test Prerequisites

**Goal**: Not required. Baseline 416 passed across 4 consecutive full runs
(2026-07-16).
**Success Criteria**: n/a
**Status**: Not required

## Stage 1: Rename `05h` → `05f`

**Goal**: `git mv`; update `name:` and self-references; propagate; confirm the
OpenCode orphan is pruned.
**Success Criteria**: AC1, AC8.
**Status**: Not Started

## Stage 2: Rescope Test Health to a Delta

**Goal**: Reframe `05f` around coverage delta base→HEAD; confirm how `test-analyst`
can produce the base side, and degrade honestly if it cannot.
**Success Criteria**: AC5, AC6; the delegation assertion passes; the baseline
question is resolved and recorded.
**Status**: Not Started

## Stage 3: Rescope the Narrator

**Goal**: Delete subphase attribution; reframe to `<merge-base>..HEAD`; add the
"what is this branch trying to do" account; make chunking structural.
**Success Criteria**: AC2, AC3, AC4, AC7.
**Status**: Not Started

## Stage 4: Dry-Run and Reconcile the Roster

**Goal**: Dry-run both against the pinned fixture; reconcile `expected_slugs` with
feature `05`.
**Success Criteria**: AC8, AC9; two reports produced; suite green.
**Status**: Not Started
