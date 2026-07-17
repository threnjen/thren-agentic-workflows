# 05 Mechanical Evaluators — Context

## Key Files

### Files being changed

| File | Role | Change Type |
|---|---|---|
| `.github/agents/05g-artifact-sweeper.agent.md` | Cheap-tier mechanical sweep for debug artifacts, TODO/FIXME markers, dead code. Verified `tools: [read, search, edit, execute]`. | Rename → `05c-artifact-sweeper.agent.md`; Modify |
| `.github/agents/05j-consistency-auditor.agent.md` | Cheap-tier convention-drift comparison. Verified `tools: [read, search, edit, execute]`. | Rename → `05d-consistency-auditor.agent.md`; Modify |
| `.github/agents/05k-dependency-auditor.agent.md` | Cheap-tier offline dependency inventory. Verified `tools: [read, search, edit, execute]`. | Rename → `05e-dependency-auditor.agent.md`; Modify |
| `tests/test_propagate_master_assets.py` | Roster + propagation enumeration. Verified: class `PropagateMasterAssetsTests`, method `test_phase_review_agents_match_all_generated_harness_outputs` (line 87), `expected_slugs` tuple (lines 89–98), blanket `self.assertNotIn("execute", agent.tools)` (line 116). | Modify |
| `claude/agents/z-artifact-sweeper.md`, `z-consistency-auditor.md`, `z-dependency-auditor.md` | Generated Claude outputs. All three stems verified present. | Regenerate |
| `opencode/agents/05g-artifact-sweeper.md`, `05j-consistency-auditor.md`, `05k-dependency-auditor.md` | Generated OpenCode outputs, keyed on slug — will orphan on renumber. | Regenerate + prune old slugs |
| `codex/agents/z-artifact-sweeper.toml`, `z-consistency-auditor.toml`, `z-dependency-auditor.toml` | Generated Codex outputs. | Regenerate |

### Read-only reference files

| File | Why it matters |
|---|---|
| `scripts/propagate_master_assets.py` | `_discover_existing_stems` (:376), `_claude_filename_for` (:389), `_claude_identifier_for` (:408), `_opencode_identifier_for` (:448). Confirms Claude names key on stem, OpenCode on slug. `"execute" -> ["Bash"]` at :332 and `-> ["bash"]` at :353 — no allowlist syntax. |
| `.github/learnings/cross-phase-decisions.md` | Lines 56–58 record the enumeration gap, the `05a` execute risk, and the correction voiding the allowlist deliverable. Line 86 records the never-restore-broad-shell rule. |
| `.github/agents/05a-baseline-worktree.agent.md` | Verified `tools: [read, search, execute]`. In the settled seven, holds `execute`, and is currently **also** omitted from `expected_slugs`. See Discovery Delta. |
| `dev/feature/02-retired-evaluator-removal/` | Deletes the current occupants of the `05c`/`05d`/`05e` slugs. Hard prerequisite for the rename. |
| `dev/feature/03-pr-review-conventions-skills/` | Defines report root `dev/pr-review/<base-sha-short>-<UTC-YYYYMMDDTHHMMSSZ>/` (plan lines 42, 126). |

## Discovery Delta

| Finding | Impact | Action |
|---|---|---|
| **`05a-baseline-worktree` is also omitted from `expected_slugs`, and it holds `execute`.** The plan (lines 23–28) says the tuple omits exactly "the three agents" for the execute reason. Verified tuple: `05b, 05c-qa-consolidator, 05d-security-rollup, 05e-ac-regression, 05f-seam-analyzer, 05h-test-health, 05i-learnings-harvester, 05l-readiness-synthesizer` — **four** roster agents are omitted (`05a`, `05g`, `05j`, `05k`), all four holding `execute`. AC8's "re-derived over the settled seven-agent roster" necessarily pulls `05a` in, and `05a`'s `execute` is recorded in `cross-phase-decisions.md:16` as an **unclosable** accepted risk (`git worktree` has no non-shell equivalent). | AC8 cannot be satisfied without a per-agent `execute` expectation for `05a` — an agent this feature's non-goals never scope in. Silently omitting `05a` to keep the tuple clean reproduces the exact gap AC8 exists to close. | **Warning to Decomposer** — AC8 needs an explicit clause admitting `05a` to the tuple with a recorded justification, or the plan must state `05a` is out of roster. Tasks generated on the seven-agent reading. |
| **Slug collision: `05c`/`05d`/`05e` are occupied today** by `05c-qa-consolidator`, `05d-security-rollup`, `05e-ac-regression` — all deleted by feature `02`. The plan's `Depends on:` lists only `03` and `04`. | Feature `02` is the true blocking dependency for AC1; renaming before `02` lands collides. Wave 5 > wave 2 makes this safe in practice, so this is a declaration defect, not a scheduling bug. | **Update plan** — add `02-retired-evaluator-removal` to `Depends on:`. |
| **All three agents hold `edit`, not just `execute`** (`tools: [read, search, edit, execute]`). The plan discusses only `execute`. | `edit` is **genuinely required** — each agent writes its own report file. An implementer reading "read-only, never remediate" in the bodies may strip `edit` and break AC5. | **Add task** — per-agent tool expectations must pin `edit` as expected, not incidental. |
| **AC3's "unverified assumption" resolves in the affirmative for `05c` and `05d`.** Grepped both bodies for command usage: `05g-artifact-sweeper` references **no shell command** — its only external call is the code-review-graph `refactor_tool` MCP invocation (:43, :50). `05j-consistency-auditor` references **zero** commands. | The plan flags this as "not verified against their current bodies' actual command use" and defers to Stage 2. It is now verified: both are clean `execute` removals. | **Refines plan** — Stage 2 is a confirmation, not an investigation, for these two. |
| **AC4 is corroborated by the `05k` body.** Lines 34–42 already encode the offline contract: "a command that may fetch or update vulnerability data, or contact the network, is unavailable for this audit." | `05e-dependency-auditor` is the one justified `execute` retention. The named command must still be recorded per AC3. | **None** — plan is correct. |
| **AC5 timestamp format.** Plan writes `<timestamp>`; feature `03` defines `<UTC-YYYYMMDDTHHMMSSZ>`. | Cosmetic; the conventions skill is authoritative per the keep-it-clean checklist ("Report paths from the conventions skill, not restated"). | **None** — defer to `03`. |
| **Claude stem survival confirmed.** `z-artifact-sweeper.md`, `z-consistency-auditor.md`, `z-dependency-auditor.md` all exist; `_claude_filename_for` prefers an existing stem. | The plan's second unverified assumption holds. OpenCode orphans (`05g-*`, `05j-*`, `05k-*`) are real and need feature `01` pruning. | **None** — verify after propagation per AC9. |
| **No phase-scoped test directory pattern.** `tests/` contains only `hooks/`, `test_propagate_master_assets.py`, `test_readiness_synthesis_agents.py`. | No consolidated phase test file is missing; the plan's test placement is correct. | **None**. |
| **Exact-assertion tests exist.** `test_phase_review_agents_match_all_generated_harness_outputs` asserts rendered agent output equals the generated file byte-for-byte across all three roots, and asserts on `05d-security-rollup` body strings (`"NO-GO"`, `"NOT RUN"`). | Any body edit fails these until all three roots are regenerated. The `05d-security-rollup` conditional is removed by feature `02` — do not re-add it for the new `05d-consistency-auditor`. | **Add task** — regenerate all three roots in the same commit as any body edit. |

## Architectural Decisions

- **Removal is the only narrowing available.** Per-agent command scoping is not expressible in Claude subagent frontmatter — `tools:` accepts only bare tool names and MCP patterns; `tools: Bash(gh:*)` is an unresolved tool name that refuses to launch. The propagator's allowlist deliverable was deleted for this reason (`cross-phase-decisions.md:58`). So AC3's options are exactly two: drop `execute`, or justify it by named command.
- **Justification must name a command, not a rationale.** "Retaining `execute` with a comment explaining why it is fine is precisely the pattern the recorded rule prohibits" (`cross-phase-decisions.md:86`). The justification names a command with no non-shell equivalent, or the grant goes.
- **Three near-identical preambles are accepted duplication.** These are separate prompts, not shared code. Shared content lives in `pr-review-conventions`.
- **Mechanical sweeps do not grow judgment.** Cheap tier is authoritative. "This TODO looks important" is `05b`'s job.
- **The graph MCP is an availability dependency, not a fallback.** When unavailable, report not-run with a stated reason and drop the verdict ceiling below GO. Never silently degrade to grep and report as if the graph answered.

## Constraints

- Cheap-tier assignment from the orchestrator is authoritative; a tier limitation is an **execution condition**, never evidence a check passed (AC7).
- **Added-line attribution is required.** Touched-file filtering is insufficient (AC6). A branch adding one line to a 900-line file did not introduce that file's 12 pre-existing TODOs.
- Report-only. Never remediate, never modify source.
- `05e-dependency-auditor` treats network-capable commands as unavailable (AC4).
- The `assertNotIn("execute", ...)` assertion may be **replaced** with per-agent expectations — never deleted, and never worked around by dropping an agent from the tuple (AC8).
- Report paths come from the conventions skill; do not restate them in agent bodies.

## Scope Boundaries

- **Do not** add allowlist syntax to the propagator — deleted from this phase.
- **Do not** touch `04e-diff-security-scan` or `test-analyst`.
- **Do not** rewrite the code-review-graph MCP integration.
- **Do not** rescope `05b`/`05f` (feature `06`) or `05g-readiness-synthesizer` (feature `07`).
- **Do not** strip `edit` — it is required for report writing.
- **Do not** re-add the `05d-security-rollup` body conditional under the new `05d-consistency-auditor` slug.
- Preserve the house pattern in all three bodies: load the conventions skill, take the tier assignment as authoritative, report-only.

## Relationships to Sibling Plans

- **Depends on `02-retired-evaluator-removal`** (undeclared in the plan — see Discovery Delta): frees the `05c`/`05d`/`05e` slugs.
- **Depends on `03-pr-review-conventions-skills`**: report root contract.
- **Depends on `04-pr-review-orchestrator`**: supplies the confirmed base and the roster naming these slugs. `04`'s AC4 prevents the empty-diff failure mode.
- **Depends on `01-propagator-orphan-pruning`** transitively: AC9's OpenCode orphan removal relies on `01`'s pruning.
- **Same wave as `06-narrative-and-test-health`, sequential with it** — both edit `expected_slugs` in `tests/test_propagate_master_assets.py`.
- **`07-synthesis-and-pr-posting`** consumes these agents' reports through `pr-review-report` templates only, never their internals.

## Suggested Implementation Order

Waves 1–4 (`01`, `02`, `03`, `04`) land first. Within this feature: Stage 1 → 2 → 3 → 4. Coordinate the `expected_slugs` edit with `06` — whichever runs second rebases onto the other's tuple rather than re-deriving it independently.

## Environment State

| Property | Value |
|---|---|
| Tech Stack | Agents are Markdown + YAML frontmatter in `.github/agents/`; propagated to `claude/`, `opencode/`, `codex/` via `scripts/propagate_master_assets.py` (Python) |
| Test Runner | `.venv/bin/python -m pytest tests/ -q` (system `python3` has no pytest — must use `.venv/bin/python`) |
| Test Baseline | 416 passed, 15 subtests passed — captured 2026-07-16 across 4 consecutive full runs, all green |
| Lint | Not configured |
| Format | Not configured |

## Relevant Learnings

From `.github/learnings/cross-phase-decisions.md`:

- **:58 (the binding constraint)** — "per-agent command scoping is not expressible on Claude at all, so the propagator was never the binding constraint. A subagent's `tools:` frontmatter accepts only bare tool names and MCP patterns; `tools: Bash(gh:*)` is not a narrower grant but an *unresolved tool name*, and Claude Code refuses to launch the subagent." OpenCode supports real per-agent `permission.bash` globs; Codex has none. Native per-agent scoping exists on **one of three harnesses** — building it anyway is "partial protection that reads as total protection."
- **:56 (this feature's charter)** — "`execute` grants on `05`/`05g`/`05j`/`05k` (set them correctly when each agent is rebuilt, rather than fixing them twice — note `05k` is not a simple removal, its contract permits an offline read-only audit command); `05a`'s unconstrained `execute`; and the propagation-enumeration gap omitting `05g`/`05j`/`05k` (only correct once the roster is settled at seven contiguous slugs)."
- **:86 (governs AC3)** — "Never restore unrestricted shell/Bash permissions to satisfy an evaluator acceptance criterion. The correct move is a narrowly scoped capability — an offline audit mode, a verifiable evidence bundle from the orchestrator, a command allowlist — never a broad grant with a comment explaining why it is fine."
- **:16 (governs the `05a` delta)** — "when the honest fix requires capability a phase has excluded, the phase records the finding — it does not redefine the finding to fit the scope." Names `05a-baseline-worktree`'s unconstrained `execute` as an explicitly unclosable High finding.
- **:6** — "Agent numbers are pipeline positions, not phase numbers." The `05a`–`05l` evaluators follow `04-phase-execute` in the pipeline; they did not renumber with the phase.
- **:60** — Reports land at `dev/pr-review/<base-sha-short>-<UTC-timestamp>/`, "keyed only by hex and digits, so no branch name reaches a filesystem path and no sanitizer exists to be wrong." The seven survivors renumber contiguously to `05a`–`05g`.

From `.github/learnings/review-learnings.md` / `project-learnings.md`: the recorded friction rule — **"rules matching ordinary text are defects, not safety"** — is the direct rationale for AC6. A sweep reporting pre-existing findings trains the reader to ignore the report.
