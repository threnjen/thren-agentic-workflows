# Phase 3: Phase Execute Audit Bookend

**Status**: Planned
**Depends on**: None at the code level. Ordered after Phase 01 and Phase 02 in the roadmap because it is executed *by* the pipeline those phases improve.
**Estimated complexity**: Large
**Cross-references**: None — single-repository phase

## What's New

When a phase finishes building, you currently know that the code it changed was reviewed, that its
tests passed, and that the diff carried no new security problems. You do not know whether the phase
made the surrounding codebase worse — because everything that looks at the work is scoped to the
diff, and degradation shows up outside it.

After this phase, `Phase - Execute` answers that question before it reports the phase complete. It
audits the codebase as it stood when the phase began, audits it again as it stands now, compares the
two, and checks each difference against both trees to establish whether the phase actually caused it
or whether it was already there. Anything serious the phase caused gets fixed automatically and
verified. Everything else is reported.

The check is on by default. You can decline it, and the phase still completes — but the final review
then says plainly that no degradation evidence exists, rather than letting a skip look like a pass.

## Objective

Give every phase execution evidence about whether it degraded the codebase outside the lines it
changed, and repair the serious degradation it caused, so "the phase is done" stops meaning "the
diff looked fine."

## Scope

### In Scope

- **A new skill owning the audit-comparison sequence, extracted from `Audit - Delta`.** The sequence
  already exists, written once, in `source_of_truth/agents/delta-auditor.agent.md` Phases 3 through
  6b: resolve the output root, materialize ref targets through `Baseline Worktree`, run the audit
  matrix, gate before spawning the delta, settle attribution in disjoint batches and prove the counts
  sum. That content moves into the skill, and `Audit - Delta` is rewired to consume it.
- **The extraction splits mechanism from conversation.** `Audit - Delta` is interactive: it states
  the audit matrix back to the user before spawning, offers the delta rather than assuming it, and
  asks before fix research. `Phase - Execute` runs unattended. Only the mechanical contract moves to
  the skill; every user-facing confirmation stays behind in `Audit - Delta`. An extraction that drags
  the confirmations along makes the skill unusable by its second caller, which is the point of
  extracting it.
- **The skill does not own the comparability rules.** They already live in
  `source_of_truth/skills/auditor-conventions/SKILL.md` under Multi-Target Audits, which every
  auditor loads for itself: identical prompt text varying only target root, snapshot label, and
  output path; no auditor reading another target's tree or another run's report; snapshot labels;
  the artifact layout; and the instruction telling an auditor to report in its own Coverage and
  Limitations section if its prompt appears tailored to one side. The skill cites that section and
  does not restate it.
- **Thin wiring in `source_of_truth/agents/04-phase-execute.agent.md`.** A new step between the
  existing Step 5 (Diff Security Review) and Step 6 (Phase Final Review) that loads the skill,
  supplies the phase-specific inputs, and feeds the outcome into `all-approved`. The wiring supplies
  inputs and records outcomes; it does not restate the sequence.
- **Frontmatter additions.** `Phase - Execute` gains `Auditor - Code`, `Auditor - Infra`,
  `Auditor - Delta`, `Auditor - Attribution`, and `Baseline Worktree` in its `agents:` list. Every
  one already exists and is a leaf, so delegation depth stays at one. No new subagent is created by
  this phase.
- **Both audits run at the end, back to back.** The baseline side audits a `Baseline Worktree`
  materialized at `<phase-baseline>`; the current side audits the working checkout. The worktree is
  released through `Baseline Worktree`'s own cleanup handshake once the delta and attribution are
  done, and never before.
- **Audit scope: touched modules plus one hop of dependents.** The starting set is the manifest's
  `key files modified` at `dev/feature/[phase-name]-execution-manifest.md`. Dependents are found by
  reference search — files that name a modified file by path, import it as a module, or use the
  names it defines. **One hop, no cap.** The bound on cost is the Step 1 announcement: the resolved
  file count is shown before anything runs, and an oversized scope is declined there by a person
  rather than silently truncated by a number nobody can justify. An import graph is not used: this
  corpus is markdown agent and skill files that reference each other by name, which a reference
  search finds and an import graph cannot.
- **What counts as source here.** Everything under `source_of_truth/` is this corpus's source code
  regardless of extension — an agent definition is executable instruction text, not prose about
  something else. Tests under `tests/` are source. "Standalone documentation" means `docs/`, `README`,
  and equivalent prose *about* the system, and that is what is excluded. `Auditor - Infra` declares
  Documentation an in-scope category with its own audit policy; the bookend's spawn prompt overrides
  it for this run and must say so explicitly, because a scope narrower than an auditor's declared
  domain is otherwise indistinguishable from an auditor that skipped work.
- **Tests are in scope under the reduced lens.** `Auditor - Code` already audits test files against
  four of its fourteen categories — Category 2 (errors and defects, which covers broken assertions
  and wrong mock setup), Category 5 (readability, for deeply nested or over-complex test code),
  Category 8 (consistency, for tests written against a different pattern than the code they cover),
  and Category 9 (DRY, for duplicated setup). Four, and no more. That slice is what catches a phase
  quietly loosening the tests that guard the code it changed, which the Step 2.5 wave gate cannot see
  because a loosened suite is still green.
- **Code audit always; infra audit only when the manifest touches CI, Docker, IaC, or build
  configuration.**
- **The manifest is supplied to both auditors for scope and intent — and the spawn prompt itself
  states that stated intent never excuses a finding.** An auditor told what a phase meant to do will
  otherwise rationalize real findings away as intended. This constraint has to appear in the rendered
  prompt, not only in this document.
- **Artifacts follow `auditor-conventions`, not the phase pipeline.** Per-snapshot reports go to
  `dev/[audit-name]/<snapshot-label>/`, the delta and its open-items queue to
  `dev/[audit-name]/[audit-name]-delta-<baseline-label>-to-<current-label>*.md`, and **everything is
  written under the newer side** — the working checkout. The baseline worktree receives no files,
  including its own report, because it is removed at the end of the run and would take them with it.
  `[audit-name]` derives from the phase name; the two labels carry short shas so the comparison is
  reproducible after the branch moves. This is the one `Phase - Execute` output that does not live
  under `docs/phases/[phase-name]/`.
- **The delta gate.** Do not spawn `Auditor - Delta` unless both sides produced full findings
  reports that state their own totals. A delta over a partial report produces confident, wrong
  arithmetic.
- **Attribution against both trees.** Every provisional finding — a current-side finding with no
  baseline counterpart — is probed by `Auditor - Attribution` before anything is called a
  regression. Batched by subsystem, with disjoint item sets whose counts sum to the delta's
  unattributed total.
- **Bounded auto-remediation.** High-or-above findings *attributed to the phase* are fixed by
  `Feature - Implementer`, once. The spawn matches the shape Step 2.5 and Step 3 already use when
  they re-spawn the implementer from prose for a single bounded retry; it does not invent a third
  shape. Everything else is reported, not fixed.
- **A targeted verification pass** over the files remediation touched, confirming each auto-fixed
  finding is closed. It is recorded as an addendum to the existing delta and **explicitly marked as
  not comparable with the full end audit**, because it ran over a narrower scope. It is never fed
  to the delta as a new snapshot.
- **The opt-in decision is taken at Step 1, not at the bookend.** `Phase - Execute` resolves the
  audit scope from the manifest during Step 1's bundle validation — the manifest is already read
  there, and the reference search needs nothing the wave loop produces — then announces the bookend,
  the resolved file count, and which audit types will run, and asks once. The answer is recorded and
  the rest of the run is unattended, which is the only arrangement consistent with an orchestrator
  that spawns implementers for hours without checking in. Asking at the end, after the cost is
  already sunk and the person has stopped watching, produces either a stall or a reflexive decline.
- **The opt-out path.** On a decline at Step 1, on a failure to materialize the baseline worktree, or
  on an unusable manifest, the bookend records a stated reason, sets `all-approved: no`, and the
  phase continues — the same shape the Step 2.5 test gate and Step 3 visual gate already use for
  missing evidence. Full-codebase auditing is offered as an alternative answer to the same Step 1
  question and recorded the same way; it is never inferred.
- **Structural guards** in `tests/`, each demonstrated to fail when its target is deleted or negated,
  per the `guard-integrity` skill.

### Out of Scope

- **Any new subagent.** Every agent this phase needs already exists.
- **Full-codebase auditing by default.** Scope is manifest-derived. Full-codebase remains an
  explicit opt-in, not the default.
- **Auditing standalone documentation files.**
- **Multi-hop dependents.** One hop, capped. A transitive closure over a corpus this
  cross-referential is most of the repository, which is the full-codebase audit this phase exists to
  avoid.
- **Security and refactor audit types in the bookend.** Code always, infra conditionally. The
  existing Step 5 diff security scan is unchanged and is not replaced by this phase.
- **Cross-type deltas.** A code delta and an infra delta are separate documents with separate
  counts, and are never reconciled into one.
- **Changing what `Audit - Delta` does.** Its behavior is preserved exactly; only the location of its
  Phases 3–6b text changes. Its interactive confirmations, its Phase 1 and 2 type and target
  selection, and its Phases 7 and 8 remediation flow stay in the agent.
- **Fixing anything below High**, and fixing anything not attributed to the phase. Pre-existing
  findings the baseline auditor did not raise are real work, but they are not this phase's damage.
- **Remediating on a baseline checkout or worktree.** Code is written to the working checkout only.

## Key Deliverables

| # | Deliverable | Description | Likely Features |
|---|-------------|-------------|-----------------|
| 1 | Audit-comparison skill | The sequence extracted from `Audit - Delta` Phases 3–6b: output-root resolution, ref-target materialization, the audit matrix, the delta gate, attribution batching and the sum check, worktree release ordering. Cites `auditor-conventions` for comparability and `audit-delta-report` for document contracts; restates neither | The contract |
| 2 | `Audit - Delta` rewire | Phases 3–6b replaced by a load of the skill plus the interactive confirmations that stay behind. Behavior unchanged | The extraction |
| 3 | `Phase - Execute` wiring | New step between Step 5 and Step 6; frontmatter `agents:` additions; scope derivation from the manifest; remediation and the verification addendum; `all-approved` integration; the outcome passed into the Step 6 Prod Code Review prompt | The wiring |
| 4 | Structural guards | Topology, workflow-ordering, single-home, and non-vacuity tests across all three | The guards |

## Technical Context

- **`source_of_truth/skills/auditor-conventions/SKILL.md`** already owns Multi-Target Audits: the
  identical-prompt rule, per-run independence, snapshot labels, the `dev/[audit-name]/<label>/`
  layout, the one-output-root rule, and the requirement that each auditor state its target root,
  output root, and the counts that scale it. Every auditor loads this for itself. Read it before
  writing anything into the new skill, and reference rather than copy.
- **`source_of_truth/agents/delta-auditor.agent.md`** (169 lines) is the source of the extraction.
  Phase 3 resolves the output root, Phase 4 materializes ref targets through `Baseline Worktree` and
  holds the "tell it the run is complete only after the delta is done" rule, Phase 5 runs the matrix
  and carries the per-auditor spawn prompt, Phase 6 holds the delta gate and the "do not present a
  regression count yet" discipline, Phase 6b holds attribution batching, the disjoint-set rule, and
  the sum check. Phases 1, 2, 7, and 8 stay put.
- **`source_of_truth/agents/04-phase-execute.agent.md`** (222 lines) is the file being extended. Its
  Step 2.5 wave test gate and Step 3 visual verification gate are the precedents for two things: an
  expensive gate with a stated-reason skip path that forces `all-approved: no`, and a bounded
  single-retry re-spawn of `Feature - Implementer` from a prose prompt rather than a plan. The
  bookend matches both rather than inventing new shapes. Its Step 1 already reads the manifest and
  extracts `key files modified`, which is everything scope derivation needs, so the ask lands there
  with no extra read. Note the one deliberate departure: Step 1 currently states "Do not ask the user
  whether QA should be generated." QA is cheap and wanted every time, so asking is pure friction. The
  bookend's cost varies by an order of magnitude with the phase's blast radius, which is exactly the
  condition that makes a single up-front question worth its interruption.
- **`source_of_truth/skills/audit-delta-report/SKILL.md`** (594 lines) is the delta and attribution
  document contract, including section 2A (the probe) and section 2D (the attribution write
  contract). Both the skill and the agent reference it; neither restates it.
- **`source_of_truth/agents/05a-baseline-worktree.agent.md`** already creates and reuses a detached
  worktree at a caller-supplied commit and returns its absolute path, with `worktree-baseline`
  holding the procedure and the cleanup handshake. This is wiring, not new machinery.
- **`source_of_truth/agents/04b-feature-implementer.agent.md`** is contractually plan-driven and
  refuses vague requests. The existing prose re-spawns at Step 2.5 and Step 3 are the established
  exception; the remediation spawn follows them.
- **`<phase-baseline>`** is bound by the path-token instruction as
  `git merge-base HEAD <default-branch>`. Step 5 already resolves it for the diff security scan, so
  the bookend uses the same resolution rather than a second one.
- **Delegation depth is one.** `Phase - Execute` is a user-invocable root and may spawn leaves.
  `Audit - Delta` is an orchestrator and is therefore unspawnable from here. This constraint is the
  reason the phase exists in this shape at all.
- **Corpus authoring register.** The skill is machine-facing and read at runtime by an agent paying
  for every token: dense but brief. `source_of_truth/` is the only authoring surface; nothing under
  `ports/` or `.github/` is hand-edited, and no agent runs `scripts/propagate_master_assets.py`.

## Dependencies & Risks

- **Dependency**: an execution manifest at `dev/feature/[phase-name]-execution-manifest.md` with a
  usable `key files modified` set. Step 1 already validates the manifest's existence, so the bookend
  inherits that guarantee — but not the quality of the file list inside it.
- **Risk — the extraction changes `Audit - Delta`'s behavior while claiming not to.** Moving text
  between files is where wording quietly shifts, and `Audit - Delta` is a working orchestrator with
  no test coverage over its prose. *Mitigation*: treat feature 2 as a move, not a rewrite; the
  guards must assert the moved rules are present in exactly one place, and the interactive
  confirmations must be enumerated before the move rather than identified during it.
- **Risk — the reference search returns nothing, or nearly everything.** A modified file nothing
  names yields no dependents; a file referenced by most of the corpus resolves to most of the corpus.
  *Mitigation*: an empty result falls back to auditing the modified files alone and says so, in
  Coverage and Limitations where the delta is required to read it. An oversized result is surfaced
  as a file count at the Step 1 ask and declined or accepted there. A numeric cap was considered and
  rejected: no defensible value exists, and a cap silently drops the dependents most worth auditing —
  the ones with the most references.
- **Risk — the byte-identical-prompt rule cannot be proven by a structural test.** A guard can prove
  the prompt template exists and that the varying fields are the only parameterized ones. It cannot
  prove the two rendered prompts matched at runtime. The auditors' own self-report requirement in
  `auditor-conventions` is a partial runtime backstop, not a proof. This is the same shape as Phase
  02's blindness rule. *Mitigation*: treat the guard as necessary and insufficient, and exercise the
  path manually on a real phase at least once before calling this phase complete.
- **Risk — cost lands at the worst moment.** The bookend runs at the end of an already long phase
  execution. If it feels punitive, it gets declined reflexively and the phase's value evaporates.
  *Mitigation*: the one-hop bound, the documentation exclusion, the reduced test lens, and the
  targeted verification pass are all cost controls, and the Step 1 ask states the resolved file count
  so the decision is informed rather than defensive — and is taken before the phase has consumed
  anything, when declining is a judgment rather than a flinch.
- **Risk — worktree cleanup.** A baseline worktree released before attribution finishes takes the
  tree that attribution needs to probe. *Mitigation*: the release handshake belongs in the skill,
  after attribution returns, and is worth a dedicated guard.
- **Risk — the verification addendum gets read as a snapshot.** A narrower-scope report sitting next
  to a full one invites a false before/after reading. *Mitigation*: the incomparability statement is
  part of the addendum's required content, not a convention.
- **Risk — attribution batch arithmetic.** Batches must be disjoint and must sum to the delta's
  unattributed total; two agents assigned the same identifier both write the same documents.
  *Mitigation*: the sum check moves into the skill intact and is guarded there.
- **Known blind spot, accepted.** A delta compares findings, not inventory, so an outright deleted
  test file produces no finding on either side and the delta cannot see it. The only signal is the
  files-audited count each auditor states in its report header, which is coarse. Building an
  inventory comparison was considered and rejected as new machinery whose counts cannot distinguish
  a legitimate consolidation from gutting.

## Success Criteria

- [ ] The audit-comparison skill exists, parses, and is referenced by both `Audit - Delta` and
      `Phase - Execute`.
- [ ] The extracted sequence text lives in exactly one file. Neither consumer restates the
      output-root rule, the ref-target materialization procedure, the delta gate, the attribution
      batching rule, or the sum check.
- [ ] The skill contains no user-facing confirmation, question, or offer; `Audit - Delta` retains all
      of its.
- [ ] `Audit - Delta`'s behavior is unchanged: same phases, same order, same prompts, same
      confirmations, same artifact paths.
- [ ] The skill cites `auditor-conventions` for comparability and `audit-delta-report` for document
      contracts, and restates neither.
- [ ] `Phase - Execute`'s `agents:` frontmatter lists `Auditor - Code`, `Auditor - Infra`,
      `Auditor - Delta`, `Auditor - Attribution`, and `Baseline Worktree`.
- [ ] `Phase - Execute` spawns no orchestrator; every agent it spawns for the bookend is a leaf.
- [ ] The two audit spawn prompts are rendered from one template whose only varying fields are
      target root, snapshot label, and output directory.
- [ ] The spawn prompt text states that the manifest supplies scope and intent, and that stated
      intent never excuses a finding.
- [ ] Scope derivation takes the manifest's modified files plus exactly one hop of reference-search
      dependents, with no numeric cap, and an empty dependents result falls back to modified files
      alone and states that in Coverage and Limitations.
- [ ] The bookend question is asked once, at Step 1, and states the resolved file count and the audit
      types that will run. No step after Step 1 asks the user anything.
- [ ] The Step 1 answer is recorded as one of: run scoped, run full-codebase, or declined with a
      stated reason. Full-codebase is never inferred from anything.
- [ ] Everything under `source_of_truth/` and `tests/` is treated as source; `docs/`-style prose is
      excluded. The spawn prompt states explicitly that it overrides `Auditor - Infra`'s declared
      Documentation category for this run.
- [ ] Test files are audited under `Auditor - Code`'s existing categories 2, 5, 8, and 9 only, with
      no category added and none of the other ten applied.
- [ ] The infra audit runs when and only when the manifest touches CI, Docker, IaC, or build
      configuration, and the reason for running or skipping it is recorded.
- [ ] A code delta and an infra delta are separate documents with separate counts; no step
      reconciles them into one.
- [ ] The baseline audit targets a worktree at `<phase-baseline>`, and no step audits the baseline
      before the wave loop completes.
- [ ] Every bookend artifact is written under the working checkout at `dev/[audit-name]/`; nothing is
      written into the baseline worktree.
- [ ] The baseline worktree is released only after attribution returns.
- [ ] The delta is not spawned unless both reports exist, are full findings reports, and state their
      own totals.
- [ ] No finding is reported as a regression before attribution has settled it.
- [ ] Attribution batches are disjoint and their item counts sum to the delta's unattributed total.
- [ ] Auto-remediation fires only for High-or-above findings attributed to the phase, at most once,
      using the Step 2.5/Step 3 re-spawn shape.
- [ ] The post-remediation verification pass is scoped to remediation-touched files, is recorded as
      an addendum, states that it is not comparable with the full end audit, and is never supplied
      to the delta as a snapshot.
- [ ] Declining the bookend, a failed worktree materialization, and an unusable manifest each record
      a stated reason, set `all-approved: no`, and allow the phase to reach Step 6.
- [ ] The bookend outcome reaches the Step 6 Prod Code Review prompt as evidence.
- [ ] Every new test is demonstrated to fail when its target is deleted or negated, per the
      `guard-integrity` skill.
- [ ] No file under `ports/` or `.github/` is hand-edited.

## QA Considerations

- **No Unity visual gate.** This repository is not a Unity project and this phase has no visual
  acceptance criteria.
- **Automated evidence.** Structural guards over the skill, both consumers, the frontmatter, the
  ordering, the single-home assertion, and the skip branches. Expect the repository-wide suite to
  retain its recorded baseline failures, and generated-output synchronization to remain pending
  maintainer propagation — neither is caused by this phase.
- **Manual evidence is required before this phase can be called complete.** Three things cannot be
  proven structurally: that the two rendered spawn prompts actually matched at runtime, that the
  worktree survived until attribution finished, and that `Audit - Delta` still behaves identically
  after the extraction. The first two need one real end-to-end exercise on an actual phase with the
  rendered prompts captured and compared; the third needs one `Audit - Delta` run.
- **No API or user-visible behavior change** outside the pipeline itself, so no frontend
  coordination is needed.

## Notes for Feature - Decomposer

Suggested split into four features, in this order:

1. **The audit-comparison skill.** Write it first; it defines the vocabulary the rest consume. Build
   it by lifting `Audit - Delta` Phases 3–6b, not by composing fresh prose — a rewrite loses rules
   that read as boilerplate and are load-bearing: the "only after the delta is done" worktree
   release, the "do not present a regression count yet" discipline, the disjoint-item-set rule, and
   the sum check. Enumerate `Audit - Delta`'s interactive confirmations before moving anything, and
   leave every one of them behind.
2. **The `Audit - Delta` rewire.** A move, not a redesign. Its acceptance criterion is behavioral
   identity, so write the criteria as "unchanged" statements rather than as new capabilities.
3. **The `Phase - Execute` wiring.** Consumes the skill by reference, never by copying. One new step
   plus frontmatter, scope derivation, remediation, the verification addendum, and `all-approved`
   integration — the existing steps keep their content. If the wiring starts restating the sequence,
   the boundary has been crossed.
4. **The guards.** Land last, assert across all three.

Features 1 and 2 are tightly coupled and must not be scheduled in parallel with each other; feature 3
depends only on the skill's finished shape.

Two boundaries to keep explicit rather than discover during implementation. The first is between
feature 1 and feature 3: the rendered spawn prompt — feature 1 defines what it must and must not
contain, feature 3 renders it. The second is between the skill and `auditor-conventions`: the skill
owns sequencing, `auditor-conventions` owns comparability, and a rule appearing in both is a defect
in feature 1 regardless of how correct it reads.
