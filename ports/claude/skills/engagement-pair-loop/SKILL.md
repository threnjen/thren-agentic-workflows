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

## Stage A: Prepare Base Reports

For each side of the pair, spawn each listed agent **unchanged from its own
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
dimension could not be scanned, is a failed spawn: re-run it with the
blocker named until it completes. No dimension is ever skipped, waived, or
recorded as anything but complete or failed.

Then verify each returned report mechanically (no content reading beyond
the first line): the file exists non-empty at its exact canonical path and
name, and opens with the internal audience banner per the
`engagement-workspace` skill. A report that fails any check — wrong name,
wrong path, empty, missing banner — is a stage failure for that dimension:
re-run that dimension's audit with the correction named; never rename or
edit files to compensate.

Record the per-dimension statuses (complete / failed with cause) and
verified pointers in the side's working-state entry. Status reflects
execution, not verdict — a retained report is `complete` regardless of its
conclusions (BLOCKED, NO-GO, critical findings). The stage is complete
only when all four dimensions are `complete` on both sides; a side with a
persistently failing dimension fails the pair per the orchestrator's
fail-fast rule — never proceed to Stage B on partial evidence.

For a side whose (repo, revision) was already scanned under another pair,
skip the audit spawns and reuse the existing verified pointers. A single
side may be re-run alone — its reports overwrite in place; the other
side's entry is untouched.

## Stage B: Delta & Security Synthesis

Runs once Stage A is complete for both sides. Spawn in order, each with
the pair name, workspace root, and report pointers:

1. **Engagement - Delta Synthesizer** — also pass the pair's `mode` and the
   SOW path (or "none configured"). Record its document pointers, the
   exclusions-partition pointer, and any missing-SOW or user-review flags in
   the working-state entry.
2. **Engagement - Security Narrative** — also pass the SOW path and the
   exclusions-partition pointer from step 1.
3. **Engagement - Introduced Issues** — internal-only output. If it reports
   findings, surface the fix-and-re-run flow to the user: after engineer
   fixes, re-run that side's audits (one-side re-run above), then re-run
   this stage before finalizing client-facing artifacts.

## Stage C: Cloud/Cost Analysis

Spawn **Engagement - Pricing Researcher** with the pair name, workspace
root, and dependency/infra report pointers. It is the **only** agent
permitted internet access during an engagement run; every other subagent
operates offline against local evidence. Record its document pointer and any
NOT RESEARCHED status.

## Stage D: Narrative & Specification Documents

Spawn **Engagement - Narrative Writer** with the pair name, the pair's
`mode`, the workspace root, and pointers to each side's docs-writer set and
code graph (plus retained report pointers where available). Record its three
document pointers in the working-state entry.
