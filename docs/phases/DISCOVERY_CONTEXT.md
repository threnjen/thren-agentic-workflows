# Discovery Context: Security & Determinism Hooks

Context gathered during planning (2026-07-14) beyond this repo's codebase. Downstream agents (phase-refiner, feature-decomposer, phase-execute) should load this file with each phase document.

## Binding Constraints (user-directed)

1. **Clean-room implementations only.** The user explicitly directed: write our own versions of these hooks/skills — no direct copies from the inspiration repos — and where possible improve and strengthen the existing patterns. Treat `docs/inspiration/` as a requirements/design source (events to hook, failure modes to cover, weaknesses to fix), never as code to copy. Do not lift pattern files (e.g., Lasso's `patterns.yaml`), scripts, or prompt text verbatim.
2. **Runtime**: Python 3 stdlib for all new hook logic (user-selected over bash and TypeScript).
3. **Enforcement**: hard-block for file access / dangerous commands; warn-and-continue for injection detection except high-confidence patterns.
4. **Distribution**: source of truth in `.github/hooks/`, propagated via `scripts/propagate_master_assets.py` alongside agents/skills/instructions.

## Project Goals (user's own framing)

1. Security/vulnerability hooks to stop prompt injection.
2. Protect the system and important files from manipulation **even with bypass permissions** (hence hooks, not `permissions.deny` — PreToolUse hooks fire in bypass mode).
3. Make deterministic what is currently agent-controlled in the workflows.
4. Auto-format files on save with the correct linter/formatter.
5. Block agent access to `.env` files and other common secret-bearing files.

Explicitly rejected: adopting agent/skill collections that duplicate the existing pipeline (e.g., claude-workflow-v2's orchestrator/reviewer/docs-writer agents — "almost the same as my current workflow").

## Additional Research Material

Nine repos cloned by the user into `/Users/jennywadkins/github_repos/claude_skills/` were crawled by subagents; full inventories live in `docs/inspiration/` (one file per repo, plus `README.md` with a comparison table and goal mapping). Summary of design references per phase:

- **Phase 01 (file-access guard)**: claudekit `file-guard` (ignore-file-driven patterns + bash-command parsing for indirect access; ships as compiled binary — a weakness we fix with readable config), claude-workflow-v2 `protect-files.py`/`security-check.py` (stdlib Python, naive path matching), hooks-mastery `pre_tool_use.py` (.env block + `rm -rf` guard), buildwithclaude `file-backup`. Existing repo hooks `bash-safety.sh` and `protect-files.sh` overlap and should be folded in or retired.
- **Phase 02 (prompt injection)**: Lasso Security `claude-hooks` — the only injection defense found; PostToolUse scanner on `Read|WebFetch|Bash|Grep|Task` with 5 pattern categories (instruction-override, roleplay/DAN, encoding-obfuscation, context-manipulation, instruction-smuggling) and severity tiers. Weaknesses to improve: warn-only (never blocks), regex-only, no homoglyph/markdown-smuggling coverage, no measurable test corpus. We author our own pattern corpus from the category taxonomy.
- **Phase 05 (format + gates)** — *renumbered from Phase 03 on 2026-07-16*: claude-workflow-v2 `format-on-edit.py` (hardcoded file-type→formatter map — improve with project-aware detection from pyproject.toml/package.json), buildwithclaude `no-vibes` Stop hook (blocks "done" claims without same-turn verification evidence — adapt evidence definition to this repo's pipeline artifacts: implementation records, review records, QA docs), claudekit Stop-gates (typecheck/lint/test-project, check-todos, check-comment-replacement).
- **Phase 06 (skill enforcement)** — *renumbered from Phase 04 on 2026-07-16*: claude-code-infrastructure-showcase — `skill-rules.json` (globs/keywords → required skills, enforcement levels block/suggest/warn) + UserPromptSubmit suggestion-injection hook + PreToolUse guard blocking edits until required skills are activated + PostToolUse tracker clearing pending enforcement. Node/tsx + sqlite implementation, single-project — we rebuild in Python for this repo's 16+ skills and multi-harness propagation.
- **Hook-event reference**: shanraisshan `claude-code-hooks` — the most complete public catalog of all 30 Claude Code hook events and which fire in agent contexts; consult when choosing attachment points.

## Phase 03 Design Notes: Phase Final Review (recorded 2026-07-14, ahead of the summary being authored)

*Renumbered 2026-07-16: this phase was Phase 05 when these notes were written. The `05a`–`05l` agent names below are pipeline-position names and are unchanged.*

User-directed addition: a new agentic flow named **"Phase Final Review"** (user renamed from "Large Phase Evaluation") for large phases divided into subphases `PHASE_0Na`–`PHASE_0NX`. User wants ALL identified evaluation modules included, liberal use of hidden subagents to keep context clean, skills wherever they make sense, and design consistency with the existing `.github/agents` house style (numbered orchestrator + lettered subagents, e.g. `04-phase-execute` + `04a`–`04d`; shared-convention skills like `auditor-conventions`; report-template skills like `implementation-record`).

**Core design rules:**
- Orchestrator (`05-phase-final-review.agent.md`) never reads code, diffs, or full subphase docs — only structured reports subagents write to `dev/phase-final-review/PHASE_0N/`; each subagent returns a ≤10-line summary.
- Must recommend/require a state-of-the-art model; warn at startup if not on one. Deep-judgment subagents (AC regression, seam analysis, synthesis) inherit top tier; mechanical sweeps (artifact/dependency) run on a cheap tier.
- Preflight: auto-suggest the pre-phase baseline commit (last commit before subphase a's first feature commit, from ledger/commit conventions), user confirms; discover subphases from `docs/phases/PHASE_0N*/`; inventory pipeline artifacts (implementation records, QA docs, security reports) and fail loudly on missing artifacts before evaluating.

**Subagent roster (05a–05l):**
- `05a-baseline-worktree` — check out the confirmed baseline commit in a git worktree; return path. (Candidate reusable skill: `worktree-baseline`; eval-grader could reuse.)
- `05b-change-narrator` — whole-phase change narrative baseline→HEAD, per-subphase attribution, multi-subphase churn hotspots; chunks diffs internally, may spawn per-directory readers.
- `05c-qa-consolidator` — master QA doc: merge all subphase QA docs, dedupe, drop superseded checks, re-order into a single efficient walkthrough. Reads QA docs only.
- `05d-security-rollup` — union + dedupe of all subphase security findings; delegate a live re-scan of final code (existing `security-scan` agent) against the full list; classify fixed / persisting / reintroduced.
- `05e-ac-regression` — re-verify EVERY subphase's acceptance criteria against the FINAL codebase (later subphases may have broken earlier ACs); one hidden verifier per subphase.
- `05f-seam-analyzer` — integration seams between subphases: interface mismatches, duplicated logic, orphaned scaffolding; built on code-review-graph tools (get_impact_radius, get_bridge_nodes).
- `05g-artifact-sweeper` — debug statements, TODOs/FIXMEs, temp feature flags, commented-out/dead code introduced since baseline (refactor_tool dead-code detection scoped to phase diff). Mechanical.
- `05h-test-health` — coverage delta baseline→now, cross-subphase test redundancy, flake candidates; delegates to existing `test-analyst`.
- `05i-learnings-harvester` — mine review records/fix commits/QA failures for recurring mistakes; draft `.github/learnings/` and instruction-file updates feeding the instructions-writer/evaluator loop.
- `05j-consistency-auditor` — convention drift across subphases (naming, error handling, patterns) with recommended canonical forms.
- `05k-dependency-auditor` — new dependencies across the phase: licenses, vulnerabilities, competing/duplicate libs. Mechanical.
- `05l-readiness-synthesizer` — reads all reports (never code); produces the go/no-go readiness report with severity-ordered blocking list. Extends `prod-code-review` conventions one level up rather than duplicating them.

**Skills to create:**
- `phase-final-review-conventions` — shared constraints for all 05x evaluators (report locations/naming, severity levels, ≤10-line return-summary contract, read-only worktree etiquette, model-tier notes). Mirrors `auditor-conventions`.
- `phase-final-review-report` — output templates: master QA doc, security rollup, AC-regression matrix, readiness report. Mirrors `implementation-record`/`eval-feature-decomposition-report`.
- `worktree-baseline` — reusable "check out commit X in a worktree, hand back path" skill.

The phase summary was authored 2026-07-15 from these notes and executed immediately after Phase 02, ahead of the remaining hook phases (it has no dependency on them). The 2026-07-16 renumber made the phase numbers match that actual execution order, so this work is now `docs/phases/PHASE_03/PHASE_03_SUMMARY.md`. The phase summary is the authoritative planning document; these notes remain the original design capture.

## Key Technical Facts Established

- PreToolUse hooks execute regardless of permission mode; a hook exiting 2 (or emitting a deny decision) blocks the tool call even under `--dangerously-skip-permissions`. This is the only reliable enforcement layer for goal 2.
- All nine surveyed repos are MIT-licensed; the clean-room constraint is the user's preference, not a legal necessity — but it stands regardless.
- Current repo hook wiring lives in `.claude/settings.json` with `$source`-tagged entries generated from `.github/hooks/*.json` definitions; existing hooks: `bash-safety` (PreToolUse), `protect-files` (PreToolUse), `audit-log` (PostToolUse), `done-notify` (Stop/Notification), plus code-review-graph update/status hooks.
- The repo's propagation mechanism is `scripts/propagate_master_assets.py` (regenerates Claude/OpenCode/Codex outputs from `.github/` source). New hooks must join this flow.
