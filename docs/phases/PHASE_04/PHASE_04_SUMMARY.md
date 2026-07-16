# Phase 4: Release Remediation & Verification

**Status**: Planned
**Depends on**: Phases 01, 02, 03 (all implemented; all release-blocked)
**Estimated complexity**: Large
**Cross-references**: `docs/phases/DISCOVERY_CONTEXT.md`, `docs/phases/PHASE_01/PHASE_01-qa-analysis.md` (SEC-01, PERF-01, DOC-01), `docs/phases/PHASE_02/PHASE_02-security-scan.md` (P2-SEC-01..03), `docs/phases/PHASE_03/PHASE_03-qa-analysis.md` (P5-SEC-01/02, REPO-SEC-06, runtime blockers), `docs/hooks/prompt-injection-defense.md`, `.github/learnings/cross-phase-decisions.md`

## What's New

Nothing new ships in this phase — that is the point. Three phases of work are finished and none of it can be released: the hooks, the injection scanner, and the phase-review agents are all implemented but sitting behind open blockers, and **not one of them has ever been tested in a live agent session**. Every claim about them rests on automated tests and payload fixtures.

This phase stops adding surface area and instead makes the existing work trustworthy. It closes the remaining security findings, replaces a performance gate that could never pass with one that measures the thing that actually matters, runs the real end-to-end QA in Claude Code, Codex, and OpenCode for the first time, and reconciles the written record with what is genuinely true. When it completes, Phases 01–03 are either releasable or honestly recorded as not releasable, with evidence either way.

## Objective

Convert Phases 01, 02, and 03 from "implemented but blocked" to a verified verdict by closing every open blocker, executing the live multi-harness QA that has never run, and correcting records and documentation that currently overstate remediation status.

## Audience and Bar

The current adopters are **the author and friends** — people who can ask a question and get an answer. That fact is what makes several residual risks in this phase acceptable, and it is recorded here because if it changes, the bar changes with it:

- Codex tool-coverage parity stays an accepted limitation, documented rather than redesigned.
- The file-access guard's friction profile stays hand-tuned to the author's workflow rather than made configurable.
- Distribution stays "clone the repo and run propagation" rather than a packaged install.

Broad public adoption would invalidate all three — partial protection that reads as total protection is worse than none once the user cannot ask. That work is deliberately **not** in this phase; see "Deferred to a Future Phase" below.

## Scope

### In Scope

- **PERF-01 (Phase 01)**: replace the unachievable wall-clock assertion with a calibrated relative budget that holds across machines and load, without weakening what the budget represents.
- **Phase 02 security gate re-run**: re-execute the security gate against the P2-SEC-01/P2-SEC-02/P2-SEC-03 remediations already made in code, and record a verified verdict.
- **Phase 03 security findings**: resolve P5-SEC-01 and P5-SEC-02 (introduced High), address the worsened REPO-SEC-06, remove or sandbox `execute`, and enforce report-root/fixture-only path allowlists with canonical no-follow containment.
- **Phase 03 runtime gaps**: close the Wave 4 `05d`/AC6 blocker (delegated Security Scan did not complete; no canonical `05d` report) and the Wave 6 full-flow blocker (eight evaluator checks not-run, AC5 partial).
- **Live harness QA**: execute the `NOT RUN` manual QA for Phases 01, 02, and 03 across Claude Code, Codex, and OpenCode, recording honest per-harness support tiers.
- **Security review of out-of-pipeline changes**: the file-access-guard false-positive tuning **loosened** enforcement (9 `legacy_bash_parity` entries reclassified `phase-retiered`; lock-file rules narrowed to write-only) during an ad-hoc debugging session with no scan, no review record, and no QA. It needs a security review, not merely a changelog entry.
- **Record reconciliation**: close DOC-01's `PENDING` commit SHAs; fold the project-root hook-command anchoring into the phase record.
- **Documentation correction**: keep statements about remediation status matched to verified reality.
- **Propagation test expansion**: enumerate all Phase 03 agents (especially `05g`/`05j`/`05k`) across all three harnesses; reconcile the execution manifest's test inventory.

### Out of Scope

- Any new hook capability, rule, or agent. This phase adds no features.
- Format-on-save and completion gates (Phase 05) and skill enforcement (Phase 06).
- **Using `05-phase-final-review` to produce this phase's verdicts.** Phase 03 built the machinery that issues go/no-go verdicts for phases, and this phase issues go/no-go verdicts for phases — including Phase 03's own. Certifying that tool with itself is not independent evidence, and standing the full flow up is more machinery than the job needs. Verdicts here are **issued by the user, by hand, from the evidence each feature produces.** The fixture dry-run remains in scope as Phase 03's own acceptance evidence; that is a dry-run, not a review flow.
- Raising, relaxing, or conditionalizing what the latency budget represents in order to make PERF-01 pass. Changing *what is measured* is in scope and is a user-approved AC change (see PERF-01 below); changing *how much latency is acceptable* is not.
- Renaming the `05-phase-final-review` agent family or the `dev/phase-final-review/fixtures/PHASE_05/` fixtures (see the roadmap's numbering note).
- Adoption readiness: packaging, install UX, configurable friction, upgrade path. See below.

### Deferred to a Future Phase

Making this suite fit for adoption beyond the author's circle is real work and is **not** part of this phase: a packaged install path (the deferred plugin-packaging idea in `.github/learnings/cross-phase-decisions.md`), a friction budget tunable without editing rule files, recovery and kill-switch documentation written for someone who is not the author, an upgrade path when rules change, and an install-time disclosure of Codex's partial coverage. This requires a new roadmap entry and belongs to `@project-planner`, not to this phase.

## Key Deliverables

| # | Deliverable | Description | Likely Features |
|---|-------------|-------------|-----------------|
| 1 | Trustworthy latency gate | PERF-01 closed: a calibrated relative budget that is deterministic across machines and load, plus proof that a genuinely slow guard still fails it. | Phase 01 performance |
| 2 | Phase 02 verified verdict | Security gate re-run against the three remediations; verdict recorded from fresh final-state evidence. | Phase 02 security verification |
| 3 | Phase 03 security remediation | P5-SEC-01, P5-SEC-02, REPO-SEC-06 resolved; `execute` removed or sandboxed; path allowlists and no-follow containment enforced; model-trusted report claims replaced with validated structured evidence. | Phase 03 security |
| 4 | Phase 03 runtime completion | `05d`/AC6 canonical report produced; the eight not-run Wave 6 evaluator checks executed; AC5 complete or explicitly evidenced as NOT RUN. | Phase 03 runtime |
| 5 | Live multi-harness QA | First live execution of Claude/Codex/OpenCode QA for Phases 01–03, with per-harness support tiers recorded honestly. | QA execution |
| 6 | Record and doc reconciliation | Security review of the guard-rule loosening; DOC-01 SHAs closed; anchoring fix recorded; propagation tests expanded; docs matched to verified reality. | Records/docs |

## Technical Context

### PERF-01

Gate at `tests/hooks/test_hook_distribution_integration.py::test_ac9_propagated_guard_median_latency_is_below_50_ms`.

The 50 ms budget is **not** the problem — the guard costs ~30 ms. The problem is the assertion's shape. A wall-clock median measured on a machine whose load is not controlled leaves ~20 ms of headroom against ambient noise, so the gate fails 2 of 6 focused runs while the guard itself has not changed. It reproduces PHASE_01-qa-analysis's original "failed two of five observed runs" for the same reason. No number of consecutive green runs fixes this; it is a probabilistic gate that can be passed by luck.

The approved reshape is a **calibrated relative budget**: capture a bare-interpreter baseline in the same run and assert the guard's cost *above* that baseline. This measures the guard's own cost rather than the machine's mood, it holds on loaded and quiet machines alike, and it directly encodes the root cause already established — the original overshoot was `python3` resolving through a pyenv shim (~50 ms of shell re-resolution per call; ~62 ms for a bare `python3 -c pass`), not guard logic.

This is a user-approved AC change per `.github/learnings/cross-phase-decisions.md` ("A fixed budget must never be relaxed to make a gate pass... the honest outcome is an explicit user-approved AC change, not a quietly edited threshold"). **PR #22 silently raised this threshold from 50 to 90 ms to mask the failure and was reverted.** The distinction that keeps this reshape honest is that a slow guard must still fail — which is why that is an explicit acceptance criterion below, not an assumption.

### Other context

- **Phase 02 remediations already in code**: `redact_tool_output` in `.github/hooks/lib/framework.py` (fixed replacement shape), scan/candidate cap fail-closed behavior in `.github/hooks/lib/injection_scanner.py` and `.github/hooks/scripts/injection-scanner.py`, and write-deny self-protection for the allowlisted source roots in `.github/hooks/config/file-access-rules.json`. Implemented but unverified by a gate re-run.
- **Phase 03 artifacts**: blockers and root-cause routing are in `docs/phases/PHASE_03/PHASE_03-qa-analysis.md` (§ "Blocking Items and Root-Cause Routing"); the remediation verification plan is `docs/phases/PHASE_03/PHASE_03_QA.md`. Both use pre-renumber Phase 05 numbering in their bodies — see the note at the top of each file.
- **`execute` blast radius**: granted in `tools:` frontmatter to `05-phase-final-review`, `05a-baseline-worktree`, `05g-artifact-sweeper`, `05j-consistency-auditor`, and `05k-dependency-auditor`. `05i-learnings-harvester` already declares a "never use `execute`" contract that is assertion-covered. `05a` genuinely needs command capability (git worktree checkout); the three mechanical sweeps are the candidates for removal or sandboxing.
- **Out-of-pipeline changes needing records**: `_project_root_hook_command` in `scripts/propagate_master_assets.py` (project-root anchoring for Claude/Codex/OpenCode wiring) and the guard-rule loosening in `.github/hooks/config/file-access-rules.json`.
- **Test entry points**: `.venv/bin/python -m pytest tests/` (system `python3` lacks pytest). Current baseline is 416 passed, 15 subtests, with the latency gate intermittently failing.

### Test impact

Deliverables 1 and 3 are the ones that will break existing tests:

- `tests/hooks/test_hook_distribution_integration.py` — the latency gate is rewritten, not merely retuned.
- `tests/test_readiness_synthesis_agents.py` — asserts agent tool contracts directly (`"never use \`execute\`" in instructions`); changing `execute` grants will move these assertions.
- `tests/test_propagate_master_assets.py` — propagates agent `tools:` frontmatter; both the `execute` change and the propagation-enumeration expansion land here.
- `tests/hooks/test_file_access_guard.py` and `tests/hooks/test_bash_command_analyzer.py` — the security review of the loosened rules may reinstate enforcement these now assert is absent.

## Dependencies & Risks

- **Dependency**: Phase 03's runtime gaps require the evaluator collaboration runtime (delegated Security Scan, Test - Analyst, code-review-graph) to actually be available. It was unavailable during the original review; if it stays unavailable, those checks cannot be closed and must be recorded as NOT RUN rather than assumed.
- **Dependency**: Live QA requires working installs of Claude Code, Codex, and OpenCode. Codex and OpenCode coverage is already classified Partial; live QA may confirm rather than remove that limitation.
- **Risk — the PERF-01 reshape is indistinguishable from the PR #22 cheat if done carelessly.** Mitigation: the budget's meaning is unchanged, the change is explicitly user-approved and recorded, and a deliberately slowed guard must fail the new gate as an acceptance criterion.
- **Risk — verification reveals more work.** Live QA has never run, so it is the most likely source of surprises. Mitigation: the findings containment rule below.
- **Risk — "remediated in code" is not "verified".** The temptation is to treat already-written fixes as done. Every remediation needs fresh final-state evidence before any status line moves.
- **Risk — live QA cannot be self-administered in this repo.** A guard failure blocks the tools needed to record the guard failure; this has already happened twice in practice, requiring the user to recover the session by hand. Mitigation: live QA runs against a scratch consumer repository with the human-only kill switch pre-armed, and evidence is recorded from outside the guarded session.
- **Risk — the fixture/agent numbering is deliberately inconsistent** with phase numbers after the 2026-07-16 renumber. Mitigation: the roadmap mapping table and per-file notes; do not "fix" `05a`–`05l` or `fixtures/PHASE_05/`.

### Findings containment rule

New findings surfaced during this phase are fixed here **only if High or Critical**. Medium and below are recorded with routing and deferred to a later phase. Without this rule, "verify the work" silently becomes "keep working" — and live QA, having never run, is exactly the kind of discovery that could expand indefinitely.

## Success Criteria

- [ ] The propagated-guard latency gate asserts a calibrated relative budget, passes reliably on both a quiet and a loaded machine, and no longer depends on ambient system load.
- [ ] A deliberately slowed guard fails the new latency gate — proving the reshape measures real cost rather than defining the problem away.
- [ ] The Phase 02 security gate has been re-run against final-state code and records a verdict derived from fresh evidence for P2-SEC-01, P2-SEC-02, and P2-SEC-03.
- [ ] P5-SEC-01, P5-SEC-02, and REPO-SEC-06 each have a recorded resolution with final-state evidence, or an explicit user-accepted residual-risk entry.
- [ ] `execute` is removed or sandboxed for every agent that does not require command capability, and report-root/fixture-only path allowlists with no-follow containment are enforced and regression-tested.
- [ ] A canonical `05d` report exists and classifies P2-SEC-01..03 from final-state evidence; the eight previously not-run Wave 6 evaluator checks are either executed or recorded as NOT RUN with reasons.
- [ ] Live QA has been executed for Phases 01, 02, and 03 on Claude Code, and attempted on Codex and OpenCode, with per-harness results and support tiers recorded — run against a scratch consumer repo, not this one.
- [ ] The guard-rule loosening has a security review recording which enforcement was removed, why it was safe, and what evidence supports that.
- [ ] No implementation record retains a `PENDING` commit SHA.
- [ ] The project-root hook-command anchoring has a phase record describing what changed and why.
- [ ] Documentation states no remediation as complete that is not backed by fresh evidence.
- [ ] Propagation tests enumerate every Phase 03 agent (including `05g`, `05j`, `05k`) across Claude, Codex, and OpenCode.
- [ ] Each of Phases 01, 02, and 03 has a user-issued verdict backed by evidence — GO or NO-GO, either is a valid outcome of this phase.

## QA Considerations

This phase is almost entirely QA, and it carries the project's **first live agent-session testing**. Manual QA docs are mandatory, not optional.

- **A smoke pass runs early, not at the tail.** Live QA is the highest-uncertainty item in the phase and has already contradicted the passing test suite twice — once via a false-positive prompt storm, once via a subdirectory outage that bricked a session. Both were found live; neither was found by 416 green tests. An early smoke pass (does the guard fire at all in a live session, does output replacement actually happen) de-risks features 1–4 before they are finished. The full walkthrough still runs at the end against the final state.
- Live QA must cover the enforcement tiers that only exist at runtime: PreToolUse deny under bypass permissions, PostToolUse output replacement, Stop behavior, and subagent contexts.
- The guard's friction profile should be QA'd deliberately: benign commands (`ls`, `grep`, `npm test > /dev/null`, reading lock files, commit messages mentioning `rm -rf`) must not prompt, while genuinely destructive commands must. This is a stated project constraint and was a live user complaint.
- Recovery paths need live verification: the human-only kill switch, and the fact that a guard failure must never require a blocked tool to recover from.
- QA must record NOT RUN honestly where a harness or delegate is unavailable. A missing check is a NO-GO input, not an omission.

## Notes for Feature - Decomposer

Suggested feature boundaries, ordered so that verification work is not blocked by remediation work:

1. **PERF-01 latency stabilization** (Phase 01) — self-contained: the calibrated-baseline methodology plus its slow-guard regression proof. Keep strictly separate from the security features; it is the only performance work here. The regression proof is an acceptance criterion, not a nice-to-have — it is what distinguishes this reshape from the reverted PR #22 threshold edit.
2. **Live QA smoke pass** — small and early. Just enough to confirm the guard and scanner behave in a live session at all. Runs against a scratch consumer repo with the kill switch armed. Feeds findings into features 1, 3, and 4 while they are still in flight.
3. **Phase 02 security gate re-run and verdict** — verification-only; no new code expected unless the re-run finds gaps. Depends on nothing else in this phase.
4. **Phase 03 security remediation** — the largest code-change feature: P5-SEC-01/02, REPO-SEC-06, `execute` sandboxing, path allowlists, structured-evidence validation. Note the overlap with feature 7: `05g`/`05j`/`05k` are simultaneously the agents holding unnecessary `execute` grants and the agents missing from the propagation test enumeration. Sequence them so the tool-contract change lands before the enumeration expansion, or they will conflict in `tests/test_propagate_master_assets.py`.
5. **Phase 03 runtime completion** — `05d`/AC6 and the Wave 6 eight checks. Depends on feature 4 landing first if the security fixes change evaluator behavior; may be blocked entirely by runtime availability, so it must degrade to explicit NOT RUN evidence rather than stalling the phase.
6. **Full live multi-harness QA** — depends on features 1, 3, 4, and 5 being complete, since it validates the final state. This is the phase's tail.
7. **Records and propagation** — safe to run in parallel with anything: the security review of the guard-rule loosening, DOC-01 SHAs, the anchoring fix record, and propagation test enumeration. **Documentation that describes verdicts is not part of this feature** — it cannot be written before the verdicts it describes, so it belongs at the tail alongside feature 6.

Integration points to watch: features 4 and 5 both touch the Phase 03 evaluator family and can conflict; features 3 and 6 both produce security evidence and must not double-record findings. The phase's defining rule is that **no status line moves without fresh evidence** — decomposition should make evidence production an explicit deliverable of each feature, not a side effect. Verdicts themselves are issued by the user, by hand; no feature should attempt to write one.
