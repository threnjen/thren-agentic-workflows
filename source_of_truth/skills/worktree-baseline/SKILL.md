---
name: worktree-baseline
description: "Reusable procedure for creating a detached, read-only git worktree at a requested baseline commit and returning its path. Use when: an evaluator or grading workflow needs an isolated local baseline checkout."
---

# Baseline Worktree

Use this procedure whenever a workflow needs to inspect a commit without
changing the caller's checkout. It is intentionally independent of Phase Final
Review and may be reused by evaluation or grading agents.

## Inputs and Defaults

Set these values before running the procedure:

```text
<REPOSITORY_ROOT>  repository containing the commit
<BASELINE_COMMIT>  full or locally resolvable commit reference
<TARGET_PATH>      absolute path for the detached worktree
```

If no target is supplied, use a deterministic temporary path derived from the
repository identity and resolved commit, for example:
`<TEMP_ROOT>/baseline-<REPOSITORY_NAME>-<SHORT_SHA>`. Resolve it to an absolute
path before invoking `git worktree add`.

## Procedure

1. Resolve the repository root and verify that it is a worktree-capable git
   repository:

   ```sh
   git -C "<REPOSITORY_ROOT>" rev-parse --show-toplevel
   ```

2. Verify the baseline commit locally before creating anything:

   ```sh
   git -C "<REPOSITORY_ROOT>" rev-parse --verify "<BASELINE_COMMIT>^{commit}"
   ```

   If this command fails, stop with:
   `Baseline commit '<BASELINE_COMMIT>' is not available locally; fetch or
   provide a locally resolvable commit before retrying.` No network fetch is
   implied by this procedure.

3. Inspect `git -C "<REPOSITORY_ROOT>" worktree list --porcelain` and the target
   path before writing.

4. Apply the **Existing Target-Path Policy** below — it is the only decision
   procedure for this step, including the exact stop messages. For its create
   cases, run:

   ```sh
   # Create only the missing parent, then register the worktree.
   mkdir -p "$(dirname "<TARGET_PATH>")"
   git -C "<REPOSITORY_ROOT>" worktree add --detach "<TARGET_PATH>" "<BASELINE_COMMIT>"
   ```

5. Verify the returned worktree before handing it to the caller:

   ```sh
   git -C "<TARGET_PATH>" rev-parse --verify HEAD
   git -C "<TARGET_PATH>" status --porcelain
   ```

   The resolved `HEAD` must equal the verified baseline commit and the status
   must be clean. Return the absolute `<TARGET_PATH>` only after both checks
   succeed.

## Existing Target-Path Policy

- **No path exists:** create it and mark it `created_by_this_invocation`.
- **Exact registered worktree:** if the target is already registered to the
  same repository at the requested commit and is clean, reuse it and mark it
  `reused_existing_worktree`.
- **Registered worktree at another commit:** inspect its status. If it is dirty,
  stop with `Target worktree '<TARGET_PATH>' is dirty; refusing to recreate it.`
  If it is clean and belongs to the requested repository, remove that
  worktree with `git worktree remove <TARGET_PATH>`, recreate it at the
  requested commit, and mark the new worktree as owned by this invocation.
- **Existing path not registered as this repository's worktree:** stop with
  `Target path '<TARGET_PATH>' exists but is not a registered worktree; refusing
  to overwrite it.`
- **Exact registered worktree with local modifications:** stop with
  `Target worktree '<TARGET_PATH>' is dirty; refusing to reuse it.` A baseline
  must never be inferred from a modified checkout.

This policy prevents accidental deletion of an unrelated directory and makes a
same-repository target deterministic without hiding local modifications.

## Read-Only Etiquette

- Use `--detach`; do not create or switch a branch in the baseline worktree.
- Read files, inspect history, and run explicitly read-only analysis only.
- Do not edit, format, install dependencies into, commit in, or reset the
  baseline worktree.
- Keep reports and temporary files in the caller's report directory, never in
  the baseline worktree.
- If an analysis tool needs a writable directory, create a separate temporary
  location and state that it is outside the baseline checkout.

## Cleanup and Ownership

Track whether this invocation created or recreated the worktree.

- For `created_by_this_invocation`, remove it after the caller finishes:

  ```sh
   git -C "<REPOSITORY_ROOT>" worktree remove "<TARGET_PATH>"
  ```

- For `reused_existing_worktree`, do not remove it automatically; its owner may
  be using it for another read-only task.
- If a caller explicitly asks for cleanup of a worktree it owns, verify it is
  clean and remove it through `git worktree remove`. Use a forced removal only
  for an owned, failed setup whose contents are disposable; never force-remove
  a reused or dirty worktree.
- If setup fails after registration, clean up only the partially created
  worktree owned by this invocation, then report the original failure and the
  cleanup result.

## Failure Contract

Every failure includes the operation, the relevant path or commit, and a
remediation. In particular, distinguish an unavailable local commit, a dirty
target, an unrelated existing path, a checkout mismatch, and a non-clean
baseline. Never return a path that has not passed the final `HEAD` and clean-
status checks.
