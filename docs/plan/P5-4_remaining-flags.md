# P5-4 — The six unpinned env reads, and the v0-surface refit lane out of the engine (MEDIUM)

**Depends on.** P5-1 (same file, serial). P4-3 (engine_head and rl_model move in-transaction). Before P5-5, which
needs a replacement for the RL_LSYM_TAB re-derivation hook.

**Done when.** No engine file reads an RL_* name that is neither a data/model_config.json `vars` entry nor in
config_manifest.INFRA_ALLOW, except the deliberate signature read below; the refit lane lives in a tool that
writes data/v0surf.pkl offline; the board is byte-identical.

**Facts — the counted list (script: every `os.environ.get/[...]` of a literal RL_/PAR_ name in code, minus the 90
manifest vars and INFRA_ALLOW; checked at ffb2663b).** Six names, ten sites in the engine plus two in one_source_selftest.py:
1. RL_UNCOMP_S — rl_model.py:924 (dev grid override).
2. RL_LSYM_TAB — _merged_recover.py:299 (L-SYMMETRY re-derivation override; default = the sealed literal :294-296).
3. RL_V0SURF_REFIT — _merged_recover.py:1994, :2101, :2440, :3196, :3200; engine/rl_after/one_source_selftest.py:752, :759.
4. RL_V0_LENS — :2133; 5. RL_LENS_BASIS — :2163; 6. RL_LANE_EXPECT — :2382 (all three inside the refit lane).
- The refit lane is the `else:` branch at :2130 through ~:2438 (frozen load :2102-2107; the no-silent-refit HALT
  :2108-2129, whose message names the refit command). It reads docs/evidence/exec_306_zlaarm/basis/*.json
  (:2163-2165, :2382-2384). The driver is session_2026-07-18/legf6/scripts/refit_v0surf.py (exists).
- NOT in scope, and must stay: the signature read `os.environ.get(g, d) for g, d in _V0SURF_GATES` (:2051). Of its
  39 names, 37 are manifest vars and RL_GAMMA's literal (0.85) DIFFERS from the manifest ('1.0'): replacing the env
  read with the literals would change the frozen signature and HALT every build. RL_DAMP_K and RL_M3_FE (not
  manifest vars) take their literal defaults because gate mode refuses them if set (config_manifest.py:121-128).
- engine/rl_after/ingestion/forward_lens.py:129 reads the contract's `must_be_unset` list, not an env name; it is
  round-lane code (P4-4).
- The pinned dials (RL_O45, RL_O49, RL_DAMP, RL_EVW, RL_LEGF, RL_M3_INPROG_Y, RL_UNCONSERVE rl_model.py:926 …) are
  config identity (README) and are NOT removed here.

**The contract field.** `must_be_unset` (data/release_contract.json; DEFAULT_MUST_UNSET release_contract.py:48 =
RL_UNCOMP_S, RL_LSYM_TAB, RL_V0SURF_REFIT) is in BAKE_LANE_FROZEN (:361-363): the contract step's
restamp_bake_identities snapshots it before its own write and refuses if IT moved it (:402-420). No tool re-seals
a frozen field. Decision for this item: LEAVE `must_be_unset` and DEFAULT_MUST_UNSET unchanged — refusing a var that
nothing reads is harmless, and gate mode refuses it anyway. If the owner later wants it emptied: hand-edit the JSON in
the act's input commit, recompute `contract_sha256` with release_contract.contract_hash (:68-72), and change
DEFAULT_MUST_UNSET in the same commit (an empty list falls back to the default, :250). Law 10 does not reserve
contract edits to the owner; the restamp's frozen check compares only across its own write, so it will not refuse.

**Change.** Delete reads 1-2 (the defaults become plain code; RL_LSYM_TAB's re-derivation becomes a module constant
`_LSYM_TAB_PATH=None` flipped on a scratch copy, per the README rule — P5-5 uses it). Move the refit lane (:2130-~2438)
into tools/refit_v0surf.py (execs the engine to the surface-build point, fits, writes the pickle); the engine keeps the
frozen load and the HALT (its message names the new tool); :2440, :3196-3200 and one_source_selftest.py:745-760 drop
the "declared refit" state (only "frozen surface LOADED" passes). Retire the session_2026-07-18 driver's role in its
docstring.

**Must not change.** The board (96896e1c); the frozen signature and `_V0SURF_GATES`; :2051; data/v0surf.pkl; config;
`must_be_unset`; every pinned dial.

**Prove it.** Re-run the counting script (put it in the commit): zero unpinned names. Bare canonical build
byte-identical; `python3 release_contract.py check`; `tools/refit_v0surf.py` on a scratch copy reproduces the frozen
surfaces (`_V0SURF[sig]` c18/surfN/surfR equal to the pinned pickle's, numpy array_equal); one_source_selftest;
acceptance `--profile full` (config_manifest, release_contract_seal).

**Lands via.** Lever act, `moves: [engine_head, rl_model]`, board unmoved by prediction.
