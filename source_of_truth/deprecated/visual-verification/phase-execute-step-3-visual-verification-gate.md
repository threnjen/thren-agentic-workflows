# Extracted from `source_of_truth/agents/03-phase-execute.agent.md`

This step sat between `##### E. Complete` (end of Step 2) and `### Step 4: QA`.

### Step 3: Visual Verification Gate (conditional)

This step produces runtime visual evidence for a phase that renders something. It catches the class of defect that compiles clean: invisible or miscolored output, broken scene wiring, and blank frames.

The per-feature trigger table is the sole entry condition for **Visual Verifier**. This section executes a firing Visual Verifier row. It adds no competing trigger. A plan with `visual_acceptance: no` does not enter this section.

For a plan with `visual_acceptance: yes`, resolve the capture config and the phase visual acceptance criteria. Two conditions end the step early:

- If the repository is not a Unity project, record `visual-verification: not a Unity project` and skip.
- If the config or the required package wiring is absent, record `visual-verification: not configured (capture inputs missing at implementation checkpoint)`, set `all-approved: no`, and skip.

Visual Verification Wiring belongs to the responsible Feature Implementer, before its A1 checkpoint. Never create or modify capture inputs after the wave checkpoints. A shadow worktree can test only committed inputs.

When the Visual Verifier row fires and its inputs are available, spawn the **Visual Verifier** subagent:

> "[SUBAGENT-MODE] Run the visual verification gate for phase [phase-name]. Visual acceptance criteria from the phase document: [list each visual AC verbatim]. Capture config path: [resolved path]. Produce the deterministic screenshots via the repository's documented visual-verification run, then assess each visual AC against the rendered frames. Write the report to `docs/phases/[phase-name]/[phase-name]-visual-verification.md` and return a verdict (`Pass` | `Fail` | `Unverified`) with per-AC results and the artifact paths."

After the subagent returns, record the verdict as `visual-verification: Pass | Fail | Unverified`. Then act on it:

- **On `Fail`, remediate once.** This is the same bounded retry the review loop uses for "Changes Requested". Re-spawn the Feature - Implementer responsible for the rendering. Give it the Visual Verifier's per-AC findings and the rendered frames. Then re-run the Visual Verifier on the same config. Retry **at most once**. If the verdict is still `Fail`, record it and proceed. The blocker escalates to the Phase Final Review (Step 6). Use this implementer prompt:
  > "[SUBAGENT-MODE] The visual verification gate failed for phase [phase-name]. Failing visual acceptance criteria, and what the rendered frames actually show: [paste the Visual Verifier's per-AC findings]. Rendered frames: [artifact paths]. Fix the rendering so these acceptance criteria are met. Do NOT edit the capture config or the visual ACs to force a pass — fix what is on screen. Return what you changed."
- **Do not retry `Unverified`.** The capture could not run, or the images were not assessable. That is a setup problem, not a rendering problem. Record it and proceed.
- If the final verdict is `Fail` or `Unverified`, set `all-approved: no`. The Phase Final Review (Step 6) then runs in standard mode, not fast-track mode, and flags it as a blocker. A blank or missing frame is a `Fail`, not an `Unverified`.

This step emits no checkpoint of its own. The Phase Final Review checkpoint (Step 6) owns the report file and stages it. The generated screenshots and manifest are build artifacts. Do not commit them.
