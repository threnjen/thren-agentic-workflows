# Feature Plan: Phase Final-Check Contract

## Execution Metadata

- **Wave:** 1
- **Parallel safe:** yes
- **Depends on:** none
- **Key files modified:** `source_of_truth/skills/[PROPOSED - name TBD: phase-final-check]/SKILL.md`
- **Sequential reason:** n/a

## A. Requirements & Traceability

### Acceptance Criteria

1. **AC1:** A new terse skill defines the final-check review contract and is suitable for both Phase - Refiner and the hidden reviewer to consume by reference.
2. **AC2:** The contract limits reading to the supplied phase document and the repository available to a newcomer, including `docs/phases/DISCOVERY_CONTEXT.md` and `docs/learnings/cross-phase-decisions.md` when present.
3. **AC3:** The contract makes blindness a spawner obligation: the spawn input contains only the phase document path and repository path, with no conversation content, session summary, settled-area briefing, or assessment of what deserves attention.
4. **AC4:** Findings are restricted to the six Phase 02 categories: contradiction, ambiguous scope boundary, uncheckable success criterion, undefined term, unaddressed dependency or risk, and deliverable without a matching success criterion.
5. **AC5:** Every finding cites a phase-document location or concrete repository fact, has no severity rating, and the report contains at most five findings.
6. **AC6:** The report states when more qualifying findings were omitted because of the cap, and states plainly when no finding qualifies without padding.
7. **AC7:** The contract excludes roadmap/discovery-context synchronization state, pass/fail judgments, blocking thresholds, retry loops, repository writes, and direct edits to the phase document.
8. **AC8:** The skill is dense and brief, and its reusable contract is not copied into consumer agent bodies.

### Non-Goals

- Do not create the reviewer agent; `06-phase-final-check-reviewer` owns it.
- Do not edit Phase - Refiner or its roster; `07-phase-refiner-final-check` owns consumer wiring.
- Do not add tests in this feature; the integration feature owns the structural and mutation-tested guards required by the phase.
- Do not add a rubric, severity scale, verdict, persisted findings artifact, or second review pass.
- Do not edit `ports/` or `.github/`, and do not run propagation.

### Traceability

| Acceptance Criteria | Code Areas/Modules | Test / Evidence Category |
|---|---|---|
| AC1–AC7 | `source_of_truth/skills/[PROPOSED - name TBD: phase-final-check]/SKILL.md` | Must-have automated test in downstream `07-phase-refiner-final-check` |
| AC8 | New skill plus existing duplicate-block guard in `tests/test_agent_corpus_invariants.py` | Existing test to update: no update expected; run as regression evidence |

## B. Correctness & Edge Cases

- Missing optional discovery or learning files do not fail the review; the reviewer proceeds with the phase document and repository state that exists.
- Repository facts may support a finding, but surrounding-file sync state is not itself a finding because the check runs before synchronization.
- Similar observations must be consolidated before applying the five-finding cap.
- A weak or speculative observation is omitted rather than padded into the response.
- The blindness boundary applies to the spawning input, not committed repository documents.
- Error handling remains outside this reusable review contract: the Refiner owns reviewer failure and no-answer continuation behavior.

## C. Consistency & Architecture Fit

- Follow the existing directory-based skill convention: one `SKILL.md` under `source_of_truth/skills/` with `name` and `description` frontmatter.
- Use `[PROPOSED - name TBD: phase-final-check]` until implementation selects and records the final idiomatic skill slug; the Phase document fixes the contract but not the skill name.
- Keep the contract in the skill and have both consumers reference it. This follows the corpus duplicate-block constraint and the Phase document's two-consumer rationale.
- Public contract consumed downstream: the skill supplies the reading boundary, blindness obligations, finding eligibility rules, cap, and response shape. `06-phase-final-check-reviewer` follows it; `07-phase-refiner-final-check` follows its spawn-input obligations.
- Relationship: `06-phase-final-check-reviewer` and `07-phase-refiner-final-check` depend on this feature's finalized contract vocabulary.

### Unverified Assumptions

- The final skill slug is not specified by Phase 02. The implementer must choose a collision-safe, concise slug and carry that exact reference into both consumers and the focused tests.

## D. Clean Design & Maintainability

- Define each obligation once.
- Separate what the reviewer may read, what qualifies as a finding, and how it reports.
- Avoid examples long enough to become a second specification.
- Keep failure handling and user interaction in Phase - Refiner rather than the shared contract.

### Keep It Clean Checklist

- [ ] No duplicated contract block in agent bodies.
- [ ] No severity or verdict vocabulary.
- [ ] No findings file or edit authority.
- [ ] No generated-output edits.

## E. Completeness: Observability, Security, Operability

- **Observability decision:** Add no logs or persisted artifacts. The response itself is the only output; zero findings and truncated-at-five are explicit response states.
- **Security:** The contract exposes only repository paths already supplied to the reviewer. It must not request secrets, uncommitted conversation content, or external systems.
- **Runbook:** Verify the skill with the focused Phase 02 guard module, then run corpus invariants. Roll back by removing the new skill and downstream references together. Propagation remains a maintainer step.
- **Baseline:** `uv run pytest tests/` collected 242 tests on 2026-08-11: 230 passed and 12 pre-existing failures. The failures are outside Phase 02: one PR Review name collision, one wildcard `applyTo` enumeration issue, and ten Phase 01 Unity reference-asset failures caused by a missing workflow asset.

## F. Test Plan

| Acceptance Criteria | Evidence | Category |
|---|---|---|
| AC1–AC3 | Parse the new skill and verify the reading/spawn boundaries without requiring one exact prose rendering | Must-have automated test |
| AC4–AC7 | Verify the six-category set, cap/report states, and excluded authority with scoped, non-vacuous guards | Must-have automated test |
| AC8 | Run the existing duplicate-block and skill-frontmatter corpus invariants | Existing test to update: no update expected; run as regression evidence |

### Top Five High-Value Checks

1. Given the contract skill, when the reading boundary is inspected, then the phase document and permitted committed context are included while conversation context is excluded.
2. Given a spawn-contract mutation that adds a session summary, when the focused guard runs, then it fails for the blindness obligation.
3. Given the finding category inventory, when one category is deleted, then the focused guard fails and names the missing category.
4. Given six qualifying observations, when the report contract is applied, then no more than five are returned and omission is disclosed.
5. Given no qualifying observation, when the report contract is applied, then the response says so plainly and creates no artifact.

### Fixtures and Test Impact

- `07-phase-refiner-final-check` creates `tests/[PROPOSED - name TBD: phase final-check contract guards]` and proves each content guard red through deletion or semantic negation before restoring green.
- `tests/test_agent_corpus_invariants.py` and `tests/test_propagate_master_assets.py` are regression inputs, not planned edit surfaces.
- No Stage 0 is required: the repository has broad structural coverage across 16 test modules. The red baseline must be preserved without absorbing unrelated failures.

## Stage 1: Contract Skill
**Goal**: Author the reusable reading, blindness, finding, and response contract.
**Success Criteria**: AC1–AC8 are represented once in a terse skill with valid frontmatter.
**Status**: Not Started

## Stage 2: Contract Review
**Goal**: Check the skill against the phase requirements and downstream consumer needs before either consumer is authored.
**Success Criteria**: Every Phase 02 contract requirement is traceable, and no consumer-only workflow or failure handling has leaked into the skill.
**Status**: Not Started

