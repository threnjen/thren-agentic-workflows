---
name: context7-mcp
description: "This skill should be used when the user asks about libraries, frameworks, API references, or needs code examples. Activates for setup questions, code generation involving libraries, or mentions of specific frameworks like React, Vue, Next.js, Prisma, Supabase, etc."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->
Call argument shapes for the Context7 procedure in the always-on baseline instructions. The baseline owns when to use Context7, the four steps, and the one-concept-per-query rule; this file adds only what it omits.

- `resolve-library-id` — `libraryName`: the library name from the user's question. `query`: the user's full question (improves relevance ranking).
- `query-docs` — `libraryId`: the selected ID, e.g. `/vercel/next.js`. `query`: the user's question scoped to a single concept.
- When the user names a version ("Next.js 15", "React 19"), prefer a version-specific library ID if the resolution step returned one.
- When several matches tie, prefer the official/primary package over a community fork.
