# qa Plan: Phase 02 — Engagement Comparison Analysis Fleet

**Date:** 2026-07-22
**Mode:** Release qa Plan
**Scope:** The engagement orchestrator (`Engagement - Orchestrator`) and its eight hidden subagents (audit runner, delta synthesizer, security narrative, introduced issues, pricing researcher, narrative writer, compliance writer, gap reviewer), plus the `engagement-workspace` and `engagement-package-manifest` skills and the `mode` field / Comparative Scans extensions to existing skills.
**Environment:** Local machine with the agents deployed to a real harness (Claude Code recommended) and a real prepared engagement pair available.

**Prerequisites:**

- Propagate and deploy the Phase 02 assets:
  - `python3 scripts/propagate_master_assets.py --once` (run twice; second run must report `converged: true, changed_passes: 0`)
  - `python3 deploy_agents.py --harness claude` (confirm `~/.claude` gains `engagement-orchestrator` and the `z-engagement-*` subagents)
- A test engagement: two local repos forming one comparison pair (an "original" and an "upgraded" side), plus an engagement configuration per the `engagement-configuration` skill (`source_of_truth/skills/engagement-configuration/SKILL.md`) with `sow` and `deliverables-spec` pointers and a per-pair `mode` (`modernization` or `modernized-and-improved`).
- Run `Engagement - Prepare` (or let the orchestrator spawn it) so at least one pair has analysis branches, docs-writer sets, and code graphs on both sides — see the `engagement-preparation-runbook` skill.
- For qa-4, the upgraded side must contain at least one security finding with no original-side counterpart (plant one deliberately if needed, e.g., a hardcoded credential in a file new to the upgraded side).

## Features Covered

| Feature | Plan | Implementation Record | Review Record |
|---------|------|-----------------------|---------------|
| 14-engagement-orchestrator-core | `dev/feature/14-engagement-orchestrator-core/14-engagement-orchestrator-core-plan.md` | `.../14-engagement-orchestrator-core-implementation.md` | `.../14-engagement-orchestrator-core-review.md` (Approved) |
| 15-comparative-audit-runs | `dev/feature/15-comparative-audit-runs/15-comparative-audit-runs-plan.md` | `.../15-comparative-audit-runs-implementation.md` | `.../15-comparative-audit-runs-review.md` (Approved with Reservations) |
| 16-delta-security-synthesis | `dev/feature/16-delta-security-synthesis/16-delta-security-synthesis-plan.md` | `.../16-delta-security-synthesis-implementation.md` | `.../16-delta-security-synthesis-review.md` (Approved) |
| 17-narrative-spec-docs | `dev/feature/17-narrative-spec-docs/17-narrative-spec-docs-plan.md` | `.../17-narrative-spec-docs-implementation.md` | `.../17-narrative-spec-docs-review.md` (Approved) |
| 18-compliance-package-manifest | `dev/feature/18-compliance-package-manifest/18-compliance-package-manifest-plan.md` | `.../18-compliance-package-manifest-implementation.md` | `.../18-compliance-package-manifest-review.md` (Approved with Reservations) |

## Coverage Map

- `docs/phases/PHASE_02/PHASE_02_qa_COVERAGE_MAP.md`

---

## Summary of Changes

Phase 02 built the engagement comparison fleet: a single orchestrator that consumes an engagement configuration, spawns `Engagement - Prepare` unchanged, then per comparison pair runs comparative audits (security, code, dependencies, infra — both sides, existing auditors unchanged), delta/security synthesis (delta report, security narrative, introduced-issues report, audit-trail proof, cloud/cost analysis), narrative/spec documents (business design, intended-behavior spec, workflow narratives), and an engagement-final compliance stage (SOW walkthrough, verification summary, package manifest, gap review). All outputs land in one workspace root outside every client repository; the orchestrator maintains `engagement-state.md` as its run record; the pricing researcher is the only engagement agent permitted internet access.

Expected workspace layout (from the implementation records):

```
<workspace-root>/
  engagement-state.md
  manifest.md
  pairs/<pair>/<side>/audits/<dimension>/{*-report.md, *-summary.md}
  pairs/<pair>/<side>/engagement-baseline-snapshot.md   (copied by manifest step)
  pairs/<pair>/exclusions-partition.md
  deliverables/<pair>/{delta-report,security-narrative,audit-trail-proof,cloud-cost-analysis,business-design,intended-behavior-spec,workflow-narratives}.md
  deliverables/{sow-compliance-walkthrough,verification-summary}.md
  internal/<pair>/introduced-issues.md
  internal/gap-review.md
```

## Automated Test Coverage

Skip re-verifying any of the following — automation and completed code review already prove them:

- Propagation fixed point, source↔generated sync, marker guards, agent/skill counts, deploy safety, naming (`z-` prefixes, aliases): `uv run pytest tests/` — 233 passed, 113 subtests at phase end; feature 18 reconciled all counts.
- Static definition content: skill schemas (`mode` field and backward compatibility, Comparative Scans convention, manifest schema rules), grant lists (pricing researcher sole web grant, others `[read, search, edit]`), reused auditors unmodified, all wording rules (NOT RUN / NOT VERIFIED / "new or newly-visible" / internal-only headers), brevity — all verified as code-review evidence in the five review records.

Manual qa exists **only** to verify runtime delegation behavior — that the deployed fleet, when actually run, follows its instructions.

---

## Manual qa Checklist

Organized by integration surface. Item numbers (qa-1 … qa-8) match the execution manifest's verification assets and the coverage map.

### End-to-End Orchestrator Run

**Features:** 14, 15, 16, 17, 18
**Covers ACs:** 14/AC1–AC5, 15/AC1–AC2, 16/AC8, 17/AC4, 18/AC1–AC2, 18/AC5
**Why manual:** Runtime delegation of a nine-subagent fleet cannot be verified by static tests; the phase plan (18/AC5) designates the full run as the runnable-whole check.

- [ ] **qa-1: Full run against a prepared pair** — With the test engagement prepared on both sides, invoke `Engagement - Orchestrator` with the engagement configuration. Let it run to completion. **Expected:** the complete markdown set from the layout above exists in one workspace root **outside** both client repos — per-pair deliverables (delta report, security narrative, audit-trail proof, cloud-cost analysis, business design, intended-behavior spec, workflow narratives), engagement-level deliverables (SOW walkthrough, verification summary), internal artifacts (introduced-issues, gap-review, exclusions partition), raw audit reports, `engagement-state.md`, and `manifest.md`. `git status` in each client repo shows no new files, and no client-repo branch history changed (`git log` on the real branches byte-identical to before).
- [ ] **qa-2: Unprepared side is named, pair blocked** — Delete or rename one side's analysis branch/graph (or use a fresh engagement where one side never ran preparation), then invoke the orchestrator past the prepare step (e.g., resume a run). **Expected:** the run report and `engagement-state.md` name the **exact side** (pair + side) that is unprepared and what is missing; no audit, synthesis, narrative, or compliance stage runs for that pair; no partial artifacts appear for it.

### Comparative Audit Runs & One-Side Re-Run

**Features:** 15 (with 14's working state)
**Covers ACs:** 15/AC1, 15/AC2, 15/AC4; 14/AC5 (state refresh)
**Why manual:** Report retention layout and overwrite-in-place scoping are observed on-disk outcomes of a real run.

- [ ] **qa-3: Per-pair per-side reports; one-side re-run refreshes only that side** — After qa-1, list `pairs/<pair>/<side>/audits/` for both sides. **Expected:** each side has one directory per dimension (security, code, dependencies, infra) containing the auditor's natural `-report.md`/`-summary.md` files. Then note the mtimes/contents of both sides' reports, make a small change on the upgraded side, and instruct the orchestrator to re-run only that side's scans (15's one-side re-run flow). **Expected:** only the upgraded side's report files and downstream synthesized artifacts change; the original side's report files are byte-identical to before; `engagement-state.md` records the refresh.

### Security Synthesis Correctness

**Features:** 16 (consuming 15's convention)
**Covers ACs:** 16/AC2, 16/AC3, 16/AC4
**Why manual:** Per-finding matching and labeling judgments on real reports, and no-SOW instruction-following, are runtime behaviors.

- [ ] **qa-4: One-sided finding matching and "new or newly-visible" labeling** — Ensure the upgraded side has a planted security finding absent from the original side (see Prerequisites), run (or re-run) the synthesis stage, then open `internal/<pair>/introduced-issues.md`. **Expected:** the one-sided finding appears with full technical detail (file, finding, severity, evidence) using the Category + file-path matching key; any finding whose original-side visibility is ambiguous (e.g., a file the original scan could not see) is labeled **"new or newly-visible"**, not asserted as introduced; the report carries the internal-only header and the fix→re-run flow.
- [ ] **qa-5: No-SOW run** — Run the engagement (or the synthesis + compliance stages) with the configuration's SOW pointer absent. **Expected:** exclusions routing is skipped — every original-side finding stays in the delta report's findings (nothing routed to out-of-scope or narrative §3); the missing SOW is recorded in `engagement-state.md` and reflected honestly in the SOW compliance walkthrough and the manifest's SOW-required labels ("no SOW" state, not silently "above-contract"); count the findings in the raw security/code reports vs. the synthesized documents — **no finding is dropped**.

### Value-Story Mode Framing

**Features:** 16, 17 (consuming 14's `mode`)
**Covers ACs:** 16/AC1, 17/AC1–AC3
**Why manual:** Whether prose framing matches the declared mode is a human reading judgment on real generated documents.

- [ ] **qa-6: Both modes produce correct framing** — Run the synthesis + narrative stages once with the pair's `mode: modernization` and once with `mode: modernized-and-improved` (two runs or two pairs). **Expected:** in modernization mode, `delta-report.md` and `workflow-narratives.md` contain **no** intentional-change/improvement framing — behavior differences are framed as "modernized, nothing changed" or honestly flagged, never as intended enhancements; in modernized-and-improved mode, intentional changes are narrated as improvements and **not** framed as regressions. `intended-behavior-spec.md` contains both mandatory sections (observable behavior; environmental assumptions), with unverified assumptions stated as assumptions. `business-design.md` reproduces no engagement source code.

### Pricing Researcher Query Hygiene & Offline Fallback

**Features:** 16
**Covers ACs:** 16/AC6
**Why manual:** The phase's highest-sensitivity control — only inspection of a real query log and a real offline session proves it.

- [ ] **qa-7a: Query log contains no engagement content** — Run the Cloud/Cost Analysis stage with internet available, then inspect the session's web-search/fetch calls (harness transcript/log for the `z-engagement-pricing-researcher` invocation). **Expected:** every query contains only generic service/product names and pricing questions (e.g., "AWS Lambda pricing 2026"); no client code, config values, repo names, identifiers, or any other engagement content appears in any query or fetched URL. Every quantified figure in `cloud-cost-analysis.md` cites source and retrieval date.
- [ ] **qa-7b: Offline run yields NOT RESEARCHED** — Re-run the stage with network access disabled (or web tools denied). **Expected:** `cloud-cost-analysis.md` is qualitative-only; every would-be quantified claim is marked **NOT RESEARCHED**; no dollar figures or numbers appear without a citation — no invented figures.

### Package Manifest & Gap Review

**Features:** 18
**Covers ACs:** 18/AC3, 18/AC4
**Why manual:** Mechanical missing-detection and the always-emit rule must be observed on a real package.

- [ ] **qa-8: Missing document flagged; gap-review present in technical section** — After a full run, delete one client-facing deliverable (e.g., `deliverables/<pair>/audit-trail-proof.md`) and re-run the compliance/manifest/gap-review stage. **Expected:** the corresponding `manifest.md` row reads **missing** (not omitted, not suppressed) with its name/path/audience/SOW-status columns intact, and the gap-review report flags the gap. Independently verify `internal/gap-review.md` exists and is listed as a standing entry in the manifest's **technical/internal** section (alongside raw reports, introduced-issues, working state, and baseline snapshots), and that `internal/introduced-issues.md` appears only in the technical section, never client-facing.

---

## Cross-Cutting Concerns

### Security
- [ ] **Confirm client content containment across the whole run** — After qa-1, search the workspace deliverables for verbatim engagement source code (spot-check a few distinctive strings from the client repos with `grep -r "<distinctive-string>" <workspace-root>/deliverables/`). **Expected:** business-framed descriptions only; no reproduced source blocks in client-facing documents; nothing from the engagement was committed to this repository (`git status` clean here).

### Operability
- [ ] **Resume from working state** — Interrupt a run mid-loop (kill the session after the audit stage), restart the orchestrator with the same config. **Expected:** it resumes from `engagement-state.md` — completed sides/stages are not redone; no silent restart-from-zero.

---

## Notes

- Reviews 15 and 18 were "Approved with Reservations"; see their `-review.md` files for the reservation details before signing off.
- Known cosmetic gap (out of scope, recorded in 18's implementation record): `docs/CODEBASE_CONTEXT.md` line 15 names `prod-code-review.md` while the file on disk is `04f-prod-code-review.md`.
- PDF assembly/branding, coverage quality gates, and finding remediation are phase non-goals — do not qa them.
- qa-3's re-run and qa-8's deletion mutate the workspace; do them **after** qa-1's layout verification, and re-run the affected stages before any final package sign-off.
