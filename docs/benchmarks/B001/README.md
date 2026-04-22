# B001 Benchmark Pack

Status: Draft v0.1
Owner: Project maintainers
Last updated: 2026-04-22

## Purpose

B001 is the first concrete benchmark pack for regression testing model and agent changes in this repository.

It is designed to answer:

- Did variant B regress quality versus baseline A?
- Did prompt/token optimization reduce cost without unacceptable quality loss?
- Which task families regressed, and by how much?

## Contents

- manifest file: benchmark metadata, thresholds, and file pointers
- core tasks file: 30 immutable Task Cards distributed across 6 families
- grader templates: deterministic and rubric expectations
- run config template: reproducible execution settings for A/B comparisons

## Family Distribution

- Family A (planning): 8 tasks
- Family B (decomposition): 5 tasks
- Family C (implementation): 6 tasks
- Family D (review): 5 tasks
- Family E (documentation): 3 tasks
- Family F (orchestration): 3 tasks

Total: 30 tasks

## Usage Outline

1. Copy runs/run-config.example.yaml to a run-specific config.
2. Set variant A and variant B model/agent definitions.
3. Execute all tasks with at least 3 repeats per task.
4. Produce a per-family delta report and a benchmark verdict.

## Runner

Runner script:

- `docs/benchmarks/B001/tools/run_b001.py`

Install dependency:

```bash
python3 -m pip install pyyaml
```

Generate a skeleton report (no task results yet):

```bash
python3 docs/benchmarks/B001/tools/run_b001.py \
	--config docs/benchmarks/B001/runs/run-config.example.yaml
```

Run an A/B evaluation using example result payloads:

```bash
python3 docs/benchmarks/B001/tools/run_b001.py \
	--config docs/benchmarks/B001/runs/run-config.example.yaml \
	--baseline-results docs/benchmarks/B001/runs/examples/baseline-results.example.json \
	--candidate-results docs/benchmarks/B001/runs/examples/candidate-results.example.json \
	--output docs/benchmarks/B001/runs/local/B001-EXAMPLE-001-report.json
```

Result payload shape:

```json
{
	"variant": "baseline-A",
	"tasks": [
		{
			"task_id": "B001-A01",
			"hard_pass": true,
			"quality_score": 4.3,
			"compliance_score": 4.7,
			"latency_ms": 800,
			"cost_usd": 0.041,
			"tokens_total": 9500
		}
	]
}
```

Report schema:

- `docs/benchmarks/B001/runs/report.schema.json`

## Batch Comparison Runner

Batch runner script:

- `docs/benchmarks/B001/tools/run_b001_batch.py`

Example batch config:

- `docs/benchmarks/B001/runs/batch-config.example.yaml`

Branch/checkout inputs:

- `baseline_branch`: branch for baseline variant
- `candidates[].branch`: branch for each candidate variant
- `git.checkout_enabled`: enable automatic `git checkout`
- `git.repo_root`: repo root where checkout commands are run
- `git.restore_original_branch`: checkout back to original branch on completion

Run a multi-candidate comparison (A vs B vs C):

```bash
python3 docs/benchmarks/B001/tools/run_b001_batch.py \
	--config docs/benchmarks/B001/runs/batch-config.example.yaml \
	--output docs/benchmarks/B001/runs/local/B001-BATCH-EXAMPLE-001-report.json
```

The batch report includes:

- ranked candidate results
- per-candidate gate evaluation and deltas
- top candidate winner

When checkout is enabled, the runner checks out baseline branch first, then each candidate branch before loading that candidate's results payload.

## Immutability Policy

- Files under this pack are immutable once B001 is baseline.
- Fixes create B001 patch notes plus a new benchmark version when needed.
- Do not edit task prompts in place after baseline capture.
