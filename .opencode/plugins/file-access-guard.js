// Generated from .github/hooks source-of-truth. Do not edit manually.
export const FileAccessGuard = async ({ $ }) => {
  return {
    "tool.execute.before": async (_input, _output) => {
      await $`python3 .github/hooks/scripts/file-access-guard.py`
    }
  }
}
