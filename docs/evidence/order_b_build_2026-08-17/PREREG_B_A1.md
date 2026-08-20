# PREREG AMENDMENT B-A1 — R-VETLEAN RE-TUNE (pushed BEFORE the re-fit)

Authority: #334 comment 5316404479 (owner rulings, the question round):
- **The flat terminal fade is DROPPED.** The shipping dial position is LADDER + TAPER, no fade. The
  fade wiring is deleted (delete-don't-disable), with an obituary; the star cut dies with it. The
  quality-conditional fade waits for the exit-hazard order.
- **R-VETLEAN (owner PREFERENCE ruling — a loss-function choice, his to make):** veteran repricing
  must LEAN OVER, NOT UNDER. The first build's tall survivor cells at 0.83 (ages 29, 31) violate it.
  The ladder is re-tuned WITHIN THE FIT'S OWN UNCERTAINTY toward B ≥ ~0.95–1.0 with the original
  over-mark calls staying dead.

## Stage re-map (code)

`RL_O33_STAGE`: 1 = tall ladder + anchor renorm s\* · 2 = +taper retirement (**the candidate,
default**). The old stage-2 fade is deleted, not disabled. Dial-off identity law unchanged.

## The re-tune rule (fixed here, before any fit is run)

- **Family and grid:** the derivation's own family ρ_j = ρ0 + g·(j−1), peak 27, KPD/KPF only,
  restricted to the fitted 90% CIs (RESULTS_B_FIT.json): ρ0 ∈ {0.000, 0.005, …, 0.080},
  g ∈ {0.0100, 0.0125, …, 0.0450}. s\* re-derived for the chosen point by the same fixed-point
  discipline (conserve the tall 23–26 anchor aggregate to <0.2%).
- **Prediction machinery (delta-space, the C-REP rule — replica for counterfactual RATIOS only):**
  predicted built cell B̂(a; ρ0,g) = B_cal(a) × [B_off(a; ρ0,g) / B_off(a; ρ0=0.030,g=0.025)], where
  B_cal(a) = the W5 tall survivor cells measured on the CALIBRATION BUILD (the original ladder in the
  new ladder+taper composition — one emit + W5 run, made first), and B_off = the offline anchored-B
  with the candidate ladder applied to tall rows (b2_fit machinery).
- **Admissible:** every scored tall survivor cell a ∈ 27..31 has B̂ ≥ **0.945** (the owner's ~0.95)
  AND B̂ ≤ **1.15** (headroom rule so no original over-mark call can resurrect; the measured
  point-to-CI-lo gaps are ≥ 0.24 in every test cell, so 1.15 cannot re-trigger a call). The BINDING
  check is the W5 harness's own calls on the final built board: the original calls (survivor
  1.21/1.28/1.33/1.66/1.41 class) must stay dead.
- **Objective among admissible:** minimize the derivation fit's own weighted closure loss
  Σ_a W_a (B̂(a) − 1)², W_a = the b2 inverse-CI weights — i.e. the admissible point closest to full
  closure. Ties → the smaller total softening (larger cumulative decline).
- **Verification and one-iteration rule:** build + emit + W5 on the chosen point. If any built cell
  lands below 0.945 by more than 0.010, or any over-mark call resurrects, ONE re-selection with the
  updated calibration is allowed and disclosed; beyond that, halt and report.
- **If the admissible set is empty:** do not force it — publish the trade-off frontier (max
  achievable min-cell vs the cells that would re-call), wire the point maximizing the minimum cell
  subject to over-marks dead, and name every cell left under 0.95. The trade-off is reported, never
  hidden.

## Re-run set

Identity rails (dial-off byte-exact vs current tree, both configs, re-run after every rebase) ·
determinism ×2 · day-0 emit guard · s\* anchor gate · rank/continuity · the standing two-sided suite
+ entry-year control (same ±1.5% bound, taper attribution expected as before) · W5 comparison
(original fit point vs softened point side by side) · ledger + both pages refreshed · packet delta in
plain language: softened ladder table, new tall-cell Bs, named-row moves vs the first build
(wilkie/mckay/andrews/battle/curnow + the star exhibits, which should now be ~0 except their taper
legs), and any cell that could not reach 0.95 without resurrecting an over-mark call.

## Predictions (scored in the delta report)

P-A1: an admissible point exists — the 29/31 under-shoots are ~0.12–0.17 below the floor and the CI
box reaches ρ0=0, so softening room exists; expected neighbourhood ρ0 ≈ 0.010–0.020, g ≈ 0.020–0.030.
P-A2: the 28-cell binds first from below (it sat 0.93–0.94 in build 1). P-A3: the 30-cell is the
over-mark risk cell (1.65 → expected to sit highest after softening) but stays uncalled under 1.15.
P-A4: star exhibits move to exactly their taper legs (+30/+28/+4 class). P-A5: entry-year yr0 cells
0.00% again; yr1 breaches remain the taper attribution set.
