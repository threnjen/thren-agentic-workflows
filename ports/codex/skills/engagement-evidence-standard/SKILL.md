---
name: engagement-evidence-standard
description: "The single classification vocabulary every engagement stage uses when judging what the evidence supports about a workflow, behavior, or SOW criterion — the evidence classes (qa-backed / comparison-only / unverified), the scope classes (sow-authorized / unresolved), and what each requires. Use when: classifying QA or comparison evidence, deciding whether a change is an authorized scoped delta, or consuming another stage's classifications."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->
# Engagement Evidence Standard

Every engagement stage that judges evidence uses these class names verbatim.
No stage invents its own vocabulary; a consumer may rely on receiving exactly
these values.

## The evidence base — what is judged

Comparisons are **docs vs. docs, never git-diff**. The evidence base is the
retained workspace reports **plus**, per side, the docs-writer set, the code
graph, and the QA package (`QA_AUTOMATED` with run results, `QA_USER`).

Docs sets, code graphs, and QA packages live at the passed analysis-branch
checkout paths **inside the client repositories** (e.g.,
`docs/CODEBASE_CONTEXT.md`, `docs/QA_AUTOMATED.md`, `docs/QA_USER.md` on the
side's analysis branch); the workspace holds only retained reports and is not
the whole evidence universe. Never infer absence from the workspace alone —
declare a source absent only after checking its passed pointer path, and name
the path checked in the absence note.

## Evidence classes — what the evidence supports

| Class | Requires |
|---|---|
| `qa-backed` | a completed PASS on an **exact matching** QA check on the upgraded side — a `QA_AUTOMATED` check ID with a run result, or a checked (`- [x]`) `QA_USER` expected result |
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

## Scope classes — how an observed change is treated

Read the SOW's explicit exceptions and scope boundaries before classifying
any delta.

| Class | Requires | Consequence |
|---|---|---|
| `sow-authorized` | expressly required or permitted by the SOW — cite the clause or explicit scope exception | An approved scoped delta under any pair `mode`. Narrated as such; never a framing discrepancy, never an unverified nonconformance |
| `unresolved` | outside SOW scope, or an ambiguity the SOW does not resolve | A framing discrepancy and a compliance risk |

Only an `unresolved` change or an `unverified` required behavior blocks
finalization.
