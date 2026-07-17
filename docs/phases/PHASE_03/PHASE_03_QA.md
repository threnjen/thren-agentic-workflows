# QA Plan: Phase 03 — PR Review Agent Family

**Date:** 2026-07-16
**Last Updated:** 2026-07-16
**Mode:** Release QA Plan
**Scope:** Consolidated release QA for all eight features of Phase 03 — propagator orphan pruning, retirement of the five phase-shaped evaluators, the rescoped conventions/report skills, the `05-pr-review` orchestrator, the mechanical evaluators, narrative and test health, synthesis and PR posting, and reconciliation.
**Environment:** This repository at `/Users/jennywadkins/github_repos/github-agents-source-of-truth` for the fixture dry run; a **separate scratch consumer repo** for every live git/`gh` check (see Prerequisites).
**Coverage Map:** `docs/phases/PHASE_03/PHASE_03_QA_COVERAGE_MAP.md`

> **Rewritten 2026-07-16, not merged.** The prior document at this path was the QA plan
> for the pre-rescope Phase Final Review family. Every checklist item it carried was
> directed at `05c-qa-consolidator`, `05d-security-rollup`, `05e-ac-regression`,
> `05f-seam-analyzer`, or `05i-learnings-harvester` — **all five deleted by feature
> `02`** — or at the `dev/phase-final-review/fixtures/PHASE_05/` root that feature `08`
> retired (13 files). Those items are not stale, they are **void**: their subjects do
> not exist and no tester can execute them. Merging them forward would ship a checklist
> that cannot pass. The historical record is preserved in `docs/phases/**`, which
> feature `02` AC6 exempts from the reference sweep, and in git history.

---

## ⚠️ Read this before planning your session

**The assembled agent family has never been run.** This is the phase's central gap and
the reason this document exists.

Feature `04` authored the orchestrator and pinned a fixture for a dry run, then deferred
that run to feature `08`. Feature `08` could not execute it — its context had no
agent-spawning tool, so a seven-evaluator fan-out could be neither run nor simulated. It
recorded AC1–AC4 **NOT DONE** with routing rather than manufacturing a partial run, which
was the correct call: a partial run would have produced below-GO evidence by
construction.

What changed is that the run is now *possible for the first time*. Every precondition
verifies: the roster resolves 8/8, the report root migration completed, run output is
gitignored, and the pinned fixture range checks out. It simply was never *performed*.

**The recorded contract, which governs this entire plan:**

> *A fixture dry-run is required release evidence; a run whose required evaluators are
> recorded `not-run` is below-GO evidence, not a passing run.*

**Eight green features are not evidence the family runs.** 582 passing tests prove the
family is *described* correctly — they prove nothing about whether it *works*. Section 1
below is the headline item. If you run only one thing from this document, run that.

---

## Features Covered

| Feature | Plan | Implementation Record | Review Record |
|---|---|---|---|
| `01-propagator-orphan-pruning` | `dev/feature/01-propagator-orphan-pruning/01-propagator-orphan-pruning-plan.md` | `…-implementation.md` | `…-review.md` |
| `02-retired-evaluator-removal` | `dev/feature/02-retired-evaluator-removal/02-retired-evaluator-removal-plan.md` | `…-implementation.md` | `…-review.md` |
| `03-pr-review-conventions-skills` | `dev/feature/03-pr-review-conventions-skills/03-pr-review-conventions-skills-plan.md` | `…-implementation.md` | `…-review.md` |
| `04-pr-review-orchestrator` | `dev/feature/04-pr-review-orchestrator/04-pr-review-orchestrator-plan.md` | `…-implementation.md` | `…-review.md` |
| `05-mechanical-evaluators` | `dev/feature/05-mechanical-evaluators/05-mechanical-evaluators-plan.md` | `…-implementation.md` | `…-review.md` |
| `06-narrative-and-test-health` | `dev/feature/06-narrative-and-test-health/06-narrative-and-test-health-plan.md` | `…-implementation.md` | `…-review.md` |
| `07-synthesis-and-pr-posting` | `dev/feature/07-synthesis-and-pr-posting/07-synthesis-and-pr-posting-plan.md` | `…-implementation.md` | `…-review.md` |
| `08-retirement-reconciliation` | `dev/feature/08-retirement-reconciliation/08-retirement-reconciliation-plan.md` | `…-implementation.md` | `…-review.md` |

**Phase document:** `docs/phases/PHASE_03/PHASE_03_SUMMARY.md`
**Manifest:** `dev/feature/phase-03-pr-review-execution-manifest.md`

---

## Prerequisites

### Test runner

```bash
cd /Users/jennywadkins/github_repos/github-agents-source-of-truth
.venv/bin/python -m pytest tests/ -q
```

The system `python3` has no pytest — use the venv binary directly. The repo's normal
`rtk` wrapper reported a hook-integrity failure during implementation; call the venv
directly rather than through it.

### The pinned fixture

`dev/pr-review/fixtures/pinned-diff-range.md` defines the base/head pair. Read it before
the dry run — it records what each evaluator is *expected* to find, which is what turns
"the fan-out completed" into "the fan-out worked."

| Field | Value |
|---|---|
| Base SHA | `f5ab960e5697756538f94430327e2a68eb113822` |
| Head SHA | `e6ff28a36293697aebf62155ae0048115c4aecca` |
| Origin | PR **#17**, `feat/visual-verification-package` |
| Range | **3 commits, 26 files, 1288 insertions, 0 deletions** |

Confirm both SHAs are present before you start:

```bash
git rev-parse --verify f5ab960e5697756538f94430327e2a68eb113822^{commit}
git rev-parse --verify e6ff28a36293697aebf62155ae0048115c4aecca^{commit}
git merge-base e6ff28a36293697aebf62155ae0048115c4aecca f5ab960e5697756538f94430327e2a68eb113822
# -> f5ab960e5697756538f94430327e2a68eb113822  (the merge-base IS the base)
```

### The scratch consumer repo — required, and never this repository

Sections 6 and 7 below **must not run against this repository**. They require an unset
`origin/HEAD`, an unauthenticated `gh`, and a branch with no PR open — states this repo
is not in and must not be put into. Create a throwaway:

```bash
scratch=$(mktemp -d)/consumer && mkdir -p "$scratch" && cd "$scratch"
git init -b main && git commit --allow-empty -m "base"
git checkout -b feature/scratch
printf 'x\n' > f.txt && git add f.txt && git commit -m "add f"
# give it a remote WITHOUT setting origin/HEAD:
git remote add origin https://github.com/example/does-not-exist.git
git symbolic-ref -q --delete refs/remotes/origin/HEAD   # ensure unset
git update-ref refs/remotes/origin/main main            # a fetchable-looking origin/main
```

Copy the propagated family into the scratch repo's agent root for the harness under test,
or point the harness at this repo's `.github/agents/` while `cwd` is the scratch repo —
whichever your harness supports. **What must not happen is the orchestrator deriving a
base, correcting a base, or invoking `gh` against this repository.**

### Harnesses

All three must be available to complete section 9: Claude Code, OpenCode, and Codex.
Section 5 (Codex delegation) **requires Codex specifically** — the depth limit it tests
does not exist on the other two.

### Graph MCP

The `code-review-graph` MCP server must be available for the happy-path dry run
(sections 1–4) and **disabled** for section 8.

---

## Summary of Changes

Phase 03 rescopes a whole-phase review family into a branch-diff review family.

**Subtraction dominates.** Feature `01` gave `scripts/propagate_master_assets.py` the
ability to remove generated outputs whose source asset is gone — a prerequisite, not a
cleanup, since every later feature deletes or renames a source asset. Feature `02` then
deleted five phase-shaped evaluators. Feature `04` deleted the riskiest code in the
phase: the two-file transactional verdict write-back with unique-match ambiguity
detection and restore-on-second-write-failure, along with ledger reading, subphase
discovery, the `eval:` commit-message fallback, the artifact-inventory refusal gate, and
archive-before-overwrite.

**What ships:** the `05-pr-review` orchestrator plus seven evaluators —
`05a-baseline-worktree` (preflight; holds `execute` for `git worktree`, recorded
unclosable), `05b-change-narrator`, `05c-artifact-sweeper`, `05d-consistency-auditor`,
`05e-dependency-auditor`, `05f-test-health` (fan-out), and `05g-readiness-synthesizer`
(synthesis) — with `04e-diff-security-scan` delegated as the sixth concurrent evaluator.
Two skills (`pr-review-conventions`, `pr-review-report`) carry the shared contracts;
`worktree-baseline` is consumed unchanged.

Reports land at `dev/pr-review/<base-sha-short>-<UTC-timestamp>/`. **The key is derived
entirely from a SHA and a timestamp — no branch name reaches a filesystem path, so no
sanitizer exists to be wrong.** The verdict is advisory: the family writes no status line
to any document.

## Automated Test Coverage — what NOT to hand-test

**196 tests across eight files.** Skip all of it; it is genuinely covered:

- **Pruning** across all three roots, the repaired Codex skills guard, zero-deletions-on-unmodified-repo, `claude/agents/README.md` survival, deletion counts (`test_propagate_master_assets.py`, 38 tests)
- **Orchestrator contracts** — deleted-machinery absence, base fallback order, self-exclusion, report-root shape, fixture SHA reachability (`test_pr_review_orchestrator.py`, 42 tests)
- **Synthesis contracts** — no-status-line, P5-SEC-02 recorded open, posting consent settings, one-way output (`test_readiness_synthesis_agents.py`, 28 tests)
- **Evaluator rescope** — subphase-concept absence, tool grants, added-line attribution prohibition, graph NOT-RUN contract (`test_mechanical_evaluators.py` 21, `test_narrative_and_test_health_agents.py` 23)
- **Reconciliation** — roster of seven, dangling references in three pattern forms (slug, display name, and the unhyphenated prose form), counts recounted from disk, `.gitignore` both directions, propagation idempotency (`test_retirement_reconciliation.py`, 21 tests)
- **Skills + retirement** (`test_pr_review_skills.py` 18, `test_retired_evaluator_removal.py` 5)

**Suite state: `1 failed, 582 passed, 106 subtests`.**

The single failure is **PERF-01** (`test_ac9_propagated_guard_median_latency_is_below_50_ms`).
**It is not a Phase 03 regression and is out of scope for this plan:** at phase baseline
`ae9823a` it fails at median 54.54 ms; at HEAD 54.35 ms — statistically identical. It is
Phase 04's already-open release blocker. Do not scope QA to it, and **never relax the
budget to make it pass** — that was done once (PR #22, 50→90 ms) and reverted.

What the tests **cannot** reach, and this plan covers: an agent actually spawning, a
report actually appearing on disk, a prompt actually not appearing, and a network call
actually not being made.

---

## Manual QA Checklist

Organized by integration surface. Sections 1–4 share a single dry run — read them
together before starting, because you are collecting evidence for all four from one
execution.

### 1. Assembled Fixture Dry Run — THE HEADLINE ITEM

**Features:** all eight (the integration point)
**Covers ACs:** `08`/AC1, `04`/AC7 (actual creation), `04`/AC13, `05`/AC5, `06`/AC7, `07`/AC3
**Why manual:** No assertion over Markdown can observe a report being created. This run
is the first execution of the assembled family in the phase's history, and it is
required release evidence.

#### Happy Path

- [ ] **Record the pre-run state** — Run `ls dev/pr-review/ 2>/dev/null` and `git status --porcelain`. **Expected:** `dev/pr-review/` contains only `fixtures/`; the working tree is clean. A pre-existing run directory would confound the check.
- [ ] **Invoke the orchestrator against the pinned fixture** — With the `code-review-graph` MCP server available, invoke `05 PR - Review` with base `f5ab960e5697756538f94430327e2a68eb113822` and head `e6ff28a36293697aebf62155ae0048115c4aecca`. Answer the upfront block; confirm the suggested base or correct it to `f5ab960`. **Expected:** the run proceeds through preflight (`05a`), a six-way concurrent fan-out, and synthesis, reaching a written report without aborting.
- [ ] **Verify exactly one run directory was created** — `ls -d dev/pr-review/*/ | grep -v fixtures`. **Expected:** exactly one directory, named `f5ab960-<UTC-YYYYMMDDTHHMMSSZ>` — a short SHA and a timestamp. **No branch name (`feat/visual-verification-package`) appears in any path component.**
- [ ] **Verify all eight reports landed under that one directory** — `ls <run-dir>/`. **Expected:** `05a-baseline-worktree-report.md`, `05b-change-narrator-report.md`, `05c-artifact-sweeper-report.md`, `05d-consistency-auditor-report.md`, `05e-dependency-auditor-report.md`, `05f-test-health-report.md`, `05g-readiness-synthesizer-report.md`, `readiness-report.md`, **plus the `04e` diff-security report**. Each is a readable, regular, **non-empty** file. **A missing report is a failed coverage check, never a pass.**
- [ ] **Verify no evaluator is recorded `not-run`** — Read `<run-dir>/readiness-report.md`'s `Checks Not Run` section and `<run-dir>/evaluator-status.jsonl`. **Expected:** `Checks Not Run` is empty or absent; every evaluator has a status record with a non-null report path. **Per the recorded contract, a run with any required evaluator recorded `not-run` is below-GO evidence, not a passing run — re-run after fixing the wiring rather than accepting it.**
- [ ] **Verify each evaluator found its expected material** — Cross-check each report against the per-evaluator table in `dev/pr-review/fixtures/pinned-diff-range.md`. **Expected:** `05c` flags the `Debug.Log` artifacts in `Tests/CaptureRunner.cs` and `Editor/CreateConfigMenu.cs`; `05e` names the `com.unity.test-framework: 1.6.0` dependency in `package.json`; `05f` reports the four C# files added under `Tests/`; `05d` names Unity package conventions (`.meta` pairing, `.asmdef`, UPM layout); `04e` covers the new filesystem-writing C#. **An evaluator that reports "nothing to report" against this fixture has not worked — the fixture was chosen specifically so each finds something real.**
- [ ] **Verify the verdict is advisory and written nowhere else** — Run `git status --porcelain docs/phases/PROJECT_ROADMAP.md docs/phases/PHASE_03/PHASE_03_SUMMARY.md`. **Expected:** both unmodified. The report file is the only verdict; no status line is written to any document on any path.
- [ ] **Verify run output stays untracked** — `git status --porcelain dev/pr-review/`. **Expected:** no output — the run directory is gitignored while `dev/pr-review/fixtures/` remains tracked.

#### Edge Cases

- [ ] **Verify no misattribution of pre-existing findings** — For each finding in `05c-artifact-sweeper-report.md`, confirm the cited line is an **added** line in the range: `git diff f5ab960..e6ff28a -- <file> | grep '^+'`. **Expected:** every finding corresponds to a line the branch added. **A file the branch touched is not the same as a line the branch added** — reporting a file's pre-existing TODOs because the branch touched one line trains the reader to ignore the report.

### 2. Single-Interaction Contract

**Features:** `04`, `07`
**Covers ACs:** `08`/AC2, `04`/AC2, `07`/AC10
**Why manual:** A prompt is a runtime event. The agent body can promise one question
block while the run asks a second one. **This is the requirement most likely to erode
silently, one reasonable question at a time** — which is exactly why it is verified on
the assembled system rather than per feature.

- [ ] **Count the question blocks in the section-1 run** — Review the full transcript of the dry run from invocation to written report. **Expected:** **exactly one** question block, before any evaluator work, containing (a) the model-tier warning if the active model is not state of the art, (b) the suggested base with its derivation source stated (e.g. `base source: refs/remotes/origin/HEAD`), and (c) the PR-comment choice. After that block: **no further prompt of any kind** through to the written report.
- [ ] **Verify the base-confirmation prompt names the three failure cases** — Read the base-confirmation portion of the block. **Expected:** it names all three cases where the suggestion is actively wrong — a branch cut from another feature branch, a rebased branch, and a squash-merged base — and presents correction as first-class, not as an escape hatch.
- [ ] **Verify the *post automatically* option states its cost** — Read the PR-comment portion of the block. **Expected:** it plainly states that *post automatically* publishes an unread verdict to collaborators, and that a posted comment is not undone by reverting the agent.

### 3. Forced-Failure Run — Fail-Closed Semantics

**Features:** `04`, `07`
**Covers ACs:** `08`/AC3, `04`/AC10 (behavior), `04`/AC11, `07`/AC4
**Why manual:** Partial-failure semantics only exist at runtime. The most dangerous
failure mode in this family is an evaluator failure that silently reads as a clean check.

- [ ] **Force one fan-out evaluator to fail and re-run** — Repeat the section-1 run with one concurrent evaluator forced to fail (make `05e-dependency-auditor` unresolvable to the harness, or induce a bounded-wait timeout). **Expected:** the run **completes** and reaches a written `readiness-report.md`. The failure never aborts the run and **never becomes a passing result**.
- [ ] **Verify the missing check is named with its reason** — Read `readiness-report.md`'s `Checks Not Run` section. **Expected:** it names the evaluator, the specific check, and a **concrete reason** — not a generic "some checks did not run."
- [ ] **Verify the status record** — Read `<run-dir>/evaluator-status.jsonl`. **Expected:** a record for the failed evaluator naming evaluator, check, reason, and `report: null`.
- [ ] **Verify the verdict ceiling dropped** — Read the verdict line. **Expected:** **not `GO`.** Even with no other blocker found, the maximum outcome is "no blockers found, coverage incomplete." A `GO` verdict with a non-empty `Checks Not Run` is a release blocker for this phase.
- [ ] **Verify no new prompt appeared on the failure path** — Review the transcript. **Expected:** the evaluator failure introduced no question; the run reached the report unattended.
- [ ] **Force the preflight evaluator to fail** — Re-run with `05a-baseline-worktree` failing. **Expected:** the run **stops**. `05a` is preflight, not a fan-out evaluator — nothing can run before the baseline exists, so its failure is the one failure that must abort. This asymmetry against the previous check is the point.

### 4. Return Discipline

**Features:** `04`, `05`, `06`
**Covers ACs:** `08`/AC4, `04`/AC12, `05`/AC5, `06`/AC7
**Why manual:** Observed on the run. This contract is the phase's only defense against a
long-lived branch blowing out context.

- [ ] **Count every subagent return in the section-1 transcript** — For each of `05a`, `05b`, `05c`, `05d`, `05e`, `05f`, `05g`, and `04e`, count the lines of the payload returned to the orchestrator. **Expected:** **every return is ≤10 lines**, with full detail on disk in the corresponding report. `05b-change-narrator` is the one to watch — it holds the top model tier and is most exposed to a large diff.
- [ ] **Verify the orchestrator never read code or diffs** — Review the orchestrator's own transcript. **Expected:** it inspects path metadata and reads only structured reports under the run's report root. It never opens a source file or a diff.

### 5. Codex Runtime Delegation — NOT statically verifiable

**Features:** `06`
**Covers ACs:** `06`/AC5, `06`/AC5b
**Why manual:** **Codex `max_depth` defaults to 1, and a blocked spawn causes a silent
inline fallback** — the agent does the work itself and **reports success**.
`05f`→`test-analyst` and `05b`→per-directory readers both sit at **depth 2**. The agent
body will correctly say "delegate" while the runtime does not. **A static assertion over
the agent body cannot detect this**, and feature `06`'s record marks AC5b "Verification
deferred to manual QA" rather than Done. Recorded in
`.github/learnings/debugging-learnings.md:25–38`.

**Run this on Codex specifically.** The depth limit does not exist on Claude or OpenCode,
so a green run there proves nothing about this AC.

- [ ] **Verify `05f` actually spawns `test-analyst`** — On Codex with default settings, run `05f-test-health` through the orchestrator against the fixture range. **Inspect the runtime transcript for the child invocation — do not infer delegation from the prompt text.** **Expected:** a `test-analyst` child invocation appears in the transcript. **If the transcript shows `05f` doing coverage analysis inline while reporting success, AC5b has failed** — that is the silent fallback, and it looks exactly like a pass from the report alone.
- [ ] **Verify `05b` spawns per-directory readers when it chunks** — Same run, inspect `05b`'s transcript. **Expected:** either per-directory reader children appear, or `05b` chunks internally without claiming to have delegated. A claim of delegation with no child invocation is the failure.
- [ ] **Verify the depth requirement is surfaced, not silently absorbed** — Where a depth-2 spawn is blocked, check the report and status record. **Expected:** the blocked spawn is reported as a condition (NOT RUN with the depth reason), not absorbed into an inline result presented as delegated work.
- [ ] **Raise `max_depth` to 2 and re-run** — Re-run with the depth limit raised. **Expected:** the child invocations now appear in the transcript. This confirms the depth limit — rather than agent wiring — was the cause, and distinguishes a configuration finding from a code defect.

### 6. Live Base Derivation — scratch consumer repo ONLY

**Features:** `04`
**Covers ACs:** `04`/AC3, `04`/AC4, `04`/AC6
**Why manual:** Requires a real repository in states this one is not in and must not be
put into. **Never run this section against this repository.**

- [ ] **Verify the `origin/HEAD` → `origin/main` fallback** — In the scratch repo (with `refs/remotes/origin/HEAD` unset per Prerequisites), invoke the orchestrator and stop at the upfront block. **Expected:** the suggestion resolves to `origin/main` and the block **states the derivation source**, naming the fallback rather than presenting the guess as authoritative.
- [ ] **Verify the `origin/master` fallback** — Delete `refs/remotes/origin/main` and add `refs/remotes/origin/master` (`git update-ref refs/remotes/origin/master main && git update-ref -d refs/remotes/origin/main`); re-invoke. **Expected:** suggestion resolves to `origin/master`, source stated.
- [ ] **Verify the candidate-selection terminal fallback** — Remove both remote refs and re-invoke. **Expected:** the run **presents the candidate branches and requires a selection**. It does not guess, and it does not proceed without one.
- [ ] **Verify self-exclusion** — At each fallback above, inspect the candidate set offered. **Expected:** neither the current branch (`feature/scratch`) nor its own remote-tracking ref (`origin/feature/scratch`) appears as a suggestion. Both report HEAD as their own merge-base, so a naive nearest-merge-base heuristic always picks the branch under review — yielding a diff of nothing and a run that reviews an empty change while reporting success.
- [ ] **Verify a base correction propagates to every downstream evaluator** — Supply a base override that differs from the suggestion; let the run proceed to fan-out. **Expected:** `git merge-base HEAD <corrected-base>` is recomputed against the corrected base, and **every** evaluator receives the corrected merge-base. Confirm from each evaluator's report header, not from the orchestrator's claim. A single evaluator still holding the suggested base silently skews its findings.

### 7. Live PR Posting and Consent — scratch consumer repo ONLY

**Features:** `07`
**Covers ACs:** `07`/AC7, `07`/AC8
**Why manual:** "No network call was made" is not assertable over Markdown. The review
found the `gh pr comment` command guard **inert** (Issue #4) and the posting path's own
one-way clause **unguarded** (Issue #3, its most serious finding) — both repaired, but
the runtime behavior remains unverified.

- [ ] **Verify *never* makes no network call** — In the scratch repo, choose **never** in the upfront block and complete a run. Observe network activity (`sudo tcpdump -i any -n host api.github.com`, or a `gh` shim on `PATH` that logs and exits non-zero). **Expected:** the report is written locally and **no `gh` invocation and no network call occur on this path**.
- [ ] **Verify *ask when ready* writes the report BEFORE prompting** — Choose **ask once the report is written**. When the prompt appears, **before answering**, check `ls -la <run-dir>/readiness-report.md` from another shell. **Expected:** the report **already exists on disk** and is complete. This is the whole design: the prompt blocks nothing because the work is already done.
- [ ] **Verify the no-PR-open path is not an error** — With the scratch branch having no PR open, choose **post automatically** and complete the run. **Expected:** the condition is **reported alongside the local report**, the local report stands as the deliverable, the run does not fail, and **no new prompt appears**.
- [ ] **Verify unauthenticated `gh` is not an error** — Run with `GH_TOKEN=` and `GH_CONFIG_DIR=$(mktemp -d)` so `gh auth status` fails; choose **post automatically**. **Expected:** the condition is reported alongside the local report; the run completes; the verdict is unchanged. **A posting condition never changes the verdict and never becomes an evaluator failure.**
- [ ] **Verify output is one-way** — Review the transcript of any posting run. **Expected:** the agent never reads PR comments or any network-sourced text back in. Ingesting PR discussion is a prompt-injection surface and is out of scope for this phase.

### 8. Graph MCP Unavailable — degradation, not silent substitution

**Features:** `05`
**Covers ACs:** `05` graph-dependency contract, `05`/AC6
**Why manual:** Both `05c-artifact-sweeper` and `05d-consistency-auditor` carry
code-review-graph dependencies. Availability is a **dependency, not a fallback**: an
unavailable graph is a NOT RUN with a reason, **never a quiet grep that reports as though
the graph answered**.

- [ ] **Disable the graph and re-run `05c`** — In a disposable harness profile, disable the `code-review-graph` MCP server; run `05c-artifact-sweeper` through the orchestrator against the fixture. **Expected:** the graph-dependent check is recorded **NOT RUN with the concrete tool-unavailability reason**; the evaluator status records the missing check; the verdict ceiling drops below GO. **No clean sweep is fabricated, and no grep result is presented as a graph answer.**
- [ ] **Disable the graph and re-run `05d`** — Same, for `05d-consistency-auditor`. **Expected:** NOT RUN for the graph-derived canonical-form check — **but note the designed partial degradation**: drift evidenced directly from the diff is **still reported**, with its recommendation marked **not-derived**. `05d` degrades partially rather than going dark. Both halves must be present: the report is not empty, and the undelivered half is labelled.
- [ ] **Confirm `05e` is unaffected** — Run `05e-dependency-auditor` with the graph still disabled. **Expected:** it completes normally — it holds no graph dependency. If `05e` reports a graph-related NOT RUN, it has acquired a dependency its contract does not declare.

### 9. Cross-Harness Loading

**Features:** all eight
**Covers ACs:** cross-cutting; `03`/AC8, `04`/AC14, `05`/AC9, `06`/AC8, `07`/AC12 (runtime half)
**Why manual:** File parity is asserted by tests. That three different runtimes each
*load* the family is not.

- [ ] **Load the family on Claude Code** — Start a session and confirm all eight agents resolve: `05 PR - Review`, `05a`–`05g`. **Expected:** all 8 resolve and are invocable; no unresolved-tool-name error. (A command-scoped `tools:` entry is an *unresolved tool name* and makes Claude Code refuse to launch the subagent — which is why per-agent command scoping was deleted from this phase.)
- [ ] **Load the family on OpenCode** — Same check against `opencode/agents/`. **Expected:** all 8 load; no orphaned old-slug file shadows a renamed agent. OpenCode filenames are keyed on the **source slug** and orphan on every renumber, so this is where a missed prune surfaces.
- [ ] **Load the family on Codex** — Same check against `codex/agents/`. **Expected:** all 8 load from their generated TOML.
- [ ] **Verify the retired slash command is gone and its replacement is live** — On Claude, list available slash commands. **Expected:** no `phase-final-review` command; the `pr-review` command is present and points at `05 PR - Review`. **A surviving stale command is the sharpest dangling reference possible — it stays user-invocable while pointing at a deleted agent.**
- [ ] **Verify no retired agent is loadable on any harness** — On each harness, attempt to resolve `05c-qa-consolidator`, `05d-security-rollup`, `05e-ac-regression`, `05f-seam-analyzer`, `05i-learnings-harvester`. **Expected:** none resolves on any of the three. Note `05c`–`05f` are now **live slugs belonging to different agents** — confirm the *new* agent answers (`05c` is the artifact sweeper, `05d` the consistency auditor, `05e` the dependency auditor, `05f` test health), not a surviving old one.

---

## Cross-Cutting Concerns

### Performance

- [ ] **Observe the fan-out's context behavior on the fixture** — During the section-1 run, watch for context pressure across the six concurrent evaluators. **Expected:** the run completes without context exhaustion. The ≤10-line return contract and reports-on-disk pattern are the only defenses here, and 26 files / 1288 insertions is a deliberately modest proxy for a long-lived branch. **If context pressure appears at this size, it is a finding** — a real PR will be larger.

*PERF-01 is excluded by design — it is Phase 04's open blocker, unchanged by this phase (54.54 ms at baseline vs 54.35 ms at HEAD).*

### Security

- [ ] **Confirm P5-SEC-02 is recorded open, not closed by prose** — Read `05g-readiness-synthesizer.agent.md:77–85` (Trust Boundary) and `.github/learnings/cross-phase-decisions.md:88–108`. **Expected:** P5-SEC-02 is recorded **OPEN** with a named owner and routing to a future hook-/script-owning phase. It is **not** marked closed. This is correct and by design: the finding closes only by attaching a schema and deterministic reducer *in code*, and this phase ships agent Markdown. Mutation-verified — flipping the declaration to "closed" trips `test_p5_sec_02_is_recorded_open_in_the_synthesizer`. **Verify it is still open; do not attempt to close it.**
- [ ] **Verify read-only boundaries after every run above** — After each section's runs, check `git status --porcelain .github/ scripts/ tests/ docs/`. **Expected:** no modifications. Evaluators are read-only against source; only the run's report directory changes.
- [ ] **Verify the baseline worktree is cleaned up** — After the section-1 run, `git worktree list --porcelain`. **Expected:** no leftover worktree from `05a`, unless it was reused or dirty (in which case it is correctly left alone).

### Accessibility

Not applicable — this phase ships agent Markdown and one Python script. No UI surface exists.

---

## Notes

- **Update — 2026-07-16:** Document rewritten for the rescoped Phase 03 PR Review family. The prior body targeted the pre-rescope Phase Final Review family; feature `02` deleted all five of its evaluators and feature `08` retired its 13-file fixture root, making every prior checklist item unexecutable. See the banner at the top.

- **The single most important thing in this document is section 1.** Eight features passed review in isolation; nothing has run them together. Feature `08`'s own record puts it plainly: *"Do not read this feature's green suite as evidence the family runs."*

- **A green suite is not a baseline for this phase.** Feature `08` reconciled 561→581 passed (exactly +20, accounted for). But the tests assert contracts over Markdown bodies — they prove the family is *described* correctly. They were never capable of proving it runs.

- **Two review issues were repaired late and remain runtime-unverified** (`07` Issues #3 and #4): the posting path's one-way clause was unguarded, and the `gh pr comment` command — the mechanism AC7 rests on — could be deleted with its test green. Both fixed; section 7 is where their runtime behavior is confirmed for the first time.

- **Known open, deliberately:** `07` Issue #5 (`REPORT_PATH` asserted against raw `_body()`, reintroducing wrap-coupling) and `05` Issues #4–#6 (phrasing-specific proxy guards, order-sensitive tool-list equality, hardcoded `GRAPH_DEPENDENT_EVALUATORS`). All Low, all latent rather than live, all deferred to a cleanup pass. Not QA items.

- **Recorded but out of scope** (from `08`'s gaps): `04-phase-execute.agent.md:176` carries a `### Step 6: Phase Final Review` heading that actually refers to **Prod Code Review** — a name collision, not a dangling reference, in a file this phase does not own. `docs/CODEBASE_CONTEXT.md:87–88` carries two count claims ("6 orchestrators", "11 visible user-facing agents") that disagree with disk and **were already wrong at baseline** — this phase changed neither number and correctly declined to widen scope into them.

- **The fixture's one recorded weakness:** the pinned range has **zero deletions**, so it is a weaker proxy for a refactor- or removal-shaped PR. This was accepted deliberately — no bounded pair in this repo's history has a dependency change *and* a test delta *and* deletions — with roster coverage weighted above shape completeness. **The fix, if a removal-shaped dry run is ever needed, is a second fixture, not a resize of this one.**

- **`dev/pr-review/fixtures/` is tracked; `dev/pr-review/<sha>-<timestamp>/` is not.** Feature `04` AC10b un-ignored the fixture path (it would otherwise have been silently untracked, failing the dry run invisibly) and feature `08` removed the four dead `dev/phase-final-review/` rules. Both directions are asserted through real traversal — but if you find run output appearing in `git status`, stop and investigate rather than adding an ignore rule.
