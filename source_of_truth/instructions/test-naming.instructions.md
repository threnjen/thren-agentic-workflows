---
description: "Names and places every test artifact for the system it covers, never for the phase, plan, or acceptance criterion that produced it. Audience is ENUMERATED deliberately - an arbitrary subset with no filename family. Add any agent that plans, writes, fixes, or reviews tests."
applyTo: "**/03o-feature-plan-author.agent.md,**/03b-feature-implementer.agent.md,**/03c-reviewer-plan-conformance.agent.md,**/04d-consistency-auditor.agent.md,**/04f-test-health.agent.md,**/test-writer.agent.md,**/test-fixer.agent.md,**/single-feature-agent.agent.md"
---

# Test Naming

Name every test artifact for the system or behavior it covers. Test artifacts are folders, namespaces, fixture classes, test methods, helpers, fixture data files, and test comments.

Never put a phase, sub-phase, feature-plan, or acceptance-criterion identifier in a test artifact. Phase letters get relettered, so these names rot.

- **Wrong:** `Tests/Phase09ZC/`, `Project.Tests.Phase09ZC`, `Phase06eFeatureTests`, `Phase09ZC_01_AC4_RigBookReplacedAlone`, `AC3_...`, `F2_AC1_...`
- **Right:** `Tests/Wardrobe/`, `Project.Tests.Wardrobe`, `RigBookTests`, `ReplacingRigBook_LeavesOtherBooksUnchanged`

Put a new test in the existing test location for the code under test. Create a new location only when none exists, and name it for the system.

Record AC-to-test traceability in the implementation record. It lists which test proves which acceptance criterion. Never encode that mapping in the test name.

A phase-named test artifact is never the canonical form, however common it is in the repository. When you touch a file that already uses one, do not copy the pattern into new tests.

Reviewers flag every test artifact that the change adds or renames with a phase, plan, or AC identifier. Record it as a finding.

## Load Canary

When this file is loaded, state once, before your first substantive output: *"Instruction loaded: test-naming."* Then proceed normally.
