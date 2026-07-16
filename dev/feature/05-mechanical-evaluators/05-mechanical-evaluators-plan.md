# 05 Mechanical Evaluators

## Execution Metadata

- **Wave:** 5
- **Parallel safe:** no
- **Depends on:** 02-retired-evaluator-removal, 03-pr-review-conventions-skills, 04-pr-review-orchestrator
- **Key files modified:** `.github/agents/05c-artifact-sweeper.agent.md` (renamed from `05g-artifact-sweeper.agent.md`), `.github/agents/05d-consistency-auditor.agent.md` (renamed from `05j-consistency-auditor.agent.md`), `.github/agents/05e-dependency-auditor.agent.md` (renamed from `05k-dependency-auditor.agent.md`), `tests/test_propagate_master_assets.py`, generated `claude/agents/`, `opencode/agents/`, `codex/agents/`
- **Sequential reason:** shares `tests/test_propagate_master_assets.py` with `06-narrative-and-test-health` in the same wave, and with upstream features

## A. Requirements & Traceability

The three cheap-tier mechanical sweeps renumber and rescope from whole-phase to
branch-diff. They share a shape — config-driven, read-only, cheap tier, mechanical
— which is why the Phase document groups them and why they are one feature.

| Old slug | New slug | Holds `execute` today |
|---|---|---|
| `05g-artifact-sweeper` | `05c-artifact-sweeper` | yes |
| `05j-consistency-auditor` | `05d-consistency-auditor` | yes |
| `05k-dependency-auditor` | `05e-dependency-auditor` | yes |

**All three hold `execute` today, and all three are the agents
`tests/test_propagate_master_assets.py:87` deliberately omits from its
`expected_slugs` tuple for exactly that reason** — the tuple asserts
`assertNotIn("execute", agent.tools)` and these three would fail it. That omission
is a documented propagation-enumeration gap, and it is closable only once the
roster is settled at seven contiguous slugs.

### Acceptance Criteria

- **AC1** — The three agents are renamed to `05c-artifact-sweeper`,
  `05d-consistency-auditor`, `05e-dependency-auditor`, with `name:` frontmatter
  and body self-references updated to match.
- **AC2** — Each is rescoped from "the current phase diff" / "across the assigned
  phase subphases" to **the branch diff `<merge-base>..HEAD`**, receiving the
  confirmed base from the orchestrator. No subphase concepts remain.
- **AC3** — **`execute` is dropped where it is not genuinely required.** Per-agent
  command scoping is not expressible on Claude (recorded in
  `cross-phase-decisions.md`), so the only narrowing available is removal. For each
  agent, either drop `execute` and use `read`/`search` plus the code-review-graph
  MCP tools, or retain it with a recorded justification naming the specific command
  that has no non-shell equivalent. "It might be handy" is not a justification.
- **AC4** — `05e-dependency-auditor` retains an **explicitly offline** read-only
  audit mode. The recorded contract is that network-capable dependency commands are
  treated as unavailable, and its `execute` grant "is not a simple removal — its
  contract permits an offline read-only audit command." If `execute` is retained
  anywhere in this feature, this is the most likely place, and it needs the AC3
  justification.
- **AC5** — Each writes its report to
  `dev/pr-review/<base-sha-short>-<timestamp>/<slug>-report.md` per feature `03`'s
  contract, and returns ≤10 lines.
- **AC6** — Diff-scoped attribution: any evaluator calling repo-wide analysis must
  require **verifiable added-line attribution**; touched-file filtering alone is
  insufficient. This is a recorded review contract and it is exactly where a
  mechanical sweep goes wrong — a file touched by the branch is not the same as a
  line added by the branch.
- **AC7** — Cheap-tier assignment is authoritative; a tier limitation is recorded
  as an execution condition, never as evidence that a check passed.
- **AC8** — `tests/test_propagate_master_assets.py`'s `expected_slugs` tuple is
  re-derived over the settled seven-agent roster. Where an agent legitimately
  retains `execute` per AC3, the blanket `assertNotIn("execute", agent.tools)`
  assertion (`:118`) must be replaced with a **per-agent expected tool list** —
  **not** deleted, and **not** worked around by removing the agent from the tuple,
  which is exactly how the current gap arose.
- **AC8b** — **`05a-baseline-worktree` enters the roster and keeps `execute`.**
  The plan's premise that three agents are omitted from `expected_slugs` for the
  `execute` reason is wrong: **four** are. `05a` holds `tools: [read, search,
  execute]` and is also absent from the tuple. Re-deriving over the settled seven
  necessarily forces `05a` in, and its grant is recorded as **unclosable** —
  `git worktree` has no non-shell equivalent (`cross-phase-decisions.md:16`). So
  `05a`'s entry must carry an explicit expected-tools list including `execute`,
  with the recorded justification attached. This is the honest outcome: the
  enumeration gap closes, and the grant is *declared* rather than hidden by
  omission. `05a` is otherwise out of scope for this feature — no rescope, no
  rename.
- **AC8c** — **`edit` is expected on all three agents and must not be stripped.**
  All three declare it and genuinely need it: they write their own report files.
  Their bodies say "read-only, never remediate," which reads as license to remove
  `edit` — doing so breaks AC5. Pin `edit` in the per-agent expected tool lists so
  a well-meaning removal fails a test.
- **AC9** — All three propagate to all three roots, and their old-slug OpenCode
  files are absent (feature `01` pruning). Claude files are keyed on agent *name*
  and may survive the renumber under the same stem; OpenCode files are keyed on
  *slug* and will orphan.

### Non-Goals

- Adding an allowlist syntax to the propagator — deleted from this phase.
- Changing `04e-diff-security-scan` or `test-analyst`.
- Rewriting the code-review-graph MCP integration.
- Rescoping `05b`/`05f` (feature `06`) or `05g` (feature `07`).

### Traceability

| Acceptance Criteria | Code Areas/Modules | Test / Evidence Category |
|---|---|---|
| AC1, AC9 | three agent files; generated roots | Must-have automated test (new) |
| AC2, AC6, AC7 | agent bodies | Must-have automated test (new) — contract assertions |
| AC3, AC4 | agent frontmatter `tools:` | Must-have automated test (update) — per-agent tool expectations |
| AC5 | agent bodies | Must-have automated test (new) |
| AC8 | `tests/test_propagate_master_assets.py:87` | Existing test to update |

## B. Correctness & Edge Cases

**AC6 is where these agents are most likely to be quietly wrong.** "Find debug
statements introduced since the base" is not "find debug statements in files the
branch touched." A branch that adds one line to a 900-line file did not introduce
the 12 pre-existing `TODO`s in it. Reporting them is noise that trains the reader
to ignore the report — the exact friction failure recorded elsewhere in this
project as "rules matching ordinary text are defects, not safety."

**The graph MCP server is an availability dependency.** `05c` and `05d` build on
code-review-graph (`refactor_tool` dead-code detection, `get_impact_radius`). When
it is unavailable, they report not-run with a stated reason and the verdict ceiling
drops below GO. They must not silently degrade to a grep and report as if the graph
answered.

### Failure modes

| Mode | Handling |
|---|---|
| Pre-existing findings attributed to the branch | AC6 — verifiable added-line attribution required |
| Graph MCP unavailable | Report not-run with reason; verdict ceiling drops; never silently degrade |
| Dependency audit reaches the network | AC4 — offline mode; network-capable commands are unavailable |
| Cheap tier can't complete the sweep | AC7 — execution condition, not a pass |
| Empty diff (base wrongly suggested as self) | Prevented upstream by `04`'s AC4; if the diff is empty, say so rather than reporting "no findings" |
| OpenCode orphan left behind by renumber | AC9 + feature `01` |

## C. Consistency & Architecture Fit

All three already follow the house pattern: load the conventions skill, take the
orchestrator's tier assignment as authoritative, report-only, never remediate.
Preserve that. The rescope is the input (branch diff instead of phase subphases)
and the report path.

Concrete names copied exactly from the Phase document: `05c-artifact-sweeper`,
`05d-consistency-auditor`, `05e-dependency-auditor`.

## D. Clean Design & Maintainability

These three are the cheapest agents in the family and should stay that way. The
temptation is to let a mechanical sweep grow judgment — "this TODO looks
important." That is `05b`'s job. A mechanical sweep reports what it matched, with
attribution, and stops.

**Duplication risk**: three agents with near-identical preamble. That is already
the case and is acceptable — they are separate prompts, not shared code. Keep the
shared parts in `pr-review-conventions`.

### Keep-it-clean checklist

- [ ] No subphase language anywhere in the three bodies
- [ ] `execute` present only with a named, command-specific justification
- [ ] Added-line attribution required, not touched-file filtering
- [ ] Cheap tier preserved; no upgrade to deep judgment
- [ ] Report paths from the conventions skill, not restated

## E. Completeness: Observability, Security, Operability

**Observability decision** — None beyond the report file and the ≤10-line return.
These agents produce findings; the findings *are* the observability.

**Security** — AC3 is the only real security content, and it is deliberately
modest. The phase's original plan was to scope these agents' shell access to
specific commands; that is not expressible on Claude, so the honest remaining move
is to remove `execute` where it isn't needed and justify it where it is. Retaining
`execute` with a comment explaining why it is fine is precisely the pattern the
recorded rule prohibits — the justification must name a command with no non-shell
equivalent, or the grant goes.

**Runbook** — Verify: dry run against the pinned fixture produces three findings
reports with added-line attribution. Rollback: `git revert`.

## F. Test Plan

**Existing tests to update**
- `tests/test_propagate_master_assets.py:87` — `expected_slugs` re-derived; the
  blanket `assertNotIn("execute", ...)` replaced with per-agent expectations (AC8).

**Must-have automated tests (new)**

Top-value cases:

1. **Roster completeness (AC8).** Given the settled seven agents, then
   `expected_slugs` names all seven — no agent may be omitted from propagation
   enumeration to dodge an assertion. This test closes the recorded enumeration gap
   and must be written so that omitting an agent fails.
2. **Per-agent tool expectation (AC3/AC4).** Given each of the three, then its
   `tools:` matches an explicit expected list. A change to a grant becomes a
   deliberate test edit rather than a silent widening.
3. **Added-line attribution declared (AC6).** Assert each body requires verifiable
   added-line attribution and does not accept touched-file filtering.
4. **No subphase concepts (AC2).** Assert no body mentions subphases or a
   `PHASE_0N` report root.
5. **Old OpenCode slugs pruned (AC9).** Assert the **exact stems**
   `opencode/agents/05g-artifact-sweeper.md`, `05j-consistency-auditor.md`, and
   `05k-dependency-auditor.md` are absent after propagation. **Do not use a
   `05g-*` glob**: feature `07` creates `opencode/agents/05g-readiness-synthesizer.md`,
   so a glob assertion passes in wave 5 and breaks in wave 6. Exact stems only.

**Manual QA** — dry run against the pinned fixture; confirm graph-unavailable
degradation reports not-run rather than a clean result.

## Unverified Assumptions

- That `05c`/`05d` can do useful work **without** `execute`, using
  `read`/`search` plus code-review-graph MCP tools. Plausible — their work is
  pattern-matching and graph queries — but not verified against their current
  bodies' actual command use. If a specific command proves necessary, AC3's
  justification path applies. Narrow and resolvable during Stage 2.
- That Claude output filenames survive the renumber under the existing `z-*` stem
  (`_claude_filename_for` prefers an existing stem, and `z-artifact-sweeper` etc.
  already exist). Verify all three roots after propagation.

## Relationship to Sibling Plans

- **Depends on `03`** (report contract) and **`04`** (the orchestrator that supplies
  the confirmed base and the roster naming these slugs).
- **Same wave as `06-narrative-and-test-health`, sequential with it** — both edit
  `tests/test_propagate_master_assets.py`'s roster assertions.
- **`07-synthesis-and-pr-posting`** consumes these agents' reports through the
  `pr-review-report` templates only, never their internals.

## Stage 0: Test Prerequisites

**Goal**: Not required. Baseline 416 passed across 4 consecutive full runs
(2026-07-16).
**Success Criteria**: n/a
**Status**: Not required

## Stage 1: Rename and Renumber

**Goal**: `git mv` all three; update `name:` and body self-references; propagate;
confirm OpenCode orphans are pruned.
**Success Criteria**: AC1, AC9.
**Status**: Not Started

## Stage 2: Audit the Grants

**Goal**: For each agent, determine whether `execute` is genuinely required. Drop
it where not; justify it by named command where so. Update per-agent tool
expectations in the test.
**Success Criteria**: AC3, AC4; each retained grant has a recorded justification.
**Status**: Not Started

## Stage 3: Rescope to the Branch Diff

**Goal**: Replace phase/subphase inputs with `<merge-base>..HEAD`; require
added-line attribution; retarget report paths.
**Success Criteria**: AC2, AC5, AC6, AC7.
**Status**: Not Started

## Stage 4: Close the Enumeration Gap

**Goal**: Re-derive `expected_slugs` over the settled roster so that no agent can
be omitted; dry-run all three against the pinned fixture.
**Success Criteria**: AC8; suite green; three reports produced.
**Status**: Not Started
