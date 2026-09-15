import type { Plugin } from "@opencode-ai/plugin"

// <!-- crosswire-comms-registration -->
const CROSSWIRE_CONFIG_PATH = "__CROSSWIRE_CONFIG_PATH__"

type IdleEvent = {
  type: "session.idle"
  properties: { sessionID: string }
}

const invokeCrosswire = async (input: Parameters<Plugin>[0], event: IdleEvent) => {
  const payload = JSON.stringify({
    event: {
      type: event.type,
      properties: { sessionID: event.properties.sessionID },
    },
    pluginInput: {
      directory: input.directory,
      worktree: input.worktree,
      project: {
        id: input.project.id,
        worktree: input.project.worktree,
      },
    },
  })

  try {
    const process = Bun.spawn(
      [
        "crosswire-turn-hook",
        "--adapter",
        "opencode",
        "--config",
        CROSSWIRE_CONFIG_PATH,
      ],
      {
        cwd: input.directory,
        stdin: "pipe",
        stdout: "ignore",
        stderr: "ignore",
      },
    )
    try {
      process.stdin.write(`${payload}\n`)
      process.stdin.end()
      await process.exited
    } catch (error) {
      try {
        process.kill()
      } catch {
        // The child may have exited while the input stream failed.
      }
      await process.exited.catch(() => undefined)
      throw error
    }
  } catch (error) {
    console.error("crosswire OpenCode idle hook failed", error)
  }
}

const CrosswireCommsPlugin: Plugin = async (input) => ({
  event: async ({ event }) => {
    if (event.type !== "session.idle") {
      return
    }
    await invokeCrosswire(input, event)
  },
})

export default CrosswireCommsPlugin
