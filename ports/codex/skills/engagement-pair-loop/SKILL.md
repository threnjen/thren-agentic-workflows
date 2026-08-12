---
name: engagement-pair-loop
description: "Standard analysis flow used by the Client Deliverable orchestrator: the per-pair evidence stage (docs + comparative audits + validation gate), then the engagement-level synthesis stages (Delta → Security → Cloud/Cost → Narrative) that produce the single holistic client-facing document set. Defines spawn inputs, ordering, gating, and working-state recording. Use when: driving the analysis stages of an engagement."
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
| code | Auditor - Code |
| dependencies | 05e Dependency Auditor |
| infra | Auditor - Infra |

There is no separate security scan. The code and infra audits surface
security findings within their own dimensions, and Stage C draws its
security material from those reports.

Each spawn carries the standing boundaries and directs the agent to write
its reports under
`<workspace-root>/pairs/<pair-name>/<side-role>/audits/<dimension>/` using
the canonical filenames from the `engagement-package-manifest` skill, and to
return its report file pointers.

**Supplied dimensions.** A dimension is `supplied` when the pair's config
provides evidence for it in either of two independent forms:

| Form | Config | What Stage B receives |
|---|---|---|
| Per-side audits | `code_audit_path` / `infra_audit_path` on **both** sides | the two side audit directories, in place of reports this loop would have produced |
| Pair-level delta | `code_delta_path` / `infra_delta_path` | the delta file, in place of the two per-side reports |

Both forms may be present for one dimension; pass whatever the config gave.
A supplied dimension is **not scanned on either side**: skip both spawns. The
dimension is `supplied` — never `failed`, never re-derived from the trees. A
dimension with neither form is scanned normally.

**Copy supplied artifacts into the workspace.** A supplied path may point
anywhere on disk; the engagement keeps its own copy so the package is
self-contained and the evidence cannot move or change underneath it. Copy every
supplied file **verbatim** — same filenames, no edits, no re-banner — into the
pair's contract location: per-side audits into
`pairs/<pair-name>/<side-role>/audits/<dimension>/`, a pair-level delta into
`pairs/<pair-name>/`. Record both the source path and the workspace copy in the
pair's working-state entry; every later stage consumes the copy. Never modify
the original, and never write back to it.

**Every dimension not supplied is mandatory on every side.** A scan with no
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
- for every scanned dimension, its two audit files from A2 —
  `<dimension>-report.md` and `<dimension>-summary.md`, each non-empty at
  its exact canonical path and name and opening with the internal audience
  banner per the `engagement-workspace` skill
- for every supplied dimension, the workspace copy exists and is non-empty at
  its contract location — a delta file (checked once for the pair, not per
  side), and per side at least one `.md` under the dimension's audits
  directory — and matches its source. No banner check applies: these were
  authored outside this pipeline. A configured source path that does not
  resolve is a config failure, not a missing artifact

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

Each stage below runs **once per engagement**, in order, and only once the
orchestrator's §4 pair gate opens. Every spawn carries the full pair roster (names,
`mode`s), the workspace root, the SOW path (or "none configured"), and
every pair's relevant report pointers. Each stage writes one client
document set at flat `deliverables/` paths with a per-repo section per
pair, plus its per-pair internal basis documents.

**Re-run invalidation**: any Stage A re-run (either side of any pair)
invalidates all Stage B–E outputs — after the re-run passes the A3 gate,
re-run stages B–E in full before finalizing. An accepted owner attestation
also invalidates B–E, but **not** Stage A: re-run synthesis only, never the
source audits.

Every B–E spawn carries the working-state file's attestation records (per the
`engagement-workspace` skill) so each stage can close the named findings per
the `engagement-evidence-standard` skill's `attested` rules.

### Stage B: Delta

Spawn **Client Deliverable - Delta Synthesizer** with every pair's audit report
pointers, and for any supplied dimension the workspace delta copy in place
of that dimension's two per-side reports — labelled as a supplied delta so
the synthesizer consumes its classifications rather than re-comparing. Record its client document pointers, each pair's
exclusions-partition and remediation-recommendations pointers, and any
missing-SOW or user-review flags; surface a non-empty remediation list to
the user alongside Stage C's fix-and-re-run flow.

### Stage C: Security Synthesis

Spawn **Client Deliverable - Security Narrative** with every pair's code and
infra report pointers for both sides (or the supplied delta path for a
supplied dimension) and exclusions-partition pointers — there is no
dedicated security report; the writer extracts the security-relevant
findings from those reports itself. Record its client document pointer and
each pair's internal security-delta report pointer. If any pair's
security-delta Introduced section is non-empty, surface the fix-and-re-run
flow to the user: after engineer fixes, re-run that side's audits (one-side
re-run above), then re-run stages B–E per the invalidation rule.

### Stage D: Cloud/Cost Analysis

Spawn **Client Deliverable - Pricing Researcher** with every pair's dependency/infra
report pointers. It is the **only** agent permitted internet access during
an engagement run; every other subagent operates offline against local
evidence. Record the client cloud/cost-analysis pointer, each pair's
internal cost-basis pointer, and any NOT RESEARCHED status.

### Stage E: Narrative & Specification Documents

Spawn **Client Deliverable - Narrative Writer** with the A3-verified concrete
paths from the working-state file — per side: the analysis-branch checkout
path, the docs-set file paths on that branch, and the code-graph pointer —
plus the exact `QA_AUTOMATED.md` and `QA_USER.md` paths, QA run-result/check
coverage pointers, the SOW/contract path, and retained report pointers where
available. Never pass abstract pointers; the docs, graphs, and QA packages
live at the passed paths inside the client repository checkouts, not the
workspace, and the spawn must say so.

The spawn directs the writer to build its evidence map and classify every
primary workflow and every mode-straining change per the
`engagement-evidence-standard` skill.

Record its three client document pointers and each pair's internal
narrative-basis pointer. The return must include compact counts/pointers per
evidence class (`qa-backed`, `comparison-only`, `unverified`) and per scope
class (`sow-authorized`, `unresolved`). If any `unresolved` change remains,
surface it to the user before the compliance stage — a client narrative
contradicted by evidence must be resolved before delivery.
