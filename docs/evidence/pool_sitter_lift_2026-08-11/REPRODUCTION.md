# ORDER 19 — HOW TO REPRODUCE EVERY FIGURE IN THIS DIRECTORY

    export PATH="/root/rl_venv312/bin:$PATH"
    SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
    cd /home/user/afl-rl-engine

## 1. The three boards (~1m10s each)

    bash docs/evidence/pool_sitter_lift_2026-08-11/build_board_o19.sh $SP/o19/board_BASE.json   nopatch
    bash docs/evidence/pool_sitter_lift_2026-08-11/build_board_o19.sh $SP/o19/board_LIFTH.json  nopatch   RL_H_POOLSIT=1.0 RL_H_UNION=1.0
    bash docs/evidence/pool_sitter_lift_2026-08-11/build_board_o19.sh $SP/o19/board_LIFTRH.json patch     RL_H_POOLSIT=1.0 RL_H_UNION=1.0
    # the disclosed second-R-site sensitivity (section 7 of the summary), NOT a variant:
    bash docs/evidence/pool_sitter_lift_2026-08-11/build_board_o19.sh $SP/o19/board_LIFTBOTH.json patchboth RL_H_POOLSIT=1.0 RL_H_UNION=1.0

Expected md5s:

| board | md5 |
|---|---|
| `board_BASE.json` | `94f1fec59f99c59d5890d5975c79fa9b` — **identical to the live board** |
| `board_LIFTH.json` | `5053a763d8c3de875999f4642cdd8165` |
| `board_LIFTRH.json` | `e47fa529cf1f79257f4863b573d5c307` |
| `board_LIFTBOTH.json` | `53ae0668c7c8a8d2f5bf59cb3cf98ad4` |

`build_board_o19.sh` never writes the checkout. It creates a detached worktree under `$SP`, applies
the variant-B patch there (patch modes only), restamps the config hash and boot identities so the
guards stay armed, runs `rl_export.py`, copies the board out, and removes the worktree.

## 2. The three walk-forward matrices (~1m45s each)

    bash docs/evidence/pool_sitter_lift_2026-08-11/emit_variant_o19.sh LIFTH   nopatch RL_H_POOLSIT=1.0 RL_H_UNION=1.0
    bash docs/evidence/pool_sitter_lift_2026-08-11/emit_variant_o19.sh LIFTRH  patch   RL_H_POOLSIT=1.0 RL_H_UNION=1.0
    bash docs/evidence/pool_sitter_lift_2026-08-11/emit_variant_o19.sh CTRL19  nopatch          # the emit control

`per_entrant_SHIP.json` is the standing live baseline emitted by the composition act; `CTRL19` is a
fresh HEAD-defaults re-emit whose `recs` must be **byte-identical** to it (control 2). Emitted
`meta.engine_head`: `a8071af4` for SHIP / LIFTH / CTRL19, **`002ff843` for LIFTRH** — the machine
proof the R patch was in the tree that emitted it.

## 3. Phase 1's derived levels, per variant

`derive/phase1_derive_CARRIED.py` is byte-identical to
`build/pool-repricing-phase1:docs/evidence/pool_repricing_2026-08-11/phase1_derive.py`
(md5 `bd6786d8a77108d48bfdfcf04694f613`, verified). **That branch is not touched by this act.**

    for L in SHIP LIFTH LIFTRH; do
      mkdir -p $SP/o19/derive_$L
      cp docs/evidence/pool_sitter_lift_2026-08-11/derive/phase1_derive_CARRIED.py $SP/o19/derive_$L/phase1_derive.py
      ( cd $SP/o19/derive_$L && OPENBLAS_NUM_THREADS=1 python phase1_derive.py $L > out.txt )
    done

The `SHIP` run must reproduce the committed `PHASE1_DERIVE.json` on that branch exactly (control 4).

## 4. The cohort instruments

Both canonical instruments are **copied, never modified**; `noarb_table_allarm.py` asserts
`noarb_table_338.py`'s md5 `0f8220351c64c56ccfa90c60edcdfa5f` at run and refuses to proceed otherwise.
They are run from a scratchpad copy because both write their json beside themselves, and the
composition evidence directory is filed evidence.

    N=$SP/o19/noarb; mkdir -p $N
    cp docs/evidence/composition_2026-08-10/noarb/{noarb_table_338.py,noarb_table_allarm.py,harness_pvc_REPINNED_pass3.py} $N/
    cd $N
    for L in SHIP LIFTH LIFTRH; do
      OPENBLAS_NUM_THREADS=1 python noarb_table_338.py $SP/per_entrant_$L.json > t338_$L.txt && mv noarb_table_338.json table_$L.json
      OPENBLAS_NUM_THREADS=1 python noarb_table_allarm.py $SP/per_entrant_$L.json $L
    done

`table_SHIP.json`'s `groups` must equal the committed
`docs/evidence/composition_2026-08-10/noarb/table_SHIP.json` (control 5).

## 5. The two measurement instruments

    cd docs/evidence/pool_sitter_lift_2026-08-11
    OPENBLAS_NUM_THREADS=1 python pool_sitter_lift.py  > pool_sitter_lift_out.txt
    OPENBLAS_NUM_THREADS=1 python lift_consequence.py  > lift_consequence_out.txt

Both assert the three pins at entry and at exit and halt rather than report if any has moved:

    board       data/rl_build/rl_app_data.json                                  94f1fec59f99c59d5890d5975c79fa9b
    store       engine/rl_after/rl_model_data.json                              d9a24282357cf3083b1640466e3ecd83
    instrument  docs/evidence/composition_2026-08-10/noarb/noarb_table_338.py   0f8220351c64c56ccfa90c60edcdfa5f
