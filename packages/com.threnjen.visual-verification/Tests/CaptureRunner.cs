using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;
using UnityEngine.SceneManagement;

namespace Threnjen.VisualVerification {
  // Deterministic scene-capture. Loads a scene by name, drives it under a fixed delta time,
  // and reads the camera's rendered frame into PNGs at the requested frame indices.
  //
  // Determinism: Time.captureDeltaTime forces every frame to advance the sim by a fixed dt
  // regardless of wall-clock, so frame N is reproducible. The consuming scene must drive its
  // simulation from Time.deltaTime (not wall-clock) for this to hold.
  //
  // URP-safe capture: the camera renders into a RenderTexture every frame (targetTexture set
  // for the whole run); ReadPixels then reads the most recently rendered frame without a
  // manual camera.Render() call, which is unreliable under URP. ReadPixels does not advance
  // the frame, so capture never perturbs the frame count.
  public static class CaptureRunner {
    const int DefaultWidth = 960;
    const int DefaultHeight = 720;
    const float DefaultDeltaTime = 1f / 60f;
    const int DefaultFrame = 120;

    public static IEnumerator CaptureScene(SceneCapture cfg, string outputDirAbs, string outputDirRel, List<Shot> shots) {
      float dt = cfg.captureDeltaTime > 0f ? cfg.captureDeltaTime : DefaultDeltaTime;
      int w = cfg.width > 0 ? cfg.width : DefaultWidth;
      int h = cfg.height > 0 ? cfg.height : DefaultHeight;
      string prefix = string.IsNullOrEmpty(cfg.namePrefix) ? cfg.scene : cfg.namePrefix;

      var wanted = new SortedSet<int>();
      if (cfg.captureFrames != null && cfg.captureFrames.Length > 0) {
        foreach (int f in cfg.captureFrames) {
          if (f >= 0) wanted.Add(f);
        }
      }
      if (wanted.Count == 0) wanted.Add(DefaultFrame);

      int maxFrame = 0;
      foreach (int f in wanted) maxFrame = Mathf.Max(maxFrame, f);

      Time.captureDeltaTime = dt;
      try {
        SceneManager.LoadScene(cfg.scene);
        yield return null; // scene load + Start() wiring (spawns units, etc.)

        Camera cam = Camera.main;
        if (cam == null) {
          throw new System.InvalidOperationException(
            $"Scene '{cfg.scene}' has no camera tagged MainCamera; cannot capture.");
        }

        var rt = new RenderTexture(w, h, 24);
        cam.targetTexture = rt;          // render into rt every frame for the whole run
        var tex = new Texture2D(w, h, TextureFormat.RGB24, false);

        for (int frame = 0; frame <= maxFrame; frame++) {
          yield return null;             // one sim step + URP renders this frame into rt
          if (!wanted.Contains(frame)) continue;

          RenderTexture prevActive = RenderTexture.active;
          RenderTexture.active = rt;
          tex.ReadPixels(new Rect(0, 0, w, h), 0, 0);
          tex.Apply();
          RenderTexture.active = prevActive;

          string fileName = $"{prefix}-frame{frame}.png";
          File.WriteAllBytes(Path.Combine(outputDirAbs, fileName), tex.EncodeToPNG());
          shots.Add(new Shot {
            scene = cfg.scene,
            frame = frame,
            path = $"{outputDirRel}/{fileName}",
            width = w,
            height = h
          });
        }

        cam.targetTexture = null;
        Object.Destroy(tex);
        rt.Release();
        Object.Destroy(rt);
      } finally {
        Time.captureDeltaTime = 0f;
      }
    }
  }
}
