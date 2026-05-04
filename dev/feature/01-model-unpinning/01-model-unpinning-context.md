# 01 Model Unpinning Context

## Key Files

### Files To Change

| Path | Role | Change Type |
|------|------|-------------|
| `.github/agents/` | Master Copilot agent definitions. Remove the single `model:` frontmatter line from the 18 files identified in the plan: `01-project-planner.agent.md`, `02-phase-refiner.agent.md`, `03-feature-decomposer.agent.md`, `04-phase-execute.agent.md`, `04a-feature-plan-expander.agent.md`, `04b-feature-implementer.agent.md`, `04c-feature-reviewer.agent.md`, `04d-feature-qa-writer.agent.md`, `agent-test-runner.agent.md`, `audit-code-or-infra.agent.md`, `auditor-code.agent.md`, `auditor-infra.agent.md`, `auditor-refactor.agent.md`, `prod-code-review.md`, `test-analyst.agent.md`, `test-fixer.agent.md`, `test-writer.agent.md`, and `unity-reviewer.agent.md`. | Modify |
| `opencode/agents/` | Derived OpenCode agent copies. Remove the single `model:` line from `03-feature-decomposer.md`, `agent-test-runner.md`, `agent-testing-agent.md`, and `web-researcher.md`. | Modify |
| `claude/agents/` | Derived Claude agent copies. Remove the single `model:` line from `z-feature-plan-expander.md` and `z-feature-qa-writer.md`. | Modify |

### Read-Only Reference Files

| Path | Role | Change Type |
|------|------|-------------|
| `README.md` | Confirms this repository is a docs-only template repo and explains the three platform variants. | Read-only reference |
| `docs/CODEBASE_CONTEXT.md` | Confirms repository structure, static-docs nature, and agent/instruction relationships. | Read-only reference |
| `docs/ARCHITECTURE.md` | Confirms `.github/` is the master source of truth and `opencode/` and `claude/` are derived platform copies. | Read-only reference |
| `.github/agents/README.md` | Documents the agent inventory and reinforces the orchestrator/subagent naming and file conventions. | Read-only reference |

## Architectural Decisions

- Treat this as a frontmatter-only edit. The implementation should delete exactly one `model:` line per targeted file and leave every other byte unchanged.
- Update `.github/agents/` first because it is the master source of truth for agent definitions in this repository.
- Apply equivalent removals to `opencode/agents/` and `claude/agents/` because those directories are maintained as platform-specific copies of the same agent set.
- Keep the existing YAML or markdown frontmatter structure intact after removal. No reordering, normalization, or formatting cleanup is allowed.
- Do not touch files that do not already contain a `model:` line, even if they sit beside targeted files in the same directory.

## Constraints

- Do not modify any `-plan.md` file.
- Do not modify `.github/instructions/` or `.github/skills/`.
- Do not add, remove, reorder, or reformat any frontmatter fields other than deleting the existing `model:` line.
- Do not change body content, headings, whitespace, or platform-specific metadata outside the removed line.
- Preserve valid frontmatter delimiters (`---`) after the edit and avoid introducing extra blank lines.
- Treat `prod-code-review.md` in `.github/agents/` the same as `.agent.md` files because it follows the same frontmatter pattern.

## Relationships to Sibling Plans

None specified in the plan. This feature is standalone and has no declared dependencies on sibling feature folders.

## Suggested Implementation Order

1. Remove `model:` lines from the `.github/agents/` master files.
2. Remove `model:` lines from the `opencode/agents/` derived copies.
3. Remove `model:` lines from the `claude/agents/` derived copies.
4. Run repository-wide verification to confirm no `model:` lines remain in the three target directories and no unrelated files changed.

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Markdown-only repository of GitHub Copilot, OpenCode, and Claude agent definitions plus reusable documentation templates. No application runtime was detected. |
| Test Runner | No tests found |
| Test Baseline | N/A on 2026-05-04. No test runner or test configuration files were detected in the repository root. |
| Lint | Not configured |
| Format | Not configured |

## Relevant Learnings

None applicable. This repository does not currently contain a `.github/learnings/` directory.