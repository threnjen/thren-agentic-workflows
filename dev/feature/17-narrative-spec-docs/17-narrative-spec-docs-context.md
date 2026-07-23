# Context: 17-narrative-spec-docs

## Key Files

### Files Being Changed

| File | Role | Change Type |
|------|------|-------------|
| `source_of_truth/agents/engagement-narrative-writer.agent.md` [PROPOSED - name TBD] | New hidden subagent (`user-invocable: false`, deploys with `z-` prefix) producing the three per-pair narrative documents | Create |
| `source_of_truth/agents/engagement-orchestrator.agent.md` [PROPOSED - name TBD] | Add narrative writer to `agents:` roster and the per-pair loop step (file created by feature 14) | Modify |
| `tests/test_propagate_master_assets.py` | Marker-guard counts (roots table ~lines 765–779) — verify; bump if agent counts shift | Verify/Modify |

### Read-Only Reference Files

| File | Role |
|------|------|
| `docs/phases/PHASE_02/PHASE_02_SUMMARY.md` | Phase document — Key Deliverable 6, bundle 4 |
| `source_of_truth/skills/engagement-configuration/SKILL.md` | Source of the per-pair value-story `mode` field (added by 14 AC7) |
| `source_of_truth/skills/engagement-workspace/SKILL.md` [PROPOSED - name TBD, created by 14] | Workspace layout the documents write into |
| Sibling agents (e.g., `source_of_truth/agents/docs-writer.md`, 16's delta synthesizer) | Grant patterns and value-story-mode framing precedent |
| `source_of_truth/agents/README.md` | Agent catalog (catalog entry may defer to 18 per 14's plan) |

## Discovery Delta

| Finding | Impact | Action |
|---------|--------|--------|
| No contradictions found | Plan's structure holds against the tree | none |
| `engagement-orchestrator.agent.md` and `engagement-workspace` skill do not exist yet — they are feature 14 outputs; `mode` is not yet in `engagement-configuration/SKILL.md` | Expected: 17 is wave 4, sequenced after 14. Implementer must verify 14 landed (file exists, `mode` defined) before starting | Add task |
| Count guards live at `tests/test_propagate_master_assets.py:765-779` (plan cited 768-769): claude/agents=28, claude/commands=19, opencode/agents=43, codex/agents=43, codex/profiles=0 | A new hidden subagent bumps opencode/agents and codex/agents by 1 each; claude/commands unchanged (not user-invocable); claude/agents +1. Recount from disk per the test's own comment — do not increment from memory. Note: 14/15/16 also add agents, so absolute counts at 17's turn depend on prior waves | Add task |
| Learning: the propagator resolves `agents:` roster references by **backticked display name**, not slug; slug references silently no-op | Roster entry and loop-step references must use the display name | Constraint below |
| Learning: propagation is not idempotent across reclassification — run until change counters are zero; second run must report zero changes | Matches plan's evidence check 4 | none |
| 16's delta synthesizer states value-story-mode framing rules (per 16's plan); plan already flags the duplication risk | Implementer states the mode rule once in a shared place (config skill's `mode` definition preferred) and references it from both agents; record the choice | Task exists |

## Architectural Decisions

- **One agent, three document contracts** — a single narrative-writer definition covers business design doc, intended-behavior spec, and before/after workflow narratives. Split only if the definition cannot stay terse; record the decision in implementation notes.
- **Evidence base is report/docs-vs-docs, never git-diff**: analysis-branch docs-writer set, graphs, and 15's retained reports.
- **Grants**: read/search/edit-class only, mirroring the other synthesis agents; no shell, no web.
- **AC2 spec is a downstream contract**: feature 18's verification summary points its functional-preservation statement at the intended-behavior spec — its final filename/location must be fixed and recorded for 18's manifest schema.
- **Mode rule stated once**: reference the engagement-config skill's `mode` definition rather than restating framing rules already in 16.

## Constraints

- `source_of_truth/` only; never hand-edit `ports/` or `.github/`. Propagate to fixed point (second run reports zero changes).
- Brevity constraint (AC6): behavior, constraints, output contract stated once each; shared rules referenced, not restated. A rule appearing twice fails review.
- Roster/sibling references by backticked display name (propagator keys the reference map on display name).
- Inherited client-code boundary passes through; documents describe behavior in business terms without reproducing engagement source content.
- Client-facing docs lead with business meaning; technical evidence goes in appendices.
- Output filenames within the workspace layout are `[PROPOSED - names TBD]` — implementer fixes and records them.

## Scope Boundaries

- Do not modify `docs-writer` (explicit non-goal).
- No user-facing usage documentation (screens/workflows) — project non-goal.
- No operational/publishing docs (Phase 03); no delta/security synthesis (owned by 16).
- Do not alter the orchestrator's entry check, workspace layout, or `mode` field definition — consume them as 14 defined them.
- Environmental assumptions that cannot be verified are stated as assumptions with what was observed, never asserted as verified facts.
- A pair with no identifiable functional changes yields an honest statement, not fabricated deltas.

## Relationships to Sibling Plans

- **Depends on 14 (engagement-orchestrator-core)**: workspace layout, compact-handoff contract, engagement-config `mode` field (14 AC7), orchestrator entry check.
- **Sequenced after 15/16** via the shared orchestrator file (wave ordering), though runtime-independent of their outputs except optional citation of 15's retained reports.
- **Upstream of 18**: the intended-behavior spec is the target of 18's functional-preservation statement; the three document names feed 18's manifest schema. Record final names in the implementation record.

## Suggested Implementation Order

Stage 1 (narrative-writer agent definition) → Stage 2 (orchestrator roster/loop wiring, propagate to fixed point, verify test baseline). Must run after 14/15/16 have landed on the branch.

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Python 3 (stdlib-only scripts) + Markdown agent/skill definitions; pytest via uv |
| Test Runner | `uv run pytest tests/` |
| Test Baseline | 233 passed, 113 subtests passed — captured 2026-07-22 |
| Lint | Not configured |
| Format | Not configured |

## Relevant Learnings

- **Propagation Contracts** (`cross-phase-decisions.md`): generated Markdown roots carry markers; propagation is not idempotent — run until every change counter is zero (`test_committed_tree_is_at_a_propagation_fixed_point` pins this); restart any `--watch` propagator after propagator changes.
- **Reference-map keying** (`debugging-learnings.md`): sibling/roster references must use backticked display names; slug references survive propagation unrewritten and silently break delegation.
- **Enumeration/guards** (`cross-phase-decisions.md`): recount marker-guard expectations from disk (`ls ports/<harness>/agents`), never increment from memory.
- **Codex `max_depth`** (`cross-phase-decisions.md`): "agent X demonstrably delegates to Y" is unverifiable by static test — delegation ACs route to runtime evidence, not new guards.
