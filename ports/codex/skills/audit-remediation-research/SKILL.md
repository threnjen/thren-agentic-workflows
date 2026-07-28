---
name: audit-remediation-research
description: ""
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->
# Audit Remediation Research

Run four stages. The root orchestrator prepares and finalizes the index; one
child researches each subsystem; one final sibling reconciles shared audit
artifacts. No child spawns another agent.

## Inputs and identity

Every stage receives the queue, full delta, baseline/current reports and
summaries, exact snapshot identities, available source roots, and index path.
The current snapshot is a ref plus resolved SHA, or a path explicitly recorded
as a dirty tree. Stop if an artifact or identity needed for safe validation is
missing.

Use queue ordinals (`1`, `2`, `D1`) as canonical research identifiers; audit
finding IDs are provenance. NEW/TRANSFORMED and dependency-closure attribution
remain separate throughout.

## Stage 1 — Prepare the draft index

The root orchestrator reads the queue and audit chain, groups candidates by the
queue's `Subsystem` field, and writes the unsuffixed index before spawning
researchers. A subsystem is the smallest stable runtime, component, or
responsibility boundary that owns the fix—not a dimension, severity, directory
chosen for convenience, or remediation phase.

For a legacy queue missing disposition, provenance, or subsystem, recover those
fields from the full delta and current report. Preserve existing research slugs
unless ownership is wrong. Use concise lowercase-hyphen slugs; resolve a
collision with the narrowest stable parent boundary.

Write all detailed reports beside the index as
`<index-stem>-<subsystem-slug>.md`. The draft index is coordination state, not a
finding verdict:

```markdown
# Fix Research — Index (<baseline> → <current>)

> **STATUS: DRAFT — UNVALIDATED.** Candidate assignments below are not findings
> or remediation conclusions. Use only after status becomes FINAL.

## Inputs

<!-- queue, delta, reports, roots, refs/SHAs -->

## Candidate subsystem assignments

| Subsystem | Candidate queue IDs | Candidate closure IDs | Report   | Status  |
| --------- | ------------------- | --------------------- | -------- | ------- |
| <name>    | <IDs>               | <D-IDs>               | `<path>` | PENDING |

## Research results

Pending.

## Upstream corrections and reconciliation

Pending.
```

Each candidate identifier appears in exactly one assignment. The draft contains
no Ready/Partial/Open counts, shared-cause conclusion, remediation order, or
claim that the queue is correct.

## Stage 2 — Research one subsystem

Spawn one researcher per subsystem with its slug, exact assigned identifiers,
exclusive report path, and the complete input set. The index and all audit
artifacts are read-only to researchers; each writes only its assigned report.

Truth-gate every assigned item:

- **Real:** reproducible evidence supports the defect.
- **True:** description, location, impact, dependencies, and constraints are
  accurate.
- **Current:** the defect exists in the supplied current snapshot.
- **Actionable:** a concrete change can close it.

Amend an inaccurate but valid item in the proposal. Omit false, unsupported,
stale, duplicate, resolved, positive/no-action, or otherwise non-actionable
items from the report. Return each omission or upstream amendment only as a
factual correction candidate for reconciliation; do not edit shared artifacts.

Open the subsystem report with its queue path, subsystem boundary, assigned and
researched counts, constraints, and shared root causes. Write valid queue items
in severity order and closure entries under `## Dependency closure`:

```markdown
### <N>. [NEW | TRANSFORMED | CLOSURE] <title>

- **Location:** `path:line`
- **Severity:** <level> **Effort:** <trivial | small | medium | large>
- **Root cause:** <underlying reason>
- **Proposed fix:** <concrete types, methods, files, and behavior>
- **Why this approach:** <alternatives and decision>
- **Trade-offs and risk:** <cost, compatibility, and affected callers>
- **Depends on / conflicts with:** <identifiers or "none">
- **Unblocks:** <closure entries only; omit from NEW/TRANSFORMED entries>
- **Verification:** <named test or exact check>
- **Sources:** <URLs/doc references or "repository patterns only">
- **Confidence:** <high | medium | low; explain unless high>
```

Read every proposed location, relevant caller, test, and constraint. Prefer
repository patterns. Cite authoritative URLs for external platform, framework,
library, API, or advisory claims. Replace guesses with the exact settling
question.

Return this compact update packet:

- Subsystem slug and report path.
- Assigned IDs and valid IDs, classified once as **Ready**, **Partial**, or
  **Open**. These outcomes are separate from evidence confidence.
- Correction candidates: identifier, supported correction, evidence, affected
  upstream artifacts, and disposition.
- Root causes, cross-subsystem dependencies/conflicts, open questions, and
  optional coupling to excluded findings.

## Stage 3 — Reconcile shared artifacts

After all researchers finish, spawn one reconciler sibling with every subsystem
report and update packet. Researchers must be re-run if a report is missing,
contains an unassigned item, duplicates another report, or lacks evidence; the
reconciler does not silently repair research.

The reconciler is the sole writer of the current report, current summary, full
delta, and queue. It validates correction candidates, then applies each accepted
correction from origin through derivatives:

1. Current audit report.
2. Current audit summary.
3. Full delta: maps, dispositions, rollups, residual risk, arithmetic, and
   conclusions.
4. Queue: entries, closure, links, exclusions, and counts.

Keep `## Queue corrections` when anything changed. State the supported
correction, evidence, affected artifacts, and disposition without repeating a
disproved claim as fact. Invalid items appear nowhere as active findings,
proposals, ordering steps, residual risks, or aggregate counts.

The reconciler returns accepted/rejected correction candidates, changed paths,
final queue/closure identifiers and totals, still-excluded Critical/High
findings, and reconciliation status. It does not edit the index or subsystem
reports.

## Stage 4 — Finalize the index

The root orchestrator serially applies researcher packets and the reconciler
return to the draft index. Replace the draft body with:

```markdown
# Fix Research — Index (<baseline> → <current>)

> **STATUS: FINAL.** Reconciled against `<current-ref@sha-or-dirty-tree>`.

## 1. Scope and truth gate

<!-- inputs; final NEW/TRANSFORMED and closure counts separately; excluded
Critical/High findings -->

## 2. Subsystem reports

| Subsystem | Report | Queue IDs | Closure IDs | Ready | Partial | Open |

## 3. Shared root causes

## 4. Suggested remediation order

<!-- dependency first, then severity; name inversions -->

## 5. Open questions

## 6. Upstream corrections and reconciliation

## 7. Residual scope and risk
```

The subsystem table is the completeness ledger. Its union equals the corrected
queue exactly. Every valid identifier occurs in one report and one index row.
The root derives only from structured returns; it does not re-research findings.

## Completion checks

- Delegation depth is one; every researcher and reconciler is a direct child of
  the root orchestrator.
- Only the root writes the index; only each researcher writes its report; only
  the reconciler writes shared audit artifacts.
- Every FINAL artifact contains only real, true, current, actionable findings.
- Report, summary, delta, queue, subsystem reports, and index reconcile.
- NEW/TRANSFORMED and closure attribution remain separate.
- No production source or configuration file changed.
