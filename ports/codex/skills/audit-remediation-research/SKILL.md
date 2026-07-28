---
name: audit-remediation-research
description: "Contract for organizing an audit open-items queue into subsystem research, validating every item, correcting false or stale audit artifacts, and producing one draft-to-final index plus one detailed report per subsystem. Use when preparing, researching, reconciling, or finalizing remediation research."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->
# Audit Remediation Research

Run four stages. The root orchestrator prepares and finalizes the index; one
child researches each subsystem; one final sibling reconciles shared audit
artifacts. No child spawns another agent.

## Run modes

The contract runs against an open-items queue from either source:

- **Comparative** — the queue came from a delta. Items carry NEW or TRANSFORMED,
  a dependency closure exists, and a baseline snapshot is available.
- **Single-target** — the queue was derived from one audit report. Every item
  carries `OPEN`, there is no delta, no baseline, and no closure.

Mode changes which inputs exist, not the stages. Wherever this contract names
the full delta, the baseline report/summary, the baseline snapshot, closure
identifiers, or NEW/TRANSFORMED attribution, those are **comparative-only**: in
single-target mode they are supplied as `not available`, and every instruction
conditioned on them is skipped rather than approximated. Never infer a baseline.

## Inputs and identity

Every stage receives the queue, the current report and summary, the exact
current snapshot identity, the available source root, the index path, and — in
comparative mode — the full delta plus the baseline report, summary, and root.
The current snapshot is a ref plus resolved SHA, or a path explicitly recorded
as a dirty tree. Stop if an artifact or identity needed for safe validation is
missing for the declared mode.

Use queue ordinals (`1`, `2`, `D1`) as canonical research identifiers; audit
finding IDs are provenance. In comparative mode NEW/TRANSFORMED and
dependency-closure attribution remain separate throughout.

## Stage 1 — Prepare the draft index

The root orchestrator reads the queue and audit chain, resolves the current
snapshot SHA or records it as a dirty tree, groups candidates by the queue's
`Subsystem` field, and writes the unsuffixed index before spawning researchers.
A subsystem is the smallest stable runtime, component, or responsibility
boundary that owns the fix—not a dimension, severity, directory chosen for
convenience, or remediation phase.

For a queue missing disposition, provenance, or subsystem, recover those fields
from the current report and, in comparative mode, the full delta. Preserve
existing research slugs unless ownership is wrong. Use concise lowercase-hyphen
slugs; resolve a collision with the narrowest stable parent boundary.

The index stem is the queue's own path with `-open-items` replaced by
`-fix-research`. Write all detailed reports beside the index as
`<index-stem>-<subsystem-slug>.md`. Before spawning, verify every candidate
identifier occurs in exactly one assignment and every assigned report path is
unique.

The draft index is coordination state, not a finding verdict:

```markdown
# Fix Research — Index (<baseline> → <current>, or <current> alone)

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

Each candidate identifier appears in exactly one assignment. In single-target
mode the closure column reads `n/a`. The draft contains no Ready/Partial/Open
counts, shared-cause conclusion, remediation order, or claim that the queue is
correct.

## Stage 2 — Research one subsystem

Spawn one researcher per subsystem — every independent assignment in a single
message — with its slug, exact assigned identifiers, exclusive report path, and
the complete input set. The index and all audit artifacts are read-only to
researchers; each writes only its assigned report.

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
### <N>. [NEW | TRANSFORMED | CLOSURE | OPEN] <title>

- **Location:** `path:line`
- **Severity:** <level> **Effort:** <trivial | small | medium | large>
- **Root cause:** <underlying reason>
- **Proposed fix:** <concrete types, methods, files, and behavior>
- **Why this approach:** <alternatives and decision>
- **Trade-offs and risk:** <cost, compatibility, and affected callers>
- **Depends on / conflicts with:** <identifiers or "none">
- **Unblocks:** <closure entries only; omit from all other entries>
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

After all researchers return, the root verifies every expected report exists and
every packet accounts for all assigned identifiers, and rejects duplicate or
unassigned identifiers. Re-run a failed subsystem once with the exact defect
named. Stop after a second failure; never reconcile a partial research set.

## Stage 3 — Reconcile shared artifacts

Spawn one reconciler sibling with every subsystem report and update packet.
Researchers must be re-run if a report is missing, contains an unassigned item,
duplicates another report, or lacks evidence; the reconciler does not silently
repair research. If the reconciler requests a re-run, run that subsystem once
with the defect named and then re-run the reconciler; stop after a second
failure of either assignment.

The reconciler is the sole writer of the current report, current summary, queue,
and — in comparative mode — the full delta. It validates correction candidates,
then applies each accepted correction from origin through derivatives:

1. Current audit report.
2. Current audit summary.
3. Full delta, comparative mode only: maps, dispositions, rollups, residual
   risk, arithmetic, and conclusions.
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
# Fix Research — Index (<baseline> → <current>, or <current> alone)

> **STATUS: FINAL.** Reconciled against `<current-ref@sha-or-dirty-tree>`.

## 1. Scope and truth gate

<!-- inputs; final counts — comparative: NEW/TRANSFORMED and closure separately,
plus excluded Critical/High findings; single-target: queued and below-threshold
counts -->

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
In single-target mode the closure column reads `n/a`.

Then present per audit type: index and subsystem report paths, queue counts,
shared causes, ordering constraints, open questions, corrections, reconciliation
PASS/FAIL, and — comparative mode — the excluded Critical/High findings.

## Completion checks

- Delegation depth is one; every researcher and reconciler is a direct child of
  the root orchestrator.
- Only the root writes the index; only each researcher writes its report; only
  the reconciler writes shared audit artifacts.
- Every FINAL artifact contains only real, true, current, actionable findings.
- Report, summary, queue, subsystem reports, index, and any delta reconcile.
- Comparative mode: NEW/TRANSFORMED and closure attribution remain separate.
- No production source or configuration file changed.
