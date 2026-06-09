# Changelog

All notable changes to `com.threnjen.visual-verification` are documented here.
This project adheres to [Semantic Versioning](https://semver.org/).

## [0.2.0]

### Added
- Quick-start checklist in the README.
- Importable **Capture config template** sample (Package Manager → Samples → Import),
  so consumers don't hand-author the config from scratch.
- Editor menu **Tools → Visual Verification → Create Config For Active Scene**, which writes
  `Assets/VisualVerification/capture-config.json` pre-filled with the open scene's name.
- `CHANGELOG.md` and `LICENSE.md`.

### Changed
- Capture now self-explains its preconditions instead of surfacing raw engine errors:
  a clear message when the configured scene is missing from Build Settings, and a one-time
  warning when no camera change is detected across stepped frames (a sign the simulation may
  be wall-clock-driven rather than `Time.deltaTime`-driven, which breaks determinism).

## [0.1.0]

### Added
- Initial release: deterministic PlayMode screenshot capture driven by a JSON config.
  Loads a scene by name, steps a fixed number of frames under `Time.captureDeltaTime`, and
  writes PNGs plus a `manifest.json`. References only `UnityEngine` and the test runner.
