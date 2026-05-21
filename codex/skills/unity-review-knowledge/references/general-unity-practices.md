# General Unity Practices

*Distilled from: Unity Game Dev Field Guide + Tips to increase productivity with Unity 6 + The Game Designer's Playbook*

---

## MonoBehaviour Lifecycle

- Initialize in `Start()`, not constructors — Unity handles object construction
- `Awake()` runs before `Start()` — use for self-initialization; `Start()` for cross-object references
- **Flag**: Dependencies on other objects in `Awake()` that aren't yet initialized — defer to `Start()`
- Physics in `FixedUpdate()`, visual updates in `Update()`, camera follow in `LateUpdate()`
- Use `Invoke()` or coroutines for delayed execution — **never** `Thread.Sleep()`
- Remove empty lifecycle methods entirely — even empty `Update()` has overhead
- Use `[RuntimeInitializeOnLoadMethod]` for one-time static setup

---

## Component Architecture

- Each component should have a single responsibility
- Cache `GetComponent<T>()` in `Start()`/`Awake()` — never in `Update()`
- Use `[RequireComponent]` attribute to enforce dependencies at add-time
- **Flag**: Circular dependencies between components (A depends on B, B depends on A)

---

## Prefabs & Scenes

- Keep scene hierarchies **flat** — deep nesting costs Transform computation
- Use Nested Prefabs and Prefab Variants for shared structure/animation
- **Flag**: Excessive prefab overrides that break the prefab link — use Variants instead
- Break large scenes into smaller scenes; load additively with `SceneManager.LoadSceneAsync`

---

## Assembly Definitions

- Use `.asmdef` files to modularize code and reduce compile times
- Reference assemblies by GUID (robust to renames)
- Verify dependency DAG: Data ← Simulation ← Rendering, Data ← UI — no circular references
- Pure data assemblies should have zero Unity assembly references

---

## Input System

- Check project's `activeInputHandler` setting: 0=Legacy, 1=New, 2=Both
- Prefer New Input System actions over `Input.GetKeyDown()` calls
- Each new `Input.GetKeyDown()` is migration debt — minimize accumulation

---

## Scripting Backend

- IL2CPP for builds/release (better performance); Mono for local iteration (faster builds)
- IL2CPP compiles differently than Mono — test on target platform, not just Editor
- Use preprocessor directives for development-only code: `#if DEVELOPMENT_BUILD`, `#if UNITY_EDITOR`
- Use `[Conditional("ENABLE_LOG")]` to strip debug methods from builds

---

## Memory Patterns

- **Object pooling** for frequently created/destroyed objects (bullets, particles, enemies)
- Prefer value types (`struct`) over reference types (`class`) for small data containers
- **Flag**: LINQ in hot paths — allocates hidden enumerators
- **Flag**: Boxing value types in collections or method signatures
- Use `ScriptableObject` for static game data — removes GameObject/Transform overhead

---

## Project Configuration

- Disable Domain Reload/Scene Reload for faster Play Mode iteration — but only if no script changes planned
- Use EditorConfig files for team-wide code style enforcement
- Force Text serialization for version-control-friendly diffs
- Use Visible Meta Files for external VCS

---

## Profiling Workflow

- Use `ProfilerMarker` to isolate performance-critical sections
- Use Memory Profiler to track allocations and detect leaks
- Project Auditor (Unity 6.1+): scan for unused assets, excessive entities, GC pressure
- Profile on target device, not Editor — Editor inflates all metrics

---

## Game Design Principles (Code-Relevant)

- **Separate concerns in scripts**: each script handles one responsibility (move, animate, health)
- Build one Prefab per concept; use Prefab Variants for variations
- Playtest on actual target devices early — don't rely on Editor testing
- Use easing curves (ease-in/out) instead of linear interpolation for natural motion
- Add "juice" (animation curves, particles, sound) to make interactions responsive
