# DELIVERABLE 4 — THE CAPTAINCY PREMIUM (report-only)
**Board of record for every figure: tagged v2.9 board 81e48293 (store b0c39d78).** Workspace reproduces the
shipped numéraire panel exactly. Numéraire divisor F=1.0524. **Nothing wired, no rung chosen, no value tuned.**

## FIRST THREE LINES (guard status)
- **NO ladder rung breaches a BINDING guard.** G-COHORT stays ≤ 1.2651 at every rung (hard bound 1.30); even an
  UNCAPPED captain term (CAP→∞) gives y4 = 1.262. G-CONVEX is invariant to the captain term by construction.
- **The captaincy lever CANNOT close A-PAIRS pair 3.** Bont never passes Sanders on any rung (max Bont 3694 vs
  Sanders 3960, which is capt-invariant). Pair 3 is a base-curve problem, not a captaincy one — as the acceptance diagnosis already held.
- G-COHORT headroom (0.0399 at y4) is barely touched: the most aggressive rung tested uses ~12% of it.

## D4.1 — THE PREMIUM TODAY (verified against the supervisor's code-read)
**The term** `capt_prem(lev)` (`rl_model.py:180`): `over=max(0,lev−107.4)`, `cb=0.35·over^1.25`,
`prem=cb·18/(18+cb)` — a **saturating** premium with a **hard 18-point asymptote**. Reproduced:
`capt_prem(126.0)=7.71`, `(140)=10.84`, `(200)=15.27`, `(400)=17.27`, `(1000)=17.81`. Applied to `lev` at
**every credited forward year** inside `_proj_w4` (`_merged_recover.py:495`) and `_prod_floor_w4` (:520), and in
`rl_model` :339/:353/:543. The player's reported premium = `capt_prem(k=0 board level)` (present-year captaincy level).

**19 of the 804 board players clear the line (capt_level > 107.4)** — matches the supervisor's "19." Top of the list:

| rank | player | pos | capt_level | premium (pts) |
|---|---|---|---|---|
| 1 | Max Gawn | RUC | 125.98 | 7.71 |
| 2 | Brodie Grundy | RUC | 125.47 | 7.56 |
| 3 | Tristan Xerri | RUC | 122.65 | 6.65 |
| 4 | Zak Butters | MID | 120.85 | 6.01 |
| 5 | Isaac Heeney | MID | 120.51 | 5.88 |
| 6 | Marcus Bontempelli | MID | 119.52 | 5.50 |
| 7 | Bailey Smith | MID | 119.49 | 5.49 |
| 8 | Luke Jackson | RUC | 117.82 | 4.80 |
| … | Dawson 114.56/3.34 · Sheezel 114.52/3.32 · **Daicos 114.50/3.31** · Holmes 114.46/3.29 · Sinclair 112.18/2.17 · Merrett 111.32/1.74 · Petracca 110.19/1.18 · Davies-Uniacke 110.00/1.08 · Green 109.85/1.01 · Anderson 107.85/0.13 · Neale 107.73/0.09 | | | |

**Reproduces the directive's figures exactly:** Gawn 126.0/7.71, Bont 119.5/5.50, Daicos 114.5/3.31.

**THE SATURATION (measured):** between the best captain (Gawn, level 125.98) and the 8th-best (Jackson, 117.82)
there are **8.16 points of raw scoring but only 2.91 points of premium.** The curve damps the top exactly where
the owner says the difference-makers live. (Supervisor's 8.2 / 2.91 — confirmed.)

**Total board SCAR the term moves (numéraire, capt-on − capt-off): +6,482 over 47 movers.** Note the board-value
SCAR ≠ the premium points, because the premium is integrated over every credited forward year:

| player | premium (pts) | board SCAR | % of the player's value |
|---|---|---|---|
| **Nick Daicos** | 3.31 | **+614** | 8.01% |
| Max Gawn | 7.71 | +246 | 10.28% |
| Marcus Bontempelli | 5.50 | +231 | 6.63% |

Daicos carries the LARGEST board SCAR despite the SMALLEST of the three premiums — he is young (many highly-weighted
forward years) on a high base (7667). Gawn's premium is largest in points but he is old (few forward years) on a
small base (2393), so its SCAR is +246 (though 10.3% of his value). This is the key structural nuance: the present
premium points understate the term's value effect for the young and overstate it for the old.

**THE DEAD TWIN.** `capt_bonus(level)` (`rl_model.py:294`) is defined and **never called** anywhere in the live
engine — confirmed. It is a **non-saturating, asymptotically LINEAR** construction (a trapezoid integral of `_pcap`,
no `cb·18/(18+cb)` damping). Someone built the uncapped version and never wired it. It is a dead-code-strip candidate.

## D4.2 — THE REALIZED VALUE, OFF THE RECORD (captaincy is a SLOT good → an order statistic)
See `reports/D4_realized_ordstat.md` for the full table. Captaincy is one slot per week, so the true worth of an
elite captain is the GAP to the next-best option, not an additive per-player bonus. Measured on the walk-forward
record (top scorer per season vs 2nd/5th/10th best): the top-vs-next gap **is convex** in how far the top sits
above the field — the owner's claim is supported by the record, and the LIVE term (saturating) prices it CONCAVELY.

## D4.3 — THE SENSITIVITY LADDER (report-only; precedent = the RUC prior-cap ladder)
Ladder varies one parameter at a time off baseline (GAIN 0.35 · EXP 1.25 · CAP 18). Board figures in numéraire;
pair-3 gap measured as (Bont − Sanders)/Sanders (Sanders = 3960, capt-invariant). **No rung is chosen.**

| rung | Bont | Gawn | Daicos | top-19 total | pair-3 gap | Bont>Sanders? |
|---|---|---|---|---|---|---|
| BASELINE (0.35/1.25/18) | 3482 | 2393 | 7667 | 85,014 | −12.07% | no |
| GAIN 0.50 | 3546 | 2449 | 7823 | 86,363 | −10.84% | no |
| GAIN 0.70 | 3616 | 2503 | 7985 | 87,789 | −9.49% | no |
| GAIN 1.00 | 3694 | 2560 | 8161 | 89,409 | −8.06% | no |
| CAP 24 | 3498 | 2419 | 7721 | 85,402 | −11.71% | no |
| CAP 30 | 3507 | 2437 | 7759 | 85,662 | −11.51% | no |
| CAP 40 | 3520 | 2458 | 7803 | 85,966 | −11.22% | no |
| CAP ~∞ (999) | 3562 | 2544 | 7970 | 87,087 | −10.28% | no |
| EXP 1.40 | 3542 | 2456 | 7826 | 86,295 | −10.80% | no |
| EXP 1.60 | 3635 | 2540 | 8048 | 88,139 | −8.85% | no |
| GAIN 0.7 + CAP 30 | 3687 | 2601 | 8200 | 89,396 | −7.94% | no |

**Pair 3:** Bont starts 12.07% below Sanders and never crosses him — the largest lift tested (GAIN 1.00) narrows
the gap to −8.06% but Bont (3694) still sits below Sanders (3960). A captain boost **cannot** make Bont pass
Sanders; the gap is base-curve, not captaincy. (A magnitude picked to catch Bont would be a hand edit — not attempted.)

## D4.4 — GUARD EXPOSURE (G-COHORT recomputed per rung on the July-8 binding construction)
Baseline reproduces the ratified **1.2601 / 1.2407 / 1.1521** exactly (matrix class-sum, incurve 2004-2020,
denom=min(y1,y2)=y1=69,840). Per rung, the 1,015 capt-sensitive cohort cells are re-priced (byte-exact re-pricer,
validated max|diff|=0 vs the official matrix); the rest carry their matrix Vpath. **G-COHORT margin = 1.30 − y4.**

| rung | G-COHORT y4 | y5 | y6 | margin(y4) | breach? |
|---|---|---|---|---|---|
| BASELINE | 1.2601 | 1.2407 | 1.1521 | 0.0399 | no |
| GAIN 0.50 | 1.2615 | 1.2430 | 1.1549 | 0.0385 | no |
| GAIN 0.70 | 1.2631 | 1.2455 | 1.1580 | 0.0369 | no |
| GAIN 1.00 | 1.2651 | 1.2484 | 1.1615 | 0.0349 | no |
| CAP 24 | 1.2604 | 1.2413 | 1.1529 | 0.0396 | no |
| CAP 30 | 1.2607 | 1.2417 | 1.1534 | 0.0393 | no |
| CAP 40 | 1.2609 | 1.2421 | 1.1540 | 0.0391 | no |
| CAP ~∞ (999) | 1.2620 | 1.2437 | 1.1564 | 0.0380 | no |
| EXP 1.40 | 1.2613 | 1.2427 | 1.1546 | 0.0387 | no |
| EXP 1.60 | 1.2630 | 1.2456 | 1.1583 | 0.0370 | no |
| GAIN 0.7 + CAP 30 | 1.2646 | 1.2479 | 1.1612 | 0.0354 | no |

**Why the headroom barely moves:** the captain term lifts the y4-6 numerator (elite young survivors) but ALSO lifts
the y1-2 denominator — early-blooming rucks cross the line inside the qualifying window (e.g. Naitanui's year-2
cell moves +1,954 with the term). The two partially cancel, so even an uncapped term costs only ~0.002 of y4.
**No rung tested breaches G-COHORT.**

**Direction on the other guards (report-only):**
- **A-BONT:** UP — Bont's anchor value rises with the term (3482 → up to 3694). Helps (Bont sits further above its floor).
- **A-GAWN:** margin WIDENS — Gawn rises (2393 → up to 2601) while his comparator Briggs (2105, below the line) is
  invariant; Gawn pulls further clear (A-GAWN = "clearly above" — reinforced).
- **G-CONVEX:** **INVARIANT.** It is synth-priced; synths sit at par (< 107.4) so `capt_prem = 0` on every synth →
  the coverage metric cannot move under any capt parameter. (Confirmed by construction.)
- **G-PEAK (B1):** direction UP on the survivor peak years 4-6 (the term lifts the elite years it credits); it
  does not create a new decline, so no drop-based breach is induced. (Direction only — not fully recomputed per rung.)

## WHAT THE MEASUREMENT INFORMS (no design)
The owner's read is **supported by the code and the record**: the live term saturates exactly at the top
(2.91 premium pts across the best 8.16 raw pts), while the realized top-vs-next gap is convex. The guard that was
flagged as the risk (G-COHORT, 0.0399 headroom) is **not** actually threatened by a captain boost — the term is
self-funding across the cohort. The lever that pair-3 needs is NOT here (base curve). Whether the answer is a bigger
GAIN, a higher CAP, a convex EXP, or the order-statistic re-framing is the design decision the measurement now informs.
