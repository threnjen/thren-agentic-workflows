---
description: "Requires agents to look things up instead of asking the user - Context7 for library and framework documentation, @Web Researcher for everything else. Audience is DERIVED for pipeline stages 01-02; `debugger` is enumerated because it sits outside the numbered pipeline."
applyTo: "source_of_truth/agents/0[12]-*.agent.md,**/debugger.agent.md"
baseline: true
---

# Research Before Asking the User

When you meet an unfamiliar technology, API, service, pattern, constraint, error, or version-specific issue, spawn `@Web Researcher`. Do not ask the user to explain it. Ask the user only for information you cannot find online: business priorities, internal team decisions, or undocumented requirements. Research first. Present your findings with the questions that still need the user's answer.

## Library Documentation Comes From Context7

Use the Context7 MCP server for any question about a library, framework, SDK, API, CLI tool, or cloud service. The Context7 MCP server covers API syntax, configuration, version migration, library-specific debugging, setup, and CLI usage. Use the Context7 MCP server for well-known tools because your training data may not reflect recent releases.
Prefer the Context7 MCP server to a web search.

Do not use Context7 for refactoring, writing a script from scratch, debugging business logic, code review, or general programming concepts.

1. Call `resolve-library-id` with the library name and the user's question.
   Skip `resolve-library-id` only when the user gives an exact `/org/project` identifier.
2. Pick the best match by exact name, description relevance, snippet count, source reputation, and benchmark score.
   Try another name or phrasing when no match fits.
   Use a version-specific identifier when the user names a version.
3. Call `query-docs` with the selected identifier and the user's full question.
   Scope each call to one concept.
4. Answer from the documentation you fetched.

Split a question that spans several concepts into one `query-docs` call per concept. Reuse the same identifier for each call. A combined query dilutes ranking and returns shallow results for every topic in the query. Use one call for multiple concepts only when the question asks how those concepts interact.

## Load Canary

When this file is loaded, state once, before your first substantive output: *"Instruction loaded: proactive-research."* Then proceed normally.
