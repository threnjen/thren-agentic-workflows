# Injection Corpus Benchmark

## Clean-Room Provenance

The production corpus in `.github/hooks/config/injection-patterns.json` was authored from the Phase 02 taxonomy and feature discovery context. No regex, code, pattern, or fixture from the surveyed repository was opened or copied while implementing this corpus. The configuration records `phase-02-clean-room-taxonomy` as its provenance.

The corpus is deliberately small: seven rules cover instruction override, persona/role-play hijack, encoding/obfuscation, context manipulation, and instruction smuggling. Production reasons are fixed, redacted descriptions and never include matched content.

## Reproducible Invocation

From any working directory, using the repository virtual environment:

```bash
/absolute/path/to/repository/.venv/bin/python /absolute/path/to/repository/tests/hooks/injection_benchmark.py
```

From the repository root:

```bash
.venv/bin/python tests/hooks/injection_benchmark.py
```

Add `--json` for machine-readable output only. The command exits `0` only when schema, inventory, positive replay, negative replay, and false-positive gates pass; otherwise it exits `1` while retaining redacted counts.

## Recorded Result

The implementation run passed with:

- 7 production rules across all 5 required categories
- 19 positive fixtures, 19 true positives, and 0 misses
- 7 realistic negative fixtures and 0 false positives
- 0 high-tier false positives
- Positive detections by category: context manipulation 2, encoding/obfuscation 7, instruction override 2, instruction smuggling 6, persona/role-play hijack 2
- Positive detections by tier: high 3, medium 15, low 1
- 0 skipped fixtures

The negative fixtures are scanned directly through `scan_output`; the source-path allowlist is not called by the benchmark and cannot mask a corpus false positive.

## Evidence and Interpretation

- Automated: schema validation, exact category inventory, bidirectional rule/fixture coverage, positive and negative replay, strongest-match selection, tier response behavior, broken-expectation exit status, cwd-independent invocation, and representative large-output timing.
- Runner-constrained: one harmless high-tier block and one medium/low warning in each propagated harness remain `NOT RUN` after Feature 07 implementation.
- Review: confirm clean-room provenance, bounded regexes, synthetic fixture content, fixed redacted reasons, and absence of allowlist masking.
- Manual: inspect the count summary and exercise one harmless block and one warning in a disposable propagated session; this evidence has not yet been recorded.

## Failure and Redaction Guarantees

The benchmark reports only counts, category names, severity tiers, and pass/fail state. It does not emit fixture bodies, matched spans, or scanner input. It fails closed for invalid JSON or rule configuration with a fixed `benchmark-input-invalid` label.

The benchmark is a deterministic lexical test corpus, not a claim of perfect prompt-injection detection. Semantic classification, remote corpus services, automatic rule learning, direct prompt scanning, and failed-tool-output scanning are outside this phase.
