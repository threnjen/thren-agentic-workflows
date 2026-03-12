You are reviewing an implementation against the planning documents attached.

Goal: Verify the code matches the intent, and surface issues in accuracy, consistency, cleanliness, bugs, edge cases, and completeness. Be skeptical and thorough.

Review tasks (do all)
1) Traceability: Map each requirement/acceptance criterion to the exact code location(s). Call out any requirement that is missing, partially implemented, or implemented differently than specified.
2) Correctness & bugs: Identify likely functional bugs, race conditions, error-handling gaps, and edge cases. Explain impact + reproduction paths.
3) Consistency: Check naming, patterns, structure, and behavior across modules. Flag inconsistences with the docs and within the codebase.
4) Cleanliness: Look for dead code, unnecessary complexity, uncelar abstractions, duplication, and readability issues. Suggest simpler alternatives.
5) Completeness: Confirm observability (logs/metrics/tracing where relevant), retries/timeouts, validation, and failure modes are handled via the docs.
6) Tests: Assess coverage vs requirements. List missing tests and the highest-value test cases.

Output format:
- Start with a short "Top risks" list (max 5), highest impact first.
- Then a table: Issue | Severity (Blocker/High/Med/Low) | Evidence (file:line) | Requirement linkage | Recommendation
- End with a "Quick Wins" section (small fixes with big payoff).

If you're uncertain, say what you'd need to confirm, but still give your best assessment from the current code.