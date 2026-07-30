---
name: unity-review-knowledge
description: "Unity best practices knowledge base distilled from 11 official Unity ebooks (Unity 6 edition). Covers C# style, performance/profiling, architecture/design patterns, DOTS/ECS, 2D art/rendering, and general Unity practices. Use when: reviewing Unity C# code, checking for Unity anti-patterns, validating design patterns, performance review, style guide compliance, or any code quality review in a Unity project."
---

# Unity Review Knowledge Base

Best practices and review rules distilled from 11 official Unity ebooks into actionable guidelines for code review.

## Reference Routing

This is the routing table for the whole skill. Load only the reference file(s) the code under review needs:

- Style/naming issues → [csharp-style-conventions.md](./references/csharp-style-conventions.md)
- Performance concerns → [performance-and-profiling.md](./references/performance-and-profiling.md)
- Architecture/pattern questions → [architecture-and-patterns.md](./references/architecture-and-patterns.md)
- DOTS/ECS code → [dots-and-ecs.md](./references/dots-and-ecs.md)
- 2D sprite/animation/lighting → [2d-art-and-rendering.md](./references/2d-art-and-rendering.md)
- General lifecycle/setup → [general-unity-practices.md](./references/general-unity-practices.md)

Cross-reference with the `unity-development` skill for project-specific runtime wiring, UI Toolkit, and test authenticity rules

## Updating

To add knowledge from new PDFs:
1. Place PDF in repo root
2. Run `python scripts/extract_pdfs.py` to extract text
3. Review extracted text in `scripts/pdf-extracts/`
4. Curate actionable rules into the appropriate reference file (or create a new one)
5. Keep each reference file under 500 lines for progressive loading efficiency
