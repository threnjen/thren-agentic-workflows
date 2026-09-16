---
name: guard-integrity
description: Verify that a test or guard asserting on file content — documentation, config, generated output, prose contracts — can actually fail. Covers inert assertions, mutation and negation sweeps, untracked-file blind spots, exemption drift, and derived-vs-enumerated coverage. Use when writing or reviewing a test that pins text rather than behavior, adding a repo sweep or tripwire, or auditing whether an existing guard proves anything.
license: MIT
---

# Guard Integrity

**When this applies.** A content guard is legitimate only when the repository delivers the text itself — a prose corpus, an agent-definition set, or a generated-output contract. In a code repository, `docs/`, `dev/`, and Markdown are not test targets. See the `test-target-scope` instruction. This skill hardens guards that already have a place. It does not license new ones.

A guard that asserts on file *content* fails silently in a way a behavior test does not. It stays green whether or not the protected content is present. Behavior tests break when the code breaks. Content guards break only when the *text* moves. Text can move for reasons unrelated to the obligation being enforced.

One question: **can this guard fail, for the right reason?** Answer it by making it fail, not by reading it.

## Prove it can fail

Never trust a passing content guard until you have seen it turn red. Before accepting one:

1. Delete or negate the thing it protects.
2. Confirm that the guard turns red.
3. Confirm the failure message names the actual obligation, not an incidental string.
4. Restore the protected content. Confirm that the guard turns green.

A guard that stays green at step 2 gates nothing, regardless of how the assertion reads.

## Four ways a content guard goes inert

- **The literal recurs.** A repeated string can satisfy an assertion at the wrong location. Match a full sentence within the section that carries the obligation.
- **A reflow splits the match.** A regex spanning words breaks when the document is rewrapped and stops matching content that remains present. Normalize whitespace before matching.
- **A pre-existing statement satisfies it.** A general statement that predates the change can satisfy a guard for a newly added path. Check which change introduced the line the guard pins.
- **It keys on the corrected value.** A guard matching `41 widgets` cannot catch a stale `43` restated elsewhere. Match the claim's *form* and assert that at least one match was found.

## Mutation sweeps must negate, not perturb

A sweep that only breaks the phrase each guard intends to pin will systematically miss inert guards. It perturbs the text the guard already watches. It must **negate load-bearing sentences**. Inverting an imperative models the regression that matters.

Treat "N/N killed, zero inert" as unverified until a negation sweep reproduces it.

Also, a guard may assert the *choice* a contract records while no guard asserts the *mechanism*. This leaves the code that performs the work deletable with the suite green. For each acceptance criterion, delete the line that performs the work and confirm that something fails.

## Bracket destructive helpers from both sides

A helper that deletes files needs two tests. One must fail if the guard is removed. The other must fail if the guard is tightened until it matches nothing. "Deletes zero files on a clean tree" is satisfied by a guard that gates nothing at all.

## Git tracks files, not directories

A `git ls-files` sweep cannot see an untracked file. A new test module that violates the sweep stays green throughout authoring and turns red at `git add`. Never accept a count measured before the feature's own files were committed.

Empty-directory residue is invisible to `git status` for the same reason. Find it with `find . -type d -empty`.

## Exemptions are almost always the wrong fix

When a sweep turns red because a new file legitimately contains the swept token, remove the token by importing the canonical definition. Do not add an exemption. Exemption lists grow monotonically, meaning they only grow, and are never audited.

Verify every factual claim used to justify an exemption, skip, or non-goal ("this directory does not exist") against the tree. A non-goal justified by "already absent" leaves the work unowned instead of deferred. Narrowing an exemption is cheap. The passing sweep proves that narrowing was safe.

When deriving guard values from an upstream list, add an assertion that fails when the list is empty. An empty upstream list silently neuters the guard.

## Close enumeration gaps by derivation

A hand-maintained enumeration silently drops the member that breaks the naming convention. Two surfaces built from the same mental roster inherit the same gap. Agreement between them is not independent evidence. Derive the set from disk and assert exact equality.

For a migration ledger, use this pattern. On completion, freeze the set at empty and invert the assertion. Do not delete the guard.

## Address a tripwire to the pass that will trip it

A deliberately failing tripwire must target the work that will reach it. If downstream work renames the exempted paths, the exemption stops matching and the tripwire fires early. This turns a clean hand-off into a red baseline. It trains implementers to ignore red.

## Evidence-shaped claims are not evidence

Claims such as "Mutation-tested", "stable across N runs", and a named counter are not evidence by themselves. Re-run each cited proof on a clean tree at the reviewed commit. A mutation test must fail for the *stated* reason and pass after you revert the change under test.

Watch for suite claims whose arithmetic reconciles to *collected* rather than *passed*.
