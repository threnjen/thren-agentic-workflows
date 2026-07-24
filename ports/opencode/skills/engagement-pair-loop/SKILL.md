---
name: engagement-pair-loop
description: "Standard analysis flow used by the engagement orchestrator: the per-pair evidence stage (docs + comparative audits + validation gate), then the engagement-level synthesis stages (Delta → Security → Cloud/Cost → Narrative) that produce the single holistic client-facing document set. Defines spawn inputs, ordering, gating, and working-state recording. Use when: driving the analysis stages of an engagement."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->

# Engagement Pair Loop

Two granularities, in order: **Stage A runs per pair** and produces the
per-pair evidence; **Stages B–E run once per engagement**, after every
pair's Stage A is complete, and produce the single holistic client-facing
document set (flat `deliverables/` paths, one per-repo section per pair)
plus each stage's per-pair internal basis documents. Every spawn carries
the orchestrator's standing boundaries (client-code security,
analysis-branch invariants, compact handoff); Stage A results are recorded
in the pair's working-state entry, Stage B–E results in engagement-level
entries — status plus artifact pointers only. Agent names below are source
names — spawn each via its deployed identifier in the current harness
(hidden subagents deploy with a `z-` prefix).
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

## Stages B–E: Engagement-Level Synthesis

Each stage below runs **once per engagement**, in order, and only when
**every pair** has completed Stage A — holistic client documents are never
written around a missing or blocked pair; a failed pair blocks all
synthesis until resolved. Every spawn carries the full pair roster (names,
`mode`s), the workspace root, the SOW path (or "none configured"), and
every pair's relevant report pointers. Each stage writes one client
document set at flat `deliverables/` paths with a per-repo section per
pair, plus its per-pair internal basis documents.

**Re-run invalidation**: any Stage A re-run (either side of any pair)
invalidates all Stage B–E outputs — after the re-run passes the A3 gate,
re-run stages B–E in full before finalizing.

### Stage B: Delta

Spawn **Engagement - Delta Synthesizer** with every pair's audit report
pointers. Record its client document pointers, each pair's
exclusions-partition and remediation-recommendations pointers, and any
missing-SOW or user-review flags; surface a non-empty remediation list to
the user alongside Stage C's fix-and-re-run flow.

### Stage C: Security Synthesis

Spawn **Engagement - Security Narrative** with every pair's security report
and exclusions-partition pointers. Record its client document pointer and
each pair's internal security-delta report pointer. If any pair's
security-delta Introduced section is non-empty, surface the fix-and-re-run
flow to the user: after engineer fixes, re-run that side's audits (one-side
re-run above), then re-run stages B–E per the invalidation rule.

### Stage D: Cloud/Cost Analysis

Spawn **Engagement - Pricing Researcher** with every pair's dependency/infra
report pointers. It is the **only** agent permitted internet access during
an engagement run; every other subagent operates offline against local
evidence. Record the client cloud/cost-analysis pointer, each pair's
internal cost-basis pointer, and any NOT RESEARCHED status.

### Stage E: Narrative & Specification Documents

Spawn **Engagement - Narrative Writer** with the A3-verified concrete
paths from the working-state file — per side: the analysis-branch checkout
path, the docs-set file paths on that branch, and the code-graph pointer —
plus the exact `QA_AUTOMATED.md` and `QA_USER.md` paths, QA run-result/check
coverage pointers, the SOW/contract path, and retained report pointers where
available. Never pass abstract pointers; the docs, graphs, and QA packages
live at the passed paths inside the client repository checkouts, not the
workspace, and the spawn must say so.

Before drafting, the writer builds a compact evidence map for every primary
workflow: original/upgraded comparison sources, exact QA check IDs and
statuses for the upgraded side, and the SOW criterion or explicit scope
exception that governs it. A completed PASS on an exact QA check is direct
evidence that the upgraded behavior was observed at that QA standard. It is
not, by itself, proof that the original side behaved identically; when
original QA is absent, preserve that asymmetry in the wording. “No
identifiable delta” means no behavioral delta was established by the
comparison evidence; it never means no source-code changes and never means
that QA was absent.

An intentional change expressly authorized by the SOW is an approved scoped
delta under any pair mode. It must be narrated as such and must not be
reported as an unresolved framing discrepancy. Only a change outside the
SOW, or a required behavior whose evidence and scope cannot be established,
remains a framing discrepancy.

Record its three client document pointers and each pair's internal
narrative-basis pointer. The return must include compact counts/pointers for
QA-backed workflows, SOW-authorized deltas, comparison-only claims, and
unresolved discrepancies. If any unresolved framing discrepancy remains,
surface it to the user before the compliance stage — a client narrative
contradicted by evidence must be resolved before delivery.
