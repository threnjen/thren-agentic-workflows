---
name: engagement-package-manifest
description: "Schema for an engagement's package manifest (`manifest.md` at the workspace root) — a two-section markdown index of the deliverable set with expected entries derived from the engagement's pairs and modes, so an incomplete package is mechanically detectable. Use when: writing the manifest, or reviewing package completeness against it (gap review)."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->
# Engagement Package Manifest

The manifest is `manifest.md` at the `engagement-workspace` root: two
sections — **Client-Facing** then **Technical / Internal** — each an ordered
table of contents of the deliverable set. All paths are workspace-root
relative and must resolve inside the root (per the `engagement-workspace`
skill); a path outside the root is a schema violation.

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
otherwise `missing`. Nothing suppresses a `missing` row — the expected-entry
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

Per pair `<p>`:

1. Business design — `deliverables/<p>/business-design.md`
2. Before/after workflow narratives — `deliverables/<p>/workflow-narratives.md`
3. Delta report — `deliverables/<p>/delta-report.md`
4. Security narrative — `deliverables/<p>/security-narrative.md`
5. Cloud/cost analysis — `deliverables/<p>/cloud-cost-analysis.md`
6. Intended-behavior specification — `deliverables/<p>/intended-behavior-spec.md`

Then the compliance materials, per engagement, with each pair's audit-trail
proof grouped among them:

7. SOW compliance walkthrough — `deliverables/sow-compliance-walkthrough.md`
8. Audit-trail proof (per pair) — `deliverables/<p>/audit-trail-proof.md`
9. Verification summary — `deliverables/verification-summary.md`

### Technical / Internal (ordered)

Standing entries first, then per-pair expansions:

1. Package manifest — `manifest.md` (this document indexes itself)
2. Orchestrator working-state/run record — `engagement-state.md`
3. Gap-review report — `internal/gap-review.md` (standing entry: expected
   even before the gap review runs)
4. Introduced-issues report (per pair) — `internal/<p>/introduced-issues.md`
5. SOW-exclusions partition (per pair) — `pairs/<p>/exclusions-partition.md`
6. Raw audit reports (per pair, per side, per dimension) —
   `pairs/<p>/<side>/audits/<dimension>/` for sides `original`/`upgraded` and
   dimensions security/code/dependencies/infra; one row per dimension
   directory, `present` when it contains that dimension's report (a dimension
   NOT RUN is a `missing` row annotated NOT RUN, never omitted)
7. Phase 01 baseline snapshots (per pair, per side) —
   `pairs/<p>/<side>/engagement-baseline-snapshot.md`. Snapshots originate on
   each side's analysis branch; the manifest-writing step copies each into
   the workspace at this path (metadata only — the snapshot contains no
   source content) so the row's path resolves inside the root.
