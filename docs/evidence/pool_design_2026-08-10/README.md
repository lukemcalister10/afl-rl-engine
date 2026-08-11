# THE POOL-DESIGN ACT (RULING 2.5) INSTRUMENTS — landed 2026-08-10

The pool-design measurement — the three-way design grid on the pool leg and the design-option
magnitudes on the owner-basis year-1 lead. #334 landing comment **5235784509**; brief
5235660463; the no-blanket law it answers to is 5235555305.

## PATH CONVENTION

`grid.py` and `options.py` hard-code the absolute scratchpad root
`SD = /tmp/.../scratchpad/`. `extra.py` does something unusual and worth stating plainly: it
does not import `grid.py`, it **re-executes grid.py's prologue as text** —

    exec(open(SD + "grid.py").read().split("rng = np.random.default_rng")[0])

— so that the cohort build and the `ROWS` construction are literally the same code, then
carries on with its own cells. Keep the three files together; `extra.py` breaks if `grid.py`
is renamed, moved, or edited above the `rng =` line.

No engine load anywhere in this set. Pure arithmetic on two committed matrices. Requires
`numpy` and `statistics.NormalDist`.

## WHAT THIS SET CONSUMES, AND WHERE THOSE LIVE

| input | md5 | where it lives |
|---|---|---|
| `s4a1.json` — stage4_amend1 per-entrant matrix (the **year-0** basis) | `b564b12e533119f49c2c6bb0c92a5d91` | origin branch `landing/334-stage-b`, `docs/evidence/act_334B_2026-08-07/stage4_amend1/noarb/per_entrant_338_stage4a1.json`. NOT on main. |
| `s5.json` — stage-5 landed matrix (the **year-1** basis) | `bfc104f4feedab2f006b4b7408bfdc15` | same branch, `.../stage5/noarb/per_entrant_338_stage5.json`. NOT on main. |

`grid_out.json` (the computed grid, landed here) is `grid.py`'s only file output.

## THE INSTRUMENT

From `grid.py`'s own header, unedited:

    F0 (year-0 honesty, stage4_amend1 matrix) = sum(vpath[3])/H^4 / sum(v0)
    F1 (year-1,          stage5 landed matrix) = sum(vpath[3])/H^3 / sum(vpath[0])
    H = 1.0939.  Pool = every non-ND-1-64 entrant.  Classes 2004-2022.
    [busts -> 0 numerator, kept in denominator]

Both readings reproduce the published seam figures to 4dp (POOLDESIGN_PROGRESS step 3: RD21+
3.242, KPF21+ 0.556, 21-22 2.149 on F0; age23+ sit 0.3235, IRE sit 0.1738, union 0.2763 on F1).

`options.py` works on a different and narrower basis, stated in its own header: the
**owner-basis full-cohort year-1 lead**, classes 2004-2025, keys present in BOTH matrices,
`lead = sum(vpath[0]) / sum(v0)`; concluded careers score 0 and stay in the denominator;
unreached classes excluded; `v0<=0` excluded. Baseline (stage-5 landed) = **0.946050**,
reproduced exactly. The `LV` (route levels) and `RDP` (per-position) constants at the top of
`options.py` are the board-currency levels of record for that basis — they are taught values
and are reproduced here unchanged.

## KEY FILES

- `grid.py` — the cohort build, `ROWS`, and the three-way (route x position x age-band) grid
  with 20,000-draw BCa intervals, player- and class-clustered. Of every three-way cell, only
  **RD x SD x age<=18** clears the F8 bar.
- `extra.py` — the stage-7 named cut cells (sitter-conditioned) re-run on the F8 bar, plus the
  mature x route x age fine cuts the no-blanket law names.
- `options.py` — design-option magnitudes on the owner-basis year-1 lead. A1 (the stage-7
  named cut, re-derived here) = **-0.0017**, against stage-7's filed -0.002 — the instrument
  cross-checks against the prior act.
- `grid_out.json` — grid output.
- `POOLDESIGN_PROGRESS.md` — the act's own step log, including the mechanism finding at
  steps 6-7: `pool_level` is age-blind (`rl_model.py:1264-1282`), pool `v0 = _v0_raw =
  raw_ev(debutyr-1)`, and the year-1 sitter price is a per-position constant times the signed
  level, **identical at every age** (MID/SD/SF .548, KPF/KPD .642, RUCK .779), while `v0`
  falls 1.00 -> 0.09 -> 0.01 from age 18 -> 22 -> 24. Those line numbers are the act's own
  citations and were not re-verified by this landing.
