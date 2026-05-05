# 03 Branch Lifecycle Migration Tasks

## Stage 1: Add Branch-Open Block to `02 Phase - Refiner`

- [ ] Add a new final section to `.github/agents/02-phase-refiner.agent.md` for the post-affirmation branch-open flow instead of folding the steps into an existing phase.
- [ ] Document absolute target-repo path confirmation, phase-slug derivation, and branch creation with the fallback to `git checkout phase/<slug>` when the branch already exists.
- [ ] Include all required branch-open sub-actions in order: branch creation, hook symlink install, `eval/runs/<phase-slug>/` directory creation, and idempotent `.gitignore` update.
- [ ] Use the exact `ln -sfn <absolute-path-to-github-agents-source-of-truth>/eval/hooks/post-commit.sh <target-repo>/.git/hooks/post-commit` command followed by `chmod +x <target-repo>/.git/hooks/post-commit`.
- [ ] Add the path-assumption risk note and the one-command reinstall guidance next to the symlink instructions.
- [ ] Read the updated master file and confirm AC1, AC2, AC3, AC4, and AC6 all pass on the `.github` source file.

## Stage 2: Remove Step 0 from `04 Phase - Execute`

- [ ] Delete only the numbered Step 0 branch-creation block from `.github/agents/04-phase-execute.agent.md`.
- [ ] Preserve the rest of the execute pipeline text, renumbering only if needed so Step 1 is the first numbered execution step.
- [ ] Read the updated master file and confirm no Step 0 or duplicate branch-creation instruction remains in the numbered pipeline.

## Stage 3: Propagate to `opencode/agents/` and `claude/agents/`

- [ ] Mirror the Stage 1 refiner changes into `opencode/agents/02-phase-refiner.md` and `claude/agents/phase-refiner.md`, preserving each platform's format differences while keeping the behavior identical.
- [ ] Mirror the Stage 2 execute changes into `opencode/agents/04-phase-execute.md` and `claude/agents/phase-execute.md`.
- [ ] Read back all four propagated files and confirm AC7: the refiner additions and execute removal match the `.github` master intent across both platform copies.
- [ ] Do a final six-file comparison pass to confirm the feature changed only the intended files and did not add commit-checkpoint behavior or other out-of-scope edits.