---
name: phase-document-writing
description: "Write or update Phase documents and Phases Overview files. Use when: creating phase summaries, writing project roadmaps, drafting PHASE_0N_SUMMARY.md files, producing PROJECT_ROADMAP.md, or any task that outputs planning documents in the docs/phases/ directory."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->
# Phase Document Writing

Templates and quality standards for the two document types produced by the project planning pipeline: individual Phase summaries and the Phases Overview roadmap.

## Phase Document Template

Each `docs/phases/PHASE_0N/PHASE_0N_SUMMARY.md` must include:

```markdown
# Phase N: [Phase Name]

**Status**: Planned | In Progress | Complete | Deferred
**Depends on**: Phase N-1 (if applicable), or "None"
**Estimated complexity**: Small | Medium | Large
**Cross-references**: [Links to counterpart docs in related repos, if applicable]

## What's New

[Brief summary of changes or new features introduced in this phase. Keep this section user-focused and use natural language to explain in practical impact terms, not technical terms. Include any relevant context for why these changes matter to the end user.]

## Problem

[The problem this phase solves, stated as a symptom rather than a mechanism. Write what is
wrong today and who it hurts, not what will be built. When the phase is driven by preference,
exploration, or taste rather than a problem, say that plainly here instead.]

## Objective

[1-2 sentences: what this phase does about the Problem above, and why that is the right response]

## Scope

### In Scope
- [Concrete deliverable 1]
- [Concrete deliverable 2]

### Out of Scope
- [Explicitly excluded item — prevents scope creep]

## Key Deliverables

| # | Deliverable | Description | Likely Features |
|---|-------------|-------------|-----------------|
| 1 | [name]      | [what it is]| [feature areas] |

## Technical Context

[Existing code, patterns, libraries, or infrastructure relevant to this phase.
Reference specific files/modules so Phase - Execute knows where to look.]

## Dependencies & Risks

- **Dependency**: [what this phase needs from prior phases or external systems]
- **Risk**: [technical or scope risk, with mitigation]

## Success Criteria

- [ ] [Testable outcome 1]
- [ ] [Testable outcome 2]
- [ ] [For phases that render UI: state each visual criterion as a discrete, on-screen-observable check — e.g. "the two teams render in distinct colors", "a health bar sits above each unit", "the play area is bounded by a visible border" — one per line, so a reviewer can judge each against what the running project shows]

## QA Considerations

- [Note whether this phase includes frontend/UI changes requiring manual QA docs]
- [For pure backend work, note if API contracts or integration behavior changes]
- [If backend changes require frontend testing, note coordination with frontend repos]

## Notes for Phase - Execute

[Guidance on how to decompose this phase: suggested feature boundaries,
areas that need careful separation of concerns, integration points between features.]
```

## Phases Overview Template

`docs/phases/PROJECT_ROADMAP.md` provides the roadmap at a glance:

```markdown
# Project Roadmap: [Project Name]

## Vision
[1-2 sentences: what the finished project looks like]

## Phases

| Phase | Name | Status | Depends On | Complexity | Description |
|-------|------|--------|------------|------------|-------------|
| 01    | ...  | Planned| None       | Medium     | ...         |
| 02    | ...  | Planned| Phase 01   | Large      | ...         |

## Constraints & Non-Goals
- [Project-wide constraint]
- [Explicit non-goal for the entire project]

## Architecture Notes
[High-level architecture decisions that span multiple phases.
Tech stack, patterns, infrastructure choices.]
```

## Quality Checklist

Before presenting or writing any Phase document, verify:

- [ ] Phase ordering respects dependencies (no forward references)
- [ ] Each phase is self-contained and independently valuable
- [ ] Scope boundaries are explicit (in-scope AND out-of-scope per phase)
- [ ] The Problem is stated as a symptom, or the phase names a non-problem driver honestly
- [ ] Success criteria are testable
- [ ] Success criteria measure the Problem moving, not merely the mechanism existing
- [ ] For phases that render UI, success criteria include discrete, visually-checkable on-screen statements (color, layout, element presence) — not just "looks correct"
- [ ] Technical context references specific files, modules, or patterns
- [ ] "Notes for Phase - Execute" section provides decomposition guidance
- [ ] Non-goals are defined at both project and phase level
- [ ] Edge cases, failure modes, and key user flows documented
- [ ] Dependencies (internal, external, cross-phase) and risks have mitigations
- [ ] Integration points with other phases/systems identified

## Phase Numbering and Recorded Decisions

- **A phase number is a public identifier — changing what it denotes breaks every document citing it, and nothing warns you.** Grep for the number before re-pointing one. Read the dependency column for execution order, never the number.
- **Agent numbers are pipeline positions, not phase numbers.** Do not "correct" them to match.
- **A decision recorded as resolved does not update itself when later work reverses it.** Treat every entry as time-stamped intent; check what actually shipped before trusting it.
- **If a rescope only relocates work, suspect the new scope is the old scope wearing a hat.** A good rescope deletes work.
- **When inventory, counts, schemas, or contract rules change, update every summary surface in the same change.** Stale intros, comparison tables, and diagrams keep advertising removed keys and mislead the agents that bootstrap from them. Recounting cannot fix a *definition* conflict — reconcile what the counted term means first.
