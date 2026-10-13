---
name: engagement-client-voice
description: "House style for every client-facing engagement deliverable — plain, direct, evidence-tied language with no corporate buzzwords, shared by all engagement agents that write under `deliverables/`. Use when: writing or revising any client-facing engagement document."
---

# Engagement Client Voice

Every document under `deliverables/` uses this voice. Every stage that writes
a document loads this skill. The rule covers all of that stage's client-facing
output without requiring the stage to restate this rule. This skill applies on
top of each agent's own content contract. When the skill and contract conflict,
the content contract wins on *what* to say, and this skill wins on *how* to say
it. Internal documents under `internal/`, `pairs/`, and `notes/` are exempt.

## Voice

- **Plain and direct.** Use short declarative sentences. Say the thing once,
  concretely, and move on. Detailed writing is good. Wordy writing is not.
  Cut any sentence that adds no new fact.
- **Non-technical by default.** Write for a business reader. Use each
  unavoidable technical term precisely. Name one term per mechanism and use
  it in every document. Explain it in plain words at its
  first use in table-of-contents reading order. Never explain it again, in
  that document or a later one.
- **No buzzwords, no marketing.** Ban these words outright: leverage, robust,
  seamless, cutting-edge, state-of-the-art, best-in-class, world-class,
  synergy, holistic, empower, unlock, journey, streamline, utilize,
  game-changing, next-generation, enterprise-grade, turnkey, mission-critical.
  Also ban related words. If a word sells rather than describes,
  replace it with what actually happened ("utilize" → "use"; "leverages a robust framework" →
  "uses <framework>, which handles <the specific thing>").
- **No hedging filler.** Drop "it should be noted", "it is important to",
  "essentially", "basically", "in order to". State facts. State genuine
  uncertainty as an explicit assumption, not a softened verb.
- **Active voice, named actors.** "We replaced X with Y", "the system now
  does Z" — not "X was replaced" with no one doing it. "We" describes
  contracted work performed. A finding's disposition credits the evidence:
  "the retained comparison records X as repaired", never "we fixed X".
- **No internal process vocabulary.** Never write evidence-class or
  scope-class tokens (`qa-backed`, `comparison-only`, `sow-authorized`,
  UNVERIFIED), native/binary status, attestation IDs, or internal record IDs
  (`INFRA-014`, `ENG-E01`). Never write an internal label such as "Owner
  disposition:". Render a disposition in plain words. Write "recorded PASS" or
  "QA confirms". Keep only
  IDs the client can look up: QA check IDs, and security finding IDs inside the
  security appendix.
- **No repeated formula.** Never open or close successive entries with the
  same phrase. State a shared fact once, in the section's lead sentence
  ("Every finding below is supported by comparison"). Never state an absence
  per entry ("Remaining exposure: none").
- **One level of detail: what the reader can act on or check.** Name the
  outcome. Omit the mechanism, the configuration value, and the checklist step
  unless the reader needs it to check the claim.
- **No intensifiers.** Drop "literally", "materially", "fully", and similar
  adverbs that add emphasis without adding a fact.
- **No editorial meta-sentences.** Never write about what a document does or
  does not conclude ("This appendix applies the same boundary…", "It is not a
  failure to preserve behavior"). Never echo a value-story mode name or
  describe the document ("each change below is…"). Open with the first fact.
- **Past tense for completed work and completed QA.** Present tense describes
  how the upgraded system behaves now.

## Claims

- Trace every factual claim to evidence. Use superlatives and value judgments
  ("dramatically improved", "significantly faster") only when a cited
  measurement backs the adverb. Otherwise, state the change and let it speak.
- Numbers carry units, sources, and dates. Describe a number that has none of
  these qualitatively instead.
- **Derive every count from what it counts.** A count in prose equals the
  number of items in the list or table it summarizes. A table total equals the
  sum of its rows. Recount after any edit to the list or table.
- Never overstate certainty. State verified facts as facts. Label assumptions
  as assumptions.
- **Evidence phrases.** Name evidence strength with exactly these phrases:
  "checked directly" (a QA check recorded the result), "supported by
  comparison" (documents, code graphs, or retained comparisons support it
  without a direct check), "confirmed by <role>" (the engagement owner or
  the client confirmed it, for example "confirmed by the engagement owner"),
  and "not verified" (no evidence supports it).
- **State each verification gap once.** A gap is something not checked
  directly. A gap that affects an SOW acceptance criterion is stated only in
  that criterion's row in the SOW compliance walkthrough. The specification's
  `Known issues and recommended follow-up` subsection links that row and gives
  only the recommendation. Every other gap is
  stated only in the intended-behavior specification's `Verification evidence
  and warranty scope` section. A QA observation is not a restated gap. A
  tester note or recorded limitation belongs on its check's row in the QA
  appendix. Never restate a gap in narratives,
  the QA appendix, or the security appendix. The security appendix may keep
  one review-method sentence on what the review did not do. Never itemize blank record-keeping
  fields (tester, date, platform version, signature). Never write
  negative-space sentences ("which is not a claim that…", "no direct
  observation is retained"). Never drop a warranty exclusion.

## Recommendations to the Client

- **Name a recommendation only where it exists.** Never promise a
  recommendation that the owning document does not state.
- **Accepted risk is not closed.** Describe a finding the owner accepted as
  "accepted as an existing risk". Never call it "closed" or count it as
  resolved. Label every severity as original or current.
- **Recommend. Do not assign.** Write "we recommend rotating or revoking it".
  Never write an owner/target-date grid or "the client must … before handoff".
- Describe an out-of-scope fix as "new work outside this engagement", not as
  something that "requires client authorization".
- When a recommendation depends on how we came to hold a client asset, such
  as a credential, name it plainly ("shared with us").

## Presentation

- Lead every document and major section with what it means for the client.
  Follow with supporting technical detail or place it in an appendix that
  cites sources by path.
- Use consistent names throughout the package. Call the two sides "the original system" and "the
  upgraded system". Give each component one name
  across all documents. Never alternate synonyms for variety.
- Use sentence-case headings that say what the section contains. Do not use
  clever titles. Do not use exclamation marks.
- Cite a contract item by the SOW's own label ("amendment A2",
  "clarification B2"). Spell out a section reference ("SOW Section 3.3", not
  "§3.3").
- **Cross-references are markdown links** whose text is the target document's
  table-of-contents title (`[Appendix — QA report](qa-appendix.md)`). Never use
  a path or filename as link text. Never point "above" or "below" at content
  that does not exist in the same document.
- Prefer short labelled bullet lists for change summaries ("Material changes",
  "Dropped", "Added"). Use prose where a reader needs the sequence or the
  reason.

## Proportion — report a finding once

The `engagement-package-manifest` skill's Claim Ownership section names the
one owner document for each claim type. Every other document links to the
owner.

State each finding **once**. Put it in the one section that owns it. Give it
the weight its severity earns. Repeat a finding only where the document's own
contract requires the entry. Examples include a QA appendix, a compliance
criterion, or a manifest row. State it plainly there. Do not re-argue it.
Never carry a finding into the executive summary, an unrelated section, or
another document's narrative for emphasis.

Report every finding truthfully and completely. Never soften or omit one.
Never inflate one. Give a low or trivial finding a low or trivial amount of the
package's attention. Describe a closed finding as closed rather than
relitigating it.
