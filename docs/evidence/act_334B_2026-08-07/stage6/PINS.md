# #334 stage B / STAGE 6 — PINS

Every identity here is **measured from the artifact on this branch**, never asserted. The commands
that produce them are in `REPRODUCE.md`.

## What MOVES on this branch (the shipped state)

| pin | before (stage-5 landing) | after (stage 6 shipped) |
|---|---|---|
| `engine_head` — `engine/rl_after/_merged_recover.py` | `98ed7070` | **`910bb422f9dabeaa4d51f5cd45e1d606`** |
| `config` — `config_manifest.canonical_hash(vars)` | `74b2a056…` | **`697da6f8b5abe1fc802a99f89a92a242caa0ddf7a4b240a2be1c5d727350935b`** |
| `data/model_config.json` (file md5) | — | `8de828f5ae00dd12779d46ff7737dd80` (64 vars; was 62) |
| `data/expected_boot.json` (file md5) | — | `1403d0ab5de0e30db38ce2598ecb179e` |
| NEW committed artifact `engine/rl_after/g6_table.json` | — | **`5656dd8bbb19b193e1acde5063664cc5`** |

## What does NOT move (asserted by rebuild, not by claim)

| pin | value | how it is held |
|---|---|---|
| `board` | **`13f8c2e0240600733a5fb42414510445`** | both dials ship at 0; rebuilt byte-exact through the full gate (`KILLSWITCH_PROOF.txt`) |
| `store` | `37ced3ce45914e6feb00d27e26922e9a` | this act writes no store |
| `rl_model` | `b35c5521b78dcdfb2423d54f5574330b` | untouched |
| `fv` | `0976195c…` | untouched |
| `v0surf` | `9713ec6c83270ab916bb4a5e3ded6cb3` @ sig `3e8e50de5103` | **re-proven** by a declared refit at `RL_G6_W` 0 / 0.5 / 1.0 (`fit_coupling_refit_log.txt`) |
| `band` / `q97m` / `peak_model` / `pvc_snapshot` / `bust_prior` / `register` | unchanged | untouched |
| pick ladder `pvc_curve_v2.json` | `curve_md5 18203822`, pick 1 = 3000 | asserted unmoved in the workbook picks sheet |

## The rung artifacts (candidates, NOT shipped)

| rung | board md5 | walk-forward matrix md5 |
|---|---|---|
| `RL_G6_W = 0.25` | `e5fee49bb9dc553ddbaf55143bd03742` | `2eff80a4bbf9031ae8e25e54ef9b63be` |
| `RL_G6_W = 0.5` | `56b6c21cec6fccdeb3711ccd9981fac1` | `8553acf07bffd5570bc6d8b4e76c9f5a` |
| `RL_G6_W = 0.75` | `b963e36a8423470ecfdc1f3e5e691806` | `22402f35c41e306bb4fbeb3d2c2302e3` |
| `RL_G6_W = 1.0` | `17c96ca4add0fd49609ed8fd5009a641` | `ca6cd25d725a22b74afe775d7b044c04` |

`RL_G6_KPD` is 0 in every artifact above. The KPD sub-dial has no built board: it is ruled separately
and its effect is printed as the identical-career KPD/KPF pair in `PROBES.txt` section (h).

## Teaching provenance

* teaching matrix `docs/evidence/act_334B_2026-08-07/stage4_amend1/noarb/per_entrant_338_stage4a1.json`
  md5 **`b564b12e533119f49c2c6bb0c92a5d91`** — asserted inside `measure_g6.py`, which halts otherwise.
* teaching board: `b56bbdde` (the board that matrix was emitted at). The surface is taught ONCE from
  the frozen matrix and never re-emitted for teaching — there is no fixed point and no build-time fit.
* raw measured rows: `s6_rows.json` (committed).

## What is NOT registered, deliberately

The out-of-round movers-registry column is **not** written by this act. Registering a candidate board
before the owner's adoption word writes un-adopted prices into all three ingestion histories and
poisons the column id against correction — the pre-fire audit's finding 11 on the stage-B directive
(`out_of_round_column.py:84-127`). Registration belongs after the adoption word.
