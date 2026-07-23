# Implementation Record: 17-narrative-spec-docs

## Summary

Created the hidden `Engagement - Narrative Writer` subagent (one agent, three per-pair document contracts — no split needed; the definition stays terse), wired it into the orchestrator's roster and per-pair loop as a "Narrative & Specification Documents" stage, propagated to fixed point, and updated count guards and doc count claims.

**Final document names (contract for feature 18's manifest schema):**
- Business design document: `deliverables/<pair-name>/business-design.md` (AC1)
- Intended-behavior specification: `deliverables/<pair-name>/intended-behavior-spec.md` (AC2 — the path 18's functional-preservation statement references)
- Before/after workflow narratives: `deliverables/<pair-name>/workflow-narratives.md` (AC3)

**Mode-rule placement decision:** the value-story `mode` semantics live in the `engagement-configuration` skill (14 AC7); the narrative writer references that definition and states only its own framing behavior (per-mode narration rules for its documents), mirroring 16's precedent — the rule is not restated.

## Sibling Features

- 14 (orchestrator core): consumed — workspace layout skill, compact-handoff contract, `mode` field, entry check. Verified present before starting.
- 15/16: shared file `engagement-orchestrator.agent.md` — appended a new stage after their Delta & Security Synthesis and Cloud/Cost stages; no edits to their content.
- 18 (compliance package/manifest): downstream — consumes the three document names above, especially `intended-behavior-spec.md`.

## AC Coverage Matrix

| AC | Criterion ID | Planned Test ID | Planned Test Pattern | Status | Implementing Files | Evidence Paths | Implement Commit SHA | Review Commit SHA |
|----|--------------|-----------------|----------------------|--------|--------------------|----------------|----------------------|-------------------|
| AC1 | AC1 | code-review | Business design contract; docs/graph evidence; no source reproduction | Done | `source_of_truth/agents/engagement-narrative-writer.agent.md` | same file, "Business Design Document" section | PENDING | PENDING |
| AC2 | AC2 | code-review | Mandatory observable-behavior + environmental-assumptions sections; fixed filename | Done | `source_of_truth/agents/engagement-narrative-writer.agent.md` | same file, "Intended-Behavior Specification" section | PENDING | PENDING |
| AC3 | AC3 | code-review | As-was/as-is walkthroughs; both modes; honest no-delta statement | Done | `source_of_truth/agents/engagement-narrative-writer.agent.md` | same file, "Before/After Workflow Narratives" section | PENDING | PENDING |
| AC4 | AC4 | code-review | Roster + loop stage under compact handoff; backticked display name | Done | `source_of_truth/agents/engagement-orchestrator.agent.md` | frontmatter `agents:` roster; "Stage: Narrative & Specification Documents"; resolved reference visible in `ports/claude/commands/engagement-orchestrator.md` | PENDING | PENDING |
| AC5 | AC5 | test_marker_guard_matches_every_real_generated_file; test_retirement_reconciliation count tests | Guard counts recounted from disk; fixed point | Done | `tests/test_propagate_master_assets.py`, `README.md`, `docs/CODEBASE_CONTEXT.md` | `tests/test_propagate_master_assets.py` roots table (35→36, 49→50 ×2) | PENDING | PENDING |
| AC6 | AC6 | code-review | Behavior/constraints/output contract stated once; shared rules referenced | Done | `source_of_truth/agents/engagement-narrative-writer.agent.md` | whole file (~60 lines) | PENDING | PENDING |

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | Business design document contract | Done | narrative-writer agent | Business terms; docs-writer set + graph evidence; no source reproduction |
| AC2 | Intended-behavior spec, mandatory env-assumptions | Done | narrative-writer agent | Filename fixed: `intended-behavior-spec.md`; unverified items stated as assumptions |
| AC3 | Before/after workflow narratives, mode-aware | Done | narrative-writer agent | Modernization mode excludes intentional-change framing; honest no-delta statement |
| AC4 | Orchestrator wiring, compact handoff | Done | orchestrator agent | Backticked display name; reference resolved to `z-engagement-narrative-writer` in ports |
| AC5 | source_of_truth only; fixed point; clean tests | Done | test guards + doc counts | Second propagation run reports zero changes |
| AC6 | Brevity | Done | narrative-writer agent | Single agent covers all three contracts; mode rule referenced, not restated |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `source_of_truth/agents/engagement-narrative-writer.agent.md` | Create | Hidden subagent, `tools: [read, search, edit]`, three document contracts | AC1–AC3, AC6 |
| `source_of_truth/agents/engagement-orchestrator.agent.md` | Modify | Roster entry + "Stage: Narrative & Specification Documents" in per-pair loop | AC4 |
| `README.md` | Modify | Source-agent count 49 → 50 | AC5 (count-claim guards) |
| `docs/CODEBASE_CONTEXT.md` | Modify | Counts 49→50, 47→48 `*.agent.md`, hidden 29→30 | AC5 (count-claim guards) |
| `ports/`, `.github/` | Generated | Regenerated by propagation to fixed point | AC5 |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| `tests/test_propagate_master_assets.py` | Modify | Roots table: claude/agents 35→36, opencode/agents 49→50, codex/agents 49→50; comment recording recount from disk | AC5 |

## Test Results
- **Baseline**: 233 passed, 113 subtests passed (before implementation)
- **Final**: 233 passed, 113 subtests passed (after implementation)
- **New tests added**: 0 (existing guards exercised; Red observed — 6 failures pre-count-update — then Green)
- **Regressions**: None

## Deviations from Plan

- None substantive. Plan left agent name and document filenames as `[PROPOSED - TBD]`; fixed as `engagement-narrative-writer.agent.md` (display name `Engagement - Narrative Writer`) and the three filenames above.

## Gaps

- Agent catalog entry in `source_of_truth/agents/README.md` deferred to feature 18 per 14's plan (consistent with 15/16, which also did not add catalog entries).
- Runtime delegation behavior (orchestrator actually spawning the writer) is unverifiable by static test per learnings — routes to phase-level manual QA.

## Reviewer Focus Areas

- Environmental-assumptions section of the narrative writer — verify it satisfies AC2's "software broke vs. environment changed" distinction.
- Mode framing — confirm `modernization` mode cannot produce intentional-change language and no rule duplicates 16's delta synthesizer or the config skill.
- Orchestrator stage placement (after Cloud/Cost) and the pass-through of `mode`, docs/graph pointers, and boundaries.
- Count updates: guards 36/20/50/50/0 and README/CODEBASE_CONTEXT claims match disk.
