---
name: audit-comparison
description: "Runs the caller-neutral sequence for independent multi-target audits, per-type deltas, attribution, reconciliation, and worktree cleanup. Use when a caller supplies audit targets and comparison inputs."
user-invocable: false
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->

# Audit Comparison

Reusable mechanism for comparing audit snapshots. Callers provide the targets,
scope, audit types, paths, and prompt content; caller-specific selection,
retry, continuation, remediation, and presentation policy stays outside this
skill.

## Inputs

Require these explicit inputs:

- `output_root`: the newer working checkout, or a caller-approved override.
  Every report, summary, delta, queue, and attribution update is written below
  this root. Never write comparison artifacts into a temporary baseline
  worktree.
- `audit_matrix`: one independent row per audit type and target, including the
  audit name, target root, snapshot label, report paths, summary paths, and
  caller-supplied scope and intent.
- `audit_prompt_template`: one template rendered once per matrix row. Across
  snapshots, only `target_root`, `snapshot_label`, and `output_directory` may
  vary. Scope and intent clauses remain byte-identical.
- `ref_targets`: repository roots and refs, with the resolved commit for every
  ref and lifecycle state for any materialized worktree.

Before spawning any child, verify that every report, summary, delta, queue,
attribution update, and output directory resolves below `output_root`. Reject
an escaping path or any path inside a read-only baseline tree; return the
concrete path-validation failure without writing an artifact.

Use the [Multi-Target Audits](../auditor-conventions/SKILL.md#multi-target-audits)
contract for comparability, independent runs, labels, layout, and read-only
target trees.

## Sequence

### 1. Resolve output root

Resolve the newer working checkout or the explicit override before spawning any
auditor. Keep all artifacts for every target under that one root. If the
current checkout is dirty, carry the non-reproducibility limitation through the
returned state; never stash, switch, reset, or otherwise mutate it.

### 2. Materialize ref targets

Resolve each ref to a commit and record both values. For each ref target,
invoke [Baseline Worktree](../../agents/04a-baseline-worktree.agent.md) with
the repository root and resolved commit, then use only its returned absolute
root. Return materialization failures with their concrete remediation after
cleaning any worktree this run already created; do not invent continuation
policy.

Keep a worktree created by this run available through audits, delta, and
attribution. Invoke the Baseline Worktree cleanup handshake only after the
last attribution result returns. Never remove a reused worktree. Follow
[worktree-baseline](../worktree-baseline/SKILL.md) for lifecycle ownership,
read-only etiquette, and failure handling.

### 3. Execute the audit matrix

Apply the linked Multi-Target Audits contract when rendering and dispatching
every row. Render each row from the one prompt template, validate each
snapshot pair so only `target_root`, `snapshot_label`, and `output_directory`
differ and scope and intent bytes match exactly, then dispatch the matrix cells
as one sibling spawn set. Each cell writes its full findings report and summary
to its own snapshot paths. Verify both artifacts for every cell before the
delta transition and preserve stated totals without interpreting movement.

Keep each audit type in its own report pair, delta, queue, reconciliation
arithmetic, provisional population, and attribution count domain. Never
produce a cross-type delta or combined count.

### 4. Gate and run each delta

For each audit type and comparison pair, verify both snapshot artifacts are
present, are full findings reports rather than summaries or partial returns,
and state their own totals. A missing, summary-only, partial, or internally
unusable report is a concrete gate failure; do not spawn `Auditor - Delta` for
that pair.

After the gate, spawn one delta per audit type and pair using the
[audit-delta-report](../audit-delta-report/SKILL.md) contract. Verify that both
the full delta and open-items queue exist and that reconciliation closes
against both source reports before returning any conclusion. The delta's
unattributed population remains provisional until attribution completes; do
not present it as a regression.

### 5. Settle attribution

If no baseline root is available, apply the `UNVERIFIED-ORIGIN` outcome defined
by `audit-delta-report` and do not spawn attribution. If the delta has no
provisional items, skip attribution cleanly.

Otherwise, batch provisional items by subsystem and send each item to exactly
one batch, dispatching all batches for the comparison set as one sibling spawn
set. Before accepting results, verify that batches are disjoint and that
their assigned-item counts sum exactly to the delta's unattributed total.
Attribution probes both trees and settles the delta and queue under the
document contract; no item is presented as `NEW` or as a regression until the
probe returns. Reject a missing, overlapping, incomplete, or unreconciled
batch result as a concrete failure, then continue to the release stage before
returning it.

After attribution, verify that no provisional marking remains and that the
queue contains only settled `NEW` and `TRANSFORMED` work items. The attribution
stage is complete when the no-baseline outcome or empty provisional set is
recorded, or when all attribution batches are accepted.

### 6. Release materialized worktrees

After the attribution stage completes—or is skipped because no baseline or
provisional items exist—perform the cleanup handshake for worktrees created by
this run and record whether cleanup succeeded. On a terminal materialization,
matrix, gate, delta, reconciliation, or attribution failure, wait for any
already-started child to return and run this same cleanup before returning the
failure. Cleanup never precedes the last baseline-tree probe and never removes
a reused worktree.

## Returned state

Return evidence for every audit type and pair, including:

- the output root and all report, summary, delta, and queue paths;
- resolved ref commits and target roots, including dirty-checkout limits;
- full-report gate, delta reconciliation, unattributed total, attribution
  batch reconciliation, and settled outcomes;
- each worktree's created/reused state and cleanup status after attribution or
  an early terminal failure; and
- concrete materialization, gate, reconciliation, attribution, or cleanup
  failures, without choosing the caller's retry or continuation policy.

Do not add normal-path logs or persistent orchestration state. These paths,
stated totals, gate results, reconciliation evidence, attribution results, and
cleanup status are the operational evidence surface.
