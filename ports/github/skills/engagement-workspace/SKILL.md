---
name: engagement-workspace
description: "Layout contract for an engagement's output workspace — the single per-engagement root outside every client repository where all engagement outputs land (client-facing docs, internal artifacts, raw reports, manifest, working-state file) — plus the working-state file shape. Use when: writing or locating any engagement output, maintaining or resuming from the working-state file, or resolving manifest paths."
---

# Engagement Workspace

One workspace root per engagement holds **every** engagement output. This
layout is the contract downstream engagement features reference — they use
these paths, they do not restate them.

## Root

The standard root is `<repo-name>-engagement/`, a **sibling of the client
repository** — e.g., analyzing `ssx-surface-capture` puts every output in
`ssx-surface-capture-engagement/` next to it. `<repo-name>` is the upgraded
side's repository directory name (branch pairs: the `repo_path` directory
name); a multi-pair engagement uses the first pair's upgraded repository and
still gets exactly one root. A user-specified root overrides the standard,
but it must always be **outside every client repository**. No agent writes
deliverables into a client repo; every manifest path must resolve inside
this root.

## Layout

```
<repo-name>-engagement/
  engagement-state.md          # working-state file (shape below)
  manifest.md                  # deliverables manifest (produced by a later stage)
  deliverables/                # client-facing documents
  internal/                    # internal-only artifacts (never client-facing)
  raw/                         # raw subagent reports, unedited
  notes/                       # optional temporary working notes
  pairs/<pair-name>/
    original/                  # per-side outputs for the pair's original side
    upgraded/                  # per-side outputs for the pair's upgraded side
```

Pair folders are named by the config pair `name`. Pair-level (cross-side)
outputs sit directly in `pairs/<pair-name>/`.

## Path Discipline — Deterministic Output

- Every document exists at **exactly one path**: the contract path named by
  the producing stage's definition (client-facing paths are enumerated in
  the `engagement-package-manifest` skill). Never write working copies,
  duplicates, or a document under an alternate name or directory.
- Filenames are **lowercase kebab-case**, exactly as the contract states —
  never UPPER_SNAKE variants, never pair-name prefixes the contract doesn't
  specify.
- Resolve every write as an absolute path against the workspace root you
  were passed — never against the current working directory. A file landing
  outside the workspace root is a defect.
- Audience is fixed by directory: `deliverables/` is client-facing;
  `internal/`, `raw/`, `pairs/`, `notes/`, and the root-level state/manifest
  files are internal. A stage never reclassifies a document by relocating it.

## Audience Banner — Required First Line

Every markdown output opens with exactly one of:

- `> **AUDIENCE: CLIENT DELIVERABLE** — hand off to design for client PDF.`
- `> **AUDIENCE: INTERNAL** — pre-delivery check; never client-facing.`

The banner must agree with the file's directory (client banner only under
`deliverables/`).

## Working-State File

`engagement-state.md` is the orchestrator's context offload, resume-recovery
point, and final run record in one artifact, written as the run progresses.
It contains:

- **Resolved engagement inputs**: config path, repo paths (and branches, for
  branch pairs), SOW document path, deliverables-spec path, pair roster
  (name, type, `mode`).
- **Per-pair/per-side results**: one entry per side of every pair — status
  (e.g., pending / prepared / failed with reason / complete) plus artifact
  pointers (paths only, never content).

Additional temporary working notes are permitted under `notes/` whenever
they reduce held context.
