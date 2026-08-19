# PREREG — ORDER S READ-ONLY SEAT

**Seat:** ORDER S READ-ONLY. **Date:** 2026-08-19. **Branch:** `land/order-29`.

**THIS SEAT BUILDS NO BOARD, ADDS NO DIAL, AND EDITS NO ENGINE FILE.** It measures and reports.
Nothing here is adopted, nothing lands, no pull request is opened, nothing is recommended.
The engine is loaded IN-PROCESS for READING only, thread-pinned, one run at a time.

**This file is pushed BEFORE any number in either task exists.** Everything below is a prediction and
a statement of what would falsify it.

**The other seat.** The main ORDER S seat owns the pricing tasks (recency, the compressed cap, the
LAMBDA re-solve, the mature-domain premium). This seat owns exactly the two tasks below and writes
only to `docs/evidence/order_s_readonly_2026-08-19/`.

---

## 0 · THE MECHANISM BEING MEASURED AROUND

Stated once so the predictions below have a fixed referent. Nothing in it is being changed.

For rows aged under 24 at the year being priced (`RL_O37`, ORDER P):

```
pi *= exp( -LAMBDA * A(g) * T(s_P) )
A(g) = 1 - exp(-g/G0)                        G0 = 9.890      A(0) = 0 exactly
T(s) = clip( 1 - THETA_R*(s - s0), 0, TMAX ) THETA_R = 0.65744, s0 = -2.4527, TMAX = 21.12
s_P  = games-weighted mean over PLAYED seasons of ( season avg - [ o32_gate_bar(pos, age) + PG(ln v0, class) ] )
LAMBDA = 0.174383, BETA_sat = LAMBDA*THETA_R = 0.114646
```

**Unplayed seasons are silent in `s_P`.** Non-selection is priced elsewhere: by the sitter fade
`D(c_u)` inside `pi`, by ORDER D's pick exponent `kappa`, by the tall/small factor that fades
sitting years more gently for KPD/KPF/RUCK, and by the ORDER A selection relief `sigma_sel`.

---

## 1 · T1 — THE PG LEVEL BY POSITION

### 1.1 The question

ORDER R measured the SLOPE `dPG/dln(v0)` per position and found no pair separable. It never measured
the LEVEL. This is the level companion.

At fixed entry price, is a position systematically OVER-BARRED — i.e. does the pooled bar
`own position's o32_gate_bar(pos, age) + pooled PG(ln v0, class)` sit ABOVE what that position
actually produces?

### 1.2 The construction, fixed here before any number exists

**Population.** ORDER P's own, unchanged: `op_lib.season_rows(M)` on matrix `OKRULED` — every season
with games played, at age 18-23, by an entrant from 2005 on, up to 2025, position in the ruler's six
groups, force-majeure keys excluded. ORDER P reports 5,041 seasons / 1,575 players / 58,488 games and
this seat asserts that count rather than assuming it.

**Estimator.** ORDER P's own `op_lib.Premium` — games-weighted local-linear kernel regression on
`ln(v0)`, tricube, bandwidth 0.40 in log-v0 units, isotonised by pool-adjacent-violators, fitted
per CLASS (TALL = KPD/KPF/RUCK, SMALL = MID/SD/SF). **Nothing about the estimator changes.**

**The object.** For each season row:

```
resid = season avg - [ o32_gate_bar(pos, age) + PG_pooled(ln v0, class) ]
```

reported as the GAMES-WEIGHTED MEAN of `resid` per position. Positive = under-barred (the position
produces above the pooled bar). Negative = over-barred (the position is charged against a bar its
own players do not reach).

**Price cuts.** Pooled over price; below the row's own CLASS median `v0`; above it; and the expensive
tail, defined in advance as `v0` above the class's own 90th percentile.

**Intervals.** Player-level cluster bootstrap, 2,000 draws, seed 32 — ORDER P's and ORDER R's own B
and seed. **The premium surface is REFITTED inside every draw**, on the resampled players, because
`PG` is an estimated object and a CI that held it fixed would understate the spread. Declared here so
it is not read as a choice made after seeing a result.

**Translation to price, declared in advance.** In the unclipped region the delivered slope is
`d ln(retained pedigree)/ds = LAMBDA*A(g)*THETA_R = BETA_sat*A(g)`. So a level offset of `x` points a
game translates to a proportional change in the retained pedigree leg of `exp(BETA_sat*A(g)*x) - 1`,
which at saturation (`A = 1`) is about **11.5% per point a game**. This is the formula the packet will
quote; it is written down now.

### 1.3 Predictions

- **SRO-1 (structural control).** Within each CLASS the games-weighted mean residual over ALL of that
  class's rows is approximately zero, because the pooled surface is fitted on exactly those rows.
  Predicted `|mean residual|` under 0.5 points a game for TALL and for SMALL.
  **Falsified if either class-level mean exceeds 0.5 points a game** — which would mean this seat has
  misunderstood the estimator, and it would be reported as such rather than as a finding about
  positions.
- **SRO-1b (the zero-sum note).** Because of SRO-1, any position-level offset within a class is a
  ZERO-SUM redistribution between that class's three positions, games-weighted. If MID is over-barred
  then SD and SF must be under-barred, and vice versa. Stated in advance so the result is not read as
  "everyone is over-barred", which the estimator cannot produce.
- **SRO-2 (the owner's Travaglia lead).** Predicted: at least one of the six positions has a 90% CI
  on its pooled-over-price mean residual that EXCLUDES zero. Directionally predicted: **MID positive
  (under-barred) and SF negative (over-barred)** within SMALL.
  **Falsified as a whole if all six intervals contain zero — that is a NULL and will be reported as a
  NULL, with the pooled level vindicated.** The DIRECTION is falsified separately if the signs come
  out the other way round, and a reversed sign will be printed as prominently as a confirmed one.
- **SRO-3 (where it binds).** Predicted: the position offsets are LARGER in absolute value in the
  expensive tail than below the class median, because at the expensive end the pooled fit is carried
  by whichever position holds the games there and the others ride its level.
  **Falsified if the tail offsets are no larger than the cheap-end offsets.**
- **SRO-4 (RUCK).** Predicted: the RUCK cell is not rulable — the widest interval of the six and the
  thinnest effective sample, consistent with ORDER R §1.2's degenerate RUCK bootstrap.
  **Falsified if RUCK's interval is narrower than the median position's.**

### 1.4 Reconciliation owed regardless of outcome

The packet must say, in plain words, what a LEVEL result means alongside ORDER R's SLOPE null, and
must state that level and slope are different objects that can disagree: a pooled fit can have the
right slope everywhere and the wrong origin for a given position, and the two tests do not substitute
for each other.

---

## 2 · T2 — THE SELECTION HANDOFF AUDIT

### 2.1 The question

Unplayed seasons are silent in `s_P`. Non-selection is priced only by the sitter machinery. For rows
WITH career games but NONE or almost none recent: **is non-selection priced once, twice, or not at
all — and is the combined treatment coherent?**

### 2.2 The construction, fixed here before any number exists

**Board state.** The engine loaded in-process on the ORDER P built board's own dial line
(`RL_O37=1` with ORDER K's ruled `RL_O36_*` setting, register v735), priced at `Y = 2026`. The ORDER K
state (`RL_O37` unset) is loaded separately as the comparison column. **No board is built. No engine
file is edited. No dial is added.** Every dial used already exists and is already default-or-declared.

**Instrumentation.** ORDER Q's pattern exactly: a wrapper on `_PV['blend']` that READS and then
DELEGATES, changing no arithmetic, plus direct reads of the engine's own
`rho31`, `o31_rho_base`, `o31_pi`, `o31_D`, `o31_cu`, `o31_fade_D`, `o31_pool_D`, `o31_played_units`,
`fade30b_clock`, `o35_kappa`, `o36_kappa`, `o36_kappa_at`, `o32_sigma_sel`, `o31_stall_run`,
`phi31`, `beta31`, `pv_pedigree`, `o32_age_credit`, `o37_factor`, `o37_surplus`, `day0_v0`.
The M3 double-call is handled by ORDER Q's `assemble`, not by picking one call.

**Staleness definition.** Career games `pv_games(p, 2026) > 0`, and games in the last 1, 2 and 3
seasons equal to zero — each reported separately. "Almost none" is defined in advance as **2 or fewer
games in the window**, and is reported as a separate cell, never merged with the zero cell.

**Leg attributions.** Each is a counterfactual on the engine's own recorded quantities, in board
points, on the identity ORDER Q verified to 9.1e-13:

```
price = rho*e + pi*ped + credit          pi = pi_base * f
pi_base = D_final*(1 - rho) + Phi*beta*rho
D_raw   = the schedule fade at c_u        D_kap = D_raw ** kappa        D_final = min(1, D_kap*(1 + 1.08*sigma_sel))
```

- charge: `(1 - f) * pi_base * ped`
- sitter fade, total: `f * (1 - rho) * ped * (1 - D_final)`
- of which the schedule: `f * (1 - rho) * ped * (1 - D_raw)`
- of which kappa: `f * (1 - rho) * ped * (D_raw - D_kap)`
- of which the selection relief: `f * (1 - rho) * ped * (D_kap - D_final)`
- the tall/small factor: `f * (1 - rho) * ped * (D_raw**kappa_small - D_kap)` where `kappa_small` is
  the same row's exponent computed with the TALL flag off — the engine's own `o36_kappa_at(pk, False)`.
- the evidence weight: `(exp(-LAMBDA*1.0*T) - f) * pi_base * ped` — what `A(g) < 1` saved the row.

**Matched pairs.** Stale against fresh, matched on: same class, `|career games| <= 3` apart,
`|age| <= 1` apart, same pathway (ND / pool). The match rule is written here before it is run.

**The price identity is asserted, not assumed:** the reassembled price must reproduce the engine's own
`ev(p, 2026)` on every row, and the failure tolerance is declared in advance at 1e-6 in engine
currency.

### 2.3 Predictions

- **SRO-5 (once, through D).** Predicted: staleness is priced ONCE on the great majority of stale
  rows, through `D(c_u)`, and NOT AT ALL through the ORDER P charge — because unplayed seasons are
  silent in `s_P` and `A(g)` reads CAREER games with no recency term.
  **Falsified if the charge factor `f` differs systematically between matched stale and fresh rows at
  the same career games and age** — which would mean the charge is reading staleness after all.
- **SRO-6 (a pocket where it is priced NOT AT ALL).** Predicted: a non-empty set of board rows has
  zero games in the last season and yet `D_final = 1` — because `c_u <= 1` leaves the fade schedule at
  1.0, and the charge is silent on the unplayed season. For those rows the missing season costs
  nothing anywhere.
  **Falsified if every row with zero recent games carries `D_final < 1`.**
- **SRO-7 (the token-season credit).** `o31_played_units` credits `min(1, games/2)` per season, so a
  TWO-GAME season cancels a FULL season of sitter clock. Predicted: at least one board row's `c_u` is
  reduced by a full unit by a season of two games or fewer.
  **Falsified if no board row's played-unit credit exceeds its actual share of a season.**
- **SRO-8 (the tall/small interaction).** For a stale TALL row with very few career games, predicted:
  the EVIDENCE WEIGHT `A(g)` saves more of the pedigree leg than the tall sitter factor does — i.e.
  the `A(g)` attribution exceeds the tall-factor attribution on the median such row.
  **Falsified if the tall-factor attribution is the larger of the two on the median such row.**
- **SRO-9 (priced twice, if anywhere).** The four legs named in the order are not the only objects in
  `ev()` that read non-selection. This seat has already located, by reading, three more: the D8 graded
  staleness cap and the mediocre-for-years decay gate, both of which cap the PRODUCTION leg at
  `v0_start * frac`; and the ITEM H pool-sitter cuts `H_POOLSIT` / `H_UNION`, which read
  "no games this year" directly. Predicted: at least one board row has BOTH a production-leg staleness
  cap binding AND `D_final < 1`, which is the same fact — an unplayed season — reducing two independent
  legs of the same price.
  **Falsified if no row is in that state.** Double-pricing is DEFINED here, in advance, as: one fact
  (a season not played) reducing two legs that are added together in the price identity.
  The D8 arm's counterfactual is taken by wrapping the engine's own `_staleness_grade` to return 1.0,
  which makes that arm exactly inert by its own algebra (`min(e, cap + 1.0*max(0, e - cap)) == e`) and
  changes no repository file.
- **SRO-10 (coherence).** Predicted: the combined treatment is INCOHERENT in at least one direction —
  specifically that the charge weights three-year-old evidence exactly as heavily as this season's,
  while the fade weights the same three years at full staleness. **This seat states no fix.** The
  recency fix is the other seat's S1; this is the map their fix has to be checked against.

### 2.4 What this seat will report regardless

Sample sizes for every cell, including thin ones printed as thin. Censoring: the population is board
rows at one as-of year, so nothing here is a longitudinal claim. Every limitation is printed, and
nulls are printed as nulls.

---

## 3 · WHAT THIS SEAT WILL NOT DO

- No board build, no engine edit, no new dial, no store write.
- No pull request, nothing on `main`, nothing adopted.
- No named-player target. Named rows appear only as illustrations of where the derived rule puts
  them, never as a gate on any number.
- No recommendation of a fix in either task.
