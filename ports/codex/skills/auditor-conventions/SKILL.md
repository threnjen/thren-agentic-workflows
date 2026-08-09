---
name: auditor-conventions
description: "Shared conventions for all auditor subagents and any agent that produces or compares audit findings. Defines standard constraints, deliverables, scope determination, Unity detection, file-type taxonomy, common exclusions, process flow, report structure, severity levels, open-items queue entries, and output format. Each auditor extends this with domain-specific content. Use when: performing any type of audit."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->
# Auditor Conventions

Common conventions for every auditor subagent and any agent that produces, queues, or compares audit findings. Load this skill first, then follow domain-specific instructions in your agent definition. Where your agent also loads a narrower conventions skill for its own family (for example `pr-review-conventions`), that skill governs wherever the two differ.

## Standard Constraints

- Complete the FULL audit before producing any deliverables
- DO NOT suggest fixes inline — only report findings with file:line references
- DO NOT skip any audit category — be comprehensive across all in-scope files
- DO NOT give vague feedback — every finding must cite specific files and locations
- DO NOT edit source files — you only create report documents

Your agent definition adds domain-specific constraints (scope focus, additional prohibitions).

## Audit finding truth gate

Treat every candidate finding as untrusted until the target snapshot supports
all of the following. Detail, repetition, severity, and agreement between
auditors are not substitutes for evidence.

1. **Population:** Mechanically enumerate findings and reconcile every stated
   total. Quarantine contradictory counts; never choose one silently.
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
loaded by your agent, or explicit paths in the spawn prompt, replace it — write
to the paths and return in the shape you were given.

Your output is a report document saved to `dev/[audit-name]/`:
- `[audit-name]-report.md` — Full structured findings
- `[audit-name]-summary.md` — Executive summary with priority action items

Present your findings in chat first, then write the deliverables.

**Subagent return contract**: when invoked as a subagent, after writing the
deliverables return a compact summary only — the report and summary file
paths, findings-by-severity totals, and status — never bulk report content.

## Scope Determination

When spawnd, determine scope with the user — or, when invoked as a subagent
with scope stated in the spawn prompt, take that scope as-is without asking:
- **Full codebase** — All in-scope files (default if unspecified)
- **Specific files/directories** — As specified by the user
- **Single file or module** — Deep audit of one area

Your agent definition specifies which file-type categories are in scope.

## Target Repository

An audit runs against one **target repository root** and writes to one
**output root**. They are not always the same directory.

- The spawn prompt may name a target root explicitly (`Target repository:
  <abs-path>`). When it does, audit that tree and no other, and express every
  finding path **relative to that target root** — never as an absolute path and
  never relative to your working directory.
- When no target is named, the target root is the current repository, and the
  output root is the same.
- The target tree is **read-only**. When the output root is a different
  repository, write deliverables there; never create files inside a target you
  were not told to write to.
- State the target root and the output root in the report header, along with
  the counts that scale it (files audited, projects, lines). A later comparison
  depends on those numbers being stated.

## Multi-Target Audits

The caller may run the same audit against several targets so the results can be
compared (typically an older and a newer revision of one product). Each target
gets its own independent audit run and its own report.

- **Each run is independent.** Audit the target you were given on its own
  terms. Do not read another target's tree, and do not read another run's
  report — a comparison is only meaningful if neither side was anchored to the
  other. The comparison itself is a separate step, performed by Auditor - Delta.
- **Identical prompts.** The caller must give every run the same instruction
  text, varying only the target root, the snapshot label, and the output path.
  If your spawn prompt appears to have been tailored to one side (extra hints,
  a list of things to look for, a prior report's conclusions), say so in your
  Coverage and Limitations section — it bounds what any comparison can claim.
- **Snapshot label.** The caller assigns each run a label (`orig-code`,
  `20260725`, a short sha). Use it in the report header and in the deliverable
  filenames it names.
- **Layout.** Per-target deliverables go to `dev/[audit-name]/<snapshot-label>/`
  under the output root, and comparison documents, when produced, go to
  `dev/[audit-name]/[audit-name]-delta-<baseline-label>-to-<current-label>*.md`.
- **One output root: the newer snapshot.** Every deliverable from every target
  is written under the newer comparison point — the later checkout, or the
  branch under review rather than the branch it targets. An older target is
  read-only and receives no files, including its own report. If your spawn
  prompt names an output path outside the tree you are auditing, that is
  intentional; write where you are told.
- **Record your own limits.** Coverage and Limitations is the section a delta
  leans on hardest: what you could not read, could not resolve, did not
  decompile, did not execute. Write it for a reader who will hold it against a
  second report of the same product.

## Unity Detection

Before discovery, test the target repository against the canonical Unity detection predicate
in the auto-loaded `tech-stack-detection` instruction.

On a match, load both `unity-development` and
`unity-review-knowledge` before proceeding, then apply the Unity guidance your
agent definition names for your domain.

## File-Type Taxonomy

All auditable files fall into these categories. Each auditor declares which categories are in scope.

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

Regardless of audit domain, exclude generated and cached directories:
- `__pycache__/`, `.venv/`, `node_modules/`, `target/`, `build/`, `dist/`
- Generated files and build artifacts

## Process

Discover all in-scope files → Read each thoroughly → Evaluate against all audit categories → Cross-reference for patterns → Apply the audit finding truth gate → Classify severity → Report.

## Report Structure

### 1. Executive Summary

- Total files audited
- Findings by severity (Critical / High / Medium / Low)
- Top 5 highest-priority items

### 2. Findings by Category

For each audit category, present a table:

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

Patterns spanning multiple files: consistency issues, DRY violations with locations, patterns to standardize.

### 4. Recommended Priority Order

1. **Quick wins** — Low effort, high impact
2. **Important fixes** — Security, correctness, or safety items
3. **Improvement pass** — Best practices, DRY cleanup, documentation, style

## Severity Levels

All auditors use this 4-level structure. Each auditor defines domain-specific meanings in its agent file.

| Level | General Guideline |
|-------|-------------------|
| **Critical** | Security vulnerability, data loss, crash, or deployment-breaking defect |
| **High** | Likely bug, missing safety controls, or significant misconfiguration |
| **Medium** | Missing best practices, DRY violations, documentation gaps, readability |
| **Low** | Style inconsistency, minor cleanup, formatting |

## Findings, Verdicts, and What Counts as Closed

- **"Remediated in code" is not "verified."** A fix without a re-run gate is not a verdict; status lines move only on fresh final-state evidence. Verdicts are issued by the user — no agent writes a status line.
- **Every finding must name the revision it examined.** An artifact that does not name its revision cannot be reconciled later, and a release dossier must confirm each artifact post-dates the code it covers.
- **Missing or incomplete required checks are a hard gate: the verdict is `NO-GO`.** A failed, hung, or unavailable evaluator never becomes a passing result, and a later success never repairs an earlier failure. Enumerate every such case by name with a concrete reason.
- **A fixed budget is never relaxed to make a gate pass.** If it is genuinely unachievable, the honest outcome is a user-approved acceptance-criterion change carrying proof that a deliberately broken implementation still fails the new gate.
- **When the honest fix needs capability the scope excludes, record the finding open with routing.** Redefining the finding to fit the scope closes nothing, and "a future rebuild will handle it" is a prediction unless it names the capability that rebuild must gain.

## Open-Items Queue Entries

An open-items queue is a standalone work list selected from audit findings. Its
reader is a remediation research agent that may never see the report it came
from. Every entry, in every mode:

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

- **Subsystem ownership.** Every item gets one `Subsystem`: the smallest stable
  runtime, component, or responsibility boundary that owns the remediation —
  never the dimension, the severity, a directory chosen for convenience, or a
  proposed work phase. Use the same concise name for items with the same
  production owner.
- **Self-contained entries.** Every entry must be actionable without the
  document it was derived from. Repeat the evidence rather than
  cross-referencing a section number.
- **No fixes.** The queue states defects and constraints. Researching and
  proposing the fix is the next agent's job; prejudging it here narrows what
  that agent considers.
- **Header.** State the current snapshot (ref plus resolved SHA, or explicitly a
  dirty tree), the selection rule, the queued count, and what the selection
  excluded, by count and severity.
- Order sections by severity, most severe first, then by dimension.
- Write the file even when nothing was selected, and say so plainly. An empty
  queue is a real result; a missing file is ambiguous.

A comparative delta extends this entry shape with attribution and closure
fields — see `audit-delta-report` section 5. Nothing else does.

## Domain-Specific Extensions

Your agent definition may add sections beyond this common format (e.g., Auditor - Refactor adds Dependency Graph Observations and Risk Matrix).

## Comparative Scans

When two independent scans of the same dimension are compared (e.g., two sides
of an engagement pair), these rules make them comparable:

- **Report against report, never a git diff.** The two scans' reports are the
  inputs; the trees are consulted only to settle a specific question.
- **Stable categories**: the producing agent's own category names are the
  canonical comparison categories — security uses Auditor - Security's 10 scope
  categories, code quality uses Auditor - Code's 14 audit categories, infra
  uses Auditor - Infra's 14 audit categories, dependencies uses the dependency
  inventory and duplicate-library checks. Never rename, merge, or invent
  categories across scans.
- **Severity**: the 4-level scale above (see Severity Levels). Compare
  severities only by these labels.
- **Posture first, then issue identity** — in every dimension. The headline
  comparison is posture-level: counts by category × severity on each side, the
  before/after of the results themselves. Per-finding matching then
  substantiates it: two findings match when they are the **same underlying
  issue**, judged from category, description, and evidence; a matching file path
  from `Location` is corroborating evidence, never the key — code moves in
  refactors and rewrites, and line numbers shift between revisions. The
  scan-local `ID` column is never used for cross-scan matching. An original
  finding that can be neither confidently matched nor confidently ruled out is
  treated as possibly persisting (unfixed), flagged for review — never silently
  counted as fixed.
- **Unmatched findings are never dropped, and are never classified from
  silence.** A finding appearing on only one side is *newly reported* or *no
  longer reported* — reporting states, not verdicts about the code. Whether it
  is a regression, a pre-existing defect, or genuinely resolved is an
  attribution question this skill does not answer. `audit-delta-report`'s
  disposition taxonomy and its attribution probe are authoritative and override
  anything here; a consumer that produces no delta reports the two reporting
  states and says the attribution was not established.
