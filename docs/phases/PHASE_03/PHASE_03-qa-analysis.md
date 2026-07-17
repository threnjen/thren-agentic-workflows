# QA Readiness Analysis: Phase 03 — PR Review Agent Family

**Date:** 2026-07-16
**Analyst:** prod-code-review (automated)
**Mode:** Standard mode (`All verdicts Approved: NO` — 8/8 Approved with Reservations)
**Verdict:** **NO-GO**
**Documents Analyzed:** 46 (40 per-feature pipeline documents, 5 phase-level documents, 1 manifest), plus source assets, all three generated roots, the propagator, and the test suite
**Findings:** 8 (3 blockers, 1 high, 2 medium, 2 low)
**Diff range:** `ae9823a..HEAD` on `phase/pr-review`

> **This document supersedes the pre-rescope analysis at this path.** The prior body was
> the QA readiness analysis for the Phase Final Review family (formerly Phase 05), whose
> five evaluators feature `02` deleted and whose fixture root feature `08` retired. It is
> preserved in git at `ae9823a`. Its verdict was also NO-GO; per `PROJECT_ROADMAP.md:29`
> that NO-GO is superseded rather than repaired.

---

## Readiness Verdict

**NO-GO.** Phase 03 must not enter manual QA as a release-ready phase.

This is not a close call and it is not a penalty for effort. The phase's own records say
it plainly: feature `08`'s reviewer wrote *"The phase is NOT GO. AC1–AC4 are unexecuted.
The assembled agent family has never run"* (`08-…-review.md:307`). The recorded contract
governs — *a fixture dry-run is required release evidence; a run whose required evaluators
are recorded `not-run` is below-GO evidence, not a passing run.* Four of feature `08`'s
eleven ACs (`AC1`–`AC4`) are recorded **NOT DONE**, and they are precisely the four the
other seven features were built toward.

Missing required checks are a hard readiness gate. The canonical verdict is NO-GO, and
no roadmap or summary status line may be updated on this verdict. **This analysis updated
no status line.**

The verdict would be NO-GO on the unexecuted dry run alone. During this review it became
**over-determined**: an independent inspection of the generated roots surfaced a concrete,
previously-unreported delegation defect (B2 below) that would break the fan-out on two of
three harnesses — the exact class of failure the never-executed dry run exists to catch,
found by looking where no test looks.

---

## Executive Summary

Phase 03 is an unusually well-documented phase whose quality of *record-keeping* is not in
question — the QA plan and coverage map are among the strongest artifacts this pipeline has
produced, and they name the phase's central gap themselves rather than obscuring it. The
work is substantially complete and 54 of ~75 ACs are provably done: the roster resolves
8/8 in source, propagation is at a verified fixed point, and the suite reproduces exactly
as recorded (`1 failed, 582 passed, 106 subtests`), with the sole failure — PERF-01 —
independently confirmed as **not** a Phase 03 regression.

The phase is nonetheless NO-GO on three blockers. **B1:** the assembled family has never
been run; `dev/pr-review/` contains only `fixtures/`, and `08/AC1`–`AC4` are recorded NOT
DONE. Eight green features are not evidence the family runs — the tests assert contracts
over Markdown bodies and prove the family is *described* correctly, never that it *works*.
**B2 (new, not in any review, security scan, or QA document):** the orchestrator's
propagated Claude and Codex bodies delegate to `05a`–`05g` slugs, but the agents in those
roots are named `z-*`; the propagator's reference rewrite is a **complete no-op** on this
orchestrator (0 rewritten references, against 9 in the working `04-phase-execute`), so the
names the fan-out delegates to do not exist in 2 of 3 generated roots. **B3:** the open
High `P3-SEC-01` — the newly-live prune path deletes without a canonical containment check,
reproduced escaping the repo root — is unremediated, and the containment helper it needs
already exists 900 lines away in the same file, unused.

Highest-risk areas are, in order: the unexecuted fan-out (B1), cross-root name resolution
(B2), and filesystem containment on the new delete path (B3). **Confidence in the QA plan's
ability to catch remaining issues is high for runtime behavior and low for security**: its
nine sections map 1:1 onto the manifest's checklist with nothing dropped, and section 1
would almost certainly have caught B2 on first execution — but the plan carries **zero**
references to `P3-SEC-01`, `P3-SEC-02`, or `REPO-SEC-06` and never cites the security scan
at all, leaving an open High on a live deletion path invisible to the tester (F4).

---

## Document Inventory

All 40 per-feature documents are present; no document is missing and none is extraneous.

### Per-Feature Documents

| Feature | plan | context | tasks | implementation | review |
|---|---|---|---|---|---|
| `01-propagator-orphan-pruning` | Yes | Yes | Yes | Yes | Yes |
| `02-retired-evaluator-removal` | Yes | Yes | Yes | Yes | Yes |
| `03-pr-review-conventions-skills` | Yes | Yes | Yes | Yes | Yes |
| `04-pr-review-orchestrator` | Yes | Yes | Yes | Yes | Yes |
| `05-mechanical-evaluators` | Yes | Yes | Yes | Yes | Yes |
| `06-narrative-and-test-health` | Yes | Yes | Yes | Yes | Yes |
| `07-synthesis-and-pr-posting` | Yes | Yes | Yes | Yes | Yes |
| `08-retirement-reconciliation` | Yes | Yes | Yes | Yes | Yes |

All eight review verdicts: **Approved with Reservations**.

### Phase-Level Documents

| Document | Path | Source | Present | Notes |
|---|---|---|---|---|
| QA Plan | `docs/phases/PHASE_03/PHASE_03_QA.md` | z-feature-qa-writer | Yes | Rewritten 2026-07-16 for the rescope; prior body void, not stale |
| Coverage Map | `docs/phases/PHASE_03/PHASE_03_QA_COVERAGE_MAP.md` | z-feature-qa-writer | Yes | 54 automated / 17 manual / 6 partial |
| Phase Summary | `docs/phases/PHASE_03/PHASE_03_SUMMARY.md` | Phase - Refiner | Yes | Status line intentionally **not** updated — correct under an unverified verdict |
| Manifest | `dev/feature/phase-03-pr-review-execution-manifest.md` | Feature - Decomposer | Yes | 9 manual checklist items, all covered |
| Security Scan | `docs/phases/PHASE_03/PHASE_03-security-scan.md` | security-scan | Yes | **Pass with Conditions.** Uncommitted in the working tree (F8) |
| Discovery Context | `docs/phases/PHASE_03/PHASE_03_DISCOVERY_CONTEXT.md` | Phase - Refiner | Yes | — |

**Note on the output path:** this file previously held the pre-rescope analysis (a
different phase's record). It is superseded here and recoverable at `ae9823a`.

---

## Independent Verification Performed

This agent re-derived the following from disk rather than accepting the records:

| Claim | Source | Verified | Result |
|---|---|---|---|
| Suite state | QA plan `:174` | `pytest tests/ -q` | **Exact match** — `1 failed, 582 passed, 106 subtests` |
| PERF-01 is the only failure | QA plan `:176` | Suite run | Confirmed; median 55.80 ms, `tests/hooks/test_hook_distribution_integration.py:223` |
| Per-file test counts (8 files) | Coverage map `:32-41` | `--collect-only` per file | **All 8 exact** (42/38/28/23/21/21/18/5 = 196) |
| Source roster resolves 8/8 | `08/AC5` | `ls .github/agents/05*` | Confirmed — `05-pr-review`, `05a`–`05g` |
| Five retired agents absent | `02/AC1` | `ls` + repo-wide grep | Confirmed (residue only in tests asserting absence, and exempt `docs/**` + learnings) |
| Fixture range | QA plan `:86-91` | `rev-parse`, `merge-base`, `diff --shortstat` | Confirmed — 3 commits, 26 files, 1288 insertions, merge-base **is** the base |
| **Family has never run** | `08/AC1` | `ls dev/pr-review/` | **Confirmed — only `fixtures/` exists** |
| Propagation is a fixed point | `08/AC8` | Re-ran propagator; `git status` | Confirmed — zero generated-file diff |
| `execute` held by exactly 2 agents | Roster decision | Frontmatter sweep | Confirmed — only `05-pr-review` and `05a-baseline-worktree` |
| `05b` lacks an `agents:` allowlist | `P3-SEC-02` | Frontmatter sweep | Confirmed — sole `agent`-holder without one; `05f` has `agents: [Test - Analyst]` |
| `P3-SEC-01` containment gap | Security scan `:68` | Read `propagate_master_assets.py:247-286` | Confirmed — leaf-only symlink guard, no canonical containment |
| **Claude/Codex delegation names** | — | Compared all 3 generated roots | **NEW DEFECT — B2** |

---

## Traceability Matrix

Condensed to ACs that are not cleanly closed. All other ACs (54 of ~75) trace Plan →
Implementation → Code → Review → QA without gap and are omitted for brevity.

| Feature | AC | Plan | Impl | Code | Review | In QA | Verdict |
|---|---|---|---|---|---|---|---|
| `08` | **AC1** — end-to-end dry run | Defined | **NOT DONE** | N/A (runtime) | Acknowledged; reviewer: *"NOT GO"* | §1 | **BLOCKED (B1)** |
| `08` | **AC2** — single-interaction end to end | Defined | **NOT DONE** | N/A | Acknowledged | §2 | **BLOCKED (B1)** |
| `08` | **AC3** — forced-failure run not `GO` | Defined | **NOT DONE** | N/A | Acknowledged | §3 | **BLOCKED (B1)** |
| `08` | **AC4** — every return ≤10 lines | Defined | **NOT DONE** | N/A | Acknowledged | §4 | **BLOCKED (B1)** |
| `06` | AC5b — Codex depth-2 delegation | Defined | *"Verification deferred to manual QA"* | Declared only | Acknowledged | §5 | **AT RISK** — not statically verifiable |
| `04` | AC14 — propagates; roster live on all roots | Defined | Done | **Defect** — see B2 | Passed (parity only) | §9 | **BLOCKED (B2)** |
| `05` | AC8b — `05a` declared with `execute` | Defined | Done | Verified | Passed | — | **OPEN by design** — declared-and-unclosable, routed |
| `01` | AC5 — never delete a non-generated file | Defined | Done | Verified (marker guard) | Passed | — | **AT RISK (B3)** — holds *inside* the root; no containment *of* the root |
| `07` | AC6 — P5-SEC-02 closed or recorded open | Defined | Done (recorded open) | Verified | Passed | Security § | **OK — correct, not a defect** |
| `08` | AC9 — baseline reconciled | Defined | Done (**false figure**) | N/A | **Disproved and fixed** | Notes | **OK on disk; record stale (F7)** |

**Manifest → QA coverage:** the manifest's 9 `## Verification Assets` checklist items map
1:1 onto the QA plan's 9 sections. **None dropped.** Verified item by item.

---

## Findings

### Blockers

#### B1 — The assembled agent family has never been run *(the central gap)*

**Severity: Blocker.** **Evidence:** `ls dev/pr-review/` returns only `fixtures/` — no run
directory has ever existed. `08-…-implementation.md:51-54,70` records `AC1`–`AC4` **NOT
DONE**; `08-…-review.md:307` states *"The phase is NOT GO."*

The causal chain is honest and correctly handled at every step: feature `04` authored the
orchestrator and pinned the fixture, then deferred the dry run to `08` — correct, since
five of eight roster agents did not exist yet. Feature `08` could not execute it: its
context had no agent-spawning tool, so a seven-way fan-out could be neither run nor
simulated. It recorded NOT DONE with routing **rather than manufacturing a partial run** —
also correct, since a partial run produces below-GO evidence by construction.

Nothing here is a defect of judgment. But a deferred verification that never executed is
still an unexecuted verification, and it is the one the phase is *for*. Every precondition
now verifies for the first time (roster 8/8, fixture reachable, output gitignored,
propagation at a fixed point) — the run is now *possible*, and simply must happen.

**B2 is the proof of why this matters**: a defect that eight green reviews and 582 passing
tests did not surface, sitting directly on the fan-out path, found in minutes by looking at
what the run would actually do.

**Root cause:** not attributable to a deficient agent — an environmental capability gap.
**Route:** manual QA §1–§4 (agent-spawning context required).

#### B2 — Orchestrator delegates to names that do not exist on Claude or Codex *(NEW)*

**Severity: Blocker.** Not reported in any review, the security scan, or any QA document.

**Evidence:**

| Root | Agent names on disk | Orchestrator delegates to | Resolves? |
|---|---|---|---|
| `opencode/agents/` | `05a-baseline-worktree.md` … `05g-readiness-synthesizer.md` | `05a-baseline-worktree`, `05g-…` | **Yes** |
| `claude/agents/` | `z-baseline-worktree.md`, `z-change-narrator.md`, `z-artifact-sweeper.md`, `z-consistency-auditor.md`, `z-dependency-auditor.md`, `z-test-health.md`, `z-readiness-synthesizer.md` | `05a-baseline-worktree`, `05b`–`05g`, `04e-diff-security-scan` | **No** |
| `codex/agents/` | `z-*.toml` (`name = "z-change-narrator"`) | same | **No** |

Counts of rewritten references:

- `claude/commands/phase-execute.md` → **9** `z-` references (rewrite fired)
- `claude/commands/pr-review.md` → **0** `z-` references (rewrite is a **complete no-op**)

**The decisive evidence** is the same delegated agent referenced two ways. `04e Diff
Security Scan` is propagated once, as `claude/agents/z-diff-security-scan.md`. The working
orchestrator names it correctly (`claude/commands/phase-execute.md:165`,
`z-diff-security-scan`); the new one does not (`claude/commands/pr-review.md:206,212`,
`04e-diff-security-scan`). One agent, one root, two orchestrators — one resolves, one
cannot.

**Root cause:** `_rewrite_agent_references` (`scripts/propagate_master_assets.py:565-567`)
rewrites body references using a map built by `_build_agent_reference_map` (`:554-562`),
which is **keyed on `agent.name`** — the *display* name. The house convention, demonstrated
by `.github/agents/04-phase-execute.agent.md:64,78,92`, is to reference subagents in the
body by **display name** (`Feature - Implementer`) so the rewrite fires.
`.github/agents/05-pr-review.agent.md:176,205,207,274` instead references them by **slug**
(`05a-baseline-worktree`, `05g-readiness-synthesizer`, bare `05b`–`05f`). The display-name
map never matches a slug, so every roster reference passes through verbatim into roots
where the agents carry `z-` names.

The orchestrator's own `agents:` frontmatter (`:5`) already carries the correct display
names — `[Baseline Worktree, 05b Change Narrator, 05c Artifact Sweeper, …]` — so the body
contradicts its own frontmatter.

**Why no test caught it:** the suite asserts (a) body contracts against the **source**, and
(b) file presence/parity per generated root (`test_roster_propagates_to_all_three_generated_roots`).
**No test asserts that a name an orchestrator body delegates to resolves to an agent
existing in the same generated root.** This is exactly the "described correctly vs actually
runs" gap the QA plan names at `:43-45` — instantiated.

**Why it is a Blocker:** it lands on the fan-out path of the phase's headline deliverable,
on the primary harness (Claude) and on the one harness §5's delegation check *requires*
(Codex). QA §9 would surface it; QA §1 would fail on it. OpenCode — the only harness that
works — works only incidentally, because it keeps source slugs.

**Fix (small, in source):** change the roster references in
`.github/agents/05-pr-review.agent.md` body from slugs to the display names already in its
own `agents:` frontmatter, then re-propagate. Recommend adding the missing invariant as a
test: every agent name referenced in a generated orchestrator body resolves within that
root.

**Root cause stage:** `z-feature-implementer` (feature `04` source body), with a
contributing gap in `z-feature-reviewer` (parity was verified as file presence, not name
resolution).

#### B3 — `P3-SEC-01`: prune deletion escapes the repository root — open High

**Severity: Blocker (release), High (security).** **Evidence:**
`scripts/propagate_master_assets.py:256` guards only the **leaf**
(`if path.is_symlink() or not path.is_file(): continue`) before `path.unlink()` at `:260`.
`:277-284` does the same before `shutil.rmtree(dest_dir)` — recursive removal. Neither
performs a canonical containment check on the generated **root** or its parents. If a root
is itself symlinked, `directory.is_dir()` follows it, `glob` enumerates the real target,
leaf files there are not symlinks, and a marker-bearing file is deleted outside the repo.
Reproduced in a sandbox per the security scan (`:76-118`). Extends `REPO-SEC-06` from
writes to deletes; **genuinely new**, since the baseline prune was inert (0/24 matched).

**The gap is sharper than the scan states:** the exact check required already exists in the
same file. `_validate_output_directory` (`:1173-1184`) performs canonical
`resolve().relative_to(resolved_root)` plus root-symlink rejection, and
`_validate_nested_output_directory` (`:1187-1205`) walks intermediate components. **Neither
prune call site (`:1444-1446`, `:1569-1581`) invokes either.** The fix is applying an
existing in-file helper, not writing a new one.

Mitigating: the marker guard (`_is_generated_output`) and the two-condition rule mean an
attacker needs both a symlinked root and marker-bearing content — hence High, not Critical.

**Root cause stage:** `z-feature-implementer` (feature `01`). **Route:** security
remediation before release, or an explicit, owner-named accepted risk. It must not enter
QA silently — see F4.

### High

#### F4 — The QA plan is blind to the phase's open security findings

**Severity: High.** **Evidence:** `PHASE_03_QA.md` and `PHASE_03_QA_COVERAGE_MAP.md`
contain **zero** occurrences of `P3-SEC-01`, `P3-SEC-02`, or `REPO-SEC-06`, and **never
cite `PHASE_03-security-scan.md`** — the only match for "security" in the plan is the
unrelated `04e` evaluator at `:154`. Both documents handle `P5-SEC-02` (2 mentions each)
and `PERF-01` (2 / 1) with real care, and the plan's Security section (`:338-342`) covers
P5-SEC-02, read-only boundaries, and worktree cleanup.

So the omission is not carelessness about security generally — it is specifically that the
two findings **this phase introduced or worsened** are absent, while the two it *inherited*
are handled. The likely cause is ordering: the QA plan was committed at `4b856a0` and the
security scan is still **uncommitted** in the working tree (F8), i.e. finalized afterward
and never reconciled back.

**Consequence:** a tester runs section 1's dry run and the propagation checks — exercising
the very delete path carrying an open, reproduced High — with no indication it exists. Per
Phase 2C, every open risk must be covered by QA or recorded as an accepted risk; this is
neither.

**Root cause stage:** `z-feature-qa-writer`. **Fix:** add a Security subsection recording
`P3-SEC-01` (open High, routed) and `P3-SEC-02` (open Medium), in the same routed-risk
style already used for PERF-01, and cite the scan in Prerequisites.

### Medium

#### F5 — `P3-SEC-02`: `05b-change-narrator` holds delegation with no allowlist

**Severity: Medium.** **Evidence:** `.github/agents/05b-change-narrator.agent.md:4` —
`tools: [agent, read, search, edit]` with **no `agents:` key**. It is the only Phase 03
agent holding `agent` without an allowlist; `.github/agents/05f-test-health.agent.md:5`
shows the pattern (`agents: [Test - Analyst]`). Propagates to
`claude/agents/z-change-narrator.md:4` as `tools: … Agent …`, unconstrained. An
unconstrained delegation grant is an indirect route to an `execute`-holding agent.

Closable in **one frontmatter line** (`agents: [<the per-directory readers 05b may spawn>]`).
Recommend closing before QA rather than routing — the cost is a line and the pattern is
already established next door.

**Root cause stage:** `z-feature-implementer` (feature `06`).

#### F6 — QA §9's Claude check is not executable as written

**Severity: Medium.** **Evidence:** `PHASE_03_QA.md:322` instructs: *"confirm all eight
agents resolve: `05 PR - Review`, `05a`–`05g`."* On Claude, **none of those names exist**:
the seven evaluators propagate as `z-*` (`claude/agents/z-change-narrator.md` etc.) and the
orchestrator propagates not as an agent but as the slash command
`claude/commands/pr-review.md`. A tester following the step literally finds 0 of 8 and
cannot tell whether that is the expected `z-`/command mapping or the real defect (B2) — the
two are indistinguishable from the instruction as written.

The step is also the phase's best detector for B2, which makes fixing its wording valuable
rather than cosmetic. §9's OpenCode line (`:323`) is correct and does note the source-slug
keying.

**Root cause stage:** `z-feature-qa-writer`.

### Low

#### F7 — A disproved test-count claim survives in the record and propagated into both QA documents

**Severity: Low.** **Evidence:** `08-…-implementation.md:77` claims *"561→581 passed,
exactly +20"*, with the arithmetic at `:257-272`. The reviewer independently disproved it
(`08-…-review.md:12-18,73`): the suite was **red** at `3cd47e5` (`2 failed, 580 passed`),
reported as `1 failed, 581 passed` from a pre-commit run never re-measured. Issue #1 (High)
was **Fixed** and reconciled to `582` (`:64,278,293`). I measured **582** — the review is
right.

But the implementation record was **never corrected**, and the QA writer read AC9 from it
rather than from the review, carrying the disproved figure into `PHASE_03_QA.md:356` and
`PHASE_03_QA_COVERAGE_MAP.md:135` — each now **contradicting its own header** (`:174` and
`:43` respectively both say 582).

Cosmetic in effect — disk is correct and the QA headline figure is right. Noted because it
is the phase's evidence-integrity pattern reaching the release documents: a falsified claim,
caught by review, still propagating two documents downstream. It bears on how much
confidence the static records carry on their own.

**Root cause stage:** `z-feature-implementer` (record not updated post-fix) →
`z-feature-qa-writer` (sourced AC9 from the record, not the review).

#### F8 — The security scan is uncommitted

**Severity: Low.** `git status` shows `docs/phases/PHASE_03/PHASE_03-security-scan.md`
modified (+401/−81) and unstaged. The phase's sole security deliverable — carrying an open
High — is not in the commit graph and would be lost by a clean checkout. Likely the
proximate cause of F4. **Fix:** commit it before QA.

---

## Cross-Document Consistency (Phases 2A–2E)

| Check | Result |
|---|---|
| 2A Plan → Implementation | **Pass with one gap.** Every AC traces; no scope creep, no silent drops. `08/AC1`–`AC4` are honestly recorded NOT DONE rather than quietly closed — the correct handling of B1. |
| 2B Implementation → Review | **Pass.** No review is Approved while carrying an open Blocker. Every "Fixed" I spot-checked has a corresponding code state. **Notable inversion:** in 8/8 features the implementer's mutation-sweep claim ("0 inert guards") was disproved by the reviewer's independent sweep — including a security-relevant one-way-boundary guard (`07` Issue #3) and a guard asserting a token appearing 13 times, which could never fail (`06`). The reviews caught all of them. This is the layer working as designed, but it means **implementer self-attestation carries near-zero independent weight in this phase** — and it is why B2, which no reviewer's sweep was scoped to catch, matters. |
| 2C Review → QA | **Fail (F4).** Runtime reservations are well covered (`07` Issues #3/#4 → §7; `06`/AC5b → §5; graph dependency → §8). Open **security** findings are not covered at all. |
| 2D Plan → QA | **Pass.** All 9 manifest checklist items map to sections; the plan explicitly tells testers what *not* to hand-test (`:163-184`), avoiding redundant manual effort; non-goals appear as negative tests (§7 *never* = no network call; §9 no retired agent loadable). |
| 2E Context accuracy | **Pass.** Architectural decisions held: report key derived from SHA+timestamp (no branch name reaches a path — verified in the declared shape); `execute` confined to 2 agents; `worktree-baseline` consumed unchanged. |

---

## QA Plan Quality Assessment (Phase 4)

The QA plan is **high quality** and should be preserved through remediation, not rewritten.

| Dimension | Assessment |
|---|---|
| Actionability | **Strong**, with one exception (F6). Nearly every item carries a concrete action, a command, and an observable expected result. Several encode *why* the naive reading fails — §6's self-exclusion rationale and §1's added-line-vs-touched-file distinction are genuinely instructive. |
| Coverage completeness | **Strong on runtime, gap on security (F4).** 17 manual items → 9 sections, 1:1 with the manifest, none dropped. |
| Efficiency | **Excellent.** The "what NOT to hand-test" section (`:163-184`) is exactly right and rare. |
| Prerequisites | **Strong.** The scratch-consumer-repo setup is copy-pasteable with a stated rationale for why this repo must not be used; the venv/`rtk` note is a real, earned detail. Missing: a pointer to the security scan (F4). |
| Error scenarios | **Excellent.** §3's asymmetry — a fan-out failure must *not* abort, an `05a` preflight failure *must* — is the sharpest test-design decision in the document. |
| Cross-cutting | **Good.** Performance framed as context pressure with PERF-01 correctly excluded; accessibility correctly N/A. Security is the weak axis (F4). |

**The plan's greatest strength is its honesty.** It leads with its own central gap
(`:22-46`), states that 582 passing tests prove the family is *described* correctly and
"prove nothing about whether it *works*", and records the fixture's own weakness (zero
deletions, `:364`). This is a QA document written to find problems rather than to be passed
— and B2 is the vindication of that framing: it was found exactly where the plan says to
look.

---

## Risk Register (Phase 5)

| # | Risk | Likelihood | Impact | QA Detection | Recommendation |
|---|---|---|---|---|---|
| 1 | Family has never run; unknown runtime defects (B1) | **Certain** | **Blocker** | **Yes — §1 is designed for it** | Execute §1–§4 before any release claim |
| 2 | Claude/Codex delegation fails to resolve (B2) | **High** (0 of 8 names resolve in 2 roots) | **Blocker** | Yes — §9 detects, §1 fails on it | Fix source body to display names; re-propagate; re-run §1 on Claude **and** Codex |
| 3 | Prune deletes outside repo root (B3 / `P3-SEC-01`) | Low (needs symlinked root + marker) | **Blocker** (unrecoverable deletion) | **No** — not in the QA plan (F4) | Apply `_validate_output_directory` at both prune sites; add symlinked-root regressions |
| 4 | Tester unaware of open security findings (F4) | **Certain** if QA proceeds as written | High | **No** — self-referential | Add a routed-risk Security subsection; cite the scan |
| 5 | `05b` unconstrained delegation (`P3-SEC-02`) | Low | Medium | No | Close now — one frontmatter line |
| 6 | Codex depth-2 silent inline fallback (`06`/AC5b) | **Medium** (`max_depth` defaults to 1) | High (reports success while not delegating) | **Yes — §5, from the transcript** | Run §5 on Codex specifically; never infer from prompt text |
| 7 | §9 Claude step misread as pass/fail (F6) | Medium | Medium | Self-referential | Reword to `z-*` names + the `/pr-review` command |
| 8 | Security scan lost from working tree (F8) | Medium | Medium | No | Commit it |
| 9 | `05a`/orchestrator `execute` grants unclosable | Certain (by design) | Medium | N/A | **No action.** Honestly recorded and routed — see below |
| 10 | `P5-SEC-02` remains open | Certain (by design) | High (inherited) | §Security verifies it stays open | **No action.** Correct as recorded |
| 11 | PERF-01 fails | Certain | N/A to this phase | Excluded by design | **No action.** Not a Phase 03 regression; **do not relax the budget** |
| 12 | Fixture has zero deletions | Certain | Low | Recorded `:364` | Accept; a second fixture if ever needed — never resize this one |

### Items assessed and found correct — no action

Three items that could be mistaken for defects are, on examination, correctly handled. This
agent's bias is toward finding problems; these are not problems.

- **`P5-SEC-02` recorded OPEN.** Verified open, negation-tested, with a named owner and
  routing. It closes only by rebuilding the readiness path *in code*; this phase ships agent
  Markdown. Recording it open is the honest outcome — **correct, not a defect.**
- **`05a` + orchestrator `execute` grants.** Narrowing was by **removal only**, and I
  verified the result: `execute` is held by exactly two agents, and `05b`–`05g` hold no
  shell. Per-agent command scoping is not expressible in Claude subagent frontmatter, so the
  two residual grants are declared-and-unclosable. The question is whether that is **honestly
  recorded** — it is: declared with justification in the agent bodies, in the security scan
  (`:340`), and routed to a hook-owning phase in `PROJECT_ROADMAP.md:29`. **Correct.**
- **PERF-01.** Independently confirmed not a Phase 03 regression (54.54 ms at `ae9823a` vs
  54.35 ms at HEAD; I measured 55.80 ms at HEAD). Correctly excluded and correctly refused a
  budget relaxation. **Correct.**

---

## Blocking Items — Root Cause Routing

1. **B1 — The assembled family has never been run.** `08/AC1`–`AC4` NOT DONE; `dev/pr-review/`
   holds only `fixtures/`.
   **Root cause:** not a deficient agent — an environmental capability gap (feature `08` had
   no agent-spawning tool). Both the deferral and the refusal to fabricate a partial run were
   correct.
   **Return to:** **manual QA execution** in an agent-spawning context — `PHASE_03_QA.md`
   §1–§4, after B2 is fixed (otherwise §1 fails on B2 and re-runs are wasted).
   **Then re-run:** this analysis, to convert `08/AC1`–`AC4` from NOT DONE to evidence-backed.

2. **B2 — Orchestrator delegates to names absent from the Claude and Codex roots.**
   **Root cause:** `.github/agents/05-pr-review.agent.md:176,205,207,274` references the
   roster by **slug**; `_build_agent_reference_map` (`propagate_master_assets.py:554-562`)
   keys on **display name**, so the rewrite is a no-op (0 refs vs 9 in `phase-execute`).
   **Return to:** `@z-feature-implementer` (feature `04`) with: *"Replace the roster's slug
   references in the `05-pr-review` body with the display names already declared in its own
   `agents:` frontmatter (`Baseline Worktree`, `05b Change Narrator`, …, `04e Diff Security
   Scan`), matching the `04-phase-execute` convention at `:64,78,92`. Re-propagate and verify
   `claude/commands/pr-review.md` and the Codex roster resolve to `z-*`. Add a test asserting
   every agent name referenced in a generated orchestrator body resolves within that root —
   the gap that let this ship."*
   **Then re-run:** propagation, the suite, feature `04` review, and QA §1 + §9 on Claude and
   Codex.

3. **B3 — `P3-SEC-01` open High: prune deletion escapes the repo root.**
   **Root cause:** `z-feature-implementer` (feature `01`) — `propagate_master_assets.py:256`
   and `:277` guard the leaf only; no canonical containment before `unlink`/`rmtree`.
   **Return to:** `@z-feature-implementer` (feature `01`) with: *"Apply the existing in-file
   `_validate_output_directory` (`:1173`) and `_validate_nested_output_directory` (`:1187`)
   at both prune call sites (`:1444-1446`, `:1569-1581`) so every generated root is
   canonically contained and no-follow before any deletion. Add symlinked-root regression
   tests per subtree. This closes `REPO-SEC-06` on the same pass."*
   **Alternative:** if deferred to the propagator/containment phase per the scan's
   recommendation (`:408`), it must be an **explicit, owner-named accepted risk** recorded in
   the QA plan — not silence (F4).
   **Then re-run:** the suite, feature `01` review, and the security scan's containment check.

**Sequencing:** fix **B2** and **B3** and **F4/F5** first, commit the security scan (F8),
then execute QA §1–§9. Running the dry run before B2 is fixed wastes the run.

---

## Recommendations

Ordered by priority.

1. **Fix B2 before anything else** — `z-feature-implementer`. It is small (one body's
   references), it blocks the headline QA item on 2 of 3 harnesses, and every hour of dry-run
   effort spent before it is fixed is wasted. Add the missing name-resolution test.
2. **Remediate or formally accept B3 (`P3-SEC-01`)** — `z-feature-implementer`. An open,
   reproduced High on a live deletion path cannot enter QA undocumented. The helper already
   exists in-file; prefer fixing over routing.
3. **Reconcile the QA plan with the security scan (F4)** — `z-feature-qa-writer`. Add a
   routed-risk Security subsection for `P3-SEC-01`/`P3-SEC-02`, in the same style already used
   well for PERF-01, and cite the scan in Prerequisites.
4. **Close `P3-SEC-02` (F5)** — `z-feature-implementer`. One frontmatter line; the pattern is
   already next door in `05f`.
5. **Commit the security scan (F8)** and **fix QA §9's Claude wording (F6)** —
   `z-feature-qa-writer`. Both are minutes of work; F6 sharpens the step most likely to detect
   B2.
6. **Then execute QA §1–§9** in an agent-spawning context — §5 on **Codex specifically**, §6–§7
   in the **scratch consumer repo only**. Treat §1 as the release gate it is.
7. **Correct the AC9 record and its two downstream copies (F7)** — low priority, but the
   phase's evidence-integrity pattern is the reason to close the loop rather than leave a
   disproved number in the release documents.
8. **Do not update any status line** until §1–§4 produce evidence. The verdict is advisory
   and unverified; `PHASE_03_SUMMARY.md` and `PROJECT_ROADMAP.md` are correctly untouched.

---

## Closing Note

The distribution of these findings is itself the phase's lesson. Fifty-four ACs are provably
done, propagation is at a fixed point, the suite reproduces to the test, the roster is
correct in source, and the two hardest security calls — `P5-SEC-02` and the unclosable
`execute` grants — were resolved the honest way rather than the convenient one. The QA plan
names its own central gap in its first section. This is careful work.

And the family still does not run on the primary harness, because nobody ran it. B2 sat in
plain sight in a generated file, past eight reviews and 582 passing tests, because every
assertion in this phase checks that the family is *described* correctly and none checks that
it *works*. The QA plan predicted this exactly — *"eight green features are not evidence the
family runs"* — and it was right on the first look.

Fix B2 and B3, reconcile the plan with the scan, then run it.
