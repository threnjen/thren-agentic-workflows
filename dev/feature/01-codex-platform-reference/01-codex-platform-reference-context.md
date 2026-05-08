# 01 Codex Platform Reference Context

## Key Files

### Files To Change

| File | Role | Change Type |
|------|------|-------------|
| `codex/CODEX_PLATFORM_REFERENCE.md` | Repository-owned Codex platform reference covering discovery rules, custom agents, skills, config/runtime locations, and provenance notes | Create |

### Read-Only Reference Files

| File | Role | Change Type |
|------|------|-------------|
| `dev/feature/01-codex-platform-reference/01-codex-platform-reference-plan.md` | Source plan for acceptance criteria, stage breakdown, and sibling relationships | Read-only reference |
| `docs/phases/PHASE_02/PHASE_02_DISCOVERY_CONTEXT.md` | Verified Codex discovery behavior, macOS install locations, and upstream source categories | Read-only reference |
| `docs/phases/PHASE_02/PHASE_02_SUMMARY.md` | Phase-level scope, sequencing, and Codex platform objectives | Read-only reference |
| `.codex/config.toml` | Existing runtime Codex config surface referenced by the feature and used to reinforce source-vs-runtime separation | Read-only reference |
| `README.md` | Repository structure and source-of-truth framing for documentation style and platform terminology | Read-only reference |

## Architectural Decisions

- Keep this feature as repository-owned documentation under `codex/`, not as live runtime configuration under `.codex/` or the user home directory.
- Author one self-contained reference document rather than splitting platform basics across multiple files, so later setup and porting guides can cite a single prerequisite.
- Structure the reference around four core topics: AGENTS discovery, custom agents, skills, and config/runtime locations.
- Separate verified upstream Codex behavior from repository policy decisions so future maintainers can distinguish platform facts from local conventions.
- Treat ambiguous or time-sensitive Codex behavior as revalidation-required instead of documenting assumptions as settled contracts.

## Constraints

- Do not create runnable Codex agents, skills, or global AGENTS files in this feature.
- Do not update shared architecture or roadmap documents in this feature.
- Do not define the broader repository-owned Codex folder structure beyond what is needed for this single reference document.
- Use literal macOS paths where required: `~/.codex/config.toml`, `~/.codex/AGENTS.md`, `~/.codex/AGENTS.override.md`, `~/.codex/agents/`, and `$HOME/.agents/skills/`.
- Make the source-vs-runtime distinction explicit between repository-owned `codex/`, runtime `.codex/`, and user-home install surfaces.
- Prefer fail-fast wording when behavior is not currently verified; direct future implementers to recheck upstream Codex behavior before treating the document as a contract.
- Follow the repository's documentation-first style: concise headings, explicit paths, and clear source-of-truth language.

## Relationships To Sibling Plans

- `01-codex-source-layout` is parallel-safe in the same wave and should stay disjoint by defining repo-owned Codex structure rather than platform semantics.
- `02-codex-macos-setup-guide` depends on this feature for the verified Codex platform model and install locations.
- `02-codex-porting-guide` depends on this feature for AGENTS precedence, custom-agent format, skill discovery roots, and the source-vs-runtime split.

## Suggested Implementation Order

1. Complete this platform reference before authoring the macOS setup guide or the `.github/` to Codex porting guide.
2. Keep the reference narrowly factual so sibling features can layer setup steps and mapping guidance on top without duplicating platform basics.

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Markdown-first source-of-truth repository for VS Code Copilot agents and cross-platform agent docs; no single application runtime or package manifest is declared at repo root |
| Test Runner | Not configured at repo root; no conventional test config or test files were discovered for this documentation feature |
| Test Baseline | No tests found - baseline: N/A (captured 2026-05-07) |
| Lint | Not configured |
| Format | Not configured |

## Relevant Learnings

None applicable.