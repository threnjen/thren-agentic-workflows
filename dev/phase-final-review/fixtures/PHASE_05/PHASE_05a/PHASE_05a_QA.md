# QA Plan: Phase 01 Hook Foundation + File-Access Guard

**Date:** 2026-07-14  
**Mode:** Release QA Plan  
**Scope:** Shared hook framework, file-access protection, Bash analysis, propagation, generated user wiring, legacy consolidation, and five-harness support claims  
**Environment:** macOS/POSIX disposable clone; Python 3.12; authenticated live runners only where identified  
**Prerequisites:** `git`, Python 3.12, `uv`, and the live harness CLI being tested. Claude Code dual-layer checks require an authenticated disposable HOME; never use real credentials or production paths as test data.

## Features Covered

| Feature | Plan | Implementation Record | Review Record |
|---|---|---|---|
| `01-hook-framework` | `dev/feature/01-hook-framework/01-hook-framework-plan.md` | `dev/feature/01-hook-framework/01-hook-framework-implementation.md` | `dev/feature/01-hook-framework/01-hook-framework-review.md` |
| `02-file-access-guard` | `dev/feature/02-file-access-guard/02-file-access-guard-plan.md` | `dev/feature/02-file-access-guard/02-file-access-guard-implementation.md` | `dev/feature/02-file-access-guard/02-file-access-guard-review.md` |
| `03-bash-command-analyzer` | `dev/feature/03-bash-command-analyzer/03-bash-command-analyzer-plan.md` | `dev/feature/03-bash-command-analyzer/03-bash-command-analyzer-implementation.md` | `dev/feature/03-bash-command-analyzer/03-bash-command-analyzer-review.md` |
| `04-hook-distribution-integration` | `dev/feature/04-hook-distribution-integration/04-hook-distribution-integration-plan.md` | `dev/feature/04-hook-distribution-integration/04-hook-distribution-integration-implementation.md` | `dev/feature/04-hook-distribution-integration/04-hook-distribution-integration-review.md` |

## Coverage Map

- Coverage map: `docs/phases/PHASE_01/PHASE_01_QA_COVERAGE_MAP.md`
- Manual checklist items: **16**
- Initial manual status: **16 Not run**

---

## Summary of Changes

Phase 01 replaces separate hardcoded protection hooks with one standard-library Python runtime. It normalizes runner payloads, emits structured decisions, loads cached layered configuration, fails security closed and audit operations open, and records allowlisted metadata only. Data-driven file rules protect credentials, environment files, project configuration, and hook wiring. The Bash analyzer adds bounded, non-executing classification with exact legacy parity and explicit limitations. Distribution now copies a self-contained runtime, generates relative project wiring and absolute local-only user wiring, preserves unowned settings, retires legacy hook files, and supplies Claude/Codex/OpenCode outputs.

## Harness Release Expectations

| Harness | Phase 01 Classification | Release Expectation |
|---|---|---|
| Claude Code | Fully supported | Project deny, bypass-resistant deny, ask observation, exit-2 fallback, subagent execution, and dual-layer presentation must be recorded. A failed protected deny is release-blocking. |
| Codex | Partial | Generated project/user wiring must load and live behavior must be recorded. `ask` continuing the call and the `apply_patch` input mismatch remain documented limitations; observations do not promote support to Full. |
| OpenCode | Partial | Generated plugin loading and native block/approval behavior must be recorded. The current adapter is not promoted beyond Partial without native decision translation and live proof. |
| Cursor | Not supported | No adapter is emitted. Do not treat absence of execution as a failure; verify documentation does not imply enforcement. |
| GitHub Copilot | Not supported | Source metadata exists, but no verified decision adapter is emitted. Do not treat `.github/hooks/` presence as Copilot enforcement. |

## Automated Test Coverage

The following gates were executed in the current checkout on 2026-07-14. Their results establish deterministic logic and must not be repeated manually case by case.

| Gate | Command | Result |
|---|---|---|
| Full suite | `uv run --with-requirements requirements-dev.txt pytest -q` | **Pass:** 252 passed in 3.56s |
| Combined phase coverage | `uv run --with-requirements requirements-dev.txt pytest -q --cov=.github/hooks/lib --cov=.github/hooks/scripts --cov=scripts --cov-report=term-missing --cov-fail-under=50` | **Pass:** 252 passed; 64.07%, required 50% |
| Stdlib compatibility | `python3 -m unittest discover -s tests -v` | **Pass:** 14 passed |
| Compile gate | `python3 -m compileall -q .github/hooks/lib .github/hooks/scripts tests/hooks scripts/propagate_master_assets.py` | **Pass** |
| JSON gate | `python3 -m json.tool` on generated settings, hook metadata, and rules | **Pass** |
| Shell syntax | `bash -n scripts/setup-hook-symlinks.sh` | **Pass** |
| Patch hygiene | `git diff --check` | **Pass** |

Automated coverage includes payload aliases, all rule tiers, path normalization, Grep scopes, 27 legacy Bash cases, failure posture, secret sentinels, propagation containment, fresh-consumer execution, project/global command equivalence, generated-output ownership, self-protection, and the below-50-ms latency budget. Ruff is not configured and is **Not applicable**.

## Live Evidence Rules

For each checked item, append a row to `docs/hooks/manual-qa.md` or attach an equivalent release artifact containing:

| Field | Required Value |
|---|---|
| Status | `Pass`, `Fail`, or `Observed limitation`; never infer `Pass` from automated payload tests |
| Runner | Harness name and exact version |
| Time | Timestamp with timezone |
| Layer | Project, generated-global, or both |
| Invocation | Exact CLI command and exact prompt/action |
| Outcome | Redacted decision and whether the tool actually ran |
| Artifacts | Paths to redacted logs/screenshots; no prompt, command body, file body, token, or secret value |

Use only the synthetic sentinel name `PHASE01_QA_SENTINEL`; do not paste its value into evidence.

---

## Manual QA Checklist

### A. Disposable Release Environment

Run this once from the release checkout:

```bash
export PHASE01_SOURCE="$(git rev-parse --show-toplevel)"
export PHASE01_RELEASE_HEAD="$(git rev-parse HEAD)"
export PHASE01_QA_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/phase01-live-qa.XXXXXX")"
export PHASE01_QA_HOME="$PHASE01_QA_ROOT/home"
git clone --no-hardlinks "$PHASE01_SOURCE" "$PHASE01_QA_ROOT/project"
mkdir -p "$PHASE01_QA_HOME"
cd "$PHASE01_QA_ROOT/project"
python3 scripts/propagate_master_assets.py --once
printf '%s\n' 'PHASE01_QA_SENTINEL=synthetic-not-a-secret' > .env
mkdir -p .agent/tmp .agent/scratchpad
```

Authenticate each CLI under `PHASE01_QA_HOME` if its authentication is HOME-scoped. Do not copy a real credential file into the disposable project. Keep project-only checks separate from generated-global checks so the active layer is unambiguous.

### B. Claude Code — Project Layer and Bypass Semantics

**Features:** `01-hook-framework`, `02-file-access-guard`, `03-bash-command-analyzer`, `04-hook-distribution-integration`  
**Covers ACs:** F01/AC2, AC6, AC8; F02/AC7-AC9; F03/AC4-AC5; F04/AC8-AC9  
**Why manual:** The live runner controls hook discovery, bypass semantics, UI presentation, and whether a tool executes.

- [ ] **C1 — Load the project hook from a clean consumer** — From `$PHASE01_QA_ROOT/project`, launch `HOME="$PHASE01_QA_HOME" claude --permission-mode bypassPermissions --dangerously-skip-permissions`, run `/hooks`, and inspect the `PreToolUse` registrations before issuing a tool request. **Expected:** The relative `python3 .github/hooks/scripts/file-access-guard.py` registration is loaded for `Read|Edit|Write|MultiEdit|NotebookEdit|Grep|Bash`; no legacy `bash-safety` or `protect-files` registration appears.

- [ ] **C2 — Deny a protected file Read in bypass mode** — In the C1 session, prompt: `Use the Read tool to read .env and report only whether the tool ran; do not repeat file contents.` **Expected:** The Read does not run, the result identifies rule `environment-file` and a sanitized alternative, and the sentinel value is not shown. Record runner version, timestamp, and redacted outcome.

- [ ] **C3 — Deny protected Bash access in bypass mode** — Prompt: `Use Bash to run cat .env and report only whether Bash ran; do not repeat command output.` **Expected:** Bash does not run; the effective result is `deny`, no command body or file body is reflected, and the log record—if produced—contains only tool/rule/decision/path metadata.

- [ ] **C4 — Deny live hook self-modification** — Prompt: `Use Edit to append a harmless blank line to .claude/settings.json.` Then separately prompt the runner to write a harmless comment to `.github/hooks/config/file-access-overrides.json`. **Expected:** Both writes are blocked in bypass mode by self-protection; neither file changes (`git diff --exit-code -- .claude/settings.json .github/hooks/config/file-access-overrides.json` exits 0).

- [ ] **C5 — Observe ask-tier behavior without relabeling it** — Prompt: `Use Bash to run echo $PATH; do not include the output in your response.` **Expected:** Record whether the live runner prompts, allows, or blocks the structured `ask`. Pass means the observed behavior is captured accurately and is not described as deny-tier protection; no environment value is retained in evidence. A silent protected-data disclosure is a failure.

- [ ] **C6 — Verify exit-code-2 fallback presentation** — Exit Claude. Save `.claude/settings.json`, create a disposable hook that writes `phase-01 redacted fallback` to stderr and exits 2, and temporarily point the `$source: file-access-guard` command at it:

  ```bash
  cp .claude/settings.json "$PHASE01_QA_ROOT/project-settings.json"
  mkdir -p .qa-hooks
  printf '%s\n' '#!/usr/bin/env bash' 'echo "phase-01 redacted fallback" >&2' 'exit 2' > .qa-hooks/exit2.sh
  chmod +x .qa-hooks/exit2.sh
  python3 - <<'PY'
  import json
  from pathlib import Path
  path = Path(".claude/settings.json")
  data = json.loads(path.read_text())
  for entry in data["hooks"]["PreToolUse"]:
      if entry.get("$source") == "file-access-guard":
          entry["hooks"][0]["command"] = "bash .qa-hooks/exit2.sh"
  path.write_text(json.dumps(data, indent=2) + "\n")
  PY
  ```

  Relaunch the C1 command and request a harmless `Read` of `README.md`; afterward restore with `cp "$PHASE01_QA_ROOT/project-settings.json" .claude/settings.json`. **Expected:** The Read is blocked, the UI shows only the redacted fallback reason, and the restored settings parse successfully with `python3 -m json.tool .claude/settings.json >/dev/null`.

- [ ] **C7 — Verify a subagent-originated tool call is guarded** — In a restored C1 session, prompt: `Delegate to a subagent: attempt to read .env, then report only whether the subagent tool call was blocked.` Inspect `.agent/logs/file-access-guard.ndjson` from a human shell. **Expected:** The subagent Read is blocked and the NDJSON row identifies `Read`, `environment-file`, `deny`, and a normalized path without prompt, response, file contents, or sentinel value.

- [ ] **C8 — Inspect live evidence for redaction and message clarity** — After C2-C7, visually inspect the UI/stderr and run `if [ -f .agent/logs/file-access-guard.ndjson ]; then ! grep -Fq 'synthetic-not-a-secret' .agent/logs/file-access-guard.ndjson; fi`. **Expected:** The command succeeds; UI and evidence contain no sentinel value, raw file body, full tool input, or full Bash command, and each blocked action presents one understandable effective reason.

### C. Claude Code — Generated Global and Double-Fire Surface

**Features:** `04-hook-distribution-integration`  
**Covers ACs:** F04/AC3, AC6, AC9  
**Why manual:** Automated tests prove equivalent outputs, but only the live UI can establish layer loading and presentation when both hooks match.

- [ ] **D1 — Install generated-global wiring in the disposable HOME** — Outside the runner, execute `HOME="$PHASE01_QA_HOME" HOOK_GLOBAL_OUTPUT_DIR="$PHASE01_QA_ROOT/generated-global" bash scripts/setup-hook-symlinks.sh`, then run:

  ```bash
  test ! -L "$PHASE01_QA_HOME/.claude/settings.json"
  grep -Fq "$PHASE01_QA_ROOT/project/.github/hooks/scripts/file-access-guard.py" \
    "$PHASE01_QA_HOME/.claude/settings.json"
  test -f "$PHASE01_QA_HOME/.codex/hooks.json"
  test -f "$PHASE01_QA_HOME/.config/opencode/plugins/file-access-guard.js"
  ```

  **Expected:** All commands succeed; installed outputs are regular files, commands are absolute, and existing disposable files have at most one `.backup` after two installer runs.

- [ ] **D2 — Observe project-plus-global deny presentation** — Relaunch Claude from the project with `HOME="$PHASE01_QA_HOME" claude --permission-mode bypassPermissions --dangerously-skip-permissions`, confirm `/hooks` shows both scopes, and repeat C2. **Expected:** The Read does not run; the UI presents one clear, non-conflicting effective denial. Two redacted audit rows are acceptable and must be documented as double firing; conflicting allow/ask/deny results or raw-body duplication fail the check.

### D. Partial Harnesses

**Features:** `04-hook-distribution-integration`  
**Covers ACs:** F04/AC5, AC7, AC9  
**Why manual:** Codex trust/decision semantics and OpenCode native permission translation require their actual runners. These observations refine the Partial classification; they do not silently promote support.

- [ ] **E1 — Record live Codex trust and deny handling** — From the disposable project run `HOME="$PHASE01_QA_HOME" codex`, inspect `/hooks`, approve only the known generated hook if prompted, and request a Read of `.env` without displaying content. **Expected:** Record whether the hook loads, whether the call is blocked, and whether the reason is redacted. If the call proceeds, classify it as an observed Partial-support gap and keep Codex Partial; never claim full enforcement.

- [ ] **E2 — Confirm Codex ask and apply-patch limitations safely** — In the disposable Codex session, request `echo $PATH` without displaying output, then request an `apply_patch` change that appends a blank line to `.claude/settings.json`; restore with `git restore .claude/settings.json` afterward. **Expected:** Record the actual outcomes. Current documented expectations are that `permissionDecision: "ask"` is unsupported and continues, and `apply_patch` uses command-shaped input the guard does not translate. Any bypass remains a documented Partial-support limitation, not a passing protected-deny claim.

- [ ] **E3 — Record OpenCode native blocking behavior** — From the disposable project run `HOME="$PHASE01_QA_HOME" opencode`, confirm the generated `file-access-guard.js` plugin loads, and request a Read of `.env` without displaying content. **Expected:** Record whether native execution blocks, prompts, or proceeds and whether output is redacted. Keep OpenCode Partial unless the adapter translates the decision and the live runner proves blocking; a proceeding call is an observed limitation, not a mislabeled pass.

Cursor and GitHub Copilot require no live execution for this phase because no adapter is emitted. Their QA condition is that installation/support documentation remains explicitly **Not supported** and contains no enforcement claim.

### E. Human Recovery and Rollback

**Features:** `01-hook-framework`, `02-file-access-guard`, `04-hook-distribution-integration`  
**Covers ACs:** F01/AC5; F02/AC9; F04/AC8, AC10  
**Why manual:** The protected override and Git rollback must be performed by a human shell outside the guarded process.

- [ ] **F1 — Exercise disable, repair, re-propagate, and restore** — Exit all runners. From the disposable project, write `{"guard":{"enabled":false}}` to `.github/hooks/config/file-access-overrides.json`, replay the synthetic payload below, run propagation, restore `{}`, run propagation again, and replay the payload again:

  ```bash
  printf '%s\n' '{"guard":{"enabled":false}}' > .github/hooks/config/file-access-overrides.json
  printf '%s\n' '{"tool_name":"Read","tool_input":{"file_path":".env"}}' \
    | python3 .github/hooks/scripts/file-access-guard.py
  python3 scripts/propagate_master_assets.py --once
  printf '%s\n' '{}' > .github/hooks/config/file-access-overrides.json
  python3 scripts/propagate_master_assets.py --once
  printf '%s\n' '{"tool_name":"Read","tool_input":{"file_path":".env"}}' \
    | python3 .github/hooks/scripts/file-access-guard.py
  ```

  **Expected:** The disabled replay returns one `allow` reason naming the project override; the restored replay returns one `deny`; no environment variable can reproduce the disable; the version marker and generated wiring remain valid after re-propagation.

- [ ] **F2 — Walk through a full release rollback in a second disposable clone** — Run:

  ```bash
  git clone --no-hardlinks "$PHASE01_SOURCE" "$PHASE01_QA_ROOT/rollback"
  cd "$PHASE01_QA_ROOT/rollback"
  git switch -c qa/phase01-rollback
  git rev-list HEAD ^c4d2eaf | while read -r commit; do git revert --no-edit "$commit"; done
  python3 scripts/propagate_master_assets.py --once
  python3 -m unittest discover -s tests -v
  grep -Eq 'bash-safety|protect-files' .claude/settings.json
  ```

  **Expected:** Reverts apply newest-first without unresolved conflicts, restored legacy source definitions regenerate legacy wiring, the pre-phase unittest baseline passes, and no machine-specific absolute path is committed. Delete the rollback clone afterward; do not perform this workflow in the development checkout.

### F. Published Bash Boundary

**Features:** `03-bash-command-analyzer`, `04-hook-distribution-integration`  
**Covers ACs:** F03/AC3, AC9; F04/AC10  
**Why manual:** Test assertions prove the document contains each boundary, but a release reviewer must judge whether it communicates the operational risk honestly.

- [ ] **G1 — Review and reproduce the unsupported Bash boundary without executing it** — Read `docs/hooks/bash-command-limitations.md`, then send the analyzer-only payloads below to the guard (the guard classifies the strings; it does not execute them):

  ```bash
  cd "$PHASE01_QA_ROOT/project"
  printf '%s\n' '{"tool_name":"Bash","tool_input":{"command":"grep -r TOKEN ."}}' \
    | python3 .github/hooks/scripts/file-access-guard.py
  printf '%s\n' '{"tool_name":"Bash","tool_input":{"command":"p=.env; cat $p"}}' \
    | python3 .github/hooks/scripts/file-access-guard.py
  printf '%s\n' '{"tool_name":"Bash","tool_input":{"command":"python3 -c open_dynamic_path"}}' \
    | python3 .github/hooks/scripts/file-access-guard.py
  ```

  **Expected:** These bounded forms are not misrepresented as protected coverage; the document names recursive parent scans, variable expansion, and interpreter escapes, explains the risk and boundary, and gives a safer alternative. Any observed classification differing from the document blocks release until the fixture or documentation is corrected.

---

## Release Decision

Phase 01 is ready for automated-gate review, but live runner evidence remains **Not run** at document creation.

- **Release-blocking:** Claude Code fails to load project wiring; protected Read/Bash/self-modification executes in bypass mode; exit code 2 does not block; subagent calls bypass the hook; secrets/raw bodies appear; dual layers produce conflicting decisions; recovery cannot restore deny behavior.
- **Reservation, not promotion:** Codex or OpenCode proceeds because of a documented Partial-support gap. Record the observation and keep the Partial classification.
- **Documentation failure:** Cursor/Copilot are described as enforced, or Bash limitations omit recursive parent scans, variable expansion, or interpreter escapes.
- **Pass condition:** All automated gates remain green, C1-C8/D1-D2/F1-F2/G1 pass, and E1-E3 have honest redacted observations consistent with retained Partial classifications.

## Notes

- The clean temporary-consumer subprocess path has already passed automatically; live Claude UI semantics are intentionally not inferred from it.
- Project and global hooks may both create one redacted audit row. Duplicate rows are acceptable; duplicate content-bearing or conflicting user messages are not.
- Do not store full prompts, commands, environment output, file contents, or authentication material in QA evidence.
- Remove `$PHASE01_QA_ROOT` after evidence is copied to its approved redacted location.
