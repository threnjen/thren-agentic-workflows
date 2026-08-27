# Extracted from `source_of_truth/skills/unity-development/SKILL.md`

This section sat between `Serialized Assets: Generate via Unity, Never Hand-Author` and `## Pre-Handoff Checklist (Unity-Specific)`.

## Visual Verification Wiring

For a View feature whose phase has visual acceptance criteria, set up its visual test the same
way you set up unit tests for logic — it is part of "done," not an afterthought. The capture
mechanism is config-driven (a generic PlayMode capture package, e.g.
`com.threnjen.visual-verification`), so "writing the visual test" means wiring the project to run
it, not authoring per-feature test code:

1. **Ensure the capture package is a dependency — default to the bundled companion.** This agent
   pack ships with a companion capture package; wire it by default so a fresh repo needs no manual
   setup. Unless the project documents an override, ensure `Packages/manifest.json` contains the
   dependency **and** a top-level `testables` entry (note `testables` is a sibling of `dependencies`,
   not nested inside it):
   ```jsonc
   {
     "dependencies": {
       "com.threnjen.visual-verification": "https://github.com/threnjen/thren-agentic-workflows.git?path=/packages/com.threnjen.visual-verification#com.threnjen.visual-verification/v0.2.1"
       // …existing dependencies…
     },
     "testables": [ "com.threnjen.visual-verification" ]
   }
   ```
   If the project documents a different capture package (a fork, or a newer tag), use that instead.
   This is the single source for the default — bump the pinned `com.threnjen.visual-verification/vX.Y.Z` tag here
   when the companion package releases. (The default resolves only if the companion repo is reachable
   from the consuming machine; for private forks, document the override.)
2. **Create or update the capture config.** Ensure `Assets/VisualVerification/capture-config.json`
   (root layout) or `game/Assets/VisualVerification/capture-config.json` (nested layout) exists,
   with an entry for the scene this feature renders: the scene name, resolution, and capture
   frames **chosen to fit the AC** — they are not a fixed magic list. A static-layout AC ("two
   teams in distinct colors") needs only one settled frame. A motion/animation AC ("units close
   on each other", "the cube rotates") needs several well-spread frames including an intermediate
   one, because endpoints can coincide (e.g. a 90° rotation of a symmetric object looks like 0°).
   Reuse the existing config if the scene is already covered.
3. **Confirm the scene is loadable.** The capture loads the scene by name, so it must be in Build
   Settings and have a `MainCamera`-tagged camera.

Record in the implementation record which scene the config covers and which visual ACs the captured
frames are meant to demonstrate, so the Visual Verifier (and the orchestrator's visual gate) have a
clear target.
