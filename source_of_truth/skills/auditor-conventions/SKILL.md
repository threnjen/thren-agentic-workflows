---
name: auditor-conventions
description: "Shared conventions for all auditor subagents and any agent that produces or compares audit findings. Defines standard constraints, deliverables, scope determination, Unity detection, file-type taxonomy, common exclusions, process flow, report structure, severity levels, open-items queue entries, and output format. Each auditor extends this with domain-specific content. Use when: performing any type of audit."
---

# Auditor Conventions

These conventions apply to every auditor subagent and every agent that produces, queues, or compares audit findings. Load this skill first. Then follow domain-specific instructions in your agent definition. If your agent also loads a narrower conventions skill for its family, follow that skill wherever the two differ.

## Standard Constraints

- Complete the FULL audit before producing deliverables.
- DO NOT suggest fixes inline. Report only findings with file:line references.
- DO NOT skip any audit category. Cover every in-scope file.
- DO NOT give vague feedback. Cite specific files and locations for every finding.
- DO NOT edit source files. Create report documents only.

Your agent definition adds domain-specific constraints (scope focus, additional prohibitions).

## Audit finding truth gate

Treat every candidate finding as untrusted until the target snapshot supports
all of the following. Detail, repetition, severity, and agreement between
auditors are not substitutes for evidence.

1. **Population:** Mechanically enumerate findings and reconcile every stated
   total. Quarantine contradictory counts. Never choose one silently.
2. **Production path:** Read the exact construct, its reachable production
   callers, and its constraining tests. Test-only bypasses, invalid object
   states, and hypothetical future callers are not current production defects
   unless that boundary is the defect.
3. **Material consequence:** Name an observed failure or enforceable security,
   correctness, operability, or maintenance hazard. Reject style preferences,
   positive observations, optional micro-optimizations, and unmeasured
   speculation.
4. **Contract:** Check repository rules, tests that preserve surprising
   behavior, and current authoritative documentation for external APIs or
   platforms. State an unresolved question instead of inventing an answer.
5. **Identity and scope:** Match the underlying responsibility and failure
   mode, not a shared path, label, technology, or category. Do not merge or
   transform unrelated defects.
6. **Bounded actionability:** Establish that an in-scope correction and a
   verification capable of failing exist, without prescribing the fix in an
   audit report. If the evidence supports only containment or the real closure
   needs an unowned decision or excluded system, state that limit.

Omit any candidate that fails production-path or material-consequence proof.
Narrow or qualify candidates whose contract, identity, scope, or actionability
is only partly supported. Use language proportional to evidence: `can`, `under
this condition`, and `has no fixed cap` are different claims from `will`,
`always`, and `unbounded`.

## Deliverables

This section governs a **full-repository audit**. A narrower conventions skill
loaded by your agent or explicit paths in the spawn prompt replace it. Write to
the specified paths and return in the specified shape.

Your output is a report document saved to `dev/[audit-name]/`:
- `[audit-name]-report.md` — Full structured findings
- `[audit-name]-summary.md` — Executive summary with priority action items

Present your findings in chat first, then write the deliverables.

**Subagent return contract**: when invoked as a subagent, after writing the
deliverables return a compact summary only — the report and summary file
paths, findings-by-severity totals, and status — never bulk report content.

## Scope Determination

When spawned, determine scope with the user. When the spawn prompt states the
scope, take it as-is without asking:
- **Full codebase** — All in-scope files (default if unspecified)
- **Specific files/directories** — As specified by the user
- **Single file or module** — Deep audit of one area

Your agent definition specifies which file-type categories are in scope.

## Target Repository

An audit runs against one **target repository root** and writes to one
**output root**. They are not always the same directory.

- The spawn prompt may name a target root explicitly (`Target repository:
  <abs-path>`). When it does, audit that tree and no other. Express every
  finding path **relative to that target root**. Never use an absolute path or a
  path relative to your working directory.
- When no target is named, the target root is the current repository, and the
  output root is the same.
- The target tree is **read-only**. When the output root is a different
  repository, write deliverables there. Never create files inside a target
  unless the prompt tells you to write there.
- State the target root and output root in the report header. Include the
  counts that scale with the target (files audited, projects, and lines). Later
  comparisons depend on these counts.

## Multi-Target Audits

The caller may run the same audit against several targets for comparison,
typically an older and newer revision of one product. Each target gets an
independent audit run and report.

- **Each run is independent.** Audit the assigned target on its own terms. Do
  not read another target's tree or another run's report. A comparison is
  meaningful only when neither side anchors to the other. Auditor - Delta
  performs the comparison as a separate step.
- **Identical prompts.** The caller must give every run the same instruction
  text. Vary only the target root, snapshot label, and output path. If the spawn
  prompt appears tailored to one side (extra hints, a list of things to inspect,
  or prior report conclusions), say so in Coverage and Limitations. This limits
  what any comparison can claim.
- **Snapshot label.** The caller assigns each run a label (`orig-code`,
  `20260725`, or a short sha). Use it in the report header and in the deliverable
  filenames.
- **Layout.** Per-target deliverables go to `dev/[audit-name]/<snapshot-label>/`
  under the output root, and comparison documents, when produced, go to
  `dev/[audit-name]/[audit-name]-delta-<baseline-label>-to-<current-label>*.md`.
- **One output root: the newer snapshot.** Write every target's deliverable
  under the newer comparison point. This is the later checkout or the branch
  under review, rather than its target branch. Keep the older target read-only.
  Do not write its own report under that target. If the spawn prompt names an output path
  outside the audited tree, write to that path as instructed.
- **Record your own limits.** A delta relies heavily on Coverage and
  Limitations. State what you could not read, resolve, decompile, or execute.
  Write for a reader who will compare this report with a second report of the
  same product.

## Unity Detection

Before discovery, test the target repository against the canonical Unity
detection predicate in the auto-loaded `tech-stack-detection` instruction.

When the predicate matches, load `unity-development` and
`unity-review-knowledge` before proceeding. Then apply the Unity guidance named
for your domain in the agent definition.

## File-Type Taxonomy

All auditable files fall into these categories. Each auditor declares its
in-scope categories.

| Category | File Types |
|----------|-----------|
| **Source code** | `.py`, `.js`, `.mjs`, `.cjs`, `.ts`, `.tsx`, `.jsx`, `.java`, `.kt`, `.kts` |
| **Test files** | `tests/`, `test_*.py`, `*_test.py`, `*.test.js`, `*.test.ts`, `*.spec.js`, `*.spec.ts` |
| **Dependency manifests** | `requirements.txt`, `pyproject.toml`, `package.json`, `pom.xml`, lock files |
| **Infrastructure (IaC)** | `.tf`, `.tfvars`, `template.yaml`, `samconfig.toml`, Kubernetes manifests |
| **Docker** | `Dockerfile`, `docker-compose.yml`, `.dockerignore` |
| **CI/CD** | `.github/workflows/*.yml`, `Jenkinsfile`, `buildspec.yml` |
| **Build scripts** | `.sh`, `.ps1`, `.bat`, `Makefile`, `build.mjs` |
| **Configuration** | `.toml`, `.cfg`, `.ini`, `.env`, `.env.*`, `.editorconfig`, `.eslintrc`, `.prettierrc`, `tsconfig.json` |
| **Documentation** | `.md`, `.rst`, `.txt`, `docs/` directories |
| **Agent/customization** | `.github/agents/`, `.github/instructions/`, `.github/prompts/`, `AGENTS.md`, `copilot-instructions.md` |

### Always Excluded

Regardless of audit domain, exclude these generated and cached directories:
- `__pycache__/`, `.venv/`, `node_modules/`, `target/`, `build/`, `dist/`
- Exclude generated files and build artifacts.

## Process

Complete these steps in order:

1. Discover all in-scope files.
2. Read each file thoroughly.
3. Evaluate every file against all audit categories.
4. Cross-reference files for patterns.
5. Apply the audit finding truth gate.
6. Classify severity.
7. Report.

## Report Structure

### 1. Executive Summary

- Total files audited
- Findings by severity (Critical / High / Medium / Low)
- Top 5 highest-priority items

### 2. Findings by Category

Present a table for each audit category:

| # | File(s) | Line(s) | Severity | Finding | Detail |
|---|---------|---------|----------|---------|--------|
| 1 | `path/to/file.py` | L12-L15 | Medium | [Short title] | [Specific explanation with context] |

**Column guidelines:**
- **File(s)**: Comma-separated paths when a finding spans multiple files
- **Line(s)**: Specific line numbers or ranges. Use `—` when structural
- **Severity**: Critical, High, Medium, or Low (see Severity Levels below)
- **Finding**: Short descriptive title
- **Detail**: Specific, actionable explanation

### 3. Cross-Cutting Observations

Record patterns that span multiple files. Include consistency issues, DRY
violations with locations, and patterns to standardize.

### 4. Recommended Priority Order

1. **Quick wins** — Low effort, high impact
2. **Important fixes** — Security, correctness, or safety items
3. **Improvement pass** — Best practices, DRY cleanup, documentation, style

## Severity Levels

All auditors use this four-level structure. Each auditor defines domain-specific
meanings in its agent file.

| Level | General Guideline |
|-------|-------------------|
| **Critical** | Security vulnerability, data loss, crash, or deployment-breaking defect |
| **High** | Likely bug, missing safety controls, or significant misconfiguration |
| **Medium** | Missing best practices, DRY violations, documentation gaps, readability |
| **Low** | Style inconsistency, minor cleanup, formatting |

## Findings, Verdicts, and What Counts as Closed

- **"Remediated in code" is not "verified."** A fix without a re-run gate is
  not a verdict. Move status lines only on fresh final-state evidence. The user
  issues verdicts. No agent writes a status line.
- **Every finding must name the revision it examined.** An artifact without its
  revision cannot be reconciled later. A release dossier must confirm that each
  artifact post-dates the code it covers.
- **Missing or incomplete required checks are a hard gate: the verdict is `NO-GO`.**
  A failed, hung, or unavailable evaluator never becomes a passing result. A
  later success never repairs an earlier failure. Enumerate every such case by
  name and give a concrete reason.
- **A fixed budget is never relaxed to make a gate pass.** If the budget is
  genuinely unachievable, the honest outcome is a user-approved
  acceptance-criterion change. Include proof that a deliberately broken
  implementation still fails the new gate.
- **When the honest fix needs capability the scope excludes, record the finding open with routing.**
  Redefining the finding to fit the scope closes nothing. "A future rebuild
  will handle it" is a prediction unless it names the capability that rebuild
  must gain.

## Open-Items Queue Entries

An open-items queue is a standalone work list selected from audit findings. A
remediation research agent reads it and may never see the source report. Use
this shape for every entry and mode:

```markdown
### <N>. [<state>] <title>
- **Location:** `path:line` (current snapshot)
- **Severity:** <Critical | High | Medium | Low | Info>
- **Dimension:** <the producing auditor's own category name>
- **Subsystem:** <stable production owner>
- **The defect:** <what is wrong, self-contained — assume no other document>
- **Evidence:** <the file content, command result, or report statement>
- **Constraints a fix must respect:** <what the audit established about this
  code — a caller depends on the current shape, a test asserts the present
  behavior — or "none recorded">
```

- **Subsystem ownership.** Give every item one `Subsystem`. Use the smallest
  stable runtime, component, or responsibility boundary that owns remediation.
  Never use the dimension, severity, a convenient directory, or a proposed
  work phase. Use the same concise name for items with the same production
  owner.
- **Self-contained entries.** Make every entry actionable without its source
  document. Repeat the evidence instead of cross-referencing a section number.
- **No fixes.** State defects and constraints in the queue. The next agent
  researches and proposes the fix. Prejudging the fix narrows that agent's
  options.
- **Header.** State the current snapshot (ref plus resolved SHA, or explicitly a
  dirty tree), the selection rule, the queued count, and what the selection
  excluded by count and severity.
- Order sections by severity, most severe first, then by dimension.
- Write the file even when nothing was selected, and say so plainly. An empty
  queue is a real result. A missing file is ambiguous.

A comparative delta extends this entry shape with attribution and closure
fields. See `audit-delta-report` section 5. No other document extends it.

## Domain-Specific Extensions

Your agent definition may add sections beyond this common format. For example,
Auditor - Refactor adds Dependency Graph Observations and Risk Matrix.

## Comparative Scans

Use these rules when comparing two independent scans of the same dimension,
such as two sides of an engagement pair:

- **Report against report, never a git diff.** Use the two scan reports as the
  inputs. Consult the trees only to settle a specific question.
- **Stable categories**: Use the producing agent's category names as the
  canonical comparison categories. Security uses Auditor - Security's 10 scope
  categories. Code quality uses Auditor - Code's 14 audit categories. Infra
  uses Auditor - Infra's 14 audit categories. Dependencies uses the dependency
  inventory and duplicate-library checks. Never rename, merge, or invent
  categories across scans.
- **Severity**: Use the 4-level scale above (see Severity Levels). Compare
  severities only by these labels.
- **Posture first, then issue identity** — in every dimension. Compare posture
  first by category × severity counts on each side. This comparison shows the
  before and after results. Then match individual findings to substantiate the
  posture comparison. Two findings match when they are the **same underlying
  issue**, judged from category, description, and evidence. Treat a matching
  `Location` file path as corroborating evidence, never as the key. Code moves
  during refactors and rewrites, and line numbers shift between revisions. Never
  use the scan-local `ID` column for cross-scan matching. Treat an original
  finding that cannot be confidently matched or ruled out as possibly persisting
  (unfixed). Flag it for review. Never silently count it as fixed.
- **Unmatched findings are never dropped, and are never classified from
  silence.** A finding on only one side is *newly reported* or *no longer
  reported*. These are reporting states, not verdicts about the code. This
  skill does not answer whether the finding is a regression, a pre-existing
  defect, or genuinely resolved. `audit-delta-report`'s disposition taxonomy
  and attribution probe are authoritative and override anything here. A
  consumer that produces no delta must report both reporting states and say that
  attribution was not established.
