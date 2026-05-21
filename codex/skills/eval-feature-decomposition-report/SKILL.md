<!-- Generated from .github/skills source-of-truth. Do not edit manually. -->
# Eval Feature Decomposition Report

Use this skill when writing a feature decomposition evaluation report. Follow the section order, table schemas, and scoring dimensions exactly as defined here.

## Output File

Write to `eval/feature_decomp_eval_round_N.md` in the target repository, where N is auto-incremented from the highest existing round number. If no prior rounds exist, start at `1`.

Do not overwrite an existing file. If the computed path already exists, increment N again.

## Report Structure

Write all sections in this exact order. Do not reorder, rename, or omit sections.

---

### 1. Header Block

```markdown
# Feature Decomposer Evaluation — Phase <phase-id>
**Date**: <YYYY-MM-DD>
**Ground truth branch**: `<golden-branch>`
**Test branch**: `<test-branch>`
**Agent evaluated**: `feature-decomposer` + `feature-plan-set` skill
```

No additional text in the header block. The four lines above are the complete header.

---

### 2. Framing Note

Always include this section immediately after the header. Adapt the language to the specific branches being compared, but always convey these two points:

1. The ground truth docs are **as-built records** — reverse-engineered from the finished diff after implementation.
2. The test docs are **forward-looking planning docs** — produced before implementation.

This asymmetry is structurally expected. Several gaps may stem from this asymmetry, not from agent failures. The evaluator must be explicit about which gaps are inherent and which are addressable.

Use a horizontal rule before and after the Framing Note section.

---

### 3. Overall Quality Score

```markdown
## Overall Quality Score: X.X / 10
```

Follow with one paragraph (3–6 sentences) that:
- States the overall quality level
- Names the strongest dimensions
- Names the main deductions with their magnitude (e.g., "concentrated in two addressable issues")
- Explicitly notes what is NOT counted against the test branch due to the planning/as-built asymmetry

---

### 4. Structural Comparison Table

```markdown
## Structural Comparison

| Dimension | Ground Truth | Test Docs | Gap |
|---|---|---|---|
| Files per feature | ... | ... | ... |
| Feature count | ... | ... | ... |
| Manifest present | Yes/No | Yes/No | ... |
| Tasks status | ... | ... | Expected (pre-implementation) or [describe] |
| AC traceability table | ... | ... | Expected (pre-implementation) or [describe] |
| Ordering note in manifest | ... | ... | [None / Test is better / Golden is better] |
```

Add rows for any other structural dimensions that differ between the branches. For dimensions where the test branch is strictly better than the golden path, write "Test is actually **better** here" in the Gap column.

---

### 5. Feature Naming Comparison Table

```markdown
## Feature Naming Comparison

| Golden Path | Test Branch | Assessment |
|---|---|---|
| `01-...` | `01-...` | [Exact match / Correctly named; ordering differs / Unnecessary prefix; ... / Unnecessary suffix; ...] |
```

Include every feature as a row. After the table, write a short paragraph summarizing:
- How many of N feature names match exactly
- What pattern of violation (if any) exists
- Which agent instruction or naming rule the violation relates to

---

### 6. Feature Ordering Analysis

Write a short prose section (1–3 paragraphs) analyzing the ordering of features between branches:
- State which branch's ordering differs (if any) and which specific features were reordered
- Quote or paraphrase the manifest ordering note if one was provided
- Assess whether the reordering was justified, noting that if both orderings are functionally valid, that is an acceptable outcome

---

### 7. Wave Structure Comparison Table

```markdown
## Wave Structure Comparison

| | Golden Path | Test Branch |
|---|---|---|
| Wave 1 | ... | ... |
| Wave 2 | ... | ... |
| ...   | ... | ... |
```

After the table, state the wave count on each branch and explain the key difference. Assess whether either approach is clearly wrong or whether both are valid interpretations of the wave rules.

---

### 8. What the Test Docs Did Well

```markdown
## What the Test Docs Did Well

### 1. [Dimension Name]
[One or more paragraphs. Be specific: cite section names, file paths, table data, or AC counts as evidence.]

### 2. ...
```

Use numbered `###` headings. Include at least 3 items. Order from most significant to least significant. When the test branch is strictly better than the golden path on a dimension, say so explicitly.

---

### 9. What the Test Docs Failed At

```markdown
## What the Test Docs Failed At

### 1. [Issue Title] ([Structural Gap — Expected] or [Addressable] or [Minor])
[One or more paragraphs. For each issue, state: (a) what was missing or wrong, (b) what the golden path had instead, (c) whether the gap is inherent to the planning/as-built asymmetry or addressable via agent/skill changes.]

### 2. ...
```

Use numbered `###` headings. Include the severity tag in the heading: `(Structural Gap — Expected)` for pipeline-asymmetry gaps, `(Addressable)` for agent/skill fixable gaps, or `(Minor)` for small divergences with no functional impact.

Do not penalize the test branch for gaps that are explicitly labelled `(Structural Gap — Expected)`.

---

### 10. Agent and Skill Improvement Opportunities

```markdown
## Agent and Skill Improvement Opportunities

### Opportunity 1: [Short Title]

**Current agent instruction**: "[Quote or paraphrase the exact current text]"

**Problem**: [What the agent produced vs what it should have produced. 2–4 sentences.]

**Suggested addition to [agent name] / [skill name]**:
> [Exact proposed instruction text in blockquote form]

### Opportunity 2: ...
```

Use numbered `###` headings. Every opportunity must:
- Quote the current instruction text (or state "No current instruction exists")
- Clearly describe the observed gap
- Propose specific, actionable instruction text in a blockquote
- Name the target file (agent or skill)

Mark opportunities that cannot be fixed by agent/skill changes as `(Pipeline Gap)` in the heading and describe the structural change required instead.

---

### 11. Why Specific Elements Were Missed

```markdown
## Why Specific Elements Were Missed

| Element | Reason | Avoidable? |
|---|---|---|
| [Element name] | [Root cause] | Yes / No / Only with pipeline changes |
```

Include every notable gap from sections 9 and 10. The table is a concise summary of the causal analysis from those sections. Do not introduce new findings here; consolidate what has already been discussed.

---

### 12. Overall Quality Assessment

```markdown
## Overall Quality Assessment

| Dimension | Score | Notes |
|---|---|---|
| Feature identification | X/10 | [1-sentence evidence] |
| Feature naming | X/10 | ... |
| Dependency analysis | X/10 | ... |
| Wave assignment | X/10 | ... |
| Plan sections (A–F) | X/10 | ... |
| AC quality | X/10 | ... |
| Context file quality | X/10 | ... |
| Manifest quality | X/10 | ... |
| Test planning | X/10 | ... |
| Missing: implementation records | N/A | Not the decomposer's role; pipeline gap |
```

Follow the table with one bold paragraph summarizing the overall verdict. The paragraph should state the overall quality level, name the strongest and weakest areas, and indicate whether the gaps are primarily addressable or inherent.

---

## Scoring Guidance

| Dimension | 10/10 | 7–9/10 | 4–6/10 | 1–3/10 |
|---|---|---|---|---|
| Feature identification | Correct count, correct scope boundaries | 1 minor scope issue | 1 feature wrong or missing | 2+ features wrong or missing |
| Feature naming | All names match golden path exactly | 1–2 names have minor qualifiers | 3+ names have qualifiers or are misleading | Names are unclear or violate conventions |
| Dependency analysis | All dependencies documented with specific file references | All deps present, some without file references | Some deps missing | Significant deps missing |
| Wave assignment | Same wave structure as golden path | Valid structure, 1 extra wave | 2 extra waves or one misassignment | Incorrect sequencing |
| Plan sections (A–F) | All sections present and fully populated | All sections present, some thin | 1–2 sections missing or empty | 3+ sections missing |
| AC quality | All ACs testable, specific, non-redundant; test branch adds valuable extras | All ACs testable; test branch roughly equivalent | Some ACs vague or untestable | Many ACs missing or not testable |
| Context file quality | All required sections present and accurate | All sections present; 1 architectural note is off | 1–2 sections missing | Major sections missing |
| Manifest quality | All required columns, verification assets, dependency graph complete | Minor omissions in verification assets | Missing dependency graph or parallel safety | Manifest is incomplete or absent |
| Test planning | Strong scenarios with `[PROPOSED]` tagging for unconfirmed names | Scenarios present; method naming could be clearer | Minimal test planning | No test planning |

**Implementation records** always score `N/A` — they are produced post-implementation and are never the decomposer's responsibility.

## Neutrality Rules

- Do not penalize the test branch for incomplete task checklists (`[ ]` vs `[x]`). Pre-implementation docs are expected to have open tasks.
- Do not penalize for the absence of exact test method names when methods are appropriately labelled `[PROPOSED]` or `[NEW]`.
- Do not penalize for the absence of "Actual Behavior Shipped" language in plan files — that language belongs in implementation records, not plans.
- Do not penalize for the absence of `-implementation.md` files — that is a pipeline-level gap, not a decomposer failure.
- When the test branch produces strictly better output on a dimension than the golden path, call that out positively.
