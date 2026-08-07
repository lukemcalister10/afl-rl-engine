# #334 stage B / STAGE 6 — PINS

Every identity here is **measured from the artifact on this branch**, never asserted. The commands
that produce them are in `REPRODUCE.md`.

> **AMENDED by the CONFORMANCE REPAIR of 2026-08-07** (issue #334 comment `5219329372`). The taught
> surface and every rung artifact were re-emitted. **No shipped pin moves**: the board, the config
> hash, `engine_head` and every frozen model are exactly as the original stage-6 build left them,
> because the repair changes a taught table that the shipped dials never open.

## What MOVES on this branch (the shipped state)

| pin | before (stage-5 landing) | after (stage 6 shipped) |
|---|---|---|
| `engine_head` — `engine/rl_after/_merged_recover.py` | `98ed7070` | **`910bb422f9dabeaa4d51f5cd45e1d606`** (UNCHANGED by the repair — no engine byte moved) |
| `config` — `config_manifest.canonical_hash(vars)` | `74b2a056…` | **`697da6f8b5abe1fc802a99f89a92a242caa0ddf7a4b240a2be1c5d727350935b`** (UNCHANGED by the repair) |
| `data/model_config.json` (file md5) | — | `a6565f111d9c612b57c54f75c5dd6cbd` — **moves with the repair**: the `_stage6_note` prose re-pins the taught-table md5. `vars` is untouched, so `config_sha256` does not move |
| `data/expected_boot.json` (file md5) | — | `1403d0ab5de0e30db38ce2598ecb179e` (UNCHANGED) |
| committed artifact `engine/rl_after/g6_table.json` | — | **`61450f0b63f725b8666a49349857b02d`** — **RE-TAUGHT** (was `5656dd8bbb19b193e1acde5063664cc5`) |

## What does NOT move (asserted by rebuild, not by claim)

| pin | value | how it is held |
|---|---|---|
| `board` | **`13f8c2e0240600733a5fb42414510445`** | both dials ship at 0; rebuilt byte-exact through the full gate **after the re-teach** (`KILLSWITCH_PROOF.txt`) |
| `store` | `37ced3ce45914e6feb00d27e26922e9a` | this act writes no store |
| `rl_model` | `b35c5521b78dcdfb2423d54f5574330b` | untouched |
| `fv` | `0976195c…` | untouched |
| `v0surf` | `9713ec6c83270ab916bb4a5e3ded6cb3` @ sig `3e8e50de5103` | **re-proven after the re-teach** by a declared refit at `RL_G6_W` 0 / 0.5 / 1.0 (`fit_coupling_refit_log.txt`) |
| `band` / `q97m` / `peak_model` / `pvc_snapshot` / `bust_prior` / `register` | unchanged | untouched |
| pick ladder `pvc_curve_v2.json` | `curve_md5 18203822`, pick 1 = 3000 | asserted unmoved in the workbook picks sheet |

## The rung artifacts (candidates, NOT shipped) — RE-EMITTED

| rung | board md5 | walk-forward matrix md5 | verdict on the registered gates |
|---|---|---|---|
| `RL_G6_W = 0.25` | `9883420bf729d4434001e15acb83d2ef` | `92b94767bd4a975c1714e9a63f63330d` | **FEASIBLE** |
| `RL_G6_W = 0.5` | `b0a3369f70398610bf8a94a1892de710` | `3161872265c12738e0ceae6e066196ad` | **STRUCK** (zero-cell, both bounds) |
| `RL_G6_W = 0.75` | `f43cdf45ddf3adf63aee684cf13c3525` | `42ea62b2fc4ba06bf1fe830d5b237e59` | **STRUCK** (zero-cell ×2, 41-64 taper, pick/player seam) |
| `RL_G6_W = 1.0` | `a270286fc09ac3cd7379950850a8357a` | `be5fba616372afbfca3d83add2f636de` | **STRUCK** (as above, worse) |

`RL_G6_KPD` is 0 in every artifact above. The KPD sub-dial has no built board: it is ruled separately
and its effect is printed as the identical-career KPD/KPF pair in `PROBES.txt` section (h).

The **superseded** rung identities (original build, tip `d405afb`) are preserved in
`boards/BOARD_MD5S.txt` under a HISTORY heading and in `README.md`'s HISTORY section.

## Other re-emitted evidence artifacts

| artifact | md5 |
|---|---|
| `s6_rows.json` (the measured teaching rows) | `9015cda31efc25bd471dcc74fdc265fa` |
| `../side_by_side/board_before_after.xlsx` | `cfba89af45508824af4bc4bfa72c7d64` |

## Teaching provenance

* teaching matrix `docs/evidence/act_334B_2026-08-07/stage4_amend1/noarb/per_entrant_338_stage4a1.json`
  md5 **`b564b12e533119f49c2c6bb0c92a5d91`** — asserted inside `measure_g6.py`, which halts otherwise.
  **Unchanged by the repair**: the repair changed the STATISTIC read off this matrix, never the matrix.
* teaching board: `b56bbdde` (the board that matrix was emitted at). The surface is taught ONCE from
  the frozen matrix and never re-emitted for teaching — there is no fixed point and no build-time fit.
* the registered estimand: F = v(career year 4) / 1.0939^(4−N); year-1 value-weighted aggregate
  **1.1363** (n=414), reproducing the cross-section of record 5215260604 to the third decimal.
* the registered performance axis: `sa`, the season scoring average in the evaluation year, read off
  the matrix records' own `seasons` rows.
* raw measured rows: `s6_rows.json` (committed).

## What is NOT registered, deliberately

The out-of-round movers-registry column is **not** written by this act. Registering a candidate board
before the owner's adoption word writes un-adopted prices into all three ingestion histories and
poisons the column id against correction — the pre-fire audit's finding 11 on the stage-B directive
(`out_of_round_column.py:84-127`). Registration belongs after the adoption word.
