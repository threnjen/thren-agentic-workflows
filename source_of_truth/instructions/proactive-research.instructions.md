---
description: "Requires agents to look things up instead of asking the user - Context7 for library and framework documentation, @Web Researcher for everything else. Audience is DERIVED for pipeline stages 01-02; `debugger` is enumerated because it sits outside the numbered pipeline."
applyTo: "source_of_truth/agents/0[12]-*.agent.md,**/debugger.agent.md"
baseline: true
---

# Proactive Research Over Asking the User

When you encounter an unfamiliar technology, API, service, pattern, constraint, error, or version-specific issue, **spawn `@Web Researcher` immediately** rather than asking the user to explain it. The user expects you to look things up yourself. Only ask the user for information that is inherently project-specific and cannot be found online (e.g., business priorities, internal team decisions, undocumented requirements). Default to researching first, then presenting what you found alongside any remaining questions that truly require the user's input.

## Library Documentation Comes From Context7

Use the Context7 MCP server whenever the user asks about a library, framework, SDK, API, CLI tool, or cloud service. This covers API syntax, configuration, version migration, library-specific debugging, setup, and CLI usage. Use it for well-known tools too. Your training data may not reflect recent releases. Prefer Context7 over a web search for library documentation.

Do not use Context7 for refactoring, writing a script from scratch, debugging business logic, code review, or general programming concepts.

Follow these steps.

1. Call `resolve-library-id` with the library name and the user's question. Skip this step only when the user supplies an exact `/org/project` identifier.
2. Pick the best match by exact name, description relevance, snippet count, source reputation, and benchmark score. Try an alternate name or phrasing when no result fits. Use a version-specific identifier when the user names a version.
3. Call `query-docs` with that identifier and the user's full question. Scope each call to one concept.
4. Answer from the fetched documentation.

Split a question that spans several concepts into one `query-docs` call per concept, reusing the same identifier. A combined query dilutes ranking and returns shallow results for each topic. Keep the concepts in one call only when the question is about how they interact.

## Load Canary

When this file is loaded, state once, before your first substantive output: *"Instruction loaded: proactive-research."* Then proceed normally.
