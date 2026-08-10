# THE DIRECTIVE-ASSEMBLY INSTRUMENTS — the build-seat computation, landed 2026-08-10

The scripts that computed the figures the composition directive is assembled from: the ITEM C
worked rows and the evidence weight `w`, the year-1 ND cohort landing, the TASK 3 conservation
sums, the alternative par reading, the seat's independent verification, and the ITEM I ruler
reconstruction attempt. The directive-assembly and tables acts already have partial presence
in the tree (`docs/evidence/composition_2026-08-10/item_a_ablation.py`, and the r30/r34 table
scripts landed with `docs/evidence/ruler_act_2026-08-10/`); this set is the remainder.

## THE LOADER IS THE POINT — READ THIS FIRST

Every engine-touching script in this set imports `engine_load.py` and calls `load()`. That
file is short and it encodes a fact the rest of the tree gets wrong:

    os.environ['RL_CONFIG_MODE'] = 'gate'
    import config_manifest as _CFG ; _CFG.enforce('gate')

`enforce('gate')` clears ambient model env and loads `data/model_config.json`. **That manifest
sets `RL_GAMMA=1.0`, not the `0.85` documented in START_HERE §2.** Only gate mode reproduces
the frozen v0surf signature `6ef67f07db98258786189a6316ce24f9` — the signature that is in
`data/v0surf.pkl` and in the G1 act's `summary.json`. Dev-shell 0.85 **halts** on the v0surf
frozen-signature guard (it produces sig `e68e2f7f...`). The shipped board's own `GAMMA` field
reads 1.0, confirming the shipped board is the gate-mode build. `sig_debug.py` is the script
that established this.

`load()` reads `_merged_recover.py`, truncates at `print("=== AFTER`, and `exec`s the prefix
with stdout redirected, returning the globals dict. It is a **single exec-load per process**
by design (START_HERE §2) — do not call it twice in one process.

## PATH CONVENTION

`engine_load.py` hard-codes `ROOT = /home/user/afl-rl-engine` and derives `RL_REPO`, `RL_FV`
and the `sys.path` entries from it. To run this set against a different checkout, edit that one
constant. Scripts that also read the board open
`/home/user/afl-rl-engine/data/rl_build/rl_app_data.json` directly by absolute path
(`sums.py`, `probe_board.py`). `ruler_probe2.py` and `probe_base.py` additionally
`sys.path.insert` the session scratchpad root so that `engine_load` resolves; the rest import
it by bare name and so must be **run from this directory**.

## PINS AND INPUTS OF RECORD (from DIRECTIVE_CALC_PROGRESS.md, verified by that seat)

| object | pin |
|---|---|
| board `data/rl_build/rl_app_data.json` | md5 `4b448a821f54180182637983f7a26a9d` — matches frozen |
| store — **not** at `data/rl_players_store.json` (does not exist) | `engine/rl_after/rl_model_data.json`, md5 `d9a24282357cf3083b1640466e3ecd83` |
| engine | `engine/rl_after/rl_model.py` (1469 lines), repo @ `37bad1a` |
| venv | `/root/rl_venv312` (py 3.12.3, numpy 2.4.4, sklearn 1.8.0) |
| currency | `ev()` is engine currency; board `v = ev / 1.0524` (`_PL_F`). Verified on Mraz 3741/3555. |

One input the seat expected was **not** where it was described: `docs/evidence/act_334B_2026-08-07/stage5/`
does not exist on main. The file matching the description is
`docs/evidence/noarb_338_2026-08-06/per_entrant_338_confirmation.json` (md5
`5fb617d09cd8341d9f36b90a1827e2e5`, 2645 records, `meta.store_md5` `37ced3ce`) — i.e. emitted
on a **pre-DOB / pre-G1 store**, which is a live discrepancy flag, not a substitution. It is
recorded here because anything re-run off that file inherits the older store.

## OBJECTS LOCATED (the seat's own citations, file:line)

- par surface, LIVE value path: `par_at(F,pos,pick,T)` `engine/forward_valuation/par_build.py:255`,
  exposed as `PR.par_at` `engine/forward_valuation/par_redesign.py:68`; consumers `_par_prior`
  `engine/rl_after/_merged_recover.py:306-308` and local `par` at `:1925`.
- par surface, `rl_model.py`'s own: `expected_c(g,pk,s)` `rl_model.py:370` on `expected()` `:221`
  ("below-par" `:1104`, "position+experience bar" `:1094`). **Both readings are computed** —
  `par_alt.py` exists precisely so the sitting sees both rather than picking one silently.
- draft-age integer `_ageR` `_merged_recover.py:1271`; age->tenure bridge `eff_ten` `:309-311`.
- entry anchor `entry_anchor()` `:1761-1765` -> `v0_start()` `:1737-1741`.
- current expectation `ev(p,Y)` `:1895-1937`.
- cap candidates: `entry_anchor` (chosen, from the w=0 identity); `R_SURF` `:1104-1125` +
  `sitout_ev` `:1847-1852`; `RUC_PRIOR_CAP` `:1138` / `_ruc_ceiling` `:1195-1201`;
  staleness/mediocre `:1929-1936`. **No object in the engine is literally "the year-1+ ND
  ceiling"** — the seat recorded this as a discrepancy rather than naming a stand-in.

## THE INSTRUMENT (ITEM C)

    w = G x Q x gate
    G    = g/(g+8)                                   g  = career games total
    Q    = clip(sa/par, 0, 2)                        sa = career games-weighted average
    par  = par_at(pos, min(effpk,KMAX), T),  T = clip(draft_age-18, 1, 6)   [the eff_ten bridge]
    gate = min(ev/entry_anchor, 1)

Verified against **all six** of the directive's worked rows, exact match on `w`
(`item_c_q3.py`'s own header states this).

## KEY FILES

- `engine_load.py` — the loader (above). Every other engine script depends on it.
- `item_c_rows.py` -> `item_c_rows.json` — the ITEM C worked rows. Its header carries the full
  object-citation block, each citation "verified by reading, then exercised live in this
  script".
- `item_c_probe.py`, `item_c_q3.py` — reproduce the directive's worked rows, then the C-Q3
  faller demonstration and the C-Q2 H ladder.
- `item_b_probe.py` — ITEM B, the pool year-0 age gradient re-derived on the DOB-written
  store. Its C5 note matters: the factors are a **relative** gradient inside the pool, so the
  unknown global scale cancels and this measurement does **not** depend on the four-instrument
  ruler's absolute level (the level ITEM I could not reproduce).
- `cohort_landing.py` — year-1 ND cohort landing re-run on the current matrix, plus ITEM C
  H-sizing. Result: mean `ev/entry_anchor` over ND in-curve class 2025, n=58 = **1.0194**
  against a filed 1.0248; played-only n=34 = 1.2742; sum/sum = 1.0842. Mean `w` over the
  year-1 cohort 0.2271 (all 58) / 0.3873 (played only).
- `sums.py` — TASK 3 conservation sums and the ITEM C sizing splits. Board total
  `sum(active.v)` = **761,574** (exact match to the filed board total after G1, delta -13 from
  761,587); sigma `entry_anchor` in board currency = 581,904.5 over 804 rows.
- `par_alt.py` — the alternative par reading (`expected_c`), reported beside `par_at`.
- `seat_verify_directive.py` — the seat's **independent** re-derivation of the deciding
  figures: own arithmetic, own cohort selection, only the loader shared. This is the
  cross-check, and it should be read as such.
- `dovaston_check.py` — the Dovaston worked example: is `v0` position-aware at the same pick,
  and what does year 1 read.
- `ruler_probe.py`, `ruler_probe2.py` — the **ITEM I** reconstruction attempt against the
  filed four-instrument levels A 1.6621 / B 1.5883 / C 1.6028 / D 1.5468 ("the year-4 price
  stands at 1.55x realized"), plus a variant sweep. These did **not** reproduce the filed
  levels — that failure is what caused the ruler act's original instruments to be landed
  separately at `docs/evidence/ruler_act_2026-08-10/` (PR #400). Kept here as the record of
  the attempt.
- `explore_engine.py`, `probe_base.py`, `probe_board.py`, `find_rows.py`, `find_rows2.py`,
  `sig_debug.py` — location probes, identity/book sums, the two real search rows for the
  worked-row table, and the v0surf signature debug that established gate mode.
- `DIRECTIVE_CALC_PROGRESS.md` — the seat's own log: input verification, engine reproduction,
  objects located, results, and the discrepancy list.

## STATUS AT THE TIME OF THE ACT

TASK 1 / 2 / 3 complete. No repo file touched by that seat; nothing committed, pushed or
posted. This landing is docs-only and changes no taught value.
