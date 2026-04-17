# DOTS & ECS Review Rules

*Distilled from: Introduction to DOTS (Unity 6 edition)*

---

## When to Use DOTS vs MonoBehaviour

DOTS (Data-Oriented Technology Stack) is for **high-volume, data-parallel workloads**: thousands of entities with uniform processing. It is not a replacement for all MonoBehaviour code.

**Use DOTS for:**
- Thousands of similar entities (crowds, bullets, particles, grid cells)
- CPU-bound simulation that benefits from cache-coherent data layout
- Workloads that parallelize well across cores (spatial queries, pathfinding, physics)

**Don't use DOTS for:**
- Small object counts where MonoBehaviour is sufficient
- Complex unique behaviors per entity (state machines with many branches)
- UI, audio, or other systems with strong Unity API dependencies
- Mixed GameObject/Entity architectures without clear boundaries

---

## Burst Compiler Rules

- **Flag**: Managed objects (classes) in Burst code — Burst compiles a subset of C# that excludes class instances
- **Require**: `[BurstCompile]` attribute on all job structs and `ISystem.OnUpdate`
- **Require**: `NativeArray<T>` / `NativeList<T>` instead of managed arrays — unmanaged, GC-free
- **Require**: `Unity.Mathematics` types (`float3`, `quaternion`) over `UnityEngine` equivalents in Burst context
- **Flag**: I/O operations (file reads, network calls) in jobs — use async APIs from main thread
- **Flag**: `static` variables in Burst jobs — not supported

---

## Job System Constraints

- **Only the main thread can schedule jobs** — flag job scheduling from worker threads
- Declare job dependencies explicitly; jobs sharing data must have ordered dependencies
- Call `Complete()` on scheduled jobs before accessing their output data on main thread
- Each job must have isolated private data; shared data requires dependency declaration
- Pass only **blittable data** into jobs (no reference types)
- Return results via `NativeContainer` types
- Schedule jobs early in frame; avoid synchronization points that block main thread

---

## ECS Patterns

- Entity components must be **unmanaged structs only** (no classes) — required for Burst compatibility
- Systems should be `partial struct` implementing `ISystem` with `[BurstCompile]` on `OnUpdate`
- Use entity queries to batch-process entities with matching component types (cache-friendly)
- **Don't mix GameObjects and Entities** without clear architectural boundaries

---

## Structural Changes

- Adding/removing components moves entities between archetypes — **expensive operation**
- **Flag**: Structural changes in tight loops — batch or defer them
- Monitor chunk allocation; too many unique archetypes fragments memory
- Use `EntityCommandBuffer` for deferred structural changes

---

## Performance Expectations

- Burst-compiled jobs have documented speedups of 245x+ over equivalent managed C#
- Primary benefit is cache-coherent data access and SIMD vectorization
- Main overhead is learning curve and architectural constraints
