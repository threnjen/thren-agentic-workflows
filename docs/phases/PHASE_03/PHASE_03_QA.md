# Phase 03 QA

## TL;DR

Run the focused guard test first. Then run the grouped regression command and
the full suite. The focused test must pass. The grouped and full suites may
retain the recorded repository baseline failures; record exact counts and
failure identities. Finish the manual runtime checklist before calling the
phase fully verified.

## Automated checks

1. Run the focused Phase 03 guards:

   `uv run pytest tests/test_phase_execute_audit_bookend.py --junitxml=dev/feature/11-audit-bookend-guards/focused.xml`

   Expected result: 13 tests pass, with zero failures or errors.

2. Run the manifest regression set:

   `uv run pytest tests/test_agent_corpus_invariants.py tests/test_unity_consumer_contract.py tests/test_propagate_master_assets.py tests/test_pr_review_orchestrator.py --junitxml=dev/feature/11-audit-bookend-guards/regression.xml`

   Record the five known baseline failures/subfailures if they remain. They
   cover generated-output counts, an unresolved instruction target, and the
   existing PR-review prose collision.

3. Run the complete suite:

   `uv run pytest tests/ --junitxml=dev/feature/11-audit-bookend-guards/wave-3.xml`

   Compare failure identities with the 2026-08-11 baseline. Any new identity
   is a Phase 03 regression until explained.

## Manual acceptance checklist

- [ ] Start Phase Execute with the Phase 03 manifest and confirm the manifest
  is the only schedule used.
- [ ] Confirm Step 1 reports the resolved source-file count and asks once for
  scoped, explicit full-codebase, or declined bookend execution.
- [ ] Confirm duplicate, outside-repository, or unusable key-file paths are
  reported as a scope limitation after normal manifest and bundle hard-stops.
- [ ] Run a live baseline/current comparison and capture both prompt bodies.
  Confirm only target root, snapshot label, and output directory differ.
- [ ] Confirm Code and optional Infra reports, deltas, queues, and attribution
  results are independent and live under the current checkout.
- [ ] During attribution, confirm the created baseline worktree remains
  available; confirm cleanup happens only after the final attribution return.
- [ ] Confirm a missing report total, materialization failure, or attribution
  mismatch sets `all-approved: no` and still reaches Step 6.
- [ ] If a phase-attributed High/Critical finding exists, confirm remediation
  is one bounded current-side retry and its verification is a non-comparable
  addendum. Confirm Medium/Low and pre-existing findings are not remediated.
- [ ] Confirm the final review receives the complete bookend evidence and uses
  standard mode whenever any gate is not green.

## Evidence boundary

Static tests cannot prove prompt byte identity, real worktree lifetime, or
end-to-end Audit - Delta behavior. Those claims require the manual checks above.
