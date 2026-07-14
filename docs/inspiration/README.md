# Inspiration Repo Inventory

Crawl of the nine repos cloned into `/Users/jennywadkins/github_repos/claude_skills`, done 2026-07-14 to bootstrap planning for (a) onboarding more security/safety hooks and (b) enhancing the agentic flow in this project. One detail file per repo in this directory.

## At a glance

| Repo | What it is | Agents | Skills | Hooks | Character | Verdict |
|---|---|---|---|---|---|---|
| [claudekit](claudekit.md) | npm CLI guardrail framework | ~35 | 0 | 20+ (TS binary) | General (JS/TS-leaning) | **Install as-is** via CLI |
| [claude-workflow-v2](claude-workflow-v2.md) | Universal workflow plugin | 7 | 14 | 15 (py/bash) | General, full SDLC | **Install as-is or cherry-pick** |
| [gstack](gstack.md) | Skill-based virtual eng team + browser/memory tooling | 0 (roles are skills) | 59 | 3 (niche) | General, opinionated pipeline | Install whole if you want the workflow; else cherry-pick skills |
| [claude-code-infrastructure-showcase](claude-code-infrastructure-showcase.md) | Skill auto-activation hook framework | 8 | 5 | 5 wired + 4 optional (bash→TS) | Reusable infra, TS-stack content | **Cherry-pick the hook framework** |
| [buildwithclaude](buildwithclaude.md) | 160-plugin marketplace/aggregator | ~226 | ~206 | 28 | Meta-catalog | **Cherry-pick only**, never bulk |
| [claude-hooks](claude-hooks.md) (Lasso) | Prompt-injection defender | 0 | 1 | 1 (py or TS) | Highly specialized (security) | Install as-is or lift `patterns.yaml` |
| [claude-code-hooks-mastery](claude-code-hooks-mastery.md) | Hook lifecycle teaching kit | 4 | 0 | 13 (uv python) | Teaching/reference | Cherry-pick (`pre_tool_use.py`, meta-agent) |
| [claude-code-hooks](claude-code-hooks.md) | All-30-hook-events sound demo | 3 | 0 | 30 (1 py script) | Specialized novelty; best hook-event catalog | Reference only |
| [ui-ux-pro-max-skill](ui-ux-pro-max-skill.md) | UI/UX design-intelligence skill | 0 | 7 | 0 | Highly specialized (design) | Install via its CLI if you do UI work |

## Read-across for this project's two goals

### Goal 1: More security/safety hooks

Current baseline in this repo: `bash-safety`, `protect-files`, `audit-log`, `done-notify` (`.github/hooks/`). The strongest candidates found, roughly in order of value:

1. **claudekit `file-guard`** — ignore-file-driven sensitive-file access blocking with bash-command parsing to catch exfiltration. Most sophisticated single safety hook found; caveat: comes as a compiled binary, so adopting the *idea* may mean reimplementing.
2. **Lasso `prompt-injection-defender`** — the only *prompt-injection* defense in the whole set; `patterns.yaml` (96 regexes) is directly liftable into a PostToolUse hook.
3. **claude-workflow-v2 `security-check.py` / `pre-commit-check.py`** — blocks writes containing secrets; flags debug/temp markers. Stdlib Python, easy to port.
4. **buildwithclaude safety hooks** — `sql-bulk-delete-warn`, `no-vibes` (blocks unverified "done" claims at Stop), `file-backup`, `security-scanner`, `dependency-checker`, `conventional-commits`.
5. **hooks-mastery `pre_tool_use.py`** — `.env`-access block + `rm -rf` guard; overlaps with existing `bash-safety`/`protect-files` but worth diffing patterns.
6. **claudekit Stop-time validation** — typecheck/lint/test-project + `check-todos` + `self-review` as completion gates; and `check-comment-replacement` as an anti-laziness guard.

### Goal 2: Agentic-flow enhancements

This repo already has a deep planner→refiner→decomposer→executor pipeline. The novel ideas worth studying:

- **infrastructure-showcase's skill auto-activation** (UserPromptSubmit suggestion injection + PreToolUse enforcement guard driven by `skill-rules.json`) — solves "skills don't activate" deterministically; the most directly relevant infra for a multi-agent source-of-truth repo.
- **claudekit `codebase-map` + `create-checkpoint`** — context injection on first prompt; git checkpoint on every Stop with `/checkpoint:restore`.
- **hooks-mastery `meta-agent`** — an agent that generates new sub-agent definitions; natural fit for a source-of-truth repo that propagates agents to multiple harnesses.
- **gstack's plan-review panel** (CEO/eng/design/DX sequential reviews, `autoplan`) and ship pipeline (`ship` → `land-and-deploy` → `canary`) — comparable philosophy to this repo's pipeline; good for gap analysis.
- **buildwithclaude `gsd` and `uc-taskmanager`** — alternative spec-driven pipelines to compare against phase-refiner/feature-decomposer.
- **claude-code-hooks (sound repo)** — reference catalog of all 30 hook events, useful when deciding which events to attach new hooks to.

## Cross-cutting cautions

- Hooks that can **block** (protect-files, security-check, skill-verification-guard, file-guard) need their pattern/enforcement config reviewed against this repo's workflows before enabling.
- Runtime stacks vary: uv-Python (hooks-mastery), stdlib Python/bash (workflow-v2, buildwithclaude), Node/tsx + sqlite (infra-showcase), Bun (gstack), compiled TS binary (claudekit). Any adoption should standardize on one or two runtimes.
- Several repos overlap heavily (multiple code-reviewers, security-auditors, docs-writers) with agents this repo already maintains — prefer diffing prompts for improvements over adding duplicates.
