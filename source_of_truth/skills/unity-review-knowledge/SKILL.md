---
name: unity-review-knowledge
description: "Unity best practices knowledge base distilled from 11 official Unity ebooks (Unity 6 edition). Covers C# style, performance/profiling, architecture/design patterns, DOTS/ECS, 2D art/rendering, and general Unity practices. Use when: reviewing Unity C# code, checking for Unity anti-patterns, validating design patterns, performance review, style guide compliance, or any code quality review in a Unity project."
---

# Unity Review Knowledge Base

Best practices and review rules distilled from 11 official Unity ebooks into actionable guidelines for code review.

## Source Material

| Reference | Source PDFs |
|---|---|
| [C# Style Conventions](./references/csharp-style-conventions.md) | Use a C# style guide for clean and scalable game code (Unity 6) |
| [Performance & Profiling](./references/performance-and-profiling.md) | Ultimate Guide to Profiling Games (Unity 6) + Optimize your game performance (Unity 6) |
| [Architecture & Patterns](./references/architecture-and-patterns.md) | Modular game architecture with ScriptableObjects (Unity 6) + Design patterns and SOLID (Unity 6) |
| [DOTS & ECS](./references/dots-and-ecs.md) | Introduction to DOTS (Unity 6) |
| [2D Art & Rendering](./references/2d-art-and-rendering.md) | 2D game art, animation & lighting (Unity 6/LTS) + Tips to increase productivity (Unity 6) |
| [General Unity Practices](./references/general-unity-practices.md) | Unity Game Dev Field Guide + Tips to increase productivity (Unity 6) + Game Designer's Playbook |

## When to Use

Load this skill when:
- Reviewing any Unity C# code for quality, performance, or correctness
- Checking code against Unity best practices and official guidelines
- Validating architecture decisions (ScriptableObject patterns, design patterns, SOLID)
- Reviewing performance-sensitive code (Update loops, rendering, memory)
- Checking C# naming conventions and code organization

## How to Use

1. Read this SKILL.md to understand available reference domains
2. Load only the reference file(s) relevant to the review:
   - Style/naming issues → [csharp-style-conventions.md](./references/csharp-style-conventions.md)
   - Performance concerns → [performance-and-profiling.md](./references/performance-and-profiling.md)
   - Architecture/pattern questions → [architecture-and-patterns.md](./references/architecture-and-patterns.md)
   - DOTS/ECS code → [dots-and-ecs.md](./references/dots-and-ecs.md)
   - 2D sprite/animation/lighting → [2d-art-and-rendering.md](./references/2d-art-and-rendering.md)
   - General lifecycle/setup → [general-unity-practices.md](./references/general-unity-practices.md)
3. Cross-reference with the `unity-development` skill for project-specific runtime wiring, UI Toolkit, and test authenticity rules

## Updating

To add knowledge from new PDFs:
1. Place PDF in repo root
2. Run `python scripts/extract_pdfs.py` to extract text
3. Review extracted text in `scripts/pdf-extracts/`
4. Curate actionable rules into the appropriate reference file (or create a new one)
5. Keep each reference file under 500 lines for progressive loading efficiency
