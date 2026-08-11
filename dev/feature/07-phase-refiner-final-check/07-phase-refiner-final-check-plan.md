# Feature Plan: Phase Refiner Final-Check Integration

## Execution Metadata

- **Wave:** 3
- **Parallel safe:** yes
- **Depends on:** `05-phase-final-check-contract`, `06-phase-final-check-reviewer`
- **Key files modified:** `source_of_truth/agents/02-phase-refiner.agent.md`, `tests/[PROPOSED - name TBD: phase final-check contract guards]`
- **Sequential reason:** n/a

## A. Requirements & Traceability

### Acceptance Criteria

1. **AC1:** Phase - Refiner's `agents:` frontmatter declares the exact display name parsed from `source_of_truth/agents/02a-phase-final-check.agent.md` while preserving its existing Web Researcher and Docs Writer entries.
2. **AC2:** Both Entry A and Entry B converge on one shared workflow that writes the phase document before offering the final check.
3. **AC3:** The offer is optional and advisory. Accept, decline, and no answer all terminate the offer step, and decline/no-answer continue without changing the phase document.
4. **AC4:** On acceptance, Phase - Refiner spawns the hidden reviewer with exactly the phase document path and repository path. The spawn prompt contains no conversation content, session summary, settled-area briefing, or Refiner assessment.
5. **AC5:** Reviewer error, timeout, or unusable output is reported in one line; the Refiner does not retry or perform the review inline and proceeds with the unchanged document.
6. **AC6:** Usable findings are relayed verbatim without filtering or editorializing, then the user is asked which findings to apply.
7. **AC7:** The Refiner rewrites the phase document in place for accepted findings only, uses no change-log framing, and proceeds unchanged if none are accepted.
8. **AC8:** Roadmap synchronization and phase-scoped discovery-context writing occur exactly once, after the offer/fold-in path is complete and before the branch step.
9. **AC9:** The existing branch creation/resume and `eval: phase-affirmed` commit behavior remains after synchronization.
10. **AC10:** Focused structural guards prove the new agent exists and parses, is a hidden leaf, inherits `read-only-agent.instructions.md`, is declared by the Refiner, and shares the finalized skill reference with the Refiner.
11. **AC11:** Focused guards cover the Refiner ordering and blindness spawn boundary without pinning one exact prose rendering, include non-vacuity checks, and are demonstrated red by deleting or semantically negating each protected obligation before restoration.
12. **AC12:** Existing corpus invariants and propagation unit tests gain no new failures; generated sync failures after source authoring are reported as maintainer propagation pending.
13. **AC13:** A manual smoke test exercises both Refiner entry paths and confirms the final-check reviewer can return useful findings or zero findings while creating no artifact.

### Non-Goals

- Do not wire the offer into Project - Planner.
- Do not add a gate, severity threshold, rubric, pass/fail verdict, automatic application, or revise-and-recheck loop.
- Do not persist findings.
- Do not rewrite unrelated Refiner phases; treat the change as a Phase 6 split and one insertion.
- Do not edit `ports/` or `.github/`, and do not run propagation.
- Do not remediate the 12 pre-existing baseline test failures.

### Traceability

| Acceptance Criteria | Code Areas/Modules | Test / Evidence Category |
|---|---|---|
| AC1–AC9 | `source_of_truth/agents/02-phase-refiner.agent.md` | Must-have automated test |
| AC10–AC12 | `tests/[PROPOSED - name TBD: phase final-check contract guards]`, existing corpus and propagation suites | Must-have automated test; existing test to update: no existing-file update expected |
| AC13 | Real Phase - Refiner sessions through Entry A and Entry B | Manual QA check |

## B. Correctness & Edge Cases

- User silence must not strand the workflow at the offer or fold-in prompt. No answer to the offer is a decline; no accepted finding leaves the document unchanged.
- Reviewer failure and malformed output are terminal for the review attempt and never trigger inline substitution or retry.
- The phase document must exist on disk before spawn so the reviewer reads a concrete artifact.
- Sync must happen after accepted edits so the roadmap and discovery context reflect final content, but exactly once to prevent competing versions.
- Entry B must not bypass the offer simply because its document was drafted in the same session.
- Verbatim relay preserves the reviewer's words; the Refiner may identify the reviewer failure state but must not rank, paraphrase, or pre-filter usable findings.
- Branch and commit steps remain after all document writes.

## C. Consistency & Architecture Fit

- Preserve the verified current phases: Phase 5 presents, current Phase 6 writes document/discovery/roadmap, and Phase 7 opens the branch. Split and reorder only the current Phase 6 responsibilities.
- Use the exact reviewer display name discovered from the new agent frontmatter; roster entries are display names and existing corpus tests derive validity from disk.
- Use the shared skill from `05-phase-final-check-contract` for the offer/spawn obligations; do not implement a second review rubric in the Refiner.
- Cross-feature API: Phase - Refiner calls the existing harness `agent` delegation mechanism with the reviewer produced by `06-phase-final-check-reviewer`. The only payload contract is the two paths fixed by Phase 02; no new code API is introduced.
- Integration feature rule: this final feature connects the skill and reviewer to the live Refiner entry paths and owns the combined smoke test.
- The focused test module should derive agent names and frontmatter through `scripts/propagate_master_assets.py` where practical, following `tests/test_agent_corpus_invariants.py`.

### Unverified Assumptions

- The focused test filename is not specified. Use `[PROPOSED - name TBD: phase final-check contract guards]` until implementation selects the repository-consistent name.
- The harness's literal spawn syntax varies after propagation. Source tests should validate the harness-neutral source contract, not generated-port wording.

## D. Clean Design & Maintainability

- Keep one converged offer path for both entries.
- Express each continuation branch explicitly: accept, decline, silence, failure, findings accepted, findings rejected.
- Reuse existing document-write, discovery-sync, roadmap-sync, and branch text with minimal movement.
- Keep focused guards in one new Phase 02 module instead of adding prose-content assertions to the generic corpus invariant suite.

### Keep It Clean Checklist

- [ ] One offer path, not one per entry.
- [ ] One reviewer attempt, no inline fallback.
- [ ] One roadmap/discovery sync pass.
- [ ] Existing branch semantics preserved.
- [ ] Content guards proven red and non-vacuous.
- [ ] No generated-output edits.

## E. Completeness: Observability, Security, Operability

- **Observability decision:** Add no persistent logs. Show the offer, reviewer result, one-line failure state, and fold-in choice in chat; create no findings artifact.
- **Security:** Spawn only the two repository-local paths. Do not transmit conversation history or external data to the reviewer.
- **Runbook:** Run the focused Phase 02 module, generic corpus invariants, and propagation unit tests without invoking propagation. Then smoke-test Entry A and Entry B. Roll back the Refiner edit, agent roster entry, focused test, reviewer, and skill as one dependency chain.
- **Baseline:** `uv run pytest tests/` collected 242 tests on 2026-08-11: 230 passed and 12 pre-existing failures. Expected existing failures are one PR Review name collision, one wildcard `applyTo` enumeration failure, and ten Unity reference-asset failures. Additional failures are Phase 02 regressions unless explained; source/generated sync failures after implementation mean propagation is pending.

## F. Test Plan

| Acceptance Criteria | Evidence | Category |
|---|---|---|
| AC1, AC10 | Derive roster, agent metadata, and instruction applicability through the propagator loader; verify exact set membership, hidden state, empty leaf roster, read-only inheritance, and shared skill references | Must-have automated test |
| AC2–AC9 | Parse scoped Refiner workflow sections and verify order/branch relationships with whitespace normalization and non-vacuity checks | Must-have automated test |
| AC11 | Delete or semantically negate every protected mechanism, confirm the focused test fails for the intended obligation, restore, and confirm green | Must-have automated test |
| AC12 | Run focused, corpus, propagation, then full repository tests against the recorded baseline | Existing test to update: no update expected; run as regression evidence |
| AC13 | Exercise Entry A and Entry B in real Refiner sessions | Manual QA check |

### Top Five High-Value Checks

1. Given either Refiner entry path, when refinement is affirmed, then document write precedes one shared offer, and sync plus branch follow the completed offer/fold-in path.
2. Given decline, silence, reviewer failure, or zero accepted findings, when the workflow continues, then the phase document is unchanged and sync/branch still execute.
3. Given reviewer acceptance, when the spawn instruction is inspected, then only phase document path and repository path are passed; adding a summary or Refiner assessment makes the guard fail.
4. Given usable findings, when they return, then the Refiner relays them verbatim and only accepted items are folded into a clean rewrite.
5. Given the new corpus topology, when loaded through the propagator, then the Refiner roster resolves to the hidden leaf and both consumers reference the same skill.

### Fixtures and Test Impact

- Create `tests/[PROPOSED - name TBD: phase final-check contract guards]` for Phase 02-specific source-contract checks and mutation helpers.
- Do not add phrase-pinning tests to `tests/test_agent_corpus_invariants.py`; run its roster, frontmatter, and duplicate-block tests unchanged.
- Run `tests/test_propagate_master_assets.py` unchanged to catch source parsing and rendering regressions. Sync assertions may remain red until maintainer propagation.
- Manual QA uses existing phase documents; it must not persist reviewer findings.
- No phase-scoped test directory pattern exists in this Python repository. One focused Phase 02 test module is the appropriate consolidated verification asset.

## Stage 1: Failing Integration Guards
**Goal**: Add scoped, non-vacuous tests for corpus topology, shared-skill references, workflow ordering, continuation branches, and blindness.
**Success Criteria**: AC1–AC12 have automated evidence, and deletion/negation mutations turn each new guard red for the intended reason.
**Status**: Not Started

## Stage 2: Refiner Workflow Integration
**Goal**: Split the existing write/sync phase, insert the optional final check, and preserve both entry paths and branch behavior.
**Success Criteria**: AC1–AC9 pass with one converged offer path and no duplicated review logic.
**Status**: Not Started

## Stage 3: Regression and Smoke Verification
**Goal**: Verify the combined skill, reviewer, and Refiner flow through automated suites and both real entry paths.
**Success Criteria**: AC10–AC13 are evidenced, no new baseline failures appear, and generated synchronization is reported as pending rather than performed.
**Status**: Not Started
