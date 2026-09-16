---
name: audit-delta-report
description: "Produces a delta document comparing two audit reports of the same codebase taken at different points in time — what was resolved, improved, unchanged, transformed, and newly introduced, with a reconciled count of every finding on both sides and defects the newer work caused separated from pre-existing ones only the newer audit raised. Use when: asked for the delta, changes, fixes, or residuals between two reports in a dev audit directory, or to compare a baseline audit against a current one."
---

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
Scans rules. Two rules from that skill govern everything below. The producing
auditor's category names are the canonical dimensions. Never rename, merge, or
invent them across snapshots. Two findings match when they are the **same
underlying issue**, judged from description and evidence. Use a matching path as
corroboration only. Code moves, so line numbers shift.

The `auditor-conventions` audit finding truth gate applies independently to
every source finding and every proposed match. Reconcile each report's actual
rows before trusting its totals. Verify reachable production paths, tests,
material consequence, contracts, and issue identity against the trees. Exclude
a false or immaterial source finding from the actionable queue. Record an
explicit upstream correction in the delta. Never preserve it merely to make
inherited arithmetic close. Do not edit the source audits. Quarantine their
disputed arithmetic and show raw versus supported populations separately.

---

## 1. Resolve inputs before writing anything

1. **Locate the two reports.** The audit directory is `dev/<audit-name>/`
   (e.g. `dev/code-audit/`, `dev/infra-audit/`). Each snapshot is either a file
   or a subdirectory named for its label (`orig-code/`, `20260725/`). If a
   snapshot is a directory, use the full findings report as input. Read the
   summary too if one exists, but treat the report as authoritative.
2. **Derive snapshot labels** from the paths (`orig-code`, `20260725`, a branch
   name). Use these labels verbatim in every heading, table column, and filename.
3. **Locate both source trees.** A delta that uses only the two reports is
   weaker than one that can settle disagreements against the code. Ask the user
   for the baseline checkout path if it is not obvious (commonly a sibling
   directory such as `<repo>-orig`). If no baseline tree is available, say so in
   Comparison Limitations and proceed. Do not stall.

   When a snapshot is a **git ref** rather than a separate checkout, record the
   branch or tag *and* its resolved commit sha in the header. A branch name
   alone does not identify a snapshot because it moves. A delta labelled only
   `main` cannot be reproduced later. If the audit used a dirty working tree
   rather than a commit, say so in the header and in Comparison Limitations.
   That side is not reconstructible from git at all.

   For a branch-versus-branch comparison, state which baseline you used: the
   target branch's tip or the merge base. These baselines answer different
   questions. Against the tip, changes made on the target branch since the
   branch point appear as findings of the branch under review.
4. **Read both reports end to end** before classifying anything, including each
   report's own Coverage/Limitations and Positive Observations sections. Those
   two sections drive several dispositions and most of the honest caveats.
5. **Record the stated totals** from each report. Your reconciliation must equal
   them. If a report's internal counts disagree with its stated total, state that
   explicitly. Enumerate the actual finding rows. Correct or quarantine the
   source artifact before computing a delta. Do not build a reconciled
   comparison on contradictory population claims.

Treat both trees as **read-only**. Write only the two deliverables.

Write two deliverables at the output paths named in the spawn prompt. Never
invent paths. Put both under the **newer** snapshot's checkout. Read the
baseline only. Never write to it or place a deliverable there.

1. The **full delta** (section 4) — the complete comparison.
2. The **open-items queue** (section 5) — the actionable findings with
   attribution kept separate. Write it so a remediation agent can read it on
   its own, without seeing the full delta.

Always write both. Write the queue last, after the full delta's arithmetic
closes. Derive it from the full delta rather than assembling it in parallel.

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

Report `NEW` alone as the regression count. Never sum it with `PRE-EXISTING` in
any table or sentence. A finding the baseline auditor simply did not raise is
`PRE-EXISTING`. The code did not get worse. Reporting improved. Conflating them
sends the next engineer hunting regressions in code nobody touched.

Classification rules:

- **Validate before classifying.** A disposition accounts for a supported
  defect, not merely a row inherited from a report. Prove production
  reachability and material consequence. Record upstream corrections for rows
  that fail the truth gate, exclude them from the actionable queue, and show
  both inherited and supported delta arithmetic. The remediation-research
  reconciler, not this read-only comparison, owns source-report correction.

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
  moving, identify any re-rating and any real change in exposure. Do this at
  the item level and again in Comparison Limitations.
- **Separate "genuine regression" from "artifact of new functionality."** A NEW
  finding in a subsystem absent at baseline differs from a release worsening
  existing code. Label every NEW Critical/High as one or the other.
- **Removing a blind spot is not a change in the code.** When the baseline could
  not read something (an undecompiled binary, an out-of-repo reference), the
  current snapshot can read it. Classify the resulting finding as TRANSFORMED or
  PRE-EXISTING, never NEW. State the alternative reading and why you chose yours.
- **Merges and splits are allowed** (2 baseline → 1 current, or 1 baseline →
  2 current). Every merge and split must be enumerated in the Reconciliation
  subsection. Each current finding has exactly one owning baseline row.

### 2A. The co-location probe — required before any NEW

Attribution is a claim about the trees, not about what two auditors chose to
mention. A **separate attribution agent** executes this probe. The delta agent
marks unmatched findings provisional and hands off the construct identity, per
section 2D. Apply the following steps to each current finding with no matched
baseline counterpart:

1. **Find the construct in the baseline tree.** Search the whole tree by symbol
   name and signature, never by path or line. Between snapshots, a file may have
   been renamed, split, or moved. A path-only miss is not evidence of absence.
2. **Record one outcome, quoting both excerpts** (or the failed search):

| Baseline state | Disposition |
|---|---|
| Construct absent | `NEW` — the newer work introduced the code |
| Present, materially identical | `PRE-EXISTING` |
| Present but changed, and the change caused the defect | `NEW` — quote both versions |
| Present but changed, defect pre-dates the change | `PRE-EXISTING` |
| No baseline tree available | `UNVERIFIED-ORIGIN` — never bare `NEW` |

Every `PRE-EXISTING` carries an `Origin` from this closed set. Use one of these
values: `baseline auditor
did not raise it`, `additional lens on baseline <id> — same construct, different
dimension`, or `baseline blind spot now readable`.

### 2B. Same-position sweep — before classifying anything

Description-only matching mints a fresh `NEW` for every lens the second auditor
applied. Prevent this outcome mechanically:

- **Index both reports by `(file, enclosing symbol)`.** Adjudicate every shared
  position explicitly and record the verdict: same defect · additional lens on
  the same defect · genuinely different defect at the same location. Never leave
  a shared position unmatched by default.
- **A self-citation is a hard match signal.** A current finding that references
  a baseline finding's ID in its prose ("beyond the correctness bug (2.1/2.2)")
  concedes the shared position. Treat the reference as evidence, not commentary.
- **A different dimension is not a different defect.** One auditor may fault a
  construct for concurrency while the other faults it for performance. Treat it
  as one position with two lenses: `PRE-EXISTING`, `Origin: additional lens on baseline <id>`.

### 2C. Calibration guard

If `PRE-EXISTING` outnumbers `NEW`, the two auditors applied materially different
lenses. Say so in Comparison Limitations and do not tell a regression story off
the raw current-side count — most of the growth is reporting, not code.

### 2D. Provisional attribution and the probe handoff

Matching two reports and reading two source trees use different inputs. Assign
these jobs to two agents. The delta agent matches reports and never probes.

**The delta agent** marks every current finding without a matched baseline
counterpart `PROVISIONAL`. List each under a `## Provisional attribution —
pending probe` section with its item identifier, `path:line`, enclosing symbol,
and signature. Count the whole set as one **unattributed** bucket. Section 3
then closes without a probe having run.

**The attribution agent** replaces each provisional marking with its section 2A
outcome. It owns exactly these fields, and nothing else in either document:

- the item's disposition, `Origin`, baseline position, and probe evidence.
- the `NEW` and `Pre-existing` columns of the section 3A severity table.
- the `NEW`, `PRE-EXISTING`, and `UNVERIFIED-ORIGIN` rows of the Disposition
  Rollup, the `new / pre-existing` split in the dimension table, and the
  regression count in the Executive Summary.
- sections 10 and 10a.
- in the queue: filing each `NEW` entry into the severity-ordered list.
- in the queue: moving each `PRE-EXISTING` and `UNVERIFIED-ORIGIN` entry out of
  the work list and into the header's exclusion counts.
- in the queue: pruning the closure. When attribution settles every dependent
  as PRE-EXISTING, remove the closure item with those dependents. Convert an item
  that a surviving queued entry names in `Blocked by` into a `D`-numbered closure
  entry instead of leaving it.
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
  `unattributed` bucket (section 2D). The identity holds either way.
- **NEW, PRE-EXISTING, and UNVERIFIED-ORIGIN are excluded from the baseline
  percentage base.** State this explicitly. Express each as a percentage of the
  *current* report's total instead.
- Any baseline row classified without a corresponding current finding (verified
  on disk, or UNVERIFIED) must be named and must not add to the current-side count.
- If the arithmetic does not close, do not adjust a disposition to make it
  close. Find the missing or double-counted finding.

---

## 3A. Severity movement must be decomposed, not netted

**For every moving count, show its components on the same row.** Never show a
net figure alone in a table or in prose. A paragraph underneath does not repair
a misleading table. Readers skim, quote, and paste the table into status
updates.

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

Immediately below the table, before any other prose, state:

- **Turnover in the top bands.** For Critical and High, name the findings that
  left and the findings that arrived. State when a band's continuity is `0 of N`.
  That value means complete population turnover. It is almost always the
  most important fact in the section.
- **How much of the movement is re-rating.** Split `Entered band` and `Left
  band` into severity re-rating (same code, different judgement) versus real
  change in exposure. Where a rise is mostly re-rating, identify the portion.
  Use the infra example: "roughly two-thirds re-rating and one-third genuine
  worsening."
- **What the net conceals.** Any band whose net change is small while its
  underlying churn is large gets named explicitly.

---

## 4. Document structure

Sections are numbered. The starred sections are conditional. Everything else is
required and appears in this order.

1. **Header** — write one line per snapshot. Include the label, path, and ref
   plus resolved sha when the snapshot came from a git ref. Include the finding
   count and a scale metric (files audited, projects, lines). Then add a
   paragraph that fixes the path convention. Paths are relative to the
   snapshot's own root. When a path exists in both trees with different content,
   name the snapshot explicitly.
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
   here. Decompose the movement on each row.
4. **Disposition Rollup** — include the disposition table with counts and % of
   baseline. Add the NEW exclusion note. Then add a **Reconciliation** subsection
   that shows both sides' arithmetic and enumerates every merge and split.
5. **Dimension-Level Movement** — table: dimension × (baseline, current, net,
   **of current: carried / new / pre-existing**, assessment). The split is required
   for the same reason as section 3A. A dimension that fell from 10 to 6 by
   resolving 9 and adding 5 is not the same dimension. The net alone hides this
   fact. The assessment column is a short clause, not a number restated. Bold
   any dimension that regressed. Follow with a paragraph on the dimensions that
   are honestly worse, distinguishing worse-in-count from worse-in-kind.
6. **\*Dedicated Analysis** — include this only when one finding dominates the
   comparison and a table row cannot carry it. Examples include a credential
   exposure, a collapsed subsystem, or a delivery-mechanism change. Structure
   the analysis around four elements. Cover baseline exposure and audience,
   current exposure and audience, and any blast-radius change (narrower in X,
   wider in Y). End with the **Verdict**. State and reject the two
   wrong-but-tempting summaries.
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

   For PRE-EXISTING items, the Baseline line carries the position the probe found
   (`Not raised — position present at <path:line>`). Start the body with
   `**Not attributable to the newer work.**` Then add the `Origin` and the
   probe's paired excerpts. Group them under a `### Highs — Pre-existing,
   Newly Reported` heading, never inside the `New` group.
8. **Medium, Low, and Info Findings — Rollup** — add one subsection per
   dimension. Use a two-column table of `Disposition | Findings`. Separate
   findings with ` · `. Name both sides' locations in each entry. Add a
   `Cross-reference` row for items itemized in document section 7. This keeps
   the dimension complete without repeating those items. Open the section with
   this completeness statement: every remaining finding from both reports
   appears exactly once below.
9. **\*Dependency Delta** — include this for infra-flavoured audits or any audit
   where the dependency surface changed materially. Use a table with package ×
   (baseline version, current version, change, note). Collapse large shim
   families into one row and say so. Close with a summary sentence naming the
   one or two regressions in an otherwise improved surface.
10. **New Findings Introduced** — include all NEW findings. Number them and group
    them by severity, most severe first. Give each finding a location and a
    one-or-two-sentence regression judgement. Close with a count breakdown and a
    sentence that characterizes the NEW Critical/High set specifically.
    PRE-EXISTING findings never appear here.
10a. **Pre-existing Findings Newly Reported** — include all PRE-EXISTING and
    UNVERIFIED-ORIGIN findings in the same format. Give each its `Origin` and
    probe evidence. Close with the calibration guard's verdict (section 2C) when
    it triggers.
11. **Residual Risk** — list what remains unaddressed, ranked by severity. Group
    related findings that constitute one risk and say so ("these three findings
    should be treated as one risk, not three"). State up front that this is a
    comparison document, not a remediation plan.
12. **Comparison Limitations** — use bolded lead-ins and one paragraph each.
    Cover the following points at minimum. Omit any point that genuinely does
    not apply:
    - **Restructuring that made matching hard** — identify findings that could
      not be matched by path. State the rule used to adjudicate them.
    - **Limitations carried forward from either report's own coverage section.**
    - **What neither audit executed** — if both are static, say every
      runtime-behaviour classification inherits that limitation from both sides.
    - **Different auditors, different calibration** — list the specific severity
      movements that are re-rating.
    - **Scope differences** between the two audits, and any metric that is not
      comparable across them. Say so, and do not compare it.
    - **Findings adjudicated outside the two reports** — enumerate each. Include
      the command or file content that supports the conclusion.
    - **UNVERIFIED items** — give one entry each. State *why it cannot be
      settled* and the *evidence that would settle it*.
    - **Related unresolved questions** that bound the document's claims without
      affecting any disposition.

---

## 5. The open-items queue

The `auditor-conventions` skill defines the base entry shape, subsystem rule,
self-contained-entry rule, no-fixes rule, and ordering under **Open-Items Queue
Entries**. This section extends those rules for comparisons with a selection
rule, attribution fields, and dependency closure.

Write a second, smaller document containing **only the NEW and TRANSFORMED
findings**. A remediation research agent receives this file, the full delta,
both snapshot reports and summaries, and the available source trees. Write the
queue to stand alone anyway. The queue remains the scoped work list, while the
other inputs validate it and correct upstream errors.

**Selection.** NEW and TRANSFORMED, plus the **dependency closure** defined
below. RESOLVED, IMPROVED, UNCHANGED, UNVERIFIED, PRE-EXISTING, and
UNVERIFIED-ORIGIN are excluded by design. This queue covers what the current
snapshot introduced or carried across in a new shape, not everything still
open. Residual Risk in the full delta remains the complete picture. The two
documents disagree on purpose.

**A pre-existing defect is not queued work.** `PRE-EXISTING` and
`UNVERIFIED-ORIGIN` are open defects the newer work did not cause. They belong
to the same class as `UNCHANGED`, differing only in whether the baseline
auditor happened to raise them. Queueing them spends the remediation research
budget on code nobody touched. Excluding UNCHANGED while including them is
incoherent. Report them in the full delta's section 10a and count them among
the queue header's exclusions. They enter the queue only through the closure,
and only as a named dependency.

**The dependency closure.** Scoping by attribution and scoping by closability
are different things. A queue that uses only attribution gives the next agent
a work list it cannot finish. An excluded finding that a queued item cannot be
fixed without is part of that item's fix, not a separate concern.

After selecting NEW and TRANSFORMED, walk every selected item and ask what
else must change for it to close. Any **still-open** excluded finding named by
that answer joins the queue in its own section. Apply these rules:

- **Eligible pool: open findings only** — UNCHANGED, UNVERIFIED, and IMPROVED
  findings whose residue is still open, plus PRE-EXISTING and UNVERIFIED-ORIGIN.
  A RESOLVED finding can never be a dependency. It is already closed.
- **Entry is by named dependent.** A finding joins only because a specific
  queued item needs it. Record which item(s) pulled it in. Nothing enters the
  closure because it is severe, adjacent, or obviously worth doing — severity is
  not a ticket in. This rule keeps the closure from becoming "everything still open"
  by degrees.
- **Blocking or partial.** State, per dependency, whether the dependent item
  cannot be closed at all without it or can be closed partially. Both belong in
  the closure. They schedule differently.
- **Transitive, to a fixed point.** A dependency may itself depend on another
  excluded finding. Keep walking until no new findings enter. Say how many
  passes it took if more than one.
- **Kept visibly separate.** Closure items are *enabling work*, not defects the
  current snapshot introduced. Never merge them into the NEW/TRANSFORMED list or
  renumber them into it. Downstream steps rely on the attribution split, which
  distinguishes what this snapshot broke from what was already broken. A fix
  plan that blurs it will misreport what the newer work is responsible for.
- **Counted separately.** The closure does not change the reconciliation: the
  queue's NEW + TRANSFORMED count still equals the Disposition Rollup. Report
  the closure's own count alongside it, never folded into it.
- **An empty closure is a result.** If every queued item is independently
  closable, say so explicitly. Silence reads as "not checked."
- **Walked before attribution, pruned after.** The delta agent does not yet know
  which provisional items are `NEW`. It walks the closure over TRANSFORMED plus
  every provisional item, a superset of the final closure, and records
  dependencies among provisional items too. The attribution agent prunes it to
  the settled set per section 2D.

The queue must state this deliberate exclusion in its own header. An UNCHANGED
Critical is still a Critical. A reader who mistakes this file for "everything that needs fixing"
will act on a partial list. State the count of excluded findings by disposition.
Name any excluded Critical or High explicitly, so the omission is visible
without opening the full delta.

**Subsystem ownership** follows the conventions skill's rule, for closure items
as well as queued ones. Cross-subsystem dependencies do not duplicate ownership.
Record them in `Blocked by` or `Pulled in by`.

**Structure.** The base fields carry their conventions-skill meanings. The
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

- **TRANSFORMED entries carry their history.** Record the baseline location and
  what moved. A defect that survived one restructuring intact will survive a
  careless second one. Say what was tried and what it did not fix.
- **Counts must agree with the full delta.** The queue's NEW + TRANSFORMED item
  count equals `NEW + TRANSFORMED` from the Disposition Rollup. If it does not,
  the delta is wrong, not the queue. Closure items are counted and reported
  separately.
- **Every closure item traces back.** Each item names at least one queued item
  that pulled it in. Every `Blocked by` reference above resolves to an existing
  closure item. Remove any closure item that nothing depends on. It is scope
  creep.
- A queue with no NEW or TRANSFORMED items has no closure either — the closure
  is derived from them. Still write the file and say what was excluded.

---

## 6. Evidence and voice rules

- **Every disposition carries evidence.** Use a command and its result, a
  `path:line` with its content, or a quoted sentence from one of the reports.
  Prefer the trees when they disagree with the reports. Say which source you
  used.
- **Quote, don't paraphrase, when citing a report's own words** — especially in
  Coverage/Limitations and Positive Observations.
- **State the judgement calls as judgement calls.** If another reader could
  reasonably classify an item differently, say so. State what they would read
  differently and whether the totals would move.
- **Never present a net count without its composition.** A net summarizes two
  flows. Alone, it can routinely say the opposite of what happened. Apply this
  rule to severity bands, dimensions, totals, and every figure quoted in prose.
  See section 3A.
- **No hedging on the headline.** If the codebase got better, say it got better.
  If a dimension regressed, bold it and name the count. Do not average an
  improvement and a regression into "mixed results."
- **Never claim a secret is safe because it left the tree.** Removal is not
  revocation. If neither audit walked git history, say so and say the credential
  must still be treated as compromised.
- **Flag partial evidence rather than leaving it silent.** When a disposition
  rests on narrower evidence than the rest, add it under Comparison Limitations.
  State what would settle it.
- Plain declarative prose. No corporate softeners, no "leverage", no
  "significant" where a number belongs.

---

## 7. Before finishing

Use this list only for completeness proofs. These cross-cutting checks do not
belong to one section. The rules are stated once where they are defined. Do not
re-derive them from this list. The last item belongs to the attribution agent
(section 2D). The other items belong to the delta agent.

- [ ] Both sides' arithmetic closes against their reports' stated totals
      (section 3), with every merge and split enumerated in Reconciliation.
- [ ] Every finding from either side appears **exactly once** across the
      document: Criticals and Highs in the document's "Critical and High
      Findings — Item by Item" section, everything else in "Medium, Low, and
      Info Findings — Rollup".
- [ ] Every shared `(file, enclosing symbol)` position was adjudicated
      (section 2B) and the calibration guard (2C) was evaluated.
- [ ] The queue exists. Its NEW + TRANSFORMED count equals the Disposition
      Rollup's. Every `Blocked by` reference resolves to an existing closure
      item. The closure was walked to a fixed point. State an empty closure
      rather than leaving it silent.
- [ ] Both source trees are unmodified. The two deliverables are the only files
      written.
- [ ] Every retained finding passed the audit finding truth gate. Every omitted
      finding has an explicit upstream correction reflected in the delta and
      queue without modifying either source audit.
- [ ] No provisional marking survives.
