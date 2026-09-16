---
name: qa-run
description: "Contract for executing a repository's automated QA runbook (`docs/QA_AUTOMATED.md`): read-only validation run over every runbook check plus every independently discovered test suite, strict binary PASS/FAIL status mapping, captured evidence, and one evidence-backed validation report ending in a single FINAL VALIDATION line. Use when: running or auditing an automated QA validation pass."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->
# QA Run

Execute the complete automated QA runbook and every test suite in the
repository. Produce one evidence-backed validation report. The report must
assign binary PASS or FAIL status to every check, every suite, and the overall
run. Inputs include the repository root, runbook path (default
`docs/QA_AUTOMATED.md`), evidence directory (default a new untracked
directory outside the source tree), and optional approved non-production
environment, credentials access method, and extra test commands.

## Operating rules

- Read the entire runbook before execution. Treat every numbered check and its
  expected result as authoritative.
- Keep tracked source, config, and documentation read-only. Never fix defects,
  update snapshots, regenerate committed artifacts, or weaken checks. Write
  evidence only to the evidence directory. The only sanctioned write is to
  record results in the runbook when the caller directs it. Write those results
  in the Run results section. Rewrite the runbook's top `VERDICT:` line to
  `VERDICT: PASS` or `VERDICT: FAIL` to match.
- Never use production resources. Never guess endpoints or credentials. Never
  print or save secrets. Redact tokens, connection strings, keys, and personal
  data from all evidence.
- Source inspection never proves runtime behavior. UI, installer, update,
  background-process, and live-integration checks require direct observation
  in the required environment.
- Never silently skip a check. Record why it could not run. Do not stop at the
  first failure. Complete every remaining safe, independent check.
- Do not install software, trust certificates, change machine policy, or
  mutate shared environments without explicit authorization. A missing
  prerequisite is BLOCKED and a binary FAIL. Do not perform destructive test
  actions.
- Retry only for an identified transient infrastructure error. Record every
  attempt.

## Status model

Assign each check a native status: PASS (you directly observe the expected
result and capture evidence), FAIL, BLOCKED (named prerequisite), NOT RUN, or
N/A (you prove the check is out of scope and give a reason). Assign binary
validation status PASS only when native status is PASS. Assign FAIL in every
other case. Missing
environments and omitted checks can never produce a passing validation. If the
runbook defines a different final-acceptance rule, apply the stricter rule.

## Phases

1. **Establish the run.** Record timestamps, repo path, branch, full SHA, git
   status, host OS/architecture, relevant toolchain versions, runbook path and
   hash, and evidence directory. Identify pre-existing changes in git status.
   Do not attribute pre-existing changes to this run. Parse the runbook into an
   inventory of every QA ID, command/action, expected result, environment
   requirement, and evidence requirement. Confirm the count. If the runbook is
   missing or unreadable, report validation-setup FAIL and stop.
2. **Discover every test suite.** Work independently of the runbook. Enumerate
   solution/workspace files, manifests, build files, CI workflows, and test
   scripts. Identify suites by naming and configuration across all present
   ecosystems, including CI-invoked commands. List every suite by name, path,
   runner, exact command, and prerequisites before execution. Count one command
   for multiple suites only when you prove inclusion of each discovered suite.
   Otherwise, run the suite directly. If you discover zero suites, report
   validation FAIL unless the runbook proves the repo is intentionally test-free.
3. **Execute preparation and suites.** Run the runbook's
   restore/build/analyzer/package/security steps in stated order. Use its exact
   configuration and warning policy. Then run every discovered suite with its
   documented command. Capture the exact command, times, exit code, full test
   counts, result artifacts, concise failure detail, and evidence path for each
   suite. A suite is PASS only when the runner exits successfully and discovers
   ≥1 expected test. All discovered tests must execute. Failed/skipped/ignored/
   inconclusive counts must be zero unless the runbook names an exception. The
   run must produce required artifacts. A total test count that differs from a
   number written in the runbook is never a failure on its own. Record the
   actual total and continue. Build success does not equal suite PASS. A
   platform the host cannot run is native BLOCKED and binary FAIL. Never
   substitute inspection.
4. **Execute every QA check.** Capture the following for each numbered check:
   QA ID, native and binary status, exact command/action, expected vs actual.
   Also capture exit code or direct observation, evidence path, failure/blocker
   reason, recommended next action, and owner. Reuse saved evidence instead of
   rerunning identical commands only when it fully satisfies the check. Static
   scans may support runtime checks but can never pass them. Walk the runbook's
   traceability matrix, which maps acceptance targets to checks. An unmapped or
   unexecuted acceptance target is binary FAIL.
5. **Reconcile.** Compare executed IDs and suites against both inventories.
   Record missing, duplicate, and unproven aggregate coverage. Confirm that
   every command has an exit code or documented reason. Downgrade any PASS
   without direct evidence to FAIL. Confirm that evidence contains no secrets.
   Re-run `git status --short`. Any unexpected tracked mutation is a validation
   FAIL. Compute totals by native status, binary totals, test-case totals, and
   traceability totals. Overall validation is PASS only if every QA check,
   every discovered suite, and every traceability target is binary PASS.

## Report

Print the report in Markdown. Use full tables instead of prose. Do not omit
failed or blocked items:

- Include an **Overall result** table. Add validation result, repo,
  branch/commit, runbook path+hash, host, timestamps, evidence directory, and
  working-tree state. Add the decisive reason in one sentence.
- Include a **Totals** table. Report QA checks, test suites, and traceability
  targets by PASS, FAIL, BLOCKED, NOT RUN, and N/A. Report total test cases
  discovered, passed, failed, skipped, and inconclusive.
- Include **Test suite results**, **Automated QA results**, **Acceptance
  traceability**, and **Failures and blockers** tables. Write `None` in
  failures only when overall is PASS.
- Include **Commands executed** in order with exit codes and redacted log
  paths.
- Include **Validation integrity**. Report inventory-vs-executed counts,
  duplicates, evidence completeness, tracked-file changes, secret-leak check,
  and limitations.

End with exactly one line: `FINAL VALIDATION: PASS` or
`FINAL VALIDATION: FAIL`.
