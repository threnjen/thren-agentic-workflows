---
name: phase-final-check
description: "Shared contract for a cold-start review of a completed phase document. Use when Phase - Refiner or its final-check reviewer performs the optional last look."
---

# Phase Final-Check Contract

Keep this contract here; consumers reference it instead of copying it.

## Reading boundary

- The spawner supplies exactly the phase-document path and repository path.
- Read the supplied phase document and committed repository facts available to a newcomer. This
  may include `docs/phases/DISCOVERY_CONTEXT.md` and
  `docs/learnings/cross-phase-decisions.md` when present.
- If optional context is missing, proceed with the supplied phase document and available committed
  repository facts; do not fail or halt the review. Do not read or request conversation history,
  secrets, uncommitted session context, or external data.

## Cold-start obligation

The spawner must pass no conversation content, session summary, settled-area briefing, or
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
similar observations, omit weak or speculative ones, and do not assign severity ratings,
pass/fail judgments, grades, gates, blocking thresholds, or ranks. Roadmap or discovery-context
synchronization state is not a finding.

## Response

- Return at most five findings. If additional qualifying findings remain after consolidation, say
  plainly that findings were omitted because of the five-finding cap.
- If none qualifies, say plainly that no qualifying findings were found; do not pad the response.
- The response is the only output. Do not write a findings file, edit the phase document, or write
  any repository file.

This contract defines no reviewer-error handling, retry or second pass, repository synchronization,
approval or fold-in, branch, commit, or continuation behavior; consuming workflows own those
concerns.
