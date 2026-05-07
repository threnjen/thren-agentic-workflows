# Agentic Evaluator — Project Plan

## What We Are Going To Do

Build a lightweight evaluation framework that lets you benchmark different harness+model combinations (Claude Code, GitHub Copilot, OpenCode, Codex, etc.) against your existing 4-agent workflow. The goal is not a universal benchmark — it is a personal one: **which combination performs best on your projects, in your workflow, with your agent definitions.**

The evaluator is not a new agent. It is a harness that sits outside your existing repo, runs a test subject through a controlled task, captures everything that happened, and scores it.

---

## What Problem It Is Solving

You have a high number of viable harness+model combinations and no objective way to compare them. Right now, your only signal is vibes — does this feel better than that? The evaluator gives you a repeatable, scored comparison so you can make a data-driven choice and revisit it as models improve.

Secondary problem: your workflow involves multiple agents with handoffs, and failures can propagate silently across stages. You need a way to track not just whether something failed, but where it first went wrong and how expensive recovery was.

---

## How It Will Work — Overview

### Two Evaluation Modes

**Planning Eval**
- Starts from a task brief (no existing code)
- Runs agents 01 and 02 (Planner → Refiner)
- Scores the resulting phase document against a rubric

**Execution Eval**
- Starts from a frozen, known-good phase document (your gold input)
- Runs agent 04 (Phase Execute)
- Scores implementation artifacts, test results, and recovery behavior

These can be run independently or chained. If chained, you get a third signal: **plan-to-execution coherence** — did the subject actually follow its own plan?

### What Gets Captured Per Run

- All artifacts written to `develop/` (phase docs, context, tasks, implementation, review, QA, docs)
- Git diff and commit log from baseline to final state
- Build/lint/test results
- A failure ledger (see below)
- Total turn count and human interventions required

### The Grader

- A fixed model, not one of the test subjects (Claude Opus or GPT-4o recommended)
- Uses the same rubric every run
- Never sees which harness produced the output — strip harness identifiers before grading
- Scores structure and coherence automatically; you score correctness and fit manually (small burden, clearly separated)

---

## Setting Up an Evaluator for a Given Project

### Step 1: Pick a Real, Completed Task as Your Gold Standard

Do not invent synthetic tasks. Use something you have already shipped.

Requirements for a good gold task:
- Has deterministic pass/fail checks (builds, tests pass, lint clean)
- Has a corresponding branch you can reset to before your work started
- Is scoped to a single feature or a small, bounded phase — not a full project
- Has artifacts you produced yourself (phase doc, implementation, QA doc)

### Step 2: Establish the Gold Package

From your completed task, extract and freeze:

```
eval/
  scenarios/
    <task-slug>/
      baseline-commit.txt       # SHA of the commit before your work started
      task-brief.md             # What the agent will be told to do
      clarification-bank.md     # Pre-written answers to likely plan questions
      gold-commit.txt           # SHA of your final, human-validated state
      acceptance-suite/
        build-check.sh          # Does it build?
        lint-check.sh           # Does lint pass?
        test-check.sh           # Do tests pass?
        manual-qa-checklist.md  # What you verified by hand
      rubric.md                 # Scoring criteria (see Scoring section)
      reference-artifacts/      # Your own plan/QA docs — for rubric calibration only
        phase-doc.md
        qa-doc.md
```

The reference artifacts are **not** used as the answer key. They are used to calibrate the grader on what "good" looks like. The test subject is allowed to reach correctness by a different path.

### Step 3: Establish the Baseline Branch

```bash
git checkout <baseline-commit-sha>
git checkout -b eval/<task-slug>/baseline
```

This is the starting state for every test subject. Each subject gets a fresh branch from here.

### Step 4: Run a Test Subject

For each harness+model combination:

```bash
# Create a fresh branch for this subject
git checkout eval/<task-slug>/baseline
git checkout -b eval/<task-slug>/<harness>-<model>

# Run the subject with the task brief
# (how you invoke this depends on the harness)
# ...

# After the run completes, collect artifacts
cp -r develop/ eval/runs/<task-slug>/<harness>-<model>/artifacts/
git diff eval/<task-slug>/baseline > eval/runs/<task-slug>/<harness>-<model>/diff.patch
git log eval/<task-slug>/baseline..HEAD > eval/runs/<task-slug>/<harness>-<model>/commits.txt
```

### Step 5: Run Deterministic Validators

```bash
cd eval/runs/<task-slug>/<harness>-<model>/
bash ../../scenarios/<task-slug>/acceptance-suite/build-check.sh
bash ../../scenarios/<task-slug>/acceptance-suite/lint-check.sh
bash ../../scenarios/<task-slug>/acceptance-suite/test-check.sh
```

Record pass/fail for each. Any unresolved blocker is a hard cap on the total score.

### Step 6: Run the Semantic Grader

Send the following to your fixed grader model with the rubric attached:
- The phase document produced (planning eval) or implementation artifacts (execution eval)
- The rubric
- The reference artifacts (for calibration context only — tell the grader these are examples, not the answer)
- Instruction to strip any harness/model identifiers before grading

### Step 7: Score the Failure Ledger

Review the failure ledger (see below) and score recovery quality manually. This is the part only you can do — it requires judgment about whether a recovery path was reasonable or expensive.

---

## Scoring Rubric

| Category | Weight | What It Measures |
|----------|--------|-----------------|
| Correctness & passing validations | 40 | Build, lint, tests, acceptance checks |
| Planning & decomposition quality | 20 | Coverage, dependency ordering, unknowns identified, validation strategy |
| Review & self-detection quality | 15 | Did the subject catch its own mistakes before you did? |
| Recovery quality | 15 | How cleanly did it recover from failures? |
| Efficiency cost | 10 | Turns, retries, human interventions required |

**Hard cap:** Any unresolved blocker failure caps the total score regardless of other categories.

### Planning Scoring Criteria

A good phase document covers:
- Objective
- Assumptions made
- Open questions (and whether the clarification bank answered them)
- Scope / non-scope boundary
- Phased breakdown
- Risks identified
- Validation strategy
- Handoff criteria

You score on: coverage of required work, dependency ordering, identification of unknowns, quality of questions asked, whether the proposed validation would actually catch the likely failures.

You do **not** score on whether the plan matches your reference plan exactly. You score on whether the plan was sufficiently complete and operational.

---

## Do You Need New Agents?

**No new agents for the test subjects.** Your existing 01/02/04 workflow runs as-is.

**Possibly one new utility:** a `05 Eval - Grader` agent that takes a run's artifacts + rubric and produces a structured score. This is optional — you can run the grader manually with a prompt. Whether to formalize it as an agent depends on how often you run evals.

What you do **not** want: an LLM orchestrating the test subjects during a run. The runner that launches the subject and captures output should be deterministic (a shell script or Python script), not another agent. Adding an LLM runner introduces variance that contaminates your results.

---

## Capturing the Failure Ledger

### Schema

Every failure event gets one record:

```json
{
  "task_slug": "feature-xyz",
  "harness": "claude-code",
  "model": "claude-opus-4-7",
  "stage": "implementation",
  "detected_by": "reviewer-agent",
  "severity": "blocker",
  "evidence": "path/to/log or description",
  "first_seen_attempt": 2,
  "resolved_attempt": 4,
  "resolved_by": "self",
  "human_intervention_required": false,
  "regression": false,
  "propagated_from_stage": null
}
```

The `propagated_from_stage` field is important: if an implementation failure traces back to a bad context document, that failure originated in the Plan Expander stage, not the Implementer. Without this, you'll misattribute failures.

### How to Capture It

**Option A: Git commit hook (recommended for automation)**

Add a `post-commit` hook to the eval branches that logs to a JSONL file:

```bash
# .git/hooks/post-commit
#!/bin/bash
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ $BRANCH == eval/* ]]; then
  COMMIT_MSG=$(git log -1 --pretty=%B)
  TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  SHA=$(git rev-parse HEAD)
  echo "{\"sha\": \"$SHA\", \"branch\": \"$BRANCH\", \"message\": \"$COMMIT_MSG\", \"timestamp\": \"$TIMESTAMP\", \"files\": $(git diff-tree --no-commit-id -r --name-only HEAD | jq -R . | jq -s .)}" >> eval/runs/commit-log.jsonl
fi
```

This gives you a raw commit log. You then annotate it post-run with failure events — the commit log tells you when things happened, and you fill in the `why`.

**Option B: Manual ledger during run (lower setup cost)**

Keep a `failures.jsonl` file open during each run. Every time you observe a failure (compile error, test failure, review rejection, manual QA finding), add a record. This is less automated but requires no hook setup.

**Option C: Hybrid (practical recommendation)**

Use the commit hook for the raw timeline, and add a post-run annotation step where you review the commit log and tag any commits that represent a failure or recovery. This keeps the hook simple and puts human judgment where it belongs.

---

## Edge Cases to Watch For

### Harness-specific behavior
Some harnesses will behave differently with the same agent definitions — they have different context windows, different tool call limits, different ways of handling long outputs. A failure that looks like a model failure may actually be a harness constraint. Log the harness version alongside the model.

### Non-determinism across runs
LLMs are not deterministic. A single run is not a valid data point. Plan for at least 3 runs per subject per task before drawing conclusions. Track variance, not just mean score.

### Plan-to-execution drift
If you chain the planning and execution evals, the execution subject may receive a plan that was produced by a different subject (or a weaker one). Decide upfront whether execution subjects always get your gold phase doc, or whether they get the plan produced by the same subject. Both are valid experiments — they just measure different things.

### Clarification bank gaps
Your clarification bank will not anticipate every question a subject asks. Decide in advance: unanticipated questions get no answer, or get a generic "use your best judgment" response. Apply the same rule to all subjects. Do not answer questions selectively.

### Silent propagation
A failure in Feature - Plan Expander (bad context doc) may not surface until the Implementer produces broken code. Review commit history carefully for cases where the first visible failure was actually caused upstream. This is why `propagated_from_stage` matters.

### Manual QA variability
Your manual QA findings will vary based on how thorough you are on a given day. Write your manual QA checklist before you run any subjects, and check against it consistently. Do not add checklist items mid-evaluation.

### Scope creep in the gold task
If you pick a task that is too large, the acceptance suite becomes unwieldy and the run takes too long. Start with the smallest task that has meaningful deterministic checks. A single well-scoped feature is better than a full phase for v1.

### Grader drift
If you use an LLM grader across many runs over many weeks, the model may be updated between runs. Pin the grader model version. If the grader model changes, re-grade your reference runs to ensure score comparability.
