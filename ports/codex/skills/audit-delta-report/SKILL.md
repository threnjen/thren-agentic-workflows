---
name: audit-delta-report
description: "Produces a delta document comparing two audit reports of the same codebase taken at different points in time — what was resolved, improved, unchanged, transformed, and newly introduced, with a reconciled count of every finding on both sides and defects the newer work caused separated from pre-existing ones only the newer audit raised. Use when: asked for the delta, changes, fixes, or residuals between two reports in a dev audit directory, or to compare a baseline audit against a current one."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->
# Audit Delta Report

Compares two audit reports of the same product — a **baseline** snapshot and a
**current** snapshot — and produces one document that accounts for every finding
on both sides exactly once.

Invoked by prompts of the form:

> I need a doc in `infra-audit` that shows the delta/changes/fixes/residuals
> between the audits between `dev/infra-audit/*-orig-code.md` and
> `dev/infra-audit/*-20260725.md`.

The output is a comparison document, not a remediation plan. It says what
changed and what the evidence is. It does not prescribe fixes.

Load `auditor-conventions` first for the severity scale and the Comparative
Scans rules. Two rules from there govern everything below: the producing
auditor's own category names are the canonical dimensions — never rename, merge,
or invent them across snapshots — and two findings match when they are the
**same underlying issue**, judged from description and evidence, with a matching
path as corroboration only. Code moves; line numbers shift.

The `auditor-conventions` audit finding truth gate applies independently to
every source finding and every proposed match. Reconcile each report's actual
rows before trusting its totals. Verify reachable production paths, tests,
material consequence, contracts, and issue identity against the trees. Omit a
false or immaterial source finding through an explicit upstream correction;
never preserve it merely to make inherited arithmetic close. Quarantine a
source report's disputed arithmetic until its finding population is corrected.

---

## 1. Resolve inputs before writing anything

1. **Locate the two reports.** The audit directory is `dev/<audit-name>/`
   (e.g. `dev/code-audit/`, `dev/infra-audit/`). Each snapshot is either a file
   or a subdirectory named for its label (`orig-code/`, `20260725/`). If a
   snapshot is a directory, the full findings report is the input; read the
   summary too if one exists, but the report is authoritative.
2. **Derive snapshot labels** from the paths (`orig-code`, `20260725`, a branch
   name). Use these labels verbatim in every heading, table column, and filename.
3. **Locate both source trees.** A delta written only from the two reports is
   weaker than one that can settle disagreements against the code. Ask the user
   for the baseline checkout path if it is not obvious (commonly a sibling
   directory such as `<repo>-orig`). If no baseline tree is available, say so in
   Comparison Limitations and proceed — do not stall.

   When a snapshot is a **git ref** rather than a separate checkout, record the
   branch or tag *and* its resolved commit sha in the header. A branch name
   alone does not identify a snapshot — it moves, and a delta labelled only
   `main` cannot be reproduced later. If a side was audited from a dirty
   working tree rather than a commit, say so in the header and in Comparison
   Limitations: that side is not reconstructible from git at all.

   For a branch-versus-branch comparison, state which baseline was used — the
   target branch's tip, or the merge base — because the two answer different
   questions. Against the tip, changes made on the target branch since the
   branch point appear as findings of the branch under review.
4. **Read both reports end to end** before classifying anything, including each
   report's own Coverage/Limitations and Positive Observations sections. Those
   two sections drive several dispositions and most of the honest caveats.
5. **Record the stated totals** from each report. Your reconciliation must equal
   them. If a report's own internal counts disagree with its stated total, say
   so explicitly, enumerate the actual finding rows, and correct or quarantine
   the source artifact before computing a delta. Do not build a reconciled
   comparison on contradictory population claims.

Both trees are **read-only**. The only files this work writes are its two
deliverables.

Two deliverables, both at the output paths the spawn prompt names — never at
paths you invent. Both land under the **newer** snapshot's checkout; the
baseline is read, never written to, and never receives a deliverable.

1. The **full delta** (section 4) — the complete comparison.
2. The **open-items queue** (section 5) — the actionable findings, attribution
   kept separate, written to be read on its own by a remediation agent that will
   never see the full delta.

Always write both. The queue is written last, after the full delta's arithmetic
closes, and is derived from it rather than assembled in parallel.

---

## 2. Disposition taxonomy

Every **baseline** finding gets exactly one of these. Every **current** finding
is either the mapped counterpart of a baseline finding, or `NEW`, or
`PRE-EXISTING`.

| Disposition | Meaning |
|---|---|
| `RESOLVED` | The defect no longer exists. Either fixed, or its responsibility was eliminated entirely. |
| `IMPROVED` | The defect persists in reduced form — narrower scope, lower reachability, smaller blast radius, or a partial fix. |
| `UNCHANGED` | The code/config position is materially identical. A severity re-rating with no code change is UNCHANGED, and must be labelled as a re-rating. |
| `TRANSFORMED` | The responsibility moved to a new file, mechanism, or format, and the defect moved with it. Same root cause, different shape. |
| `UNVERIFIED` | Neither report nor either tree can settle it. Requires a stated reason plus the specific evidence that would settle it. |
| `NEW` | The defect is attributable to the newer work: the code carrying it did not exist at baseline, or baseline code changed in a way that caused it. |
| `PRE-EXISTING` | A real, open defect the current report raised and the baseline report did not, whose code position is **materially identical in the baseline tree**. Not attributable to the newer work. |
| `UNVERIFIED-ORIGIN` | Raised only by the current report, and no baseline tree is available to establish whether the position pre-dates the newer work. |

`NEW` is the regression count, reported alone and never summed with
`PRE-EXISTING` in any table or sentence. A finding the baseline auditor simply
did not raise is `PRE-EXISTING`: the code did not get worse, the reporting got
better. Conflating them sends the next engineer hunting regressions in code
nobody touched.

Classification rules:

- **Validate before classifying.** A disposition accounts for a supported
  defect, not merely a row inherited from a report. Prove production
  reachability and material consequence. Record upstream corrections for rows
  that fail the truth gate, remove them consistently from reports, summaries,
  queues, and delta arithmetic, then reconcile the corrected populations.

- **Judge the defect, not the file.** A deleted file does not mean a resolved
  weakness. Ask: did the *responsibility* survive? If yes, did the *defect*
  survive with it? Responsibility gone → RESOLVED. Responsibility moved, defect
  moved too → TRANSFORMED.
- **RESOLVED requires positive evidence**, not the absence of a mention. Cite a
  command result, a file's current content, a test that asserts the invariant,
  or an explicit statement in the current report. "The current auditor did not
  raise it" is not evidence of resolution — that is UNCHANGED-if-verified or
  UNVERIFIED.
- **Separate re-rating from regression.** When severity moves without the code
  moving, say which portion is re-rating and which (if any) is a real change in
  exposure. Do this at the item level and again in Comparison Limitations.
- **Separate "genuine regression" from "artifact of new functionality."** A NEW
  finding in a subsystem that did not exist at baseline is not the same as the
  release making existing code worse. Label every NEW Critical/High as one or
  the other.
- **Removing a blind spot is not a change in the code.** When the baseline could
  not read something (an undecompiled binary, an out-of-repo reference) and the
  current snapshot can, the resulting finding is TRANSFORMED or PRE-EXISTING,
  never NEW — state the alternative reading and why you chose yours.
- **Merges and splits are allowed** (2 baseline → 1 current, or 1 baseline →
  2 current). Every merge and split must be enumerated in the Reconciliation
  subsection. Each current finding has exactly one owning baseline row.

### 2A. The co-location probe — required before any NEW

Attribution is a claim about the trees, not about what two auditors chose to
mention. A **separate attribution agent** executes this probe; the delta agent
marks unmatched findings provisional and hands off the construct identity, per
section 2D. For each current finding with no matched baseline counterpart:

1. **Find the construct in the baseline tree** — search the whole tree by symbol
   name and signature, never by path or line: between two snapshots a file may
   have been renamed, split, or moved, and a path-only miss is not evidence of
   absence.
2. **Record one outcome, quoting both excerpts** (or the failed search):

| Baseline state | Disposition |
|---|---|
| Construct absent | `NEW` — the newer work introduced the code |
| Present, materially identical | `PRE-EXISTING` |
| Present but changed, and the change caused the defect | `NEW` — quote both versions |
| Present but changed, defect pre-dates the change | `PRE-EXISTING` |
| No baseline tree available | `UNVERIFIED-ORIGIN` — never bare `NEW` |

Every `PRE-EXISTING` carries an `Origin` from this closed set: `baseline auditor
did not raise it`; `additional lens on baseline <id> — same construct, different
dimension`; `baseline blind spot now readable`.

### 2B. Same-position sweep — before classifying anything

Description-only matching mints a fresh `NEW` for every lens the second auditor
applied. Prevent it mechanically:

- **Index both reports by `(file, enclosing symbol)`.** Adjudicate every shared
  position explicitly and record the verdict: same defect · additional lens on
  the same defect · genuinely different defect at the same location. Never leave
  a shared position unmatched by default.
- **A self-citation is a hard match signal.** A current finding referencing a
  baseline finding's ID in its own prose ("beyond the correctness bug (2.1/2.2)")
  concedes the shared position. Treat it as evidence, not commentary.
- **A different dimension is not a different defect.** One construct faulted for
  concurrency by one auditor and performance by the other is one position with
  two lenses: `PRE-EXISTING`, `Origin: additional lens on baseline <id>`.

### 2C. Calibration guard

If `PRE-EXISTING` outnumbers `NEW`, the two auditors applied materially different
lenses. Say so in Comparison Limitations and do not tell a regression story off
the raw current-side count — most of the growth is reporting, not code.

### 2D. Provisional attribution and the probe handoff

Matching two reports and reading two source trees are different jobs on different
inputs, so they belong to two agents. The delta agent does the first and never
probes.

**The delta agent** marks every current finding with no matched baseline
counterpart `PROVISIONAL` and lists it under a `## Provisional attribution —
pending probe` section: item identifier, `path:line`, enclosing symbol, and
signature. Its arithmetic counts the whole set as one **unattributed** bucket, so
section 3 closes without any probe having run.

**The attribution agent** replaces each provisional marking with its section 2A
outcome, and owns exactly these fields — nothing else in either document:

- the item's disposition, `Origin`, baseline position, and probe evidence;
- the `NEW` and `Pre-existing` columns of the section 3A severity table;
- the `NEW`, `PRE-EXISTING`, and `UNVERIFIED-ORIGIN` rows of the Disposition
  Rollup, the `new / pre-existing` split in the dimension table, and the
  regression count in the Executive Summary;
- sections 10 and 10a;
- in the queue: filing each `NEW` entry into the severity-ordered list, moving
  each `PRE-EXISTING` and `UNVERIFIED-ORIGIN` entry out of the work list and into
  the header's exclusion counts, and pruning the closure — a closure item whose
  every dependent settled PRE-EXISTING leaves with them, and an item a surviving
  queued entry names in `Blocked by` becomes a `D`-numbered closure entry instead
  of leaving;
- the calibration guard's verdict.

The bucket's **total is invariant** under probing — only its internal split
changes — so this rewrite cannot break the delta's reconciliation. The
attribution agent verifies that invariant, stops if it fails, and deletes the
provisional section once every item in it is settled.

---

## 3. Reconciliation arithmetic (non-negotiable)

The document must prove its own completeness:

- **Baseline side:** `RESOLVED + IMPROVED + UNCHANGED + TRANSFORMED + UNVERIFIED`
  = the baseline report's stated total.
- **Current side:** `mapped counterparts + NEW + PRE-EXISTING + UNVERIFIED-ORIGIN`
  = the current report's stated total. Before the probe those three are one
  `unattributed` bucket (section 2D); the identity holds either way.
- **NEW, PRE-EXISTING, and UNVERIFIED-ORIGIN are excluded from the baseline
  percentage base.** State this explicitly. Express each as a percentage of the
  *current* report's total instead.
- Any baseline row classified without a corresponding current finding (verified
  on disk, or UNVERIFIED) must be named and must not add to the current-side count.
- If the arithmetic does not close, do not adjust a disposition to make it
  close. Find the missing or double-counted finding.

---

## 3A. Severity movement must be decomposed, not netted

**Every count in this document that moves must show what it is made of, on the
same row.** Never a net figure alone, in a table or in prose. A paragraph
underneath does not repair a misleading table — the table is what gets skimmed,
quoted, and pasted into a status update.

Build the severity table by tracking the flow through each band:

| Severity | Baseline | Resolved | Left band | Carried at band | Entered band | NEW | Pre-existing | Current | Continuity |
|---|---|---|---|---|---|---|---|---|---|
| Critical | 2 | 2 | 0 | 0 | 1 | 1 | 0 | 2 | 0 of 2 |

Columns:

- **Baseline / Current** — each report's count at that severity.
- **Resolved** — baseline findings at this band that are gone.
- **Left band** — baseline findings still present but no longer at this
  severity: improved to a lower band, or re-rated down.
- **Carried at band** — findings present on both sides at this same severity
  (UNCHANGED or TRANSFORMED without a severity move). This is the only column
  that represents genuine continuity.
- **Entered band** — findings that exist on both sides but arrived at this
  severity from another one: re-rated up, or a defect that genuinely worsened.
- **NEW** — findings the newer work is answerable for.
- **Pre-existing** — raised only by the current auditor, position identical at
  baseline. Include `UNVERIFIED-ORIGIN` here and footnote the count.
- **Continuity** — `carried of current`, in words: how many of today's findings
  at this severity are the same findings as yesterday's. This is the column
  that would have prevented the misleading zero.

Each row must satisfy: `Baseline = Resolved + Left band + Carried at band`, and
`Current = Carried at band + Entered band + NEW + Pre-existing`. Include a
`**Total**` row.

Then, immediately below the table and before any other prose, state:

- **Turnover in the top bands.** For Critical and High, name the findings that
  left and the findings that arrived. A band whose continuity is `0 of N` must
  say so in a sentence — that is a complete population turnover and it is
  almost always the most important fact in the section.
- **How much of the movement is re-rating.** Split `Entered band` and `Left
  band` into severity re-rating (same code, different judgement) versus real
  change in exposure. Where a rise is mostly re-rating, say which portion, as
  the infra example does: "roughly two-thirds re-rating and one-third genuine
  worsening."
- **What the net conceals.** Any band whose net change is small while its
  underlying churn is large gets named explicitly.

---

## 4. Document structure

Sections are numbered. The starred sections are conditional; everything else is
required and appears in this order.

1. **Header** — one line per snapshot: label, path (and ref plus resolved sha,
   when the snapshot came from a git ref), finding count, and a scale
   metric (files audited, projects, lines). Then a paragraph fixing the path
   convention: paths are relative to the snapshot's own root, and where a path
   exists in both trees with different content, the snapshot is named explicitly.
2. **Executive Summary** — the honest headline in prose, no bullets. Lead with
   where the improvement is concentrated and *why* it is concentrated there
   (usually one structural change resolves many findings at once). Then state
   plainly what got worse. Name the number of genuinely resolved findings and
   the Critical/High movement. State the regression count as `NEW` alone, and
   separately how many current findings are pre-existing conditions the baseline
   auditor did not raise. End with a one-sentence net verdict that a reader could
   act on. Never let a favourable total hide an unfavourable composition, and
   never let a growth in findings read as a growth in defects.
3. **Severity Movement** — see section 3A. A net-count table is not acceptable
   here; the movement must be decomposed on the row.
4. **Disposition Rollup** — the disposition table with counts and % of baseline,
   the NEW exclusion note, then a **Reconciliation** subsection showing both
   sides' arithmetic and enumerating every merge and split.
5. **Dimension-Level Movement** — table: dimension × (baseline, current, net,
   **of current: carried / new / pre-existing**, assessment). The split is required
   for the same reason as section 3A: a dimension that fell from 10 to 6 by
   resolving 9 and adding 5 is not the same dimension, and the net alone says
   it is. The assessment column is a short clause, not a number restated. Bold
   any dimension that regressed. Follow with a paragraph on the dimensions that
   are honestly worse, distinguishing worse-in-count from worse-in-kind.
6. **\*Dedicated Analysis** — include only when one finding dominates the
   comparison and a table row cannot carry it (a credential exposure, a
   collapsed subsystem, a delivery-mechanism change). Structure: what the
   baseline exposed and to whom → what the current snapshot exposes and to whom
   → did the blast radius change (narrower in X, wider in Y) → **Verdict**, with
   the two wrong-but-tempting summaries stated and rejected.
7. **Critical and High Findings — Item by Item** — every Critical and High from
   *either* side, grouped under `### Criticals` then `### Highs — Resolved and
   Improved`, `### Highs — Unchanged and Transformed`, `### Highs — New`. Item
   format:

   ```markdown
   #### [DISPOSITION] <finding title>
   - **Baseline:** [Severity] `path:line`   (or "Not present")
   - **Current:** [Severity] `path:line`    (or "Not present")
   - **What changed:** <mechanism — what actually moved, and what did not>
   - **Evidence:** <command output, file content, quoted report statement>
   ```

   For NEW items the Baseline line may be dropped and the body replaced with a
   bolded regression judgement (`**Genuine regression.**` /
   `**Artifact of new functionality.**`) plus the explanation.

   For PRE-EXISTING items the Baseline line carries the position the probe found
   (`Not raised — position present at <path:line>`), and the body leads with
   `**Not attributable to the newer work.**` followed by the `Origin` and the
   probe's paired excerpts. Group them under a `### Highs — Pre-existing,
   Newly Reported` heading, never inside the `New` group.
8. **Medium, Low, and Info Findings — Rollup** — one subsection per dimension,
   each a two-column table of `Disposition | Findings`, findings separated by
   ` · `. Each entry names both sides' locations. Add a `Cross-reference` row
   for items itemized in document section 7 so the dimension still reads completely
   without repeating them. Open the section with the completeness statement:
   every remaining finding from both reports appears exactly once below.
9. **\*Dependency Delta** — for infra-flavoured audits, or any audit where the
   dependency surface changed materially. Table: package × (baseline version,
   current version, change, note). Collapse large shim families into one row and
   say so. Close with a summary sentence naming the one or two regressions in an
   otherwise improved surface.
10. **New Findings Introduced** — all NEW findings, numbered, grouped by
    severity, most severe first, each with a location and a one-or-two-sentence
    regression judgement. Close with a count breakdown and a sentence
    characterizing the NEW Critical/High set specifically. PRE-EXISTING findings
    never appear here.
10a. **Pre-existing Findings Newly Reported** — all PRE-EXISTING and
    UNVERIFIED-ORIGIN findings, same format, each with its `Origin` and probe
    evidence. Close with the calibration guard's verdict (section 2C) when it
    triggers.
11. **Residual Risk** — what remains unaddressed, ranked by severity. Group
    related findings that constitute one risk and say so ("these three findings
    should be treated as one risk, not three"). State up front that this is a
    comparison document, not a remediation plan.
12. **Comparison Limitations** — bolded lead-ins, one paragraph each. Cover at
    minimum, and omit any that genuinely does not apply:
    - **Restructuring that made matching hard** — which findings could not be
      matched by path, and the rule used to adjudicate them.
    - **Limitations carried forward from either report's own coverage section.**
    - **What neither audit executed** — if both are static, say every
      runtime-behaviour classification inherits that from both sides.
    - **Different auditors, different calibration** — list the specific severity
      movements that are re-rating.
    - **Scope differences** between the two audits, and any metric that is
      therefore not comparable across them (say so; do not compare it).
    - **Findings adjudicated outside the two reports** — enumerate each, with
      the command or file content the conclusion rests on.
    - **UNVERIFIED items** — one entry each: *why it cannot be settled* and
      *evidence that would settle it*.
    - **Related unresolved questions** that bound the document's claims without
      affecting any disposition.

---

## 5. The open-items queue

The base entry shape, the subsystem rule, the self-contained-entry rule, the
no-fixes rule, and the ordering are defined in `auditor-conventions` under
**Open-Items Queue Entries**. This section is the comparative extension of it:
the selection rule, the attribution fields, and the dependency closure.

A second, smaller document containing **only the NEW and TRANSFORMED findings**.
Its reader is a remediation research agent that receives this file, the full
delta, both snapshot reports and summaries, and the available source trees.
Write it to stand alone anyway: the queue remains the scoped work list, while
the other inputs exist to validate it and correct upstream errors.

**Selection.** NEW and TRANSFORMED, plus the **dependency closure** defined
below. RESOLVED, IMPROVED, UNCHANGED, UNVERIFIED, PRE-EXISTING, and
UNVERIFIED-ORIGIN are excluded by design: this queue is scoped to what the
current snapshot introduced or carried across in a new shape, not to everything
still open. Residual Risk in the full delta remains the complete picture, and
the two documents disagree on purpose.

**A pre-existing defect is not queued work.** `PRE-EXISTING` and
`UNVERIFIED-ORIGIN` are open defects the newer work did not cause — the same
class as `UNCHANGED`, differing only in whether the baseline auditor happened to
raise them. Queueing them spends the remediation research budget on code nobody
touched, and excluding UNCHANGED while including them is incoherent. They are
reported in the full delta's section 10a and counted among the queue header's
exclusions. They enter the queue only through the closure, and only as a named
dependency.

**The dependency closure.** Scoping by attribution and scoping by closability
are different things, and a queue that only does the first hands the next agent
a work list it cannot finish. An excluded finding that a queued item cannot be
fixed without is not a separate concern — it is part of that item's fix.

So: after selecting NEW and TRANSFORMED, walk every selected item and ask what
else must change for it to close. Any **still-open** excluded finding that
answer names joins the queue in its own section. Rules:

- **Eligible pool: open findings only** — UNCHANGED, UNVERIFIED, and IMPROVED
  findings whose residue is still open, plus PRE-EXISTING and UNVERIFIED-ORIGIN.
  A RESOLVED finding can never be a dependency; it is already closed.
- **Entry is by named dependent.** A finding joins only because a specific
  queued item needs it. Record which item(s) pulled it in. Nothing enters the
  closure because it is severe, adjacent, or obviously worth doing — severity is
  not a ticket in, and this is the rule that keeps the closure from becoming
  "everything still open" by degrees.
- **Blocking or partial.** State, per dependency, whether the dependent item
  cannot be closed at all without it or can be closed partially. Both belong in
  the closure; they schedule differently.
- **Transitive, to a fixed point.** A dependency may itself depend on another
  excluded finding. Keep walking until no new findings enter. Say how many
  passes it took if more than one.
- **Kept visibly separate.** Closure items are *enabling work*, not defects the
  current snapshot introduced. Never merge them into the NEW/TRANSFORMED list or
  renumber them into it. The attribution split — what this snapshot broke versus
  what was already broken — is load-bearing downstream, and a fix plan that
  blurs it will misreport what the newer work is responsible for.
- **Counted separately.** The closure does not change the reconciliation: the
  queue's NEW + TRANSFORMED count still equals the Disposition Rollup. Report
  the closure's own count alongside it, never folded into it.
- **An empty closure is a result.** If every queued item is independently
  closable, say so explicitly. Silence reads as "not checked."
- **Walked before attribution, pruned after.** Which provisional items are `NEW`
  is not known yet, so the delta agent walks the closure over TRANSFORMED plus
  every provisional item — a superset of the final closure — recording
  dependencies among provisional items too. The attribution agent prunes it to
  the settled set per section 2D.

Because the exclusion is deliberate and consequential, the queue must say so in
its own header — an UNCHANGED Critical is still a Critical, and a reader who
mistakes this file for "everything that needs fixing" will act on a partial
list. State the count of excluded findings by disposition, and name any
excluded Critical or High explicitly, so the omission is visible without
opening the full delta.

**Subsystem ownership** follows the conventions skill's rule, for closure items
as well as queued ones. Cross-subsystem dependencies do not duplicate ownership;
record them in `Blocked by` or `Pulled in by`.

**Structure.** The base fields carry their conventions-skill meanings; the
fields marked below are this mode's additions.

```markdown
# <Audit type> Delta — Open Items — <baseline-label> → <current-label>

Source: `<full delta filename>`. Current snapshot: `<label>`, audited at
`<path or ref@sha>`, <N> findings.

Scope: the <N> findings classified NEW or TRANSFORMED — the defects this
snapshot is answerable for — plus <N> excluded findings pulled in as their
dependency closure. **Not a complete list of open defects.** Excluded by design:
<N> RESOLVED, <N> IMPROVED, <N> UNCHANGED, <N> UNVERIFIED, <N> PRE-EXISTING, <N>
UNVERIFIED-ORIGIN. After the closure, the still-excluded set contains <N>
Critical and <N> High findings that remain open — see the full delta's Residual
Risk section: <one line naming each still-excluded Critical and High>.

## <Severity> — <N> items

### <N>. [NEW | TRANSFORMED] <title>
- **Source finding:** <current audit report identifier>          # added
- <the conventions skill's base fields, in its order>
- **Origin:** genuine regression | artifact of new functionality | reporting
  difference | responsibility moved from `<baseline path:line>`  # added
- **Blocked by:** <closure item number(s) this cannot close without, or "none">  # added

## Dependency closure — <N> items

Excluded findings that queued items above cannot close without. These are
enabling work, not defects this snapshot introduced. <N> closure passes.

### D<N>. [<original disposition>] <title>
- **Source finding:** <current audit report identifier>          # added
- <the conventions skill's base fields, in its order>
- **Pulled in by:** item <N> (<blocking | partial>), item <N> (<blocking | partial>)  # added
- **What the dependent items need from it:** <the specific decision or artifact
  that unblocks each — not a restatement of the finding>          # added
```

Number closure items with a `D` prefix so the two sets can never be conflated by
an item number alone.

**Rules.**

- **TRANSFORMED entries carry their history.** The baseline location and what
  moved are the useful part: a defect that survived one restructuring intact
  will survive a careless second one. Say what was tried and what it did not fix.
- **Counts must agree with the full delta.** The queue's NEW + TRANSFORMED item
  count equals `NEW + TRANSFORMED` from the Disposition Rollup. If it does not,
  the delta is wrong, not the queue. Closure items are counted and reported
  separately.
- **Every closure item traces back.** Each one names at least one queued item
  that pulled it in, and every `Blocked by` reference above resolves to a
  closure item that exists. A closure item nothing depends on is scope creep —
  remove it.
- A queue with no NEW or TRANSFORMED items has no closure either — the closure
  is derived from them. Still write the file and say what was excluded.

---

## 6. Evidence and voice rules

- **Every disposition carries evidence.** A command and its result, a
  `path:line` with its content, or a quoted sentence from one of the reports.
  Prefer the trees over the reports when they disagree, and say which you used.
- **Quote, don't paraphrase, when citing a report's own words** — especially in
  Coverage/Limitations and Positive Observations.
- **State the judgement calls as judgement calls.** Where a different reader
  could reasonably classify an item differently, say so, say what they would be
  reading differently, and say whether the totals would move.
- **Never present a net count without its composition.** A net is a summary of
  two flows, and on its own it routinely says the opposite of what happened.
  This applies to severity bands, dimensions, totals, and any figure quoted in
  prose. See section 3A.
- **No hedging on the headline.** If the codebase got better, say it got better.
  If a dimension regressed, bold it and name the count. Do not average an
  improvement and a regression into "mixed results."
- **Never claim a secret is safe because it left the tree.** Removal is not
  revocation. If neither audit walked git history, say so and say the credential
  must still be treated as compromised.
- **Flag partial evidence rather than leaving it silent.** When a disposition
  rests on narrower evidence than the rest, add it under Comparison Limitations
  with what would settle it.
- Plain declarative prose. No corporate softeners, no "leverage", no
  "significant" where a number belongs.

---

## 7. Before finishing

Completeness proofs only — the cross-cutting checks no single section above can
establish on its own. The rules themselves are stated once, where they are
defined; do not re-derive them from this list. The last item is the attribution
agent's (section 2D); the rest are the delta agent's.

- [ ] Both sides' arithmetic closes against their reports' stated totals
      (section 3), with every merge and split enumerated in Reconciliation.
- [ ] Every finding from either side appears **exactly once** across the
      document: Criticals and Highs in the document's "Critical and High
      Findings — Item by Item" section, everything else in "Medium, Low, and
      Info Findings — Rollup".
- [ ] Every shared `(file, enclosing symbol)` position was adjudicated
      (section 2B) and the calibration guard (2C) was evaluated.
- [ ] The queue exists; its NEW + TRANSFORMED count equals the Disposition
      Rollup's; every `Blocked by` reference resolves to a closure item that
      exists; the closure was walked to a fixed point, and an empty closure is
      stated rather than left silent.
- [ ] Both source trees are unmodified; the two deliverables are the only files
      written.
- [ ] Every retained finding passed the audit finding truth gate; every omitted
      finding has an explicit upstream correction reflected in all affected
      counts and artifacts.
- [ ] No provisional marking survives.
