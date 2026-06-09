using System.IO;
using UnityEditor;
using UnityEngine;
using UnityEngine.SceneManagement;

namespace Threnjen.VisualVerification.Editor {
  // Scaffolds a capture-config.json pre-filled with the currently open scene, so consumers
  // don't hand-author it. Writes to the consuming project's Assets/VisualVerification/.
  static class CreateConfigMenu {
    const string MenuPath = "Tools/Visual Verification/Create Config For Active Scene";
    const string ConfigDir = "Assets/VisualVerification";
    const string ConfigPath = ConfigDir + "/capture-config.json";

    [MenuItem(MenuPath)]
    static void CreateConfig() {
      Scene scene = SceneManager.GetActiveScene();
      string sceneName = string.IsNullOrEmpty(scene.name) ? "YourScene" : scene.name;

      if (File.Exists(ConfigPath) &&
          !EditorUtility.DisplayDialog(
            "Visual Verification",
            $"{ConfigPath} already exists.\n\nOverwrite it with a config for scene '{sceneName}'?",
            "Overwrite", "Cancel")) {
        return;
      }

      Directory.CreateDirectory(ConfigDir);
      File.WriteAllText(ConfigPath, BuildConfigJson(sceneName));
      AssetDatabase.Refresh();
      Debug.Log($"[Visual Verification] Wrote {ConfigPath} for scene '{sceneName}'.");

      if (!IsSceneInBuildSettings(scene.path)) {
        Debug.LogWarning(
          $"[Visual Verification] Scene '{sceneName}' is not enabled in Build Settings. " +
          "Add it via File → Build Settings, or capture cannot load it by name.");
      }

      TextAsset asset = AssetDatabase.LoadAssetAtPath<TextAsset>(ConfigPath);
      if (asset != null) EditorGUIUtility.PingObject(asset);
    }

    static string BuildConfigJson(string sceneName) {
      return
$@"{{
  ""outputDir"": ""dev/screenshots"",
  ""scenes"": [
    {{
      ""scene"": ""{sceneName}"",
      ""captureDeltaTime"": 0.0166667,
      ""captureFrames"": [0, 60, 120],
      ""width"": 960,
      ""height"": 720,
      ""namePrefix"": ""{sceneName}""
    }}
  ]
}}
";
    }

    static bool IsSceneInBuildSettings(string scenePath) {
      if (string.IsNullOrEmpty(scenePath)) return false;
      foreach (EditorBuildSettingsScene s in EditorBuildSettings.scenes) {
        if (s.enabled && s.path == scenePath) return true;
      }
      return false;
    }
  }
}
