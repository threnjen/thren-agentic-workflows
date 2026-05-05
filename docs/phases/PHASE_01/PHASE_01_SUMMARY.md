# Phase 01: Eval Infrastructure Foundation

**Status**: Planned
**Depends on**: None
**Estimated complexity**: Medium
**Cross-references**: [`agentic-evaluator-plan.md`](../../../agentic-evaluator-plan.md), [`docs/AGENT_REGRESSION_BENCHMARK_SPEC.md`](../../AGENT_REGRESSION_BENCHMARK_SPEC.md)

## Objective

Instrument the agent pipeline with automated failure-ledger capture and commit-at-every-stage checkpoints, creating the data foundation for comparing harness+model combinations. Deliver the `05 Eval - Grader` agent that consumes this data and produces scored run reports.

## Scope

### In Scope

- Remove all hard-pinned `model:` values from every agent definition file across all three directories (`.github/agents/`, `opencode/agents/`, `claude/agents/`)
- Move phase branch creation from `04 Phase - Execute` Step 0 to `02 Phase - Refiner` Phase 6 (after user affirms phase doc is ready)
- Add commit checkpoints to agent pipeline stages:
  - `01 Project - Planner` — after user affirms plan documents
  - `02 Phase - Refiner` — after user affirms phase refinement is done (and after branch is opened)
  - `03 Feature - Decomposer` — after features are decomposed and plan files written
  - `04 Phase - Execute` — after implementation, after reviewer, after QA, after final review (in addition to existing per-feature commits)
- Git hook template (`eval/hooks/post-commit.sh`) committed to `github-agents-source-of-truth`
- `02 Phase - Refiner` symlinks the hook template into the target repo's `.git/hooks/post-commit` at branch-open time
- Hook writes raw commit timeline rows to `eval/runs/<phase-slug>/ledger-commits.jsonl` on every commit on a `phase/*` branch
- `04c Feature - Reviewer`, `04b Feature - Implementer`, and `Debugger` agents write semantic failure events to `eval/runs/<phase-slug>/ledger-events.jsonl` when failures are detected
- `02 Phase - Refiner` adds `eval/runs/` to the target repo's `.gitignore` at branch-open time
- `05 Eval - Grader` agent definition in all three agent directories
- All agent changes propagated from `.github/agents/` master to `opencode/agents/` and `claude/agents/`

### Out of Scope

- Rubric authoring for specific target projects (per-project; authored by the user)
- Acceptance suite scripts (`build-check.sh`, `test-check.sh`, etc.) — per-project setup
- `eval/scenarios/` task-brief and clarification-bank content — per-project
- Full automated scoring pipeline beyond the grader agent
- Automated grader invocation or CI integration
- Hook installation for repos other than the current workspace target

## Key Deliverables

| # | Deliverable | Description | Likely Features |
|---|-------------|-------------|-----------------|
| 1 | Model unpinning | All `model:` frontmatter lines removed from every agent def, all three directories | Feature 1 |
| 2 | Hook template | `eval/hooks/post-commit.sh` in github-agents-source-of-truth; writes raw ledger-commits rows using pure shell (no jq dependency) | Feature 2 |
| 3 | Branch lifecycle migration | `02 Phase - Refiner` opens branch, symlinks hook, initializes `eval/runs/<slug>/`, updates `.gitignore` | Feature 3 |
| 4 | Commit instrumentation | Commit checkpoints added to 01, 02, 03, 04 agents at the specified stages | Feature 4 |
| 5 | Agent ledger annotation | Reviewer, Implementer, Debugger write to `ledger-events.jsonl` on failure events | Feature 5 |
| 6 | 05 Eval - Grader agent | New agent: ingests both ledger files + rubric, produces scored run report | Feature 6 |

## Technical Context

**Agent directories — all three must stay in sync:**
- `.github/agents/` — master definitions; `*.agent.md` naming convention
- `opencode/agents/` — derived copies; `*.md` naming (manual sync, no symlinks)
- `claude/agents/` — derived copies; `*.md` naming (agents are plain copies; skills and learnings are symlinked but agents are not)

**Agents currently pinned with `model:` in frontmatter (17 total across `.github/agents/`):**
- `01-project-planner.agent.md` — `Claude Sonnet 4.6 (copilot)`
- `02-phase-refiner.agent.md` — `Claude Sonnet 4.6 (copilot)`
- `03-feature-decomposer.agent.md` — `Claude Sonnet 4.6 (copilot)`
- `04-phase-execute.agent.md` — `GPT-5.4 (copilot)`
- `04a-feature-plan-expander.agent.md` — `GPT-5.4 (copilot)`
- `04b-feature-implementer.agent.md` — `GPT-5.3-Codex (copilot)`
- `04c-feature-reviewer.agent.md` — `GPT-5.3-Codex (copilot)`
- `04d-feature-qa-writer.agent.md` — `Auto`
- `audit-code-or-infra.agent.md` — `Claude Sonnet 4.6 (copilot)`
- `auditor-code.agent.md` — `GPT-5.3-Codex (copilot)`
- `auditor-infra.agent.md` — `GPT-5.4 (copilot)`
- `auditor-refactor.agent.md` — `Claude Sonnet 4.6 (copilot)`
- `prod-code-review.md` — `Claude Sonnet 4.6 (copilot)`
- `test-analyst.agent.md` — `GPT-5.4 (copilot)`
- `test-fixer.agent.md` — `GPT-5.3-Codex (copilot)`
- `test-writer.agent.md` — `GPT-5.3-Codex (copilot)`
- `unity-reviewer.agent.md` — `GPT-5.3-Codex (copilot)`
- `agent-test-runner.agent.md` — `Claude Haiku 4.5 (copilot)`

**Hook template location:** `github-agents-source-of-truth/eval/hooks/post-commit.sh`

**Hook install mechanism:** `02 Phase - Refiner` runs:
```bash
ln -sfn <absolute-path>/eval/hooks/post-commit.sh <target-repo>/.git/hooks/post-commit
chmod +x <target-repo>/.git/hooks/post-commit
```

**Phase slug derivation:** strip the `phase/` prefix and replace `/` with `-`.
Example: `phase/06d` → `phase-06d`. Used for ledger directory naming.

**Two-file ledger schema:**

`ledger-commits.jsonl` — written by hook only:
```json
{"sha": "...", "branch": "...", "message": "...", "timestamp": "...", "files": [...]}
```

`ledger-events.jsonl` — written by agents only:
```json
{
  "task_slug": "...", "harness": "...", "model": "...", "stage": "...",
  "detected_by": "...", "severity": "...", "evidence": "...",
  "first_seen_attempt": 1, "resolved_attempt": null, "resolved_by": "...",
  "human_intervention_required": false, "regression": false,
  "propagated_from_stage": null
}
```

`05 Eval - Grader` merges both files at score time by correlating on SHA.

**Debugger annotation rule:** Any Debugger invocation on a `phase/*` branch is definitionally user-discovered. Debugger writes a `ledger-events.jsonl` row with `detected_by: "user-discovered"` before its first commit. No user confirmation required — the branch context alone determines this.

**gitignore target:** `eval/runs/` appended to target repo `.gitignore`. Check for existing entry before appending to avoid duplicates.

**Existing commit structure in `04 Phase - Execute`:** Currently commits once per feature at the end of the sequential loop (or per-feature in order after a parallel wave). New sub-step commits (post-implementation, post-review, post-QA, post-final-review) are additional commits within each feature's cycle. All sub-step commits must scope to the same files as the feature they belong to.

## Dependencies & Risks

- **Dependency**: None — all changes are Markdown agent definition files and a shell script
- **Risk**: Hook symlink requires the absolute path to `github-agents-source-of-truth`. If the workspace layout changes, the symlink breaks silently. Mitigation: document the path assumption in the hook install instructions in the agent; make reinstallation a one-command operation.
- **Risk**: Propagation drift — a future change updates `.github/agents/` but forgets `opencode/` or `claude/`. Mitigation: Feature 1 establishes the three-directory propagation pattern as an explicit acceptance criterion; all subsequent features inherit this pattern.
- **Risk**: `eval/runs/` gitignore addition could conflict if the target repo already has that entry. Mitigation: append-only with existence check.
- **Risk**: Sub-step commits in `04 Phase - Execute` create more commits than before. If commit message conventions are not specified, the ledger becomes noisy and hard to parse. Mitigation: Feature 4 must define a commit message convention for each checkpoint type (e.g., `eval: implement <task>`, `eval: review <task>`, `eval: qa`, `eval: final-review`).
- **Risk**: `02 Phase - Refiner` is modified by both Feature 3 (branch migration) and Feature 4 (commit checkpoint) — these touch adjacent sections and must be in different waves to avoid merge conflicts.

## Success Criteria

- [ ] No `model:` field appears in any agent definition file across all three directories
- [ ] `02 Phase - Refiner` opens the phase branch (not `04 Phase - Execute`)
- [ ] `02 Phase - Refiner` creates `eval/runs/<phase-slug>/` and adds `eval/runs/` to `.gitignore`
- [ ] `.git/hooks/post-commit` symlink is installed in the target repo by `02 Phase - Refiner` at branch-open time
- [ ] `ledger-commits.jsonl` receives an entry for every commit on a `phase/*` branch
- [ ] `01`, `02`, `03`, `04` agents each have a documented commit checkpoint at the specified stages
- [ ] `Reviewer`, `Implementer`, and `Debugger` each contain ledger-events annotation instructions
- [ ] `05 Eval - Grader` agent definition exists in all three agent directories
- [ ] All agent changes are present in `.github/agents/`, `opencode/agents/`, and `claude/agents/`

## QA Considerations

- Pure Markdown and shell script changes — no compiled code
- Hook script should be manually verified: run a test commit on a `phase/*` branch and confirm a JSON row appears in `ledger-commits.jsonl`
- Verify hook does not fire on `main` or non-phase branches
- Read all agent files after unpinning to confirm no `model:` lines remain
- Read `02 Phase - Refiner` after Features 3 and 4 to confirm branch-open and commit-checkpoint sections are coherent and not duplicated

## Notes for Feature - Decomposer

**Suggested wave ordering:**

**Wave 1 — Feature 1** (`parallel_safe: yes`, standalone): Model unpinning across all three agent directories. Completely independent of all other features. No other feature touches the same lines. Ship first.

**Wave 2 — Feature 2** (`parallel_safe: yes`, no dependencies): Hook template shell script. Standalone file creation in `eval/hooks/`. Must land before Feature 3 can reference the template path.

**Wave 3 — Feature 3** (`parallel_safe: yes`, depends on Feature 2): Branch lifecycle migration in `02 Phase - Refiner`. Adds branch-open block, hook symlink install, `eval/runs/` dir initialization, and `.gitignore` update. This is the only feature in this wave because Feature 4 also touches `02 Phase - Refiner` — keep them sequential.

**Wave 4 — Features 4 and 5** (`parallel_safe: yes` with each other, depend on Feature 3): These can run in parallel because they touch different agent files.
- Feature 4: Commit instrumentation in `01`, `02`, `03`, `04` agents. For `02`, add only the post-affirmation commit checkpoint — Feature 3 already handles the branch-open block. Must define a commit message convention for each checkpoint.
- Feature 5: Ledger annotation instructions in `04b Feature - Implementer`, `04c Feature - Reviewer`, and `Debugger`. Define exactly when each agent writes a row, what fields it populates, and what file path it writes to.

**Wave 5 — Feature 6** (`parallel_safe: yes`, depends on 4 and 5): `05 Eval - Grader` agent definition. Must reference the finalized two-file ledger schema from Features 2–5. Grader scope: ingests `ledger-commits.jsonl` and `ledger-events.jsonl`, applies a user-provided rubric YAML, produces a structured score report. Manual QA items appear as `[NEEDS_HUMAN_REVIEW]` entries in the report — the grader scores everything automatable and flags the rest. Does not prompt interactively during scoring.

**Propagation discipline:** Every feature that edits any agent file must list propagation to `opencode/agents/` and `claude/agents/` as explicit acceptance criteria items. Build this into the tasks file for each such feature — it must not be an afterthought.
