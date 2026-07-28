<!-- Generated from source_of_truth/skills. Do not edit manually. -->
# Project Learnings

Seed file. Agents append project-specific findings here — framework quirks, config traps, library behavior. Keep entries to a claim, a fix, and the signal to watch for. Review patterns go in `review-learnings.md`; runtime diagnosis in `debugging-learnings.md`.

## Profile interpreter resolution before blaming the code under a latency gate

A 50 ms subprocess gate failed at 84–383 ms. The gate invoked bare `python3`, resolving through a pyenv shim that re-resolves on every call and costs ~50 ms alone (`python3 -c pass`: ~62 ms shimmed, ~9 ms direct). The program itself ran ~30 ms.

**Fix**: invoke `sys.executable`; account for interpreter-resolution overhead separately from program cost.
**Watch for**: any subprocess benchmark on a pyenv/asdf machine spawning bare `python3`/`node`/`ruby`.

## A relative script path in a hook command makes every subdirectory session an outage

Harnesses run hook commands with the *session* working directory, not the project root, so a relative path depends on where the session happens to be — and a fail-closed guard then blocks every tool call, including the `cd` that would recover.

**Fix**: anchor at emit time per harness — Claude `$CLAUDE_PROJECT_DIR`, Codex `$(git rev-parse --show-toplevel)` (no project-root variable exists), OpenCode pin plugin `cwd` to the plugin `directory`. Only works in shell-form commands; a test invoking without `shell=True` sees `$VAR` literally.
**Watch for**: any bare relative path in a hook command, and any fail-closed guard whose failure mode is "blocks everything" rather than "blocks its own tool".

## Security caps must fail closed, not downgrade to warnings

A scanner treated its own byte cap as permission to pass unassessed content with a warning, and redaction preserved attacker-controlled keys — bounded-work limits implemented as effort limits rather than trust boundaries.

**Fix**: replace overflow blocks wholesale with a fixed valid shape so no untrusted key, value, or primitive survives.
**Watch for**: any filter whose resource limit (bytes, depth, timeout) silently passes the unexamined remainder; any redaction that recurses into attacker-controlled containers instead of replacing them.

## Substring-matched command rules generate constant false-positive prompts

Fixed-string matchers cannot distinguish an executed command token from quoted text, flags, or redirects, so commit messages quoting `rm -rf` and `echo $PATH` all prompt.

**Fix**: anchor to the executed-command position (`(?:^|[;&|()])\s*(?:\S*/)?cmd\b`), exempt redirection to null/stdout/stderr/tty/zero, prompt on env echo only for credential-named variables, make lock-file rules write-only.
**Watch for**: any rule using a fixed string for a word that appears in ordinary text, and any read-side `ask` on files agents routinely inspect.

## Never require a check whose evidence cannot exist in the agent's capability envelope

A required check plus a capability boundary compose into a dead end: demanded by the verdict rules, unrunnable by design, with no pipeline step that could supply the evidence. Every run records it not-run and a no-GO-with-missing-checks rule makes GO permanently unreachable.

**Fix**: remove it from scope and declare it an explicit non-goal in the agent body, so the absence reads as a decision rather than a gap — or build the evidence supply path.
**Watch for**: any contract marking a check "NOT RUN when no artifact is supplied" while nothing produces or documents how to supply that artifact.
