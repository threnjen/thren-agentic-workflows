# ui-ux-pro-max-skill (nextlevelbuilder)

**Local path:** `/Users/jennywadkins/github_repos/claude_skills/ui-ux-pro-max-skill`

## Overview

A mature, actively maintained **UI/UX design-intelligence skill** for AI coding assistants (v2.11.0, MIT, npm `ui-ux-pro-max-cli`, marketed at uupm.cc). Core value: a **BM25 search engine over local CSV design databases** — 84 UI styles, ~192 color palettes, ~74 font pairings, 25 chart types, 98 UX guidelines, GSAP motion presets, and stack-specific guidance for 22 frameworks (React, Next.js, Vue, Svelte, SwiftUI, Flutter, Tailwind, shadcn/ui, Compose, WPF, Three.js, …). Flagship v2 feature: an AI "Design System Generator" reasoning engine. CI, semantic-release, Playwright e2e tests.

## Agents

None.

## Skills (7)

- **ui-ux-pro-max** — Core: searchable local design database across 22 stacks.
- **design** — Umbrella: brand identity, logos, corporate identity, HTML slides, banners, icons, social photos.
- **design-system** — Three-layer token architecture (primitive→semantic→component), CSS variables, scales, component specs.
- **brand** — Brand voice, visual identity, messaging frameworks, consistency compliance.
- **banner-design** — Banners for social/ads/hero/print with multiple art-direction options.
- **slides** — Strategic HTML presentations with Chart.js, design tokens, copywriting formulas.
- **ui-styling** — Accessible UIs with shadcn/ui + Radix + Tailwind, dark mode, responsive layouts.

## Hooks

None (no hooks, no settings.json, no automation).

## Other assets

- TypeScript CLI installer supporting 19+ platforms (`npx ui-ux-pro-max-cli init --ai claude`).
- Python search scripts (stdlib-based BM25 + design-system generator with variance/motion/density dials).
- ~35 CSV data files; per-platform install templates; Claude plugin marketplace manifests (`.claude-plugin/`); example HTML projects. No MCP servers.

## Character

**Highly specialized, single-domain** — purpose-built UI/UX/visual-design intelligence, multi-platform by design. For anyone who wants opinionated design guidance instead of templated defaults.

## Install verdict

**Install as-is via its official mechanism if you do UI work; otherwise reference only.** Low-risk adoption: no hooks, no agents, no MCP, no state-changing automation — just skills, read-only Python search over local CSVs, and data. Nothing runs unless invoked. Only dependency: Python 3 for the search engine. If you never build UI, skip it.
