# Context: 15-comparative-audit-runs

## Key Files

### Files Being Changed

| File | Role | Change Type |
|------|------|-------------|
| `source_of_truth/skills/auditor-conventions/SKILL.md` | Shared auditor conventions; gains comparability section (stable categories, shared severity scale, security per-finding IDs, new/resolved classification) | Modify |
| `source_of_truth/agents/engagement-audit-runner.agent.md` [PROPOSED - name TBD] | Scan-run subagent(s) invoking the four audit dimensions per side, writing retained reports into the workspace layout | Create |
| `source_of_truth/agents/engagement-orchestrator.agent.md` [PROPOSED - name TBD, created by feature 14] | Roster entries + per-pair loop step invoking scan runs | Modify (shared with 14) |
| `tests/test_propagate_master_assets.py` | Marker-guard agent counts (lines ~766-771) | Modify (verify; bump if counts shift) |

### Read-Only Reference Files

| File | Role |
|------|------|
| `source_of_truth/agents/security-scan.agent.md` | Security dimension asset — reused unchanged; source of severity vocabulary (Critical/High/Medium/Low) and phase-relationship labels |
| `source_of_truth/agents/auditor-code.agent.md` | Code-quality dimension — reused unchanged (`z-auditor-code` when deployed) |
| `source_of_truth/agents/auditor-infra.agent.md` | Infra/config dimension — reused unchanged |
| `source_of_truth/agents/05e-dependency-auditor.agent.md` | Dependency/supply-chain dimension — reused unchanged (`z-dependency-auditor`) |
| `source_of_truth/agents/engagement-prepare.agent.md` | House style for engagement agents (frontmatter, security-boundary section, fail-fast, terse prose) |
| `dev/feature/14-engagement-orchestrator-core/14-engagement-orchestrator-core-plan.md` | Workspace layout, working-state schema, subagent contract this feature consumes |
| `docs/phases/PHASE_02/PHASE_02_SUMMARY.md` | Phase document (Key Deliverable 2, bundle 2) |

## Discovery Delta

| Finding | Impact | Action |
|---------|--------|--------|
| Feature 14 artifacts do not exist yet — `engagement-orchestrator.agent.md` and the engagement-workspace skill are both `[PROPOSED - name TBD]` in 14's plan (only `14-...-plan.md` exists; not yet expanded or implemented) | This feature cannot start until 14 lands; final orchestrator and workspace-skill names must be read from 14's implementation record | Confirmed sequential dependency; Implementer must resolve names from 14's output, not from this plan |
| `auditor-conventions/SKILL.md` verified: already defines the 4-level severity scale (Critical/High/Medium/Low) and a "Domain-Specific Extensions" section — natural insertion point for the comparability section | AC3 is an extension, not a new scale; severity labels are existing vocabulary, not `[PROPOSED]` | Reuse existing severity table; add only categories, security per-finding IDs, and new/resolved rules |
| `security-scan.agent.md` verified: uses Critical/High/Medium/Low and a findings table with `ID`, `Severity`, `Category`, `Location` columns plus phase-relationship labels (`Introduced`/`Worsened`/`Pre-existing`/`Unclear`) | Security per-finding matching identifiers should build on the existing `ID`/`Category`/`Location` columns rather than invent a new schema | Derive matching-identifier spec from this table |
| Count guard is at `tests/test_propagate_master_assets.py:766-771` (roots list: claude/agents 28, claude/commands 19, opencode 43, codex 43); comment mandates recounting from disk, not incrementing from memory | A new hidden (`user-invocable: false`) runner agent bumps opencode/codex counts but not claude/commands; 14 will also bump counts first | Recount from `ls ports/<harness>/agents` after propagation, per the in-file comment |
| Test baseline captured: 233 passed, 113 subtests, 0 failed | Clean baseline for AC7 comparison | None |
| No `.github/learnings/` entries specific to engagement audits; general propagate/count-guard learning applies (see Relevant Learnings) | Minor | None |
| No contradictions with the plan's approach otherwise | — | None |

## Architectural Decisions

- **Extend `auditor-conventions` in place** — all four reused audit assets already load or align with it, so comparability comes free without editing any auditor (plan §C).
- **Runner shape is an open design decision**: one runner agent parameterized by dimension+side, or thin per-dimension wrappers. Choose the fewest new definitions keeping the orchestrator handoff compact; the phase permits either. Document the choice in the implementation record.
- **Per-finding matching identifiers for security only**; category-level rollups for the other three dimensions. Unmatched findings are classified "new" or "resolved," never dropped.
- **Git history is the version record** for one-side re-runs — reports overwrite in place; no report-versioning machinery.
- Report filenames keep the existing `-report.md` / `-summary.md` convention; only their location (14's workspace layout, per dimension/side/pair) is new.

## Constraints

- `source_of_truth/` only; never hand-edit `ports/` or `.github/`; propagate to fixed point (second run reports zero changes).
- Do NOT modify `auditor-code`, `auditor-infra`, `05e-dependency-auditor`, or `security-scan` agent files (non-goal).
- Auditors keep existing grants — no shell grant added (AC5). Dependency vulnerability evidence is supplied offline or the dimension is NOT RUN — never a pass. Graph unavailability → NOT RUN with reason.
- NOT RUN on one side → recorded as **asymmetric evidence** for the pair, never a delta.
- Runner follows 14's subagent contract: return compact summary + report pointers only; inherited client-code boundaries pass through verbatim.
- Brevity (AC8): each rule stated once; the conventions extension must not restate what auditors already define.
- Category names in the conventions extension must be derived from the auditors' current vocabulary, not a parallel taxonomy; new labels are `[PROPOSED - names TBD]` until the implementer derives them.

## Scope Boundaries

- Delta synthesis and any client-facing document — feature 16.
- Remediation of findings — out of scope.
- Report-versioning machinery or heavyweight report schemas — not built.
- The four reused audit agent definitions — untouched.
- The other side's reports during a one-side re-run — must not be touched.
- Deduplicated repos across pairs: pointer reuse per (pair, side), not re-scan.

## Relationships to Sibling Plans

- **Depends on 14-engagement-orchestrator-core** (wave 1): consumes its workspace layout, working-state schema, subagent contract, and shares the orchestrator agent file. Not parallel safe.
- **Upstream of 16-delta-security-synthesis**: retained per-side reports and the comparability convention (categories, severities, security finding identifiers, asymmetric-evidence flag) are 16's inputs — these contracts are ACs here per the cross-feature API rule.

## Suggested Implementation Order

After 14 completes. Within this feature: Stage 1 (conventions extension) → Stage 2 (runner + orchestrator wiring) → Stage 3 (propagate + verify).

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Markdown agent/skill definitions + Python 3 (stdlib-only) transform/deploy scripts |
| Test Runner | `uv run pytest tests/` |
| Test Baseline | 233 passed, 113 subtests, 0 failed — captured 2026-07-22 |
| Lint | Not configured |
| Format | Not configured |
| Propagation | `python3 scripts/propagate_master_assets.py --once` (run twice; second run must report zero changes) |

## Relevant Learnings

- From repo conventions (`tests/test_propagate_master_assets.py:760-764` comment and prior count bumps): when agent counts shift, recount deployed files from disk (`ls ports/<harness>/agents`) rather than incrementing the guard from memory. A hidden subagent gets a `z-` prefix at deploy and appears in opencode/codex agent counts but not claude commands.
- Terse-definition constraint (CLAUDE.md / memory): authored agent and skill files are loaded into runtime context — state behavior, constraints, and output contract once each; a definition that says the same thing twice fails review.
- No other `.github/learnings/` entries applicable.
