# Codex Pilot Slice Plan — Historical Record

This document records the original pilot used to validate Codex porting across global guidance, a custom agent, and a skill. It is historical and non-operational. Its former runtime-link installation steps are retired and must not be followed.

The pilot selected `output-verbosity-policy.instructions.md`, the Feature Decomposer agent, and the `feature-plan-set` skill because together they exercised metadata removal, TOML agent rendering, and skill-directory propagation. Those selection and portability conclusions remain useful history.

Current installation uses the managed-copy workflow in [HARNESS_SETUP.md](../HARNESS_SETUP.md): fixed-point repository convergence, reviewed destination inventory, `scripts/propagate_master_assets.py --runtime-deploy`, fixed-point rerun, and fresh-session discovery. Native Windows and WSL require separate runs; unavailable evidence is `NOT RUN`.

This record is intentionally not an alternate setup path. Future pilot validation must use regular managed copies and the current generated roster.
