# Visual Verification

Deterministic PlayMode screenshot capture for visual acceptance testing.

It loads a scene, steps a fixed number of frames under a fixed delta time, and writes PNGs
plus a `manifest.json`. A downstream reviewer — a human, or a multimodal agent — judges the
frames against the project's visual acceptance criteria. **The package captures; it does not
judge.** That split keeps it free of brittle golden images.

Why it exists: code can compile clean, pass every unit test, and pass static review while
rendering nothing usable (invisible/miscolored output, broken scene wiring, a blank frame).
The only proof is a rendered frame, looked at. This produces that frame reproducibly and
headlessly.

## Quick start

1. **Install** — add the dependency + `testables` to `Packages/manifest.json` (see below).
2. **Configure** — get a `capture-config.json` into `Assets/VisualVerification/`. Either
   **Tools → Visual Verification → Create Config For Active Scene** (fills in the open scene),
   or import the **Capture config template** sample (Package Manager → this package → Samples),
   then set your scene name.
3. **Preconditions** — the scene is in Build Settings, has a `MainCamera`, and drives its
   simulation from `Time.deltaTime` (not wall-clock). See [Requirements](#requirements--notes).
4. **Run** — the `-runTests -testPlatform PlayMode` command below. PNGs + `manifest.json`
   land in `outputDir`.
5. **Judge** — look at the frames, or let the Visual Verifier agent assess them against the
   phase's visual ACs.

## Install

Add to the consuming project's `Packages/manifest.json`:

```jsonc
{
  "dependencies": {
    "visual-verification":
      "https://github.com/threnjen/thren-agentic-workflows.git?path=/packages/visual-verification#visual-verification/v0.2.1"
  },
  "testables": [ "visual-verification" ]
}
```

`testables` is required — it tells Unity to include this package's PlayMode test (the capture
entry point) in the project's test run.

## Configure

Get a `capture-config.json` into `Assets/VisualVerification/`. Fastest paths:

- **Editor menu:** *Tools → Visual Verification → Create Config For Active Scene* — writes the
  file pre-filled with the currently open scene's name.
- **Sample:** *Package Manager → Visual Verification → Samples → Capture config template →
  Import*, then move it to `Assets/VisualVerification/capture-config.json` and set the scene.

Or point the `VISUAL_VERIFICATION_CONFIG` environment variable at any path. The schema:

```jsonc
{
  "outputDir": "dev/screenshots",
  "scenes": [
    {
      "scene": "YourScene",            // must be in Build Settings
      "captureDeltaTime": 0.0166667,   // fixed dt per frame; default 1/60
      "captureFrames": [0, 60, 120],   // frame indices to grab; default [120]
      "width": 960,                    // default 960
      "height": 720,                   // default 720
      "namePrefix": "frame"            // default: scene name
    }
  ]
}
```

## Run

```
Unity.exe -batchmode -runTests -testPlatform PlayMode -projectPath . \
  -testResults playmode-results.xml -logFile playmode.log
```

No `-quit` (it would quit before tests run) and no `-nographics` (capture needs the GPU).
Verify by confirming `playmode-results.xml` shows the capture test passed and that the PNGs +
`manifest.json` exist under `outputDir`. Exit code 0 alone is not proof.

If the project has other PlayMode tests, target just this one with
`-testFilter "Threnjen.VisualVerification.*"`.

## Output

`outputDir` receives `<namePrefix>-frame<N>.png` for each captured frame, plus:

```jsonc
{
  "generatedAtUtc": "2026-06-07T12:00:00Z",
  "config": "<resolved config path>",
  "shots": [
    { "scene": "YourScene", "frame": 0,   "path": "dev/screenshots/frame-frame0.png",   "width": 960, "height": 720 },
    { "scene": "YourScene", "frame": 120, "path": "dev/screenshots/frame-frame120.png", "width": 960, "height": 720 }
  ]
}
```

## Requirements & notes

- The scene must have a `MainCamera`-tagged camera and be present in Build Settings.
- The scene's simulation must advance from `Time.deltaTime` (a parameter-driven sim), not
  wall-clock, for determinism to hold.
- Screen-Space-Overlay UI does not render into the capture RenderTexture; world-space content
  does. Capture reflects what the camera sees.
- The package references only `UnityEngine` and the test runner — never consumer assemblies.
  Scenes are addressed by name, so no project-specific types leak into the package.
