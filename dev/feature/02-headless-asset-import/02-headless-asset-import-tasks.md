# Feature Tasks: Headless Asset Import

## Stage 1: Asset Contract Guards

- [x] Confirm `01-unity-test-execution-contract` is complete, read its final context/tasks/implementation artifacts, and resolve the actual shared Unity guard filename before editing.
- [x] In `tests/[PROPOSED - name TBD: Unity skill contract guards]`, add a scoped guard that parses the Serialized Assets section and verifies the plain import command includes `-batchmode`, `-quit`, `-projectPath <path>`, and `-logFile -` without `-runTests` (AC1, AC6).
- [x] Add a guard proving the plain import procedure remains separate from and does not remove the existing `-batchmode -executeMethod <Type>.<Method> -quit` asset-construction procedure (AC1, AC2, AC6).
- [x] Add a guard preserving the Unity-generated serializer/GUID authority boundary and the prohibition on hand-authoring serialized YAML (AC2, AC6).
- [x] Add a source-wide contradiction sweep derived from tracked files under `source_of_truth/`; assert at least one file was inspected and distinguish prohibited human/GUI-open requirements from valid “Editor API” and “Unity Editor serializer” language (AC3, AC6).
- [x] Add a source-wide path sweep that asserts `Assets/Tests/EditMode` is absent, the corrected `Assets/Tests/Editor` guidance is discoverable, `Assets/Tests/PlayMode` remains present, and the file enumeration is non-empty (AC4, AC6).
- [x] Prove every new guard red by targeted deletion or negation of its protected mechanism, record which mutation failed which obligation, and restore the fixture/source before proceeding (AC6).

## Stage 2: Serialized Asset and Test-Path Guidance

- [x] Extend `source_of_truth/skills/unity-development/SKILL.md` under `## Serialized Assets: Generate via Unity, Never Hand-Author` with one concise plain import procedure using `Unity -batchmode -quit -projectPath <path> -logFile -` (AC1).
- [x] State that the headless import performs asset-database import and missing `.meta`/GUID generation without requiring a human-opened or GUI-opened Editor (AC1, AC3).
- [x] Preserve Unity as the only authority that generates serialized assets and GUIDs; do not add any exception allowing hand-authored `.meta` files or serialized YAML (AC2).
- [x] Preserve the existing `-batchmode -executeMethod <Type>.<Method> -quit` procedure for Unity Editor API asset-construction scripts as a separate operation (AC1, AC2).
- [x] Replace the assembly-reference example's `Assets/Tests/EditMode` path with the verified reference-project `Assets/Tests/Editor` convention without presenting it as universal (AC4).
- [x] Replace the Refactor/Rewire inventory's `Assets/Tests/EditMode` path with `Assets/Tests/Editor` and leave `Assets/Tests/PlayMode` guidance unchanged (AC4).
- [x] Run the focused shared guard module and confirm AC1–AC4 and AC6 are green while Feature 01's Test Execution guards remain green.

## Stage 3: Headless Import Verification

- [ ] Verify the external target is `/Users/jennywadkins/github_repos/the-movies`, its `ProjectSettings/ProjectVersion.txt` reports Unity `6000.3.13f1`, and its working tree is clean before any mutation (AC5). — blocked: target/version were verified, but unrelated untracked Phase 08O planning artifacts make the working tree non-clean.
- [x] Resolve the Unity 6000.3.13f1 executable through the finalized editor-discovery procedure; do not assume a bare `Unity` command or persist the machine-specific path (AC5).
- [ ] Select one validated, tracked asset with a recoverable `.meta` file; record its exact path and restoration method before moving or otherwise withholding only that `.meta` file (AC5). — skipped because the clean-tree precondition failed.
- [x] If no safe single-file mutation or Unity executable is available, do not modify the external project; record AC5 as unverified with the concrete reason and skip the remaining mutation steps.
- [ ] If safe verification is available, run the documented headless import with `-batchmode -quit -projectPath /Users/jennywadkins/github_repos/the-movies -logFile -` and record that no GUI opened, the process outcome, and relevant log evidence (AC5). — not executed because the clean-tree precondition failed.
- [ ] Verify Unity regenerated the controlled missing `.meta` file and that the result is Unity-authored; do not hand-create or commit it (AC2, AC5). — unverified; no `.meta` was withheld.
- [ ] Restore the controlled scenario exactly and require `git -C /Users/jennywadkins/github_repos/the-movies status --short` to return clean; if it does not, stop and report the residual paths rather than broad-cleaning the repository (AC5). — no controlled mutation occurred; the pre-existing unrelated untracked planning paths remain and were reported without cleanup.

## Stage 4: Regression Verification

- [x] Re-run `uv run pytest tests/[PROPOSED - name TBD: Unity skill contract guards]` using the final filename and record the focused pass/fail counts.
- [x] Re-run the targeted deletion/negation mutation checks and confirm every structural guard still fails for its intended reason, then restore the green state (AC6).
- [x] Sweep all tracked `source_of_truth/` files again and confirm no human/GUI-open requirement for `.meta` generation and no `Assets/Tests/EditMode` occurrence remains (AC3, AC4).
- [x] Re-read Feature 01's finalized `## Test Execution` section and run its guards to confirm the import-specific use of `-quit` did not permit `-quit` with `-runTests`, alter platform flags, or change `-testFilter` semantics.
- [x] Run `uv run pytest tests/` and compare the result with the captured baseline of 141 passes and the two unrelated failures; identify any additional failure as feature-caused until resolved or explained.
- [x] Confirm no files under `ports/` or `.github/` were edited and do not run propagation; report any sync-only failures as maintainer propagation pending.
- [x] Record the final AC1–AC6 evidence, including an explicit verified/unverified outcome for AC5 and final cleanliness evidence for the external project.
