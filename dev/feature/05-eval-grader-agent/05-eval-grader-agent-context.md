# 05 Eval Grader Agent Context

## Key Files

### Files To Change

| File | Role | Change Type |
|------|------|-------------|
| `.github/agents/05-eval-grader.agent.md` | Master GitHub Copilot agent definition for the grader workflow | Create |
| `opencode/agents/05-eval-grader.md` | OpenCode variant of the grader agent | Create |
| `claude/agents/05-eval-grader.md` | Claude Code variant of the grader agent | Create |
| `eval/rubrics/phase-eval-infrastructure-foundation.example.yaml` | Seed rubric file that makes the grader schema concrete for future runs | Create |

### Read-Only Reference Files

| File | Role | Change Type |
|------|------|-------------|
| `dev/feature/05-eval-grader-agent/05-eval-grader-agent-plan.md` | Source plan, acceptance criteria, stages, and traceability for this feature | Read-only reference |
| `docs/CODEBASE_CONTEXT.md` | Repo-level constraints and structure; confirms this is a Markdown-only template repository | Read-only reference |
| `README.md` | Platform and source-of-truth model for `.github/`, `opencode/`, and `claude/` variants | Read-only reference |
| `.github/agents/README.md` | Agent catalog and pipeline documentation for the master agent set | Read-only reference |

## Architectural Decisions

- Keep `.github/agents/05-eval-grader.agent.md` as the master definition and propagate the same grader behavior to `opencode/agents/` and `claude/agents/`.
- Keep the grader non-interactive after invocation. The agent may require a rubric path up front, but the scoring flow itself must not pause for confirmations or mid-run prompts.
- Limit tool needs to `read`, `search`, and `edit`; the grader reads ledger and rubric files, evaluates automatable checks, and writes a report without invoking other agents or shell execution.
- Use a sequential scoring pipeline: intake rubric path, read `ledger-commits.jsonl` and `ledger-events.jsonl`, correlate rows by commit SHA, evaluate automatable criteria, flag manual criteria as `[NEEDS_HUMAN_REVIEW]`, then write the final report.
- Treat the report artifact as the durable output contract: write Markdown to `eval/runs/<phase-slug>/score-report-<timestamp>.md` with run metadata, per-feature summaries, failures, human-review items, regression flags, and overall verdict.
- Handle missing or empty ledgers explicitly in the report. Missing files are observable conditions, not silent failures; empty files are valid zero-row inputs.
- Omit any `model:` frontmatter field so the new agent remains consistent with the repository's model-unpinning direction.

## Constraints

- Preserve the plan's non-goals: no bespoke per-project production rubric authoring beyond the seeded example, no CI or subagent invocation, no ledger mutation, no automatic invocation flow, and no grading for non-phase branches.
- The grader must accept a user-provided rubric YAML path at invocation time and abort clearly when that path is not supplied.
- The grader must make its rubric schema explicit and keep the seeded example rubric aligned with that schema.
- The unified timeline must correlate commit and event ledgers by SHA and use that timeline to support per-feature scoring.
- Use the literal marker `[NEEDS_HUMAN_REVIEW]` for any criterion marked `human_intervention_required: true`, `requires_human: true`, or otherwise lacking an automatable check.
- Keep the three platform variants aligned in behavior and report format. Platform-specific filename or frontmatter differences must not change the grader workflow.
- This repository is documentation-driven. New agent files should follow existing Markdown and frontmatter conventions instead of introducing runnable code, scripts, or external dependencies.
- Repository conventions in `docs/CODEBASE_CONTEXT.md` indicate that agent-catalog documentation should stay in sync when the agent inventory changes.

## Relationships to Sibling Plans

- Depends on `04-commit-instrumentation`: the grader consumes `ledger-commits.jsonl`, so commit-ledger generation must exist before this agent is useful.
- Depends on `04-ledger-annotation`: the grader consumes `ledger-events.jsonl`, so semantic event annotation must exist before failure breakdowns and regression flags can be computed.
- This feature is a downstream consumer of both ledger-producing features rather than an independent source of evaluation data.

## Suggested Implementation Order

1. Confirm the upstream ledger contracts from `04-commit-instrumentation` and `04-ledger-annotation` are stable enough to reference in the grader instructions.
2. Write the master GitHub Copilot agent definition in `.github/agents/05-eval-grader.agent.md`.
3. Propagate the same grader body to `opencode/agents/05-eval-grader.md` and `claude/agents/05-eval-grader.md`.
4. Add the seeded example rubric under `eval/rubrics/` so the schema has a concrete reference implementation.
5. Verify the three platform copies stay behaviorally aligned and that the report/output instructions match the plan.

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Markdown-only repository of GitHub Copilot, OpenCode, and Claude Code agent definitions and supporting documentation; no package-managed runtime declared |
| Test Runner | `N/A` - no executable test harness is configured for this repository |
| Test Baseline | No tests found - baseline: N/A (captured 2026-05-04) |
| Lint | Not configured |
| Format | Not configured |

Verification note: `docs/CODEBASE_CONTEXT.md` describes this repository as containing no runnable code, and a repository scan for common test, lint, and format config files found agent-definition filenames but no executable test harness or config.

## Relevant Learnings

None applicable. No `.github/learnings/*.md` files are present in this repository.