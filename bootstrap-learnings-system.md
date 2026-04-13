# Bootstrap: Two-Tier Learnings System for Agent Pipeline

## Goal

Set up a "living learnings" infrastructure across two repos — an **agents/skills repo** (cross-project patterns) and the **project repo** (project-specific findings). This system ensures agents learn from past mistakes, reviewers don't rediscover known issues, and deferred decisions from previous phases aren't lost.

The system has two tiers:

1. **Project repo** (`<PROJECT_REPO>/.github/learnings/`) — project-specific findings shareable with the whole team via git
2. **Agents repo** (`<AGENTS_REPO>/.github/learnings/`) — cross-project patterns that apply to any project using this agent pipeline

---

## Part 1: Create the Learnings Files

Create these files. Start them with headers and a `---` separator. Leave them empty of entries (no seed data) — agents will populate them as they work.

### A. Project repo: `.github/learnings/project-learnings.md`

```markdown
# Project Learnings

Project-specific findings and patterns discovered during development. All team members should read this early when debugging or planning features for this project. Append new entries as issues are discovered and resolved.

---
```

Entry format (for agents to follow when appending):

```markdown
## YYYY-MM-DD — Short title

**Problem:** What was broken and how it manifested
**Root cause:** The actual underlying issue
**Fix:** What was changed
**Watch for:** How to spot this pattern early next time
```

### B. Project repo: `.github/learnings/review-learnings.md`

```markdown
# Review Learnings

Recurring patterns found during code reviews. Read this before reviewing new features to catch known issues faster.

---
```

Entry format:

```markdown
## YYYY-MM-DD — Short title

**Pattern:** What the recurring issue is
**Impact:** Low/Medium/High — what breaks or degrades
**Watch for:** How to detect this during review
```

### C. Project repo: `.github/learnings/cross-phase-decisions.md`

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

### D. Agents repo: `.github/learnings/debugging-learnings.md`

```markdown
# Debugging Learnings

Cross-project patterns from past debugging sessions. Check these before diagnosing new issues. For project-specific findings, also check `.github/learnings/` in the project repo.

---
```

Same entry format as project-learnings.md (Problem, Root cause, Fix, Watch for). Only cross-project patterns belong here — anything specific to one project's tech stack goes in the project repo instead.

---

## Part 2: Wire Agents to Read Learnings

Modify these agent definition files to read learnings at the start of their workflows.

### Feature Reviewer agent

In the **Required Inputs** section, add as input #4 (or the next number):

```
4. **Learnings** — Read `.github/learnings/project-learnings.md`, `.github/learnings/review-learnings.md`,
   and `.github/learnings/cross-phase-decisions.md` (project repo) and `.github/learnings/debugging-learnings.md`
   (agents repo) if they exist. Check for known patterns that apply to the code under review.
```

### Feature Decomposer agent

In the **Phase 1: Discovery** section, add these two bullet points to the list of things to read:

```
- Read `.github/learnings/project-learnings.md` (project repo) and `.github/learnings/debugging-learnings.md`
  (agents repo) if they exist — they contain past mistakes and patterns to avoid when planning features
- Read `.github/learnings/cross-phase-decisions.md` (project repo) if it exists — it contains deferred work
  and known gaps from previous phases that may need to be addressed in the current phase
```

### Phase Refiner agent

In **Phase 2A** (existing document path), in the list of materials to read, add:

```
- `.github/learnings/cross-phase-decisions.md` (project repo) if it exists — contains deferred work,
  known gaps, and design decisions from prior phases that may need to be pulled into this phase's scope
```

In **Phase 2B** (standalone feature path), in the "Gather context" step, add to the instruction:

```
Read `.github/learnings/cross-phase-decisions.md` (project repo) if it exists — it contains deferred work
and known gaps from prior phases.
```

### Debugger agent (or debugging mode)

Add a **Step 6 — Record Learnings** after the verify step:

```markdown
### Step 6 — Record Learnings

After completing a fix, append a concise entry to the appropriate learnings file:
- **Project-specific findings** (framework quirks, config issues, library behavior)
  → `.github/learnings/project-learnings.md` in the project repo. Create the file if it doesn't exist.
- **Cross-project patterns** (pipeline gaps, architectural anti-patterns, agent workflow failures)
  → `.github/learnings/debugging-learnings.md` in the agents repo.

Each entry should include:
- **Date and short title**
- **Problem** — What was broken and how it manifested
- **Root cause** — The actual underlying issue
- **Fix** — What was changed
- **Watch for** — A sentence on how to spot this pattern early next time

Before diagnosing any new issue, read both learnings files if they exist — a similar pattern may
already be documented:
1. `.github/learnings/project-learnings.md` (project repo — project-specific)
2. `.github/learnings/debugging-learnings.md` (agents repo — cross-project)
```

---

## Part 3: Wire the Feature Reviewer to WRITE Learnings

This is the critical loop-closing step. The Reviewer doesn't just read — it appends after every review.

Add a new section to the Feature Reviewer agent **after the "Write Review Record" section** and **before** the final return-to-orchestrator instructions:

```markdown
## Update Review Learnings

After writing the review record, check whether any issues found represent **recurring patterns** worth
capturing (not one-off bugs). If so, append a dated entry to `.github/learnings/review-learnings.md`
in the project repo. Follow the existing format: Pattern, Impact, Watch for.

Also check for **decisions that affect future phases** (deferred work, documented deviations, scope gaps).
If found, append them to `.github/learnings/cross-phase-decisions.md` under the appropriate section.
Follow the existing format and categorization.

Create either file if it doesn't exist.
```

---

## Part 4: Add Integration Feature Rule (prevents missing bootstrap)

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
