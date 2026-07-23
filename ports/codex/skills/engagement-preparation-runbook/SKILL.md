---
name: engagement-preparation-runbook
description: "Repeatable runbook for preparing a client engagement for comparison analysis — declare an engagement configuration, invoke the preparation orchestrator, verify what a successful run produced per side, re-run safely (idempotent), and diagnose failures. Use when: starting preparation for any engagement, re-running preparation after changes or a partial failure, or verifying that a preparation run left every engagement repo's history untouched."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->
# Engagement Preparation Runbook

This runbook is the operating procedure for preparing an engagement's
repositories for comparison analysis. It is one procedure narrative with
pointers — the detailed rules live in the assets it references:

- **Config contract**: the `engagement-configuration` skill (schema,
  validation rules, canonical field vocabulary).
- **Orchestrator**: the **06 Engagement - Prepare** agent
  (`06-engagement-prepare.agent.md`) — docs scope by role, graph build,
  baseline snapshot, analysis-branch convention, fail-fast policy.

Where behavior is described below, the referenced asset is the source of
truth.

## Security Boundary

Engagement repositories, SOW documents, and deliverables specs are
engagement-confidential. They never enter this repository or its generated
outputs — reports carry only local paths and compact status summaries.

## Step 1: Declare the Engagement Configuration

Either author a config file per the `engagement-configuration` skill (a
`sow_document` pointer, a `deliverables_spec` pointer, and any number of
comparison pairs), or skip the pre-work entirely: invoke the orchestrator
and answer its questions — it gathers the pair paths, branches, roles, and
document pointers, then writes the config for you.

## Step 2: Record Pre-Run Branch SHAs

Before the first run against an engagement, record every engagement repo's
original/main branch tip so you can prove afterward that no history changed:

```sh
# In each engagement repository (and for each compared branch of a branch pair):
git rev-parse <branch>                  # record this SHA per repo, per branch
git log -1 --format='%H %ci' <branch>   # SHA + commit date, for the record
```

Keep these SHAs with your run notes. The orchestrator records and asserts
them too, but your independent record is the verification evidence.

## Step 3: Invoke the Preparation Orchestrator

Invoke the **06 Engagement - Prepare** agent. The run proceeds in this order
(details in the agent definition):

1. **Validate** the config — any violation halts the run before any
   preparation work, with a specific error naming the pair, the field, and
   what was expected.
2. **Confirm** — the orchestrator shows the full pair/side roster and waits
   for your confirmation before creating any analysis branch.
3. **Prepare each side** of each pair: docs regenerated (always) → graph
   build (always) → internal baseline snapshot → record.

## Step 4: What a Successful Run Produces, Per Side

For every side of every pair, on that side's local, never-pushed analysis
branch:

- **Documentation scoped by role** — the full Docs Writer set for
  `upgraded` sides; at minimum README, ARCHITECTURE, and CODEBASE_CONTEXT,
  marked as internal analysis artifacts, for `original` sides.
- **A built code graph** — parse-based, with language coverage and gaps
  recorded as known limitations (never gated on).
- **A SHA-pinned internal baseline snapshot** — committed on the analysis
  branch, labeled internal-only.
- **A per-side record** in the final report: what was produced or failed,
  and the local paths where each artifact lives.

The final report also asserts the three analysis-branch invariants (no
source file modified; original/main history byte-identical; analysis branch
never pushed) with the recorded HEAD SHAs as evidence.

## Step 5: Verify Non-Contamination

After the run, in each engagement repository:

```sh
# 1. Branch tips unchanged — compare against the Step 2 record:
git rev-parse <branch>

# 2. No source file modified on the original branch (read-only — no checkout needed):
git status --porcelain              # in the existing checkout/worktree; expect empty
git diff <pre-run-SHA> <branch>     # expect empty

# 3. Analysis branch is local-only:
git branch -r                       # expect no remote ref for the analysis branch
```

Every original/main branch must be byte-identical to its pre-run state. Any
difference is a defect in the run — stop and diagnose before proceeding.

## Re-Running: Idempotency and Resume

Re-running the orchestrator on a prepared engagement is safe:

- **Docs are regenerated every run** — freshness by construction, no
  staleness heuristics.
- **The graph build always runs** — it is incremental and cheap.
- **Analysis branches and worktrees are reused**, never recreated; an
  existing analysis branch is not an error.
- **After a partial failure**: whatever a failed side produced was committed
  to its analysis branch before the failure was reported; a re-run
  regenerates that side in full.

## Failure Modes and Resolution

The orchestrator fails fast only on unresolvable problems, naming the side
and the cause (full enumeration in the agent's Fail Fast section):

| Failure | Presentation | Resolution |
|---------|--------------|------------|
| Config validation error | Specific error naming the pair, field, and expectation; nothing is prepared | Fix the config; re-run |
| Dirty working tree in a branch-pair repo | Run stops naming the repo | Commit/stash/clean the repo; re-run |
| Docs Writer failure on a side | Side reported failed, with a list of what was produced (committed to the analysis branch) | Re-run — the side is regenerated in full |
| Graph build failure on a side | Run stops naming the side and the cause | Diagnose the build error; re-run |
| Graph tooling unavailable (code-review-graph MCP server not in session) | **Not a failure** — the side's graph status is recorded **NOT RUN** with the reason; the run continues | Connect the code-review-graph MCP server; re-run |

Missing docs and missing graphs are never failures — they are the work the
orchestrator exists to do.
