# Debugging Learnings

Cross-project patterns from past debugging sessions. Check these before diagnosing new issues. For project-specific findings, also check `.github/learnings/` in the project repo.

---

## 2026-04-13 — Missing integration bootstrap

**Problem:** A phase with 7 independent features all passed code review and unit tests, but the application didn't actually run — no bootstrap/initialization wired the features together at runtime.

**Root cause:** Feature Decomposer created independent feature plans but no integration feature as the final task. Each feature was implemented and reviewed in isolation. Reviewers noted "requires visual verification" but didn't flag the missing wiring as a blocker.

**Fix:** Created a bootstrap script. Patched the Feature Decomposer and feature-plan-set skill to require an integration feature when multiple features must run together.

**Watch for:** When a phase decomposes into multiple library/service features, always check: is there a final feature that wires them into a launchable entry point? Unit tests passing ≠ application working. This is a planning failure, not an implementation failure — fix it at the Decomposer level.

---

## 2026-04-13 — Don't replace working code to fix warnings

**Problem:** UI panels were rendering correctly with a programmatically-created `PanelSettings`. A "No Theme Style Sheet" warning appeared. Replaced the working code with a `Resources.Load` + `return` pattern that required a pre-created asset, causing a full regression — all UI disappeared.

**Root cause:** Treated a non-blocking warning as a critical error. The "fix" added a hard `return` that killed all UI setup when the asset didn't exist.

**Fix:** Reverted to the working programmatic creation. The warning is cosmetic — panels render fine without a theme.

**Watch for:** Before replacing working code to suppress a warning: (1) verify the warning actually causes a user-visible problem, (2) never add early `return` that gates all downstream functionality on an optional dependency. If the current approach works, make the improvement additive, not a replacement.

---

## 2026-04-13 — Unity UI Toolkit layout pitfalls (cross-project)

**Problem:** Multiple compounding issues prevented UI Toolkit panels from rendering in a Unity 6 project with programmatic bootstrap.

**Root causes (in order of discovery):**
1. `AddComponent<T>()` triggers `Awake()` synchronously — fields set after the call aren't available in `Awake()`
2. `VisualTreeAsset.Instantiate()` wraps content in `TemplateContainer` — breaks `position: absolute` layout
3. `Resources.Load<StyleSheet>()` unreliable for USS — use `<Style src="...">` in UXML instead
4. `UIDocument` needs `PanelSettings` to render at all

**Watch for:** When debugging "UI doesn't appear" in Unity UI Toolkit, check this sequence: PanelSettings assigned? → Lifecycle timing correct? → Using CloneTree vs Instantiate? → Stylesheets loading?
