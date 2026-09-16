---
name: phase-final-check
description: "Shared contract for a cold-start review of a completed phase document. Use when Phase - Refiner or its final-check reviewer performs the optional last look."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->
# Phase Final-Check Contract

Keep this contract here. Consumers reference it instead of copying it.

## Reading boundary

- The spawner supplies exactly the phase-document path and the repository path.
- Read the supplied phase document and the committed repository facts available to a newcomer. This
  may include `docs/phases/DISCOVERY_CONTEXT.md` and
  `docs/learnings/cross-phase-decisions.md` when present.
- If optional context is missing, proceed with the supplied phase document and the committed
  repository facts available to a newcomer. Do not fail the review. Do not halt the review. Do not
  read or request conversation history,
  secrets, uncommitted session context, or external data.

## Cold-start obligation

The spawner must pass no conversation content, session summary, briefing about settled areas, or
assessment of what deserves attention. The reviewer starts from the two paths alone.

## Qualifying findings

Report only observations in these six categories:

1. contradiction
2. ambiguous scope boundary
3. uncheckable success criterion
4. undefined term
5. unaddressed dependency or risk
6. deliverable without a matching success criterion

Every finding must cite a phase-document location or a concrete repository fact. Consolidate
similar observations. Omit weak or speculative observations. Do not assign severity ratings,
pass/fail judgments, grades, gates, blocking thresholds, or ranks. The synchronization state for
the roadmap or discovery context is not a finding.

## Response

- Return at most five findings. If additional qualifying findings remain after consolidation, say
  plainly that you omitted findings because of the five-finding cap.
- If none qualifies, say plainly that no qualifying findings were found. Do not pad the response.
- The response is the only output. Do not write a findings file. Do not edit the phase document.
  Do not write any repository file.

This contract defines no reviewer-error handling, retry or second pass, repository synchronization,
approval or fold-in, branch, commit, or continuation behavior. Consuming workflows own those
concerns.
