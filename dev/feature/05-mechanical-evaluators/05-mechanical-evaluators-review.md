# Review Record: 05 Mechanical Evaluators

## Summary

The three cheap-tier sweeps were renumbered to `05c`/`05d`/`05e`, rescoped to the
branch diff, migrated to the `dev/pr-review/` root, and stripped of `execute`. The
propagation-enumeration gap is genuinely closed: the roster is derived from disk and
asserted against a per-agent tool map, expanding harness-output verification from
three agents to seven.

This review verified by **execution**, not reading:

- **Mutation sweep: 42 mutations, 42 correct, 0 inert.** I ran my own harness against
  an isolated repo copy rather than trusting the implementer's reported 31/31. Every
  guard bit when the thing it claims to check was broken. **This is the first feature
  in this phase with no inert guards** — features 02–04 each had them, and feature 04's
  reviewer found five beyond the two self-reported. The implementer's `_prose`
  whitespace-normalization fix (catching 9 guards passing on line-break position) is
  the reason, and it is a durable pattern.
- **Propagation fixed point:** propagator run twice; all counters zero on the repeat,
  tree clean. AC9 confirmed, not inferred.
- **Grant removal propagated end-to-end:** Claude output for `05e` grants
  `Skill, Read, Grep, Glob, Edit, Write` (no Bash); OpenCode `05e` permission block has
  no `bash: allow`. Control agent `05a` retains bash in both roots.
- **Suite:** `1 failed, 513 passed, 108 subtests`. The single failure is PERF-01, a
  pre-existing Phase 04 blocker that reproduces identically at the phase baseline. Not
  this feature's regression; not touched.

All four orchestrator-flagged adjudications resolve **in the implementer's favor**, and
each was checked against evidence rather than argument.

## Verdict

**Approved with Reservations**

The reservation is not a defect: AC5/AC6/AC7 are *behavioral* contracts pinned only
**statically**. The guards prove each body *says* the right thing and that the guards
bite; they do **not** prove the agents *attribute correctly at runtime*. Confirming that
requires an agent-harness dry run against the pinned fixture, which no test-suite pass
can substitute for. The implementer declared this gap explicitly and correctly.

## Traceability

| AC | Status | Code Location | Notes |
|----|--------|---------------|-------|
| AC1 | **Met** (verified) | `05c/05d/05e-*.agent.md`; `.github/agents/README.md` | Renames complete. No retired identifier survives outside historical docs/tests. Mutation-verified both directions. |
| AC2 | **Met** (verified) | 3 agent bodies | `<merge-base>..HEAD` in all three; zero `phase`/`subphase`/`dev/phase-final-review` occurrences confirmed by grep. |
| AC3 | **Met** (verified) | 3 frontmatter; `test_propagate_master_assets.py` | `execute` dropped from all three. Justified — see Adjudication 1. Widening mutation-killed on `05c` and `05e`. |
| AC4 | **Met** (verified, deviating) | `05e-dependency-auditor.agent.md:25-39` | Offline **mode** survives intact and is *strengthened*; the **grant** is gone. See Adjudication 1. |
| AC5 | **Unverified — requires agent-harness dry run** | 3 agent bodies | Bodies name `<slug>-report.md`, defer the root to the conventions skill, and bound the return to 10 lines. Static text confirmed; *actual* report emission and line count not observed. |
| AC6 | **Unverified — requires agent-harness dry run** | 3 agent bodies | Attribution requirement, touched-file rejection, and `Checks Not Run` disposal all present and mutation-verified. Whether the agent *actually* attributes to added lines at runtime is unobserved. This is the highest-consequence unverified AC. |
| AC7 | **Unverified — requires agent-harness dry run** | 3 agent bodies | Tier-authoritative and "never convert a missing check into a pass" present and mutation-verified. Runtime adherence unobserved. |
| AC8 | **Met** (verified) | `test_propagate_master_assets.py:15-64` | Roster derived from disk. Omitting `05c`, omitting `05a`, adding a phantom key, and adding a new on-disk agent without an expectation **all fail**. Verified by mutation. |
| AC8b | **Met** (verified) | `PR_REVIEW_EVALUATOR_TOOLS["05a-baseline-worktree"]` | `execute` is **visible with an explicit list**, not hidden by omission. Trips in both directions — see Adjudication 4. |
| AC8c | **Met** (verified) | same | Stripping `edit` from `05d` fails. Mutation-verified. |
| AC9 | **Met** (verified) | generated roots | No OpenCode/Claude/Codex orphans. `z-*` stems survived the renumber as the plan predicted. Fixed point proven by repeat propagator run. |

## Adjudications

### 1. Dropping `execute` from `05e` (reverses the plan's AC4 expectation) — **CORRECT**

The implementer's reading governs, and the evidence is decisive on three independent
grounds:

**AC4's text never mandated retention.** It reads "*If* `execute` is retained anywhere
in this feature, this is the most likely place, and it needs the AC3 justification."
That is conditional. AC3 is unconditional and governing: the justification "must name a
command with no non-shell equivalent, **or the grant goes**."

**No command could be named — verified in-environment.** `pip-audit`, `osv-scanner`,
`safety`, `trivy`, `grype`, `snyk`: all absent from PATH and from `.venv`. `npm` exists,
but **the repo has no `package.json` at all**, so `npm audit` was never a candidate —
`npm audit --offline` fails with `ENOLOCK`. The implementer's claim understated their own
case.

**The non-shell equivalent is architecturally provided.** This is the decisive point and
it is stronger than the implementer argued. `05b-change-narrator` — the evaluator whose
*entire job is the diff* — has always run on `[agent, read, search, edit]` with **no
`execute`**, obtaining everything by reading the worktree `05a` creates:
"Use that baseline worktree for every baseline-to-HEAD comparison; do not create,
switch, or remove a worktree yourself." The house architecture is: **`05a` holds the one
unclosable `execute` (`git worktree`) and returns a path; every other evaluator reads two
trees.** Dropping `execute` from `05c`/`05d`/`05e` does not weaken them — it *aligns*
them with a pattern already proven in production by `05b`.

**AC4's offline mode survives intact and is strengthened.** Converting offline from a
policy the agent is trusted to observe into a capability boundary it cannot violate is
strictly stronger. Frontmatter and body were changed together (`05e:27` now declares
"This audit holds no shell grant"), so the two agree — the failure mode of a body
promising a capability its frontmatter withholds is closed and guarded.

Retaining the grant would have been the exact anti-pattern
`cross-phase-decisions.md:86` prohibits: a broad grant with a comment explaining why it
is fine.

### 2. `05d`'s new code-review-graph dependency — **JUSTIFIED**

Verified against the baseline: pre-rename `05j` referenced the graph **zero** times. The
plan's assertion that `05c`/`05d` both build on the graph was **factually wrong**
(`05g` did, with `refactor_tool`; `05j` did not). The implementer reported the plan's
error rather than fabricating an integration to match it — the correct response.

The rescope *forced* the addition: `05j` derived canonical forms by comparing subphases
against each other, and with subphases gone the canonical form must come from the
repository's established patterns. Locating prior art is exactly what
`semantic_search_nodes`/`query_graph` are for, and this repo's `CLAUDE.md` mandates the
graph over grep for precisely that. Declining `get_impact_radius` is correct: it answers
blast-radius questions, not convention drift — using it to satisfy the plan's letter
would have been cargo-cult.

The added failure mode is handled gracefully: graph-down is NOT RUN with a verdict-ceiling
drop, but drift evidenced directly from the diff is *still reported* with its
recommendation marked not-derived. The agent degrades partially rather than going dark.
MCP tools are never declared in frontmatter anywhere in this repo, so the `execute` removal
does not jeopardize the graph dependency.

### 3. Guards are not inert — **VERIFIED BY EXECUTION (42/42)**

I did not trust the reported 31/31. I built an independent harness against an isolated
repo copy and ran 42 mutations, including cases the implementer did not:

- Widening `execute` onto `05c` **and** `05e` → both fail.
- Narrowing: `edit` stripped from `05d` → fails.
- **`05a`'s `execute` removed** → fails. **`execute` added to `05b`** → fails.
- Roster: omit `05c`; omit `05a`; add a phantom key; add a real new on-disk agent with no
  expectation → **all four fail**.
- Every one of the 21 body contracts, each broken at its own anchor.
- OpenCode orphan resurrection; new-slug deletion; feature-04 ledger regression.

**0 inert, 0 survived.** Two initial "failures" were my own anchor errors (I guessed
line-break positions wrong), not guard defects — corrected and both killed. Notably I also
ran the **counter-check**: inserting a `05g-readiness-synthesizer` reference does **not**
trip the retired-identifier ban, confirming the implementer's claim that the guard bans
retired *identifiers* rather than the bare `05g` substring. Feature 07 will not be
misfired on.

### 4. AC8b — `05a`'s grant is genuinely visible, not hidden — **CONFIRMED**

`PR_REVIEW_EVALUATOR_TOOLS["05a-baseline-worktree"] = ["read", "search", "execute"]` with
the justification recorded inline. The roster trips in **both** directions under mutation:
removing `05a`'s `execute` fails, and adding `execute` to an agent that shouldn't have it
fails. It is declared, not dodged. `05a` was otherwise untouched, per plan scope.

A structural win worth naming: `expected_slugs` is now
`tuple(sorted(PR_REVIEW_EVALUATOR_TOOLS))`, so
`test_phase_review_agents_match_all_generated_harness_outputs` iterates **seven** agents
instead of three. Harness-output verification more than doubled as a side effect of
closing the gap. That is the 17 → 108 subtest jump.

## Issues Found

| # | Issue | Severity | File:Line | AC | Status |
|---|-------|----------|-----------|-----|--------|
| 1 | Runtime behavior unverified: AC5/AC6/AC7 pinned statically only | Medium (inherent) | 3 agent bodies | AC5/6/7 | Open — needs QA dry run |
| 2 | `assertIn("authoritative", ...)` is a substring guard; a body reading "is *not* authoritative" would pass | Low | `test_mechanical_evaluators.py:159` | AC7 | Open |
| 3 | `assertIn("added-line attribution", ...)` likewise passes on "…is optional" | Low | `test_mechanical_evaluators.py:127` | AC6 | Open |
| 4 | `test_the_audit_declares_no_shell_grant` keys on the literal phrase "audit command" — phrasing-specific proxy | Low | `test_mechanical_evaluators.py:210` | AC4 | Open |
| 5 | Tool-grant assertion is order-sensitive list equality; a semantically neutral reorder fails | Low | `test_propagate_master_assets.py:169` | AC8 | Open |
| 6 | `GRAPH_DEPENDENT_EVALUATORS` is a hardcoded tuple; if `05e` later gains a graph dep, its NOT-RUN contract goes unenforced | Low | `test_mechanical_evaluators.py:34` | AC7 | Open |

**On #2–#4 (deliberately not fixed):** each weak substring guard is covered in practice
by a *complementary* regex guard that is mutation-verified — #2 by
`test_no_body_converts_a_missing_check_into_a_pass`, #3 by
`test_each_body_explicitly_rejects_touched_file_filtering`, #4 by the frontmatter
grant assertion in `test_propagate_master_assets.py`. The realistic failure mode is
caught. Churning mutation-verified tests to harden a theoretical rewording attack would
trade proven guards for unproven ones — a bad trade.

**On #5:** errs safe. It fails loudly and opens no hole; strictness is arguably the point
("a grant change is a deliberate edit").

## Fixes Applied

**None.** No Blocker, High, or actionable Medium issue was found. Issue #1 is inherent to
prompt-based agents and cannot be closed by an edit — it requires a QA harness run. Issues
#2–#6 are Low and, per the rationale above, are better left documented than churned.

I made no edits to source, tests, or generated outputs. The tree is exactly as the
implementer left it, and the propagator confirms it is at a fixed point.

## Remaining Concerns

- **Issue #1 — the real one.** AC6 is the AC most likely to be quietly wrong at runtime
  (the plan says so itself), and it is verified only as text. A sweep that reports
  pre-existing findings as branch-introduced *looks exactly like a working sweep*. Static
  assertions confirm the body forbids this; nothing yet confirms the agent obeys. **QA
  should dry-run all three against the pinned fixture (`f5ab960..e6ff28a`) and confirm
  added-line attribution plus graph-unavailable degradation.**
- **Issues #2–#6:** Low. Defer to a cleanup pass.
- **Declared, correctly out of scope:** the orchestrator's roster still names `05f`/`05g`,
  which resolve only after features 06/07; `cross-phase-decisions.md` still describes these
  grants as open (a historical ledger, the harvester's job); `.github/agents/README.md`
  still omits `05a`. The implementer's observation that the four agents missing from the
  README were *precisely* the four missing from `expected_slugs` — the same four `execute`
  holders — is a sharp catch and worth feature 08's attention.

## Test Coverage Assessment

- **Covered (verified):** AC1, AC2, AC3, AC4, AC8, AC8b, AC8c, AC9 — all mutation-verified.
- **Covered as text only:** AC5, AC6, AC7 — contracts pinned and guards proven to bite,
  runtime behavior unobserved.
- **Missing:** no runtime/integration test for any of the three agents (inherent — they are
  prompts). No test asserts the orchestrator's dispatch roster resolves to agents that
  exist on disk; that gap is real and belongs to feature 08.

## Risk Summary

- **`tests/test_mechanical_evaluators.py` asserts on prose via regex.** Mutation-proven to
  bite *today*, but inherently brittle to rewording. The `_prose` whitespace normalization
  removes the worst failure mode (reflow silently dropping an assertion). The mutation
  harness is the only evidence these keep biting — re-run it if the bodies are reworded.
- **AC6 correctness is unobserved at runtime** — the highest-consequence residual risk in
  this feature.
- **`05d` now carries an availability dependency it did not have.** Justified and gracefully
  degraded, but it is the one place this feature added capability rather than removing it.
- **Shared surface with feature 06:** `PR_REVIEW_EVALUATOR_TOOLS` is a dict keyed by source
  slug and is extensible by design; the derived roster check will force feature 06 to rename
  the key when it renames `05h`→`05f`. Intended, and left extensible as required.
- **PERF-01 remains red** — pre-existing, reproduces identically at phase baseline
  (54.5 ms vs 54.3 ms at HEAD), owned by Phase 04. Untouched by this feature.
</content>
