# PREREG — ORDER 33 SEAT W6: THE FROZEN q97 CEILING vs REALIZED 97th-PERCENTILE OUTCOMES

Committed and pushed BEFORE any result is computed. READ-ONLY MANDATE: this seat writes only into
`docs/evidence/order33_w6_2026-08-17/`. No engine, board, law, pin or pickle is touched. The object
under review — `data/q97m.pkl` (md5 pinned `cfdc7321…` in `data/expected_boot.json`, frozen
2026-07-14 by the owner determinism ruling, commit f14710d) — is FROZEN; the deliverable is a
recommendation for a future bake-time refit via the committed entry point `refit_q97m.py`, never a
live change.

Program brief: issue #334 comment 5312369107 (ORDER 33). Motivating observations:
(a) ORDER 32 S6: 341 of 804 active rows price the q97 "ceiling" scenario BELOW scenario five;
(b) the owner's catch (2026-08-17): nick-madden (PDA RUCK, age 22, 10 games) shows a q97-scenario
price ~1,300–1,400 while S7's entry-conditioned realized 97th-percentile career outcomes for
comparable cells sit ~1,500–2,600 (RD|RUCK 2,634; RD pooled 2,086; PDA 1,543) — and a games-getting
22-year-old ruck vantage is CONDITIONED BETTER than entry, so the vantage-true q97 should sit at or
above those.

## 1. The question

Does the frozen q97 ceiling, AS CONSUMED BY THE PRICING PATH (q97m prediction -> `max(·, band q90)`
-> the v7 age-taper), systematically underpredict realized 97th-percentile outcomes for
early-career players, especially talls/rucks — and which of the two suspects (the frozen q97m model
itself vs the v7 age-taper) produces (i) the ▼ inversions and (ii) the young-tall compression?

## 2. Ground truth — vantage-conditioned realized outcomes from the store's own scoring history

**Vantage set.** Every real store player p with a mapped position group (`MA.GRP[p['pos']]`), every
as-of year Y from d0 = `debutyr(p)-1` through `min(last_season, CUTOFF)`, skipping unobservable
seasons `d0 < Y < first_observable_season()` (the engine's own T1 rule, reused). PRIMARY window
CUTOFF = 2019 (every vantage has >= 7 forward seasons observed to 2026); SENSITIVITY window
CUTOFF = 2016 (>= 10 forward seasons). No pathway is excluded from the ground-truth population —
the pricing path prices pool/MSD/pickless rows, so the ground truth must include them. A secondary
"training-pool view" restricted to q97m's own training filter (debut <= 2021, has pick or _ft,
type != MSD) is also reported, to separate "the world" from "what the model was allowed to see".

**Outcome 1 — subsequent peak production** (the model's own target quantity):
`peak_fwd = fwd_best3_from(p, Y, 2026)` — the engine's own function, verbatim. Units: season-avg
level, the same units b6/q97m emit. This is the unit-exact test of the ceiling.

**Outcome 2 — subsequent career delivered value** (what a ceiling is worth if it lands):
`dv_fwd = sum over seasons y > Y of MA.SCALE * season_raw(avg_y, bar_pos_y) * w_sqrt(games_y) /
(1 + MA.LENS['bal'])^(y - Y)` — the grace-A season-valuation formula (o26b_layer2.py
`observed_value`, `season_raw = MA.posval(X + capt_prem(X) - BARS[pos]) * 21`, `w_sqrt =
min(1, sqrt(g/10))`, BARS = REPL - REPL_DROP), discounted to the VANTAGE year (k = y - Y), no
entry-grace shift (grace is an entry-time concept; this is a vantage-time measure — stated, not
hidden). `bar_pos` from the store season row's own 'pos' via the engine's `season_bar_group` rule
(lowest-REPL member of the split), falling back to `gfut(p)`. Units: board points, the same family
as S7's grace-A fans (S7 discounts to ENTRY; this discounts to the vantage — the two are stated as
cousins, not identical).

**Cells.** age band at vantage (`cp._age_asof`) x position group x career games through vantage
(`games_through`):
  age: {<=19, 20-21, 22-23, 24-26, 27+}
  pos: {MID, SD, SF, KPD, KPF, RUCK} + TALL (KPD+KPF+RUCK pooled — rucks are known-thin) + ALL
  games: {0, 1-10, 11-30, 31-60, 61+}
Quantile estimator: linear interpolation between order statistics at index f*(n-1) (the project's
own `q()` convention, reimplemented verbatim). Levels reported: q50/q90/q97 + max.

**Resolution (declared before data is seen, S7's own rules):** level f is RESOLVED in a cell iff
n*(1-f) >= 1 — q97 needs n >= 34, q90 needs n >= 10. Unresolved level -> sample MAX flagged
BOUND(max), never smoothed, never borrowed. n < 8 (the project N_FLOOR): no fan, n/min/median/max
only. Every cell reports n and per-level resolution flags. Player-vantage rows within a cell are
NOT independent (one player contributes several vantages); per-cell we also report n_players, and
treat n_players as the honest resolution denominator wherever it is the binding one (a q97 with
n >= 34 rows but < 34 distinct players is flagged `thin_players`).

## 3. The model side — what the pricing path actually emits at those same vantages

At every vantage (p, Y), read-only, on the loaded engine (RL_O31=1, artefact md5s asserted:
rl_model.py 14000af2, rl_model_data.json cb38ef11, pvc_curve_v2.json 78ad9842, q97m.pkl =
expected_boot pin cfdc7321):
  - `pred_raw` = `q97m.predict(cp._feat(p, Y))` — the frozen model on the inference feature path
    (the pricing path's own features; the train/inference feature mismatch is documented in-engine)
  - `b` = `cond_prior_band(p, cm, Y)` (five levels); `b5_raw = max(pred_raw, b[4])` — the pre-taper
    band[5] exactly as `_b6_core` forms it
  - `b5_tap` = `b6(p, Y)[5]` — the engine's own public b6, v7 age-taper included
  - taper telemetry: asc(age), phi (the W4 form-retention), band median m = b[2].

## 4. Prereg'd comparisons

1. **Per-vantage exceedance (the calibration test).** Share of vantages with
   `peak_fwd > pred_raw`, `> b5_raw`, `> b5_tap`, per cell and overall. A calibrated 97th-percentile
   predictor exceeds ~3% of the time. Wilson 95% CI per cell. This is the PRIMARY statistic: it
   tests the model's own conditional prediction row-by-row and does not depend on cell homogeneity.
2. **Per-cell level comparison.** realized q97(peak_fwd) vs the cell mean and median of pred_raw /
   b5_raw / b5_tap. (Secondary — a cell pools heterogeneous vantages; read beside #1, not alone.)
3. **Taper decomposition.** Per cell: mean(b5_raw - b5_tap) (pure taper bite, level units), and the
   inversion count b5_tap < b[4]. CODE FACT stated up front and verified empirically on every
   vantage: `_b6_core` returns band[5] = max(pred, b[4]) >= b[4], so PRE-taper inversions are
   impossible — every ▼ inversion is attributable to the v7 taper by construction. The empirical
   check (count of b5_raw < b[4], expected exactly 0) is a control that can fail.
4. **Training-construction audit (static + measured).** From `refit_q97m.py` + the in-engine pool:
   hyperparameters (quantile loss alpha=.97, 200 trees, lr .05, min_samples_leaf=25); pool filters
   (debut <= 2021, pick/_ft required, MSD excluded); TARGET CENSORING: yy = fwd_best3_from(p,Y,2026)
   — report the share of training vantages with < 3 / < 5 fully-observed forward seasons, by debut
   cohort; REPRESENTATION: count active-board rows whose pathway (pickless pool arms, MSD) is
   excluded from the training pool entirely (nick-madden PDA pickless is one — verified from the
   store, `pick: null`, `_pickless: true`).
5. **DV side.** realized q97(dv_fwd) per cell (board points), set beside the named rows' S6 q97
   scenario prices and S7's entry-conditioned fans. Stated as a scale-cousin comparison (different
   discount anchors), used to bound "what the top 3% actually delivered from such a vantage", not
   as an exact identity.

## 5. Named rows + board impact bound (display/bake recommendation only)

Named rows: nick-madden, ned-moyle, lachlan-mcandrew, samuel-grlj + four young talls from the S6
emit's widest rows: mitchell-edwards, jordan-croft, jonty-faull, alix-tauru. Per row: b6 at 2026,
pred_raw, b5_raw, b5_tap, asc/phi, the matched vantage cell's realized q97 (both outcomes, with n
and resolution flags), and the S6 scenario prices.

Board impact bound, for all 804 S6 rows at Y=2026 (control: reproduce S6's committed b6 values
first; max |dev| reported, tolerance 1e-6 on rows where the emit and this run share context):
  - Variant A (taper off): ceiling = b5_raw. Δscenario6 via SCALE_DIST * v_at_peak in price6's own
    context (the S6 fan() transcription); Δboard_row ≈ rho * m_downstream * W6[5] * Δsix_raw[5]
    (first-order, the S6-disclosed approximation, stated as such).
  - Variant B (cell-matched refit proxy): ceiling = max(b5_raw, realized q97 level of the row's
    age x pos x games cell, resolved cells only; unresolved rows unchanged and flagged).
Report per-row deltas, totals, and the movers list. These are BOUNDS for the owner, not proposals
to wire; any actual refit goes through `refit_q97m.py` at a bake with full re-certification.

## 6. Environment / determinism

`/root/rl_venv312/bin` python; OPENBLAS/OMP/MKL/NUMEXPR/VECLIB threads = 1; PYTHONHASHSEED=0;
strictly sequential, one engine process per script run. Engine loaded read-only exactly as
`docs/evidence/order32_s6_2026-08-17/s6_emit_fan.py` does (rl_model import + _merged_recover.py
prefix exec), WITHOUT the scratch board tree (no printed prices are consumed from a board; S6's
committed emit supplies rho/m/scenario prices for the impact bound).

## 7. Honesty bounds (declared now)

- q97 cells are inherently thin: every unresolved level prints as BOUND(max) and is never treated
  as an estimate. Per-cell n and n_players always printed.
- Even at CUTOFF=2019 a 17-19yo vantage's true peak can lie beyond 2026 → `peak_fwd` is still
  right-censored for the youngest bands; this biases the GROUND TRUTH DOWN, so any measured
  underprediction is a LOWER bound on the true underprediction (and the 2016 window checks it).
- 2026 board vantages are mid-season (10 games at R14 ≠ 10 games at season end); historical
  vantages are end-of-season. Noted where cells are matched to 2026 rows.
- Exceedance compares a conditional prediction to realized draws — 3% is the calibrated target
  only on average over the feature distribution; per-cell CIs carry the noise statement.
- "The ceiling is right and the page mislabeled it" remains a valid outcome; the verdict section
  of PACKET_W6.md must state which of the four outcomes (model, taper, both, neither) the evidence
  supports, with the S6/S7 display-layer stance in the meantime.

## 8. Outputs

- `w6_ceiling.py` — the instrument (read-only; halts on any md5/control failure)
- `W6_CELLS.json` — all cells, both outcomes, both windows, model-side aggregates + controls
- `W6_VANTAGES.csv` — the per-vantage table (compact)
- `W6_NAMED.json` — the named rows
- `W6_BOARD_IMPACT.json` — variants A/B per active row + totals
- `W6_out.txt` — full console transcript
- `PACKET_W6.md` — the owner-readable packet (verdict + bake-time recommendation + interim display
  stance)
