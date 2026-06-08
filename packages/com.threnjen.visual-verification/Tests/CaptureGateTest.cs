using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.TestTools;

namespace Threnjen.VisualVerification {
  // PlayMode entry point. A consuming project adds this package to `testables`, provides a
  // capture-config.json, and runs:
  //   Unity.exe -batchmode -runTests -testPlatform PlayMode -projectPath . ...
  // (no -quit, no -nographics). The test produces the screenshots + manifest; judgement of
  // the frames against visual acceptance criteria happens outside the package.
  public class CaptureGateTest {
    const string ConfigEnvVar = "VISUAL_VERIFICATION_CONFIG";
    const string DefaultConfigRelative = "VisualVerification/capture-config.json"; // under Assets/
    const string DefaultOutputDir = "dev/screenshots";

    [UnityTest]
    public IEnumerator Capture_From_Config() {
      string projectRoot = Path.GetFullPath(Path.Combine(Application.dataPath, ".."));

      string configPath = ResolveConfigPath(projectRoot);
      Assert.IsTrue(File.Exists(configPath),
        $"Capture config not found at '{configPath}'. Set {ConfigEnvVar} or create Assets/{DefaultConfigRelative}.");

      CaptureConfig config = JsonUtility.FromJson<CaptureConfig>(File.ReadAllText(configPath));
      Assert.IsNotNull(config, $"Could not parse capture config at '{configPath}'.");
      Assert.IsTrue(config.scenes != null && config.scenes.Length > 0,
        $"Capture config '{configPath}' lists no scenes.");

      string outputDirRel = string.IsNullOrEmpty(config.outputDir) ? DefaultOutputDir : config.outputDir.Replace('\\', '/').TrimEnd('/');
      string outputDirAbs = Path.GetFullPath(Path.Combine(projectRoot, outputDirRel));
      Directory.CreateDirectory(outputDirAbs);

      var shots = new List<Shot>();
      foreach (SceneCapture sc in config.scenes) {
        Assert.IsFalse(string.IsNullOrEmpty(sc.scene), "Capture config has a scene entry with no name.");
        yield return CaptureRunner.CaptureScene(sc, outputDirAbs, outputDirRel, shots);
      }

      var manifest = new CaptureManifest {
        generatedAtUtc = DateTime.UtcNow.ToString("o"),
        config = configPath,
        shots = shots.ToArray()
      };
      string manifestPath = Path.Combine(outputDirAbs, "manifest.json");
      File.WriteAllText(manifestPath, JsonUtility.ToJson(manifest, true));
      Debug.Log($"VISUAL_VERIFICATION_MANIFEST={manifestPath}");

      Assert.Greater(shots.Count, 0, "No screenshots were captured.");
      foreach (Shot s in shots) {
        string abs = Path.GetFullPath(Path.Combine(projectRoot, s.path));
        Assert.IsTrue(File.Exists(abs), $"Expected screenshot was not written: {s.path}");
      }
    }

    static string ResolveConfigPath(string projectRoot) {
      string env = Environment.GetEnvironmentVariable(ConfigEnvVar);
      if (!string.IsNullOrEmpty(env)) {
        return Path.IsPathRooted(env) ? env : Path.GetFullPath(Path.Combine(projectRoot, env));
      }
      return Path.GetFullPath(Path.Combine(Application.dataPath, DefaultConfigRelative));
    }
  }
}
