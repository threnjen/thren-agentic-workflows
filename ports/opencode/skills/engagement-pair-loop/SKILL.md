---
name: engagement-pair-loop
description: "Standard analysis flow used by the Client Deliverable orchestrator: the per-pair evidence stage (docs + comparative audits + validation gate), then the engagement-level synthesis stages (Delta → Security → Cloud/Cost → Narrative) that produce the single holistic client-facing document set. Defines spawn inputs, ordering, gating, and working-state recording. Use when: driving the analysis stages of an engagement."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->

# Engagement Pair Loop

The workflow has two granularities, in order. **Stage A runs per pair** and
produces the per-pair evidence. **Stages B–E run once per engagement** after
every pair's Stage A is complete. These stages produce the single holistic
client-facing document set at flat `deliverables/` paths, with one per-repo
section per pair. They also produce each stage's per-pair internal basis
documents.

Every spawn carries the orchestrator's standing boundaries (client-code
security, analysis-branch invariants, compact handoff). Record Stage A
results in the pair's working-state entry. Record Stage B–E results in
engagement-level entries. Record status plus artifact pointers only. The
agent names below are source names. Spawn each agent through its deployed
identifier in the current harness. Hidden subagents deploy with a `z-`
prefix.

## Stage A: Prepare All Evidence

Stage A produces **every evidence artifact the rest of the workflow
consumes**. Validate the full set before any later stage runs.

Subagent nesting has one level. The orchestrator spawns every agent below
itself. No child spawns further agents.

### A1: Documentation

For each side, spawn **Docs Writer** against the side's analysis-branch
checkout at the side's revision on every invocation. Do not run a staleness
check. Do not skip the spawn. Scope the work by role. For `upgraded` sides,
request the full document set according to Docs Writer's own applicability
assessment.
For `original` sides, request at minimum README, ARCHITECTURE, and
CODEBASE_CONTEXT. Head each document as an internal analysis artifact.
Commit the produced docs onto the side's analysis branch. Record the
docs-set pointer.

### A2: Comparative Audits

For each side, spawn each listed agent **unchanged from its own
definition**. Do not add grants or alter scope. Run each agent against the
side's analysis-branch checkout:

| Dimension | Agent |
|-----------|-------|
| code | Auditor - Code |
| dependencies | 04e Dependency Auditor |
| infra | Auditor - Infra |

There is no separate security scan. The code and infra audits surface
security findings within their own dimensions. Stage C draws its security
material from those reports.

Each spawn carries the standing boundaries. Direct each agent to write its
reports under
`<workspace-root>/pairs/<pair-name>/<side-role>/audits/<dimension>/` using
the canonical filenames from the `engagement-package-manifest` skill. Direct
each agent to return its report file pointers.

**Supplied dimensions.** A dimension is `supplied` when the pair's config
provides evidence for it in either of two independent forms:

| Form | Config | What Stage B receives |
|---|---|---|
| Per-side audits | `code_audit_path` / `infra_audit_path` on **both** sides | the two side audit directories, in place of reports this loop would have produced |
| Pair-level delta | `code_delta_path` / `infra_delta_path` | the delta file, in place of the two per-side reports |

Both forms may be present for one dimension. Pass whatever the config gave.
A supplied dimension is **not scanned on either side**. Skip both spawns. The
Treat the dimension as `supplied`. Never record it as `failed`. Never
re-derive it from the trees. Scan a dimension with neither form normally.

**Copy supplied artifacts into the workspace.** A supplied path may point
anywhere on disk. The engagement keeps its own copy so the package is
self-contained and the evidence cannot move or change underneath it. Copy
every supplied file **verbatim**. Use the same filenames. Make no edits. Add
no re-banner. Copy per-side audits into
`pairs/<pair-name>/<side-role>/audits/<dimension>/`. Copy a pair-level delta
into `pairs/<pair-name>/`. Record both the source path and the workspace copy
in the pair's working-state entry. Every later stage consumes the copy. Never
modify the original. Never write back to it.

**Every dimension not supplied is mandatory on every side.** A scan with no
findings is a complete scan with an empty findings table. It still writes its
reports. An agent that returns without its reports or claims that it could not
scan a dimension has failed to spawn. Re-run it once with the blocker named.
If it still returns incomplete, this is a FAIL FAST report to the user. Stop
the pipeline. Never skip or waive a dimension. Record every dimension as
complete or failed.

### A3: Evidence Validation Gate

Verify mechanically that every artifact the later stages consume exists for
**both sides**. Use existence and first-line checks only. Never read content.

- Verify the analysis branch, code graph, and baseline snapshot from
  preparation on disk. Do not trust the report.
- Verify the side's docs set from A1.
- For every scanned dimension, verify its two audit files from A2:
  `<dimension>-report.md` and `<dimension>-summary.md`. Each file must be
  non-empty at its exact canonical path and name. Each file must open with the
  internal audience banner per the `engagement-workspace` skill.
- For every supplied dimension, verify that the workspace copy exists and is
  non-empty at its contract location. Verify one delta file once for the pair,
  not per side. Verify at least one `.md` under each side's dimension audits
  directory. Verify that each copy matches its source. No banner check
  applies. These files come from outside this pipeline. A configured
  source path that does not resolve is a config failure, not a missing artifact.

If an artifact fails any check (absent, wrong name, wrong path, empty, or
missing banner), treat its producing step as a stage failure. Re-run that step
with the correction named. Never rename, stub, or edit files to compensate.

Record per-side statuses (complete / failed with cause) and verified pointers
in the working-state entry. Status reflects execution, not verdict. A
retained report is `complete` regardless of its conclusions (BLOCKED, NO-GO,
critical findings). Stage A is complete only when every checklist item above
is verified on both sides. If a side has a persistently failing artifact, fail
the pair per the orchestrator's fail-fast rule. Never run a later stage on
partial evidence.

For a side whose (repo, revision) already passed this gate under another pair,
skip its spawns and reuse the existing verified pointers. A single side may be
re-run alone. Its artifacts overwrite in place. Leave the other side's entry
untouched.

## Stages B–E: Engagement-Level Synthesis

Each stage below runs **once per engagement** and in order. Run it only after
the orchestrator's §4 pair gate opens. Every spawn carries the full pair roster
(names, `mode`s), the workspace root, the SOW path (or "none configured"),
and every pair's relevant report pointers. Each stage writes one client
document set at flat `deliverables/` paths. Include one per-repo section per
pair. Also write its per-pair internal basis documents.

**Re-run invalidation**: Any Stage A re-run (either side of any pair)
invalidates all Stage B–E outputs. After the re-run passes the A3 gate, re-run
stages B–E in full before finalizing. An accepted owner attestation also
invalidates B–E, but **not** Stage A. Re-run synthesis only. Never re-run the
source audits.

Every B–E spawn carries the working-state file's attestation records per the
`engagement-workspace` skill. This lets each stage close the named findings
under the `engagement-evidence-standard` skill's `attested` rules.

### Stage B: Delta

Spawn **Client Deliverable - Delta Synthesizer** with every pair's audit report
pointers. For any supplied dimension, use the workspace delta copy in place
of that dimension's two per-side reports. Label it as a supplied delta so the
synthesizer consumes its classifications rather than re-comparing. Record its
client document pointers. Record each pair's exclusions-partition and
remediation-recommendations pointers. Record any missing-SOW or user-review
flags. Surface a non-empty remediation list to the user alongside Stage C's
fix-and-re-run flow.

### Stage C: Security Synthesis

Spawn **Client Deliverable - Security Narrative** with every pair's code and
infra report pointers for both sides. For a supplied dimension, use the
supplied delta path instead. Include exclusions-partition pointers. There is
no dedicated security report. The writer extracts the security-relevant
findings from those reports. Record its client document pointer and each
pair's internal security-delta report pointer. If any pair's security-delta
Introduced section is non-empty, surface the fix-and-re-run flow to the user.
After engineer fixes, re-run that side's audits (one-side re-run above). Then
re-run stages B–E per the invalidation rule.

### Stage D: Cloud/Cost Analysis

Spawn **Client Deliverable - Pricing Researcher** with every pair's
dependency/infra report pointers. It is the **only** agent permitted internet
access during an engagement run. Every other subagent operates offline
against local evidence. Record the client cloud/cost-analysis pointer, each
pair's internal cost-basis pointer, and any NOT RESEARCHED status.

### Stage E: Narrative & Specification Documents

Spawn **Client Deliverable - Narrative Writer** with the A3-verified concrete
paths from the working-state file. For each side, pass the analysis-branch
checkout path, the docs-set file paths on that branch, and the code-graph
pointer. Also pass the exact `QA_AUTOMATED.md` and `QA_USER.md` paths, QA
run-result/check coverage pointers, the SOW/contract path, and retained report
pointers where available. Never pass abstract pointers. The docs, graphs, and
QA packages live at the passed paths inside the client repository checkouts,
not the workspace. State this in the spawn.

The spawn directs the writer to build its evidence map and classify every
primary workflow and every mode-straining change per the
`engagement-evidence-standard` skill.

Record its three client document pointers and each pair's internal
narrative-basis pointer. The return must include compact counts/pointers per
evidence class (`qa-backed`, `comparison-only`, `unverified`) and per scope
class (`sow-authorized`, `unresolved`). If any `unresolved` change remains,
surface it to the user before the compliance stage. Resolve a client narrative
contradicted by evidence before delivery.
