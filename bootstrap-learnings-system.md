# Bootstrap: Learnings System for Agent Pipeline

## Goal

Set up a "living learnings" infrastructure in your **project repo** (`.github/learnings/`). This system ensures agents learn from past mistakes, reviewers don't rediscover known issues, and deferred decisions from previous phases aren't lost.

All learnings are stored in the project repo — the agents repo contains no learnings. This repo is always loaded alongside the project repo, so agents reference `.github/learnings/` paths which resolve in the project workspace.

---

## Part 1: Create the Learnings Files

Create these files in your project repo. Start them with headers and a `---` separator. Leave them empty of entries (no seed data) — agents will populate them as they work.

### A. `.github/learnings/project-learnings.md`

```markdown
# Project Learnings

Project-specific findings and patterns discovered during development. All team members should read this early when debugging or planning features for this project. Append new entries as issues are discovered and resolved.

---
```

Entry format (for agents to follow when appending):

```markdown
## If you see X, check Y

**Problem:** What was broken and how it manifested
**Root cause:** The actual underlying issue
**Fix:** What was changed
**Watch for:** How to spot this pattern early next time
```

### B. `.github/learnings/review-learnings.md`

```markdown
# Review Learnings

Recurring patterns found during code reviews. Read this before reviewing new features to catch known issues faster.

---
```

Entry format:

```markdown
## If you see X, check Y

**Pattern:** What the recurring issue is
**Impact:** Low/Medium/High — what breaks or degrades
**Watch for:** How to detect this during review
```

### C. `.github/learnings/cross-phase-decisions.md`

```markdown
# Cross-Phase Decisions

Decisions, deferrals, and known gaps from completed phases that affect future planning. Read this during Phase Refinement and Feature Decomposition to avoid rediscovering buried context.

---
```

Organize entries under section headers by source phase. Use three categories:

- `### Must-do before Phase NN` — tech debt that blocks the next phase
- `### Known gaps to address when needed` — deferred items with no immediate urgency
- `### Design interpretations` — not bugs, but decisions to revisit if gameplay/UX feedback warrants it

Each entry is a bullet point: `- **Short title**: Description. *(Source: NN-feature-name review)*`

### D. `.github/learnings/debugging-learnings.md`

```markdown
# Debugging Learnings

Patterns from past debugging sessions. Check these before diagnosing new issues.

---
```

Same entry format as project-learnings.md (Problem, Root cause, Fix, Watch for).

---

## Part 2: Agent Wiring (already done)

The following agents are already wired to read and write learnings files in `.github/learnings/`:

- **Feature Reviewer** — Reads all four learnings files before review. Writes to `review-learnings.md` and `cross-phase-decisions.md` after each review.
- **Feature Decomposer** — Reads `project-learnings.md`, `debugging-learnings.md`, and `cross-phase-decisions.md` during discovery.
- **Phase Refiner** — Reads `cross-phase-decisions.md` when refining phase documents or drafting standalone features.
- **Debugger** — Reads `project-learnings.md` and `debugging-learnings.md` before diagnosing. Writes to `project-learnings.md` or `debugging-learnings.md` after fixing.

---

## Part 3: Add Integration Feature Rule (prevents missing bootstrap)

This prevents the specific failure where multiple features pass review individually but produce a non-functional application because no one wired them together.

### In the feature-plan-set skill (SKILL.md)

Add to the **Decomposition Rules** section:

```
- **Integration feature rule**: When a phase produces multiple features that must work together at
  runtime (e.g., a data system, a renderer, and a UI that all need to be wired into a running
  application), the **final numbered feature** must be an integration/bootstrap task. This feature
  initializes and connects the other features into a runnable application entry point (e.g., a scene
  bootstrap script, an app startup module, a main entry point). Its acceptance criteria must include:
  the application launches and all features from the phase are visually or functionally demonstrated
  working together. Omitting this step causes all features to pass review in isolation while producing
  a non-functional application.
```

Add to the **Quality Checklist** section:

```
- [ ] If phase has 2+ features that must interact at runtime, the final feature is an
      integration/bootstrap task
```

### In the Feature Decomposer agent

Add to **Phase 2: Decomposition**, after the decomposition analysis:

```
**Integration check**: After decomposition, evaluate whether the resulting features need to work
together at runtime. If they do (e.g., a data layer, rendering system, and UI that must all be
initialized and connected to produce a working application), you MUST create a final
integration/bootstrap feature that wires them into a runnable entry point. See the "Integration
feature rule" in the `feature-plan-set` skill. Omitting this step results in features that pass
review in isolation but produce a non-functional application.
```

---

## Summary: Read/Write Matrix

| File | Location | Who reads | Who writes |
|------|----------|-----------|------------|
| `project-learnings.md` | Project `.github/learnings/` | Reviewer, Decomposer, Debugger | Debugger |
| `review-learnings.md` | Project `.github/learnings/` | Reviewer | Reviewer |
| `cross-phase-decisions.md` | Project `.github/learnings/` | Reviewer, Decomposer, Phase Refiner | Reviewer |
| `debugging-learnings.md` | Agents `.github/learnings/` | Reviewer, Decomposer, Debugger | Debugger |

## The Feedback Loop

```
Debugger finds bugs
  → writes to project-learnings + debugging-learnings
    → Reviewer reads them during next review
      → Reviewer finds patterns
        → writes to review-learnings + cross-phase-decisions
          → Decomposer and Refiner read those during next planning cycle
            → fewer bugs reach the Debugger
```

---

Replace `<PROJECT_REPO>` and `<AGENTS_REPO>` with the actual repo paths in your workspace.
