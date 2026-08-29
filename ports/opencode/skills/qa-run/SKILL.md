---
name: qa-run
description: "Contract for executing a repository's automated QA runbook (`docs/QA_AUTOMATED.md`): read-only validation run over every runbook check plus every independently discovered test suite, strict binary PASS/FAIL status mapping, captured evidence, and one evidence-backed validation report ending in a single FINAL VALIDATION line. Use when: running or auditing an automated QA validation pass."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->

# QA Run

Execute the complete automated QA runbook and every test suite in the
repository; produce one evidence-backed validation report with a binary PASS
or FAIL for every check, every suite, and the run overall. Inputs: repository
root, runbook path (default `docs/QA_AUTOMATED.md`), evidence directory
(default a new untracked directory outside the source tree), and optional
approved non-production environment, credentials access method, and extra
test commands.

## Operating rules

- Read the entire runbook before executing; every numbered check and its
  expected result is authoritative.
- Read-only for tracked source, config, and documentation: never fix
  defects, update snapshots, regenerate committed artifacts, or weaken
  checks. Evidence goes only in the evidence directory. The one sanctioned
  write is recording results into the runbook when the caller directs it:
  the Run results section, plus rewriting the runbook's top `VERDICT:` line
  to `VERDICT: PASS` or `VERDICT: FAIL` to match.
- Never use production resources, guess endpoints or credentials, or print/
  save secrets; redact tokens, connection strings, keys, and personal data
  from all evidence.
- Source inspection never proves runtime behavior — UI, installer, update,
  background-process, and live-integration checks require direct observation
  in the required environment.
- Never silently skip a check; record why it could not run. Do not stop at
  the first failure — complete every remaining safe, independent check.
- No installing software, trusting certificates, changing machine policy, or
  mutating shared environments without explicit authorization: a missing
  prerequisite is BLOCKED, and a binary FAIL. No destructive test actions.
- Retry only for an identified transient infrastructure error; record every
  attempt.

## Status model

Native status per check: PASS (expected result directly observed, evidence
captured), FAIL, BLOCKED (named prerequisite), NOT RUN, N/A (proven out of
scope, with reason). Binary validation status: PASS only when native status
is PASS; everything else is FAIL — missing environments and omitted checks
can never produce a false green. If the runbook defines a different
final-acceptance rule, apply the stricter.

## Phases

1. **Establish the run** — record timestamps, repo path, branch, full SHA,
   git status (identify pre-existing changes; do not attribute them to this
   run), host OS/architecture, relevant toolchain versions, runbook path and
   hash, evidence directory. Parse the runbook into an inventory of every QA
   ID, command/action, expected result, environment requirement, and
   evidence requirement; confirm the count. Missing/unreadable runbook →
   report validation-setup FAIL and stop.
2. **Discover every test suite** — independently of the runbook: enumerate
   solution/workspace files, manifests, build files, CI workflows, and test
   scripts; identify suites by naming and configuration across all
   ecosystems present, including CI-invoked commands. List every suite
   (name, path, runner, exact command, prerequisites) before execution.
   Aggregate commands count only when inclusion of each discovered suite is
   proven — otherwise run the suite directly. Zero discovered suites is a
   validation FAIL unless the runbook proves the repo is intentionally
   test-free.
3. **Execute preparation and suites** — run the runbook's restore/build/
   analyzer/package/security steps in stated order with its exact
   configuration and warning policy; then every discovered suite with its
   documented command. Capture per suite: exact command, times, exit code,
   full test counts, result artifacts, concise failure detail, evidence
   path. A suite is PASS only when the runner exits successfully, ≥1
   expected test is discovered, all discovered tests execute, failed/
   skipped/ignored/inconclusive counts are zero (unless the runbook names an
   exception), and required artifacts were produced. A total test count that
   differs from a number written in the runbook is never a failure on its
   own — record the actual total and continue. Build success ≠ suite PASS. A platform the host
   cannot run is native BLOCKED, binary FAIL — never substitute inspection.
4. **Execute every QA check** — for each numbered check capture: QA ID,
   native and binary status, exact command/action, expected vs actual,
   exit code or direct observation, evidence path, failure/blocker reason,
   recommended next action and owner. Reuse saved evidence instead of
   rerunning identical commands only when it fully satisfies the check;
   static scans may support but never pass runtime checks. Walk the
   runbook's traceability matrix — an unmapped or unexecuted acceptance
   target is binary FAIL.
5. **Reconcile** — compare executed IDs and suites against both inventories
   (missing, duplicate, unproven aggregate coverage); confirm every command
   has an exit code or documented reason; downgrade any PASS without direct
   evidence to FAIL; confirm no secrets in evidence; re-run
   `git status --short` — any unexpected tracked mutation is a validation
   FAIL. Compute totals by native status, binary totals, test-case totals,
   and traceability totals. Overall validation is PASS only if every QA
   check, every discovered suite, and every traceability target is binary
   PASS.

## Report

Print in Markdown — full tables, never a prose substitute, never omitting
failed or blocked items:

- **Overall result** table (validation result, repo, branch/commit, runbook
  path+hash, host, timestamps, evidence directory, working-tree state) plus
  the decisive reason in one sentence.
- **Totals** table (QA checks / test suites / traceability targets ×
  PASS / FAIL / BLOCKED / NOT RUN / N/A) plus total test cases discovered/
  passed/failed/skipped/inconclusive.
- **Test suite results**, **Automated QA results**, **Acceptance
  traceability**, and **Failures and blockers** tables (write `None` in
  failures only when overall is PASS).
- **Commands executed** in order with exit codes and redacted log paths.
- **Validation integrity**: inventory-vs-executed counts, duplicates,
  evidence completeness, tracked-file changes, secret-leak check,
  limitations.

End with exactly one line: `FINAL VALIDATION: PASS` or
`FINAL VALIDATION: FAIL`.
