---
name: qa-generation
description: "Contract for generating a repository's two complementary QA documents — `docs/AUTOMATED_QA.md` (evidence-producing technical runbook for an agent or release engineer) and `docs/USER_QA.md` (plain-language manual acceptance checklist for an operator or client) — from the repository plus optional manual QA, SOW/contract, and plan acceptance inputs. Use when: writing or updating either QA document."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->

# QA Generation

Produce two documents for one repository, from whatever inputs were supplied
(all optional except the repository root): existing user QA, manual QA
writeups, acceptance inputs (SOW, plans, deliverables specs, pasted ACs), and
scope notes. Default outputs: `docs/AUTOMATED_QA.md` and `docs/USER_QA.md`;
when an existing user-facing QA path is supplied, update that file in place
instead of creating `USER_QA.md`.

**Audience separation is absolute.** Source inspection, dependency audits,
build commands, automated tests, packaging, and security checks belong in
AUTOMATED_QA. Observable installation and product workflows belong in
USER_QA. Never merge the audiences or force symmetry.

## Operating rules

- Read-only with respect to production source: only the two QA documents and
  a small discoverability link (README/docs index) may change.
- Never claim a build, test, install, update, integration, or runtime
  behavior passed unless directly observed.
- Never put credentials, tokens, connection strings, PINs, or passwords in QA
  documents or evidence examples; never use production resources without
  explicit written approval.
- Record low-risk assumptions; ask only when an unresolved choice materially
  changes scope or acceptance.
- Use exact commands verified for the repository's toolchain — no generic
  placeholders where the repo defines a supported command. Consult current
  primary documentation for SDK/CLI-dependent commands.
- For PDF acceptance sources, inspect rendered pages as well as extracted
  text when layout or scope labels may affect meaning.

## Phase 1 — Inventory

Record branch/commit, languages, application type, platforms, entry points,
active workflows (do not assume legacy code is active), main user and
integration flows, test fixtures and their environment constraints, build/
publish/installer/update/config/logging/recovery behavior, compatibility-
sensitive boundaries (APIs, headers, file formats, storage, queues, auth,
outputs), prerequisites vs bundled dependencies, and known limitations.

## Phase 2 — Atomic acceptance inventory

Before drafting, build an internal inventory of atomic targets with stable
source IDs (`MANUAL-00N`, `SOW-00N`, `PLAN-00N`, `REPO-00N`). Per target
record: exact source wording; direct-repo vs sister-project vs excluded/
conditional/unresolved; evidence type needed (static, automated, packaging,
manual, live integration); implemented behavior and existing evidence; the
planned AUTOMATED_QA check; the planned USER_QA check or why agent-only.

Source hierarchy: signed SOW/contract ACs > approved plan/phase ACs > client
deliverables spec > existing manual QA > repository-derived evidence. Never
silently discard a conflict: preserve the legacy wording verbatim (Appendix
A), state the corrected active expectation and why, map both, and flag a
contractual acceptance risk when the correction conflicts with an
authoritative SOW. Sister-project internals never become a direct pass/fail
gate for this repository — cross-system handoff stays an integration
checkpoint. Without SOW/plan inputs, label targets repository-derived; never
invent contract terms.

## Phase 3 — AUTOMATED_QA

The document's **first line after the title** is a machine-readable verdict
line, exactly `VERDICT: NOT RUN` at generation time. An execution run
rewrites it to `VERDICT: PASS` or `VERDICT: FAIL` (matching the Run results
section's `FINAL VALIDATION`); downstream gates read only this line, so it
appears exactly once.

Self-contained runbook containing: purpose/audience; acceptance sources and
authority; scope, boundaries, exclusions; result vocabulary (PASS, FAIL,
BLOCKED, NOT RUN, N/A) and final acceptance rules stating which unresolved
statuses prevent signoff; a run-evidence header (commit, branch, environment,
toolchain, version, approved test resources, test data, evidence location);
safety/redaction rules; numbered stable `AG-QA-NNN` checks covering:
repository and dependency scans; build/warning/analyzer/test/coverage gates;
packaging, installer, signing, fresh-install, and update checks where
applicable; auth/config/selection checks; every primary workflow with
positive, negative, progress, recovery, and handoff paths; background work,
resume, cancel, retry, cleanup, retention, diagnostics; compatibility
boundaries; operations/maintenance/limitations; documentation and
client-package completeness gates; a final verification-summary requirement;
and a traceability matrix mapping every applicable target to one or more
checks. Each check states the setup or command, exact expected result,
required evidence, whether static evidence is insufficient, and how to
classify blockers or cross-system failures. Include a **Run results** section
(initially "not yet run") where an execution run records per-check status and
the overall result.

## Phase 4 — USER_QA

Executable by a non-developer: plain-language purpose and scope; product vs
sister-system distinction; Pass/Fail/Blocked definitions; a test record
(tester, date, environment, version, account, evidence, overall result); a
no-secrets warning; prerequisites and representative-test-data checklist;
numbered stable `QA-NNN` checks covering installation and update, auth and
authorization, every normal workflow with concrete actions and visible
expected results, negative/error cases, responsiveness and recovery,
cancel/retry/resume where implemented, end-to-end receiving-system checks
(with sender-vs-receiver defect guidance), maintenance/reinstall/known
limitations/out-of-scope statements, delivery-documentation checks, and a
final signoff table. Every manual check: numbered steps, observable expected
results, Pass/Fail/Blocked, evidence-or-issue field.

**Checkbox contract (mechanically verified downstream):** every executable
manual check is a Markdown checkbox item written unchecked (`- [ ]`); the
tester marks it `- [x]` only after executing it and recording its result.
Checkboxes appear **only** on executable checks — never on headings, notes,
prerequisites prose, or appendix material — because downstream gates treat
any remaining `[ ]` in USER_QA as "manual QA not complete".

## Phase 5 — Appendix A (original manual QA)

When any original manual QA writeup exists, append "Appendix A - Original
manual QA checklist" to USER_QA reproducing every original heading and
question verbatim in original order — no silent fixes — followed by labeled
notes for any legacy wording whose active expectation was corrected. Original
and appendix question counts must match exactly. Omit only when no original
writeup exists.

## Phase 6 — Appendix B (target traceability)

Append "Appendix B - QA target traceability" to USER_QA: one row per atomic
manual target and per directly applicable SOW/plan criterion, columns
`Target ID | Source | Original target | Scope | AUTOMATED_QA coverage |
USER_QA coverage`, linking to exact check headings via stable relative
anchors. Use "Agent-only" for non-user-observable targets, "Integration
boundary" for cross-system handoffs, "N/A - sister project" only with a
reason. No grouping of unrelated targets, no blank cells, no "covered
elsewhere".

## Phase 7 — Cross-check

Verify: every direct target maps to ≥1 AG-QA check; every user-observable
target maps to ≥1 USER_QA check; Appendix A verbatim and counts; Appendix B
completeness; sister-project separation; prerequisites vs bundled deps;
static evidence not claiming live behavior; commands/paths/counts match the
repository; Markdown structure, anchors, and IDs valid. Add a
discoverability link from the docs index or README when one exists.

## Report

Return: both output paths; AG-QA and USER_QA check counts; preserved original
question count; traceability row count; the most important scope separation
or corrected legacy expectation; validation performed; any check blocked by a
missing source, platform, credential, or environment. Never claim the product
passed QA — this skill produces the specification only.
