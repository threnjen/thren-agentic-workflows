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

## Install

Add to the consuming project's `Packages/manifest.json`:

```jsonc
{
  "dependencies": {
    "com.threnjen.visual-verification":
      "https://github.com/threnjen/github-agents-source-of-truth.git?path=/packages/com.threnjen.visual-verification#visual-verification/v0.1.0"
  },
  "testables": [ "com.threnjen.visual-verification" ]
}
```

`testables` is required — it tells Unity to include this package's PlayMode test (the capture
entry point) in the project's test run.

## Configure

Create `Assets/VisualVerification/capture-config.json` (or point the
`VISUAL_VERIFICATION_CONFIG` environment variable at any path):

```jsonc
{
  "outputDir": "dev/screenshots",
  "scenes": [
    {
      "scene": "CombatSandbox",        // must be in Build Settings
      "captureDeltaTime": 0.0166667,   // fixed dt per frame; default 1/60
      "captureFrames": [0, 60, 120],   // frame indices to grab; default [120]
      "width": 960,                    // default 960
      "height": 720,                   // default 720
      "namePrefix": "combat"           // default: scene name
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
    { "scene": "CombatSandbox", "frame": 0,   "path": "dev/screenshots/combat-frame0.png",   "width": 960, "height": 720 },
    { "scene": "CombatSandbox", "frame": 120, "path": "dev/screenshots/combat-frame120.png", "width": 960, "height": 720 }
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
