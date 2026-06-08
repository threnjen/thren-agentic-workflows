using System;

namespace Threnjen.VisualVerification {
  // Machine-readable record of a capture run, written alongside the PNGs so a downstream
  // reviewer (human or agent) gets structured input instead of globbing a directory.
  [Serializable]
  public class CaptureManifest {
    public string generatedAtUtc;
    public string config;
    public Shot[] shots;
  }

  [Serializable]
  public class Shot {
    public string scene;
    public int frame;
    // Path relative to the project root, forward-slashed.
    public string path;
    public int width;
    public int height;
  }
}
