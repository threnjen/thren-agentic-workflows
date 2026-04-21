# Project Learnings

## 2026-04-21 - Phase Refiner next-step routing mismatch

- Problem: Phase refiner guidance routed users directly to Execute (04) even when the intended next manual step was Feature Decomposer (03), and some Claude agent next-step prompts used non-Claude agent handles.
- Root cause: Pipeline language diverged across parallel agent definition sets (.github vs claude), and user-facing "what to do next" strings were not kept in sync with naming conventions.
- Fix: Updated phase refiner pipeline/next-step text to route to Feature Decomposer first; updated Claude feature decomposer next-step handles to use Claude agent names.
- Watch for: Any instruction sentence that starts with "open a new chat with" or "run @..." should be validated against the naming scheme of that agent set.

## 2026-04-21 - Claude next-step handle normalization

- Problem: A Claude user-facing next-step message referenced `@phase-execute`, which does not match the configured Claude phase execution handle.
- Root cause: Handle naming mixed shorthand and configured numbered Claude agent names.
- Fix: Updated standalone next-step guidance to use `@04-phase-execute`.
- Watch for: In Claude agent docs, verify next-step mentions against the `name:` field in the target agent file before merging wording changes.
