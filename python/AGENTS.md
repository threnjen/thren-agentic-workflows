# Agent Guidelines

## Principles

- Incremental progress over big bangs — small changes that compile and pass tests
- Learn from existing code — find 3 similar features, study patterns before implementing
- Pragmatic over dogmatic — adapt to project reality
- Clear intent over clever code — be boring and obvious
- Single responsibility per function/class
- Composition over inheritance; interfaces over singletons
- Explicit data flow; fail fast with descriptive errors
- Include context for debugging; handle errors at appropriate level; never silently swallow exceptions
- If you need to explain it, it's too complex

## Plan Mode Rules

- **NEVER** output code blocks in Plan mode
- Describe changes for someone else to execute later
- If you catch yourself writing implementation, **STOP**
- Link to files and reference `symbols`, don't show code

## Process

### Implementation Flow
1. **Plan** — study existing patterns.
2. **Test** — write test first (red)
3. **Implement** — minimal code to pass (green)
4. **Refactor** — clean up with tests passing
5. **Commit** — clear message explaining "why"

### When Stuck (Max 3 Attempts)
1. Document what failed (steps, errors, hypothesis)
2. Research 2-3 alternative implementations
3. Question fundamentals — simpler approach? different abstraction?
4. Try different angle — then STOP and reassess

## Testing

### TDD Workflow
- Write tests BEFORE implementation; confirm they fail first.
- Run full suite to catch regressions.
- SHOULD NOT add test unless it can fail for a real defect.
- Strong assertions (`toEqual` over `toBeGreaterThanOrEqual`)
- One assertion per test; group under `describe(functionName)`

### When Requirements Change
- Udpate/delete affected tests FIRST, then change code
- Stale tests (for removed behavior) should be deleted, not skipped
- Deprecated functions: remove tests entirely or update to test new stub behavior
- If unsure whether a test is stale: check if the requirement still exists

## Quality Standards

### Every Commit Must
- [ ] Compile successfully
- [ ] Pass all tests (new functionality included)
- [ ] Follow project formatting/linting
- [ ] Have clear commit message (Conventional Commits)
- [ ] No TODOs without issue numbers
- [ ] Check plan is up-to-date before commit

### Always
- Commit early and often with meaningful messages

### Never
- Use `--no-verify` to bypass hooks
- Disable tests instead of fixing them
- Commit code that doesn't compile
- Reference "Claude" or "AI-generated" in messages

### Decision Priority
Testability → Readability → Consistency → Simplicity → Reversibility

## Agent Operations

### Context Clearing
Clear at 60k tokens or 30% context:
1. Write progress to `.md` file
2. `/clear` the context
3. Start fresh session reading the `.md` file

### Subagents
- Main agent spawns Task(...) clones for parallel work
- Fresh context = better critique for self-review
- Review for: spaghetti code, API changes, missing error handling, security issues

### Self-Review Checklist
- [ ] Logic easy to follow?
- [ ] No unnecessary imports/functions/comments?
- [ ] Error handling complete?
- [ ] Security vulnerabilities addressed?

## Task Documentation

### Three-File Pattern
```
dev/active/[task-name]/
├── [task-name]-plan.md      # Accepted plan with stages
├── [task-name]-context.md   # Key files, decisions
└── [task-name]-tasks.md     # Checklist of work
```

### Plan Template
```markdown
## Stage N: [Name]
**Goal**: [Specific deliverable]
**Success Criteria**: [Testable outcomes]
**Status**: [Not Started|In Progress|Complete]
```

### Workflow
- Create task directory when starting large work
- Update status immediately as tasks complete
- Check `/dev/active/` for existing tasks before starting
- Read all three files before proceeding with existing task
- Remove plan file when all stages done

## Extended Guides

Load when applicable:
- *Phase Planning* -> `docs/PLANNING_WORKFLOW.md` - for migrations or multi-stage projects spanning multiple commits
- *Style Guide* -> `docs/STYLE_GUIDE.md` - When writing new modules or unfamiliar with project conventions
