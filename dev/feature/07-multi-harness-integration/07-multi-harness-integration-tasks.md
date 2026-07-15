# Feature 07: Multi-Harness Integration — Tasks

## Stage 1: Harness Contract Investigation

- [ ] Confirm `05-injection-scanner`, `05-webfetch-exfiltration-guard`, and `06-injection-pattern-corpus` are implemented, reviewed, and green; read their implementation records and record every finalized runtime file, public API, config/corpus path, benchmark command, and selected harmless smoke fixture. (AC3, AC4, AC7)
- [ ] Replace all plan-time proposed upstream paths and symbols with the finalized implementation contracts in Feature 07 implementation/evidence artifacts; return any missing reusable scanner, normalization, validation, generation, or URL-classifier contract to the owning upstream feature instead of duplicating it. (AC3, AC4)
- [ ] Reconcile current Phase 01 prerequisite evidence for SEC-01 nested destination containment and PERF-01 latency stability before changing propagation; record the authoritative status, reproduction/review evidence, owning scope, and either reviewed resolution or explicit prerequisite risk acceptance. (AC10)
- [ ] Time-box Codex primary-documentation review and direct safe experiments for the current runner version, recording date, version, event name, payload shape, event timing relative to model ingestion, output suppression/replacement/annotation semantics, exit handling, and redacted evidence. (AC1)
- [ ] Time-box OpenCode primary-documentation review and direct safe experiments using the same evidence fields, including whether a plugin can prevent or replace successful tool output before model context and how hook return values/errors are consumed. (AC1)
- [ ] Verify Claude Code's finalized scanner source contract against the Phase 02 discovery evidence and record which behaviors require live confirmation rather than inferring them from unit tests. (AC1, AC3, AC8)
- [ ] Assign Claude Code, Codex, and OpenCode exactly one outcome row each: equivalent block/warn enforcement with evidence, or an evidence-backed platform limitation requiring explicit user sign-off; reject event-name presence, command launch, or warning-only behavior as proof of equivalent suppression. (AC2)
- [ ] Define the explicit sign-off artifact and decision fields `[PROPOSED - name TBD]` for any limitation, ensuring user acceptance is recorded rather than inferred; keep the feature incomplete while a required sign-off is absent. (AC2)
- [ ] Keep Cursor and GitHub Copilot classified Not supported and confirm no investigation result accidentally expands implementation scope to those harnesses. (AC9)

## Stage 2: Harness Adapters and Source Wiring

- [ ] For each capable harness, map its verified payload fields to the finalized upstream scanner input contract and its upstream structured result to the native block/suppress, replace, or warning mechanism; document the mapping without introducing policy. (AC3)
- [ ] Implement the narrowest translation adapter `[PROPOSED - name TBD]` only where the verified contract requires one, calling upstream normalization, validation, rule loading, scanning, strongest-match, truncation, allowlist, and failure behavior rather than reproducing them. (AC3)
- [ ] Revalidate translated result values at the harness emission boundary and fail according to the upstream security posture when payload translation, result validation, or emission fails. (AC3, AC8)
- [ ] Add supported-harness tests for successful built-in, Task/subagent, and MCP outputs as available, covering highest-match selection, high suppression, medium/low warning with intact output, truncation notice, allowlist bypass, and redacted fail-closed behavior. (AC3)
- [ ] Add sentinel assertions proving translated stdout, stderr, native result objects, warnings, and retained evidence never include full output, matched text, decoded candidates, prompt sentinels, URLs, commands, or secrets. (AC3, AC8)
- [ ] Verify adapters contain no production injection phrases, regexes, URL signatures, severity policy, normalization, matching, or audit duplication; record code-review evidence for the shared upstream calls actually used. (AC3)
- [ ] For any harness that cannot call upstream logic because it lacks pre-context interception, add no simulated enforcement adapter; complete only the evidence-backed limitation and explicit sign-off path. (AC2, AC3)
- [ ] Finalize source hook metadata and adapter filenames only after behavioral evidence selects the contract; retain existing source tags and preserve unrelated source definitions. (AC3, AC5)

## Stage 3: Propagation and Generated Outputs

- [ ] Add regression tests that preserve unrelated untagged Claude/Codex entries, remove only stale `$source`-owned entries, preserve user-owned OpenCode plugins, and remove only exact generated-header plugins before changing propagation. (AC5)
- [ ] Extend hook propagation to emit every finalized scanner entrypoint/module, production corpus, allowlist, WebFetch/Bash guard module/config update, supported harness adapter, and source definition into a temporary consumer. (AC4)
- [ ] Verify every generated command and adapter import resolves inside the consumer's emitted hook tree, cannot escape the target root, and does not depend on the source repository, ambient `PYTHONPATH`, pip, `.venv`, or symlinks. (AC4, AC6)
- [ ] Apply the reviewed Phase 01 containment contract to every new copied/generated/removed Phase 02 asset, including intermediate runtime/config/settings/plugin directories and the distribution marker; retain adversarial symlink regressions. (AC4, AC6, AC10)
- [ ] Update the distribution-version contract so any finalized scanner, corpus, allowlist, WebFetch/Bash, adapter, or source-metadata change updates the marker, while an unchanged second propagation remains byte-stable. (AC4, AC5)
- [ ] Generate `.claude/settings.json`, `.codex/hooks.json`, and supported OpenCode plugins from source metadata; assert source tag, matcher/event, timeout, command target, adapter target, and no references to omitted assets. (AC4, AC5)
- [ ] Test stale generated scanner/guard entries and plugins across all three outputs, confirming coherent removal without deleting user/tool-owned PostToolUse or SessionStart wiring. (AC5)
- [ ] Propagate twice over unchanged inputs and once over changed Phase 02 inputs, then assert settings preservation, deterministic cleanup, stable/revised marker behavior, and byte-level idempotence. (AC4, AC5)
- [ ] Detach the temporary consumer from the source checkout and invoke every supported scanner/guard entrypoint using only `python3` and emitted files. (AC4, AC6)
- [ ] Verify the Phase 01 guard denies agent writes to every propagated scanner module, entrypoint, corpus, allowlist, URL-classifier/config, adapter, source definition, generated settings file, and generated plugin while normal read-only inspection remains allowed. (AC6)
- [ ] Verify the configured scanner allowlist still bypasses only approved repository-owned sources and cannot be broadened through a propagated, agent-writable file. (AC6)
- [ ] Run the focused propagation and distribution suites after each wiring change; do not regenerate checked-in outputs until the temporary-consumer gates are green. (AC4–AC6, AC10)

## Stage 4: Combined Smoke and Security Evidence

- [ ] Extend `tests/hooks/test_hook_distribution_integration.py` as the Phase 02 consolidated smoke harness, reusing selected upstream fixtures and public APIs rather than copying corpus patterns or URL signatures. (AC7)
- [ ] In one detached propagated consumer flow, prove a harmless high scanner fixture suppresses output with redacted no-retry/manual-inspection guidance. (AC7)
- [ ] In the same flow, prove a harmless medium/low fixture preserves the original logical output and appends one redacted warning context. (AC7)
- [ ] Prove runner truncation scans available content and appends the unscanned-tail notice without weakening a detected high block. (AC7)
- [ ] Prove approved source allowlisting skips scanner enforcement while an unapproved/missing/outside source does not gain an allowlist bypass. (AC7)
- [ ] Prove WebFetch known-secret-format URLs deny, ambiguous high-entropy URLs ask, and ordinary URLs allow using synthetic sentinels and reserved hosts. (AC7)
- [ ] Prove literal Bash `curl` and `wget` URL operands produce outcomes equivalent to the shared WebFetch classifier while existing protected-file/destructive-command regressions remain green. (AC7)
- [ ] Search stdout, stderr, structured decisions, warnings, audit records, generated outputs, and retained docs/evidence for each synthetic prompt/secret/URL/command sentinel; require every sensitive sentinel absent. (AC8)
- [ ] Measure representative propagated scanner, WebFetch, curl, and wget invocations using the Phase 01 budget approach; record individual and combined timings and preserve the fixed accepted threshold rather than weakening it to accommodate failures. (AC8, AC10)
- [ ] Run the focused integration suites, then the complete pytest suite and combined coverage command after installing only `requirements-dev.txt`; require coverage at or above 50% and distinguish fresh results from historical Phase 01 evidence. (AC4–AC8, AC10)
- [ ] Run `python3 -m unittest discover -s tests -v` and preserve at least the fresh 14-test stdlib compatibility baseline plus any intentionally added stdlib cases. (AC4–AC8)
- [ ] Perform code-review evidence checks for complete artifact propagation, target containment, no policy duplication, deterministic generated ownership, support-status honesty, and absence of unredacted data. (AC2–AC10)
- [ ] In a disposable live Claude Code session, record one real high suppression, one warning pass-through, one no-retry observation, Task/MCP coverage where available, and human-only kill-switch recovery; leave every unexecuted item explicitly `NOT RUN`. (AC3, AC8, AC9)
- [ ] For each supported Codex/OpenCode path, run equivalent disposable live checks; for each limited path, retain the investigation evidence and explicit user sign-off instead of manufacturing a passing check. (AC2, AC3, AC8)

## Stage 5: Operations, Limitations, and Sign-Off

- [ ] Update `docs/hooks/installation.md` with the finalized Phase 02 artifact set, propagation command, generated-output verification, dependency-free consumer contract, current three-harness support matrix, and unchanged Cursor/Copilot Not supported classification. (AC2, AC9)
- [ ] Update `docs/hooks/hook-verification.md` with non-silent checks for source wiring, emitted assets, command/adapter targets, version marker, detached execution, ownership preservation, self-protection, and supported block/warn behavior. (AC4–AC6, AC9)
- [ ] Update `docs/hooks/manual-qa.md` with redacted automated-versus-live evidence, disposable harness setup, Claude block/warn/no-retry steps, supported Codex/OpenCode steps, limitation evidence, explicit sign-off status, and `NOT RUN` labels. (AC2, AC8, AC9)
- [ ] Create or finalize the prompt-injection defense guide `[PROPOSED - name TBD]` covering severity behavior, truncation and allowlist semantics, clean-room corpus/benchmark verification, fail-closed recovery, and the known regex, shell, and failed-output boundaries. (AC9)
- [ ] Document rollback through a reviewed prior source/runtime state followed by re-propagation; verify the procedure in a disposable clone without changing the active development checkout or retaining machine-specific paths. (AC9)
- [ ] Document the human-only override recovery procedure and confirm no environment/process input, generated adapter, or user-owned setting creates an alternate bypass. (AC6, AC9)
- [ ] Record runner versions, evidence dates, redacted observations, support classifications, and explicit user decisions in the finalized support/sign-off artifact; reject incomplete, inferred, or contradictory rows. (AC1, AC2, AC9)
- [ ] Reconcile documentation assertions against the generated files and automated/live evidence so no launcher-only output is described as enforcement and no runner-constrained item is described as passed. (AC2, AC9)
- [ ] Verify `tests/hooks/README.md` against the fresh stdlib and pytest/coverage evidence; if its two-test wording is stale rather than intentionally historical, update it to distinguish the current baseline from historical Phase 01 setup notes. (AC9)
- [ ] Run exact documentation assertions for all five harness names, required support labels, known limitations, installation, verification, recovery, rollback, and sign-off status. (AC2, AC9)
- [ ] Regenerate final checked-in outputs once from the finalized source of truth, inspect the scoped diff for unrelated churn or sensitive evidence, rerun all Stage 4 gates, and record the exact final distribution marker. (AC4–AC9)
- [ ] Confirm AC1–AC10 are each backed by automated tests, runner-constrained evidence, code-review evidence, manual QA, or explicit risk/sign-off evidence as appropriate; keep the feature incomplete if any harness remains in a third/unresolved state. (AC1–AC10)
