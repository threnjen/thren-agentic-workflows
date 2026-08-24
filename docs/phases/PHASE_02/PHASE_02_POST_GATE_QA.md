# Phase 02 Post-Gate QA

## TL;DR

This checklist confirms behavior that source files and generated output cannot prove.
Open the deploy gate after the phase lands.
Record the harness version with every result.
Record `PASS`, `FAIL`, or `UNVERIFIED` plus the observed evidence and the observation.

## Checklist

1. Confirm each deploy destination with `python3 deploy_agents.py --list`.
   Record the resolved destination and the `deploy_agents.py` version or commit.

2. Deploy each harness with `python3 deploy_agents.py --all`.
   Record the harness versions and confirm every Phase 02 agent is available at its expected destination.

3. Run the Phase - Execute preflight on Claude Code.
   Record the Claude Code version and confirm the displayed `low`, `medium`, and `high` rows show the requested model, any run-only override, the observed route, and the correct `resolution_status`.

4. Run the Phase - Execute preflight on Codex.
   Record the Codex version and confirm the displayed route matches the app-server model and effort evidence, or remains `unverified` when the child response does not expose a model.

5. Run the Phase - Execute preflight on OpenCode.
   Record the OpenCode version and confirm the child output identifies the configured provider and model, or remains `unverified` when no stable child result exists.

6. Run the Phase - Execute preflight on Cursor.
   Record the Cursor version and confirm the child model shown in the session matches the selected route, or remains `unverified` when Auto or session routing hides the exact model.

7. Run the Phase - Execute preflight on GitHub Copilot CLI.
   Record the Copilot CLI version and confirm the CLI output or `gen_ai.response.model` telemetry identifies the child model. Record `unverified` for cloud surfaces without equivalent runtime evidence.

8. Repeat preflight with one override for each tier.
   Record the harness version and confirm each override changes only the current run while `source_of_truth/config/model-routing.json` remains byte-identical.

9. Run one Markdown-only feature through the committee loop.
   Record the harness version and confirm the trigger table selects the expected lanes, four committee reports return, the consolidator writes one fix list, and the implementer receives that list.

10. Verify held-open implementer behavior on each harness that supports resumable child handles.
    Record the harness version and confirm the original implementer handles a fix round. Record the fallback path when the harness requires a fresh implementer.

11. Confirm the GitHub baseline splice.
    First confirm the repository destination. Then remove `.github/copilot-instructions.md` with `git rm .github/copilot-instructions.md`, run `python3 deploy_agents.py --harness github`, and confirm the file returns with all baseline sections. Run the same deploy command again and confirm the result reports `unchanged`. Restore the file with `git checkout -- .github/copilot-instructions.md` if the check must be rolled back.

## Why source evidence is insufficient

The source and generated trees prove names, routes, fields, and render shape. They cannot prove a harness accepted the route, reported the child model, resumed a child handle, installed the generated assets at the intended destination, or recreated the GitHub baseline splice.

## Result record

| Check | Harness and version | Result | Observation or artifact |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |
| 6 |  |  |  |
| 7 |  |  |  |
| 8 |  |  |  |
| 9 |  |  |  |
| 10 |  |  |  |
| 11 |  |  |  |
