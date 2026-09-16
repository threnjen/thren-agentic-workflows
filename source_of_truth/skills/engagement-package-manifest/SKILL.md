---
name: engagement-package-manifest
description: "Schema for an engagement's package manifest (`manifest.md` at the workspace root) — a two-section markdown index of the deliverable set with expected entries derived from the engagement's pairs and modes, so an incomplete package is mechanically detectable. Use when: writing the manifest, or reviewing package completeness against it (gap review)."
---

# Engagement Package Manifest

The manifest is `manifest.md` at the `engagement-workspace` root: two
sections — **Client-Facing** then **Technical / Internal** — each an ordered
table of contents of the deliverable set. All paths are workspace-root
relative and must resolve inside the root, as required by the
`engagement-workspace` skill. A path outside the root violates the schema. The
only exception is a supplied scan-delta row (see Technical / Internal entry
11). It records the caller-provided path as configured, whether absolute or
outside the root.

## Row Fields

Every entry is one table row:

| Field | Content |
|-------|---------|
| Document | Document name |
| Path | Workspace-root-relative path |
| Audience | `client` or `internal` |
| Contract status | `SOW-required` / `above-contract` / `no SOW` (see below) |
| Present | `present` / `missing` |

**Present/missing detection** applies to every row. A row is `present` only if
the file exists at its path with non-empty content. Otherwise, the row is
`missing`. The check is **mechanical**. Stat each path on disk at
manifest-write time. Never fill the column from memory or stage statuses.
Nothing suppresses a `missing` row. The expected-entry list comes from the
derivation below, not from what happens to be on disk.

**Contract status** is `SOW-required` when the engagement's SOW/deliverables
spec names the document or the deliverable it embodies. Otherwise, it is
`above-contract`. With no SOW configured, set every row to `no SOW`. Never
silently set a row to `above-contract`.

## Expected Entries — Derived, Never Hand-Enumerated

The engagement configuration's pair roster determines expected entries.
Repeat each per-pair entry once for each pair. Support any number of pairs. Do
not assume a single pair. The `mode` affects document content upstream, not the
expected-entry set. Both modes expect the same entries.

### Client-Facing (ordered)

Client documents are **engagement-level**. Use one fixed set for every pair
count. Each document covers every pair holistically with one per-repo section
per pair. Single-pair engagements keep the same shape. All paths are flat under
`deliverables/`:

0. Package table of contents — `deliverables/table-of-contents.md`
1. Business design — `deliverables/business-design.md`
2. Before/after workflow narratives — `deliverables/workflow-narratives.md`
3. Findings report (before/after) — `deliverables/delta-report.md`
4. Security narrative — `deliverables/security-narrative.md`
5. Cloud/cost analysis — `deliverables/cloud-cost-analysis.md`
6. Intended-behavior specification — `deliverables/intended-behavior-spec.md`
7. SOW compliance walkthrough — `deliverables/sow-compliance-walkthrough.md`
8. Verification summary — `deliverables/verification-summary.md`
9. QA appendix — `deliverables/qa-appendix.md` (The appendix has one section per
   repository. Each section contains its QA_USER acceptance checklist and, for agent-only
   targets, an automated-QA run summary. Client Deliverable - Prepare writes
   this document at its QA gate.)
10. Engagement team — `deliverables/engagement-team.md` (This document names
    the people who worked the engagement and what they did. The user supplies
    the content, as defined in the Engagement Team section below.)

Report metrics in holistic documents **per pair**. Include an engagement-wide
roll-up only when no repository is shared across pairs. Otherwise, omit the
roll-up and add a one-line note. Never double-count a shared repository's
findings.

## Package Table of Contents

Use `deliverables/table-of-contents.md` as the client package's assembly order.
The downstream design step reads it from top to bottom to build the final client
deliverable. This gives every engagement's package the same opening order. The
manifest assembler writes it from the derived client-facing expected entries
above, in exactly that order. Exclude the table of contents itself. Add one row
per document with its order number, document title, and
workspace-root-relative path. List every expected client document whether or
not it is present on disk. Record present/missing in the manifest, never here.
This file is client-facing and uses a client-deliverable banner. It contains no
internal entries.

## Engagement Team

`deliverables/engagement-team.md` names the people who worked the engagement
and what each did. Do not derive its content from a repository or audit. The
orchestrator collects the content from the user (see the Client Deliverable
orchestrator's stage 5) and writes the file. No other stage writes it. An agent
never overwrites or rewrites an existing file.

The file contains a client banner, one heading, and one table. It includes one
contact line when the user provides a contact address:

```markdown
> **AUDIENCE: CLIENT DELIVERABLE** — hand off to design for client PDF.

# Engagement team

| Name | Role |
|---|---|
| <name> | <short list of what they did> |

Questions about any part of this package can be directed to the engagement
team at `<contact>`.
```

Add one row per person in the order the user provides. Keep each role cell to
one or two short phrases. This is a credits page, not a responsibility matrix.
Omit the contact line when the user provides no contact address.

### Technical / Internal (ordered)

List standing entries first, then expand per-pair entries:

1. Package manifest — `manifest.md` (the manifest indexes itself)
2. Orchestrator working-state/run record — `engagement-state.md`
3. Gap-review report — `internal/gap-review.md` (This standing entry remains
   expected before the gap review runs.)
4. Compliance-basis report — `internal/compliance-basis.md`
5. Manifest-basis report — `internal/manifest-basis.md` (The manifest assembler
   writes this standing entry alongside this document.)
6. Remediation recommendations (per pair) —
   `internal/<p>/remediation-recommendations.md`
7. Security-delta report (per pair) — `internal/<p>/security-delta.md`
8. Cost-basis report (per pair) — `internal/<p>/cost-basis.md`
9. Narrative-basis report (per pair) — `internal/<p>/narrative-basis.md`
10. SOW-exclusions partition (per pair) — `pairs/<p>/exclusions-partition.md`
11. Raw audit reports (per pair, per side, per dimension) —
   Use `pairs/<p>/<side>/audits/<dimension>/` for sides `original`/`upgraded`
   and dimensions code/dependencies/infra. Use canonical filenames on both sides.
   Do not add pair or side prefixes. Use `<dimension>-report.md` and
   `<dimension>-summary.md`. Add one row per dimension directory. Mark the row
   `present` when the directory contains that dimension's report. Every scanned
   dimension is mandatory. Mark an empty dimension directory as a `missing` row.
   Surface this missing row as a pipeline defect. Never omit it. For a
   **supplied** dimension, replace the per-side scan rows with rows for the
   values that the config gave.
   Set each row's audience to `internal`. Mark each row `present` when its path
   resolves. Add one row per side.
   Use the label ("Supplied `<dimension>` audit, `<side>`", path the side's
   `code_audit_path`/`infra_audit_path`). Mark the row `present` when the
   directory contains a non-empty `.md` file. When a delta is configured, add
   one pair-level row ("Supplied `<dimension>` scan delta", path the configured
   file). Mark the row `present` when the configured file resolves to non-empty
   content.
12. Phase 01 baseline snapshots (per pair, per side) —
   `pairs/<p>/<side>/engagement-baseline-snapshot.md`. Snapshots originate on
   each side's analysis branch. The manifest-writing step copies each snapshot
   into the workspace at this path. The snapshot contains metadata only, not
   source content. This makes the row's path resolve inside the root.
