# PACKET S3 — DOES BEING PICKED ITSELF PREDICT? (ORDER 32, seat S3)

**Measurement only. Nothing was wired.** Prereg: `PREREG_S3.md`, committed and pushed BEFORE any
result (commit 096a339 on land/order-29). Full numeric tables: `RESULTS_S3_out.txt` /
`RESULTS_S3.json`; dataset and its validation gate: `DATASET_S3.json`, `VALIDATE_S3.txt`,
`s3_build.py`, `s3_fit.py` — all in this directory.

---

## 1. The question, and the words used

Your law prices a player as `ρ(g)·P̂ + [D(c_u)·(1−ρ) + Φ·β·ρ]·v0`. Games played (`g`) only decides
**how much the production is believed** (ρ). It never adds value of its own. Your hypothesis: *being
selectable — playing lots of games — is in itself evidence of future value, beyond the scores
produced; it thins the bust tail* (your words, re annand vs cooke, duff-tytler, murdock).

**Terms used below**

- **Focal season** — a player's first played season (k=1; his rookie year). Replications use k=2,3.
- **Surplus (S)** — his average that season minus the replacement bar of the position he played
  (KPD 65.4, KPF 63.8, MID 77.1, RUCK 75.5, SD 75.3, SF 67.9). "Fixed output" = holding S fixed.
- **Y5** — delivered board points over the NEXT five seasons (the Layer-2 career scorer's own units,
  pick 1 ≙ 3000; below-bar and unplayed seasons credit 0, never negative). Undiscounted, so entry
  age can't leak into the outcome. Y1 = next season only; Yrc = full rest of career (retired only).
- **Bust** — Y5 = 0: delivered literally nothing above replacement in the next five years.
- **Pedigree cell** — ND pick band (your tighter bands 1-10/11-20/21-30/31-40/41-64), ND>64, or the
  pool pathway (MSD, SSP, RD, ...).

**The measurement**: at fixed surplus, fixed age, fixed pedigree cell, fixed cohort year, fixed
position — does the games count of the focal season predict Y1/Y5/Yrc?

## 2. Population, window, exclusions (all counted)

Entrants 2004–2021 (the engine's own teaching window; ≥2022 is your ruled sensitivity-only tier —
552 entrants excluded by that rule). Force majeure: thomas-boyd, paddy-mccartin out; the 2013/14
whole-draft slide applied, verbatim replication of the standing ruling (2 excluded). A first season
that was never played carries no row by store law, so the k=1 sample conditions on having played at
least one game (1,129 entrants had no k=1 row — disclosed; the annand-vs-cooke question is posed
among players who played, so this is the right sample for it). 2026 is in progress and neither
serves as a focal season nor as an outcome year. Y5 requires focal year ≤ 2020 so all five outcome
years are complete.

**Scorer validation gate (prereg §3): PASS — 2650/2650 careers reproduced exactly** against
`LAYER2.json::base.obs` under the flat-14 discount (`VALIDATE_S3.txt`). Every delivered-value number
below is the engine's own valuation law, not a new one.

**Primary sample**: n = 863 rookie seasons with Y5 observable. Games: mean 8.4, sd 6.4, terciles at
≤4 / 5–10 / >10. Y5: mean 679, sd 1094, median 149, q25 2, q75 912; P(Y5=0) = 0.072. Dispersion is
enormous — every effect below should be read against that sd.

## 3. THE HEADLINE: yes — games predict, at fixed output. (H1 supported, with one honest caveat.)

Pooled spec (games + surplus + age + band + cohort + position dummies, robust SEs):

| outcome | n | pts per marginal game | se | t | 95% CI |
|---|---|---|---|---|---|
| Y1 next-1yr | 967 | **+4.6** | 0.9 | 5.2 | [2.8, 6.3] |
| Y5 next-5yr | 863 | **+21.5** | 6.3 | 3.4 | [9.0, 33.9] |
| Y5 disc-to-focal (flat-14) | 863 | +14.7 | 4.1 | 3.6 | [6.7, 22.7] |
| Yrc rest-of-career (retired only) | 666 | +36.6 | 15.0 | 2.4 | [7.3, 66.0] |
| Y5, k=1..3 pooled, cluster-by-player, prior-games controlled | 2877 | +19.6 | 3.3 | 6.0 | [13.2, 25.9] |

In money terms: a 7-game gap at the same output ≈ **+150 Y5 points** (+107 in the below-bar stratum
where the named players live) — on the order of a quarter of an MSD-RUCK v0 (448) or a fifth of a
late-first-round v0 (~700–850). Not decoration; not a fortune either.

**The caveat, in full**: the maximally strict cell spec (demeaning inside cohort-year × band ×
position cells, half the sample dropped into cells of n<3) keeps the positive sign but loses
significance on Y5 (b = +10.0, t = 1.05; Y1 b = +2.6, t = 1.90). And the per-band cuts are noisy:
ND11-20 +42 (t 2.0), ND21-30 +16, POOL +10, while ND1-10, ND31-40, ND41-64 sit at zero
(|t| ≤ 0.3 — indistinguishable from zero, not evidence of a negative). Eras agree (2004-12: +27,
t 3.1; 2013-21: +17, t 1.7) and every position group is positive. Read: **the effect is real in the
pooled population but is not sharp enough to survive slicing into 100+ tiny cells** — the prereg
falsifier (CI covering 0 AND inconsistent sign) is not met, so H1 stands.

## 4. THE SHAPE: a threshold at ~5–10 games, then saturation. (H2 supported, sharpened.)

Spline segments (Y5, knots 5/10/15): **0–5 games −84 (se 28) · 5–10 games +72 (se 24) · 10–15 +26
(se 32) · 15+ +11 (se 31)**. Raw tercile means: 342 / 587 / 1152.

The information is NOT linear in games. One to four games carry no positive signal at fixed output
(the 0–5 segment is actually negative — a handful of games looks like "tried and set aside", not
like selection). The signal lives in the **5-to-10-games step** — precisely the region where your
measured backbone already has evidence overtaking pedigree (6–10 games) — and flattens past 10–15.
Games sqrt fits nearly as well as linear overall (R² 0.273 vs 0.276; spline 0.286); the honest
summary is *threshold-then-saturating*, not linear.

## 5. THE BUST TAIL: your actual intuition, and it is the strongest result here. (H3 supported.)

P(Y5 = 0) by games tercile, below-bar output (S<0), all pedigree pooled:

| games | ≤4 | 5–10 | >10 |
|---|---|---|---|
| P(bust) | **0.14** | **0.05** | **0.02** |
| median Y5 | 23 | 140 | 473 |

The full pedigree × surplus × tercile table is in §8 — the gradient holds inside every ND band with
enough rows (e.g. ND31-40 S<0: 0.12 / 0.00 / 0.00; POOL S<0: 0.28 / 0.10 / 0.07). Logistic with the
full controls: **odds of a bust fall ×0.848 per game — a 7-game gap cuts bust odds to about a third
(×0.32)**, se on the log-odds 0.045. The de-minimis threshold variant (Y5 < 100) agrees (b −0.048,
se 0.016).

**One honest asymmetry**: in point units the quantile effects RISE with the quantile (q25 +2.1, q50
+15.8, q75 +32.6 pts/game) — the left tail is floored at zero, so tail-thinning shows up as the
probability collapse above, not as points at q25. Games at fixed output both thin the bust tail AND
predict more upside. The prereg's literal q25>q75 falsifier fails in points; the bust-probability
reading — which is the intuition you actually stated — is strongly supported.

## 6. WHAT the games are telling us (H4), and is it NEW beyond ρ? (H5 — yes.)

- **Channel split**: each focal game predicts **+1.5 future games** over the next five years
  (t = 7.1) and **+0.33 points of future per-game surplus** (t = 3.3). Selection persists AND the
  scoring improves; roughly, the future-games channel carries the larger share of the Y5 effect.
- **The new-channel test (prereg H5, the sharpest one)**: under a pure evidence-weighting story —
  ρ's channel — more games at BELOW-bar output is more proof of badness and should predict a *worse*
  career. Measured: **the games slope among below-bar rookies is +15.3 pts/game (se 6.7, t = 2.3,
  CI [2.2, 28.4], n = 780)** — positive. Coaches' repeated selection of a player who is not yet
  producing carries information the produced average does not. That is exactly your claim, and it is
  the part of the effect the current law cannot express: nothing in ρ(g)·P̂ can make 9 games at 59.8
  worth more than 2 games at 59.8 in the same cell once ρ has done its believing.

## 7. THE OPPORTUNITY CONFOUNDER — named, controlled as far as the repo's data allows

Selection is partly team context: rebuilding clubs play kids. What the repo has was searched before
the prereg: **no per-season club history and no historical ladder/team-strength data exist anywhere**
(store carries draft club and current club only). Per the brief, nothing was faked. The available
control is **draft-club × focal-year fixed effects** — exact for players still at their draft club
in year 1 (the overwhelming majority of rookies), misattributed for early movers, movement rate
unobservable, disclosed.

Result: the games coefficient is **unmoved — +21.5 → +22.3 (se 7.1) with club-season FE**. Within
the same club in the same season, the kid who got more games at the same output still delivered
more. What the FE cannot remove: within-club selection quality (the coach choosing between his own
kids is the very signal being measured — that is the hypothesis, not a confound) and moves in year
1 (unobservable; plausible direction: movers are disproportionately discards, which if anything
biases the games effect DOWN, since low-games players who moved and recovered elsewhere would mask
it). Verdict: **the effect is not a rebuilding-club artifact at the resolution this data can see.**

## 8. Full tables

`RESULTS_S3_out.txt` carries every table verbatim: the pooled and cell specs for all four outcomes,
the spline/sqrt/tercile shape fits, the complete P(bust) table by pedigree group × surplus band ×
games tercile with cell n's, the logistic and quantile fits with bootstrap CIs (B=150, seed
320317), the band/era/position stability cuts, and the FE comparison. `RESULTS_S3.json` is the
machine-readable copy.

## 9. The named five, read through the history

| player | season | cell | games tercile | historical cell says |
|---|---|---|---|---|
| kye-annand | 9g @ 59.8, MSD KPD (S −5.6) | pool, below bar | T2 | pool/below-bar cell (n=201): P(bust) 0.18, median Y5 14. His tercile's median 16; model-implied +7-game edge over a 2-game twin: **+107 Y5 pts and bust odds ×~0.32** |
| lukas-cooke | 2g @ 43.5, MSD KPD (S −21.9) | pool, below bar | T1 | same cell, T1 median 2. Two games carry no selection signal (the 0–5 segment is flat-to-negative); his price rightly rests on pedigree |
| cooper-duff-tytler | 13g @ 50.3, ND1-10 KPF (S −13.5) | top-10 pick, below bar | T3 | ND1-10/S<0 (n=128): P(bust) 0.01, median Y5 942; his tercile's median **1331 vs 456 for the T1 twin** — at pick-band top, high selection at weak output has historically been the *good* sign |
| harry-dean | 17g @ 59.7, ND1-10 KPD (S −5.7) | top-10 pick, below bar | T3 | same cell as duff-tytler, same read, with better output |
| milan-murdock | 17g @ 70.1, SSP SF (S +2.2) | pool, above bar | T3 | thin cell (n=14, named): P(bust) 0.00, same-tercile median 475 — small history, all of it benign |

Their 2026 seasons are in progress and taught nothing here; these are historical-cell reads at the
stats you quoted.

## 10. IF RULED IN — candidate forms. **AWAITING RULING; none of this is wired.**

The no-double-counting constraint governs all three: games already drive ρ, so a selection term may
only carry what §6 shows is NEW beyond ρ's channel — the below-bar-positive, threshold-shaped,
bust-thinning residual.

- **(a) A selection term inside the pedigree leg's fade** — selection as bust-tail relief on v0:
  `D(c_u) → D(c_u) · (1 + λ·σ(g_season))` with σ a saturating threshold shape (0 below ~5 games,
  rising 5–10, flat ≥10 — the measured spline, not a new free curve), capped so relief never exceeds
  the measured bust-odds gradient (×0.848/game). Rationale: the measured effect is strongest as
  tail-thinning on the *unproduced* part of the price, which is exactly the leg D governs. Cleanest
  separation from ρ: it touches only the v0 leg.
- **(b) A floor on P̂ keyed to selection** — at fixed output, high-selection seasons predict +0.33
  surplus pts/game next years: let the production projection carry a selection-informed prior,
  `P̂ → max(P̂, bar + κ·(g − g₀)₊)` with κ ≤ 0.33 and g₀ ≈ 5. Risk: this leaks into the leg ρ
  already weights — double-counting hazard is highest here; it would need the H5 residual (below-bar
  slope 15.3, not the full 21.5) as its ceiling.
- **(c) A two-argument evidence weight** `ρ(g, played-share)` — ρ rises faster when the games came
  as sustained selection (many games in one season) than as scattered singles, honouring the
  threshold shape. Smallest surgery, but weakest fidelity to the finding: it still cannot price
  selection at fixed output, only re-time belief — it captures the H2 shape but NOT the H5 channel.

Measurement's own ranking, for whatever it is worth at a ruling: (a) matches the evidence best
(tail-thinning on the unproduced leg, below-bar-positive, saturating); (b) only with the H5 ceiling;
(c) is not really this finding.

## 11. Limitations, complete list

Cell-spec attenuation (§3) — pooled controls, not saturated cells, carry the significance. Per-band
noise: three of six ND bands individually null. The k=1 sample conditions on having played ≥1 game.
Team-season control is draft-club-approximate; per-season clubs and ladder positions do not exist in
this repo. Surplus is a season average — at 1–3 games it is a noisy control, and part of the raw
games gradient at very low games may be measurement noise in S (this is exactly ρ's channel; the H5
below-bar test is the guard, and it passed). Yrc for actives is right-censored (retired-only fit
reported instead; consistent, larger point estimate). All exclusion counts are in `DATASET_S3.json::_doc`.
