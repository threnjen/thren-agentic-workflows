---
name: unity-development
description: "Implementation and review rules for Unity C# projects. Covers runtime wiring, MonoBehaviour lifecycle, UI Toolkit pitfalls, test authenticity, bootstrap verification, and batch compilation gates. Load when: implementing or reviewing code in a Unity project (detected via Assets/ + ProjectSettings/ directories or copilot-instructions.md Unity identifier)."
---

# Unity Development Skill

Stack-specific rules for Unity C# projects. These rules supplement the standard implementation and review workflows — they do not replace them.

## When to Load This Skill

Load this skill when any of these indicators are present:

- The repo's `.github/copilot-instructions.md` identifies the project as Unity
- The repo contains `Assets/`, `ProjectSettings/`, and `*.asmdef` files
- The plan or phase document references Unity, MonoBehaviour, or Unity-specific systems

## Runtime Wiring Rules

Every feature must be reachable at runtime. Unity does not auto-discover or auto-wire pure C# classes.

### 1. Every New System Needs an Explicit Caller

- **MonoBehaviours** are called by Unity's lifecycle (`Awake`, `Start`, `Update`, etc.) — but only if attached to an active GameObject in the scene or created via `AddComponent<T>()`
- **Pure C# classes** (state machines, managers, subsystems) have NO lifecycle. If the class has per-frame methods (e.g., `UpdateCursor()`, `Tick()`, `Process()`), a MonoBehaviour must call them from its `Update()` or equivalent
- **For every new class**, document in the implementation record: "Called by [X] in [Y method]"

### 2. Bootstrap / Entry Point Verification

If the project has a bootstrap script (e.g., `GameBootstrap.cs`, a scene initializer):

- Every new system that needs initialization must be added to the bootstrap
- Initialization order matters — verify dependencies are initialized before dependents
- If the bootstrap uses `[RuntimeInitializeOnLoadMethod]`, the initialization runs before scene objects are available
- After modifying the bootstrap, verify the full initialization chain still makes sense (read the whole file, don't just append)

### 3. Map/Registry Integration

If the project uses a Map, Grid, or entity registry pattern:

- New entity types must be registered via the project's spawn/despawn pipeline (e.g., `Map.NotifySpawned()`)
- Do NOT register entities directly in tests if production code uses a different path — this masks integration gaps
- Verify that all subsystems that need spawn/despawn awareness are wired into the notification chain

## MonoBehaviour Lifecycle Gotchas

- **`AddComponent<T>()` triggers `Awake()` synchronously.** Fields set after the `AddComponent` call are NOT available in `Awake()`. Use `Start()` or a deferred init method for anything set post-construction.
- **`Destroy()` is deferred to end of frame.** `DestroyImmediate()` runs immediately but should only be used in Editor code or tests. Don't rely on `Destroy()` having taken effect within the same frame.
- **Execution order is not guaranteed** between MonoBehaviours unless explicitly set via Script Execution Order or `[DefaultExecutionOrder]`.

## UI Toolkit Rules

### ScrollView Child Routing

`ScrollView` routes `Add()` calls to its internal `contentContainer`, but `childCount` and `Children()` enumerate the root element's direct children (scroll bars, viewport). **Always use**:

```csharp
scrollView.contentContainer.childCount    // NOT scrollView.childCount
scrollView.contentContainer.Children()    // NOT scrollView.Children()
```

This bug has recurred multiple times. It is the single most common UI Toolkit mistake in this pipeline.

### VisualTreeAsset Instantiation

- Use `visualTreeAsset.CloneTree(parent)` — NOT `visualTreeAsset.Instantiate()`
- `Instantiate()` wraps content in a `TemplateContainer` that breaks `position: absolute` layout

### Stylesheet Loading

- Reference stylesheets from UXML via `<Style src="...">` — NOT via `Resources.Load<StyleSheet>()`
- `Resources.Load<StyleSheet>()` is unreliable in Unity 6

### PanelSettings

- `UIDocument` requires a `PanelSettings` asset with a theme to render
- Runtime-created `PanelSettings` via `ScriptableObject.CreateInstance` lacks the default theme
- Load a pre-created asset via `Resources.Load<PanelSettings>()`

### Working Code + Warning ≠ Broken

- Don't replace working UI code to suppress cosmetic warnings (e.g., "No Theme Style Sheet")
- Never add an early `return` that gates all downstream functionality on an optional dependency
- If the current approach works, make improvements additive, not replacements

## Test Authenticity Rules

### Don't Mock Framework Types with Simplified Stand-ins

When tests substitute a plain `VisualElement` for a `ScrollView` (or any framework widget with different internal routing/behavior), the test will pass but runtime will break. This pattern has caused repeated bugs.

**Rule:** If the code under test interacts with framework-specific behavior (child routing, layout, event bubbling), use the real framework type in tests or document the gap explicitly.

### Don't Bypass the Spawn/Registration Pipeline

Tests that call `RegisterTickable()`, `AddToGrid()`, or similar registration methods directly — when production code goes through `Map.NotifySpawned()` or equivalent — will pass while runtime integration is broken.

**Rule:** Tests should exercise the same code paths as production wherever possible. If a shortcut is necessary for test isolation, add a comment: `// NOTE: Bypasses Map.NotifySpawned() — integration tested in [X]`.

### Verify Event Handlers Do Real Work

Tests that verify "event was fired" are necessary but insufficient. If a UI confirm button fires an event and the handler only hides panels without performing the domain action (e.g., `building.Destroy()`), the test passes but the feature doesn't work.

**Rule:** For any event handler test, also verify the downstream side effect (entity destroyed, state changed, etc.) — or note the gap in the implementation record.

## Rendering Patterns

### Build Before Destroy

Never destroy a mesh/material/resource before building its replacement. If the rebuild throws an exception, the original is permanently lost.

```csharp
// WRONG: destroy-then-rebuild
Object.Destroy(oldMesh);
BuildNewMesh(); // if this throws, mesh is gone forever

// RIGHT: build-then-destroy
var newMesh = BuildNewMesh();
Object.Destroy(oldMesh);
mesh = newMesh;
```

### Avoid Per-Frame Allocations

- Don't allocate `MaterialPropertyBlock`, `List<T>`, or other objects inside per-frame rendering methods
- Cache them as instance fields and reuse
- Unity's GC is generational but frequent small allocations still cause frame hitches

### Batch Renderer State Changes

Batch renderers that only rebuild on add/remove won't reflect per-entity state changes (e.g., degradation tinting). Use dirty flags or periodic polling to trigger rebuilds on state changes.

## Shader Safety

- Verify any `Shader.Find()` string argument exists in the target Unity version
- For opaque colored quads, use an opaque shader (`Unlit/Color`, custom vertex color) — not `Sprites/Default` (transparency shader)
- Safe built-in shaders: `Sprites/Default`, `Unlit/Color`, `Standard`

## Assembly Definition Conventions

- Reference assemblies by GUID in `.asmdef` files when possible (more robust to renames)
- `TheMovies.Core.Data` must have zero direct Unity assembly references (pure C# data layer)
- Verify the dependency DAG: Data ← Simulation ← Rendering, Data ← UI, etc. No circular references.

## Input System

- Check `ProjectSettings.asset` for `activeInputHandler` setting: `0` = Legacy, `1` = New Input System, `2` = Both
- If using "Both" mode, prefer migrating to Input System actions over adding more legacy `Input.GetKeyDown()` calls
- Legacy input calls accumulate tech debt — each new `Input.GetKeyDown()` is one more thing to migrate later

## Save/Load Considerations

- After loading, all subsystems must be rewired to new object instances (Grid, Map, etc.)
- A `LoadManager` that replaces references without notifying subsystems produces stale-reference bugs that are invisible until the player loads a save
- Verify: does every subsystem that holds a Grid/Map reference get updated after load?

## Pre-Handoff Checklist (Unity-Specific)

Before writing the implementation record, verify these in addition to the universal self-check:

1. **Bootstrap updated** — If the feature adds a new system, is it initialized in the bootstrap script in the correct order?
2. **Assembly references correct** — If new files were added, do they live in the right assembly and reference only permitted assemblies?
3. **Def wiring** — If new CompProperties or Def fields were added, does `DefLoader`/`DefSerializer` know how to deserialize them? Is the naming convention followed (`CompX` → `CompProperties_X`)?
4. **TickerType match** — If a new `ThingComp` overrides `CompTickRare` or `CompTickLong`, does the parent Thing's Def set the matching `tickerType`?
5. **PlacedSize vs def.size** — Any code computing building footprints uses `Building.PlacedSize` (the actual placed/rotated size), NOT `def.size` (blueprint size).
6. **Input method** — New keyboard/mouse handling uses the project's established input pattern (check cross-phase-decisions for migration status).
