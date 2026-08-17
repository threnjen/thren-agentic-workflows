---
name: engagement-evidence-standard
description: "The single classification vocabulary every engagement stage uses when judging what the evidence supports about a workflow, behavior, or SOW criterion — the evidence classes (qa-backed / comparison-only / unverified), the scope classes (sow-authorized / unresolved), and what each requires. Use when: classifying QA or comparison evidence, deciding whether a change is an authorized scoped delta, or consuming another stage's classifications."
user-invocable: false
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->

# Engagement Evidence Standard

Every engagement stage that judges evidence uses these class names verbatim.
No stage invents its own vocabulary; a consumer may rely on receiving exactly
these values.

## The evidence base — what is judged

Comparisons are **docs vs. docs, never git-diff**. The evidence base is the
retained workspace reports **plus**, per side, the docs-writer set, the code
graph, and the QA package (`QA_AUTOMATED` with run results, plus the manual QA
checklist — `QA_USER` by default, or the engagement's configured manual QA
document(s)).

Docs sets, code graphs, and QA packages live at the passed analysis-branch
checkout paths **inside the client repositories** (e.g.,
`docs/CODEBASE_CONTEXT.md`, `docs/QA_AUTOMATED.md`, the manual QA checklist on the
side's analysis branch); the workspace holds only retained reports and is not
the whole evidence universe. Never infer absence from the workspace alone —
declare a source absent only after checking its passed pointer path, and name
the path checked in the absence note.

## Evidence classes — what the evidence supports

| Class | Requires |
|---|---|
| `qa-backed` | a completed PASS on an **exact matching** QA check on the upgraded side — a `QA_AUTOMATED` check ID with a run result, or a checked (`- [x]`) expected result in the manual QA checklist |
| `attested` | an accepted statement from the engagement owner closing a specific finding — remediated, or researched and dispositioned (rules below) |
| `comparison-only` | before/after comparison evidence (docs sets, graphs, retained reports) with no matching QA check |
| `unverified` | neither |

- `qa-backed` means the upgraded behavior was observed at the recorded QA
  standard. It is not, by itself, proof the original side behaved identically.
- A generic repository-level PASS with no matching check never yields
  `qa-backed`; that claim is `unverified`.
- Only `comparison-only` or better supports a "preserved from the original"
  statement.
- In client-facing compliance documents, `unverified` is rendered
  **NOT VERIFIED**.
- When the original side has no QA package the runtime evidence is
  asymmetric — state the asymmetry. Never convert it into a claim that the
  upgraded behavior was untested, nor into proof of before/after equivalence.
- "No identifiable delta" means no behavioral delta was established by the
  comparison evidence. It never means the codebase has no changes, and never
  means QA was absent.

## `attested` — owner-stated closure

An explicit statement from the engagement owner closes the identified finding
**without** rerunning audits, scans, or QA. Two forms qualify.

**Remediation.** The statement identifies the finding, states the corrected
behavior, and confirms the outcome. "The security items are fixed" is
insufficient — no finding identified, no behavior stated. "SEC-05 has been
remediated. JWT audience validation is now enforced." qualifies.

**Researched disposition.** The owner researched the finding and reached a
conclusion about it — invalid, already-correct behavior, immaterial, or real
but accepted at a stated severity. The statement identifies the finding, gives
the conclusion, and gives the basis in one line. "I researched INFRA-014; the
path is unreachable in the deployed configuration, so it is trivial" qualifies.
A bare severity opinion with no basis does not. The owner's own research is
sufficient basis — never demand an independent re-derivation of it.

**Settled means settled.** An accepted attestation of either form ends the
matter. No stage re-argues it, re-raises it as an open finding, asks for
further evidence, or re-surfaces it to the user for reconsideration. The only
thing that reopens it is retained evidence that directly contradicts it (see
Conflict below) or the user reopening it.

**How it is recorded.** The closure is `remediated (attested)` or
`dispositioned (attested)` — never `qa-backed`. The `engagement-workspace`
working-state file retains the finding ID, the statement, its form, its date,
the repository, and the attestor.

**What it closes, and only that.** The attested finding leaves the
introduced, residual-remediation, and open-work counts. It verifies no
unrelated behavior and provides no repository-wide assurance. Client documents
may describe the finding as remediated, or at the severity the owner's research
established; their methodology note must distinguish an owner attestation from
independently executed QA.

**Finalization.** `attested` satisfies the finalization gate for its own
finding. Never require refreshed audits solely to confirm an accepted
attestation — after accepting one, re-run synthesis only (findings, security,
narratives, compliance, manifest, gap review), never the source audits unless
the user explicitly asks.

**Conflict.** Retained evidence that directly contradicts an attestation is
`conflicted-attestation`: pause finalization for that finding and request
resolution. Never silently prefer either source.

## Scope classes — how an observed change is treated

Read the SOW's explicit exceptions and scope boundaries before classifying
any delta.

| Class | Requires | Consequence |
|---|---|---|
| `sow-authorized` | expressly required or permitted by the SOW — cite the clause or explicit scope exception | An approved scoped delta under any pair `mode`. Narrated as such; never a framing discrepancy, never an unverified nonconformance |
| `unresolved` | outside SOW scope, or an ambiguity the SOW does not resolve | A framing discrepancy and a compliance risk |

Only an `unresolved` change, an `unverified` required behavior, or a
`conflicted-attestation` finding blocks finalization. `attested` never does.
