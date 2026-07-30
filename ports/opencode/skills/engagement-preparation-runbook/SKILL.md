---
name: engagement-preparation-runbook
description: "Repeatable runbook for preparing a client engagement for comparison analysis — author an engagement configuration file, invoke the Client Deliverable orchestrator with it, verify what a successful run produced per side, re-run safely (idempotent), and diagnose failures. Use when: starting preparation for any engagement, re-running preparation after changes or a partial failure, or verifying that a preparation run left every engagement repo's history untouched."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->

# Engagement Preparation Runbook

This runbook is the operating procedure for preparing an engagement's
repositories for comparison analysis. It is one procedure narrative with
pointers — the detailed rules live in the assets it references:

- **Config contract**: the `engagement-configuration` skill (schema,
  validation rules, canonical field vocabulary).
- **Entry point**: the **Client Deliverable** agent — the only user-invocable
  agent in the fleet. It validates the config, scaffolds the workspace, then
  spawns its preparation stage (Run Flow steps 1–2 of its definition).
- **Preparation stage**: the **Client Deliverable - Prepare** agent — QA gate
  and QA appendix, analysis-branch convention, graph build, baseline snapshot,
  fail-fast policy, idempotency, final report. It is spawned by the root
  orchestrator, never invoked directly. It spawns no agents; documentation is
  produced later by the evidence stage (`engagement-pair-loop` skill, Stage A).

Where behavior is described below, the referenced asset is the source of
truth.

## Security Boundary

Per the `engagement-workspace` skill's Security Boundary section.

## Step 1: Declare the Engagement Configuration

Preparation is config-file-driven; there is no interactive Q&A. Author the
config file per the `engagement-configuration` skill before invoking
anything: a `sow_document` pointer, a `deliverables_spec` pointer, and any
number of comparison pairs (each with `name`, `type`, `original`,
`upgraded`, and — for branch pairs — `repo_path`). By convention it is
`engagement.yaml` at the root of the engagement's working directory; any
path works, and relative paths inside it resolve against its own directory.

The config is the single declaration of the run, which is what makes the run
repeatable: the same config re-invoked produces the same preparation.

## Step 2: Record Pre-Run Branch SHAs

Before the first run against an engagement, record every engagement repo's
original/main branch tip so you can prove afterward that no history changed:

```sh
# In each engagement repository (and for each compared branch of a branch pair):
git rev-parse <branch>                  # record this SHA per repo, per branch
git log -1 --format='%H %ci' <branch>   # SHA + commit date, for the record
```

Keep these SHAs with your run notes. The preparation stage records and
asserts them too, but your independent record is the verification evidence.

## Step 3: Invoke the Client Deliverable Orchestrator

Invoke the **Client Deliverable** agent and give it the path to the config
file from Step 1. That is the whole interaction — a single non-interactive
invocation, with no Q&A and no confirmation gate.

The orchestrator then, per its Run Flow: validates the config against the
`engagement-configuration` skill's Validation Rules (any violation halts the
run before anything is prepared), scaffolds the engagement workspace per the
`engagement-workspace` skill, records the resolved inputs in
`engagement-state.md`, and spawns **Client Deliverable - Prepare** with that
validated config. Because validation happens before the spawn, the
preparation stage never asks you anything — it receives a config it can
trust. Its preflights, prepare order, and per-side outputs are defined in
its agent definition.

If you want preparation only, stop after reading the preparation results
(Step 4) — the orchestrator's later analysis stages are out of this
runbook's scope.

## Step 4: What a Successful Run Produces, Per Side

Per the preparation stage's Final Report section: a per-side row for every
side of every pair (analysis-branch status, graph status, baseline snapshot
path, QA package paths and QA-gate status, the `deliverables/qa-appendix.md`
pointer), and the three analysis-branch invariant assertions with their
recorded HEAD SHAs as evidence. The orchestrator relays that report and
records the same per-side status and pointers in the workspace's
`engagement-state.md` — read that file to verify per side after the fact.
Verify the SHAs independently in Step 5.

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

Re-run the same way: invoke **Client Deliverable** again with the same
config file. Re-running on a prepared engagement is safe — rules in the
preparation stage's Idempotency section (graph builds are incremental,
snapshots re-emit identically, analysis branches and worktrees are reused).
The orchestrator resumes from `engagement-state.md`, redoing only sides not
recorded complete; a re-run after a partial failure regenerates the failed
side in full. Because the run is driven entirely by the config file, nothing
about a re-run depends on remembering what you typed the first time.

## Failure Modes and Resolution

The preparation stage's Fail Fast section enumerates what stops a run and
what it reports. Your resolutions:

| Failure | Resolution |
|---------|------------|
| Config validation error | Fix the config; re-run |
| Dirty working tree in a branch-pair repo | Commit/stash/clean the repo; re-run |
| Graph build failure on a side | Diagnose the build error; re-run |
| Graph tooling unavailable (`code-review-graph` CLI not installed) — recorded **NOT RUN**, not a failure | Install the `code-review-graph` CLI; re-run |
