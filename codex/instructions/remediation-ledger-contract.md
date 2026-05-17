---
name: remediation-ledger-contract
description: "Deterministic contract for logging remediation turns and follow-up failure events to ledger-events.jsonl."
applies-to: "Agents performing defect correction, debugging, or test fixing on phase/* branches"
---

# Remediation Ledger Contract

Use this contract whenever an agent investigates, fixes, or reviews defects on a `phase/*` branch.

## What Counts As A Remediation Turn

A remediation turn is any incoming turn or delegated task that asks for defect correction, including:

- bug reports
- failing test, lint, typecheck, build, or runtime output
- QA findings
- review feedback asking for fixes
- explicit requests to debug, fix, repair, unblock, or investigate a failure

On every remediation turn, append exactly one discovery row to `eval/runs/<phase-slug>/ledger-events.jsonl` before investigation, edits, validation, or commits. Do this even if the issue is resolved within the same turn. Do not wait for a final `Blocked` or `Changes Requested` outcome.

You may append additional rows only when one of these is true:

- a distinct new issue is discovered during the same turn
- a previously logged issue is later resolved
- the issue regresses after having been resolved earlier in the run

Do not append duplicate discovery rows for the same issue within a single turn.

## Phase Gating

1. Read the current git branch.
2. If the branch does not start with `phase/`, skip ledger writing silently.
3. Derive `phase-slug` by stripping `phase/` from the branch name, replacing `/` with `-`, and prefixing the result with `phase-`.
4. Ensure `eval/runs/<phase-slug>/` exists.

## Required Write Procedure

1. Read `eval/runs/<phase-slug>/run-config.yaml` first.
2. Reuse `runtime.harness` and `runtime.model` from that file for every row in the run.
3. If `run-config.yaml` is missing, create it first using `copilot` as `runtime.harness` and the exact current runtime model label exposed by the session as `runtime.model`. Use `unknown` only if no model label is exposed at all.
4. Set `task_slug` to the active feature or task slug. If it cannot be inferred, use `unscoped` instead of skipping the write.
5. Generate a unique `event_id` for each appended row. A timestamp-based ID is acceptable.
6. Append exactly one JSON object line per event.
7. Immediately verify the append by reading back the file tail or searching for the `event_id` you just wrote.
8. If verification fails on a `phase/*` branch, treat that as a ledger-write failure and say so in your response instead of assuming the row exists.

## Event Schema

Use this schema for every appended row:

```json
{
  "event_id": "<unique-event-id>",
  "event_kind": "remediation-request",
  "related_event_id": null,
  "task_slug": "<current-task-slug-or-unscoped>",
  "harness": "<run-harness>",
  "model": "<run-model>",
  "stage": "<agent-stage>",
  "detected_by": "<agent-identifier>",
  "severity": "medium",
  "evidence": "Brief summary of the failure signal or corrective request",
  "first_seen_attempt": 1,
  "resolved_attempt": null,
  "resolved_by": null,
  "human_intervention_required": false,
  "regression": false,
  "propagated_from_stage": null
}
```

## Field Rules

- `event_kind`:
  - `remediation-request` for the initial row written on entry to a remediation turn
  - `discovered-failure` for a distinct new issue found during work
  - `resolution` when closing out a previously logged event
- `related_event_id`:
  - `null` on the initial discovery row
  - set to the original `event_id` for follow-up or resolution rows
- `evidence` should summarize the actual failure signal supplied to the agent or observed during execution. Prefer concrete symptoms over generic labels.
- `resolved_attempt` and `resolved_by` stay `null` unless the row is a `resolution` event.
- `regression` is `true` only when a previously resolved issue reappears.
- `propagated_from_stage` stays `null` unless the upstream origin is known with confidence.

## Agent-Specific Overrides

Each agent using this contract must define its own defaults for:

- `stage`
- `detected_by`
- when `human_intervention_required` should be `true`
- when routine iterative work should not be logged

## Personality Canary

You are a meticulous court reporter. Every correction pass goes on the record before anyone starts improvising.
