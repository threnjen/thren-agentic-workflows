# Performance & Profiling Review Rules

*Distilled from: Ultimate Guide to Profiling Games (Unity 6 edition) + Optimize your game performance for consoles and PCs (Unity 6 edition)*

---

## Garbage Collection & Memory

### Zero-Allocation Gameplay Loop

The target is **zero GC allocations in Update/LateUpdate/FixedUpdate**. Flag each item below when it appears in a hot path:

- Avoid string creation and manipulation in hot paths. Use `StringBuilder` for runtime string building.
- Use `CompareTag()` instead of comparing `GameObject.tag`. This avoids string allocation.
- Cache and reuse `new WaitForSeconds()` instances in coroutines.
- Avoid LINQ expressions because they involve hidden boxing and enumerator allocation.
- Avoid regular expressions in hot paths. They allocate behind the scenes.
- Avoid lambda captures in hot paths. Lambdas that capture `this`, instance members, or locals create delegates and GC traffic.
- Do not declare or populate `List<T>` or other collections every frame. Make them class members. Call `Clear()` each frame.
- Cache arrays returned from Unity APIs.
- Avoid boxing value types (int/float/struct → object). Use concrete generics.

### GC Timing

- Call `GC.Collect()` only during non-interactive moments, such as loading screens and menus.
- Enable Incremental GC to spread collection across frames. Read-write barriers add ~1ms overhead per frame.

### Memory Budget

- Profile on the lowest-spec target device.
- Use ~80–90% of physical RAM as the budget, not 100%.
- For mobile, reserve ~35% of frame time as idle time for thermal throttling. Use a 22ms budget for 30fps, not 33.33ms.

---

## CPU Optimization

### Update Loop Rules

- **Remove empty `Update()`, `LateUpdate()`, and `FixedUpdate()` methods.** Empty methods still have overhead.
- Execute logic only when the state changes. Do not execute logic every frame.
- Time-slice expensive work by using `if (Time.frameCount % interval == 0)` or by processing 1/N of the data each frame.

### Caching

- Cache `GetComponent<T>()` in `Awake()` or `Start()`. Never call it in `Update()`.
- Cache a `Camera.main` reference.
- Use `Animator.StringToHash()` and `Shader.PropertyToID()`. Cache the resulting hash values.

### API & Interop

- Do not use `AddComponent<T>()` at runtime. Instantiate prefabs with components pre-attached.
- Use `Transform.SetPositionAndRotation()` to update both in one call.
- Minimize C#↔C++ interop boundary crossings. Use a custom `UpdateManager` for thousands of objects.

### Object Pooling

- Use the `UnityEngine.Pool` namespace (Unity 2021+) for frequently instantiated and destroyed objects.
- Initialize pools during loading screens before gameplay starts.
- Set a maximum pool size to prevent unbounded growth.

### Data & Algorithms

- Choose the correct collection for each use case: List, Array, or Dictionary.
- Avoid LINQ in performance-critical code.
- Use `StringBuilder` for string concatenation.

---

## GPU & Rendering

### Draw Call Reduction

- **Static Batching**: Mark non-moving meshes as Batching Static.
- **GPU Instancing**: Enable GPU Instancing on materials with identical mesh and material (trees, buildings, grass).
- **SRP Batcher**: Enable the SRP Batcher in the Pipeline Asset. Minimize Shader Variants and Keywords.
- Use `Renderer.sharedMaterial`, not `Renderer.material`. This avoids material instance creation.
- Use texture atlases. Fewer materials produce fewer draw calls.
- Use the Frame Debugger (Window > Analysis > Frame Debugger) to identify unnecessary draws.

### Culling

- Use `Camera.layerCullDistances` for distance culling by layer.
- Enable Occlusion Culling for complex indoor scenes. Mark objects as Occluders or Occludees.
- Use GPU Resident Drawer and GPU Occlusion Culling in Unity 6 to reduce draw calls automatically.

### Shader Rules

- Remove unused nodes from Shader Graphs.
- Bake values into textures instead of computing them in a shader (pre-brighten texture > brightness node).
- Use `half` precision instead of `float` on mobile.
- Reduce branching. Blend instead of using if/else.
- Use `#pragma shader_feature`, not `multi_compile`, for material-specific variants. Unused variants get stripped.
- Strip unused shaders from Graphics Settings → Always Included.

### Overdraw

- Minimize overlapping transparent geometry.
- Reduce particle system overlap.
- Consolidate overlapping UI elements.
- Visualize overdraw in Scene view > Overdraw mode (Built-in) or Rendering Debugger > TransparencyOverdraw (HDRP).

### LOD & Dynamic Resolution

- Use LOD Groups with lower-res meshes and simpler materials at distance.
- Enable Dynamic Resolution (`Camera.allowDynamicResolution`) for GPU-bound frames.

---

## Textures & Meshes

### Texture Rules

- Use power-of-two sizes for compression compatibility.
- **Disable Read/Write** unless generating textures at runtime. Read/Write doubles memory.
- Disable mipmaps for fixed-size sprites and UI (2D). Keep mipmaps for 3D distance rendering.
- Enable Texture Streaming (Quality Settings) for large 3D scenes.
- Use ASTC (iOS/Android) and BC7/DXT1 (PC/Console) compression formats.

### Mesh Rules

- Enable Mesh Compression. It reduces disk usage, not runtime memory.
- **Disable Read/Write** on meshes. Read/Write duplicates mesh data in memory. The default was enabled pre-2019.2.
- Disable rigs and BlendShapes if they are not animated.
- Enable `Optimize Mesh Data` to strip unused vertex attributes.
- Use Player Settings > Vertex Compression for per-channel compression.

---

## Physics

- Replace mesh colliders with primitives or simplified geometry.
- Enable `Prebake Collision Meshes`.
- Simplify the Layer Collision Matrix to the minimum required.
- Use non-allocating physics queries. Use `OverlapSphereNonAlloc` and batch `RaycastCommand` with Job System.
- Disable `autoSyncTransforms`. Call `Physics.SyncTransforms()` manually when needed.
- Move a Rigidbody via `Rigidbody.position` or `Rigidbody.MovePosition()`, not `transform.position`.
- Run physics in `FixedUpdate()`, never in `Update()`.

---

## Animation

- Prefer Generic rigs over Humanoid when possible. Humanoid uses 30–50% more CPU from IK/retargeting.
- Do not use Animator for simple tweens. Use DOTween or easing functions.
- Avoid scale curves in animation clips. Translation and rotation are cheaper.
- Set Culling Mode to "Based on Renderers". Disable "Update When Offscreen".
- Use `Animator.StringToHash()` for parameter lookups.
- Separate animating hierarchies. Do not share common parents because they create a threading bottleneck.

---

## Audio

- Set Force To Mono on spatial audio sources. Stereo uses 2x memory and CPU conversion.
- Set Load Type by size: use Decompress On Load for <200KB and Streaming for >350KB.
- Use a 22050Hz sample rate on mobile. It is sufficient. Never use 48000Hz.
- Minimize SFX Reverb groups. They are expensive even with no signal.
- Avoid single-child mixer groups. Combine them into one.

---

## UI

### UGUI

- Split the UI into multiple Canvases by update frequency, such as static and dynamic.
- Disable Raycast Target on non-interactive elements.
- Disable GraphicRaycaster on non-interactive Canvases.
- Avoid Layout Groups because they are inherently expensive. Use anchors instead.
- Reuse pooled UI elements for large lists. Do not create 1 element per item.
- Disable the Canvas component, not the GameObject, to hide the UI without rebuilding the mesh.
- For fullscreen UI, disable the 3D camera and background Canvases.

### UI Toolkit (Recommended for Unity 6)

- Use lean stylesheets with minimal selectors.
- Run heavy operations during initialization, not per frame.
- Unsubscribe event handlers when no longer needed.

---

## Profiling Methodology

### Frame Budget

| Target | Budget | Notes |
|--------|--------|-------|
| 60 fps | 16.66 ms | Desktop/console target |
| 30 fps | 33.33 ms | Mobile acceptable |
| 30 fps (mobile thermal) | ~22 ms | Reserve 35% for cooling headroom |

**Always measure in milliseconds, not FPS.** FPS is deceptive. A 1.11ms regression looks like only a 4 FPS drop at 60fps, but it has the same absolute cost.

### CPU vs GPU Bound

- **CPU-bound**: `Gfx.WaitForCommands` in Profiler means that the GPU waits for the CPU.
- **GPU-bound**: `Gfx.WaitForPresentOnGfxThread` or `Gfx.PresentFrame` means that the CPU waits for the GPU.
- If the render thread is busy in `Camera.Render`, treat it as a CPU-side bottleneck caused by too many draw calls.

### Profiler Best Practices

- Profile on the target device, not in the Editor. The Editor inflates memory and CPU use.
- Enable only the Profiler modules you need. Each module adds overhead.
- Use `ProfilerMarker` for custom instrumentation without Deep Profiling overhead.
- Use Deep Profiling only for a specific slowdown investigation. It has high overhead.
- Use Profile Analyzer for statistical comparison (before/after).
- Use Memory Profiler snapshots to track leaks over time.

### Debug Stripping

- Remove `Debug.Log()` from builds, especially in Update loops.
- Use the `[System.Diagnostics.Conditional("ENABLE_LOG")]` attribute.
- Disable Stack Trace logging in release builds.

---

## Project Configuration

- Use IL2CPP for release builds because it provides better runtime performance. Use Mono for fast iteration.
- Disable Auto Graphics API. Remove unsupported APIs for each platform.
- Strip unnecessary shader variants.
- Set Asset Serialization to Force Text. Force Text is version-control friendly.
- Use Addressables for asset loading. Disable CRC on consoles.
- Use flat scene hierarchies. Deep nesting adds Transform computation overhead.
