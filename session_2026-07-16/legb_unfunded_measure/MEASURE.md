# LEG B UNFUNDED MEASUREMENT — RESULTS (C≡1; ships nothing) · 2026-07-16 · seat 10

Measures the DECIDED output-anchored family (memo v1.3 §2) with the §3 per-position conservation
renorm turned **OFF (C≡1)** via `RL_UNCONSERVE=1`, against the frozen instruments, at five points.
**No selection is made. Nothing ships.** Disposition returns to the owner.

- Base `91d08f2` · store `b1fd0bce` (untouched) · board OFF = `8d90c9ac` (A/B byte-exact) · toggle `6d9a4269`.
- All verdicts from FROZEN instruments (S4): β via `beta_measure.py` md5 `14c59139`; G-COHORT via the
  REAL July-8 gate `ship_gates_check._b1_july8` (extracted verbatim; matrix `__meta__` hashes asserted
  == running engine); ledgers via the seg-5 `ledger_dump.py`; ranks/pool/sincerity over the active-804.
- **Thread-invariance proven:** OFF reproduces the Leg-A head byte-exact (y4 1.3017 / y5 1.3160 /
  y6 1.2664), and s=1.00 reproduces solo (y4 0.7740, β 0.7492), single- vs multi-threaded BLAS.
- **Measurement note:** matrices are built dev-shell (no `RL_CONFIG_MODE`) because gate-mode config
  CLEARS/REJECTS the declared kill-switches — it can only measure the *baked* config; an unbaked
  env-toggled candidate MUST be measured dev-shell. The July-8 *construction* is identical.

## THE GRID (C≡1 at s ∈ {0.65, 0.85, 1.00, 1.25, 1.50})

| point | β | CI | width | n | G-COHORT y4 / y5 / y6 | ≤1.30 | E/B | net board ΣΔ | sinc-fail |
|---|---|---|---|---|---|---|---|---|---|
| **β_c / OFF** | 0.6219 | [0.484,0.790] | 0.306 | 116 | 1.3017 / 1.3160 / 1.2664 | BREACH y4,y5 | 1.766× | 0 (=8d90c9ac) | — |
| s=0.65 | 0.7045 | [0.566,0.871] | 0.305 | 116 | 0.8801 / 0.8009 / 0.7466 | PASS ×3 | 3.080× | −174,696 | 0 |
| s=0.85 | 0.7299 | [0.586,0.901] | 0.314 | 116 | 0.8134 / 0.7166 / 0.6563 | PASS ×3 | 3.656× | −204,370 | 0 |
| s=1.00 | 0.7492 | [0.599,0.926] | 0.326 | 116 | 0.7740 / 0.6666 / 0.6015 | PASS ×3 | 4.156× | −222,115 | 0 |
| s=1.25 | 0.7815 | [0.618,0.975] | **0.357** | 116 | 0.7234 / 0.6026 / 0.5288 | PASS ×3 | 5.149× | −245,107 | 0 |
| s=1.50 | 0.8137 | [0.634,1.022] | **0.388** | 116 | 0.6867 / 0.5565 / 0.4745 | PASS ×3 | 6.379× | −261,402 | 0 |

Rails: width ≤ 0.35 breached at s≥1.25; **n = 116 < 120 at EVERY point** (incl. OFF — the proven-27+
sample is 116, a standing precision limit of the β instrument, not a property of the map).

## THE UNMEASURED QUESTION OF RECORD — does the decided family UNFUNDED hold ≤1.30?
**YES — emphatically, at all five points — but by DEFLATION, not by the funded cure.** Unconserved,
the July-8 cohort curve *inverts*: y4/y5/y6 fall from ~1.30 to 0.47–0.88, i.e. the older cohorts
(y4–y6) drop BELOW the y1/y2 base. The gate clears not because the growth law is healthy but because
the proven/older production is marked DOWN across the board. G-COHORT ≤1.30 is satisfied trivially and
should not be read as a pass in spirit.

## β — rises with s, crosses 0.80 only at s=1.50 (and only there, at a rail cost)
β climbs monotonically 0.622 (off) → 0.814 (s=1.50). It reaches the owner's 0.80 reference **only at
s=1.50**, where the CI width rail (0.35) is breached (0.388) and the CI now spans 1.0. So the unfunded
family buys β at the price of precision, and never clears the bar with a clean CI in this grid.

## E/B — "passes" 1.75 by GUTTING the donor, not funding the elite
OFF: English 3655 / Briggs 2070 = 1.766× (already at the floor post-Leg-A). ON: 3.08× → 6.38×. The
ratio explodes because **Briggs collapses** (2070 → 512 at s=1.50, −75%), while English barely moves
(3655 → 3266). The hard floor is cleared for the wrong reason: sub-elite demolition, not elite lift.

## CENSUS / POOL RE-RATE — a ~30% net board deflation, concentrated in MID and GEN_DEF
The map is production-side only (pedigree/iso/pick-priors nominal by construction), so with C≡1 the
per-position production total is NOT conserved and the net board FALLS hard: −174,696 (s=0.65) →
−261,402 (s=1.50); at s=1.00 that is **−30.3% of the 734,044 active-804 baseline sum**. This is the
value conservation (C) would have recycled — the size of the "unfunded" hole. Pool ΣΔnum (s=1.00):
MID −81,808 · GEN_DEF −55,666 · GEN_FWD −40,750 · KEY_FWD −23,168 · KEY_DEF −21,393 · RUC +670.
**MID and GEN_DEF re-rate down hardest; RUC is the sole near-neutral/rising pool** (RUC +5,115 at s=1.50).
(The BINDING census-v2 cell-gate — global ≤15,612 + cells — runs bake/gate-mode only and is fenced
OUT; the net-injection figure above is the honest ledger reading of the unfunded cost.)

## SINCERITY LEDGER (item 256, all 804 rows) — clean on the strict test; the transfer is generational
- **SCAR-up-rank-down failures: 0 at every point.** No player's SCAR rises while its rank falls.
- **Bontempelli PASSES the owner's test at every point:** SCAR up (+15 → +35) AND rank up (35 → 6–11).
  Caveat: his SCAR lift is small (+0.4% to +1.0%); the rank jump is driven mostly by the field
  deflating around him, not by a large own-lift.
- The real movement is GENERATIONAL, visible in the top-20 gainers/losers (per-point files):
  - **Gutted (young pedigree, SCAR & rank down):** Nick Daicos 8140→3783 (−54%), Harry Sheezel
    8006→3576 (−55%), Max Holmes, Wanganeen-Milera, Finn Callaghan, Lachlan Ash, Archie Roberts.
    The #1/#2 board players are halved.
  - **Lifted (veteran proven, esp. RUC):** Toby Nankervis +1,094, Jarrod Witts +741, Darcy Cameron
    +648, Rowan Marshall +566, Pendlebury +334, J.Kelly +283, Viney +241.
  Not a sincerity failure by the strict definition, but the owner should SEE that unfunded, the
  output-anchored family reprices young pedigree DOWN and veteran realised-output UP, wholesale.

## ARTIFACTS (this directory / out/)
- `GRID.out` — the compact grid table (β, G-COHORT, per-point, pool).
- `SINCERITY_all804_s<s>.csv` — the item-256 ledger, all 804 rows: ΔSCAR, Δ%, rank before/after, Δrank,
  ρ_num, ρ_ratio, w — one file per point.
- `POINT_s<s>.md` — per-point pool re-rate, census reading, E/B, Bontempelli, top-20 gainers/losers,
  SCAR-up-rank-down roster.
- `led_*.json` — the raw ledger dumps (OFF + five ON points).
- `gc_*.txt` / `beta_*.txt` — raw frozen-instrument outputs.
- `measure_gcohort.py` / `analyze_unfunded.py` / `aggregate.py` / `run_grid.sh` — the measurement code.

## DISPOSITION (returns to the owner)
The decided family run UNFUNDED (C≡1) clears G-COHORT ≤1.30 at every s and lifts β and E/B past their
bars — but the mechanism is a broad DEFLATION: ~30% of board value removed net, the young pedigree
elite halved, veteran realised-output raised, the cohort growth-law inverted, and the guard passes are
cosmetic (G-COHORT by deflation, E/B by donor demolition, β only at s=1.50 with a blown CI rail).
The bar/grid and this reading return to the owner; no s is selected here.
