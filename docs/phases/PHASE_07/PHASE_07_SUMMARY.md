# Phase 7: Hook Release Remediation & Verification

**Status**: Planned
**Depends on**: Phases 01, 02 (both implemented; both release-blocked)
**Required by**: Phases 05 and 06 — both build on a verified hook foundation. This phase carries a number higher than its dependents because phase numbers in this project record identity, not execution order; the `Depends On` column is authoritative.
**Estimated complexity**: Medium
**Cross-references**: `docs/phases/DISCOVERY_CONTEXT.md`, `docs/phases/PHASE_01/PHASE_01-qa-analysis.md` (SEC-01, PERF-01, DOC-01), `docs/phases/PHASE_02/PHASE_02-security-scan.md` (P2-SEC-01..03), `docs/phases/PHASE_03/PHASE_03-qa-analysis.md` (Phase 03's open findings, retained by Phase 03's own rescope), `docs/phases/PHASE_03/PHASE_03_SUMMARY.md` (the PR Review rescope that retains them), `dev/phase-final-review/PHASE_05/z-security-scan-final.md` (F-15), `docs/hooks/prompt-injection-defense.md`, `.github/learnings/cross-phase-decisions.md`

## What's New

Nothing new ships in this phase — that is the point. The hook suite is finished and cannot be released: the file-access guard and the injection scanner are both implemented but sitting behind open blockers, and **neither has ever been tested in a live agent session**. Every claim about them rests on automated tests and payload fixtures.

This phase stops adding surface area and makes the hooks trustworthy. It closes the remaining hook blockers, fixes a command-rewrite hook that can bypass the guard's own analysis, replaces a performance gate that could never pass with one that measures the thing that actually matters, runs the real end-to-end QA in Claude Code, Codex, and OpenCode for the first time, and reconciles the written record with what is genuinely true. When it completes, Phases 01 and 02 are either releasable or honestly recorded as not releasable, with evidence either way.

## Objective

Convert Phases 01 and 02 from "implemented but blocked" to a verified verdict by closing every open hook blocker, executing the live multi-harness QA that has never run, and correcting records and documentation that currently overstate remediation status.

## Why This Phase Is Hooks-Only

Phase 03 built the `05-phase-final-review` orchestrator and its `05a`–`05l` evaluator family. **Phase 03 has since been rescoped in place** into the `05-pr-review` family, which changes what verifying that work would mean here. Repairing an orchestrator that is about to be rewritten, and auditing evaluator evidence describing five agents that are about to be retired, is effort spent on code that will not exist.

Phase 03's open findings are therefore **retained by Phase 03 and closed by its rescope**, not repaired here. Its verdict is a **NO-GO issued in this phase from existing evidence** — honest history, since the work happened and the surviving evaluators carry forward. This is not the agent family being abandoned; seven of its twelve evaluators are already diff-shaped and transfer directly.

The practical effect is that this phase gets smaller and keeps a single coherent identity: **verify the hooks.** That is also the part closest to actually shipping.

## Audience and Bar

The current adopters are **the author and friends** — people who can ask a question and get an answer. That fact is what makes several residual risks acceptable, and it is recorded here because if it changes, the bar changes with it:

- Codex tool-coverage parity stays an accepted limitation, documented rather than redesigned.
- The file-access guard's friction profile stays hand-tuned to the author's workflow rather than made configurable.
- Distribution stays "clone the repo and run propagation" rather than a packaged install.

Broad public adoption would invalidate all three — partial protection that reads as total protection is worse than none once the user cannot ask. That work is deliberately **not** in this phase; see "Deferred to a Future Phase" below.

## Scope

### In Scope

- **PERF-01 (Phase 01)**: replace the unachievable wall-clock assertion with a calibrated relative budget that holds across machines and load, without weakening what the budget represents.
- **Bash-rewrite bypass (Phase 01)**: the guard's bash analysis can be invalidated by a PreToolUse hook that rewrites the command after classification. See "The Bash-Rewrite Boundary" below.
- **Phase 02 security gate re-run**: re-execute the security gate against the P2-SEC-01/P2-SEC-02/P2-SEC-03 remediations already made in code, and record a verified verdict from final-state evidence.
- **Guard-rule security review**: the file-access-guard false-positive tuning **loosened** enforcement across 17 rules during an ad-hoc debugging session with no scan, no review record, and no QA. It needs a security review, not merely a changelog entry.
- **REPO-SEC-06**: resolve the propagation containment gap via a single canonical no-follow contract. This is propagation code, independent of the agent family.
- **Live harness QA**: execute the `NOT RUN` manual QA for Phases 01 and 02 across Claude Code, Codex, and OpenCode, recording honest per-harness support tiers.
- **Record reconciliation**: close DOC-01's `PENDING` commit SHAs; fold the project-root hook-command anchoring into the phase record.
- **Documentation correction**: keep statements about remediation status matched to verified reality.
- **Phase 03 verdict**: issue a NO-GO from existing evidence, with its open findings enumerated and routed back to Phase 03's rescope.

### Out of Scope

- Any new hook capability, rule, or agent. This phase adds no features.
- **The `05a`–`05l` agent family.** Its `execute` grants, its propagation-enumeration gap, its runtime evidence, and P5-SEC-02 all belong to Phase 03's rescope. Fixing capability grants on agents slated for rewrite is churn, and enumerating agents slated for retirement is worse.
- Format-on-save and completion gates, and skill enforcement.
- Raising, relaxing, or conditionalizing what the latency budget represents in order to make PERF-01 pass. Changing *what is measured* is in scope and is a user-approved AC change (see PERF-01 below); changing *how much latency is acceptable* is not.
- Adoption readiness: packaging, install UX, configurable friction, upgrade path. See below.

### Deferred to a Future Phase

Making this suite fit for adoption beyond the author's circle is real work and is **not** part of this phase: a packaged install path (the deferred plugin-packaging idea in `.github/learnings/cross-phase-decisions.md`), a friction budget tunable without editing rule files, recovery and kill-switch documentation written for someone who is not the author, an upgrade path when rules change, and an install-time disclosure of Codex's partial coverage. This requires a new roadmap entry and belongs to `@project-planner`.

### Retained by Phase 03's Rescope

These are real, open, and deliberately not addressed here. Each is a NO-GO input for Phase 03's verdict, and each is closed by the PR Review rescope in `docs/phases/PHASE_03/PHASE_03_SUMMARY.md` rather than by this phase.

| Finding | Why it moves | Disposition |
|---|---|---|
| **P5-SEC-02** — the readiness path consumes report claims after metadata-only validation | Closing it requires a strict schema and deterministic status reducer. There is no code to attach that to today: the readiness path is agent Markdown. Phase 03's rescope rebuilds that path as `05g-readiness-synthesizer`, so the validator arrives with the rebuild instead of being bolted onto prose. | Open High; a requirement of Phase 03's rescope. |
| **`execute` grants on `05`, `05g`, `05j`, `05k`** | The orchestrator is being rewritten; the three sweeps are being rescoped. Grants should be set correctly when each agent is rebuilt, not fixed twice. `05k` in particular is not a simple removal — its contract permits an offline read-only audit command. | Open High; the rescope must not carry `execute` forward without justification. |
| **`05a` unconstrained `execute`** | The propagation format maps `execute` to `Bash`/`bash` with no allowlist syntax, so a narrower grant is inexpressible today. `05a` genuinely needs `git worktree`. Phase 03's rescope adds that allowlist syntax as its first deliverable, which makes the narrow grant expressible for the first time. | Closable in Phase 03; not a residual risk once the allowlist lands. |
| **Propagation enumeration omits `05g`/`05j`/`05k`** | The enumeration and the `execute` grants land in the same test function, and the enumeration is only correct once the roster is settled. Phase 03 settles it at seven contiguous slugs. | Open High; belongs with Phase 03's rescoped roster. |
| **Absent curl/wget exfiltration enforcement** | Four of the 17 loosened rules describe patterns with no enforcement rule behind them. "Reinstating" means authoring rules that never existed — new capability. | Coverage gap, recorded with routing. The review still adjudicates all 17. |

## Key Deliverables

| # | Deliverable | Description | Likely Features |
|---|-------------|-------------|-----------------|
| 1 | Trustworthy latency gate | PERF-01 closed: a calibrated relative budget that is deterministic across machines and load, plus proof that a genuinely slow guard still fails it. | Phase 01 performance |
| 2 | Guard analysis that survives rewriting | The bash-rewrite bypass closed: the guard's decision provably applies to the command that actually executes, with the rewrite binary pinned and verified. | Phase 01 security |
| 3 | Phase 02 verified verdict | Security gate re-run against final-state code; verdict recorded from fresh evidence for all three P2-SEC findings. | Phase 02 security verification |
| 4 | Guard-rule security review | All 17 loosened rules adjudicated against real enforcement; unjustified loosenings reinstated with regression coverage; gaps recorded with routing. | Guard rules |
| 5 | Containment contract | REPO-SEC-06 resolved through one canonical no-follow contract in the propagation write path. | Propagation security |
| 6 | Live multi-harness QA | First live execution of Claude/Codex/OpenCode QA for Phases 01–02, with per-harness support tiers recorded honestly. | QA execution |
| 7 | Record and doc reconciliation | DOC-01 SHAs closed; anchoring fix recorded; docs matched to verified reality; Phase 03's findings enumerated and routed. | Records/docs |

## Technical Context

### PERF-01

Gate at `tests/hooks/test_hook_distribution_integration.py::test_ac9_propagated_guard_median_latency_is_below_50_ms`.

The 50 ms budget is **not** the problem — the guard costs ~30 ms. The problem is the assertion's shape. A wall-clock median measured on a machine whose load is not controlled leaves ~20 ms of headroom against ambient noise, so the gate fails intermittently while the guard itself has not changed. This is directly observable: **independent runs of the full suite on an unmodified tree produce both `416 passed, 0 failed` and `415 passed, 1 failed`, the failure being this gate at 64 ms.** Same tree, same command, different verdicts. No number of consecutive green runs fixes this; it is a probabilistic gate that can be passed by luck, and a green run is not a baseline.

The approved reshape is a **calibrated relative budget**: capture a bare-interpreter baseline in the same run and assert the guard's cost *above* that baseline. This measures the guard's own cost rather than the machine's mood, it holds on loaded and quiet machines alike, and it directly encodes the root cause already established — the original overshoot was `python3` resolving through a pyenv shim (~50 ms of shell re-resolution per call; ~62 ms for a bare `python3 -c pass`), not guard logic.

This is a user-approved AC change per `.github/learnings/cross-phase-decisions.md` ("A fixed budget must never be relaxed to make a gate pass... the honest outcome is an explicit user-approved AC change, not a quietly edited threshold"). **PR #22 silently raised this threshold from 50 to 90 ms to mask the failure and was reverted.** The distinction that keeps this reshape honest is that a slow guard must still fail — which is why that is an explicit acceptance criterion below, not an assumption.

### The Bash-Rewrite Boundary

A PreToolUse `Bash` hook rewrites `tool_input.command` before execution, while the file-access guard classifies commands through its bash analyzer. If the guard evaluates the pre-rewrite string, **the executed command is not the command that was approved** — a bypass of the exact boundary Phase 01 exists to establish. A guard that can be bypassed by command rewriting means Phase 01 is not releasable, which is why closing this is remediation rather than new capability.

Current configuration:

- The user's **global** `~/.claude/settings.json` registers a PreToolUse `Bash` hook pointing at an absolute path into this repository: `.github/hooks/scripts/rtk-rewrite.sh`.
- This project's `.claude/settings.json` registers a PreToolUse hook covering `Bash` (among other tools) → `.github/hooks/scripts/file-access-guard.py`.
- `rtk-rewrite.sh` reads `.tool_input.command` and delegates rewriting to an external `rtk` binary resolved from `PATH`.

Three properties make this fragile:

1. **Ordering determines correctness.** Whether the guard's analysis applies to the executed command depends on hook ordering between a global and a project hook. No test covers this.
2. **The blast radius is not this repo.** A global hook means every Bash command in every project routes through a script living here. Moving this repository breaks Bash hooks everywhere it is registered — the same absolute-path fragility already recorded for the eval hook symlink.
3. **The binary is unpinned and trusted on `PATH`.** The project's own RTK reference documents a name collision with a different published tool of the same name, making shadowing a stated install hazard rather than a hypothetical.

The fix has three parts, and all three are required: order the rewrite strictly before the guard (or re-run analysis on the rewritten command) so the guard's decision provably applies to what executes; pin and verify the `rtk` binary and its resolved path so a shadowed binary cannot enter the authorization path; and add a regression asserting that guard decisions apply to the rewritten command. The first alone closes the bypass but leaves an unpinned `PATH`-resolved binary inside the authorization boundary.

The general rule, recorded for future hook work: **any hook that mutates tool input must be ordered strictly before every hook that authorizes on that input, and that ordering needs a test.** Composition safety is not inheritable from the safety of each hook alone.

### Why the Phase 02 gate re-run is the right instrument

The Phase 03 evaluator run's delegated scan (`dev/phase-final-review/PHASE_05/z-security-scan-final.md`) classifies P2-SEC-01, P2-SEC-02, and P2-SEC-03 as **persisting**. That classification is correct for the revision it examined and does not describe current code. The scan records its subject explicitly: revision `344711df78c5` on branch `phase/phase-final-review-2`. At that commit, `redact_tool_output` in `.github/hooks/lib/framework.py` recursed through mappings and lists preserving container shape — the P2-SEC-01 defect itself. At HEAD the same function returns a fixed redacted shape and documents P2-SEC-01 by name.

The two conclusions are not in conflict; they describe different code. This is precisely why *"remediated in code is not verified"* cuts both ways: a stale scan is no more authoritative than a stale fix. Deliverable 3 exists to classify all three findings against final-state code, and the evidence-recency check in Deliverable 7 exists to catch this class of mismatch generally.

### Guard-rule loosening

`.github/hooks/config/file-access-rules.json` contains a `legacy_bash_parity` block with **17** entries classified `phase-retiered`, plus a lock-file rule narrowed to write-only.

`legacy_bash_parity` is a **metadata inventory, not enforcement**. Its entries carry only `source_pattern`, `classification`, and `rationale`; live enforcement lives in the `bash_rules`, `rules`, and `bash_analysis` blocks. Two consequences shape the review:

- Reinstating a rule means editing the enforcement blocks. Changing a `classification` value relabels an inventory entry and enforces nothing.
- The mapping is not one-to-one. Some entries collapse to a single enforcement rule; four curl/wget entries have no enforcement rule at all (see the inherited-findings table).

The review adjudicates all 17 against real enforcement. `tests/hooks/fixtures/bash/legacy-parity.json` is hard-coupled to this file via exact-string and count assertions, so any pattern change requires a lockstep fixture update.

### Other context

- **Phase 02 remediations already in code**: `redact_tool_output` in `.github/hooks/lib/framework.py` (fixed replacement shape), scan/candidate cap fail-closed behavior, and write-deny self-protection for the allowlisted source roots in `.github/hooks/config/file-access-rules.json`. Implemented but unverified by a gate re-run. Note that P2-SEC-02 covers **three** overflow paths — the scan-byte cap, the encoded-candidate budget, and `max_decoded_bytes` — and that the fail-closed block/replace behavior lives in `.github/hooks/scripts/injection-scanner.py`, not in the lib module, which only truncates and raises a notice. A classification drawn from the lib alone is a false negative.
- **REPO-SEC-06 containment**: a canonical helper already exists in `scripts/propagate_master_assets.py` (`_validate_nested_output_directory`). The work is routing the write path's call sites through it, not authoring a second contract — a second helper alongside it would be the finding rather than the fix.
- **Out-of-pipeline changes needing records**: `_project_root_hook_command` in `scripts/propagate_master_assets.py` (project-root anchoring for Claude/Codex/OpenCode wiring) and the guard-rule loosening.
- **Test entry points**: `.venv/bin/python -m pytest tests/` (system `python3` lacks pytest). The suite is **not a stable baseline** while PERF-01 is open — see PERF-01 above.

### Test impact

- `tests/hooks/test_hook_distribution_integration.py` — the latency gate is rewritten, not merely retuned. This file also pins the honesty of `docs/hooks/prompt-injection-defense.md` via exact-string assertions (`"50 ms"`, `"117 to 383 ms"`, `"NOT RUN"`, and a dated residual-risk approval), so Deliverable 7's documentation corrections require lockstep assertion updates. These documents are test-asserted by design; correcting them is expected to touch tests.
- `tests/hooks/test_file_access_guard.py`, `tests/hooks/test_bash_command_analyzer.py`, and the hard-coupled fixture `tests/hooks/fixtures/bash/legacy-parity.json` — encode the current, loosened behavior. Any reinstatement breaks them, correctly.
- `tests/hooks/test_rtk_rewrite_hook.py` — exists and covers the rewrite hook. Deliverable 2's ordering guarantee and binary pinning land here and in the guard's analyzer tests.
- Stale PERF-01 and NO-GO status text lives in four documents under `docs/hooks/`, not one. Deliverable 7 is unsatisfiable while the unnamed three contradict the corrected status.

## Dependencies & Risks

- **Dependency**: Live QA requires working installs of Claude Code, Codex, and OpenCode. Codex and OpenCode coverage is already classified Partial; live QA may confirm rather than remove that limitation.
- **Risk — the PERF-01 reshape is indistinguishable from the PR #22 cheat if done carelessly.** Mitigation: the budget's meaning is unchanged, the change is explicitly user-approved and recorded, and a deliberately slowed guard must fail the new gate as an acceptance criterion.
- **Risk — the rtk fix changes a hook every project depends on.** The rewrite hook is registered globally; a mistake here breaks Bash tool calls everywhere, not just in this repo. Mitigation: the fix is verified against a scratch consumer repo before the global registration is touched, and the absolute-path fragility is recorded regardless of whether it is re-pointed.
- **Risk — verification reveals more work.** Live QA has never run, so it is the most likely source of surprises. Mitigation: the findings containment rule below.
- **Risk — "remediated in code" is not "verified", and neither is a stale scan.** Every remediation needs fresh final-state evidence before any status line moves, and every finding classification needs to name the revision it examined.
- **Risk — live QA cannot be self-administered in this repo.** A guard failure blocks the tools needed to record the guard failure; this has already happened twice in practice, requiring the user to recover the session by hand. Mitigation: live QA runs against a scratch consumer repository with the kill switches pre-armed, and evidence is recorded from outside the guarded session.
- **Risk — the recovery path is two switches, not one.** `file-access-overrides.json` gates only the file-access guard; the injection scanner reads a separate `injection-overrides.json`, which does not exist. Creating that file disables the scanner, so restoring it means **deleting** it rather than writing `{}`. Arming one switch while provoking the other component is the self-administration failure above, with the recovery path missing for the component under test.

### Findings containment rule

New findings surfaced during this phase are fixed here **only if High or Critical**. Medium and below are recorded with routing and deferred. Without this rule, "verify the work" silently becomes "keep working" — and live QA, having never run, is exactly the kind of discovery that could expand indefinitely.

The rule cuts both ways and is not a lever. A finding is not promoted to High because fixing it is desirable, and not demoted to Medium because fixing it is inconvenient.

## Success Criteria

- [ ] The propagated-guard latency gate asserts a calibrated relative budget, passes reliably on both a quiet and a loaded machine, and no longer depends on ambient system load.
- [ ] A deliberately slowed guard fails the new latency gate — proving the reshape measures real cost rather than defining the problem away.
- [ ] The guard's decision provably applies to the command that actually executes, proven by a regression test that fails if a rewrite can slip past classification.
- [ ] The `rtk` binary and its resolved path are pinned and verified, so a shadowed binary on `PATH` cannot enter the authorization path.
- [ ] The Phase 02 security gate has been re-run against final-state code and records a verdict derived from fresh evidence for P2-SEC-01, P2-SEC-02 (all three overflow paths), and P2-SEC-03.
- [ ] All 17 loosened guard rules have a recorded verdict against real enforcement; unjustified loosenings are reinstated with a test pair proving the attack blocks and the benign input still passes; the curl/wget coverage gap is recorded with routing.
- [ ] REPO-SEC-06 is resolved through a single canonical no-follow containment contract, routed through the existing helper rather than a second one.
- [ ] Live QA has been executed for Phases 01 and 02 on Claude Code, and attempted on Codex and OpenCode, with per-harness results and support tiers recorded — run against a scratch consumer repo, not this one.
- [ ] No implementation record retains a `PENDING` commit SHA.
- [ ] The project-root hook-command anchoring has a phase record describing what changed and why.
- [ ] Documentation states no remediation as complete that is not backed by fresh evidence, across all four affected `docs/hooks/` documents, with test assertions updated in lockstep.
- [ ] Every piece of evidence post-dates the last change to the code it covers; anything invalidated by a later change is re-run or marked stale.
- [ ] Phase 03 has a user-issued NO-GO with its open findings enumerated and routed back to Phase 03's rescope.
- [ ] Each of Phases 01 and 02 has a user-issued verdict backed by evidence — GO or NO-GO, either is a valid outcome of this phase.

## QA Considerations

This phase is largely QA, and it carries the project's **first live agent-session testing**. Manual QA docs are mandatory, not optional.

- **A smoke pass runs early, not at the tail.** Live QA is the highest-uncertainty item in the phase and has already contradicted the passing test suite twice — once via a false-positive prompt storm, once via a subdirectory outage that bricked a session. Both were found live; neither was found by a green suite. An early smoke pass de-risks the remediation work before it is finished. The full walkthrough still runs at the end against the final state.
- Live QA must cover the enforcement tiers that only exist at runtime: PreToolUse deny under bypass permissions, PostToolUse output replacement, Stop behavior, and subagent contexts.
- **The rewrite-ordering fix needs live verification, not just a unit test.** The bypass depends on how a global hook and a project hook compose at runtime, which is exactly the class of thing that passes in isolation and fails in a session.
- The subdirectory case must be tested **per harness**, not once. The project-root anchoring rewrites Claude and Codex hook commands but leaves OpenCode's unchanged — OpenCode relies on its plugin working directory instead. A pass on one harness is not evidence about the others.
- The guard's friction profile should be QA'd deliberately: benign commands (`ls`, `grep`, `npm test > /dev/null`, reading lock files, commit messages mentioning `rm -rf`) must not prompt, while genuinely destructive commands must. This is a stated project constraint and was a live user complaint.
- Recovery paths need live verification: **both** kill switches, and the fact that a guard failure must never require a blocked tool to recover from.
- QA must record NOT RUN honestly where a harness is unavailable. A missing check is a NO-GO input, not an omission.

## Notes for Feature - Decomposer

Suggested feature boundaries, ordered so that verification work is not blocked by remediation work:

1. **PERF-01 latency stabilization** — self-contained: the calibrated-baseline methodology plus its slow-guard regression proof. The regression proof is an acceptance criterion, not a nice-to-have — it is what distinguishes this reshape from the reverted PR #22 threshold edit.
2. **Live QA smoke pass** — small and early. Just enough to confirm the guard and scanner behave in a live session at all. Runs against a scratch consumer repo with **both** kill switches armed. Feeds findings into the remediation features while they are still in flight.
3. **Bash-rewrite bypass fix** — ordering guarantee, binary pinning, and the regression that proves guard decisions apply to the executed command. Verify against a scratch consumer repo before touching the global registration; a mistake here breaks Bash tool calls in every project.
4. **Guard-rule security review** — all 17 rules, adjudicated against real enforcement rather than the metadata inventory. Owns `file-access-rules.json` and its hard-coupled parity fixture.
5. **Phase 02 security gate re-run and verdict** — verification-only. **Sequence it after the guard-rule review**: P2-SEC-03's remediation lives in the same rules file, so a scan run before that review lands classifies a file that then changes. This is the same staleness that produced the `344711d` mismatch; do not reproduce it.
6. **REPO-SEC-06 containment** — propagation write path only. Independent of everything else here; parallel-safe.
7. **Full live multi-harness QA** — depends on the remediation features being complete, since it validates the final state. This is the phase's tail.
8. **Records and reconciliation** — the DOC-01 SHAs and the anchoring record. **Documentation that describes verdicts is not part of this feature** — it cannot be written before the verdicts it describes, so it belongs at the tail.
9. **Release evidence consolidation** — the integration feature. Every other feature produces evidence in isolation and none can tell whether the evidence, taken together, supports a release decision. This one assembles the per-phase dossier, verifies that every artifact post-dates the code it covers, surfaces contradictions rather than averaging them, enumerates Phase 03's open findings for routing, hands the dossier to the user for hand-issued verdicts, and only then writes the records those verdicts imply.

Integration points to watch: features 4 and 5 both touch `file-access-rules.json`; features 3 and 7 both exercise the guard's bash analysis and must not double-record findings. The phase's defining rule is that **no status line moves without fresh evidence** — decomposition should make evidence production an explicit deliverable of each feature, not a side effect. Verdicts themselves are issued by the user, by hand; no feature should attempt to write one.
