# Phase 1: Unity Headless Test Execution

**Status**: In Progress
**Depends on**: None
**Estimated complexity**: Medium
**Cross-references**: None — single-repository phase
**Readiness verdict**: NO-GO — source authoring is implemented; required runtime evidence and a green final gate are outstanding

## What's New

Agent-driven Unity tests use a headless three-rung execution contract. The primary path targets one
persistent detached shadow worktree, keeps EditMode non-graphical, keeps PlayMode graphics enabled,
and writes XML and logs to absolute paths in the main checkout. If a license or project lock blocks
the shadow worktree, the agent asks for the main Editor to close and runs the test itself in the main
checkout. It never launches a GUI or delegates test execution to the user.

Unity's serializer remains authoritative for `.meta` files and asset GUIDs. The corpus documents a
headless asset-database import command without requiring a human-opened Editor, while treating actual
missing-`.meta` regeneration as unverified until a controlled run succeeds on the target project.

The phase contains an inert GameCI workflow template and a 14-step local testing runbook. The
workflow is not installed anywhere. It requires GitHub Actions semantic validation and full-SHA
action pinning before activation. The phase has no visual acceptance criteria, so screenshot capture
is not part of its evidence.

## Objective

Make every agent-driven Unity test run headless and agent-owned by defining a persistent shadow
worktree as the standard CLI execution target, with a bounded fallback when a second concurrent
Unity process is unavailable and honest `not-executed` reporting when evidence cannot be obtained.

## Scope

### In Scope

- The **Test Execution** section of `source_of_truth/skills/unity-development/SKILL.md` defines:
  - `-batchmode` as **mandatory** at every execution tier.
  - The graphics flag is stated **per test platform, as a two-row table**: EditMode runs use
    `-batchmode -nographics`; PlayMode and visual-capture runs use `-batchmode` with graphics
    enabled, because `-nographics` prevents rendering and would break visual verification.
  - The prohibition on pairing `-quit` with `-runTests`.
- A **three-rung execution ladder** owns lock and licensing behavior:
  1. Commit the working tree, refresh the persistent shadow worktree to that commit, run headless
     in the worktree. The maintainer's Editor stays open and usable.
  2. If the worktree run fails on licensing or a lock, ask the user to close the Editor, then run
     headless in the main checkout.
  3. Never silently refuse, and never launch a GUI. `not-executed` is reachable only when the user
     declines rung 2, or when the agent is running unattended and no response arrives — a
     non-response is treated as a decline and reported as `not-executed: editor open, user
     unavailable`.
- Test results are always written to an **absolute path in the main checkout**
  (`dev/test-results/`), never to the worktree's copy of that path. The shadow worktree is a pure
  execution target; nothing ever reads output from it.
- The Unity binary is located by the **existing editor-discovery procedure** used by
  `04g-unity-visual-verification`, not by assuming a bare `Unity` is on `PATH`.
- **Commit-before-test is an explicit precondition** of the design: a worktree can only test
  committed code. In practice most runs need no extra commit because the Feature - Implementer
  already commits per feature; only a mid-feature run adds one.
- The **persistent shadow worktree procedure** covers detached checkout, sibling
  location, first-need creation with announced cost, indefinite persistence, refresh by checkout,
  `Library/` retention, `git worktree prune` on each use, manual teardown command.
- The **headless `.meta` / asset-import procedure** uses
  (`"<resolved-unity-editor>" -batchmode -quit -projectPath "<execution-unity-project>" -logFile -`)
  to request missing `.meta` and asset GUID generation, with the capability
  kept conditional until a controlled target-project run succeeds.
- The **Refactor / Rewire Test Preservation Rules** use the verified reference-project EditMode
  convention, `Assets/Tests/Editor`, and preserve `Assets/Tests/PlayMode` guidance.
- Two copyable reference assets exist: a GameCI GitHub Actions workflow template and a
  human-facing local Unity test runbook (TL;DR, then numbered steps).
- Every consuming agent follows the canonical contracts:
  `04-phase-execute.agent.md` (Step 2.5 wave test gate), `04g-unity-visual-verification.agent.md`,
  `04h-unity-reviewer.agent.md` (batch import / asset-integrity gate).
- Structural corpus tests cover every authored contract and include non-vacuous mutation proof.

### Out of Scope

- **Installing CI in any Unity repository.** No workflow is wired up, no Unity license secret is
  configured, no runner is provisioned. The workflow ships as an inert asset.
- **Any change to what Unity tests assert.** This phase changes how tests are invoked, never their
  content, and never the Test Authenticity Rules.
- **Removing the supervisor-attestation escape hatch** in `04-phase-execute` Step 2.5. It stays; it
  remains a narrow, explicitly identified evidence exception.
- **Visual verification redesign.** `04g` keeps its editor-location logic and its capture-config
  bootstrap; only its invocation flags and `-projectPath` target are touched.
- **Automated worktree teardown.** The shadow worktree is permanent by design. Teardown is a
  documented manual command only.
- Running `scripts/propagate_master_assets.py`. Source edits only; the maintainer propagates.
- Renaming, renumbering, or restructuring any agent.

## Key Deliverables

| # | Deliverable | Description | Likely Features |
|---|-------------|-------------|-----------------|
| 1 | Test Execution rules | `unity-development` Test Execution contract: mandatory `-batchmode`, per-platform graphics flags, no `-quit` with `-runTests`, absolute main-checkout evidence, and deployed editor discovery | Skill authoring |
| 2 | Execution ladder + shadow worktree procedure | Three-rung ladder covering commit-before-test, detached creation, sibling location, announced cost, indefinite persistence, refresh, `Library/` retention, prune, and manual teardown | Skill authoring |
| 3 | Headless asset-import procedure | Conditional `.meta` / GUID generation without a GUI, serializer authority, contradiction sweep, and the `Assets/Tests/Editor` convention | Skill authoring, corpus sweep |
| 4 | Consumer agent alignment | `04-phase-execute` Step 2.5, `04g-unity-visual-verification`, and `04h-unity-reviewer` consume the canonical contracts | Agent authoring |
| 5 | Reference CI workflow + local runbook | GameCI workflow template at `source_of_truth/skills/unity-development/references/`; runbook at `docs/unity/`. Both copyable, neither active | Asset authoring, docs |
| 6 | Structural tests | Guards proving the new rules are present and the deleted rule is gone | Testing |

## Execution Readiness

All four source-authoring features have implementation and review records. The current feature
verdicts are:

| Feature | Review verdict | Current evidence state |
|---|---|---|
| `01-unity-test-execution-contract` | Changes Requested | AC7/AC11 are `not-executed (main Editor-open condition unavailable)`; the closed-Editor XML is not concurrency or Editor-usability evidence. |
| `02-headless-asset-import` | Changes Requested | AC5 is `not-executed (reference project not clean)`; no `.meta` was withheld and Unity was not launched for import. |
| `03-unity-consumer-alignment` | Approved with Reservations | All 30 focused consumer guards pass; missing capture inputs fail non-green in a future visual phase. PHASE_01 has no visual ACs. |
| `04-unity-test-reference-assets` | Approved with Reservations | Structural and generic-YAML checks pass; `actionlint` is unavailable and the inert workflow has not run in GitHub Actions. |

The three manifest verification assets contain 99 passing focused guards:
`tests/test_unity_skill_contract.py`, `tests/test_unity_consumer_contract.py`, and
`tests/test_unity_reference_assets.py`. The authoritative safe final gate is
`dev/test-results/phase-01-wave-3-final-safe.xml`: 239 passed, 2 failed, 1 propagation fixed-point
test deselected, and 63 subtests. Both failures match the pre-phase baseline:

- `tests/test_pr_review_orchestrator.py::test_agent_name_does_not_collide_with_prose_in_any_source_asset`
- `tests/test_propagate_master_assets.py::InstructionApplyToTests::test_every_enumerated_applyto_target_exists`

The exact unfiltered suite is not run by agents because its fixed-point test invokes propagation
against the working tree. The final gate remains `executed-failing` even though both failures predate
this phase. The diff-scoped security verdict is PASS WITH CONDITIONS: 0 Critical, 0 High, and 1
Medium finding. Before activation, every action in the inert workflow must use a verified full commit
SHA. Maintainer propagation remains pending.

## Technical Context

**Authoritative implementation surfaces.**

- `source_of_truth/skills/unity-development/SKILL.md` — the Test Execution section owns mandatory
  batch flags, editor discovery, root-or-nested project paths, absolute evidence, the worktree
  ladder, filtering, XML interpretation, and manual teardown.
- `source_of_truth/skills/unity-development/SKILL.md` Refactor / Rewire Test Preservation Rules use
  the verified `Assets/Tests/Editor` convention for the reference project's EditMode tests.
- `source_of_truth/skills/unity-development/SKILL.md` Serialized Assets section keeps Unity as the
  serializer authority and separates plain headless import from Editor-API asset construction.
- `source_of_truth/agents/04-phase-execute.agent.md` Step 2.5 consumes the canonical Test Execution
  ladder, preserves `-testFilter` scoping, and keeps non-executed evidence non-green.
- `source_of_truth/agents/04g-unity-visual-verification.agent.md` owns deployed editor discovery and
  graphics-enabled PlayMode invocation against the selected root-or-nested Unity project.
- `source_of_truth/agents/04h-unity-reviewer.agent.md` delegates test execution and conditional
  serialized-asset import to their distinct canonical skill sections.

**Shadow worktree mechanics, as verified against the reference project.**

- **Detached, always.** Create with `git worktree add --detach <path> HEAD`; refresh with
  `git -C <path> checkout --detach <sha>`. Git refuses to check out the same branch in two
  worktrees, so a branch-tracking worktree would fail in exactly the situation this phase
  targets — the maintainer's Editor open on the branch under test.
- **One fixed path per project: `<project-dir>-agent-tests/`, a sibling of the project directory.**
  A fixed name is what lets the agent tell "one already exists" from "create one" — the absence of a
  convention is how the reference project accumulated four stale worktrees. Never nest it inside the
  Unity project directory; Unity would import it as project assets.
- **`Library/` survives a refresh.** It is gitignored (`.gitignore:60`, `[Ll]ibrary/*`), so a
  detached checkout does not touch the import cache. This is what makes reuse cheap and what makes
  per-run worktree creation an anti-pattern.
- **Created on first need, announced.** The agent reports the worktree path, the approximate disk
  cost, and that the first run performs a full asset import taking minutes.
- **Permanent.** One shadow worktree per Unity project, persisting indefinitely. `git worktree
  prune` runs on each use; teardown is manual and documented in the runbook.

**Corpus conventions that constrain the work.**

- Every edit lands in `source_of_truth/`. `ports/` and `.github/` are generated; a sync-test failure
  after these edits means "propagation is pending," not "fix the output."
- Skill directories propagate all bundled files, not just `SKILL.md`, which is why the GameCI
  template can live under `unity-development/references/`. `docs/` is not propagated, which is why
  the human-facing runbook lives there.
- Agent and skill files are machine-facing and read at runtime — dense but brief. The runbook in
  Deliverable 5 is human-facing and follows the runbook rules: TL;DR in five lines or fewer, then
  numbered steps with the exact command and what a correct result looks like.
- Instruction files may contain deliberate personality-canary blocks. Never delete one.

## Dependencies & Risks

- **Dependency**: None on prior phases. Requires access to the reference Unity project to *verify*
  the documented invocations; the rules can be authored without a Unity install.
- **Risk — Unity Personal may not permit a second concurrent Unity process. This is the phase's
  primary open risk.** AC7/AC11 remain unverified because no main-Editor-open run exists. The ladder
  degrades to an agent-run main-checkout command after the Editor closes, but the phase stays NO-GO
  until the concurrent condition and Editor usability are recorded honestly.
- **Risk — missing-`.meta` regeneration is not empirically verified.** AC5 remains
  `not-executed (reference project not clean)`. The contract keeps the capability conditional until
  a controlled Unity 6000.3.13f1 import regenerates one selected fixture and restoration returns the
  checkout to a clean state.
- **Risk — workflow dependencies are mutable before activation.** The inert GameCI template uses
  major-version action tags and passes Unity secret references to the test action. *Mitigation*:
  replace every action reference with a verified full commit SHA and run `actionlint` on the adapted
  workflow before enabling it.
- **Risk — shadow worktree cold start.** A fresh worktree has no `Library/`, so its first run does a
  full asset import taking minutes. *Mitigation*: the procedure mandates a persistent, reused
  worktree refreshed by checkout. A per-run throwaway worktree is an explicit anti-pattern and must
  be named as one in the skill text.
- **Risk — disk cost.** The reference project is 602 MB, of which `Library/` is 309 MB, so a shadow
  worktree costs roughly 600 MB per project. *Mitigation*: state the figure plainly in the runbook
  alongside the teardown command; do not hide it.
- **Risk — worktree accumulation. Observed, not hypothetical.** The reference project already
  carries four stale prunable worktrees left by earlier agent runs. *Mitigation*: `git worktree
  prune` is part of the procedure on every use, and the shadow worktree has a single fixed path per
  project so it cannot multiply.
- **Risk — commit-before-test produces noisy history.** Testing uncommitted work requires a commit
  first. *Mitigation*: most runs land on the Feature - Implementer's existing per-feature commit;
  only mid-feature runs add one, and normal branch hygiene applies.
- **Risk — `-nographics` applied too broadly breaks visual verification.** PlayMode capture needs a
  graphics device. *Mitigation*: the rule is stated per test platform as a two-row table, and `04g`
  is verified against it as part of Deliverable 4.
- **Risk — a wording-keyed test goes inert on reword.** *Mitigation*: guards are structural and must
  be proven able to fail (mutation check per the `guard-integrity` skill). No test asserts on prose
  phrasing.

## Success Criteria

- [x] The string asserting `-batchmode` is optional no longer exists anywhere in `source_of_truth/`.
- [x] The `unity-development` skill states the graphics flag per test platform as a two-row table —
      `-batchmode -nographics` for EditMode, `-batchmode` with graphics for PlayMode/visual —
      unambiguously, and states `-batchmode` as mandatory at every tier.
- [x] The skill documents the three-rung execution ladder, and rung 3 forbids silent refusal and
      forbids launching a GUI.
- [x] The Editor-lock rule no longer instructs the agent to refuse and hand the run back to the
      user; it redirects to the shadow worktree, then to close-the-Editor.
- [x] The skill states commit-before-test as a precondition of worktree execution.
- [x] The skill states that `-testResults` takes an absolute path in the main checkout, and names
      reading results from inside the worktree as wrong.
- [x] The skill names the shadow worktree path convention `<project-dir>-agent-tests/` and states it
      is one fixed path per project.
- [x] The skill locates the Unity binary via editor discovery rather than a bare `Unity` on `PATH`.
- [x] An unattended agent that reaches rung 2 and gets no response reports
      `not-executed: editor open, user unavailable` rather than hanging or escalating to a GUI.
- [x] The skill documents the shadow worktree as detached, sibling-located, created on first need
      with its cost announced, permanent, refreshed by checkout, pruned on each use, and torn down
      only manually — and names per-run worktree creation as an anti-pattern.
- [x] The skill documents a headless `.meta` / asset-import invocation, and no file in
      `source_of_truth/` asserts that a human must open the Editor to generate `.meta` files.
- [x] No file in `source_of_truth/` names `Assets/Tests/EditMode` as the EditMode test path.
- [x] `04-phase-execute`, `04g-unity-visual-verification`, and `04h-unity-reviewer` are consistent
      with the new rules, with `04g` still running PlayMode with graphics enabled.
- [x] A GameCI reference workflow exists at `source_of_truth/skills/unity-development/references/`
      and a local Unity test runbook exists under `docs/unity/`, and the runbook opens with a TL;DR
      of five lines or fewer followed by numbered steps.
- [x] Structural tests cover each rule above and each has been shown to fail when the rule is removed.
- [ ] The persistent shadow-worktree EditMode command has run against
      `/Users/jennywadkins/github_repos/the-movies` while its main Editor is open, with concurrency,
      GUI absence, mouse availability, Editor usability, licensing, and absolute artifacts recorded.
- [ ] A controlled missing-`.meta` import has run against a clean reference checkout, with generated
      GUID evidence, no GUI, exact restoration, and final cleanliness recorded.
- [ ] The final safe repository gate is `executed-green`; the current artifact records 239 passed,
      2 pre-existing failures, 1 fixed-point test deselected, and 63 subtests.

## QA Considerations

- **No frontend, UI, or visual acceptance criteria.** This phase produces corpus rules, structural
  guards, documentation, and an inert workflow; record `visual-verification: no visual ACs`.
- **Manual QA is required for the Unity invocations**, because nothing in this repository can
  execute them — there is no Unity project here. The QA steps are: (a) run the documented headless
  import against `/Users/jennywadkins/github_repos/the-movies` and confirm `.meta` files are
  generated with no GUI; (b) create the shadow worktree, run the documented headless EditMode test
  command in it **with the maintainer's Editor open on the project**, and confirm no GUI appears,
  the mouse is never captured, the Editor stays usable, and the run completes; (c) record whether
  the concurrent run succeeded or failed on licensing, since that determines which rung of the
  ladder is the normal path.
- **Coordination note**: those steps need the reference Unity project and a licensed Editor, which
  live outside this repository. Plan them as explicitly maintainer-executed checks.
- Sync tests and any test reading `ports/` will fail until the maintainer propagates. That is
  expected and must be reported plainly, never worked around.
- The inert GameCI workflow requires `actionlint` and current official-documentation validation
  before adaptation. Every action reference must be replaced with a verified full commit SHA before
  activation.

## Notes for Feature - Decomposer

**Feature boundaries** — four file-ownership scopes with a shared-skill dependency:

1. **Test Execution rules rewrite** — `unity-development/SKILL.md` Test Execution section only
   (Deliverables 1 and 2). Owns lines 169–183, the per-platform table, the three-rung ladder, the
   commit-before-test precondition, and the full shadow worktree procedure. This is the largest
   feature. Sequential first; everything else reads its output.
2. **Headless asset-import procedure + corpus sweep** — Deliverable 3. Touches the Serialized Assets
   and Refactor/Rewire sections of the same skill file, so it **cannot** run parallel with feature 1
   — same file. Its guards sweep `source_of_truth/` for contradictory GUI requirements and verify
   the `Assets/Tests/Editor` convention in both owning sections.
3. **Consumer agent alignment** — Deliverable 4. Three separate agent files, disjoint from the skill
   file, but depends on features 1 and 2 being final. Parallel-safe against feature 4.
4. **Reference assets** — Deliverable 5. New files only, no existing file touched. Parallel-safe
   against feature 3.

Deliverable 6 (tests) is not a separate feature — each feature writes the guards for its own rules,
per the repo's TDD posture.

**Careful separation of concerns.**

- Features 1 and 2 both edit `unity-development/SKILL.md`. Mark them `parallel_safe: no` relative to
  each other and order 1 before 2.
- The per-test-platform distinction (`-nographics` for EditMode, graphics for PlayMode) is the single
  most likely thing to get flattened into one blanket rule. Feature 1 owns it and must state it as a
  two-row table, not prose.
- The second most likely failure is collapsing the three-rung ladder back into a binary
  worktree-or-refuse rule. All three rungs must survive, in order, with rung 3's prohibitions intact.

**Integration points.**

- The skill's `-testFilter` guidance (line 178) is consumed by `04-phase-execute` Step 2.5. Do not
  change its semantics while rewriting the surrounding section.
- `04g-unity-visual-verification` saves a discovered editor path once and reuses it. The shadow
  worktree changes the `-projectPath` it passes, not the editor path. Keep those two concerns
  separate. That same discovery procedure is what the skill's command template must reference for
  locating the Unity binary — feature 1 points at it, feature 3 confirms `04g` still owns it.
  Neither feature may fork a second discovery implementation.
- `04-phase-execute` Step 2.5 keeps `not-executed` non-green for a declined or unattended fallback,
  genuinely unavailable evidence, and a supervisor-directed skip. The direct-supervisor-attestation
  exception remains distinct.

**Verification assets.** Structural tests under `tests/`, plus the maintainer-executed Unity
invocation checks described in QA Considerations. There is no automated way to prove the Unity
commands work from inside this repository; say so rather than fabricating a green gate.
