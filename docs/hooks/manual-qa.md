# Hook Distribution Manual QA

## Automated evidence

The focused suites cover the shared framework, injection scanner, injection
corpus, generated hook distribution, ownership-safe retired-asset cleanup, and
propagation idempotency. They also verify behavioral absence: ordinary Read and
Bash payloads do not produce a file-access decision or audit row.

## Manual evidence — NOT RUN

1. Create a disposable consuming repository and propagate the hook assets twice.
2. Inspect Claude Code, Codex, and OpenCode hook rosters. Confirm the injection
   scanner and unrelated hooks remain, with no file-access guard or automatic RTK
   rewrite registration.
3. Exercise benign Read and Bash operations without displaying secret content.
   Confirm no retired prompt, denial, decision, or audit file appears.
4. Feed a synthetic prompt-injection fixture through a PostToolUse event and
   confirm it is blocked or redacted.
5. Run an explicit `rtk git status`; confirm RTK is available. Run an unprefixed
   benign command and confirm it is not rewritten automatically.
6. Add same-named unowned retired assets to a disposable consumer and confirm
   propagation preserves them.

Record runner versions, results, and artifact paths. Do not record live secret
values. Prompt-injection defense is **not a replacement** for the removed
protected-file or Bash-command controls.
