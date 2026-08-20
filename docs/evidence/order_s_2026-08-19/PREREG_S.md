# PREREG S — SIX FINDINGS, MEASURED THEN PRICED

**Seat:** ORDER S. **Date:** 2026-08-19. **Branch:** `land/order-29`, worktree off `7259617`.
**Engine at the time of writing:** `engine/rl_after/_merged_recover.py` md5
`ea5c5e5e11132479f0925a9e32e6f632` — ORDER R's pin, unedited.
**Store:** `cb38ef1171dcf20aae66ebf12682be0d`.

**THIS FILE IS COMMITTED AND PUSHED BEFORE THE FIRST ENGINE EDIT.**

**THIS IS A MEASUREMENT + PRICING ORDER. NOTHING IS ADOPTED. NOTHING LANDS. NO VARIANT IS
RECOMMENDED. NO PULL REQUEST WILL BE OPENED. NOTHING WILL BE PUSHED TO `main`.**

> **SCOPE CHANGE, RECORDED ON THE PREREG BEFORE THE FIRST ENGINE EDIT (2026-08-19).** The supervisor
> re-scoped this seat on the owner's wall-clock parallelisation request: **S4 (PG level by position)
> and S6 (the selection handoff audit) are HANDED OFF to a parallel READ-ONLY seat** and are NOT
> measured here. **Their sections 4 and 6 below are left EXACTLY as written and their predictions
> stand for the record** — they were written before any measurement and are not withdrawn, they are
> simply scored by another seat. Their results live at
> `docs/evidence/order_s_readonly_2026-08-19/`. **THIS SEAT KEEPS S1, S2, S3 and S5**, and S5 keeps
> both its measurement and its conditional pricing because the pricing depends directly on the
> measurement. Nothing else in this prereg changes.

Boards this order is measured against: live `88ce647f` (never touched) · ORDER K `f3101883`
673,097 · **ORDER P `374d4e44` 666,434 (the dial-off target)** · ORDER Q A+B1 `cbbb94d4` 662,685 ·
ORDER R `R20A` `7f88f509` 664,950 · ORDER R `R20b2A` `aaab992e` 666,056.

---

## 0 · THE MECHANISM UNDER TEST, WRITTEN OUT SO THE PREDICTIONS BIND

    pi *= exp( -LAMBDA * A(g) * T(s_P) )
    A(g) = 1 - exp(-g/G0),          G0 = 9.89,        g = CAREER games
    T(s) = clip( 1 - THETA_R*(s - s0), 0, TMAX )
    s_P  = games-weighted mean over PLAYED seasons of ( season avg - [o32_gate_bar(pos,age) + PG(ln v0, class)] )
    LAMBDA   = 0.1743833036575403   SOLVED so the new charge removes the same total (101,402.7) as the old blind charge
    BETA_sat = 0.11464630061141393  MEASURED, 90% CI [0.10416359711151935, 0.1271777523096214]
    THETA_R  = BETA_sat / LAMBDA    NOT FREE
    TMAX     = 1 - THETA_R*(s_pQ - s0)   NOT FREE given the anchor percentile Q
    s0       = -2.4527 (games-weighted cohort centre),  s_p5 = -33.06133449874688

---

## 1 · S1 — RECENCY WEIGHTING IN THE SURPLUS

### 1.1 The defect, confirmed in code before this prereg was written

`o37_surplus` (engine `_merged_recover.py` ~line 3985) accumulates
`_num += _gg*(avg - bar)` and `_den += _gg` over every played season with `_x['year'] <= Y`.
**The only weight is games. A 2024 season and a 2026 season with the same games count identically.**
`o38_parts` (the FIX A decomposition) carries the same rule, so the repair inherits it.

### 1.2 What will be MEASURED, and the rule fixed here

**Question:** does the predictive value of a played season for NEXT-season production decay with the
season's age?

**Population.** The store's own history. Every (player, state-year Y) with at least one played season
at or before Y and a played season at Y+1, drawn from the ORDER K matrix `per_entrant_OKRULED.json`
plus the store, on the same bar object the charge uses (`o32_gate_bar`, reproduced by
`on_lib.bar`). Right-censored at `LAST_REAL_SEASON = 2025` for TARGETS — the 2026 in-progress season
is never a target. It may be a PREDICTOR only where a state-year is 2026, which no target uses.

**Predictand.** `d_{Y+1} = avg_{Y+1} - o32_gate_bar(pos_{Y+1}, age_{Y+1})` — the same units the
surplus is in, in AFL Fantasy points per game.

**Predictor family, ONE parameter.**

    L_w(Y) = SUM_k games_{Y-k} * w^k * d_{Y-k}   /   SUM_k games_{Y-k} * w^k        , w in (0, 1]

`w = 1` is the engine's own object exactly. Nothing else is added: no intercept beyond the fitted
one, no trajectory term, no age term in the predictor itself.

**Estimation: WALK-FORWARD, NEVER IN-SAMPLE.** For each target season `T` in 2010..2025 the
retention `w*` is chosen on states whose target year is strictly `< T`, and scored on states whose
target year is exactly `T`. The pooled out-of-sample error is the sum over `T` of the held-out
squared error at that `T`'s own `w*`. A single-`w` in-sample fit will ALSO be printed, labelled
in-sample, purely so the two can be told apart on sight.

**Reported:** the per-year `w*` path, the pooled OOS RMSE curve across the `w` grid, the OOS-optimal
`w`, the implied normalised three-season weights, and the same split by (a) seasons of history,
(b) age band, (c) position class. Games-weighted and unweighted scoring both.

**Prior art, stated and NOT copied:** ORDER 33 seat W4's measured optimum was `w* ~ 0.45-0.5`, i.e.
normalised `[0.57-0.61, 0.27-0.29, 0.12-0.14]`; the recency audit measured the ENGINE's effective
production weighting at a median `[0.745, 0.161, 0.066]`. **Neither number is used. The weights
priced here come from this order's own walk-forward fit on the surplus's own predictand.**

### 1.3 What will be PRICED

A dial `RL_O40_RECW` giving the retention `w` used inside `o37_surplus` and `o38_parts` — the SAME
number in both, so FIX A's decomposition identity `s_P(v) = OUT - wT*PG(v,TALL) - wS*PG(v,SMALL)`
survives exactly. Unset = 1.0 = ORDER P byte for byte.

### 1.4 THE SEASON-TURN AXIS — the cliff this must not create

**Structural claim, to be VERIFIED not assumed:** a pure geometric-in-years-back weight is EXACTLY
invariant to the calendar turn, because at the turn every played season's exponent `k` increases by
one, `w^(k+1) = w * w^k` uniformly, and the common factor cancels in the normalisation. The only
thing that changes at a turn is the ARRIVAL of new data. **This will be swept: every real row's
charge factor and price recomputed with all years-back incremented by one, at fixed data, and the
largest step printed.** The bar is the step ORDER P created on the 23->24 age axis, **0.4653**.

### 1.5 PREDICTIONS (S1)

- **S1-P1** The OOS-optimal `w` lies strictly inside (0.30, 0.85) — the predictive value of a season
  DOES decay, and neither a flat average nor a last-season-only read wins.
- **S1-P2** The per-year `w*` path is stable: max minus min across target years <= 0.30.
- **S1-P3** The season-turn sweep produces a largest step of **exactly 0.0000** on the charge factor
  at fixed data, because of the cancellation in 1.4.
- **S1-P4** Recency weighting MOVES ROWS BOTH WAYS and the net board effect is small in magnitude:
  `|total - RB1| < 4,000` points.
- **S1-P5** Rows whose bad seasons are OLD (the stale-evidence shape) gain; rows whose bad seasons
  are RECENT lose. The correlation between (row's price move) and (recency-weighted minus
  games-weighted surplus) is positive and above +0.8.

### 1.6 FALSIFIERS (S1) — these HALT AND REPORT

- **S1-F1** If the OOS-optimal `w >= 0.95` on the pooled criterion, **recency weighting inside the
  surplus is UNSUPPORTED by this store's own history and MUST NOT be priced.** The dial is written
  anyway and reported as unsupported; no variant is recommended either way.
- **S1-F2** If the season-turn sweep produces any step in the charge factor above `1e-9` at fixed
  data, the claimed invariance is false and the form is REJECTED as a new cliff.
- **S1-F3** If the OOS-optimal `w` differs from the in-sample optimal `w` by more than 0.20, the fit
  is overfitting the criterion and the measurement is reported as UNSTABLE, not as an optimum.

---

## 2 · S2 — THE OWNER'S COMPRESSED CAP, REPLACING THE HARD CLIP

### 2.1 The owner's spec, verbatim intent

> "what if P20 was just the floor, and everything scaled in between? So someone at P10 would still
> appear a little ahead of P5, but both would be at or above the old P20. Means everyone is lifted a
> bit, but gaps between players still count."

Formally: `T'(s)` strictly increasing in shortfall EVERYWHERE, bounded by the anchor-percentile
ceiling `C`, **never a flat segment**.

### 2.2 The form, and WHY it adds no free parameter

    T_raw(s) = max( 1 - THETA_R*(s - s0), 0 )            the UNCLIPPED charge, zero-clipped only
    C        = 1 - THETA_R*(s_pQ - s0)                   the anchor ceiling, Q in {15, 20} — the SAME
                                                          object ORDER P/R used as TMAX
    T'(s)    = C * ( 1 - exp( -T_raw(s) / C ) )          THE COMPRESSION

**Why this form and no other:**

1. `T'(0) = 0` — a row at or above the cohort centre's crossing is untouched, so the zero end of the
   scale is unmoved and `T(s0) = 1` still holds to first order.
2. `dT'/dT_raw = exp(-T_raw/C)`, which is **strictly positive for every finite `T_raw`**. There is no
   flat segment anywhere. Worse play ALWAYS costs strictly more. That is the owner's requirement,
   met exactly rather than approximately.
3. `dT'/dT_raw -> 1` as `T_raw -> 0`. **The compression agrees with the uncompressed charge to first
   order at the shallow end**, so it is not a re-scaling of the whole line — it only bends where the
   line was going to be clipped.
4. `T' -> C` as `T_raw -> infinity`, and `T' < C` everywhere. The ceiling is the p15/p20 anchor and
   is never exceeded. "Both would be at or above the old P20" is satisfied for EVERY row, because
   `T' < C = TMAX(Q)` pointwise, so every row's charge is at most the hard-clip-at-Q charge.
5. **The only quantity chosen is `C`, and `C` is the anchor percentile's `TMAX` — the same object the
   hard clip used.** Requirements 1 and 3 (value and slope matched at zero) fix the exponential's
   rate to `1/C` uniquely. **There is NO free parameter beyond the anchor percentile.**

A pure hard clip fails (2). A linear rescale `T' = T_raw * C / TMAX_p5` fails (3) and rescales rows
that were never near the cap. A power/logistic form needs a second constant. This form is the unique
one-constant family satisfying 1-4.

### 2.3 What will be PRICED

`RL_O40_CAPFORM=smooth` with `RL_O40_CAPPCT` in {15, 20}, on and off FIX A, on top of FIX B1.
Unset = ORDER P's hard clip byte for byte.

### 2.4 PREDICTIONS (S2)

- **S2-P1** The compression is SOFTER than the hard clip at the same anchor everywhere: board total
  above `R15`/`R20` respectively, and the max charge lower.
- **S2-P2** At the p20 anchor the max charge falls below **80%** of the pedigree leg (against 97.28%
  on ORDER P and 86.86% on `R20`).
- **S2-P3** The known pair reverses correctly: among heavy underperformers, the row with the WORSE
  per-game surplus is charged strictly more than the row with the better one at the same `A(g)`,
  at every surplus pair on a dense sweep — **0 of N inversions in shortfall**, against a
  hard-clip board where every pair past the crossing ties.
- **S2-P4** Relief regressivity FALLS: measured as the share of total relief (vs ORDER P) captured by
  the deepest surplus decile, the compression concentrates LESS relief in that decile than the
  hard-clip move to the same anchor does.
- **S2-P5** The W2 class mark rises relative to `R15`/`R20` and stays under 1.14.

### 2.5 FALSIFIERS (S2) — these HALT AND REPORT

- **S2-F1** If `dT'/ds < 0` fails anywhere, i.e. `T'` is not strictly increasing in shortfall on a
  dense sweep of `s`, the form is broken.
- **S2-F2** If any row is charged MORE than under ORDER P's clip at the same anchor and slope.
- **S2-F3** If the W2 class mark leaves [1.03, 1.14).
- **S2-F4** If any row prices above its uncharged price.

---

## 3 · S3 — THE LAMBDA LEVEL, RE-SOLVED AGAINST THE RAILS

### 3.1 What is being re-opened, and what is not

`LAMBDA` was SOLVED by an anchoring identity: bisection so the new charge removes exactly the same
total points (**101,402.7**) from the year-1 class-mark population as ORDER K's blind charge did.
The DISTRIBUTION was fixed by ORDER P; **the LEVEL was inherited from the defective charge and never
independently validated.** `THETA_R = BETA_sat/LAMBDA` and `TMAX` will be RECOMPUTED consistently on
every candidate `LAMBDA` (falsifier-asserted, R9/R10 style). `BETA_sat` is NOT moved here.

### 3.2 The objective and the constraint

**Objective:** close the late-band sell-side reds as far as possible — PRIMARY picks 31-40 (ORDER P
-8.88%) and 41-64 (-5.03%), MODERN 21-30 / 31-40 / 41-64.
**Constraint:** the class mark stays in **[1.03, 1.14)** on the **registered W2 basis: DRAFT classes
2005-2015, ENTRY_FLOOR 2005** — NOT `ok_class.py`'s 2004-2014 cohort-clock window. Both readings
will be printed so they can be told apart on sight, and BOTH the aggregate mark and the per-class
marks will be reported.

**If the rails and the class floor conflict, this seat HALTS AND REPORTS THE FRONTIER. It does not
pick a side.**

### 3.3 PREDICTIONS (S3)

- **S3-P1** The sell-red-closing direction is DOWN: the solved `LAMBDA` is **below** 0.1743833, and
  the implied tonnage is **below** 101,402.7. (Basis: every ORDER R softening improved every
  sell-side band; picks 31-40 went -8.88% -> -7.59%.)
- **S3-P2** The AGGREGATE W2 mark does not bind first: it has 0.0787 of room at ORDER P and rises
  with softening at roughly 0.005 per 1,000 board points, so it clears 1.14 only far past any
  plausible solve.
- **S3-P3** The PER-CLASS reading binds IMMEDIATELY and is ALREADY breached at ORDER P (draft 2010
  1.1570, 2011 1.1595, 2015 1.2047). **Under the per-class reading no `LAMBDA` in the softening
  direction is admissible, and this seat will report the frontier rather than choose.**
- **S3-P4** The late-band sell-reds do NOT close at any admissible `LAMBDA`: PRIMARY 31-40 stays
  below -4% and MODERN 41-64 stays below -20% even at `LAMBDA -> 0`. The residual sell-red is
  structural and not a tonnage fact.
- **S3-P5** Lowering `LAMBDA` at fixed `BETA_sat` RAISES `THETA_R` and RAISES `TMAX`, so it is NOT a
  pure softening: the T line steepens about `s0` even as the exponent's multiplier falls. The net
  on deep rows will be measured, not assumed.

### 3.4 FALSIFIERS (S3) — these HALT AND REPORT

- **S3-F1** `LAMBDA*THETA_R != BETA_sat` at load, to 1e-15.
- **S3-F2** `TMAX` not recomputed from the effective `THETA_R` (a stale cap carried), to 1e-12.
- **S3-F3** The aggregate W2 mark leaves [1.03, 1.14) on any priced cell.
- **S3-F4** The tonnage identity cannot be reproduced at `LAMBDA = 0.1743833` to within 0.1 points of
  101,402.7 on this seat's own re-implementation — in which case the anchor is not reproducible and
  the whole re-solve is reported as ungrounded.

---

## 4 · S4 — PG LEVEL BY POSITION (READ-ONLY)

ORDER R's null covers SLOPES only. This measures the LEVEL.

**Object:** for every season row in ORDER P's own population (games>0, age 18-23, entrant from 2005,
up to 2025), the residual

    resid = ( season avg - o32_gate_bar(pos, age) ) - PG( ln v0, class of pos )

**Reported per position:** the games-weighted mean residual, with a **player-clustered bootstrap**
CI (2,000 draws, seed 32 — ORDER P's own seed), (a) raw, and (b) **price-stratified**: within deciles
of `v0` computed on the whole population, so entry price is held fixed and composition cannot carry
the answer. Also the same on the MATURE population as a cross-read for S5.

**PREDICTIONS (S4)**
- **S4-P1** MID's mean residual is positive and SD/SF's are negative at fixed price — the owner's
  lead. Point estimates ordered MID > SD, MID > SF.
- **S4-P2** With player-clustered CIs, **at most two of the six positions have a level residual whose
  90% CI excludes zero**, and the pooled TALL and SMALL levels are within 1.5 points a game of zero.
- **S4-P3** A null is a live outcome and is reported as one.

**FALSIFIER (S4)** — **S4-F1** if the games-weighted residual mean over the WHOLE population is not
within 0.5 points a game of zero, the premium surface is not centred on its own fitting population
and every position read off it is suspect.

---

## 5 · S5 — THE PREMIUM'S DOMAIN AT 24+ (B1's WEAKNESS)

`PG` was fitted on age 18-23 seasons. FIX B1 applies it at EVERY age.

**Measured:** `PG_mature` — the identical estimator (games-weighted local-linear, tricube, h=0.40 in
log-v0, isotonised, GRID_N 121) refitted on seasons at **age >= 24** only, and a joint age-interacted
read. Compared to `PG_young` pointwise across the shared support, with player-clustered bootstrap
bands. Also reported: the premium by career stage (career games before the season) as a second axis,
because age and stage are not the same object.

**PRICED IF IT DIFFERS MATERIALLY:** `RL_O40_PGMAT` — the charge reads `PG_mature` on seasons at
24+ and `PG_young` below, games-weighted within the row exactly as the class mix already is; and
`RL_O40_PGFADE` — a premium faded toward the mature level with age. Materiality: a pointwise gap of
more than **1.0 point a game** anywhere in the 10th-90th percentile of the young cohort's `v0`.

**PREDICTIONS (S5)**
- **S5-P1** The mature premium is SHALLOWER than the young premium at the expensive end — the
  price-premium shrinks with age. Gap at `v0 = 3,000` is at least 2 points a game.
- **S5-P2** The mature population is much larger in rows than the young one, so the mature fit's ESS
  at `v0 = 3,000` exceeds the young fit's.
- **S5-P3** Pricing the mature refit REDUCES B1's mature-row cost (currently 245 rows, -6,567): the
  cost falls by more than 20%, because a shallower premium sets a LOWER bar on expensive mature rows
  and so a HIGHER surplus and a SMALLER charge.
- **S5-P4** Setterfield-shaped rows — above the AGE bar, below the PEDIGREE bar, 24+ — are the
  population that moves most. **They are watched and never targeted.**

**FALSIFIERS (S5)**
- **S5-F1** If `|PG_mature - PG_young| <= 1.0` point a game everywhere in the 10th-90th `v0`
  percentile, the domain concern is a NULL, no refit is priced, and B1's domain is reported clean.
- **S5-F2** If the mature refit is not monotone after isotonisation on its own grid.
- **S5-F3** If pricing the mature refit moves any row ABOVE its uncharged price.

---

## 6 · S6 — THE SELECTION HANDOFF AUDIT (READ-ONLY, NO BOARD)

Unplayed seasons are SILENT in `o37_surplus` — the loop `if _gg<=0.0: continue` skips them outright.
Non-selection is priced by the separate sitter machinery: `o31_cu` (the UNPLAYED clock), `o31_D` (the
fade, through ORDER D `kappa(pick)` and ORDER I's TALL/SMALL exponent), `o32_sigma_sel` (the
selection buy-back), and `o31_stall_run` -> `phi31` (the STALL conditioning, which explicitly SKIPS
gameless seasons).

**Traced end to end, on the actual board population,** for rows WITH career games but NONE recent:
is non-selection priced ONCE, TWICE, or NOT AT ALL? Quantified in board points per row and in total.

**Barnett is noted as the order names him** — RUCK, 2 games, `s_ped -44.7`, charged 49% because
`A(2) = 0.18`, and talls take the owner-ruled gentler sitter fade. **He is evidence about a shape,
never a target.**

**PREDICTIONS (S6)**
- **S6-P1** By DESIGN there is no double charge: the code comments state the no-stacking rule and the
  stall run skips gameless seasons. **Measured, the count of rows carrying both a fade below 1 and a
  stall-run charge sourced from the same unplayed seasons is ZERO.**
- **S6-P2** But the handoff is INCOMPLETE in the other direction: a row with old games and no recent
  ones has its `A(g)` fixed by CAREER games forever, so the pedigree charge NEVER decays with
  staleness, while the surplus keeps its old bad seasons at full weight. **The combined treatment is
  incoherent in level, not in double-counting.** This is what S1 addresses and the two findings will
  be reported together.
- **S6-P3** The stale-evidence population is small: fewer than 60 rows on the 804-row board have
  career games > 0 and zero games in the last two completed seasons.

**FALSIFIER (S6)** — **S6-F1** if any row is measurably charged twice for the same unplayed seasons,
that is a live defect and HALTS.

---

## 7 · STANDING REQUIREMENTS ON EVERY PRICED VARIANT

Every priced variant carries its own dial, default off. For each:

1. **dial-off byte-exact** to ORDER P `374d4e44` (and to FIX B1 `1b1817f3` / A+B1 `cbbb94d4` on the
   respective dial lines);
2. **determinism x2** — an identical repeat with the same md5;
3. **day-0 89/89** on the printed-day-0 assert, on the CAREER-games population (ORDER R's §14
   correction is carried: `cg == 0`, not season games);
4. **no row above its uncharged price**;
5. the STANDING no-arb tables — five bands plus ALL / 1-20 / 21-64, BOTH windows (PRIMARY 2005-2023,
   MODERN 2019-2023), pool arms, both baselines;
6. **the owner's loosened-rail PATH TEST on every breaching cell** — a year-1 breach is acceptable
   ONLY if (a) no year 2..7 beats carry and (b) yr7 <= yr6 AND yr7 <= carry7;
7. class marks on the registered **W2** basis plus the per-class table;
8. board total, movers vs ORDER P and vs ORDER K;
9. mature-row movement (the 429 rows aged 24+);
10. continuity including **the 23/24 age axis** and **the season-turn axis (S1)**.

**HALT AND REPORT on law breaches.** **NO NAMED-PLAYER TARGETS** — Travaglia, Pickett, Duursma,
Setterfield, Draper, Barnett and every other row inform BAND-LEVEL evidence only, and no row's value
is an acceptance criterion. **PLAIN SPEECH. MEASURED is marked MEASURED and asserted is marked
asserted. Nulls are reported as nulls. What was not built is named.**

---

## 8 · WHAT THIS ORDER WILL NOT BUILD, SAID IN ADVANCE

- **No per-position PREMIUM SPLIT.** ORDER R measured that null and the register rules it out. S4
  measures the LEVEL and reports; it builds no split.
- **No FIX B2 in any combination.** B2 is dead.
- **No re-opening of par, two-sided pedigree, or peak restoration** — owner-ruled, register v735.
- **No move of `s0`, and no move of `BETA_sat`** outside what ORDER R already priced. S3 moves
  `LAMBDA` only.
- **No refit of the young `PG` surface.** S5 adds a mature companion; it does not re-estimate the
  young object.
- **No hold-out for the premium surface.** ORDER P disclosed that it is estimated on the same board's
  `v0` it is applied to; that is unchanged here and is a standing disclosure, not a new one.
- **No adoption, no recommendation, no PR, nothing on `main`.**
