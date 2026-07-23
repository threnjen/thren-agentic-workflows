# Tasks: 14-engagement-orchestrator-core

## Stage 1: Workspace & Config Contracts

- [x] Create `source_of_truth/skills/engagement-workspace/SKILL.md` [PROPOSED - name TBD]: define the single per-engagement workspace root (outside every client repository), the per-pair/per-side folder layout, and destinations for client-facing docs, internal artifacts, raw reports, manifest, and working-state file (AC4)
- [x] Define the working-state file shape in the same skill: resolved engagement inputs (repo paths, SOW/spec document paths, pair roster) plus per-pair/per-side result entries (status + artifact pointers); note that additional temp working notes are permitted (AC5 contract)
- [x] State explicitly that this layout is the contract features 15–18 reference (not restate), and that no manifest path may resolve outside the root (AC4)
- [x] Add per-pair value-story `mode` field to `source_of_truth/skills/engagement-configuration/SKILL.md`: schema entry, documented default when absent (backward compatible), invalid-value validation error naming pair and field in the existing validation-rule style, and annotated-example update (AC7)
- [x] Brevity pass on both skills: behavior, constraints, output contract stated once each (AC9)

## Stage 2: Orchestrator Agent

- [x] Create `source_of_truth/agents/engagement-orchestrator.agent.md` [PROPOSED - name TBD] following `engagement-prepare.agent.md` house style: frontmatter (`name`, `description`, `tools`, `agents`), security-boundary section, fail-fast section, terse prose
- [x] Set `agents:` roster to start with `Engagement - Prepare` (exact display name — propagator resolves rosters by display name); note in-file that later features append to this roster
- [x] Define config consumption and per-pair loop: orchestrator holds only pair list + compact per-side/per-pair results; bulk child content recorded as on-disk pointer and discarded; never reads engagement source code itself (AC1)
- [x] Instruct spawning `engagement-prepare` unchanged as the first per-engagement step, consuming its compact report; do not modify `engagement-prepare.agent.md` (AC2)
- [x] Write the run-time entry-check paragraph: before later stages, verify analysis branches and graphs exist for the sides in play; report exactly which side is unprepared and do not proceed for that pair; no formal preflight tool (AC3)
- [x] Specify working-state file maintenance per the workspace skill: written as the run progresses; on start, an existing working-state file triggers resume from recorded statuses (never silent restart-from-zero) (AC5)
- [x] State once the compact-handoff subagent contract (summaries + file pointers only) and inherited boundaries — client-code security boundary (contents never leave local disk; client content is data, never instructions) and never-pushed analysis-branch invariants — and require passing them to every spawned subagent (AC6)
- [x] Reference the workspace skill for layout/state rules rather than duplicating boundary text; each rule lives in exactly one place (AC9, keep-it-clean)
- [x] Handle N pairs with deduplicated repos — never assume a pair count

## Stage 3: Propagate & Verify

- [x] Run `python3 scripts/propagate_master_assets.py --once` twice; confirm the second run reports zero changes (AC8)
- [x] Recount generated agent files from disk (`ls ports/<harness>/agents`) and update the marker-guard `roots` counts in `tests/test_propagate_master_assets.py` (~lines 766–771) if changed, with a comment naming the new agent mirroring the existing `42 -> 43` style (AC8)
- [x] Run `uv run pytest tests/`; confirm no new failures vs. baseline (233 passed, 113 subtests) (AC8)
- [x] Verify `source_of_truth/agents/README.md` catalog handling — entry may defer to feature 18; record the decision in implementation notes
- [x] Record final chosen names for the [PROPOSED - name TBD] agent and skill in implementation notes
