# 04 PR Review Orchestrator — Context

## Key Files

### Files being changed

| File | Role | Change type |
|---|---|---|
| `.github/agents/05-phase-final-review.agent.md` | The 249-line orchestrator being rescoped. Rename to `.github/agents/05-pr-review.agent.md`. Its preflight checklist, invocation shape, model-tier table, `evaluator-status.jsonl` contract, and bounded-wait semantics are reusable; ledger/subphase/artifact-inventory/write-back/archive sections are deleted. | Rename + Modify |
| `.gitignore` | **Blocks AC13.** `dev/*` ignores everything under `dev/`; only `dev/phase-final-review/fixtures/**` is un-ignored. `dev/pr-review/fixtures/` must be un-ignored the same way, while the AC7 report root stays ignored. | Modify (not in plan's key-files list) |
| `dev/pr-review/fixtures/` | New pinned base/branch SHA pair fixture (AC13). Directory does not exist. `[PROPOSED - name TBD]` for the fixture file path. | Create |
| `tests/test_propagate_master_assets.py` | Lines 198–202 pin five exact orchestrator paths/strings; all five change on rename. Shared with features 01, 02, 03, 05, 06, 07. | Modify |
| `tests/test_pr_review_orchestrator.py` `[PROPOSED - name TBD]` | No plan in this phase names a home for feature 04's new contract assertions. Either a new file or an addition to an existing one; the implementer picks and records it. | Create |
| `.github/agents/README.md` | `:136` carries the orchestrator's row under its old display name; `:163+` name it in the parent column of every surviving `05x` row. Feature 02's AC5 covers only *retired agent* rows, so these survive it. Owner unconfirmed. | Modify (gap — see Discovery Delta) |
| `claude/agents/`, `claude/commands/`, `opencode/agents/`, `codex/agents/`, `codex/profiles/` | Generated roots. Rename produces `pr-review` outputs and orphans the `phase-final-review` set. | Generated |

### Read-only reference

| File | Why it matters |
|---|---|
| `.github/agents/04-phase-execute.agent.md` | House style for numbered orchestrators. **Its Step 6 is *titled* "Phase Final Review" but spawns Prod Code Review**, and it does not list this orchestrator in its `agents:`. The rename dangles nothing here. |
| `.github/agents/04e-diff-security-scan.agent.md` | The delegated security scan (AC10). Verified: `name: 04e Diff Security Scan`, `tools: [read, search, edit]` — no `execute` — `user-invocable: false`. |
| `.github/agents/05a-baseline-worktree.agent.md` | Preflight delegate. **`name: Baseline Worktree` — no numeric prefix**, unlike every other `05x`. |
| `scripts/propagate_master_assets.py` | `_claude_filename_for` (:389), `_build_agent_reference_map` (:412), `_rewrite_agent_references` (:423) govern rename identity. |
| `tests/test_readiness_synthesis_agents.py` | The style model the plan cites for contract assertions. Verified: module-level `Path` constants + plain `assert`, pytest-style (note `test_propagate_master_assets.py` uses `unittest` classes instead). |
| `.github/skills/pr-review-conventions/`, `.github/skills/pr-review-report/` | Feature 03's renamed contracts. Report templates and severity live there — do not restate them in the orchestrator. |

## Discovery Delta

| Finding | Impact | Action |
|---|---|---|
| **`.gitignore` blocks the AC13 fixture.** `.gitignore:5` is `dev/*`; the only un-ignore rules are `!dev/phase-final-review/`, `dev/phase-final-review/*`, `!dev/phase-final-review/fixtures/`, `!dev/phase-final-review/fixtures/**`. Verified: `git check-ignore -v dev/pr-review/fixtures/foo.md` → ignored by `dev/*`. AC13's fixture cannot be committed as written. | AC13 silently unachievable. The plan never mentions `.gitignore`. | **Add task** — mirror the four-rule pattern for `dev/pr-review/`. The existing pattern is the exact template and correctly splits tracked fixtures from ignored run artifacts (AC7's `dev/pr-review/<sha>-<ts>/` should stay ignored). |
| **AC10's "fans out to `05a`–`05g`" conflates three roles.** In the settled roster, `05a` is the baseline-worktree preflight delegate and `05g` is the readiness synthesizer that *consumes* the other reports. Only `05b`–`05f` plus `04e` (six) fan out concurrently. The existing agent already encodes this three-tier structure (`05a` → `05b`–`05k` → `05l`), and AC11's retained partial-failure semantics depend on it. | A literal reading of AC10 flattens preflight, fan-out, and synthesis into one step, breaking AC11. | **Refine plan** — declare the roster of seven + `04e`; fan-out set is `05b`–`05f` + `04e`. Raised to Decomposer. |
| **Renumbering map verified** from features 05/06/07 metadata + learnings: `05g-artifact-sweeper`→`05c`, `05j-consistency-auditor`→`05d`, `05k-dependency-auditor`→`05e`, `05h-test-health`→`05f`, `05l-readiness-synthesizer`→`05g`; `05a`/`05b` unchanged. | The plan's Unverified Assumption #1 is **confirmed accurate**: these targets do not exist at wave 4. The `agents:` frontmatter will name agents that do not exist until wave 6. | **Accepted risk** — as the plan states; `08-retirement-reconciliation` verifies. Map recorded here so the implementer does not re-derive it. |
| **Naive display-name replacement collides with common prose.** `_rewrite_agent_references` (`scripts/propagate_master_assets.py:423`) does unanchored `text.replace(agent.name, identifier)` across every agent body, sorted by name length descending. A short/generic `name:` such as `PR Review` would rewrite the common-noun phrase "PR Review" throughout this phase's agent and skill prose. | Constrains the `[PROPOSED]` `name:` choice. The ` - ` separator in `05 Phase - Final Review` is what made it collision-safe; `05 PR - Review` preserves that. | **Add constraint** to the name decision. |
| **Plan's Unverified Assumption #2 is largely resolvable now, and is mostly a non-issue.** The literal `05 Phase - Final Review` appears in **no other source agent body**. Only `.github/agents/README.md` and `tests/test_propagate_master_assets.py:198` carry it. | Verification burden is far smaller than the plan implies. | **Update plan** — narrow the assumption to the README and the test. Still verify all three roots after rename. |
| **`.github/agents/README.md` orchestrator rows are unowned.** Feature 02's AC5 removes *retired agent* rows only. The orchestrator's own row (`:136`) and the parent column of every surviving `05x` row still read `05 Phase - Final Review` after feature 02. Neither 02 nor 04 lists them. | A stale roster doc naming a deleted agent. | **Add task** — or confirm ownership with `08-retirement-reconciliation`. |
| **`tests/test_propagate_master_assets.py:198–202` pins five exact strings**: `.github/agents/05-phase-final-review.agent.md` → `name: 05 Phase - Final Review`, `claude/commands/phase-final-review.md`, `opencode/agents/05-phase-final-review.md`, `codex/agents/05-phase-final-review.toml`, `codex/profiles/phase-final-review.config.toml`. Note the Claude output is a **command**, not an agent — the orchestrator is user-invocable. | Makes the plan's one-line "Existing tests to update" concrete. | **Add task** with the exact line range. |
| **`expected_slugs` (`tests/test_propagate_master_assets.py:87`) omits `execute` holders**, including this orchestrator, because the tuple asserts `assertNotIn("execute", agent.tools)`. The rescoped orchestrator retains `execute` (a non-goal). | No change needed here; feature 05 closes that enumeration gap once the roster is contiguous. | **None** |
| **AC4's git evidence verified exactly** on this branch: HEAD `ae9823a` on `repo_improvements_project`; `git merge-base HEAD main` → `e3398c7`; `git merge-base HEAD repo_improvements_project` → `ae9823a` (HEAD itself). `origin/HEAD` **is** set here (`refs/remotes/origin/main`). | AC4 is sound. Confirms the plan's live-QA-in-a-scratch-repo requirement for the `origin/HEAD`-unset path — it cannot be exercised locally without unsetting it. | **None** |
| **The fixture pair implied by AC4's evidence is too large.** `e3398c7..ae9823a` is 5 commits, 242 files, 27,041 insertions. The plan's Section F expects "two commits". | A 27k-insertion dry run against a top-tier narrator is slow and costly. | **Add constraint** to Stage 1 — select a bounded pair: non-trivial but small. |
| **Working tree is not clean and the old fixture's retirement is already in flight.** `dev/phase-final-review/fixtures/**` (14 tracked files) are deleted in the working tree but uncommitted; `.github/learnings/cross-phase-decisions.md` is modified. | Do not assume a clean baseline. The old fixture's deletion may belong to a sibling. | **Confirm owner** (02 or 08) before touching it here. |
| **The `!dev/phase-final-review/` un-ignore rules go dead** once the old fixture retires. | Leftover gitignore rules for a path that no longer exists. | **Confirm owner** — likely `08-retirement-reconciliation`. |
| `dev/pr-review/` does not exist in any form. | This feature creates the tree. | **None** |

## Architectural Decisions

- **Rescope, do not rewrite** (plan §C). The existing orchestrator already embodies the numbered-orchestrator house style. The parts that survive are the parts that were never about phases: the preflight checklist shape, the evaluator invocation template, the model-tier table, the `evaluator-status.jsonl` contract, and bounded-wait semantics.
- **The design is subtractive** (plan §D). ~180 of 249 lines are preflight, ledger parsing, artifact inventory, and write-back. The rescoped agent is a base confirmation, a fan-out, and a report path. Deleting the write-back path is the single highest-value action in the phase — it was the riskiest implemented code (two-file transactional edits with restore-on-failure) and the rescope leaves it with no reason to exist.
- **Base derivation is suggest-and-confirm, because git cannot do better.** A ref is a SHA with no parentage. The reflog records the SHA, never the branch name, and is local-only and gc-pruned. `origin/HEAD` names the remote's *default* branch, not this branch's base. There is no correct algorithm.
- **Self-exclusion is load-bearing** (AC4). A branch is always its own nearest base, and so is its remote-tracking ref. Any ranking that omits the filter returns the branch under review with a diff of nothing — a run that reports no findings and looks like a pass.
- **Preflight collapses from four steps to two.** Steps 2 (subphase discovery) and 3 (artifact inventory) are deleted; step 1 becomes base suggest-and-confirm; step 4 (model tier) survives. Both remaining questions merge into the single upfront block.
- **The report root is keyed by SHA + timestamp so no branch name — an attacker-influenceable string — reaches a filesystem path.** There is no sanitizer because there is nothing to sanitize.
- **Security is delegated to the existing `04e-diff-security-scan`**, which is already diff-shaped and already holds no `execute`. No new security agent is authored.
- **The orchestrator retains `execute`** because base derivation needs `git`. Per-agent command scoping is not expressible on Claude (`tools: Bash(git:*)` is an unresolved tool name that makes Claude Code refuse to launch the agent). Recorded as residual risk routed to a hook-owning phase.

## Constraints

- **After the upfront block, no code path may introduce a new prompt** (AC2) — including evaluator failure, timeout, absent `gh`, and no-PR-exists. This is the requirement most likely to erode silently, one reasonable-seeming question at a time.
- **The agent writes no status line** in `PROJECT_ROADMAP.md` or any phase summary on any path (AC9). Verdicts are issued by the user by hand.
- **Deleted machinery must not survive in any form** (AC8) — not commented out, not behind a flag.
- **The verdict can never be GO while any check is missing** (AC11).
- **The orchestrator never reads code or diffs** (AC12); it inspects path metadata and reads only structured reports under the run's report root. Every subagent return is ≤10 lines.
- **Do not record model or harness identity** in retained reports — an existing constraint that survives the rescope.
- **Do not restate report templates or severity levels** — they live in `pr-review-report` / `pr-review-conventions` (feature 03).
- **One-way output only.** Never read PR comments or other network-sourced text back in; ingestion is a prompt-injection surface.
- The `name:` value must not be a substring of common prose (see Discovery Delta).

## Scope Boundaries

- **Do not implement `gh` posting.** The *choice* is captured here (AC2c); the posting path is `07-synthesis-and-pr-posting`, which edits this same file again.
- **Do not rescope any evaluator's internals** — features `05`–`07` own that.
- **Do not narrow any `execute` grant.** The phase's allowlist deliverable was deleted because per-agent command scoping is not expressible on Claude.
- **Do not do any hook work**, including an enforcement hook on the verdict. Advisory only.
- **Do not rename the `05x` evaluators here** — features `05`–`07` own their own slugs.
- **Do not touch `worktree-baseline`** — deliberately generic and shared with `eval-grader`.
- **Do not hand-delete orphaned generated files.** `claude/commands/phase-final-review.md` must disappear via feature `01`'s pruning (AC14); hand-deleting it would hide whether pruning works.
- **Preserve** the `evaluator-status.jsonl` contract, the bounded wait, the ≤10-line return contract, and the read-only etiquette verbatim in force.

## Relationships to Sibling Plans

- **Depends on `03-pr-review-conventions-skills`** (wave 3) — this agent is authored against its report roster, report root, and return contract.
- **Depends on `01-propagator-orphan-pruning`** (wave 1) — AC14. The orphaned `claude/commands/phase-final-review.md` is the sharpest case: it stays user-invocable, so a stale command file leaves a live slash command pointing at a deleted agent.
- **Follows `02-retired-evaluator-removal`** (wave 2), which already edits this file's `agents:` roster and body mentions to drop the five retired evaluators, and owns `.github/agents/README.md` for retired rows.
- **Blocks `05`, `06`, `07`** — each evaluator is dry-run through this orchestrator as it lands.
- **`07-synthesis-and-pr-posting` edits this file again** to add the posting path — the reason that feature is `parallel_safe: no`.
- **Shares `tests/test_propagate_master_assets.py`** with features 01, 02, 03, 05, 06, 07 — the phase-wide sequential bottleneck.

## Suggested Implementation Order

Wave 4, after `01`, `02`, and `03`. Within the feature, follow the plan's stages: Pin the Fixture → Subtract → Base Suggest-and-Confirm → One Interaction, One Roster → Rename, Propagate, Dry-Run. Subtract before adding: the deletions (Stage 2) shrink the surface the later stages edit.

## Environment State

| Property | Value |
|---|---|
| Tech Stack | Agents are Markdown with YAML frontmatter in `.github/agents/`; propagated by `scripts/propagate_master_assets.py` to `claude/`, `opencode/`, `codex/`. Tests are Python. |
| Test Runner | `.venv/bin/python -m pytest tests/ -q` — **system `python3` has no pytest; `.venv/bin/python` is required** |
| Test Baseline | 416 passed, 15 subtests passed — captured 2026-07-16 across 4 consecutive full runs, all green |
| Lint | Not configured |
| Format | Not configured |

## Relevant Learnings

From `.github/learnings/cross-phase-decisions.md`, **PR-Review Rescope (Phase 03; resolved 2026-07-16)**:

- **Git cannot determine a branch's base. This is a data-model fact, not a tooling gap — do not design around an assumption that it can.** A ref is a SHA and nothing else. `git merge-base HEAD main` requires already knowing the base (circular); the reflog records `branch: Created from HEAD` — the *SHA*, never the branch name — and is local-only, never cloned, and gc-pruned at 90 days, so it is absent in CI and fresh clones; `git symbolic-ref refs/remotes/origin/HEAD` is the most reliable signal but yields the repo's *default* branch rather than *this branch's* base, and is frequently unset. **The chosen design is suggest-and-confirm.** Suggestion order is `origin/HEAD` → `origin/main` → `origin/master` → present candidates.
- **The nearest-merge-base heuristic returns the branch under review. Exclude self and self's tracking ref explicitly.** Demonstrated on `repo_improvements_project` at HEAD `ae9823a`: `git merge-base HEAD main` and `git merge-base HEAD origin/main` both give `e3398c7`, but `git merge-base HEAD repo_improvements_project` and `git merge-base HEAD origin/repo_improvements_project` both give `ae9823a` — HEAD itself. **A branch is always its own nearest base, and so is its remote-tracking ref.**
- **Per-agent command scoping is not expressible on Claude at all.** A subagent's `tools:` frontmatter accepts only bare tool names and MCP patterns; `tools: Bash(gh:*)` is not a narrower grant but an *unresolved tool name*, and Claude Code refuses to launch the subagent. Command scoping exists only in project/session-wide `settings.json` rules or a per-agent PreToolUse hook, which this phase excludes.
- **The `gh` grant never cost anything.** The orchestrator needs `git symbolic-ref`/`git merge-base`/`git branch` for base derivation, so it holds unrestricted Bash *regardless* of the PR-comment feature. Adding `gh` widens nothing.
- **One upfront interaction is a design outcome, not a politeness feature.** It became achievable only because ledger disambiguation, artifact refusal, and write-back ambiguity were all removed, leaving base confirmation as the only blocking question. **A question asked after the work is on disk blocks nothing** — that is what makes "ask me once the report is written" both unattended and safe. Guard this.
- **Removing the multi-subphase premise deleted work rather than moving it.** `merge-base` replaced all of the baseline machinery. **If a rescope only relocates work, suspect the new scope is the old scope wearing a hat.**
- **The seven survivors renumber contiguously to `05a`–`05g`**; five phase-shaped evaluators are deleted.
- **Reports land at `dev/pr-review/<base-sha-short>-<UTC-timestamp>/`** — keyed only by hex and digits, so no branch name reaches a filesystem path and no sanitizer exists to be wrong; every run owns its directory, which also deletes archive-before-overwrite.

From **Phase Numbering**:
- **Agent numbers are pipeline positions, not phase numbers.** `05-phase-final-review` and its evaluators follow `04-phase-execute` in the pipeline; they did not renumber with the phase and must not be "corrected" to match it.

From **Propagation Contracts**:
- The propagator's generated roots are `claude/`, `opencode/`, and `codex/`; `.claude/skills/` and `.claude/agents/` are **not** generated destinations.
- `$source` metadata is guaranteed for propagated hook JSON entries, **not** for generated skill or agent Markdown/TOML.

From **Release Verification**:
- **A fixed budget must never be relaxed to make a gate pass.** If a criterion is genuinely unachievable, the honest outcome is an explicit user-approved AC change, not a quietly edited threshold.
