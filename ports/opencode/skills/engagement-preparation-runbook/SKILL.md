---
name: engagement-preparation-runbook
description: "Repeatable runbook for preparing a client engagement for comparison analysis — author an engagement configuration file, invoke the Client Deliverable orchestrator with it, verify what a successful run produced per side, re-run safely (idempotent), and diagnose failures. Use when: starting preparation for any engagement, re-running preparation after changes or a partial failure, or verifying that a preparation run left every engagement repo's history untouched."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->

# Engagement Preparation Runbook

This runbook describes how to prepare an engagement's repositories for
comparison analysis. It provides one procedure with pointers. The referenced
assets contain the detailed rules:

- **Config contract**: the `engagement-configuration` skill (schema,
  validation rules, canonical field vocabulary).
- **Entry point**: the **Client Deliverable** agent. It is the only
  user-invocable agent in the fleet. It validates the config, scaffolds the
  workspace, then spawns its preparation stage (Run Flow steps 1–2 of its
  definition).
- **Preparation stage**: the **Client Deliverable - Prepare** agent. It covers
  the QA gate and QA appendix, analysis-branch convention, graph build, baseline
  snapshot, fail-fast policy, idempotency, and final report. The root
  orchestrator spawns it. Do not invoke it directly. It spawns no agents. The
  evidence stage later produces documentation (`engagement-pair-loop` skill,
  Stage A).

Where this runbook describes behavior, use the referenced asset as the source
of truth.

## Security Boundary

Follow the `engagement-workspace` skill's Security Boundary section.

## Step 1: Declare the Engagement Configuration

Preparation uses the config file. It has no interactive Q&A.

**Starting fresh?** Invoke the **Client Deliverable** agent with no config.
It asks for an engagement name, creates the workspace, and leaves an
`engagement.yaml` with blank fields at its root. It tells you the path. Fill in
every `FILL ME`. Then continue at Step 2.

**Already have a config?** Any path works. Relative paths inside it resolve
against its own directory. Use the `engagement-configuration` skill as the
schema and validation reference.

The config is the run's single declaration. It makes the run repeatable.
Re-invoking the same config produces the same preparation.

## Step 2: Record Pre-Run Branch SHAs

Before the first run for an engagement, record each engagement repo's
original/main branch tip. Use those tips later to prove that no history changed:

```sh
# In each engagement repository (and for each compared branch of a branch pair):
git rev-parse <branch>                  # record this SHA per repo, per branch
git log -1 --format='%H %ci' <branch>   # SHA + commit date, for the record
```

Keep these SHAs with your run notes. The preparation stage also records and
asserts them. Your independent record provides verification evidence.

## Step 3: Invoke the Client Deliverable Orchestrator

Invoke the **Client Deliverable** agent with the config path from Step 1. This
single invocation is non-interactive. It includes no Q&A or confirmation gate.

Per its Run Flow, the orchestrator validates the config against the
`engagement-configuration` skill's Validation Rules. Any violation halts the
run before preparation starts. It scaffolds the engagement workspace per the
`engagement-workspace` skill. It records the resolved inputs in
`engagement-state.md`. It then spawns **Client Deliverable - Prepare** with
that validated config. Validation occurs before the spawn, so the preparation
stage never asks questions. It receives a config it can trust. Its agent
definition specifies its preflights, prepare order, and per-side outputs.

For preparation only, stop after reading the preparation results in Step 4.
The orchestrator's later analysis stages are outside this runbook's scope.

## Step 4: What a Successful Run Produces, Per Side

The preparation stage's Final Report section lists one row per side of every
pair. Each row includes analysis-branch status, graph status, baseline snapshot
path, QA package paths, QA-gate status, and the `deliverables/qa-appendix.md`
pointer. It also includes the three analysis-branch invariant assertions and
their recorded HEAD SHAs as evidence. The orchestrator relays that report. It
records the same per-side status and pointers in the workspace's
`engagement-state.md`. Read that file to verify each side afterward. Verify
the SHAs independently in Step 5.

## Step 5: Verify Non-Contamination

After the run, perform these checks in each engagement repository:

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
difference is a defect in the run. Stop and diagnose before proceeding.

## Re-Running: Idempotency and Resume

Re-run the same way: invoke **Client Deliverable** again with the same config
file. Re-running on a prepared engagement is safe. The preparation stage's
Idempotency section defines these rules: graph builds are incremental,
snapshots re-emit identically, and analysis branches and worktrees are reused.
The orchestrator resumes from `engagement-state.md`. It repeats only sides
that the state does not mark complete. After a partial failure, a re-run
regenerates the failed side in full. The config file drives the entire run. A
re-run therefore does not depend on remembering what you typed the first time.

## Failure Modes and Resolution

The preparation stage's Fail Fast section lists what stops a run and what it
reports. Use these resolutions:

| Failure | Resolution |
|---------|------------|
| Config validation error | Fix the config. Then re-run. |
| Dirty working tree in a branch-pair repo | Commit, stash, or clean the repo. Then re-run. |
| Graph build failure on a side | Diagnose the build error. Then re-run. |
| Graph tooling unavailable (`code-review-graph` CLI not installed) — recorded **NOT RUN**, not a failure | Install the `code-review-graph` CLI. Then re-run. |
