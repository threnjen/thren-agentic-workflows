# Feature Plan: Phase Final-Check Reviewer

## Execution Metadata

- **Wave:** 2
- **Parallel safe:** yes
- **Depends on:** `05-phase-final-check-contract`
- **Key files modified:** `source_of_truth/agents/02a-phase-final-check.agent.md`, `source_of_truth/instructions/read-only-agent.instructions.md`
- **Sequential reason:** n/a

## A. Requirements & Traceability

### Acceptance Criteria

1. **AC1:** `source_of_truth/agents/02a-phase-final-check.agent.md` exists with valid hidden-agent frontmatter, the exact Phase-specified path, and `user-invocable: false`.
2. **AC2:** The agent is a leaf: it declares no `agents:` roster, spawns nothing, and exposes only the minimum tools needed to read and search.
3. **AC3:** The agent is stricter than the standard read-only pattern: it writes no repository file and returns all findings only in its response.
4. **AC4:** The agent consumes the finalized skill from `05-phase-final-check-contract` by reference and does not duplicate the contract body.
5. **AC5:** Given only a phase document path and repository path, the agent reads the allowed committed context and evaluates the document without requesting or inferring conversation history.
6. **AC6:** Its return follows the skill contract: at most five concrete findings, verbatim-ready for relay, no severity or verdict, explicit truncation when applicable, and a plain zero-findings result.
7. **AC7:** It never edits the phase document, roadmap, discovery context, or learning files and never creates a findings artifact.
8. **AC8:** `source_of_truth/instructions/read-only-agent.instructions.md` explicitly includes `**/02a-phase-final-check.agent.md` in its enumerated `applyTo` list, so the reviewer actually inherits the standard read-only constraint before applying its stricter no-file-write rule.

### Non-Goals

- Do not modify Phase - Refiner, its frontmatter roster, or its workflow.
- Do not redefine or inline the shared review contract.
- Do not add user approval, fold-in behavior, retry behavior, or failure recovery; those belong to the Refiner integration.
- Do not run propagation or edit generated surfaces.

### Traceability

| Acceptance Criteria | Code Areas/Modules | Test / Evidence Category |
|---|---|---|
| AC1–AC4 | `source_of_truth/agents/02a-phase-final-check.agent.md` | Must-have automated test in downstream `07-phase-refiner-final-check` |
| AC5–AC7 | New agent body plus contract skill from `05-phase-final-check-contract` | Must-have automated test; manual QA check for real finding quality |
| AC8 | `source_of_truth/instructions/read-only-agent.instructions.md` | Must-have automated test in downstream `07-phase-refiner-final-check` |

## B. Correctness & Edge Cases

- A missing optional project discovery or cross-phase decision file is not an error.
- A missing or unreadable supplied phase document is reported to the caller; the agent does not search for a substitute phase.
- Findings about unsynchronized roadmap or phase discovery files are excluded even if visible.
- If more than five issues qualify, select the five most concrete and disclose omission without assigning severity.
- If nothing qualifies, return the explicit no-findings state rather than inventing advice.
- The agent does not compensate for bad spawn input by accepting a session summary; the caller must satisfy the blindness contract.

## C. Consistency & Architecture Fit

- Follow the verified hidden-leaf frontmatter shape in `source_of_truth/agents/05c-artifact-sweeper.agent.md`, while narrowing tools because this reviewer writes nothing.
- Update the verified enumerated `applyTo` list in `source_of_truth/instructions/read-only-agent.instructions.md`; without this companion edit, the Phase document's direct-inheritance requirement is false.
- Preserve the exact phase-specified filename `02a-phase-final-check.agent.md`; the `02a` prefix is the pipeline position under Phase - Refiner, not a project phase number.
- Use the final skill slug selected by `05-phase-final-check-contract` and keep the agent body to role, input, workflow, and return contract.
- Relationship: this feature depends on the contract skill at runtime. `07-phase-refiner-final-check` depends on this feature's display name for the roster and spawn call.
- No duplicated review implementation is permitted in the agent body.

### Unverified Assumptions

- The display name is not fixed verbatim by the Phase document. The implementer must select a name consistent with nearby numbered agents and use the exact parsed name in the Refiner roster.
- The minimum tool list must be verified against the propagator's valid tool keys and nearby read/search-only agents.

## D. Clean Design & Maintainability

- Keep the leaf stateless and response-only.
- Give it one input contract and one output contract.
- Point to the shared skill instead of paraphrasing it.
- Avoid general phase-refinement advice that would blur the reviewer/refiner boundary.

### Keep It Clean Checklist

- [ ] No `agents:` roster.
- [ ] No edit or execute capability unless codebase verification proves it unavoidable.
- [ ] No file output path.
- [ ] No copied contract block.
- [ ] Read-only instruction applicability verified through the propagator.
- [ ] No generated-output edits.

## E. Completeness: Observability, Security, Operability

- **Observability decision:** Add no logs. The structured response is sufficient, and no normal-path artifact survives the session.
- **Security:** Read only the supplied repository. Do not access external systems or ask for conversation transcripts.
- **Runbook:** Run focused Phase 02 guards and existing corpus invariants. Smoke-test through the Refiner integration in Feature 07. Roll back the agent together with its roster and spawn references.
- **Baseline:** `uv run pytest tests/` collected 242 tests on 2026-08-11: 230 passed and 12 unrelated pre-existing failures. Feature verification must introduce no additional failures.

## F. Test Plan

| Acceptance Criteria | Evidence | Category |
|---|---|---|
| AC1–AC4, AC8 | Parse frontmatter with the propagator loader and verify hidden leaf, no roster, narrow tools, exact shared-skill reference, and read-only instruction applicability | Must-have automated test |
| AC5–AC7 | Inspect the scoped workflow/return sections and mutation-test the no-write and response-only obligations | Must-have automated test |
| AC6 | Invoke through Phase - Refiner against an existing phase document | Manual QA check |

### Top Five High-Value Checks

1. Given the new file, when loaded through the propagator, then its name and description parse, `user-invocable` is false, and its child roster is empty.
2. Given the new agent path, when instruction applicability is derived through the propagator, then the existing read-only instruction applies to it.
3. Given a mutation that adds a file-writing instruction or child roster, when the focused guard runs, then it fails for the leaf/no-write obligation.
4. Given the agent body, when shared-contract usage is inspected, then it references the final skill and does not contain a duplicated contract-sized block.
5. Given no qualifying gap or more than five qualifying gaps, when invoked cold, then it returns the correct bounded response and writes nothing.

### Fixtures and Test Impact

- `07-phase-refiner-final-check` owns the new focused test module and mutation evidence.
- Existing `RosterTests`, `FrontmatterShapeTests`, and `DuplicateBlockTests` in `tests/test_agent_corpus_invariants.py` provide regression evidence without modification.
- No Stage 0 is required; existing corpus parsing and roster coverage is substantial.

## Stage 1: Hidden Leaf Definition
**Goal**: Add the response-only final-check reviewer with valid hidden-agent frontmatter.
**Success Criteria**: AC1–AC5, AC7, and AC8 hold, and the agent consumes the shared skill without duplication.
**Status**: Not Started

## Stage 2: Return Contract Verification
**Goal**: Verify the leaf's response shape and strict no-write boundary before Refiner integration.
**Success Criteria**: AC6 is traceable to the shared contract and focused structural checks can detect roster, write-authority, or output-shape regressions.
**Status**: Not Started
