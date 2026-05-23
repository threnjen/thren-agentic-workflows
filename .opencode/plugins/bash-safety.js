// Generated from .github/hooks source-of-truth. Do not edit manually.
export const BashSafety = async ({ $ }) => {
  return {
    "pre_tool_call": async (_input, _output) => {
      await $`bash .github/hooks/scripts/bash-safety.sh`
    }
  }
}
