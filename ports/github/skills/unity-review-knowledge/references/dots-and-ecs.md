# DOTS & ECS Review Rules

*Distilled from: Introduction to DOTS (Unity 6 edition)*

---

## When to Use DOTS vs MonoBehaviour

DOTS (Data-Oriented Technology Stack) is for **high-volume, data-parallel workloads**: thousands of entities with uniform processing. It is not a replacement for all MonoBehaviour code.

**Use DOTS for:**
- Process thousands of similar entities with DOTS (crowds, bullets, particles, grid cells).
- Use DOTS for CPU-bound simulation that benefits from cache-coherent data layout.
- Use DOTS for workloads that parallelize well across cores (spatial queries, pathfinding, physics).

**Do not use DOTS for:**
- Do not use DOTS for small object counts where MonoBehaviour is sufficient.
- Do not use DOTS for complex unique behaviors per entity (state machines with many branches).
- Do not use DOTS for UI, audio, or other systems with strong Unity API dependencies.
- Do not use DOTS for mixed GameObject/Entity architectures without clear boundaries.

---

## Burst Compiler Rules

- **Flag** managed objects (classes) in Burst code. Burst compiles a subset of C# that excludes class instances.
- **Require** the `[BurstCompile]` attribute on all job structs and `ISystem.OnUpdate`.
- **Require** `NativeArray<T>` / `NativeList<T>` instead of managed arrays. These types are unmanaged and GC-free.
- **Require** `Unity.Mathematics` types (`float3`, `quaternion`) instead of `UnityEngine` equivalents in Burst context.
- **Flag** I/O operations (file reads, network calls) in jobs. Use async APIs from the main thread.
- **Flag** `static` variables in Burst jobs. Burst jobs do not support them.

---

## Job System Constraints

- **Only the main thread can schedule jobs**. Flag any job scheduling from worker threads.
- Declare job dependencies explicitly. Jobs that share data must have ordered dependencies.
- Call `Complete()` on scheduled jobs before accessing their output data on the main thread.
- Keep each job's data isolated and private. Shared data requires a dependency declaration.
- Pass only **blittable data** into jobs. Do not pass reference types.
- Return results via `NativeContainer` types.
- Schedule jobs early in the frame. Avoid synchronization points that block the main thread.

---

## ECS Patterns

- Entity components must be **unmanaged structs only**. Do not use classes. This restriction is required for Burst compatibility.
- Systems should be `partial struct` types that implement `ISystem` with `[BurstCompile]` on `OnUpdate`.
- Use entity queries to batch-process entities with matching component types. This approach is cache-friendly.
- **Do not mix GameObjects and Entities** without clear architectural boundaries.

---

## Structural Changes

- Adding or removing components moves entities between archetypes. This operation is expensive.
- **Flag** structural changes in tight loops. Batch or defer them.
- Monitor chunk allocation. Too many unique archetypes fragment memory.
- Use `EntityCommandBuffer` for deferred structural changes.

---

## Performance Expectations

- Burst-compiled jobs have documented speedups of 245x+ over equivalent managed C#.
- The primary benefit is cache-coherent data access and SIMD vectorization.
- The main overhead comes from the learning curve and architectural constraints.
