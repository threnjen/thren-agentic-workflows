// Generated from .github/hooks source-of-truth. Do not edit manually.
export const AuditLog = async ({ $ }) => {
  return {
    "post_tool_call": async (_input, _output) => {
      await $`bash .github/hooks/scripts/audit-log.sh`
    }
  }
}
