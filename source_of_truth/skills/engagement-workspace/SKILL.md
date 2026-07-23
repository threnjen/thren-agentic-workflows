---
name: engagement-workspace
description: "Layout contract for an engagement's output workspace — the single per-engagement root outside every client repository where all engagement outputs land (client-facing docs, internal artifacts, raw reports, manifest, working-state file) — plus the working-state file shape. Use when: writing or locating any engagement output, maintaining or resuming from the working-state file, or resolving manifest paths."
---

# Engagement Workspace

One workspace root per engagement holds **every** engagement output. This
layout is the contract downstream engagement features reference — they use
these paths, they do not restate them.

## Root

By convention the root is `engagement-workspace/`, a sibling of the
engagement config file (i.e., at the root of the engagement's working
directory). Any location works provided it is **outside every client
repository**. No agent writes deliverables into a client repo; every
manifest path must resolve inside this root.

## Layout

```
engagement-workspace/
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
outputs sit directly in `pairs/<pair-name>/`. Whether a given artifact is
client-facing (`deliverables/`), internal (`internal/`), or raw (`raw/`) is
decided by the stage that produces it.

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
