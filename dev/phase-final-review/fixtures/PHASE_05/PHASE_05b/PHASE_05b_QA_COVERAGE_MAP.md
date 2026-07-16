# Phase 02 QA Coverage Map

**Date:** 2026-07-15  
**Scope:** Injection Scanner, WebFetch Exfiltration Guard, Injection Pattern Corpus, and Multi-Harness Integration  
**Release evidence state:** Automated functional evidence is recorded; PERF-01 remains **FAIL (risk accepted)**; Codex remains **Partial (risk accepted)**; all live/manual checks are **NOT RUN**

## Evidence Legend

- **No**: deterministic automated/static evidence is sufficient for the criterion.
- **Partial**: automated evidence exists, but live runner, human recovery, presentation, or release-environment evidence remains.
- **Yes**: a live runner or human-controlled action is essential.
- `NOT RUN` always means no live/manual observation is claimed. User sign-off accepts a stated risk only; it is not execution evidence.

## Acceptance-Criteria Coverage

| Feature | AC | Automated coverage | Manual QA? | Remaining evidence / disposition |
|---|---|---|---|---|
| `05-injection-scanner` | AC1 | Framework tests cover exact PostToolUse fields and preserved PreToolUse aliases/decisions. | No | Deterministic contract is covered. |
| `05-injection-scanner` | AC2 | Scanner tests cover NFKC, homoglyph, invisible characters, bounded base64/hex, and raw-output immutability. | No | Deterministic normalization is covered. |
| `05-injection-scanner` | AC3 | Rule validation, immutable data-driven policy, unsafe regex rejection, and no engine-embedded production policy are tested. | No | Static/behavioral coverage is sufficient. |
| `05-injection-scanner` | AC4 | Public `load_injection_rules`/`scan_output` APIs and structured redacted metadata are exercised by scanner and corpus suites. | No | Reuse contract is automated. |
| `05-injection-scanner` | AC5 | Entrypoint tests prove high block, structured shape-preserving redaction, and no-retry/manual-inspection reason. | Yes | Real Claude built-in/MCP suppression and no-retry remain **NOT RUN**; QA C1, C3, C4. |
| `05-injection-scanner` | AC6 | Warning tests prove intact logical output plus redacted `additionalContext`. | Yes | Live warning attachment/presentation remains **NOT RUN**; QA C2. |
| `05-injection-scanner` | AC7 | Existing/missing paths, traversal, symlinks, repository containment, protected config, and approved-root restrictions are tested. | Partial | Real source-path allowlist and protected-write behavior remain **NOT RUN**; QA C5, P2. |
| `05-injection-scanner` | AC8 | Empty, binary-shaped, structured, capped, truncated, multi-match, and tie-break paths are tested. | Partial | Live truncation and structured runner behavior remain **NOT RUN**; QA C4-C5. |
| `05-injection-scanner` | AC9 | Parse/config/normalization/matching/emission failure posture and project-only override recovery are tested. | Yes | Human disable/repair/restore remains **NOT RUN**; QA R2. |
| `05-injection-scanner` | AC10 | Recorded built-in, Task/subagent, MCP, JSON, truncation, binary-shaped, and malformed payloads pass; registration is PostToolUse-only. | Yes | Real Task/subagent/MCP tool coverage remains **NOT RUN**; QA C4. |
| `05-webfetch-exfiltration-guard` | AC1 | Recorded WebFetch payloads verify exact `tool_input.url` routing and matcher. | Yes | Interactive WebFetch remains **NOT RUN**; QA W1. |
| `05-webfetch-exfiltration-guard` | AC2 | WebFetch and Bash tests call one `analyze_url` classifier. | Partial | Live consumer parity remains **NOT RUN**; QA W1-W2. |
| `05-webfetch-exfiltration-guard` | AC3 | Known credential/encoded shapes deny through configuration-driven tests. | Yes | Real runner deny remains **NOT RUN**; QA W1-W2. |
| `05-webfetch-exfiltration-guard` | AC4 | Ambiguous entropy asks and bypass escalation are tested in both consumers. | Yes | Live `ask` presentation remains **NOT RUN**; QA W1-W2. |
| `05-webfetch-exfiltration-guard` | AC5 | Ordinary hosts, ports, fragments, encoding, UUID/hash assets, and request-body negatives pass. | Partial | Real ordinary URL pass-through remains **NOT RUN**; QA W1-W2. |
| `05-webfetch-exfiltration-guard` | AC6 | Direct, quoted, option-reordered, piped, and redirection URL forms plus action/priority selection are tested. | Yes | Live curl/wget parity remains **NOT RUN**; QA W2. |
| `05-webfetch-exfiltration-guard` | AC7 | URL patterns, thresholds, actions, guidance, priority, escalation, and command coverage are validated from config. | No | Data-driven policy is automated/static. |
| `05-webfetch-exfiltration-guard` | AC8 | Missing/non-string/malformed inputs, malformed escapes/ports, bounded parsing, and documented dynamic-shell limits are covered. | Partial | Human boundary review and representative live forms remain **NOT RUN**; QA W2. |
| `05-webfetch-exfiltration-guard` | AC9 | Decisions/audit sentinel tests exclude URL, host, path, query, command, and secret content. | Yes | Live UI/stderr/audit inspection remains **NOT RUN**; QA R1. |
| `06-injection-pattern-corpus` | AC1 | Production config/doc record clean-room provenance; review confirmed no surveyed pattern source was opened/copied. | No | Static provenance review is sufficient. |
| `06-injection-pattern-corpus` | AC2 | Seven rules cover five required categories; markdown fixtures cover required native channels. | No | Inventory/replay is automated. |
| `06-injection-pattern-corpus` | AC3 | Unique complete rule metadata, exact severity inventory, safe matchers, and invalid-schema failures are tested. | No | Schema is automated. |
| `06-injection-pattern-corpus` | AC4 | Exact bidirectional rule-to-positive-fixture inventory and strongest-result metadata pass. | No | Fixture completeness is automated. |
| `06-injection-pattern-corpus` | AC5 | Seven realistic synthetic legitimate content classes scan without allowlisting and produce no matches. | Partial | Result is corpus-bounded; broader soak/review is advisable but not a claimed live pass. |
| `06-injection-pattern-corpus` | AC6 | Cwd-independent benchmark reports deterministic total/category/tier counts, fails non-zero, and redacts bodies. | No | Benchmark recorded 19 TP, 0 misses/FP/skips. |
| `06-injection-pattern-corpus` | AC7 | Benchmark enforces zero high false positives and exact high-block/lower-warn response mapping. | Yes | Live high/warn presentation remains **NOT RUN**; QA C1-C2. |
| `06-injection-pattern-corpus` | AC8 | Plain, NFKC, homoglyph, zero-width, base64, hex, leetspeak, multi-match, markdown, and representative corpus timing pass. | Partial | Corpus timing passes; phase-level PERF-01 still fails separately. Live obfuscated output is not required, but PERF disposition is QA P3. |
| `07-multi-harness-integration` | AC1 | Versions/date/contracts and safe automated experiments are documented for Claude, Codex, and OpenCode. | Partial | Live runner observations remain **NOT RUN**; QA H1-H2. |
| `07-multi-harness-integration` | AC2 | Claude/OpenCode automated parity and Codex limitation/sign-off produce one recorded state per harness. | Partial | Codex **Partial risk accepted**; live checks remain **NOT RUN**; QA H1-H3. |
| `07-multi-harness-integration` | AC3 | Claude built-in/MCP replacement, Codex supported subset, and OpenCode mutable-output translation are tested. | Yes | Real runner replacement/warning behavior remains **NOT RUN**; QA C1-C4, H1-H2. |
| `07-multi-harness-integration` | AC4 | Propagation tests verify complete detached runtime/corpus/allowlist/URL/adapters/version outputs. | Partial | Release-candidate fresh consumer reproduction remains **NOT RUN**; QA P1-P2. |
| `07-multi-harness-integration` | AC5 | Preservation, stale cleanup, command-target integrity, and byte idempotence are tested. | Partial | Human inspection/reproduction remains **NOT RUN**; QA P1. |
| `07-multi-harness-integration` | AC6 | Detached consumer, protected assets, allowlist translation, and external/internal nested symlink tests pass. | Partial | Human SEC-01 and write-denial reproduction remain **NOT RUN**; QA P2, S1. |
| `07-multi-harness-integration` | AC7 | Consolidated propagated smoke covers scanner block/warn/truncation/allowlist plus WebFetch and Bash deny/ask/allow. | Partial | Live end-to-end runner behavior remains **NOT RUN**; QA C1-C5, W1-W2. |
| `07-multi-harness-integration` | AC8 | Automated sentinels and adapter tests pass; fixed latency test remains red. | Yes | Live redaction/no-retry **NOT RUN**; PERF-01 **FAIL risk accepted**; QA R1, P3. |
| `07-multi-harness-integration` | AC9 | Installation/verification/manual/recovery/support docs and classifications are asserted by tests. | Yes | Human recovery and live support observations remain **NOT RUN**; QA R2, H1-H3. |
| `07-multi-harness-integration` | AC10 | SEC-01 containment regressions pass; unchanged 50 ms gate reproduces failure. | Partial | SEC-01 release reproduction **NOT RUN**; PERF-01 remains **FAIL risk accepted**; QA S1, P3. |

## Manifest Verification Assets

| Required asset / check | Automated coverage | Release disposition |
|---|---|---|
| `tests/hooks/test_injection_scanner.py` | Normalization, schema, block/warn, allowlist, boundaries, failure posture, tool coverage, imports, performance. | Passed in reviewed focused suites; live portions remain QA C1-C5/R2. |
| `tests/hooks/test_injection_corpus.py` | Clean-room inventory, fixtures, response mapping, negatives, benchmark behavior, performance. | Passed; negative result is bounded to the recorded corpus. |
| `tests/hooks/injection_benchmark.py` | Direct production API replay with deterministic redacted counts and non-zero failures. | 19 TP, 0 misses, 0 FP, 0 high FP, 0 skipped. |
| `tests/hooks/fixtures/injection/post-tool-use-payloads.json` | Built-in, Task/subagent, MCP, structured, truncated, malformed, and binary-shaped payload replay. | Automated passed; live Task/MCP/truncation **NOT RUN**. |
| `tests/hooks/fixtures/url_exfiltration/recorded_payloads.json` | Synthetic `.invalid` WebFetch deny/ask/allow and malformed payloads. | Automated passed; interactive WebFetch **NOT RUN**. |
| `tests/hooks/fixtures/injection/positive.json` | Per-rule positives plus normalization/encoding/leetspeak/multi-match variants. | Automated passed. |
| `tests/hooks/fixtures/injection/negative.json` | Seven required legitimate content classes, without allowlisting. | 0 matches in benchmark; corpus-bounded reservation retained. |
| `tests/hooks/fixtures/injection/markdown-smuggling.json` | Link title, image alt, reference definition, HTML/code comment, and HTML attribute channels. | Automated passed. |
| `docs/hooks/injection-benchmark.md` | Provenance, invocation, result interpretation, redaction, limits. | Review verified; compare against release benchmark output. |
| `tests/hooks/test_hook_distribution_integration.py` | Fresh consumer, combined Phase 02 smoke, self-protection, redaction, docs, and latency. | Functional checks pass; PERF-01 fixed gate fails. |
| Real Claude high block | QA C1. | **NOT RUN**. |
| Real Claude warning | QA C2. | **NOT RUN**. |
| No-retry behavior | QA C3. | **NOT RUN**. |
| Truncation and allowlist | QA C5. | **NOT RUN**. |
| WebFetch deny/ask/allow | QA W1. | **NOT RUN**. |
| Bash parity | QA W2. | **NOT RUN**. |
| Sentinel redaction | Automated plus QA R1. | Automated passed; live **NOT RUN**. |
| Human kill switch | Automated config behavior plus QA R2. | Human workflow **NOT RUN**. |
| Codex/OpenCode evidence or limitations/sign-off | QA H1-H3. | Codex risk accepted and remains Partial; all live checks **NOT RUN**. |
| Preservation and stale cleanup | Automated propagation tests plus QA P1. | Automated passed; manual **NOT RUN**. |
| Symlink containment / SEC-01 | Automated regressions plus QA S1. | **PASS automated**; manual reproduction **NOT RUN**. |
| PERF-01 disposition | Fixed test plus QA P3. | **FAIL risk accepted**; latest reviewed median 135.42 ms, historical range about 117–383 ms. |

## Current Phase Gate Summary

| Gate | Status |
|---|---|
| Scanner and corpus functional behavior | Passed automated review evidence. |
| URL exfiltration functional behavior | Passed automated review evidence. |
| Combined propagated functional smoke | Passed automated review evidence. |
| Full suite | 383 passed, 1 failed; sole failure PERF-01. |
| Coverage | 71.42% with two fixed timing assertions deselected; threshold 50%. |
| Benchmark | 19 TP, 0 misses, 0 FP, 0 high FP, 0 skipped. |
| Codex parity | Partial; residual gap accepted, not fixed. |
| SEC-01 | Pass automated. |
| PERF-01 | Fail; risk accepted. |
| Live/manual QA | All items NOT RUN. |
