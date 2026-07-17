# OpenCode Managed-Copy Setup

This legacy filename remains as a compatibility entry point. Runtime symlink setup is retired.

Generate repository outputs with `python3 scripts/propagate_master_assets.py --once`, require successful fixed-point convergence, then pass the result through `resolve_destinations_after_convergence`. Review the destination inventory for the active `OPENCODE_CONFIG_DIR` (or documented default), expected agent and skill rosters, ownership evidence, and collisions. Only after review, invoke `deploy_managed_copies_after_convergence`.

Verify that OpenCode agents and skills are fresh regular managed copies, foreign content is preserved, the second run makes no changes, and a fresh OpenCode session discovers the expected assets. Project-local deployment is out of scope; do not create a project-local runtime-link fallback. Generated notification plugins remain outside this managed asset roster until a documented deployment API supports them.

On partial failure, preserve the previous usable state, do not prune the failed harness, report the exact category, and rerun after remediation. Never use the retired link model as rollback.
