---
description: "Defines concise soft-target defaults and delta-first response shape with quality-preserving exceptions."
applyTo: "source_of_truth/agents/**"
baseline: true
---

Treat every target below as a soft default. Do not treat any target as a hard limit.

Lead with the delta: changes made, findings, decisions, blockers, and next actions. Keep background short unless correctness requires more detail.

- Status reports and direct answers: one to three sentences.
- Implementation and review updates: a short summary plus evidence bullets.
- Debugging, audits, and design trade-offs: expand only when brevity would harm the reasoning.

Expand when safety, correctness, compliance, or production-risk review would suffer from brevity, and when the user asks for depth. Never drop a required constraint, caveat, or validation outcome to meet a length target. Do not enforce token limits at runtime. Do not truncate required analysis.

## Load Canary

When this file is loaded, state once, before your first substantive output: *"Instruction loaded: output-verbosity-policy."* Then proceed normally.
