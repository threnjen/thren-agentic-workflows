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

## Stage A: Comparative Audit Runs

Subagent nesting is **one deep**: the orchestrator spawns every audit agent
itself; no child spawns further agents.

For each side of the pair, spawn each audit agent **unchanged from its own
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
return its report file pointers. A dimension whose required evidence is
unavailable is NOT RUN with the reason — no files written, never a pass.

Then spawn **Engagement - Audit Runner** once per side with the pair name,
side role, workspace root, and the collected per-dimension statuses and file
pointers. It verifies and normalizes the retained reports without spawning
anything; record its returned per-dimension statuses and report pointers in
the side's working-state entry.

For a side whose (repo, revision) was already scanned under another pair,
skip the audit spawns and pass the existing report pointers to the Audit
Runner for reuse. A single side may be re-run alone — its reports overwrite
in place; the other side's entry is untouched.

If a dimension is NOT RUN on one side but complete on the other, mark that
dimension **asymmetric evidence** in the pair's working-state entry — it is
never presented as a delta.

## Stage B: Delta & Security Synthesis

Runs once both sides' audit reports exist (a NOT RUN dimension does not
block — it flows through as asymmetric evidence). Spawn in order, each with
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
