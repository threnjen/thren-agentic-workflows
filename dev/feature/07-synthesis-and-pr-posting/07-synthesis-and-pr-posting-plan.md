# 07 Synthesis and PR Posting

## Execution Metadata

- **Wave:** 6
- **Parallel safe:** no
- **Depends on:** 04-pr-review-orchestrator, 05-mechanical-evaluators, 06-narrative-and-test-health
- **Key files modified:** `.github/agents/05g-readiness-synthesizer.agent.md` (renamed from `05l-readiness-synthesizer.agent.md`), `.github/agents/05-pr-review.agent.md` (posting path), `tests/test_readiness_synthesis_agents.py`, `tests/test_propagate_master_assets.py`, generated `claude/agents/`, `claude/commands/`, `opencode/agents/`, `codex/agents/`
- **Sequential reason:** shares `.github/agents/05-pr-review.agent.md` with upstream `04-pr-review-orchestrator`, and `tests/test_propagate_master_assets.py` with upstream features

## A. Requirements & Traceability

Deliverable 6 in the Phase document, kept whole: the synthesizer and the posting
path ship together because posting has nothing to post until synthesis produces a
report, and the consent model chosen upfront in feature `04` is meaningless until
something acts on it.

### Acceptance Criteria

- **AC1** — `05l-readiness-synthesizer.agent.md` is renamed to
  `05g-readiness-synthesizer.agent.md`, with `name:` and self-references updated.
- **AC2** — `05g` reads **only report files**, never code and never other agents'
  internals. Its inputs are pinned to the `pr-review-report` templates from feature
  `03`.
- **AC3** — It produces a severity-ordered readiness report at
  `dev/pr-review/<base-sha-short>-<timestamp>/readiness-report.md` carrying `GO`,
  `GO WITH CONDITIONS`, or `NO-GO` with a blocking list.
- **AC4** — **A `Checks Not Run` section names every missing, unreadable, not-run,
  or failed check by evaluator, check, and concrete reason.** The verdict can never
  be `GO` while any check is missing; the ceiling is "no blockers found, coverage
  incomplete."
- **AC5** — **The agent writes no status line** in `PROJECT_ROADMAP.md` or any
  phase summary, on any path. The report file is the verdict; it is advisory.
- **AC6** — **P5-SEC-02 is closed here or explicitly recorded as still open.** The
  recorded finding: the readiness path consumes report *claims* after metadata-only
  validation, and it was unclosable because the path was agent Markdown with no code
  to attach a schema and deterministic reducer to. The recorded expectation is that
  **the rescope rebuilds that path, so the validator arrives with the rebuild.**
  If this feature does not add a strict schema and a deterministic status reducer
  over structured records, P5-SEC-02 remains open and must be recorded as such —
  tightening the prose does not close it, and the Phase 03 scan already faulted
  exactly that move.
- **AC7** — **PR posting is opt-in and honors the choice captured upfront** in
  feature `04`: *post automatically*, *ask once the report is written*, or *never*.
  With *never*, **no network call is made**. With *ask when ready*, the report
  exists on disk **before** the prompt appears.
- **AC8** — **No pull request open is not an error.** Report the condition and
  leave the local report as the deliverable. Same for `gh` absent or
  unauthenticated: reported alongside the local report, never a run failure.
- **AC9** — **Output to the PR is one-way.** The agent never reads PR comments or
  any other network-sourced text back in. Ingesting PR discussion is a
  prompt-injection surface and is out of scope for this phase.
- **AC10** — The posting path introduces **no new prompt** beyond the upfront block,
  with the single designed exception of the *ask when ready* confirmation — which
  blocks nothing, because the work is already on disk.
- **AC11** — `tests/test_readiness_synthesis_agents.py` is rewritten: its three
  `05i-learnings-harvester` tests are already gone (feature `02`); its remaining
  assertions retarget `05g`, the renamed skills, and the new report root. The
  literal-string assertions ``never use `execute` `` at lines 63 and 90 belong to
  the deleted `05i` tests and go with them. **Two further items the rewrite must
  cover:**
  - `:16`'s assertion `"never read\ncode" in body.lower()` is coupled to the exact
    **line-wrap position** in the agent body — it breaks on any rewrap, and the
    rescope rewraps. Reassert the contract without depending on where the line
    happens to break.
  - `:31`'s `"canonical hand-off report"` and the body's `master-qa.md`,
    `security-rollup.md`, and `ac-regression-matrix.md` all name **retired
    evaluators' outputs** and must leave with them.
- **AC11b** — In `tests/test_propagate_master_assets.py`, the `05d-security-rollup`
  conditional must be **deleted, not re-keyed**. Under the new roster `05d` is
  `05d-consistency-auditor`; re-pointing the conditional at the new `05d` would
  silently assert a security-rollup contract against a consistency auditor and pass
  for the wrong reason.
- **AC11c** — `05l`'s body contains a **live counterexample to AC5**: it states that
  "the orchestrator owns verdict write-back and the learnings agent owns draft
  proposals." Both clauses are false after the rescope — write-back is deleted and
  the learnings agent is retired. Remove it; do not leave it as harmless stale prose,
  because it contradicts the no-write-back contract this feature must assert.
- **AC12** — `05g` propagates to all three roots; `opencode/agents/05l-*` is absent
  via feature `01`'s pruning.

### Non-Goals

- Mechanical enforcement of the verdict. No hook blocks push or merge on `NO-GO` —
  deferred to a hook-owning phase and recorded as such.
- Auto-remediation of findings.
- Reading PR comments (AC9).
- Modifying `prod-code-review`. `05g` extends its conventions; it does not rewrite
  the existing gate.
- Narrowing the orchestrator's `execute` to `gh`. Not expressible on Claude; the
  allowlist deliverable was deleted from this phase.

### Traceability

| Acceptance Criteria | Code Areas/Modules | Test / Evidence Category |
|---|---|---|
| AC1, AC12 | `05g` file; generated roots | Must-have automated test (new) |
| AC2, AC3, AC4, AC5 | `05g` body | Existing test to update — `tests/test_readiness_synthesis_agents.py` |
| AC6 | `05g` body + any new validator | Code-review evidence; **must record open/closed explicitly** |
| AC7, AC8, AC10 | `05-pr-review.agent.md` posting path | Must-have automated test (new) — contract assertions; **live QA in a scratch repo** |
| AC9 | orchestrator + `05g` bodies | Must-have automated test (new) — absence assertion |
| AC11 | `tests/test_readiness_synthesis_agents.py` | Existing test to update |

## B. Correctness & Edge Cases

**AC6 is the acceptance criterion most likely to be quietly dropped.** P5-SEC-02 is
a recorded High finding, and the recorded reason it stayed open is that there was
no code to attach a validator to. This feature rebuilds the readiness path — which
is exactly the moment the recorded plan says the validator should arrive. If the
rebuild ships as Markdown prose again, the finding does not close, and the honest
outcome is to say so. The recorded rule is explicit: **when the honest fix requires
capability a phase has excluded, the phase records the finding — it does not
redefine the finding to fit the scope.** Note the tension to resolve openly: a
"strict schema and deterministic reducer" implies code, and this phase ships agent
Markdown. Resolve it as a decision with an owner, not by rewording the finding.

**Posting publishes a verdict to collaborators.** *Auto* means a `NO-GO` with a
severity-ordered blocking list appears on a colleague's PR before the author has
read it. The upfront prompt must say that plainly. *Ask when ready* is the
recommended default precisely because it preserves the unattended run while keeping
a human between the finding and the audience.

### Failure modes

| Mode | Handling |
|---|---|
| `gh` absent / unauthenticated | AC8 — report alongside the local report; not a failure |
| No PR open for the branch | AC8 — report the condition; local report stands |
| `gh` posting fails mid-way (network, rate limit, permissions) | Report the failure; the local report is the deliverable. Never retry into a prompt |
| Report too large for a PR comment | Truncate with a pointer to the local report path, or post a summary. Decide and record — a silently truncated verdict is a misreported verdict |
| An evaluator report is missing or unreadable | AC4 — named in `Checks Not Run`; verdict below GO |
| Every evaluator failed | Verdict is `NO-GO` with an explicit no-evidence outcome; do not emit an empty GO |
| A prompt appears after the block | AC10 — only the designed *ask when ready* confirmation, which blocks nothing |

## C. Consistency & Architecture Fit

`05g` extends `prod-code-review`'s conventions on a different axis: `prod-code-review`
gates a phase's feature set from pipeline documents; `05g` gates a branch diff from
evaluator reports. The existing `05l` body already references
`.github/agents/prod-code-review.md` and the four severity levels — preserve both.

The existing `05l` is close to correct already: report-only synthesis, never reads
code, `Checks Not Run`, "no blockers found, coverage incomplete" ceiling, ≤10-line
return, top tier. Verified present in
`tests/test_readiness_synthesis_agents.py`'s current assertions. **Rescope, don't
rewrite.** What changes is the report root, the roster it reads, and the deletion
of the verdict write-back that its orchestrator used to perform.

Concrete names copied exactly from the Phase document: `05g-readiness-synthesizer`,
`readiness-report.md`, `GO`, `GO WITH CONDITIONS`, `NO-GO`, `Checks Not Run`.

## D. Clean Design & Maintainability

The synthesizer's whole value is that it cannot be fooled by an absence. Every
design decision should serve that: structured status records in, named missing
checks out, no verdict above the evidence.

**Complexity risk**: posting logic accreting retries, formatting modes, and
fallbacks inside an agent prompt. Posting is one command with three outcomes
(posted / no PR / unavailable). Keep it that size.

### Keep-it-clean checklist

- [ ] `05g` reads reports only — no code, no other agents' internals
- [ ] `Checks Not Run` cannot be omitted
- [ ] No status-line write-back anywhere
- [ ] `never` makes no network call
- [ ] P5-SEC-02 explicitly closed or explicitly recorded open
- [ ] Posting stays one command with three outcomes

## E. Completeness: Observability, Security, Operability

**Observability decision** — The readiness report *is* the observability artifact.
`evaluator-status.jsonl` from feature `04` is its input. Add nothing else. The
report must name the revision it examined — the recorded lesson is that an evidence
artifact which does not name its revision cannot be reconciled against later work,
and a readiness verdict is exactly such an artifact.

**Security** —
- AC9 (one-way output) is a prompt-injection boundary, not a preference. A PR
  comment thread is attacker-influenceable text; reading it back into an agent that
  holds `execute` is the injection surface this project has a whole phase about.
- AC6 (P5-SEC-02) is a recorded High finding whose closure this feature owns.
- Posting requires `gh`, which runs through the orchestrator's existing `execute`.
  This adds **no new exposure**: the orchestrator already holds unrestricted Bash
  for base derivation, so `gh` widens nothing. The phase's original premise — that
  granting `gh` meant granting every shell command and therefore needed an allowlist
  first — was false in the direction that matters: the grant was already there.

**Runbook** — Verify: dry run with each of the three consent settings. Rollback:
`git revert`. Note that a posted PR comment is **not** rolled back by reverting the
agent; it is already published. That asymmetry is why *ask when ready* is the
recommended default.

## F. Test Plan

**Existing tests to update**
- `tests/test_readiness_synthesis_agents.py` — retarget to `05g`, the renamed
  skills, and the new report root (AC11). The file's `05i` tests are already deleted
  by feature `02`; this feature finishes the rewrite.
- `tests/test_propagate_master_assets.py` — `expected_slugs` roster reconciliation.

**Must-have automated tests (new)**

Top-value cases:

1. **`Checks Not Run` is mandatory and GO is capped (AC4).** Given a body assertion
   suite, then the agent declares that any not-run or incomplete record makes `GO`
   invalid and that missing checks are named. This is the phase's central safety
   property.
2. **No write-back on any path (AC5).** Assert neither `05g` nor the orchestrator
   references `PROJECT_ROADMAP.md` or a phase summary status line.
3. **`never` makes no network call (AC7).** Assert the posting path declares that
   the *never* setting performs no `gh` invocation.
4. **One-way output (AC9).** Assert no body reads PR comments or network-sourced
   text back in.
5. **Report-only synthesis (AC2).** Retain the existing assertion that `05g` never
   reads code — it exists today and must survive the rescope.

**Manual QA checks**
- **Live QA in a scratch consumer repo, never this one**: post with a real PR open;
  post with no PR open; post with `gh` unauthenticated; run with *never* and confirm
  no network call.
- Dry run with *ask when ready*: confirm the report file exists on disk **before**
  the prompt appears — the property that makes the option both unattended and safe.

## Unverified Assumptions

- That `gh pr comment` can address the PR for the current branch without the caller
  knowing the PR number. `gh pr view` / `gh pr comment` resolve the PR from the
  current branch when one exists; the no-PR-exists path (AC8) is the documented
  failure. Verify in the scratch repo rather than assuming.
- That a readiness report fits in a PR comment. GitHub comment bodies have a size
  limit; a large branch could exceed it. Resolve the truncation decision in Stage 3.

## Relationship to Sibling Plans

- **Depends on `04`** (orchestrator; this feature edits the same file to add the
  posting path — the reason it is `parallel_safe: no`), **`05`** and **`06`** (their
  reports are `05g`'s inputs).
- **Consumes feature `03`'s** `pr-review-report` templates as pinned inputs.
- **Blocks `08-retirement-reconciliation`**, which verifies the whole assembly.

## Stage 0: Test Prerequisites

**Goal**: Not required. Baseline 416 passed across 4 consecutive full runs
(2026-07-16). Note the count will have dropped by feature `02`'s deletions.
**Success Criteria**: n/a
**Status**: Not required

## Stage 1: Rename and Retarget the Synthesizer

**Goal**: `git mv` `05l` → `05g`; retarget the report root and the roster it reads;
preserve the report-only, `Checks Not Run`, and GO-ceiling contracts verbatim.
**Success Criteria**: AC1, AC2, AC3, AC4, AC5, AC12.
**Status**: Not Started

## Stage 2: Resolve P5-SEC-02

**Goal**: Decide and record whether the rebuilt readiness path carries a strict
schema and deterministic status reducer, or whether P5-SEC-02 stays open. Record the
decision with an owner either way.
**Success Criteria**: AC6 — an explicit, recorded outcome. "Tightened the wording"
is not an outcome.
**Expected outcome, stated up front so it is not discovered as a surprise**: the
recorded finding says P5-SEC-02 "is closed by rebuilding the readiness path **in
code**" (`cross-phase-decisions.md`). This phase ships **agent Markdown**, not code.
So the honest default is **"remains open, recorded with an owner and routing"** —
and that is an acceptable Stage outcome. What is *not* acceptable is closing it by
asserting the contract more firmly in prose, which is the exact move the Phase 03
security scan already faulted.
**Status**: Not Started

## Stage 3: Posting Path

**Goal**: Implement auto / ask-when-ready / never against the choice captured
upfront; handle no-PR, absent `gh`, and unauthenticated `gh` as reported conditions;
decide the oversized-comment behavior.
**Success Criteria**: AC7, AC8, AC10.
**Status**: Not Started

## Stage 4: Rewrite the Synthesis Tests and Prove It

**Goal**: Rewrite `tests/test_readiness_synthesis_agents.py`; add the posting and
one-way assertions; dry-run all three consent settings.
**Success Criteria**: AC9, AC11; suite green; report-before-prompt verified.
**Status**: Not Started
