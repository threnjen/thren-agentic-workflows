# Retired Bash Command Analyzer

The repository Bash command analyzer and automatic `rtk-rewrite.sh` integration
were retired in Phase 04. The repository no longer parses Bash commands to infer
file access, enforce protected-file rules, or rewrite unprefixed commands.

This retirement does not remove RTK. Use explicit `rtk` prefixes where current
repository instructions recommend them. Prompt-injection scanning remains a
PostToolUse output control and is **not a replacement** for Bash authorization or
file-access enforcement.

Historical phase and security records may still describe the former analyzer;
those records are evidence of past behavior, not active operating guidance.
