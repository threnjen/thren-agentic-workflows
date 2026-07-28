# Cross-Phase Decisions

Seed file. Agents append project-specific deferred work, known gaps, and design decisions here; `02 Phase Refiner` reads it to decide what to pull into scope. Entries below are the durable, project-independent ones — keep new entries in the same shape (one bolded claim, one or two sentences of consequence) and delete any that stop being true.

## Identifiers and scope

- **A phase number is a public identifier — changing what it denotes breaks every document citing it, and nothing warns you.** Grep for the number before re-pointing one. Read the dependency column for execution order, never the number.
- **Agent numbers are pipeline positions, not phase numbers.** Do not "correct" them to match.
- **A decision recorded as resolved does not update itself when later work reverses it.** Treat every entry as time-stamped intent; check what actually shipped before trusting it.
- **If a rescope only relocates work, suspect the new scope is the old scope wearing a hat.** A good rescope deletes work.

## Verification and verdicts

- **"Remediated in code" is not "verified."** A fix without a re-run gate is not a verdict; status lines move only on fresh final-state evidence. Verdicts are issued by the user — no agent writes a status line.
- **Every finding must name the revision it examined.** An artifact that does not name its revision cannot be reconciled later, and a release dossier must confirm each artifact post-dates the code it covers.
- **Missing or incomplete required checks are a hard gate: the verdict is `NO-GO`.** A failed, hung, or unavailable evaluator never becomes a passing result, and a later success never repairs an earlier failure. Enumerate every such case by name with a concrete reason.
- **A fixed budget is never relaxed to make a gate pass.** If it is genuinely unachievable the honest outcome is a user-approved AC change carrying proof that a deliberately broken implementation still fails the new gate.
- **When the honest fix needs capability the scope excludes, record the finding open with routing.** Redefining the finding to fit the scope closes nothing, and "a future rebuild will handle it" is a prediction unless it names the capability that rebuild must gain.
- **Report validation is metadata-only** (readable, regular, non-empty, under the run's report root). Do not mistake it for validating a report's *claims*.

## Capability grants

- **A capability boundary is not a policy.** Where evidence can only come from artifacts supplied to the run, their absence is `NOT RUN`, never a pass — supply the artifact, do not restore the grant. Never widen shell permissions to satisfy an acceptance criterion.
- **The decisive evidence that a grant is required is a sibling with the same job operating without it**, not the strength of the justification. The capability is usually already supplied as an artifact by one privileged component.
- **MCP tools are not declared in agent frontmatter**, so `tools:` neither grants nor withholds graph access. Graph unavailability is `NOT RUN` with a verdict-ceiling drop, never a silent downgrade to grep.

## Git base derivation

- **Git cannot determine a branch's base — a data-model fact, not a tooling gap.** `git merge-base HEAD main` requires already knowing the base; the reflog is SHA-only, local, and gc-pruned; `origin/HEAD` gives the repo default, not this branch's base. Use suggest-and-confirm: infer a candidate, compute `merge-base`, show the implied diff scope, let the user override. Inference is actively wrong for branches cut from another feature branch, rebased branches, and squash-merged bases.
- **A branch is always its own nearest merge-base, and so is its remote-tracking ref.** Filter both before ranking candidates.
