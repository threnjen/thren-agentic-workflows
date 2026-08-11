---
name: engagement-configuration
description: "Schema and validation rules for an engagement configuration file — the declaration of an engagement's comparison pairs, SOW/contract pointer, and deliverables-spec pointer. Use when: loading or validating an engagement config, authoring one for a new engagement, or referencing the canonical field vocabulary for preparation orchestration and baseline capture."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->
# Engagement Configuration

This skill defines the format of an engagement configuration file and the
validation rules an orchestrator applies when loading it. The schema section
below is the **load contract**: the Client Deliverable orchestrator loads and
validates configs against it before spawning any stage, the preparation stage
re-checks against it, and the graph baseline capture procedure reuses
its field vocabulary. Field names defined here are canonical — downstream
consumers must use them verbatim.

There is no executable validator; validation is behavior the loading
orchestrator performs by following the rules in this skill.

## Config Location Convention

The config is a single YAML file. By convention it is named
`engagement.yaml` and lives at the root of the engagement's working
directory, but any path works. The user authors the file and points the
orchestrator at it; the orchestrator never scans the filesystem for a config
nobody pointed at, and never gathers configuration interactively.

## Bootstrapping a New Config

`engagement-template.yaml`, beside this file, is the canonical starting
config: a commented fill-in-the-blank version of the schema below. The
Client Deliverable orchestrator copies it into a new workspace as
`engagement.yaml` and hands the user its path — that copy, not an interview,
is how a config gets authored. Keep the template in step with the schema:
every required field appears in it uncommented, every optional field appears
commented out.

A copy still containing the literal `FILL ME` is **unfilled, not invalid** —
it has not been authored yet. Do not run the Validation Rules against it or
emit their errors; say plainly which file is waiting and which lines still
read `FILL ME`.

## Schema

Top-level fields:

| Field | Required | Meaning |
|-------|----------|---------|
| `sow_document` | yes | The SOW/contract for the engagement: a single path, **or** a list of paths in priority order |
| `deliverables_spec` | yes | Path to the deliverables-specification document |
| `pairs` | yes | List of comparison pairs; **any number, one or more** — the schema imposes no upper bound and no expected count |

### Multi-document SOWs

An engagement whose contract spans a base SOW plus updates and amendments
lists them all under `sow_document`, **lowest priority first**: each entry
supersedes every entry before it wherever they conflict. A single path is
shorthand for a one-entry list; consumers treat both forms identically and
never assume a single document.

No document is merged, rewritten, or combined into a master copy — the list
*is* the resolution order. A consumer citing a SOW obligation cites the
specific document it came from, and when two documents cover the same
obligation it reports the winning one. This ordering is the only conflict
rule; there is no per-clause negotiation.

`sow_document` and `deliverables_spec` are engagement-confidential. Their
contents must never be copied into generated outputs, reports, or committed
artifacts; only the paths appear in the config.

### Comparison pairs

Each entry in `pairs` is one comparison and has:

| Field | Required | Meaning |
|-------|----------|---------|
| `name` | yes | Unique label for the pair, used in error messages and outputs |
| `type` | yes | `repo` (two separate repositories) or `branch` (two branches of one repository) |
| `original` | yes | The side representing the original codebase |
| `upgraded` | yes | The side representing the upgraded codebase |
| `repo_path` | branch pairs only | Path to the single repository whose branches are compared |
| `mode` | no | Value story for the pair: `modernization` (pure modernization) or `modernized-and-improved` (modernization plus improvements). **Defaults to `modernization` when absent** — existing configs without it remain valid |
| `code_delta_path` | no | Path to an already-completed code-scan delta report for this pair (original vs. upgraded). When present, the code dimension is not scanned on either side; the supplied delta is consumed directly |
| `infra_delta_path` | no | Path to an already-completed infra-scan delta report for this pair. Same effect for the infra dimension |

`code_delta_path` and `infra_delta_path` are independent — supplying one
does not imply the other. Supplying neither is the normal case: both
dimensions are scanned fresh on both sides.

Exactly one side is `original` and exactly one side is `upgraded` — the role
is expressed by which key the side sits under, so a pair with both roles
present has them by construction; a pair missing either key is invalid.

Side fields by pair type:

- **`type: repo`** — `original` and `upgraded` each contain `path`: the
  local path to that side's repository.
- **`type: branch`** — the pair contains `repo_path`, and `original` and
  `upgraded` each contain `branch`: the branch name for that side.

Either side may also carry `code_audit_path` and `infra_audit_path`: paths to
a **directory** holding that side's already-completed audit for that
dimension. They are how an engagement reuses audits it already ran instead
of re-scanning. A dimension counts as supplied only when **both** sides
declare it; one side alone is a validation error, because a comparison needs
two sides. A supplied dimension is not scanned on either side — see the
`engagement-pair-loop` skill for what the loop does with it.

`code_audit_path`/`infra_audit_path` (per-side audit directories) and
`code_delta_path`/`infra_delta_path` (a pair-level delta file, below) are
two independent ways to supply a dimension, and may both be present: the
audits are the per-side evidence and the delta is the comparison. Supplying
either form skips that dimension's scans.

Either side may also carry `manual_qa_paths`: a list of paths, relative to
that side's repository root, naming that repository's manual QA
document(s). It **overrides** the default manual-QA gate target
(`docs/QA_USER.md`) for that side — a repository whose manual QA lives in
`docs/QA_MICK.md` declares it here and is never asked for `QA_USER.md`.
Absent, the default applies. This overrides only the manual QA document;
the automated runbook is always `docs/QA_AUTOMATED.md`.

### Paths

Paths may be absolute or relative. Relative paths resolve against the
directory containing the config file. This applies to every path field:
`sow_document` (each entry), `deliverables_spec`, `path`, `repo_path`,
`code_delta_path`, `infra_delta_path`, `code_audit_path`, and
`infra_audit_path`. The exception is `manual_qa_paths`, whose entries
resolve against **their own side's repository root**, not the config.

### Annotated example

The example below shows N=2 purely for illustration — a config may declare
any number of pairs; the pair count is unbounded and never assumed.

```yaml
sow_document:                         # a list: later entries supersede earlier
  - docs/sow1.md                      # relative to this file's directory
  - docs/sow-update-20260707.md
  - docs/sow-amendments.md            # wins on conflict
deliverables_spec: docs/deliverables.md

pairs:
  - name: service-api                 # a repo pair: two separate repositories
    type: repo
    original:
      path: repos/service-api-legacy
      code_audit_path: repos/service-api-legacy/dev/code-audit/orig/codex
      infra_audit_path: repos/service-api-legacy/dev/infra-audit/orig/codex
    upgraded:
      path: /abs/path/service-api-v2  # absolute paths are also accepted
      manual_qa_paths:                # optional; overrides docs/QA_USER.md
        - docs/QA_MICK.md
      code_audit_path: /abs/path/service-api-v2/dev/code-audit/20260804/codex
      infra_audit_path: /abs/path/service-api-v2/dev/infra-audit/20260804/codex
    mode: modernized-and-improved     # optional; omitted -> modernization
    code_delta_path: scans/service-api-code-delta.md    # optional; skips the code scans
    infra_delta_path: scans/service-api-infra-delta.md  # optional; skips the infra scans

  - name: web-frontend                # a branch pair: two branches of one repo
    type: branch
    repo_path: repos/web-frontend
    original:
      branch: main
    upgraded:
      branch: upgrade/framework-bump
```

## Validation Rules

Validation runs when the orchestrator loads the config, **before any
preparation work starts**. Any violation halts preparation immediately
(fail fast); nothing is prepared against a partially valid config. Every
violation produces a specific, named error identifying the pair, the field,
and what was expected:

| Rule | Error emitted |
|------|---------------|
| `sow_document` present, and every entry (one path, or each list entry) resolves | `sow_document: path '<value>' does not resolve (expected an existing file)` |
| `sow_document`, when a list, is non-empty | `sow_document: empty list (expected at least one document, in priority order)` |
| `deliverables_spec` present and path resolves | `deliverables_spec: path '<value>' does not resolve (expected an existing file)` |
| `pairs` is non-empty | `pairs: empty list (expected at least one comparison pair)` |
| Every pair has a unique `name` | `pair '<name>': duplicate name (expected pair names to be unique)` |
| Every pair `type` is `repo` or `branch` | `pair '<name>': type '<value>' (expected 'repo' or 'branch')` |
| Every pair has both `original` and `upgraded`, each exactly once | `pair '<name>': missing '<original|upgraded>' (expected exactly one of each role per pair)` |
| Repo pair: each side's `path` resolves to a directory | `pair '<name>': <original|upgraded>.path '<value>' does not resolve (expected an existing directory)` |
| Repo pair: the two sides' paths are not the same directory | `pair '<name>': original.path and upgraded.path resolve to the same directory (expected two distinct repositories)` |
| Branch pair: `repo_path` resolves to a repository | `pair '<name>': repo_path '<value>' does not resolve (expected an existing repository directory)` |
| Branch pair: each side's `branch` exists in the repository | `pair '<name>': <original|upgraded>.branch '<value>' does not exist in '<repo_path>' (expected an existing branch)` |
| Branch pair: the two branches are not the same ref | `pair '<name>': original.branch and upgraded.branch name the same ref (expected two distinct branches)` |
| `mode`, when present, is `modernization` or `modernized-and-improved` | `pair '<name>': mode '<value>' (expected 'modernization' or 'modernized-and-improved')` |
| `code_audit_path` / `infra_audit_path`, when present, resolve to an existing directory | `pair '<name>': <original\|upgraded>.<code\|infra>_audit_path '<value>' does not resolve (expected an existing directory)` |
| `code_audit_path` / `infra_audit_path`, when present on one side, are present on the other | `pair '<name>': <code\|infra>_audit_path given on '<side>' only (expected it on both sides, or neither)` |
| `manual_qa_paths`, when present, is a non-empty list (entries are resolved by the preparation stage, not here) | `pair '<name>': <original\|upgraded>.manual_qa_paths is empty (expected at least one path, or omit the field)` |
| `code_delta_path` / `infra_delta_path`, when present, resolve to an existing non-empty file | `pair '<name>': <code|infra>_delta_path '<value>' does not resolve (expected an existing non-empty file)` |

Explicitly allowed (do not over-validate):

- The **same repository may appear in more than one pair** — a repo
  participating in multiple comparisons is valid.

## Not Validation Failures

Missing supporting artifacts — documentation or code graphs for a declared
repository — are **not** config validation failures. They are work for the
preparation stage, which regenerates them after the config validates.
Validation covers only the config's own declarations (paths, branches,
roles, structure).
