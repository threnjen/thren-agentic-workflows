# Phase 1: Unity Headless Test Execution

**Status**: Planned
**Depends on**: None
**Estimated complexity**: Medium
**Cross-references**: None — single-repository phase

## What's New

Unity tests stop taking over your machine. Today an agent asked to run Unity tests either launches
Unity Hub and hijacks your mouse for the duration, or refuses outright because your Editor is open
and tells you to run the tests yourself. After this phase, neither happens: every agent-driven Unity
test run is headless, and it runs against its own persistent copy of the project, so you can leave
the Editor open and keep working while tests run. If that copy cannot be used, the agent asks you to
close the Editor and then runs the tests itself — it never hands the job back to you.

It also removes a false belief that has been steering agents wrong — that Unity needs a human to
open the app before it will generate `.meta` files. It does not, and agents will stop acting as
though it does.

Finally, this phase ships a ready-to-copy CI workflow and a runbook for the day you want Unity tests
running on push instead of on demand. Nothing is installed anywhere by this phase; the assets sit in
the corpus until you choose to use them.

## Objective

Make every agent-driven Unity test run headless, non-blocking, and independent of the maintainer's
running Editor, by correcting the rules in `unity-development` and introducing a persistent shadow
worktree as the standard CLI execution target, with a bounded fallback for the case where a second
concurrent Unity process is not available.

## Scope

### In Scope

- Rewrite the **Test Execution** section of `source_of_truth/skills/unity-development/SKILL.md`:
  - `-batchmode` is **mandatory** at every execution tier. The current "`-batchmode` is optional"
    wording is deleted, not softened.
  - The graphics flag is stated **per test platform, as a two-row table**: EditMode runs use
    `-batchmode -nographics`; PlayMode and visual-capture runs use `-batchmode` with graphics
    enabled, because `-nographics` prevents rendering and would break visual verification.
  - Restate the existing prohibition on pairing `-quit` with `-runTests`.
- Replace the Editor-lock refusal rule (`SKILL.md` line 181) with a **three-rung execution ladder**:
  1. Commit the working tree, refresh the persistent shadow worktree to that commit, run headless
     in the worktree. The maintainer's Editor stays open and usable.
  2. If the worktree run fails on licensing or a lock, ask the user to close the Editor, then run
     headless in the main checkout.
  3. Never silently refuse, and never launch a GUI. `not-executed` is reachable only when the user
     declines rung 2, or when the agent is running unattended and no response arrives — a
     non-response is treated as a decline and reported as `not-executed: editor open, user
     unavailable`.
- State that test results are always written to an **absolute path in the main checkout**
  (`dev/test-results/`), never to the worktree's copy of that path. The shadow worktree is a pure
  execution target; nothing ever reads output from it.
- State that the Unity binary is located by the **existing editor-discovery procedure** used by
  `04g-unity-visual-verification`, not by assuming a bare `Unity` is on `PATH`.
- State **commit-before-test as an explicit precondition** of the design: a worktree can only test
  committed code. In practice most runs need no extra commit because the Feature - Implementer
  already commits per feature; only a mid-feature run adds one.
- Document the **persistent shadow worktree procedure** in full: detached checkout, sibling
  location, first-need creation with announced cost, indefinite persistence, refresh by checkout,
  `Library/` retention, `git worktree prune` on each use, manual teardown command.
- Add a documented **headless `.meta` / asset-import procedure**
  (`Unity -batchmode -quit -projectPath <path> -logFile -`) as the sanctioned way to generate missing
  `.meta` files and asset GUIDs, and correct any corpus text implying a human must open the Editor.
- Correct the **Refactor / Rewire Test Preservation Rules** section of the same skill, which names
  `Assets/Tests/EditMode` as the EditMode test path. The reference project keeps EditMode tests in
  `Assets/Tests/Editor`; the rule must not name a path that does not exist.
- Ship two copyable reference assets: a GameCI GitHub Actions workflow template, and a
  human-facing local Unity test runbook (TL;DR, then numbered steps).
- Propagate the rule change to every consuming agent so no agent carries a stale instruction:
  `04-phase-execute.agent.md` (Step 2.5 wave test gate), `04g-unity-visual-verification.agent.md`,
  `04h-unity-reviewer.agent.md` (batch import / asset-integrity gate).
- Structural corpus tests covering the new rules.

### Out of Scope

- **Installing CI in any Unity repository.** No workflow is wired up, no Unity license secret is
  configured, no runner is provisioned. The workflow ships as an inert asset.
- **Any change to what Unity tests assert.** This phase changes how tests are invoked, never their
  content, and never the Test Authenticity Rules.
- **Removing the supervisor-attestation escape hatch** in `04-phase-execute` Step 2.5. It stays; it
  should simply become rare.
- **Visual verification redesign.** `04g` keeps its editor-location logic and its capture-config
  bootstrap; only its invocation flags and `-projectPath` target are touched.
- **Automated worktree teardown.** The shadow worktree is permanent by design. Teardown is a
  documented manual command only.
- Running `scripts/propagate_master_assets.py`. Source edits only; the maintainer propagates.
- Renaming, renumbering, or restructuring any agent.

## Key Deliverables

| # | Deliverable | Description | Likely Features |
|---|-------------|-------------|-----------------|
| 1 | Corrected Test Execution rules | `unity-development` SKILL.md Test Execution section rewritten: mandatory `-batchmode`, graphics flag as a per-platform two-row table, no `-quit` with `-runTests`, results to an absolute path under the main checkout's `dev/test-results/`, Unity binary located by editor discovery | Skill authoring |
| 2 | Execution ladder + shadow worktree procedure | Replaces the Editor-lock refusal with the three-rung ladder. Covers commit-before-test, detached creation, sibling location, announced cost, indefinite persistence, refresh, `Library/` retention, prune, manual teardown | Skill authoring |
| 3 | Headless asset-import procedure | Sanctioned `.meta` / GUID generation without a GUI, plus correction of any corpus text asserting the opposite, plus the `Assets/Tests/Editor` path correction | Skill authoring, corpus sweep |
| 4 | Consumer agent updates | `04-phase-execute` Step 2.5, `04g-unity-visual-verification`, `04h-unity-reviewer` aligned to the new rules | Agent authoring |
| 5 | Reference CI workflow + local runbook | GameCI workflow template at `source_of_truth/skills/unity-development/references/`; runbook at `docs/unity/`. Both copyable, neither active | Asset authoring, docs |
| 6 | Structural tests | Guards proving the new rules are present and the deleted rule is gone | Testing |

## Technical Context

**Files that carry the defect.**

- `source_of_truth/skills/unity-development/SKILL.md` lines 169–183 — the Test Execution section.
  Line 177 is the mouse-hijack cause; line 181 is the refusal cause. Lines 173–175 hold the command
  template. Line 178 defines `-testFilter` scoping for affected-suite runs, which stays as-is.
- `source_of_truth/skills/unity-development/SKILL.md` Refactor / Rewire Test Preservation Rules —
  names `Assets/Tests/EditMode`, a path absent from the reference project.
- `source_of_truth/skills/unity-development/SKILL.md` lines 257–279 — Serialized Assets section.
  Already correct that Unity must generate assets, and already prescribes running the Editor API in
  batch mode. Deliverable 3 extends it with the explicit `.meta` regeneration invocation and must not
  contradict it.
- `source_of_truth/agents/04-phase-execute.agent.md` line 107 — points at the skill's Test Execution
  section for command and `-testFilter` scoping. Line 111 is the `not-executed` handling, which the
  ladder makes reachable only when the user declines rung 2.
- `source_of_truth/agents/04g-unity-visual-verification.agent.md` lines 40–69 — editor discovery,
  the `-runTests` / `-quit` prohibition, and the saved-editor-path behavior. Its PlayMode runs need
  graphics; do not let a blanket `-nographics` rule reach it.
- `source_of_truth/agents/04h-unity-reviewer.agent.md` line 34 — serialized-asset validation runs a
  documented batch compile/import. Align its invocation with Deliverable 3.

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
  primary open risk.** The maintainer's license is Unity Personal, a single-seat activation. If a
  batchmode instance cannot run while the Editor holds the license, rung 1 of the ladder is
  unavailable on the target machine. *Mitigation*: the ladder is designed to degrade — rung 2
  (ask the user to close the Editor, then run headless) still eliminates both reported symptoms.
  Verify empirically against the reference project before finalizing the rules; if rung 1 fails,
  document it as the expected path on Personal licenses rather than shipping a rule that misleads.
- **Risk — the Unity CLI behavior is asserted, not empirically verified.** The headless-import and
  `.meta`-generation claims come from working knowledge, not from a run against Unity 6000.3.13f1.
  *Mitigation*: verify both invocations against the reference project during execution before the
  rules are finalized; if a claim fails, correct the rule rather than shipping it.
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

- [ ] The string asserting `-batchmode` is optional no longer exists anywhere in `source_of_truth/`.
- [ ] The `unity-development` skill states the graphics flag per test platform as a two-row table —
      `-batchmode -nographics` for EditMode, `-batchmode` with graphics for PlayMode/visual —
      unambiguously, and states `-batchmode` as mandatory at every tier.
- [ ] The skill documents the three-rung execution ladder, and rung 3 forbids silent refusal and
      forbids launching a GUI.
- [ ] The Editor-lock rule no longer instructs the agent to refuse and hand the run back to the
      user; it redirects to the shadow worktree, then to close-the-Editor.
- [ ] The skill states commit-before-test as a precondition of worktree execution.
- [ ] The skill states that `-testResults` takes an absolute path in the main checkout, and names
      reading results from inside the worktree as wrong.
- [ ] The skill names the shadow worktree path convention `<project-dir>-agent-tests/` and states it
      is one fixed path per project.
- [ ] The skill locates the Unity binary via editor discovery rather than a bare `Unity` on `PATH`.
- [ ] An unattended agent that reaches rung 2 and gets no response reports
      `not-executed: editor open, user unavailable` rather than hanging or escalating to a GUI.
- [ ] The skill documents the shadow worktree as detached, sibling-located, created on first need
      with its cost announced, permanent, refreshed by checkout, pruned on each use, and torn down
      only manually — and names per-run worktree creation as an anti-pattern.
- [ ] The skill documents a headless `.meta` / asset-import invocation, and no file in
      `source_of_truth/` asserts that a human must open the Editor to generate `.meta` files.
- [ ] No file in `source_of_truth/` names `Assets/Tests/EditMode` as the EditMode test path.
- [ ] `04-phase-execute`, `04g-unity-visual-verification`, and `04h-unity-reviewer` are consistent
      with the new rules, with `04g` still running PlayMode with graphics enabled.
- [ ] A GameCI reference workflow exists at `source_of_truth/skills/unity-development/references/`
      and a local Unity test runbook exists under `docs/unity/`, and the runbook opens with a TL;DR
      of five lines or fewer followed by numbered steps.
- [ ] Structural tests cover each rule above and each has been shown to fail when the rule is removed.
- [ ] Both Unity invocations documented by this phase have been executed successfully against
      `/Users/jennywadkins/github_repos/the-movies`, and the results are recorded — including
      whether rung 1 of the ladder is available under the maintainer's Unity Personal license.

## QA Considerations

- **No frontend or UI changes.** This phase produces Markdown assets only; no manual UI QA applies.
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

## Notes for Feature - Decomposer

**Suggested feature boundaries** — roughly four, split by file ownership so they can run in parallel
where scopes are disjoint:

1. **Test Execution rules rewrite** — `unity-development/SKILL.md` Test Execution section only
   (Deliverables 1 and 2). Owns lines 169–183, the per-platform table, the three-rung ladder, the
   commit-before-test precondition, and the full shadow worktree procedure. This is the largest
   feature. Sequential first; everything else reads its output.
2. **Headless asset-import procedure + corpus sweep** — Deliverable 3. Touches the Serialized Assets
   and Refactor/Rewire sections of the same skill file, so it **cannot** run parallel with feature 1
   — same file. Also sweeps `source_of_truth/` for text contradicting the headless-import rule and
   for the `Assets/Tests/EditMode` path.
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
- `04-phase-execute` Step 2.5 `not-executed` handling stays, but becomes reachable only when the
  user declines rung 2. Do not delete it.

**Verification assets.** Structural tests under `tests/`, plus the maintainer-executed Unity
invocation checks described in QA Considerations. There is no automated way to prove the Unity
commands work from inside this repository; say so rather than fabricating a green gate.
