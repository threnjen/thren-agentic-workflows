# Review Learnings

## 2026-04-14: Redundant intro lines after consolidation

- **Pattern:** When consolidating a bulleted list into a single sentence, the original section's intro line often becomes redundant with the new consolidated sentence. Both the intro and the sentence start with the same directive (e.g., "Exclude these…" followed by "Exclude anything…").
- **Impact:** Adds unnecessary tokens and reads awkwardly — directly contradicts the goal of token reduction.
- **Watch for:** Any time a list is being condensed into a sentence, check whether the section's intro line is now subsumed by the consolidated text.

## 2026-04-14: ARCHITECTURE.md not updated when adding instruction/skill files

- **Pattern:** When creating new `.github/instructions/` or `.github/skills/` files, the implementation updated `docs/CODEBASE_CONTEXT.md` (file count, folder structure) but missed updating the instructions table and mermaid diagram in `docs/ARCHITECTURE.md`.
- **Impact:** Documentation falls out of sync — ARCHITECTURE.md becomes inaccurate for downstream agents and human readers relying on it for the instruction→agent mapping.
- **Watch for:** Any implementation that adds or removes instruction or skill files. Verify both `CODEBASE_CONTEXT.md` AND `ARCHITECTURE.md` are updated (mermaid diagram nodes + summary tables).

## 2026-04-22: Comparability rules without capture fields

- **Pattern:** Specs require baseline/variant comparability across runtime settings, but the capture schema omits the runtime-setting fields needed to verify equivalence.
- **Impact:** Comparability checks become subjective and can incorrectly approve non-equivalent runs.
- **Watch for:** Whenever a spec says settings must match, confirm the evidence contract includes explicit fields (for example model ID, sampling settings, and tool-policy version).

## 2026-04-22: KaTeX command regressions in equations

- **Pattern:** Formula edits can silently drop leading backslashes in LaTeX commands (for example `\text`), causing malformed rendered equations.
- **Impact:** Mathematical criteria become harder to interpret and easier to misapply during reviews.
- **Watch for:** Re-open changed equation blocks and verify command names render correctly; prefer commands less prone to escape ambiguity when possible.

## 2026-04-22: Inventory count drift in README during doc-only compaction

- **Pattern:** Compaction edits to `README.md` preserved old agent-count and role-breakdown numbers while adjacent docs already reflected updated counts.
- **Impact:** Repository overview becomes self-contradictory and can mislead maintainers during onboarding/review.
- **Watch for:** Any PR touching structural docs (`README.md`, `docs/CODEBASE_CONTEXT.md`, `docs/ARCHITECTURE.md`) should include a count-sync check against `.github/agents/*.agent.md` and role split.

## 2026-04-22: Grouped change map misses remediated categories

- **Pattern:** Phase/feature change maps were updated for initial compaction categories but not refreshed after remediation touched additional categories (for example agents and instructions).
- **Impact:** AC traceability appears complete in narrative, but the grouped map under-reports actual scope and weakens one-PR review usability.
- **Watch for:** After remediation edits, re-derive grouped summaries directly from implementation file lists so every changed category is represented.

## 2026-04-22: ARCHITECTURE agent-inventory count drift

- **Pattern:** Documentation-focused updates touched instruction mappings but left adjacent architecture inventory counts stale (for example orchestrator/subagent totals and overall agent count in diagrams/narrative).
- **Impact:** Cross-document contradictions reduce trust in planning/review artifacts and can mislead downstream agents relying on architecture facts.
- **Watch for:** Any edit to `.github/agents/` or architecture/inventory docs should trigger a parity check across `README.md`, `docs/CODEBASE_CONTEXT.md`, and `docs/ARCHITECTURE.md` counts.

## 2026-04-22: Candidate artifact metadata drift across benchmark outputs

- **Pattern:** Generated benchmark JSON for a candidate can carry forward `run_id` and `candidate_variant` values from a different candidate when copied or rerun from example configs.
- **Impact:** AC traceability and gating can be assessed against mislabeled evidence, producing incorrect review conclusions.
- **Watch for:** For each candidate report file, verify filename, `run_id`, and `candidate_variant` align before using the artifact in validation narratives.
