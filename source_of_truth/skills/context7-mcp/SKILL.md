---
name: context7-mcp
description: This skill should be used when the user asks about libraries, frameworks, API references, or needs code examples. Activates for setup questions, code generation involving libraries, or mentions of specific frameworks like React, Vue, Next.js, Prisma, Supabase, etc.
---

Use the always-on baseline instructions for Context7 call argument shapes. The baseline defines when to use Context7, the four steps, and the one-concept-per-query rule. This file defines only details that the baseline does not define.

- `resolve-library-id` — `libraryName`: the library name from the user's question. `query`: the user's full question (improves relevance ranking).
- `query-docs` — `libraryId`: the selected ID, e.g. `/vercel/next.js`. `query`: the user's question scoped to a single concept.
- When the user names a version ("Next.js 15", "React 19"), prefer a version-specific library ID if the resolution step returned one.
- When several matches tie, prefer the official or primary package over a community fork.
