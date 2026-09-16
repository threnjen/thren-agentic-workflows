---
name: unity-development
description: "Implementation and review rules for Unity C# projects. Covers runtime wiring, MonoBehaviour lifecycle, UI Toolkit pitfalls, test authenticity, bootstrap verification, and batch compilation gates. Load when: implementing or reviewing code in a Unity project - detected by the canonical Unity predicate in tech-stack-detection: Assets/ + ProjectSettings/ at the repo root or inside one nested directory (e.g. game/Assets/), or .github/copilot-instructions.md identifying the project as Unity, or a plan or phase document targeting Unity, MonoBehaviour, or Unity-specific systems. *.asmdef files corroborate but are not required."
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->
# Unity Development Skill

These rules apply to Unity C# projects. They supplement standard implementation and review workflows. They do not replace them.

## Preflight (read these files before writing any code)

Before writing Unity-specific code, read the following project files. Record each finding in the implementation record's summary. These checks are required. Skipping one may lead to incorrect assumptions.

### 1. Input handling mode
**Read:** `ProjectSettings/ProjectSettings.asset` — search for `activeInputHandler:`.

| Value | Meaning | What to use |
|-------|---------|-------------|
| `0` | Legacy input | `Input.GetMouseButtonDown`, `Input.mousePosition`, etc. |
| `1` | New Input System | `Mouse.current.leftButton.wasPressedThisFrame`, etc. |
| `2` | Both | Prefer new Input System API. Legacy calls still work |

**Record in implementation record:** `activeInputHandler: <value> — using <which API>`.

### 2. Assembly reference graph
**Read:** the `.asmdef` file for every assembly you will create or modify. For the View layer, read `Assets/Scripts/View/Combat/View.asmdef`. For Controllers, read `Assets/Scripts/Controllers/Controllers.asmdef`. For Tests, find the project's EditMode test assembly. The verified reference convention places it under `Assets/Tests/Editor/`.

For each new `using` directive you add to a `.cs` file, confirm that its assembly appears in that `.asmdef` file's `"references"` array. A known implicit dependency also satisfies this rule, including `System`, `System.Collections.Generic`, and `UnityEngine` when `noEngineReferences` is `false`.

**Record in implementation record:** every new assembly reference added and why.

### 3. Scene wiring (MonoBehaviours only)
**Read:** the relevant `.unity` scene file (e.g., `Assets/Scenes/CombatSandbox.unity`).

If your feature creates a new `MonoBehaviour`, one of these must be true:
- The component is attached to a GameObject in the scene (visible in the scene YAML under the component's `m_Script` GUID).
- An existing MonoBehaviour calls `AddComponent<T>()` to create it at runtime (find the call site).
- It is instantiated from a prefab (find the prefab and confirm the component is on it).

If none of these are true, the component is **dead code**. Unity will never instantiate it or call its `Awake`/`Start`/`Update` methods. Every method on it is unreachable.

**Record in implementation record:** "`[ComponentName]` is attached to `[GameObject]` via [scene / AddComponent at X / prefab at Y]."

### 4. Render pipeline
**Read:** `Project Settings > Graphics` (or `Assets/` for the active pipeline asset) or search for `ScriptableRendererFeature`/`UniversalRenderPipelineAsset` in the project.

If your feature creates any renderable object at runtime (`new GameObject(..., typeof(LineRenderer))`, `new GameObject(..., typeof(SpriteRenderer))`, `new GameObject(..., typeof(MeshRenderer))`), confirm that the material you assign is compatible with the active pipeline. Apply the same check to Unity's default material:
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

This block records the project-configuration decisions that you made and verified. The reviewer does not need to derive them again.

---

## C# Carve-outs Inside Unity Assemblies

General C# standards (`csharp-standards`, `instructions/csharp-style.instructions.md`) apply with these Unity-only overrides. These overrides apply only inside Unity assemblies. Each rule states its reason.

- **Never use `?.`, `??`, or `??=` on a `UnityEngine.Object` subclass** (`GameObject`, `Component`, MonoBehaviour, `ScriptableObject`). Unity overloads `==`/`!=`. A *destroyed* object compares equal to `null` while its managed reference is not null. The null-conditional and null-coalescing operators bypass that overload and see the live reference. Therefore, `destroyed?.transform` still executes. `_cached ??= GetComponent<T>()` keeps a destroyed component forever. Use an explicit `== null` / `!= null` check.
  ```csharp
  // NEVER
  var t = _maybeDestroyed?.transform;
  _cached ??= GetComponent<Rigidbody>();
  // MUST
  if (_maybeDestroyed != null) { var t = _maybeDestroyed.transform; }
  if (_cached == null) { _cached = GetComponent<Rigidbody>(); }
  ```
- **`[SerializeField]` private fields are `camelCase` with no leading underscore**, and are never `readonly` or `init`. The Inspector derives its label from the field name. The deserializer assigns the fields after construction. Non-serialized private fields keep `_camelCase`. The attribute distinguishes the two forms. Do not widen them to a public setter.
- **Types serialized by `JsonUtility` are `[Serializable] class`/`struct` with public fields**, not `record`. `JsonUtility` ignores records, `init` setters, and properties. A `record` DTO silently round-trips as all-default. With Newtonsoft.Json or System.Text.Json, the general `record` rule applies.
- **Enable nullable reference types per assembly, not via `.csproj`**. Unity regenerates project settings on every import. A per-`.asmdef` `csc.rsp` is not honored. Use `Assets/csc.rsp` containing `-nullable:enable` for the predefined `Assembly-CSharp`. Add a file-scoped `#nullable enable` at the top of every file in an `.asmdef` assembly. Enable pure-domain assemblies (no `UnityEngine` surface) first. The engine boundary generates noise that buries real findings.
- **`record` and `init` need an `IsExternalInit` polyfill**. Unity's .NET Standard 2.1 runtime omits it. The compiler then fails with `CS0518`. Add one `internal static class IsExternalInit { }` in `namespace System.Runtime.CompilerServices` per assembly.
- **Never touch the Unity API from a `Task` continuation without marshalling back to the main thread**. Continuations do not resume on the main thread. Most engine APIs throw when called off it. Use coroutines or `Awaitable`/`UniTask` for frame-paced logic. Reserve `Task` for background I/O at the edge.

## Runtime Wiring Rules

Every feature must be reachable at runtime. Unity does not auto-discover or auto-wire pure C# classes.

### 1. Every New System Needs an Explicit Caller

- **MonoBehaviours** receive calls from Unity's lifecycle (`Awake`, `Start`, `Update`, etc.). Unity calls them only when they are attached to an active GameObject in the scene or created via `AddComponent<T>()`.
- **Pure C# classes** (state machines, managers, subsystems) have no lifecycle. If a class has per-frame methods (e.g., `UpdateCursor()`, `Tick()`, `Process()`), a MonoBehaviour must call them from its `Update()` or equivalent.
- **For every new class**, document in the implementation record: "Called by [X] in [Y method]"

### 2. Bootstrap / Entry Point Verification

If the project has a bootstrap script (e.g., `GameBootstrap.cs`, a scene initializer):

- Every new system that needs initialization must be added to the bootstrap
- Check that dependencies initialize before dependents.
- If the bootstrap uses `[RuntimeInitializeOnLoadMethod]`, the initialization runs before scene objects are available
- After modifying the bootstrap, read the whole file and verify the full initialization chain. Do not append blindly.

### 3. Map/Registry Integration

If the project uses a Map, Grid, or entity registry pattern:

- New entity types must be registered via the project's spawn/despawn pipeline (e.g., `Map.NotifySpawned()`)
- Do not register entities directly in tests when production code uses a different path. Direct registration hides integration gaps.
- Verify that all subsystems that need spawn/despawn awareness are wired into the notification chain

## MonoBehaviour Lifecycle Gotchas

- **`AddComponent<T>()` triggers `Awake()` synchronously.** Fields set after the `AddComponent` call are not available in `Awake()`. Use `Start()` or a deferred init method for anything set post-construction.
- **`Destroy()` is deferred to end of frame.** `DestroyImmediate()` runs immediately but should only be used in Editor code or tests. Do not rely on `Destroy()` having taken effect within the same frame.
- **Execution order is not guaranteed** between MonoBehaviours unless explicitly set via Script Execution Order or `[DefaultExecutionOrder]`.

## UI Toolkit Rules

### ScrollView Child Routing

`ScrollView` routes `Add()` calls to its internal `contentContainer`. `childCount` and `Children()` enumerate the root element's direct children, such as scroll bars and the viewport. **Always use**:

```csharp
scrollView.contentContainer.childCount    // NOT scrollView.childCount
scrollView.contentContainer.Children()    // NOT scrollView.Children()
```

This bug has recurred multiple times. It is the most common UI Toolkit mistake in this pipeline.

### VisualTreeAsset Instantiation

- Use `visualTreeAsset.CloneTree(parent)`. Do not use `visualTreeAsset.Instantiate()`.
- `Instantiate()` wraps content in a `TemplateContainer` that breaks `position: absolute` layout

### Stylesheet Loading

- Reference stylesheets from UXML via `<Style src="...">`. Do not use `Resources.Load<StyleSheet>()`.
- `Resources.Load<StyleSheet>()` is unreliable in Unity 6

### PanelSettings

- `UIDocument` requires a `PanelSettings` asset with a theme to render
- Runtime-created `PanelSettings` via `ScriptableObject.CreateInstance` lacks the default theme
- Load a pre-created asset via `Resources.Load<PanelSettings>()`

### Tooltip Testing

- Use `VisualElement.tooltip` when tests only need to verify the tooltip property state.
- If EditMode panel tests must verify hover-triggered tooltip visibility, assume native tooltip behavior is insufficient unless the codebase already proves otherwise.
- For hover visibility, prefer a small runtime overlay driven by `PointerEnterEvent` and `PointerLeaveEvent`. Use the real panel/controller structure in tests.
- For plans that touch UI Toolkit tooltips, mark related `.uxml`, `.uss`, and test root builder files as `(verify)` when companion changes are uncertain.

### Working Code + Warning ≠ Broken

- Do not replace working UI code to suppress cosmetic warnings (e.g., "No Theme Style Sheet").
- Never add an early `return` that gates all downstream functionality on an optional dependency
- If the current approach works, make improvements additive, not replacements

## Refactor / Rewire Test Preservation Rules

- Before planning a refactor, runtime rewire, API change, or behavior change, inventory the affected Unity tests and harnesses. Include the project's EditMode directory (verified reference convention: `Assets/Tests/Editor`), `Assets/Tests/PlayMode`, phase-scoped or editor tests, and UI Toolkit test root builders. Plan these files as part of the work. Do not defer them as cleanup.
- If the change alters a public API, bootstrap path, serialized asset layout, scene wiring, prefab, event contract, or lifecycle behavior, assume related tests will need updates. Include those files in the plan's scope and verification assets.
- When a Unity test becomes obsolete because production behavior changed, update or retire it in the same feature. Document the reason. Leave no orphaned or silently broken tests behind.
- For controller, UI Toolkit, or scene-wiring changes, include the corresponding test assembly and test root builder files in the planned scope. State whether each file needs test updates.

## Test Execution

Unity Test Framework is the authoritative runner. Compilation success and focused harnesses do not count as test execution. See the `test-execution-evidence` instruction.

`-batchmode` is mandatory for every agent-driven Unity test run. Never assume a bare `Unity` executable is on `PATH`.

**Editor discovery.** Resolve the editor path in this order. Stop at the first hit:

1. Use the `VISUAL_VERIFICATION_UNITY` environment variable if it is set. The name is historical. The path is machine-wide and applies to every Unity run, not only capture runs.
2. Use the machine-local override file `dev/com.threnjen.visual-verification.local.json` if it exists. It must contain `{ "unityEditorPath": "…" }`. The filename is historical.
3. Derive the path from the project's Unity version in `<execution-unity-project>/ProjectSettings/ProjectVersion.txt` and the Unity Hub layout. Check the default location (`…/Hub/Editor/<version>/Editor/Unity.exe`). Also check any custom editor-install location recorded in the Hub config. Hub config uses `%APPDATA%/UnityHub/` on Windows, `~/Library/Application Support/UnityHub/` on macOS, and `~/.config/UnityHub/` on Linux. This covers an editor relocated to another drive.

This skill is the single canonical implementation of editor discovery.

**Project paths.** Resolve `<main-repo-root>` as the Git checkout root. Resolve `<unity-project-relative-path>` as `.` for a root Unity layout, or as the nested directory containing `Assets/` and `ProjectSettings/`, such as `game`. A shadow `<worktree-root>` is a checkout of the whole repository. Set `<execution-unity-project>` to `<worktree-root>/<unity-project-relative-path>`. For the main-checkout fallback, use `<main-repo-root>/<unity-project-relative-path>`. Never pass a monorepo root without a Unity project to `-projectPath`.

| Platform | Required flags |
|----------|----------------|
| EditMode | `-batchmode -nographics` |
| PlayMode | `-batchmode` with graphics enabled. They exclude `-nographics` |

```bash
"<resolved-unity-editor>" -batchmode -nographics -runTests -projectPath "<execution-unity-project>" -testPlatform EditMode -testResults "<absolute-main-checkout>/dev/test-results/<results.xml>" -logFile "<absolute-main-checkout>/dev/test-results/<unity.log>"
"<resolved-unity-editor>" -batchmode -runTests -projectPath "<execution-unity-project>" -testPlatform PlayMode -testResults "<absolute-main-checkout>/dev/test-results/<results.xml>" -logFile "<absolute-main-checkout>/dev/test-results/<unity.log>"
```

- Never pair `-quit` with `-runTests`. Unity can exit before the tests execute and return a false-green zero exit code.
- **Affected-suite runs use `-testFilter`**. Use a semicolon-separated list of full test names or a regex, with negation supported. Scope the filter to the suites that exercise the changed symbol. Gate runs (feature integration gate, phase end) are unfiltered.
- `-testResults` always receives an absolute path under the main checkout's `dev/test-results/`. `-logFile` uses the same absolute artifact directory. The shadow worktree is an execution target only. Never read results from the shadow worktree. Never read logs from it either.

**Precondition.** Commit before testing in a shadow worktree. It can represent only committed code. The normal per-feature commit usually satisfies this precondition. A dirty checkout requires a commit before this procedure begins.

### Execution Ladder

1. **Persistent shadow worktree.** From `<main-repo-root>`, run `git worktree prune`. Then use the one fixed detached sibling `<project-dir>-agent-tests/` as `<worktree-root>`. Before reuse, verify that the existing path is a registered worktree for this repository. Never overwrite foreign content. On first use, announce its path, approximate disk cost, and multi-minute first import. Then create it with `git worktree add --detach "<project-dir>-agent-tests/" "<committed-sha>"`. On every use, refresh it with `git -C "<project-dir>-agent-tests/" checkout --detach "<committed-sha>"`. Before running Unity, verify that the worktree has no tracked changes or untracked files and no ignored content outside `<execution-unity-project>/Library/` (or its root-layout equivalent). Otherwise, stop and report `not-executed` without deleting or overwriting anything. Its gitignored `Library/` remains in place. Run the appropriate headless command against `<execution-unity-project>` once while the main Editor remains open and usable.
2. **Licensing or lock fallback.** If rung 1 fails because of licensing or a project lock, ask the user to close the Editor once. After it closes, the agent runs the headless command once in the main checkout. Never delegate the test run to the user.
3. **Decline or unattended fallback.** Never launch a GUI and never refuse silently. A decline reports `not-executed`. Treat unattended non-response as a decline and report exactly `not-executed: editor open, user unavailable`.

The one shadow worktree persists indefinitely. Per-run worktree creation is an anti-pattern. It discards `Library/` and repeats the cold import. Teardown is manual only. After validating that the fixed path belongs to this repository, the maintainer may run `git -C "<main-checkout>" worktree remove "<project-dir>-agent-tests/"`. Never automate teardown.

**Reading the results XML.** Exit code zero is not evidence. Root `<test-run total= passed= failed=>` gives the counts. Failing test names come from `<test-case result="Failed">`. A run reporting zero tests discovered is `not-executed`.

## Test Authenticity Rules

### Do Not Mock Framework Types with Simplified Stand-ins

When tests substitute a plain `VisualElement` for a `ScrollView`, the test will pass while runtime breaks. The same risk applies to any framework widget with different internal routing or behavior. This pattern has caused repeated bugs.

**Rule:** If the code under test interacts with framework-specific behavior (child routing, layout, event bubbling), use the real framework type in tests or document the gap explicitly.

### Do Not Bypass the Spawn/Registration Pipeline

Tests may call `RegisterTickable()`, `AddToGrid()`, or similar registration methods directly. If production code goes through `Map.NotifySpawned()` or an equivalent path, those tests will pass while runtime integration remains broken.

**Rule:** Tests should exercise the same code paths as production wherever possible. If a shortcut is necessary for test isolation, add a comment: `// NOTE: Bypasses Map.NotifySpawned() — integration tested in [X]`.

### Verify Event Handlers Do Real Work

Tests that verify "event was fired" are necessary but insufficient. If a UI confirm button fires an event but the handler only hides panels, the test passes while the feature fails. Also verify the domain action, such as `building.Destroy()`.

**Rule:** For any event handler test, also verify the downstream side effect, such as an entity destroyed or state changed. Otherwise, note the gap in the implementation record.

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

- Do not allocate `MaterialPropertyBlock`, `List<T>`, or other objects inside per-frame rendering methods.
- Cache those objects as instance fields and reuse them.
- Unity's GC is generational. Frequent small allocations still cause frame hitches.

### Batch Renderer State Changes

Batch renderers that rebuild only on add/remove do not reflect per-entity state changes, such as degradation tinting. Use dirty flags or periodic polling to trigger rebuilds when state changes.

## Shader Safety

- Verify that each `Shader.Find()` string argument exists in the target Unity version.
- For opaque colored quads, use an opaque shader (`Unlit/Color`, custom vertex color). Do not use `Sprites/Default`, which is a transparency shader.
- Safe built-in shaders include `Sprites/Default`, `Unlit/Color`, and `Standard`.

## Assembly Definition Conventions

- The **Preflight (#2)** check already confirms that every new `using` directive maps to an explicit `.asmdef` reference. Do not skip it.
- Reference assemblies by GUID in `.asmdef` files when possible (more robust to renames).
- `TheMovies.Core.Data` must have zero direct Unity assembly references (pure C# data layer).
- Verify the dependency DAG: Data ← Simulation ← Rendering and Data ← UI. Do not add circular references.

## Input System

- The **Preflight (#1)** check already determined `activeInputHandler`. Read the Preflight block in the implementation record.
- If using "Both" mode, prefer migrating to Input System actions over adding more legacy `Input.GetKeyDown()` calls.
- Legacy input calls accumulate tech debt. Each new `Input.GetKeyDown()` call adds another migration task.

## Save/Load Considerations

- After loading, rewire all subsystems to the new object instances, such as Grid and Map.
- A `LoadManager` that replaces references without notifying subsystems produces stale-reference bugs. These bugs remain invisible until the player loads a save.
- Verify that every subsystem holding a Grid/Map reference gets updated after load.

## Serialized Assets: Generate via Unity, Never Hand-Author

Unity's serializer produces `.prefab`, `.unity` scenes, `.mat`, `.asset` files (including SRP pipeline/renderer assets), and `.meta` files. The Editor is the sole authority for GUIDs, fileIDs, class ids, required-component dependencies, and version-correct format. An agent that hand-writes these files impersonates that serializer **blind**. The agent has no access to the real GUID database, no component-dependency enforcement, and no way to validate the output. This is the single most common source of "compiles green, tests pass, but nothing renders / NRE every frame" failures.

**Headless asset-database import.** Use `"<resolved-unity-editor>" -batchmode -quit -projectPath "<execution-unity-project>" -logFile -`. Use the editor and root-or-nested Unity project path resolved by Test Execution. For a controlled main-checkout check, `<execution-unity-project>` is `<main-repo-root>/<unity-project-relative-path>`. This asks Unity's asset database to import and generate missing `.meta`/GUID files without a human-opened or GUI-opened Editor. The rule is: treat regeneration as unverified until a controlled missing-`.meta` run succeeds on the target Unity version. Unity Editor's serializer remains the sole authority for every generated file.

**Rule: do not hand-author serialized Unity assets from scratch.** Build them by running the Unity Editor API in batch mode (an `Editor/` script Unity executes), so Unity generates the asset, its GUIDs, and its `.meta`:

- Prefabs → construct the GameObject with `new GameObject(...)` + `AddComponent<T>()`, then `PrefabUtility.SaveAsPrefabAsset`.
- Scenes → `EditorSceneManager.NewScene`/`OpenScene`, build contents, `EditorSceneManager.SaveScene`.
- Materials / ScriptableObjects / SRP assets → `new Material(Shader.Find(...))` / `ScriptableObject.CreateInstance<T>()` (or the type's `Create()` helper) + `AssetDatabase.CreateAsset`.
- Sprites/textures → import a real source file. Never invent a texture/sprite `.meta` GUID.

Run via `-batchmode -executeMethod <Type>.<Method> -quit`. Then confirm that the assets imported without errors.

**Boundary:** a *surgical edit* to an existing, Unity-generated asset is acceptable. This means changing a serialized value in a file the Editor already produced. *Authoring a whole asset as raw YAML* is the anti-pattern. The risk is highest in unattended pipeline runs where no human Play-tests each step.

### Invalid-asset red flags (when producing OR reviewing any serialized asset)

- A `MonoBehaviour.m_Script` GUID of `0000000000000000f000000000000000` is builtin-extra. It is valid only for builtin fonts, textures, and materials, and **never** for a script. Any `m_Script`/asset GUID without a matching `.cs.meta` or package meta produces a silent "missing script" and `null` at runtime.
- A class-id tag must match the component body. `SpriteRenderer` is `!u!212`, not `!u!23` (`MeshRenderer`). UI elements need `RectTransform` (`!u!224`), not `Transform` (`!u!4`).
- **(uGUI / legacy UI only)** A UI `Graphic` (`Image`/`Text`) needs its required `CanvasRenderer` (`!u!222`) and `RectTransform`. A `Canvas` needs a `RectTransform`. UI Toolkit projects use `UIDocument`/`PanelSettings` instead. This check does not apply to them.
- An asset reference (`m_Sprite`, `m_Materials`, `m_Font`, renderer/pipeline) must point to a GUID defined by an existing `.meta` file. Otherwise, the dangling reference renders nothing and reports no error.
- **(URP only)** The render-pipeline chain must resolve fully: `QualitySettings`/`GraphicsSettings` → URP pipeline `.asset` → renderer `.asset`. All links must exist. A missing link silently disables sprite/line rendering with no console error. Built-in Render Pipeline projects have no such chain.
- A serialized field reported as "wired" must target a component whose script GUID resolves. A present fileID is **not** proof that the reference resolves.


## Pre-Handoff Checklist (Unity-Specific)

Before writing the implementation record, confirm each item. The Preflight section covers items 1–4. This checklist is a final verification pass, not a substitute.

1. **Preflight complete** — Re-read the `## Preflight` block in your implementation record. Check that it covers all four checks: input, assemblies, scene wiring, and pipeline. If any check is missing, complete it before proceeding.
2. **Bootstrap updated** — If the feature adds a new system, verify that the bootstrap script initializes it in the correct order.
3. **Def wiring** — If new CompProperties or Def fields were added, check that `DefLoader`/`DefSerializer` can deserialize them. Check that the naming convention is followed (`CompX` → `CompProperties_X`).
4. **TickerType match** — If a new `ThingComp` overrides `CompTickRare` or `CompTickLong`, check that the parent Thing's Def sets the matching `tickerType`.
5. **PlacedSize vs def.size** — Code that computes building footprints must use `Building.PlacedSize` (the actual placed/rotated size), not `def.size` (blueprint size).
6. **Serialized assets generated, not hand-written** — Any new or changed `.prefab`/`.unity`/`.mat`/`.asset` must be produced via the Unity Editor API (batch-mode `Editor/` script), not hand-authored YAML. Do not fabricate GUIDs. Do not use `0000…f000` `m_Script` references. Do not omit required components or leave dangling asset references. See "Serialized Assets: Generate via Unity, Never Hand-Author".
