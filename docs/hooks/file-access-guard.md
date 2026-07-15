# File-Access Guard

The Phase 01 file-access guard evaluates path-bearing file tools and explicit
Grep scopes before tool execution. Policy is data-driven in
`.github/hooks/config/file-access-rules.json`; the Python engine contains only
schema validation, normalization, matching, precedence, and payload adaptation.

## Policy and Configuration Contract

Rules are keyed by a stable identifier. Each rule repeats that identifier in
`id` and defines `action`, `reason`, `matcher`, `pattern`, and integer
`priority`. Blocking and held rules also define `safe_alternative`.
`escalate_in_bypass` may be set only to `deny`.
Rules may set `access` to `read` or `write`; self-protection uses `write` so
agents can inspect hook policy but cannot modify or deregister it.

Supported matchers are `basename`, `basename_glob`, `path_suffix`, and
`path_glob`. Concrete paths select the highest matching priority, breaking ties
in favor of `deny`, then `ask`, then `allow`. Wildcard Grep scopes are matched
conservatively against every protected path they can include; the strongest
overlapping action wins before priority. The explicit `.env.sample` and
`.env.example` allow rules therefore remain narrow exceptions for exact paths,
without allowing a broader wildcard scope that could also include `.env`.

Project owners may add or refine rules in
`.github/hooks/config/file-access-overrides.json`. The shared framework merges
that file over defaults and invalidates its cache on mtime changes. This
protected file is also the only kill-switch channel:

```json
{"guard": {"enabled": false}}
```

There is no environment-variable kill switch. A human must make and later
revert this protected override change.

## Normalization and Reuse

`.github/hooks/lib/file_access.py` exposes `normalize_path`, `load_rules`, and
`evaluate_path`. Paths are expanded from `~`, anchored to the event working
directory, collapsed through `..`, resolved through existing or broken
symlinks, and case-folded only when the filesystem is detected as
case-insensitive. Feature 03 imports this evaluator rather than creating a
second path or tier engine.

## Tool Boundary

The guard handles `Read`, `Edit`, `Write`, `MultiEdit`, and `NotebookEdit` file
paths. For `Grep`, it evaluates the recorded explicit `path` and `glob` scope
fields. A Grep without either explicit scope is allowed; recursive scope hidden
inside a Bash command belongs to the Bash analyzer. `Glob` is deliberately not
in the hook matcher. Bash is included in the source hook definition for Feature
03 but is allowed by this feature until that analyzer is integrated.

Denied or held output includes only the rule identifier, normalized offending
path, configured reason, and safe alternative. The audit record is limited to
timestamp, tool, rule, decision, and normalized path. File content, search
patterns, command bodies, and full tool input are never recorded.

## Verification

```text
uv run --with-requirements requirements-dev.txt pytest -q
uv run --with-requirements requirements-dev.txt pytest tests/hooks/test_file_access_guard.py --cov=.github/hooks/lib --cov=.github/hooks/scripts --cov-report=term-missing --cov-fail-under=50 -q
python3 -m unittest discover -s tests -v
python3 -m compileall -q .github/hooks/lib .github/hooks/scripts/file-access-guard.py tests/hooks/test_file_access_guard.py
```

Automated fixtures cover every file tool, both Grep scope fields, environment
templates and variants, credential names and directories, traversal, tilde,
symlink and case behavior, project overrides, self-protection, redaction,
induced failures, and bypass escalation.

Runner-constrained evidence for a real `bypass-permissions` session remains
`NOT RUN` until Feature 04's disposable consuming-project harness is available.
That pass must attempt `.env` and generated wiring edits and record the observed
deny results; automated unit behavior is not a substitute for this premise
check.

## Recovery and Rollback

If the guard blocks legitimate work, prefer the safe alternative named in the
decision or add a narrowly scoped human-reviewed override rule. For emergency
recovery, a human may disable the guard through the protected override file,
perform the repair, restore `guard.enabled` to `true` (or remove the override),
and rerun the verification commands.

Feature 02 does not alter generated Claude, Codex, or OpenCode wiring. Until
Feature 04 completes propagation and parity verification, rollback is simply to
leave the existing legacy hook wiring active and omit the new source hook from
generated outputs.
