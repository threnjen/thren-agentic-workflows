# 04 Ledger Annotation

## Execution Metadata

- **Wave:** 4
- **Parallel safe:** yes
- **Depends on:** 03-branch-lifecycle-migration
- **Key files modified:** `.github/agents/04b-feature-implementer.agent.md`, `.github/agents/04c-feature-reviewer.agent.md`, `.github/agents/debugger.agent.md`, and all copies in `opencode/agents/` and `claude/agents/`
- **Sequential reason:** n/a (parallel-safe with 04-commit-instrumentation; disjoint file sets)

> **Sibling plan note**: `04-commit-instrumentation` runs in the same wave. File sets are fully disjoint — this feature touches 04b, 04c, and debugger; commit-instrumentation touches 01, 02, 03, 04. Safe to run in parallel.

---

## A. Requirements & Traceability

### Acceptance Criteria

- **AC1**: `04c Feature - Reviewer` writes a `ledger-events.jsonl` row when it returns a "Changes Requested" verdict, with `detected_by: "reviewer"` and `stage: "review"`
- **AC2**: `04b Feature - Implementer` writes a `ledger-events.jsonl` row when it encounters a failing test or an unresolvable issue, with `detected_by: "implementer"` and `stage: "implement"`
- **AC3**: `Debugger` writes a `ledger-events.jsonl` row with `detected_by: "user-discovered"` before its first commit on any `phase/*` branch. No user confirmation needed — branch context determines the annotation.
- **AC4**: Each ledger row written by any agent populates all required fields: `task_slug`, `harness`, `model`, `stage`, `detected_by`, `severity`, `evidence`, `first_seen_attempt`, `resolved_attempt`, `resolved_by`, `human_intervention_required`, `regression`, `propagated_from_stage`
- **AC5**: The ledger file path for all agents is `eval/runs/<phase-slug>/ledger-events.jsonl` in the target repo
- **AC6**: Phase slug is derived by reading the current git branch, stripping `phase/`, and replacing `/` with `-`
- **AC7**: If the current branch is not a `phase/*` branch, agents skip ledger writing silently
- **AC8**: All changes propagated to copies in `opencode/agents/` and `claude/agents/`

### Non-Goals

- Does not add ledger writing to `04a Feature - Plan Expander` or `04d Feature - QA Writer`
- Does not write to `ledger-commits.jsonl` — that file is hook-written only
- Does not validate or parse existing ledger rows
- Does not change the agents' core logic — only adds the ledger write as an additional step

### Traceability

| AC | File | Verification |
|----|------|--------------|
| AC1 | `04c-feature-reviewer.agent.md` | Read file: ledger-write instruction present in "Changes Requested" path |
| AC2 | `04b-feature-implementer.agent.md` | Read file: ledger-write instruction present in failure/blocking path |
| AC3 | `debugger.agent.md` | Read file: ledger-write with user-discovered annotation before first commit on phase/* |
| AC4 | All three agent files | Full schema fields listed in each agent's ledger-write instruction |
| AC5 | All three agent files | File path `eval/runs/<phase-slug>/ledger-events.jsonl` specified |
| AC6 | All three agent files | Slug derivation instruction present |
| AC7 | All three agent files | Branch guard documented |
| AC8 | 6 copy files | Same sections present in all copies |

---

## B. Correctness & Edge Cases

### `ledger-events.jsonl` Schema (full)

Each row is a single JSON object on one line:

```json
{
  "task_slug": "04-ledger-annotation",
  "harness": "copilot",
  "model": "claude-sonnet-4-6",
  "stage": "review",
  "detected_by": "reviewer",
  "severity": "medium",
  "evidence": "AC3 not met: branch guard missing from annotation logic",
  "first_seen_attempt": 1,
  "resolved_attempt": null,
  "resolved_by": null,
  "human_intervention_required": false,
  "regression": false,
  "propagated_from_stage": null
}
```

### Field Derivation Instructions (per agent)

| Field | How Agent Derives It |
|-------|----------------------|
| `task_slug` | Current feature directory name (e.g., `04-ledger-annotation`) |
| `harness` | Agent notes the harness it is running in (copilot / opencode / claude-code / unknown) |
| `model` | Agent reads its own `name:` frontmatter context or leaves as `unknown` if not available |
| `stage` | Hard-coded per agent: `"review"` for Reviewer, `"implement"` for Implementer, `"debug"` for Debugger |
| `detected_by` | Hard-coded per agent: `"reviewer"`, `"implementer"`, `"user-discovered"` |
| `severity` | Agent's judgment: `"low"` / `"medium"` / `"high"` / `"blocking"` |
| `evidence` | Brief description of what failed or why human intervention was invoked |
| `first_seen_attempt` | Set to `1` for initial failure detection |
| `resolved_attempt` | `null` at time of writing; updated if/when the agent resolves the issue |
| `resolved_by` | `null` at initial write; set to `"implementer"` / `"reviewer"` / `"user"` if resolved |
| `human_intervention_required` | `false` by default; `true` for Debugger (user-discovered) |
| `regression` | `false` at initial detection; set to `true` if a previously passing acceptance criterion fails again |
| `propagated_from_stage` | `null` unless the failure was propagated from a prior stage |

### Agent-Specific Placement

**`04c Feature - Reviewer`**: Write the row immediately before returning "Changes Requested" to the orchestrator. If the verdict is "Approved" or "Approved with Reservations", do not write a row.

**`04b Feature - Implementer`**: Write the row when implementation cannot proceed due to failing tests or a blocking issue that requires human input. Write before suspending or returning a failure status. Do not write a row for routine Red-Green-Refactor iterations.

**`Debugger`**: Write the row as Step 1a (inserted between existing Step 1 — Triage — and the investigation steps). On a `phase/*` branch, before beginning any fixes, append the row. On a non-phase branch, skip silently.

### Edge Cases

- **`resolved_attempt` update**: The Reviewer and Implementer should update the row (by appending a new row with the same `task_slug` and `stage` but with `resolved_attempt` and `resolved_by` populated) when the issue is subsequently resolved. Appending a new row is safer than in-place editing JSONL.
- **Harness detection**: Agents cannot reliably know which harness is running them. Instruct them to write `"harness": "unknown"` unless context clearly indicates otherwise (e.g., VS Code Copilot vs CLI). This is acceptable — the grader can backfill from the run config.
- **Model detection**: Same challenge. Write `"model": "unknown"` unless the agent can read its own frontmatter model field from context.
- **`eval/runs/<slug>/` may not exist**: The directory is created by `02 Phase - Refiner` (Feature 3). On a phase branch, it should exist. If it doesn't, the agent must create it with `mkdir -p` before writing.
- **JSONL append**: All writes use `>>` (append), never overwrite.

---

## C. Consistency & Architecture Fit

### Existing Agent Structure

All three agents have numbered Steps. The ledger-write instruction fits cleanly as:
- In Reviewer: added to the "Changes Requested" return path (a conditional branch that already exists)
- In Implementer: added to the failure/blocking return path
- In Debugger: inserted as a new Step 1a before the investigation begins

### Two-File Design Rationale

`ledger-commits.jsonl` (hook-written) records the raw git timeline. `ledger-events.jsonl` (agent-written) records semantic failure events. The grader joins them on SHA. This feature only adds to the semantic side.

---

## D. Clean Design & Maintainability

- Each agent gets one small instruction block — not a restructuring
- The full schema is listed once in each agent's new block — no cross-references
- Agents are told to use `>>` append and `mkdir -p` — not to implement complex error recovery

### Keep-It-Clean Checklist

- [ ] Reviewer annotation only on "Changes Requested" — not on other verdicts
- [ ] Implementer annotation only on blocking failures — not on routine TDD cycles
- [ ] Debugger annotation precedes all fixes, regardless of failure type
- [ ] All three agents include the branch guard (`phase/*` only)
- [ ] All three agents include `mkdir -p` guard before first write
- [ ] All six copy files updated

---

## E. Completeness: Observability, Security, Operability

**Observability**: `ledger-events.jsonl` is the semantic layer that `05 Eval - Grader` uses to score failures and interventions. Without this feature, the grader only has raw commit timestamps — no semantic context.

**Security**: No credentials. Ledger files are `.gitignore`'d by Feature 3. Local only.

**Operability**: Appending JSONL is idempotent from a data integrity standpoint. Multiple rows for the same task/stage are valid — the grader deduplicates by `first_seen_attempt`.

---

## F. Test Plan

No automated tests — Markdown agent definition changes.

### MV1 (AC1): Reviewer annotation

Read `.github/agents/04c-feature-reviewer.agent.md`. Confirm: a `ledger-events.jsonl` write instruction exists in the "Changes Requested" decision path. Confirm full schema fields are listed.

### MV2 (AC2): Implementer annotation

Read `.github/agents/04b-feature-implementer.agent.md`. Confirm: a `ledger-events.jsonl` write instruction exists in the blocking/failure path. Confirm it is NOT in the routine iteration path.

### MV3 (AC3): Debugger user-discovered annotation

Read `.github/agents/debugger.agent.md`. Confirm: Step 1a (or equivalent) exists with `detected_by: "user-discovered"` and precedes all fix steps. Confirm branch guard present.

### MV4 (AC4, AC5, AC6, AC7): Schema completeness and guards

In each of the three master files, confirm: all 13 schema fields listed, file path `eval/runs/<phase-slug>/ledger-events.jsonl` specified, slug derivation instruction present, non-phase branch guard present.

### MV5 (AC8): Propagation

Read all six copy files. Confirm the same ledger-write sections are present.

---

## Stage 1: Add ledger annotation to `04c Feature - Reviewer`

**Goal**: Add the `ledger-events.jsonl` write instruction to the "Changes Requested" return path in `.github/agents/04c-feature-reviewer.agent.md`.
**Success Criteria**: MV1 passes.
**Status**: Not Started

## Stage 2: Add ledger annotation to `04b Feature - Implementer`

**Goal**: Add the `ledger-events.jsonl` write instruction to the blocking-failure path in `.github/agents/04b-feature-implementer.agent.md`.
**Success Criteria**: MV2 passes.
**Status**: Not Started

## Stage 3: Add user-discovered annotation to `Debugger`

**Goal**: Add Step 1a with `detected_by: "user-discovered"` to `.github/agents/debugger.agent.md`, before all fix steps, with branch guard.
**Success Criteria**: MV3 passes.
**Status**: Not Started

## Stage 4: Verify schema completeness across all three master files

**Goal**: Read each modified master file and confirm AC4–AC7 for each.
**Success Criteria**: MV4 passes for all three files.
**Status**: Not Started

## Stage 5: Propagate to all copy files

**Goal**: Apply identical changes to all six copy files across `opencode/agents/` and `claude/agents/`.
**Success Criteria**: MV5 passes.
**Status**: Not Started
