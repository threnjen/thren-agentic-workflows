# Implementation Record: 01 Model Unpinning

## Summary
Removed the `model:` frontmatter line from all in-scope agent definition files in `.github/agents/`, `opencode/agents/`, and `claude/agents/` exactly as planned. No other frontmatter keys or body content were modified.

## Sibling Features
- `02-hook-template` (Wave 2): independent workflow/template work; no overlap with this feature's target files.
- `03-branch-lifecycle-migration` (Wave 3): branch/process migration scope; no overlap with model frontmatter removal.
- `04-commit-instrumentation` (Wave 4): commit instrumentation scope; no overlap with agent frontmatter edits.
- `04-ledger-annotation` (Wave 4): ledger annotation scope; no overlap with model-pin cleanup.
- `05-eval-grader-agent` (Wave 5): grader-agent scope may consume unpinned agents later; this feature stays limited to removing `model:` lines only.
- Shared module awareness: all sibling work appears orthogonal; this feature only touches agent definition markdown files.

## Acceptance Criteria Status

| AC | Description | Status | Implementing Files | Notes |
|----|-------------|--------|--------------------|-------|
| AC1 | No `model:` field appears in any agent definition file in `.github/agents/` | Done | `.github/agents/*` targeted files listed below | Verified by scoped grep returning no matches. |
| AC2 | No `model:` field appears in any agent definition file in `opencode/agents/` | Done | `opencode/agents/03-feature-decomposer.md`, `opencode/agents/agent-test-runner.md`, `opencode/agents/agent-testing-agent.md`, `opencode/agents/web-researcher.md` | Verified by scoped grep returning no matches. |
| AC3 | No `model:` field appears in any agent definition file in `claude/agents/` | Done | `claude/agents/z-feature-plan-expander.md`, `claude/agents/z-feature-qa-writer.md` | Verified by scoped grep returning no matches. |
| AC4 | All other frontmatter fields and agent body content remain byte-for-byte unchanged | Done | All modified files | Diff shows deletions only; no added lines in scoped diff. |
| AC5 | Files that had no `model:` line are not modified | Done | N/A (negative set) | Only 24 known files changed, matching pre-change `model:` inventory. |

## Files Changed

### Source Files

| File | Change Type | What Changed | Why |
|------|-------------|--------------|-----|
| `.github/agents/01-project-planner.agent.md` | Modify | Removed one `model:` line from frontmatter | Unpin model per feature requirement |
| `.github/agents/02-phase-refiner.agent.md` | Modify | Removed one `model:` line from frontmatter | Unpin model per feature requirement |
| `.github/agents/03-feature-decomposer.agent.md` | Modify | Removed one `model:` line from frontmatter | Unpin model per feature requirement |
| `.github/agents/04-phase-execute.agent.md` | Modify | Removed one `model:` line from frontmatter | Unpin model per feature requirement |
| `.github/agents/04a-feature-plan-expander.agent.md` | Modify | Removed one `model:` line from frontmatter | Unpin model per feature requirement |
| `.github/agents/04b-feature-implementer.agent.md` | Modify | Removed one `model:` line from frontmatter | Unpin model per feature requirement |
| `.github/agents/04c-feature-reviewer.agent.md` | Modify | Removed one `model:` line from frontmatter | Unpin model per feature requirement |
| `.github/agents/04d-feature-qa-writer.agent.md` | Modify | Removed one `model:` line from frontmatter (`Auto`) | Unpin model per feature requirement |
| `.github/agents/agent-test-runner.agent.md` | Modify | Removed one `model:` line from frontmatter | Unpin model per feature requirement |
| `.github/agents/audit-code-or-infra.agent.md` | Modify | Removed one `model:` line from frontmatter | Unpin model per feature requirement |
| `.github/agents/auditor-code.agent.md` | Modify | Removed one `model:` line from frontmatter | Unpin model per feature requirement |
| `.github/agents/auditor-infra.agent.md` | Modify | Removed one `model:` line from frontmatter | Unpin model per feature requirement |
| `.github/agents/auditor-refactor.agent.md` | Modify | Removed one `model:` line from frontmatter | Unpin model per feature requirement |
| `.github/agents/prod-code-review.md` | Modify | Removed one `model:` line from frontmatter | Unpin model per feature requirement |
| `.github/agents/test-analyst.agent.md` | Modify | Removed one `model:` line from frontmatter | Unpin model per feature requirement |
| `.github/agents/test-fixer.agent.md` | Modify | Removed one `model:` line from frontmatter | Unpin model per feature requirement |
| `.github/agents/test-writer.agent.md` | Modify | Removed one `model:` line from frontmatter | Unpin model per feature requirement |
| `.github/agents/unity-reviewer.agent.md` | Modify | Removed one `model:` line from frontmatter | Unpin model per feature requirement |
| `opencode/agents/03-feature-decomposer.md` | Modify | Removed one `model:` line from frontmatter | Unpin model per feature requirement |
| `opencode/agents/agent-test-runner.md` | Modify | Removed one `model:` line from frontmatter | Unpin model per feature requirement |
| `opencode/agents/agent-testing-agent.md` | Modify | Removed one `model:` line from frontmatter | Unpin model per feature requirement |
| `opencode/agents/web-researcher.md` | Modify | Removed one `model:` line from frontmatter | Unpin model per feature requirement |
| `claude/agents/z-feature-plan-expander.md` | Modify | Removed one `model:` line from frontmatter | Unpin model per feature requirement |
| `claude/agents/z-feature-qa-writer.md` | Modify | Removed one `model:` line from frontmatter | Unpin model per feature requirement |
| `dev/feature/01-model-unpinning/01-model-unpinning-implementation.md` | Add | Added implementation record artifact | Required deliverable for reviewer handoff |

### Test Files

| File | Change Type | What Changed | Covers |
|------|-------------|--------------|--------|
| None | N/A | No automated test files in scope for this markdown-only slice | Validation performed via targeted executable checks |

## Test Results
- **Baseline**: 0 passed, 0 failed (no compiled automated test suite for this docs-only slice; pre-change red check found 24 scoped `model:` matches)
- **Final**: 0 passed, 0 failed (post-change validation shows 0 scoped `model:` matches)
- **New tests added**: 0
- **Regressions**: None

## Deviations from Plan
- Used `perl -i -ne 'print unless /^model:/'` for precise line removal instead of `replace_string_in_file` because that tool is not available in this environment.
- Missing-test-suite gate was explicitly overridden by subagent-mode instruction for this feature.

## Gaps
- None

## Reviewer Focus Areas
- Confirm every changed file removes exactly one `model:` line and no other content.
- Confirm no file outside the 24 targeted agent files was modified (except this implementation record artifact).
- Confirm frontmatter delimiters remain valid in each modified directory variant (`.github/agents`, `opencode/agents`, `claude/agents`).
- Confirm scoped grep remains empty: `grep -R '^model:' .github/agents opencode/agents claude/agents`.
