---
name: engagement-package-manifest
description: "Schema for an engagement's package manifest (`manifest.md` at the workspace root) — a two-section markdown index of the deliverable set with expected entries derived from the engagement's pairs and modes, so an incomplete package is mechanically detectable. Use when: writing the manifest, or reviewing package completeness against it (gap review)."
---

# Engagement Package Manifest

The manifest is `manifest.md` at the `engagement-workspace` root: two
sections — **Client-Facing** then **Technical / Internal** — each an ordered
table of contents of the deliverable set. A **Deliverables-Spec Mapping**
table follows them. All paths are workspace-root
relative and must resolve inside the root, as required by the
`engagement-workspace` skill. A path outside the root violates the schema. The
only exception is a supplied scan-delta row (see Technical / Internal entry
12). It records the caller-provided path as configured, whether absolute or
outside the root. When that path resolves only on a side's analysis branch,
the row also cites the workspace copy under `pairs/<p>/`.

## Row Fields

Every entry is one table row:

| Field | Content |
|-------|---------|
| Document | Document name |
| Path | Workspace-root-relative path |
| Audience | `client` or `internal` |
| Contract status | `SOW-required` / `above-contract` / `no SOW` (see below) |
| Present | `present` / `missing` / `not-applicable` |

**Present/missing detection** applies to every row. A row is `present` only if
the file exists at its path with non-empty content. Otherwise, the row is
`missing`. The manifest's own row and the manifest-basis row are `present`
by construction, because the assembler writes both in the same invocation.
The other exception is a conditional row whose producing stage
returned `not-applicable`. Mark that row `not-applicable` and append the
stage's one-line reason to the Document cell. The check is **mechanical**. Stat each path on disk at
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
`deliverables/`. The document title in this list is the document's H1 and its
table-of-contents title:

1. Table of contents — `deliverables/table-of-contents.md`
2. How to read this package — `deliverables/how-to-read-this-package.md`
   (The manifest assembler writes this document. See How to Read This Package
   below.)
3. Business design — `deliverables/business-design.md`
4. Before/after workflow narratives — `deliverables/workflow-narratives.md`
5. Intended-behavior specification — `deliverables/intended-behavior-spec.md`
   (Its final section, `Verification evidence and warranty scope`, carries the
   functional-preservation statement. No separate verification summary
   exists.)
6. SOW compliance walkthrough — `deliverables/sow-compliance-walkthrough.md`
7. Cloud/cost analysis — `deliverables/cloud-cost-analysis.md`
   (**Conditional.** The pricing researcher writes it only when the upgrade
   has a material cost impact. Otherwise the row is `not-applicable` and the
   table of contents omits it.)
8. Appendix — Security narrative — `deliverables/security-narrative.md`
9. Appendix — QA report — `deliverables/qa-appendix.md` (The appendix has one
   section per repository. Each section contains its manual QA results
   and, for agent-only targets, an automated-QA run summary. Client
   Deliverable - Prepare writes this document at its QA gate.)
10. Engagement team — `deliverables/engagement-team.md` (This document names
    the people who worked the engagement and what they did. The user supplies
    the content, as defined in the Engagement Team section below.)

The comparison record is internal
(`internal/comparison-record.md`). Never add it to the client set.

Report metrics in holistic documents **per pair**. Include an engagement-wide
roll-up only when no repository is shared across pairs. Otherwise, omit the
roll-up and add a one-line note. Never double-count a shared repository's
findings.

### Technical / Internal (ordered)

List standing entries first, then expand per-pair entries:

1. Package manifest — `manifest.md` (the manifest indexes itself)
2. Orchestrator working-state/run record — `engagement-state.md`
3. Gap-review report — `internal/gap-review.md` (This standing entry remains
   expected before the gap review runs.)
4. Compliance-basis report — `internal/compliance-basis.md`
5. Manifest-basis report — `internal/manifest-basis.md` (The manifest assembler
   writes this standing entry alongside this document.)
6. Comparison record (before/after) — `internal/comparison-record.md`
7. Remediation recommendations (per pair) —
   `internal/<p>/remediation-recommendations.md`
8. Security-delta report (per pair) — `internal/<p>/security-delta.md`
9. Cost-basis report (per pair) — `internal/<p>/cost-basis.md`
10. Narrative-basis report (per pair) — `internal/<p>/narrative-basis.md`
11. SOW-exclusions partition (per pair) — `pairs/<p>/exclusions-partition.md`
12. Raw audit reports (per pair, per side, per dimension) —
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
13. Phase 01 baseline snapshots (per pair, per side) —
   `pairs/<p>/<side>/engagement-baseline-snapshot.md`. Snapshots originate on
   each side's analysis branch. The manifest-writing step copies each snapshot
   into the workspace at this path. The snapshot contains metadata only, not
   source content. This makes the row's path resolve inside the root.

## Deliverables-Spec Mapping

Give each item of the configured deliverables spec one row: the spec item,
then the manifest row that embodies it or the status `not produced`. A `not
produced` row carries a one-line reason. A `not produced` row is not a gap.
Omit the table when no deliverables spec is configured.

## Claim Ownership

Each claim type has exactly one owner document:

| Claim type | Owner |
|---|---|
| System purpose, structure, and the material changes at system level | Business design |
| What changed for the operator in each workflow, and why | Before/after workflow narratives |
| Checkable upgraded behavior, assumptions, warranty scope, the functional-preservation statement, and the one statement of what was checked directly versus supported by comparison | Intended-behavior specification |
| Each open in-scope item, Blocked QA check, and SOW criterion not fully Met, each with one recommendation | Intended-behavior specification, `### Known issues and recommended follow-up` |
| Contractual satisfaction of each SOW acceptance criterion, and each client acceptance of a change outside SOW scope | SOW compliance walkthrough |
| Cost and hosting impact | Cloud/cost analysis |
| Every security finding, credential issue, and security recommendation | Appendix — Security narrative |
| What QA observed: check IDs, results, and verdicts | Appendix — QA report |
| Which document covers what, and the one-line package-level regression result | How to read this package |

Apply these rules to every client document:

1. State a claim in full only in its owner document.
2. Everywhere else, link to the owner by its table-of-contents title. Do not
   restate the claim.
3. **Evidence stays at the point of use.** An SOW criterion row and an
   intended-behavior `Basis` cell cite their own evidence. Never replace that
   citation with a link.
4. Two claims on one subject with different evidence strength are two claims.
   Never merge them. Merging keeps the stronger claim and drops the hedge.
5. Each document's H1 equals its table-of-contents title exactly.
6. A change visible inside a workflow belongs to the workflow narratives.
   Business design carries only system-level changes. State each change under
   one heading only.
7. State a client acceptance of a change outside SOW scope only in the SOW
   compliance walkthrough. State any other owner or client confirmation once,
   in the document that owns the claim it supports. Elsewhere, state the
   resulting fact without re-citing the confirmation.

## Length Budgets

Each client document has a word budget. The budget is a ceiling, not a target.
Never cut a warranted behavior, a scope or evidence hedge, a recommendation, a
finding, a warranty exclusion, a verification gap, or a SOW criterion to meet
it. Every `sow-authorized` or `client-accepted` change keeps a specification
row or exclusion bullet. Compute it as base + per-pair × pair count. Words are counted with `wc -w`
on the whole file, tables included.

| Document | Base | Per pair |
|---|---:|---:|
| How to read this package | 350 | 0 |
| Business design | 150 | 300 |
| Before/after workflow narratives | 50 | 275 |
| Intended-behavior specification | 300 | 1050 |
| SOW compliance walkthrough | 100 words per SOW acceptance criterion (100 with no SOW) | 0 |
| Cloud/cost analysis | 600 | 0 |
| Appendix — Security narrative | 150 | 900 |
| Appendix — QA report | 100 | 525 |

A writer without a shell estimates its document's word count before it
returns and reports the estimate with the budget. The
orchestrator measures each client document with `wc -w` after its stage
returns. When a document exceeds its budget by more than 20%, the orchestrator
respawns that stage once and names the measured overrun. The writer then cuts
detail by the rules of its own agent definition. When the document still
exceeds the budget with only protected content left, the writer returns the
overrun and its cause.

## Package Table of Contents

Use `deliverables/table-of-contents.md` as the client package's assembly order.
The downstream design step reads it from top to bottom to build the final client
deliverable. This gives every engagement's package the same opening order. The
manifest assembler writes it from the derived client-facing expected entries
above, in exactly that order. Include the table of contents itself as row 1.
Add one row per document with its order number and a relative markdown link
whose text is the document title (`[Business design](business-design.md)`).
Omit a `not-applicable` row and number the remaining rows consecutively.
List every other expected client document whether
or not it is present on disk. Record present/missing in the manifest, never
here. This file is client-facing and uses a client-deliverable banner. It
contains no internal entries.

## How to Read This Package

The manifest assembler writes `deliverables/how-to-read-this-package.md` after
every other client document exists. It is a reading guide, not a summary. It
contains:

1. One sentence naming the systems the package covers.
2. One short paragraph on the reading order: from the systems' purpose, to
   their changes, to acceptance evidence, to supporting detail. End it by
   saying that each document assumes the context of the documents before it.
3. A bulleted list of every client document in table-of-contents order. Each
   bullet is a markdown link with the document's title, plus one sentence on
   what the document answers. Group the bullets:
   - Context: business design and workflow narratives, as top-level bullets.
   - "If you are accepting the work": the intended-behavior specification and
     the SOW compliance walkthrough. Follow them with one sentence saying that
     both documents mark each statement's evidence strength. Link that
     sentence to the specification's `Verification evidence and warranty
     scope` section. Define nothing.
   - "Other supporting details": the cloud/cost analysis when present, both
     appendices, and the engagement team.
4. Inside the security appendix bullet, the delta synthesizer's
   package-level regression line, verbatim. It covers every audited dimension
   and ends with its caveat that the package is not an exhaustive list of
   pre-existing issues.

It carries no definitions, findings, obligations, or caveats beyond item 4.

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
