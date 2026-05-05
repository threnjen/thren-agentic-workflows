# 05 Eval Grader Agent

## Execution Metadata

- **Wave:** 5
- **Parallel safe:** yes
- **Depends on:** 04-commit-instrumentation, 04-ledger-annotation
- **Key files modified:** `.github/agents/05-eval-grader.agent.md` (new), `opencode/agents/05-eval-grader.md` (new), `claude/agents/05-eval-grader.md` (new)
- **Sequential reason:** n/a

---

## A. Requirements & Traceability

### Acceptance Criteria

- **AC1**: `05 Eval - Grader` agent definition exists in all three agent directories: `.github/agents/05-eval-grader.agent.md`, `opencode/agents/05-eval-grader.md`, `claude/agents/05-eval-grader.md`
- **AC2**: Agent ingests both `eval/runs/<phase-slug>/ledger-commits.jsonl` and `eval/runs/<phase-slug>/ledger-events.jsonl` as its primary data sources
- **AC3**: Agent accepts a user-provided rubric YAML file (path specified by the user at invocation time)
- **AC4**: Agent produces a structured score report covering all automatable criteria
- **AC5**: Manual QA items (flagged as `human_intervention_required: true` or with no automatable check) appear as `[NEEDS_HUMAN_REVIEW]` entries in the report
- **AC6**: Agent does not prompt interactively during scoring — it completes the full scoring run and outputs the report without pausing for user input
- **AC7**: Agent correlates rows from `ledger-commits.jsonl` and `ledger-events.jsonl` by commit SHA to produce a unified timeline showing: what was committed, what events were detected, when
- **AC8**: Score report is written to `eval/runs/<phase-slug>/score-report-<timestamp>.md` in the target repo
- **AC9**: Score report structure includes: run metadata, per-feature summary table, failure breakdown, human intervention count, regression flags, and overall pass/fail verdict

### Non-Goals

- Does not author or validate the rubric — that is a per-project artifact the user provides
- Does not invoke other agents or trigger CI — scoring is a standalone read-and-analyze operation
- Does not modify `ledger-commits.jsonl` or `ledger-events.jsonl`
- No automated grader invocation — user invokes manually at the end of a phase
- No scoring of commits on non-phase branches

### Traceability

| AC | Code Area | Verification |
|----|-----------|--------------|
| AC1 | 3 new agent files | `ls .github/agents/05-eval-grader.agent.md opencode/agents/05-eval-grader.md claude/agents/05-eval-grader.md` |
| AC2 | Agent body: "Required Inputs" section | Read file: both ledger files listed as inputs |
| AC3 | Agent body: rubric intake step | Read file: rubric YAML path intake described |
| AC4 | Agent body: scoring procedure | Read file: scoring logic for automatable criteria described |
| AC5 | Agent body: NEEDS_HUMAN_REVIEW handling | Read file: flag format defined for manual items |
| AC6 | Agent body: no interactive prompts | Read file: no "ask user" instructions mid-scoring |
| AC7 | Agent body: SHA correlation step | Read file: correlation procedure described |
| AC8 | Agent body: output step | Read file: `score-report-<timestamp>.md` path specified |
| AC9 | Agent body: report structure section | Read file: all nine report sections defined |

---

## B. Correctness & Edge Cases

### Rubric YAML Format

The agent must document the expected rubric schema. Proposed minimal format:

```yaml
phase: phase-06d
harness: copilot
model: claude-sonnet-4-6
criteria:
  - id: C01
    description: "No model: field in any agent file"
    automatable: true
    check: "grep -r '^model:' .github/agents/ opencode/agents/ claude/agents/ returns no output"
  - id: C02
    description: "ledger-commits.jsonl has a row for every eval: prefixed commit"
    automatable: true
    check: "count eval: commit messages in ledger equals expected count"
  - id: C03
    description: "Manual review: reviewer verdict matches expected outcome"
    automatable: false
    requires_human: true
```

The agent reads this file, applies automatable checks where possible, and flags `requires_human: true` items as `[NEEDS_HUMAN_REVIEW]`.

### Score Report Structure (AC9)

```markdown
# Eval Score Report — phase-06d

**Generated**: 2026-05-04T15:00:00Z
**Harness**: copilot
**Model**: claude-sonnet-4-6
**Ledger commits**: 12 rows
**Ledger events**: 3 rows

## Per-Feature Summary

| Feature | Criteria Met | Criteria Failed | Human Review Required | Verdict |
|---------|-------------|-----------------|----------------------|---------|
| 01-model-unpinning | 4/4 | 0 | 0 | PASS |
| 02-hook-template | 3/5 | 1 | 1 | NEEDS_REVIEW |
| ... | | | | |

## Failure Breakdown

[List each failed criterion with evidence from ledger-events.jsonl]

## [NEEDS_HUMAN_REVIEW] Items

[List each manual QA item from rubric]

## Regression Flags

[List any ledger-events rows where regression: true]

## Summary

- Total criteria: N
- Automatable pass: X
- Automatable fail: Y
- Human review required: Z
- **Overall verdict**: PASS | FAIL | PARTIAL
```

### SHA Correlation Procedure

1. Load all rows from `ledger-commits.jsonl` into a timeline keyed by `sha`
2. Load all rows from `ledger-events.jsonl`
3. For each ledger-events row, find the nearest preceding SHA in the commit timeline (matching by `task_slug` when possible)
4. Build a unified timeline: `[commit-sha] [message] → [event: detected_by / severity / evidence]`
5. Use this timeline for the per-feature summary

### Edge Cases

- **Missing ledger files**: If either ledger file doesn't exist, the agent must note this in the report rather than failing silently. A missing `ledger-commits.jsonl` means the hook wasn't installed; a missing `ledger-events.jsonl` means no semantic failures were recorded.
- **Empty ledger files**: Valid state. Zero rows means no failures detected.
- **Rubric file not provided**: Agent should abort with a clear instruction: "Please provide the path to your rubric YAML file."
- **Unknown harness/model in ledger rows**: `"unknown"` values are valid; report them as-is
- **Multiple score reports**: Report filename includes timestamp (`score-report-20260504-150000.md`) to avoid overwriting previous runs

---

## C. Consistency & Architecture Fit

### Agent Naming and File Convention

- `.github/agents/` uses `*.agent.md` naming: `05-eval-grader.agent.md`
- `opencode/agents/` uses `*.md` naming: `05-eval-grader.md`
- `claude/agents/` uses `*.md` naming: `05-eval-grader.md`

### Frontmatter Template

```yaml
---
name: 05 Eval - Grader
description: "Scores a completed phase run by ingesting ledger-commits.jsonl and ledger-events.jsonl against a user-provided rubric YAML. Produces a structured score report. Does not prompt interactively during scoring."
tools: [read, search, edit]
---
```

No `model:` field — this is consistent with the output of Feature 1 (model unpinning).

### Tool Requirements

The grader only needs `read` (to load ledger files and rubric), `search` (to run automatable grep-style checks), and `edit` (to write the score report). No `execute` or `agent` tools needed.

---

## D. Clean Design & Maintainability

- Single agent definition, ~150–200 lines
- Scoring procedure is sequential: intake → read ledgers → read rubric → correlate → score automatable → flag manual → write report
- No sub-agents invoked
- Report format is Markdown — readable by humans and parseable by future tooling

### Keep-It-Clean Checklist

- [ ] No interactive prompts mid-scoring (AC6)
- [ ] Report written to file — not only printed to stdout
- [ ] `[NEEDS_HUMAN_REVIEW]` is a consistent literal string used as a marker
- [ ] Rubric-not-found case handled with clear abort message
- [ ] Missing ledger file case noted in report, not a hard failure
- [ ] All three agent copies are identical in body content (only filename differs)

---

## E. Completeness: Observability, Security, Operability

**Output**: `score-report-<timestamp>.md` in `eval/runs/<phase-slug>/`. This is the primary human-readable artifact for comparing harness+model runs.

**Security**: Reads local files only. No network calls. No credentials.

**Operability**: Report is self-contained — a reader with no prior context can understand the scoring from the report alone. Each `[NEEDS_HUMAN_REVIEW]` item includes the criterion description and what check would be needed.

**Future**: The two-file ledger design means a future automated grader could replace the agent entirely, consuming the same JSONL schema. The agent is the v1 implementation; the schema is the durable contract.

---

## F. Test Plan

No automated tests — this is a new agent definition file (Markdown).

### MV1 (AC1): Files exist in all three directories

```sh
ls .github/agents/05-eval-grader.agent.md
ls opencode/agents/05-eval-grader.md
ls claude/agents/05-eval-grader.md
```
All three must exist.

### MV2 (AC2, AC3): Inputs documented

Read `.github/agents/05-eval-grader.agent.md`. Confirm: both ledger files and rubric YAML are listed as required inputs in a "Required Inputs" section.

### MV3 (AC4, AC5): Scoring and human-review handling

In the same file, confirm: scoring procedure for automatable criteria is described, and `[NEEDS_HUMAN_REVIEW]` marker format is defined for manual items.

### MV4 (AC6): No interactive prompts

Read the agent body. Confirm: no instructions to "ask the user" or "wait for confirmation" appear between the scoring start and the report write.

### MV5 (AC7, AC8, AC9): Correlation and report structure

Confirm: SHA correlation step described, output path `eval/runs/<phase-slug>/score-report-<timestamp>.md` specified, and all nine report sections listed.

### MV6 (AC1, body parity): Copy files match

Read `opencode/agents/05-eval-grader.md` and `claude/agents/05-eval-grader.md`. Confirm body content is identical to the master file.

---

## Stage 1: Write master agent definition

**Goal**: Create `.github/agents/05-eval-grader.agent.md` with the full agent body: frontmatter, required inputs, SHA correlation procedure, rubric intake, scoring logic, `[NEEDS_HUMAN_REVIEW]` handling, and score report write step.
**Success Criteria**: MV2–MV5 pass on the master file.
**Status**: Not Started

## Stage 2: Propagate to `opencode/agents/` and `claude/agents/`

**Goal**: Create `opencode/agents/05-eval-grader.md` and `claude/agents/05-eval-grader.md` with identical body content.
**Success Criteria**: MV1 and MV6 pass.
**Status**: Not Started
