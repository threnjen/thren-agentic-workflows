---
name: phase-document-writing
description: "Write or update Phase documents and Phases Overview files. Use when: creating phase summaries, writing project roadmaps, drafting PHASE_0N_SUMMARY.md files, producing PROJECT_ROADMAP.md, or any task that outputs planning documents in the docs/phases/ directory."
---

# Phase Document Writing

This skill defines templates and quality standards for two document types: individual Phase summaries and the Phases Overview roadmap.

## Phase Document Template

Each `docs/phases/PHASE_0N/PHASE_0N_SUMMARY.md` must include:

```markdown
# Phase N: [Phase Name]

**Status**: Planned | In Progress | Complete | Deferred
**Depends on**: Phase N-1 (if applicable), or "None"
**Estimated complexity**: Small | Medium | Large
**Cross-references**: [Links to counterpart docs in related repos, if applicable]

## What's New

[Write a brief summary of changes or new features introduced in this phase. Focus this section on users. Use natural language to explain practical impact, not technical details. Include context that explains why these changes matter to the end user.]

## Problem

[State the problem this phase solves as a symptom, not a mechanism. Describe what is wrong today and who it hurts, not what you will build. If preference, exploration, or taste drives the phase, say so plainly.]

## Objective

[Write 1-2 sentences. State what this phase does about the Problem above. Explain why this response is appropriate.]

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

[Describe existing code, patterns, libraries, or infrastructure relevant to this phase. Reference specific files/modules so Phase - Execute knows where to look.]

## Dependencies & Risks

- **Dependency**: [State what this phase needs from prior phases or external systems]
- **Risk**: [State the technical or scope risk and its mitigation]

## Success Criteria

- [ ] [Testable outcome 1]
- [ ] [Testable outcome 2]
- [ ] [For phases that render UI: state each visual criterion as a discrete, on-screen-observable check. Write one criterion per line. A reviewer must be able to judge each criterion against what the running project shows. Examples: "the two teams render in distinct colors", "a health bar sits above each unit", "the play area is bounded by a visible border"]

## QA Considerations

- [State whether this phase includes frontend/UI changes that require manual QA docs]
- [For pure backend work, state whether API contracts or integration behavior change]
- [If backend changes require frontend testing, state how this phase coordinates with frontend repos]

## Notes for Phase - Execute

[Describe how to decompose this phase. Suggest feature boundaries. Identify areas that need careful separation of concerns. Identify integration points between features.]
```

## Phases Overview Template

`docs/phases/PROJECT_ROADMAP.md` provides a concise roadmap:

```markdown
# Project Roadmap: [Project Name]

## Vision
[Describe the finished project in 1-2 sentences.]

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

- [ ] Phase ordering respects dependencies. No forward references exist.
- [ ] Each phase is self-contained and independently valuable
- [ ] Each phase has explicit in-scope and out-of-scope boundaries
- [ ] The Problem is a symptom. A phase with a non-problem driver names that driver honestly.
- [ ] Success criteria are testable
- [ ] Success criteria measure progress on the Problem, not only the mechanism
- [ ] For phases that render UI, success criteria include discrete, visually-checkable on-screen statements (color, layout, element presence). Do not write only "looks correct".
- [ ] Technical context references specific files, modules, or patterns
- [ ] "Notes for Phase - Execute" section provides decomposition guidance
- [ ] Each phase defines project- and phase-level non-goals
- [ ] Document edge cases, failure modes, and key user flows
- [ ] Dependencies and risks include mitigations
- [ ] Identify integration points with other phases or systems

## Phase Numbering and Recorded Decisions

- **A phase number is a public identifier. Changing its meaning breaks every document that cites it. No warning identifies the break.** Grep for the number before you re-point it. Read the dependency column for execution order, never the number.
- **Agent numbers are pipeline positions, not phase numbers.** Do not "correct" them to match.
- **A resolved decision does not change when later work reverses it.** Treat every entry as time-stamped intent. Check what actually shipped before trusting it.
- **If a rescope only relocates work, suspect that it preserves the old scope.** A good rescope deletes work.
- **When inventory, counts, schemas, or contract rules change, update every summary surface in the same change.** Stale intros, comparison tables, and diagrams still list removed keys and mislead agents that bootstrap from them. Recounting cannot resolve a *definition* conflict. Reconcile the counted term first.
