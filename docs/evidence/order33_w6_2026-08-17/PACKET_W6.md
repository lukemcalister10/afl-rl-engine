# PACKET — ORDER 33 SEAT W6: THE FROZEN q97 CEILING vs REALIZED 97th-PERCENTILE OUTCOMES

**Read-only seat.** Nothing in `engine/`, no pin, no pickle, no law constant was touched. `data/q97m.pkl`
stays frozen at the owner's 2026-07-14 determinism ruling (md5 `cfdc7321…` == the expected_boot pin,
asserted before any number was read). Everything below is measurement plus a **bake-time
recommendation**; the only legitimate change path remains `refit_q97m.py` at a controlled bake with full
re-certification.

Prereg: `PREREG_W6.md`, pushed before any result. Instrument: `w6_ceiling.py`. All controls passed:
C2 pre-taper inversions **0 of 9,877** · C3 engine-reconstruction **exact (0.0e+00)** · C4 reproduction
of the committed S6 emit's b6 on all 804 active rows **exact (0.0e+00)**.

---

## 1. VERDICT, in one paragraph

**The frozen q97m model is approximately calibrated. The v7 age-taper is the defect.** Across 9,877
historical vantages (every store player, every as-of year ≤ 2019, outcomes observed to 2026), realized
forward best-3 production exceeds the raw q97m prediction **3.63 %** of the time [Wilson 95 %:
3.28–4.02 %] against a calibrated target of ~3 % — and that holds at the deeper ≤ 2016 window (3.72 %)
and on the pathway classes the model never trained on (3.02 %). After the v7 age-taper the same
"97th-percentile" ceiling is exceeded **8.66 %** of the time overall and **13.2 % for every vantage aged
22 or older — the board's printed q97 scenario is actually a ~q87 for anyone the taper touches.** All
341 ▼ inversions on the active board are taper-caused — provably: `_b6_core` sets
band[5] = max(q97m, band q90), so a pre-taper inversion is impossible (verified empirically, 0 of
9,877). The owner's nick-madden catch decomposes into the taper plus a display-semantics mislabel — the
raw model's ceiling for his cell is **exactly right** (§3).

| exceedance of the ceiling (target ~3 %) | raw q97m | + max(·, q90) | + v7 taper (as priced) |
|---|---|---|---|
| all vantages ≤ 2019 (n = 9,877) | 3.63 % | 3.60 % | **8.66 %** |
| age ≥ 22 (taper active, n = 4,931) | 3.73 % | 3.71 % | **13.20 %** |
| age < 22 (taper ~inert, n = 4,946) | 3.54 % | 3.50 % | 4.10 % |
| RUCK, all ages (n = 798) | 4.26 % | 4.26 % | **12.16 %** |
| TALL age 20–23 (n = 1,203) | 2.99 % | 2.91 % | 6.65 % |
| sensitivity window ≤ 2016 (n = 7,370) | 3.72 % | 3.70 % | 8.22 % |

## 2. What was measured (ground truth, not model-vs-model)

From the store's own scoring history: every real player, every as-of year Y from draft year to 2019
(≥ 7 forward seasons observed; T1 unobservable-season rule reused), realized (1) **subsequent peak
production** = `fwd_best3_from(p, Y, 2026)` — the frozen model's own target quantity, same units — and
(2) **subsequent career delivered value** = the grace-A season-valuation formula discounted to the
vantage. Cells = age × position × games-through-vantage, S7's resolution rules (q97 needs n ≥ 34, else
BOUND(max) flagged `*`, never smoothed; n_players printed beside n). Model side at the SAME vantages,
on the pricing path's own inference features: `pred_raw` (q97m), `b5_raw = max(pred, q90-band)`,
`b5_tap` (through the engine's own `b6`, exact to 0.0e+00 on a 200-vantage control). Full tables:
`W6_out.txt` / `W6_CELLS.json`; per-vantage table `W6_VANTAGES.csv`.

## 3. The owner's catch, decomposed (nick-madden, PDA RUCK, age 22, 10 games, cand 715)

His matched vantage cell (age 22–23 RUCK, 1–10 games, n = 35 rows / 23 players — q97 resolved on rows,
thin on players and flagged): realized 97th-percentile forward best-3 = **111.4**. The frozen model's
raw prediction at his 2026 vantage: **111.4 — exactly the realized cell ceiling.** Three separate
things then happen to it:

1. **The v7 taper cuts 111.4 → 105.1** (asc = 0.76 at age 22). The W4 form-retention relax cannot
   rescue him: it requires `nqual ≥ 1`, and `_nqual` counts only ≥ 10-game seasons — his 3-game and
   7-game ruck stints at 86.0 / 78.4 avg count for nothing, so an early-career ruck **getting games at
   a good level** is tapered as if he were unproven speculation. (This is the general young-tall
   pattern: games 1–10 at ages 20–23 rarely clear the 10-game season bar.)
2. **Price convexity amplifies the level cut.** At his profile the scenario-6 career value is 3,883
   tapered vs **5,104 untapered** (+31 %) — the realized q97 delivered-value from his cell is 3,042
   (vantage-discounted board points; scale-cousin, stated in the prereg). The engine's own career
   value at the ceiling is in the right range; the taper is what pulls it under.
3. **The page number ~1,300 is a rho-blend, not a ceiling value.** The S6 scenario price is
   `anchor + rho × (ceiling leg)` with rho = 0.345 — it answers "what would his BOARD PRICE be if the
   ceiling lands", with 65 % of the price still sitting on the pedigree leg. It is NOT "the career
   value of his q97 outcome" (which the fan itself carries as six_raw[5] = 3,883). The owner compared
   ~1,300 against realized career outcomes in the 2,000s — the like-for-like comparison is
   3,883 (or 5,104 untapered) vs 3,042, and the model side is not low there. **"The ceiling is right
   and the page mislabeled it" is a substantial part of this catch — plus the taper.**

Untapered, his q97 scenario price would print ≈ 1,800 rather than 1,388 (Δ six_raw[5] = +1,221 through
rho·m·W6).

## 4. The other named rows (full details in `W6_NAMED.json`)

| row | pred_raw | b5_tap | realized cell q97 (n) | reading |
|---|---|---|---|---|
| nick-madden (PDA RUCK 22, 10 g) | 111.4 | 105.1 | 111.4 (35) | raw exact; taper is the whole gap |
| ned-moyle (MSD RUCK 24, 27 g) | 114.4 | 104.3 ▼ | 100.9 (44) | raw above the cell pool (his own level is high — conditioning, not error); the ▼ display is still wrong-shaped |
| lachlan-mcandrew (SSP RUCK 26, 22 g) | 103.7 | 91.0 ▼ | 100.9 (44) | taper pushes the ceiling below the cell's realized q97 |
| samuel-grlj (ND MID 19, 19 g) | 114.0 | 114.0 | **125.7 (75, resolved)** | no taper at 19 — here the RAW model is ~12 pts LOW; productive-teen cells are the one place q97m itself compresses (≤19 MID 11–30 exceedance 6.7 %) |
| mitchell-edwards (ND RUCK 21, 16 g) | 124.0 | 119.3 | 128.9* (24, BOUND) | raw near the bound; mild taper |
| jordan-croft (ND KPF 21, 18 g) | 87.4 | 84.3 | 98.0 (67, resolved) | raw ~11 low vs cell pool (young-KPF cell exceedance only 3.0 % — within noise, but the cell pool sits above his conditional) |
| jonty-faull (ND KPF 20, 26 g) | 88.8 | 88.8 | 98.0 (67) | as croft, untapered at 20 |
| alix-tauru (ND KPD 20, 18 g) | 92.0 | 92.0 | 94.9 (81) | fine |

## 5. Suspect decomposition

**The v7 age-taper (100 % of the inversions; ~2/3 of the miscalibration mass).**
`bb[5] = m + asc·(bb[5] − m)`, asc = interp(age, [20,22,24,27] → [1.0, 0.76, 0.58, 0.40]). Provenance:
assembled into the D4 bake candidate from the M1+v7 prototype (2026-07-02), retained at D7 by the
owner's ruling when its sibling v7-cB was deleted; its supporting evidence was **cohort-mean
concentration** (2020-cohort markdown mediocrity-concentrated, Spearman +0.706 — D5 ASK2), i.e. it was
validated as a *mean-price* concentrator. **It was never validated as a quantile.** But band[5] IS a
quantile — and q97m already has age as a feature and is calibrated at every age band raw (age ≥ 22 raw
exceedance 3.7 %). The taper is a second, uncalibrated age adjustment stacked on an already-age-aware
q97, and it is what turns the printed ceiling into a ~q87 (age ≥ 22), inverts 341 board fans (301 of
them age ≥ 24), and bites hardest exactly where the owner looked: RUCK cells lose 9–19 level points at
ages 22+ (taper-bite column, `W6_out.txt`).

**The frozen q97m model (mild, specific residuals).** Overall calibrated (3.6 %), including on the
never-trained pathway classes (3.0 % on SSP/MSD/IRE/UNR/PD* vantages — it generalizes today, though
nothing enforces that). Real residuals, all visible in the cell tables: (a) productive teens — ≤19 MID
11–30 exceedance 6.7 %, grlj's cell realized 125.7 vs pred ~118 cell-mean; (b) RUCK mildly hot-side
low at 4.3–4.8 % exceedance; (c) late-arrival 0-game cells at 22+ underpredicted (22–23 ALL 0 g: 9.3 %
raw). Two training-construction facts a bake refit should address: **target right-censoring** — 13.0 %
of the 13,169 training vantages have < 5 observable forward seasons (41 % of the 2019–21 debut
cohorts), which biases learned ceilings down precisely at young-feature vantages; and **class
exclusion** — MSD (106 players) and the pickless pool classes (SSP/IRE/UNR/PDA/PDN/PDS, 283) never
train, while **149 of the 804 active rows are from those classes** and are priced by this model every
day.

## 6. Board impact bound (first-order, display of the S6-disclosed reading; not a proposal to wire)

- **Variant A — taper off** (`bb[5] = max(q97m, q90-band)`, the well-defined counterfactual): 566 rows
  move, total **+30,223 pts = +4.53 % of the board total** (666,913). Over the 341 currently-inverted
  rows: +20,448. Early-career segment (age ≤ 23, ≤ 30 games): +3,778 over 102 rows — most of the mass
  is 24+ veterans whose ceilings are currently tapered to ~40 % of their excess over the band median
  (top movers De Koning +207, Bryan +166, Samson Ryan +164 — RUCK-heavy, as the owner suspected).
- **Variant B — ceiling raised to the cell-matched realized q97** (resolved, non-thin cells only):
  +125,976 total, but **read the caveat**: an age×pos×games cell q97 is unconditional on current
  level, so on established veterans variant B mostly measures cell coarseness, not model error. Its
  honest use is the early-career segment: **+14,784 over 160 rows** (madden +41, moyle +120,
  mcandrew +104, grlj +213 via his resolved MID cell). Per-row detail: `W6_BOARD_IMPACT.json`.

## 7. RECOMMENDATION (bake-time; nothing moves now)

1. **Retire or re-derive the v7 asc taper at the next bake — this is the primary fix.** Options in
   descending preference: (a) delete the taper from bb[5] (variant A above is its exact board bound);
   (b) if the owner wants the 2020-style mediocrity concentration preserved, move that effect into the
   mean layers (WQ6 weight, or the existing form-conditioned levers) rather than bending a quantile
   that is measured calibrated without it; (c) at minimum, fix the `_nqual ≥ 1` gate (10-game season
   bar) that denies the W4 form-retention to early-career players whose evidence arrives in < 10-game
   stints — the madden profile. Any of these ends the ▼ inversions by construction.
2. **Refit q97m via `refit_q97m.py` at the same bake, with two training changes:** (i)
   censoring-aware pool — drop (or down-weight) vantages with < 3 observable forward seasons (750
   rows, 5.7 %), re-evaluate at < 5; (ii) owner ruling requested: admit MSD and the pickless pool
   classes to the q97m pool (they are priced by it; the exclusion rides the calibration-pool filter,
   and the L4 MSD exclusion is a ruled dial — this seat flags, does not decide). Expected effect is
   mild and mostly upward at productive-teen and young-ruck features; the refit is secondary to the
   taper.
3. **Neither is a live change.** Both go through the committed entry point at a bake, with the full
   re-pin + re-certification HALT chain `refit_q97m.py` already enforces.
4. **Interim display (S6/S7 layer):** S7's outcome fans remain the honest ceiling display until the
   bake. The S6 page should (a) keep the ▼ flag; (b) relabel the sixth scenario "price if the ceiling
   lands" — it is a rho-blend, not the ceiling's career value, and that mislabel is half the
   nick-madden surprise; (c) where a row's matched cell resolves, show the realized q97
   delivered-value beside the scenario price (the data is in `W6_CELLS.json`).

## 8. Honesty bounds

q97 cells are thin: every BOUND(max) is flagged `*` and never treated as an estimate; RUCK q97 cells
are frequently bounds, and madden's cell is rows-resolved but players-thin (23 players). Ground-truth
peaks are still right-censored for the youngest bands even at ≤ 2019 (their true peaks can lie beyond
2026), so measured underprediction there is a **lower** bound — the ≤ 2016 window agrees within 0.5 pts
of exceedance. The exceedance test is average-calibration; per-cell reads carry Wilson CIs in
`W6_CELLS.json`. 2026 vantages are mid-season, historical vantages end-of-season — cell matches for
the named rows inherit that seam. Cell-mean vs conditional-prediction comparisons (moyle, croft) can
disagree in either direction without the model being wrong; the per-vantage exceedance is the primary
statistic throughout.

## 9. Files

| path | what |
|---|---|
| `PREREG_W6.md` | the prereg (pushed before results) |
| `w6_ceiling.py` | the instrument (read-only; halts on any md5/control failure) |
| `W6_out.txt` | full console transcript incl. every cell table |
| `W6_CELLS.json` | all cells × both windows × both scopes, model aggregates, controls |
| `W6_VANTAGES.csv` | the 9,877-vantage table |
| `W6_NAMED.json` | the eight named rows |
| `W6_BOARD_IMPACT.json` | variants A/B per active row + totals + segment split |

Reproduce: `export PATH=/root/rl_venv312/bin:$PATH`, thread pins to 1, then
`python3 docs/evidence/order33_w6_2026-08-17/w6_ceiling.py` (~2 min; engine load dominates;
deterministic — the rerun reproduced every number).
