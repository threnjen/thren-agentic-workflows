---
name: engagement-preparation-runbook
description: "Repeatable runbook for preparing a client engagement for comparison analysis — declare an engagement configuration, invoke the preparation orchestrator, verify what a successful run produced per side, re-run safely (idempotent), and diagnose failures. Use when: starting preparation for any engagement, re-running preparation after changes or a partial failure, or verifying that a preparation run left every engagement repo's history untouched."
---

# Engagement Preparation Runbook

This runbook is the operating procedure for preparing an engagement's
repositories for comparison analysis. It is one procedure narrative with
pointers — the detailed rules live in the assets it references:

- **Config contract**: the `engagement-configuration` skill (schema,
  validation rules, canonical field vocabulary).
- **Orchestrator**: the **Client Deliverable - Prepare** agent — graph build,
  baseline snapshot, analysis-branch convention, fail-fast policy. It spawns no agents;
  documentation is produced later by the Client Deliverable orchestrator's
  evidence stage (`engagement-pair-loop` skill, Stage A).

Where behavior is described below, the referenced asset is the source of
truth.

## Security Boundary

Per the `engagement-workspace` skill's Security Boundary section.

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

Invoke the **Client Deliverable - Prepare** agent. It is a single
non-interactive invocation — there is no confirmation gate. Its preflights,
prepare order, and per-side outputs are defined in the agent definition.

## Step 4: What a Successful Run Produces, Per Side

Per the agent's Final Report section: a per-side row for every side of every
pair, and the three analysis-branch invariant assertions with their recorded
HEAD SHAs as evidence. Verify those SHAs independently in Step 5.

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

Re-running on a prepared engagement is safe — rules in the agent's
Idempotency section. A re-run after a partial failure regenerates the failed
side in full.

## Failure Modes and Resolution

The agent's Fail Fast section enumerates what stops a run and what it reports.
Your resolutions:

| Failure | Resolution |
|---------|------------|
| Config validation error | Fix the config; re-run |
| Dirty working tree in a branch-pair repo | Commit/stash/clean the repo; re-run |
| Graph build failure on a side | Diagnose the build error; re-run |
| Graph tooling unavailable (`code-review-graph` CLI not installed) — recorded **NOT RUN**, not a failure | Install the `code-review-graph` CLI; re-run |
