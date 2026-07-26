<!-- Generated from source_of_truth/skills. Do not edit manually. -->
# Project Learnings

## If a fixed subprocess latency gate fails, profile interpreter resolution before the code

**Problem**
A 50 ms subprocess latency gate failed with medians of 84–383 ms and the program under test was blamed.

**Root cause**
The gate invoked bare `python3`, which resolved through a pyenv shim — a shell script that re-resolves the interpreter on every call and alone costs ~50 ms (`python3 -c pass` was ~62 ms via shim, ~9 ms direct). The program itself ran ~30 ms.

**Fix**
Invoke `sys.executable` directly; document environment interpreter-resolution overhead separately from program cost.

**Watch for**
Any subprocess benchmark on a pyenv/asdf machine that spawns bare `python3`/`node`/`ruby` — measure `<interpreter> -c pass` first to isolate shim cost before optimizing the program.

## If a hook command uses a relative script path, any subdirectory session is an outage

**Problem**
Generated hook wiring invoked its script via a repo-relative path. Any session whose working directory was not the repository root could not resolve the script, and the fail-closed posture then blocked every tool call — including the `cd` that would have recovered. Only a human running `cd` outside the agent could restore the session.

**Root cause**
Claude Code and Codex both execute hook commands with the *session* working directory, not the project root. A relative path silently depends on where the session happens to be, and fail-closed turns that into a total outage.

**Fix**
Anchor generated commands to the project root per harness — Claude: `$CLAUDE_PROJECT_DIR`; Codex: `$(git rev-parse --show-toplevel)` (no project-root variable exists); OpenCode: pin plugin `cwd` to the plugin `directory`. Source manifests stay relative; anchoring happens at emit time. The anchored form only works because these are shell-form commands — a test that executes the command without `shell=True` sees the quotes and `$VAR` literally.

**Watch for**
Any hook command token that is a bare relative path, and any fail-closed guard whose failure mode is "blocks everything" rather than "blocks its own tool" — the recovery path must not itself require a blocked tool.

## Security caps must fail closed, not downgrade to warnings

**Problem**
An injection scanner treated its own scan-byte cap and encoded-candidate budget as permission to pass unassessed content with a warning, and block redaction preserved attacker-controlled mapping keys.

**Root cause**
Bounded-work limits were implemented as scan-effort limits rather than trust boundaries, and redaction tried to preserve output shape instead of replacing it.

**Fix**
Cap overflow blocks with a fixed replacement; blocked output is replaced wholesale with a fixed runner-valid shape so no untrusted key, value, or primitive survives.

**Watch for**
Any scanner/filter whose resource limit (bytes, candidates, depth, timeout) silently passes the unexamined remainder, and any redaction that recurses into attacker-controlled containers instead of replacing them.

## Substring-matched command rules generate constant false-positive prompts

**Problem**
Destructive-command `ask` rules matched fixed substrings anywhere in the Bash command text, so redirects, commit messages quoting "rm -rf", option flags, and `echo $PATH` all prompted for confirmation.

**Root cause**
Fixed-string matchers cannot distinguish an executed command token from quoted text, option flags, or redirects to harmless devices.

**Fix**
Anchor destructive matchers to the executed-command position (`(?:^|[;&|()])\s*(?:\S*/)?cmd\b`), exempt device redirection to null/stdout/stderr/tty/zero, prompt on env echo only for credential-named variables, and make lock-file rules write-only.

**Watch for**
Any command rule using a fixed string for a word that can appear in ordinary text, and any read-side `ask` on files agents routinely inspect.

## Review runtime inventory by content-bound digest, not by path list

**Problem**
An inventory containing only destination names can become stale when generated content or destination types change while retaining the same paths.

**Fix**
The runtime deployment path emits home-relative classifications with generated-source fingerprints and binds operator review to their deterministic SHA-256 digest. It rebuilds the inventory immediately before mutation and fails closed on drift.

**Watch for**
Boolean confirmation flags, inventories keyed only by modification time, absolute home paths in normal output, or tests that treat simulated platform policy as live fresh-session evidence.

## Prose-guard tests match exact strings across the source's line wraps

**Problem**
Editing PR-review agent/skill prose broke `test_readiness_synthesis_agents.py` and `test_pr_review_orchestrator.py` even when the intended wording was present.

**Root cause**
These tests assert exact needle strings against raw file text, so a needle fails when a Markdown line wrap splits it across lines. Frontmatter `description` fields are also pinned.

**Fix**
Keep pinned phrases on a single unwrapped line; when intentionally changing pinned wording, update the corresponding needle in the test. Retain required scope words in agent descriptions.

**Watch for**
Any prose edit under `source_of_truth/agents/05*` or `skills/pr-review-*`: re-run both PR-review test modules and reflow so guarded phrases don't straddle a newline.

## Never give an offline agent a required check whose evidence cannot exist locally

**Problem**
`05e-dependency-auditor` required license and CVE checks, but its offline-by-capability contract meant the evidence (registry metadata, advisory data) could never be obtained. Any branch adding a dependency recorded them as not-run, and the no-GO-with-missing-checks rule made GO permanently unreachable.

**Root cause**
A required check and a capability boundary composed into a structural dead end: the check was demanded by the verdict rules but unrunnable by design, with no pipeline step that could ever supply the evidence.

**Fix**
Removed license/CVE auditing from `05e` scope entirely and declared it an explicit non-goal in the agent body — CVE and license verification belong to CI tooling or the full `security-scan`, not PR review. Out-of-scope is stated, not silently omitted, so the absence reads as a design decision rather than a coverage gap.

**Watch for**
Any evaluator whose contract marks a check "NOT RUN when no artifact is supplied" while nothing in the pipeline produces or documents how to supply that artifact — that check will block or condition every verdict forever. Either delete the check, or build the evidence supply path; never leave a permanently unsatisfiable required check.
