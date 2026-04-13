# Debugging Learnings

Accumulated findings from past debugging sessions. Check these patterns early when diagnosing similar issues.

## 2026-04-13 — Missing integration bootstrap (Unity / the-movies)

**Problem:** Phase 01 had 7 features (Def system, Grid, Tick engine, Camera, UI, etc.) all implemented and passing 368 unit tests in isolation, but the Unity scene was completely empty — no GameObjects, no MonoBehaviours attached, no bootstrap script. All features were code-correct but never wired together into a runnable application.

**Root cause:** The Feature Decomposer created 7 independent feature plans but never created an integration/bootstrap feature as the final task. Each feature's Implementer built its piece, each Reviewer verified it in isolation, and everyone assumed "visual verification" would happen later — but there was no work item to produce the wiring.

**Fix:** Created `GameBootstrap.cs` MonoBehaviour that initializes all systems in order (DefLoader → Grid → GridRenderer → TickManager → Camera → UI panels). Also patched the Feature Decomposer agent and feature-plan-set skill to require an integration feature when multiple features must run together.

**Watch for:** When a phase decomposes into multiple features that produce libraries/systems rather than a single runnable artifact, always check: does the final deliverable include something that ties them together into a launchable state? Unit tests passing ≠ application working.
