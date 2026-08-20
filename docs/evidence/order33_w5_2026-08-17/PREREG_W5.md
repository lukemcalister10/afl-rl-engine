# ORDER 33 SEAT W5 — PREREGISTRATION (pushed BEFORE any result)

**Question.** Is the engine's late-career decline rate right? The candidate walk-forward matrix marks
still-listed survivors down ~13–16%/yr through ages ~28–30. That rate comes from inherited aging
machinery (age curves + peak machinery predating the one-law) never validated against realized
late-career delivery. Test object: players observed at ages 27–31 at historical vantages — engine
as-of remaining-value mark vs realized remaining delivered value.

**Mandate.** READ-ONLY. Measure and report; no engine/board/law changes. Any wiring is a future order.

## Inputs (frozen)
- Candidate walk-forward matrix: scratchpad `per_entrant_O31FFINAL.json`, md5 `d97f1aee4161ebcf785cd635ed095038` (2648 recs).
- Current 804-row board: scratchpad `cand31.json`, md5 `d4e80349392e52f704d1284e2cbc0298` (sizing + named rows only).
- No engine import, no store write.

## Ruler (reused verbatim from Order 32 S4, `docs/evidence/order32_s4_2026-08-17/s4_shootout.py`; no new ruler)
- Season value SV(k,t) = w_sqrt(games) × season_raw(avg, bar) with S4's constants:
  BARS {KPD 65.4, KPF 63.8, MID 77.1, RUCK 75.5, SD 75.3, SF 67.9}, S_SH 3.0,
  LCAPT (105.0, 109.5, 1.85, 1.00), w_sqrt(g)=min(1, sqrt(g/10)), ×21.
- Realized remaining value from vantage Y: R(k,Y) = Σ_{t>Y, t≤2025} 1.14^−(t−Y) · SV(k,t).
  Seasons with year>2025 or bar∉BARS skipped (S4 rules). LAST_REAL_SEASON 2025.
- Engine mark at vantage Y: vpath[i] where yrs[i]==Y (the as-of mark after observing season Y,
  pricing seasons t>Y — identical indexing to S4's vantage construction).

## Cohort rules
- Arms: S4's `arm_of` (ND teaches_curve, or pool RD/MSD/OTHERPOOL) — the all-arm window. Entry year ≥2005.
  Force-majeure exclusions: paddy-mccartin, thomas-boyd.
- Vantage years Y: 2005–2021 inclusive (≥4 observable future seasons).
- Age at vantage a = age_draft + (Y − entry year). Extract a ∈ 23–31.
  **Test cells: a = 27,28,29,30,31. Calibration anchor: pooled a = 23–26** (the engine's value unit is
  not asserted to equal delivered points; the anchor makes the AGE PROFILE of the mark/realized ratio
  scale-free).
- PRIMARY cohort: career-complete players only — (retired_now or delisted) and last_game_year ≤2025 and
  no season >2025 → R is fully observed, retirement tail exact.
  SECONDARY (disclosed, censored): still-active/incomplete rows reported separately, never pooled.
- vpath entries that are None: row skipped (counted).
- Known cell sizes (counting only, computed pre-registration): complete a=27..31 → 348/287/234/167/106.

## Metrics
**M-BIAS.** Per age cell: ratio ρ(a) = mean(mark)/mean(realized R), full cohort (retirement tail IN —
players with R=0 included). Anchored profile B(a) = ρ(a)/ρ(23–26 pooled). B(a)>1 ⇒ engine over-marks
age a relative to its own prime-age calibration; B(a)<1 ⇒ under-marks.
Splits (each with its own anchor from the same split where n permits, else global anchor, disclosed):
- position group at vantage-season bar: TALL = KPD+KPF, SMALL = MID+SD+SF, RUCK;
- output tier: terciles of trailing delivered value T2 = SV(Y)+SV(Y−1) within each age cell
  (star/mid/role);
- era of vantage: Y ≤2015 vs Y ≥2016.
**Retirement decomposition.** Same ratios on the survivor-conditional cohort (≥1 season after Y, i.e.
R>0-tail players removed... precisely: players with at least one season t>Y). Gap between full and
survivor-conditional B(a) = the list-survival component; survivor-conditional B(a) = the production
component. Also report exit share e(a) = share of marked players at age a with no season after Y.
**M-RATE.** Survivor-linked pairs (same player marked at a and a+1): engine decline
mean(M_{a+1})/mean(M_a) vs realized decline mean(R_{a+1})/mean(R_a) on the identical pairs, for steps
26→27 … 30→31. If the mark is an unbiased price of R (up to one scale constant), the two decline
rates match; engine shallower than realized ⇒ veterans over-held.
**M-RANK.** Spearman(mark, R) per age cell 27–31, full cohort; also per era.

## Inference & verdict rules
- Cluster bootstrap by player key (a player contributes multiple age cells), B=2000, seed 33,
  90% interval (5th–95th pct), thread pins on, sequential.
- Cell scored only if n≥20 (S4 rule).
- Bias at age a is CALLED only if the anchored B(a) 90% CI excludes 1.0 (per cohort view).
- "The aging curve is right" (all test-cell CIs cover 1.0 and rate deltas cover 0) is a complete result.

## Board sizing (only if bias called)
For ages with called bias in the PRIMARY full-cohort view: correction Δ_row = cand × (1/B(a) − 1)
applied to current-board rows (cand31.json) with age 27–31; report aggregate points and the top
named 28–31yo high-cand veterans read through B(a). Sizing is illustrative, rulings-material;
no wiring proposed in this seat.

## Honesty commitments
Dispersion on every headline; era stability reported; censored cohort disclosed separately;
zero-tail share reported; ratio-of-means only (no mean-of-ratios); scale caveat carried on all
unanchored ratios; mechanism localization (which aging object drives any bias) is code-reading only.
