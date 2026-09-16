# General Unity Practices

*Distilled from Unity Game Dev Field Guide, Tips to increase productivity with Unity 6, and The Game Designer's Playbook.*

---

## MonoBehaviour Lifecycle

- Initialize in `Start()`, not in constructors. Unity handles object construction.
- `Awake()` runs before `Start()`. Use `Awake()` for self-initialization. Use `Start()` for cross-object references.
- **Flag** dependencies on other objects in `Awake()` when those objects are not initialized. Defer those dependencies to `Start()`.
- Run physics in `FixedUpdate()`. Run visual updates in `Update()`. Run camera follow in `LateUpdate()`.
- Use `spawn()` or coroutines for delayed execution. **Never** use `Thread.Sleep()`.
- Remove empty lifecycle methods entirely. Even an empty `Update()` has overhead.
- Use `[RuntimeInitializeOnLoadMethod]` for one-time static setup

---

## Component Architecture

- Each component should have a single responsibility
- Cache `GetComponent<T>()` in `Start()` or `Awake()`. Never cache it in `Update()`.
- Use the `[RequireComponent]` attribute to enforce dependencies when you add a component.
- **Flag** circular dependencies between components. For example, A depends on B and B depends on A.

---

## Prefabs & Scenes

- Keep scene hierarchies **flat**. Deep nesting increases Transform computation costs.
- Use Nested Prefabs and Prefab Variants for shared structure and animation.
- **Flag** excessive prefab overrides that break the prefab link. Use Variants instead.
- Break large scenes into smaller scenes. Load scenes additively with `SceneManager.LoadSceneAsync`.

---

## Assembly Definitions

- Use `.asmdef` files to modularize code and reduce compile times
- Reference assemblies by GUID. GUID references remain robust to renames.
- Verify the dependency DAG: Data ← Simulation ← Rendering, Data ← UI, with no circular references.
- Pure data assemblies should have zero Unity assembly references

---

## Input System

- Check the project's `activeInputHandler` setting: 0=Legacy, 1=New, 2=Both.
- Prefer New Input System actions over `Input.GetKeyDown()` calls
- Each new `Input.GetKeyDown()` adds migration debt. Minimize migration debt.

---

## Scripting Backend

- Use IL2CPP for builds and release for better performance. Use Mono for local iteration for faster builds.
- IL2CPP compiles differently from Mono. Test on the target platform, not only in the Editor.
- Use preprocessor directives for development-only code: `#if DEVELOPMENT_BUILD`, `#if UNITY_EDITOR`
- Use `[Conditional("ENABLE_LOG")]` to strip debug methods from builds

---

## Memory Patterns

- Use **object pooling** for frequently created and destroyed objects (bullets, particles, enemies).
- Prefer value types (`struct`) over reference types (`class`) for small data containers
- **Flag** LINQ in hot paths. LINQ allocates hidden enumerators.
- **Flag** boxing of value types in collections or method signatures.
- Use `ScriptableObject` for static game data. This removes GameObject and Transform overhead.

---

## Project Configuration

- Disable Domain Reload and Scene Reload for faster Play Mode iteration, but only if you plan no script changes.
- Use EditorConfig files for team-wide code style enforcement
- Force Text serialization for version-control-friendly diffs
- Use Visible Meta Files for external version control systems.

---

## Profiling Workflow

- Use `ProfilerMarker` to isolate performance-critical sections
- Use Memory Profiler to track allocations and detect leaks
- Use Project Auditor (Unity 6.1+) to scan for unused assets, excessive entities, and garbage-collection (GC) pressure.
- Profile on the target device, not in the Editor. The Editor inflates all metrics.

---

## Game Design Principles (Code-Relevant)

- **Separate concerns in scripts**. Each script should handle one responsibility, such as movement, animation, or health.
- Build one Prefab for each concept. Use Prefab Variants for variations.
- Playtest on actual target devices early. Do not rely on Editor testing.
- Use easing curves (ease-in or ease-out) instead of linear interpolation for natural motion.
- Add "juice" (animation curves, particles, sound) to make interactions responsive
