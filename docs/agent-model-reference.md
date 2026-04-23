# Agent Model Selection Reference

**Last updated:** 2026-04-23
**Available models:** GPT 5.4, GPT 5.3-Codex, Sonnet 4.6, Haiku 4.6, Kimi-K2.6, GLM 5.1, MiniMax 2.6

> **Reasoning levels defined:**
> - **Low** — Mechanical or template-driven. Reads structured inputs, produces structured outputs. Minimal judgment required.
> - **Medium** — Pattern matching and structured analysis. Requires domain judgment but follows well-defined rules. Little or no code generation.
> - **High** — Complex multi-step reasoning, code generation, deep analysis, or cross-cutting synthesis across many documents.

> **Model notes:**
> - **Kimi-K2.6** is a reasoning model — internal chain-of-thought tokens are billed and can be 5–20× visible output. Reserve for tasks where depth genuinely justifies the cost.
> - **GPT 5.3-Codex** is code-specialized — prefer it over GPT 5.4 for implementation, debugging, and review tasks.
> - **Haiku 4.6** and **MiniMax 2.6** are best for high-volume, low-stakes invocations (run once per feature, every pipeline run).
> - **GLM 5.1** is a solid mid-tier option for structured document generation from well-defined inputs.

---

## Agent Roster

| Agent File | Role | Reasoning Level | Primary Recommendation | Alternatives |
|---|---|---|---|---|
| `01-project-planner.agent.md` | Creates multi-phase project roadmaps; iterates with user; produces self-contained phase documents | **Medium–High** | Sonnet 4.6 | GPT 5.4, GLM 5.1 |
| `02-phase-refiner.agent.md` | Probes edge cases in phase documents; surfaces dependencies; stress-tests scope before decomposition | **High** | Sonnet 4.6 | GPT 5.4, Kimi-K2.6 |
| `03-feature-decomposer.agent.md` | Decomposes a phase into independent features; produces plan files with AC, traceability, test strategy | **High** | Sonnet 4.6 | GPT 5.4, GPT 5.3-Codex |
| `04-phase-execute.agent.md` | Orchestrates full phase pipeline; manages parallel/sequential subagent invocations; tracks verdicts and state | **High** | Sonnet 4.6 | GPT 5.4, Kimi-K2.6 |
| `04a-feature-plan-expander.agent.md` | Reads plan files; generates -context.md and -tasks.md; captures environment state and relevant learnings | **Medium** | GLM 5.1 | MiniMax 2.6, Haiku 4.6 |
| `04b-feature-implementer.agent.md` | Writes code from plans using Red-Green-Refactor TDD; produces implementation record | **High** | GPT 5.3-Codex | Sonnet 4.6, Kimi-K2.6 |
| `04c-feature-reviewer.agent.md` | Reviews code against plan; applies fixes for Blocker/High/Medium issues directly; produces review record | **High** | GPT 5.3-Codex | Sonnet 4.6, Kimi-K2.6 |
| `04d-feature-qa-writer.agent.md` | Writes consolidated manual QA plan from pipeline documents; filters automated vs. manual coverage | **Medium** | GLM 5.1 | MiniMax 2.6, Sonnet 4.6 |
| `04e-phase-final-review.agent.md` | Exhaustive cross-validation of all pipeline documents; runs fast-track or standard mode; GO/NO-GO assessment | **High** | Sonnet 4.6 | GPT 5.4, Kimi-K2.6 |
| `debugger.agent.md` | Diagnoses root causes of runtime errors; traces through multi-layer stacks; applies targeted fixes | **High** | GPT 5.3-Codex | Sonnet 4.6, Kimi-K2.6 |
| `unity-reviewer.agent.md` | Deep Unity C# code review applying Unity-specific lifecycle, architecture, and performance rules | **High** | GPT 5.3-Codex | Sonnet 4.6, Kimi-K2.6 |
| `audit-code-or-infra.agent.md` | Orchestrates multi-domain audits; delegates to auditor subagents; optional remediation pipeline | **High** | Sonnet 4.6 | GPT 5.4 |
| `auditor-code.agent.md` | Deep code quality audit: security, DRY, type hints, readability, dependencies | **High** | GPT 5.3-Codex | Sonnet 4.6, Kimi-K2.6 |
| `auditor-refactor.agent.md` | Architecture audit: module organization, coupling, cohesion, separation of concerns | **High** | Sonnet 4.6 | GPT 5.4, Kimi-K2.6 |
| `auditor-infra.agent.md` | Infrastructure/config audit: Dockerfiles, CI/CD, IaC, build scripts; structured findings report | **Medium** | Sonnet 4.6 | GLM 5.1, MiniMax 2.6 |
| `agent-testing-agent.agent.md` | Meta-agent for testing other agents; complex judgment about agent behavior correctness | **High** | Sonnet 4.6 | GPT 5.4, Kimi-K2.6 |
| `web-research-specialist.agent.md` | Researches technical topics across the internet; synthesizes findings into structured report | **Medium** | Sonnet 4.6 | GLM 5.1, MiniMax 2.6 |
| `documentation-architect.agent.md` | Creates and updates repository documentation; scans for staleness; writes README, ARCHITECTURE, etc. | **Medium** | Sonnet 4.6 | GLM 5.1, MiniMax 2.6 |
| `agent-test-runner.agent.md` | Runs agent benchmark tests; collects and reports pass/fail results | **Low** | Haiku 4.6 | MiniMax 2.6, GLM 5.1 |
| `test-orchestrator.agent.md` | Orchestrates test analysis, writing, and fixing pipelines; delegates to test subagents | **High** | Sonnet 4.6 | GPT 5.4 |
| `test-writer.agent.md` | Bootstraps test suites from scratch; creates test files, fixtures, and config for untested code | **Medium** | GPT 5.3-Codex | Sonnet 4.6, GLM 5.1 |
| `test-analyst.agent.md` | Analyzes test suites for coverage gaps, redundancy, and quality; produces reduction plan (no code changes) | **Medium** | Sonnet 4.6 | GLM 5.1, MiniMax 2.6 |
| `test-fixer.agent.md` | Diagnoses and fixes broken tests; updates assertions, mocks, fixtures; never modifies source | **Medium** | GPT 5.3-Codex | Sonnet 4.6, GLM 5.1 |

---

## Decision Guide

**Use Kimi-K2.6 when:**
- The task involves novel problem-solving where deep chain-of-thought is genuinely necessary
- You are running a one-off high-stakes analysis (not repeated N times per phase)
- Token cost is secondary to solution quality

**Use GPT 5.3-Codex when:**
- The primary output is code (implementation, test writing, debugging, review with fixes)
- Code correctness and idiomatic style matter more than broad reasoning

**Use Sonnet 4.6 when:**
- The task requires strong reasoning but is invoked repeatedly (N features × pipeline steps)
- Orchestration, complex document analysis, or cross-cutting synthesis across many files

**Use GLM 5.1 / MiniMax 2.6 when:**
- The task is structured document generation from well-defined inputs
- Cost efficiency matters and the task is high-volume (e.g., plan expander runs once per feature per pipeline run)

**Use Haiku 4.6 when:**
- The task is purely mechanical: running commands, reporting results, filling templates
- Invoked very frequently and judgment is minimal
