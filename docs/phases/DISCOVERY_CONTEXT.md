# Discovery Context

Context gathered during project planning that is not derivable from the codebase alone. Read by
Phase - Refiner and Feature - Decomposer so the user does not have to re-supply it.

## Source of the Roadmap

The three phases originate from maintainer-reported friction, not from a code review. Each carries
a stated problem the maintainer experienced directly.

## Phase 01 — Reported Symptoms and Diagnosis

**Reported symptoms.** Agent-driven Unity testing behaves inconsistently: sometimes an agent opens
Unity Hub and runs tests itself, taking over the maintainer's mouse and making the machine unusable;
other times an agent refuses to run tests at all and asks the maintainer to run them by hand. The
maintainer's stated hypothesis was that Unity cannot generate `.meta` files unless the Editor is
opened by a human.

**Diagnosis reached during planning — the hypothesis is incorrect, and both symptoms are corpus
rules, not Unity limitations.**

1. **`.meta` files do not require a human-opened Editor.** A headless import
   (`Unity -batchmode -quit -projectPath <path> -logFile -`) imports the full asset database and
   writes every missing `.meta`. There is no GUI requirement.
2. **The mouse-hijack symptom is caused by `source_of_truth/skills/unity-development/SKILL.md`
   line 177**, which currently reads: *"`-batchmode` is optional. Omit it to run against the Editor
   UI; add it for headless runs."* Agents read "optional," omit it, and the Editor GUI launches.
3. **The refusal symptom is caused by the same file, line 181** — the Editor-lock rule instructs the
   agent to report `not-executed: editor lock` and ask the user whenever `Temp/UnityLockfile` exists
   or the Editor is open on the project.
4. **The correct fix for the lock is a second checkout, not closing the Editor.** Two Unity
   processes operating on two separate directories do not contend. A persistent shadow worktree with
   its own retained `Library/` cache lets the CLI run proceed while the maintainer's Editor stays
   open.

**Known cold-start constraint.** A freshly created Unity worktree has no `Library/` folder, so its
first headless run performs a full asset import — minutes, not seconds, on a real project. The
shadow worktree must therefore be **persistent and reused**, refreshed by checkout rather than
recreated per run. Any design that creates a throwaway worktree per test run reintroduces the delay
it was meant to remove.

## Decisions Made During Planning

Recorded as time-stamped intent. Verify against what shipped before relying on any of these.

| Decision | Choice | Rationale |
|---|---|---|
| Phase 01 delivery surface | Corpus rules plus copyable reference assets only | This repository contains no Unity project. Wiring CI into a real Unity repo would make the phase span two repositories and block on Unity license setup. |
| Unity test runner strategy | Local persistent shadow worktree first; CI deferred | Works today with no Unity license secret, no Docker images, and no runner maintenance. Removes the maintainer from the loop immediately. GameCI on GitHub-hosted runners remains a later, separate decision. |
| Phase 02 final-check enforcement | Advisory and opt-in. The refiner offers it; nothing blocks | **Supersedes an earlier decision in this table that made it a blocking gate on High-or-above rubric findings.** The maintainer clarified the intent: this is a scoped last look for anything the user and agent missed, not an adversarial gate. There is no rubric, no severity threshold, and no verdict. |
| Phase 02 final-check retry budget | None — one pass, no recheck | **Supersedes an earlier one-revise-and-recheck decision.** With nothing blocking, there is nothing to re-clear. Findings are reported once and the user chooses what to apply. |
| Phase 02 findings handling | Report verbatim, then offer to fold accepted findings into the document | Report-only was considered and rejected. A check that surfaces a real gap and then leaves the user to fix it by hand at the end of a long session gets skipped after a few uses — and a skipped check is worse than none, because it still appears to exist. |
| Phase 02 binding point | End of Phase - Refiner only, after the document is written and before the working branch opens | Scoped by maintainer directive. Project - Planner is deferred, not rejected — see `docs/learnings/cross-phase-decisions.md`. |
| Audit bookend scope | The manifest's modified files plus **one hop, uncapped**, of dependents, found by reference search — files that name a modified file by path, import it, or use the names it defines | Two full-codebase audits per phase plus a delta was judged too slow and expensive, and most of each report would be unchanged noise the delta must reconcile. Full-codebase remains an explicit opt-in. An import graph was rejected on evidence: this corpus is markdown agent and skill files that reference each other by name, and the repository's own `code-review-graph` index covers 30 source files, none of them the corpus. Multi-hop was rejected because the transitive closure over a corpus this cross-referential is most of the repository. |
| Audit bookend exclusions | Standalone documentation excluded from both audits. **Test files are in scope** under `Auditor - Code`'s existing reduced lens — broken assertions, wrong mocks, over-complex test code, pattern drift, duplicated setup | The exclusion directive was priced against a full test audit; the actual cost is four of fourteen categories over the touched files' tests. That slice catches a phase quietly loosening the tests guarding the code it changed, which the Step 2.5 wave gate cannot see because a loosened suite is still green. Accepted blind spot: a delta compares findings, not inventory, so an outright deleted test file is invisible to it — only the files-audited count in each report header hints at it. |
| Audit type selection | Code audit always; infra audit only when the manifest touches CI, Docker, IaC, or build config | Stated as an assumption during planning and accepted without objection. |
| Drift remediation policy | Auto-fix High-or-above drift attributed to the phase, then re-run the end audit once; report everything else | Bounded cost. Auto-fixing every severity risks a long tail of Low findings ballooning the phase through repeated re-audits. |
| Manifest role in the audits | Read input for both audits, supplying scope **and** intent | The execution manifest exists before any feature is implemented, which makes it a clean statement of what the phase intends to change, uncontaminated by what was actually built. |
| Audit bookend home | The audit-comparison sequence is **extracted out of `Audit - Delta` Phases 3–6b into a shared skill** that both `Audit - Delta` and `Phase - Execute` consume; `Phase - Execute` carries thin wiring | Delegation depth is one, so `Phase - Execute` cannot spawn `Audit - Delta` and must spawn the leaf auditors itself. Inlining the orchestration was rejected: the rules would then exist in two places and drift silently, with the bookend still running and no longer meaning anything. Writing a fresh skill alongside the existing one was rejected for the same reason — the sequence is already written once and should stay that way. A separate user-invocable orchestrator run by hand was rejected on the Phase 02 lesson: a check the user must remember gets skipped, and a skipped check is worse than none. The extraction moves only the mechanical contract; `Audit - Delta`'s user-facing confirmations stay in the agent, because `Phase - Execute` runs unattended. |
| Comparability rules ownership | `auditor-conventions` owns them; nothing else restates them | Its Multi-Target Audits section already carries the identical-prompt rule, per-run independence, snapshot labels, the `dev/[audit-name]/<snapshot-label>/` layout, the one-output-root rule, and an instruction telling an auditor to self-report if its prompt looks tailored to one side. Every auditor loads it directly. A second copy in an orchestration skill is the exact drift the bookend exists to prevent. |
| Audit bookend timing | **Both audits run at the end, back to back. The baseline side audits a `Baseline Worktree` at `<phase-baseline>`.** | **Supersedes the original roadmap wording, which said the first audit runs at phase start.** The baseline tree is a commit and does not change, so the two placements produce the same bytes. Running both at the end means they share session and model conditions — and the comparison's load-bearing claim is that the two reports differ because the *code* differs, so any condition drift between them lands in the delta as a phantom finding that attribution must spend probes clearing. It is also re-runnable: a start audit that failed cannot be redone once the phase has moved on. The cost is losing early warning about pre-existing problems, judged small because those findings surface in the end audit regardless. Caching a baseline report keyed on its sha was considered and rejected as a correctness trap for a saving realized only on phase re-runs. |
| Audit bookend default | On by default. The single opt-in question is asked **at Step 1**, stating the resolved file count and the audit types; the answer is recorded and nothing after Step 1 asks the user anything | Front-loading it is what keeps the rest of the run unattended, which is `Phase - Execute`'s whole shape — it spawns implementers for hours without checking in. Asking at the bookend itself means either a stall against an absent user or a reflexive decline after the cost is already sunk. A numeric file cap was considered as the cost bound and rejected: no defensible value exists, and a cap drops the most-referenced dependents, which are the ones most worth auditing. The informed decision at Step 1 replaces it. |
| Audit bookend skip semantics | A decline, a failed baseline worktree, or an unusable manifest each record a stated reason and force `all-approved: no` | Matches how the pipeline already handles expensive-or-unavailable evidence: the Step 2.5 test gate and Step 3 visual gate both record a stated skip reason and force `all-approved: no` rather than passing silently. Declining must never masquerade as a pass. Always-on was rejected because a one-feature documentation phase paying for two audits and a delta trains the maintainer to dread running the pipeline. |
| Post-remediation verification | Targeted verification pass over the files remediation touched, recorded as an addendum to the existing delta | **Supersedes "re-run the end audit once" in the row above.** Re-running the end audit honestly means re-running the delta and the attribution probes too, which doubles the bookend's cost in exactly the case where the phase is already running long. The gap — a fix breaking something outside its own files — is already covered more cheaply by the Step 2.5 wave test gate and the Step 6 pre-production gate. |
| Comparability of the verification pass | The targeted pass is **not** a new snapshot and is never fed to the delta | An audit run over a narrower scope is not comparable with the full end audit. The addendum must say so explicitly, or a later reader will treat two incomparable reports as a before/after. |

## Standing Constraint on the Manifest-as-Intent Design

The manifest is supplied to the auditors **for scope and intent only. Stated intent never excuses a
finding.** An auditor told what a phase meant to do will otherwise rationalize real findings away as
"intended." This constraint must survive into the spawn prompt itself, not live only in the phase
document.

## Phase 03 — how dependents are derived, and what it cannot see

**One hop of reference search, capped, with the cap declared.** For each file the manifest lists as
modified, find the files that name it by path, import it as a module, or use the names it defines.
Stop at one hop. Apply a file-count cap. Both the cap and what it excluded must reach the auditors'
Coverage and Limitations section, because that is where the delta is required to read them.

Two degenerate cases are handled rather than assumed away. A modified file nothing references yields
no dependents: fall back to auditing the modified files alone and say so. A widely-referenced file
blows the cap: state the cap and what it excluded. Narrower evidence is recoverable; silently-wrong
scope is not.

## Context Not Gathered

- No external URLs, specifications, or design documents were supplied.
- No web research was performed. The Unity CLI behavior above is asserted from working knowledge and
  should be verified empirically during Phase 01 execution against the actual Unity version in use.
- No additional repositories or monorepo packages were referenced. All three phases are
  single-repository work inside `github-agents-source-of-truth`.
