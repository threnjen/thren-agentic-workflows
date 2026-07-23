# Plan: 17-narrative-spec-docs

## Execution Metadata

- **Wave:** 4
- **Parallel safe:** no
- **Depends on:** 14-engagement-orchestrator-core
- **Key files modified:** `source_of_truth/agents/engagement-narrative-writer.agent.md` [PROPOSED - name TBD], `source_of_truth/agents/engagement-orchestrator.agent.md` [PROPOSED - name TBD] (roster + loop step), `tests/test_propagate_master_assets.py` (verify — marker-guard counts)
- **Sequential reason:** shares the orchestrator agent file with upstream 14 (and with 15/16 which also edit it in earlier waves)

Phase document: `docs/phases/PHASE_02/PHASE_02_SUMMARY.md` (Key Deliverable 6, bundle 4).

Agent-count note: one narrative-writer agent producing three per-pair documents is the proposed simplest shape; the implementer may split if one definition cannot stay terse while covering all three contracts — record the decision.

## A. Requirements & Traceability

Acceptance criteria:

- **AC1 (business design document)**: Per pair, a client-facing document describing what the system is and does, in business terms, derived from the analysis-branch docs-writer set and graphs — no engagement source content reproduced.
- **AC2 (intended-behavior specification)**: Per pair, a client-facing specification of how the system is supposed to work — the warranty baseline and future dispute-resolution reference. It states observable behavior **and** the environmental assumptions that behavior depends on (runtime versions, services, configuration), so later misbehavior can be distinguished as "the software broke" vs. "the environment changed underneath warranted behavior." Feature 18's verification summary points its functional-preservation statement here — this document's identity/location is a contract 18 consumes.
- **AC3 (before/after workflow narratives)**: For components with functional changes, each workflow is walked as-was and as-is. Both value-story modes supported: pure-modernization pairs get "modernized, nothing changed" framing; improved pairs get intentional-change narratives. `mode` comes from the engagement config (14's AC7).
- **AC4**: Wired into the orchestrator loop under the compact-handoff contract, writing into the workspace layout; inherited boundaries pass through; client-facing docs lead with business meaning, technical evidence in appendices.
- **AC5**: `source_of_truth/` only; propagation to fixed point; no new test failures (count guards updated if agent counts shift).
- **AC6 (brevity)**: each definition states behavior, constraints, output contract once; shared rules referenced, not restated.

Traceability:

| Acceptance Criteria | Code Areas/Modules | Test / Evidence Category |
|---|---|---|
| AC1–AC3 | narrative-writer agent [PROPOSED - name TBD] | Code-review evidence (three document contracts; environmental-assumptions requirement; both modes) |
| AC4 | narrative-writer + orchestrator file | Code-review evidence |
| AC5 | `ports/`, `.github/`, `tests/test_propagate_master_assets.py:768-769` | Existing automated suite; count bump if needed |
| AC6 | authored files | Code-review evidence |

Non-goals: user-facing usage documentation (screens/workflows — project non-goal); operational/publishing docs (Phase 03); delta/security synthesis (16); any modification to docs-writer.

## B. Correctness & Edge Cases

- Pure-modernization pair → workflow narratives still exist where workflows are visible, framed "modernized, nothing changed"; a pair with no identifiable functional changes yields an honest statement, not fabricated deltas.
- Missing docs-writer set on a side (unprepared) → caught by the orchestrator's entry check (14); the narrative writer must state its evidence sources, not silently write from nothing.
- Environmental assumptions unknown/unverifiable → stated as assumptions with what was observed, never asserted as verified facts.

## C. Consistency & Architecture Fit

- Evidence base: analysis-branch docs (docs-writer set), graphs, and 15's retained reports where relevant — report/docs-vs-docs, never git-diff.
- Grants: read/search/edit-class only, mirroring the other synthesis agents; no shell, no web.
- Output filenames within the workspace layout are `[PROPOSED - names TBD]`; implementer fixes and records them for 18's manifest schema, and the intended-behavior spec's name is the one 18 references (AC2 contract).

## D. Clean Design & Maintainability

One agent, three document contracts, each stated once. Duplication risk: value-story-mode framing rules already exist in 16's delta synthesizer — state the mode rule in one shared place (the workspace or conventions skill, or by reference to the config skill's `mode` definition) rather than twice; implementer documents the choice.

## E. Observability, Security, Operability

- Observability: outputs cited in working state; no new logging.
- Security: inherited client-code boundary; documents describe behavior in business terms without reproducing engagement source.
- Runbook: propagate → test → deploy on request.

## F. Test Plan

- Must-have automated: existing propagation/sync suite; count-guard bump (verify).
- Code-review evidence: AC1–AC4, AC6 — especially the environmental-assumptions requirement and both-modes support.
- Manual QA: phase-level — verify narrative output for both value-story modes (see execution manifest).

Top evidence checks:
1. Given the intended-behavior spec contract, when reviewed, then observable behavior and environmental assumptions are both mandatory sections.
2. Given a pure-modernization `mode`, when the instructions are walked, then no intentional-change framing can appear.
3. Given the agent definition, when reviewed, then evidence sources are named (docs set, graphs, retained reports) and engagement-source reproduction is excluded.
4. Given propagation, second run reports zero changes.
5. Given the definition, when reviewed for brevity, then no rule appears twice.

## Stage 1: Narrative Writer Agent
**Goal**: agent definition covering the three per-pair document contracts, mode-aware
**Success Criteria**: AC1, AC2, AC3, AC6
**Status**: Not Started

## Stage 2: Orchestrator Wiring, Propagate & Verify
**Goal**: roster/loop integration; fixed point; clean baseline
**Success Criteria**: AC4, AC5
**Status**: Not Started

## Relationship Notes

Consumes 14 (workspace, contract, `mode`). Runtime-independent of 15/16 outputs except optional report citation, but file-sequenced after them via the shared orchestrator file. Upstream of 18: the intended-behavior spec is the target of the verification summary's functional-preservation statement; document names feed the manifest schema.
