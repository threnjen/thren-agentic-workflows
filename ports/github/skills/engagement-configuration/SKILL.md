---
name: engagement-configuration
description: "Schema and validation rules for an engagement configuration file — the declaration of an engagement's comparison pairs, SOW/contract pointer, and deliverables-spec pointer. Use when: loading or validating an engagement config, authoring one for a new engagement, or referencing the canonical field vocabulary for preparation orchestration and baseline capture."
---

# Engagement Configuration

This skill defines the format of an engagement configuration file and the
validation rules an orchestrator applies when loading it. The schema section
below is the **load contract**: the preparation orchestrator loads and
validates configs against it, and the graph baseline capture procedure reuses
its field vocabulary. Field names defined here are canonical — downstream
consumers must use them verbatim.

There is no executable validator; validation is behavior the loading
orchestrator performs by following the rules in this skill.

## Config Location Convention

The config is a single YAML file whose path is **supplied by the user** when
an engagement workflow is invoked. By convention it is named
`engagement.yaml` and lives at the root of the engagement's working
directory, but the orchestrator must accept any user-supplied path and must
not search for a config the user did not point at.

Decision record: a user-supplied path was chosen over a fixed discovery
location because engagements live outside this repository and their layout
is not ours to dictate; the filename convention is advisory only.

## Schema

Top-level fields:

| Field | Required | Meaning |
|-------|----------|---------|
| `sow_document` | yes | Path to the SOW/contract document for the engagement |
| `deliverables_spec` | yes | Path to the deliverables-specification document |
| `pairs` | yes | List of comparison pairs; **any number, one or more** — the schema imposes no upper bound and no expected count |

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

Exactly one side is `original` and exactly one side is `upgraded` — the role
is expressed by which key the side sits under, so a pair with both roles
present has them by construction; a pair missing either key is invalid.

Side fields by pair type:

- **`type: repo`** — `original` and `upgraded` each contain `path`: the
  local path to that side's repository.
- **`type: branch`** — the pair contains `repo_path`, and `original` and
  `upgraded` each contain `branch`: the branch name for that side.

### Paths

Paths may be absolute or relative. Relative paths resolve against the
directory containing the config file. This applies to `sow_document`,
`deliverables_spec`, `path`, and `repo_path`.

### Annotated example

The example below shows N=2 purely for illustration — a config may declare
any number of pairs; the pair count is unbounded and never assumed.

```yaml
sow_document: docs/sow.pdf            # relative to this file's directory
deliverables_spec: docs/deliverables.md

pairs:
  - name: service-api                 # a repo pair: two separate repositories
    type: repo
    original:
      path: repos/service-api-legacy
    upgraded:
      path: /abs/path/service-api-v2  # absolute paths are also accepted

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
| `sow_document` present and path resolves | `sow_document: path '<value>' does not resolve (expected an existing file)` |
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

Explicitly allowed (do not over-validate):

- The **same repository may appear in more than one pair** — a repo
  participating in multiple comparisons is valid.

## Not Validation Failures

Missing or stale supporting artifacts are **not** config validation
failures. In particular: missing or out-of-date documentation for a declared
repository, and missing or stale code graphs, do not fail validation. They
are **prepare-or-verify work** for the preparation orchestrator, which
builds or refreshes them after the config validates. Validation covers only
the config's own declarations (paths, branches, roles, structure).
