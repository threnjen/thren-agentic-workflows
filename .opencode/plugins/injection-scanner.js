// Generated from .github/hooks source-of-truth. Do not edit manually.
export const InjectionScanner = async ({ directory }) => {
  return {
    "tool.execute.after": async (input, output) => {
      const payload = {
        hook_event_name: "PostToolUse",
        tool_name: input.tool,
        tool_input: input.args ?? {},
        tool_output: output.output,
        tool_output_truncated: false,
        session_id: input.sessionID
      }
      const proc = Bun.spawnSync(["python3", ".github/hooks/scripts/injection-scanner.py"], {
        cwd: directory,
        stdin: new TextEncoder().encode(JSON.stringify(payload)),
        stdout: "pipe", stderr: "pipe"
      })
      const stdout = new TextDecoder().decode(proc.stdout)
      let result
      try { result = JSON.parse(stdout) } catch { result = null }
      const context = result?.hookSpecificOutput?.additionalContext
      const isBlock = result?.decision === "block" && typeof result.reason === "string"
      const isWarn = result?.decision === undefined && typeof context === "string" && context.length > 0
      const isAllow = result && Object.keys(result).length === 0
      if (proc.exitCode !== 0 || (!isBlock && !isWarn && !isAllow)) {
        output.output = "Injection scanner blocked tool output. guard error"
      } else if (isBlock) {
        output.output = result.reason
      } else if (isWarn) {
        output.output += `\n\n${context}`
      }
    }
  }
}
