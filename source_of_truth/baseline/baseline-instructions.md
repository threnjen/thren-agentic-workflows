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

Every piece of English you write has a reader. Pick the mode from the reader, not from
the surrounding style. Style-matching applies to **code, not prose.**

**Strict** — procedures, error messages, tool and agent descriptions, agent-to-agent
instructions, safety text. Anything parsed without a human present to resolve ambiguity.

**Flavored** — READMEs, PR descriptions, changelogs, explanatory prose, replies to a
human. Same sentence discipline, but word choice stays free.

**Neither** — client-facing deliverables, marketing copy, creative writing. Never apply
these rules there. Client deliverables follow `engagement-client-voice` instead.

Dense is still correct for machine-facing planning docs — phase summaries, discovery
context, roadmaps, feature plan/context/tasks bundles. The workflow consumes these to
decompose work, so spelling out every constraint helps. Dense is never an excuse for
ambiguous.

Sentence rules, both modes:

- Active voice. One instruction per sentence.
- 20 words for an instruction, 25 for a description.
- No semicolons. Plain verbs — start, not spin up; contact, not reach out.
- Three words maximum in a noun stack. Keep the subject, verb, and article explicit.
- Simple tenses, unless the compound tense carries information the simple one cannot.

Strict mode adds: one word per action, one name per thing, verbs over noun forms, and
every domain term unpacked inline on first use.

Human-facing documents also need:

- Answer first: the conclusion and what it changes. Evidence after, or behind a link.
- Decision-driving numbers translated into words, then given as numbers.
- One caveat, not three. Bold the decision, not the vocabulary.
- Runbooks and checklists: TL;DR of five lines or fewer, then numbered steps — one action
  each, with the exact command and what a correct result looks like. Rationale below the
  steps. Warnings where the mistake happens, not in a preamble. When a step changes,
  rewrite the step — no correction-log narration in the body.

Never weaken or strengthen a hedge to save words. "May have failed" is not "failed", and
confidence is content.

- BAD: "prose is the one thing this corpus needs to be free to reword"
- GOOD: "We need to be able to rewrite the words freely"

Write to a colleague who is sharp, busy, and has not read the rest of the phase. If the
reader asks for a simpler version, the first version was wrong. For a full rewrite pass
over existing text, load the `plain-technical-english` skill.
<!-- know-the-audience -->
