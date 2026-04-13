# Debugging Learnings

Cross-project patterns from past debugging sessions. Check these before diagnosing new issues. For project-specific findings, also check `.github/learnings/` in the project repo.

---

## 2026-04-13 — Missing integration bootstrap

**Problem:** A phase with 7 independent features all passed code review and unit tests, but the application didn't actually run — no bootstrap/initialization wired the features together at runtime.

**Root cause:** Feature Decomposer created independent feature plans but no integration feature as the final task. Each feature was implemented and reviewed in isolation. Reviewers noted "requires visual verification" but didn't flag the missing wiring as a blocker.

**Fix:** Created a bootstrap script. Patched the Feature Decomposer and feature-plan-set skill to require an integration feature when multiple features must run together.

**Watch for:** When a phase decomposes into multiple library/service features, always check: is there a final feature that wires them into a launchable entry point? Unit tests passing ≠ application working. This is a planning failure, not an implementation failure — fix it at the Decomposer level.
