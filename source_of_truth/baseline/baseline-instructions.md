<!-- context7 -->
Use Context7 MCP to fetch current documentation whenever the user asks about a library, framework, SDK, API, CLI tool, or cloud service — even well-known ones like React, Next.js, Prisma, Express, Tailwind, Django, or Spring Boot. This includes API syntax, configuration, version migration, library-specific debugging, setup instructions, and CLI tool usage. Use even when you think you know the answer — your training data may not reflect recent changes. Prefer this over web search for library docs.

Do not use for: refactoring, writing scripts from scratch, debugging business logic, code review, or general programming concepts.

## Steps

1. Always start with `resolve-library-id` using the library name and the user's question, unless the user provides an exact library ID in `/org/project` format
2. Pick the best match (ID format: `/org/project`) by: exact name match, description relevance, code snippet count, source reputation (High/Medium preferred), and benchmark score (higher is better). If results don't look right, try alternate names or queries (e.g., "next.js" not "nextjs", or rephrase the question). Use version-specific IDs when the user mentions a version
3. `query-docs` with the selected library ID and the user's full question (not single words), scoped to a single concept. If the question spans multiple distinct concepts (e.g. routing and auth and caching), make a separate `query-docs` call per concept with the same library ID, unless the question is about how the concepts interact — combined queries dilute ranking and return shallow results for each topic
4. Answer using the fetched docs
<!-- context7 -->

<!-- code-review-graph -->
## MCP Tools: code-review-graph

When a project has a code-review-graph knowledge graph available, use the
code-review-graph MCP tools BEFORE using file search or reading files to
explore the codebase. The graph is faster, cheaper (fewer tokens), and gives
structural context (callers, dependents, test coverage) that file scanning
cannot.

Use graph tools first for:

- **Exploring code**: `semantic_search_nodes` or `query_graph` instead of text search
- **Understanding impact**: `get_impact_radius` instead of manually tracing imports
- **Code review**: `detect_changes` + `get_review_context` instead of reading entire files
- **Finding relationships**: `query_graph` with callers_of/callees_of/imports_of/tests_for
- **Architecture questions**: `get_architecture_overview` + `list_communities`

Fall back to file search and reading files only when the graph doesn't cover
what you need or the graph tools are unavailable in the session.
<!-- code-review-graph -->

<!-- phase-doc-sync -->
## Phase Document Sync

When working in a repository that has a `docs/phases/` directory, or when the
user references a phase QA doc, a `_QA.md` checklist, QA failures, or asks for
fixes/tweaks/small updates during phase work: load the `phase-doc-sync` skill
before making code changes and follow its documentation-reconciliation
contract. Any change that alters what a phase delivers or how it behaves is
not complete until the affected `PHASE_0N_SUMMARY.md` and `PROJECT_ROADMAP.md`
(or `PHASES_OVERVIEW.md` in legacy repos) entries are updated as baseline
truth — rewritten in place with no change-log framing.
<!-- phase-doc-sync -->

<!-- agent-discovery -->
## Custom Agent and Skill Discovery

When the user asks {harness_title} to act as a named agent, resolve its definition from:

{agent_paths}

When the user explicitly names a skill that is not already available in the
session skill catalog, look for it in:

{skill_paths}

Read the selected agent or skill instructions completely before beginning work.
Do not spawn an agent merely because the user asks {harness_title} to act in that role.
<!-- agent-discovery -->

<!-- know-the-audience -->
## Know The Audience

**Dense is correct for machine-facing docs and spawned subagents** — phase summaries,
discovery context, roadmaps, feature plan/context/tasks bundles. The workflow consumes
these to decompose work, so spelling out every constraint helps.

**Simple is mandatory for human-facing docs and interaction** — QA plans, checklists,
runbooks, chat replies. A runbook's only job is that someone follows it and succeeds.
If it has to be parsed, it failed.

Never carry the machine-facing register into a human-facing doc or a reply.
Style-matching applies to **code, not prose.**

- BAD: "prose is the one thing this corpus needs to be free to reword"
- GOOD: "We need to be able to rewrite the words freely"

Rules for replies and human-facing docs:

- Answer first: open with the conclusion and what it changes. Tables and citations come
  after, or behind a link.
- Unpack every unfamiliar term inline on first use — "monotone (moves one direction, no zigzag)".
- Translate any decision-driving number into plain words, then give the number.
- One idea per sentence. One caveat, not three.
- Bold the decision, not the vocabulary.

Extra rules for runbooks and checklists:

- Open with a TL;DR of five lines or fewer, then numbered steps — one action each, with the
  exact command and what a correct result looks like. Rationale goes below the steps.
- Put warnings where the mistake happens, not in a preamble.
- When a step changes, rewrite the step — no correction-log narration in the body.

Write to a colleague who is sharp, busy, and has not read the rest of the phase. If the
reader asks for a simpler version, the first version was wrong.
<!-- know-the-audience -->
