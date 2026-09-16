---
name: audit-remediation-research
description:
  "Contract for organizing an audit open-items queue into subsystem research,
  validating every item, correcting false or stale audit artifacts, and
  producing one draft-to-final index plus one detailed report per subsystem. Use
  when preparing, researching, reconciling, or finalizing remediation research."
---

# Audit Remediation Research

Load `auditor-conventions` first. Its truth gate for audit findings sets the
minimum admission standard. Apply the evidence standard below to consensus and fix
research in greater detail.

Run Stages 1–4. Run Stage 0 first when the output directory holds more than one
audit sample. The root orchestrator prepares and finalizes the index. One child
researches each subsystem. One final sibling reconciles shared audit artifacts.
No child spawns another agent.

## Run modes

The contract runs against an open-items queue from either source:

- **Comparative** — a delta produced the queue. Work items carry NEW or
  TRANSFORMED, a dependency closure exists, and a baseline snapshot is available.
  `PROVISIONAL` items mean that the queue's attribution is unsettled. Stop and
  report that state. Do not research unattributed findings. A `PRE-EXISTING`
  item in the work list also makes the queue defective. Exclude that item from
  work. Include it only as a `D`-numbered closure dependency.
- **Single-target** — one audit report produced the queue. Every item carries
  `OPEN`. The queue has no delta, baseline, or closure.

Mode changes which inputs exist, not the stages. This contract marks the full
delta, baseline report/summary, baseline snapshot, closure identifiers, and
disposition attribution as **comparative-only**. Single-target mode supplies
`not available` for those inputs. Skip every instruction that depends on them.
Never infer a baseline.

## Inputs and identity

Every stage receives the queue, the current report and summary, the exact
current snapshot identity, the available source root, and the index path. In
comparative mode, every stage also receives the full delta and the baseline
report, summary, and root. The current snapshot is a ref plus resolved SHA, or
a path explicitly recorded as a dirty tree. Stop when safe validation lacks an
artifact or identity required by the declared mode.

Use queue ordinals (`1`, `2`, `D1`) as canonical research identifiers. Use audit
finding IDs as provenance. In comparative mode, keep NEW/TRANSFORMED and
dependency closure separate throughout. Never present a closure item as
something the newer work introduced. Never include a closure item in a
regression count. A closure item enables work. Some closure items carry a
`PRE-EXISTING` original disposition.

## Evidence standard — mandatory at every stage

Treat every report, queue, delta, and consensus item as an untrusted claim until
the supplied snapshot proves it. More prose does not add rigor. Rigor means the
claim survives hostile checks against the implementation, reachable callers,
tests, repository rules, and authoritative external contracts.

Before retaining any item:

1. **Prove the population.** Enumerate finding rows and queue entries
   mechanically. Reconcile them with every stated total. A report whose header,
   tables, and summary disagree does not provide count evidence. Quarantine the
   disputed arithmetic instead of choosing a convenient number.
2. **Prove the path.** Read the exact construct, its production callers, and the
   tests that constrain it. If only an invalid object, hypothetical future
   implementation, or test-only bypass can reach a behavior, do not call it a
   current production defect unless that boundary is wrong.
3. **Prove the consequence.** Separate an observed failure or enforceable
   maintenance hazard from a technically true statement. Formatting, naming,
   optional micro-optimizations, intentional duplication, positive observations,
   and unmeasured performance or security speculation are not remediation work.
4. **Prove the contract.** Tests may establish that surprising behavior is
   deliberate. Repository rules may prohibit the proposed change. External API,
   framework, or platform claims require current authoritative documentation.
   Replace an unsupported assertion with the exact question that remains open.
5. **Prove identity and scope.** Match the underlying responsibility and failure
   mode, not a shared word, number, file, or technology. Do not label unrelated
   old and new concurrency, logging, credential, or storage mechanisms
   `TRANSFORMED` merely because they occupy the same category.
6. **Prove actionability.** Name a bounded change that closes the supported
   defect. Name a verification that can fail. If only part can close in scope,
   classify it `Partial`. If closure needs an unowned decision or unavailable
   system, classify it `Open`. Never present an in-repository containment step as
   full closure of an external trust or platform boundary.

Use precise language proportional to evidence. Replace “will,” “always,”
“unbounded,” “starves,” or “secure” when the snapshot proves only “can,”
“under this condition,” “has no fixed cap,” “can time out,” or “narrows
exposure.” Consensus is a candidate filter, not a verdict. Stage 2 must still
delete consensus items that fail this standard.

## Stage 0 — Consensus condensation (conditional)

Stage 0 runs only when the queue's directory holds more than one independent
audit sample of the same target. Each sample records a blind run by a different
model or session and has its own report, summary, or delta set. Count distinct
sample sets. Never infer a sample from filenames alone. Skip this stage with a
single set.

With multiple sets, stop. Ask the user whether to condense them into one
consensus queue before research. Never condense silently. Never proceed on
multiple queues silently. If the user declines, ask which single queue is
canonical.

If the user accepts, restate a preliminary plan with the samples found,
disagreements to research, exclusions in force, and output path. Get explicit
approval before starting work.

Before condensing, run the Evidence standard's population check on every sample.
Record the actual report-row count, queue-entry count, disposition count, and
whether the sample's own arithmetic closes. A malformed queue whose headline
claims more items than its standalone entries is not research-ready. Recover its
candidates for adjudication. Do not inherit its totals or structure.

Condensation rules:

- Include every item classified NEW or TRANSFORMED (comparative) or OPEN
  (single-target). Preserve each item's own attribution. Include an excluded
  item — UNCHANGED, PRE-EXISTING, or otherwise — only when the queue needs it to
  fix a queued item. Include that item as a closure entry, not a work item.
- When samples disagree, research the disputed claim against the current
  snapshot. Rule the claim valid or invalid. Never average, vote, or defer.
- Challenge agreements too. Independent reports can repeat the same unsupported
  premise. A detailed finding can still be false, unreachable, immaterial,
  duplicate, or intentionally tested behavior.
- Correct false positives and stale claims in the originating audit reports.
  Write the corrections in the present tense with no changelog framing.
- The caller supplies the exclusion list. Default to none. Excluded items appear
  only in a trailing Exclusions appendix, never in the body.

The consensus queue uses the same structure as a single-sample queue. Use the
disposition vocabulary of the declared mode. Write present-tense ground truth.
Include no sample, model, or report-difference commentary.

Write the consensus queue beside the samples as
`<queue-stem>-consensus-open-items.md`. Retain every source sample unmodified
except for factual corrections. Use the consensus queue as Stage 1's input. Do
not replace the source samples.

## Stage 1 — Prepare the draft index

The root orchestrator reads the queue and audit chain. It resolves the current
snapshot SHA or records a dirty tree. It groups candidates by the queue's
`Subsystem` field. It writes the unsuffixed index before spawning researchers.
A subsystem is the smallest stable runtime, component, or responsibility
boundary that owns the fix. It is not a dimension, severity, directory chosen
for convenience, or remediation phase.

If a queue lacks disposition, provenance, or subsystem, recover those fields from
the current report. In comparative mode, also use the full delta. Preserve
existing research slugs unless ownership is wrong. Use concise lowercase-hyphen
slugs. Resolve a collision with the narrowest stable parent boundary.

Use the queue's own path for the index stem. Replace `-open-items` with
`-fix-research`. Write all detailed reports beside the index as
`<index-stem>-<subsystem-slug>.md`. Before spawning, verify that every candidate
identifier occurs in exactly one assignment. Verify that every assigned report
path is unique.

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
mode, the closure column reads `n/a`. The draft contains no Ready/Partial/Open
counts, shared-cause conclusion, remediation order, or claim that the queue is
correct.

## Stage 2 — Research one subsystem

Spawn one researcher per subsystem. Put every independent assignment in a
single message. Include its slug, exact assigned identifiers, exclusive report
path, and complete input set. Researchers must treat the index and all audit
artifacts as read-only. Each researcher writes only its assigned report.

Truth-gate every assigned item:

- **Real:** reproducible evidence supports the defect.
- **True:** description, location, impact, dependencies, and constraints are
  accurate.
- **Current:** the defect exists in the supplied current snapshot.
- **Actionable:** a concrete change can close it.

Execute the Evidence standard for each item. In particular:

- Inspect all production callers and relevant tests, not only the cited lines.
- Distinguish an invalid direct-call test case from a reachable production path.
- Treat deliberate, test-protected behavior as a requirements question, not an
  implementation defect.
- Reject a style cleanup or allocation reduction unless evidence establishes a
  material behavior, maintenance, or measured resource consequence.
- Verify that a proposed abstraction removes real drift without coupling owners
  that intentionally differ.
- Preserve the original exception, cancellation, durability, security, and
  compatibility semantics in every proposal.
- State what the evidence does **not** prove. Do not turn a plausible runtime
  risk into measured incidence, guaranteed failure, or full compromise.

Amend an inaccurate but valid item in the proposal. Omit false, unsupported,
stale, duplicate, resolved, positive/no-action, or otherwise non-actionable
items from the report. Return each omission or upstream amendment only as a
factual correction candidate for reconciliation. Do not edit shared artifacts.

Open the subsystem report with its queue path, subsystem boundary, assigned and
researched counts, constraints, and shared root causes. Write valid queue items
in severity order. Write closure entries under `## Dependency closure`:

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
library, API, or advisory claims. Replace guesses with the exact question that
will settle them.

Return this compact update packet:

- Subsystem slug and report path.
- Assigned IDs and valid IDs, classified once as **Ready**, **Partial**, or
  **Open**. These outcomes are separate from evidence confidence.
- Correction candidates: identifier, supported correction, evidence, affected
  upstream artifacts, and disposition.
- Root causes, cross-subsystem dependencies/conflicts, open questions, and
  optional coupling to excluded findings.

After all researchers return, the root verifies that every expected report
exists. It verifies that every packet accounts for all assigned identifiers. It
rejects duplicate or unassigned identifiers. Re-run a failed subsystem once and
name the exact defect. Stop after a second failure. Never reconcile a partial
research set.

Count omissions as successful truth-gate outcomes, not researcher failures.
Remove every false, harmless, intentional, or non-actionable consensus item from
all active artifacts.

## Stage 3 — Reconcile shared artifacts

Spawn one reconciler sibling with every subsystem report and update packet.
Re-run researchers when a report is missing, contains an unassigned item,
duplicates another report, or lacks evidence. The reconciler must not silently
repair research. If the reconciler requests a re-run, run that subsystem once
with the defect named. Then re-run the reconciler. Stop after a second failure
of either assignment.

The reconciler is the sole writer of the current report, current summary, queue,
and — in comparative mode — the full delta. It validates correction candidates.
Then it applies each accepted correction from origin through derivatives:

1. Current audit report.
2. Current audit summary.
3. Full delta, comparative mode only: maps, dispositions, rollups, residual
   risk, arithmetic, and conclusions.
4. Queue: entries, closure, links, exclusions, and counts.

When Stage 0 condensed multiple samples, supply every originating report,
summary, delta, and queue that contains an accepted correction. Reconcile each
sample independently against its own finding population. If an artifact cannot
close because its source totals or mappings were already contradictory, mark it
prominently `UNRECONCILED — DO NOT USE FOR COUNTS OR REMEDIATION`. Preserve it
only for trace evidence. Make the consensus queue authoritative. Never invent a
remap or force arithmetic to preserve a source artifact's headline.

Keep `## Queue corrections` when anything changed. State the supported
correction, evidence, affected artifacts, and disposition without repeating a
disproved claim as fact. Do not include invalid items as active findings,
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

<!-- inputs; final counts — comparative: NEW/TRANSFORMED and closure counted
separately, plus excluded Critical/High findings; single-target: queued and
below-threshold counts -->

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
The root derives results only from structured returns. It does not re-research
findings. In single-target mode, the closure column reads `n/a`.

For each audit type, present the index and subsystem report paths, queue counts,
shared causes, and ordering constraints. Also present open questions,
corrections, reconciliation PASS/FAIL, and — in comparative mode — the excluded
Critical/High findings.

## Completion checks

- Delegation depth is one. Every researcher and reconciler is a direct child of
  the root orchestrator.
- Only the root writes the index. Each researcher writes only its report. The
  reconciler writes only shared audit artifacts.
- Every FINAL artifact contains only real, true, current, actionable findings.
- Every retained item records its production reachability, material consequence,
  relevant test contract, and the narrowest claim the evidence supports.
- Remove every omitted item from reports, summaries, deltas, queues, counts,
  residual risks, ordering, and active proposals. A correction note is not an
  active finding.
- Report, summary, queue, subsystem reports, index, and any delta reconcile.
- Comparative mode: Keep NEW/TRANSFORMED and closure attribution separate. Do
  not report a closure item as a regression. Do not research a PRE-EXISTING
  finding except as a named dependency.
- No production source or configuration file changed.
