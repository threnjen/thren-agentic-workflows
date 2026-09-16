---
name: engagement-evidence-standard
description: "The single classification vocabulary every engagement stage uses when judging what the evidence supports about a workflow, behavior, or SOW criterion — the evidence classes (qa-backed / comparison-only / unverified), the scope classes (sow-authorized / unresolved), and what each requires. Use when: classifying QA or comparison evidence, deciding whether a change is an authorized scoped delta, or consuming another stage's classifications."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->
# Engagement Evidence Standard

Every engagement stage that judges evidence uses these class names verbatim.
No stage invents its own vocabulary. A consumer may rely on receiving exactly
these values.

## The evidence base — what is judged

Use **docs vs. docs, never git-diff** for comparisons. Use the retained workspace
reports as the evidence base. For each side, also use the docs-writer set, the
code graph, and the QA package. The QA package includes `QA_AUTOMATED` with run
results and the manual QA checklist. Use `QA_USER` by default for the manual QA
checklist. Use the engagement's configured manual QA document(s) when the
engagement specifies them.

Find docs sets, code graphs, and QA packages at the passed analysis-branch
checkout paths **inside the client repositories**. Examples include
`docs/CODEBASE_CONTEXT.md`, `docs/QA_AUTOMATED.md`, and the manual QA checklist
on the side's analysis branch. The workspace holds only retained reports. It is
not the whole evidence universe. Never infer absence from the workspace alone.
Declare a source absent only after checking its passed pointer path. Name the
checked path in the absence note.

## Evidence classes — what the evidence supports

| Class | Requires |
|---|---|
| `qa-backed` | a completed PASS on an **exact matching** QA check on the upgraded side. The check must be either a `QA_AUTOMATED` check ID with a run result, or a checked (`- [x]`) expected result in the manual QA checklist |
| `attested` | an accepted statement from the engagement owner closing a specific finding. The statement must show that the finding was remediated or researched and dispositioned (rules below) |
| `comparison-only` | before/after comparison evidence (docs sets, graphs, retained reports) with no matching QA check |
| `unverified` | neither |

- The QA record shows the upgraded behavior at the recorded QA standard. The
  `qa-backed` class does not, by itself, prove that the original side behaved
  identically.
- A generic repository-level PASS with no matching check never yields
  `qa-backed`. Record that claim as `unverified`.
- Use only `comparison-only` or a stronger class for a "preserved from the
  original" statement.
- Render `unverified` as **NOT VERIFIED** in client-facing compliance documents.
- When the original side has no QA package, runtime evidence is asymmetric.
  State the asymmetry. Never use it to claim that the upgraded behavior was
  untested. Never use it as proof of before/after equivalence.
- "No identifiable delta" means that comparison evidence established no
  behavioral delta. It never means that the codebase has no changes. It never
  means that QA was absent.

## `attested` — owner-stated closure

An explicit statement from the engagement owner closes the identified finding
**without** rerunning audits, scans, or QA. Two forms qualify.

**Remediation.** The statement must identify the finding. It must state the
corrected behavior. It must confirm the outcome. "The security items are fixed"
is insufficient. It identifies no finding and states no behavior. "SEC-05 has
been remediated. JWT audience validation is now enforced." qualifies.

**Researched disposition.** The owner researches the finding and reaches a
conclusion about it. The conclusion can be invalid, already-correct behavior,
immaterial, or real but accepted at a stated severity. The statement must
identify the finding. It must give the conclusion and the basis in one line. "I
researched INFRA-014; the path is unreachable in the deployed configuration,
so it is trivial" qualifies. A bare severity opinion with no basis does not
qualify. The owner's own research is sufficient basis. Never demand an
independent re-derivation of that research.

**Settled means settled.** An accepted attestation of either form ends the
matter. No stage may re-argue it. No stage may re-raise it as an open finding.
No stage may ask for further evidence. No stage may re-surface it to the user
for reconsideration. Only two events can reopen it. Retained evidence that
directly contradicts it can reopen it (see Conflict below). The user can also
reopen it.

**How it is recorded.** Record the closure as `remediated (attested)` or
`dispositioned (attested)`. Never record it as `qa-backed`. The
`engagement-workspace` working-state file retains the finding ID, the statement,
its form, its date, the repository, and the attestor.

**What it closes, and only that.** Remove the attested finding from the
introduced, residual-remediation, and open-work counts. It verifies no
unrelated behavior. It provides no repository-wide assurance. Client documents
may describe the finding as remediated. They may instead use the severity that
the owner's research established. Each methodology note must distinguish an
owner attestation from independently executed QA.

**Finalization.** `attested` satisfies the finalization gate for its own
finding. Never require refreshed audits solely to confirm an accepted
attestation. After accepting the attestation, re-run synthesis only. Synthesis
includes findings, security, narratives, compliance, manifest, and gap review.
Never rerun the source audits unless the user explicitly asks.

**Conflict.** Classify retained evidence that directly contradicts an
attestation as `conflicted-attestation`. Pause finalization for that finding.
Request resolution. Never silently prefer either source.

## Scope classes — how an observed change is treated

Read the SOW's explicit exceptions and scope boundaries before classifying
any delta.

| Class | Requires | Consequence |
|---|---|---|
| `sow-authorized` | expressly required or permitted by the SOW. Cite the clause or explicit scope exception | Treat the change as an approved scoped delta under any pair `mode`. Narrate the change as such. Never call it a framing discrepancy. Never call it an unverified nonconformance. |
| `unresolved` | the change falls outside SOW scope, or the SOW does not resolve an ambiguity | Treat the change as a framing discrepancy and a compliance risk |

Finalization is blocked only by an `unresolved` change, an `unverified` required
behavior, or a `conflicted-attestation` finding. The `attested` class never
blocks finalization.
