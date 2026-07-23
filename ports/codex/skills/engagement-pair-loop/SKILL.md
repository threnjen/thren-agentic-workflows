---
name: engagement-pair-loop
description: "Standard per-pair analysis loop used by the engagement orchestrator. Defines the Comparative Audits → Delta & Security Synthesis → Cloud/Cost → Narrative stage cycle, including spawn inputs, ordering, and working-state recording. Use when: driving the analysis stages for one engagement comparison pair."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->
# Engagement Pair Loop

The stage cycle the engagement orchestrator runs for each comparison pair.
Stages run in order; every spawn carries the orchestrator's standing
boundaries (client-code security, analysis-branch invariants, compact
handoff), and every result is recorded in the pair's working-state entry as
status plus artifact pointers only.

## Stage A: Prepare All Evidence

Stage A produces **every evidence artifact the rest of the workflow
consumes**, then validates the full set before any later stage runs.
Subagent nesting is one deep: the orchestrator spawns every agent below
itself; no child spawns further agents.

### A1: Documentation

For each side, spawn **Docs Writer** against the side's analysis-branch
checkout at the side's revision, on every invocation — no staleness check,
no skip. Scope by role: `upgraded` sides get the full document set per Docs
Writer's own applicability assessment; `original` sides get at minimum
README, ARCHITECTURE, and CODEBASE_CONTEXT, each headed as an internal
analysis artifact. Commit the produced docs onto the side's analysis
branch; record the docs-set pointer.

### A2: Comparative Audits

For each side, spawn each listed agent **unchanged from its own
definition** — no added grants, no altered scope — against the side's
analysis-branch checkout:

| Dimension | Agent |
|-----------|-------|
| security | Security Scan (full codebase) |
| code | Auditor - Code |
| dependencies | 05e Dependency Auditor |
| infra | Auditor - Infra |

Each spawn carries the standing boundaries and directs the agent to write
its reports under
`<workspace-root>/pairs/<pair-name>/<side-role>/audits/<dimension>/` using
the canonical filenames from the `engagement-package-manifest` skill, and to
return its report file pointers.

**All four dimensions are mandatory on every side.** A scan with no
findings is a complete scan with an empty findings table — it still writes
its reports. An agent returning without its reports, or claiming a
dimension could not be scanned, is a failed spawn: re-run it once with the
blocker named. If it still returns incomplete, this is a FAIL FAST report to the user and stops the pipeline. 
No dimension is ever skipped, waived, or
recorded as anything but complete or failed.

### A3: Evidence Validation Gate

Verify mechanically (existence and first-line checks only — never read
content) that every artifact the later stages consume exists for **both
sides**:

- analysis branch, code graph, and baseline snapshot (from preparation;
  re-confirm on disk, do not trust the report)
- the side's docs set from A1
- all eight audit files from A2 — `<dimension>-report.md` and
  `<dimension>-summary.md` per dimension, each non-empty at its exact
  canonical path and name and opening with the internal audience banner
  per the `engagement-workspace` skill

An artifact that fails any check — absent, wrong name, wrong path, empty,
missing banner — is a stage failure for its producing step: re-run that
step with the correction named; never rename, stub, or edit files to
compensate.

Record per-side statuses (complete / failed with cause) and verified
pointers in the working-state entry. Status reflects execution, not
verdict — a retained report is `complete` regardless of its conclusions
(BLOCKED, NO-GO, critical findings). Stage A is complete only when every
checklist item above is verified on both sides; a side with a persistently
failing artifact fails the pair per the orchestrator's fail-fast rule —
no later stage ever runs on partial evidence.

For a side whose (repo, revision) already passed this gate under another
pair, skip the spawns and reuse the existing verified pointers. A single
side may be re-run alone — its artifacts overwrite in place; the other
side's entry is untouched.

## Stage B: Delta

Runs once Stage A is complete for both sides. Spawn with
the pair name, workspace root, and report pointers:

Spawn **Engagement - Delta Synthesizer** — also pass the pair's `mode` and the
SOW path (or "none configured"). Record its document pointers, the
exclusions-partition and remediation-recommendations pointers, and any
missing-SOW or user-review flags in the working-state entry; surface a
non-empty remediation list to the user alongside step 3's
fix-and-re-run flow.


## Stage C: Security Synthesis

Runs once Stage B is complete for both sides. Spawn with
the pair name, workspace root, and report pointers:

Spawn **Engagement - Security Narrative** — also pass the SOW path and the
exclusions-partition pointer. Record its document pointers,
including the internal security-delta report. If the security delta's
Introduced section is non-empty, surface the fix-and-re-run flow to the
user: after engineer fixes, re-run that side's audits (one-side re-run
above), then re-run this stage before finalizing client-facing
artifacts.

## Stage D: Cloud/Cost Analysis

Spawn **Engagement - Pricing Researcher** with the pair name, workspace
root, and dependency/infra report pointers. It is the **only** agent
permitted internet access during an engagement run; every other subagent
operates offline against local evidence. Record both document pointers —
the client cloud/cost analysis and the internal cost-basis report — and any
NOT RESEARCHED status.

## Stage E: Narrative & Specification Documents

Spawn **Engagement - Narrative Writer** with the pair name, the pair's
`mode`, the workspace root, and pointers to each side's docs-writer set and
code graph (plus retained report pointers where available). Record its four
document pointers, including the internal narrative-basis report. If that
report's framing-discrepancies section is non-empty, surface it to the user
before the compliance stage — a client narrative contradicted by evidence
must be resolved before delivery.
