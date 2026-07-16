# Phase Final Review Development Fixture

This fixture provides one synthetic phase with two pseudo-subphases for local
Phase Final Review dry runs:

```text
fixtures/
└── PHASE_05/
    ├── PHASE_05a/  # copied from docs/phases/PHASE_01/
    └── PHASE_05b/  # copied from docs/phases/PHASE_02/
```

The artifact contents are copied verbatim from the source paths below. The
filenames are normalized from `PHASE_01`/`PHASE_02` to the synthetic subphase
IDs so an orchestrator can discover the same artifact types by subphase:

| Fixture subphase | Source directory | Included artifacts |
|---|---|---|
| `PHASE_05a` | `docs/phases/PHASE_01/` | summary, QA plan, QA coverage map, QA analysis, security scan |
| `PHASE_05b` | `docs/phases/PHASE_02/` | summary, QA plan, QA coverage map, QA analysis, security scan, discovery context |

`PHASE_05b` intentionally includes the real Phase 02 release case: its copied
summary contains the **NO-GO** production verdict, and its copied security scan
contains the introduced High-severity findings. This is fixture input, not a
new assessment.

The Phase 02 discovery context is included because it is a real source artifact
even though the minimum fixture checklist does not require it. No
implementation records are included: neither source phase retains those
records under `docs/phases/`, and this fixture does not invent substitutes.

To regenerate the fixture, copy the listed source files into the corresponding
synthetic subphase directories and preserve their contents. Do not point a dry
run at, or modify, the live `docs/phases/PHASE_01/` or `docs/phases/PHASE_02/`
directories. The `.gitignore` exceptions in the repository root keep this
fixture path trackable while leaving other `dev/` content ignored.
