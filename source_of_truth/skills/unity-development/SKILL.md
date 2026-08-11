---
name: unity-development
description: "Implementation and review rules for Unity C# projects. Covers runtime wiring, MonoBehaviour lifecycle, UI Toolkit pitfalls, test authenticity, bootstrap verification, and batch compilation gates. Load when: implementing or reviewing code in a Unity project - detected by the canonical Unity predicate in tech-stack-detection: Assets/ + ProjectSettings/ at the repo root or inside one nested directory (e.g. game/Assets/), or .github/copilot-instructions.md identifying the project as Unity, or a plan or phase document targeting Unity, MonoBehaviour, or Unity-specific systems. *.asmdef files corroborate but are not required."
---

# Unity Development Skill

Stack-specific rules for Unity C# projects. These rules supplement the standard implementation and review workflows — they do not replace them.

## Preflight (read these files before writing any code)

Before writing any Unity-specific code, read the following project files and document each finding in the implementation record's summary. These are not advisory — skipping one means writing code against assumptions that may be wrong.

### 1. Input handling mode
**Read:** `ProjectSettings/ProjectSettings.asset` — search for `activeInputHandler:`.

| Value | Meaning | What to use |
|-------|---------|-------------|
| `0` | Legacy input | `Input.GetMouseButtonDown`, `Input.mousePosition`, etc. |
| `1` | New Input System | `Mouse.current.leftButton.wasPressedThisFrame`, etc. |
| `2` | Both | Prefer new Input System API; legacy calls still work |

**Record in implementation record:** `activeInputHandler: <value> — using <which API>`.

### 2. Assembly reference graph
**Read:** the `.asmdef` file for every assembly you will create or modify. (For the View layer: `Assets/Scripts/View/Combat/View.asmdef`. For Controllers: `Assets/Scripts/Controllers/Controllers.asmdef`. For Tests: `Assets/Tests/EditMode/Tests.EditMode.asmdef`.)

For each new `using` directive you add to any `.cs` file, confirm the assembly named after `using` appears in that `.asmdef`'s `"references"` array or is a known implicit dependency (e.g., `System`, `System.Collections.Generic`, `UnityEngine` when `noEngineReferences` is `false`).

**Record in implementation record:** every new assembly reference added and why.

### 3. Scene wiring (MonoBehaviours only)
**Read:** the relevant `.unity` scene file (e.g., `Assets/Scenes/CombatSandbox.unity`).

If your feature creates a new `MonoBehaviour`, one of these must be true:
- The component is attached to a GameObject in the scene (visible in the scene YAML under the component's `m_Script` GUID).
- An existing MonoBehaviour calls `AddComponent<T>()` to create it at runtime (find the call site).
- It is instantiated from a prefab (find the prefab and confirm the component is on it).

If none of these are true, the component is **dead code** — it will never be instantiated, never receive `Awake`/`Start`/`Update`, and every method on it is unreachable.

**Record in implementation record:** "`[ComponentName]` is attached to `[GameObject]` via [scene / AddComponent at X / prefab at Y]."

### 4. Render pipeline
**Read:** `Project Settings > Graphics` (or `Assets/` for the active pipeline asset) or search for `ScriptableRendererFeature`/`UniversalRenderPipelineAsset` in the project.

If your feature creates any renderable object at runtime (`new GameObject(..., typeof(LineRenderer))`, `new GameObject(..., typeof(SpriteRenderer))`, `new GameObject(..., typeof(MeshRenderer))`), confirm the material you assign (or the default Unity assigns) is compatible with the active pipeline:
- **Built-in RP:** default materials work.
- **URP:** the built-in `Default-Line` material does not work. Either instantiate a URP-compatible material (e.g., `new Material(Shader.Find("Universal Render Pipeline/Lit"))`) or share one from an existing renderer in the scene (e.g., `boundsRenderer.sharedMaterial`).

**Record in implementation record:** "Active pipeline: [URP/BiRP/HDRP]. Runtime renderers: [list] — material sourced from [explicit assignment / shared from X]."

### 5. Preflight findings go in the implementation record
At the top of the implementation record's Summary section, add a **Preflight** block:

```
## Preflight
- activeInputHandler: 1 (using new Input System API)
- View.asmdef references: Model, Controllers, Unity.InputSystem (added)
- CombatInputView auto-added via AddComponent in CombatSceneView.Initialize
- Pipeline: URP. LineRenderer material shared from boundsRenderer.sharedMaterial
```

This block is not a formality — it tells the reviewer exactly which project-configuration decisions were made and verified, so they don't have to re-derive them.

---

## C# Carve-outs Inside Unity Assemblies

General C# standards (`csharp-standards`, `instructions/csharp-style.instructions.md`) apply, with these Unity-only overrides. Each wins inside Unity assemblies only, for the reason stated.

- **Never use `?.`, `??`, or `??=` on a `UnityEngine.Object` subclass** (`GameObject`, `Component`, MonoBehaviour, `ScriptableObject`). Unity overloads `==`/`!=` so a *destroyed* object compares equal to `null` while the managed reference is not null; the null-conditional and null-coalescing operators bypass that overload and see the live reference. So `destroyed?.transform` still executes, and `_cached ??= GetComponent<T>()` keeps a destroyed component forever. Use an explicit `== null` / `!= null` check.
  ```csharp
  // NEVER
  var t = _maybeDestroyed?.transform;
  _cached ??= GetComponent<Rigidbody>();
  // MUST
  if (_maybeDestroyed != null) { var t = _maybeDestroyed.transform; }
  if (_cached == null) { _cached = GetComponent<Rigidbody>(); }
  ```
- **`[SerializeField]` private fields are `camelCase` with no leading underscore**, and are never `readonly` or `init`. The Inspector derives its label from the field name, and the deserializer assigns them after construction. Non-serialized private fields keep `_camelCase` — the attribute is the signal distinguishing the two. Do not widen them to a public setter.
- **Types serialized by `JsonUtility` are `[Serializable] class`/`struct` with public fields**, not `record`. `JsonUtility` ignores records, `init` setters, and properties — a `record` DTO silently round-trips as all-default. With Newtonsoft.Json or System.Text.Json the general `record` rule applies.
- **Enable nullable reference types per assembly, not via `.csproj`** — Unity regenerates it on every import, and a per-`.asmdef` `csc.rsp` is not honored. Use `Assets/csc.rsp` containing `-nullable:enable` for the predefined `Assembly-CSharp`, and a file-scoped `#nullable enable` at the top of every file in an `.asmdef` assembly. Enable pure-domain assemblies (no `UnityEngine` surface) first; the engine boundary generates noise that buries real findings.
- **`record` and `init` need an `IsExternalInit` polyfill** — Unity's .NET Standard 2.1 runtime omits it and the compiler fails with `CS0518`. One `internal static class IsExternalInit { }` in `namespace System.Runtime.CompilerServices` per assembly.
- **Never touch the Unity API from a `Task` continuation without marshalling back to the main thread** — continuations do not resume on it and most engine APIs throw off it. Use coroutines or `Awaitable`/`UniTask` for frame-paced logic; reserve `Task` for background I/O at the edge.

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

## Refactor / Rewire Test Preservation Rules

- Before planning a refactor, runtime rewire, API change, or behavior change, inventory the affected Unity tests and harnesses (`Assets/Tests/EditMode`, `Assets/Tests/PlayMode`, any phase-scoped or editor tests, and UI Toolkit test root builders). Plan them as part of the work, not as a deferred cleanup.
- If the change alters a public API, bootstrap path, serialized asset layout, scene wiring, prefab, event contract, or lifecycle behavior, assume related tests will need updates and include those files in the plan's scope and verification assets.
- When a Unity test becomes obsolete because production behavior changed, update or retire it in the same feature and document the reason. Leave no orphaned or silently broken tests behind.
- For controller, UI Toolkit, or scene-wiring changes, include the corresponding test assembly and test root builder files in the planned scope and explicitly note whether each needs test updates.

## Test Execution

Unity Test Framework is the authoritative runner. Compilation success and focused harnesses are not test execution — see the `test-execution-evidence` instruction.

`-batchmode` is mandatory for every agent-driven Unity test run. Resolve the editor executable through the existing procedure in `source_of_truth/agents/04g-unity-visual-verification.agent.md`. Never assume a bare `Unity` executable is on `PATH`.

| Platform | Required flags |
|----------|----------------|
| EditMode | `-batchmode -nographics` |
| PlayMode and visual capture | `-batchmode` with graphics enabled; exclude `-nographics` |

```bash
"<resolved-unity-editor>" -batchmode -nographics -runTests -projectPath "<execution-checkout>" -testPlatform EditMode -testResults "<absolute-main-checkout>/dev/test-results/<results.xml>"
"<resolved-unity-editor>" -batchmode -runTests -projectPath "<execution-checkout>" -testPlatform PlayMode -testResults "<absolute-main-checkout>/dev/test-results/<results.xml>"
```

- Never pair `-quit` with `-runTests`; Unity can exit before the tests execute and return a false-green zero exit code.
- **Affected-suite runs use `-testFilter`** — a semicolon-separated list of full test names or a regex, negation supported. Scope it to the suites exercising the changed symbol. Gate runs (wave boundary, phase end) are unfiltered.
- `-testResults` always receives an absolute path under the main checkout's `dev/test-results/`. The shadow worktree is an execution target only. Never read results from the shadow worktree.

**Precondition.** Commit before testing in a shadow worktree; it can represent only committed code. The normal per-feature commit usually satisfies this precondition. A dirty checkout requires a commit before this procedure begins.

### Execution Ladder

1. **Persistent shadow worktree.** From the main checkout, run `git worktree prune`, then use the one fixed detached sibling `<project-dir>-agent-tests/`. Before reuse, verify that an existing path is a registered worktree for this repository; never overwrite foreign content. On first use, announce its path, approximate disk cost, and multi-minute first import, then create it with `git worktree add --detach "<project-dir>-agent-tests/" "<committed-sha>"`. On every use, refresh it with `git -C "<project-dir>-agent-tests/" checkout --detach "<committed-sha>"`. Its gitignored `Library/` remains in place. Run the appropriate headless command there once while the main Editor remains open and usable.
2. **Licensing or lock fallback.** If rung 1 fails because of licensing or a project lock, ask the user to close the Editor once. After it closes, the agent runs the headless command once in the main checkout. Never delegate the test run to the user.
3. **Decline or unattended fallback.** Never launch a GUI and never refuse silently. A decline reports `not-executed`. Treat unattended non-response as a decline and report exactly `not-executed: editor open, user unavailable`.

The one shadow worktree persists indefinitely. Per-run worktree creation is an anti-pattern because it discards `Library/` and repeats the cold import. Teardown is manual only: after validating the fixed path belongs to this repository, the maintainer may run `git -C "<main-checkout>" worktree remove "<project-dir>-agent-tests/"`. Never automate teardown.

**Reading the results XML.** Exit code zero is not evidence. Root `<test-run total= passed= failed=>` gives the counts; failing test names come from `<test-case result="Failed">`. A run reporting zero tests discovered is `not-executed`.

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

- The **Preflight (#2)** has already verified that every new `using` directive maps to an explicit `.asmdef` reference — do not skip it.
- Reference assemblies by GUID in `.asmdef` files when possible (more robust to renames).
- `TheMovies.Core.Data` must have zero direct Unity assembly references (pure C# data layer).
- Verify the dependency DAG: Data ← Simulation ← Rendering, Data ← UI, etc. No circular references.

## Input System

- The **Preflight (#1)** has already determined `activeInputHandler` — read the Preflight block in the implementation record.
- If using "Both" mode, prefer migrating to Input System actions over adding more legacy `Input.GetKeyDown()` calls.
- Legacy input calls accumulate tech debt — each new `Input.GetKeyDown()` is one more thing to migrate later.

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

1. **Ensure the capture package is a dependency — default to the bundled companion.** This agent
   pack ships with a companion capture package; wire it by default so a fresh repo needs no manual
   setup. Unless the project documents an override, ensure `Packages/manifest.json` contains the
   dependency **and** a top-level `testables` entry (note `testables` is a sibling of `dependencies`,
   not nested inside it):
   ```jsonc
   {
     "dependencies": {
       "com.threnjen.visual-verification": "https://github.com/threnjen/thren-agentic-workflows.git?path=/packages/com.threnjen.visual-verification#com.threnjen.visual-verification/v0.2.1"
       // …existing dependencies…
     },
     "testables": [ "com.threnjen.visual-verification" ]
   }
   ```
   If the project documents a different capture package (a fork, or a newer tag), use that instead.
   This is the single source for the default — bump the pinned `com.threnjen.visual-verification/vX.Y.Z` tag here
   when the companion package releases. (The default resolves only if the companion repo is reachable
   from the consuming machine; for private forks, document the override.)
2. **Create or update the capture config.** Ensure `Assets/VisualVerification/capture-config.json`
   (root layout) or `game/Assets/VisualVerification/capture-config.json` (nested layout) exists,
   with an entry for the scene this feature renders: the scene name, resolution, and capture
   frames **chosen to fit the AC** — they are not a fixed magic list. A static-layout AC ("two
   teams in distinct colors") needs only one settled frame. A motion/animation AC ("units close
   on each other", "the cube rotates") needs several well-spread frames including an intermediate
   one, because endpoints can coincide (e.g. a 90° rotation of a symmetric object looks like 0°).
   Reuse the existing config if the scene is already covered.
3. **Confirm the scene is loadable.** The capture loads the scene by name, so it must be in Build
   Settings and have a `MainCamera`-tagged camera.

Record in the implementation record which scene the config covers and which visual ACs the captured
frames are meant to demonstrate, so the Visual Verifier (and the orchestrator's visual gate) have a
clear target.

## Pre-Handoff Checklist (Unity-Specific)

Before writing the implementation record, confirm each of these. Items 1–4 are covered by the Preflight section above — this checklist is a final verification pass, not a substitute.

1. **Preflight complete** — Re-read the `## Preflight` block in your implementation record. Does it cover all four checks (input, assemblies, scene wiring, pipeline)? If any are missing, go back and do them before proceeding.
2. **Bootstrap updated** — If the feature adds a new system, is it initialized in the bootstrap script in the correct order?
3. **Def wiring** — If new CompProperties or Def fields were added, does `DefLoader`/`DefSerializer` know how to deserialize them? Is the naming convention followed (`CompX` → `CompProperties_X`)?
4. **TickerType match** — If a new `ThingComp` overrides `CompTickRare` or `CompTickLong`, does the parent Thing's Def set the matching `tickerType`?
5. **PlacedSize vs def.size** — Any code computing building footprints uses `Building.PlacedSize` (the actual placed/rotated size), NOT `def.size` (blueprint size).
6. **Serialized assets generated, not hand-written** — Any new/changed `.prefab`/`.unity`/`.mat`/`.asset` was produced via the Unity Editor API (batch-mode `Editor/` script), not hand-authored YAML. No fabricated GUIDs, no `0000…f000` `m_Script` references, no missing required components or dangling asset references. See "Serialized Assets: Generate via Unity, Never Hand-Author".
7. **Visual test wired** — For a View feature with visual ACs, is the capture config present for this scene and the capture package a dependency listed under `testables`? Is the scene in Build Settings with a `MainCamera`? See "Visual Verification Wiring".
