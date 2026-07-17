# Cross-Phase Decisions

## Phase Numbering

- **Phase 04 split 2026-07-16, and "Phase 04" therefore means two different things depending on when a note was written.** The phase originally scoped as *Hook Release Remediation & Verification* is now **Phase 07** and retains all of that content unchanged (`docs/phases/PHASE_07/PHASE_07_SUMMARY.md`). **Phase 04 is now *Guard Accuracy & Propagation Reach*** — the GUARD-01 false-positive fix plus user-global symlink propagation — and owns none of the verification work. **Anywhere in this file that "Phase 04" is described as owning PERF-01, the bash-rewrite bypass, the 17-rule guard review, REPO-SEC-06, live harness QA, record reconciliation, or Phase 03's NO-GO, it means Phase 07.** Those notes predate the split and are left as written; only live routing was retargeted.
- **Phase 07 runs before Phases 05 and 06, which both depend on it.** It was filed at 07 rather than renumbering 05→06→07. **This is the direct application of the lesson recorded immediately below**: the 2026-07-16 renumber silently changed the meaning of the plugin-packaging deferral, and re-sequencing two more phases to keep the count tidy would have put both at that same risk to satisfy a convention this project had already abandoned when agent numbers stopped tracking phases. **Execution order is 01 → 02 → 03 → 04 → 07 → 05 → 06; read the roadmap's dependency column, never the number.**
- **The split itself is the cautionary case.** Re-pointing Phase 04 at new work took one edit; it silently invalidated two `Depends On` declarations and the roadmap's entire ordering rationale, all of which referenced the phase by number. **A phase number is a public identifier — changing what it denotes is a breaking change to every document that cites it, and nothing warns you.** Grep for the number before re-pointing one, and expect the referents to be in the columns you were not editing.
- **Phases were renumbered 2026-07-16** so numbers match the order work actually happened: Phase Final Review (was 05) → **03**; new Release Remediation & Verification → **04**; Format-on-Save + Completion Gates (was 03) → **05**; Skill Enforcement (was 04) → **06**. Phases 01 and 02 are unchanged. Documents written before that date use the old scheme; the mapping table is in `docs/phases/PROJECT_ROADMAP.md`.
- **Agent numbers are pipeline positions, not phase numbers.** `05-phase-final-review` and its `05a`–`05l` evaluators follow `04-phase-execute` in the pipeline; they did not renumber with the phase and must not be "corrected" to match it.
- **~~Development fixtures keep legacy phase identifiers.~~ Retired 2026-07-16 by `08-retirement-reconciliation`.** The note said `dev/phase-final-review/fixtures/PHASE_05/` (pseudo-subphases `PHASE_05a`/`PHASE_05b`) and the report root `dev/phase-final-review/PHASE_05/` were synthetic identifiers pinned to recorded commit SHAs, and that renaming them would invalidate the fixture contract. Both are gone: the report root migrated to `dev/pr-review/<base-sha-short>-<UTC-timestamp>/` (feature `07`) and the fixture tree was deleted, its replacement being `dev/pr-review/fixtures/pinned-diff-range.md`. The advice was sound and is preserved for the *new* fixture, which is likewise pinned to recorded SHAs (`f5ab960..e6ff28a`) and must not be re-pointed. The dead half is struck rather than deleted because it is the premise two later notes reasoned from.

## Release Verification

- **"Remediated in code" is not "verified".** Phase 02's P2-SEC-01..03 fixes and Phase 01's SEC-01 fix exist in code, but a fix without a re-run gate is not a release verdict. Status lines move only on fresh final-state evidence — this is the operational form of the Final Review Contract below.
- **A fixed budget must never be relaxed to make a gate pass.** PERF-01's 50 ms propagated-guard budget was silently raised to 90 ms in PR #22 to mask a failure; that was reverted. If a budget is genuinely unachievable, the honest outcome is an explicit user-approved AC change, not a quietly edited threshold.
- **PERF-01's AC was reshaped by explicit user approval on 2026-07-16 — this is that escape hatch being used correctly, and the distinction matters.** What was unachievable was never the 50 ms number (the guard costs ~30 ms); it was asserting a *wall-clock median* on a machine whose load is not controlled, which left ~20 ms of headroom against ambient noise and failed 2 of 6 focused runs while the guard itself was unchanged. The replacement asserts a **calibrated relative budget**: a bare-interpreter baseline captured in the same run, with the guard's cost measured above it. How much latency is acceptable did not change; what is measured did. The guardrail that keeps this distinct from the PR #22 edit is a required acceptance criterion that **a deliberately slowed guard must still fail the new gate** — a reshape that cannot fail a real regression is a deletion wearing a disguise. Any future AC reshape must carry an equivalent proof.
- **Fixes made outside the pipeline still need phase records.** Hook-command project-root anchoring and file-access-guard false-positive tuning both changed shipped behavior during ad-hoc debugging sessions with no phase record. Reconciling them is Phase 04 scope. (Recorded 2026-07-16.)
- **A stale scan is no more authoritative than a stale fix — every finding classification must name the revision it examined.** The Phase 03 delegated scan (`dev/phase-final-review/PHASE_05/z-security-scan-final.md`) classifies P2-SEC-01..03 as *persisting*; it names its subject as revision `344711df78c5` on `phase/phase-final-review-2`, where `redact_tool_output` still recursed through mappings preserving container shape — the P2-SEC-01 defect. At HEAD that function returns a fixed redacted shape. Both conclusions are correct about different code. The lesson generalizes: "remediated in code is not verified" is usually read as *fixes need gates*, but the converse holds equally — **an ungated finding is not a current finding**. Any evidence artifact that does not name its revision cannot be reconciled against later work, and any release dossier must verify that each artifact post-dates the code it covers. (Recorded 2026-07-16.)
- **Some High findings are not closable without new capability, and recording them honestly is the correct outcome.** Phase 04 hits three: **P5-SEC-02** (readiness-report trust boundary — no code to attach a schema/reducer to, because the readiness path is agent Markdown; a prose constraint is exactly what the Phase 03 scan faulted, so tightening wording would make the record say closed without closing anything); **`05a-baseline-worktree`'s unconstrained `execute`** (the propagation format maps `execute` to `Bash`/`bash` with no allowlist syntax, so "Bash but only `git worktree`" is inexpressible); and **absent curl/wget exfiltration enforcement** (four `legacy_bash_parity` entries describe patterns with no enforcement rule behind them, so "reinstating" means authoring rules that never existed). Each is recorded as open with routing rather than closed, and each is a NO-GO input. The general rule: **when the honest fix requires capability a phase has excluded, the phase records the finding — it does not redefine the finding to fit the scope.** (Recorded 2026-07-16.)
- **`legacy_bash_parity` in `file-access-rules.json` is a metadata inventory, not enforcement.** Its entries carry only `source_pattern`, `classification`, and `rationale`; live enforcement lives in the `bash_rules`, `rules`, and `bash_analysis` blocks, and the mapping between them is not one-to-one. Changing a `classification` value relabels an inventory entry and enforces nothing. `tests/hooks/fixtures/bash/legacy-parity.json` is hard-coupled via exact-string and count assertions, so pattern edits need lockstep fixture updates. Anyone auditing or reinstating a rule must work against the enforcement blocks. (Recorded 2026-07-16.)

## Deferred Pipeline Work

- **`.github/skills/` count claims are false on both documentation surfaces. OPEN. Owner: whoever owns `README.md` / `docs/CODEBASE_CONTEXT.md`; routing: recount from disk and guard by claim-shape.** `README.md:18` and `docs/CODEBASE_CONTEXT.md:17,34` claim 16 skills; disk holds 24. Found at feature `08` review. **Not falsified by the PR-Review phase** — the phase renamed two skill directories and changed no count — which is why it was recorded rather than fixed there: AC6b scoped to the counts the phase itself made false, and widening scope mid-review to adjacent wrong numbers is how a feature stops being reviewable. The agent and hidden-subagent counts on those same surfaces are now guarded by `_assert_every_count_claim` in `tests/test_retirement_reconciliation.py`; the skills count needs the same treatment plus a decision on what "shared skill" counts. (Recorded 2026-07-16.)
- **`docs/CODEBASE_CONTEXT.md:87-88`'s "6 orchestrators" and "11 visible user-facing agents" disagree with disk, and the two surfaces disagree on the *definition*. OPEN. Owner: whoever owns that doc.** Disk holds 19 user-invocable agents; the 3 auditors it counts as user-facing declare `user-invocable: false`; its 6-orchestrator list omits `05 PR - Review` while `.github/agents/README.md:410` says "Four orchestrators" and names a different set. This is not a stale number but two live definitions of "orchestrator", so recounting cannot fix it — the definition has to be reconciled first. Both predate the PR-Review phase. (Recorded 2026-07-16 at feature `08` review.)

- **PR posting (AC7/AC8) ships verified by contract assertion only; live QA is outstanding
  and routed to the QA stage with a scratch consumer repo.** `07-synthesis-and-pr-posting`
  implements the auto / ask-when-ready / never consent path and the no-PR, absent-`gh`, and
  unauthenticated-`gh` reported conditions entirely as agent Markdown. Every guard on it is
  a static assertion that the body *declares* the contract; none observes `gh` behaving as
  described. Two plan assumptions remain unverified by execution: that `gh pr comment`
  resolves the PR from the current branch without a PR number, and that a readiness report
  fits inside a GitHub comment (mitigated, not measured, by the recorded truncation
  decision — truncate with an explicit notice, keeping Verdict, Blocking List, and
  `Checks Not Run`). The property most needing live confirmation is *never*, whose entire
  content is a negative: a setting that must make **no** network call cannot be proven by
  reading prose, and silently degrading to "posted anyway" publishes a verdict to
  collaborators that no revert can retract. Do this in a scratch repo — never against this
  one. (Recorded 2026-07-16 by `07-synthesis-and-pr-posting`'s review.)

- `04 Phase - Execute` still uses one consolidated QA-writer invocation for all features, so per-feature `eval: qa <task>` checkpoints cannot be both phase-shared and feature-local. A future phase must either move QA invocation into each feature cycle or redefine QA checkpointing as a single phase-level commit.
- **Pre-edit file backup layer** (snapshot protected-adjacent files before Edit/Write, config-gated) was cut from Hooks Phase 01 during refinement. Candidate for the format-on-save/completion-gates phase, which owns edit-time hooks — that phase is **Phase 05** as of the 2026-07-16 renumber (it was Phase 03 when this note was written). (Recorded 2026-07-14; renumber noted 2026-07-16.)
- **WebFetch as an exfiltration channel** is deliberately unguarded in Hooks Phase 01 (the guard blocks reading secrets in the first place). Addressed: pulled into Hooks Phase 02 scope as the WebFetch exfiltration guard deliverable (see `docs/phases/PHASE_02/PHASE_02_SUMMARY.md`). (Recorded 2026-07-14.)
- **Plugin packaging as a distribution target**: propagation could emit a Claude Code plugin package (`${CLAUDE_PLUGIN_ROOT}`-relative hook paths) so others install the hook suite with one command, no cloning. Deferred; best revisited after the hook phases stabilize the hook set — written 2026-07-14 as "after Hooks Phases 01–03", which under the pre-renumber scheme meant **01, 02, and what is now Phase 05**. It does not mean the current Phase 03 (Phase Final Review), and Phase 04 does not unblock it. Folded into the adoption-readiness item below. (Recorded 2026-07-14; renumber ambiguity resolved 2026-07-16.)
- **~~`dev/phase-final-review/fixtures/PHASE_05/` is still on disk and now has no owner.~~
  Closed 2026-07-16 by `08-retirement-reconciliation`: deleted.**
  The Phase document instructed retiring both `dev/phase-final-review/fixtures/PHASE_05/`
  and the report root `dev/phase-final-review/PHASE_05/`.
  `02-retired-evaluator-removal`'s plan listed this as a Non-Goal on the stated grounds
  that the directory "does not exist" — true of the report root, **false of the
  fixtures**, which were tracked. Because it was dismissed as absent rather than
  deferred, no feature inherited it. That diagnosis was right and is the reusable half
  of this entry: **a Non-Goal justified by a factual claim inherits nothing when the
  claim is wrong — a deferral names an owner, a dismissal does not, and only one of them
  survives being mistaken.**
  **The blocking half of the note was itself false, and it is worth recording why it
  survived four features.** It said seven surviving agents named the fixture root as live
  wiring, so retiring it had "real blast radius". That conflated two different roots: the
  seven agents declared the **report** root (`dev/phase-final-review/PHASE_0N/`), the
  output they write; **no agent ever named the fixture root**, the input. `git grep`
  across `.github/agents/` returns zero hits for the fixture path at every commit in this
  phase. Feature `07` then migrated the report root to `dev/pr-review/`, so even the true
  half stopped holding. The fixture's actual consumers were the five phase-shaped
  evaluators feature `02` deleted, and its `PHASE_05a`/`PHASE_05b` pseudo-subphase shape
  *is* the phase premise this rescope retired. Its replacement is
  `dev/pr-review/fixtures/pinned-diff-range.md`.
  **The lesson: a blast-radius claim is a factual claim and needs the same evidence as
  any other.** This one was recorded once by a review, restated by features `04`, `06`,
  and `07` as settled fact, and never re-derived — each restatement made it look better
  attested while adding no evidence. A cheap `grep` refuted it at any point. **Corroboration
  is not evidence when every corroborator is quoting the same source.** (Recorded
  2026-07-16 by `02-retired-evaluator-removal`'s review; refuted and closed 2026-07-16 by
  `08-retirement-reconciliation`.)
- **The seven surviving `05x` agents still declare `dev/phase-final-review/PHASE_0N/` report
  roots** while `pr-review-conventions` now declares
  `dev/pr-review/<base-sha-short>-<UTC-…>/`. The mismatch is **intentional and temporary** —
  features `04`–`07` own those agent bodies and `03` correctly touched skill-reference tokens
  only. But **no test pins either root**, so nothing forces the migration to actually happen:
  if `04`–`07` each assume another owns it, the split ships silently and every evaluator
  writes to a root its own contract does not declare. Suggested close: `07` adds a test
  asserting the agent-declared root matches the skill-declared root. (Recorded 2026-07-16 by
  `03-pr-review-conventions-skills`'s review; originated as that feature's Gap 1.)
  **Update: the "no test pins either root" half is now closed.**
  `04-pr-review-orchestrator` added
  `tests/test_pr_review_orchestrator.py::test_report_root_migration_cannot_split_silently`,
  which asserts the **exact set** of six evaluators still on the retired root
  (`05b`, `05g`, `05h`, `05j`, `05k`, `05l`). It fails the moment any of them migrates,
  cannot be satisfied by regressing the orchestrator or the skills (both are separately
  asserted onto the new root), and is deleted when the set empties. Verified by mutation in
  both directions. The **migration itself is still open** and still owned by `05`–`07`; what
  changed is that it can no longer ship half-done in silence. (Recorded 2026-07-16 by
  `04-pr-review-orchestrator`'s review.)
  **Update: closed 2026-07-16. The migration completed and the mechanism worked.** Features
  `05`–`07` migrated all six; the ledger set is now empty and every `05x` agent declares
  `dev/pr-review/`. Feature `07` **converted** the guard rather than deleting it as its own
  docstring invited: the set is frozen empty and the assertion inverted, so it no longer
  records drift but denies it exists. That is worth keeping as the pattern — **a migration
  ledger that deletes itself on completion takes the regression guard with it.** Emptying the
  set is the migration; inverting the assertion is what stops the next feature quietly
  regressing to the retired root. Verified at `08`: no `05x` body names the retired root.
- **User-local configuration referencing the retired skill names** (`phase-final-review-conventions`,
  `phase-final-review-report`) — e.g. a personal `~/.claude/` setup — cannot be verified or
  fixed from this repository. Verified clean for `.github/`, `tests/`, `scripts/`, and all
  three generated roots. Routes to `08-retirement-reconciliation`'s notes as an
  acknowledged, unclosable assumption rather than a gap. (Recorded 2026-07-16 by
  `03-pr-review-conventions-skills`'s review.)
- **Adoption readiness is unplanned work with no roadmap entry.** Phases 01–04 are scoped for an audience of the author and friends — people who can ask a question and get an answer. That assumption is what makes three residual risks acceptable: Codex's partial tool coverage stays documented rather than redesigned, the file-access guard's friction profile stays hand-tuned to one workflow, and distribution stays "clone and run propagation". Adoption beyond that circle invalidates all three, because partial protection that reads as total protection is worse than none once the user cannot ask. A future phase would need: a packaged install path (see plugin packaging above), a friction budget tunable without editing rule files, recovery/kill-switch docs written for a stranger, an upgrade path when rules change, and install-time disclosure of Codex's coverage gap. **This needs a roadmap entry from `@project-planner`; it is explicitly out of scope for Phase 04.** (Recorded 2026-07-16.)

- **The PR Review fixture dry run (`04-pr-review-orchestrator` AC13) is deferred to
  `08-retirement-reconciliation`, and deferral is the only correct option.** The fixture
  (`dev/pr-review/fixtures/pinned-diff-range.md`, `f5ab960..e6ff28a`, 26 files / 1288
  insertions) is pinned, tracked, and asserted, but the run was not executed. Five of the
  eight roster names — `05c`, `05d`, `05e`, `05f`, `05g` — resolve to **no agent on disk**
  until features `05`–`07` land in waves 5–6. A dry run today would record five of six
  fan-out evaluators as `not-run`, which by the orchestrator's own AC11 semantics caps the
  verdict at NO-GO **by construction**: it would manufacture below-GO evidence from an
  unrunnable roster, which is precisely what the recorded release rule (*a run whose required
  evaluators are recorded `not-run` is below-GO evidence, not a passing run*) exists to
  forbid. The report-root split above is a second, independent blocker: evaluators would be
  routed to a root they do not write to. `08` already owns verifying the roster resolves and
  is the first point at which the run is possible. **The general rule: a required-evidence
  run whose prerequisites cannot exist yet must be deferred with a named owner, never
  executed early to produce an artifact.** (Recorded 2026-07-16 by
  `04-pr-review-orchestrator`'s review.)
- **The `05x` roster forward reference is safe today because the propagator resolves
  `agents:` by display name, not slug.** `05 PR - Review` forward-references `05g Readiness
  Synthesizer` while `05g-artifact-sweeper.agent.md` exists on disk with the display name
  `05g Artifact Sweeper`. Verified: no roster entry mis-binds to an existing agent. A
  slug-based resolver would silently bind the synthesis position to the artifact sweeper.
  Any future change to agent-reference resolution must preserve display-name matching, or
  re-check every forward reference in the roster. (Recorded 2026-07-16 by
  `04-pr-review-orchestrator`'s review.)
- **P5-SEC-02 remains OPEN after the readiness-path rebuild. Owner: a future hook- or
  script-owning phase; routing: the same phase that gains code execution for the PR Review
  path.** The earlier record said the finding "is closed by rebuilding the readiness path
  **in code**", and anticipated that the rescope *would be* that rebuild — so the validator
  would arrive with it. It did not, and the distinction matters: the rescope rebuilt the
  readiness path **as agent Markdown**, not as code. `05g-readiness-synthesizer` still
  reduces evaluator *claims* into a verdict behind metadata-only validation (readable,
  regular, non-empty, under the current run root). There is still no strict schema and no
  deterministic status reducer over structured records, because there is still no code to
  attach them to — only a differently-worded prompt. Closing it here would have meant
  asserting the trust contract more firmly in prose, which is precisely the move the Phase
  03 scan faulted, and would have made the record say closed without closing anything.
  What this feature did instead: `05g` names the gap in its own body (**Trust Boundary**)
  and instructs against resolving it by tightening prose, so the agent cannot present a
  metadata check as claim validation. That is honest scoping, not closure. **The rule
  applied: when the honest fix requires capability a phase has excluded, the phase records
  the finding — it does not redefine the finding to fit the scope.** The generalization
  worth carrying: "the rebuild will bring the validator" is a prediction, not a plan, and a
  finding routed to a rebuild must name the capability the rebuild has to gain — otherwise
  the rebuild arrives, lacks it, and the finding silently looks overdue instead of
  correctly deferred. (Recorded 2026-07-16 by `07-synthesis-and-pr-posting`.)
- **Per-agent command scoping. OPEN. Owner: a hook-owning phase (Phase 05 or 06); routing:
  a per-agent `PreToolUse` hook.** This is what the phase set out to achieve and could not.
  It is not expressible in Claude subagent frontmatter (`tools:` takes bare tool names and
  MCP patterns; `Bash(gh:*)` is an unresolved tool name and Claude Code refuses to launch
  the subagent), it is native only on OpenCode (`permission.bash` globs), and it does not
  exist per-profile on Codex. Native support on one of three harnesses means building the
  syntax would be real on OpenCode and decorative elsewhere — "partial protection that reads
  as total protection", aimed at ourselves. **What the phase achieved instead is narrower
  and real, and is stated that way deliberately:** `execute` was *removed* from the
  evaluators that did not need it (feature `05`), *never added* to those that never had it
  (feature `06`), and *retained only* where a named command has no non-shell equivalent —
  `05a-baseline-worktree`'s `git worktree`, and the orchestrator's `git symbolic-ref`/
  `merge-base`/`branch`. Removal is the only narrowing the target formats can express, so
  the residue is recorded open rather than reworded into looking closed. (Recorded
  2026-07-16 by `08-retirement-reconciliation`.)
- **The `NO-GO` enforcement hook. OPEN. Owner: a hook-owning phase; routing: the same phase
  that gains `PreToolUse`/`PostToolUse` capability for the PR Review path.** The readiness
  verdict is **advisory**: `05 PR - Review` records no verdict in any document and nothing
  blocks a merge on `NO-GO`. Making a verdict binding needs a hook, which this phase
  excludes. Recorded so that "the reviewer said NO-GO" is not mistaken for "the NO-GO
  stopped something". (Recorded 2026-07-16 by `08-retirement-reconciliation`.)
- **Propagation is not idempotent across an agent-identifier reclassification. OPEN. Owner:
  a propagator-owning feature; routing: `_claude_filename_for` / `_claude_identifier_for`
  identifier resolution.** Both resolve identifiers against **on-disk stems**, so removing or
  renaming a generated file changes the identifier computed on the *next* run. Feature `02`
  needed three `--once` runs to converge after the `Security Scan` dual-use cascade; feature
  `07` hit it again on the `05l`→`05g` rename. A single run therefore leaves a valid-looking
  but non-converged tree. **The operational rule until it is fixed: run propagation
  repeatedly until every change counter is zero — "I ran the propagator" is not evidence of
  convergence.** Pinned by `tests/test_retirement_reconciliation.py::
  test_committed_tree_is_at_a_propagation_fixed_point`, which fails on an unconverged tree,
  so the wart can no longer ship silently even while the resolution defect stands. Not fixed
  in `08`: changing identifier resolution is propagator surgery this feature does not own.
  (Recorded 2026-07-16 by `02-retired-evaluator-removal`; routed 2026-07-16 by
  `08-retirement-reconciliation`.)
- **A hand-maintained enumeration of a set will drop the member that does not match the
  set's naming convention, and the drop is invisible because the remainder looks complete.**
  The evidence is a natural experiment. At the phase baseline, the agent catalogue's subagent
  table and `expected_slugs` omitted **exactly the same four** evaluators — `05a`, `05g`,
  `05j`, `05k` — and all four held `execute`, which looked like the explanation. It is not:
  `expected_slugs` had a motive (omission dodged a blanket `assertNotIn("execute", ...)`),
  but a README has no assertion to dodge. The real shared cause is **category**: those four
  are the mechanical, tool-running evaluators — the decomposition independently named its
  feature `05-mechanical-evaluators` after exactly that set — and `execute` is a *marker* of
  the category, not the cause of the omission. **Two surfaces built from the same mental
  roster inherit the same gap, and correlation between them is not corroboration.**
  Feature `05` closed the `expected_slugs` half by deriving it from disk. Nothing derived the
  catalogue, and the defect duly reproduced there — at `08` the catalogue still omitted `05a`
  and still listed `05f` under its retired `05h` slug, while the tested surface stayed
  correct. **The fix is not vigilance, it is derivation:** `tests/
  test_retirement_reconciliation.py::test_agents_readme_roster_covers_every_pr_review
  _evaluator_on_disk` now derives the expectation from `.github/agents/`, so cataloguing is
  no longer optional. (Recorded 2026-07-16 by `08-retirement-reconciliation`.)
- **The PR Review fixture dry run (`04` AC13 → `08` AC1–AC4) is STILL UNEXECUTED. OPEN.
  Owner: the QA stage or any context that can spawn subagents; routing: run
  `05 PR - Review` against `dev/pr-review/fixtures/pinned-diff-range.md`.** The recorded
  blocker is gone — all eight roster names now resolve to agents on disk (verified), the
  report-root split is closed, and the pinned range `f5ab960..e6ff28a` resolves to exactly
  its recorded 3 commits / 26 files / 1288 insertions. **The run was not performed because
  `08`'s implementation context has no agent-spawning tool, and a seven-evaluator fan-out
  cannot be simulated.** Per the standing rule — *a run whose required evaluators are
  recorded `not-run` is below-GO evidence, not a passing run* — manufacturing a partial
  artifact would be worse than recording the gap. **This agent family has still never
  demonstrably worked end to end**, and that remains the phase's largest open risk: eight
  features passed review in isolation and nothing has yet run them together. (Recorded
  2026-07-16 by `08-retirement-reconciliation`.)
- **User-local configuration naming the retired skills** (`phase-final-review-conventions`,
  `phase-final-review-report`) — e.g. a personal `~/.claude/` setup — cannot be verified or
  fixed from this repository, and `08` confirms it stays open as an acknowledged, unclosable
  assumption rather than a gap. Verified clean everywhere this repo controls: `.github/`,
  all three generated roots, `tests/`, and `scripts/`. (Routed to `08` by
  `03-pr-review-conventions-skills`'s review; acknowledged 2026-07-16.)

## Hook Composition

- **A PreToolUse hook that rewrites `tool_input.command` can invalidate another PreToolUse hook's analysis of that same command.** `.github/hooks/scripts/rtk-rewrite.sh` reads `.tool_input.command` and delegates rewriting to an external `rtk` binary resolved from `PATH`; the file-access guard classifies Bash commands through its bash analyzer. If the guard evaluates the pre-rewrite string, the executed command is not the command that was approved. Three properties make this a standing concern rather than a one-off: **(1)** correctness depends on hook ordering between a *global* (`~/.claude/settings.json`) and a *project* hook, which no test covers; **(2)** the global registration uses an absolute path into this repository, so every Bash command in every project the user runs routes through a script living here, and moving this repo breaks Bash hooks everywhere — the same absolute-path fragility already recorded for the eval hook symlink; **(3)** the `rtk` binary is unpinned and trusted on `PATH`, and this project's own RTK reference documents a name collision with a different published tool of the same name, making shadowing a stated install hazard rather than a hypothetical. Phase 04 investigates ordering empirically and assigns severity from the evidence. **The general rule for future hook work: any hook that mutates tool input must be ordered strictly before every hook that authorizes on that input, and that ordering needs a test — composition safety is not inheritable from the safety of each hook alone.** (Recorded 2026-07-16.)
- **The kill switch is two switches.** `.github/hooks/config/file-access-overrides.json` gates only the PreToolUse file-access guard; the injection scanner reads `.github/hooks/config/injection-overrides.json`, which does not exist. Because an absent config layer reads as `{}`, *creating* that file disables the scanner — so restoring it means **deleting** it, not writing `{}`. The restore is asymmetric between the two. Any live QA that provokes the scanner must arm both first; arming one while provoking the other leaves the component under test with no recovery path. (Recorded 2026-07-16.)

## Guard Friction and Command Prompting (raised 2026-07-16; revisit at Phase 04 refinement)

**Two items to revisit together at Phase 04 refinement. They look like separate complaints and are one component.**

- **There is no command-allowlist hook in this repo. The thing that prompts on commands is the file-access guard.** Raised 2026-07-16: the friction was initially attributed to the guard, then re-attributed to "the command allowlist." Neither framing is quite right, because they are the same code path — `scripts/file-access-guard.py` loads `bash_rules` from `config/file-access-rules.json` through `lib/bash_analyzer.py`. Nothing else in the repo gates commands. (Claude Code's own native permission prompts are the other source of command friction, and are not ours to tune.)
- **The friction and the security live in different config blocks, and that is the whole point.** Measured 2026-07-16 in `config/file-access-rules.json`: **`bash_rules` is 20 entries, every single one `action: ask`** — 5 environment probes (`printenv`, bare `env`, `set`, `export`, `echo $VAR`) and 15 destructive operations (`rm -rf`, `git push --force`/`-f`, `git reset --hard`, `git clean -f`/`-fd`, `chmod -R`, `dd`, `mkfs`, device redirection, `truncate`, `shred`, `wipefs`, `DROP TABLE`, `DROP DATABASE`). The file-access `rules` block is 37 entries: **32 `deny`**, 3 `ask`, 2 `allow`. ~~**Every prompt comes from the ask-rules; the bypass-permissions protection that the roadmap Vision sells is the 32 silent denies, which never prompt at all.** Retiring the guard to stop the prompting would delete 32 deny rules to fix 20 ask rules.~~
- ~~**The five environment probes are the first thing to examine.** `echo $VAR` and `printenv` are ordinary work, not destructive acts. If the friction is concentrated there, the fix is editing one JSON config — not removing a phase deliverable.~~
- **Before retiring anything, measure which rule IDs actually fired.** `audit_log` is configured in the same rules file. The question "which of these 20 rules interrupted me, how often, and on what command" is answerable from evidence rather than memory, and it is the difference between deleting five bad regexes and deleting the phase's headline feature.

  **Correction, 2026-07-16 (Phase 04 refinement, measuring rather than counting): the two struck claims above are false, and the advice that survives is the one that disproved them.** Read `.agent/logs/file-access-guard.ndjson` — it existed the whole time and had never been opened. 22 events from one session, **all 22 `tool: "Bash"`**: 18 `deny`, 4 `ask`. `kubeconfig-file` 10, `ssh-rsa` 5, `credential-json` 3 — **every one a false positive**; `destructive-rm-recursive-force-variants` 3 (correct); `environment-printenv` **1**. The denies are not silent, they are 82% of observed traffic, and they hard-block with no override. The environment probes predicted to be the main irritant fired once. Not one of the 18 denials was provoked by anything resembling a credential.
- **The root cause is extraction, not policy, and no rule is at fault.** `_candidate_paths` in `lib/bash_analyzer.py` extracts **grep's pattern operand as a filesystem path**. `evaluate_path` normalizes it against the repo root, and `_glob_patterns_overlap` in `lib/file_access.py` then asks whether the candidate glob and the rule glob could both match some string — building the witness from literals scraped from **both**: `re.findall(r"[A-Za-z0-9_-]+", first + " " + second)`. For `foo*` against the rule pattern `*kubeconfig` it synthesizes `fookubeconfig`, sees both match, and denies. **Any candidate ending in `*` overlaps any rule.** `grep -rn "test*" .` is hard-denied as a Kubernetes credentials access. Phase 04 fixes the grammar; **no rule pattern is edited and none is deleted.**
- **`_glob_patterns_overlap` looks wrong and is right — do not "fix" it.** It is exactly what makes `cat ~/.ssh/id_*` deny correctly. Rebuilding the witness from the candidate's own literals — the obvious cleanup, and the fix proposed and abandoned during this refinement — silently breaks real secret detection while making every grep test pass. Verified by execution: `cat ~/.ssh/id_rsa` DENY, `cat ~/.ssh/id_*` DENY, `grep -rn "foo*" .` DENY (wrong), `grep -rn "hello" .` clean.
- **Coverage hole found while proving the above: `ls ~/.ssh/id_rsa` is clean** while `cat ~/.ssh/id_rsa` denies. `ls` is not in the reader command set. Recorded with routing (Medium — `ls` discloses existence, not contents), not fixed in Phase 04.
- **The generalizable lesson, and it cost this project a near-miss on deleting its headline feature: counting rules is not measuring behavior.** The struck analysis was careful, quantitative, and derived entirely from the *shape of the config* — 20 ask rules, 32 deny rules, therefore prompts come from ask rules. Every number in it was correct. The conclusion was still wrong, because a rule's tier tells you what it does *when it fires*, never *whether it fires*. **When an instrument exists, reasoning from structure instead of reading it is a choice, not a constraint** — and a confident, numerate analysis is the kind most likely to go unchecked. The one instruction in this entry that pointed at the log is the one that held.

## File-Access Guard Retirement (proposed 2026-07-16; RESOLVED at Phase 04 refinement 2026-07-16 — fix, do not retire)

- **Decision: the guard is fixed, not retired.** Taken at Phase 04 refinement after reading the audit log (see the Correction above). The retirement was proposed on friction grounds, and the friction turned out to be a bounded extraction defect — grep's pattern operand evaluated as a filesystem path — rather than a policy outcome. Fixing the grammar removes ~82% of observed events while editing zero rules. The 32 deny rules, the 20 ask rules, `_glob_patterns_overlap`, `lib/file_access.py`, and `lib/bash_analyzer.py` all stay. Phase 04 owns the fix; the separability audit below is retained as accurate reference in case the question reopens.
- **The user's stated intent was to retire the file-access guard and keep the hook framework.** Recorded 2026-07-16 during Phase 03 decomposition, explicitly as intent rather than a decision — the call was reserved for `@phase-refiner` on Phase 04. The stated reason was friction: the guard judged more trouble than it was worth, while the framework stays wanted for the hooks Phases 05 and 06 plan to build. **The complaint was legitimate and was underestimated, not overstated** — `grep -rn "test*" .` was being hard-denied with no override. Deferring the call to a refinement that would measure first is what turned a headline-feature deletion into a grammar fix.
- **The general lesson: "this tool annoys me" is a bug report, and it deserves a diagnosis before it gets a verdict.** Both available framings — *retire it* and *it's only five bad regexes* — were wrong, and both were arrived at without reading the instrument. Taking the complaint seriously enough to measure it served the user better than either honoring it or arguing with it would have.
- **The guard is cleanly separable, verified 2026-07-16.** `lib/bash_analyzer.py` is imported by exactly one consumer, `scripts/file-access-guard.py`, and itself imports `lib/file_access.py`. Nothing else imports either. `scripts/injection-scanner.py` and `lib/injection_scanner.py` import neither, so **Phase 02 is unaffected**, and `lib/framework.py` is not involved. The retirement unit is: `scripts/file-access-guard.py`, `lib/file_access.py`, `lib/bash_analyzer.py`, `config/file-access-rules.json`, `config/file-access-overrides.json`, `.github/hooks/file-access-guard.json`, their tests under `tests/hooks/`, and the propagated wiring in all three generated roots.

  **Correction, 2026-07-16 (Phase 04 refinement): the import graph is right, the retirement unit is incomplete on three counts.** **(1)** `lib/url_exfiltration.py` is **guard-only, not scanner-adjacent** — its only importers are `lib/bash_analyzer.py` and `scripts/file-access-guard.py`, and its policy lives in the `url_exfiltration` block of `config/file-access-rules.json`. Neither injection-scanner module references it. Retiring the guard **orphans 344 lines with zero callers** and deletes its config with the rules file; the original entry lists it on the scanner's side of the cut, which is backwards. **(2)** `tests/hooks/test_injection_scanner.py` imports `lib.file_access` and reads the rules file to assert the `self-hook-assets` deny rule protects the scanner's own configs — a real guard→scanner test coupling, and a protection property that dies with the guard. **(3)** Three test files mix guard assertions with scanner/propagation assertions and need surgery rather than deletion: `test_hook_distribution_integration.py`, `test_injection_scanner.py`, and `test_propagate_master_assets.py` — the last uses the guard as its **fixture vehicle** in `_seed_hooks`, so ~15 propagation tests assert on `$source == "file-access-guard"` while testing nothing about the guard. Propagation itself needs only a `RETIRED_HOOK_ASSETS` addition; the hook list is discovered by glob, not hardcoded. **The lesson: "nothing imports X" answers whether X can be removed, never what removing X leaves behind.** A separability audit needs the reverse direction too — what becomes unreachable, and what was quietly leaning on it as scaffolding.
- **This is a Phase 01 retirement that Phase 04 would verify — not a Phase 04 edit.** Phase 01 is named "Hook Foundation + File-Access Guard" and the guard is its headline deliverable; the roadmap Vision sells "hardens every project against prompt injection and file/secret manipulation — even under bypass permissions," and the bypass-permissions claim is the guard's alone. Retiring it changes Phase 01's status, the Vision paragraph, and the "Why hooks, not permissions" architecture note. That is `@project-planner` surface, not a phase-local scope trim.
- **Most of Phase 04 is guard work, so retirement moots it rather than shrinking it.** PERF-01 (the propagated-*guard* latency budget), the bash-rewrite bypass (which is about the *guard's* classification of a command being invalidated by `rtk-rewrite.sh`), and the security review of the 17 loosened guard rules all evaporate. What survives: the Phase 02 security-gate re-run, live Claude/Codex/OpenCode QA, REPO-SEC-06, and records reconciliation. **PERF-01 is Phase 01's release blocker**, so retiring the guard does not just delete work — it changes which phases are releasable and why. Weigh that at refinement: the tidiest outcome of "I dislike this feature" should not be an accidental release unblock.
- **Retiring the guard deletes the repo's only bash-command parser.** `lib/bash_analyzer.py` goes with it, since the guard is its only consumer. That is precisely the component a future per-agent command-allowlist hook would reuse (see the Phase 03 allowlist finding below). Not an argument against retirement — an argument for recording what the deletion costs, so a later phase does not rebuild it believing it never existed.

## PR-Review Rescope (Phase 03; resolved 2026-07-16)

- **`05-phase-final-review` is rescoped into `05-pr-review`, gating diffs on the current branch against its base.** Decided 2026-07-16. The original scope — evaluate a whole phase divided into subphases `PHASE_0Na`–`PHASE_0NX` — was not the right shape. The replacement runs when a branch is ready to PR.
- **The rescope lands in Phase 03 itself, not a new phase, and this is what dissolved the numbering collision.** Phase 03 is where the agent family was built, so amending its scope needs no new roadmap entry and no renumber. The alternative was ugly: `05` and `06` are already Format-on-Save + Completion Gates and Skill Enforcement, so a new phase at `05` meant another renumber — and the 2026-07-16 renumber is recorded below as having silently changed the meaning of the plugin-packaging deferral — while appending at `07` would have put the number out of execution order, the very thing the last renumber existed to fix. **The general lesson: when a rescope has no clean home, check whether the originating phase is the home.** Reopening a phase's scope is cheaper than renumbering around it.
- **The evaluator roster splits roughly in half, and this is what makes the rescope tractable.** Seven of twelve are already diff-shaped and transfer directly — some fit *better* than they do now: `05a-baseline-worktree` (checks out a baseline commit → the base branch), `05b-change-narrator` (narrative baseline→HEAD → the PR's diff), `05g-artifact-sweeper` (debug statements/TODOs since baseline), `05h-test-health` (coverage delta), `05j-consistency-auditor`, `05k-dependency-auditor`, `05l-readiness-synthesizer` (go/no-go → PR gate verdict). **Five are phase-shaped and are retired**: `05c-qa-consolidator` (merges *subphase* QA docs), `05d-security-rollup` (union of *subphase* findings), `05e-ac-regression` (re-verifies *every subphase's* ACs), `05f-seam-analyzer` (seams *between subphases*), `05i-learnings-harvester` (mines *pipeline review records*). A PR has no subphases and no ACs. Little working code is lost — the whole-phase flow has never successfully run against a real phase.
- **Git cannot determine a branch's base. This is a data-model fact, not a tooling gap — do not design around an assumption that it can.** A ref is a SHA and nothing else; there is no parentage metadata anywhere. Verified 2026-07-16: `git merge-base HEAD main` works but requires already knowing the base (circular); the reflog records `branch: Created from HEAD` — the *SHA*, never the branch name — and is local-only, never cloned, and gc-pruned (90 days default), so it is absent in CI and fresh clones; `git symbolic-ref refs/remotes/origin/HEAD` is the most reliable signal but yields the repo's *default* branch rather than *this branch's* base, and is frequently unset (needs `git remote set-head origin -a`). **The chosen design is suggest-and-confirm**: infer a candidate from `origin/HEAD`, compute `merge-base`, show the implied diff scope (commit count, files touched), let the user accept or override. This matches the existing `05` preflight pattern (auto-suggest the baseline commit, user confirms) and fails safe — an unset `origin/HEAD` means asking rather than guessing. Suggestion order is `origin/HEAD` → `origin/main` → `origin/master` → present candidates for selection. Cases where inference is actively wrong and must be named in the agent: a branch cut from another feature branch (merge-base against the default silently includes the parent's work in the diff), a rebased branch, and a squash-merged base.
- **The nearest-merge-base heuristic returns the branch under review. Exclude self and self's tracking ref explicitly.** Demonstrated 2026-07-16 on branch `repo_improvements_project` at HEAD `ae9823a`: `git merge-base HEAD main` and `git merge-base HEAD origin/main` both give `e3398c7`, but `git merge-base HEAD repo_improvements_project` and `git merge-base HEAD origin/repo_improvements_project` both give `ae9823a` — HEAD itself. **A branch is always its own nearest base, and so is its remote-tracking ref.** Any ranking over candidate branches must filter both before comparing.
- **The rescope inherits Phase 03's open findings rather than leaving them for Phase 04.** P5-SEC-02 (readiness path consumes report claims after metadata-only validation) is the notable one: it was unclosable because the readiness path is agent Markdown with no code to attach a schema and deterministic reducer to. ~~**The rescope rebuilds that path, so the validator arrives with the rebuild instead of being new capability bolted onto prose.**~~ Also inherited: `execute` grants on `05`/`05g`/`05j`/`05k` (set them correctly when each agent is rebuilt, rather than fixing them twice — note `05k` is not a simple removal, its contract permits an offline read-only audit command); `05a`'s unconstrained `execute`; and the propagation-enumeration gap omitting `05g`/`05j`/`05k` (only correct once the roster is settled at seven contiguous slugs).
  **Correction, 2026-07-16 (`08-retirement-reconciliation`, verifying as-built): the struck
  sentence is false, and P5-SEC-02 is still open** — see the standing entry under Deferred
  Pipeline Work. The rescope rebuilt the readiness path **as agent Markdown**, not as code,
  so the validator did not arrive with the rebuild and there is still nothing to attach a
  schema or reducer to. Feature `07` recorded it open rather than tightening prose to look
  closed. **The lesson, generalized by `07` and worth keeping: "the rebuild will bring the
  validator" is a prediction, not a plan.** A finding routed to a future rebuild must name
  the capability that rebuild has to gain; otherwise the rebuild lands without it, and the
  finding reads as overdue rather than as correctly deferred.
  **Second correction: the enumeration gap was four agents, not three — `05a`, `05g`, `05j`,
  `05k`.** This sentence drops `05a` while the same entry discusses `05a`'s `execute` one
  clause earlier, which is the tell: `05a` is the one evaluator whose display name carries no
  numeric prefix (`Baseline Worktree`, not `05a Baseline Worktree`), so every roster
  eyeballed by display name loses it silently. It was missing from `expected_slugs`, from the
  agent catalogue, and from this very list — three surfaces, same blind spot. **A member that
  does not match the naming convention of its own set will be dropped from every hand-built
  enumeration of that set, and its absence will look like the set.**
- **The propagator's missing `execute` allowlist syntax stopped being a residual risk the moment a feature needed it.** `scripts/propagate_master_assets.py:332` maps `"execute": ["Bash"]` and `:353` maps `"execute": ["bash"]`; there is no allowlist syntax, so every narrow grant — `05a`'s `git worktree`, the orchestrator's `gh` — is inexpressible and gets recorded as accepted risk instead. It sat open because nothing forced it. The opt-in PR-comment feature needs `gh`, and "grant `gh`" is mechanically "grant every shell command," which two recorded decisions prohibit. **So the allowlist became Phase 03's first deliverable, and closing it closes the `05a` and mechanical-sweep grants as a side effect.** The general lesson: a capability gap recorded as accepted risk will stay open indefinitely unless some feature's correctness depends on closing it. Look for the forcing function rather than re-recording the risk.
- **Correction, 2026-07-16 (decomposition): the allowlist forcing function above is void — per-agent command scoping is not expressible on Claude at all, so the propagator was never the binding constraint.** Verified against current Claude Code docs: a subagent's `tools:` frontmatter accepts only bare tool names and MCP patterns; `tools: Bash(gh:*)` is not a narrower grant but an *unresolved tool name*, and Claude Code refuses to launch the subagent. Subagents have no `permissions`/`allowed-tools` key; `permissionMode` selects how prompts are handled, never which commands are allowed. Command scoping exists only in project/session-wide `settings.json` permission rules — which are not per-agent — or in a **per-agent PreToolUse hook**, which Phase 03 excludes. Harness survey: **OpenCode** supports real per-agent `permission.bash` globs (last-match-wins, so the `"*"` catch-all must come *first*, and patterns match parsed commands — `"git status"` will not match `git status --short`; use `"git status *"`); **Codex** has no per-profile command list at all (`ConfigProfile` carries only `approval_policy`, `approvals_reviewer`, `sandbox_mode`, `tools`), and its execpolicy rules are global, sandbox-escape-only, Starlark, and experimental. So native per-agent scoping exists on **one of three harnesses**. Building the syntax anyway would be real on OpenCode and decorative on Claude and Codex — the "partial protection that reads as total protection" failure recorded under adoption readiness, aimed at ourselves.
- **The sharper correction: the `gh` grant never cost anything.** The premise was "grant `gh` = grant every shell command, which two decisions prohibit." But the orchestrator needs `git symbolic-ref`/`git merge-base`/`git branch` for base derivation, so it holds unrestricted Bash *regardless* of the PR-comment feature. Adding `gh` widens nothing. **The general lesson, and the reason this is worth recording rather than quietly fixing: "look for the forcing function rather than re-recording the risk" was good advice that found a fake one.** A forcing function is only real if the feature is actually blocked without the capability — check that the blockage exists before promoting it to Deliverable 1. Here the blockage was assumed from the propagator's source mapping without checking whether the *target* format could express the result.
- **Decisions taken in refinement, 2026-07-16.** Pipeline artifacts are **optional enrichment** — the run proceeds on the diff alone and says what evidence was unavailable; this is also the boundary that keeps PR Review from being a duplicate of `prod-code-review` (document-driven, phase-scoped) rather than a complement (diff-driven, branch-scoped). **No verdict write-back**: the report file is the verdict, which deletes the two-file transactional status-line edit, its unique-match ambiguity detection, and its restore-on-second-write-failure path — the riskiest implemented code in the phase, now with no reason to exist. **The five phase-shaped evaluators are deleted** from source and from all three generated roots; **the seven survivors renumber contiguously to `05a`–`05g`**. **Reports land at `dev/pr-review/<base-sha-short>-<UTC-timestamp>/`** — keyed only by hex and digits, so no branch name reaches a filesystem path and no sanitizer exists to be wrong; every run owns its directory, which also deletes archive-before-overwrite. **The verdict is advisory**; a hook that blocks push or merge on `NO-GO` is deferred to a hook-owning phase. **Security is delegated to the existing `04e-diff-security-scan`**, which is already diff-shaped and already holds no `execute` — no new security agent is authored.
- **Removing the multi-subphase premise deleted work rather than moving it, and that is the shape to expect from a good rescope.** Gone entirely: subphase discovery, ledger parsing and multi-run disambiguation, the `eval:` commit-message fallback, the "ledger reality" dependency and risk, the artifact-inventory refusal gate, verdict write-back, and archiving. `merge-base` replaced all of the baseline machinery. Phase 03 dropped from Large to Medium. **If a rescope only relocates work, suspect the new scope is the old scope wearing a hat.**
- **One upfront interaction is a design outcome, not a politeness feature.** The requirement was that questions arrive before the run so an unattended run is never found stuck. It became achievable only because the decisions above removed every other blocking question: with ledger disambiguation, artifact refusal, and write-back ambiguity all gone, **base confirmation is the only blocking question left**, and the PR-comment choice joins it in the same block. The subtlety worth keeping: **a question asked after the work is on disk blocks nothing.** That is what makes "ask me once the report is written" both unattended and safe — the user sees the content before it is published. Guard this: it is the requirement most likely to erode silently, one reasonable-seeming question at a time.
- **Phase 03's verdict is NO-GO, issued in Phase 07 from existing evidence, and superseded rather than repaired.** The work happened and seven evaluators carry forward, so this is honest history rather than abandonment. The general principle worth keeping: **when a deliverable is slated for rescope, verifying it as-built is archaeology.** Phase 07 dropped its agent-family work for exactly this reason and got smaller and more coherent as a result — it is now hooks-only.

## Propagation Contracts

- The current master-asset propagator's generated roots are `claude/`,
  `opencode/`, and `codex/`; `.claude/skills/` and `.claude/agents/` are
  not generated destinations. Future feature plans must name the actual roots
  or explicitly add an adapter.
- `$source` metadata is guaranteed for propagated hook JSON entries, not for
  generated skill Markdown or agent Markdown/TOML. Downstream checks must not
  require that metadata on non-hook assets without a corresponding propagator
  change.
- **All Markdown generated roots now carry a generated marker, and the propagator
  prunes orphans in all eight roots** (`01-propagator-orphan-pruning`). The marker
  is `GENERATED_AGENT_MARKDOWN_HEADER` for `claude/agents`, `claude/commands`, and
  `opencode/agents`; `GENERATED_SKILL_HEADER` for the three `*/skills` roots;
  `GENERATED_AGENT_HEADER` for the Codex TOML roots. Generated skill `SKILL.md`
  files are therefore **no longer byte-identical to their `.github/skills/` source**
  — they differ by exactly the marker line. Any future check that assumes byte
  identity between source and generated skill output must be updated.
- **Deletion is gated on the marker, so a file orphaned before the marker existed
  is unmarked and permanently unprunable.** This is a structural limitation of the
  marker approach, accepted deliberately because it fails closed. Blast radius
  measured at exactly one file (`claude/agents/single-feature.md`), owned by
  `08-retirement-reconciliation`. Any future asset rename must land while the
  propagator is marker-aware, or it leaves an orphan no sweep will ever collect.
- **A `--watch` propagator holding pre-marker code is a silent-failure hazard.** It
  rewrites generated roots without markers using stale code, disabling every prune
  while the code still reads as correct. Restart the watcher after any propagator
  change before trusting a propagation run.
- **Propagation is not idempotent across a reclassification: one run does not prove
  convergence — run until every counter is zero.** `_claude_filename_for` resolves an
  output name against the stems already on disk, and pruning deliberately runs *after*
  emission (so a survivor is never handed a different filename mid-run). The two
  together mean that when an agent changes emission class, the stem it resolved
  against is only deleted at the end of that run, so the *next* run computes a
  different identifier. Retiring `05d-security-rollup` reclassified `Security Scan`
  from dual-use to command-only and took **three** `--once` runs to reach a fixed
  point (prune+reclassify → rename the command → settle `codex_profiles`). A single
  run leaves the tree valid-looking but non-converged, and the committed roots are
  then not a pure function of source. No test asserts this: the existing
  `test_phase02_generated_wiring_is_complete_and_idempotent` covers
  `propagate_hooks_once`, not `propagate_once`. Fixing it means changing identifier
  resolution to derive from source rather than disk state. (Recorded 2026-07-16 by
  `02-retired-evaluator-removal`'s review; first triggered there.)
- **An agent that is user-invocable *and* declared as some orchestrator's child is
  "dual-use" and gets both a slash command and a spawnable subagent file. Deleting its
  last parent silently reclassifies it, which can rename a user-facing command.**
  Retiring `05d` dropped `Security Scan` from `_referenced_agent_names`, removing
  `claude/agents/z-security-scan.md` and renaming `/z-security-scan` → `/security-scan`.
  That rename was a correction — `z-` marks hidden subagents, and OpenCode/Codex already
  used the bare name — but the general lesson is that **deleting an orchestrator can
  change the public name of an agent it merely referenced.** Before retiring any agent,
  check what its `agents:` roster is the last declarer of.

## Review Contracts

These are scope-independent. They were learned building the whole-phase review and carry into PR Review unchanged, because none of them is about phases — they are about not reporting an absence of evidence as evidence of absence.

- Missing or incomplete required checks are a hard readiness gate: the canonical verdict is `NO-GO`. An unverified verdict must not update roadmap or summary status lines. In this project verdicts are issued by the user by hand; no agent writes a status line.
- A failed, hung, or unavailable evaluator never becomes a passing result, and a later evaluator's success never repairs an earlier one's failure. Every such case gets a record naming the evaluator, the check, and a concrete reason, and the readiness report must enumerate them by name.
- Report validation is metadata-only at the orchestrator (readable, regular, non-empty, under the run's report root) and must not be mistaken for validating a report's *claims*. Validating claims requires a strict schema and a deterministic status reducer over structured records — this is P5-SEC-02, and it is closed by rebuilding the readiness path in code rather than asserting it in prose.
- Diff-scoped evaluators that call repo-wide analysis must require verifiable added-line attribution; touched-file filtering alone is insufficient.
- Read-only dependency vulnerability checks must use supplied local evidence or an explicitly offline audit mode; network-capable commands are treated as unavailable.
- Fixture dry-runs remain required release evidence for agent wiring and degradation behavior. Static contract review cannot observe runtime report creation, and a run whose required evaluators are recorded `not-run` is artifact-level, below-GO evidence — not a passing dry run.
- **Never restore unrestricted shell/Bash permissions to satisfy an evaluator acceptance criterion.** This bound `05i`'s history mining, which is retired; the rule outlives it and now governs the `gh` grant. The correct move is a narrowly scoped capability — an offline audit mode, a verifiable evidence bundle from the orchestrator, a command allowlist — never a broad grant with a comment explaining why it is fine.

## Mechanical Evaluator Grants (resolved at feature 05)

- **The mechanical sweeps hold no shell grant.** `05c-artifact-sweeper`, `05d-consistency-auditor` and `05e-dependency-auditor` all carry `[read, search, edit]`. The removal bar — name a command with no non-shell equivalent, or the grant goes — could not be met for any of them, including the dependency auditor, which was the anticipated exception.
- **The offline dependency audit is now a capability boundary, not a policy.** The earlier contract permitted an offline read-only audit command and trusted the agent to stay local. With the grant gone, the contract cannot be violated by a lapse in judgment. The cost is declared and load-bearing: vulnerability evidence comes only from artifacts supplied to the run, and their absence is `NOT RUN`, never a pass. Do not reintroduce the grant to restore a scanner; supply the artifact instead.
- **The architectural reason the removal is safe, and the precedent for future grant audits:** `05a-baseline-worktree` holds the one `execute` recorded as unclosable (`git worktree`) and returns a path; every other evaluator reads two trees. `05b-change-narrator` — whose entire job is the diff — has always operated this way with no shell. The baseline worktree *is* the non-shell equivalent of `git diff` for this family. Any future proposal to grant shell to an evaluator must first explain why reading `05a`'s worktree is insufficient.
- **`05c` and `05d` depend on the code-review-graph MCP; `05e` does not.** The graph is an availability dependency, not a preference: unavailable means `NOT RUN` with a reason and a verdict-ceiling drop, never a silent downgrade to grep. `05d`'s dependency was added at feature 05 because the rescope removed its previous source of canonical forms (subphase comparison); it degrades partially rather than going dark — drift evidenced from the diff is still reported, with its recommendation marked not-derived. MCP tools are not declared in agent frontmatter anywhere in this repo, so `tools:` lists neither grant nor withhold graph access.
- **Propagation enumeration is closed by derivation, not by listing.** The evaluator roster in `tests/test_propagate_master_assets.py` is read from disk and asserted against a per-agent tool map, because a hand-written list cannot satisfy a requirement that omission fail — omission from a literal is silent by construction, which is how the original gap arose. Grants are pinned per agent in both directions: `edit` is required (these agents write their own reports, and "read-only, never remediate" reads as license to strip it), and `execute` is declared rather than hidden. Renaming an agent without renaming its key in that map fails, by design.
- **Open for feature 08:** the four agents historically missing from `.github/agents/README.md` are precisely the four that were missing from `expected_slugs` — the same four `execute` holders. The enumeration gap is closed; the README gap is not (`05a-baseline-worktree` remains unlisted). The correlation is pre-existing and unconfirmed, but a reconciliation pass should assume the two omissions share a cause. Nothing yet asserts that the orchestrator's dispatch roster resolves to agents that exist on disk — a real gap, and feature 08's to close.
- **Behavioral evaluator ACs are not closable by static contract tests.** Feature 05's attribution, report-path and tier contracts are pinned in prose and mutation-verified, which proves the bodies *say* the right thing and that the guards bite. It does not prove the agents *behave*. A sweep that reports pre-existing findings as branch-introduced looks exactly like a working sweep. The fixture dry-run remains outstanding release evidence for these.

## Phase 04 Runtime Deployment Contract (verified 2026-07-17)

- Runtime deployment uses one ordered path: repository convergence, destination
  preflight, classified inventory, immediate inventory recheck, managed-copy
  deployment, owned reconciliation, and regular-copy verification.
- Human review is bound to the exact home-relative inventory and generated-source
  fingerprints by SHA-256. A missing digest returns `review_required`; a changed
  digest returns `inventory_drift`; neither state permits a runtime write.
- Scratch-home automation is not live-platform evidence. macOS, Linux, native
  Windows, and WSL retain separate evidence rows, and any `NOT RUN` row caps the
  full cross-platform verdict below GO.
- Phase 04 does not move Phase 01, Phase 02, or Phase 07 status lines. Those remain
  project-level reconciliation work.

## Project-Planner Reconciliation (2026-07-17)

- **Resolved: Phase 04 did retire the guard, not fix it — the "fix, do not retire" decision recorded above under "File-Access Guard Retirement" was superseded.** That entry, dated 2026-07-16, records a refinement-time decision to fix the extraction defect rather than delete the guard. `docs/phases/PHASE_04/PHASE_04_SUMMARY.md`'s scope and its "Implementation Verification (2026-07-17)" section instead show the guard, its Bash analyzer, and `rtk-rewrite.sh` fully removed, with automated scratch-home evidence for the retirement and no trace of a grammar fix. The as-built state is retirement; the 2026-07-16 note is left in place, struck nowhere, because it is accurate history of a decision that was later reversed — read it as *what was decided then*, not *what shipped*. Anyone reasoning from that entry alone would conclude the guard still exists; it does not.
- **`docs/phases/PROJECT_ROADMAP.md`, `docs/phases/PHASE_01/PHASE_01_SUMMARY.md`, and `docs/phases/PHASE_07/PHASE_07_SUMMARY.md` are reconciled to the as-built (retired) state.** Phase 01's status line now reads "partially retired"; its guard/analyzer deliverables (2 and 3) are marked retired in place rather than rewritten out, with a retirement note pointing at Phase 04. Phase 07 drops PERF-01, the bash-rewrite bypass fix, and the 17-rule guard review (all moot — nothing left to time, bypass, or review) and shrinks from Large to Medium; its Phase 02 gate re-run, REPO-SEC-06, live QA, and record-reconciliation deliverables survive unchanged. The Vision paragraph and two Architecture Notes bullets ("Enforcement posture", "Why hooks, not permissions") no longer describe file-access enforcement as live.
- **The general lesson: a superseded decision recorded as resolved does not update itself when later work reverses it.** The 2026-07-16 "fix, do not retire" entry was correct when written and was never wrong on its own terms — Phase 04's later scope simply chose differently. Nothing forced the roadmap, Phase 01, or Phase 07 to notice; the roadmap had in fact already flagged the gap itself ("`project-planner` must reconcile the affected phase documents... before their release path is treated as authoritative"), which is what this reconciliation closes. Any cross-phase-decisions entry describing a decision should be treated as time-stamped intent, not as a live contract — check the phase's own summary and its "Implementation Verification" section for what actually shipped before trusting an earlier decision note.

## Phase 07 Rescope: Package for General Use (2026-07-17)

- **Phase 07 is rescoped from "Hook Release Remediation & Verification" to "Package for General Use", and moved from 5th in execution order to last (after Phases 05 and 06).** Decided at Phase 07 refinement 2026-07-17. The trigger: the user established that the hook suite protects only this repository — `--runtime-deploy` ships agents/commands/skills/learnings but no hooks (`scripts/runtime_deployment.py` `_ASSET_POLICIES`), and hook wiring is generated only into this repo's own config surfaces. Spending a phase verifying an undistributable suite was the wrong next investment; distribution is what makes the hook work meaningful. The prior verification scope (Phase 02 gate re-run, REPO-SEC-06, live multi-harness QA, record reconciliation, Phase 02/03 verdicts) is **absorbed as the rescoped phase's tail, not dropped**.
- **This closes the "adoption readiness is unplanned work with no roadmap entry" item above.** Phase 07 now owns: packaged global install via a `hooks` asset class in the managed-copy flow, user-level wiring registration, per-repo opt-out, stranger-grade install/upgrade/recovery docs, and install-time per-harness disclosure. Public registry publication stays out of scope.
- **All three harnesses support user-global hooks — verified from primary sources 2026-07-17** (report: `dev/research/codex-hooks-mechanism/`). Claude Code: `~/.claude/settings.json`. OpenCode: global config/plugin dir. Codex: `~/.codex/hooks.json` / `[hooks]` in `~/.codex/config.toml`, additive merge with repo layers, Claude-Code-shaped events and decision protocol. Codex caveats to carry: per-hook hash-based trust (regeneration requires re-trust via `/hooks`, so upgrades are non-silent), only "simple" `unified_exec` shell calls intercepted, `codex exec` repo-hook dispatch bug (#26383/#26452 — user-global layer behavior unverified), minimum version ~v0.123 (Apr 2026), enterprise `allow_managed_hooks_only` can suppress everything.
- **Accepted consequence: Phase 02 carries its NO-GO (unverified) status through Phases 05 and 06**, since its verdict evidence (live QA, gate re-run) now lands last. Accepted because the scanner protects only this repo until Phase 07 ships anyway. **Anywhere above that says Phase 07 "runs before Phases 05 and 06" or is "required by" them predates this rescope** — those notes are left as written per this file's convention; execution order is now 01 → 02 → 03 → 04 → 05 → 06 → 07.
- **The live PR Review run finally started.** During this same session the user launched `05 PR - Review` against a real external repo — the first end-to-end run of the family, previously recorded above as "STILL UNEXECUTED" and the phase's largest open risk. Its outcome is verdict-evidence input for Phase 07's deliverable 6; the "STILL UNEXECUTED" entry above should be updated with the result once known.

## Narrative and Test Health (resolved at feature 06)

- **The report-root migration ledger is now one entry from empty.** `EVALUATORS_AWAITING_REPORT_ROOT_MIGRATION` in `tests/test_pr_review_orchestrator.py` holds only `05l-readiness-synthesizer.agent.md`, which feature 07 owns. When 07 migrates it, the set is empty and `test_report_root_migration_cannot_split_silently` should be deleted rather than left asserting an empty set. Note the shape that made this safe to shrink: the compared set is *derived from disk* and asserted by exact equality, so removing an entry is reconciliation, not exemption — a regressing agent re-enters the derived set and fails. Verified by mutation at feature 06. A ledger keyed to a hand-written allowlist would not have this property; do not replace it with one.
- **Codex `max_depth` is an operator prerequisite that no repository artifact can enforce.** `[agents] max_depth = 2` lives in `~/.codex/config.toml` and is global, not a per-agent field — the propagator emits no such key and none of the three generated roots can carry one. Both `05f-test-health` (to `Test - Analyst`) and `05b-change-narrator` (to per-directory readers) spawn at depth 2 through the orchestrator. With the default of 1 the spawn is blocked, the model **silently does the work inline and reports success**, and the output is indistinguishable from real delegation. Both bodies name the trap; nothing can assert it. **Any future AC of the form "agent X demonstrably delegates to Y" is unverifiable by static test and must route to a runtime transcript.** Do not accept a green declaration assertion as covering it — it passes in exactly the failure case. Recording the prerequisite in operator documentation is open for feature 08.
- **The no-`execute` grant is what structurally prevents `05f-test-health` growing a coverage runner.** Neither `05f` nor its delegate `test-analyst` holds `execute`, so no agent in the chain can measure coverage at any revision. This is a capability boundary, not a policy: `05f` reports a *measured* coverage delta only when the orchestrator supplies coverage evidence for both revisions, and otherwise reports **not-measurable** plus the structural suite delta derived from reading both trees. The degradation is deliberate and is the honest one. Absence of coverage tooling in a consuming repository is a stated limitation, never a failure. Do not close this gap by granting `execute`; supply the evidence artifact instead — the same resolution feature 05 reached for the dependency audit.
- **Inert guards are a recurring phase-level defect, not a per-feature lapse.** Feature 06 self-caught five and shipped four more, found at review by an independent sweep; earlier features had five found only at review. Every guard in this family asserts on prose, and prose restates its own vocabulary, so short-phrase membership checks are inert by default. Treat a "zero inert" claim as unverified until a sweep that *negates load-bearing sentences* — not merely damages the named phrase — reproduces it.
