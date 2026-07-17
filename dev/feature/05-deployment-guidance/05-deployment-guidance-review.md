# Review Record: Deployment Guidance

## Summary

Reviewed implementation commit `e8b0140` against AC1–AC8, including the
settled propagation and deployment APIs, exact Evangelize renderer parity,
supported setup surfaces, historical/security distinctions, platform evidence,
and the phase requirement to preserve explicit RTK use. Three documentation
defects were found and fixed. The most important attributed collision and
ownership evidence to a pre-mutation inventory API that cannot return it.

## Verdict

Approved

## Traceability

| AC | Status | Evidence | Notes |
|----|--------|----------|-------|
| AC1 | Verified after fix | `.github/agents/evangelize.agent.md:38`; `tests/test_phase04_runtime_deployment.py:684` | Evangelize requires convergence before managed-copy deployment and contains no supported runtime-link creation, repair, recommendation, or validation path. |
| AC2 | Verified after fix | `.github/agents/evangelize.agent.md:40`; `.github/agents/evangelize.agent.md:45`; `scripts/runtime_deployment.py:309` | Pre-mutation inventory review is now limited to fields the settled API actually returns; collision and reconciliation outcomes are checked on the returned managed-copy result. |
| AC3 | Verified | `tests/test_propagate_master_assets.py:220`; generated Evangelize outputs | Renderer equality covers Claude command, OpenCode agent, Codex agent, and Codex profile exactly. Regeneration reached a zero-change verification pass. |
| AC4 | Verified after fixes | `HARNESS_SETUP.md:5`; `claude/SYMLINK_SETUP.md:5`; `codex/MACOS_SETUP_AND_SYMLINKS.md:5`; `opencode/SYMLINK_SETUP.md:5` | Supported guides use fixed-point propagation, reviewed destination records/inventory, managed-copy deployment, result inspection, and fresh-session discovery. |
| AC5 | Verified after fix | `claude/agents/README.md:98`; `tests/test_phase04_runtime_deployment.py:684` | The final stale instruction to validate runtime symlinks was removed; no supported surface contains an operational link creation or validation recipe. |
| AC6 | Verified | `.github/agents/evangelize.agent.md:69`; `codex/MACOS_SETUP_AND_SYMLINKS.md:23`; `codex/PILOT_SLICE_PLAN.md:1` | Hostile-link containment remains security guidance, while the pilot is explicitly historical and non-operational. |
| AC7 | Verified after fix | `tests/test_phase04_runtime_deployment.py:677`; `tests/test_phase04_runtime_deployment.py:690` | POSIX, PowerShell, and Windows runtime-link recipes remain negative fixtures; stale link-validation wording is also rejected. |
| AC8 | Verified | `.github/agents/evangelize.agent.md:59`; `HARNESS_SETUP.md:52`; `tests/test_phase04_runtime_deployment.py:735` | Native Windows and WSL are separate runs, unavailable environments are `NOT RUN`, and either blocks full cross-platform GO. |

## Issues Found

| # | Severity | Issue | Status |
|---|----------|-------|--------|
| 1 | Medium | Evangelize and setup guides claimed `destination_inventory(records)` exposed active-home, ownership, and collision evidence. The settled API returns only harness, asset class, status, and a home-relative destination; collision/reconciliation evidence exists only in the deployment result. | Fixed |
| 2 | Medium | `claude/agents/README.md` still instructed operators to check runtime symlinks when an agent failed to load, preserving retired validation behavior on a supported surface. | Fixed |
| 3 | Low | The HARNESS setup rewrite removed unrelated Copilot multi-root and Context7 setup guidance, leaving `docs/TROUBLESHOOTING.md` pointing to missing multi-root instructions. | Fixed |

## Fixes Applied

| Files | Change |
|-------|--------|
| `.github/agents/evangelize.agent.md`; generated Evangelize variants | Limited destination-inventory review to roster/destination evidence and moved collision, copy, replacement, pruning, failure, and skipped-reconciliation checks to the returned managed-copy result. Regenerated all variants from source. |
| `HARNESS_SETUP.md`; Claude, Codex, and OpenCode setup guides | Corrected the same settled-API sequence and restored concise Copilot multi-root and Context7 guidance unrelated to retired runtime-link deployment. |
| `claude/agents/README.md` | Replaced stale symlink validation with managed-copy result and fresh-session discovery checks. |
| `tests/test_phase04_runtime_deployment.py` | Added regression coverage for stale link validation, the post-deployment result obligation, and preserved explicit RTK guidance. |

## Test Coverage Assessment

- Full suite: `uv run pytest` — 391 passed.
- Focused deployment and propagation suites: 91 passed via `unittest`.
- Propagation regeneration: converged with zero verification changes.
- `git diff --check`: passed.
- Static supported-surface audit found no `ln -s`, PowerShell symbolic-link,
  `mklink`, or stale `Check symlinks:` recipe.
- Graph review rated the original direct changes low risk (0.40), while the
  two-hop documentation/test blast radius was high; exact renderer parity and
  full-suite coverage address the affected generated surfaces.

## Remaining Concerns

Native Windows, WSL, and fresh live-harness discovery evidence remain assigned
to Feature 06. This runner verifies the documentation contract and deterministic
platform distinctions but does not convert `NOT RUN` platforms into release
evidence. No unresolved feature-scope finding remains.

## Risk Summary

- Generated Evangelize files exactly match the established renderers.
- Runtime deployment uses only the settled convergence, destination-resolution,
  inventory, and managed-copy APIs; it does not invent copy or link algorithms.
- Supported guidance has no runtime symlink/junction creation, repair, or
  validation path for generated assets.
- Historical and hostile-link security discussion remains explicitly distinct
  from supported operational setup.
- Explicit RTK guidance remains present in hook limitations, verification, and
  manual-QA documentation; automatic RTK rewriting is not restored.
