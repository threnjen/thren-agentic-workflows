# Phase 05 Discovery Context

## Source Material

- `slim-implementation-pipeline.md` is a behavioral reference copied from another project fork.
- The reference document is not an acceptance contract for this repository.
- Its branch status, fixed agent counts, phase links, and implementation history do not apply here.
- The branch `phase/phase-05e-descendant-ownership-closure-05d-phase-close` also belongs to that external fork and is outside this phase's evidence.

## Current Repository Baseline

- The current repository exposes `04 PR - Review` as its local pre-PR review command.
- The current command owns base confirmation, evaluator fan-out, readiness synthesis, and optional forge posting.
- Phase 04 will remove the close-review chorus from Phase Execute before this phase changes the local command.
- Agent counts must be derived from the finished source tree. No external count is a deletion target.

## Decisions Carried Into This Phase

- Split execution slimming and local-review unification into separate phases.
- Make this phase depend on Phase 04.
- Use `phase-final-checks` as the primary command and preserve `pr-review` as an alias.
- Keep the workflow local and advisory until the user explicitly requests one repair pass.
- Emit aliases only on Claude, Codex, OpenCode, and Cursor. GitHub keeps its native mirrored agent surface.
- Make local validation and repair independent of phase plans and implementation records.
- Exclude unrelated Bash standards, model-routing changes, and wholesale prose rewrites.
- Preserve Audit, Test, Wrap-up, and Prod Code Review behavior except for required reference updates.

## Verification Guidance

- Verify every behavior against the current source before implementation.
- Treat source display names as agent identity. Do not infer identity from numbered filenames.
- Search for both producer and consumer references before retiring an evaluator.
- Use filesystem-safe report paths across all supported platforms.
- Preserve the pre-repair readiness report and write repair outcomes separately.
- Stop after source edits with propagation pending.
