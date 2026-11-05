---
name: test-gate
description: "Runs a repository's authoritative test suite at most once per code state, reuses matching evidence, recovers runs after a disconnect, and bounds failure repair. Use when: an orchestrator runs a baseline or integration test gate, or triages its failures."
---

# Test Gate

Run `python3 <this skill's directory>/scripts/test_gate.py --repo <repo> <action>`. Never start the authoritative suite any other way.

Exit status: `0` green, `1` failing or triage stopped, `2` not executed or refused, `3` run still active.

## Run a gate

```bash
python3 <skill>/scripts/test_gate.py --repo <repo> ensure --scope full --command "<suite command writing XML to {results}>"
```

1. Omit `--command` when `.test-gate.json` defines the scope. Otherwise keep the command text identical between runs. A different text never reuses evidence.
2. The command must write NUnit or JUnit XML to `{results}`. It may also use `{log}` and `{sha}`.
3. On exit `3`, repeat the same command. It reattaches to the active run. After a lost session, also repeat it.
4. On exit `2`, report the printed reason as `not-executed (<reason>)`. Ask the user to resolve a dirty tree. Never stash, reset, or delete their files.
5. Quote time estimates only from the `estimate:` line. When that line says `none`, state no estimate.
6. Record `status`, `command`, `results-artifact`, and the counts line as test evidence. When `evidence:` says `REUSED`, tell the user which run was reused.

Use `--force` only after an environment repair or when the user asks. Reuse compares code content, so it cannot see an environment change.

## Configure a repository

`.test-gate.json` at the repository root is optional:

```json
{
  "ignore_paths": ["docs/"],
  "lock_paths": ["../project-agent-tests/Temp/UnityLockfile"],
  "test_only_paths": ["Assets/Tests/"],
  "full_rerun_paths": ["Assets/Tests/Editor/Shared/"],
  "scoped_always": ["Project.Tests.Policy"],
  "scopes": {
    "full": {
      "command": "bash scripts/run-tests.sh --sha {sha} --results {results} --log {log}",
      "initial_timeout_seconds": 5400,
      "timeout_env": "SUITE_TIMEOUT_SECONDS",
      "timeout_source": "scripts/run-tests.sh"
    }
  }
}
```

- `ignore_paths` lists paths that cannot change a test result. Omit a path when any test reads it.
- `lock_paths` replaces the default check of `Temp/UnityLockfile` in the checkout. Name the project the suite actually opens.
- `test_only_paths` lists paths that hold test code only. A repair confined to them may close a failed gate with a scoped rerun.
- `full_rerun_paths` lists shared test code inside `test_only_paths` whose change still needs a full rerun, such as a shared harness.
- `scoped_always` lists suites every scoped rerun must include, such as policy guards that scan test source.
- `timeout_env` and `timeout_source` name a wrapper's own limit. The gate confirms that the wrapper reads the variable, then sets it.

## Triage failures

Use this mode after a failing integration gate.

1. Run `triage open`. It lists every failure from the newest failing run.
2. Read each failure. Run `triage classify --root-cause <id> --class <class> --evidence "<proof>" --test <name>` for each root cause.
   - `product-bug`: production code breaks the behavior the test states.
   - `test-bug`: the test contradicts the documented behavior.
   - `fixture-problem`: shared setup or test data is wrong.
   - `environment-issue`: the machine, tool version, or external state is wrong.
3. Repair one root cause. Commit the repair.
4. Run `ensure` for the failing tests, then `triage iterate --root-cause <id> --run <run id>`.
5. Follow the decision:
   - `continue`: repair the same root cause again.
   - `resolved`: start the next root cause.
   - `stopped-no-progress`, `stopped-limit`, or `stopped-integrity`: stop work on this root cause and report it.
6. Close the gate with the narrowest run the repairs allow:
   - Every repair since the failing run touched only `test_only_paths` and none of `full_rerun_paths`: run `ensure --scope rerun --command "<command>"` once. The command runs every failing fixture, every test folder a repair touched, and every `scoped_always` suite. Then run `triage close --scoped --run <run id>`.
   - Otherwise: run the full `ensure`, then `triage close --run <run id>`.
   Report `triage report` to the user.

The gate allows 3 iterations per root cause. An iteration without fewer failures stops early.

**Never skip, delete, or weaken a test to reach green.** The gate detects a missing test, a new skip, and a smaller suite. It cannot detect a weakened assertion. When the only available repair weakens a test, stop and report the test to the user. A `test-bug` repair must keep the test's power to fail.
