# ORDER 33 SEAT W5 — IS THE LATE-CAREER DECLINE RATE RIGHT?
**Read-only measurement. Prereg pushed first (PREREG_W5.md, commit dd5cd25); rules were not changed after.**
Inputs: candidate walk-forward matrix `per_entrant_O31FFINAL.json` (md5 d97f1aee…), current board `cand31.json`
(md5 d4e80349…). Ruler reused verbatim from Order 32 S4 (`docs/evidence/order32_s4_2026-08-17/s4_shootout.py`):
season value = √games-weighted points-above-bar ×21, realized remaining value R = Σ 1.14⁻ᵏ·SV over future seasons.
Cohort: all-arm entrants ≥2005, vantages 2005–2021, career-complete primary (R fully observed, retirement tail exact),
3,218 vantage rows (ages 23–31), test cells 27–31 with n = 348/287/234/167/106. Cluster bootstrap by player, B=2000,
seed 33, 90% CI. Anchored profile B(a) = (mark/realized at age a) ÷ (mark/realized at pooled ages 23–26) — scale-free;
B>1 = over-mark vs the engine's own prime-age calibration. "Called" = CI excludes 1.0.

## THE ONE-PARAGRAPH ANSWER
**In aggregate the aging curve survives its first validation.** Pooled across positions, the veteran marks at 27–31 are
statistically indistinguishable from prime-age calibration (B = 0.95 → 1.15, every CI covers 1.0), and the veteran
ordering is genuinely informative (Spearman 0.75 at 27, still 0.56 at 31). **Two specific failures are called.**
(1) **TALLS: the engine systematically over-marks veteran key-position players** — B = 1.29 / 1.34 / 1.76 at ages
28/29/30, all called, in BOTH the with-retirement-tail and survivor-only views, in both eras. A veteran tall's mark is
~30–75% richer than what talls of that age went on to deliver. (2) **The terminal step is too shallow:** at 30→31 the
engine's survivor marks decline 21%/yr while realized remaining value declines 37%/yr (Δ = +15.4pp, CI [+2.1, +31.4],
called), and the gap trends wider from 27 onward. Everything else — smalls, rucks, stars vs role players — holds
within dispersion (one thin role-tier cell excepted).

## (a) BIAS — engine mark ÷ realized remaining value, anchored at ages 23–26
Primary, full cohort (retirement tail IN). `*` = called at 90%.

| age | n | raw ratio | B(a) | 90% CI | survivor-only B(a) |
|----:|---:|---------:|-----:|:------|-------------------:|
| 27 | 348 | 2.74 | 0.95 | [0.87, 1.04] | 0.96 |
| 28 | 287 | 2.88 | 1.00 | [0.90, 1.11] | 1.00 |
| 29 | 234 | 2.94 | 1.02 | [0.88, 1.19] | 1.00 |
| 30 | 167 | 3.12 | 1.08 | [0.91, 1.32] | 1.06 |
| 31 | 106 | 3.32 | 1.15 | [0.93, 1.47] | 1.04 |

Raw ratio ≈2.7–3.3 everywhere is the engine's value unit vs the delivered-points unit (scale, also ~2.9 at prime ages);
only the anchored profile is meaningful. The drift 0.95→1.15 is real in sign but not called at cell level; it is the
same shape the RATE test then calls at the terminal step.

**By position group** (own anchors; talls = KPD+KPF, smalls = MID+SD+SF):

| age | TALL full | TALL surv | SMALL full | RUCK full |
|----:|----------:|----------:|-----------:|----------:|
| 27 | 1.18 [0.99,1.42] | **1.21*** | **0.89*** [0.81,0.97] | 0.95 |
| 28 | **1.29*** [1.09,1.55] | **1.28*** | 0.90 | 1.07 |
| 29 | **1.34*** [1.06,1.73] | **1.33*** | 0.92 | 1.08 |
| 30 | **1.76*** [1.33,2.62] | **1.66*** | 0.88 | 1.15 |
| 31 | 1.47 [0.99,3.00] | 1.41 | 1.13 | (n<20) |

- **Talls are the finding.** Over-mark called at 28/29/30 with the tail in, and at 27/28/29/30 survivor-only. Because the
  survivor-conditional B is nearly as high as the full-cohort B (1.66 vs 1.76 at 30), this is mostly a **production-decline
  mispricing, not an exit-risk mispricing**: veteran talls who keep playing still deliver ~25–40% less than their mark
  implies. Robustness peek: present in both eras (≤2015: 1.23/1.41 at 27/28; 2016+: drift to 1.41 at 30) on top of each
  era's own level tilt.
- **Smalls read mildly cheap** (B ≈ 0.88–0.92 through 30; called only at 27). The engine's veteran haircut is, if anything,
  a touch harsh on running players.
- **Rucks — "rucks age differently" is priced about right**: B 0.95–1.15, nothing called, though cells are thin (21–34).

**By output tier** (terciles of trailing 2-season delivered value): stars are clean (B 0.95–1.10, nothing called);
mid tier noisy, nothing called; role tier has one called cell (age 29 full B=3.59*, survivor 2.03*) — low-output
veterans' small marks price a future that mostly is not there, but cells are thin and denominators tiny; flag, not verdict.

## (b) RATE — survivor-linked pairs (same player marked at a and a+1)

| step | n | engine decline | realized decline | Δ (engine−realized) | 90% CI | verdict |
|-----:|---:|---------------:|-----------------:|--------------------:|:------|:--------|
| 26→27 | 340 | −18.8% | −19.8% | +0.9pp | [−5.1, +7.1] | match |
| 27→28 | 285 | −19.1% | −25.2% | +6.1pp | [−1.1, +13.4] | match |
| 28→29 | 230 | −24.3% | −30.2% | +5.9pp | [−2.7, +15.1] | match |
| 29→30 | 165 | −23.6% | −33.8% | +10.1pp | [−0.4, +22.3] | match (borderline) |
| 30→31 | 106 | −21.5% | −36.8% | **+15.4pp** | [+2.1, +31.4] | **engine shallower*** |

The measured survivor mark-decline here is 19–24%/yr — steeper than the 13–16%/yr quoted for cohort-years 8–10 in the
program brief; the difference is construction (age-linked consecutive pairs vs cohort-year all-arm means), disclosed, not
a contradiction. The realized decline steepens monotonically with age (−20 → −37%/yr); the engine's does not (it sits at
~19–24%/yr flat). By 30→31 that is a called shallowness: **the engine treats a 31-year-old's remaining value like a
30-year-old's, and the world does not.**

## (c) RANK — Spearman(mark, realized R) at fixed age
0.75 / 0.72 / 0.69 / 0.63 / 0.56 at 27/28/29/30/31 (all CIs well above 0; full table in RESULTS_W5.json). Era-stable
where both eras have cells (27: 0.74 vs 0.75). The engine orders veterans well; skill decays gracefully with age. Any
repricing should shift LEVELS, not trust in the ordering.

## Retirement handling (the crux, decomposed)
Exit share (no season after vantage) rises 12.9% → 12.9% → 20.1% → 22.2% → 23.6% across 27→31; these zero-R players are
IN the full-cohort ratios above. The decomposition says the aggregate curve absorbs this hazard adequately (full vs
survivor B nearly coincide at 27–29 and differ by ~0.05–0.11 at 30–31), i.e. the small aggregate drift at 30–31 and the
called rate gap are roughly half list-survival (the rising exit hazard the flat discount doesn't see) and half production
decline; for talls the split is ~90% production. Censored secondary (still-active at 2025, n=65/47/25 at 27/28/29,
never pooled): B = 0.77/0.64/0.62 **before crediting any of their unobserved future seasons** — today's durable veterans
are if anything under-marked, so the tall/terminal findings are not an artifact of dropping active players.

## Era stability (honesty)
The era split is the least stable cut: ≤2015 shows over-mark at 29 (B=1.36*), 2016+ shows under-mark at 27–29
(B≈0.77–0.83*). Two known confounds, disclosed: (i) the raw scale anchor differs by era (2.60 vs 3.62), and (ii) the
career-complete requirement at recent vantages retains early retirees — which inflates the 2016+ ANCHOR cells
(washed-out 23–26yos) and mechanically deflates recent-era B(a). The TALL and terminal-rate findings survive both eras;
the era-level tilts themselves should not be read as verdicts.

## Mechanism (located, read-only — engine/rl_after/rl_model.py)
The mark's future stream is `proj_from_peak` (line 1018): level path `lp·frac(age+k, PEAK_AGE[pos])` discounted at the
flat balanced rate. Four objects set the veteran mark, all predating the one-law:
1. **`DELTAS` (line 825)** — one shared fraction-of-peak table for all positions: −1/−2/−4/−6/−9% at peak+1…+5. Very
   gentle early post-peak production decline; most of the mark's decline comes from the discount ladder, not the level path.
2. **`PEAK_AGE` (params.json): {MID 25, SF 25, SD 26, KPD 27, KPF 27, RUCK 27}** — talls are assumed latest-peaking, so
   the gentle DELTAS tail is shifted ~2 years later for KPD/KPF than for smalls. A 30yo KPF is priced at 96% of peak level.
   **This is the primary driver of the called tall over-mark.**
3. **The tall stream premium (line 1037): `if g in('KPF','KPD'): prod *= 1.05`** — a flat +5% on the whole discounted
   stream at any age; compounds driver 2.
4. **The flat 14%/yr future discount (`LENS['bal']`, line 972; age-dynamic variant `RL_AGE_DISC` exists but is dial-OFF)**
   — list-survival risk is priced identically at 23 and 31, while realized exit hazard doubles (13%→24%) and realized
   survivor decline steepens to −37%/yr. **This is the driver of the called 30→31 shallowness.** (The parked V2/V4/V5
   age-dynamic ladders at lines 889–933 all end at 15–16% at 28+, the right sign but ~half the size this measurement implies
   for the terminal step; noted for the future order, not proposed here.)
   Also noted: `AGE_CURVE` (dev-projection only) carries the same late tall peak (KPD 0.91 at 30).

## Board points (current 804-row board, 666,913 cand pts; illustrative, rulings-material)
Per prereg, sized only where called (TALL, ages 28–30; correction cand×(1/B(a)−1)):
- 38 tall rows aged 28–30 carry 18,662 pts; the called bias prices them **−5,942 pts (−32%)**:
  −1,261 at 28, −1,350 at 29, −3,330 at 30. (~0.9% of the whole board, but concentrated.)
- Aggregate-view sizing is ZERO — no called bias in the pooled profile at any age.

**Named rows read through the findings** (high-cand 28–31yo veterans):
| row | age/pos | cand | read |
|-----|---------|-----:|------|
| Callum Wilkie | 30 KPD | 3,422 | largest single exposure: TALL-30 correction −1,481 |
| Peter Wright | 30 KPF | 1,522 | −659 |
| Harris Andrews | 30 KPD | 1,521 | −658 |
| Josh Battle | 28 KPD | 1,879 | −422 |
| Harry McKay | 29 KPF | 1,626 | −410 |
| Charlie Curnow | 29 KPF | 1,289 | −325 |
| Marcus Bontempelli | 31 MID | 3,677 | no called level bias for smalls/stars; but the 30→31 rate finding (+15pp too shallow) reads directly onto the board's oldest premium rows — his NEXT mark-down is the step the engine underestimates |
| Jack Sinclair | 31 SD | 3,180 | same terminal-step caution; level OK |
| Zachary Merrett | 31 MID | 2,542 | same |
| Isaac Heeney | 30 MID | 3,359 | clean: smalls/stars validated (B≈0.88–1.10, not called) |
| Timothy English | 29 RUCK | 3,289 | rucks priced about right (B 0.95–1.15, thin cells) |

## Verdicts (prereg rules)
- **BIAS**: aggregate curve NOT rejected (complete, valuable result). TALL over-mark CALLED at 28/29/30 (both views).
  SMALL under-mark called at 27 only (mild). RUCK: nothing called. Role-tier 29 flagged (thin).
- **RATE**: engine shallower CALLED at 30→31 (+15.4pp); monotone widening trend 27+.
- **RANK**: veteran ordering good (0.75→0.56), era-stable.
- **Rulings-material, no wiring proposed**: the aging machinery predates the one-law; candidate objects for a future
  order are PEAK_AGE[KPD/KPF], the ×1.05 tall stream premium, and an age-dynamic terminal discount. Any change is its
  own order with its own prereg.

Files: PREREG_W5.md · w5_veteran_mark.py · RESULTS_W5.json · this packet. Seed 33, B=2000, thread-pinned, sequential.
