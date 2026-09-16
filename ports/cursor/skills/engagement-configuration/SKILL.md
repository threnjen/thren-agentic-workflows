---
name: engagement-configuration
description: "Schema and validation rules for an engagement configuration file — the declaration of an engagement's comparison pairs, SOW/contract pointer, and deliverables-spec pointer. Use when: loading or validating an engagement config, authoring one for a new engagement, or referencing the canonical field vocabulary for preparation orchestration and baseline capture."
user-invocable: false
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->

# Engagement Configuration

This skill defines the format of an engagement configuration file and the
validation rules an orchestrator applies when loading it. The schema section
is the **load contract**. The Client Deliverable orchestrator loads and
validates configs against it before spawning any stage. The preparation stage
checks each config against it again. The procedure that captures graph
baselines reuses its field vocabulary. Field names defined here are canonical.
Downstream consumers must use them verbatim.

There is no executable validator. The loading orchestrator validates configs
by following the rules in this skill.

## Config Location Convention

The config is a single YAML file. By convention, the config uses the name
`engagement.yaml` and lives at the root of the engagement's working
directory. Any path still works. The user authors the file and points the
orchestrator at it. The orchestrator never scans the filesystem for a config
that no caller referenced. It never gathers configuration
interactively.

## Bootstrapping a New Config

The canonical starting config is `engagement-template.yaml`, beside this
file. It contains a commented fill-in-the-blank version of the schema below.
The Client Deliverable orchestrator copies it into a new workspace as
`engagement.yaml`. It gives the user that copy's path. The user authors the
config from that copy, not through an interview. Keep the template in step
with the schema. The template leaves every required field uncommented. It
comments out every optional field.

A copy that still contains the literal `FILL ME` is **unfilled, not invalid**.
The config has not been authored yet. Do not run the Validation Rules against
it. Do not emit their errors. State plainly which file is waiting and which
lines still read `FILL ME`.

## Schema

Top-level fields:

| Field | Required | Meaning |
|-------|----------|---------|
| `sow_document` | yes | The SOW/contract for the engagement: a single path, **or** a list of paths in priority order |
| `deliverables_spec` | yes | Path to the deliverables-specification document |
| `pairs` | yes | List of comparison pairs; **any number, one or more** — the schema imposes no upper bound and no expected count |

### Multi-document SOWs

An engagement may have a contract that spans a base SOW, updates, and
amendments. List all documents under `sow_document`, **lowest priority
first**. Each entry supersedes every earlier entry wherever they conflict. A
single path is shorthand for a one-entry list. Consumers treat both forms
identically. Consumers never assume a single document.

The workflow never merges, rewrites, or combines documents into a master copy.
The list *is* the resolution order. A consumer citing a SOW obligation cites
the specific document it came from. The consumer reports the winning one when
two documents cover the same obligation. This ordering is the only conflict
rule. There is no per-clause negotiation.

`sow_document` and `deliverables_spec` are engagement-confidential. Their
contents must never be copied into generated outputs, reports, or committed
artifacts. Only the paths appear in the config.

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

`code_delta_path` and `infra_delta_path` are independent. Supplying one does
not imply the other. Supplying neither is the normal case. Both dimensions
are scanned fresh on both sides.

Exactly one side is `original`, and exactly one side is `upgraded`. The role
comes from the key under which each side appears. A pair with both keys
therefore has both roles. A pair missing either key is invalid.

Side fields by pair type:

- **`type: repo`** — `original` and `upgraded` each contain `path`: the
  local path to that side's repository.
- **`type: branch`** — the pair contains `repo_path`, and `original` and
  `upgraded` each contain `branch`: the branch name for that side.

Either side may also carry `code_audit_path` and `infra_audit_path`. Each path
names a **directory** holding that side's completed audit for one dimension.
These paths let an engagement reuse existing audits instead of scanning
again. A dimension counts as supplied only when **both** sides declare it. One
side alone is a validation error because a comparison needs two sides.
The orchestrator does not scan a supplied dimension on either side. See the
`engagement-pair-loop` skill for what the loop does with it.

`code_audit_path`/`infra_audit_path` (per-side audit directories) and
`code_delta_path`/`infra_delta_path` (a pair-level delta file, below)
independently supply a dimension. Both forms may be present. The audits are
the per-side evidence. The delta is the comparison. Supplying either form
skips that dimension's scans.

Every supplied path may point anywhere on disk, including inside a repository
or another engagement's output. The loop copies each supplied document into
the engagement's `pairs/` tree. The loop works from that copy. It never
modifies or writes back the original.

Either side may also carry `manual_qa_paths`. The field lists paths relative
to that side's repository root. The paths name that repository's manual QA
document(s). It **overrides** the default manual-QA gate target
(`docs/QA_USER.md`) for that side. A repository whose manual QA lives in
`docs/QA_MICK.md` declares it here. The gate never asks that repository for
`QA_USER.md`. If the field is absent, the default applies. This overrides only
the manual QA document. The automated runbook is always
`docs/QA_AUTOMATED.md`.

### Paths

Paths may be absolute or relative. Relative paths resolve against the
directory containing the config file. This applies to every path field:
`sow_document` (each entry), `deliverables_spec`, `path`, `repo_path`,
`code_delta_path`, `infra_delta_path`, `code_audit_path`, and
`infra_audit_path`. The exception is `manual_qa_paths`, whose entries
resolve against **their own side's repository root**, not the config.

### Annotated example

The example below shows N=2 only for illustration. A config may declare any
number of pairs. The pair count is unbounded and never assumed.

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
(fail fast). Nothing is prepared against a partially valid config. Every
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
repository — are **not** config validation failures. The preparation stage
regenerates them after the config validates.
Validation covers only the config's own declarations (paths, branches,
roles, structure).
