---
name: unity-review-knowledge
description: "Unity best practices knowledge base distilled from 11 official Unity ebooks (Unity 6 edition). Covers C# style, performance/profiling, architecture/design patterns, DOTS/ECS, 2D art/rendering, and general Unity practices. Use when: reviewing Unity C# code, checking for Unity anti-patterns, validating design patterns, performance review, style guide compliance, or any code quality review in a Unity project."
user-invocable: false
---
<!-- Generated from source_of_truth/skills. Do not edit manually. -->

# Unity Review Knowledge Base

This knowledge base distills best practices and review rules from 11 official Unity ebooks into actionable code-review guidelines.

## Reference Routing

Use this routing table for the skill. Load only the reference files that the code under review needs:

- Style/naming issues → [csharp-style-conventions.md](./references/csharp-style-conventions.md)
- Performance concerns → [performance-and-profiling.md](./references/performance-and-profiling.md)
- Architecture/pattern questions → [architecture-and-patterns.md](./references/architecture-and-patterns.md)
- DOTS/ECS code → [dots-and-ecs.md](./references/dots-and-ecs.md)
- 2D sprite/animation/lighting → [2d-art-and-rendering.md](./references/2d-art-and-rendering.md)
- General lifecycle/setup → [general-unity-practices.md](./references/general-unity-practices.md)

Cross-reference the `unity-development` skill for project-specific runtime wiring, UI Toolkit, and test authenticity rules.

## Updating

To add knowledge from new PDFs:
1. Place the PDF in the repository root.
2. Run `python scripts/extract_pdfs.py` to extract text.
3. Review the extracted text in `scripts/pdf-extracts/`.
4. Curate actionable rules into the appropriate reference file, or create a new reference file.
5. Keep each reference file under 500 lines for efficient progressive loading.
