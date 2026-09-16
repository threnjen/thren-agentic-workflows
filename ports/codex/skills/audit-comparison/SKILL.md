---
name: audit-comparison
description: "Runs the caller-neutral sequence for independent multi-target audits, per-type deltas, attribution, reconciliation, and worktree cleanup. Use when a caller supplies audit targets and comparison inputs."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->
# Audit Comparison

This skill provides a reusable mechanism for comparing audit snapshots. Callers
provide the targets, scope, audit types, paths, and prompt content. Keep
caller-specific selection, retry, continuation, remediation, and presentation
policy outside this skill.

## Inputs

Require the following inputs:

- `output_root`: the newer working checkout, or a caller-approved override.
  Every report, summary, delta, queue, and attribution update is written below
  this root. Never write comparison artifacts into a temporary baseline
  worktree.
- `audit_matrix`: one independent row per audit type and target, including the
  audit name, target root, snapshot label, report paths, summary paths, and
  caller-supplied scope and intent.
- `audit_prompt_template`: use one template for each matrix row. Across
  snapshots, vary only `target_root`, `snapshot_label`, and `output_directory`.
  Keep scope and intent clauses byte-identical.
- `ref_targets`: repository roots and refs, with the resolved commit for every
  ref and lifecycle state for any materialized worktree.

Before spawning any child, verify that every report, summary, delta, queue,
attribution update, and output directory resolves below `output_root`. Reject
an escaping path or any path inside a read-only baseline tree. Return the
concrete path-validation failure without writing an artifact.

Use the [Multi-Target Audits](../auditor-conventions/SKILL.md#multi-target-audits)
contract for comparability, independent runs, labels, layout, and read-only
target trees.

## Sequence

### 1. Resolve output root

Resolve the newer working checkout or the explicit override before spawning any
auditor. Keep all artifacts for every target under that one root. If the
current checkout is dirty, record the non-reproducibility limitation in the
returned state. Never stash, switch, reset, or otherwise mutate the checkout.

### 2. Materialize ref targets

Resolve each ref to a commit. Record each ref and its resolved commit. For each
ref target, invoke [Baseline Worktree](../../agents/04a-baseline-worktree.agent.md)
with the repository root and resolved commit. Use only its returned absolute
root. After cleaning any worktree this run created, return each materialization
failure with its concrete remediation. Do not invent continuation policy.

Keep a worktree created by this run available through audits, delta, and
attribution. Invoke the Baseline Worktree cleanup handshake only after the
last attribution result returns. Never remove a reused worktree. Follow
[worktree-baseline](../worktree-baseline/SKILL.md) for lifecycle ownership,
read-only etiquette, and failure handling.

### 3. Execute the audit matrix

Apply the linked Multi-Target Audits contract to every row. Render each row from
the one prompt template. Validate each snapshot pair so only `target_root`,
`snapshot_label`, and `output_directory` differ.
Ensure that scope and intent bytes match exactly. Dispatch the matrix cells as
one sibling spawn set. Each cell writes its full findings report and summary to
its own snapshot paths. Verify both artifacts for every cell before the delta
transition. Preserve stated totals without interpreting movement.

Keep each audit type in its own report pair, delta, queue, reconciliation
arithmetic, provisional population, and attribution count domain. Never
produce a cross-type delta or combined count.

### 4. Gate and run each delta

For each audit type and comparison pair, verify that both snapshot artifacts
are present. Verify that each artifact is a full findings report rather than a
summary or partial return. Verify that each report states its own totals. Treat
a missing, summary-only, partial, or internally unusable report as a concrete
gate failure. Do not spawn `Auditor - Delta` for that pair.

After the gate, spawn one delta per audit type and pair using the
[audit-delta-report](../audit-delta-report/SKILL.md) contract. Verify that the
full delta and open-items queue exist. Verify that reconciliation closes
against both source reports before returning any conclusion. Keep the delta's
unattributed population provisional until attribution completes. In this state,
do not present it as a regression.

### 5. Settle attribution

If no baseline root is available, apply the `UNVERIFIED-ORIGIN` outcome defined
by `audit-delta-report`. Do not spawn attribution. If the delta has no
provisional items, skip attribution.

Otherwise, batch provisional items by subsystem. Send each item to exactly one
batch. Dispatch all batches for the comparison set as one sibling spawn set.
Before accepting results, verify that batches are disjoint. Verify that their
assigned-item counts sum exactly to the delta's unattributed total. Use
attribution to probe both trees. Use attribution to settle the delta and queue
under the document contract. Do not present an item as `NEW` or as a regression
until the probe returns. Reject a missing, overlapping, incomplete, or
unreconciled batch result as a concrete failure. Continue to the release stage
before returning the failure.

After attribution, verify that no provisional marking remains. Verify that the
queue contains only settled `NEW` and `TRANSFORMED` work items. Mark the
attribution stage complete after recording the no-baseline outcome or empty
provisional set, or after accepting all attribution batches.

### 6. Release materialized worktrees

After the attribution stage completes, run the cleanup handshake for worktrees
created by this run. Run it after you skip attribution because no baseline or
provisional items exist. Record whether cleanup succeeded. If a terminal materialization,
matrix, gate, delta, reconciliation, or attribution failure occurs, wait for
any already-started child to return. Run this same cleanup before returning the
failure. Cleanup never precedes the last baseline-tree probe. Cleanup never
removes a reused worktree.

## Returned state

Return evidence for every audit type and pair, including:

- the output root and all report, summary, delta, and queue paths.
- resolved ref commits and target roots, including dirty-checkout limits.
- full-report gate, delta reconciliation, unattributed total, attribution
  batch reconciliation, and settled outcomes.
- each worktree's created/reused state and cleanup status after attribution or
  an early terminal failure.
- concrete materialization, gate, reconciliation, attribution, or cleanup
  failures, without choosing the caller's retry or continuation policy.

Do not add normal-path logs or persistent orchestration state. These paths,
stated totals, gate results, reconciliation evidence, attribution results, and
cleanup status form the operational evidence surface.
