# Cross-Phase Decisions

## Phase Numbering

- **Phases were renumbered 2026-07-16** so numbers match the order work actually happened: Phase Final Review (was 05) → **03**; new Release Remediation & Verification → **04**; Format-on-Save + Completion Gates (was 03) → **05**; Skill Enforcement (was 04) → **06**. Phases 01 and 02 are unchanged. Documents written before that date use the old scheme; the mapping table is in `docs/phases/PROJECT_ROADMAP.md`.
- **Agent numbers are pipeline positions, not phase numbers.** `05-phase-final-review` and its `05a`–`05l` evaluators follow `04-phase-execute` in the pipeline; they did not renumber with the phase and must not be "corrected" to match it.
- **Development fixtures keep legacy phase identifiers.** `dev/phase-final-review/fixtures/PHASE_05/` (pseudo-subphases `PHASE_05a`/`PHASE_05b`) and the report root `dev/phase-final-review/PHASE_05/` are synthetic identifiers pinned to recorded commit SHAs. Renaming them would invalidate the fixture contract.

## Release Verification

- **"Remediated in code" is not "verified".** Phase 02's P2-SEC-01..03 fixes and Phase 01's SEC-01 fix exist in code, but a fix without a re-run gate is not a release verdict. Status lines move only on fresh final-state evidence — this is the operational form of the Final Review Contract below.
- **A fixed budget must never be relaxed to make a gate pass.** PERF-01's 50 ms propagated-guard budget was silently raised to 90 ms in PR #22 to mask a failure; that was reverted. If a budget is genuinely unachievable, the honest outcome is an explicit user-approved AC change, not a quietly edited threshold.
- **PERF-01's AC was reshaped by explicit user approval on 2026-07-16 — this is that escape hatch being used correctly, and the distinction matters.** What was unachievable was never the 50 ms number (the guard costs ~30 ms); it was asserting a *wall-clock median* on a machine whose load is not controlled, which left ~20 ms of headroom against ambient noise and failed 2 of 6 focused runs while the guard itself was unchanged. The replacement asserts a **calibrated relative budget**: a bare-interpreter baseline captured in the same run, with the guard's cost measured above it. How much latency is acceptable did not change; what is measured did. The guardrail that keeps this distinct from the PR #22 edit is a required acceptance criterion that **a deliberately slowed guard must still fail the new gate** — a reshape that cannot fail a real regression is a deletion wearing a disguise. Any future AC reshape must carry an equivalent proof.
- **Fixes made outside the pipeline still need phase records.** Hook-command project-root anchoring and file-access-guard false-positive tuning both changed shipped behavior during ad-hoc debugging sessions with no phase record. Reconciling them is Phase 04 scope. (Recorded 2026-07-16.)
- **A stale scan is no more authoritative than a stale fix — every finding classification must name the revision it examined.** The Phase 03 delegated scan (`dev/phase-final-review/PHASE_05/z-security-scan-final.md`) classifies P2-SEC-01..03 as *persisting*; it names its subject as revision `344711df78c5` on `phase/phase-final-review-2`, where `redact_tool_output` still recursed through mappings preserving container shape — the P2-SEC-01 defect. At HEAD that function returns a fixed redacted shape. Both conclusions are correct about different code. The lesson generalizes: "remediated in code is not verified" is usually read as *fixes need gates*, but the converse holds equally — **an ungated finding is not a current finding**. Any evidence artifact that does not name its revision cannot be reconciled against later work, and any release dossier must verify that each artifact post-dates the code it covers. (Recorded 2026-07-16.)
- **Some High findings are not closable without new capability, and recording them honestly is the correct outcome.** Phase 04 hits three: **P5-SEC-02** (readiness-report trust boundary — no code to attach a schema/reducer to, because the readiness path is agent Markdown; a prose constraint is exactly what the Phase 03 scan faulted, so tightening wording would make the record say closed without closing anything); **`05a-baseline-worktree`'s unconstrained `execute`** (the propagation format maps `execute` to `Bash`/`bash` with no allowlist syntax, so "Bash but only `git worktree`" is inexpressible); and **absent curl/wget exfiltration enforcement** (four `legacy_bash_parity` entries describe patterns with no enforcement rule behind them, so "reinstating" means authoring rules that never existed). Each is recorded as open with routing rather than closed, and each is a NO-GO input. The general rule: **when the honest fix requires capability a phase has excluded, the phase records the finding — it does not redefine the finding to fit the scope.** (Recorded 2026-07-16.)
- **`legacy_bash_parity` in `file-access-rules.json` is a metadata inventory, not enforcement.** Its entries carry only `source_pattern`, `classification`, and `rationale`; live enforcement lives in the `bash_rules`, `rules`, and `bash_analysis` blocks, and the mapping between them is not one-to-one. Changing a `classification` value relabels an inventory entry and enforces nothing. `tests/hooks/fixtures/bash/legacy-parity.json` is hard-coupled via exact-string and count assertions, so pattern edits need lockstep fixture updates. Anyone auditing or reinstating a rule must work against the enforcement blocks. (Recorded 2026-07-16.)

## Deferred Pipeline Work

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
- **`dev/phase-final-review/fixtures/PHASE_05/` is still on disk and now has no owner.**
  The Phase document instructs retiring both `dev/phase-final-review/fixtures/PHASE_05/`
  and the report root `dev/phase-final-review/PHASE_05/`.
  `02-retired-evaluator-removal`'s plan listed this as a Non-Goal on the stated grounds
  that the directory "does not exist" — that is true of the report root but **false of
  the fixtures**, which are tracked. Because it was dismissed as absent rather than
  deferred, no feature inherited it. It is also not a simple deletion: seven surviving
  agents (`05` orchestrator, `05b`, `05g`, `05h`, `05j`, `05k`, `05l`) name the fixture
  root as live wiring, and the Phase Numbering note above pins the fixtures to recorded
  commit SHAs. Retiring them is a design decision with real blast radius, not cleanup.
  Needs an explicit owner. (Recorded 2026-07-16 by `02-retired-evaluator-removal`'s
  review.)
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

## Hook Composition

- **A PreToolUse hook that rewrites `tool_input.command` can invalidate another PreToolUse hook's analysis of that same command.** `.github/hooks/scripts/rtk-rewrite.sh` reads `.tool_input.command` and delegates rewriting to an external `rtk` binary resolved from `PATH`; the file-access guard classifies Bash commands through its bash analyzer. If the guard evaluates the pre-rewrite string, the executed command is not the command that was approved. Three properties make this a standing concern rather than a one-off: **(1)** correctness depends on hook ordering between a *global* (`~/.claude/settings.json`) and a *project* hook, which no test covers; **(2)** the global registration uses an absolute path into this repository, so every Bash command in every project the user runs routes through a script living here, and moving this repo breaks Bash hooks everywhere — the same absolute-path fragility already recorded for the eval hook symlink; **(3)** the `rtk` binary is unpinned and trusted on `PATH`, and this project's own RTK reference documents a name collision with a different published tool of the same name, making shadowing a stated install hazard rather than a hypothetical. Phase 04 investigates ordering empirically and assigns severity from the evidence. **The general rule for future hook work: any hook that mutates tool input must be ordered strictly before every hook that authorizes on that input, and that ordering needs a test — composition safety is not inheritable from the safety of each hook alone.** (Recorded 2026-07-16.)
- **The kill switch is two switches.** `.github/hooks/config/file-access-overrides.json` gates only the PreToolUse file-access guard; the injection scanner reads `.github/hooks/config/injection-overrides.json`, which does not exist. Because an absent config layer reads as `{}`, *creating* that file disables the scanner — so restoring it means **deleting** it, not writing `{}`. The restore is asymmetric between the two. Any live QA that provokes the scanner must arm both first; arming one while provoking the other leaves the component under test with no recovery path. (Recorded 2026-07-16.)

## Guard Friction and Command Prompting (raised 2026-07-16; revisit at Phase 04 refinement)

**Two items to revisit together at Phase 04 refinement. They look like separate complaints and are one component.**

- **There is no command-allowlist hook in this repo. The thing that prompts on commands is the file-access guard.** Raised 2026-07-16: the friction was initially attributed to the guard, then re-attributed to "the command allowlist." Neither framing is quite right, because they are the same code path — `scripts/file-access-guard.py` loads `bash_rules` from `config/file-access-rules.json` through `lib/bash_analyzer.py`. Nothing else in the repo gates commands. (Claude Code's own native permission prompts are the other source of command friction, and are not ours to tune.)
- **The friction and the security live in different config blocks, and that is the whole point.** Measured 2026-07-16 in `config/file-access-rules.json`: **`bash_rules` is 20 entries, every single one `action: ask`** — 5 environment probes (`printenv`, bare `env`, `set`, `export`, `echo $VAR`) and 15 destructive operations (`rm -rf`, `git push --force`/`-f`, `git reset --hard`, `git clean -f`/`-fd`, `chmod -R`, `dd`, `mkfs`, device redirection, `truncate`, `shred`, `wipefs`, `DROP TABLE`, `DROP DATABASE`). The file-access `rules` block is 37 entries: **32 `deny`**, 3 `ask`, 2 `allow`. **Every prompt comes from the ask-rules; the bypass-permissions protection that the roadmap Vision sells is the 32 silent denies, which never prompt at all.** Retiring the guard to stop the prompting would delete 32 deny rules to fix 20 ask rules.
- **The five environment probes are the first thing to examine.** `echo $VAR` and `printenv` are ordinary work, not destructive acts. The roadmap's own Friction budget already states the test: "Rules matching ordinary text (commit messages, search patterns, benign redirects, lock-file reads) are defects, not safety." If the friction is concentrated there, the fix is editing one JSON config — not removing a phase deliverable. Phase 04 already owns a security review of the 17 loosened guard rules, so a friction pass belongs in the same work.
- **Before retiring anything, measure which rule IDs actually fired.** `audit_log` is configured in the same rules file. The question "which of these 20 rules interrupted me, how often, and on what command" is answerable from evidence rather than memory, and it is the difference between deleting five bad regexes and deleting the phase's headline feature.

## File-Access Guard Retirement (proposed 2026-07-16; decide at Phase 04 refinement)

- **The user's stated intent is to retire the file-access guard and keep the hook framework.** Recorded 2026-07-16 during Phase 03 decomposition, explicitly as intent rather than a decision — the call gets made when `@phase-refiner` runs on Phase 04. The stated reason is friction: the guard is judged more trouble than it is worth, while the framework is still wanted for the hooks Phases 05 and 06 plan to build. **Read this alongside the friction findings above, which suggest the complaint may be satisfiable by config tuning rather than retirement.**
- **The guard is cleanly separable, verified 2026-07-16.** `lib/bash_analyzer.py` is imported by exactly one consumer, `scripts/file-access-guard.py`, and itself imports `lib/file_access.py`. Nothing else imports either. `scripts/injection-scanner.py` and `lib/injection_scanner.py`/`lib/url_exfiltration.py` import neither, so **Phase 02 is unaffected**, and `lib/framework.py` is not involved. The retirement unit is: `scripts/file-access-guard.py`, `lib/file_access.py`, `lib/bash_analyzer.py`, `config/file-access-rules.json`, `config/file-access-overrides.json`, `.github/hooks/file-access-guard.json`, their tests under `tests/hooks/`, and the propagated wiring in all three generated roots.
- **This is a Phase 01 retirement that Phase 04 would verify — not a Phase 04 edit.** Phase 01 is named "Hook Foundation + File-Access Guard" and the guard is its headline deliverable; the roadmap Vision sells "hardens every project against prompt injection and file/secret manipulation — even under bypass permissions," and the bypass-permissions claim is the guard's alone. Retiring it changes Phase 01's status, the Vision paragraph, and the "Why hooks, not permissions" architecture note. That is `@project-planner` surface, not a phase-local scope trim.
- **Most of Phase 04 is guard work, so retirement moots it rather than shrinking it.** PERF-01 (the propagated-*guard* latency budget), the bash-rewrite bypass (which is about the *guard's* classification of a command being invalidated by `rtk-rewrite.sh`), and the security review of the 17 loosened guard rules all evaporate. What survives: the Phase 02 security-gate re-run, live Claude/Codex/OpenCode QA, REPO-SEC-06, and records reconciliation. **PERF-01 is Phase 01's release blocker**, so retiring the guard does not just delete work — it changes which phases are releasable and why. Weigh that at refinement: the tidiest outcome of "I dislike this feature" should not be an accidental release unblock.
- **Retiring the guard deletes the repo's only bash-command parser.** `lib/bash_analyzer.py` goes with it, since the guard is its only consumer. That is precisely the component a future per-agent command-allowlist hook would reuse (see the Phase 03 allowlist finding below). Not an argument against retirement — an argument for recording what the deletion costs, so a later phase does not rebuild it believing it never existed.

## PR-Review Rescope (Phase 03; resolved 2026-07-16)

- **`05-phase-final-review` is rescoped into `05-pr-review`, gating diffs on the current branch against its base.** Decided 2026-07-16. The original scope — evaluate a whole phase divided into subphases `PHASE_0Na`–`PHASE_0NX` — was not the right shape. The replacement runs when a branch is ready to PR.
- **The rescope lands in Phase 03 itself, not a new phase, and this is what dissolved the numbering collision.** Phase 03 is where the agent family was built, so amending its scope needs no new roadmap entry and no renumber. The alternative was ugly: `05` and `06` are already Format-on-Save + Completion Gates and Skill Enforcement, so a new phase at `05` meant another renumber — and the 2026-07-16 renumber is recorded below as having silently changed the meaning of the plugin-packaging deferral — while appending at `07` would have put the number out of execution order, the very thing the last renumber existed to fix. **The general lesson: when a rescope has no clean home, check whether the originating phase is the home.** Reopening a phase's scope is cheaper than renumbering around it.
- **The evaluator roster splits roughly in half, and this is what makes the rescope tractable.** Seven of twelve are already diff-shaped and transfer directly — some fit *better* than they do now: `05a-baseline-worktree` (checks out a baseline commit → the base branch), `05b-change-narrator` (narrative baseline→HEAD → the PR's diff), `05g-artifact-sweeper` (debug statements/TODOs since baseline), `05h-test-health` (coverage delta), `05j-consistency-auditor`, `05k-dependency-auditor`, `05l-readiness-synthesizer` (go/no-go → PR gate verdict). **Five are phase-shaped and are retired**: `05c-qa-consolidator` (merges *subphase* QA docs), `05d-security-rollup` (union of *subphase* findings), `05e-ac-regression` (re-verifies *every subphase's* ACs), `05f-seam-analyzer` (seams *between subphases*), `05i-learnings-harvester` (mines *pipeline review records*). A PR has no subphases and no ACs. Little working code is lost — the whole-phase flow has never successfully run against a real phase.
- **Git cannot determine a branch's base. This is a data-model fact, not a tooling gap — do not design around an assumption that it can.** A ref is a SHA and nothing else; there is no parentage metadata anywhere. Verified 2026-07-16: `git merge-base HEAD main` works but requires already knowing the base (circular); the reflog records `branch: Created from HEAD` — the *SHA*, never the branch name — and is local-only, never cloned, and gc-pruned (90 days default), so it is absent in CI and fresh clones; `git symbolic-ref refs/remotes/origin/HEAD` is the most reliable signal but yields the repo's *default* branch rather than *this branch's* base, and is frequently unset (needs `git remote set-head origin -a`). **The chosen design is suggest-and-confirm**: infer a candidate from `origin/HEAD`, compute `merge-base`, show the implied diff scope (commit count, files touched), let the user accept or override. This matches the existing `05` preflight pattern (auto-suggest the baseline commit, user confirms) and fails safe — an unset `origin/HEAD` means asking rather than guessing. Suggestion order is `origin/HEAD` → `origin/main` → `origin/master` → present candidates for selection. Cases where inference is actively wrong and must be named in the agent: a branch cut from another feature branch (merge-base against the default silently includes the parent's work in the diff), a rebased branch, and a squash-merged base.
- **The nearest-merge-base heuristic returns the branch under review. Exclude self and self's tracking ref explicitly.** Demonstrated 2026-07-16 on branch `repo_improvements_project` at HEAD `ae9823a`: `git merge-base HEAD main` and `git merge-base HEAD origin/main` both give `e3398c7`, but `git merge-base HEAD repo_improvements_project` and `git merge-base HEAD origin/repo_improvements_project` both give `ae9823a` — HEAD itself. **A branch is always its own nearest base, and so is its remote-tracking ref.** Any ranking over candidate branches must filter both before comparing.
- **The rescope inherits Phase 03's open findings rather than leaving them for Phase 04.** P5-SEC-02 (readiness path consumes report claims after metadata-only validation) is the notable one: it was unclosable because the readiness path is agent Markdown with no code to attach a schema and deterministic reducer to. **The rescope rebuilds that path, so the validator arrives with the rebuild instead of being new capability bolted onto prose.** Also inherited: `execute` grants on `05`/`05g`/`05j`/`05k` (set them correctly when each agent is rebuilt, rather than fixing them twice — note `05k` is not a simple removal, its contract permits an offline read-only audit command); `05a`'s unconstrained `execute`; and the propagation-enumeration gap omitting `05g`/`05j`/`05k` (only correct once the roster is settled at seven contiguous slugs).
- **The propagator's missing `execute` allowlist syntax stopped being a residual risk the moment a feature needed it.** `scripts/propagate_master_assets.py:332` maps `"execute": ["Bash"]` and `:353` maps `"execute": ["bash"]`; there is no allowlist syntax, so every narrow grant — `05a`'s `git worktree`, the orchestrator's `gh` — is inexpressible and gets recorded as accepted risk instead. It sat open because nothing forced it. The opt-in PR-comment feature needs `gh`, and "grant `gh`" is mechanically "grant every shell command," which two recorded decisions prohibit. **So the allowlist became Phase 03's first deliverable, and closing it closes the `05a` and mechanical-sweep grants as a side effect.** The general lesson: a capability gap recorded as accepted risk will stay open indefinitely unless some feature's correctness depends on closing it. Look for the forcing function rather than re-recording the risk.
- **Correction, 2026-07-16 (decomposition): the allowlist forcing function above is void — per-agent command scoping is not expressible on Claude at all, so the propagator was never the binding constraint.** Verified against current Claude Code docs: a subagent's `tools:` frontmatter accepts only bare tool names and MCP patterns; `tools: Bash(gh:*)` is not a narrower grant but an *unresolved tool name*, and Claude Code refuses to launch the subagent. Subagents have no `permissions`/`allowed-tools` key; `permissionMode` selects how prompts are handled, never which commands are allowed. Command scoping exists only in project/session-wide `settings.json` permission rules — which are not per-agent — or in a **per-agent PreToolUse hook**, which Phase 03 excludes. Harness survey: **OpenCode** supports real per-agent `permission.bash` globs (last-match-wins, so the `"*"` catch-all must come *first*, and patterns match parsed commands — `"git status"` will not match `git status --short`; use `"git status *"`); **Codex** has no per-profile command list at all (`ConfigProfile` carries only `approval_policy`, `approvals_reviewer`, `sandbox_mode`, `tools`), and its execpolicy rules are global, sandbox-escape-only, Starlark, and experimental. So native per-agent scoping exists on **one of three harnesses**. Building the syntax anyway would be real on OpenCode and decorative on Claude and Codex — the "partial protection that reads as total protection" failure recorded under adoption readiness, aimed at ourselves.
- **The sharper correction: the `gh` grant never cost anything.** The premise was "grant `gh` = grant every shell command, which two decisions prohibit." But the orchestrator needs `git symbolic-ref`/`git merge-base`/`git branch` for base derivation, so it holds unrestricted Bash *regardless* of the PR-comment feature. Adding `gh` widens nothing. **The general lesson, and the reason this is worth recording rather than quietly fixing: "look for the forcing function rather than re-recording the risk" was good advice that found a fake one.** A forcing function is only real if the feature is actually blocked without the capability — check that the blockage exists before promoting it to Deliverable 1. Here the blockage was assumed from the propagator's source mapping without checking whether the *target* format could express the result.
- **Decisions taken in refinement, 2026-07-16.** Pipeline artifacts are **optional enrichment** — the run proceeds on the diff alone and says what evidence was unavailable; this is also the boundary that keeps PR Review from being a duplicate of `prod-code-review` (document-driven, phase-scoped) rather than a complement (diff-driven, branch-scoped). **No verdict write-back**: the report file is the verdict, which deletes the two-file transactional status-line edit, its unique-match ambiguity detection, and its restore-on-second-write-failure path — the riskiest implemented code in the phase, now with no reason to exist. **The five phase-shaped evaluators are deleted** from source and from all three generated roots; **the seven survivors renumber contiguously to `05a`–`05g`**. **Reports land at `dev/pr-review/<base-sha-short>-<UTC-timestamp>/`** — keyed only by hex and digits, so no branch name reaches a filesystem path and no sanitizer exists to be wrong; every run owns its directory, which also deletes archive-before-overwrite. **The verdict is advisory**; a hook that blocks push or merge on `NO-GO` is deferred to a hook-owning phase. **Security is delegated to the existing `04e-diff-security-scan`**, which is already diff-shaped and already holds no `execute` — no new security agent is authored.
- **Removing the multi-subphase premise deleted work rather than moving it, and that is the shape to expect from a good rescope.** Gone entirely: subphase discovery, ledger parsing and multi-run disambiguation, the `eval:` commit-message fallback, the "ledger reality" dependency and risk, the artifact-inventory refusal gate, verdict write-back, and archiving. `merge-base` replaced all of the baseline machinery. Phase 03 dropped from Large to Medium. **If a rescope only relocates work, suspect the new scope is the old scope wearing a hat.**
- **One upfront interaction is a design outcome, not a politeness feature.** The requirement was that questions arrive before the run so an unattended run is never found stuck. It became achievable only because the decisions above removed every other blocking question: with ledger disambiguation, artifact refusal, and write-back ambiguity all gone, **base confirmation is the only blocking question left**, and the PR-comment choice joins it in the same block. The subtlety worth keeping: **a question asked after the work is on disk blocks nothing.** That is what makes "ask me once the report is written" both unattended and safe — the user sees the content before it is published. Guard this: it is the requirement most likely to erode silently, one reasonable-seeming question at a time.
- **Phase 03's verdict is NO-GO, issued in Phase 04 from existing evidence, and superseded rather than repaired.** The work happened and seven evaluators carry forward, so this is honest history rather than abandonment. The general principle worth keeping: **when a deliverable is slated for rescope, verifying it as-built is archaeology.** Phase 04 dropped its agent-family work for exactly this reason and got smaller and more coherent as a result — it is now hooks-only.

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

## Narrative and Test Health (resolved at feature 06)

- **The report-root migration ledger is now one entry from empty.** `EVALUATORS_AWAITING_REPORT_ROOT_MIGRATION` in `tests/test_pr_review_orchestrator.py` holds only `05l-readiness-synthesizer.agent.md`, which feature 07 owns. When 07 migrates it, the set is empty and `test_report_root_migration_cannot_split_silently` should be deleted rather than left asserting an empty set. Note the shape that made this safe to shrink: the compared set is *derived from disk* and asserted by exact equality, so removing an entry is reconciliation, not exemption — a regressing agent re-enters the derived set and fails. Verified by mutation at feature 06. A ledger keyed to a hand-written allowlist would not have this property; do not replace it with one.
- **Codex `max_depth` is an operator prerequisite that no repository artifact can enforce.** `[agents] max_depth = 2` lives in `~/.codex/config.toml` and is global, not a per-agent field — the propagator emits no such key and none of the three generated roots can carry one. Both `05f-test-health` (to `Test - Analyst`) and `05b-change-narrator` (to per-directory readers) spawn at depth 2 through the orchestrator. With the default of 1 the spawn is blocked, the model **silently does the work inline and reports success**, and the output is indistinguishable from real delegation. Both bodies name the trap; nothing can assert it. **Any future AC of the form "agent X demonstrably delegates to Y" is unverifiable by static test and must route to a runtime transcript.** Do not accept a green declaration assertion as covering it — it passes in exactly the failure case. Recording the prerequisite in operator documentation is open for feature 08.
- **The no-`execute` grant is what structurally prevents `05f-test-health` growing a coverage runner.** Neither `05f` nor its delegate `test-analyst` holds `execute`, so no agent in the chain can measure coverage at any revision. This is a capability boundary, not a policy: `05f` reports a *measured* coverage delta only when the orchestrator supplies coverage evidence for both revisions, and otherwise reports **not-measurable** plus the structural suite delta derived from reading both trees. The degradation is deliberate and is the honest one. Absence of coverage tooling in a consuming repository is a stated limitation, never a failure. Do not close this gap by granting `execute`; supply the evidence artifact instead — the same resolution feature 05 reached for the dependency audit.
- **Inert guards are a recurring phase-level defect, not a per-feature lapse.** Feature 06 self-caught five and shipped four more, found at review by an independent sweep; earlier features had five found only at review. Every guard in this family asserts on prose, and prose restates its own vocabulary, so short-phrase membership checks are inert by default. Treat a "zero inert" claim as unverified until a sweep that *negates load-bearing sentences* — not merely damages the named phrase — reproduces it.
