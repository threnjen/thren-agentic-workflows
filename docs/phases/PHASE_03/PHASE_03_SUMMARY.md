# Phase 3: PR Review Agent Family

**Status**: Partially implemented — rescoped; the readiness/report core is built, the diff-scoped orchestration is re-planned
**Depends on**: None (independent of the hook phases; consumes existing pipeline assets only)
**Estimated complexity**: Medium
**Cross-references**: `docs/phases/PHASE_03/PHASE_03_DISCOVERY_CONTEXT.md`, `docs/phases/DISCOVERY_CONTEXT.md` (§ "Phase 03 Design Notes"), `.github/learnings/cross-phase-decisions.md` (§ "PR-Review Rescope"), `docs/phases/PHASE_04/PHASE_04_SUMMARY.md` (hook remediation phase; hands this phase its `execute`-grant and P5-SEC-02 findings)

> **Agent numbers are pipeline positions, not phase numbers.** The `05-pr-review`
> orchestrator and its `05a`–`05g` evaluators sit at position 5 of the working
> pipeline (`01-project-planner` → `02-phase-refiner` → `03-feature-decomposer`
> → `04-phase-execute` → `05-pr-review`). That this phase is numbered 03 and its
> agents are numbered 05 is correct and intentional. See the mapping table in
> `docs/phases/PROJECT_ROADMAP.md`.

## What's New

When a branch is ready to open a pull request against its base, nothing in this
project looks at the whole branch as one unit. Individual features got reviewed
as they landed, but nothing re-reads the accumulated diff, asks whether the
branch drifted from its own conventions, notices scaffolding left behind three
commits ago, or answers "is this branch actually ready to merge?"

This phase adds a **PR Review** flow: one orchestrator you invoke when a branch
is PR-ready, which asks you exactly one question up front, fans out to seven
specialist evaluators over the diff between the branch and its base, and hands
back a single severity-ordered go/no-go readiness report — optionally posted to
the pull request.

## Objective

Build the `05-pr-review` orchestrator, its `05a`–`05g` evaluator subagents, and
the supporting skills so that the diff between a branch and its base can be
evaluated end-to-end — change narrative, artifact sweep, consistency,
dependencies, test health, diff-scoped security, and readiness synthesis — with
strict context discipline, a single upfront interaction, and no unattended
blocking.

## Scope

### In Scope

- **Propagation pruning**: `scripts/propagate_master_assets.py` removes generated
  outputs whose source asset no longer exists. This is a prerequisite for the
  retirement and renaming this phase performs, not an incidental cleanup — without
  it, every deleted or renamed agent, skill, and command leaves a live artifact
  behind in the generated roots.
- **Orchestrator**: `.github/agents/05-pr-review.agent.md` — numbered-orchestrator
  house style (matching `04-phase-execute` + lettered subagents). Never reads
  code or diffs; consumes only structured reports subagents write to the run's
  report root; each subagent returns a ≤10-line summary.
- **Single upfront interaction**: every question the run could ask is asked once,
  before any evaluator work, in one block:
  1. the model-tier warning, if the active model is not state of the art;
  2. the suggested base branch and its derivation, for confirmation or correction;
  3. the PR-comment choice — post automatically, ask once the report is written,
     or never.

  After that block the run proceeds to a written report without further prompts.
  No evaluator, failure path, or synthesis step may introduce a new question.
- **Base-branch suggestion**: a branch's base is not recoverable from git. A ref
  is only a SHA and carries no parentage; the reflog records `Created from HEAD`
  — the SHA, never the branch name — and is local-only and gc-pruned. The base is
  therefore **suggested and confirmed**, never determined. Suggestion order:
  `refs/remotes/origin/HEAD` → `origin/main` → `origin/master` → present the
  candidate branches and require a selection. The suggester must exclude the
  current branch and its own remote-tracking ref: both report HEAD as their own
  merge-base, so a naive nearest-merge-base heuristic always picks the branch
  under review. Once the base is confirmed, `git merge-base HEAD <base>` fixes
  the diff origin for every downstream evaluator.
- **Cases where the suggestion is wrong, and must be correctable**: a branch cut
  from another feature branch rather than the default branch; a rebased branch,
  whose merge-base no longer reflects where work began; a base that was
  squash-merged, leaving no shared commit.
- **Artifact posture**: pipeline artifacts (implementation records, QA docs,
  security reports) are **optional enrichment, not a precondition**. When present,
  evaluators use them as additional evidence. When absent, the run proceeds on the
  diff alone and the readiness report states which evidence was unavailable. The
  agent reviews any branch against any base, not only pipeline-produced branches.
  This is the boundary with `prod-code-review`, which remains the document-driven
  gate over a phase's feature set.
- **Report root**: `dev/pr-review/<base-sha-short>-<UTC-YYYYMMDDTHHMMSSZ>/`. The
  key is derived entirely from a SHA and a timestamp — no branch name reaches a
  filesystem path, so no sanitizer exists to be wrong. Every run owns its own
  directory; there is no overwrite and therefore no archiving step.
- **Partial-failure semantics**: if an evaluator fails mid-run (crash,
  unavailable dependency, worktree error, bounded-wait timeout), the run completes
  with the remaining evaluators; the readiness report enumerates exactly which
  checks did not run and why; and the verdict can never be GO while any check is
  missing — the ceiling is "no blockers found, coverage incomplete."
- **Verdict**: the readiness report is the verdict. It carries `GO`,
  `GO WITH CONDITIONS`, or `NO-GO` with a severity-ordered blocking list. The
  agent writes no status lines in `PROJECT_ROADMAP.md` or any phase summary.
  Enforcement is advisory; nothing is mechanically blocked.
- **PR comment output** (opt-in, chosen in the upfront block): post the readiness
  report to the pull request via `gh`. When the choice is *ask once the report is
  written*, the run completes unattended and prompts only when a finished report
  exists to review — the work is already on disk, so this prompt blocks nothing.
  When no pull request exists for the branch yet, posting is not an error: report
  the condition and leave the local report as the deliverable.
- **`execute` posture**: an agent either holds `execute` or it does not. Per-agent
  command scoping is not expressible in the harnesses this project propagates to
  (see Technical Context), so the only narrowing available is **removal**.
  Accordingly: `execute` is dropped from every evaluator that does not require a
  shell command with no non-shell equivalent, is never added to an evaluator that
  lacks it today, and is **declared with a named justification** where it is
  genuinely required — `git worktree` for `05a`, and `git` base derivation plus
  `gh` posting for the orchestrator. A grant retained with a comment explaining why
  it is acceptable is not a justification; the justification must name the command.
- **Evaluator subagents** (`05a`–`05g`, all read-only against source):
  - `05a-baseline-worktree` — check out the confirmed merge-base commit in a git
    worktree; return the path. Already accepts a caller-specified baseline commit.
  - `05b-change-narrator` — narrative of the branch diff baseline→HEAD, with churn
    hotspots and an account of what the branch is trying to do; chunks diffs
    internally, may spawn per-directory readers.
  - `05c-artifact-sweeper` — debug statements, TODOs/FIXMEs, temp feature flags,
    commented-out and dead code introduced since the base. Mechanical.
  - `05d-consistency-auditor` — convention drift between the branch and the
    surrounding codebase (naming, error handling, patterns), with recommended
    canonical forms. Mechanical.
  - `05e-dependency-auditor` — dependencies added by the branch: licenses,
    vulnerabilities, competing or duplicate libraries. Mechanical; its contract
    permits an explicitly offline read-only audit command.
  - `05f-test-health` — coverage delta base→HEAD, test redundancy, flake
    candidates; delegates to the existing `test-analyst` agent.
  - `05g-readiness-synthesizer` — reads all reports (never code); produces the
    go/no-go readiness report with a severity-ordered blocking list and a
    `Checks Not Run` section. Extends `prod-code-review` conventions rather than
    duplicating them.
- **Roster positions are not one flat fan-out**: `05a` runs at preflight and its
  failure stops the run; `05b`–`05f` plus `04e-diff-security-scan` are the six
  concurrent evaluators, whose individual failures never abort the run; `05g` runs
  last and consumes the others' output.
- **Security coverage by delegation**: the orchestrator invokes the existing
  `04e-diff-security-scan` agent directly with the confirmed diff range. It is
  already diff-shaped, already holds no `execute`, and already declares its
  diff-scope limitations. It writes its report on the same contract, so `05g`
  consumes it like any other evaluator report. No new security agent is authored.
- **Skills** (in `.github/skills/`):
  - `pr-review-conventions` — shared constraints for all 05x evaluators (report
    locations/naming, severity levels, ≤10-line return-summary contract,
    read-only worktree etiquette, model-tier notes). Mirrors `auditor-conventions`.
  - `pr-review-report` — output templates: change narrative, findings reports, and
    the readiness report. Mirrors `implementation-record`.

  `worktree-baseline` already exists, is already independent of any review scope,
  and is already propagated. It is consumed as-is and must not be modified by this
  phase.
- **Development fixture**: a base/branch SHA pair drawn from this repo's own
  history, pinned in the fixture definition, sized to a realistic pull request —
  large enough that every evaluator finds something, small enough to dry-run
  repeatedly. `.gitignore` must be amended so the fixture is trackable while run
  output stays ignored.
- **Retirement**: `05c-qa-consolidator`, `05d-security-rollup`, `05e-ac-regression`,
  `05f-seam-analyzer`, and `05i-learnings-harvester` are deleted from
  `.github/agents/`, along with their generated Claude, OpenCode, and Codex
  outputs, and every reference to them across agents, skills, tests, and
  documentation.
- **Propagation**: all agents and skills join `scripts/propagate_master_assets.py`
  output for Claude/OpenCode/Codex, consistent with the rest of `.github/`.

### Out of Scope

- Any hook work (Phases 01, 04, 05, 06 territory) — this phase touches no
  `.github/hooks/` assets. The propagation pruning change is to
  `scripts/propagate_master_assets.py`, which is shared asset infrastructure this
  phase already depends on, not hook logic.
- **Per-agent command scoping.** Restricting an agent to a named set of shell
  commands requires a PreToolUse hook on Claude, and this phase owns no hooks. It
  is deferred to a hook-owning phase and recorded with routing in
  `.github/learnings/cross-phase-decisions.md`.
- **Narrowing `execute` on agents outside the PR Review family.** Twenty-six agents
  declare `execute`, including `04-phase-execute` and its subagents — which this
  phase explicitly does not touch — and agents such as `debugger` and `test-writer`
  whose purpose is running arbitrary commands. Deferred.
- Mechanical enforcement of the verdict. A hook that blocks push or merge on
  `NO-GO` is deferred; it belongs to a phase that owns hooks. Recorded as a
  deferred capability in `.github/learnings/cross-phase-decisions.md`.
- Multi-subphase whole-phase review. The agent reviews a branch diff. Phases are
  reviewed by their own artifacts and by `prod-code-review`.
- Changing the existing per-feature pipeline (`04-phase-execute` and its
  subagents) — PR Review runs after it, never replaces it.
- Modifying `prod-code-review` itself — `05g` extends its conventions; it does not
  rewrite the existing gate.
- Modifying `worktree-baseline` or `test-analyst`, both consumed as-is.
- Auto-remediation of findings — the readiness report identifies blockers; fixing
  them is follow-up work through the normal feature pipeline.
- Reading pull-request comments or any other network-sourced text back into the
  agent. Output to the PR is one-way. Ingesting PR discussion is a prompt-injection
  surface and belongs to the injection-defense phase if it is ever wanted.
- Partial re-run machinery. The policy is a full re-run; each run writes its own
  report directory.

## Key Deliverables

| # | Deliverable | Description | Likely Features |
|---|-------------|-------------|-----------------|
| 1 | Propagation orphan pruning | Generated outputs whose source asset is gone are removed from all three roots, guarded so hand-maintained files inside generated roots survive; the dead Codex skills guard is repaired | Propagation script, prune tests |
| 2 | Retirement of the five phase-shaped evaluators | Delete `05c-qa-consolidator`, `05d-security-rollup`, `05e-ac-regression`, `05f-seam-analyzer`, `05i-learnings-harvester` and their generated outputs; reconcile the orchestrator roster, the agent catalogue, and the tests that pin them | Agent deletion, test rewrite |
| 3 | Conventions + report skills | Rescope the two shared skills from whole-phase to branch-diff: report root, the seven-report roster, severity, return contract, optional-artifact posture | Skill rescope |
| 4 | Orchestrator + single upfront interaction + fixture | `05-pr-review.agent.md` with base suggestion/confirmation, model-tier warning, PR-comment choice, the no-questions-after-the-block rule, the `04e` delegation seam, and the pinned base/branch pair | Orchestration, git base derivation, fixture pinning |
| 5 | Mechanical evaluators | `05c-artifact-sweeper`, `05d-consistency-auditor`, `05e-dependency-auditor` | Cheap-tier sweep agents |
| 6 | Narrative + test health | `05b-change-narrator`, `05f-test-health` | Diff chunking, agent delegation |
| 7 | Synthesis + PR posting | `05g-readiness-synthesizer`; `gh` posting with auto / ask-when-ready / never, and the no-PR-exists path | Go/no-go report |
| 8 | Reconciliation + end-to-end proof | Dangling-reference sweep across the agent catalogue and repository docs; propagation idempotency; the assembled dry run against the fixture, including a forced-failure run | Cleanup, integration verification |

## Technical Context

- **House style to follow**: numbered orchestrator + lettered subagents
  (`04-phase-execute` + `04a`–`04e` in `.github/agents/`); shared-convention skills
  (`auditor-conventions`); report-template skills (`implementation-record`).
- **Base derivation, verified in this repo**: `git symbolic-ref refs/remotes/origin/HEAD`
  returns `refs/remotes/origin/main` here, but it is commonly unset in fresh
  clones, and it names the *default* branch rather than *this branch's* base.
  `git merge-base HEAD <base>` is exact but requires already knowing the base.
  The self-exclusion trap is demonstrable: `git merge-base HEAD <current-branch>`
  and `git merge-base HEAD origin/<current-branch>` both return HEAD.
- **Per-agent command scoping is not expressible, and this is a harness fact rather
  than a propagator gap.** A Claude subagent's `tools:` frontmatter accepts only
  bare tool names and MCP patterns; a command-scoped entry is an *unresolved tool
  name* and Claude Code refuses to launch the subagent. Subagents have no
  `permissions` or `allowed-tools` key, and `permissionMode` selects how prompts are
  handled rather than which commands are allowed. Command scoping lives in
  project/session-wide settings rules, which are not per-agent, or in a per-agent
  PreToolUse hook. **OpenCode** does support per-agent `permission.bash` globs
  (last-match-wins, so the `*` catch-all must come first; patterns match parsed
  commands). **Codex** has no per-profile command list; its execpolicy rules are
  global, sandbox-escape-only, and experimental. Native per-agent scoping therefore
  exists on one of three harnesses, and emitting it anyway would be real on OpenCode
  and decorative on the other two.
- **Propagation prunes only Codex agents and profiles today, and one prune that
  looks implemented is dead code.** Generated Codex agent TOML carries a header
  marker that its prune guard matches. The Codex *skills* guard tests the same
  marker with a prefix check, but generated skill Markdown opens with YAML
  frontmatter and carries the marker below it, so the guard never matches and that
  prune has never fired. Claude agents, Claude commands, and OpenCode agents have no
  prune and carry no marker at all to guard one by. `claude/agents/README.md` is a
  hand-maintained file living inside a generated root, so an expected-set sweep with
  no guard would delete it. Suggested implementation shape, to be verified by
  Feature Decomposer against current code and tests: emit a Markdown-safe marker
  (the skill constant is an HTML comment; the agent constant is a TOML comment and
  would render as a heading), then guard on it; skill directories, which have no
  marker, key on directory-name expectation instead.
- **Emission must complete before pruning.** Claude and OpenCode output filenames
  are chosen by inspecting stems already present on disk, so deleting during
  emission can change a surviving agent's identifier.
- **Renaming is asymmetric across harnesses.** Claude filenames are keyed on the
  agent's display name and mostly survive a renumber; OpenCode filenames are keyed
  on the source slug and orphan on every renumber. Agent references in prose are
  rewritten by display name, so a renamed agent leaves any un-updated mention
  shipping as a literal string.
- **Codex `max_depth` defaults to 1, and a blocked spawn falls back to inline work
  silently.** `05f`→`test-analyst` and `05b`→per-directory readers both sit at depth
  2. The agent will correctly state that it delegates while the runtime does not, so
  delegation must be verified from a runtime transcript; a static assertion over the
  agent body cannot detect it. Recorded in `.github/learnings/debugging-learnings.md`.
- **Agents reused by delegation**: `04e-diff-security-scan` (security),
  `test-analyst` (`05f`).
- **Graph tooling**: `05c` and `05d` build on the code-review-graph MCP server
  (`refactor_tool` dead-code detection, `get_impact_radius`).
- **Precedent for readiness gates**: the `prod-code-review` agent/skill — `05g`
  operates on a different axis (branch diff vs. phase document set) and extends its
  conventions.
- **`.gitignore` ignores `dev/*`** and un-ignores only the legacy review fixture
  path. The pinned fixture is untrackable until that is amended, and the failure is
  silent.
- **Propagation**: `scripts/propagate_master_assets.py` regenerates
  Claude/OpenCode/Codex outputs from `.github/`. Generated roots are `claude/`,
  `opencode/`, and `codex/`; retired agents must disappear from all three.

## Dependencies & Risks

- **Dependency**: `gh` availability and authentication for the PR-comment path.
  Mitigation: posting is opt-in and never required; an unavailable or
  unauthenticated `gh` is reported alongside the local report, not treated as a
  run failure.
- **Dependency**: code-review-graph MCP server availability for `05c`/`05d`.
  Mitigation: partial-failure semantics — those evaluators report as not-run with a
  stated reason, the run completes, and the verdict ceiling drops below GO.
- **Risk**: the base suggestion is silently wrong, skewing every diff-based
  evaluator. Mitigation: the base is always user-confirmed, its derivation source
  is shown, and the three known-wrong cases (branch off a feature branch, rebased
  branch, squash-merged base) are named in the confirmation prompt.
- **Risk**: pruning deletes a file it did not generate. This phase adds a
  file-deleting capability to a script that regenerates three whole directory trees.
  Mitigation: a positive generated-marker guard where a marker can exist; an
  acceptance criterion that a run against the unmodified repository deletes zero
  files; deletion counts surfaced rather than silent; and every generated root is
  committed, so an over-deletion is recoverable from version control.
- **Risk**: a long-lived branch produces a diff as large as a whole phase, and
  context blows out. Mitigation: the ≤10-line return-summary contract and
  reports-on-disk pattern are hard requirements in `pr-review-conventions`, not
  suggestions; `05b` chunks internally; `05g` reads reports only, never code.
- **Risk**: a delegating evaluator silently becomes a reimplementation under Codex's
  depth limit, and reports success. Mitigation: runtime verification of the child
  invocation during the dry run; the delegation claim in the agent body is not
  evidence.
- **Risk**: a mechanical sweep attributes pre-existing findings to the branch by
  filtering on touched files rather than added lines. Mitigation: verifiable
  added-line attribution is required of any evaluator calling repo-wide analysis.
  Reporting a file's twelve pre-existing TODOs because the branch touched one line
  trains the reader to ignore the report.
- **Risk**: an evaluator failure silently reads as a clean check. Mitigation: the
  readiness report must enumerate not-run checks by name, and `05g` is prohibited
  from issuing GO while any check is missing.
- **Risk**: posting publishes findings to collaborators before the author has read
  them. Mitigation: the *ask once the report is written* option is the default
  recommendation; *auto* is available but the upfront prompt states plainly that it
  publishes an unread verdict. A posted comment is not undone by reverting the agent.
- **Risk**: overlap with `prod-code-review` blurs which gate is authoritative.
  Mitigation: explicit scope line — `prod-code-review` gates a phase's feature set
  using pipeline documents; PR Review gates a branch diff and treats those documents
  as optional enrichment.
- **Risk**: deleting five agents leaves dangling references in skills, docs, and
  generated outputs. Mitigation: deletion lands early so the five are out of every
  later feature's blast radius, and a dedicated reconciliation deliverable sweeps
  references as a test rather than a checklist.
- **Risk**: this agent family has never demonstrably run end to end — the
  whole-phase flow it descends from never completed a real run. The assembled dry
  run in Deliverable 8 is the first proof, and a dry run whose evaluators report
  `not-run` is evidence of broken wiring, not a pass.

## Success Criteria

- [ ] `scripts/propagate_master_assets.py` removes generated agent, command, and
      skill outputs whose source asset no longer exists, across all three roots;
      the Codex skills guard actually matches; `claude/agents/README.md` survives
      every run; a run against the unmodified repository deletes zero files; and
      deletion counts are reported.
- [ ] No agent in the PR Review family carries `execute` unless a named command
      with no non-shell equivalent requires it, and each such grant is declared with
      that justification. `05a`'s `git worktree` grant and the orchestrator's
      `git`/`gh` grant are declared, not omitted from the propagation roster.
- [ ] The propagation roster enumerates all seven `05a`–`05g` agents with per-agent
      expected tool lists. No agent may be omitted from enumeration to avoid an
      assertion.
- [ ] `05-pr-review.agent.md` and all seven `05a`–`05g` subagent files exist in
      `.github/agents/`, follow the numbered/lettered house style, and propagate
      cleanly to Claude, OpenCode, and Codex outputs.
- [ ] `pr-review-conventions` and `pr-review-report` exist in `.github/skills/` and
      propagate cleanly; `worktree-baseline` is unchanged.
- [ ] The five retired evaluators are absent from `.github/agents/` and from all
      three generated roots, and no skill, test, or document references them — by
      slug, by display name, or by prose name. Historical records in
      `docs/phases/**` and `.github/learnings/**` retain them.
- [ ] No generated root contains an artifact of a deleted or renamed source asset,
      including the orchestrator's superseded slash command.
- [ ] The upfront interaction asks the model-tier warning, base confirmation, and
      the PR-comment choice in one block, and the run reaches a written report with
      no further prompt on every path — including evaluator failure, timeout, and
      absent `gh`.
- [ ] Base suggestion resolves via `origin/HEAD`; with `origin/HEAD` unset it falls
      back to `origin/main`, then `origin/master`, then presents candidates for
      selection. It never suggests the current branch or its own remote-tracking
      ref.
- [ ] A user-supplied base correction overrides the suggestion, and every
      downstream evaluator receives the corrected merge-base.
- [ ] Reports are written under `dev/pr-review/<base-sha-short>-<timestamp>/`, and
      no branch name appears in any path component.
- [ ] Subphase discovery, ledger parsing, the `eval:` commit-message fallback, the
      artifact-inventory refusal gate, verdict write-back, and archive-before-overwrite
      are absent from the orchestrator — not disabled, not behind a flag.
- [ ] With one evaluator forced to fail during a dry run, the run completes, the
      readiness report names the missing check and its reason, and the verdict is
      not GO.
- [ ] Every subagent's return payload in the dry run is ≤10 lines, with full detail
      on disk.
- [ ] A dry run against the pinned base/branch fixture pair produces a change
      narrative, artifact/consistency/dependency findings, a test-health report, a
      diff-scoped security report from `04e`, and a severity-ordered readiness
      report — all present, none recorded `not-run`.
- [ ] `05f` and the security seam demonstrably delegate to the existing
      `test-analyst` and `04e-diff-security-scan` agents rather than reimplementing
      them, verified from a runtime transcript on a harness where the depth limit
      applies.
- [ ] With the PR-comment choice set to *ask when ready*, the report is written
      before the prompt appears. With it set to *never*, no network call is made.
      With no pull request open, the condition is reported and the local report
      still stands.
- [ ] The agent writes no status line in `PROJECT_ROADMAP.md` or any phase summary
      on any path.
- [ ] P5-SEC-02 is either closed by the rebuilt readiness path or recorded as open
      with an owner and routing. It is not closed by asserting the contract more
      firmly in prose.

## QA Considerations

- No frontend/UI changes — no manual QA docs required on that basis.
- This phase ships agents, skills, and one propagation-script change. QA is
  primarily **behavioral**: dry-run the orchestrator against the pinned fixture pair
  and verify the single-interaction contract, report structure, return-summary
  discipline, and failure modes.
- **A fixture dry-run is required release evidence.** Static contract review cannot
  observe runtime report creation, and a run whose required evaluators are recorded
  `not-run` is artifact-level, below-GO evidence rather than a passing dry run.
- **Live QA against a scratch consumer repo**, never this one, for: `origin/HEAD`
  unset, base correction, no-PR-exists posting, and `gh` unauthenticated.
- **Runtime delegation QA** on Codex, where the default depth limit blocks the
  depth-2 spawns and the fallback is silent.
- Propagation QA: after each feature, verify Claude/OpenCode/Codex outputs
  regenerate without diff noise in unrelated assets, that retired agents are gone
  from all three roots, and that a second consecutive run changes nothing.
- **Test impact is real and lockstep-required.** `tests/test_propagate_master_assets.py`
  pins a slug tuple that deliberately omits the four agents holding `execute`,
  asserts their absence of that grant, and carries a conditional keyed to a retired
  agent; `tests/test_readiness_synthesis_agents.py` asserts literal strings from two
  agents, one of which retires, and one assertion is coupled to an exact line-wrap
  position. All of these break under the new roster and must be rewritten with the
  features that break them — not deferred to a cleanup pass. New coverage is owed
  for pruning, base-suggestion self-exclusion, the fallback chain, and report-root
  derivation.
- **The test baseline is unstable.** A green local run is not a baseline: the
  propagated-guard latency gate (PERF-01, owned by Phase 04) fails
  probabilistically, and this repo has already recorded a coin flip landing heads
  as a clean baseline. Capture repeated runs before claiming a regression, and never
  relax a fixed budget to make a gate pass.

## Notes for Feature - Decomposer

- **Pruning first**: Deliverable 1 is the first feature and every later one depends
  on it. Each subsequent deliverable deletes or renames a source asset, and without
  pruning each one strands a live artifact in the generated roots. The superseded
  slash command is the sharpest case: it stays user-invocable while pointing at a
  deleted agent.
- **Retirement second, reconciliation last.** Deleting the five phase-shaped
  evaluators early removes them from every later feature's blast radius; the
  dangling-reference sweep and the end-to-end proof stay at the end, where they are
  the integration point.
- **Conventions before evaluators**: Deliverable 3 settles the report root, the
  seven-report roster, and the return contract. Every evaluator is authored against
  those contracts, so settling them once prevents each evaluator feature from
  re-litigating them.
- **Orchestrator before the evaluators** so each evaluator can be dry-run through it
  as it lands. The orchestrator owns the roster in one place, including the `04e`
  seam.
- **The single-interaction rule is an acceptance criterion, not a style note.**
  Every feature that adds a code path must show that path reaches a report without a
  new prompt. This is the requirement most likely to erode silently, one reasonable
  question at a time.
- **The rescope subtracts more than it adds.** The largest single act of this phase
  is deleting the verdict write-back path — two-file transactional edits with
  unique-match ambiguity detection and restore-on-second-write-failure. It was the
  riskiest implemented code here and the rescope leaves it with no reason to exist.
  Prefer deletion to porting.
- **Group evaluators by kind**: mechanical sweeps (`05c`/`05d`/`05e`) share a
  cheap-tier, config-driven shape and belong in one feature; `05b` and `05f` differ
  enough to warrant individual design.
- **Careful separation**: `05g` must depend only on report files, never on other
  agents' internals — keep its feature late and its inputs pinned to the
  `pr-review-report` templates.
- **Integration points**: `05f`→`test-analyst`, orchestrator→`04e-diff-security-scan`,
  `05c`/`05d`→code-review-graph MCP tools, orchestrator→`gh`,
  everything→`propagate_master_assets.py`. Each is a seam worth an explicit
  acceptance criterion.
- **Expect the work to be near-sequential.** The propagator, its test file, and the
  orchestrator thread through most deliverables, and the propagation roster
  assertion is touched by most evaluator work. Parallelism here would mean
  concurrent edits to one assertion.
