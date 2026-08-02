---
name: guard-integrity
description: Verify that a test or guard asserting on file content — documentation, config, generated output, prose contracts — can actually fail. Covers inert assertions, mutation and negation sweeps, untracked-file blind spots, exemption drift, and derived-vs-enumerated coverage. Use when writing or reviewing a test that pins text rather than behavior, adding a repo sweep or tripwire, or auditing whether an existing guard proves anything.
license: MIT
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->

# Guard Integrity

A guard that asserts on file *content* fails silently in a way a behavior test does not: it stays green whether or not the thing it protects is present. Behavior tests break when the code breaks. Content guards break only when the *text* moves — and text moves for reasons unrelated to the obligation being enforced.

One question: **can this guard fail, for the right reason?** Answer it by making it fail, not by reading it.

## Prove it can fail

Never trust a passing content guard you have not seen red. Before accepting one:

1. Delete or negate the thing it protects.
2. Confirm the guard goes red.
3. Confirm the failure message names the actual obligation, not an incidental string.
4. Restore, confirm green.

A guard that stays green at step 2 gates nothing, regardless of how the assertion reads.

## Four ways a content guard goes inert

- **The literal recurs.** A string asserted anywhere in a document is unconditionally true wherever else it appears. Anchor on a full sentence, scoped to the section that carries the obligation.
- **A reflow splits the match.** A regex spanning words breaks when the document is rewrapped, and stops matching content that is still present. Normalize whitespace before matching.
- **A pre-existing statement satisfies it.** A guard on a newly added path can be satisfied by a general statement elsewhere that predates the change. Check which change introduced the line the guard pins.
- **It keys on the corrected value.** A guard matching `41 widgets` cannot catch a stale `43` restated elsewhere. Match the claim's *shape*, and assert at least one match was found.

## Mutation sweeps must negate, not perturb

A sweep that only breaks the phrase each guard intends to pin will systematically miss inert guards — it perturbs the text the guard already watches. It must **negate load-bearing sentences**: inverting an imperative models the regression that actually matters.

Treat "N/N killed, zero inert" as unverified until a negation sweep reproduces it.

Related: guards that assert the *choice* a contract records, while none assert the *mechanism*, leave the code doing the work deletable with the suite green. Per acceptance criterion, delete the line that performs the work and confirm something fails.

## Bracket destructive helpers from both sides

A helper that deletes files needs two tests: one that fails if the guard is removed, and one that fails if the guard is tightened until it matches nothing. "Deletes zero files on a clean tree" is satisfied by a guard that gates nothing at all.

## Git tracks files, not directories

A `git ls-files` sweep cannot see an untracked file. A new test module violating the sweep is green for its entire authoring life and turns red at `git add` — so never accept a count measured before the feature's own files were committed.

Empty-directory residue is invisible to `git status` for the same reason. Find it with `find . -type d -empty`.

## Exemptions are almost always the wrong fix

When a sweep goes red because a new file legitimately contains the swept token, remove the token by importing the canonical definition. Do not add an exemption — exemption lists grow monotonically and are never audited.

Verify any factual claim used to justify an exemption, skip, or non-goal ("this directory does not exist") against the tree. A non-goal justified by "already absent" leaves work unowned rather than deferred. Narrowing an exemption is cheap, and the passing sweep proves the narrowing was safe.

When deriving a guard's values from an upstream list, add a vacuity assert — an empty upstream silently neuters the guard.

## Close enumeration gaps by derivation

A hand-maintained enumeration drops the member that breaks the naming convention, invisibly. Two surfaces built from the same mental roster inherit the same gap: correlation is not corroboration. Derive the set from disk and assert exact equality.

For a migration ledger, that shape is the safe one. On completion, freeze the set empty and invert the assertion rather than deleting the guard.

## Address a tripwire to the pass that will trip it

A deliberately-failing tripwire must be aimed at the work that will actually reach it. If downstream work renames the exempted paths, the exemption stops matching and the tripwire fires early — turning a clean hand-off into a red baseline, which trains implementers to ignore red.

## Evidence-shaped claims are not evidence

"Mutation-tested", "stable across N runs", a named counter — re-run each cited proof on a clean tree at the reviewed commit. A mutation test must fail for the *stated* reason and pass once the change under test is reverted.

Watch for suite claims whose arithmetic reconciles to *collected* rather than *passed*.
