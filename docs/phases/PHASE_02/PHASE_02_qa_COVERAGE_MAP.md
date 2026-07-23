# AC Coverage Map: Phase 02 — Engagement Comparison Analysis Fleet

**Date:** 2026-07-22
**qa Plan:** `docs/phases/PHASE_02/PHASE_02_qa.md`

All Phase 02 deliverables are Markdown agent/skill assets. Automated coverage is the existing propagation/deploy suite (`uv run pytest tests/`, 233 passed / 113 subtests at phase end, marker-guard counts reconciled by feature 18) plus per-feature code-review evidence recorded in each `-review.md`. What automation and static review **cannot** verify is runtime delegation behavior — whether the deployed orchestrator and its nine subagents actually produce the documented artifacts when run against a real prepared engagement. Those runtime behaviors are the only manual qa items.

| Feature | AC | Automated Coverage | Manual qa Needed? | Reason |
|---------|----|--------------------|-------------------|--------|
| 14-engagement-orchestrator-core | AC1 (slim orchestrator, per-pair loop) | Code-review evidence; sync suite guards generated file | Partial — runtime run only (qa-1) | Whether the orchestrator actually spawns subagents and holds only pointers is runtime behavior, unverifiable by static test |
| 14-engagement-orchestrator-core | AC2 (spawns engagement-prepare unchanged) | Code review; `git status` clean on prepare file | Partial (qa-1) | Live spawn is runtime behavior |
| 14-engagement-orchestrator-core | AC3 (entry check names unprepared side) | Code review of instruction paragraph | Yes (qa-2) | Instruction-following in a real run with a real unprepared side; text review cannot prove behavior |
| 14-engagement-orchestrator-core | AC4 (workspace root outside client repos) | Code review of workspace skill | Yes (qa-1) | Observed on-disk layout of a real run is the proof |
| 14-engagement-orchestrator-core | AC5 (working-state file, resume) | Code review | Partial (qa-1, qa-3) | State file written during a real run; resume/refresh behavior observed |
| 14-engagement-orchestrator-core | AC6 (boundaries passed to subagents) | Code review | No | Wording verified in review; runtime evidence indirect (qa-1 observes outputs stay local) |
| 14-engagement-orchestrator-core | AC7 (`mode` field, backward compatible) | Code review; skill sync tests; Phase-01 config validity walked in review | No | Schema/validation text, assertable by review |
| 14-engagement-orchestrator-core | AC8 (propagation fixed point, suite clean) | Full automated suite; marker guards | No | Fully automated |
| 14-engagement-orchestrator-core | AC9 (brevity) | Code review | No | Review judgment, complete |
| 15-comparative-audit-runs | AC1 (four dimensions, both sides, agents unchanged) | Code review; reused agent files git-clean | Partial (qa-3) | Real per-side runs producing reports is runtime behavior |
| 15-comparative-audit-runs | AC2 (raw reports retained per pair/side/dimension) | Code review of retention section | Yes (qa-3) | Files on disk in the agreed layout after a real run |
| 15-comparative-audit-runs | AC3 (comparability convention in auditor-conventions) | Code review; skill sync tests; category vocab cross-check done in review | No | Static convention text |
| 15-comparative-audit-runs | AC4 (one-side re-run, overwrite in place) | Code review | Yes (qa-3) | Observed: only that side's reports and downstream artifacts refresh |
| 15-comparative-audit-runs | AC5 (no new grants; NOT RUN never a pass; asymmetric evidence) | Code review (grant lists, wording) | No | Grant lists and wording are statically verifiable; downstream asymmetry surfacing is covered by review evidence checks |
| 15-comparative-audit-runs | AC6 (orchestrator wiring) | Code review; propagation resolves roster names | Partial (qa-1) | Runtime delegation |
| 15-comparative-audit-runs | AC7 (propagation, count guards) | Automated suite | No | Fully automated |
| 15-comparative-audit-runs | AC8 (brevity) | Code review | No | Review judgment, complete |
| 16-delta-security-synthesis | AC1 (delta document, mode framing) | Code review | Partial (qa-6) | Mode-dependent framing of a real synthesized document needs human reading |
| 16-delta-security-synthesis | AC2 (SOW-exclusions routing; no-SOW path) | Code review of partition section | Yes (qa-5) | No-SOW run: routing skipped, missing input recorded, no finding dropped — runtime instruction-following |
| 16-delta-security-synthesis | AC3 (security narrative, classification completeness) | Code review (walked in review: unclassified impossible by construction) | Partial (qa-4) | Real per-finding matching behavior on real reports |
| 16-delta-security-synthesis | AC4 (introduced-issues report, "new or newly-visible") | Code review (header, labeling, fix flow) | Yes (qa-4) | Correct labeling on a real one-sided finding is a runtime judgment call |
| 16-delta-security-synthesis | AC5 (audit-trail proof, NOT VERIFIED) | Code review (merged into synthesizer; wording verified) | No | Wording statically verified; presence in package covered by qa-8 |
| 16-delta-security-synthesis | AC6 (pricing researcher: query hygiene, offline fallback) | Code review (all rules in the one definition; sole web grant) | Yes (qa-7) | Only a real query log proves no engagement content leaks; only a real offline run proves NOT RESEARCHED over invented figures |
| 16-delta-security-synthesis | AC7 (asymmetric evidence never a delta) | Code review (fixed in review for pricing researcher) | No | Wording verified in all documents in review |
| 16-delta-security-synthesis | AC8 (orchestrator wiring) | Code review | Partial (qa-1) | Runtime delegation |
| 16-delta-security-synthesis | AC9 (propagation, guards) | Automated suite | No | Fully automated |
| 16-delta-security-synthesis | AC10 (brevity) | Code review | No | Review judgment, complete |
| 17-narrative-spec-docs | AC1 (business design doc, no source reproduction) | Code review | Partial (qa-6) | Output quality of a real document needs human reading |
| 17-narrative-spec-docs | AC2 (intended-behavior spec, env assumptions) | Code review (mandatory sections verified) | Partial (qa-6) | Real output contains both mandatory sections with honest assumptions |
| 17-narrative-spec-docs | AC3 (before/after narratives, both modes) | Code review (mode framing rules) | Yes (qa-6) | Both value-story modes must be exercised on real pairs; framing correctness is human judgment |
| 17-narrative-spec-docs | AC4 (orchestrator wiring) | Code review; resolved reference in ports verified | Partial (qa-1) | Runtime delegation (implementation record explicitly routes this to phase manual qa) |
| 17-narrative-spec-docs | AC5 (propagation, guards) | Automated suite | No | Fully automated |
| 17-narrative-spec-docs | AC6 (brevity) | Code review | No | Review judgment, complete |
| 18-compliance-package-manifest | AC1 (SOW compliance walkthrough) | Code review (criteria only from SOW; evidence citations) | Partial (qa-1, qa-5) | Real walkthrough against a real SOW; no-SOW honest state |
| 18-compliance-package-manifest | AC2 (verification summary references spec) | Code review | No | Static reference verified; presence covered by qa-1/qa-8 |
| 18-compliance-package-manifest | AC3 (manifest schema, present/missing detection) | Code review (one expected-entry rule per document; missing never suppressed) | Yes (qa-8) | Mechanical missing-detection must be observed flagging a deliberately missing document |
| 18-compliance-package-manifest | AC4 (gap review always emitted, in technical section) | Code review (unconditional-emit rule) | Yes (qa-8) | Presence of the internal report in a real package's technical section |
| 18-compliance-package-manifest | AC5 (end-to-end integration) | Code review of complete loop | Yes (qa-1) | The phase's runnable-whole check — explicitly designated manual qa in the plan |
| 18-compliance-package-manifest | AC6 (catalog/count reconciliation) | Existing count/derivation guards; code review | No | Fully automated + review |
| 18-compliance-package-manifest | AC7 (propagation, full suite) | Automated suite (phase-final gate, green) | No | Fully automated |
| 18-compliance-package-manifest | AC8 (brevity) | Code review | No | Review judgment, complete |

**qa item key:** qa-1 … qa-8 refer to the numbered manual checklist items in `PHASE_02_qa.md` (matching the execution manifest's verification assets).
