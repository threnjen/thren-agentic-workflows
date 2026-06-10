using System;

namespace Threnjen.VisualVerification {
  // Config model loaded from the consuming project (JSON, deserialized via JsonUtility).
  // The package references no consumer assemblies: scenes are addressed by name, never by
  // type. A scene named here must be loadable (present in Build Settings).
  [Serializable]
  public class CaptureConfig {
    // Output directory for PNGs + manifest, relative to the project root (the folder
    // containing Assets/). Defaults to "dev/screenshots" when empty.
    public string outputDir;

    public SceneCapture[] scenes;
  }

  [Serializable]
  public class SceneCapture {
    // Scene name as listed in Build Settings.
    public string scene;

    // Fixed delta time applied to every frame so the simulation is reproducible
    // regardless of wall-clock. Defaults to 1/60 when <= 0.
    public float captureDeltaTime;

    // Frame indices (number of stepped frames since scene load) at which to grab a PNG.
    // Defaults to a single frame at 120 when empty.
    public int[] captureFrames;

    // Capture resolution. Default 960x720 when <= 0.
    public int width;
    public int height;

    // Output file prefix; defaults to the scene name when empty.
    public string namePrefix;
  }
}
