# afl-rl-engine — AFL SuperCoach RL valuation engine

**Start here: `START_HERE.md`** (3-step resume: `bootstrap.sh` → `verify_restore.sh` → hold).

Current baked board: **BAKED v2.7 2026-07-10** (Chapter-3 injury/availability + R-i=advance). Restore seed: final checkpoint 2026-07-02 (lineage root below).
- engine head: `7a07e369` (BAKED v2.7; was `c47cb43d` at v2.4) · rl_model.py: `4cd7e37f` · store: `a2fbc9a0` · band: `34faa865` · config: `69ead79b` · board: `e2c9bc51` · book stable-seal: `2a74c731`
- lineage: `e0ac9c37 → 8aed420a → c47cb43d` (v2.4) `→ efea88e5` (v2.5) `→ 4b08796c` (v2.6) `→ 7a07e369` (v2.7). Full identity + resume steps: `START_HERE.md`.
- source bundle (restore seed): `rl_complete_8aed420a_final2026-07-02.tar.gz` (md5 `414706b0eb8b90d32c05f96c323dbc7b`)
- restore-verified in three environments (build container, offline clean extraction, repo-seeding container): 9 PASS / 0 FAIL, panel 10/10.

Process rules: `docs/process/`. Required external inputs: `REQUIRED_INPUTS.md`. Nothing bakes without Luke's explicit go.
