---
name: unity-development
description: "Implementation and review rules for Unity C# projects. Covers runtime wiring, MonoBehaviour lifecycle, UI Toolkit pitfalls, test authenticity, bootstrap verification, and batch compilation gates. Load when: implementing or reviewing code in a Unity project (detected via Assets/ + ProjectSettings/ directories or copilot-instructions.md Unity identifier)."
---
<!-- Generated from .github/skills source-of-truth. Do not edit manually. -->
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

### Tooltip Testing

- `VisualElement.tooltip` is appropriate when tests only need to verify the tooltip property state
- If EditMode panel tests must verify hover-triggered tooltip visibility, assume native tooltip behavior is insufficient unless the codebase already proves otherwise
- For hover visibility, prefer a small runtime overlay driven by `PointerEnterEvent` and `PointerLeaveEvent`, with tests using the real panel/controller structure
- Plans that touch UI Toolkit tooltips should still mark related `.uxml`, `.uss`, and test root builder files as `(verify)` when companion changes are uncertain

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

## Serialized Assets: Generate via Unity, Never Hand-Author

Unity's serialized assets — `.prefab`, `.unity` scenes, `.mat`, `.asset` (including SRP pipeline/renderer assets), and `.meta` files — are produced by the Unity Editor's serializer. The Editor is the sole authority for GUIDs, fileIDs, class ids, required-component dependencies, and version-correct format. An agent hand-writing these files is impersonating that serializer **blind**: no access to the real GUID database, no enforcement of component dependencies, no way to validate the output. This is the single most common source of "compiles green, tests pass, but nothing renders / NRE every frame" failures.

**Rule: do not hand-author serialized Unity assets from scratch.** Build them by running the Unity Editor API in batch mode (an `Editor/` script Unity executes), so Unity generates the asset, its GUIDs, and its `.meta`:

- Prefabs → construct the GameObject with `new GameObject(...)` + `AddComponent<T>()`, then `PrefabUtility.SaveAsPrefabAsset`.
- Scenes → `EditorSceneManager.NewScene`/`OpenScene`, build contents, `EditorSceneManager.SaveScene`.
- Materials / ScriptableObjects / SRP assets → `new Material(Shader.Find(...))` / `ScriptableObject.CreateInstance<T>()` (or the type's `Create()` helper) + `AssetDatabase.CreateAsset`.
- Sprites/textures → import a real source file; never invent a texture/sprite `.meta` GUID.

Run via `-batchmode -executeMethod <Type>.<Method> -quit`, then confirm the assets imported without errors.

**Boundary:** a *surgical edit* to an existing, Unity-generated asset (changing a serialized value in a file the Editor already produced) is acceptable. *Authoring a whole asset as raw YAML* is the anti-pattern. The risk is highest in unattended pipeline runs where no human Play-tests each step.

### Invalid-asset red flags (when producing OR reviewing any serialized asset)

- A `MonoBehaviour.m_Script` GUID of `0000000000000000f000000000000000` (builtin-extra — valid only for builtin fonts/textures/materials, **never** a script), or any `m_Script`/asset GUID with no matching `.cs.meta` or package meta → silent "missing script" → `null` at runtime.
- A class-id tag that doesn't match the component body: `SpriteRenderer` is `!u!212` (not `!u!23` = MeshRenderer); UI elements need `RectTransform` (`!u!224`), not `Transform` (`!u!4`).
- **(uGUI / legacy UI only)** A UI `Graphic` (`Image`/`Text`) missing its required `CanvasRenderer` (`!u!222`) and `RectTransform`; a `Canvas` missing a `RectTransform`. (UI Toolkit projects use `UIDocument`/`PanelSettings` instead — not applicable.)
- An asset reference (`m_Sprite`, `m_Materials`, `m_Font`, renderer/pipeline) whose GUID no existing `.meta` defines → dangling reference → renders nothing, no error.
- **(URP only)** A render-pipeline chain that doesn't fully resolve: `QualitySettings`/`GraphicsSettings` → URP pipeline `.asset` → renderer `.asset` must all exist. A missing link silently disables sprite/line rendering with no console error. (Built-in Render Pipeline projects have no such chain.)
- A serialized field reported as "wired" whose target component's script GUID does not resolve — a present fileID is **not** proof the reference resolves.

## Visual Verification Wiring

For a View feature whose phase has visual acceptance criteria, set up its visual test the same
way you set up unit tests for logic — it is part of "done," not an afterthought. The capture
mechanism is config-driven (a generic PlayMode capture package, e.g.
`com.threnjen.visual-verification`), so "writing the visual test" means wiring the project to run
it, not authoring per-feature test code:

1. **Ensure the capture package is a dependency.** If the project documents a visual-verification
   capture package (in `Packages/manifest.json`, `CLAUDE.md`, or setup docs), confirm it is present
   in `Packages/manifest.json` and listed under `testables`. Do not invent a package URL — if none
   is documented and none is present, record the gap in the implementation record rather than
   guessing.
2. **Create or update the capture config.** Ensure `Assets/VisualVerification/capture-config.json`
   (root layout) or `game/Assets/VisualVerification/capture-config.json` (nested layout) exists,
   with an entry for the scene this feature renders: the scene name, capture frames that show the
   feature's behavior (e.g. an early frame and a later frame), and resolution. Reuse the existing
   config if the scene is already covered.
3. **Confirm the scene is loadable.** The capture loads the scene by name, so it must be in Build
   Settings and have a `MainCamera`-tagged camera.

Record in the implementation record which scene the config covers and which visual ACs the captured
frames are meant to demonstrate, so the Visual Verifier (and the orchestrator's visual gate) have a
clear target.

## Pre-Handoff Checklist (Unity-Specific)

Before writing the implementation record, verify these in addition to the universal self-check:

1. **Bootstrap updated** — If the feature adds a new system, is it initialized in the bootstrap script in the correct order?
2. **Assembly references correct** — If new files were added, do they live in the right assembly and reference only permitted assemblies?
3. **Def wiring** — If new CompProperties or Def fields were added, does `DefLoader`/`DefSerializer` know how to deserialize them? Is the naming convention followed (`CompX` → `CompProperties_X`)?
4. **TickerType match** — If a new `ThingComp` overrides `CompTickRare` or `CompTickLong`, does the parent Thing's Def set the matching `tickerType`?
5. **PlacedSize vs def.size** — Any code computing building footprints uses `Building.PlacedSize` (the actual placed/rotated size), NOT `def.size` (blueprint size).
6. **Input method** — New keyboard/mouse handling uses the project's established input pattern (check cross-phase-decisions for migration status).
7. **Serialized assets generated, not hand-written** — Any new/changed `.prefab`/`.unity`/`.mat`/`.asset` was produced via the Unity Editor API (batch-mode `Editor/` script), not hand-authored YAML. No fabricated GUIDs, no `0000…f000` `m_Script` references, no missing required components or dangling asset references. See "Serialized Assets: Generate via Unity, Never Hand-Author".
8. **Visual test wired** — For a View feature with visual ACs, is the capture config present for this scene and the capture package a dependency listed under `testables`? Is the scene in Build Settings with a `MainCamera`? See "Visual Verification Wiring".
