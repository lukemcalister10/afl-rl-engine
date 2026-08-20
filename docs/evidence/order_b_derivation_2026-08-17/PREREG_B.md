# PREREG — ORDER B DERIVATION SEAT (read-only; authority = #334 comment 5312733761)

Pushed BEFORE any curve is derived. Rules below are fixed; any post-hoc deviation will be disclosed in
PACKET_B_DERIVATION.md as a deviation, not silently absorbed. This seat derives and previews; it wires
NOTHING. The Order B build launches only after Candidate 32 lands and re-runs the frozen procedures on
the Candidate 32 matrix (wiring spec §W).

## Inputs (hashes asserted at run time; any mismatch = HALT)
- Candidate walk-forward matrix `per_entrant_O31FFINAL.json` md5 `d97f1aee…` (supervisor scratchpad).
- Current board `cand31.json` md5 `d4e80349…` — per-row carries BOTH baselines: `cand` (Candidate 31,
  board md5 `fe6be9d6…`) and `live` (board md5 `88ce647f…`).
- W5 evidence verbatim: `docs/evidence/order33_w5_2026-08-17/{RESULTS_W5.json, w5_veteran_mark.py}`
  (ruler + cohort construction reused, not re-invented).
- W6 evidence verbatim: `docs/evidence/order33_w6_2026-08-17/W6_VANTAGES.csv` (9,877 vantages),
  `W6_BOARD_IMPACT.json` (variant-A per-row board deltas), `W6_CELLS.json`.
- S6 emit `docs/evidence/order32_s6_2026-08-17/S6_FAN_EMIT.json` (per-row b6 fans).
- Engine read-only reference: `engine/rl_after/rl_model.py` (DELTAS ~l.825, PEAK_AGE params.json,
  ×1.05 premium l.1038, LENS bal l.972, proj_from_peak l.1018). Nothing in `engine/` is executed or
  modified by this seat.

Seed 34, cluster bootstrap by player B=2000 (LP/quantile objects B=200 per Amendment A1 precedent),
90% CIs throughout, thread pins to 1, sequential runs.

## Object 1 — TALL (and RUCK-check) decline curves, FITTED
**Data**: all seasons (year ≤ 2025) of the W5 cohort's entrants (all-arm, entry ≥ 2005, force-majeure
pair excluded). Season level = `avg` with games ≥ 4 (the engine's own latest_avg floor). Position of a
season = its `bar`. Age at season t = age_draft + (t − draft_year).
**Estimator**: within-player consecutive-season level ratios L(a+1)/L(a), both seasons ≥ 4 games,
weight w = min(g_a, g_{a+1}, 22); pair classified by the EARLIER season's bar group
(TALL=KPD+KPF pooled — primary; KPD-vs-KPF split reported as a check, flag if they disagree beyond CI;
RUCK; SMALL as control only). Group-switch pairs (bar group changes across the pair) are excluded and
their share disclosed. Age steps a→a+1 for a ∈ 21..33.
**Curve**: chained F(a): F(24)=1, F(a+1)=F(a)·ratio(a). Fitted peak age = argmax F over estimable
steps. New decline deltas d(j) = F(pa*+j)/F(pa*), j ≥ 1. POST-PEAK SIDE ONLY is proposed for wiring;
the shared pre-peak rise stays (Order A adjacency); the measured rise side is reported for information.
**CIs**: cluster bootstrap by player on the chained curve (every reported F(a) and d(j) carries a CI).
**Thin cells**: a step with n < 20 pairs is NOT estimated — the curve is BOUNDED there (report the
step's raw envelope); the wired tail beyond the last n ≥ 20 step holds the last estimated annual
decline RATE flat (never shallower), flagged as extrapolation-by-rule. No smoothing through thin cells.
**Verification (closure)**: an offline stream replica of `proj_from_peak` (posval + capt_prem + REPL +
DELTAS/PEAK_AGE + flat-14% ladder, per-player lp from trailing-2 level) must first REPRODUCE the
engine's measured survivor step declines within ±3pp at each W5 step (control C-REP; failure = the
replica is unfit and the fit falls back to the analytic bound path, disclosed). Then: implied
B_new(a) = B_W5(a) × M_new(a)/M_old(a) for TALL at 28/29/30 must land inside the W5 realized CI
around 1.0 — i.e. the fitted curve must CLOSE the called bias, not halve it. RUCK: if the fitted curve
sits within CI of the engine's current tall-machinery path for RUCK, the verdict is KEEP (matches W5
"priced about right").
**Rank preservation**: Spearman(replica-corrected mark, realized R) at each age 27–31 must be ≥ the
W5 rank − 0.05; the repricing is a levels object.

## Object 2 — AGE-DYNAMIC TERMINAL DISCOUNT, FITTED
**Form**: current-age-keyed r(a), piecewise-linear (the existing `_pw_interp` machinery), with the HARD
CONSTRAINT r(a) = 0.14 for a ≤ 27 (the young end stays put; if the fit demands otherwise it is
reported but NOT proposed). Knots at 28, 29, 30, 31; flat beyond 31 (beyond-31 is unidentified by the
data — bound, not smooth). Monotone nondecreasing.
**Fit**: on the W5 survivor-linked pairs (career-complete primary, vantages ≤ 2021), with the Object-1
tall curves already applied in the replica (derivation order: curves first, discount second — the
discount absorbs only the RESIDUAL, which the W5 §6 decomposition reads as ~half survival risk), solve
the knots so the replica's step declines match the REALIZED declines at 27→28 … 30→31 (weighted least
squares, weights = inverse bootstrap variance of the realized step). 26→27 is a no-touch control (must
stay matched — the constraint r(≤27)=0.14 enforces the mechanism; verify the number).
**CIs**: refit on each of B=2000 bootstrap draws of the realized step vector → knot CIs.
**Cross-check**: the hazard arithmetic — exit share rises ~13% (≤28) → 20/22/24% (29/30/31); the
fitted knots are compared against r(a) ≈ 0.14 + Δh(a) and the agreement/disagreement reported.
**Interaction guard**: verify the fitted schedule moves NOTHING below age 28 in the replica
(byte-level: rate identical at a ≤ 27), and quantify the combined (curve+discount) implied B for TALL
at 28–31 — the combination must not overshoot below the realized CI (no over-correction).

## Object 3 — the ×1.05 TALL PREMIUM, MEASURED
Facts to publish: (i) analytic — a flat all-age multiplier CANCELS in W5's anchored B(a); its marginal
contribution to the CALLED bias profile is exactly zero (shown numerically with the replica);
(ii) level evidence — the raw prime-age (23–26) mark/realized anchors by position (TALL 2.42 vs SMALL
3.08 vs RUCK 2.64 vs pooled 2.88, from RESULTS_W5.json), with the cross-position caveats (REPL/bar/
posval-convexity confounds) stated; (iii) replica magnitude of removal (−4.76% flat on tall marks at
every age). Decision rule, fixed now: the premium is an AGE-FLAT LEVEL object; W5's instrument cannot
call it (unidentified under anchoring). If the prime-age tall anchor shows talls at-or-below the pooled
anchor, the verdict is KEEP (removing it would cut prime talls the instrument reads as not-rich, and
the called defect is closed by Objects 1–2); a re-derivation would need a cross-position level
instrument (S4/no-arb territory) — named as future work, not performed here. "The premium stays" is a
valid outcome per the mandate.

## Object 4 — the W6 TAPER, RE-DERIVED AS A QUANTILE OBJECT
**Data**: `W6_VANTAGES.csv` (age, pred_raw, b5_raw, b5_tap, asc, realized peak_fwd). The taper's own
median m is recovered exactly per vantage where asc < 0.999 via m = (b5_tap − asc·b5_raw)/(1 − asc).
**Fit**: age bands ≤19, 20–21, 22–23, 24–26, 27+. Per band, exceedance(asc′) = share of
peak_fwd > m + asc′·(b5_raw − m) over the asc′ grid 0.40…1.00 (step 0.05), Wilson 95% intervals,
B=200 bootstrap where a CI on the fitted asc′ is needed. The fitted taper asc*(band) = the asc′ that
hits the 3% target within the family asc′ ∈ (0,1]; if exceedance at asc′=1 is already ≥ 3% for a band
(the raw model is at-or-above target), the solution is the BOUNDARY asc*=1 and the finding is that no
taper in the family is calibrated — the derived object is RETIREMENT (asc ≡ 1, band[5] = max(q97m,
q90-band)), with the residual (exceedance above 3% at asc′=1) assigned to the q97m refit already ruled
to the bake (R-W6). asc′ > 1 (an inflater) is OUT of family — it would be a second age adjustment on
an age-aware quantile, the exact defect W6 called.
**Impact**: the 341 ▼ rows under the derived object (retirement ⇒ 0 by construction — re-verified from
the emit), the S6 page effect (per-row Δ from W6_BOARD_IMPACT variant A; +30,223 pts / +4.53% if
retirement), young-row reach (age < 22 band[5] movement) for the interaction check.

## Object 5 — BOARD IMPACT PREVIEW (offline, both baselines)
Per active row: preview = cand + Δ_prod + Δ_taper, where
- Δ_prod = production_pts × (ratio_both(age, pos, level) − 1), ratio_both from ONE replica call
  carrying Object 1 + Object 2 jointly (no double count); reference level = cohort-typical veteran
  level for the row's position with a [10th, 90th]-pct lp sensitivity band published; rows of every
  age/pos go through the same function (young rows naturally ratio ≈ 1).
- Δ_taper = W6 variant-A per-row dprice_A (the derived Object-4 outcome, if retirement; else recomputed
  at asc*).
Reported per row vs BOTH baselines: (preview − cand) and (preview − live). Constituency: the named
rows FIRST (Wilkie, Wright, Andrews, Battle, McKay, Curnow, Moyle, De Koning ×2, Bontempelli,
Sinclair, Merrett, plus Heeney/English as validated-clean controls), then the 38 tall 28–30 rows, then
top taper movers; full 804-row table in JSON. This is rulings-material arithmetic, not a wired board:
first-order on the production leg, stated as such.

## Object 6 — ORDER A INTERACTION CHECK
Verify and report: (i) terminal discount reach — exactly zero below age 28 (by constraint;
verified numerically); (ii) tall-curve back-propagation into YOUNG tall rows via their projection
streams' post-peak seasons — replica ratio at ages 20–26 published (expected small; if any age < 25
moves > 3% it is flagged loudly); (iii) taper retirement's young-row reach (band[5] only — the
ceiling/scenario leg, no shared object with Order A's gate-bar/played-credit/c_u/D/Φ/remix channels);
(iv) an explicit object-by-object no-overlap table against the Order A scope list of 5312733761.

## Honesty commitments
Fitted-not-tuned: every wired number traces to an estimator defined above; no hand adjustment.
CIs on every curve. Thin cells bounded, never smoothed. The replica control C-REP gates the whole
Object-1/2 pipeline. Deviations disclosed. The packet states plainly wherever an object is
UNIDENTIFIED by the available instruments (premium; r beyond 31; tall deltas beyond the last fat cell).

Files to be produced in this directory: `b1_curves.py`, `b2_discount.py`, `b3_taper.py`,
`b4_board.py`, `RESULTS_B_CURVES.json`, `RESULTS_B_DISCOUNT.json`, `RESULTS_B_TAPER.json`,
`BOARD_PREVIEW_B.json`, `PACKET_B_DERIVATION.md`.
