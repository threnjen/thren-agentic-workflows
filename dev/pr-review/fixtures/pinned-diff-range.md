# Pinned Diff Range Fixture

The base/head SHA pair the PR Review orchestrator (`05 PR - Review`) is dry-run
against. Pinned so a dry run is reproducible: every evaluator gets the same diff
every time, and a change in evaluator output means the evaluator changed.

## The pair

| Field | Value |
|---|---|
| **Base SHA** | `f5ab960e5697756538f94430327e2a68eb113822` |
| **Head SHA** | `e6ff28a36293697aebf62155ae0048115c4aecca` |
| Base subject | `add pdf extract script` (2026-06-07) |
| Head subject | `fix(packages): visual-verification v0.2.1 — declare test-framework dependency` (2026-06-09) |
| Origin | Pull request **#17**, `feat/visual-verification-package`, merged at `2191b2e` |
| Commits in range | **3** |
| Diffstat | **26 files changed, 1288 insertions(+), 0 deletions(-)** |

Derivation, reproducible from this repository's own history:

```
git merge-base e6ff28a36293697aebf62155ae0048115c4aecca \
               f5ab960e5697756538f94430327e2a68eb113822
# -> f5ab960e5697756538f94430327e2a68eb113822
```

The merge-base of the head and the base **is** the base. That is what makes this
a base/head pair rather than two commits that merely differ: the head branch
descends from the base. This is the exact relationship the orchestrator's
suggest-and-confirm step exists to establish at run time, so the fixture
exercises the real path rather than a synthetic one.

Note that PR #17's branch was cut from `f5ab960` while PR #16 landed on top of
it independently — so the merge commit's first parent (`7ff1974`) is *not* the
base. Taking the merge commit's first parent as the base would have produced a
diff that silently includes PR #16's 41 files. This pair is a live instance of
why the orchestrator confirms a base instead of assuming one.

## Why this pair

Selected against two constraints that pull in opposite directions: the range
must be **small enough for a cheap dry run** and **substantial enough that every
evaluator on the roster finds something real**. A fixture that no evaluator can
find anything in proves only that the fan-out completed.

**Rejected: `e3398c7..ae9823a`** — the pair that appears in the base-derivation
evidence for AC4. It is 5 commits, **242 files, 27,041 insertions**: a
whole-phase diff, not a pull request. It served a different purpose there (a
demonstration of merge-base self-exclusion) and inheriting it as a fixture would
be borrowing a number that was never sized for this job.

**Rejected: PR #16 (`f5ab960..983546c`)** — 10 commits, 41 files, +858/−95, and
a better *drift* surface (it touches `.github/agents/` source alongside all
three generated roots). Rejected because it contains **no test delta and no
dependency manifest**: the test-health and dependency evaluators would both
return "nothing to report", so the dry run would not exercise them at all. Its
only `.toml` files are agent configs, not dependency declarations.

**Selected: PR #17.** Every evaluator on the roster has real material:

| Evaluator | What it should find in this range |
|---|---|
| `05b` change narrator | Three commits telling a coherent story: package added → onboarding/scaffolding → dependency fix. A real narrative arc, not one squashed blob. |
| `05c` artifact sweeper | A genuine debug artifact: `Debug.Log($"VISUAL_VERIFICATION_MANIFEST={manifestPath}")` in `Tests/CaptureRunner.cs`, plus `Debug.Log`/`Debug.LogWarning` in `Editor/CreateConfigMenu.cs`. |
| `05d` consistency auditor | Unity package conventions: `.meta` files paired to every asset, two `.asmdef` files, UPM layout, a `Samples~/` directory. |
| `05e` dependency auditor | `package.json` declaring `com.unity.test-framework: 1.6.0`, plus the `Tests.asmdef` `precompiledReferences: nunit.framework.dll` and `UnityEngine.TestRunner` reference. The head commit **is** the dependency fix — its subject line says so. |
| `05f` test health | Four C# files under `Tests/`, including `CaptureGateTest.cs`, added with the code they cover. |
| `04e` diff security scan | ~500 lines of new C# doing filesystem writes (`ConfigPath`, manifest/PNG output) and JSON parsing. |
| `05a` baseline worktree | Checks out `f5ab960` cleanly; both SHAs are reachable from this repo's history and not gc-able (both are ancestors of `main`). |
| `05g` readiness synthesizer | Consumes the above. |

Deliberate residual weakness, recorded rather than hidden: the range has **zero
deletions**, so it is a weaker proxy for a refactor-shaped or removal-shaped PR.
It was accepted because no bounded pair in this repository's history has both a
dependency change and a test delta *and* deletions; coverage of the roster was
weighted above shape-completeness. A second fixture is the fix if a
removal-shaped dry run is ever needed — not a resize of this one.

The 674-line `LICENSE.md` (GPL-3.0) is filler and accounts for over half the
insertion count. Real signal is ~600 lines.

## Stability

Both SHAs are ancestors of `main` (via merge commit `2191b2e`), so neither is
reachable only from a deleted branch and neither can be gc-pruned. The range is
history, so its content cannot change; a rewrite of `main` that orphaned either
SHA would break this fixture loudly (the `rev-parse --verify` assertion in
`tests/test_pr_review_orchestrator.py`), not silently.
