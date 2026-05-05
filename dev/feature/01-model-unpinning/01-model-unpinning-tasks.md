# 01 Model Unpinning Tasks

## Stage 1: Remove `model:` from `.github/agents/`

- [ ] Remove the `model:` frontmatter line from each targeted `.github/agents/` file listed in the plan.
- [ ] Leave all remaining frontmatter keys, delimiters, and agent body content unchanged in those files.
- [ ] Confirm `.github/agents/` files that never had a `model:` line are not modified.

## Stage 2: Remove `model:` from `opencode/agents/`

- [ ] Remove the `model:` frontmatter line from `opencode/agents/03-feature-decomposer.md`, `opencode/agents/agent-test-runner.md`, `opencode/agents/agent-testing-agent.md`, and `opencode/agents/web-researcher.md`.
- [ ] Preserve all other OpenCode frontmatter and body content byte-for-byte.
- [ ] Confirm the other `opencode/agents/` files remain untouched.

## Stage 3: Remove `model:` from `claude/agents/`

- [ ] Remove the `model:` line from `claude/agents/z-feature-plan-expander.md` and `claude/agents/z-feature-qa-writer.md`.
- [ ] Preserve the surrounding markdown structure and any remaining metadata without reformatting.
- [ ] Confirm the other `claude/agents/` files remain untouched.

## Stage 4: Final Verification

- [ ] Run `grep -r "^model:" .github/agents/ opencode/agents/ claude/agents/` and confirm it returns no matches.
- [ ] Review the diff and verify every modified file only deletes a single `model:` line.
- [ ] Spot-check at least one modified file from each target directory to confirm frontmatter delimiters and readability are intact.
- [ ] Confirm files without a `model:` line do not appear in the final diff.