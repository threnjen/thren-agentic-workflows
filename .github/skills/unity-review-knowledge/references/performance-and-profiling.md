# Performance & Profiling Review Rules

*Distilled from: Ultimate Guide to Profiling Games (Unity 6 edition) + Optimize your game performance for consoles and PCs (Unity 6 edition)*

---

## Garbage Collection & Memory

### Zero-Allocation Gameplay Loop

The target is **zero GC allocations in Update/LateUpdate/FixedUpdate**. Flag any of these in hot paths:

- String creation/manipulation — use `StringBuilder` for runtime string building
- `GameObject.tag` comparison — use `CompareTag()` instead (avoids string alloc)
- `new WaitForSeconds()` in coroutines — cache and reuse
- LINQ expressions — hidden boxing and enumerator allocation
- Regular expressions — allocate behind the scenes
- Lambda captures — lambdas capturing `this`, instance members, or locals create delegates + GC traffic
- Declaring/populating `List<T>` or collections every frame — make them class members, call `Clear()` per frame
- Returning arrays from Unity APIs — cache the results
- Boxing value types (int/float/struct → object) — use concrete generics

### GC Timing

- Call `GC.Collect()` only during non-interactive moments (loading screens, menus)
- Enable Incremental GC to spread collection across frames (~1ms overhead per frame from read-write barriers)

### Memory Budget

- Profile on lowest-spec target device
- Use ~80–90% of physical RAM as budget (not 100%)
- Mobile: Reserve ~35% frame time idle for thermal throttling (use 22ms budget for 30fps, not 33.33ms)

---

## CPU Optimization

### Update Loop Rules

- **Remove empty `Update()`, `LateUpdate()`, `FixedUpdate()` methods** — even empty ones have overhead
- Only execute logic when state changes, not every frame
- Time-slice expensive work: `if (Time.frameCount % interval == 0)` or process 1/N of data each frame

### Caching

- Cache `GetComponent<T>()` in `Awake()`/`Start()`, never in `Update()`
- Cache `Camera.main` reference
- Use `Animator.StringToHash()` and `Shader.PropertyToID()` — cache the hash values

### API & Interop

- Don't use `AddComponent<T>()` at runtime — instantiate prefabs with components pre-attached
- Use `Transform.SetPositionAndRotation()` to update both in one call
- Minimize C#↔C++ interop boundary crossings — custom `UpdateManager` for thousands of objects

### Object Pooling

- Use `UnityEngine.Pool` namespace (Unity 2021+) for frequently instantiated/destroyed objects
- Initialize pools during loading screens before gameplay starts
- Set max pool size to prevent unbounded growth

### Data & Algorithms

- Choose correct collection: List vs Array vs Dictionary per use case
- Avoid LINQ in performance-critical code
- Use `StringBuilder` for string concatenation

---

## GPU & Rendering

### Draw Call Reduction

- **Static Batching**: Mark non-moving meshes as Batching Static
- **GPU Instancing**: Enable on materials with identical mesh+material (trees, buildings, grass)
- **SRP Batcher**: Enable in Pipeline Asset; minimize Shader Variants and Keywords
- Use `Renderer.sharedMaterial`, NOT `Renderer.material` (avoids material instance creation)
- Use texture atlases — fewer materials = fewer draw calls
- Use Frame Debugger (Window > Analysis > Frame Debugger) to identify unnecessary draws

### Culling

- Use `Camera.layerCullDistances` for per-layer distance culling
- Enable Occlusion Culling for complex indoor scenes (mark objects as Occluders/Occludees)
- GPU Resident Drawer + GPU Occlusion Culling in Unity 6 for automatic draw call reduction

### Shader Rules

- Remove unused nodes from Shader Graphs
- Bake values into textures instead of computing in shader (pre-brighten texture > brightness node)
- Use `half` precision instead of `float` on mobile
- Reduce branching; blend instead of if/else
- Use `#pragma shader_feature` (not `multi_compile`) for material-specific variants — unused get stripped
- Strip unused shaders from Graphics Settings → Always Included

### Overdraw

- Minimize overlapping transparent geometry
- Reduce particle system overlap
- Consolidate overlapping UI elements
- Visualize: Scene view > Overdraw mode (Built-in) or Rendering Debugger > TransparencyOverdraw (HDRP)

### LOD & Dynamic Resolution

- Use LOD Groups: lower-res meshes + simpler materials at distance
- Enable Dynamic Resolution (`Camera.allowDynamicResolution`) for GPU-bound frames

---

## Textures & Meshes

### Texture Rules

- Use power-of-two sizes for compression compatibility
- **Disable Read/Write** unless generating textures at runtime (doubles memory)
- Disable mipmaps for fixed-size sprites/UI (2D); keep for 3D distance rendering
- Enable Texture Streaming (Quality Settings) for large 3D scenes
- Compression formats: ASTC (iOS/Android), BC7/DXT1 (PC/Console)

### Mesh Rules

- Enable Mesh Compression (reduces disk, not runtime memory)
- **Disable Read/Write** on meshes (duplicates in memory; default was enabled pre-2019.2)
- Disable rigs/BlendShapes if not animated
- Enable `Optimize Mesh Data` to strip unused vertex attributes
- Use Player Settings > Vertex Compression for per-channel compression

---

## Physics

- Replace mesh colliders with primitives or simplified geometry
- Enable `Prebake Collision Meshes`
- Simplify Layer Collision Matrix to minimum needed
- Use non-allocating physics queries: `OverlapSphereNonAlloc`, `RaycastCommand` batch with Job System
- Disable `autoSyncTransforms`; manually call `Physics.SyncTransforms()` when needed
- Move Rigidbody via `Rigidbody.position`/`Rigidbody.MovePosition()`, not `transform.position`
- Physics in `FixedUpdate()`, never in `Update()`

---

## Animation

- Generic rigs over Humanoid when possible (Humanoid = 30–50% more CPU from IK/retargeting)
- Don't use Animator for simple tweens — use DOTween or easing functions
- Avoid scale curves in animation clips (translation/rotation are cheaper)
- Set Culling Mode: "Based on Renderers" + disable "Update When Offscreen"
- Use `Animator.StringToHash()` for parameter lookups
- Separate animating hierarchies — don't share common parents (threading bottleneck)

---

## Audio

- Force To Mono on spatial audio sources (stereo = 2x memory + CPU conversion)
- Load Type by size: <200KB → Decompress On Load; >350KB → Streaming
- Mobile sample rate: 22050Hz sufficient (never 48000Hz)
- Minimize SFX Reverb groups — expensive even with no signal
- Avoid single-child mixer groups — combine into one

---

## UI

### UGUI

- Split into multiple Canvases by update frequency (static vs dynamic)
- Disable Raycast Target on non-interactive elements
- Disable GraphicRaycaster on non-interactive Canvases
- Avoid Layout Groups (inherently expensive); use anchors instead
- Reuse pooled UI elements for large lists (not 1 element per item)
- Disable Canvas component (not GameObject) to hide without mesh rebuild
- Fullscreen UI: disable 3D camera and background Canvases

### UI Toolkit (Recommended for Unity 6)

- Lean stylesheets with minimal selectors
- Heavy operations only during init, not per-frame
- Unsubscribe event handlers when no longer needed

---

## Profiling Methodology

### Frame Budget

| Target | Budget | Notes |
|--------|--------|-------|
| 60 fps | 16.66 ms | Desktop/console target |
| 30 fps | 33.33 ms | Mobile acceptable |
| 30 fps (mobile thermal) | ~22 ms | Reserve 35% for cooling headroom |

**Always measure in milliseconds, not FPS.** FPS is deceptive — a 1.11ms regression looks like only 4 FPS drop at 60fps but is the same absolute cost.

### CPU vs GPU Bound

- **CPU-bound**: `Gfx.WaitForCommands` in Profiler — GPU waiting for CPU
- **GPU-bound**: `Gfx.WaitForPresentOnGfxThread` or `Gfx.PresentFrame` — CPU waiting for GPU
- If render thread busy in `Camera.Render`: CPU-side bottleneck (too many draw calls)

### Profiler Best Practices

- Profile on target device, not Editor (Editor inflates memory/CPU)
- Enable only needed Profiler modules (each adds overhead)
- Use `ProfilerMarker` for custom instrumentation without Deep Profiling overhead
- Deep Profiling: only for specific slowdown investigation (high overhead)
- Use Profile Analyzer for statistical comparison (before/after)
- Use Memory Profiler snapshots to track leaks over time

### Debug Stripping

- Remove `Debug.Log()` from builds, especially in Update loops
- Use `[System.Diagnostics.Conditional("ENABLE_LOG")]` attribute
- Disable Stack Trace logging in release builds

---

## Project Configuration

- IL2CPP for release builds (better runtime performance); Mono for fast iteration
- Disable Auto Graphics API; remove unsupported APIs per platform
- Strip unnecessary shader variants
- Asset Serialization: Force Text (version control friendly)
- Use Addressables for asset loading; disable CRC on consoles
- Flat scene hierarchies (deep nesting = Transform computation overhead)
