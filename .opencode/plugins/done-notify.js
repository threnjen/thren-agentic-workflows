// Generated from .github/hooks source-of-truth. Do not edit manually.
export const DoneNotify = async ({ $ }) => {
  return {
    "session.idle": async (_input, _output) => {
      await $`osascript -e 'display notification "OpenCode is done" with title "OpenCode"'`
    }
  }
}
