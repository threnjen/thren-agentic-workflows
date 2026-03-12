You are conducting a structured test suite evaluation.

Goal: Reduce unnecessary or low-value tests while preserving behavioral guarantees and meaningful coverage.

Do NOT delete or modify tests in this session.
Your task is analysis and planning only.
Your deliverable is planning documents according to your AGENTS.md file.

For each test file:
1. Identify what behavior or invariant it protects.
2. Determine whether it tests:
    - Core business logic
    - Public API contract
    - Edge cases with real production risk
    - Implementation details
    - Redundant permutations
    - Framework/library behavior
3. Flag tests that appear:
    - Redundant with other tests
    - Testing implementation rather than behavior
    - Overly granular with low signal
    - Snapshot-based without strong justification
    - Exessively mocking internal structure

Produce:

1. A categorized inventory:
    - High-value tests (must-keep)
    - Questionable-value tests (review required)
    - Likely redundant tests
    - Candidates for consolidation

2. Risk assessment
    - What would break if removed?
    - Where coverage would drop meaningfully

3. A staged redution plan:
    - Phase 1: safe removals
    - Phase 2: Consolidations
    - Phase 3: Refactors to improve signal

4. Guiding principles for future test additions.

Format the deliverables according to AGENTS.md.
Do not propose blind deletions. Every recommendation must include rationale.