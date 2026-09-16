---
name: qa-generation
description: "Contract for generating a repository's two complementary QA documents — `docs/QA_AUTOMATED.md` (evidence-producing technical runbook for an agent or release engineer) and `docs/QA_USER.md` (plain-language manual acceptance checklist for an operator or client) — from the repository plus optional manual QA, SOW/contract, and plan acceptance inputs. Use when: writing or updating either QA document."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->
# QA Generation

Generate two documents for one repository. Accept the repository root and any
supplied inputs. Inputs may include existing user QA, manual QA writeups,
acceptance inputs (SOW, plans, deliverables specs, pasted ACs), and scope
notes. All inputs are optional except the repository root. Use
`docs/QA_AUTOMATED.md` and `docs/QA_USER.md` as the default outputs. When an
existing user-facing QA path is supplied, update that file in place instead of
creating `QA_USER.md`.

**Keep audiences separate.** Put source inspection, dependency audits, build
commands, automated tests, packaging, and security checks in QA_AUTOMATED. Put
observable installation and product workflows in QA_USER. Do not merge the
audiences or force symmetry.

## Operating rules

- Keep production source read-only. Limit changes to the two QA documents and,
  when applicable, a small discoverability link (README/docs index).
- Do not claim that a build, test, install, update, integration, or runtime
  behavior passed unless you directly observe it.
- Do not put credentials, tokens, connection strings, PINs, or passwords in QA
  documents or evidence examples. Do not use production resources without
  explicit written approval.
- Record low-risk assumptions. Ask only when an unresolved choice materially
  changes scope or acceptance.
- Use exact commands verified for the repository's toolchain. Do not use
  generic placeholders where the repository defines a supported command.
  Consult current primary documentation for SDK/CLI-dependent commands.
- For PDF acceptance sources, inspect rendered pages and extracted text when
  layout or scope labels may affect meaning.

## Phase 1 — Inventory

Record the branch and commit, languages, application type, platforms, and entry
points. Record active workflows. Do not assume legacy code is active. Record
main user and integration flows, test fixtures, and their environment
constraints. Record build/publish/installer/update/config/logging/recovery
behavior, compatibility-sensitive boundaries (APIs, headers, file formats,
storage, queues, auth, outputs), prerequisites versus bundled dependencies,
and known limitations.

## Phase 2 — Atomic acceptance inventory

Before drafting, build an internal inventory of atomic targets with stable
source IDs (`MANUAL-00N`, `SOW-00N`, `PLAN-00N`, `REPO-00N`). For each target,
record the following:

- exact source wording
- direct-repo, sister-project, excluded, conditional, or unresolved scope
- needed evidence type (static, automated, packaging, manual, live integration)
- implemented behavior and existing evidence
- planned QA_AUTOMATED check
- planned QA_USER check or why the target is agent-only

Apply this source hierarchy: signed SOW/contract ACs > approved plan/phase ACs
> client deliverables spec > existing manual QA > repository-derived evidence.
Do not silently discard a conflict. Preserve the legacy wording verbatim
(Appendix A). State the corrected active expectation and its reason. Map both
expectations. Flag a contractual acceptance risk when the correction conflicts
with an authoritative SOW. Sister-project internals never become a direct
pass/fail gate for this repository. Keep the cross-system handoff as an
integration checkpoint. Without SOW/plan inputs, label targets
repository-derived. Do not invent contract terms.

## Phase 3 — QA_AUTOMATED

Place a machine-readable verdict line as the document's **first line after the
title**. Set it to exactly `VERDICT: NOT RUN` at generation time. During an
execution run, rewrite it to `VERDICT: PASS` or `VERDICT: FAIL`. Match the
`Run results` section's `FINAL VALIDATION`. Downstream gates read only this
line. Include it exactly once.

Make the runbook self-contained. Include the following:

- purpose and audience
- acceptance sources and authority
- scope, boundaries, and exclusions
- result vocabulary (PASS, FAIL, BLOCKED, NOT RUN, N/A)
- final acceptance rules that state which unresolved statuses prevent signoff
- a run-evidence header (commit, branch, environment, toolchain, version,
  approved test resources, test data, and evidence location)
- safety/redaction rules

Use numbered stable `AG-QA-NNN` checks. Cover the following:

- repository and dependency scans
- build, warning, analyzer, test, and coverage gates
- packaging, installer, signing, fresh-install, and update checks where
  applicable
- auth, config, and selection checks
- every primary workflow with positive, negative, progress, recovery, and
  handoff paths
- background work, resume, cancel, retry, cleanup, retention, and diagnostics
- compatibility boundaries
- operations, maintenance, and limitations
- documentation and client-package completeness gates
- a final verification-summary requirement
- a traceability matrix mapping every applicable target to one or more checks

Each check must state its setup or command, exact expected result, and required
evidence. Each check must state whether static evidence is insufficient. Each
check must define blocker and cross-system failure classification. Do not write
a specific test, file, or item total into an expected result. A suite passes on
a successful exit code with zero failures. Do not require a number that grows
when someone adds a test. Include a **Run results** section. Set it initially to
"not yet run". During an execution run, record per-check status and the overall
result.

## Phase 4 — QA_USER

Make QA_USER executable by a non-developer. Include the following:

- plain-language purpose and scope
- product versus sister-system distinction
- Pass/Fail/Blocked definitions
- a test record (tester, date, environment, version, account, evidence, and
  overall result)
- a no-secrets warning
- prerequisites and representative-test-data checklist
- numbered stable `QA-NNN` checks covering:
  - installation and update
  - auth and authorization
  - every normal workflow with concrete actions and visible expected results
  - negative/error cases
  - responsiveness and recovery
  - cancel/retry/resume where implemented
  - end-to-end receiving-system checks (with sender-vs-receiver defect guidance)
  - maintenance/reinstall/known limitations/out-of-scope statements
  - delivery-documentation checks
  - a final signoff table

**Check template (mandatory shape, mechanically verified downstream).** Use this
shape for every check. Write prerequisite and test-data items as unchecked
checkbox lines (`- [ ]`). Write numbered action steps first. Write every
observable expected result as its own checkbox.

```markdown
### QA-NN - Title

1. Concrete action step.
2. Concrete action step.

Expected:

- [ ] Observable result.
- [ ] Observable result.

Status: Pass / Fail / Blocked

Evidence or issue:
```

Write every box unchecked. The tester marks `- [x]` only after observing that
result. Use checkboxes **only** on prerequisite items and expected results. Do
not use them on headings, notes, or appendix material. Downstream gates treat
any remaining `[ ]` in QA_USER as "manual QA not complete". Do not use the
inline-prose alternative (`**Expected:** ...` with a `Result: ______` line).
It defeats the mechanical completeness check.

## Phase 5 — Appendix A (original manual QA)

If any original manual QA writeup exists, append "Appendix A - Original manual QA checklist"
to QA_USER. Reproduce every original heading and question
verbatim and in original order. Do not apply silent fixes. Add labeled notes
for legacy wording whose active expectation was corrected. Keep the original
and appendix question counts exactly equal. Omit Appendix A only when no
original writeup exists.

## Phase 6 — Appendix B (target traceability)

Append "Appendix B - QA target traceability" to QA_USER. Add one row per atomic
manual target and per directly applicable SOW/plan criterion. Use these
columns: `Target ID | Source | Original target | Scope | QA_AUTOMATED coverage |
QA_USER coverage`. Link each row to exact check headings through stable
relative anchors. Use "Agent-only" for non-user-observable targets. Use
"Integration boundary" for cross-system handoffs. Use "N/A - sister project"
only with a reason. Do not group unrelated targets. Do not leave blank cells.
Do not write "covered elsewhere".

## Phase 7 — Cross-check

Run these cross-checks:

- Map every direct target to ≥1 AG-QA check.
- Map every user-observable target to ≥1 QA_USER check.
- Preserve Appendix A verbatim and match its counts.
- Complete Appendix B.
- Keep sister-project scope separate.
- Distinguish prerequisites from bundled dependencies.
- Ensure static evidence does not claim live behavior.
- Match commands, paths, and counts to the repository.
- Validate Markdown structure, anchors, and IDs.

Run these checks mechanically with grep, not judgment:

- QA_AUTOMATED contains exactly one `VERDICT:` line reading `VERDICT: NOT RUN`
  as the first line after the title.
- QA_USER contains at least one unchecked `- [ ]` box and no inline `Result: ___`
  prose forms.

Add a discoverability link from the docs index or README when one exists.

## Report

Return the following:

- both output paths
- AG-QA and QA_USER check counts
- preserved original question count
- traceability row count
- the most important scope separation or corrected legacy expectation
- validation performed
- any check blocked by a missing source, platform, credential, or environment

Do not claim that the product passed QA. This skill produces the specification
only.
