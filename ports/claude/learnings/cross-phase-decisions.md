<!-- Generated from source_of_truth/skills. Do not edit manually. -->
# Cross-Phase Decisions

Durable decisions and lessons that outlive any single phase. Phase-by-phase history lives in `docs/phases/`; this file keeps only what still governs future work.

## Roadmap and Identifiers

- **A phase number is a public identifier — changing what it denotes is a breaking change to every document that cites it, and nothing warns you.** Grep for the number before re-pointing one, and expect the referents to be in the columns you were not editing. Read the roadmap's dependency column for execution order, never the number.
- **Agent numbers are pipeline positions, not phase numbers.** They must not be "corrected" to match phase numbering.
- **When a rescope has no clean home, check whether the originating phase is the home.** Reopening a phase's scope is cheaper than renumbering around it.
- **A superseded decision recorded as resolved does not update itself when later work reverses it.** Treat any decision entry as time-stamped intent, not a live contract — check the phase's own summary and its Implementation Verification section for what actually shipped before trusting an earlier note.

## Release Verification

- **"Remediated in code" is not "verified".** A fix without a re-run gate is not a release verdict. Status lines move only on fresh final-state evidence.
- **A fixed budget must never be relaxed to make a gate pass.** If a budget is genuinely unachievable, the honest outcome is an explicit user-approved AC change, not a quietly edited threshold. Any AC reshape must carry proof that a deliberately broken implementation still fails the new gate — a reshape that cannot fail a real regression is a deletion wearing a disguise.
- **Every finding classification must name the revision it examined.** "Remediated in code is not verified" cuts both ways: an ungated finding is not a current finding. Any evidence artifact that does not name its revision cannot be reconciled against later work, and a release dossier must verify each artifact post-dates the code it covers.
- **When the honest fix requires capability a phase has excluded, record the finding open with routing — do not redefine the finding to fit the scope.** Tightening prose to make a record say "closed" closes nothing.
- **"The rebuild will bring the validator" is a prediction, not a plan.** A finding routed to a future rebuild must name the capability the rebuild has to gain; otherwise the rebuild lands without it and the finding reads as overdue rather than correctly deferred.
- **Fixes made outside the pipeline still need phase records.** Ad-hoc debugging changes that alter shipped behavior must be reconciled into a phase record.
- **A required-evidence run whose prerequisites cannot exist yet must be deferred with a named owner, never executed early to produce an artifact.** A run whose required evaluators are recorded `not-run` is below-GO evidence, not a passing run.

## Open Items

- **PR posting (`gh` comment path) has never had live QA.** Every guard on it is a static assertion that the body *declares* the contract. The property most needing live confirmation is the "never post" setting, whose entire content is a negative — silently degrading to "posted anyway" publishes a verdict no revert can retract. Verify in a scratch repo, never against this one.
- **The readiness verdict is advisory.** `05 PR - Review` records no verdict in any document and nothing blocks a merge on `NO-GO`. Making it binding needs a hook, owned by a future hook-owning phase. Do not mistake "the reviewer said NO-GO" for "the NO-GO stopped something".
- **Readiness-path trust boundary (P5-SEC-02) is open.** Report validation is metadata-only; validating *claims* needs a strict schema and deterministic reducer, which requires code the PR Review path (agent Markdown) does not have. `05g-readiness-synthesizer` names the gap in its own body rather than papering over it in prose.
- **Per-agent command scoping is not expressible on Claude** (`tools:` takes bare tool names only; `Bash(gh:*)` is an unresolved tool name and the subagent fails to launch), is native only on OpenCode (`permission.bash` globs, last-match-wins), and does not exist per-profile on Codex. Removal is the only narrowing all three targets can express — `execute` is granted only where a named command has no non-shell equivalent.
- **Phase-01 feature 13 owns a deferred reconciliation bundle.** Adding `06-engagement-prepare` (feature 11) left three intentional gaps for the runbook feature: the hardcoded generated-file counts in `tests/test_propagate_master_assets.py` marker-guard (opencode/agents and codex/agents 42→43), the CODEBASE_CONTEXT hidden-subagent claim (23 vs disk), and the missing catalog entry for the agent in `source_of_truth/agents/README.md`. Feature 11's review must not fix these; feature 13's review must verify all three landed.
- **Pilot-validation run removed as a project deliverable (user direction, 2026-07-22, during Phase 02 refinement).** The runtime-verification obligations formerly owned by Phase-01 feature 13's pilot run — confirming the graph-build and baseline-snapshot ACs in `06-engagement-prepare`, and resolving the [PROPOSED] analysis-branch and snapshot-filename markers — are no longer gates for any downstream phase. Those ACs remain statically-verified-only until some engagement run happens to exercise them; Phase 02's entry condition is a run-time check that analysis branches and graphs exist for the sides being compared, nothing more.
- **Roadmap consolidated to two phases (user direction, 2026-07-22).** Former Phases 02–06 (comparative audits, narrative/spec docs, operational docs, compliance proof, assembly/self-review) are collapsed into a single Phase 02: one slim engagement orchestrator owning the per-pair loop, with all work in subagents returning compact summaries plus pointers. `engagement-prepare` is spawned unchanged as the orchestrator's first step — it is not modified; the value-story `mode` field extends the engagement-configuration skill instead. Any document citing Phases 03–06 refers to work now inside Phase 02's feature bundles.
- **Phase 02 deliverable-set restructure (user direction, 2026-07-22 refinement pass).** The delta document *is* the findings report — no separate "findings report" exists. The standalone out-of-scope register is dropped: SOW-excluded security findings live in the security narrative's out-of-scope section; all other excluded findings live in the delta document's "out of scope under the SOW" section. Branded PDF assembly and the branding template are removed from the project — the user assembles PDFs in Claude Design from a schema-defined two-section (client-facing / technical) package manifest that doubles as a table of contents with present/missing detection. Operational/publishing docs moved out of the orchestrator into a standalone Phase 03 agent. New pricing-researcher subagent (sole internet-touching engagement agent; generic pricing queries only, no engagement content) backs a per-pair cloud/cost analysis with cited, dated figures. The orchestrator keeps an on-disk working-state file (inputs, statuses, pointers) serving as its run record.
- **Documentation count claims drift.** README / CODEBASE_CONTEXT agent, skill, and orchestrator counts have repeatedly disagreed with disk, and in one case two surfaces held two live *definitions* of "orchestrator". Recounting cannot fix a definition conflict — reconcile the definition first, then guard the count by claim-shape (see `_assert_every_count_claim`-style derivation tests).

## Review Contracts

These are scope-independent — they are about not reporting an absence of evidence as evidence of absence.

- Missing or incomplete required checks are a hard readiness gate: the canonical verdict is `NO-GO`. An unverified verdict must not update roadmap or summary status lines. Verdicts are issued by the user by hand; no agent writes a status line.
- A failed, hung, or unavailable evaluator never becomes a passing result, and a later evaluator's success never repairs an earlier one's failure. Every such case gets a record naming the evaluator, the check, and a concrete reason, and the readiness report must enumerate them by name.
- Report validation is metadata-only at the orchestrator (readable, regular, non-empty, under the run's report root) and must not be mistaken for validating a report's *claims*.
- Diff-scoped evaluators that call repo-wide analysis must require verifiable added-line attribution; touched-file filtering alone is insufficient.
- Read-only dependency vulnerability checks must use supplied local evidence or an explicitly offline audit mode; network-capable commands are treated as unavailable.
- Fixture dry-runs remain required release evidence for agent wiring and degradation behavior. Static contract review cannot observe runtime report creation.
- **Never restore unrestricted shell/Bash permissions to satisfy an evaluator acceptance criterion.** The correct move is a narrowly scoped capability — an offline audit mode, a verifiable evidence bundle from the orchestrator, a command allowlist — never a broad grant with a comment explaining why it is fine.

## Evaluator Grants

- **The mechanical sweep evaluators hold no shell grant** (`[read, search, edit]` only). The removal bar — name a command with no non-shell equivalent, or the grant goes — could not be met for any of them.
- **`05a-baseline-worktree` holds the one unclosable `execute` (`git worktree`) and returns a path; every other evaluator reads two trees.** The baseline worktree *is* the non-shell equivalent of `git diff` for this family. Any future proposal to grant shell to an evaluator must first explain why reading `05a`'s worktree is insufficient.
- **The offline dependency audit is a capability boundary, not a policy.** Vulnerability evidence comes only from artifacts supplied to the run; their absence is `NOT RUN`, never a pass. Do not reintroduce a grant to restore a scanner; supply the artifact instead. The same applies to coverage measurement: no agent in the test-health chain holds `execute`, so a measured coverage delta exists only when the orchestrator supplies coverage evidence for both revisions — otherwise the honest report is "not-measurable" plus the structural suite delta.
- **MCP tools are not declared in agent frontmatter**, so `tools:` lists neither grant nor withhold graph access. Graph unavailability means `NOT RUN` with a reason and a verdict-ceiling drop, never a silent downgrade to grep.
- **A forcing function is only real if the feature is actually blocked without the capability.** Check that the blockage exists — including whether the target format can even express the fix — before promoting a capability gap to a deliverable.

## Git Base Derivation

- **Git cannot determine a branch's base. This is a data-model fact, not a tooling gap.** A ref is a SHA and nothing else. `git merge-base HEAD main` requires already knowing the base (circular); the reflog records only SHAs, is local-only, and gc-pruned; `origin/HEAD` yields the repo's *default* branch, not this branch's base, and is frequently unset. The chosen design is **suggest-and-confirm**: infer a candidate (`origin/HEAD` → `origin/main` → `origin/master` → present candidates), compute `merge-base`, show the implied diff scope, let the user accept or override. Cases where inference is actively wrong: a branch cut from another feature branch, a rebased branch, a squash-merged base.
- **A branch is always its own nearest merge-base, and so is its remote-tracking ref.** Any ranking over candidate base branches must filter both before comparing.

## Propagation Contracts

- The generated roots are `claude/`, `opencode/`, and `codex/`; `.claude/skills/` and `.claude/agents/` are not generated destinations. Future plans must name the actual roots or explicitly add an adapter.
- `$source` metadata is guaranteed for propagated hook JSON entries only, not for generated skill or agent files.
- **All generated Markdown roots carry a generated marker, and the propagator prunes orphans gated on that marker.** Generated skill files are therefore not byte-identical to source — they differ by exactly the marker line. A file orphaned before the marker existed is permanently unprunable (accepted: fails closed). Any asset rename must land while the propagator is marker-aware.
- **A `--watch` propagator holding stale code is a silent-failure hazard** — restart the watcher after any propagator change before trusting a run.
- **Propagation is not idempotent across an agent reclassification or rename: run until every change counter is zero.** Identifier resolution reads on-disk stems and pruning runs after emission, so one run can leave a valid-looking but non-converged tree. "I ran the propagator" is not evidence of convergence. Pinned by `test_committed_tree_is_at_a_propagation_fixed_point`.
- **Deleting an orchestrator can change the public name of an agent it merely referenced.** A dual-use agent (user-invocable *and* some orchestrator's declared child) gets both a slash command and a subagent file; deleting its last parent reclassifies it and can rename the user-facing command. Before retiring any agent, check what its `agents:` roster is the last declarer of.
- **The propagator resolves `agents:` roster references by display name, not slug.** Any change to reference resolution must preserve display-name matching or re-verify every forward reference.
- **Codex `max_depth` is an operator prerequisite no repository artifact can enforce.** With the default of 1, a depth-2 spawn is blocked and the model silently does the work inline, indistinguishable from real delegation. Any AC of the form "agent X demonstrably delegates to Y" is unverifiable by static test and must route to a runtime transcript.

## Enumeration and Guard Lessons

- **Close enumeration gaps by derivation, not by listing.** A hand-maintained enumeration of a set will drop the member that does not match the set's naming convention, and the drop is invisible because the remainder looks complete. Two surfaces built from the same mental roster inherit the same gap — correlation between them is not corroboration. Derive expectations from disk so omission fails by construction.
- **A blast-radius claim is a factual claim and needs the same evidence as any other.** A claim restated by several features without re-derivation looks better attested while adding no evidence; corroboration is not evidence when every corroborator quotes the same source. A cheap grep settles it.
- **A Non-Goal justified by a factual claim inherits nothing when the claim is wrong.** A deferral names an owner; a dismissal does not, and only one of them survives being mistaken. Verify "does not exist" claims against the tree.
- **A migration ledger derived from disk and asserted by exact equality is the safe shape** — removing an entry is reconciliation, not exemption, and a regressing item re-enters the set and fails. On completion, freeze the set empty and invert the assertion rather than deleting the guard: emptying the set is the migration; the inverted assertion is what stops the next change quietly regressing.
- **Inert guards are a recurring phase-level defect, not a per-feature lapse.** Guards that assert on prose are inert by default because prose restates its own vocabulary. Treat any "zero inert" claim as unverified until a sweep that *negates load-bearing sentences* — not merely damages the named phrase — reproduces it. (Full treatment in `review-learnings.md`.)
- **A question asked after the work is on disk blocks nothing.** One upfront interaction (all blocking questions asked before the run) is a design outcome that erodes one reasonable-seeming question at a time — guard it. "Ask me once the report is written" is both unattended and safe because the user sees content before it is published.
- **If a rescope only relocates work, suspect the new scope is the old scope wearing a hat.** A good rescope deletes work.

## Runtime Deployment Contract

- Runtime deployment uses one ordered path: repository convergence, destination preflight, classified inventory, immediate inventory recheck, managed-copy deployment, owned reconciliation, and regular-copy verification.
- Human review is bound to the exact home-relative inventory and generated-source fingerprints by SHA-256. A missing digest returns `review_required`; a changed digest returns `inventory_drift`; neither state permits a runtime write.
- Scratch-home automation is not live-platform evidence. macOS, Linux, native Windows, and WSL retain separate evidence rows, and any `NOT RUN` row caps the full cross-platform verdict below GO.

## Harness Hook Support (verified from primary sources 2026-07-17)

All three harnesses support user-global hooks. Claude Code: `~/.claude/settings.json`. OpenCode: global config/plugin dir. Codex: `~/.codex/hooks.json` / `[hooks]` in `~/.codex/config.toml`, additive merge with repo layers. Codex caveats: per-hook hash-based trust (regeneration requires re-trust via `/hooks`, so upgrades are non-silent), only "simple" `unified_exec` shell calls intercepted, `codex exec` repo-hook dispatch bug (#26383/#26452), minimum version ~v0.123, enterprise `allow_managed_hooks_only` can suppress everything. Research report: `dev/research/codex-hooks-mechanism/`.
