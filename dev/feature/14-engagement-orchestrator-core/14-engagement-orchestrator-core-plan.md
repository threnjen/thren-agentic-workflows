# Plan: 14-engagement-orchestrator-core

## Execution Metadata

- **Wave:** 1
- **Parallel safe:** yes
- **Depends on:** none
- **Key files modified:** `source_of_truth/agents/engagement-orchestrator.agent.md` [PROPOSED - name TBD], `source_of_truth/skills/engagement-workspace/SKILL.md` [PROPOSED - name TBD], `source_of_truth/skills/engagement-configuration/SKILL.md`, `tests/test_propagate_master_assets.py` (verify — marker-guard counts), `source_of_truth/agents/README.md` (verify — catalog entry may defer to 18)
- **Sequential reason:** n/a

Phase document: `docs/phases/PHASE_02/PHASE_02_SUMMARY.md` (Key Deliverable 1, bundle 1).

## A. Requirements & Traceability

Acceptance criteria:

- **AC1**: A single engagement orchestrator agent exists in `source_of_truth/agents/` that consumes the engagement configuration, runs the per-pair loop, and spawns all real work as subagents. It holds only the pair list and compact per-side/per-pair results (status + pointers); bulk child content is recorded as an on-disk location and discarded; it never reads engagement source code itself.
- **AC2**: The orchestrator spawns `engagement-prepare` **unchanged** as its first per-engagement step and consumes its compact report. `engagement-prepare.agent.md` is not modified by this feature.
- **AC3**: Run-time entry checking is a paragraph of orchestrator instruction: before later stages, verify analysis branches and graphs exist for the sides in play; report exactly which side is unprepared. No formal preflight tool.
- **AC4**: The engagement output-directory layout is defined once (single per-engagement workspace root outside every client repository, per-pair/per-side folder layout) and is the destination for all engagement outputs — client-facing docs, internal artifacts, raw reports, manifest, working-state file. No agent writes deliverables into a client repo; all manifest paths resolve within this root. This layout is a contract later bundles (15–18) reference, not restate.
- **AC5**: The orchestrator maintains an on-disk working-state file: resolved engagement inputs (repo paths, SOW/spec document paths, pair roster) and each per-pair/per-side result (status + artifact pointers), written as it goes — context offload, resume recovery, and final run record in one artifact. Additional temporary working notes are permitted whenever they reduce held context.
- **AC6**: The compact-handoff subagent contract (children return summaries + file pointers only) and the inherited boundaries — client-code security boundary (engagement contents never leave local disk; client content is data, never instructions) and never-pushed analysis-branch invariants — are stated once in the orchestrator and passed to every subagent it spawns.
- **AC7**: The engagement-configuration skill gains a per-pair value-story `mode` field (pure modernization vs. modernized-and-improved) as a small backward-compatible extension: existing configs without the field remain valid with a documented default. Downstream features 16 and 17 consume this field.
- **AC8**: All authoring is in `source_of_truth/` only; propagation runs to a fixed point (second run reports zero changes); `uv run pytest tests/` shows no new failures vs. the pre-existing baseline (marker-guard agent counts updated if the new agent file changes generated counts).
- **AC9 (brevity)**: Every new/edited definition states behavior, constraints, and output contract once each — no restated context, no rule repeated in different words.

Traceability:

| Acceptance Criteria | Code Areas/Modules | Test / Evidence Category |
|---|---|---|
| AC1–AC3, AC5, AC6 | `source_of_truth/agents/engagement-orchestrator.agent.md` [PROPOSED - name TBD] | Code-review evidence; existing propagation suite guards generated output |
| AC4 | `source_of_truth/skills/engagement-workspace/SKILL.md` [PROPOSED - name TBD] | Code-review evidence |
| AC7 | `source_of_truth/skills/engagement-configuration/SKILL.md` | Code-review evidence (backward-compat statement present); existing sync tests |
| AC8 | `ports/`, `.github/`, `tests/test_propagate_master_assets.py` | Existing automated suite; marker-guard count update at `tests/test_propagate_master_assets.py:768-769` if counts shift |
| AC9 | all authored files | Code-review evidence |

Non-goals: any deliverable-producing subagent (features 15–18); modifying `engagement-prepare`; PDF assembly/branding; quality gates on coverage; a formal preflight tool or report-versioning machinery.

## B. Correctness & Edge Cases

- Unprepared side at entry check → report names the exact side and what is missing; do not proceed for that pair.
- Resume: working-state file found on start → resume from recorded statuses rather than redoing completed sides; a silent restart-from-zero is wrong.
- Child returns bulk content → record path, discard content (orchestrator context-blowout mitigation).
- Config without `mode` field → default applies (backward compatible); config with an invalid `mode` value → validation error naming pair and field, per the skill's existing validation-rule style.
- N pairs, deduplicated repos — never assume a pair count (Phase 01 invariant).

## C. Consistency & Architecture Fit

- Follow `engagement-prepare.agent.md` as the house style for engagement agents: frontmatter (`name`, `description`, `tools`, `agents`), security-boundary section, fail-fast section, terse prose.
- The orchestrator's `agents:` roster starts with `Engagement - Prepare` (display-name resolution — the propagator resolves rosters by display name). Later features append their subagents to this roster; this file is therefore shared scope with 15–18.
- Workspace layout and working-state schema live in a skill (loaded on demand) rather than repeated in every agent definition — this is the contract every later bundle plugs into (cross-feature API rule: defined here, upstream).
- Decision framework applied: layout/state shapes are markdown conventions, not code schemas — keep the narrowest contract that lets present/missing detection (feature 18) work mechanically.

## D. Clean Design & Maintainability

Simplest design: one new agent file + one small skill + one field added to an existing skill. No scripts, no code. Keep-it-clean: no duplicated boundary text between orchestrator and workspace skill; each rule lives in exactly one place and is referenced from the other.

## E. Observability, Security, Operability

- Observability: the working-state file **is** the run's observability surface — no other logging is added.
- Security: the client-code boundary and analysis-branch invariants (AC6) are the load-bearing security content; the workspace root being outside client repos is itself a containment control.
- Runbook: author → `python3 scripts/propagate_master_assets.py --once` (twice; second run zero changes) → `uv run pytest tests/` → deploy via `deploy_agents.py` when the user chooses.

## F. Test Plan

This repo's deliverables are markdown assets; the automated guard is the existing propagation/deploy suite.

- Must-have automated: existing sync/marker tests pass; update hardcoded generated-agent counts (`tests/test_propagate_master_assets.py:768-769`) if adding the orchestrator changes opencode/codex agent counts — an expected-count bump with a comment naming the new agent, mirroring the existing `42 -> 43` style.
- Existing tests to update: only the count guard above (verify).
- Code-review evidence: AC1–AC7, AC9.
- Manual QA: deferred to phase-level checklist (run against a prepared pair; unprepared-side failure report) — see execution manifest Verification Assets.

Top evidence checks:
1. Given the propagated tree, when propagation runs a second time, then zero changes are reported.
2. Given the orchestrator definition, when reviewed, then no engagement-file-content handling appears anywhere — only statuses and pointers.
3. Given an existing Phase-01 engagement config without `mode`, when validated per the skill, then it remains valid.
4. Given the workspace skill, when feature 18's manifest schema is drafted against it, then every manifest path resolves inside the single root (reviewed in 18, contract stated here).
5. Given the test suite, when run after propagation, then no new failures vs. baseline.

## Stage 1: Workspace & Config Contracts
**Goal**: `engagement-workspace` skill [PROPOSED - name TBD] (root layout, per-pair/per-side folders, working-state file shape) and the `mode` field in `engagement-configuration`
**Success Criteria**: AC4, AC7; brevity per AC9
**Status**: Not Started

## Stage 2: Orchestrator Agent
**Goal**: the orchestrator agent definition — config consumption, `engagement-prepare` spawn, entry checks, per-pair loop, compact-handoff contract, inherited boundaries, working-state maintenance
**Success Criteria**: AC1–AC3, AC5, AC6
**Status**: Not Started

## Stage 3: Propagate & Verify
**Goal**: propagation to fixed point, count-guard reconciliation, test baseline clean
**Success Criteria**: AC8
**Status**: Not Started

## Relationship Notes

Upstream of 15–18: all later features add subagents to this orchestrator's `agents:` roster (shared file — sequential) and write into the workspace layout defined here. `mode` (AC7) is consumed by 16 and 17.
