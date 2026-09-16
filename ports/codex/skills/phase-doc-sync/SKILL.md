---
name: phase-doc-sync
description: "Reconcile phase documents after any code fix, tweak, or small update made during phase work or phase QA. Use when: making fixes, tweaks, or small updates to a project that has a docs/phases/ directory; when the user references a phase QA doc, _QA.md checklist, QA failures, or asks for project fixes on a phase branch; after any change that alters what a phase delivers or how it behaves."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->
# Phase Document Sync

During phase work, reconcile the phase documents in the same pass after any code change. Include QA fixes, tweaks, and small updates. The phase documents must remain the project's ground truth. A phase document that describes pre-fix behavior is a defect, even when the code is correct.

## The Contract

After completing any code change in a repo with a `docs/phases/` directory:

1. **Identify the affected phase.** Determine which phase owns the changed files. Use the current branch name or the phase documents' scope and deliverables sections. Ask the user when the phase remains genuinely ambiguous.
2. **Update the phase document.** Edit `docs/phases/PHASE_0N/PHASE_0N_SUMMARY.md`. Ensure that every section in the document describes the **current, post-change state** of the phase. Apply this requirement to scope, deliverables, acceptance criteria, technical decisions, and What's New.
3. **Update the roadmap entry.** If the change alters anything visible at the roadmap level (scope, status, deliverables, dependencies), update this phase's entry in `docs/phases/PROJECT_ROADMAP.md`. Use `docs/phases/PHASES_OVERVIEW.md` in legacy repos. Touch only this phase's section(s). Never restructure or rewrite other phases.
4. **Update the QA docs if they exist.** Check whether the phase has a manual QA plan (`docs/phases/PHASE_0N/PHASE_0N_QA.md`) or an automated QA document (`docs/phases/PHASE_0N/PHASE_0N_QA_AUTOMATED.md`). Update the affected step when the change alters its expected behavior. If the change alters an automated check's expected result, clear that check's status. The changed expected result invalidates the recorded run. The runner must produce a fresh one.

Load the `phase-document-writing` skill when the structure of a section needs to change. Use its Phase Document Template and Phases Overview Template.

## Baseline-Truth Rule (non-negotiable)

Treat every document update **as if the new state had always been the plan**:

- Rewrite the affected sentences and bullets in place to describe the current behavior.
- **Never** add change-log framing. Do not add "Updated:", "Changed from X to Y", "Fix:", "(revised)", dated notes, strikethrough, or a "Changes" / "History" section.
- Do not preserve the old wording alongside the new. The document has no memory. Git history is the change log.

## Scope Discipline

- Sync only the sections affected by the change. Do not reformat untouched sections. Do not restyle untouched sections. Do not "improve" untouched sections.
- If the change is purely internal (refactor, test fix) and alters nothing the phase documents describe, state that explicitly. Do not make a no-op edit.
- Treat a change that contradicts the phase's stated scope or acceptance criteria as possible scope creep. Surface the possible scope creep to the user before rewriting the docs around it.

## Completion Check

Complete a change under this skill only after one of these conditions holds:
- You updated and reread the affected phase doc(s) and confirmed that they describe the current state, or
- You explicitly stated that no phase-doc content was affected and why.
