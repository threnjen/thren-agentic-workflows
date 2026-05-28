---
name: phase-document-writing
description: "Write or update Phase documents and Phases Overview files. Use when: creating phase summaries, writing project roadmaps, drafting PHASE_0N_SUMMARY.md files, producing PROJECT_ROADMAP.md, or any task that outputs planning documents in the docs/phases/ directory."
---

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

## Objective

[1-2 sentences: what this phase accomplishes and why it matters]

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
Reference specific files/modules so the Feature - Decomposer knows where to look.]

## Dependencies & Risks

- **Dependency**: [what this phase needs from prior phases or external systems]
- **Risk**: [technical or scope risk, with mitigation]

## Success Criteria

- [ ] [Testable outcome 1]
- [ ] [Testable outcome 2]

## QA Considerations

- [Note whether this phase includes frontend/UI changes requiring manual QA docs]
- [For pure backend work, note if API contracts or integration behavior changes]
- [If backend changes require frontend testing, note coordination with frontend repos]

## Notes for Feature - Decomposer

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
- [ ] Success criteria are testable
- [ ] Technical context references specific files, modules, or patterns
- [ ] "Notes for Feature - Decomposer" section provides decomposition guidance
- [ ] Non-goals are defined at both project and phase level
- [ ] Edge cases, failure modes, and key user flows documented
- [ ] Dependencies (internal, external, cross-phase) and risks have mitigations
- [ ] Integration points with other phases/systems identified
