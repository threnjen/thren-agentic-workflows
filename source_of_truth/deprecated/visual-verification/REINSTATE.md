# Reinstating Visual Verification

Visual verification is extracted, not deleted. Nothing in `source_of_truth/` references it, so
it loads into no agent's context and fires from no trigger. This directory sits outside the
`source_of_truth/agents/*.md` glob at `scripts/propagate_master_assets.py:650`, so propagation
neither deploys it nor prunes it.

## What is here

| File | Was |
|---|---|
| `03g-unity-visual-verification.agent.md` | `source_of_truth/agents/03g-unity-visual-verification.agent.md` — the `Visual Verifier` agent, whole and unmodified |
| `phase-execute-step-3-visual-verification-gate.md` | `### Step 3` of `03-phase-execute.agent.md`, between `##### E. Complete` and `### Step 4: QA` |
| `unity-development-visual-verification-wiring.md` | `## Visual Verification Wiring` in `skills/unity-development/SKILL.md`, before `## Pre-Handoff Checklist (Unity-Specific)` |

The Unity capture package `packages/com.threnjen.visual-verification/` was left in place. It is a
UPM package on disk that no agent loads, so it costs no context. It still works.

## Restoring the three extracted files

1. `git mv` the agent back to `source_of_truth/agents/`.
2. Paste Step 3 back into `03-phase-execute.agent.md` between `##### E. Complete` and `### Step 4: QA`.
3. Paste the wiring section back into `unity-development/SKILL.md` before the Pre-Handoff Checklist.

## Restoring the references that pointed at them

Pasting the three files back is not enough. Fourteen references in eleven files were removed, and
the gate does not run without them. Each row below names the file, what to restore, and why it
mattered.

### `source_of_truth/agents/03-phase-execute.agent.md`

| Site | Restore |
|---|---|
| `agents:` roster | Add `Visual Verifier` after `Unity Reviewer`. Without this the agent is not spawnable. |
| Implementer spawn prompt | Append to the Unity sentence: `For a Unity feature contributing to the phase's visual acceptance criteria, follow` `unity-development` `→ Visual Verification Wiring before returning so the A1 checkpoint commits those inputs.` This is what commits capture inputs before the A1 checkpoint — a shadow worktree can only test committed inputs, so without it the gate reads a stale checkout. |
| Step 4b QA escalation | `exactly like the security scan.` → `exactly like the security scan and the visual gate.` |
| Step 4c staging rules | `The skill's staging rules exclude one artifact.` → `exclude two artifacts`, and re-add `The Step 6 checkpoint owns the Step 3 visual-verification report.` |
| Step 5 phase-close ordering | `Three things must complete first:` → `Four things`, re-adding `visual verification` after the integration test gate. |
| Step 6 `all-approved` inputs | `Four other results also feed it:` → `Five other results`, re-adding `the visual verification verdict from Step 3,` after the stage D gate. |
| Step 6 Prod Code Review substitutions | `Substitute three values:` → `Substitute four values:`, re-adding `the visual-verification verdict from Step 3 or its skip reason,` before the Step 5 phase-close result. |
| Fast-track prompt template | Re-add ` Visual verification: [Pass \| skip reason].` after the test-execution sentence. |
| Standard prompt template | Re-add ` Visual verification: [Pass \| Fail \| Unverified \| skip reason].` in the same position. |
| Step 6 final checkpoint | Re-add `the Step 3 visual-verification report,` to the aggregation list. |

**The Step 3 slot is no longer free.** After the gate was removed, the remaining steps were
renumbered to close the gap. The file now runs 1, 2, 3 (QA), 4 (Phase-Close Audits), 5 (Phase Final
Review), 6 (Report), 7 (Documentation).

Every step number in the table above, and in
`phase-execute-step-3-visual-verification-gate.md`, uses the **post-reinstatement** numbering, which
is the numbering the file had when the gate was removed. Reinstating the gate as Step 3 shifts
today's Steps 3 through 7 to 4 through 8 and makes those numbers correct again. Renumber first, then
restore the references. Find each site by its quoted text, not by its step number.

Two test modules also pin these headings and need the same shift:
`tests/test_phase_execute_contracts.py` and `tests/test_audit_comparison_contracts.py`.

### The plan flag — the actual entry point

The gate fired only for a plan carrying `visual_acceptance: yes`. Two files defined that flag, and
both must be restored or every plan is treated as non-visual:

- `agents/03o-feature-plan-author.agent.md` — re-add to the plan-contents sentence: ``Each plan carries the required `visual_acceptance: yes | no` flag. Set it to `yes` when an acceptance criterion states what must appear on screen. Never default a missing flag to `no`.``
- `skills/feature-plan-set/SKILL.md` — re-add the same flag definition plus `A plan without the flag fails validation. The executor never defaults a missing flag to `no`.`

A trigger-table row keyed on `visual_acceptance: yes` also has to exist under
`##### Per-feature review triggers` in `03-phase-execute.agent.md`. Note that at the time of
extraction that whole table was already absent from the file, which is why the gate had not been
firing at all.

### Other source files

- `skills/unity-development/SKILL.md` — the PlayMode flags row read `| PlayMode and visual capture |`; the Pre-Handoff Checklist had an item 7, `**Visual test wired** — For a View feature with visual ACs, is the capture config present for this scene and the capture package a dependency listed under `testables`? Is the scene in Build Settings with a `MainCamera`? See "Visual Verification Wiring".`
- `instructions/tech-stack-detection.instructions.md` — re-add `**/03g-unity-visual-verification.agent.md,` to the `applyTo` glob.
- `skills/phase-document-writing/SKILL.md` — the visual-criteria template item ended `so a reviewer or the Visual Verifier can judge each against a rendered frame]`.

### Editor discovery — read this before restoring

The Visual Verifier's Step 1 owned the Unity editor-path resolution ladder, and
`unity-development/SKILL.md` delegated to it for **every** Unity test run, EditMode included.
Removing the agent would have broken ordinary Unity testing, so that ladder was inlined into the
skill's Test Execution section and the skill now declares itself the single canonical
implementation.

On reinstatement, do not restore the old delegation. Two copies of the ladder is the duplication
the original contract existed to prevent. Leave discovery in the skill and have the agent read it
from there.

`VISUAL_VERIFICATION_UNITY` and `dev/com.threnjen.visual-verification.local.json` kept their
historical names in the skill so existing machine configuration keeps working, despite no longer
being capture-specific.

## Tests

Deleted rather than left to pass vacuously on absent text:

- `test_phase_execute_contracts.py` (formerly `test_review_trigger_tables.py`) — `Visual Verifier` roster entry, the `visual_acceptance` parameter and its predicate branch, `test_visual_verifier_uses_the_required_plan_flag`, `_visual_flag_errors`, `test_visual_plan_flag_guard_is_load_bearing`. `test_visual_and_security_rows_have_one_entry_point` was narrowed to the security row and renamed `test_security_row_has_one_entry_point`.
- `test_unity_consumer_contract.py` — the `visual_verifier` consumer entry (and its `len(CONSUMER_PATHS)` count, 3 → 2), `_visual_verifier_errors`, `_phase_visual_gate_errors`, `test_phase_execute_visual_gate_commit_contract`, `test_visual_verifier_invocation_contract`, and both parametrized mutation blocks.
- `test_unity_skill_contract.py` — the editor-discovery contract was **inverted**, not deleted. It asserted the skill must *not* copy `VISUAL_VERIFICATION_UNITY`; it now asserts the skill *must* own the ladder. Three mutation rows were retargeted onto the inverted obligations. Restoring the old delegation means re-inverting this, which the discovery note above advises against.
- `test_model_routing.py`, `test_agent_renumbering.py` — one row each for `03g`.

## Why it was disabled

It never fired in practice. Commenting out Step 3 was tried first and was worse: it removed the
destination while leaving all ten pointers to it, and the contract tests kept passing because they
locate the section by splitting on its heading string, which an HTML comment does not change.
