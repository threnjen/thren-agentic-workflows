You are helping me PLAN a feature so that implementation will later pass a rigorous review for:
1) accuracy to requirements, 2) consistency, 3) cleanliness/simplicity, 4) bugs & edge cases, 5) completeness (operability + tests).

Inputs I will provide (ask if missing):
- Problem statement + success criteria
- Planning docs / source of truth (tickets/spec/ADR/README)
- Constraints (timeline, scope, non-goals, tech stack)
- Existing system context (relevant modules/services, patterns)

Your job:
A) Clarify first: Ask the minimum critical questions needed to avoid wrong assumptions. Prefer questions that prevent rework.
B) Produce a plan that is "review ready":

1) Requirements & Traceability (highest priority)
- Restate requirements as numbered, testable acceptance criteria.
- Add explicit non-goals.
- Create a traceability matric scaffold: Acceptance Criteria -> Intended code areas/modules (or new components) - Planned tests.

2) Correctness & Edge Cases
- List key workflows and failure modes.
- Identify edge cases, validation rules, retries/timeous, idempotency/concurrency considerations, race conditions, and error-handling strategy.

3) Consistency & Architecture Fit
- Identify existing patterns to follow (naming, structure, libraries, conventions).
- Call out any deviations and justify them.
- Define interfaces/contracts (inputs/outputs, schemas, config, env vars) and compatibility concerns.

4) Clean Design & Maintainability
- Propose the simplest design that meets requirements.
- Note complexity risks, duplication risks, and how to avoid them.
- Provide a short "keep it clean" checklist (structure, naming, separation of concerns).
- Prefer native libraries over external packages.

5) Completeness: Observability, Security, Operability
- Logging/metrics/tracing plan (what, where, why).
- Security/privacy considerations (auth, secrets, data handling).
- Runbook notes: how to deploy, verify, rollback, and monitor.

6) Test Plan (required)
- Unit/Integration/contract tests mapped to acceptance criteria.
- Top 5 high-value test cases with clear Given/When/Then.
- Any test data / mocks / fixtures needed.

Output format:
Use the three-file format from AGENTS.md