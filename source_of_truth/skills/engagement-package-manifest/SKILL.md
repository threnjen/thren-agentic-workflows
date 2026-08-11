---
name: engagement-package-manifest
description: "Schema for an engagement's package manifest (`manifest.md` at the workspace root) — a two-section markdown index of the deliverable set with expected entries derived from the engagement's pairs and modes, so an incomplete package is mechanically detectable. Use when: writing the manifest, or reviewing package completeness against it (gap review)."
---

# Engagement Package Manifest

The manifest is `manifest.md` at the `engagement-workspace` root: two
sections — **Client-Facing** then **Technical / Internal** — each an ordered
table of contents of the deliverable set. All paths are workspace-root
relative and must resolve inside the root (per the `engagement-workspace`
skill); a path outside the root is a schema violation. The one exception is a
supplied scan-delta row (see Technical / Internal entry 11), which records
the caller-provided path as configured — absolute or outside the root.

## Row Fields

Every entry is one table row:

| Field | Content |
|-------|---------|
| Document | Document name |
| Path | Workspace-root-relative path |
| Audience | `client` or `internal` |
| Contract status | `SOW-required` / `above-contract` / `no SOW` (see below) |
| Present | `present` / `missing` |

**Present/missing detection** (stated once, applied to every row): a row is
`present` only if the file exists at its path with non-empty content;
otherwise `missing`. The check is **mechanical** — stat each path on disk at
manifest-write time; never fill the column from memory or from stage
statuses. Nothing suppresses a `missing` row — the expected-entry
list comes from the derivation below, never from what happens to be on disk.

**Contract status**: `SOW-required` when the engagement's SOW/deliverables
spec names the document (or the deliverable it embodies); `above-contract`
otherwise. With no SOW configured, every row reads `no SOW` — never silently
`above-contract`.

## Expected Entries — Derived, Never Hand-Enumerated

Expected entries are derived from the engagement configuration's pair roster.
Per-pair entries repeat once per pair (any number of pairs; single-pair is
not assumed). `mode` affects document content upstream, not the expected-entry
set — both modes expect the same entries.

### Client-Facing (ordered)

Client documents are **engagement-level**: one fixed set regardless of pair
count, each covering every pair holistically with one per-repo section per
pair (single-pair engagements keep the identical shape). All paths are flat
under `deliverables/`:

0. Package table of contents — `deliverables/table-of-contents.md`
1. Business design — `deliverables/business-design.md`
2. Before/after workflow narratives — `deliverables/workflow-narratives.md`
3. Findings report (before/after) — `deliverables/delta-report.md`
4. Security narrative — `deliverables/security-narrative.md`
5. Cloud/cost analysis — `deliverables/cloud-cost-analysis.md`
6. Intended-behavior specification — `deliverables/intended-behavior-spec.md`
7. SOW compliance walkthrough — `deliverables/sow-compliance-walkthrough.md`
8. Verification summary — `deliverables/verification-summary.md`
9. QA appendix — `deliverables/qa-appendix.md` (one section per repository:
   its QA_USER acceptance checklist plus an automated-QA run summary for
   agent-only targets; written by Client Deliverable - Prepare at its QA gate)

Metrics in holistic documents are reported **per pair**; an engagement-wide
roll-up appears only when no repository is shared across pairs — otherwise
the roll-up is omitted with a one-line note (never double-count a shared
repo's findings).

## Package Table of Contents

`deliverables/table-of-contents.md` is the client package's assembly order —
the downstream design step builds the final client deliverable by reading
it top to bottom, so every engagement's package opens in the identical
order. The manifest assembler writes it from the derived client-facing
expected entries above, in exactly that order (excluding itself): one row
per document — order number, document title, and workspace-root-relative
path. It lists every expected client
document whether or not it is present on disk; present/missing lives in the
manifest, never here. It is client-facing (client-deliverable banner) and
contains no internal entries.

### Technical / Internal (ordered)

Standing entries first, then per-pair expansions:

1. Package manifest — `manifest.md` (this document indexes itself)
2. Orchestrator working-state/run record — `engagement-state.md`
3. Gap-review report — `internal/gap-review.md` (standing entry: expected
   even before the gap review runs)
4. Compliance-basis report — `internal/compliance-basis.md`
5. Manifest-basis report — `internal/manifest-basis.md` (standing entry:
   written by the manifest assembler alongside this document)
6. Remediation recommendations (per pair) —
   `internal/<p>/remediation-recommendations.md`
7. Security-delta report (per pair) — `internal/<p>/security-delta.md`
8. Cost-basis report (per pair) — `internal/<p>/cost-basis.md`
9. Narrative-basis report (per pair) — `internal/<p>/narrative-basis.md`
10. SOW-exclusions partition (per pair) — `pairs/<p>/exclusions-partition.md`
11. Raw audit reports (per pair, per side, per dimension) —
   `pairs/<p>/<side>/audits/<dimension>/` for sides `original`/`upgraded` and
   dimensions code/dependencies/infra. Canonical filenames, identical
   on both sides, no pair or side prefixes: `<dimension>-report.md` and
   `<dimension>-summary.md`. One row per dimension directory, `present`
   when it contains that dimension's report. Every scanned dimension is
   mandatory — an empty dimension directory is a `missing` row (a pipeline
   defect to surface), never omitted. For a **supplied** dimension the
   per-side scan rows are replaced by rows for what the config gave, each
   audience `internal`, `present` when its path resolves: one row per side
   ("Supplied `<dimension>` audit, `<side>`", path the side's
   `code_audit_path`/`infra_audit_path`, present when the directory holds a
   non-empty `.md`), and, when a delta was configured, one pair-level row
   ("Supplied `<dimension>` scan delta", path the configured file, present
   when it resolves non-empty)
12. Phase 01 baseline snapshots (per pair, per side) —
   `pairs/<p>/<side>/engagement-baseline-snapshot.md`. Snapshots originate on
   each side's analysis branch; the manifest-writing step copies each into
   the workspace at this path (metadata only — the snapshot contains no
   source content) so the row's path resolves inside the root.
