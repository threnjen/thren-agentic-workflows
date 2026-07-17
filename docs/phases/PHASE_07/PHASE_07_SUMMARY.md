# Phase 7: Hook Release Remediation & Verification

**Status**: Planned
**Depends on**: Phases 01, 02 (Phase 01's framework/propagation implemented and carried forward by Phase 04; Phase 02 implemented and release-blocked)
**Required by**: Phases 05 and 06 — both build on a verified hook foundation. This phase carries a number higher than its dependents because phase numbers in this project record identity, not execution order; the `Depends On` column is authoritative.
**Estimated complexity**: Medium
**Cross-references**: `docs/phases/DISCOVERY_CONTEXT.md`, `docs/phases/PHASE_02/PHASE_02-security-scan.md` (P2-SEC-01..03), `docs/phases/PHASE_03/PHASE_03-qa-analysis.md` (Phase 03's open findings, retained by Phase 03's own rescope), `docs/phases/PHASE_03/PHASE_03_SUMMARY.md` (the PR Review rescope that retains them), `docs/phases/PHASE_01/PHASE_01_SUMMARY.md` (surviving framework/propagation deliverables), `docs/phases/PHASE_04/PHASE_04_SUMMARY.md` (guard retirement; cross-platform deployment this phase's QA verifies), `dev/phase-final-review/PHASE_05/z-security-scan-final.md` (F-15), `docs/hooks/prompt-injection-defense.md`, `.github/learnings/cross-phase-decisions.md`

## What's New

Nothing new ships in this phase — that is the point. The project's one remaining live hook-security component, the injection scanner, is implemented but sitting behind an open blocker, and **has never been tested in a live agent session**. Every claim about it rests on automated tests and payload fixtures. Phase 01's hook framework and propagation deliverables carry a similar gap: they are implemented and extended by Phase 04's cross-platform deployment, but that deployment's live fresh-session evidence is `NOT RUN` on every platform.

This phase stops adding surface area and makes the surviving hooks trustworthy. It closes the remaining Phase 02 blocker, resolves a propagation-containment gap, runs the real end-to-end QA in Claude Code, Codex, and OpenCode for the first time, and reconciles the written record with what is genuinely true. When it completes, Phase 02 is either releasable or honestly recorded as not releasable, with evidence either way, and Phase 01's surviving framework/propagation deliverables have live QA evidence to match what Phase 04 already implemented.

## Objective

Convert Phase 02 from "implemented but blocked" to a verified verdict, and give Phase 01's surviving framework/propagation deliverables their first live-harness evidence, by closing the open Phase 02 blocker, resolving REPO-SEC-06, executing the live multi-harness QA that has never run, and correcting records and documentation that currently overstate remediation status.

## Audience and Bar

The current adopters are **the author and friends** — people who can ask a question and get an answer. That fact is what makes several residual risks acceptable, and it is recorded here because if it changes, the bar changes with it:

- Codex tool-coverage parity stays an accepted limitation, documented rather than redesigned.
- Distribution stays "clone the repo and run propagation" rather than a packaged install.

Broad public adoption would invalidate both — partial protection that reads as total protection is worse than none once the user cannot ask. That work is deliberately **not** in this phase; see "Deferred to a Future Phase" below.

## Scope

### In Scope

- **Phase 02 security gate re-run**: re-execute the security gate against the P2-SEC-01/P2-SEC-02/P2-SEC-03 remediations already made in code, and record a verified verdict from final-state evidence.
- **REPO-SEC-06**: resolve the propagation containment gap via a single canonical no-follow contract. This is propagation code, independent of the agent family.
- **Live harness QA**: execute the `NOT RUN` manual QA for Phase 02's scanner and for Phase 01's surviving framework/propagation deliverables across Claude Code, Codex, and OpenCode, recording honest per-harness support tiers.
- **Record reconciliation**: close DOC-01's `PENDING` commit SHAs; fold the project-root hook-command anchoring into the phase record.
- **Documentation correction**: keep statements about remediation status matched to verified reality.
- **Phase 03 verdict**: issue a NO-GO from existing evidence, with its open findings enumerated and routed back to Phase 03's rescope.

### Out of Scope

- Any new hook capability, rule, or agent. This phase adds no features.
- **The `05a`–`05l` agent family.** Its `execute` grants, its propagation-enumeration gap, its runtime evidence, and P5-SEC-02 all belong to Phase 03's rescope. Fixing capability grants on agents slated for rewrite is churn, and enumerating agents slated for retirement is worse.
- Format-on-save and completion gates, and skill enforcement.
- Adoption readiness: packaging, install UX, configurable friction, upgrade path. See below.

### Deferred to a Future Phase

Making this suite fit for adoption beyond the author's circle is real work and is **not** part of this phase: a packaged install path (the deferred plugin-packaging idea in `.github/learnings/cross-phase-decisions.md`), recovery documentation written for someone who is not the author, an upgrade path when rules change, and an install-time disclosure of Codex's partial coverage. This requires a new roadmap entry and belongs to `@project-planner`.

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
| 1 | Phase 02 verified verdict | Security gate re-run against final-state code; verdict recorded from fresh evidence for all three P2-SEC findings. | Phase 02 security verification |
| 2 | Containment contract | REPO-SEC-06 resolved through one canonical no-follow contract in the propagation write path. | Propagation security |
| 3 | Live multi-harness QA | First live execution of Claude/Codex/OpenCode QA for Phase 02's scanner and Phase 01's surviving framework/propagation deliverables, with per-harness support tiers recorded honestly. | QA execution |
| 4 | Record and doc reconciliation | DOC-01 SHAs closed; anchoring fix recorded; docs matched to verified reality; Phase 03's findings enumerated and routed. | Records/docs |

## Technical Context

### Why the Phase 02 gate re-run is the right instrument

The Phase 03 evaluator run's delegated scan (`dev/phase-final-review/PHASE_05/z-security-scan-final.md`) classifies P2-SEC-01, P2-SEC-02, and P2-SEC-03 as **persisting**. That classification is correct for the revision it examined and does not describe current code. The scan records its subject explicitly: revision `344711df78c5` on branch `phase/phase-final-review-2`. At that commit, `redact_tool_output` in `.github/hooks/lib/framework.py` recursed through mappings and lists preserving container shape — the P2-SEC-01 defect itself. At HEAD the same function returns a fixed redacted shape and documents P2-SEC-01 by name.

The two conclusions are not in conflict; they describe different code. This is precisely why *"remediated in code is not verified"* cuts both ways: a stale scan is no more authoritative than a stale fix. Deliverable 1 exists to classify all three findings against final-state code, and the evidence-recency check in Deliverable 4 exists to catch this class of mismatch generally.

### Other context

- **Phase 02 remediations already in code**: `redact_tool_output` in `.github/hooks/lib/framework.py` (fixed replacement shape) and scan/candidate cap fail-closed behavior. Implemented but unverified by a gate re-run. Note that P2-SEC-02 covers **three** overflow paths — the scan-byte cap, the encoded-candidate budget, and `max_decoded_bytes` — and that the fail-closed block/replace behavior lives in `.github/hooks/scripts/injection-scanner.py`, not in the lib module, which only truncates and raises a notice. A classification drawn from the lib alone is a false negative.
- **REPO-SEC-06 containment**: a canonical helper already exists in `scripts/propagate_master_assets.py` (`_validate_nested_output_directory`). The work is routing the write path's call sites through it, not authoring a second contract — a second helper alongside it would be the finding rather than the fix.
- **Out-of-pipeline changes needing records**: `_project_root_hook_command` in `scripts/propagate_master_assets.py` (project-root anchoring for Claude/Codex/OpenCode wiring).
- **Test entry points**: `.venv/bin/python -m pytest tests/` (system `python3` lacks pytest).

### Test impact

- This file also pins the honesty of `docs/hooks/prompt-injection-defense.md` via exact-string assertions (`"NOT RUN"` and a dated residual-risk approval), so Deliverable 4's documentation corrections require lockstep assertion updates. These documents are test-asserted by design; correcting them is expected to touch tests.
- Stale NO-GO status text lives in multiple documents under `docs/hooks/`. Deliverable 4 is unsatisfiable while any of them contradict the corrected status.

## Dependencies & Risks

- **Dependency**: Live QA requires working installs of Claude Code, Codex, and OpenCode. Codex and OpenCode coverage is already classified Partial; live QA may confirm rather than remove that limitation.
- **Risk — verification reveals more work.** Live QA has never run, so it is the most likely source of surprises. Mitigation: the findings containment rule below.
- **Risk — "remediated in code" is not "verified", and neither is a stale scan.** Every remediation needs fresh final-state evidence before any status line moves, and every finding classification needs to name the revision it examined.
- **Risk — the recovery path for the scanner is a separate switch from the retired guard's.** `.github/hooks/config/injection-overrides.json` does not exist by default; creating it disables the scanner, so restoring it means **deleting** it rather than writing `{}`. Any live QA that provokes the scanner must arm this switch before doing so.

### Findings containment rule

New findings surfaced during this phase are fixed here **only if High or Critical**. Medium and below are recorded with routing and deferred. Without this rule, "verify the work" silently becomes "keep working" — and live QA, having never run, is exactly the kind of discovery that could expand indefinitely.

The rule cuts both ways and is not a lever. A finding is not promoted to High because fixing it is desirable, and not demoted to Medium because fixing it is inconvenient.

## Success Criteria

- [ ] The Phase 02 security gate has been re-run against final-state code and records a verdict derived from fresh evidence for P2-SEC-01, P2-SEC-02 (all three overflow paths), and P2-SEC-03.
- [ ] REPO-SEC-06 is resolved through a single canonical no-follow containment contract, routed through the existing helper rather than a second one.
- [ ] Live QA has been executed for Phase 02 on Claude Code, and attempted on Codex and OpenCode, with per-harness results and support tiers recorded — run against a scratch consumer repo, not this one.
- [ ] Live QA has been executed for Phase 01's surviving framework and propagation deliverables on Claude Code, and attempted on Codex and OpenCode, with per-harness results recorded.
- [ ] No implementation record retains a `PENDING` commit SHA.
- [ ] The project-root hook-command anchoring has a phase record describing what changed and why.
- [ ] Documentation states no remediation as complete that is not backed by fresh evidence, with test assertions updated in lockstep.
- [ ] Every piece of evidence post-dates the last change to the code it covers; anything invalidated by a later change is re-run or marked stale.
- [ ] Phase 03 has a user-issued NO-GO with its open findings enumerated and routed back to Phase 03's rescope.
- [ ] Phase 02 has a user-issued verdict backed by evidence — GO or NO-GO, either is a valid outcome of this phase.

## QA Considerations

This phase is largely QA, and it carries the project's **first live agent-session testing**. Manual QA docs are mandatory, not optional.

- **A smoke pass runs early, not at the tail.** Live QA is the highest-uncertainty item in the phase — this project's hooks have already contradicted a passing test suite live before, and neither incident was found by a green suite. An early smoke pass de-risks the remediation work before it is finished. The full walkthrough still runs at the end against the final state.
- Live QA must cover the enforcement tiers that only exist at runtime: PostToolUse output replacement, Stop behavior, and subagent contexts.
- The subdirectory case must be tested **per harness**, not once. The project-root anchoring rewrites Claude and Codex hook commands but leaves OpenCode's unchanged — OpenCode relies on its plugin working directory instead. A pass on one harness is not evidence about the others.
- Recovery needs live verification: the scanner's kill switch, and the fact that a scanner failure must never require a blocked tool to recover from.
- QA must record NOT RUN honestly where a harness is unavailable. A missing check is a NO-GO input, not an omission.

## Notes for Feature - Decomposer

Suggested feature boundaries, ordered so that verification work is not blocked by remediation work:

1. **Live QA smoke pass** — small and early. Just enough to confirm the scanner and hook framework behave in a live session at all. Runs against a scratch consumer repo with the kill switch armed. Feeds findings into the remediation features while they are still in flight.
2. **Phase 02 security gate re-run and verdict** — verification-only, against final-state code.
3. **REPO-SEC-06 containment** — propagation write path only. Independent of everything else here; parallel-safe.
4. **Full live multi-harness QA** — depends on the remediation features being complete, since it validates the final state. This is the phase's tail.
5. **Records and reconciliation** — the DOC-01 SHAs and the anchoring record. **Documentation that describes verdicts is not part of this feature** — it cannot be written before the verdicts it describes, so it belongs at the tail.
6. **Release evidence consolidation** — the integration feature. Every other feature produces evidence in isolation and none can tell whether the evidence, taken together, supports a release decision. This one assembles the per-phase dossier, verifies that every artifact post-dates the code it covers, surfaces contradictions rather than averaging them, enumerates Phase 03's open findings for routing, hands the dossier to the user for hand-issued verdicts, and only then writes the records those verdicts imply.

Integration point to watch: feature 4 exercises the surviving hooks in a live session and must not double-record findings already surfaced by feature 1's smoke pass. The phase's defining rule is that **no status line moves without fresh evidence** — decomposition should make evidence production an explicit deliverable of each feature, not a side effect. Verdicts themselves are issued by the user, by hand; no feature should attempt to write one.
