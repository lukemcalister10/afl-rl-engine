# AUDIT-1 INSTRUMENTS — the year-0 surface audit, landed 2026-08-10

The independent audit of the **year-0** surface, run against origin branch
`landing/334-stage-b` @ `e8c772c`. Brief: #334 comment **5235093657**. Its verdicts are the
ones the later acts lean on — in particular the finding that **the KPD error is made between
year 0 and year 1, not at year 0**, which is what put the mark-up trace (2.6) on the year-0 ->
year-1 step in the first place.

## PATH CONVENTION

`a1_lib.py` hard-codes the scratchpad root as `SC` and defaults to loading `stage4a1.json`.
`a1_meas.py` imports `a1_lib` by module name, so **run these from this directory** (or put it
on `PYTHONPATH`). `a1_kpd.py` and `a1_scan.py` re-declare `SC` themselves.

No engine load — `a1_scan.py` reads the frozen v0 surface pickle directly and rebuilds the
year-0 surface by hand, which is the whole point of the audit: it does not take the act's word
for the surface, it re-derives it.

## WHAT THIS SET CONSUMES, AND WHERE THOSE LIVE

| input | md5 | where it lives |
|---|---|---|
| `stage4a1.json` (a.k.a. `matrix.json`, `s4a1.json`, `pe338.json`) — the stage4_amend1 per-entrant matrix | `b564b12e533119f49c2c6bb0c92a5d91` | origin branch `landing/334-stage-b`, `docs/evidence/act_334B_2026-08-07/stage4_amend1/noarb/per_entrant_338_stage4a1.json`. NOT on main. AUDIT1_PROGRESS step 1 records this md5 as its own check that it had the right file. |
| `s6rows_branch.json` — the stage-6 per-row emission | `9015cda31efc25bd471dcc74fdc265fa` | session scratchpad root, byte-identical to `s6_rows.json`. NOT on main. |
| `v0surf_branch.pkl` — the frozen v0 surface, read at key `3e8e50de51030297c99cf367161c161f` | `9713ec6c83270ab916bb4a5e3ded6cb3` | session scratchpad root. The surface signature is the pickle's own dict key — if you supply a different pickle you must supply the matching key. |
| `pvc2.json` — the board picks curve (`['curve']`, pick -> value) | `73d6f679dc62281b1640fb81a5ba5fe4` | session scratchpad root. |

`a1_scan.py` writes `inv_players.json` and `inv_surface.json` back to the scratchpad root
(the inverted-step listings). Those two outputs are **not** landed: they are regenerable in
seconds from the four inputs above and they are large relative to their value. Noted in the
INDEX.

## THE INSTRUMENT

    H = 1.0939
    v4(rec)  = vpath[3] if the career reached year 4 else 0      (busts kept in, at zero)
    F0       = sum(v4)/H^4 / sum(v0)                              (value-weighted, ratio of sums)

`a1_meas.py` bootstraps at B = 20,000 with `random.seed(3341)`; `a1_kpd.py` seeds 991 and uses
`statistics.NormalDist`. Reproduction gate (AUDIT1_PROGRESS step 2): ND picks 1-64, classes
2004-2022, n=1197, aggregate `vpath[3]/v0` = 1.4321 against target 1.4327 and aggregate F0 =
1.0001 against target 1.0006.

## KEY FILES AND WHAT THEY FOUND

- `a1_lib.py` — shared loader, `v4`, `pop`, `H`.
- `a1_meas.py` — headline levels and the grids. Whole book F0 = 0.939; ND alone 0.991
  (honest); **pool routes alone 0.725**, CI clear of 1. Position x pick-band grid (36 cells):
  two ND cells clear 1 — KPD picks 41-64 under-priced (later marked **marginal**: it stops
  clearing once class era is held constant, step 12) and KPD picks 65+ over-priced. Pool route
  x age grid: **draft age is the big miss** — pool entrants aged <=18 deliver 0.56 of price,
  aged 21+ deliver 2.07, both CIs clear of 1.
- `a1_kpd.py` — the KPD case, on the act's own year-1 file. Reproduces the filed KPD 0.6680
  (n=35) exactly, then puts year 0 and year 1 side by side on the same 35 players: year 0
  reads 1.574 against a leg par of 1.671 = **0.94 of par**; year 1 reads 0.668 against 1.136 =
  **0.59 of par**. This is the finding that hands the problem to the year-0 -> year-1 step.
- `a1_scan.py` — the hand-rebuilt year-0 surface and the monotonicity scan. **446 inverted
  steps** across position/age/pick on the branch (main has 437 — the branch neither causes nor
  fixes the defect); 29 inverted adjacent pairs on real players in the matrix, named. 11 of
  the 12 inverted pick seams are **inside** bands, not at band seams — so the defect is not a
  banding artifact. Also carries the second year-0 defect: **any national draftee with no date
  of birth is priced as if he is 18**, the most expensive age; 175 such players in picks 1-64,
  whose MIDs deliver 0.68 of price and KPDs 0.44.
- `AUDIT1_PROGRESS.md` — the audit's own step log (steps 1-13).

The no-DOB defect at step 10 is the same defect the DOB write act
(`docs/evidence/dob_write_2026-08-10/`) later addressed; this set is the measurement that
sized it.
