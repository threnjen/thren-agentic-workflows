# 03 Codex Pilot Slice Definition Context

## Key Files

### Files to Change

| File | Role | Change Type |
|------|------|-------------|
| `codex/PILOT_SLICE_PLAN.md` | New pilot-definition document that selects the instruction slice, custom agent, and skill; defines expected Codex outputs; and records validation and exit criteria. | Create |

### Read-Only Reference Files

| File | Role | Change Type |
|------|------|-------------|
| `dev/feature/03-codex-pilot-slice-definition/03-codex-pilot-slice-definition-plan.md` | Governing feature plan and acceptance-criteria source for this implementation slice. | Read-only reference |
| `.github/instructions/output-verbosity-policy.instructions.md` | Default pilot instruction slice for the global Codex AGENTS guidance surface. | Read-only reference |
| `.github/agents/03-feature-decomposer.agent.md` | Default pilot custom-agent source for the Codex TOML agent surface. | Read-only reference |
| `.github/skills/feature-plan-set/SKILL.md` | Default pilot skill source and contract for the Codex skill-directory surface. | Read-only reference |
| `codex/README.md` | Expected Codex source-layout contract and landing-zone reference from `01-codex-source-layout`; not present in the workspace yet. | Read-only reference |
| `codex/CODEX_PORTING_GUIDE.md` | Expected mapping-rules dependency from `02-codex-porting-guide`; not present in the workspace yet. | Read-only reference |
| `codex/MACOS_SETUP_AND_SYMLINKS.md` | Expected validation/install workflow dependency from `02-codex-macos-setup-guide`; not present in the workspace yet. | Read-only reference |

## Architectural Decisions

- Use one narrow pilot trio that still spans all three Codex-native surfaces: global guidance, a custom agent, and a skill directory.
- Keep the default trio as `.github/instructions/output-verbosity-policy.instructions.md`, `.github/agents/03-feature-decomposer.agent.md`, and `.github/skills/feature-plan-set/` unless later discovery produces a demonstrably lower-risk trio with explicit evidence.
- Reuse real repository assets instead of inventing a synthetic pilot so the pilot validates the actual `.github/` source tree and Phase 02 goals.
- Keep the pilot definition document-only: this feature defines `codex/PILOT_SLICE_PLAN.md` but does not implement Codex AGENTS content, TOML agents, or copied skill directories.
- Treat the setup guide, porting guide, and Codex source-layout document as prerequisites. The pilot plan should consume their rules, not replace them.

## Constraints

- Do not implement the pilot Codex artifacts in this feature.
- Do not expand the pilot into a full-catalog Codex conversion.
- Do not change the Phase 02 macOS setup or mapping rules in this feature.
- Follow the Phase 02 rule that pilot validation must pass before broader Codex parity work begins.
- Reuse repository-owned `.github/` assets and previously planned Codex guides rather than inventing new setup or mapping rules.
- Keep the plan free of machine-specific absolute paths beyond generic macOS install roots.
- If the default trio is blocked, record a documented replacement decision instead of silently changing scope.
- Current workspace gap: `codex/` is still empty, so `codex/README.md`, `codex/CODEX_PORTING_GUIDE.md`, and `codex/MACOS_SETUP_AND_SYMLINKS.md` remain upstream prerequisites rather than live references.

## Relationships to Sibling Plans

- `01-codex-source-layout` should land first because this feature needs the Codex source-area contract and the intended landing zones described in `codex/README.md`.
- `02-codex-porting-guide` should land before this feature because the pilot must reuse its mapping rules for instructions, agents, and skills.
- `02-codex-macos-setup-guide` should land before this feature because the pilot validation flow must reuse its install and verification steps.
- This feature is intentionally the last feature in the phase decomposition because it consumes those earlier documentation outputs and turns them into a go or no-go pilot gate.

## Suggested Implementation Order

1. Complete `01-codex-source-layout` so the Codex source-area contract exists.
2. Complete `02-codex-porting-guide` and `02-codex-macos-setup-guide` so mapping and validation guidance exist.
3. Create `codex/PILOT_SLICE_PLAN.md` using the default trio unless a better low-risk trio is documented with evidence.
4. Use the pilot exit criteria to gate any broader Codex conversion work.

## Environment State

| Property | Value |
|----------|-------|
| Tech Stack | Markdown documentation plus YAML-frontmatter Copilot agent definitions and skill directories; no package-manager-based application stack detected in this repo. |
| Test Runner | `No tests found` |
| Test Baseline | No tests found - baseline: N/A (captured 2026-05-07) |
| Lint | Not configured |
| Format | Not configured |

## Relevant Learnings

- `.github/learnings/review-learnings.md`: When parity or inventory work touches user-facing agent surfaces, update every documentation surface that summarizes agent inventories or counts, not just the primary catalog. This matters if the pilot definition or follow-on port changes how Codex-visible agents are described.
- `.github/learnings/review-learnings.md`: When behavior is mirrored across source-of-truth and derived copies, document both the source rule and the synchronized downstream behavior so parity work does not drift across platforms.