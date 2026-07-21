---
name: phase-doc-sync
description: "Reconcile phase documents after any code fix, tweak, or small update made during phase work or phase QA. Use when: making fixes, tweaks, or small updates to a project that has a docs/phases/ directory; when the user references a phase QA doc, _QA.md checklist, QA failures, or asks for project fixes on a phase branch; after any change that alters what a phase delivers or how it behaves."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->

# Phase Document Sync

When code changes during phase work — QA fixes, tweaks, small updates — the phase documents must be reconciled in the same pass so they remain the ground truth for the project. A phase doc that describes the pre-fix behavior is a defect, even if the code is correct.

## The Contract

After completing any code change in a repo with a `docs/phases/` directory:

1. **Identify the affected phase.** Determine which phase the changed files belong to. Use the current branch name, the phase docs' scope/deliverables sections, or ask the user if genuinely ambiguous.
2. **Update the phase document.** Edit `docs/phases/PHASE_0N/PHASE_0N_SUMMARY.md` so every section it contains (scope, deliverables, acceptance criteria, technical decisions, What's New) describes the **current, post-change state** of the phase.
3. **Update the roadmap entry.** If the change alters anything visible at the roadmap level (scope, status, deliverables, dependencies), update this phase's entry in `docs/phases/PROJECT_ROADMAP.md` — or `docs/phases/PHASES_OVERVIEW.md` in legacy repos. Touch only this phase's section(s); never restructure or rewrite other phases.
4. **Update the QA doc if one exists.** If the phase has a QA plan (`[phase-name]_QA.md`) and the change alters a step's expected behavior, update that step to match the new behavior.

Load the `phase-document-writing` skill for the Phase Document Template and Phases Overview Template when the structure of a section needs to change.

## Baseline-Truth Rule (non-negotiable)

Write every doc update **as if the new state was always the plan**:

- Rewrite the affected sentences and bullets in place to describe the current behavior.
- **Never** add change-log framing: no "Updated:", "Changed from X to Y", "Fix:", "(revised)", dated notes, strikethrough, or a "Changes" / "History" section.
- Do not preserve the old wording alongside the new. The document has no memory; git history is the change log.

## Scope Discipline

- Sync only the sections affected by the change. Do not reformat, restyle, or "improve" untouched sections.
- If the change is purely internal (refactor, test fix) and alters nothing the phase docs describe, state that explicitly instead of making a no-op edit.
- If the change contradicts a phase's stated scope or acceptance criteria in a way that looks like scope creep rather than a fix, surface that to the user before rewriting the docs around it.

## Completion Check

A change made under this skill is not done until either:
- the affected phase doc(s) have been updated and re-read to confirm they describe the current state, or
- you have explicitly stated that no phase-doc content was affected and why.
