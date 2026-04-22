# Cross-Phase Decisions

## 2026-04-22

- Decision: Phase 01 benchmark capture schema must include runtime-setting metadata (`model_id`, `temperature`, `top_p`, `tool_policy_id`) in addition to provenance fields.
- Why: Comparability requirements already mandate equivalent major runtime settings; explicit schema fields make this auditable and reproducible for downstream validation.
- Affects: `02-prompt-instruction-compaction`, `02-output-verbosity-policy`, `03-end-to-end-validation-regression-analysis` (all must emit these fields in baseline/variant artifacts).

- Decision: `comparable=false` is explicitly treated as `REVIEW_REQUIRED` in Phase 01 verdict semantics and must block delta-based promotion decisions.
- Why: Prevents false PASS/FAIL outcomes when baseline and variant runs are not validly comparable.
- Affects: Any benchmark report or validator consuming Phase 01 status rules.

- Decision: Feature 02 compaction remains partially complete; broad `.github/agents/*.agent.md` and `.github/instructions/*.instructions.md` compaction is deferred to a follow-up pass rather than forced into this review fix.
- Why: Completing that sweep now would require a large cross-module rewrite that exceeds review-fix scope and raises semantic-drift risk.
- Affects: `02-prompt-instruction-compaction` closure criteria and `03-end-to-end-validation-regression-analysis` assumptions about compaction coverage.

- Decision: Edge-case discovery quality cannot be marked pass when benchmark outputs do not provide a direct edge-case metric; status must remain inconclusive/fail-until-evidenced.
- Why: Absence of a regression signal is not equivalent to evidence of non-regression for AC3 quality gating.
- Affects: `03-end-to-end-validation-regression-analysis` report language and future benchmark schema evolution for quality-gate evidence.
